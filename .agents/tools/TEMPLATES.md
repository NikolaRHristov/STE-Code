# External templates convention

## Purpose

This file is a pointer. The canonical description of how prompt and output text
is stored, named, rendered and audited lives in
[lib/PROMPTS.md](lib/PROMPTS.md). Read that file. This one exists only so that a
reader who lands on `.agents/tools/TEMPLATES.md` is redirected rather than
served a second, drifting copy of the same rules.

## Footprint

- Reads: nothing. This document describes a convention; it is not executed.
- The convention it points at is implemented by
  `.agents/tools/lib/templater.py`.

## Usage

    python3 .agents/tools/lib/audit_prompt_migration.py   # tools with inline prompts
    python3 .agents/tools/lib/survey_prompts.py           # classify string literals

## Behaviour

- Every tool that sends text to a model keeps that text in `templates/*.md`
  beside the script, loaded through `lib/templater.py`.
- Placeholders use double braces, `{{name}}`, so literal braces and pipes in
  markdown need no escaping.
- `render()` is strict: a missing placeholder and an unused variable are both
  errors.
- `templates/` also holds generated-output blocks such as
  `grouping/templates/group_header.md`. Same loader, different destination — the
  distinction that matters is whether the text reaches a model.

## Configuration

- No tunable knobs. The loader takes its encoding from `runtime.encoding` in
  `.agents/config/defaults.yaml`.
- Template locations are fixed by convention: `<unit>/templates/<name>.md`.
- Never hardcode prompt text in a `.py` file.

## Failure modes

- `KeyError` — the template needs a placeholder the caller did not pass.
- `ValueError` — the caller passed a variable the template never uses.
- Silent drift — editing a template changes model behaviour with no test to
  catch it. Diff a rendered prompt against the previous output before shipping a
  reword.

## See also

- [lib/PROMPTS.md](lib/PROMPTS.md) — canonical, read this first
- [lib/templater.py](lib/templater.py) — the loader
- [README.md](README.md) — tools directory overview
