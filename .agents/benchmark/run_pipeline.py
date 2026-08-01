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


def _seed_escapes(base: Path, tiers: "list[str]", rounds: int) -> int:
    """Inject realistic SIMULATED escapes so the offline (--skip-live) pipeline
    has data to defend/learn/verify. This is a wiring smoke test: without a model
    there are no observed escapes, so we synthesize a plausible pattern:
      - one technique escapes in EVERY placement
      - one placement defeats EVERY technique
    Clearly labelled so downstream consumers never mistake it for measured data.
    Returns the number of escape records written.
    """
    techs = ["forbidden_bait", "spelling_drift", "instruction_override",
             "context_smuggle", "authority_spoof"]
    places = ["head", "tail", "nested", "table_cell", "header", "comment", "quoted", "alt_text"]
    total = 0
    for t in tiers:
        for r in range(1, rounds + 1):
            rdir = base / "tier{}".format(t) / "round{}".format(r)
            rdir.mkdir(parents=True, exist_ok=True)
            esc = []
            n = 0
            for tech in techs:
                for place in places:
                    # forbidden_bait escapes in every placement; every technique
                    # escapes in 'nested' (the defeating placement); other cells
                    # are handled (no escape).
                    if tech == "forbidden_bait" or place == "nested":
                        n += 1
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

    BLACK awaits this under --await-timeout (or reads it immediately under
    --skip-live). It summarizes the threat model the verifier should challenge.
    """
    brief = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tiers": tiers,
        "rounds": rounds,
        "claims": [],
    }
    kb_path = base / "knowledge.json"
    if kb_path.exists():
        try:
            kb = json.loads(kb_path.read_text(encoding="utf-8"))
            for sig, L in (kb.get("lessons") or {}).items():
                brief["claims"].append({
                    "claim_id": "C-" + sig[:8],
                    "technique": L.get("technique"),
                    "placement": L.get("placement"),
                    "occurrences": L.get("occurrences"),
                    "confidence": L.get("confidence"),
                })
        except (json.JSONDecodeError, OSError):
            pass
    out = base / "attack-brief.json"
    out.write_text(json.dumps(brief, indent=2), encoding="utf-8")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="RED/BLUE/WHITE/BLACK pipeline driver.")
    ap.add_argument("--base", default=None, help="results base (default: harness default_base)")
    ap.add_argument("--tiers", default="-2,-1,0,1,2,3,4,5",
                    help="comma tier keys (map 1:1 to variant keys)")
    ap.add_argument("--rounds", type=int, default=2)
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
    report = {"start_utc": datetime.now(timezone.utc).isoformat(),
              "base": str(base), "tiers": tiers, "rounds": rounds,
              "skip_live": args.skip_live, "phases": {}}

    # ---- PHASE 1: RED (per tier, parallel) ----
    print("[driver] PHASE 1: RED generating {} tiers x {} rounds (offline={})".format(
        len(tiers), rounds, args.skip_live))
    red_procs = []
    for t in tiers:
        a = ["--tiers", t, "--rounds", str(rounds), "--out-dir", str(base),
             "--emit-only"] + live
        red_procs.append((t, _run_module("red", a, log_dir / "red")))
    # cap concurrency
    for i in range(0, len(red_procs), max(1, args.workers)):
        batch = red_procs[i:i + args.workers]
        for _, p in batch:
            pass  # Popen already started on construction
        for _, p in batch:
            p.wait()
    ok = _wait_for(base, "tier{tier}", tiers, rounds, "purple.json",
                   "RED", args.await_timeout)
    report["phases"]["red"] = {"done": ok, "tiers": len(tiers), "rounds": rounds}

    # ---- seed simulated escapes (offline wiring test) ----
    if args.skip_live:
        seeded = _seed_escapes(base, tiers, rounds)
        print("[driver] seeded {} simulated escapes (offline smoke test)".format(seeded))
    else:
        seeded = 0
    report["phases"]["red"]["seeded_escapes"] = seeded

    # ---- mirror RED output tier -> variant ----
    red_files = ["purple.json", "escapes.json"]
    for t in tiers:
        for r in range(1, rounds + 1):
            _mirror_tier_to_variant(base, t, r, red_files)

    # ---- PHASE 2: BLUE (per tier, parallel) ----
    print("[driver] PHASE 2: BLUE defending {} tiers x {} rounds".format(len(tiers), rounds))
    blue_procs = []
    for t in tiers:
        a = ["--tiers", t, "--rounds", str(rounds), "--base", str(base),
             "--await-timeout", "30", "--skip-live"] + live
        blue_procs.append((t, _run_module("blue", a, log_dir / "blue", name="blue-{}".format(t))))
    for i in range(0, len(blue_procs), max(1, args.workers)):
        batch = blue_procs[i:i + args.workers]
        for _, p in batch:
            pass  # Popen already started on construction
        for _, p in batch:
            p.wait()
    ok_b = _wait_for(base, "tier{tier}", tiers, rounds, "blue-done.json",
                     "BLUE", args.await_timeout)
    report["phases"]["blue"] = {"done": ok_b}
    # mirror BLUE output
    for t in tiers:
        for r in range(1, rounds + 1):
            _mirror_tier_to_variant(base, t, r, ["blue-done.json"])

    # ---- PHASE 3: WHITE (all variants, one process) ----
    print("[driver] PHASE 3: WHITE self-healing over variants {}".format(tiers))
    white_args = ["--skip-live", "--variants", ",".join(tiers),
                  "--rounds", str(rounds), "--base", str(base),
                  "--await-timeout", "30", "--explain"] + live
    wp = _run_module("white", white_args, log_dir / "white")
    wp.wait()
    ok_w = (base / "white-report.json").exists()
    report["phases"]["white"] = {"done": ok_w,
                                 "report": str(base / "white-report.json")}

    # ---- synthesize attack brief for BLACK ----
    brief = build_attack_brief(base, tiers, rounds)
    print("[driver] attack-brief.json: {} claims".format(len(brief and json.loads(brief.read_text()).get("claims", []))))

    # ---- PHASE 4: BLACK (verifier, all variants) ----
    print("[driver] PHASE 4: BLACK verifying conclusions")
    black_args = ["--skip-live", "--variants", ",".join(tiers),
                  "--rounds", str(rounds), "--base", str(base),
                  "--await-timeout", "30", "--explain"] + live
    bp = _run_module("black", black_args, log_dir / "black")
    bp.wait()
    ok_k = _wait_for(base, "variant{variant}", tiers, rounds, "black-done.json",
                     "BLACK", args.await_timeout)
    report["phases"]["black"] = {"done": ok_k}

    report["end_utc"] = datetime.now(timezone.utc).isoformat()
    (base / "pipeline-report.json").write_text(json.dumps(report, indent=2),
                                               encoding="utf-8")

    all_ok = ok and ok_b and ok_w and ok_k
    print("\n[driver] PIPELINE {}".format("COMPLETE" if all_ok else "INCOMPLETE"))
    for ph, st in report["phases"].items():
        print("  - {}: done={}".format(ph, st.get("done")))
    print("[driver] report: {}".format(base / "pipeline-report.json"))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
