#!/usr/bin/env python3
"""Re-score benchmark outputs with fixed extraction logic.
Usage: python3 rescore.py [run_dir]
  If run_dir not provided, uses the latest run in results/"""
import json, os, re, glob, sys
from collections import defaultdict

# Auto-detect paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
TEST_DIR = os.path.join(PROJECT_ROOT, ".agents/benchmark/test-cases")
RESULTS_DIR = os.path.join(PROJECT_ROOT, ".agents/benchmark/results")

# Use provided run dir or find latest
if len(sys.argv) > 1:
    RUN_DIR = sys.argv[1]
else:
    runs = sorted(glob.glob(os.path.join(RESULTS_DIR, "run-*")))
    RUN_DIR = runs[-1] if runs else None

if not RUN_DIR or not os.path.isdir(RUN_DIR):
    print(f"ERROR: No run directory found. Usage: python3 rescore.py [run_dir]")
    sys.exit(1)

print(f"Re-scoring: {RUN_DIR}")

# Load test cases
test_map = {}
for cat_file in sorted(glob.glob(os.path.join(TEST_DIR, "category-*.json"))):
    with open(cat_file) as f:
        for t in json.load(f):
            test_map[t["id"]] = t

def extract_corrected_text(output):
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
    for marker in [r'\*\*Compliance Summary\*\*', r'## Compliance Summary', r'COMPLIANCE SUMMARY',
                   r'# Compliance Summary', r'Compliance Summary']:
        m = re.search(re.escape(marker) if '**' in marker else marker + r'\s*\n(.*)', output, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() if m.lastindex else m.group(0)
    return ""

PRINCIPLE_KEYWORDS = {
    "P1":["approved word","dictionary","unapproved"],"P2":["part of speech"],"P3":["meaning","approved meaning"],
    "P4":["active voice","passive voice","imperative","passive"],"P5":["sentence length","word limit","procedural sentence"],
    "P6":["technical noun","technical code"],"P7":["noun as verb"],"P8":["standard","well-known"],
    "P9":["short","clear","wordiness","concise"],"P10":["slang","jargon","regional","vague","informal","filler"],
    "P11":["consistent","one term","synonym"],"P12":["technical verb"],"P13":["verb as noun"],"P14":["american","spelling"],
}

def check_principles(output, expected_principles):
    compliance = extract_compliance_section(output)
    full_lower = (compliance + " " + output).lower()
    satisfied, missed = [], []
    for p in expected_principles:
        found = False
        if re.search(r'\b' + re.escape(p) + r'\b', compliance): found = True
        if not found and p in PRINCIPLE_KEYWORDS:
            for kw in PRINCIPLE_KEYWORDS[p]:
                if kw.lower() in full_lower: found = True; break
        if not found and re.search(r'\b' + re.escape(p) + r'\b', output): found = True
        if found: satisfied.append(p)
        else: missed.append(p)
    return satisfied, missed

def check_keywords(text_lower, keywords):
    return [kw for kw in keywords if kw.lower() in text_lower]

def calc_correctness(expected_principles, satisfied, forbidden_found, total_forbidden, expected_kw_found, total_expected_kw):
    score = 0.4
    if expected_principles: score += 0.6 * len(satisfied) / len(expected_principles)
    if total_forbidden > 0: score -= 0.3 * len(forbidden_found) / total_forbidden
    if total_expected_kw > 0: score += 0.1 * len(expected_kw_found) / total_expected_kw
    return round(max(0.0, min(1.0, score)), 2)

# Re-score
results = []
category_stats = defaultdict(lambda: {"passed": 0, "failed": 0, "scores": []})

for test_id, tc in sorted(test_map.items()):
    out_file = os.path.join(RUN_DIR, f"{test_id}-output.txt")
    if not os.path.exists(out_file):
        print(f"  SKIP {test_id}: no output file")
        continue
    
    with open(out_file) as f:
        output = f.read()
    
    cat = tc["category"]
    corrected = extract_corrected_text(output)
    corrected_lower = corrected.lower()
    
    satisfied, missed = check_principles(output, tc["expected_principles"])
    forbidden = tc.get("forbidden_keywords", [])
    forbidden_found = check_keywords(corrected_lower, forbidden)
    expected_kw = tc.get("expected_keywords", [])
    expected_found = check_keywords(corrected_lower, expected_kw)
    
    correctness = calc_correctness(tc["expected_principles"], satisfied, forbidden_found, len(forbidden), expected_found, len(expected_kw))
    passed = correctness >= 0.7
    
    notes_parts = []
    if missed: notes_parts.append(f"Missed: {', '.join(missed)}")
    if forbidden_found: notes_parts.append(f"Forbidden: {', '.join(forbidden_found)}")
    if expected_found: notes_parts.append(f"Keywords: {len(expected_found)}/{len(expected_kw)}")
    
    results.append({
        "test_id": test_id, "category": cat, "description": tc.get("description", ""),
        "input": tc.get("prompt", tc.get("input", "")), "output": corrected,
        "compliance_summary": extract_compliance_section(output),
        "expected_principles": tc["expected_principles"],
        "expected_principles_satisfied": satisfied, "expected_principles_missed": missed,
        "forbidden_keywords": forbidden, "forbidden_keywords_found": forbidden_found,
        "expected_keywords": expected_kw, "expected_keywords_found": expected_found,
        "correctness_score": correctness, "passed": passed,
        "notes": "; ".join(notes_parts) if notes_parts else "All checks passed",
        "difficulty": tc.get("difficulty", "unknown"),
    })
    
    if passed: category_stats[cat]["passed"] += 1
    else: category_stats[cat]["failed"] += 1
    category_stats[cat]["scores"].append(correctness)

# Print summary
passed_count = sum(1 for r in results if r["passed"])
failed_count = len(results) - passed_count
scores = [r["correctness_score"] for r in results]

print(f"=== RE-SCORED RESULTS ===")
print(f"Total: {len(results)} | Passed: {passed_count} | Failed: {failed_count}")
print(f"Pass rate: {round(passed_count/len(results)*100,1)}%")
print(f"Avg correctness: {round(sum(scores)/len(scores),3)}")
print()

print(f"{'Category':<15} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Avg':>7}")
print("-" * 50)
for cat in sorted(category_stats.keys()):
    s = category_stats[cat]
    total = s["passed"] + s["failed"]
    avg = round(sum(s["scores"])/len(s["scores"]), 3) if s["scores"] else 0
    print(f"{cat:<15} {total:>6} {s['passed']:>7} {s['failed']:>7} {avg:>7.3f}")

print(f"\nRe-scored results saved: {RUN_DIR}/rescored-results.json")
