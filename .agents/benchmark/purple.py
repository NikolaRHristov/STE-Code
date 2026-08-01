#!/usr/bin/env python3
"""RED/BLUE adversarial benchmark for STE-Code — independent launches, stitched later.

The two sides are DECOUPLED so they can be launched in parallel and converged
at stitch time:

  RED  (--mode red)   generates adversarial inputs engineered to violate rules,
                      runs them against each tier prompt, and writes a LEDGER
                      (escapes.json) per tier/round. Emits a red-done.json
                      sentinel when a round's RED run finishes.

  BLUE (--mode blue)  launches INDEPENDENTLY and IMMEDIATELY. For each tier/round
                      it AWAITS RED's PURPLE HANDSHAKE (tests/redblue/<tier>/roundN/
                      purple.json — a filesystem signal, NOT a process dependency)
                      up to --await-timeout. Once RED's ledger lands, BLUE builds
                      targeted PROBES from the escapes and re-runs the SAME tier
                      prompt against them. Writes blue-done.json.

  STITCH (--mode both, or redblue_stitch.py) merges the per-tier/round
                      red-done.json / blue-done.json / escapes.json into one
                      report.json with the full interplay matrix (which schematic
                      escaped, BLUE resistance per round, residuals).

Why await-a-file and not a pipe: RED and BLUE are separate background processes
(subprocess / Hermes background / different machines even). BLUE just polls
tests/redblue/<tier>/roundN/red-done.json; if it never appears (RED crashed or
found 0 escapes and stopped), BLUE times out that round and moves on — no hang.

Deterministic RED (adversarial.py, no LLM). BLUE uses the same model as RED.
Run a mock 'hermes' on PATH for fast verification.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
BENCH = PROJECT / ".agents" / "benchmark"
ORCH = BENCH / "orchestrator.py"
TIER_DIR = {t: (PROJECT / "ste-code" / "artifacts" / f"level{t}" / "system-prompt.txt")
            for t in (-2, -1, 0, 1, 2, 3, 4, 5)}

sys.path.insert(0, str(BENCH))
import adversarial as _adv  # noqa: E402
from harness_config import load_config, resolve_base  # noqa: E402


def _run_orchestrator(test_dir: Path, sp: Path, results_dir: Path,
                      model: str, max_workers: int, timeout: int) -> dict | None:
    results_dir.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(ORCH),
                        "--test-dir", str(test_dir),
                        "--system-prompt-file", str(sp),
                        "--results-dir", str(results_dir),
                        "--max-workers", str(max_workers),
                        "--timeout", str(timeout), "--poll-interval", "1",
                        "--model", model],
                       cwd=str(PROJECT), capture_output=True, text=True,
                       timeout=60 * 60)
    runs = sorted(results_dir.glob("run-*"))
    if not runs:
        return None
    last = runs[-1]
    agg = None
    if (last / "aggregate-results.json").exists():
        agg = json.load(open(last / "aggregate-results.json"))
    per_test = []
    if (last / "per-test-results.json").exists():
        per_test = json.load(open(last / "per-test-results.json"))
    if agg is not None:
        agg["per_test"] = per_test
        return agg
    if per_test:
        passed = sum(1 for t in per_test if t.get("passed"))
        return {"total_tests": len(per_test), "passed": passed,
                "pass_rate_pct": round(passed / len(per_test) * 100, 1) if per_test else 0,
                "per_test": per_test}
    return None


def _extract_ledger(per_test: list[dict], tier: int, round_n: int,
                   tech_by_id: dict | None = None) -> list[dict]:
    escapes = []
    for t in per_test:
        if not t.get("passed"):
            tid = t.get("test_id")
            escapes.append({
                "tier": tier, "round": round_n, "test_id": tid,
                "technique": (tech_by_id or {}).get(tid, "unknown"),
                "category": t.get("category"),
                "missed_principles": t.get("expected_principles_missed", []),
                "forbidden_found": t.get("forbidden_keywords_found", []),
                "correctness_score": t.get("correctness_score"),
                "input": t.get("input"),
                "violating_output": t.get("output"),
            })
    return escapes


def _build_blue_probes(escapes: list[dict]) -> list[dict]:
    probes = []
    for e in escapes:
        probes.append({
            "id": f"blue-{e['test_id']}",
            "category": e.get("category", "readme"),
            "description": f"BLUE probe of RED escape ({e['technique']})",
            "input": e["input"],
            "expected_principles": e.get("missed_principles") or ["P1", "P10", "P4"],
            "expected_keywords": [],
            "forbidden_keywords": sorted(set(e.get("forbidden_found", []))),
            "max_tokens": 1500, "difficulty": "hard",
            "adversarial_technique": e["technique"], "blue_probe": True,
        })
    return probes


def _await_file(path: Path, timeout: int, poll: int) -> bool:
    """Block until path exists or timeout. Returns True if found."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(poll)
    return False


def run_red(tier: int, args, base: Path, report: dict) -> list[dict]:
    """Run RED rounds for one tier. Writes escapes.json + red-done.json per round.
    Returns the list of residuals (escapes BLUE should probe) carried forward."""
    sp = TIER_DIR[tier]
    residuals: list[dict] = []
    tier_rounds = []
    for rnd in range(1, args.rounds + 1):
        rdir = base / f"tier{tier}" / f"round{rnd}"
        red_cases = _adv.build_red_cases(tier, args.per_technique,
                                         seed=args.seed + rnd * 100 + tier)
        if residuals:
            red_cases += [{"id": f"red-mut-{e['test_id']}",
                           "category": e.get("category", "readme"),
                           "description": f"RED mutation of {e['technique']}",
                           "input": e["input"],
                           "expected_principles": e.get("missed_principles") or ["P1"],
                           "expected_keywords": [],
                           "forbidden_keywords": sorted(set(e.get("forbidden_found", []))),
                           "max_tokens": 1500, "difficulty": "hard",
                           "adversarial_technique": e["technique"], "red": True}
                          for e in residuals]
        red_dir = rdir / "red"
        (red_dir / "test-cases").mkdir(parents=True, exist_ok=True)
        (red_dir / "test-cases" / "category-red.json").write_text(
            json.dumps(red_cases, indent=2))
        red_agg = None
        if not args.skip_live:
            red_agg = _run_orchestrator(red_dir / "test-cases", sp, red_dir / "run",
                                        args.model, args.max_workers, args.timeout)
        red_pass = red_agg.get("passed", 0) if red_agg else 0
        red_total = red_agg.get("total_tests", len(red_cases)) if red_agg else len(red_cases)
        per_test = red_agg.get("per_test") if red_agg else []
        if not per_test:
            per_test = []
        escapes = _extract_ledger(per_test, tier, rnd,
                                  {c["id"]: c["adversarial_technique"] for c in red_cases})
        (rdir / "escapes.json").write_text(json.dumps(escapes, indent=2))
        # PURPLE HANDSHAKE: RED signals a round is complete (even if 0 escapes)
        # by writing purple.json. BLUE awaits this file (not a process dep) to
        # know the ledger is ready to consume.
        (rdir / "purple.json").write_text(json.dumps({
            "tier": tier, "round": rnd, "handshake": "purple",
            "ledger": "escapes.json",
            "red_total": red_total, "red_passed": red_pass,
            "red_pass_rate_pct": round(red_pass / red_total * 100, 1) if red_total else 0,
            "escapes": len(escapes),
        }, indent=2))
        tier_rounds.append({"round": rnd, "red_total": red_total,
                             "red_passed": red_pass,
                             "red_pass_rate_pct": round(red_pass / red_total * 100, 1) if red_total else 0,
                             "escapes": len(escapes),
                             "techniques_escaped": sorted({e["technique"] for e in escapes})})
        residuals = escapes  # next round re-probes these
        if not escapes:
            break  # compliant -> stop
    report.setdefault("per_tier", {})[tier] = {"mode": "red", "rounds": tier_rounds}
    return residuals


def run_blue(tier: int, args, base: Path, report: dict) -> None:
    """Await RED's ledger per round, then run BLUE probes. Independent launch."""
    sp = TIER_DIR[tier]
    tier_rounds = []
    for rnd in range(1, args.rounds + 1):
        rdir = base / f"tier{tier}" / f"round{rnd}"
        sentinel = rdir / "purple.json"  # PURPLE HANDSHAKE from RED
        found = _await_file(sentinel, args.await_timeout, args.poll_interval)
        if not found:
            # RED never produced this round (crashed / stopped). Move on.
            tier_rounds.append({"round": rnd, "status": "await-timeout",
                                 "blue_pass_rate_pct": None, "blue_probes": 0})
            break
        red_summary = json.load(open(sentinel))
        escapes = json.load(open(rdir / "escapes.json")) if (rdir / "escapes.json").exists() else []
        if not escapes:
            # RED found 0 escapes -> BLUE has nothing to probe; stop.
            tier_rounds.append({"round": rnd, "status": "no-escapes",
                                 "blue_pass_rate_pct": None, "blue_probes": 0})
            break
        probes = _build_blue_probes(escapes)
        blue_dir = rdir / "blue"
        (blue_dir / "test-cases").mkdir(parents=True, exist_ok=True)
        (blue_dir / "test-cases" / "category-blue.json").write_text(
            json.dumps(probes, indent=2))
        blue_agg = None
        if not args.skip_live:
            blue_agg = _run_orchestrator(blue_dir / "test-cases", sp, blue_dir / "run",
                                         args.model, args.max_workers, args.timeout)
        bp = blue_agg.get("passed", 0) if blue_agg else 0
        bt = blue_agg.get("total_tests", len(probes)) if blue_agg else len(probes)
        blue_rate = round(bp / bt * 100, 1) if bt else 0.0
        # residual = escapes BLUE still failed
        bper = blue_agg.get("per_test") if blue_agg else []
        if not bper:
            bper = []
        residual = [e for e in escapes
                    if any(p.get("test_id") == f"blue-{e['test_id']}" and not p.get("passed")
                           for p in bper)] or escapes
        (rdir / "blue-done.json").write_text(json.dumps({
            "tier": tier, "round": rnd, "blue_probes": len(probes),
            "blue_passed": bp, "blue_pass_rate_pct": blue_rate,
            "residual_escapes": len(residual),
        }, indent=2))
        tier_rounds.append({"round": rnd, "status": "done",
                             "blue_probes": len(probes),
                             "blue_pass_rate_pct": blue_rate,
                             "residual_escapes": len(residual),
                             "techniques_escaped": sorted({e["technique"] for e in escapes})})
        if blue_rate >= args.blue_threshold:
            break
        if not residual:
            break
    report.setdefault("per_tier", {})[tier] = {"mode": "blue", "rounds": tier_rounds}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["red", "blue", "both"], default="both")
    ap.add_argument("--tiers", default="-2,-1,0,1,2,3,4,5")
    ap.add_argument("--model", default="tencent/hy3:free")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument("--per-technique", type=int, default=2)
    ap.add_argument("--blue-threshold", type=float, default=95.0)
    ap.add_argument("--await-timeout", type=int, default=3600,
                    help="BLUE: max seconds to wait for RED's red-done.json per round")
    ap.add_argument("--poll-interval", type=int, default=15)
    ap.add_argument("--max-workers", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--results-base", default=None,
                    help="output dir (default: <results_base>/redblue); must stay under it")
    ap.add_argument("--skip-live", action="store_true")
    args = ap.parse_args()

    base = resolve_base(load_config(), args.results_base)
    base.mkdir(parents=True, exist_ok=True)
    tiers = [int(x) for x in args.tiers.split(",")]
    report = {"timestamp": datetime.now(timezone.utc).isoformat(),
              "mode": args.mode, "model": args.model, "tiers": tiers,
              "rounds": args.rounds, "per_tier": {}}

    if args.mode in ("red", "both"):
        for t in tiers:
            run_red(t, args, base, report)
    if args.mode in ("blue", "both"):
        for t in tiers:
            run_blue(t, args, base, report)

    # schematic breakdown (only meaningful when both sides present)
    from collections import Counter
    tech: Counter = Counter()
    for t, tr in report.get("per_tier", {}).items():
        for r in tr.get("rounds", []):
            for x in r.get("techniques_escaped", []):
                tech[x] += 1
    report["escapes_by_technique"] = dict(tech.most_common())
    (base / "report.json").write_text(json.dumps(report, indent=2))

    print(f"\nWrote {base / 'report.json'} (mode={args.mode})")
    for t, tr in report.get("per_tier", {}).items():
        for r in tr.get("rounds", []):
            print(f"  tier{t} r{r.get('round')}: {r}")
    print("escapes_by_technique:", report["escapes_by_technique"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
