# Benchmark: Running

```bash
# Full benchmark (59 tests, parallel workers)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, no STE-Code)
python3 .agents/benchmark/orchestrator-control.py

# Re-score a previous run
python3 .agents/benchmark/rescore.py results/run-YYYYMMDD-HHMMSS/

# Launch level workers (rewrites at levels 1-4)
python3 .agents/benchmark/launch-levels.py
```

Results: `.agents/benchmark/results/run-YYYYMMDD-HHMMSS/`
Control: `.agents/benchmark/results-control/run-YYYYMMDD-HHMMSS/`
