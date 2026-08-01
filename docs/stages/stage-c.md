# Stage C — Grouping

**Purpose:** reorganize the 109 refined page files into 24 semantically
coherent group files. This stage is **deterministic**: it concatenates and
splits, and no model re-types the content.

| | |
|---|---|
| **Reads** | `ste-code/refined/rNNN-pA-B.md` |
| **Writes** | `ste-code/grouped/group-NNN-*.md` (24 groups) plus `GROUPING-NOTES.md` |
| **Type** | Pure Python, no LLM |
| **Runner** | `.agents/tools/runners/phase-c-run.py` |
| **Orchestrator** | `.agents/tools/grouping/group_batch.py` |
| **Gate** | `.agents/tools/grouping/verify-groups.py` |

---

## Commands

```bash
# Plan only, write nothing
python3 .agents/tools/runners/phase-c-run.py --dry-run

# Assemble the groups, then run the post-assembly gate
python3 .agents/tools/runners/phase-c-run.py --verify

# Overwrite existing groups
python3 .agents/tools/runners/phase-c-run.py --force

# Direct assembler use
python3 .agents/tools/grouping/group_batch.py --dry-run
python3 .agents/tools/grouping/group_batch.py --plan-json

# Gate on its own
python3 .agents/tools/grouping/verify-groups.py
```

`--agent` and `--model` are accepted but ignored, and the runner prints a note
that says so: grouping is deterministic, so there is no agent to select.

---

## Why this stage has no LLM

An earlier version gave the full 109-file → 24-group concatenation (about
600 KB of output) to one free-tier model and asked it to re-emit every byte.
That guarantees mid-stream truncation, which is silent, corpus-wide content
loss. Grouping is a reorganization and not a judgement, so it is pure Python:
bytes are moved, never re-typed.

---

## The 24 groups

| Group | Contents |
|-------|----------|
| `group-001-front-matter.md` | Front matter |
| `group-002-toc-and-nav.md` | Table of contents and navigation |
| `group-003-introduction.md` | Introduction |
| `group-004-rules-sec-1.md` … `group-012-rules-sec-9.md` | Rule sections 1–9 |
| `group-013-dictionary-intro.md` | Dictionary introduction |
| `group-014-dict-a-b.md` … `group-023-dict-t-y.md` | Dictionary, split into balanced alphabetical buckets |
| `group-024-appendix.md` | Appendix |

The dictionary is split into buckets of about 28 pages so the downstream
adaptation reader never receives a 285-page monolith.

---

## Key tools

| Tool | Purpose |
|------|---------|
| `.agents/tools/grouping/group_engine.py` | The single source of the plan and the parity primitives |
| `.agents/tools/grouping/group_batch.py` | Assembler and in-run gates |
| `.agents/tools/grouping/dict_normalize.py` | Converts each refined dictionary page into one clean 4-column table |
| `.agents/tools/grouping/verify-groups.py` | Post-assembly verifier |
| `.agents/tools/grouping/repair_markers.py` | Repairs page markers |
| `.agents/tools/grouping/diagnose_markers.py` | Diagnoses marker problems |
| `.agents/tools/grouping/test_grouping.py` | Grouping tests |

The plan lives in one module (`group_engine.py`) that the assembler, the
verifier, and the runner all import, so the plan and the gate cannot disagree.

---

## Verification gate

`verify-groups.py` must pass all five checks:

1. **Coverage** — every page from 1 to 434 appears in exactly one group, and
   the group page ranges tile the corpus with no gap and no overlap.
2. **Parity** — for each group, the content-token multiset of the written file
   equals the multiset of its source pages. Missing tokens are named, so a
   regression is diagnosable.
3. **Marks** — every `<mark>` highlight in the sources survives into the group.
4. **No split dictionary entry** — no dictionary group starts or ends in the
   middle of an entry.
5. **One table** — each dictionary group contains exactly one table header.

---

## Next stage

[Stage D — Adaptation](stage-d.md) reads `ste-code/grouped/`.
