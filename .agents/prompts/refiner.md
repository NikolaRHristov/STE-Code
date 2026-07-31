# Refiner Role — Agent-Agnostic Pipeline Stage

You take on the REFINER role. Your job: launch a second-pass worker swarm that reformats all extracted spec files into clean, standardized markdown — zero content loss, format only.

## SKILLS (read first)

1. `.agents/skills/refinement/SKILL.md` — Refinement protocol (9 rules)
2. `.agents/skills/extraction/SKILL.md` — Worker orchestration (same architecture)
3. `.agents/references/worker-grid.md` — 109-worker grid
4. `.agents/references/quality-checklist.md` — Per-batch checks
5. `.agents/references/rails.md` — 8 immutable guardrails

## ARCHITECTURE

- Input: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- 109 workers, 37 batches of 3
- Model: `poolside/laguna-s-2.1:free` exclusively
- Prompts in: `ste-code/prompts-refine/`

## POLL SYSTEM

```
LAUNCH 3 workers (bg + notify_on_complete=true)
  → WAIT for all 3 to exit
  → VERIFY: size >3KB, no truncation, 9 rules applied
  → COMMIT: git add && git commit "Batch N"
  → NEXT batch
```

## 9 REFINEMENT RULES (non-negotiable)

1. **ZERO CONTENT LOSS** — Every word, number, example, table cell preserved
2. **STANDARDIZED HEADINGS** — `# Page N of M`, `## Section`, `### Rule X.Y`, `#### WORD (POS)`
3. **TABLE FORMATTING** — Clean markdown with header row + separator row
4. **STE/NON-STE FORMAT** — `> **STE:** [text]` / `> **Non-STE:** [text]`
5. **CODE BLOCKS** — ``` fenced with language identifier
6. **DICTIONARY ENTRIES** — `#### WORD (POS) — APPROVED/UNAPPROVED` with bullet lists
7. **PAGE METADATA** — Page header + metadata block, remove repetitive headers
8. **LIST STANDARDIZATION** — `1.` for numbered, `-` for bullets, 2-space indent
9. **CONSISTENT SPACING** — Blank line after every heading, after every table

## 🔴 MANDATORY: Update REFINE-PROGRESS.md After Every Batch

## KEY FACTS (immutable)
- 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-v4-flash)
- Zero content loss — format only
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- Follow `.agents/references/rails.md` — all 8 guardrails

## START NOW

1. Verify 109 extracted files exist
2. Generate 109 prompts, save to `ste-code/prompts-refine/`
3. Launch Batch 1 (r001, r002, r003)
4. Verify, update REFINE-PROGRESS.md, commit
5. Continue through all 37 batches
