# Refinement templates

## Purpose

This folder holds the prompt text for the refinement stage workers — the level-1
compression worker and the page-refinement workers driven by `refine_batch.py`.
Edit these `.md` files to change worker wording; never the Python.

## Footprint

From `.agents/tools/refinement/config.yaml`:

```yaml
unit: refinement
inputs:
    extracted: ste-code/extracted
outputs:
    refined: ste-code/refined
    state: .agents/state
    checkpoint: .agents/state/refine-checkpoint.json
    trajectory: .agents/tmp
layout:
    worker_file: "w{worker:03d}-p{start}-{end}.md"
    refined_file: "r{worker:03d}-p{start}-{end}.md"
format:
    encoding: utf-8
    mark_open: "<mark>"
    mark_close: "</mark>"
thresholds:
    total_workers: 109
    word_ratio_min: 0.98
agent:
    model: poolside/laguna-s-2.1:free
    workers_per_batch: 3
    timeout_s: 600
```

Templates in this folder are read only; the stage writes to `outputs:` above.

## Usage

    python3 .agents/tools/refinement/refine_batch.py [start_batch] [num_batches]
    python3 .agents/tools/refinement/refine_batch.py --resume
    python3 .agents/tools/refinement/assemble-level1.py [--dry-run]

## Templates

| Template | Used by | Placeholders |
|---|---|---|
| `refine-worker.md` | `refine_batch.py` — refine one page range | `input_filename`, `output_filename`, `start_page`, `end_page` |
| `refine-batch.md` | `refine_batch.py` — wrapper around N tasks | `n`, `tasks` |
| `refine-batch-task.md` | `refine_batch.py` — one task row in the wrapper | `i`, `n`, `inp`, `out`, `s`, `e` |
| `level1-worker.md` | `assemble-level1.py::build_prompt()` — compress Level 2 to Level 1 | `level2_text` |

`level2_text` carries the whole Level 2 system prompt, so a rendered level-1 prompt
reaches roughly 78k characters. That is expected.

## Behaviour

- `refine_batch.py` renders one `refine-batch-task` block per page range, then
  interpolates the joined blocks into `refine-batch` as `tasks`.
- Single-page work renders `refine-worker` directly.
- The refinement `SKILL.md` is appended at run time through `skill_prompt`; the
  template is the thin task wrapper and the skill is the protocol.
- Refined pages are named by `layout.refined_file` — the extracted stem with an `r`
  prefix — and written through `ste_io`.
- Workers wrap retained source spans in `format.mark_open` / `format.mark_close`;
  the grouping stage reads those marks back.
- Output must reach `thresholds.word_ratio_min` of the source word count. Never gate
  on raw line count: table and collapse rules make correct output legitimately
  shorter.
- Progress checkpoints to `outputs.checkpoint`, so `--resume` continues a killed run.

## Configuration

- `agent.model` — `poolside/laguna-s-2.1:free`. This unit overrides the shared
  default because worker sub-agents need the long-context model for large pages.
- `agent.workers_per_batch`, `agent.timeout_s` — concurrency and per-worker budget.
- `thresholds.total_workers`, `thresholds.word_ratio_min` — coverage and quality
  gates.
- `layout.*`, `format.*` — filename grammar, encoding and mark tags.
- `runtime.retry_attempts`, `runtime.backoff_base_s`, `runtime.batch_divisor` —
  shared pre-flight knobs from `.agents/config/defaults.yaml`.
- Knobs live only in config. A model name or output path hardcoded in a template or
  script is a defect; `assemble-level1.py` resolves its output path itself and does
  not interpolate one into the prompt.

## Failure modes

- `KeyError` / `ValueError` at render — placeholder drift between caller and
  template. The table above is the contract.
- **Word-ratio gate** — output below `thresholds.word_ratio_min` is rejected and the
  page is queued for redo through `continuation/verify_continuation.py`.
- **Lost marks** — a worker that drops `<mark>` spans breaks grouping parity
  downstream.
- **HTTP 429** — more than three concurrent workers on the free tier.
- **Timeout** — the level-1 prompt is very large; a worker over `agent.timeout_s` is
  killed and retried.
- **Concurrent writers** — Phase B1 also writes into `ste-code/refined/`. Never run
  continuation while refinement is active.
- **Partial batch** — rerun with `--resume`; the checkpoint holds completed pages.

## See also

- [../config.yaml](../config.yaml) — unit footprint
- [../../continuation/](../../continuation/) — redo queue for incomplete pages
- [../../lib/PROMPTS.md](../../lib/PROMPTS.md) — canonical prompt system
- [../../../config/defaults.yaml](../../../config/defaults.yaml) — shared defaults
