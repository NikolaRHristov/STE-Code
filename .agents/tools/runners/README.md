# runners

## Purpose

Runners stage of the STE-Code pipeline. Reads the unit's declared
inputs, transforms them, and writes the declared outputs. Every tunable knob
lives in `config.yaml` (or the shared `defaults.yaml`), never hardcoded.

## Footprint

### inputs

  - (none declared)

### outputs

  - (none declared)

## Usage

```bash
python3 .agents/tools/runners/phase-a-gen.py
```

## Behaviour

- Loads `config.yaml` via `ste_config.load(__file__)`.
- Resolves runtime knobs (wrapper path, retry count, batch divisor) via
  `ste_runtime.resolve(__file__)`.
- Writes outputs through the gated `ste_io` helper, confined to the repo.
- On crash, resumes from the checkpoint written by `ste_checkpoint`.

## Configuration

- `agent.model` — inherited from `defaults.yaml` unless this unit overrides it.
- `runtime.retry_attempts`, `runtime.batch_divisor`, `runtime.encoding` — pre-flight
  knobs declared in `defaults.yaml` under `runtime:`.
- All paths are unit-local in `config.yaml`; shared values stay in `defaults.yaml`.

## Failure modes

- Worker timeout (`agent.timeout_s`): the caller retries up to `runtime.retry_attempts`.
- HTTP 429 from the model API: back off; keep concurrency at `agent.workers_per_batch`
  (above 3 the free tier rate-limits).
- Partial write: `ste_io` is atomic, and the checkpoint lets a re-run resume.

## See also

- ../lib/README.md (shared helpers: ste_io, ste_config, ste_runtime, ste_checkpoint)
- ../../config/defaults.yaml (shared agent + runtime defaults)
