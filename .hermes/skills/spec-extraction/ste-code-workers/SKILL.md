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

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

Extract the 434-page ASD-STE100 Issue 9 spec using 109 parallel `hermes -z` workers,
each processing exactly 4 pages. Coordinated in 37 batches of 3 workers.

**v3 changes from v2:**
- CORRECTED: `hermes -z` DOES support file I/O (verified with W0 test)
- 4 pages per worker (not 30-112) — prevents truncation
- 109 workers (not 9) — full parallelization
- Output to `ste-code/extracted/` (not `ste-code/extracted/`)
- Prompts in `.hermes/prompts/refine/` (separate from output)


> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## When to Use

- Extracting 100+ page specification documents
- When extraction fidelity is critical (no summarization, no truncation)
- When the coordinator should oversee rather than extract inline

## Worker Command Template

```bash
hermes -z "Read spec/issue-09-2025/page-<<START_PAGE>>.md through page-<<END_PAGE>>.md. 
Extract ALL content exactly into ste-code/extracted/w<<NNN>>-p<<START>>-<<END>>.md.
Do not summarize. Include every word, every table, every example.
Output ONLY the markdown file." -m deepseek-v4-pro --yolo
```

## Launch Rules

- **Always** use `hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo`
- **Always** launch exactly 3 workers per batch (never more)
- **Always** verify output after each batch before launching next
- **Never** use inline extraction — it defeats parallelization
- **Never** exceed 4 pages per worker (prevents truncation)
- **Always** save state: `git gcommit-hermes "Batch N complete"` after each batch

## 🔴 MANDATORY: Progress Tracking

**After EVERY batch, update `.hermes/state/PROGRESS.md` before launching the next batch.**
This is NOT optional. The execution auditor cross-references PROGRESS.md against disk
evidence. A stale PROGRESS.md is treated as a 🔴 CRITICAL tracking discrepancy.

To update:
1. Flip the batch's `[ ]` to `[x]` for all 3 workers in PROGRESS.md
2. Update the progress counter line at the bottom
3. Verify the update: `grep "\[x\]" .hermes/state/PROGRESS.md | wc -l` should match completed workers

```markdown
# Example: after completing Batch 27, change:
| 27 | W079(313-316), W080(317-320), W081(321-324) | 313-324 | [x] |

# And update:
**Progress: 81/109 workers (74%) — 324/434 pages**
```

## Quality Checks (Per Batch)

After each batch of 3 workers completes:

1. **File check**: All 3 output files exist in `ste-code/extracted/`
2. **Size check**: Each file > 3KB (>30 lines) for 4-page extraction
3. **Truncation check**: Last 3 lines end cleanly (period, footer, or table row)
4. **Content signal**: Expected keywords present (see section-types.md for per-range signals)
5. **Fabrication check**: No commentary, no modern examples in spec extraction
6. **Tracking check**: PROGRESS.md updated to reflect this batch ✅

If any check fails, re-extract with the worker's page range split in half.

## Worker Grid

Full grid at: `references/worker-grid.md`
Section types at: `references/section-types.md`

**Progress: 109/109 workers complete (ALL 37 batches, pages 1-434) ✨ EXTRACTION COMPLETE**
