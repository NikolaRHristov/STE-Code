# results-v2/

This directory holds benchmark outputs from `orchestrator.py` — the
STE-Code-instructed runs that measure model compliance with the 14
STE-Code principles (P1–P14).

## Run directory naming

Each run creates a subdirectory named:

```
original-YYYYMMDD-HHMMSS/
```

where the timestamp is the UTC wall-clock time at which the orchestrator
started. Example: `original-20260730-145213/`

## Per-run contents

Each test case produces two files:

| File | Contents |
|---|---|
| `bench-NNN-prompt.txt` | The full prompt sent to the model (system prompt + test input) |
| `bench-NNN-output.txt` | The raw model response |

After `rescore.py` processes a run directory, two additional files appear:

| File | Contents |
|---|---|
| `per-test-results.json` | Array of `TestResult` objects (one per bench-NNN) |
| `aggregate-report.json` | Single `AggregateReport` object with totals, by-category scores, and recommendations |

## Rescoring

```bash
# Score a specific run:
python .agents/benchmark/rescore.py --run-dir .agents/benchmark/results-v2/original-20260730-145213

# Score the most recent run:
python .agents/benchmark/rescore.py
```

## Schema

All JSON output conforms to `.agents/benchmark/schema.json`.
