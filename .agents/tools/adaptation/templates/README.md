# Adaptation templates

## Purpose

This folder holds the external worker-prompt templates for the Phase D
adaptation tools. Edit the `.md` files here to change what adaptation workers
receive; do not edit the `.py`. Anyone changing adaptation wording reads this
file first.

## Footprint

From `.agents/tools/adaptation/config.yaml`:

```yaml
unit: adaptation
inputs:
    grouped: ste-code/grouped
outputs:
    adapted: ste-code/adapted
    state: .agents/state
agent:
    model: tencent/hy3:free
    workers_per_batch: 3
    timeout_s: 600
```

Templates in this folder are read by `adapt_batch.py`; they are never written
to.

## Usage

    python3 .agents/tools/adaptation/adapt_batch.py [--resume] [--dry-run]
    python3 .agents/tools/adaptation/adapt_batch.py 3 1     # section 3 only
    python3 .agents/tools/adaptation/test_adapt.py          # render checks

## Templates

| File           | Rendered by                     | Placeholders                                                            |
| -------------- | ------------------------------- | ----------------------------------------------------------------------- |
| `adapt-sec.md` | `adapt_batch.py::_build_prompt` | `section_num`, `section_title`, `rule_count`, `rule_ids`, `source_text` |

## Behaviour

- `adapt_batch.py` builds `TPL = Templater(__file__)`, binding to this folder.
- `TPL.render("adapt-sec", ...)` substitutes every `{{placeholder}}` in the
  table.
- Rendering is strict: a missing variable and an unused variable are both
  errors.
- The authoritative adaptation protocol — the 6-pass pipeline, category mapping,
  before/after examples and gates — is embedded at run time from
  `.agents/skills/ste-code-authoring/adaptation/SKILL.md` via
  `skill_prompt.skill_section("adaptation")`. Edit the SKILL to change
  behaviour, and the template only to change the task wrapper.
- `verify-adaptation.py` gates the stage on aerospace leakage, synonyms and
  coverage.

## Configuration

- `agent.model` — `tencent/hy3:free`, declared in the unit `config.yaml`; it
  overrides `.agents/config/defaults.yaml`.
- `agent.workers_per_batch`, `agent.timeout_s` — worker concurrency and
  wall-clock budget.
- `runtime.retry_attempts`, `runtime.backoff_base_s`, `runtime.batch_divisor` —
  pre-flight knobs from `defaults.yaml`.
- Templates must not name a model, a path or a threshold. Those resolve through
  `ste_config`, `ste_paths` and `ste_io` at run time.

## Failure modes

- `KeyError` / `ValueError` at render — the caller and the template disagree on
  the placeholder set. Update both together with the table above.
- **HTTP 429** — more than three concurrent workers on the free tier. Keep
  `agent.workers_per_batch` at 3.
- **Timeout** — `source_text` carries a whole rule section, so prompts are
  large. A worker over `agent.timeout_s` is killed and retried.
- **Protocol fork** — copying SKILL text into the template makes the two
  disagree. Inject the skill instead.
- **Gate failure** — `verify-adaptation.py` exiting non-zero means the section
  is not adapted. Resume rather than advancing.

## See also

- [../config.yaml](../config.yaml) — unit footprint
- [../../lib/PROMPTS.md](../../lib/PROMPTS.md) — canonical prompt system
- [../../../config/defaults.yaml](../../../config/defaults.yaml) — shared
  defaults
