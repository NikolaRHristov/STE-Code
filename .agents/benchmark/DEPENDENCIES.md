# Benchmark Dependencies

## Purpose

This document lists everything the benchmark needs that the repository does not
carry: one external CLI binary and a Python interpreter. An operator reads it
before the first run to confirm the machine is ready.

## Footprint

| Kind     | Value                                                                           |
| -------- | ------------------------------------------------------------------------------- |
| Reads    | `.agents/benchmark/config/harness.json`, `.agents/config/defaults.yaml`         |
| Reads    | `.agents/benchmark/test-cases/`, the variant prompt under `ste-code/artifacts/` |
| Writes   | `.agents/benchmark/tests/<run-name>/run-<timestamp>/`                           |
| Requires | the `hermes` CLI on `PATH`, Python 3.9 or later                                 |

## Usage

Confirm both dependencies before a run:

    which hermes && hermes --version
    python3 --version

Then run the harness self-test, which needs no network:

    python3 .agents/benchmark/selftest.py

## Behaviour

- The runner shells out to the `hermes` CLI once per case and reads the response
  from stdout.
- The model name is supplied by the harness, never by the operator's shell
  environment.
- Every other benchmark module is offline and uses only the Python standard
  library.
- Results land under `.agents/benchmark/tests/`; nothing else in the tree is
  written.

## Configuration

Knobs live in configuration, never in a script.

| Key                                | File                                    | Meaning                                       |
| ---------------------------------- | --------------------------------------- | --------------------------------------------- |
| `runner.default_model`             | `.agents/benchmark/config/harness.json` | The configured model default for the harness  |
| `runner.default_max_workers`       | same                                    | Concurrent workers, default 2                 |
| `runner.default_timeout_s`         | same                                    | Per-worker wall-clock budget                  |
| `runner.argv_template`             | same                                    | The exact flags passed to the scoring backend |
| `agent.model`                      | `.agents/config/defaults.yaml`          | Shared default for the rest of the pipeline   |
| `agent.retries`, `agent.backoff_s` | same                                    | Retry policy for a failed call                |

The legacy entry points `orchestrator.py`, `orchestrator-control.py` and
`benchmark-levels.py` carry their own `--model` default of
`poolside/laguna-s-2.1:free`. Override it on the command line, or drive the run
through `harness_config.build_runner_argv()`, which supplies
`runner.default_model` from the profile document instead.

### The `hermes` CLI

`hermes` is a local CLI that sends a prompt to the configured model backend and
writes the response to stdout. It is not an open-source package and is not
committed to this repository. Backend and credential handling belong to the CLI,
not to the benchmark; see `.agents/config/agents.yaml` for the backend registry.

    hermes -z "<full prompt text>" -m <model> --yolo

| Flag         | Meaning                                                           |
| ------------ | ----------------------------------------------------------------- |
| `-z`         | Pass the argument as a combined system and user prompt            |
| `-m <model>` | Model name, supplied by the harness from configuration            |
| `--yolo`     | Skip interactive confirmation, required for unattended batch runs |

### Python

Python 3.9 or later. No third-party package is required. The modules used are
`subprocess`, `os`, `sys`, `time`, `json`, `re`, `glob`, `difflib`, `typing`,
`argparse`, `pathlib` and `dataclasses`. Shared file access goes through
`.agents/tools/lib/ste_io.py`, path resolution through `ste_paths.py`, and
pre-flight retry logic through `ste_runtime.py`.

## Failure modes

- `hermes` absent from `PATH`: every case fails immediately; `which hermes`
  returns nothing.
- Missing or invalid credentials in the CLI's own environment: the runner
  records a failed case and continues; the aggregate pass rate collapses to
  zero.
- HTTP 429 from the free tier above roughly three concurrent workers: lower
  `--max-workers` and let `agent.retries` and `agent.backoff_s` absorb the rest.
- Timeout at `runner.default_timeout_s`: the case is recorded as timed out and
  the run continues.
- Python older than 3.9: modules that use `from __future__ import annotations`
  still import, but newer syntax in the colour modules fails at compile time;
  `selftest.py` catches this.

## See also

- `CONTRACT.md` — genericity rules and the handshake protocol
- `tests/README.md` — where output goes and how to reset it
- `config/harness.json` — the profile document
- `../config/defaults.yaml` — shared agent defaults
- `../config/agents.yaml` — agent backend registry
