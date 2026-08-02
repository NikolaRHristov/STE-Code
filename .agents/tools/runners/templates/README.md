# Runners templates

## Purpose

This folder holds the external worker-prompt templates for the phase runners in
`.agents/tools/runners/`. Edit the `.md` files here to change the prompts workers
receive; do not edit the `.py`. Anyone changing phase-runner wording, or auditing
which templates are still live, reads this file first.

## Footprint

`.agents/tools/runners/` has no `config.yaml`. Each runner delegates to the unit
that owns the stage and inherits that unit's footprint.

| Runner | Delegates to | Footprint declared in |
|---|---|---|
| `phase-a-run.py`, `phase-a-gen.py` | `extraction/extract_batch.py` | `../../extraction/config.yaml` |
| `phase-b-run.py` | `refinement/refine_batch.py` | `../../refinement/config.yaml` |
| `phase-b1-run.py` | `continuation/continue_batch.py` | `../../continuation/config.yaml` |
| `phase-c-run.py` | `grouping/group_batch.py` | `../../grouping/config.yaml` |
| `phase-d-run.py` | `adaptation/adapt_batch.py` | `../../adaptation/config.yaml` |
| `phase-e-run.py` | `extension/extend_batch.py` | `../../extension/config.yaml` |
| `phase-f-run.py` | `artifacts/artifact_batch.py` | `../../artifacts/config.yaml` |
| `phase-g-run.py` | `finalize/finalize_batch.py` | `../../finalize/config.yaml` |

Templates in this folder are read only.

## Usage

    python3 .agents/tools/runners/phase-a-run.py
    python3 .agents/tools/runners/phase-b-run.py
    python3 .agents/tools/runners/phase-b1-run.py --queue Q.json [--resume]
    python3 .agents/tools/runners/phase-d-run.py [--resume] [--verify]
    python3 .agents/tools/runners/phase-f-run.py [--dry-run] [--verify]
    .agents/tools/runners/launch-downstream.sh        # C -> D -> E -> F

## Templates

Live templates, rendered on every run:

| File | Rendered by | Placeholders |
|---|---|---|
| `phase-a-worker.md` | `phase-a-run.py` | — |
| `phase-a-creative-block.md` | `phase-a-gen.py` | — |
| `phase-a-execution-block.md` | `phase-a-gen.py` | `target` |
| `phase-b-worker.md` | `phase-b-run.py` | `batch`, `extracted_dir`, `refined_dir` |

Orphaned templates, retained but not rendered by any script:

| File | Placeholders | Status |
|---|---|---|
| `phase-b1-worker.md` | — | `phase-b1-run.py` delegates to `continue_batch.py` and builds no prompt |
| `phase-d-worker.md` | `grouped_dir`, `adapted_dir`, `adapt_instruction` | `phase-d-run.py` delegates to `adapt_batch.py`, which renders `adaptation/templates/adapt-sec.md` |
| `phase-f-worker.md` | `adapted_dir`, `artifacts_dir` | `phase-f-run.py` delegates to `artifact_batch.py`, a deterministic stage with no worker prompt |

Editing an orphaned template changes nothing. Verify with a grep for the template
name before assuming a change takes effect.

## Behaviour

- Runners load templates through `.agents/tools/lib/templater.py`:
  `TPL = Templater(__file__)` then `TPL.render("phase-a-worker", var=value)`.
- Placeholder syntax is double-brace. Markdown content has literal single braces and
  pipes, so `.format()` would break; `{{name}}` never collides.
- Rendering is strict: a missing variable and an unused variable are both errors.
- Phases B1, C, D, E, F and G are thin delegators. They forward flags to the owning
  unit's batch script and do not construct prompts themselves.
- Runners resolve the interpreter through `ste_paths.venv_python()` and the repo root
  through `repo_root()`, so neither is a literal path.
- Stage settings resolve through `ste_config.load(__file__)` against the owning
  unit's `config.yaml`.

## Configuration

- `agent.model`, `agent.workers_per_batch`, `agent.timeout_s` — inherited from
  `.agents/config/defaults.yaml` unless the owning unit overrides them. Refinement
  overrides the model; adaptation and finalize pin it explicitly.
- `runtime.retry_attempts`, `runtime.backoff_base_s`, `runtime.batch_divisor` —
  shared pre-flight knobs.
- `--agent` and `--model` on phases D and F are accepted as informational no-ops,
  kept for the legacy one-shot CLI. Change the model in `config.yaml`.
- All writes are gated by `ste_io`; templates never name an absolute path.

## Failure modes

- **Editing an orphan** — a reworded `phase-b1`, `phase-d` or `phase-f` template has
  no effect, because nothing renders it.
- `KeyError` / `ValueError` at render — placeholder drift between runner and
  template.
- **Missing queue** — `phase-b1-run.py` prints usage and exits without `--queue`.
  This is deliberate: B1 writes into `ste-code/refined/`, which refinement also owns.
- **Concurrent writers** — never run B1 while refinement is active.
- **HTTP 429** — the free tier rejects more than three concurrent workers.
- **Timeout** — a worker over `agent.timeout_s` is killed and retried
  `runtime.retry_attempts` times.
- **Gate failure** — `--verify` on D and F runs the unit's verify script. Non-zero
  means the stage did not produce valid output; do not advance.

## See also

- [../README.md](../README.md) — runner overview
- [../../lib/PROMPTS.md](../../lib/PROMPTS.md) — canonical prompt system
- [../../README.md](../../README.md) — tools directory overview
- [../../../config/defaults.yaml](../../../config/defaults.yaml) — shared defaults
