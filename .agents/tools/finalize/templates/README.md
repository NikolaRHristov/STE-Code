# Finalize templates

Prompt text for `finalize_batch.py`. Edit these to change worker wording — never
the Python. See `.agents/tools/lib/PROMPTS.md` for the system.

| template | used by | placeholders |
|---|---|---|
| `finalize-worker.md` | `_build_prompt()` — enrich one rule file | `adapted_path_name`, `self_num`, `title`, `src`, `prev`, `refs` |

## Placeholders

| name | supplied from | what it carries |
|---|---|---|
| `adapted_path_name` | `adapted_path.name` | filename only, not the full path — appears three times (input line, read instruction, output path) |
| `self_num` | caller | rule number, e.g. `1.1` |
| `title` | caller | rule title |
| `src` | `adapted_path.read_text()` | the full current adapted rule |
| `prev` | `_previous_documents_context()` | prior pipeline stages, for traceability and vocabulary |
| `refs` | `_reference_context()` | vendor style guides the worker borrows approved words from |

`src`, `prev` and `refs` are large — a rendered prompt runs to roughly 70k
characters. That is expected: this is the creative enrichment stage and the
worker needs the full context.

## Constraints

`adapted_path_name` is the **basename**, not a path. The template writes
`ste-code/final/rules/{{adapted_path_name}}`, so passing a full path would
produce a nested directory that does not exist.

The worker is instructed to write the file itself and produce no chat output.
Do not soften that — the batch runner reads the file from disk and treats chat
narration as a failure.
