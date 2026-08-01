#!/usr/bin/env python3
"""Sample STE-Code benchmark — SESSION-based (delegate), not fork-worker.

Mirrors the orchestrator's prompt format and scoring, but instead of `os.fork()`
fire-and-forget workers, each test runs as a REAL hermes SESSION (--session <id>)
so the skill + standard execution flow is fully traceable (session history in
.hermes/sessions/). All prompt/output I/O lives under .agents/benchmark/sample-session/
(which is gitignored) — nothing is written to the repo root.

Input standard: ste-code/artifacts/ste-code-level5-max.txt ("all from ste-code").

One test per category (14 tests) = a representative SAMPLE, not the full 59.

Usage:
  python3 run_sample_session.py            # run all 14 sample tests
  python3 run_sample_session.py --category comment
"""
from __future__ import annotations

import os
import sys
import json
import glob
import subprocess
import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent  # .agents/benchmark -> .agents -> repo root (STE-Code)
SAMPLE_DIR = HERE / "sample-session"
STANDARD = ROOT / "ste-code" / "artifacts" / "ste-code-level5-max.txt"
MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
HERMES = "hermes"

sys.path.insert(0, str(HERE))
import benchmark_lib as bl  # reuse extract_corrected_text / check_principles / score


def _load_sample_tests():
    """Pick ONE representative test from each category (first test in each file)."""
    tests = []
    for f in sorted(glob.glob(str(HERE / "test-cases" / "category-*.json"))):
        arr = json.loads(Path(f).read_text())
        if arr:
            tests.append(arr[0])
    return tests


def _build_prompt(test: dict) -> str:
    system = STANDARD.read_text(errors="ignore")
    if test.get("input"):  # correction test
        return f"""{system}

## TASK
Check the following text for STE-Code compliance. Apply all 14 principles (P1-P14).
Replace unapproved terms using the synonym table.
IMPORTANT: Do NOT create any files. Output the corrected text inline.
Produce the corrected text first, then a compliance summary table.

## TEXT TO CORRECT
{test['input']}"""
    else:  # generation test
        return f"""{system}

## TASK
{test['prompt']}
IMPORTANT: Do NOT create any files. Output all code and documentation inline as text.
Use STE-Code principles (P1-P14) for all documentation and text you generate.
Apply the synonym table for all word choices.
Produce the requested output first, then a compliance summary table showing which
principles you followed."""


def run_one(test: dict) -> dict:
    tid = test["id"]
    session = f"ste-bench-{tid}"
    prompt = _build_prompt(test)
    SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
    (SAMPLE_DIR / f"{tid}-prompt.txt").write_text(prompt, encoding="utf-8")

    # Real hermes SESSION (traceable). -z non-interactive; --continue <name> creates a
    # named delegate session whose history is recorded in .hermes/sessions/ (so the
    # skill + standard execution flow is fully traceable), unlike the orchestrator's
    # fire-and-forget fork workers.
    out_file = SAMPLE_DIR / f"{tid}-output.txt"
    try:
        r = subprocess.run(
            [HERMES, "-z", prompt, "--model", MODEL, "--continue", session, "--yolo"],
            capture_output=True, text=True, timeout=600,
        )
        output = r.stdout
        if not output.strip() and r.stderr.strip():
            output = "HERMES_ERROR " + r.stderr[:500]
    except subprocess.TimeoutExpired:
        output = "HERMES_ERROR timeout after 600s"
    out_file.write_text(output, encoding="utf-8")

    # Score with the same formula as the orchestrator (benchmark_lib).
    corrected = bl.extract_corrected_text(output)
    satisfied, missed = bl.check_principles(output, test.get("expected_principles", []))
    corrected_lower = corrected.lower()
    expected_kw = test.get("expected_keywords", [])
    forbidden = test.get("forbidden_keywords", [])
    expected_kw_found = bl.check_keywords(corrected_lower, expected_kw) if expected_kw else []
    forbidden_found = bl.check_keywords(corrected_lower, forbidden) if forbidden else []
    sc = bl.calc_correctness(
        expected_principles=test.get("expected_principles", []),
        satisfied=satisfied,
        forbidden_found=forbidden_found,
        total_forbidden=len(forbidden),
        expected_kw_found=expected_kw_found,
        total_expected_kw=len(expected_kw),
    )
    return {
        "id": tid,
        "category": test.get("category"),
        "difficulty": test.get("difficulty"),
        "session": session,
        "score": sc,
        "principles_satisfied": satisfied,
        "principles_missed": missed,
        "forbidden_found": forbidden_found,
        "output_len": len(output),
        "prompt_file": str(SAMPLE_DIR / f"{tid}-prompt.txt"),
        "output_file": str(out_file),
    }


def main():
    args = sys.argv[1:]
    only_cat = None
    for a in args:
        if a.startswith("--category"):
            only_cat = a.split("=", 1)[-1] if "=" in a else args[args.index(a) + 1]

    tests = _load_sample_tests()
    if only_cat:
        tests = [t for t in tests if t.get("category") == only_cat]
    if not tests:
        print("No sample tests found."); sys.exit(1)

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = SAMPLE_DIR / f"run-{stamp}"
    run_dir.mkdir(parents=True, exist_ok=True)

    results = []
    print(f"Sample benchmark: {len(tests)} tests (1/session), model={MODEL}\n")
    for t in tests:
        print(f"  [{t['id']}] {t['category']} ({t.get('difficulty')}) -> session ste-bench-{t['id']} ...", flush=True)
        res = run_one(t)
        results.append(res)
        print(f"      score={res['score']} principles {len(res['principles_satisfied'])}/{len(res['principles_satisfied'])+len(res['principles_missed'])} -> {res['output_file']}", flush=True)

    # Aggregate
    scored = [r["score"] for r in results if isinstance(r["score"], (int, float))]
    avg = sum(scored) / len(scored) if scored else 0
    passed = sum(1 for s in scored if s >= 0.70)
    agg = {
        "model": MODEL,
        "standard": str(STANDARD),
        "run_dir": str(run_dir),
        "n_tests": len(results),
        "avg_score": round(avg, 3),
        "pass_rate": f"{passed}/{len(scored)}",
        "per_test": results,
    }
    (run_dir / "aggregate-results.json").write_text(json.dumps(agg, indent=2), encoding="utf-8")
    print(f"\n=== SAMPLE BENCHMARK: avg_score={avg:.3f} pass={passed}/{len(scored)} ===")
    print(f"    run dir: {run_dir}")


if __name__ == "__main__":
    main()
