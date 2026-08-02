# Benchmark output

Empty by design. Every benchmark run writes here and nowhere else.

```
.agents/benchmark/tests/
  <run-name>/            one directory per run
    run-<timestamp>/     one directory per attempt
```

## One output root

Each runner defaults into this directory:

| Runner | Flag |
|---|---|
| `orchestrator.py` | `--results-dir <name>` |
| `orchestrator-control.py` | `--results-dir <name>` |
| `benchmark-levels.py` | `--results-dir <name>` |
| `run_pipeline.py` | `--base <name>` |
| `run_all_variations.py` | `--base <name>` |

Pass a **bare name**, not a path. A bare name resolves to a subdirectory
here; an absolute path outside this tree is rejected. Under the `bench` jail
policy the kernel refuses the write as well, so a runner cannot scatter
output across the machine even when a prompt asks it to.

## Reset

```bash
rm -rf .agents/benchmark/tests/*
```

Nothing here is an input. Test cases live in `../test-cases/`, configuration
in `../config/`, and the tiered prompts in the artifacts tree.
