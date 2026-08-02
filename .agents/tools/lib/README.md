# tools/lib — shared helpers

Every script under `.agents/tools/<unit>/` imports from here. These modules are
the single source for cross-cutting behaviour; no unit re-implements them.

## Modules

- `repo_root.py` — locate the repo by marker (`.git` / `Makefile`), not by
  counting parent directories. `repo_root(path)` and `ensure_inside_repo(path)`.
- `ste_io.py` — **the only write path scripts should use.** `write_text`,
  `write_json`, `read_text`, `mkdir` — all confined to the repo by the jail
  policy. A `clean=True` escape hatch exists for operator-driven setup that is
  explicitly outside the pipeline; it can never widen the repo boundary.
- `ste_config.py` — per-unit configuration. `load(__file__)` reads the unit's
  `config.yaml` merged under `defaults.yaml` (agent + runtime keys only). Exposes
  `cfg.model`, `cfg.path(...)`, `cfg.pattern(...)`, `cfg.get(...)`.
- `ste_runtime.py` — pre-flight runtime resolution. `resolve(__file__)` computes
  the wrapper path, venv interpreter, retry count, batch divisor and encoding
  from the repo. The shared source of these knobs (see `defaults.yaml` `runtime:`).
- `ste_checkpoint.py` — atomic checkpoint load/save for crash-safe resume; routes
  through `ste_io`.
- `ste_paths.py` — `venv_python()` and `wrapper_path()` (agent runtime locations).
- `ste_time.py` — `run_stamp()`; the one run-stamp timestamp format.
- `ste_retry.py` — `retry()` with exponential backoff.
- `ste_cli.py` — argparse scaffolding for the entrypoints.

## Rule
If a script needs to write a file, read a config, resolve a path, or stamp a
run, it imports from `lib/` — it does not hand-roll `open(...,"w")`,
`str(Path.home()/".hermes"/...)`, or a timestamp format. This keeps the pipeline
DRY and the jail boundary honest.

## See also
- ../../config/defaults.yaml (shared agent + runtime defaults)
- ../README.md (per-unit index)
