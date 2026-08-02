# Finalize templates

## Purpose

This folder holds the prompt text for `finalize_batch.py`, the Phase G enrichment
stage. Edit these `.md` files to change worker wording; never the Python. Anyone
tuning final-rule enrichment reads this file first.

## Footprint

From `.agents/tools/finalize/config.yaml`:

```yaml
unit: finalize
inputs:
    adapted: ste-code/adapted
    grouped: ste-code/grouped
    refined: ste-code/refined
    vendor: .agents/vendor
outputs:
    final_rules: ste-code/final/rules
    state: .agents/state
agent:
    model: tencent/hy3:free
    workers_per_batch: 3
    timeout_s: 600
```

Templates in this folder are read by `finalize_batch.py`; they are never written to.

## Usage

    python3 .agents/tools/finalize/finalize_batch.py [--resume] [--dry-run]
    python3 .agents/tools/finalize/verify_final.py
    python3 .agents/tools/finalize/verify_final_assembly.py

## Templates

| Template | Used by | Placeholders |
|---|---|---|
| `finalize-worker.md` | `_build_prompt()` — enrich one rule file | `adapted_path_name`, `self_num`, `title`, `src`, `prev`, `refs` |

| Name | Supplied from | What it carries |
|---|---|---|
| `adapted_path_name` | `adapted_path.name` | filename only, not the full path — appears three times |
| `self_num` | caller | rule number, e.g. `1.1` |
| `title` | caller | rule title |
| `src` | `adapted_path` read through `ste_io.read_text` | the full current adapted rule |
| `prev` | `_previous_documents_context()` | prior pipeline stages, for traceability and vocabulary |
| `refs` | `_reference_context()` | vendor style guides the worker borrows approved words from |

## Behaviour

- `finalize_batch.py` binds `Templater(__file__)` to this folder and renders
  `finalize-worker` once per adapted rule file.
- `src`, `prev` and `refs` are large; a rendered prompt runs to roughly 70k
  characters. That is expected — this is the creative enrichment stage and the
  worker needs the full context.
- The worker writes its own output file and produces no chat output. The batch
  runner reads the file from disk and treats chat narration as a failure. Do not
  soften that instruction.
- Writes land under `ste-code/final/rules` through `ste_io`, which confines every
  path to the repo root.
- Progress checkpoints into `.agents/state`, so `--resume` continues a killed run.

## Configuration

- `agent.model` — `tencent/hy3:free` from the unit `config.yaml`, overriding
  `.agents/config/defaults.yaml`.
- `agent.workers_per_batch`, `agent.timeout_s` — concurrency and per-worker budget.
- `runtime.retry_attempts`, `runtime.backoff_base_s`, `runtime.encoding` — shared
  pre-flight knobs.
- All writes are gated by `ste_io`; the template never names an absolute path.
- `adapted_path_name` must be the basename. The template writes
  `ste-code/final/rules/{{adapted_path_name}}`, so a full path would produce a
  nested directory that does not exist.

## Failure modes

- **Nested output directory** — passing a path instead of a basename for
  `adapted_path_name` writes to a directory that does not exist.
- **Chat narration** — a worker that answers in chat instead of writing the file
  leaves nothing on disk and the item counts as failed.
- **Timeout** — 70k-character prompts are slow; a worker over `agent.timeout_s` is
  killed and retried `runtime.retry_attempts` times.
- **HTTP 429** — the free tier rejects more than three concurrent workers.
- `KeyError` / `ValueError` at render — placeholder set drift between caller and
  template.
- **Partial batch** — a killed run leaves completed rules on disk; rerun with
  `--resume`.

## See also

- [../config.yaml](../config.yaml) — unit footprint
- [../../lib/PROMPTS.md](../../lib/PROMPTS.md) — canonical prompt system
- [../../../config/defaults.yaml](../../../config/defaults.yaml) — shared defaults
