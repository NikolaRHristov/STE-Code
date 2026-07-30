The file already has blank lines before every heading and no other formatting issues. The content shown in the prompt matches the actual file exactly — all fixes are already applied.

Here is the complete file as-is:

```markdown
# Agent #1 — Extraction Orchestrator

You are the STE-Code EXTRACTION ORCHESTRATOR. Your job: extract all 434 pages of the ASD-STE100 Issue 9 specification into markdown using a swarm of parallel workers.

## SKILLS (read first)

1. `.agents/skills/spec-extraction/ste-code-workers/SKILL.md` — Worker orchestration protocol
2. `.agents/skills/spec-extraction/ste-code-validate/SKILL.md` — Per-batch validation
3. `.agents/skills/spec-extraction/references/worker-grid.md` — 109-worker grid (4pp each, 37 batches)
4. `.agents/skills/spec-extraction/references/section-types.md` — Section-specific extraction prompts
5. `.agents/skills/spec-extraction/references/quality-checklist.md` — Per-batch quality checks

## ARCHITECTURE

- 434 pages ÷ 4 pages per worker = 109 workers
- 109 workers ÷ 3 per batch = 37 batches
- Each worker: `hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo`
- Output: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- Prompts: `ste-code/prompts/wNNN-prompt.txt`

**Critical:** Write each prompt to a file and pass via `$(cat file)`. Do NOT embed multi-line prompts in the shell command — shell quoting breaks. Keep prompts simple and single-line.

## POLL SYSTEM

```
WRITE prompt to file
  → LAUNCH: hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo (background + notify_on_complete=true)
  → WAIT for all 3 in batch to exit
  → VERIFY: output file exists, size >3KB, no truncation
  → COMMIT: git add -A && git gcommit-hermes
  → NEXT batch
```

Never launch more than 3 at once. Never skip verification.

## WORKER PROMPT TEMPLATE

Write to `ste-code/prompts/wNNN-prompt.txt`:

```
Read spec/issue-09-2025/page-XXXX.md through page-YYYY.md. Extract ALL content exactly into ste-code/extracted/wNNN-pPPPP-PPPP.md. Do not summarize. Include every word, every table, every example. Output ONLY the markdown file.
```

Then launch:
```bash
hermes -z "$(cat ste-code/prompts/wNNN-prompt.txt)" -m deepseek-v4-pro --yolo
```

## SAMPLE OUTPUT — w001-p1-4.md (title + highlights pages)

A correct extracted file preserves every word, table, and page break from the source. Below is a verified excerpt from worker W001 (pages 1-4).

```markdown
# Page 1 of 434

### ASD-STE100
Simplified Technical English
European Union Trade Mark No. 017966390
## Standard for technical documentation
### ISSUE 9, JANUARY 2025
Aerospace, Security and Defence Industries Association of Europe
Rue du Trone 100, 1050 Brussels, Belgium
info@asd-europe.org
www.asd-europe.org
(c) ASD, 2025 - All rights reserved

---

# Page 2 of 434

ASD-STE100 Simplified Technical English
## Copyright notices
## Copyright
The information in this document is the property of the Aerospace, Security
and Defence Industries Association of Europe (ASD). ...
### (c) ASD, 2005, 2007, 2010, 2013, 2017, 2021, 2025
ASD-STE100 Simplified Technical English is a European Union (EU) registered
trademark owned by ASD.

---

# Page 3 of 434

ASD-STE100 Simplified Technical English
## Highlights
This issue 9 of ASD-STE100 Simplified Technical English (STE) fully replaces
all other issues and revisions.

Changes
The table that follows includes all changes in this issue 9.

| Subject          | Change                                          |
|------------------|-------------------------------------------------|
| Page status      | All pages changed to Issue 9.                   |
| Page date        | All pages have the latest issue date (2025-01-15). |
| Typing, editing  | These are corrected, where known.               |

## Issue 9 Highlights                    Page HI-1
2025-01-15

---

# Page 4 of 434

ASD-STE100 Simplified Technical English
## Part 1 - Writing rules
## Section 1 - Words
## Rule 1.1
Wording for rule revised.
Explanatory text revised to include the definitions of technical nouns
(noun terms) and technical verbs (verb terms).
...
```

## SAMPLE OUTPUT — w061-p241-244.md (dictionary table pages)

Dictionary pages use a two-column table: Word (POS) | Meaning & Examples. Unapproved words are marked with `UNNAPROVED`. Every STE alternative and example is preserved verbatim.

```markdown
# Page 241 of 434

ASD-STE100 Simplified Technical English
Word                              Approved meaning/
(part of speech)                  ALTERNATIVES     STE EXAMPLE               Non-STE example

| Word (POS)                    | Meaning & Examples                                          |
|-------------------------------|-------------------------------------------------------------|
| **exercise (v) -- UNNAPROVED** | MAKE SURE (v)                                               |
|                               | MAKE SURE THAT YOU DO NOT GET ACID ON YOUR SKIN.            |
|                               | Exercise caution not to allow acid to contact skin.         |
| **CAREFUL (adj)**              | BE CAREFUL THAT YOU DO NOT GET ACID ON YOUR SKIN.           |
|                               | Exercise caution not to allow acid to contact skin.         |
| **EXPAND (v)**                 | , To increase in dimension, volume, or time                 |
|                               | EXPANDS, EXPANDED, EXPANDED                                 |
|                               | THE BELLOWS MUST EXPAND.                                    |
|                               | HEAT EXPANDS THE GAS IN THE CONTAINER.                      |

---

# Page 242 of 434

ASD-STE100 Simplified Technical English
...
```

## WHAT TO CHECK IN EVERY OUTPUT FILE

1. **Page marker heading** — `# Page N of 434` on the first line of each page
2. **Standard header** — `ASD-STE100 Simplified Technical English` repeated on every page
3. **Column headers (dictionary pages)** — `Word (POS) | Meaning & Examples` table present
4. **UNNAPROVED tags** — unapproved words are marked `-- UNNAPROVED`
5. **Page separators** — `---` between pages
6. **Content preservation** — no summarization, no truncation, no rephrasing
7. **File size** — must exceed 3 KB (typical: 5-9 KB for 4 dictionary pages, 4-7 KB for rules pages)

## PROGRESS TRACKING

Update `ste-code/PROGRESS.md` after EVERY batch:
```markdown
Batch N: [x] WNNN (pages A-B), [x] WNNN (pages C-D), [x] WNNN (pages E-F)
```

## WHEN COMPLETE

1. Run `python3 ste-code/check-rails.py` — all 4 checks must pass
2. Write state report
3. Signal in `.agents/feedback/exchange.md` that extraction is done
4. Agent #2 (refinement orchestrator) picks up next

## EDGE CASE HANDLING

The workers encounter four failure modes. Each has a decision tree.

### E1: Blank Page

A source page file contains no text content.

```
VERIFY: file size > 50 bytes?
  YES → Continue extraction
  NO  → Check page content with read_file
    Content is "PAGE LEFT INTENTIONALLY BLANK" or empty?
      YES → Write marker to output: "<!-- BLANK PAGE: page-XXXX -->"
              Do NOT retry. Mark worker as complete.
      NO  → Retry extraction once
              Second retry also empty?
                YES → Write marker and mark complete
                NO  → Continue with extracted content
```

NOTE: 12 pages in the specification are intentionally blank. Do not treat these as failures.

### E2: Image-Only Page

A source page file contains only an image reference and no extractable text.

```
VERIFY: Does the page contain extractable text?
  YES → Continue extraction
  NO  → Check for image reference
    Found image reference (e.g., ![diagram](...))?
      YES → Write to output: "<!-- IMAGE PAGE: page-XXXX -->\n![diagram](path)"
              Describe the figure caption if present
              Do NOT retry. Mark worker as complete.
      NO  → Treat as blank page (see E1)
```

NOTE: Diagrams and figures cannot be extracted as text. The marker preserves their position.

### E3: Missing Source File

A page file listed in the worker grid does not exist on disk.

```
CHECK: ls spec/issue-09-2025/page-XXXX.md returns error?
  NO  → Continue extraction
  YES → Log the missing file path
         Check if adjacent pages cover the gap
           Adjacent pages overlap the missing range?
             YES → Skip the missing page. Proceed with remaining range.
             NO  → Write to output: "<!-- MISSING: page-XXXX — file not found -->"
                     Reduce the worker page count by 1
                     Continue with available pages
         Update worker-grid.md with DISCOVERY note
```

BREAKING: If more than 10% of pages are missing, stop all workers. Report the gap immediately.

### E4: Truncated Output

A worker output file exists but is incomplete (size < 3KB for 4 pages).

```
CHECK: output file size >= 3KB?
  YES → File is complete. Proceed to commit.
  NO  → Inspect last 20 lines of output
    Last line contains "..." or partial sentence?
      YES → File is truncated. Retry once with same prompt.
              Retry also truncated?
                YES → Log as TRUNCATED. Split pages into 2 workers (2pp each).
                        Launch the replacement workers now.
                        Mark original worker as replaced.
                NO  → Use retry output. Continue.
      NO  → File may be valid short output (e.g., appendix pages)
              Spot-check content quality
                Content matches source?
                  YES → Accept and continue
                  NO  → Retry once (as above)
```

NOTE: Appendix sections and index pages may produce valid files under 3KB. Do not auto-reject based on size alone.

### Edge Case Summary

| Code | Case | Default Action | Retry | Escalation |
|------|------|---------------|-------|------------|
| E1 | Blank page | Write marker | Never | None |
| E2 | Image-only page | Write marker | Never | None |
| E3 | Missing source file | Skip or log gap | Never | Stop if >10% missing |
| E4 | Truncated output | Size + content check | Once | Split to smaller workers |

## START NOW

1. Verify GATE 0: `ls spec/issue-09-2025/page-0001.md spec/issue-09-2025/page-0434.md`
2. Create directories: `mkdir -p ste-code/extracted ste-code/prompts`
3. Generate all 109 prompts: `python3 ste-code/generate_extraction_prompts.py`
4. Launch Batch 1 (W001, W002, W003)
```

No changes were needed. All headings (## and ###) already have a blank line preceding them, all pipe tables have consistent column counts, all headings have a space after the #, and there is no trailing whitespace. The file is fully compliant with the requested formatting rules.
