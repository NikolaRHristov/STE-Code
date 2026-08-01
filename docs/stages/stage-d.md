# Stage D — Adaptation

**Purpose:** rewrite the grouped aerospace specification into the code domain.
Rule numbers, dictionary architecture, and structure stay the same; the
examples become code-documentation examples.

| | |
|---|---|
| **Reads** | `ste-code/grouped/*.md` |
| **Writes** | `ste-code/adapted/a-secN-ruleX.Y.md`, `a-sec9-gr1..4.md`, `a-dictionary.md`, `a-categories.md` |
| **Type** | LLM worker per rule section (9 sections + GR1–GR4) |
| **Runner** | `.agents/tools/runners/phase-d-run.py` |
| **Orchestrator** | `.agents/tools/adaptation/adapt_batch.py` |
| **Gate** | `.agents/tools/adaptation/verify-adaptation.py` |
| **Checkpoint** | `.agents/state/adapt-checkpoint.json` |

---

## Commands

```bash
# Full orchestrated adaptation (all 9 sections + GR)
python3 .agents/tools/runners/phase-d-run.py

# Resume from the checkpoint
python3 .agents/tools/runners/phase-d-run.py --resume

# One section only (section 3, one section)
python3 .agents/tools/runners/phase-d-run.py 3 1

# Gate only
python3 .agents/tools/runners/phase-d-run.py --verify

# Direct orchestrator use
python3 .agents/tools/adaptation/adapt_batch.py 1 9
python3 .agents/tools/adaptation/adapt_batch.py --resume
python3 .agents/tools/adaptation/adapt_batch.py --force
STE_MODEL=tencent/hy3:free python3 .agents/tools/adaptation/adapt_batch.py

# Gate with explicit directories
python3 .agents/tools/adaptation/verify-adaptation.py
python3 .agents/tools/adaptation/verify-adaptation.py --grouped ste-code/grouped --adapted ste-code/adapted
```

`--agent` and `--model` are accepted for ad-hoc single-worker use and are
forwarded as informational no-ops. The model is resolved from `STE_MODEL`.

---

## Rule sections

The orchestrator adapts these sections (`SECTIONS` in `adapt_batch.py`):

| Section | Name | Rules |
|:-------:|------|:-----:|
| 1 | Words | 14 |
| 2 | Multi-word Nouns | 3 |
| 3 | Verbs | 7 |
| 4 | Sentences | 5 |
| 5 | Procedural Writing | 5 |
| 6 | Descriptive Writing | 6 |
| 7 | Safety Instructions | 3 |
| 8 | Punctuation | 7 |
| 9 | Writing Practices | 4, plus GR1–GR4 |

!!! note
    The section map above is what `adapt_batch.py` expects and what
    `ste-code/adapted/` contains today: 54 `a-secN-ruleX.Y.md` files plus the
    four General Rule files, which is 58 files. The section counts sum to 54,
    and the README badge quotes the same 54.

---

## What the orchestrator does

* Slices the section text out of `ste-code/grouped/*.md` with the group
  headers that Stage C emits (for example `# Rules Sec 3`).
* Embeds the adaptation `SKILL.md` and the externalized worker prompt
  (`.agents/tools/runners/templates/phase-d-worker.md`,
  `.agents/tools/adaptation/templates/`).
* Refuses to start when `ste-code/grouped/` is missing, empty, or too small,
  and tells you to run `phase-c-run.py` first.
* Commits each section only after its verification gate passes.
* Writes a checkpoint after each section, so `--resume` is crash-safe.

The creative transform is model-driven on purpose. Everything around it stays
deterministic: chunking by section, externalized prompts, and gates that block
a bad section from being committed.

---

## Verification gate

`verify-adaptation.py` runs after the adapted files are written and checks the
classic failure modes:

* aerospace terms that leaked into the code-domain text,
* synonym drift (non-approved synonyms),
* missing rule files,
* missing Non-STE / STE example pairs,
* broken backlinks to the grouped source.

The gate is deterministic — no model and no network. Exit code `0` means all
gates pass.

---

## Next stage

[Stage E — Extension](stage-e.md) fills the documented code-domain gaps.
