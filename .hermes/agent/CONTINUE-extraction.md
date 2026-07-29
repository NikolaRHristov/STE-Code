# CONTINUE — Extraction Orchestrator

You are the STE-Code EXTRACTION ORCHESTRATOR. Your job: launch parallel hermes -z workers to extract spec pages into markdown. The coordinator launches workers in batches of 3; workers read pages and write output. Coordinator oversees, polls, verifies, merges.

## When to use

The extraction pipeline needs to be re-run (new spec version, different document, recovery from corruption).

## Setup

```bash
cd /Volumes/CORSAIR/Developer/macOS/Application/Manual
mkdir -p ste-code/extracted
```

## Worker Launch Pattern

Each worker reads 4 pages and writes verbatim markdown:

```bash
hermes -z "Read spec/issue-09-2025/page-NNNN.md through page-NNNN.md. Extract ALL verbatim into ste-code/extracted/wNNN-pPPPP-PPPP.md. No summary. Markdown only." -m deepseek-pro --yolo
```

Launch 3 at a time via background terminal. Wait for all 3 to complete, then git save, then next batch. Never more than 3 simultaneously.

## Worker Grid

434 pages ÷ 4 = 109 workers, 37 batches. See `.hermes/skills/spec-extraction/references/worker-grid.md` for the full grid.

## Skills

Load for detailed protocol:
- `skill_view(name='ste-code-workers')` — launch protocol, batch management
- `skill_view(name='ste-code-merge')` — merge into master after extraction

## Key files

- `ste-code/extracted/` — worker output goes here (109 .md files)
- `ste-code/merged/master.md` — merge target
- `ste-code/PROGRESS.md` — progress tracker

## Git after each batch

```bash
git add -A && git gcommit-hermes
```
