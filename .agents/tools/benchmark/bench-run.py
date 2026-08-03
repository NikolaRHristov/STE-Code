#!/usr/bin/env python3
"""Lightweight benchmark — uses hermes -z via subprocess (telemetry pattern).

Runs all 59 test cases against one level prompt, scores results.
Usage: python3 .agents/tools/benchmark/bench-run.py <level> [--dry-run]
"""

import json, subprocess, sys, time
from pathlib import Path

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
from ste_io import write_text, mkdir  # noqa: E402
from ste_time import run_stamp  # noqa: E402

TEST_DIR = PROJECT / ".agents" / "benchmark" / "test-cases"
RESULTS_DIR = PROJECT / ".agents" / "benchmark" / "results-v3"

LEVEL_PROMPTS = {
    "1": PROJECT / "ste-code" / "artifacts" / "level1" / "system-prompt.txt",
    "2": PROJECT / "ste-code" / "artifacts" / "level2" / "system-prompt.txt",
    "3": PROJECT / "ste-code" / "artifacts" / "level3" / "system-prompt.txt",
    "4": PROJECT / "ste-code" / "artifacts" / "level4" / "system-prompt.txt",
}

# Load scoring rules from benchmark_lib
sys.path.insert(0, str(PROJECT / ".agents" / "benchmark"))
from benchmark_lib import (
    PRINCIPLE_KEYWORDS,
    calc_correctness,
    check_principles,
    check_keywords,
)


def load_tests():
    tests = []
    for f in sorted(TEST_DIR.glob("category-*.json")):
        tests.extend(json.loads(f.read_text()))
    return tests


def run_test(tc, system_prompt, model="poolside/laguna-s-2.1:free"):
    """Run one test case. Returns (output, elapsed, exit_code)."""
    full_prompt = f"""{system_prompt}

## TASK
Check this text for STE-Code compliance. Fix all violations.
Output the corrected text, then list which principles you applied.

TEXT:
{tc.get("input", tc.get("prompt", ""))}"""

    start = time.time()
    try:
        result = subprocess.run(
            ["hermes", "-z", full_prompt, "-m", model, "--yolo"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        elapsed = time.time() - start
        return result.stdout.strip(), elapsed, result.returncode
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]", time.time() - start, -1


def score_test(tc, output):
    """Score one test output against expected principles/keywords."""
    output_lower = output.lower()
    satisfied, missed = check_principles(output, tc.get("expected_principles", []))
    forbidden_found = check_keywords(output_lower, tc.get("forbidden_keywords", []))
    expected_found = check_keywords(output_lower, tc.get("expected_keywords", []))

    score = calc_correctness(
        tc.get("expected_principles", []),
        satisfied,
        forbidden_found,
        len(tc.get("forbidden_keywords", [])),
        expected_found,
        len(tc.get("expected_keywords", [])),
    )
    return min(1.0, max(0.0, score))


def main():
    if len(sys.argv) < 2:
        print("Usage: bench-run.py <level> [--dry-run]")
        sys.exit(1)

    level = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    prompt_file = LEVEL_PROMPTS.get(level)
    if not prompt_file or not prompt_file.exists():
        print(f"ERROR: Level {level} prompt not found at {prompt_file}")
        sys.exit(1)

    system_prompt = prompt_file.read_text()
    tests = load_tests()

    print(f"Level {level}: {prompt_file.name} ({len(system_prompt) // 4:,} tokens)")
    print(
        f"Tests: {len(tests)} across {len(list(TEST_DIR.glob('category-*.json')))} categories"
    )

    if dry_run:
        return

    mkdir(RESULTS_DIR)
    timestamp = run_stamp()
    results = []

    for i, tc in enumerate(tests):
        print(f"  [{i + 1}/{len(tests)}] {tc['id']}...", end=" ", flush=True)
        output, elapsed, rc = run_test(tc, system_prompt)
        score = score_test(tc, output) if rc == 0 and output != "[TIMEOUT]" else 0.0
        passed = score >= 0.7
        status = "PASS" if passed else "FAIL"
        print(f"{status} ({score:.2f}) in {elapsed:.0f}s")

        results.append(
            {
                "id": tc["id"],
                "category": tc.get("category", ""),
                "input": tc.get("input", tc.get("prompt", "")),
                "output": output[:500],
                "score": round(score, 3),
                "passed": passed,
                "elapsed": round(elapsed, 1),
                "exit_code": rc,
            }
        )

    # Summary
    passed = sum(1 for r in results if r["passed"])
    avg_score = sum(r["score"] for r in results) / len(results)
    total_time = sum(r["elapsed"] for r in results)

    report = {
        "timestamp": timestamp,
        "level": level,
        "prompt_tokens": len(system_prompt) // 4,
        "tests": len(results),
        "passed": passed,
        "pass_rate": f"{passed}/{len(results)} ({100 * passed / len(results):.1f}%)",
        "avg_score": round(avg_score, 3),
        "total_elapsed_s": round(total_time, 1),
        "results": results,
    }

    report_file = RESULTS_DIR / f"level-{level}-{timestamp}.json"
    write_text(report_file, json.dumps(report, indent=2))

    print(
        f"\nLevel {level}: {passed}/{len(results)} passed ({100 * passed / len(results):.1f}%)"
    )
    print(f"Avg score: {avg_score:.3f}")
    print(f"Total time: {total_time:.0f}s")
    print(f"Report: {report_file}")


if __name__ == "__main__":
    main()
