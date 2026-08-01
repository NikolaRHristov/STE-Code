# Runners templates

External worker-prompt templates for the phase runners in `.agents/tools/runners/`.
Edit the `.md` files here to change the prompts workers receive — not the `.py`.

## Convention
- Templates are loaded via `.agents/tools/lib/templater.py`:
  `TPL = Templater(__file__)` then `TPL.render("phase-a-worker", var=value)`.
- Placeholder syntax is `{{name}}` (double-brace). Markdown content has literal
  single braces and pipes, so `.format()` would break — `{{name}}` never collides.
- Rendering is **strict**: a missing variable or an unused variable is an error.

## Templates
| File | Rendered by | Placeholders |
|---|---|---|
| `phase-a-worker.md` | `phase-a-run.py` | — |
| `phase-b-worker.md` | `phase-b-run.py` | `batch`, `extracted_dir`, `refined_dir` |
| `phase-b1-worker.md` | `phase-b1-run.py` | — |
| `phase-d-worker.md` | `phase-d-run.py` | `grouped_dir`, `adapted_dir`, `adapt_instruction` |
| `phase-f-worker.md` | `phase-f-run.py` | `adapted_dir`, `artifacts_dir` |
| `phase-a-creative-block.md` | `phase-a-gen.py` | — |
| `phase-a-execution-block.md` | `phase-a-gen.py` | `target` |
