# Benchmark Suite

59 tests across 14 categories measure STE-Code compliance against a plain
assistant baseline.

## Results

| | STE-Code | Plain Assistant | Improvement |
|---|:------:|:------:|:------:|
| Pass rate | 96.6% (57/59) | 11.9% (7/59) | **+84.7%** |
| Avg score | 0.919 | 0.471 | **+0.448** |

## Categories

| # | Category | Tests | STE-Code Avg | Plain Avg | Delta |
|---|----------|:-----:|:------:|:------:|:-----:|
| 1 | README files | 5 | 0.92 | 0.48 | +0.44 |
| 2 | API documentation | 5 | 0.89 | 0.42 | +0.47 |
| 3 | Commit messages | 5 | 0.95 | 0.51 | +0.44 |
| 4 | Error messages | 5 | 0.93 | 0.37 | +0.56 |
| 5 | Code comments | 5 | 0.95 | 0.37 | +0.58 |
| 6 | Changelog entries | 4 | 0.91 | 0.44 | +0.47 |
| 7 | Config files | 4 | 0.90 | 0.38 | +0.52 |
| 8 | Composite documents | 4 | 0.88 | 0.45 | +0.43 |
| 9 | Generated function docs | 4 | 0.90 | 0.42 | +0.48 |
| 10 | Generated PR reviews | 4 | 0.89 | 0.40 | +0.49 |
| 11 | Generated API docs | 4 | 0.87 | 0.43 | +0.44 |
| 12 | Generated commit messages | 4 | 0.93 | 0.49 | +0.44 |
| 13 | Generated error messages | 4 | 0.91 | 0.39 | +0.52 |
| 14 | Generated README | 2 | 0.92 | 0.48 | +0.44 |

Top 3: **comments** (+0.580), **error messages** (+0.560), **config files** (+0.520).

## Running

```bash
# Full benchmark (59 tests, parallel)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, no STE-Code)
python3 .agents/benchmark/orchestrator-control.py

# Re-score a previous run
python3 .agents/benchmark/rescore.py results/run-YYYYMMDD-HHMMSS/

# Launch level workers (rewrites at levels 1-4)
python3 .agents/benchmark/launch-levels.py
```

Results are written to `.agents/benchmark/results/run-YYYYMMDD-HHMMSS/`.

## Scoring

Each test is scored against the 14 STE-Code principles. Keywords from the
synonym table are checked. Violations are weighted by severity. The aggregate
score is the mean across all tests in a category.
