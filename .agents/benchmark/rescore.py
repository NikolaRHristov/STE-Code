#!/usr/bin/env python3
"""Re-score benchmark outputs with fixed extraction logic.

Usage:
  python3 rescore.py [run_dir]                  Basic re-score
  python3 rescore.py [run_dir] --diff            Show score changes vs previous
  python3 rescore.py [run_dir] --output report   Write aggregate + recommendations

If run_dir is not provided, uses the latest run in results/.
"""
import argparse
import difflib
import glob as _glob
import json
import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Import shared benchmark library — single source of truth for:
#   PRINCIPLE_KEYWORDS, extract_corrected_text, extract_compliance_section,
#   check_principles, check_keywords, calc_correctness, build_recommendations,
#   load_test_cases, load_previous_results, resolve_project_root.
# ---------------------------------------------------------------------------
from benchmark_lib import (                      # noqa: E402
    PRINCIPLE_KEYWORDS,
    build_recommendations,
    calc_correctness,
    check_keywords,
    check_principles,
    extract_compliance_section,
    extract_corrected_text,
    load_previous_results,
    load_test_cases,
    resolve_project_root,
)

# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Re-score benchmark outputs with updated extraction/scoring logic.",
    )
    p.add_argument(
        "run_dir", nargs="?",
        help="Run directory to re-score (default: latest in results/).",
    )
    p.add_argument(
        "--diff", action="store_true",
        help="Show per-test score deltas vs the previous scoring run.",
    )
    p.add_argument(
        "--output", choices=["summary", "report", "json"], default="summary",
        help="Output format. 'summary' = terminal table only (default). "
             "'report' = terminal table + recommendations. "
             "'json' = write aggregate JSON, no terminal output.",
    )
    p.add_argument(
        "--out-file",
        help="Write aggregate JSON to a specific file "
             "(default: <run_dir>/rescored-results.json).",
    )
    p.add_argument(
        "--test-dir",
        help="Directory containing category-*.json test case files "
             "(default: auto-detect).",
    )
    return p.parse_args()


# ---------------------------------------------------------------------------
# Required-patterns check — matches orchestrator.py Phase 3 logic.
# ---------------------------------------------------------------------------

def check_required_patterns(
    output: str, required_patterns: List[str],
) -> Tuple[List[str], List[str]]:
    """Check which required regex patterns are present in *output*.

    Returns (patterns_found, patterns_missed).
    """
    found: List[str] = []
    missed: List[str] = []
    for pat in required_patterns:
        if re.search(pat, output, re.IGNORECASE | re.DOTALL):
            found.append(pat)
        else:
            missed.append(pat)
    return found, missed


# ---------------------------------------------------------------------------
# Scoring orchestration — one test case at a time.
# ---------------------------------------------------------------------------

def score_one_test(
    test_case: dict,
    output: str,
    previous: Optional[dict] = None,
) -> dict:
    """Score a single test case against its expected output.

    Uses the canonical scoring pipeline from benchmark_lib and adds:
      - required-patterns check (generation tests)
      - pattern penalty (up to 0.2 off correctness)
      - token estimation
      - diff ratio
      - latency preservation from previous run when available
    """
    tid = test_case["id"]
    cat = test_case["category"]
    is_generation = "prompt" in test_case
    task_text = test_case.get("prompt", test_case.get("input", ""))

    # Extract corrected text and compliance section.
    corrected = extract_corrected_text(output)
    corrected_lower = corrected.lower()
    compliance_summary = extract_compliance_section(output)

    # Check principles.
    satisfied, missed = check_principles(
        output, test_case["expected_principles"],
    )

    # Check forbidden keywords (in corrected text only).
    forbidden = test_case.get("forbidden_keywords", [])
    forbidden_found = check_keywords(corrected_lower, forbidden)

    # Check expected keywords.
    expected_kw = test_case.get("expected_keywords", [])
    expected_found = check_keywords(corrected_lower, expected_kw)

    # Check required patterns (generation tests).
    required_patterns = test_case.get("required_patterns", [])
    patterns_found, patterns_missed = check_required_patterns(
        output, required_patterns,
    )

    # Calculate base correctness.
    correctness = calc_correctness(
        test_case["expected_principles"], satisfied,
        forbidden_found, len(forbidden),
        expected_found, len(expected_kw),
    )

    # Pattern penalty — up to 0.2 off for missing required patterns.
    pattern_penalty = 0.0
    if required_patterns:
        pattern_penalty = round(
            0.2 * len(patterns_missed) / len(required_patterns), 2,
        )
        correctness = round(max(0.0, correctness - pattern_penalty), 2)

    # Token estimation (full output).
    token_input = len(task_text) // 4
    token_output = len(output) // 4

    # Diff ratio — how much the output changed from the input.
    if corrected and task_text:
        ratio = difflib.SequenceMatcher(
            None, task_text.lower(), corrected.lower(),
        ).ratio()
        diff_ratio = round(1.0 - ratio, 2)
    else:
        diff_ratio = 0.0

    # Truncation detection.
    is_truncated = len(output) < 20 or output.startswith("HERMES_ERROR")

    # Pass/fail threshold: 0.7
    passed = correctness >= 0.7

    # ---- Preserve latency / token data from previous run when available ----
    latency_ms = None
    prev_token_input = None
    prev_token_output = None
    if previous:
        latency_ms = previous.get("latency_ms")
        prev_token_input = previous.get("token_count_input")
        prev_token_output = previous.get("token_count_output")

    # ---- Build notes ----
    notes_parts: List[str] = []
    if missed:
        notes_parts.append(f"Missed: {', '.join(missed)}")
    if forbidden_found:
        notes_parts.append(f"Forbidden found: {', '.join(forbidden_found)}")
    if expected_found:
        notes_parts.append(f"Keywords OK: {len(expected_found)}/{len(expected_kw)}")
    if patterns_missed:
        notes_parts.append(f"Patterns missed: {len(patterns_missed)}/{len(required_patterns)}")

    result = {
        "test_id": tid,
        "category": cat,
        "description": test_case.get("description", ""),
        "input": task_text,
        "test_type": "generation" if is_generation else "correction",
        "output": corrected,
        "compliance_summary": compliance_summary,
        "expected_principles_satisfied": satisfied,
        "expected_principles_missed": missed,
        "forbidden_keywords_found": forbidden_found,
        "expected_keywords_found": expected_found,
        "required_patterns": required_patterns,
        "required_patterns_found": patterns_found,
        "required_patterns_missed": patterns_missed,
        "pattern_penalty": pattern_penalty,
        "correctness_score": correctness,
        "latency_ms": latency_ms,
        "token_count_input": prev_token_input or token_input,
        "token_count_output": prev_token_output or token_output,
        "diff_ratio": diff_ratio,
        "truncated": is_truncated,
        "passed": passed,
        "notes": "; ".join(notes_parts) if notes_parts else "All checks passed",
        "difficulty": test_case.get("difficulty", "unknown"),
        "rescored_at": None,  # filled by caller
    }
    return result


# ---------------------------------------------------------------------------
# Diff computation — compare rescored results against previous run.
# ---------------------------------------------------------------------------

def compute_diffs(
    results: List[dict],
    previous_map: Optional[Dict[str, dict]],
) -> List[dict]:
    """Build per-test delta entries showing what changed between rescore and previous."""
    if not previous_map:
        return []
    deltas: List[dict] = []
    for r in results:
        tid = r["test_id"]
        prev = previous_map.get(tid)
        if prev is None:
            deltas.append({
                "test_id": tid,
                "status": "new",
                "old_score": None,
                "new_score": r["correctness_score"],
                "delta": None,
            })
            continue

        old_score = prev.get("correctness_score", 0.0)
        new_score = r["correctness_score"]
        delta = round(new_score - old_score, 2)
        old_passed = prev.get("passed", False)
        new_passed = r["passed"]

        # Determine why scores differ (if at all).
        reasons: List[str] = []
        if r["expected_principles_missed"] != prev.get("expected_principles_missed", []):
            reasons.append("principle detection changed")
        if r["forbidden_keywords_found"] != prev.get("forbidden_keywords_found", []):
            reasons.append("forbidden keywords changed")
        if r["expected_keywords_found"] != prev.get("expected_keywords_found", []):
            reasons.append("keyword detection changed")
        if r.get("pattern_penalty", 0.0) > 0:
            # Previous run had no pattern check — this is a new penalty source.
            reasons.append("pattern penalty applied (was missing)")

        deltas.append({
            "test_id": tid,
            "category": r["category"],
            "status": "flip" if old_passed != new_passed else ("changed" if delta != 0 else "same"),
            "old_score": old_score,
            "new_score": new_score,
            "delta": delta,
            "old_passed": old_passed,
            "new_passed": new_passed,
            "reasons": reasons if delta != 0 else [],
        })
    # Also record tests that were in previous but not in this rescore.
    if previous_map:
        current_ids = {r["test_id"] for r in results}
        for tid in previous_map:
            if tid not in current_ids:
                deltas.append({
                    "test_id": tid,
                    "category": previous_map[tid].get("category", "unknown"),
                    "status": "removed",
                    "old_score": previous_map[tid].get("correctness_score", 0.0),
                    "new_score": None,
                    "delta": None,
                })
    return deltas


# ---------------------------------------------------------------------------
# Aggregate computation
# ---------------------------------------------------------------------------

def compute_aggregate(
    results: List[dict], deltas: Optional[List[dict]] = None,
) -> dict:
    """Build the aggregate results dict, mirroring orchestrator.py Phase 4 output."""
    from datetime import datetime, timezone

    passed = sum(1 for r in results if r["passed"])
    failed = len(results) - passed
    scores = [r["correctness_score"] for r in results]

    # Category stats.
    cat_stats: Dict[str, dict] = defaultdict(
        lambda: {"passed": 0, "failed": 0, "scores": [], "latencies": []},
    )
    for r in results:
        cat = r["category"]
        if r["passed"]:
            cat_stats[cat]["passed"] += 1
        else:
            cat_stats[cat]["failed"] += 1
        cat_stats[cat]["scores"].append(r["correctness_score"])
        if r.get("latency_ms") is not None:
            cat_stats[cat]["latencies"].append(r["latency_ms"])

    by_category: Dict[str, dict] = {}
    for cat in sorted(cat_stats):
        s = cat_stats[cat]
        total = s["passed"] + s["failed"]
        # Use 0.0 as fallback when no scores exist.
        avg_score = round(sum(s["scores"]) / len(s["scores"]), 3) if s["scores"] else 0.0
        latencies = s["latencies"]
        avg_lat = round(sum(latencies) / len(latencies)) if latencies else 0
        by_category[cat] = {
            "passed": s["passed"],
            "failed": s["failed"],
            "total": total,
            "avg_correctness": avg_score,
            "avg_latency_ms": avg_lat,
        }

    # Difficulty stats.
    diff_stats: Dict[str, dict] = defaultdict(
        lambda: {"passed": 0, "failed": 0, "scores": []},
    )
    for r in results:
        d = r["difficulty"]
        if r["passed"]:
            diff_stats[d]["passed"] += 1
        else:
            diff_stats[d]["failed"] += 1
        diff_stats[d]["scores"].append(r["correctness_score"])

    by_difficulty: Dict[str, dict] = {}
    for diff in ["easy", "medium", "hard"]:
        if diff in diff_stats:
            s = diff_stats[diff]
            total = s["passed"] + s["failed"]
            avg = round(sum(s["scores"]) / len(s["scores"]), 3) if s["scores"] else 0.0
            by_difficulty[diff] = {
                "passed": s["passed"],
                "failed": s["failed"],
                "total": total,
                "avg_correctness": avg,
            }

    # Latency and token aggregates.
    latencies = [r["latency_ms"] for r in results if r.get("latency_ms") is not None]
    tokens_in = [r["token_count_input"] for r in results if r.get("token_count_input") is not None]
    tokens_out = [r["token_count_output"] for r in results if r.get("token_count_output") is not None]

    avg_latency = round(sum(latencies) / len(latencies)) if latencies else 0
    avg_score = round(sum(scores) / len(scores), 3) if scores else 0.0
    min_correctness = min(scores) if scores else 0.0
    max_correctness = max(scores) if scores else 0.0
    min_lat = min(latencies) if latencies else 0
    max_lat = max(latencies) if latencies else 0
    avg_token_in = round(sum(tokens_in) / len(tokens_in)) if tokens_in else 0
    avg_token_out = round(sum(tokens_out) / len(tokens_out)) if tokens_out else 0
    total_token_in = sum(tokens_in)
    total_token_out = sum(tokens_out)

    # Recommendations.
    cat_scores_map = {c: d["avg_correctness"] for c, d in by_category.items()}
    truncated_count = sum(1 for r in results if r.get("truncated", False))
    recommendations = build_recommendations(
        avg_correctness=avg_score,
        avg_latency_ms=float(avg_latency),
        category_scores=cat_scores_map,
        total_tests=len(results),
        retry_count=0,
        timed_out_count=0,
        truncated_count=truncated_count,
    )

    # Diff summary.
    diff_summary = None
    if deltas:
        changed = [d for d in deltas if d.get("status") in ("changed", "flip")]
        flips = [d for d in deltas if d.get("status") == "flip"]
        diff_summary = {
            "total_deltas": len(deltas),
            "changed": len(changed),
            "unchanged": sum(1 for d in deltas if d.get("status") == "same"),
            "flips": len(flips),
            "new": sum(1 for d in deltas if d.get("status") == "new"),
            "removed": sum(1 for d in deltas if d.get("status") == "removed"),
            "score_improved": sum(1 for d in changed if (d.get("delta") or 0) > 0),
            "score_declined": sum(1 for d in changed if (d.get("delta") or 0) < 0),
        }

    aggregate = {
        "benchmark_id": "ste-code-rescore-v2.0.0",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "total_tests": len(results),
        "passed": passed,
        "failed": failed,
        "pass_rate_pct": round(passed / len(results) * 100, 1) if results else 0.0,
        "aggregates": {
            "avg_correctness": avg_score,
            "min_correctness": min_correctness,
            "max_correctness": max_correctness,
            "avg_latency_ms": avg_latency,
            "min_latency_ms": min_lat,
            "max_latency_ms": max_lat,
            "avg_token_input": avg_token_in,
            "avg_token_output": avg_token_out,
            "total_tokens_input": total_token_in,
            "total_tokens_output": total_token_out,
        },
        "by_category": by_category,
        "by_difficulty": by_difficulty,
        "failures": [r for r in results if not r["passed"]],
        "recommendations": recommendations,
        "diff_summary": diff_summary,
        "deltas": deltas if deltas else [],
        "note": "Rescored with benchmark_lib — canonical extraction and keywords.",
    }
    return aggregate


# ---------------------------------------------------------------------------
# Terminal report printing
# ---------------------------------------------------------------------------

def print_report(aggregate: dict, deltas: Optional[List[dict]] = None) -> None:
    """Print a formatted terminal report."""
    print()
    print("=" * 70)
    print("  STE-CODE RE-SCORE RESULTS")
    print("=" * 70)
    print(f"  Timestamp:   {aggregate['timestamp']}")
    print(f"  Total:       {aggregate['total_tests']} tests")
    print(f"  Passed:      {aggregate['passed']} ({aggregate['pass_rate_pct']}%)")
    print(f"  Failed:      {aggregate['failed']}")
    print()
    ag = aggregate["aggregates"]
    print("  Averages:")
    print(f"    Correctness:  {ag['avg_correctness']:.3f}  "
          f"(range: {ag['min_correctness']:.2f} – {ag['max_correctness']:.2f})")
    if ag["avg_latency_ms"]:
        print(f"    Latency:      {ag['avg_latency_ms']} ms  "
              f"(range: {ag['min_latency_ms']} – {ag['max_latency_ms']} ms)")
    if ag["avg_token_input"]:
        print(f"    Tokens in:    {ag['avg_token_input']} avg  "
              f"({ag['total_tokens_input']} total)")
    if ag["avg_token_output"]:
        print(f"    Tokens out:   {ag['avg_token_output']} avg  "
              f"({ag['total_tokens_output']} total)")
    print()

    # Category breakdown.
    print("-" * 70)
    print(f"  {'Category':<15} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Rate':>7} {'Avg Score':>10} {'Avg Lat':>8}")
    print("-" * 70)
    for cat in sorted(aggregate["by_category"]):
        d = aggregate["by_category"][cat]
        rate = round(d["passed"] / d["total"] * 100) if d["total"] else 0
        print(f"  {cat:<15} {d['total']:>6} {d['passed']:>7} {d['failed']:>7} "
              f"{rate:>6}% {d['avg_correctness']:>10.3f} {d['avg_latency_ms']:>7}ms")
    print("-" * 70)

    # Difficulty breakdown.
    print()
    print(f"  {'Difficulty':<12} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Avg Score':>10}")
    print("-" * 45)
    for diff in ["easy", "medium", "hard"]:
        if diff in aggregate["by_difficulty"]:
            d = aggregate["by_difficulty"][diff]
            print(f"  {diff:<12} {d['total']:>6} {d['passed']:>7} {d['failed']:>7} {d['avg_correctness']:>10.3f}")

    # Per-test detail.
    failures = aggregate.get("failures", [])
    # Collect all results from the aggregate (they are stored in failures only).
    # We need per-test for the table — read from the aggregate's internal state.
    # Since we have the results list in main(), we pass deltas directly.

    # Failures detail.
    if failures:
        print()
        print(f"=== FAILURES ({len(failures)}) ===")
        for r in failures:
            print(f"  {r['test_id']} ({r['category']}, {r['difficulty']}): score={r['correctness_score']}")
            print(f"    Input:  {r['input'][:80]}...")
            print(f"    Output: {r['output'][:80]}...")
            print(f"    Missed principles: {r['expected_principles_missed']}")
            print(f"    Forbidden found:   {r['forbidden_keywords_found']}")
            print(f"    Patterns missed:   {r.get('required_patterns_missed', [])}")
            print()

    # Recommendations.
    if aggregate.get("recommendations"):
        print("=== RECOMMENDATIONS ===")
        for rec in aggregate["recommendations"]:
            print(f"  * {rec}")
        print()

    # Diff summary.
    if deltas:
        print_diff_summary(deltas)


def print_diff_summary(deltas: List[dict]) -> None:
    """Print a diff summary showing which tests changed score and by how much."""
    changed = [d for d in deltas if d.get("status") in ("changed", "flip")]
    if not changed:
        print("=== SCORE DIFF === (no changes)")
        return

    print("=== SCORE DIFF ===")
    print(f"  {len(changed)} test(s) changed score:")
    print()
    print(f"  {'ID':<12} {'Status':<10} {'Old':>6} {'New':>6} {'Delta':>7}  Reason")
    print("-" * 70)
    for d in sorted(changed, key=lambda x: abs(x.get("delta", 0)), reverse=True):
        status = d.get("status", "?")
        old_s = f"{d['old_score']:.2f}" if d["old_score"] is not None else "  N/A"
        new_s = f"{d['new_score']:.2f}" if d["new_score"] is not None else "  N/A"
        delta_s = f"{d['delta']:+.2f}" if d["delta"] is not None else "  N/A"
        reason = "; ".join(d.get("reasons", [])) if d.get("reasons") else "-"
        print(f"  {d['test_id']:<12} {status:<10} {old_s:>6} {new_s:>6} {delta_s:>7}  {reason[:50]}")
    print("-" * 70)

    # Flip summary.
    flips = [d for d in deltas if d.get("status") == "flip"]
    if flips:
        print()
        print("  Pass/fail flips:")
        for d in flips:
            direction = "PASS  FAIL" if d.get("old_passed") and not d.get("new_passed") else "FAIL  PASS"
            print(f"    {d['test_id']}  {direction}  ({d.get('old_score', 0):.2f}  {d.get('new_score', 0):.2f})")
    print()


def print_per_test_table(results: List[dict]) -> None:
    """Print a compact per-test results table."""
    print()
    print("-" * 70)
    print(f"  {'ID':<12} {'Category':<12} {'Score':>6} {'Latency':>8} {'Result':>7}  Notes")
    print("-" * 70)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        lat_str = f"{r['latency_ms']}ms" if r.get("latency_ms") is not None else "     N/A"
        print(f"  {r['test_id']:<12} {r['category']:<12} {r['correctness_score']:>6.2f} "
              f"{lat_str:>8} {status:>7}  {r['notes'][:60]}")
    print("-" * 70)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    # Resolve paths.
    project_root = resolve_project_root()
    test_dir = args.test_dir or os.path.join(
        project_root, ".agents/benchmark/test-cases",
    )
    results_dir = os.path.join(project_root, ".agents/benchmark/results")

    # Determine run directory.
    if args.run_dir:
        run_dir = os.path.abspath(args.run_dir)
    else:
        runs = sorted(_glob.glob(os.path.join(results_dir, "run-*")))
        if not runs:
            print(
                "ERROR: No run directories found in results/. "
                "Run orchestrator.py first.",
            )
            sys.exit(1)
        run_dir = runs[-1]

    if not os.path.isdir(run_dir):
        print(f"ERROR: Run directory not found: {run_dir}")
        sys.exit(1)

    print(f"Re-scoring: {run_dir}")

    # Load test cases.
    try:
        test_map = load_test_cases(test_dir)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    # Load previous per-test results (for latency/token preservation + diff).
    previous_map = load_previous_results(run_dir)

    # Re-score each test.
    results: List[dict] = []
    for test_id, tc in sorted(test_map.items()):
        out_file = os.path.join(run_dir, f"{test_id}-output.txt")
        if not os.path.exists(out_file):
            print(f"  SKIP {test_id}: no output file")
            continue

        with open(out_file) as f:
            output = f.read()

        prev = previous_map.get(test_id) if previous_map else None
        result = score_one_test(tc, output, previous=prev)
        results.append(result)

    if not results:
        print("ERROR: No output files found to score.")
        sys.exit(1)

    # Compute diffs if requested or if previous results exist.
    deltas: Optional[List[dict]] = None
    if args.diff or previous_map:
        deltas = compute_diffs(results, previous_map)

    # Compute aggregate.
    aggregate = compute_aggregate(results, deltas)

    # Write output.
    from datetime import datetime, timezone
    rescored_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    for r in results:
        r["rescored_at"] = rescored_at

    out_file = args.out_file or os.path.join(run_dir, "rescored-results.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    # Write per-test results.
    per_test_file = os.path.join(
        os.path.dirname(out_file), "rescored-per-test.json",
    )
    with open(per_test_file, "w") as f:
        json.dump(results, f, indent=2)

    # Write aggregate.
    with open(out_file, "w") as f:
        json.dump(aggregate, f, indent=2)

    # Write deltas separately for tooling.
    if deltas:
        deltas_file = os.path.join(
            os.path.dirname(out_file), "rescored-deltas.json",
        )
        with open(deltas_file, "w") as f:
            json.dump(deltas, f, indent=2)

    # Terminal output.
    if args.output in ("summary", "report"):
        print_report(aggregate, deltas if args.diff else None)
        print_per_test_table(results)

    elif args.output == "json":
        print(f"JSON written to: {out_file}")

    # Always print file locations.
    print(f"Per-test:  {per_test_file}")
    print(f"Aggregate: {out_file}")
    if deltas:
        print(f"Deltas:    {os.path.join(os.path.dirname(out_file), 'rescored-deltas.json')}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
