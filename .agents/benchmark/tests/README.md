# Benchmark output

## Purpose

This directory is the single output root for every benchmark run. It is empty by
design and carries no inputs. An operator reads this to learn where results land
and how to reset them.

## Footprint

| Kind          | Value                                                               |
| ------------- | ------------------------------------------------------------------- |
| Inputs        | none — this tree is write-only for the harness                      |
| Outputs       | `.agents/benchmark/tests/<run-name>/run-<timestamp>/`               |
| Outputs       | `aggregate-results.json`, `per-test-results.json` per run directory |
| Configured by | `paths.results_base` in `../config/harness.json`                    |

```
.agents/benchmark/tests/
  <run-name>/            one directory per run
    run-<timestamp>/     one directory per attempt
```

## Usage

Each runner takes a bare run name and resolves it inside this directory:

    python3 .agents/benchmark/orchestrator.py --results-dir <name>
    python3 .agents/benchmark/orchestrator-control.py --results-dir <name>
    python3 .agents/benchmark/benchmark-levels.py --results-dir <name>
    python3 .agents/benchmark/run_pipeline.py --base <name>
    python3 .agents/benchmark/run_all_variations.py --base <name>

Reset the tree:

    rm -rf .agents/benchmark/tests/*

## Behaviour

- A bare name resolves to a subdirectory here; an absolute path outside this
  tree is rejected.
- Path resolution goes through `ste_paths`, which keeps a write inside the
  checkout.
- Under the `bench` jail policy the kernel refuses an outside write as well, so
  a runner cannot scatter output across the machine even when a prompt asks it
  to.
- Each attempt gets its own timestamped directory, so reruns never overwrite
  earlier evidence.
- Result filenames come from `runner.aggregate_filename` and
  `runner.per_test_filename`.

## Configuration

Knobs live in `../config/harness.json`, never in a runner.

| Key                            | Governs                                   |
| ------------------------------ | ----------------------------------------- |
| `paths.results_base`           | This directory                            |
| `runner.run_dir_glob`          | The `run-*` attempt pattern               |
| `runner.aggregate_filename`    | `aggregate-results.json`                  |
| `runner.per_test_filename`     | `per-test-results.json`                   |
| `handshake.round_dir_template` | Round layout for the adversarial pipeline |

## Failure modes

- A `--results-dir` given as an absolute path outside the repository is rejected
  before any write.
- A run interrupted part way leaves a timestamped directory without an aggregate
  file; treat a missing `aggregate-results.json` as "did not finish", not as a
  zero score.
- Deleting the tree deletes all historical evidence; nothing here is regenerated
  automatically.

## See also

- `../CONTRACT.md` — handshake protocol and record shapes
- `../DEPENDENCIES.md` — what a run needs on the machine
- `../config/harness.json` — the profile document
- `../test-cases/` — the static case corpus
