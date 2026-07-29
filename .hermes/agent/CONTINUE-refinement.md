# CONTINUE — Refinement Orchestrator

You are the STE-Code REFINEMENT ORCHESTRATOR. Your job: take the 109 raw extraction files in `ste-code/extracted/` and reformat them into clean, standardized markdown in `ste-code/refined/`. The refinement preserves all content but fixes formatting, table structure, heading hierarchy, and example pair formatting.

## Setup

```bash
cd /Volumes/CORSAIR/Developer/macOS/Application/Manual
mkdir -p ste-code/refined
```

## Worker Launch Pattern

Each refinement worker takes one extracted file and produces one refined file:

```bash
hermes -z "Read ste-code/extracted/wNNN-pPPPP-PPPP.md. Reformat into clean standardized markdown. Preserve ALL content exactly — no summarization. Write to ste-code/refined/rNNN-pPPPP-PPPP.md. Output ONLY markdown." -m deepseek-pro --yolo
```

Launch 3 at a time. 109 total. See `ste-code/REFINE-PROGRESS.md` for the grid.

## Refinement Rules

- Zero content loss — every word preserved
- Table reconstruction — fix broken PDF→MD tables
- STE/non-STE example formatting — use blockquotes
- Dictionary entry normalization — consistent structure
- Heading hierarchy enforcement — ## for sections, ### for entries
- Remove page headers (Page N of 434) — keep only the ASD-STE100 header

## Skills

Load for detailed protocol:
- `skill_view(name='ste-code-refine')` — refinement protocol and formatting rules
- `skill_view(name='ste-code-validate')` — validation checks

## Git after each batch

```bash
git add -A && git gcommit-hermes
```
