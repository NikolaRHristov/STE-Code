---
description: "Generate code-domain placeholder entries for STE-Code gaps using batched poll workers. Dictionary, categories, anti-patterns, domain extensions."
version: "1.0.0"
related: [".agents/agent/agent-8-extension-worker.md", "SCE/core/categories/synonym-table.json", "SCE/data/vocabulary/approved-verbs.json"]
---

# Extension Worker Orchestration — Agent-Agnostic

Generate code-domain extensions to fill gaps between aerospace ASD-STE100 and the code documentation domain. Uses the same batched poll worker pattern as Agent #1 (Extractor).

## Gap Areas

| # | Area | Target Count | Current | Gap |
|---|------|:---:|:---:|:---:|
| 1 | Approved Verbs (with code examples) | 50 | 35 | 15 |
| 2 | Approved Adjectives (with code examples) | 25 | ~6 | 19 |
| 3 | Noun Category Examples (concrete) | 200 | ~114 | 86 |
| 4 | Verb Category Examples | 20 | 0 | 20 |
| 5 | Code Anti-Patterns | 15 | 5 | 10 |
| 6 | Domain Extensions | 50 | ~3 | 47 |

## Worker Command Template

```bash
hermes -z "$(cat /tmp/ext-worker-prompt.txt)" -m deepseek-v4-pro --yolo > OUTPUT_FILE 2>&1 &
```

## Launch Rules
- 3 workers per batch (never more)
- Verify output after each batch
- `git gcommit-hermes "Extension batch N: <area>"` after each batch
- Never exceed 20 entries per worker

## Output Directories
- Verbs: `SCE/data/vocabulary/generated/`
- Adjectives: `SCE/data/vocabulary/generated/`
- Noun examples: `SCE/core/categories/generated/`
- Anti-patterns: `SCE/compute/generated/`
- Domain extensions: `SCE/data/vocabulary/generated/`

## Entry Schema
See `.agents/agent/agent-8-extension-worker.md` for full JSON schemas.

## State
Progress tracked in `.agents/state/EXTENSION-PROGRESS.md`
