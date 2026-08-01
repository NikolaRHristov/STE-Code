# Prompt organization system

How LLM-bound text is stored, named and validated across `.agents/`.

## The rule

**No prompt text lives inside a `.py` file.** Every string sent to a model lives
in a markdown file under a `templates/` folder beside the tool that uses it, and
is loaded through `.agents/tools/lib/templater.py`.

Python holds control flow. Markdown holds words. Editing wording must never
require touching Python.

## Why `{{name}}` and not f-strings

Prompt text is full of literal braces (JSON examples, code fences, `{start}-{end}`
in prose) and literal pipes (markdown tables). `str.format()` and f-strings choke
on all of them and force escaping like `\\|` — which is how the old inline
prompts ended up unreadable.

`{{name}}` only ever matches an intended placeholder, so template authors write
natural markdown with zero escaping.

```python
from templater import Templater
tpl = Templater(__file__)                    # templates/ next to the tool
text = tpl.render("refine-worker", input_filename="w001-p1-4.md",
                  start_page=1, end_page=4)
```

`render()` is **strict by default**: it raises if the template needs a
placeholder you did not pass, *and* if you pass one the template never uses.
Both are bugs — a typo'd placeholder silently shipping to a worker is exactly
the failure this system exists to prevent.

## Layout

```
.agents/tools/<family>/
├── <tool>.py                  control flow only
└── templates/
    ├── README.md              what each template is for  (optional but wanted)
    ├── <role>-worker.md       prompt sent to a sub-agent
    ├── <role>-batch.md        prompt for the batched variant
    └── <fragment>.md          shared block included by others
```

Naming: `<what-it-does>-<who-runs-it>.md`. A template driving one worker over one
file is `-worker`; the multi-file variant is `-batch`. Fragments composed into
larger prompts take a plain descriptive name.

## What is NOT a template

Three categories stay in Python. Extracting them would be a regression:

| category | why it stays |
|---|---|
| **Docstrings** | documentation for the reader of the code, never sent to a model |
| **`templates/` for generated *output*** | e.g. `grouping/templates/group_header.md` builds a markdown artifact, not a prompt. Same mechanism, different use case — do not merge the two |
| **Log lines, SQL, argparse help** | not model-bound |

The distinction that matters is **destination**, not shape: does this text reach
a model? Prose in a `print()` does not.

## Skills are the source of truth, not templates

Several tools embed a whole `SKILL.md` into the worker prompt via
`.agents/tools/lib/skill_prompt.py`:

```python
skill = skill_prompt.skill_section("refinement")
prompt = tpl.render("refine-worker", ...) + skill
```

Oneshot sub-agents do not inherit the `ste-code` profile's skills, so the skill
text is injected. **Never copy skill content into a template** — that forks the
protocol. The template is the thin task wrapper; the skill is the law.

## Audit tooling

Two read-only scripts keep the system honest:

```bash
# every large string literal, classified prompt / docstring / sql / other
python3 .agents/tools/lib/survey_prompts.py

# the work list: tools that dispatch to a model with prompts still inline
python3 .agents/tools/lib/audit_prompt_migration.py
```

`audit_prompt_migration.py` is the one to run before declaring the migration
finished. A tool appears as a target only when it dispatches to a model, builds
that text inline, and does not already import `templater`. When the target list
is empty, the system holds.

## Migration status

23 tools already load prompts through `templater`. The audit tracks what remains.

Migrating one tool:

1. Run the audit; note the line numbers and the interpolated names.
2. Create `templates/<name>.md` with the prose, converting each `{var}` to
   `{{var}}`. Keep the wording **byte-identical** apart from the placeholder
   syntax — this is a move, not a rewrite.
3. Replace the inline string with a `tpl.render(...)` call.
4. Diff the rendered output against the original prompt for a real input. It
   must match exactly before the change is considered done.
5. Re-run the audit — the file should no longer be listed.

Step 4 is not optional. A prompt migration that changes wording silently changes
model behaviour, and nothing downstream will catch it.
