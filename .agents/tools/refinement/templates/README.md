# Refinement templates

Prompt text for `refine_batch.py`. Edit these to change worker wording — never
the Python. See `.agents/tools/lib/PROMPTS.md` for the system.

| template | used by | placeholders |
|---|---|---|
| `refine-worker.md` | `_build_prompt()` — one worker, one file | `input_filename`, `output_filename`, `start_page`, `end_page` |
| `refine-batch.md` | `_build_batch_prompt()` — one worker, N files | `n`, `tasks` |
| `refine-batch-task.md` | per-file block composed into `{{tasks}}` | `i`, `n`, `inp`, `out`, `s`, `e` |

## Composition

```
refine-batch.md
  └── {{tasks}}  ←  "\n\n".join(refine-batch-task.md rendered per file)
```

Both top-level prompts are concatenated with the refinement `SKILL.md`
(injected via `skill_prompt.skill_section("refinement")`) plus a closing
output-only instruction, in this order:

```
wrapper (this template) + SKILL.md + "Output ONLY the refined markdown file..."
```

**The skill is the authoritative protocol** — the 9 rules, before/after examples
and failure recovery live there. These templates are only the task wrapper. Do
not copy skill content in; that would fork the protocol.

## Constraints

`refine-batch-task.md` has **no trailing newline**. Blocks are joined with
`\n\n`, so a trailing newline would produce three blank lines between file
tasks. If you edit it, preserve that.

The en-dash in `# Page {{s}}–{{e}} of 434` is intentional and load-bearing — the
refined output is checked against that exact header shape.
