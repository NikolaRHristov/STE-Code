# STE-Code Final Pass Plan — Worker-Driven, Self-Healing

> **Trigger:** After the other agent completes maturity fixes + expansion generators.
> **Principle:** Every task is a poll worker. Every worker self-heals. Every batch commits.
> **Model:** `deepseek-v4-pro` exclusively. Batch size: 3. Pattern: `hermes -z "$(cat prompt.txt)" --yolo` + `write_file`.

---

## Architecture: 6-Phase Pipeline

```
Phase A: Maturity Fixes      →  Apply audit gaps to ~85 instruction files
Phase B: Expansion (5 Passes) →  Code-domain examples, dictionary, categories, anti-patterns, paradigms
Phase C: SCE Population       →  Rules + vocabulary + synonyms + system prompts → SCE/
Phase D: Artifact Regen       →  Rebuild 6 deployable artifacts from expanded content
Phase E: Translations         →  Discovery + blank placeholders for 9 locales
Phase F: Final Audit          →  Cross-check every output, rail verification, consistency
```

## Worker Count

| Phase | Workers | Batches | Self-Healing |
|-------|:------:|:------:|-------------|
| A — Maturity Fixes | 61 | 21 | Re-run failed fix prompts with narrowed scope; skip already-applied fixes |
| B1 — Rule Examples | 55 | 19 | Detect duplicate JSON entries → re-launch with expanded blacklist; validate JSON schema before accept |
| B2 — Dictionary Depth | 30 | 10 | Per-term: check if already in approved-verbs/adjectives JSON → skip; detect conflicting definitions → flag for human |
| B3 — Category Entries | 9 | 3 | Cross-check category IDs against master.md → flag mismatches; ensure no duplicate terms across categories |
| B4 — Anti-Patterns + Paradigms | 6 | 2 | Anti-patterns: verify each violates a specific P# from the 14 principles; Paradigms: verify each example compiles (pseudocode) |
| C — SCE Population | 18 | 6 | Validate frontmatter YAML against schema before write; check rule IDs match adapted file numbering |
| D — Artifact Regen | 6 | 2 | Token budget check per artifact spec; cross-reference every claim to master.md source line |
| E — Translations | 30 | 10 | Check placeholder file exists + empty before skip; catalog re-sync after each locale batch |
| F — Final Audit | 10 | 4 | 8-rail compliance per output; zero-byte sweep; gap analysis between expected vs actual file counts |
| **Total** | **225** | **77** | |

## Self-Healing Per Worker

Every worker embeds this protocol in its prompt:

```
BEFORE WRITING OUTPUT:
1. Check if output file already exists with valid content → SKIP (don't overwrite)
2. Check if input dependencies exist on disk → if missing, write RECOVERY-NEEDED marker instead
3. Validate output against schema/format rules → if invalid, retry once with narrowed scope
4. Check for duplication against blacklist → if duplicate found, generate alternative
5. Report: [PASS|SKIP|RETRY|RECOVERY] + metrics (entries generated, blacklist hits, time)

AFTER WRITING:
6. Verify file on disk: test -f <output> && wc -c <output> > 0
7. If verification fails: write RECOVERY-NEEDED/<worker-id>.md with exact failure details
8. Self-commit: never commit alone — wait for batch coordinator
```

## Phase A: Maturity Fixes (61 workers)

**Source:** 61 pre-generated prompts in `.agents/prompts/maturity-fixes/`

**Per-worker task:** Read target file → apply gaps + improvements → write improved file.

**Self-healing:**
- Before writing: `diff` against original to verify changes are additive (no deletions)
- After writing: verify file parses correctly (`.md` → valid headings, `.py` → `python3 -c "compile(open(...).read(), ...)" ` → syntax OK, `.json` → `json.load`)
- On failure: re-launch with single-gap scope (only fix the first gap, skip the rest)

**Priority order:** HIGH files first (Agent #3, #4, #5 broken refs) → MEDIUM → LOW.

**Recovery:** `RECOVERY-NEEDED/<prompt-name>.md` lists: target file, attempted gap, failure reason, suggested narrower prompt.

---

## Phase B: Expansion (5 Passes)

### B1 — Rule Examples (55 workers, 19 batches)
**Already prompted.** Each worker generates 3-5 new STE/non-STE code example pairs for one adapted rule file.

**Self-healing:**
- Validate output is valid JSON with required fields (`rule`, `principle`, `ste_example`, `non_ste_example`)
- Check all `non_ste_example` strings against synonym blacklist — flag violations
- Verify no aerospace terms (`aircraft`, `engine`, `ream`, `flange`, `screw`, `actuator`, `fuselage`, `landing gear`) in any output
- Dedup against ALL previously generated entries in `ste-code/adapted/expanded/*.json`
- On duplicate: increment retry counter, add found duplicates to blacklist, re-launch

### B2 — Dictionary Depth (30 workers, 10 batches)
**Not yet prompted.** Target: ~875 approved + ~1,400 unapproved terms from `ste-code/adapted/a-dictionary.md` (5,943 lines).

**Per-worker scope:** ~75 terms each. For each term, generate:
```json
{"term": "deploy", "type": "verb", "approved": true,
 "code_meaning": "Move code or configuration to a target environment.",
 "code_example_ste": "Deploy the application to production.",
 "code_example_non_ste": "Ship the app to prod when ready.",
 "replaces_code_terms": ["ship", "roll out", "push to"],
 "domain": "CI/CD"}
```

**Self-healing:**
- Cross-reference each term against `SCE/data/vocabulary/approved-verbs.json` and `approved-adjectives.json` — skip if already defined
- Detect conflicting meanings between aerospace and code domains → flag, don't overwrite
- Verify `code_meaning` doesn't recycle aerospace wording verbatim
- On schema violation: retry with stricter format enforcement

### B3 — Category Entries (9 workers, 3 batches)
**Not yet prompted.** Target: 10+ concrete code-domain terms per 19 categories.

**Per-worker scope:** 2 categories each (except last worker: 3). For each category, generate terms with definitions and approved status.

**Self-healing:**
- Verify each category ID matches `ste-code/adapted/a-categories.md` numbering
- Check no term appears in multiple categories (cross-category dedup)
- Ensure each term has a `definition` field that's code-domain specific (not a copy of the category name)

### B4 — Anti-Patterns + Paradigms (6 workers, 2 batches)
**Not yet prompted.** 
- **Anti-patterns (3 workers, 1 batch):** 30 code-specific documentation anti-patterns, each tied to a specific P# violation
- **Paradigms (3 workers, 1 batch):** 6 paradigms (OOP, FP, Procedural, Declarative, Systems, Scripting) × 3 code examples each

**Self-healing (anti-patterns):**
- Verify each anti-pattern violates exactly one P# principle
- Check `ste_example` actually demonstrates STE-Code compliance (not just reworded non-STE)
- Validate `severity` field is one of: `blocking`, `warning`, `advisory`

**Self-healing (paradigms):**
- Verify each example uses correct paradigm idioms (OOP → classes, FP → pure functions, etc.)
- Check examples don't cross-contaminate paradigms
- Ensure each example pair shows the STE documentation alongside the code

---

## Phase C: SCE Population (18 workers, 6 batches)

### Schema validation upfront
Before any worker runs, verify `SCE/compute/schemas/rule-frontmatter.schema.json` and `vocabulary-entry.schema.json` exist. If missing (as maturity audit found), generate them from the v2 copies at `ste-code/v2/compute/schemas/`.

### C1 — Rule Population (9 workers, 3 batches)
**1 worker per section** (9 sections: sec1-sec9). Each reads all adapted rules in its section, creates `SCE/core/rules/rule-X.Y.md` with YAML frontmatter + adapted content.

**Self-healing:**
- Validate frontmatter YAML against schema before write
- Verify `id` field matches filename (`rule-1.1.md` → `id: rule-1.1`)
- Check `section` and `principle` fields match the rule's location in the spec
- On schema fail: retry with only the frontmatter block, skip body content

### C2 — Vocabulary JSON (3 workers, 1 batch)
Three workers reading `master.md` dictionary section: one for approved verbs, one for approved adjectives, one for unapproved entries.

**Self-healing:**
- Validate each entry against `vocabulary-entry.schema.json`
- Dedup: if term already in `SCE/data/vocabulary/approved-verbs.json`, skip
- Check POS tags match dictionary conventions (v, adj, n, prep, adv, conj)
- On schema fail: retry with individual entry scope

### C3 — Synonym Table (1 worker)
Read merged dictionary, extract all unapproved→approved pairs, write `SCE/core/categories/synonym-table.json`.

**Self-healing:**
- Verify each unapproved term has exactly one approved alternative
- Check no circular references (A→B and B→A)
- Validate against existing `ste-code/v2/data/synonyms/synonym-table.json` for consistency

### C4 — System Prompts (4 workers, 2 batches)
Regenerate 4 SCE system prompts from artifact content: `ste-code-micro.md`, `ste-code-full.md`, `ste-code-agentic.md`, `ste-code-developer.md`.

**Self-healing:**
- Token budget check: micro (~400), full (~4,000), agentic (~2,500), developer (full)
- Cross-reference: every principle and synonym must trace to an adapted rule or dictionary entry
- Verify `--yolo` compatible (no interactive prompts)

### C5 — Validation (1 worker)
Run all SCE files against their schemas. Flag violations.

---

## Phase D: Artifact Regeneration (6 workers, 2 batches)

Rebuild the 6 deployable artifacts from expanded adapted rules + dictionary.

| # | Artifact | Token Budget | Workers |
|---|----------|:---:|:---:|
| 1 | `ste-code-distilled-system-prompt.txt` | ~1,200 | 1 |
| 2 | `ste-code-self-reading-manual.txt` | ~7,000 | 1 |
| 3 | `ste-code-extraction-methodology.txt` | ~1,400 | 1 |
| 4 | `ste-code-example-turn.txt` | ~500 | 1 |
| 5 | `ste-code-deployment-guide.txt` | ~1,800 | 1 |
| 6 | `README.md` | ~500 | 1 |

**Self-healing:**
- Token count check: `wc -c <file>` ÷ 4 ≈ tokens; must be within ±20% of budget
- Cross-reference check: every claim must trace to a specific master.md line or adapted rule
- Anti-fabrication: no term, example, or fact without a source in the pipeline
- On budget violation: trim or expand with structured additions

---

## Phase E: Translations (30 workers, 10 batches)

10 discovery targets × 3 locale workers each. Workers explore source directories, reason about translatability, create blank placeholders for 9 locales.

**Can run in parallel with Phases C+D** — translations only read source files, never modify pipeline output.

**Self-healing:**
- Skip files that already have placeholders (`test -f translations/<locale>/<path>`)
- Verify placeholder is actually empty (`wc -c == 0`) — if not, flag as POLLUTED
- Re-sync catalog after each locale batch
- On discovery of new source directory not in the 10-target list: append to list automatically

---

## Phase F: Final Audit (10 workers, 4 batches)

Cross-check every output against expectations.

| Check | Workers | What |
|-------|:------:|------|
| File counts | 2 | Count expected vs actual per directory; flag gaps |
| Zero-byte sweep | 1 | Find any zero-byte or truncated output files |
| Rail compliance | 3 | 8-rail verification per pipeline stage |
| Consistency | 2 | Cross-reference adapted rules ↔ SCE rules ↔ system prompts ↔ dictionary |
| Benchmark re-run | 2 | Re-run 59 tests against regenerated artifacts; compare scores |

**Self-healing:**
- Auto-fix safe patterns: stale files, duplicate files, incorrect naming (wNNN vs rNNN)
- Flag unfixable: missing content, conflicting definitions, rail violations
- Produce final state report with trust scores per phase

---

## Execution Order

```
Phase A (already prompted) → Phase B1 (already prompted)
                            → Phase B2-B4 (needs prompt generation)
                            → Phase C  (needs prompt generation)
                            → Phase D  (depends on C)
Phase E (parallel with C+D) ┘
Phase F (after all phases)  ┘
```

**Critical path:** A → B1 → B2 → C → D → F (~55 batches, ~55 minutes)
**Parallel track:** E and F-audit run alongside.

## Commit Cadence

- Commit after EVERY batch (3 workers)
- Message format: `phase:<letter> batch:<N> — <what was done>`
- Push after every 3 batches

## Recovery Protocol

If any batch fails:
1. Check `RECOVERY-NEEDED/` for auto-generated recovery markers
2. Read recovery file → understand what failed and why
3. Re-launch affected workers with narrowed scope (split the task)
4. Never skip a failed batch — every [ ] in progress tracker must become [x] before next phase
