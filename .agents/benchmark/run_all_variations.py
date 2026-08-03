#!/usr/bin/env python3
"""Run the STE-Code benchmark across ALL tier variations in parallel.

For each of the 8 tiers (level-2 .. level5) this runs the orchestrator TWICE:
  (a) STATIC  — against the fixed 59-case suite (test-cases/)
  (b) ADHOC   — against freshly generated ad-hoc cases (generate_adhoc_tests.py)

Plus a CONTROL baseline (plain assistant, no STE-Code prompt) on the static
suite, so we can compare STE-Code vs plain assistant.

Concurrency is capped GLOBALLY at --max-orchestrators (default 3) so we do not
blast the model with dozens of simultaneous sessions (avoids 429s). Each
orchestrator internally fans out its own workers (--max-workers), but the
number of *simultaneous orchestrator processes* never exceeds the cap.

Output: each orchestrator writes under --results-base/<tier>-static/ etc.
A final comparison.json summarizes pass-rate per tier/variant.

Usage:
  python3 run_all_variations.py
  python3 run_all_variations.py --max-orchestrators 3 --max-workers 2 --model tencent/hy3:free
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import concurrent.futures
from pathlib import Path
from datetime import datetime, timezone

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
BENCH = PROJECT / ".agents" / "benchmark"
sys.path.insert(0, str(BENCH))
from harness_config import load_config, resolve_base  # noqa: E402

ORCH = BENCH / "orchestrator.py"
CONTROL = BENCH / "orchestrator-control.py"
GEN = BENCH / "generate_adhoc_tests.py"
STATIC_DIR = BENCH / "test-cases"
ADHOC_DIR = BENCH / "test-cases-adhoc"

TIERS = [-2, -1, 0, 1, 2, 3, 4, 5]
TIER_DIR = {
    t: (PROJECT / "ste-code" / "artifacts" / f"level{t}" / "system-prompt.txt")
    for t in TIERS
}


def _run_one(name: str, cmd: list[str], results_dir: Path, model: str) -> dict:
    """Run one orchestrator subprocess; return a result record."""
    results_dir.mkdir(parents=True, exist_ok=True)
    log = results_dir.parent / f"{name}.log"
    t0 = time.time()
    try:
        r = subprocess.run(
            cmd, cwd=str(PROJECT), capture_output=True, text=True, timeout=60 * 60
        )
        rc = r.returncode
        log.write_text(f"RC={rc}\nSTDOUT\n{r.stdout}\nSTDERR\n{r.stderr}\n")
    except subprocess.TimeoutExpired:
        rc = -1
        log.write_text("TIMEOUT after 60m\n")
    elapsed = time.time() - t0

    # Find the aggregate results for this run.
    agg = None
    runs = sorted(results_dir.glob("run-*"))
    if runs and (runs[-1] / "aggregate-results.json").exists():
        try:
            agg = json.load(open(runs[-1] / "aggregate-results.json"))
        except Exception:
            agg = None
    return {
        "name": name,
        "rc": rc,
        "elapsed_s": round(elapsed),
        "results_dir": str(results_dir),
        "aggregate": agg,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="tencent/hy3:free")
    ap.add_argument(
        "--max-orchestrators",
        type=int,
        default=3,
        help="global cap on simultaneous orchestrator processes",
    )
    ap.add_argument(
        "--max-workers", type=int, default=2, help="per-orchestrator worker fan-out"
    )
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument(
        "--results-base",
        default=None,
        help="parent dir (default: <results_base>); each variation "
        "writes <base>/<name>/ and must stay under it",
    )
    ap.add_argument("--skip-adhoc", action="store_true")
    ap.add_argument("--skip-control", action="store_true")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    cfg = load_config()
    base = (
        cfg.results_base
        if args.results_base is None
        else resolve_base(cfg, args.results_base)
    )
    base.mkdir(parents=True, exist_ok=True)

    # Generate ad-hoc cases pre-run.
    if not args.skip_adhoc:
        print(f"[gen] generating ad-hoc tests (seed={args.seed}) ...", flush=True)
        g = subprocess.run(
            [
                sys.executable,
                str(GEN),
                "--out-dir",
                str(ADHOC_DIR),
                "--seed",
                str(args.seed),
            ],
            cwd=str(PROJECT),
            capture_output=True,
            text=True,
        )
        print(g.stdout.strip() or g.stderr.strip(), flush=True)

    # Build the job list.
    jobs = []
    for t in TIERS:
        sp = TIER_DIR[t]
        # static
        jobs.append(
            (
                f"tier{t}-static",
                [
                    sys.executable,
                    str(ORCH),
                    "--test-dir",
                    str(STATIC_DIR),
                    "--system-prompt-file",
                    str(sp),
                    "--results-dir",
                    str(base / f"tier{t}-static"),
                    "--max-workers",
                    str(args.max_workers),
                    "--timeout",
                    str(args.timeout),
                    "--poll-interval",
                    "2",
                    "--model",
                    args.model,
                ],
            )
        )
        # adhoc
        if not args.skip_adhoc:
            jobs.append(
                (
                    f"tier{t}-adhoc",
                    [
                        sys.executable,
                        str(ORCH),
                        "--test-dir",
                        str(ADHOC_DIR),
                        "--system-prompt-file",
                        str(sp),
                        "--results-dir",
                        str(base / f"tier{t}-adhoc"),
                        "--max-workers",
                        str(args.max_workers),
                        "--timeout",
                        str(args.timeout),
                        "--poll-interval",
                        "2",
                        "--model",
                        args.model,
                    ],
                )
            )
    if not args.skip_control:
        jobs.append(
            (
                "control-static",
                [
                    sys.executable,
                    str(CONTROL),
                    "--test-dir",
                    str(STATIC_DIR),
                    "--results-dir",
                    str(base / "control-static"),
                    "--timeout",
                    str(args.timeout),
                    "--retries",
                    "1",
                    "--model",
                    args.model,
                ],
            )
        )

    print(
        f"[run] {len(jobs)} orchestrator jobs, cap={args.max_orchestrators} "
        f"concurrent, model={args.model}",
        flush=True,
    )

    results = []
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=args.max_orchestrators
    ) as ex:
        futs = {
            ex.submit(_run_one, name, cmd, base / name, args.model): name
            for name, cmd in jobs
        }
        for fut in concurrent.futures.as_completed(futs):
            rec = fut.result()
            results.append(rec)
            agg = rec["aggregate"]
            if agg:
                print(
                    f"  done {rec['name']}: rc={rec['rc']} "
                    f"pass={agg.get('pass_rate_pct')}% "
                    f"({agg.get('passed')}/{agg.get('total_tests')}) "
                    f"in {rec['elapsed_s']:.0f}s",
                    flush=True,
                )
            else:
                print(
                    f"  done {rec['name']}: rc={rec['rc']} (no aggregate) "
                    f"in {rec['elapsed_s']:.0f}s",
                    flush=True,
                )

    # Comparison report.
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "jobs": len(jobs),
        "results": [],
    }
    for r in sorted(results, key=lambda x: x["name"]):
        a = r["aggregate"]
        report["results"].append(
            {
                "name": r["name"],
                "rc": r["rc"],
                "pass_rate_pct": a.get("pass_rate_pct") if a else None,
                "passed": a.get("passed") if a else None,
                "total_tests": a.get("total_tests") if a else None,
                "avg_correctness": a.get("aggregates", {}).get("avg_correctness")
                if a
                else None,
                "results_dir": r["results_dir"],
            }
        )
    (base / "comparison.json").write_text(json.dumps(report, indent=2))
    print(f"\nWrote {base / 'comparison.json'}")
    print("\nSUMMARY")
    for row in report["results"]:
        pr = row["pass_rate_pct"]
        print(
            f"  {row['name']:<16} pass={pr if pr is None else str(pr) + '%'} "
            f"({row['passed']}/{row['total_tests']})"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
