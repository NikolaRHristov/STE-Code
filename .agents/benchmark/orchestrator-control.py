#!/usr/bin/env python3
"""Control Group Benchmark — plain coding assistant, no STE-Code rails. Same 59 tests."""

import json, os, subprocess, time, sys, re, tempfile, glob
from collections import defaultdict
from datetime import datetime, timezone

# Auto-detect project root (works on any machine)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
TEST_DIR = os.path.join(PROJECT_ROOT, ".agents/benchmark/test-cases")
RESULTS_DIR = os.path.join(PROJECT_ROOT, ".agents/benchmark/results-control")
MODEL = "deepseek-v4-pro"

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

print(f"=== Control Group Benchmark (Plain Assistant) ===")
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

print(f"All {len(workers)} workers launched. Waiting for completion...")
print()

# Phase 2: Wait for all workers
MAX_WAIT = 600  # 10 minute timeout
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

print()
print("=== All workers finished. Scoring... ===")
print()

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
    print(f"=== FAILURES ({len(failures)}) ===")
    for r in failures:
        print(f"  {r['test_id']} ({r['category']}, {r['difficulty']}): score={r['correctness_score']}")
        print(f"    Input:  {r['input'][:80]}...")
        print(f"    Output: {r['output'][:80]}...")
        print(f"    Missed principles: {r['expected_principles_missed']}")
        print(f"    Forbidden found:   {r['forbidden_keywords_found']}")
        print()

# Recommendations
if aggregate["recommendations"]:
    print("=== RECOMMENDATIONS ===")
    for rec in aggregate["recommendations"]:
        print(f"  • {rec}")

print()
print(f"Full results: {run_dir}/")
print(f"Aggregate:    {agg_file}")
print(f"Per-test:     {details_file}")
print()
print("Done.")
