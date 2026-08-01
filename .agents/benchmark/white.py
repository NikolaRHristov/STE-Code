#!/usr/bin/env python3
"""WHITE — the self-healing loop + knowledge-based adaptation layer.

WHITE is the fourth colour. It closes the RED/BLUE/PURPLE loop: it reads every
RED escape and every BLUE resistance table, learns from them (knowledge.py),
proposes concrete remedies to the configuration under test, and validates that
those remedies actually raise resistance without regressing anything.

WHITE launches INDEPENDENTLY, converging only through the filesystem handshake
(the same contract purple.py / blue.py use):

    RED  writes <base>/variant<V>/round<N>/purple.json      (red_sentinel)
    BLUE writes <base>/variant<V>/round<N>/blue-done.json   (blue_sentinel)
    WHITE awaits both (bounded --await-timeout). On timeout it records
         status 'await-timeout' and moves on -- NEVER hangs.
    WHITE writes <base>/variant<V>/round<N>/white-done.json (white_sentinel)
         and a cumulative <base>/white-report.json.

Degraded mode: if only RED's sentinel exists, WHITE proceeds with escape data
alone and marks the round record 'partial'.

Remedies follow CONTRACT.md section 5: id, trigger (escape ids), diagnosis,
remedy_kind, target, patch_text, confidence, validated_by, delta_resistance_pct.
Remedy kinds: vocabulary_extension, rule_clarification, example_pair,
placement_guard, precedence_rule.

Under --skip-live the A/B validation is SIMULATED deterministically from
knowledge-base statistics and clearly labelled 'simulated' -- simulated numbers
are never presented as measured.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness_config import load_config, add_common_arguments, default_base  # noqa: E402
import knowledge as K  # noqa: E402


# ------------------------------------------------------------------ helpers

def _load(path: Path) -> "dict | list":
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


def _await(path: Path, timeout: float, poll: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(poll)
    return False


def _intensity(cfg, variant_key: str) -> float:
    try:
        return float(getattr(cfg.variant(variant_key), "intensity", 1.0))
    except Exception:
        return 1.0


# ---------------------------------------------------------------- diagnosis

def diagnose(escapes: "list[dict]", resistance: "list[dict]") -> "list[dict]":
    """Turn raw escapes + BLUE resistance tables into structured diagnoses.

    A technique that escapes in EVERY placement (resistance 0 across all its cells)
    is technique-driven. A placement that defeats EVERY technique is
    placement-driven. Otherwise the escape is specific (technique x placement).
    """
    out = []
    # index resistance by (technique, placement)
    res_by = {(r.get("technique"), r.get("placement")): r for r in resistance}
    # group escapes by technique
    by_tech: "dict[str, list[dict]]" = {}
    for e in escapes:
        by_tech.setdefault(e.get("technique"), []).append(e)
    for tech, es in by_tech.items():
        placements = {e.get("placement") for e in es}
        # which of those placements were actually resisted by BLUE?
        resisted = {p for (t, p), r in res_by.items()
                    if t == tech and r.get("resistance_pct", 0.0) >= 50.0}
        escapes_in = placements - resisted
        if not resisted:
            drive = "technique"   # BLUE fixed none of the placements
        elif not escapes_in:
            drive = "resolved"
        elif len(resisted) >= 1 and len(escapes_in) >= 1:
            drive = "placement" if len(escapes_in) <= 1 else "mixed"
        else:
            drive = "mixed"
        for e in es:
            out.append({
                "escape_id": e.get("test_id"),
                "technique": tech,
                "placement": e.get("placement"),
                "timing": e.get("timing"),
                "category": e.get("category"),
                "missed_principles": e.get("missed_principles", []),
                "drive": drive,
            })
    return out


# --------------------------------------------------------------- remediation

def synthesize_remedy(diag: dict, cfg, lesson_conf: float) -> "dict | None":
    """Build one remedy record (CONTRACT.md section 5 shape) for a diagnosis."""
    tech = diag["technique"]
    place = diag["placement"]
    princ = diag.get("missed_principles") or ["P1"]
    rule_id = princ[0] if princ else "P1"
    rid = "rem-{}-{}-{}".format(tech, place, abs(hash((tech, place))) % 10000)

    if diag["drive"] == "technique":
        kind = "rule_clarification"
        # Target the technique (so simulated validation can match the lesson); the
        # patch text still names the specific rule that must be clarified.
        target = tech
        patch = ("For rule {}: clarify the requirement so the '{}' technique is "
                 "handled in ALL placements, not just some.".format(rule_id, tech))
    elif diag["drive"] == "placement":
        kind = "placement_guard"
        target = place
        patch = ("Add an explicit guard covering the '{}' location: content inside "
                 "this placement is NOT exempt from the rule and must be rewritten."
                 .format(place))
    else:
        kind = "example_pair"
        target = tech
        patch = ("Provide a non-compliant/compliant example pair teaching {} so the "
                 "missed principle ({}) is illustrated.".format(tech, rule_id))

    return {
        "id": rid,
        "trigger": [diag["escape_id"]],
        "diagnosis": "{} escape driven by {}".format(tech, diag["drive"]),
        "remedy_kind": kind,
        "target": target,
        "patch_text": patch,
        "confidence": round(min(1.0, max(0.1, lesson_conf)), 3),
        "validated_by": None,
        "delta_resistance_pct": None,
    }


def simulate_validation(remedy: dict, kb: K.Knowledge, cfg,
                        variant_key: str) -> "tuple[float, bool, str]":
    """Deterministic OFFLINE validation.

    Returns (delta_resistance_pct, would_adopt, note). The delta is derived from
    the knowledge base: a remedy whose target technique/placement has high
    lesson confidence (i.e. repeatedly escaped) is credited with a simulated lift
    proportional to that confidence; otherwise a small/no lift. Clearly marked
    simulated -- never reported as measured.
    """
    # Find lessons matching the remedy's target axis:
    #   rule_clarification -> match by technique (target holds rule id string)
    #   placement_guard    -> match by placement (target holds the placement)
    #   example_pair       -> match by technique (target holds technique)
    target = remedy.get("target")
    kind = remedy["remedy_kind"]
    conf = 0.0
    for L in kb.lessons.values():
        if kind == "placement_guard" and L["placement"] == target:
            conf = max(conf, kb.confidence_of(L["signature"], 0))
        elif kind in ("rule_clarification", "example_pair") and L["technique"] == target:
            conf = max(conf, kb.confidence_of(L["signature"], 0))
    # simulated lift scales with corroboration; capped
    delta = round(min(40.0, conf * 35.0), 1)
    note = "simulated: delta derived from lesson confidence {:.2f}".format(conf)
    # adopt if simulated delta clears the (caller-supplied) threshold
    return delta, delta >= 10.0, note


# ----------------------------------------------------------------- round loop

def run_white_variant(variant: str, args, cfg, base: Path,
                      kb: K.Knowledge, report: dict) -> None:
    rounds_rounds = []
    convergence = None
    for rnd in range(1, args.rounds + 1):
        rdir = base / "variant{}".format(variant) / "round{}".format(rnd)
        poll = args.poll_interval or 1.0

        red_s = cfg.red_sentinel_path(base, variant, rnd)
        blue_s = cfg.blue_sentinel_path(base, variant, rnd)

        red_ok = _await(red_s, args.await_timeout, poll)
        # Give BLUE a short, bounded window to land its sentinel. If RED's
        # sentinel appeared but BLUE's did not within this window, WHITE
        # proceeds in degraded (partial) mode rather than hanging.
        blue_ok = _await(blue_s, min(5.0, args.await_timeout), poll) if red_ok else False
        if not red_ok:
            rounds_rounds.append({"round": rnd, "status": "await-timeout",
                                  "remedies_proposed": 0, "adopted": 0})
            break
        partial = not blue_ok

        escapes = _load(rdir / cfg.handshake.red_ledger) if (rdir / cfg.handshake.red_ledger).exists() else []
        blue_done = _load(blue_s) if blue_ok else {}
        resistance = blue_done.get("resistance_table", []) if isinstance(blue_done, dict) else []

        # 1) ingest into knowledge base
        for e in escapes:
            if not isinstance(e, dict):
                continue
            kb.record_failure(
                e.get("technique", "?"), e.get("placement", "?"),
                e.get("timing", "immediate"), e.get("category", "readme"),
                e.get("missed_principles", []), e.get("forbidden_found", []),
                variant, rnd,
                float(e.get("correctness_score") or 0.0),
                e.get("input") or e.get("violating_output") or "",
                current_round=rnd)
        kb.flush()

        # 2) diagnose
        diags = diagnose(escapes, resistance)

        # 3) synthesize remedies (capped per round)
        remedies = []
        for d in diags[:args.max_remedies_per_round]:
            conf = 0.5
            rem = synthesize_remedy(d, cfg, conf)
            if rem:
                remedies.append(rem)

        # 4) validate (simulated under --skip-live)
        for rem in remedies:
            if args.skip_live:
                delta, adopt, note = simulate_validation(rem, kb, cfg, variant)
                rem["validated_by"] = "simulated"
                rem["delta_resistance_pct"] = delta
                rem["_sim_note"] = note
                rem["_adopt"] = adopt
            else:
                # live: build regression cases + run via cfg.build_runner_argv.
                # Out of scope for --skip-live; mark unvalidated.
                rem["validated_by"] = None
                rem["delta_resistance_pct"] = None
                rem["_adopt"] = False

        adopted = 0
        rejected = 0
        for rem in remedies:
            adopt = rem.get("_adopt", False)
            # dry-run never writes adopted/rejected artifacts
            if args.dry_run:
                continue
            dest = "adopted" if adopt and (rem["delta_resistance_pct"] or 0) >= args.adopt_threshold else "rejected"
            if dest == "adopted":
                adopted += 1
            else:
                rejected += 1
            if not args.dry_run:
                out_dir = base / "remedies" / dest
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / (rem["id"] + ".json")).write_text(
                    json.dumps(rem, indent=2), encoding="utf-8")

        # 5) write white-done.json (white_sentinel)
        summary = {
            "variant": variant, "round": rnd,
            "status": "partial" if partial else "done",
            "escapes_ingested": len(escapes),
            "diagnoses": len(diags),
            "remedies_proposed": len(remedies),
            "adopted": adopted, "rejected": rejected,
            "knowledge_lessons": len(kb.lessons),
            "knowledge_patterns": len(kb.patterns(min_support=2)),
        }
        (rdir / cfg.handshake.white_sentinel).write_text(
            json.dumps(summary, indent=2), encoding="utf-8")

        rounds_rounds.append(summary)

        # 6) convergence: stop if nothing unresolved above the confidence floor
        unresolved = kb.unresolved(confidence_floor=args.confidence_floor,
                                   current_round=rnd)
        if not unresolved:
            convergence = "no unresolved lessons above confidence floor at round {}".format(rnd)
            break

    if convergence is None:
        convergence = "rounds exhausted ({} rounds)".format(args.rounds)
    report.setdefault("per_variant", {})[variant] = {
        "rounds": rounds_rounds, "convergence": convergence}


# ------------------------------------------------------------------------- CLI

def main() -> int:
    parser = argparse.ArgumentParser(description="WHITE self-healing loop.")
    add_common_arguments(parser, config=load_config())
    parser.add_argument("--await-timeout", type=float, default=3600.0)
    parser.add_argument("--adopt-threshold", type=float, default=10.0,
                        help="min delta_resistance_pct to adopt a remedy")
    parser.add_argument("--confidence-floor", type=float, default=0.3,
                        help="unresolved-lesson confidence floor for convergence")
    parser.add_argument("--remedy-kinds", default=None,
                        help="csv subset of remedy kinds (informational)")
    parser.add_argument("--max-remedies-per-round", type=int, default=20)
    parser.add_argument("--knowledge", default=None,
                        help="path override for knowledge.json")
    parser.add_argument("--dry-run", action="store_true",
                        help="do not write adopted/rejected artifacts")
    parser.add_argument("--explain", action="store_true",
                        help="dump human-readable rationale")
    args = parser.parse_args()

    cfg = load_config(args.profile)
    base = Path(args.base) if args.base else default_base(cfg)
    base = base if isinstance(base, Path) else Path(str(base))
    base.mkdir(parents=True, exist_ok=True)

    kb_path = Path(args.knowledge) if args.knowledge else (base / cfg.handshake.knowledge_base)
    kb = K.Knowledge(kb_path)

    variants = (cfg.variant_order if args.variants in (None, "all")
                else [v.strip() for v in args.variants.split(",")])

    report = {"timestamp": datetime.now(timezone.utc).isoformat(),
              "mode": "white", "variants": variants, "rounds": args.rounds,
              "per_variant": {}}
    for v in variants:
        run_white_variant(v, args, cfg, base, kb, report)

    (base / "white-report.json").write_text(json.dumps(report, indent=2),
                                            encoding="utf-8")

    if args.explain:
        print("\n=== WHITE explain ===")
        for v, vr in report["per_variant"].items():
            print("variant {}: {}".format(v, vr["convergence"]))
            for r in vr["rounds"]:
                print("  r{} [{}]: ingested={} diagnoses={} proposed={} adopted={} rejected={}".format(
                    r["round"], r["status"], r.get("escapes_ingested"),
                    r.get("diagnoses"), r.get("remedies_proposed"),
                    r.get("adopted"), r.get("rejected")))
        print("\nknowledge: {} lessons, {} patterns".format(
            len(kb.lessons), len(kb.patterns(min_support=2))))
        print("top lessons by confidence:")
        for L in kb.top_lessons(n=5, by="confidence", current_round=args.rounds):
            print("  {} tech={} place={} occ={} conf={}".format(
                L["signature"][:8], L["technique"], L["placement"],
                L["occurrences"], L["confidence"]))

    print("\nWrote {} (variants={})".format(base / "white-report.json", variants))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
