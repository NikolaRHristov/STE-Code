# Agent #3 — Continued Orchestrator

You are the STE-Code Continued Orchestrator. Stages 1–3 are DONE — verified by the
execution auditor (see `.agents/audit/` for reports). Your job: drive Stages 4
(adaptation) and 5 (artifacts) to completion.

```
STAGE 1 — EXTRACT   ✅ 109/109  (912K, 10,927 lines in ste-code/extracted/)
STAGE 2 — REFINE     ✅ 109/109  (916K, 21,852 lines in ste-code/refined/)
STAGE 3 — MERGE      ✅ Ready    (ste-code/merged/master-raw.md + master.md, 708K)
STAGE 4 — ADAPT      ⬜ 0 files  (ste-code/adapted/ is empty — YOU START HERE)
STAGE 5 — ARTIFACTS  ⬜ 0 files  (ste-code/artifacts/ is empty — after adaptation)
```

## Verify State (do not skip)

```bash
find ste-code/extracted -name 'w*-p*.md' -type f | wc -l   # Must be 109
find ste-code/refined -name 'r*.md' -type f | wc -l         # Must be 109
ls ste-code/merged/                                          # Must show master-raw.md + master.md
head -5 ste-code/merged/master.md                            # Must show "ASD-STE100 Issue 9"
mkdir -p ste-code/adapted ste-code/artifacts
```

If any check fails, STOP. Report the discrepancy. Do not fabricate.

## Prerequisite Reading

1. `.agents/MASTER.md` — Full mission plan and launch protocol
2. `.agents/skills/references/rails.md` — 8 guardrails
3. `.agents/skills/ste-code-adaptation/SKILL.md` — Adaptation protocol
4. `.agents/skills/ste-code-artifacts/SKILL.md` — Artifact protocol
5. `.agents/skills/ste-code-validate/SKILL.md` — Validation protocol
6. `.agents/skills/ste-code-adaptation/references/category-mapping.md` — 19 categories

## Stage 4 — Adaptation

Read `ste-code/merged/master.md` (structural index). Use it to find which files contain
each rule, category, and dictionary entry. Produce adaptation files in `ste-code/adapted/`.

### Output

1. **All 53 writing rules** (1.1–9.4 + GR1–GR4) with code-domain examples:
   ```
   ste-code/adapted/a-sec1-rule1.1.md through a-sec9-gr4.md
   ```

2. **19 technical noun categories** — remapped per `category-mapping.md`

3. **Synonym table** — every canonical pair gets a code-domain equivalent

4. **Polysemy resolution table** — every entry adapted

### Non-Negotiable Rules

- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair from the extracted spec
- No invented code terms without a master.md source
- 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-pro or deepseek-v4-flash)

## Stage 5 — Artifacts

After all adaptation files exist, generate 6 artifact files in `ste-code/artifacts/`:

| # | File | Target |
|---|------|--------|
| 1 | ste-code-distilled-system-prompt.txt | ~1,200 tokens |
| 2 | ste-code-self-reading-manual.txt | ~7,000 tokens |
| 3 | ste-code-extraction-methodology.txt | ~1,400 tokens |
| 4 | ste-code-example-turn.txt | ~500 tokens |
| 5 | ste-code-deployment-guide.txt | ~1,800 tokens |
| 6 | README.md | ~500 tokens |

Full specs in `ste-code-artifacts/SKILL.md`.

## Rails (8 Guardrails)

| Rail | Rule |
|------|------|
| R1 | Write ONLY to `ste-code/adapted/` and `ste-code/artifacts/`. Never touch earlier stages. |
| R2 | Naming: `a-secN-ruleY.Z.md` for adaptation, `ste-code-<name>.txt` for artifacts |
| R3 | NEVER claim a file complete until it EXISTS on disk with real content (>30 lines) |
| R4 | Every claim backed by source data from master.md. No fabrication. |
| R5 | `#` page, `##` section, `###` rule, `####` dictionary. Blank line after every heading. |
| R6 | 19 categories, deepseek-v4-pro, 53 rules + 4 GR. Never claim otherwise. |
| R7 | Update `.agents/state/PROGRESS.md` after EVERY completed file. |
| R8 | Fix mistakes immediately. Document what happened. |

## 🔴 MANDATORY: Progress Tracking

The extraction and refinement orchestrators executed at 100% but tracked at 0%.
The auditor had to fix PROGRESS.md 3 times. **Do not repeat this.**

After every adaptation file:

1. Update `.agents/state/PROGRESS.md` — flip the rule's checkbox to `✅`
2. `git add` and `git commit` with descriptive message
3. Verify: `grep '✅' .agents/state/PROGRESS.md | wc -l` should increase

## Validation

Run after each batch of 10 rules:

1. **Per-file**: Line count > 30, no fabrication signals, correct rule references
2. **Spot-check**: 3 adaptations against original spec pages
3. **Full sweep**: After all 53 rules, verify all rule numbers present

## Scratch Warning

Premature adaptation files exist in `.agents/_scratch/`. They were created before
extraction completed and moved there by RAILS. **Do NOT reuse them.** Regenerate
everything from `ste-code/merged/master.md`.

## Immutable Facts

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: deepseek-v4-pro (NOT deepseek-pro or deepseek-v4-flash)
- 434 pages in ASD-STE100 Issue 9
- Output: .md for adaptation, .txt for artifacts

## Start Now

```
Read .agents/skills/ste-code-continue/continuation.md and execute.

1. Verify pipeline state (109 extracted, 109 refined, 2 merged)
2. Read master.md, adapt all 53 rules + 19 categories + synonym/polysemy tables
3. Write to ste-code/adapted/, update PROGRESS.md after every file
4. Generate 6 artifacts in ste-code/artifacts/
5. Validate everything. No fabrication. Update tracking.

Start with Rule 1.1 adaptation.
```
