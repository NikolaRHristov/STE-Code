# Adaptation templates

External worker-prompt templates for the Phase D adaptation tools. Edit the
`.md` files here to change what adaptation workers receive — not the `.py`.

## Convention
- Loaded via `.agents/tools/lib/templater.py`: `TPL = Templater(__file__)`.
- Placeholder syntax `{{name}}` (double-brace). Markdown prompts have literal
  single braces and pipes, so `.format()` would break — `{{name}}` never collides.
- Rendering is **strict**: a missing variable or an unused variable is an error.

## Templates
| File | Rendered by | Placeholders |
|---|---|---|
| `adapt-sec.md` | `adapt_batch.py::_build_prompt` | `section_num`, `section_title`, `rule_count`, `rule_ids`, `source_text` |

The authoritative adaptation protocol (6-pass pipeline, category mapping, before/after
examples, gates) is embedded at runtime from `.agents/skills/adaptation/SKILL.md` via
`skill_prompt.skill_section("adaptation")` — edit the SKILL to change *behavior*, not the
prompt template.
