# Extractor Role — Agent-Agnostic Pipeline Stage

You take on the EXTRACTOR role. Your job: extract all 434 pages of the ASD-STE100 Issue 9 specification into markdown using a swarm of parallel workers. This role can be performed by any agent in the pipeline.

## SKILLS (read first — any agent can use these)

1. `.agents/skills/extraction/SKILL.md` — Worker orchestration protocol
2. `.agents/skills/auditing/SKILL.md` — Per-batch validation
3. `.agents/references/worker-grid.md` — 109-worker grid (4pp each, 37 batches)
4. `.agents/references/section-types.md` — Section-specific extraction prompts
5. `.agents/references/quality-checklist.md` — Per-batch quality checks

## ARCHITECTURE

- 434 pages ÷ 4 pages per worker = 109 workers
- 109 workers ÷ 3 per batch = 37 batches
- Each worker: `hermes -z "$(cat prompt.txt)" -m poolside/laguna-s-2.1:free --yolo`
- Input: `spec/issue-09-2025/page-dir/page-<spec-id>.md` (spec page identifiers)
- Output: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- Prompts: `ste-code/prompts/wNNN-prompt.txt`

**Critical:** Write each prompt to a file and pass via `$(cat file)`. Do NOT embed multi-line prompts in the shell command — shell quoting breaks. Keep prompts simple and single-line.

**Note:** The old `page-NNNN.md` files (sequential numbering) have been replaced by `page-dir/page-<spec-id>.md` files (spec page identifiers like HI-1, 1-1-1, 2-1-A1). Use `spec/issue-09-2025/split_spec.py` to regenerate if needed.

## POLL SYSTEM

```
WRITE prompt to file
  → LAUNCH: hermes -z "$(cat prompt.txt)" -m poolside/laguna-s-2.1:free --yolo (background + notify_on_complete=true)
  → WAIT for all 3 in batch to exit
  → VERIFY: output file exists, size >3KB, no truncation
  → COMMIT: git add -A && git gcommit-hermes
  → NEXT batch
```

Never launch more than 3 at once. Never skip verification.

## WORKER PROMPT TEMPLATE

Write to `ste-code/prompts/wNNN-prompt.txt`:

```
Read spec/issue-09-2025/page-dir/page-XXXX.md through page-YYYY.md. Extract ALL content exactly into ste-code/extracted/wNNN-pPPPP-PPPP.md. Do not summarize. Include every word, every table, every example. Output ONLY the markdown file.
```

Then launch:
```bash
hermes -z "$(cat ste-code/prompts/wNNN-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo
```

## PROGRESS TRACKING

Update `ste-code/PROGRESS.md` after EVERY batch:
```markdown
Batch N: [x] WNNN (pages A-B), [x] WNNN (pages C-D), [x] WNNN (pages E-F)
```

## WHEN COMPLETE

1. Run `python3 ste-code/check-rails.py` — all 4 checks must pass
2. Write state report using `.agents/skills/state-report.md`
3. Signal in `.agents/feedback/exchange.md` that extraction is done
4. Any agent can then pick up the refiner role next

## START NOW

1. Verify GATE 0: `ls spec/issue-09-2025/page-dir/page-front-matter.md spec/issue-09-2025/page-dir/page-2-1-Y2.md`
2. Create directories: `mkdir -p ste-code/extracted ste-code/prompts`
3. Generate all 109 prompts: `python3 ste-code/generate_extraction_prompts.py`
4. Launch Batch 1 (W001, W002, W003)
