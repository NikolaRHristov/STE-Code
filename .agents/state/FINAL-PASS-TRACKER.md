# STE-Code Final Pass Plan — Single-Session Orchestration

> **One session to rule them all.** Launch, track, and verify every worker from one place.
> **Model:** `deepseek-v4-pro`. Batch size: 3. Pattern: `hermes -z "$(cat prompt.txt)" --yolo` + `write_file`.

---

## Single-Session Orchestration Protocol

The orchestrator (you) manages all 6 phases from one Hermes session. Track progress in `.agents/state/FINAL-PASS-TRACKER.md` (created at launch).

```
LAUNCH LOOP (per batch):
  1. Select next 3 workers from the current phase
  2. Launch: hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo (background + notify_on_complete=true)
  3. Wait for all 3 to exit
  4. VERIFY: output file exists, valid content, no self-healing failures
  5. UPDATE tracker: flip [ ] → [x] for completed workers
  6. COMMIT: git add -A && git gcommit-hermes "phase:<letter> batch:<N>"
  7. PUSH every 3 batches
  8. If batch fails: read RECOVERY-NEEDED/<worker>.md → fix → re-launch
  9. Continue until tracker shows all [x]
```

**Never launch more than 3 at once. Never skip verification. Never advance phase until all workers in current phase pass.**

---

## Master Worker Grid

| Phase | Workers | Batches | Prompts | Status |
|-------|:------:|:------:|---------|:------:|
| **A0** — Missing Maturity Fixes | 2 | 1 | Manual (inline) | ⬜ |
| **A** — Maturity Fixes | 61 | 21 | `.agents/prompts/maturity-fixes/` | ✅ Generated |
| **B1** — Rule Examples | 55 | 19 | `.agents/prompts/expansion-pass1/` | ✅ Generated |
| **B2** — Dictionary Depth | 30 | 10 | Needs generation | ⬜ |
| **B3** — Category Entries | 9 | 3 | Needs generation | ⬜ |
| **B4** — Anti-Patterns + Paradigms | 6 | 2 | Needs generation | ⬜ |
| **C** — SCE Population | 18 | 6 | Needs generation | ⬜ |
| **D** — Artifact Regen | 6 | 2 | Manual (per spec) | ⬜ |
| **E** — Translations | 30 | 10 | Manual (discovery) | ⬜ |
| **F** — Final Audit | 10 | 4 | Manual (commands) | ⬜ |
| **Total** | **227** | **78** | | |

---

## Phase A0: Missing Maturity Fixes (2 workers, 1 batch)

**These were skipped by Agent #4's 61-worker run despite being HIGH priority in the audit.** Fix them first before proceeding to expansion.

### A0-W1: Agent #5 — SCE Populator

**Target:** `.agents/agent/agent-5-sce-populator.md`
**Gaps from audit:**
- 2 broken schema references: `SCE/compute/schemas/rule-frontmatter.schema.json` and `vocabulary-entry.schema.json` — neither path exists
- No example of a complete populated rule file (frontmatter + body)
- No edge case handling for missing adapted files or conflicting alternatives
- Validation task is a single vague sentence

**Fix actions:**
1. Change schema references to actual paths: `ste-code/v2/compute/schemas/rule-frontmatter.schema.json` and `ste-code/v2/compute/schemas/vocabulary-entry.schema.json` (these exist on disk)
2. Add a complete example of a populated rule file (rule-1.1 with frontmatter + body)
3. Add edge case table: missing adapted file → log + skip, conflicting alternatives → prefer shorter approved word, count mismatch → diff and report
4. Replace validation step with concrete `jsonschema` commands

**Self-healing:** Verify both new schema paths exist before writing. If v2 schemas are also missing, generate schema inline from adapted file structure.

### A0-W2: Agent #6 — STE-Code Analysis Agent

**Target:** `.agents/agent/agent-6-phi-sce.md`
**Gaps from audit:**
- Zero cross-references to any project file — operates in vacuum
- No examples of completed output (template only, never filled in)
- No edge case handling: code keyword vs unapproved word, missing paradigm, uncorrectable violations
- No cross-reference to the full dictionary or adapted rules

**Fix actions:**
1. Add cross-references to: `ste-code/adapted/a-dictionary.md` (full dictionary), `ste-code/adapted/` (53 adapted rules), Agent #4 (source of rules), Agent #5 (source of vocabulary JSONs)
2. Add one complete worked example: Java method with docstring + filled-in audit table + corrections + unresolved items
3. Add edge case table: code keyword vs unapproved word → code keyword takes precedence (P5/P6), uncorrectable violation → flag in "Unresolved", missing paradigm → fall back to Procedural
4. Set minimum pass threshold: 12/14 principles must pass, P1-P4 hard fail

**Self-healing:** Verify all cross-referenced files exist on disk. Flag any broken references before writing.

### A0 Tracker

```
[A0 Batch 1: [ ] W1 (agent-5-sce-populator)  [ ] W2 (agent-6-phi-sce)]
```

---

## Phase A: Maturity Fixes (61 workers, 21 batches)

**Source:** 61 pre-generated prompts in `.agents/prompts/maturity-fixes/`. Already run once by Agent #4 — 20/22 HIGH files fixed. Re-run will self-skip already-fixed files. The 2 remaining HIGH files are handled in Phase A0 above.

**Self-healing:** Skip file if `git diff` shows changes already applied. Verify output parses correctly. On failure: re-launch with single-gap scope.

### Tracker

```
Batch A01: [ ] fix-001  [ ] fix-002  [ ] fix-003
Batch A02: [ ] fix-004  [ ] fix-005  [ ] fix-006
Batch A03: [ ] fix-007  [ ] fix-008  [ ] fix-009
Batch A04: [ ] fix-010  [ ] fix-011  [ ] fix-012
Batch A05: [ ] fix-013  [ ] fix-014  [ ] fix-015
Batch A06: [ ] fix-016  [ ] fix-017  [ ] fix-018
Batch A07: [ ] fix-019  [ ] fix-020  [ ] fix-021
Batch A08: [ ] fix-022  [ ] fix-023  [ ] fix-024
Batch A09: [ ] fix-025  [ ] fix-026  [ ] fix-027
Batch A10: [ ] fix-028  [ ] fix-029  [ ] fix-030
Batch A11: [ ] fix-031  [ ] fix-032  [ ] fix-033
Batch A12: [ ] fix-034  [ ] fix-035  [ ] fix-036
Batch A13: [ ] fix-037  [ ] fix-038  [ ] fix-039
Batch A14: [ ] fix-040  [ ] fix-041  [ ] fix-042
Batch A15: [ ] fix-043  [ ] fix-044  [ ] fix-045
Batch A16: [ ] fix-046  [ ] fix-047  [ ] fix-048
Batch A17: [ ] fix-049  [ ] fix-050  [ ] fix-051
Batch A18: [ ] fix-052  [ ] fix-053  [ ] fix-054
Batch A19: [ ] fix-055  [ ] fix-056  [ ] fix-057
Batch A20: [ ] fix-058  [ ] fix-059  [ ] fix-060
Batch A21: [ ] fix-061
```

---

## Phase B1: Rule Examples (55 workers, 19 batches)

**Source:** 55 pre-generated prompts in `.agents/prompts/expansion-pass1/`. Already tested — 3 workers passed (batch 001-003) with valid JSON output. Remaining 52 prompts ready.

**Launch command:**
```bash
hermes -z "$(cat .agents/prompts/expansion-pass1/pass1-batch-NNN.txt)" -m deepseek-v4-pro --yolo
```

**Self-healing:** Validate JSON. Check aerospace terms blacklist. Dedup against `ste-code/adapted/expanded/*.json`. On duplicate: re-launch with expanded blacklist.

### Tracker

```
Batch B1-01: [x] pass1-001  [x] pass1-002  [x] pass1-003
Batch B1-02: [ ] pass1-004  [ ] pass1-005  [ ] pass1-006
Batch B1-03: [ ] pass1-007  [ ] pass1-008  [ ] pass1-009
Batch B1-04: [ ] pass1-010  [ ] pass1-011  [ ] pass1-012
Batch B1-05: [ ] pass1-013  [ ] pass1-014  [ ] pass1-015
Batch B1-06: [ ] pass1-016  [ ] pass1-017  [ ] pass1-018
Batch B1-07: [ ] pass1-019  [ ] pass1-020  [ ] pass1-021
Batch B1-08: [ ] pass1-022  [ ] pass1-023  [ ] pass1-024
Batch B1-09: [ ] pass1-025  [ ] pass1-026  [ ] pass1-027
Batch B1-10: [ ] pass1-028  [ ] pass1-029  [ ] pass1-030
Batch B1-11: [ ] pass1-031  [ ] pass1-032  [ ] pass1-033
Batch B1-12: [ ] pass1-034  [ ] pass1-035  [ ] pass1-036
Batch B1-13: [ ] pass1-037  [ ] pass1-038  [ ] pass1-039
Batch B1-14: [ ] pass1-040  [ ] pass1-041  [ ] pass1-042
Batch B1-15: [ ] pass1-043  [ ] pass1-044  [ ] pass1-045
Batch B1-16: [ ] pass1-046  [ ] pass1-047  [ ] pass1-048
Batch B1-17: [ ] pass1-049  [ ] pass1-050  [ ] pass1-051
Batch B1-18: [ ] pass1-052  [ ] pass1-053  [ ] pass1-054
Batch B1-19: [ ] pass1-055
```

---

## Phase B2: Dictionary Depth (30 workers, 10 batches)

**Not yet prompted.** Target: ~875 approved + ~1,400 unapproved terms from `ste-code/adapted/a-dictionary.md` (5,943 lines). 75 terms per worker.

**Prompt generation:** Create prompts via a script (to be written) that reads the dictionary, splits terms into 30 batches, embeds synonym table + dedup blacklist.

**Self-healing:** Skip already-defined terms. Detect aerospace→code meaning conflicts. On schema fail: retry with stricter format.

### Tracker

```
Batch B2-01: [ ] dict-001  [ ] dict-002  [ ] dict-003
Batch B2-02: [ ] dict-004  [ ] dict-005  [ ] dict-006
Batch B2-03: [ ] dict-007  [ ] dict-008  [ ] dict-009
Batch B2-04: [ ] dict-010  [ ] dict-011  [ ] dict-012
Batch B2-05: [ ] dict-013  [ ] dict-014  [ ] dict-015
Batch B2-06: [ ] dict-016  [ ] dict-017  [ ] dict-018
Batch B2-07: [ ] dict-019  [ ] dict-020  [ ] dict-021
Batch B2-08: [ ] dict-022  [ ] dict-023  [ ] dict-024
Batch B2-09: [ ] dict-025  [ ] dict-026  [ ] dict-027
Batch B2-10: [ ] dict-028  [ ] dict-029  [ ] dict-030
```

---

## Phase B3: Category Entries (9 workers, 3 batches)

**Not yet prompted.** Target: 10+ concrete code-domain terms per 19 categories, 2 categories per worker.

**Self-healing:** Cross-check category IDs against `a-categories.md`. Dedup terms across categories.

### Tracker

```
Batch B3-01: [ ] cat-001  [ ] cat-002  [ ] cat-003
Batch B3-02: [ ] cat-004  [ ] cat-005  [ ] cat-006
Batch B3-03: [ ] cat-007  [ ] cat-008  [ ] cat-009
```

---

## Phase B4: Anti-Patterns + Paradigms (6 workers, 2 batches)

### Tracker

```
Batch B4-01: [ ] ap-001 (anti-patterns 1-10)  [ ] ap-002 (anti-patterns 11-20)  [ ] ap-003 (anti-patterns 21-30)
Batch B4-02: [ ] para-001 (OOP+FP)  [ ] para-002 (Procedural+Declarative)  [ ] para-003 (Systems+Scripting)
```

---

## Phase C: SCE Population (18 workers, 6 batches)

### Pre-flight
Before launching, verify schemas exist. If `SCE/compute/schemas/` is empty, copy from `ste-code/v2/compute/schemas/`:
```bash
mkdir -p SCE/compute/schemas
cp ste-code/v2/compute/schemas/rule-frontmatter.schema.json SCE/compute/schemas/ 2>/dev/null
cp ste-code/v2/compute/schemas/vocabulary-entry.schema.json SCE/compute/schemas/ 2>/dev/null
```

### Tracker

```
Batch C01: [ ] rules-sec1  [ ] rules-sec2  [ ] rules-sec3
Batch C02: [ ] rules-sec4  [ ] rules-sec5  [ ] rules-sec6
Batch C03: [ ] rules-sec7  [ ] rules-sec8  [ ] rules-sec9
Batch C04: [ ] vocab-verbs  [ ] vocab-adj  [ ] vocab-unapproved
Batch C05: [ ] synonym-table  [ ] prompt-micro  [ ] prompt-full
Batch C06: [ ] prompt-agentic  [ ] prompt-developer  [ ] sce-validate
```

---

## Phase D: Artifact Regeneration (6 workers, 2 batches)

### Tracker

```
Batch D01: [ ] distilled-prompt  [ ] self-reading-manual  [ ] methodology
Batch D02: [ ] example-turn  [ ] deployment-guide  [ ] readme
```

---

## Phase E: Translations (30 workers, 10 batches)

10 discovery targets × 3 locale workers (zh-CN+ja+ko, es+fr+de, pt-BR+ru+ar).

### Tracker

```
Batch E01: [ ] tr-artifacts-1  [ ] tr-artifacts-2  [ ] tr-artifacts-3
Batch E02: [ ] tr-adapted-1    [ ] tr-adapted-2    [ ] tr-adapted-3
Batch E03: [ ] tr-sce-prompts-1 [ ] tr-sce-prompts-2 [ ] tr-sce-prompts-3
Batch E04: [ ] tr-sce-examples-1 [ ] tr-sce-examples-2 [ ] tr-sce-examples-3
Batch E05: [ ] tr-sce-rules-1  [ ] tr-sce-rules-2  [ ] tr-sce-rules-3
Batch E06: [ ] tr-v2-prompts-1 [ ] tr-v2-prompts-2 [ ] tr-v2-prompts-3
Batch E07: [ ] tr-v2-examples-1 [ ] tr-v2-examples-2 [ ] tr-v2-examples-3
Batch E08: [ ] tr-v2-rules-1   [ ] tr-v2-rules-2   [ ] tr-v2-rules-3
Batch E09: [ ] tr-compute-1    [ ] tr-compute-2    [ ] tr-compute-3
Batch E10: [ ] tr-v2-compute-1 [ ] tr-v2-compute-2 [ ] tr-v2-compute-3
```

---

## Phase F: Final Audit (10 workers, 4 batches)

### Tracker

```
Batch F01: [ ] audit-counts-1  [ ] audit-counts-2  [ ] audit-zerobyte
Batch F02: [ ] audit-rail-1    [ ] audit-rail-2    [ ] audit-rail-3
Batch F03: [ ] audit-consistency-1  [ ] audit-consistency-2
Batch F04: [ ] benchmark-rerun-1    [ ] benchmark-rerun-2
```

---

## Execution Order

```
Phase A0 (missing fixes) → Phase A (maturity) → Phase B1 (rule examples)
                                                → Phase B2 (dictionary) → needs prompt gen
                                                → Phase B3 (categories) → needs prompt gen
                                                → Phase B4 (anti-patterns + paradigms)
                                                → Phase C (SCE population)
                                                → Phase D (artifact regen)
Phase E (translations — parallel with C+D) ┘
Phase F (final audit — after all) ┘
```

| Metric | Count |
|--------|:----:|
| Total workers | 227 |
| Total batches | 78 |
| Already prompted | 118 (A + B1) |
| Needs prompt generation | 64 (B2-B4 + C + D) |
| Manual/inline | 45 (A0 + E + F) |
| Pre-completed | 3 (B1 batch 1) |
| Critical path (A0→D) | ~62 batches |
| Wall-clock estimate | ~62 min at 3 concurrent |

## Commit Cadence

```
After EVERY batch:  git add -A && git gcommit-hermes "phase:<letter> batch:<N>"
After EVERY 3 batches: git push
Track in: .agents/state/FINAL-PASS-TRACKER.md (copy this file + flip [ ] → [x])
```

## Recovery Protocol

If any batch fails:
1. Check `RECOVERY-NEEDED/` for auto-generated recovery markers
2. Read recovery file → understand what failed and why
3. Re-launch affected workers with narrowed scope
4. Never leave a [ ] in the tracker — every batch must be [x] before phase advance
