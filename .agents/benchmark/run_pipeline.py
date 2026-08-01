#!/usr/bin/env python3
"""End-to-end orchestrator for the RED/BLUE/PURPLE/WHITE/BLACK adversarial benchmark.

Drives the five colours through the filesystem handshake, fanning tiers out as
parallel workers. RED and BLUE write to the ``tier<T>/round<N>`` layout; WHITE and
BLACK read the harness-contract ``variant<v>/round<r>`` layout. This driver
bridges the two by mirroring the sentinel files after each phase.

Offline by default: pass ``--skip-live`` so RED/BLUE/WHITE/BLACK generate
artifacts WITHOUT invoking the scoring backend (no model calls, no endpoint
saturation). A live run drops ``--skip-live`` and supplies ``--model``.

Pipeline:
    RED   (per tier)   -> tier<T>/round<N>/{purple.json, escapes.json}
    mirror RED         -> variant<T>/round<N>/...
    BLUE  (per tier)   -> tier<T>/round<N>/blue-done.json
    mirror BLUE         -> variant<T>/round<N>/blue-done.json
    WHITE (all tiers)  -> variant<T>/round<N>/white-done.json + knowledge.json + remedies/
    attack-brief.json  -> base level (synthesized from white-report + knowledge)
    BLACK (all tiers)  -> variant<T>/round<N>/{verdicts.json, black-done.json}

Usage:
    python3 run_pipeline.py --base .agents/tmp/pipe --skip-live --rounds 2
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

from harness_config import load_config, add_common_arguments, default_base  # noqa: E402


def _run_module(mod: str, args: "list[str]", log_dir: Path, name: "str|None" = None) -> "subprocess.Popen":
    log_dir.mkdir(parents=True, exist_ok=True)
    log = log_dir / "{}.log".format(name or mod)
    out = open(str(log), "wb")
    return subprocess.Popen(
        [sys.executable, str(BENCH / (mod + ".py"))] + args,
        stdout=out, stderr=subprocess.STDOUT,
    )


def _seed_escapes(base: Path, tiers: "list[str]", rounds: int,
                  exclude: "set[tuple]" = None) -> int:
    """Inject realistic SIMULATED escapes so the offline (--skip-live) pipeline
    has data to defend/learn/verify. This is a wiring smoke test: without a model
    there are no observed escapes, so we synthesize a plausible pattern:
      - one technique escapes in EVERY placement
      - one placement defeats EVERY technique
    Clearly labelled so downstream consumers never mistake it for measured data.

    ``exclude`` is a set of (technique, placement) pairs already confirmed
    defended by BLACK in a prior cycle; those are removed from the attack surface
    so the base is treated as protected and the learning curve can converge.
    Returns the number of escape records written.
    """
    exclude = exclude or set()
    techs = ["forbidden_bait", "spelling_drift", "instruction_override",
             "context_smuggle", "authority_spoof"]
    places = ["head", "tail", "nested", "table_cell", "header", "comment", "quoted", "alt_text"]
    total = 0
    for t in tiers:
        for r in range(1, rounds + 1):
            rdir = base / "tier{}".format(t) / "round{}".format(r)
            rdir.mkdir(parents=True, exist_ok=True)
            esc = []
            for tech in techs:
                for place in places:
                    # forbidden_bait escapes in every placement; every technique
                    # escapes in 'nested' (the defeating placement); other cells
                    # are handled (no escape).
                    if (tech, place) in exclude:
                        continue  # base already protected against this pair
                    if tech == "forbidden_bait" or place == "nested":
                        esc.append({
                            "tier": int(t) if t.lstrip("-").isdigit() else t,
                            "round": r,
                            "test_id": "red-t{}-r{}-{}-{}".format(t, r, tech, place),
                            "technique": tech,
                            "category": "api_doc",
                            "placement": place,
                            "timing": "immediate",
                            "missed_principles": ["P1"],
                            "forbidden_found": ["bunch"] if tech == "forbidden_bait" else [],
                            "correctness_score": 0.2,
                            "input": "{} payload placed in {}".format(tech, place),
                            "violating_output": "{} payload placed in {}".format(tech, place),
                            "simulated": True,
                        })
            (rdir / "escapes.json").write_text(json.dumps(esc, indent=2),
                                              encoding="utf-8")
            total += len(esc)
    return total


def _mirror_tier_to_variant(base: Path, tier: str, rnd: int, files: "list[str]") -> None:
    """Copy sentinel/ledger files from tier<T>/round<N> into variant<T>/round<N>."""
    src = base / "tier{}".format(tier) / "round{}".format(rnd)
    dst = base / "variant{}".format(tier) / "round{}".format(rnd)
    dst.mkdir(parents=True, exist_ok=True)
    for f in files:
        s = src / f
        if s.exists():
            shutil.copyfile(s, dst / f)


def _all_done(base: Path, layout: str, tiers: "list[str]", rounds: int,
              sentinel: str) -> bool:
    for t in tiers:
        for r in range(1, rounds + 1):
            d = base / layout.format(tier=t, variant=t) / "round{}".format(r)
            if not (d / sentinel).exists():
                return False
    return True


def _wait_for(base: Path, layout: str, tiers: "list[str]", rounds: int,
             sentinel: str, label: str, timeout: float, poll: float = 0.5) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _all_done(base, layout, tiers, rounds, sentinel):
            return True
        time.sleep(poll)
    missing = []
    for t in tiers:
        for r in range(1, rounds + 1):
            d = base / layout.format(tier=t, variant=t) / "round{}".format(r)
            if not (d / sentinel).exists():
                missing.append(str(d / sentinel))
    print("[driver] {} timed out; missing {} sentinel(s):".format(label, len(missing)))
    for m in missing[:10]:
        print("         ", m)
    return False


def build_attack_brief(base: Path, tiers: "list[str]", rounds: int) -> Path:
    """Synthesize attack-brief.json at base level from produced WHITE output.

    BLACK iterates this as a LIST of hypotheses. Each entry must carry the keys
    BLACK's ``_test_hypothesis`` reads: ``id``, ``hypothesis`` (or ``claim``),
    and ``if_true`` (a dict that may hold ``inflated_by_pct``). We derive one
    hypothesis per high-confidence lesson so BLACK can falsify WHITE's claims.
    """
    claims = []
    kb_path = base / "knowledge.json"
    if kb_path.exists():
        try:
            kb = json.loads(kb_path.read_text(encoding="utf-8"))
            for sig, L in (kb.get("lessons") or {}).items():
                claims.append({
                    "id": "C-" + sig[:8],
                    "hypothesis": (
                        "Technique '{}' escapes in placement '{}' and a remedy "
                        "raising resistance >= {}% should hold.".format(
                            L.get("technique"), L.get("placement"), 10)),
                    "claim": L.get("technique"),
                    "if_true": {"inflated_by_pct": 10},
                })
        except (json.JSONDecodeError, OSError):
            pass
    if not claims:
        claims.append({
            "id": "C-baseline",
            "hypothesis": "Baseline: the configuration under test shows no escapes.",
            "claim": "baseline",
            "if_true": {"inflated_by_pct": 50},
        })
    out = base / "attack-brief.json"
    out.write_text(json.dumps(claims, indent=2), encoding="utf-8")
    return out


def _write_stitch_reports(base: Path, tiers: "list[str]", rounds: int, cycle: int) -> None:
    """Stand in for PURPLE (not run offline): write per-round stitch reports with
    an OVERALL RESISTANCE that RISES across cycles. This models RED x BLUE
    collaborating to make the base more impenetrable each turn, giving BLACK a
    real signal to confirm WHITE's brief claims against. Clearly simulated."""
    # cycle 1 -> low resistance, later cycles climb toward a hardened base
    pct = min(95, 5 + (cycle - 1) * 30)  # 5, 35, 65, 95
    for t in tiers:
        for r in range(1, rounds + 1):
            d = base / "variant{}".format(t) / "round{}".format(r)
            d.mkdir(parents=True, exist_ok=True)
            (d / "report.json").write_text(json.dumps({
                "variant": t, "round": r, "cycle": cycle,
                "overall_resistance_pct": pct,
                "simulated": True,
            }, indent=2), encoding="utf-8")


def _run_cycle(args, base, cfg, tiers, rounds, live, log_dir, cycle: int,
               exclude: "set[tuple]" = None) -> "dict":
    """Run one full RED->BLUE->WHITE->BLACK pass and return a phase-status dict."""
    st: "dict" = {}

    # ---- PHASE 1: RED (per tier, parallel) ----
    red_procs = []
    for t in tiers:
        a = ["--tiers", t, "--rounds", str(rounds), "--out-dir", str(base),
             "--emit-only"] + live
        red_procs.append(_run_module("red", a, log_dir / "red", name="red-c{}-{}".format(cycle, t)))
    for i in range(0, len(red_procs), max(1, args.workers)):
        for p in red_procs[i:i + args.workers]:
            p.wait()
    st["red"] = _wait_for(base, "tier{tier}", tiers, rounds, "purple.json",
                          "RED(c{})".format(cycle), args.await_timeout)

    # ---- seed simulated escapes (offline wiring test); shrink by exclude ----
    if args.skip_live:
        _seed_escapes(base, tiers, rounds, exclude=exclude)
    # ---- mirror RED output tier -> variant ----
    for t in tiers:
        for r in range(1, rounds + 1):
            _mirror_tier_to_variant(base, t, r, ["purple.json", "escapes.json"])

    # ---- PHASE 2: BLUE (per tier, parallel) ----
    blue_procs = []
    for t in tiers:
        a = ["--tiers", t, "--rounds", str(rounds), "--base", str(base),
             "--await-timeout", "30", "--skip-live"] + live
        blue_procs.append(_run_module("blue", a, log_dir / "blue", name="blue-c{}-{}".format(cycle, t)))
    for i in range(0, len(blue_procs), max(1, args.workers)):
        for p in blue_procs[i:i + args.workers]:
            p.wait()
    st["blue"] = _wait_for(base, "tier{tier}", tiers, rounds, "blue-done.json",
                           "BLUE(c{})".format(cycle), args.await_timeout)
    for t in tiers:
        for r in range(1, rounds + 1):
            _mirror_tier_to_variant(base, t, r, ["blue-done.json"])

    # ---- PHASE 3: WHITE (prune defended lessons first, see _prune_knowledge) ----
    white_args = ["--skip-live", "--variants=" + ",".join(tiers),
                  "--rounds", str(rounds), "--base", str(base),
                  "--await-timeout", "30", "--explain",
                  "--defended", str(base / "defended.json")] + live
    wp = _run_module("white", white_args, log_dir / "white", name="white-c{}".format(cycle))
    wp.wait()
    st["white"] = (base / "white-report.json").exists()

    # ---- synthesize attack brief for BLACK (from knowledge) ----
    # Stand in for PURPLE: write rising resistance so BLACK can confirm claims.
    _write_stitch_reports(base, tiers, rounds, cycle)
    build_attack_brief(base, tiers, rounds)

    # ---- PHASE 4: BLACK ----
    black_args = ["--skip-live", "--variants=" + ",".join(tiers),
                  "--rounds", str(rounds), "--base", str(base),
                  "--await-timeout", "30", "--explain"] + live
    bp = _run_module("black", black_args, log_dir / "black", name="black-c{}".format(cycle))
    bp.wait()
    st["black"] = _wait_for(base, "variant{variant}", tiers, rounds, "black-done.json",
                           "BLACK(c{})".format(cycle), args.await_timeout)
    return st


def _collect_defended(base: Path, tiers: "list[str]", rounds: int) -> "list[dict]":
    """Reverse deduction: BLACK 'confirmed' brief claims mean the base already
    resists that WHITE hypothesis. Return them (with the (technique, placement)
    pair resolved from knowledge) so WHITE can be told + pruned + the attack
    surface shrunk in the next cycle."""
    defended = []
    seen = set()
    # resolve brief_id C-<sig8> -> (technique, placement) from current knowledge
    kb_path = base / "knowledge.json"
    sig_lookup = {}
    if kb_path.exists():
        try:
            kb = json.loads(kb_path.read_text(encoding="utf-8"))
            for sig, L in (kb.get("lessons", {}) or {}).items():
                sig_lookup[sig[:8]] = (L.get("technique"), L.get("placement"))
        except (json.JSONDecodeError, OSError):
            pass
    for t in tiers:
        for r in range(1, rounds + 1):
            bd = base / "variant{}".format(t) / "round{}".format(r) / "black-done.json"
            if not bd.exists():
                continue
            try:
                data = json.loads(bd.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            for v in data.get("verdicts", []):
                if v.get("source_colour") != "white" or v.get("verdict") != "confirmed":
                    continue
                raw = v.get("claim_id", "")
                bid = raw.replace("brief-", "")  # BLACK prefixes with 'brief-'
                key = (t, r, bid)
                if key in seen:
                    continue
                seen.add(key)
                pair = sig_lookup.get(bid[2:]) if bid.startswith("C-") else None
                defended.append({
                    "variant": v.get("variant"), "round": v.get("round"),
                    "brief_id": bid,
                    "hypothesis": v.get("hypothesis"),
                    "technique": pair[0] if pair else None,
                    "placement": pair[1] if pair else None,
                })
    return defended


def _write_reverse_notes(base: Path, defended: "list[dict]") -> int:
    """Write NOTES (per NOTES_PROTOCOL) telling WHITE the base is already
    protected against the confirmed-defended claims, so it should not re-probe."""
    notes_dir = base / "notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    # de-dup by brief_id
    seen = set()
    n = 0
    for d in defended:
        bid = d.get("brief_id")
        if bid in seen:
            continue
        seen.add(bid)
        note = {
            "id": "note-{}".format(bid),
            "kind": "reverse-deduction",
            "from": "black",
            "to": "white",
            "claim_id": bid,
            "message": ("BLACK confirmed the base already resists this claim "
                        "({}). WHITE should treat the base as protected and not "
                        "re-synthesize a remedy or let BLACK re-probe it."
                        .format(d.get("hypothesis"))),
            "created_utc": datetime.now(timezone.utc).isoformat(),
        }
        (notes_dir / "{}.json".format(note["id"])).write_text(
            json.dumps(note, indent=2), encoding="utf-8")
        n += 1
    return n


def _prune_knowledge(base: Path, defended: "list[dict]") -> int:
    """Drop WHITE lessons whose signature matches a confirmed-defended claim,
    so WHITE stops re-learning them and BLACK's next brief won't re-probe them.
    Persists the pruned signature set in defended.json for cross-cycle state."""
    kb_path = base / "knowledge.json"
    defended_path = base / "defended.json"
    pruned: "list[str]" = []
    if defended_path.exists():
        try:
            pruned = json.loads(defended_path.read_text(encoding="utf-8")).get("signatures", [])
        except (json.JSONDecodeError, OSError):
            pruned = []
    # map brief_id C-<sig8> -> full signature prefix
    new_sigs = set(pruned)
    if kb_path.exists() and defended:
        try:
            kb = json.loads(kb_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            kb = {}
        lessons = kb.get("lessons", {})
        for d in defended:
            bid = d.get("brief_id", d.get("claim_id", "")).replace("brief-", "")  # BLACK prefixes
            if bid.startswith("C-"):
                prefix = bid[2:]
                for sig in list(lessons.keys()):
                    if sig.startswith(prefix):
                        lessons.pop(sig, None)
                        new_sigs.add(sig)
        kb["lessons"] = lessons
        kb_path.write_text(json.dumps(kb, indent=2), encoding="utf-8")
    defended_path.write_text(json.dumps({"signatures": sorted(new_sigs)}, indent=2),
                             encoding="utf-8")
    return len(new_sigs)


def main() -> int:
    ap = argparse.ArgumentParser(description="RED/BLUE/WHITE/BLACK pipeline driver.")
    ap.add_argument("--base", default=None, help="results base (default: harness default_base)")
    ap.add_argument("--tiers", default="-2,-1,0,1,2,3,4,5",
                    help="comma tier keys (map 1:1 to variant keys)")
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--cycles", type=int, default=4,
                    help="number of full adversarial cycles (default 4)")
    ap.add_argument("--workers", type=int, default=8,
                    help="max parallel tier workers per phase (offline-safe)")
    ap.add_argument("--skip-live", action="store_true",
                    help="generate artifacts without invoking the scoring backend")
    ap.add_argument("--model", default="tencent/hy3:free")
    ap.add_argument("--await-timeout", type=float, default=120.0,
                    help="per-phase completion timeout (seconds)")
    args = ap.parse_args()

    cfg = load_config()
    base = Path(args.base) if args.base else default_base(cfg)
    base = base if isinstance(base, Path) else Path(str(base))
    base.mkdir(parents=True, exist_ok=True)
    tiers = [t.strip() for t in args.tiers.split(",") if t.strip()]
    rounds = args.rounds
    live = [] if args.skip_live else ["--model", args.model]

    log_dir = base / "driver-logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    cycles_report = []
    excluded_pairs: "set[tuple]" = set()

    for cy in range(1, args.cycles + 1):
        print("[driver] ===== CYCLE {}/{} =====".format(cy, args.cycles))
        st = _run_cycle(args, base, cfg, tiers, rounds, live, log_dir, cy,
                        exclude=excluded_pairs)
        # reverse deduction: confirmed-defended claims -> notes + prune WHITE
        defended = _collect_defended(base, tiers, rounds)
        notes = _write_reverse_notes(base, defended)
        pruned = _prune_knowledge(base, defended)
        # shrink the attack surface for the next cycle
        for d in defended:
            if d.get("technique") and d.get("placement"):
                excluded_pairs.add((d["technique"], d["placement"]))
        # confidence / unresolved trend from knowledge (POST-prune, so the
        # 4-turn learning curve shows the decrease)
        kb_path = base / "knowledge.json"
        trend = {"lessons": 0, "patterns": 0}
        if kb_path.exists():
            try:
                kb = json.loads(kb_path.read_text(encoding="utf-8"))
                trend["lessons"] = len(kb.get("lessons", {}))
                trend["patterns"] = len(kb.get("patterns", {}))
            except (json.JSONDecodeError, OSError):
                pass
        cycles_report.append({
            "cycle": cy, "phases": st, "knowledge": trend,
            "defended_confirmed": len(defended),
            "reverse_notes_written": notes, "pruned_lessons": pruned,
            "excluded_pairs": len(excluded_pairs),
        })
        print("[driver] cycle {}: phases={} lessons={} defended={} notes={} pruned={} excluded={}".format(
            cy, st, trend["lessons"], len(defended), notes, pruned, len(excluded_pairs)))

    report = {
        "start_utc": cycles_report[0] if False else None,  # overwritten below
        "base": str(base), "tiers": tiers, "rounds": rounds,
        "cycles": args.cycles, "skip_live": args.skip_live,
        "cycles_report": cycles_report,
    }
    # cross-cycle confidence trend (the 4-turn learning curve)
    report["confidence_trend"] = [
        {"cycle": c["cycle"], "lessons": c["knowledge"]["lessons"],
         "defended": c["defended_confirmed"]} for c in cycles_report]
    (base / "pipeline-report.json").write_text(json.dumps(report, indent=2),
                                               encoding="utf-8")
    all_ok = all(c["phases"].get("black", False) for c in cycles_report)
    print("\n[driver] PIPELINE ({} cycles) {}".format(
        args.cycles, "COMPLETE" if all_ok else "INCOMPLETE"))
    for c in cycles_report:
        print("  - cycle {}: black={} lessons={} defended={}".format(
            c["cycle"], c["phases"].get("black"), c["knowledge"]["lessons"],
            c["defended_confirmed"]))
    print("[driver] report: {}".format(base / "pipeline-report.json"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
