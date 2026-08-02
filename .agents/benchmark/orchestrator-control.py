#!/usr/bin/env python3
"""Control Group Benchmark — plain coding assistant, no STE-Code rails. Same 59 tests."""

# DESIGN RATIONALE — WHY THIS FILE EXISTS
# This is the CONTROL GROUP for the STE-Code benchmark suite. It runs the
# identical 59 tests as `orchestrator.py` but uses a plain system prompt
# with NO STE-Code rules. The purpose: measure how much a standard coding
# assistant accidentally conforms to STE-Code principles without being
# instructed to do so.
#
# CROSS-REFERENCE: `orchestrator.py` (sibling file)
#   - orchestrator.py:     STE-Code system prompt → tests/run-*/
#   - orchestrator-control.py:  Plain system prompt → tests/control/run-*/
#   - Both run the same 59 test cases from test-cases/category-*.json
#   - Both use the SAME scoring engine (PRINCIPLE_KEYWORDS, check_principles,
#     calc_correctness) to ensure an apples-to-apples comparison
#
# SHARED CODE (~90% overlap with orchestrator.py lines 128-501):
#   Lines 129-484 of this file are functionally identical to the scoring,
#   aggregation, and reporting phases of orchestrator.py. This duplication
#   is INTENTIONAL for the following reasons:
#   1. Both files must produce bitwise-comparable aggregate JSON schemas
#   2. The scoring logic must never diverge between experiment and control
#   3. Any bug fix applied to one MUST be manually replicated in the other
#      (see MAINTENANCE NOTE below)
#   MAINTENANCE NOTE: When you change scoring/reporting logic in
#   orchestrator.py, also apply the same change to this file (lines 129-484).
#   A future refactor may extract shared code into benchmark_lib.py.
#
# ACCIDENTAL COMPLIANCE — WHY WE SCORE WITH STE-CODE KEYWORDS:
#   The control group assistant is NOT told about STE-Code principles. Yet
#   we score its output using the same PRINCIPLE_KEYWORDS dictionary (P1-P14)
#   and the same forbidden/expected keyword lists. This measures "accidental
#   compliance": how often a plain assistant happens to use approved terms,
#   avoid jargon, prefer short sentences, and so on.
#
#   This is a VALID experimental design, not an error:
#   - If the control group scores high, STE-Code rules add little value
#   - If the control group scores low (actual result: ~47% vs ~92% for
#     STE-Code), the rules provide measurable improvement
#   - The keyword-based scoring is a PROXY for principle adherence, not
#     a direct measure. A control-group output may mention "approved" or
#     "consistent" without actually following STE-Code rules. This proxy
#     is intentionally lenient — it gives the control group every benefit
#     of the doubt, making the comparison conservative.

import json, os, subprocess, time, sys, re, tempfile, glob
from collections import defaultdict
from datetime import datetime, timezone

# CLI: Optional command-line overrides (added before hardcoded defaults)
# The script works without any CLI arguments — all defaults are hardcoded
# below. When arguments are provided, they supersede the hardcoded values
# in the override block that follows the constants section.
import argparse as _argparse
_cli_parser = _argparse.ArgumentParser(
    description="Control Group Benchmark — plain assistant, no STE-Code prompt. "
                "Compares against STE-Code orchestrator results."
)
_cli_parser.add_argument(
    "--model", default=None,
    help="Model to use (default: poolside/laguna-s-2.1:free)"
)
_cli_parser.add_argument(
    "--timeout", type=int, default=None,
    help="Maximum wait time per worker in seconds (default: 600)"
)
_cli_parser.add_argument(
    "--compare", action="store_true",
    help="Run post-run delta report against the latest STE-Code results"
)
_cli_parser.add_argument(
    "--ste-results", default=None,
    help="Path to STE-Code aggregate JSON for comparison "
         "(auto-detects latest tests/run-*/aggregate-results.json if --compare set)"
)
_cli_parser.add_argument(
    "--retries", type=int, default=0,
    help="Number of retries for workers with empty or missing output (default: 0)"
)
_cli_parser.add_argument(
    "--no-report", action="store_true",
    help="Skip the terminal report and only write JSON files"
)
_cli_args, _ = _cli_parser.parse_known_args()

# SIGNAL HANDLING: Clean shutdown for parallel child processes
# When the user presses Ctrl+C, we must kill all forked worker processes
# to avoid orphaned hermes invocations. Without this handler, a SIGINT
# terminates only the parent while children keep running in the background.
import signal as _signal

_CHILD_PIDS = []  # Populated during Phase 1 — tracks all forked PIDs

def _cleanup_workers(signum=None, frame=None):
    """Kill all tracked child processes and exit cleanly."""
    if _CHILD_PIDS:
        print(f"\nSignal received. Cleaning up {len(_CHILD_PIDS)} worker processes...")
        for pid in _CHILD_PIDS:
            try:
                os.kill(pid, _signal.SIGTERM)
            except ProcessLookupError:
                pass  # Already exited
    print("All workers stopped. Exiting.")
    sys.exit(1)

_signal.signal(_signal.SIGINT, _cleanup_workers)
_signal.signal(_signal.SIGTERM, _cleanup_workers)

# Auto-detect project root (works on any machine)
# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT_ROOT = _repo_root(__file__)
TEST_DIR = os.path.join(PROJECT_ROOT, ".agents/benchmark/test-cases")
RESULTS_DIR = os.path.join(PROJECT_ROOT, ".agents/benchmark/tests/control")
MODEL = "poolside/laguna-s-2.1:free"

# ---- CLI overrides: supersede hardcoded defaults when arguments provided ----
if _cli_args.model is not None:
    MODEL = _cli_args.model
_CLI_MAX_WAIT = 600  # Default, overridden below if --timeout provided
if _cli_args.timeout is not None:
    _CLI_MAX_WAIT = _cli_args.timeout
_CLI_RETRIES = _cli_args.retries
_CLI_COMPARE = _cli_args.compare
_CLI_STE_RESULTS = _cli_args.ste_results
_CLI_NO_REPORT = _cli_args.no_report

# Plain system prompt — no STE-Code rules
SYSTEM_PROMPT = """You are a helpful coding assistant. Write clear, professional code documentation.
Use standard technical English. Be concise and accurate."""

# Load all test cases
test_cases = []
for cat_file in sorted(glob.glob(os.path.join(TEST_DIR, "category-*.json"))):
    with open(cat_file) as f:
        tests = json.load(f)
    for t in tests:
        t["_file"] = cat_file
        test_cases.append(t)

print(f"Control Group Benchmark (Plain Assistant)")
print(f"Model: {MODEL}")
print(f"Test cases loaded: {len(test_cases)}")
print(f"Launching {len(test_cases)} parallel workers...")
print()

# Create run directory
timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
run_dir = os.path.join(RESULTS_DIR, f"run-{timestamp}")
os.makedirs(run_dir, exist_ok=True)

# Phase 1: Launch all workers in parallel
workers = {}  # test_id -> {pid, out_file}

for tc in test_cases:
    tid = tc["id"]
    
    # Determine test type: correction (has "input") or generation (has "prompt")
    is_generation = "prompt" in tc
    task_input = tc.get("prompt", tc.get("input", ""))
    
    # Build full prompt based on type
    if is_generation:
        full_prompt = f"""{SYSTEM_PROMPT}

## TASK
{task_input}

IMPORTANT: Do NOT create any files. Output all code and documentation inline as text.
Be clear, concise, and professional."""
    else:
        full_prompt = f"""{SYSTEM_PROMPT}

## TASK
Check the following text for clarity and professionalism. Improve it if needed.
IMPORTANT: Do NOT create any files. Output the improved text inline.

## TEXT
{task_input}"""

    # Write prompt to temp file
    prompt_file = os.path.join(run_dir, f"{tid}-prompt.txt")
    with open(prompt_file, "w") as f:
        f.write(full_prompt)

    out_file = os.path.join(run_dir, f"{tid}-output.txt")

    # Launch fire-and-forget worker in isolated temp dir
    pid = os.fork()
    if pid == 0:
        # Child: isolate CWD to prevent root file leaks
        worker_dir = os.path.join(run_dir, f"worker-{tid}")
        os.makedirs(worker_dir, exist_ok=True)
        os.chdir(worker_dir)
        # Redirect stdout/stderr to output file
        with open(out_file, "w") as outf:
            os.dup2(outf.fileno(), 1)
            os.dup2(outf.fileno(), 2)
        os.execvp("hermes", ["hermes", "-z", full_prompt, "-m", MODEL, "--yolo"])
        os._exit(1)  # should not reach
    
    workers[tid] = {"pid": pid, "out_file": out_file, "start_time": time.time()}
    _CHILD_PIDS.append(pid)  # Track for signal handler cleanup

print(f"All {len(workers)} workers launched. Waiting for completion...")
print()

# Phase 2: Wait for all workers
MAX_WAIT = 600  # 10 minute timeout
# ---- CLI timeout override (applied after hardcoded default) ----
if _cli_args.timeout is not None:
    MAX_WAIT = _cli_args.timeout
poll_interval = 5
elapsed = 0

pending = set(workers.keys())
while pending and elapsed < MAX_WAIT:
    time.sleep(poll_interval)
    elapsed += poll_interval
    
    just_finished = []
    for tid in list(pending):
        pid = workers[tid]["pid"]
        try:
            wpid, status = os.waitpid(pid, os.WNOHANG)
            if wpid != 0:
                just_finished.append(tid)
        except ChildProcessError:
            just_finished.append(tid)
    
    for tid in just_finished:
        pending.discard(tid)
    
    if just_finished:
        print(f"  [{len(workers)-len(pending)}/{len(workers)}] Completed: {', '.join(just_finished)}")
    elif elapsed % 30 == 0:
        print(f"  ... still waiting ({len(pending)} remaining, {elapsed}s elapsed)")

if pending:
    print(f"WARNING: {len(pending)} workers timed out: {', '.join(sorted(pending))}")

# RETRY LOGIC: Re-launch workers with empty, missing, or error output
# Some workers may produce empty output (model refused, API error, crash)
# or very short stub output (<20 chars). This block checks all outputs and
# re-launches failing workers up to _CLI_RETRIES times with a shorter timeout.
# Retried workers are tracked separately so their latency reflects total time.
# NOTE: This block runs BEFORE scoring because scoring depends on the output
# files. Timed-out workers from Phase 2 are included in the retry pool.

if _CLI_RETRIES > 0:
    _retry_pool = []
    for tc in test_cases:
        tid = tc["id"]
        out_file = workers[tid]["out_file"]
        # Check if output is missing, empty, or too short
        try:
            with open(out_file) as f:
                content = f.read()
            if len(content.strip()) < 20 or content.startswith("HERMES_ERROR"):
                _retry_pool.append(tid)
        except FileNotFoundError:
            _retry_pool.append(tid)

    if _retry_pool:
        print(f"\nRetry: {len(_retry_pool)} workers have empty/missing output. "
              f"Retrying up to {_CLI_RETRIES} time(s)...")
        _RETRY_TIMEOUT = max(MAX_WAIT // 3, 60)  # Shorter timeout for retries

        for _attempt in range(1, _CLI_RETRIES + 1):
            if not _retry_pool:
                break

            print(f"  Retry attempt {_attempt}/{_CLI_RETRIES} for {len(_retry_pool)} workers...")
            _still_failing = []

            for tid in list(_retry_pool):
                tc = next(t for t in test_cases if t["id"] == tid)
                task_input = tc.get("prompt", tc.get("input", ""))
                is_generation = "prompt" in tc

                if is_generation:
                    full_prompt = f"""{SYSTEM_PROMPT}

## TASK
{task_input}

IMPORTANT: Do NOT create any files. Output all code and documentation inline as text.
Be clear, concise, and professional."""
                else:
                    full_prompt = f"""{SYSTEM_PROMPT}

## TASK
Check the following text for clarity and professionalism. Improve it if needed.
IMPORTANT: Do NOT create any files. Output the improved text inline.

## TEXT
{task_input}"""

                out_file = workers[tid]["out_file"]
                # Re-fork
                pid = os.fork()
                if pid == 0:
                    worker_dir = os.path.join(run_dir, f"worker-{tid}-retry{_attempt}")
                    os.makedirs(worker_dir, exist_ok=True)
                    os.chdir(worker_dir)
                    with open(out_file, "w") as outf:
                        os.dup2(outf.fileno(), 1)
                        os.dup2(outf.fileno(), 2)
                    os.execvp("hermes", ["hermes", "-z", full_prompt, "-m", MODEL, "--yolo"])
                    os._exit(1)

                workers[tid]["pid"] = pid
                workers[tid]["retry_attempt"] = _attempt
                _CHILD_PIDS.append(pid)

            # Wait for retried workers (shorter timeout)
            _retry_pending = set(_retry_pool)
            _retry_elapsed = 0
            while _retry_pending and _retry_elapsed < _RETRY_TIMEOUT:
                time.sleep(poll_interval)
                _retry_elapsed += poll_interval
                _finished = []
                for tid in list(_retry_pending):
                    pid = workers[tid]["pid"]
                    try:
                        wpid, status = os.waitpid(pid, os.WNOHANG)
                        if wpid != 0:
                            _finished.append(tid)
                    except ChildProcessError:
                        _finished.append(tid)
                for tid in _finished:
                    _retry_pending.discard(tid)

            # Check which retried workers still have bad output
            for tid in _retry_pool:
                out_file = workers[tid]["out_file"]
                try:
                    with open(out_file) as f:
                        content = f.read()
                    if len(content.strip()) < 20 or content.startswith("HERMES_ERROR"):
                        _still_failing.append(tid)
                except FileNotFoundError:
                    _still_failing.append(tid)

            _retry_pool = _still_failing

        if _retry_pool:
            print(f"  WARNING: {len(_retry_pool)} workers still failing after "
                  f"{_CLI_RETRIES} retries: {', '.join(sorted(_retry_pool))}")
        else:
            print("  All retried workers now have output.")

print()
print("All workers finished. Scoring...")
print()

# SCORING ENGINE — Shared with orchestrator.py (lines 133-228)
# The PRINCIPLE_KEYWORDS dictionary, extract_corrected_text(),
# extract_compliance_section(), check_principles(), check_keywords(), and
# calc_correctness() are IDENTICAL to orchestrator.py.
#
# DESIGN NOTE — Accidental Compliance Measurement:
#   These functions score STE-Code principle adherence using keyword heuristics
#   even though the control group assistant was NEVER told about STE-Code.
#   This is intentional: it measures how much a plain assistant happens to
#   produce text that looks STE-Code-compliant by coincidence.
#
#   A control-group output that mentions "approved" or "consistent" gets
#   partial credit even if the assistant was not consciously applying P1 or
#   P11. This makes the scoring lenient toward the control group — a
#   conservative experimental design that avoids inflating the STE-Code
#   advantage. Any delta between STE-Code and control scores is therefore
#   a lower bound on the true improvement.

# Phase 3: Score each output
PRINCIPLE_KEYWORDS = {
    "P1":  ["approved", "dictionary"],
    "P2":  ["part of speech"],
    "P3":  ["meaning"],
    "P4":  ["verb", "active voice", "passive", "imperative"],
    "P5":  ["technical", "noun", "keyword", "framework"],
    "P6":  ["non-approved"],
    "P7":  ["noun as verb", "technical noun"],
    "P8":  ["standard", "well-known"],
    "P9":  ["short", "clear"],
    "P10": ["slang", "jargon", "regional", "vague", "informal"],
    "P11": ["consistent", "one term", "synonym"],
    "P12": ["technical verb", "build", "deploy", "test", "lint"],
    "P13": ["verb as noun"],
    "P14": ["american", "spelling", "color", "analyze"],
}

def extract_corrected_text(output):
    """Extract corrected text - handle multiple output formats."""
    for marker in [r'\*\*Corrected Text:\*\*', r'## Corrected Text', r'CORRECTED TEXT',
                   r'# Corrected Text', r'Corrected Text \(STE-Code Compliant\)',
                   r'# STE-Code Corrected Text']:
        m = re.search(marker + r'\s*\n+(.*?)(?:\n---\n|\n## Compliance|\n# Compliance|\nCOMPLIANCE|\n\*\*Compliance)', output, re.DOTALL | re.IGNORECASE)
        if m and m.group(1).strip():
            return m.group(1).strip()
    m = re.search(r'^(.*?)(?:\n---\n|\n#+\s*Compliance|\nCOMPLIANCE)', output, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
        text = re.sub(r'^#+\s*(?:Corrected|STE-Code).*?\n+', '', text, flags=re.IGNORECASE)
        if text: return text.strip()
    return output.strip()

def extract_compliance_section(output):
    """Extract compliance summary - handle multiple formats."""
    for marker in [r'\*\*Compliance Summary\*\*', r'## Compliance Summary', r'COMPLIANCE SUMMARY',
                   r'# Compliance Summary', r'Compliance Summary']:
        m = re.search(re.escape(marker) if '**' in marker else marker + r'\s*\n(.*)', output, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() if m.lastindex else m.group(0)
    return ""

def check_principles(output, expected_principles):
    """Check principles in BOTH compliance section AND full output."""
    compliance = extract_compliance_section(output)
    full_lower = (compliance + " " + output).lower()
    
    satisfied = []
    missed = []
    
    for p in expected_principles:
        found = False
        # 1. Explicit principle number mention in compliance
        if re.search(r'\b' + re.escape(p) + r'\b', compliance):
            found = True
        # 2. Keyword heuristics
        if not found and p in PRINCIPLE_KEYWORDS:
            for kw in PRINCIPLE_KEYWORDS[p]:
                if kw.lower() in full_lower:
                    found = True
                    break
        # 3. Also check full output for principle number
        if not found and re.search(r'\b' + re.escape(p) + r'\b', output):
            found = True
        
        if found:
            satisfied.append(p)
        else:
            missed.append(p)
    
    return satisfied, missed

def check_keywords(text_lower, keywords):
    """Check which keywords appear in text."""
    found = []
    for kw in keywords:
        if kw.lower() in text_lower:
            found.append(kw)
    return found

def calc_correctness(expected_principles, satisfied, forbidden_found, total_forbidden, expected_kw_found, total_expected_kw):
    """Calculate correctness score 0-1 using weighted formula."""
    score = 0.4  # base
    
    # Principle compliance: 60% weight
    if expected_principles:
        score += 0.6 * len(satisfied) / len(expected_principles)
    
    # Forbidden keywords penalty: deduct up to 0.3
    if total_forbidden > 0:
        score -= 0.3 * len(forbidden_found) / total_forbidden
    
    # Expected keywords bonus: add up to 0.1
    if total_expected_kw > 0:
        score += 0.1 * len(expected_kw_found) / total_expected_kw
    
    return round(max(0.0, min(1.0, score)), 2)

results = []
category_stats = defaultdict(lambda: {"passed": 0, "failed": 0, "scores": [], "latencies": []})

for tc in test_cases:
    tid = tc["id"]
    cat = tc["category"]
    is_generation = "prompt" in tc
    task_text = tc.get("prompt", tc.get("input", ""))
    out_file = workers[tid]["out_file"]
    
    # Read output
    try:
        with open(out_file) as f:
            output = f.read()
    except FileNotFoundError:
        output = "OUTPUT_FILE_MISSING"
    
    latency_ms = int((time.time() - workers[tid]["start_time"]) * 1000)
    
    # Extract corrected text
    corrected = extract_corrected_text(output)
    corrected_lower = corrected.lower()
    
    # Check principles
    satisfied, missed = check_principles(output, tc["expected_principles"])
    
    # Check forbidden keywords (only in corrected text, not compliance summary)
    forbidden = tc.get("forbidden_keywords", [])
    forbidden_found = check_keywords(corrected_lower, forbidden)
    
    # Check expected keywords in corrected text
    expected_kw = tc.get("expected_keywords", [])
    expected_found = check_keywords(corrected_lower, expected_kw)
    
    # Check required patterns (for generation tests)
    required_patterns = tc.get("required_patterns", [])
    patterns_found = []
    patterns_missed = []
    for pat in required_patterns:
        if re.search(pat, output, re.IGNORECASE | re.DOTALL):
            patterns_found.append(pat)
        else:
            patterns_missed.append(pat)
    
    # Calculate correctness (single call with all params)
    correctness = calc_correctness(tc["expected_principles"], satisfied, forbidden_found, len(forbidden),
                                   expected_found, len(expected_kw))
    
    # Penalty for missing required patterns
    if required_patterns:
        pattern_penalty = 0.2 * len(patterns_missed) / len(required_patterns)
        correctness = round(max(0.0, correctness - pattern_penalty), 2)
    
    # Token estimation (handle both input and prompt)
    task_text = tc.get("prompt", tc.get("input", ""))
    token_input = len(task_text) // 4
    token_output = len(corrected) // 4
    
    # Pass/fail threshold
    passed = correctness >= 0.7
    
    # Notes
    notes_parts = []
    if missed:
        notes_parts.append(f"Missed: {', '.join(missed)}")
    if forbidden_found:
        notes_parts.append(f"Forbidden found: {', '.join(forbidden_found)}")
    if expected_found:
        notes_parts.append(f"Keywords OK: {len(expected_found)}/{len(expected_kw)}")
    if patterns_missed:
        notes_parts.append(f"Patterns missed: {', '.join(patterns_missed)}")
    
    result = {
        "test_id": tid,
        "category": cat,
        "description": tc.get("description", ""),
        "input": task_text,
        "test_type": "generation" if is_generation else "correction",
        "output": corrected,
        "compliance_summary": extract_compliance_section(output),
        "expected_principles_satisfied": satisfied,
        "expected_principles_missed": missed,
        "forbidden_keywords_found": forbidden_found,
        "expected_keywords_found": expected_found,
        "correctness_score": correctness,
        "latency_ms": latency_ms,
        "token_count_input": token_input,
        "token_count_output": token_output,
        "diff_ratio": 0.0,  # Would need expected output text for real diff
        "passed": passed,
        "notes": "; ".join(notes_parts) if notes_parts else "All checks passed",
        "difficulty": tc.get("difficulty", "unknown"),
    }
    results.append(result)
    
    # Track category stats
    if passed:
        category_stats[cat]["passed"] += 1
    else:
        category_stats[cat]["failed"] += 1
    category_stats[cat]["scores"].append(correctness)
    category_stats[cat]["latencies"].append(latency_ms)

# Phase 4: Aggregate
passed_count = sum(1 for r in results if r["passed"])
failed_count = len(results) - passed_count

scores = [r["correctness_score"] for r in results]
latencies = [r["latency_ms"] for r in results]
tokens_in = [r["token_count_input"] for r in results]
tokens_out = [r["token_count_output"] for r in results]

aggregate = {
    "benchmark_id": "ste-code-v1.0.0",
    "group": "control",  # Distinguishes control from STE-Code experiment runs
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "model": MODEL,
    "total_tests": len(results),
    "passed": passed_count,
    "failed": failed_count,
    "pass_rate_pct": round(passed_count / len(results) * 100, 1),
    "aggregates": {
        "avg_correctness": round(sum(scores) / len(scores), 3),
        "min_correctness": min(scores),
        "max_correctness": max(scores),
        "avg_latency_ms": round(sum(latencies) / len(latencies)),
        "min_latency_ms": min(latencies),
        "max_latency_ms": max(latencies),
        "avg_token_input": round(sum(tokens_in) / len(tokens_in)),
        "avg_token_output": round(sum(tokens_out) / len(tokens_out)),
        "total_tokens_input": sum(tokens_in),
        "total_tokens_output": sum(tokens_out),
    },
    "by_category": {},
    "by_difficulty": {},
    "failures": [r for r in results if not r["passed"]],
    "recommendations": [],
}

# By category
for cat in sorted(category_stats.keys()):
    s = category_stats[cat]
    aggregate["by_category"][cat] = {
        "passed": s["passed"],
        "failed": s["failed"],
        "total": s["passed"] + s["failed"],
        "avg_correctness": round(sum(s["scores"]) / len(s["scores"]), 3),
        "avg_latency_ms": round(sum(s["latencies"]) / len(s["latencies"])),
    }

# By difficulty
diff_stats = defaultdict(lambda: {"passed": 0, "failed": 0, "scores": []})
for r in results:
    d = r["difficulty"]
    if r["passed"]:
        diff_stats[d]["passed"] += 1
    else:
        diff_stats[d]["failed"] += 1
    diff_stats[d]["scores"].append(r["correctness_score"])

for diff in ["easy", "medium", "hard"]:
    if diff in diff_stats:
        s = diff_stats[diff]
        aggregate["by_difficulty"][diff] = {
            "passed": s["passed"],
            "failed": s["failed"],
            "total": s["passed"] + s["failed"],
            "avg_correctness": round(sum(s["scores"]) / len(s["scores"]), 3),
        }

# Recommendations
if aggregate["aggregates"]["avg_correctness"] < 0.7:
    aggregate["recommendations"].append("System prompt needs improvement — avg correctness below 0.7")
if aggregate["aggregates"]["avg_latency_ms"] > 5000:
    aggregate["recommendations"].append("Latency above 5s average — consider flash model for simple cases")
for cat, data in aggregate["by_category"].items():
    if data["avg_correctness"] < 0.6:
        aggregate["recommendations"].append(f"Category '{cat}' underperforming (avg {data['avg_correctness']}) — review test design or prompt coverage")

# Write results
agg_file = os.path.join(run_dir, "aggregate-results.json")
with open(agg_file, "w") as f:
    json.dump(aggregate, f, indent=2)

details_file = os.path.join(run_dir, "per-test-results.json")
with open(details_file, "w") as f:
    json.dump(results, f, indent=2)

# Phase 5: Print report
if not _CLI_NO_REPORT:
    print()
    print("=" * 70)
    print("  STE-CODE BENCHMARK RESULTS")
    print("=" * 70)
    print(f"  Model:      {MODEL}")
    print(f"  Timestamp:  {aggregate['timestamp']}")
    print(f"  Total:      {aggregate['total_tests']} tests")
    print(f"  Passed:     {aggregate['passed']} ({aggregate['pass_rate_pct']}%)")
    print(f"  Failed:     {aggregate['failed']}")
    print()
    print(f"  Averages:")
    print(f"    Correctness:  {aggregate['aggregates']['avg_correctness']:.3f}  (range: {aggregate['aggregates']['min_correctness']:.2f}–{aggregate['aggregates']['max_correctness']:.2f})")
    print(f"    Latency:      {aggregate['aggregates']['avg_latency_ms']}ms  (range: {aggregate['aggregates']['min_latency_ms']}–{aggregate['aggregates']['max_latency_ms']}ms)")
    print(f"    Tokens in:    {aggregate['aggregates']['avg_token_input']} avg  ({aggregate['aggregates']['total_tokens_input']} total)")
    print(f"    Tokens out:   {aggregate['aggregates']['avg_token_output']} avg  ({aggregate['aggregates']['total_tokens_output']} total)")
    print()

    # Category breakdown table
    print("-" * 70)
    print(f"  {'Category':<15} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Rate':>7} {'Avg Score':>10} {'Avg Lat':>8}")
    print("-" * 70)
    for cat in sorted(aggregate["by_category"].keys()):
        d = aggregate["by_category"][cat]
        rate = round(d["passed"] / d["total"] * 100) if d["total"] else 0
        print(f"  {cat:<15} {d['total']:>6} {d['passed']:>7} {d['failed']:>7} {rate:>6}% {d['avg_correctness']:>10.3f} {d['avg_latency_ms']:>7}ms")
    print("-" * 70)

    # Difficulty breakdown
    print()
    print(f"  {'Difficulty':<12} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Avg Score':>10}")
    print("-" * 45)
    for diff in ["easy", "medium", "hard"]:
        if diff in aggregate["by_difficulty"]:
            d = aggregate["by_difficulty"][diff]
            print(f"  {diff:<12} {d['total']:>6} {d['passed']:>7} {d['failed']:>7} {d['avg_correctness']:>10.3f}")

    # Per-test detail
    print()
    print("-" * 70)
    print(f"  {'ID':<12} {'Category':<12} {'Score':>6} {'Latency':>8} {'Result':>7}  Notes")
    print("-" * 70)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  {r['test_id']:<12} {r['category']:<12} {r['correctness_score']:>6.2f} {r['latency_ms']:>7}ms {status:>7}  {r['notes'][:60]}")
    print("-" * 70)

    # Failures detail
    failures = [r for r in results if not r["passed"]]
    if failures:
        print()
        print(f"FAILURES ({len(failures)})")
        for r in failures:
            print(f"  {r['test_id']} ({r['category']}, {r['difficulty']}): score={r['correctness_score']}")
            print(f"    Input:  {r['input'][:80]}...")
            print(f"    Output: {r['output'][:80]}...")
            print(f"    Missed principles: {r['expected_principles_missed']}")
            print(f"    Forbidden found:   {r['forbidden_keywords_found']}")
            print()

    # Recommendations
    if aggregate["recommendations"]:
        print("RECOMMENDATIONS")
        for rec in aggregate["recommendations"]:
            print(f"  • {rec}")

    print()
    print(f"Full results: {run_dir}/")
    print(f"Aggregate:    {agg_file}")
    print(f"Per-test:     {details_file}")
    print()
    print("Done.")

# Phase 6: Post-Run Delta Report — Control vs STE-Code Comparison
# Automatically loads the latest STE-Code aggregate JSON (from tests/run-*/)
# and prints a side-by-side delta report. Activated by --compare flag or
# called explicitly. If --ste-results is provided, uses that file directly.
# Falls back to auto-detecting the most recent STE-Code run directory.
#
# This comparison is the whole point of the control group: quantify the
# difference that STE-Code system prompt instructions make vs a plain
# assistant. Without this automated step, you must manually open both
# aggregate JSON files and compute deltas by hand.

def _find_latest_ste_run():
    """Auto-detect the most recent STE-Code results directory.

    Searches PROJECT_ROOT/.agents/benchmark/tests/run-*/ for the
    newest aggregate-results.json (NOT tests/control — those are us).
    Returns path to aggregate JSON or None if not found.
    """
    ste_results_dir = os.path.join(PROJECT_ROOT, ".agents/benchmark", "tests")
    if not os.path.isdir(ste_results_dir):
        return None

    run_dirs = sorted(glob.glob(os.path.join(ste_results_dir, "run-*")), reverse=True)
    for rd in run_dirs:
        agg_path = os.path.join(rd, "aggregate-results.json")
        if os.path.isfile(agg_path):
            return agg_path
    return None


def _load_aggregate(path):
    """Safely load a benchmark aggregate JSON file. Returns dict or None."""
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        print(f"  NOTE: Cannot load {path}: {e}")
        return None


def _print_delta_report(control_agg, ste_agg):
    """Print a side-by-side delta report: control vs STE-Code.

    Shows pass rate deltas, average score deltas, per-category improvements,
    and the categories where STE-Code provides the largest benefit.
    All deltas are STE-Code minus control (positive = STE-Code wins).
    """
    print()
    print("=" * 70)
    print("  DELTA REPORT: Control vs STE-Code")
    print("=" * 70)

    # --- Top-level deltas ---
    c_pass = control_agg.get("pass_rate_pct", 0)
    s_pass = ste_agg.get("pass_rate_pct", 0)
    c_avg = control_agg.get("aggregates", {}).get("avg_correctness", 0)
    s_avg = ste_agg.get("aggregates", {}).get("avg_correctness", 0)
    c_lat = control_agg.get("aggregates", {}).get("avg_latency_ms", 0)
    s_lat = ste_agg.get("aggregates", {}).get("avg_latency_ms", 0)

    print(f"  {'Metric':<22} {'Control':>10} {'STE-Code':>10} {'Delta':>10}")
    print("-" * 55)
    print(f"  {'Pass rate':<22} {c_pass:>9.1f}% {s_pass:>9.1f}% {(s_pass - c_pass):>+9.1f}%")
    print(f"  {'Avg correctness':<22} {c_avg:>10.3f} {s_avg:>10.3f} {(s_avg - c_avg):>+10.3f}")
    print(f"  {'Avg latency':<22} {c_lat:>9}ms {s_lat:>9}ms {(s_lat - c_lat):>+10}ms")
    print()

    # --- Per-category deltas ---
    c_cats = control_agg.get("by_category", {})
    s_cats = ste_agg.get("by_category", {})
    all_cats = sorted(set(list(c_cats.keys()) + list(s_cats.keys())))

    print(f"  {'Category':<16} {'Control':>8} {'STE-Code':>8} {'Delta':>8} {'Improvement':>12}")
    print("-" * 58)

    cat_deltas = []
    for cat in all_cats:
        c_score = c_cats.get(cat, {}).get("avg_correctness", 0)
        s_score = s_cats.get(cat, {}).get("avg_correctness", 0)
        delta = s_score - c_score
        cat_deltas.append((cat, c_score, s_score, delta))

    # Sort by delta descending (largest improvement first)
    cat_deltas.sort(key=lambda x: x[3], reverse=True)
    for cat, c_score, s_score, delta in cat_deltas:
        bar = "+" * max(0, min(10, int(delta * 10))) if delta > 0 else ""
        print(f"  {cat:<16} {c_score:>8.3f} {s_score:>8.3f} {delta:>+8.3f} {bar:<12}")

    print()

    # --- Top 3 winners ---
    winners = cat_deltas[:3]
    if winners:
        print("  Top 3 categories where STE-Code helps most:")
        for i, (cat, c_score, s_score, delta) in enumerate(winners, 1):
            print(f"    {i}. {cat}: +{delta:.3f} (control={c_score:.3f}, ste={s_score:.3f})")
        print()

    # --- Negative deltas (control beats STE-Code) ---
    losers = [d for d in cat_deltas if d[3] < -0.02]
    if losers:
        print(f"  Categories where control OUTPERFORMS STE-Code ({len(losers)}):")
        for cat, c_score, s_score, delta in losers:
            print(f"    {cat}: {delta:.3f} (control={c_score:.3f}, ste={s_score:.3f})")
        print("  NOTE: Negative deltas may indicate scoring proxy limitations")
        print("        (keyword match does not guarantee principle adherence)")
        print()

    # --- Overall verdict ---
    print("-" * 55)
    overall_delta = s_avg - c_avg
    if overall_delta > 0.2:
        verdict = "STRONG — STE-Code provides substantial improvement"
    elif overall_delta > 0.1:
        verdict = "MODERATE — STE-Code provides meaningful improvement"
    elif overall_delta > 0.0:
        verdict = "MODEST — STE-Code provides small but measurable improvement"
    elif overall_delta == 0.0:
        verdict = "NEGLIGIBLE — no measurable difference"
    else:
        verdict = "NEGATIVE — control outperforms STE-Code (check scoring proxy)"
    print(f"  Verdict: {verdict}")
    print(f"  Net correctness gain: {overall_delta:+.3f}")
    print(f"  Pass rate improvement: {s_pass - c_pass:+.1f}%")
    print("=" * 70)


# --- Execute comparison if requested ---
if _CLI_COMPARE or _CLI_STE_RESULTS:
    ste_agg_path = _CLI_STE_RESULTS or _find_latest_ste_run()

    if ste_agg_path is None:
        print("\nNOTE: No STE-Code results found for comparison.")
        print("  Run orchestrator.py first to generate STE-Code benchmark results.")
        print("  Or use --ste-results PATH to specify the aggregate JSON file.")
    else:
        ste_agg = _load_aggregate(ste_agg_path)
        if ste_agg is not None:
            _print_delta_report(aggregate, ste_agg)
        else:
            print(f"\nNOTE: Could not load STE-Code results from: {ste_agg_path}")
