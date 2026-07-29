---
name: ste-code-workers
description: "Launch parallel hermes -z workers to extract spec pages into markdown, batched in groups of 3. v3: 4 pages per worker, 109 workers total."
version: 3.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [spec-extraction, workers, parallel, batch, ste-code]
---

# STE-Code Worker Orchestration v3

## Overview

Extract the 434-page ASD-STE100 Issue 9 spec using 109 parallel `hermes -z` workers,
each processing exactly 4 pages. Coordinated in 37 batches of 3 workers.

**v3 changes from v2:**
- CORRECTED: `hermes -z` DOES support file I/O (verified with W0 test)
- 4 pages per worker (not 30-112) — prevents truncation
- 109 workers (not 9) — full parallelization
- Output to `ste-code/extracted/` (not `ste-code/workers/`)
- Prompts in `ste-code/prompts/` (separate from output)

## When to Use

- Extracting 100+ page specification documents
- When extraction fidelity is critical (no summarization, no truncation)
- When the coordinator should oversee rather than extract inline

## Worker Command Template

```bash
hermes -z "Read spec/issue-09-2025/page-<<START_PAGE>>.md through page-<<END_PAGE>>.md. 
Extract ALL content exactly into ste-code/extracted/w<<NNN>>-p<<START>>-<<END>>.md.
Do not summarize. Include every word, every table, every example.
Output ONLY the markdown file." -m deepseek-pro --yolo
```

## Launch Rules

- **Always** use `hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo`
- **Always** launch exactly 3 workers per batch (never more)
- **Always** verify output after each batch before launching next
- **Never** use inline extraction — it defeats parallelization
- **Never** exceed 4 pages per worker (prevents truncation)
- **Always** save state: `git gcommit-hermes "Batch N complete"` after each batch

## Quality Checks (Per Batch)

After each batch of 3 workers completes:

1. **File check**: All 3 output files exist in `ste-code/extracted/`
2. **Size check**: Each file > 3KB (>30 lines) for 4-page extraction
3. **Truncation check**: Last 3 lines end cleanly (period, footer, or table row)
4. **Content signal**: Expected keywords present (see section-types.md for per-range signals)
5. **Fabrication check**: No commentary, no modern examples in spec extraction

If any check fails, re-extract with the worker's page range split in half.

## Progress Tracking

Update `ste-code/PROGRESS.md` after each batch:
```markdown
Batch N: [x] W### (pages A-B), [x] W### (pages C-D), [x] W### (pages E-F)
```

## Worker Grid

Full grid at: `references/worker-grid.md`
Section types at: `references/section-types.md`

Currently: 12/109 workers complete (batches 1-4, pages 1-48)
