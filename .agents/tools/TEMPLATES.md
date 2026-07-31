# External templates convention (STE-Code tools)

Every pipeline tool that **generates markdown or worker prompts** keeps that text
in an external `templates/*.md` file beside the script, **not** as inline
f-strings. This makes the generated text easy to review, diff, and edit without
touching Python, and avoids the brace/pipe escaping hell of `.format()`.

## Loader
`from templater import Templater` (`.agents/tools/lib/templater.py`):
```python
TPL = Templater(__file__)                 # -> <tool_dir>/templates/
text = TPL.render("name", var=value)      # -> templates/name.md
```

## Placeholder syntax: `{{name}}`
Double-brace, **not** `.format()`. Markdown prompts are full of literal `{` `}`
(JSON, code fences) and `|` (tables) — `{{name}}` never collides, so template
authors write natural markdown with zero escaping.

## Strict by default
A template that needs a var you didn't pass raises `KeyError`; a var you passed
but the template doesn't use raises `ValueError`. Pass `strict=False` to relax
(both are real bugs to surface early — a typo'd placeholder shipping to a worker
silently corrupts output).

## Where templates live
- `grouping/templates/` — group header / metadata blocks
- `runners/templates/` — phase worker prompts
- (other tool folders follow the same pattern as they're converted)

## Refinement folder note
`refinement/*.py` is managed by the refinement orchestration agent and is
intentionally NOT converted here. When that work stabilizes, its inline
`f"""..."""` worker prompts (`_build_prompt`, `_build_batch_prompt`) should
follow this same convention.
