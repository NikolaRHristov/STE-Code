# results-control/

This directory holds benchmark outputs from `orchestrator-control.py` — the
baseline (no STE-Code system prompt) runs used to measure the delta that
STE-Code instruction adds.

## Current state

This directory is intentionally empty. The control orchestrator
(`orchestrator-control.py`) has not yet been run against the current test
suite. Without control data there is no empirical baseline to compare the
`results-v2/` runs against.

## How to populate

```bash
# From the project root:
python .agents/benchmark/orchestrator-control.py
```

Outputs follow the same naming convention as `results-v2/`:

```
results-control/
  control-YYYYMMDD-HHMMSS/
    bench-001-prompt.txt
    bench-001-output.txt
    ...
    per-test-results.json     # written by rescore.py
    aggregate-report.json     # written by rescore.py
```

## A/B comparison

Once both `results-v2/<run>/aggregate-report.json` and
`results-control/<run>/aggregate-report.json` exist for the same test suite
version, compare `avg_correctness` and `by_category` scores to quantify
the improvement STE-Code instruction provides over the unguided baseline.
