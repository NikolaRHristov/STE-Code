---
id: ste-code-agentic
version: 1.0.0
tokens: ~800
use-when: pipeline agent context
---

# STE-Code Agentic — Agent Behavioral Layer

Load this file as the behavioral constraint layer for any STE-Code pipeline agent. This file covers ONLY agent behavior — for vocabulary and rule content, load `ste-code-micro.md` or `ste-code-full.md`.

---

## Rails (All Blocking Unless Noted)

**R001 — No fabrication:** Every claim must trace to a source file or spec page. Never invent page numbers, rule IDs, or file paths.

**R002 — No truncation:** Never truncate output. If the task cannot complete in one turn, commit partial work and report state.

**R003 — Commit before state change:** Commit all completed work before beginning a new stage or batch.

**R004 — State report every turn (warning):** End every turn with: files written | pages covered | gate status | next action.

**R005 — One term per concept:** Never alternate synonyms for the same entity within a document.

**R006 — Approved vocabulary only:** Check synonym-table.json before using any term.

**R007 — Sentence length (warning):** Max 20 words procedural, max 25 words descriptive.

**R008 — Safety markers:** Use BREAKING / DEPRECATED / NOTE. BREAKING requires version + migration path.

---

## Gate Conditions

| Gate | Stage | Key Test |
|------|-------|----------|
| GATE-0 | Pre-extract | Source PDF present, page count correct |
| GATE-1 | Post-extract | All 109 files present, no truncation, no fabrication |
| GATE-2 | Post-refine | All 109 refined files present, source references intact |
| GATE-3 | Post-adapt | All 55 rule files present, valid frontmatter |
| GATE-4 | Post-artifact | All 6 artifacts present, system prompt ≤ 3,000 tokens |

---

## Worker Contract

**Must:** Process only the assigned range | write file before reporting | include state block | trace all claims | commit before next batch.

**Must not:** Invent content | truncate output | start next stage before gate passes | write outside assigned directory.

**State block format:**
```
files_written: [paths]
pages_covered: pXXX-pXXX
gate_status: PASS | FAIL | PENDING
next_action: [description]
```
