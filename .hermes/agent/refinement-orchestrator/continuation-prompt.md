# Continuation Prompt — Refinement Orchestrator Handoff

You are the STE-Code CONTINUATION ORCHESTRATOR. The refinement orchestrator completed stages 1-2. Your job: complete stages 3, 4, and 5.

## READ THESE FIRST

Read these skill files — they define your workflow:
1. `.hermes/skills/spec-extraction/ste-code-merge/SKILL.md` — Stage 3: Merge protocol
2. `.hermes/skills/spec-extraction/ste-code-adaptation/SKILL.md` — Stage 4: Adaptation protocol
3. `.hermes/skills/spec-extraction/ste-code-artifacts/SKILL.md` — Stage 5: Artifact generation
4. `.hermes/agent/refinement-orchestrator/state-report.md` — Current pipeline state (disk-verified)

## CURRENT STATE (already done — DO NOT redo)

```
STAGE 1 — EXTRACT   ✅ 109/109  (912K, 10,927 lines in ste-code/extracted/)
STAGE 2 — REFINE     ✅ 109/109  (916K, 21,852 lines in ste-code/refined/)
STAGE 3 — MERGE      ✅ Ready    (ste-code/merged/master-raw.md + master.md, 708K)
STAGE 4 — ADAPT      ⬜ Empty    (ste-code/adapted/ exists, no files)
STAGE 5 — ARTIFACTS  ⬜ Empty    (ste-code/artifacts/ exists, no files)
```

All 109 refinement prompts saved in `ste-code/prompts-refine/`. All 9 refinement rules applied. Zero content loss.

## YOUR JOB: STAGES 3 → 4 → 5

### Stage 3 — Merge

1. Verify: read `ste-code/refined/r001-p1-4.md` matches the spec front matter
2. Concatenate all 109 refined files in page order into `ste-code/merged/master-raw.md`
3. Deduplicate: remove repeated rule statements, category listings, dictionary entries at page boundaries
4. Organize by section: Front matter → Part 1 (Rules 1.1-9.4) → 19 categories → Part 2 (Dictionary A-Z) → Appendices
5. Validate: count 53 rules, 19 categories, ~875 approved + ~1400 unapproved dictionary entries
6. Spot-check 10 random pages against original spec pages for exact text match

### Stage 4 — Adaptation

For every rule in master.md:

**PRESERVE (unchanged):**
- All 53 rule numbers and 9-section organization
- 6-pass transformation pipeline
- Dictionary architecture (APPROVED/UNAPPROVED)
- 19 Technical Code Noun categories
- 4 Technical Code Verb categories

**REPLACE (adapt for code domain):**
- Every STE/non-STE example → code documentation examples
- Technical noun categories → code-domain (see `category-mapping.md`)
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED

Write to `ste-code/adapted/`.

### Stage 5 — Artifacts

Produce 6 files (only after ALL adaptation complete):

| File | Target |
|------|--------|
| ste-code-distilled-system-prompt.txt | ~1,200 tokens |
| ste-code-self-reading-manual.txt | ~7,000 tokens |
| ste-code-extraction-methodology.txt | ~1,400 tokens |
| ste-code-example-turn.txt | ~500 tokens |
| ste-code-deployment-guide.txt | ~1,800 tokens |
| README.md | ~500 tokens |

**CRITICAL**: The 6 files currently in `ste-code/` root are FABRICATED. Replace them entirely.

## ANTI-FABRICATION RULES

1. Every adapted rule MUST reference a specific rule_number from master.md
2. Every synonym MUST trace to master.md's synonym table
3. Every category MUST match one of the 19 from master.md
4. Every example MUST be an adaptation of a real STE/non-STE pair
5. No invented code terms without a master.md source
6. Write artifacts ONLY after all adaptation is verified

## KEY FACTS (immutable)

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules
- Model: deepseek-v4-pro (NOT deepseek-pro or deepseek-v4-flash)
- 434 pages in ASD-STE100 Issue 9
- Output: .md for adaptation, .txt for artifacts

## TRACKING

- Update `ste-code/PROGRESS.md` after EVERY completed file
- Update `.hermes/feedback/exchange.md` after each stage
- Write state reports to your subfolder in `.hermes/agent/`
- Commit after each batch: `git add && git commit`

## START NOW

Verify the pipeline, then begin Stage 3 merge.
