# Grouping templates

External markdown templates for the Phase C grouping tools. **Edit these `.md`
files to change generated output — do not edit the f-strings in the `.py`.**

## How it works
Tools load templates via the shared loader `.agents/tools/lib/templater.py`:

```python
from templater import Templater
TPL = Templater(__file__)                 # -> this templates/ folder
header = TPL.render("group_header", gid="001-front-matter", page_start=1, ...)
```

## Placeholder syntax: `{{name}}`
Substitution uses **double-brace** placeholders, never Python `.format()`.
Markdown/prompt content is full of literal single braces (JSON, code fences) and
pipes (`|` tables); `{{name}}` never collides with them, so you write natural
markdown with **zero escaping**. Rendering is **strict**: an unsupplied
placeholder or an unused variable is an error (catches typos before they ship).

## Templates in this folder
| File | Rendered by | Placeholders |
|---|---|---|
| `group_header.md` | `group_batch.py::assemble_group` | `gid`, `page_start`, `page_end`, `section`, `key`, `key_suffix`, `workers`, `page_count`, `title` |

## Adding a template
1. Create `templates/<name>.md` with `{{placeholders}}`.
2. Render it: `TPL.render("<name>", placeholder=value, ...)`.
3. Add a row to the table above.
