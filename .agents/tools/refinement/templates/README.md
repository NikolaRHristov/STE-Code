# Refinement level-1 templates

Prompt text for `assemble-level1.py`. Edit these to change the compression
worker's wording — never the Python. See `.agents/tools/lib/PROMPTS.md`.

| template | used by | placeholders |
|---|---|---|
| `level1-worker.md` | `build_prompt()` — compress Level 2 → Level 1 | `level2_text`, `OUTPUT` |

## Placeholders

| name | supplied from | meaning |
|---|---|---|
| `level2_text` | `LEVEL2_INPUT.read_text()` | the full Level 2 system prompt |
| `OUTPUT` | `str(OUTPUT)` | absolute path the worker must write to |

`level2_text` is large (the whole Level 2 prompt, ~4,500 tokens) — a rendered
prompt is ~78k characters. That is expected.

## Constraint

`OUTPUT` is the **absolute path** to the Level 1 output file. The original
prompt interpolated the module global directly; keep passing `str(OUTPUT)` so
the worker writes to the right place.
