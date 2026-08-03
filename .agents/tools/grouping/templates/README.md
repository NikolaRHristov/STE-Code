# Grouping templates

## Purpose

This folder holds the external markdown templates for the Phase C grouping
tools. Edit these `.md` files to change generated output; do not edit the
f-strings in the `.py`. Anyone changing the shape of a group header reads this
file first.

Note the destination: these templates build a markdown **artifact**, not a model
prompt. Grouping is deterministic and calls no model.

## Footprint

From `.agents/tools/grouping/config.yaml`:

```yaml
unit: grouping
inputs:
    refined: ste-code/refined
outputs:
    grouped: ste-code/grouped
    state: .agents/state
format:
    encoding: utf-8
layout:
    source_page_re: '^r?(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$'
```

The unit declares no `agent:` block, because no stage in it calls a model.

## Usage

    python3 .agents/tools/grouping/group_batch.py [--dry-run]
    python3 .agents/tools/grouping/verify-groups.py
    python3 .agents/tools/grouping/test_grouping.py

## Templates

| File              | Rendered by                      | Placeholders                                                                                      |
| ----------------- | -------------------------------- | ------------------------------------------------------------------------------------------------- |
| `group_header.md` | `group_batch.py::assemble_group` | `gid`, `page_start`, `page_end`, `section`, `key`, `key_suffix`, `workers`, `page_count`, `title` |

## Behaviour

- Tools load templates through the shared loader
  `.agents/tools/lib/templater.py`:

    ```python
    from templater import Templater
    TPL = Templater(__file__)                 # -> this templates/ folder
    header = TPL.render("group_header", gid="001-front-matter", page_start=1, ...)
    ```

- Substitution uses double-brace placeholders, never Python `.format()`.
  Markdown content is full of literal single braces and pipes; `{{name}}` never
  collides with them, so templates are written with zero escaping.
- Rendering is strict: an unsupplied placeholder or an unused variable is an
  error, which catches typos before they ship.
- `group_engine.py` owns the plan and parity primitives; the template only
  formats the header the engine computed.
- `verify-groups.py` gates the stage on coverage, parity and marks.
- Output is written through `ste_io`, which confines every path to the repo
  root.

### Adding a template

1. Create `templates/<name>.md` with `{{placeholders}}`.
2. Render it: `TPL.render("<name>", placeholder=value, ...)`.
3. Add a row to the table above.

## Configuration

- `layout.source_page_re` — the filename grammar for refined source pages.
- `format.encoding` — text encoding for reads and writes.
- `inputs.refined`, `outputs.grouped`, `outputs.state` — the complete path
  footprint.
- `runtime.encoding`, `runtime.batch_divisor` — shared knobs from
  `.agents/config/defaults.yaml`.
- No `agent.model` applies here; the stage is deterministic.
- Knobs live only in `config.yaml`. A regex or path hardcoded in a `.py` is a
  defect.

## Failure modes

- `KeyError` / `ValueError` at render — the caller and the template disagree on
  the placeholder set. Update both together with the table above.
- **Parity failure** — `verify-groups.py` reports a page present in `refined/`
  but missing from `grouped/`, or counted twice. The stage did not complete.
- **Filename mismatch** — a refined page that does not match
  `layout.source_page_re` is skipped silently by the glob and shows up later as
  a coverage gap.
- **Marker damage** — `<mark>` spans written by refinement are read back here;
  `diagnose_markers.py` and `repair_markers.py` triage broken spans.
- **Partial writes** — a killed run leaves some groups assembled. Rerun;
  assembly is deterministic and idempotent.

## See also

- [../config.yaml](../config.yaml) — unit footprint
- [../group_engine.py](../group_engine.py) — plan and parity primitives
- [../../lib/PROMPTS.md](../../lib/PROMPTS.md) — templating system and the
  prompt-versus-output distinction
- [../../../config/defaults.yaml](../../../config/defaults.yaml) — shared
  defaults
