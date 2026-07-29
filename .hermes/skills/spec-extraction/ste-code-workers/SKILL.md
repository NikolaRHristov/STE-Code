---
name: ste-code-worker-orchestration
description: "Launch parallel hermes -z workers to extract spec pages into markdown, batched in groups of 3."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [spec-extraction, workers, parallel, batch, ste-code, asd-ste100]
---

# STE-Code Worker Orchestration

## Overview

Extract large specifications into structured markdown using parallel `hermes -z` worker sessions. Coordinator oversees; workers read pages and write output.

**Core principle:** Fresh `hermes -z` session per batch = clean context = high-fidelity extraction.

## When to Use

- Extracting 100+ page specification documents
- Parallel read-heavy extraction tasks
- Building knowledge bases from structured documents

## Quick Start

```bash
# 1. Create worker prompts
# 2. Launch Batch 1 (3 workers)
cd PROJECT_ROOT
hermes -z "$(cat workers/w1-prompt.txt)" -m deepseek-pro --yolo &
hermes -z "$(cat workers/w2-prompt.txt)" -m deepseek-pro --yolo &
hermes -z "$(cat workers/w3-prompt.txt)" -m deepseek-pro --yolo &

# 3. Wait for completion, verify outputs
# 4. Launch Batch 2 (W4, W5, W6)
# 5. Launch Batch 3 (W7, W8, W9)
```

## Worker Split (434-page spec)

| Worker | Pages | Task | Output |
|--------|-------|------|--------|
| W1 | 1–30 | Front matter, TOC, Section 1.1-1.6 | w1-sec1-rules.md |
| W2 | 31–66 | Rules 1.7-1.14, 22 TN categories, 4 TV categories, Sections 2-3 | w2-sec2-3-rules.md |
| W3 | 67–94 | Sections 3-5 rules | w3-sec3-5-rules.md |
| W4 | 95–114 | Sections 6-8 rules | w4-sec6-8-rules.md |
| W5 | 115–128 | Section 9 + GR-1 to GR-8 | w5-sec9-gr-rules.md |
| W6 | 129–240 | Dictionary A–F | w6-dict-a-f.md |
| W7 | 241–300 | Dictionary G–P | w7-dict-g-p.md |
| W8 | 301–360 | Dictionary Q–Z | w8-dict-q-z.md |
| W9 | 361–434 | Appendices, index, history | w9-appendices.md |

## Prompt Template

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE.

PAGES: spec/issue-09-2025/page-<START>.md through page-<END>.md

TASK: Read every page and extract ALL content into <OUTPUT_FILE>

INCLUDE: [specific targets]

FORMAT: Markdown with ## headings. Quote examples as blockquotes.
Preserve EXACT text. Output ONLY the markdown file.
```

## Launch Rules

- **Always** use `hermes -z "$(cat prompt.txt)"` — never inline multi-line prompts
- **Always** add `--yolo` to skip approval prompts
- **Always** use `-m deepseek-pro` (normalizes to deepseek-v4-flash)
- **Never** use `hermes --cli` with stdin pipe (0 tool calls)
- **Never** more than 3 workers simultaneously
- **Always** verify output before launching next batch

## Verification

After each batch:
1. Check output file size (>5KB per worker)
2. Check last 10 lines for mid-sentence truncation
3. If truncated, split worker into smaller page ranges

## Full Prompts

See `references/worker-prompts.md` for all 9 prompts used for ASD-STE100 Issue 9 extraction.
