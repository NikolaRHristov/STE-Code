---
description: "Measure STE-Code correctness and performance against 59 tests across 14 categories. Includes control group comparison."
version: "2.0.0"
related: [".agents/benchmark/orchestrator.py", ".agents/benchmark/orchestrator-control.py", ".agents/benchmark/schema.json", ".agents/benchmark/test-cases/"]
---

# Benchmarking Orchestrator — Agent-Agnostic

Measure STE-Code correctness and performance against a defined test suite. Run pre-defined test cases through `hermes -z` with the STE-Code system prompt, compare outputs against expected results, and produce structured benchmark reports. A control group runs the same tests with a plain assistant prompt for comparison.

## Architecture

```
TEST CASES (14 categories, 59 tests) → hermes -z (deepseek-v4-pro) → SCORED RESULTS
```

### Categories

| # | Category | Tests | Type |
|---|----------|-------|------|
| 1 | readme | 5 | Correction |
| 2 | api_doc | 5 | Correction |
| 3 | commit | 5 | Correction |
| 4 | error | 5 | Correction |
| 5 | comment | 5 | Correction |
| 6 | changelog | 3 | Correction |
| 7 | config | 3 | Correction |
| 8 | composite | 4 | Correction |
| 9 | gen_function | 4 | Generation |
| 10 | gen_pr_review | 4 | Generation |
| 11 | gen_api_doc | 4 | Generation |
| 12 | gen_commit | 4 | Generation |
| 13 | gen_error | 4 | Generation |
| 14 | gen_readme | 4 | Generation |
| **Total** | | **59** | |

## Test Case Schema

Correction tests have `input` (text to fix). Generation tests have `prompt` (coding task) + `required_patterns` (regex structures that must appear).

```json
{
  "id": "bench-001",
  "category": "readme",
  "description": "README introduction with jargon",
  "input": "This library does a bunch of stuff...",
  "expected_principles": ["P1", "P4", "P10"],
  "expected_keywords": ["library", "call"],
  "forbidden_keywords": ["bunch", "stuff"],
  "required_patterns": [],
  "max_tokens": 300,
  "difficulty": "easy"
}
```

## Scoring Formula

```
score = 0.40 (base)
      + 0.60 × (principles_satisfied / expected)     ← 60% weight
      − 0.30 × (forbidden_found / total_forbidden)    ← penalty
      + 0.10 × (keywords_found / total_expected)      ← bonus
      − 0.20 × (patterns_missed / total_patterns)     ← gen-only
```

Pass threshold: ≥ 0.70

## Execution

```bash
# STE-Code benchmark (full 59 tests, parallel workers)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, same tests)
python3 .agents/benchmark/orchestrator-control.py

# Re-score existing outputs
python3 .agents/benchmark/rescore.py [run_dir]
```

## Results

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| Pass rate | 96.6% (57/59) | 11.9% (7/59) | +84.7% |
| Avg correctness | 0.919 | 0.471 | +0.448 |

## Output
- Per-test results: `.agents/benchmark/results/run-{timestamp}/per-test-results.json`
- Aggregate report: `.agents/benchmark/results/run-{timestamp}/aggregate-results.json`
- Control group: `.agents/benchmark/results-control/run-{timestamp}/`
- All prompt/output files gitignored — only aggregate JSONs tracked
