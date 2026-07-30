---
description: "Launch parallel hermes -z workers to extract spec pages into markdown, batched in groups of 3. 4 pages per worker, 109 workers total."
version: "3.0.0"
related: [".agents/references/worker-grid.md", ".agents/references/section-types.md", ".agents/references/rails.md"]
---

# Extraction Worker Orchestration

Extract the 434-page ASD-STE100 Issue 9 spec using 109 parallel `hermes -z` workers, each processing exactly 4 pages. Coordinated in 37 batches of 3 workers. This skill is agent-agnostic — any agent can use it.

## Worker Command Template

```bash
hermes -z "Read spec/issue-09-2025/page-<<START>>.md through page-<<END>>.md. 
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

## Quality Checks (Per Batch)

1. All 3 output files exist in `ste-code/extracted/`
2. Each file > 3KB (>30 lines)
3. Last 3 lines end cleanly (no mid-word truncation)
4. Expected keywords present
5. No fabrication signals (no "TODO", "TBD", modern software terms)
6. PROGRESS.md updated

If any check fails, re-extract with the worker's page range split in half.

## Worker Grid: `.agents/references/worker-grid.md`
## Section types: `.agents/references/section-types.md`
