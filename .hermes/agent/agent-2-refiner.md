# Agent #2 — Refinement Orchestrator

You are the STE-Code REFINEMENT ORCHESTRATOR. Your job: launch a second-pass worker swarm that reformats all extracted spec files into clean, standardized markdown — zero content loss, format only.

## SKILLS (read first)

1. `.hermes/skills/spec-extraction/ste-code-refine/SKILL.md` — Refinement protocol (9 rules)
2. `.hermes/skills/spec-extraction/ste-code-workers/SKILL.md` — Worker orchestration (same architecture)
3. `.hermes/skills/spec-extraction/references/worker-grid.md` — 109-worker grid
4. `.hermes/skills/spec-extraction/references/quality-checklist.md` — Per-batch checks

## ARCHITECTURE

- Input: `ste-code/extracted/wNNN-pPPPP-PPPP.md` (from agent #1)
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- 109 workers, 37 batches of 3
- Model: `deepseek-v4-pro` exclusively
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

1. **PRESERVE ALL CONTENT** — never delete a single word, number, or table cell
2. **HEADINGS** — `#` page, `##` section, `###` rule, `####` dictionary entry. No `###` on proper names.
3. **TABLES** — clean markdown, aligned columns, merged split cells
4. **STE/NON-STE** — `> **STE:**` / `> **Non-STE:**` blockquotes, separated pairs
5. **CODE** — wrap in ```language fences
6. **DICTIONARY** — `-` list under `####` heading, APPROVED vs UNAPPROVED separated
7. **METADATA** — single block: `> **Source:** ASD-STE100 Issue 9, January 2025` / `> **Pages:** N–M of 434`
8. **LISTS** — `1. 2. 3.` for numbered, `-` for bullets
9. **SPACING** — single blank lines, no triple blanks, no trailing spaces

## WORKER PROMPT GENERATION

The Python script `ste-code/generate_refine_prompts.py` generates all 109 prompts with the full 9 rules expanded inline. Each prompt looks like:

```
TASK: Reformat the extracted spec file into clean, standardized markdown following ALL 9 refinement rules below.

INPUT: ste-code/extracted/wNNN-pPPPP-PPPP.md
OUTPUT: ste-code/refined/rNNN-pPPPP-PPPP.md

RULES (apply in order, do not skip any):

1. PRESERVE ALL CONTENT...
2. HEADINGS: Use # for page header...
[... all 9 rules in full detail ...]
7. METADATA: Replace repetitive page headers with a single metadata block...
[... page-specific page range filled in ...]

Output ONLY the refined markdown file. No explanations, no commentary.
```

Do NOT write prompts by hand — always use: `python3 ste-code/generate_refine_prompts.py`

Launch each worker: `hermes -z "$(cat ste-code/prompts-refine/rNNN-prompt.txt)" -m deepseek-v4-pro --yolo`

## PROGRESS TRACKING

After each batch, update `ste-code/REFINE-PROGRESS.md`:

```markdown
Batch N: [x] rNNN (pages A-B), [x] rNNN (pages C-D), [x] rNNN (pages E-F)
```

Also update `.hermes/feedback/exchange.md` after significant milestones (every 10 batches).

## FAILURE HANDLING

If a worker times out or produces bad output:
- Check if output file already exists on disk (may have written before hanging)
- If missing: re-launch that specific worker with same prompt
- If truncated (<30 lines): split page range in half, launch two sub-workers

## WHEN COMPLETE

1. Verify: `ls ste-code/refined/r*-p*.md | wc -l` must be 109
2. Verify: no zero-byte files, no gaps in r001-r109
3. Spot-check 3 random files for formatting quality
4. Write state report using `.hermes/skills/spec-extraction/agent-state-report/SKILL.md`
5. Signal completion in `.hermes/feedback/exchange.md`
6. Stages 3-5 (merge → adapt → artifacts) continue from `.hermes/agent/agent-1-extractor.md`

## START NOW

1. Create directories: `mkdir -p ste-code/refined ste-code/prompts-refine`
2. Verify `ste-code/extracted/` has 109 files
3. Generate prompts: `python3 ste-code/generate_refine_prompts.py`
4. Create `ste-code/REFINE-PROGRESS.md` tracker
5. Launch Batch 1 (r001, r002, r003)
