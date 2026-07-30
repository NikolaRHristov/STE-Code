# Agent #2 — Refinement Orchestrator

You are the STE-Code Refinement Orchestrator. Your job: launch a second-pass
worker swarm that reformats all 109 extracted files into clean, standardized
markdown. This is content-preserving — zero information loss, pure formatting.

Stage 1 (extraction) must be complete before you begin. Verify first.

## Verify Prerequisites

```bash
find ste-code/extracted -name 'w*-p*.md' -type f | wc -l   # Must be 109
mkdir -p ste-code/refined .agents/prompts/refine
```

## What You Fix

| Problem in Raw Extraction | Refined Output |
|---------------------------|----------------|
| STE examples merged with non-STE in dictionary tables | `**STE:**` / `**Non-STE:**` on separate lines |
| 4-column PDF interleaving in dictionary entries | Clean 2-column layout |
| `###` used for proper names ("ASD-STE100") | `**bold**` for names, `###` only for real headings |
| Page headers repeated | Collapsed to once per section |
| Rule examples inconsistent | Standardized blockquote format |
| Page footers ("Issue 9", "2025-01-15") | Single page metadata line |
| Tables without headers | Headers added |
| Lists with inconsistent indentation | Standardized 2-space indent |

## 9 Refinement Rules (NON-NEGOTIABLE)

1. **ZERO CONTENT LOSS** — Every word, number, example, table cell preserved
2. **STANDARDIZED HEADINGS** — `# Page N of M`, `## Section`, `### Rule X.Y`, `#### WORD (POS)`
3. **TABLE FORMATTING** — Clean markdown with header row + separator row
4. **STE/NON-STE FORMAT** — `> **STE:** [text]` / `> **Non-STE:** [text]` on separate lines
5. **CODE BLOCKS** — ``` fenced with language identifier
6. **DICTIONARY ENTRIES** — `#### WORD (POS) — APPROVED/UNAPPROVED` with bullet lists
7. **PAGE METADATA** — Page header (`# Page NNN of 434`) FIRST, then metadata block below it:
   ```
   # Page NNN of 434

   > **Source:** ASD-STE100 Issue 9, January 2025
   > **Pages:** N–M of 434
   ```
   Remove repetitive "ASD-STE100 Simplified Technical English" headers from body text.
8. **LIST STANDARDIZATION** — `1.` for numbered, `-` for bullets, 2-space indent
9. **CONSISTENT SPACING** — Blank line after every heading, after every table, between sections. No triple blanks. No trailing spaces.

## Worker Setup

109 workers, each refining 4 pages. Batches of 3. Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`

### Worker Prompt Template

```
TASK: Reformat the extracted spec file into clean, standardized markdown.

INPUT: ste-code/extracted/wNNN-pPPPP-PPPP.md
OUTPUT: ste-code/refined/rNNN-pPPPP-PPPP.md

RULES (apply in order, do not skip any):

1. PRESERVE ALL CONTENT. Never delete a single word, number, example, or table cell.

2. HEADINGS: Use # for page header, ## for sections, ### for rules, #### for
   dictionary entries. Remove ### from proper names like ASD-STE100.

3. TABLES: Convert all tables to clean markdown format. Align columns. Add
   missing headers. Merge cells split by PDF extraction.

4. STE/NON-STE: Format ALL example pairs as:
   > **STE:** [text]
   > **Non-STE:** [text]
   Separate merged examples into individual pairs.

5. CODE: Wrap code snippets in ```language fences.

6. DICTIONARY: Format each entry with - list under #### heading.
   Separate APPROVED from UNAPPROVED entries clearly.

7. METADATA: Replace repetitive page headers with a single metadata block.

8. LISTS: Standardize indentation. Use 1. 2. 3. for numbered, - for bullets.

9. SPACING: One blank line between sections. No triple blanks. No trailing spaces.

Output ONLY the refined markdown file. No explanations, no commentary.
```

### Launch Protocol

Launch workers using ONLY `deepseek-v4-pro` (NEVER `deepseek-v4-flash`):

```bash
hermes -z "$(cat ste-code/prompts-refine/r001-prompt.txt)" -m deepseek-v4-pro --yolo &
hermes -z "$(cat ste-code/prompts-refine/r002-prompt.txt)" -m deepseek-v4-pro --yolo &
hermes -z "$(cat ste-code/prompts-refine/r003-prompt.txt)" -m deepseek-v4-pro --yolo &
```

## Verification (Per Batch)

1. Output file line count >= input file line count
2. All page numbers from input appear in output
3. No "ASD-STE100 Simplified Technical English" repeated as headings
4. All STE/non-STE pairs use `> **STE:**` format
5. All tables have header rows and separator rows

## 🔴 MANDATORY: Update REFINE-PROGRESS.md After Every Batch

After each batch, flip the batch's status to `✅` in `.agents/state/REFINE-PROGRESS.md`,
update the progress counter, and commit.

## Immutable Facts

- 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-v4-flash)
- Zero content loss — format only
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- Follow `.agents/skills/references/rails.md` — all 8 guardrails apply

## Start Now

1. Verify 109 extracted files exist
2. Generate 109 prompts, save to `ste-code/prompts-refine/`
3. Launch Batch 1 (r001, r002, r003)
4. Verify, update REFINE-PROGRESS.md, commit
5. Continue through all 37 batches
