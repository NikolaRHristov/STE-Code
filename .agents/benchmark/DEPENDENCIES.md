# Benchmark Dependencies

All benchmark scripts (`run.py`, `orchestrator.py`, `orchestrator-control.py`,
`rescore.py`, `enlarge-ste-code.py`) share one hard external dependency: the
`hermes` CLI binary. Everything else is Python standard library.

---

## `hermes` — Required External Binary

`hermes` is a local CLI wrapper around the DeepSeek API. It is **not** a
standard open-source package and is not committed to this repository.

### What it does

Accepts a prompt string, calls the DeepSeek API with the specified model, and
writes the model response to stdout.

### Required invocation form

```bash
hermes -z "<full prompt text>" -m poolside/laguna-s-2.1:free --yolo
```

| Flag | Meaning |
|---|---|
| `-z` | Pass the argument as a combined system+user prompt (zero-shot single-string mode) |
| `-m <model>` | Model name. All benchmark scripts hardcode `poolside/laguna-s-2.1:free`. |
| `--yolo` | Skip all interactive confirmation prompts. Required for unattended batch runs. |

### Expected location

`hermes` must be on `PATH`. Verify with:

```bash
which hermes && hermes --version
```

### Model

All benchmark scripts use `poolside/laguna-s-2.1:free`. The model name is hardcoded in
each script as `MODEL = "poolside/laguna-s-2.1:free"`. To override, edit the `MODEL`
constant at the top of the relevant script.

### API credentials

`hermes` reads credentials from the environment. Set the required environment
variable before running any benchmark script:

```bash
export DEEPSEEK_API_KEY="<your key>"
```

(The exact variable name may differ depending on your `hermes` build.
Check `hermes --help` if the above does not work.)

---

## Python Requirements

All benchmark scripts run on Python 3.9+. No third-party packages are required.
The following standard library modules are used:

| Module | Used by |
|---|---|
| `subprocess` | `orchestrator.py`, `orchestrator-control.py`, `enlarge-ste-code.py`, `run.py` |
| `os`, `sys`, `time` | all scripts |
| `json` | all scripts |
| `re` | `benchmark_lib.py`, `orchestrator.py`, `rescore.py` |
| `glob` | `benchmark_lib.py`, `rescore.py` |
| `difflib` | `orchestrator.py`, `rescore.py` (SequenceMatcher for diff_ratio) |
| `typing` | `benchmark_lib.py` |
| `argparse` | `rescore.py`, `run.py` |

---

## Results Directories

| Directory | Status | Populated by |
|---|---|---|
| `results-v2/` | ✅ Has runs | `orchestrator.py` + `rescore.py` |
| `results-control/` | ⚠️ Empty | `orchestrator-control.py` + `rescore.py` (not yet run) |

See `results-control/README.md` for how to populate the control baseline.
