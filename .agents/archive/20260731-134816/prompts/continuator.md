# Continuator Role — Agent-Agnostic Pipeline Stages 3-5

You take on the CONTINUATOR role. Extraction and refinement are done. Your job: merge, adapt, and produce the 6 final artifact files.

## READ THESE FIRST

1. `.agents/skills/merging/SKILL.md` — Stage 3: Merge protocol
2. `.agents/skills/adaptation/SKILL.md` — Stage 4: Adaptation protocol
3. `.agents/skills/artifacts/SKILL.md` — Stage 5: Artifact generation
4. `.agents/references/category-mapping.md` — 19-category mapping
5. `.agents/skills/state-report.md` — State reports

## STAGE 3 — MERGE

1. Read all 109 refined files from `ste-code/refined/r001-p1-4.md` through `r109-p433-434.md`
2. Concatenate in page order into `ste-code/merged/master-raw.md`
3. Deduplicate: remove repeated rule statements, category listings, dictionary entries at page boundaries
4. Organize by section into `ste-code/merged/master.md`
5. Validate: count 53 rules, 19 categories, dictionary entries
6. Spot-check 10 random pages against original spec pages

## STAGE 4 — ADAPTATION

Only after master.md is validated. Write to `ste-code/adapted/`.

### PRESERVE (unchanged from spec)
- All 53 rule numbers and 9-section organization
- 6-pass transformation pipeline
- Dictionary architecture: APPROVED vs UNAPPROVED
- 19 Technical Code Noun categories
- 4 Technical Code Verb categories

### REPLACE (adapt for code domain)
- Every STE/non-STE example pair → code documentation examples
- Technical noun categories → code-domain categories
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

## STAGE 5 — ARTIFACTS

Only after ALL adaptation is complete. Write to `ste-code/artifacts/`:

| # | File | Target Size |
|---|------|-------------|
| 1 | `ste-code-distilled-system-prompt.txt` | ~1,200 tokens |
| 2 | `ste-code-self-reading-manual.txt` | ~7,000 tokens |
| 3 | `ste-code-extraction-methodology.txt` | ~1,400 tokens |
| 4 | `ste-code-example-turn.txt` | ~500 tokens |
| 5 | `ste-code-deployment-guide.txt` | ~1,800 tokens |
| 6 | `README.md` | ~500 tokens |

## ANTI-FABRICATION RULES

1. Every adapted rule MUST reference a specific rule_number from master.md
2. Every synonym MUST trace to master.md's synonym table
3. Every category MUST match one of the 19 from master.md
4. Every example MUST be an adaptation of a real STE/non-STE pair
5. No invented code terms without a master.md source
6. Write artifacts ONLY after all adaptation checkboxes pass
7. 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-pro)

## KEY FACTS (immutable)

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules
- Model: poolside/laguna-s-2.1:free
- 434 pages in ASD-STE100 Issue 9, January 2025

## START NOW

1. Verify pipeline state (run file counts)
2. Begin Stage 3: merge all 109 refined files
3. Proceed to Stage 4 only after master.md passes all checks
4. Proceed to Stage 5 only after all adaptation files pass checks
