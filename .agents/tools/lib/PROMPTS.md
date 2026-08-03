# Prompt organization system

## Purpose

This document is the canonical rule for how model-bound text is stored, named
and validated across `.agents/`. Anyone editing a worker prompt, adding a tool
that calls a model, or auditing the migration reads this file first. Every other
description of the templating convention defers to this one.

## Footprint

- Reads: `.agents/tools/<unit>/templates/*.md`, `.agents/skills/*/SKILL.md`.
- Implemented by: `.agents/tools/lib/templater.py`,
  `.agents/tools/lib/skill_prompt.py`.
- Audited by: `.agents/tools/lib/audit_prompt_migration.py`,
  `.agents/tools/lib/survey_prompts.py`,
  `.agents/tools/lib/verify_prompt_move.py`,
  `.agents/tools/lib/migrate_prompt.py`.
- Writes: nothing. The audit scripts are read-only.

## Usage

    # every large string literal, classified prompt / docstring / sql / other
    python3 .agents/tools/lib/survey_prompts.py

    # the work list: tools that dispatch to a model with prompts still inline
    python3 .agents/tools/lib/audit_prompt_migration.py

    # extract an inline prompt into a template
    python3 .agents/tools/lib/migrate_prompt.py \
        --out .agents/tools/finalize/templates/finalize-worker.md

    # prove a migrated template renders byte-identically to the old prompt
    python3 .agents/tools/lib/verify_prompt_move.py check --name refine-worker

## The rule

No prompt text lives inside a `.py` file. Every string sent to a model lives in
a markdown file under a `templates/` folder beside the tool that uses it, and
loads through `.agents/tools/lib/templater.py`.

Python holds control flow. Markdown holds words. Editing wording never requires
touching Python.

## Behaviour

- `Templater(__file__)` binds to the `templates/` folder next to the calling
  tool.
- `render("<name>", var=value)` loads `templates/<name>.md` and substitutes
  `{{var}}`. Templates are cached after first read.
- Placeholders are double-brace. Prompt text is full of literal braces (JSON
  examples, code fences) and pipes (markdown tables); `str.format()` chokes on
  all of them, while `{{name}}` only ever matches an intended placeholder.
- `render()` is strict by default. It raises if the template needs a placeholder
  the caller did not pass, and if the caller passes one the template never uses.
  Both are bugs — a typo'd placeholder shipping to a worker is the exact failure
  this system prevents.
- `load("<name>")` returns raw template text for fragments composed into a
  larger prompt.
- Oneshot sub-agents do not inherit the profile's skills, so `skill_prompt`
  injects the governing `SKILL.md` into the prompt at run time.

```python
from templater import Templater
tpl = Templater(__file__)                    # templates/ next to the tool
text = tpl.render("refine-worker", input_filename="w001-p1-4.md",
                  start_page=1, end_page=4)
```

## Layout

```
.agents/tools/<family>/
├── <tool>.py                  control flow only
└── templates/
    ├── README.md              what each template is for
    ├── <role>-worker.md       prompt sent to a sub-agent
    ├── <role>-batch.md        prompt for the batched variant
    └── <fragment>.md          shared block included by others
```

Naming: `<what-it-does>-<who-runs-it>.md`. A template driving one worker over
one file is `-worker`; the multi-file variant is `-batch`. Fragments composed
into larger prompts take a plain descriptive name.

A few cross-unit prompts live in `.agents/tools/prompts/` and are loaded by
absolute path rather than through `Templater`. They follow the same authoring
rules.

## What is NOT a template

Three categories stay in Python. Extracting them would be a regression.

| category                                | why it stays                                                                                                                             |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Docstrings**                          | documentation for the reader of the code, never sent to a model                                                                          |
| **`templates/` for generated _output_** | `grouping/templates/group_header.md` builds a markdown artifact, not a prompt. Same mechanism, different use case — do not merge the two |
| **Log lines, SQL, argparse help**       | not model-bound                                                                                                                          |

The distinction that matters is **destination**, not shape: does this text reach
a model? Prose in a `print()` does not.

## Skills are the source of truth, not templates

Several tools embed a whole `SKILL.md` into the worker prompt:

```python
skill = skill_prompt.skill_section("refinement")
prompt = tpl.render("refine-worker", ...) + skill
```

Never copy skill content into a template — that forks the protocol. The template
is the thin task wrapper; the skill is the law.

## Configuration

- `runtime.encoding` — text encoding for template reads, from
  `.agents/config/defaults.yaml`.
- `agent.model`, `agent.timeout_s`, `agent.workers_per_batch` — resolved from
  the calling unit's `config.yaml`, never named inside a template.
- Template folder location is fixed by convention, not configurable.
- A template must not name a model, an absolute interpreter path or a repo path.
  Those come from `ste_config`, `ste_paths` and `ste_io` at render time.

## Migrating one tool

1. Run the audit; note the line numbers and the interpolated names.
2. Create `templates/<name>.md` with the prose, converting each `{var}` to
   `{{var}}`. Keep the wording byte-identical apart from the placeholder syntax
   — this is a move, not a rewrite.
3. Replace the inline string with a `tpl.render(...)` call.
4. Diff the rendered output against the original prompt for a real input. It
   must match exactly before the change counts as done.
5. Re-run the audit — the file no longer appears.

Step 4 is not optional. A prompt migration that changes wording silently changes
model behaviour, and nothing downstream catches it.

## Failure modes

- `KeyError` at render — the template references a placeholder the caller
  omitted.
- `ValueError` at render — the caller supplied a variable the template never
  uses.
- **Silent behaviour change** — a reworded template ships new instructions to
  every worker with no failing test. Verify with `verify_prompt_move.py`.
- **Forked protocol** — skill text copied into a template drifts from the SKILL
  and the two disagree. Inject the skill instead.
- **Orphaned template** — a `templates/*.md` file no tool renders. The audit
  does not flag these; grep for the template name before trusting a
  `templates/README.md` table.
- **Oversized prompt** — enrichment templates interpolate whole documents and
  reach tens of thousands of characters. That is expected, but it raises timeout
  and 429 risk on the free tier.

## Migration status

The audit tracks what remains. A tool appears as a target only when it
dispatches to a model, builds that text inline, and does not already import
`templater`. When the target list is empty, the system holds. Run
`python3 .agents/tools/lib/audit_prompt_migration.py` for the current count
rather than trusting a number written here.

## See also

- [templater.py](templater.py) — the loader
- [skill_prompt.py](skill_prompt.py) — skill injection
- [../TEMPLATES.md](../TEMPLATES.md) — pointer to this file
- [../README.md](../README.md) — tools directory overview
- [../../config/defaults.yaml](../../config/defaults.yaml) — shared agent
  defaults
