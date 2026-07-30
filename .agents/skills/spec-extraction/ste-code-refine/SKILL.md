---
name: ste-code-refine
description: "Launch a second-pass worker swarm to reformat extracted spec files into clean, standardized markdown without losing any content. Fixes table formatting, headings, code blocks, and PDF extraction artifacts."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, refine, formatting, markdown, tables, workers, batch]
---

# STE-Code Refinement Orchestrator

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

After the extraction phase, a second worker swarm reformats all extracted files
into clean, highly legible, standardized markdown. This is a **content-preserving**
transformation — zero information loss, pure formatting improvement.

**Launch command (single line — paste into a new session):**

```
Read .agents/skills/spec-extraction/ste-code-refine/SKILL.md.
Launch the refinement worker swarm on all files in ste-code/extracted/.
4 pages per worker, batches of 3. Output to ste-code/refined/.
```


> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## When to Use

- After extraction phase is complete (all 109 raw files exist)
- When extracted tables show PDF 4-column interleaving artifacts
- When heading hierarchy is inconsistent
- When STE/non-STE examples are not clearly delineated
- When page headers/footers clutter the content
- Before adaptation phase (clean input = better adaptation)

## What This Fixes

| Problem in Raw Extraction | Refined Output |
|---------------------------|----------------|
| STE examples merged with non-STE in dictionary tables | Clear `**STE:**` / `**Non-STE:**` line separation |
| 4-column PDF interleaving in dictionary entries | Reconstructed into clean 2-column layout |
| `###` used for proper names ("ASD-STE100") | `**bold**` for names, `###` only for real headings |
| Page headers ("ASD-STE100 Simplified Technical English") repeated | Collapsed to once per section |
| Rule examples in inconsistent format | Standardized: `> **STE:**` and `> **Non-STE:**` blockquotes |
| Page footers ("Issue 9", "2025-01-15") | Moved to a single page metadata line |
| Missing or inconsistent code blocks | All code examples in ``` fenced blocks |
| Tables without headers | Headers added where detectable |
| Lists with inconsistent indentation | Standardized to 2-space indent |

## Refinement Rules (NON-NEGOTIABLE)

### Rule 1: ZERO CONTENT LOSS
Every word, every number, every example, every table cell from the original
extraction MUST appear in the refined output. Format only — never delete.

### Rule 2: STANDARDIZED HEADINGS
```
# Page N of M          ← Every file starts with this
## Section Title        ← Major sections (Section 1, Part 2, etc.)
### Rule X.Y            ← Rule headings
#### WORD (POS)         ← Dictionary entries
**STE:**                ← STE examples (bold label, not a heading)
**Non-STE:**            ← Non-STE examples (bold label, not a heading)
```

### Rule 3: TABLE FORMATTING
All tables MUST use clean markdown:
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```
- Align columns consistently
- Escape pipe characters inside cells: `\|`
- Merge split cells where the PDF layout broke them

### Rule 4: STE/NON-STE EXAMPLE FORMAT
All example pairs MUST use this exact format:
```markdown
> **STE:** [The STE-compliant example text]

> **Non-STE:** [The non-compliant example text]
```
Never merge STE and non-STE into the same line or paragraph.

### Rule 5: CODE BLOCKS
Any code-like content (pipeline steps, shell commands, Python snippets) in
``` fenced code blocks with language identifier.

### Rule 6: DICTIONARY ENTRY FORMAT
Each dictionary entry MUST be:
```markdown
#### WORD (POS) — APPROVED
- **Meaning:** [exact approved meaning]
- **Forms:** [form1, form2, form3]
- **STE:** [example]
- **Non-STE:** [example]

#### word (POS) — UNAPPROVED
- **Alternatives:** [alternative1 (POS), alternative2 (POS)]
- **STE:** [example using alternative]
- **Non-STE:** [example using unapproved word]
```

### Rule 7: PAGE METADATA
Remove repetitive page headers ("ASD-STE100 Simplified Technical English" on
every page). Replace with a single metadata block at file start:
7. METADATA: Add page header FIRST, then metadata block below it:
   # Page NNN of 434
   
   > **Source:** ASD-STE100 Issue 9, January 2025
   > **Pages:** NN–MM of 434
   
   Remove repetitive "ASD-STE100 Simplified Technical English" headers from body text.
```

### Rule 8: LIST STANDARDIZATION
- Numbered steps: `1. `, `2. ` (not `1)` or `1-`)
- Bullet lists: `- ` (not `* ` or `• `)
- Nested lists: 2-space indent
- Multi-paragraph list items: 2-space indent on continuation lines

### Rule 9: CONSISTENT SPACING — HEADINGS, PARAGRAPHS, TABLES

**CRITICAL: Never glue headings to text. Always separate with blank lines.**

```
❌ WRONG:
### Rule 1.1
Rule text starts immediately...

❌ WRONG:
| Header |
|--------|
| Cell |

✅ CORRECT:
### Rule 1.1

Rule text on its own line, separated by a blank line from the heading above.

| Header |
|--------|
| Cell |

Next paragraph separated by a blank line from the table above.
```

**Spacing rules (non-negotiable):**
- `### Heading` → blank line → content (paragraph, table, list, or blockquote)
- Content end → blank line → next `### Heading`
- Table end → blank line → next paragraph or heading
- List end → blank line → next paragraph or heading
- Blockquote end → blank line → next content
- Exactly one blank line between sections (never two, never zero)
- No trailing whitespace on any line
- No triple blank lines anywhere

## Worker Setup

### Worker Count
Same as extraction: 109 workers, each processing the refinement of 4 pages.
Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`

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

Launch workers using ONLY `deepseek-v4-pro` (the most reasoning-capable model — NEVER flash):

```bash
# Single command to launch the entire refinement swarm:
# (requires the coordinator to generate 109 prompts and launch in 37 batches)
hermes -z "$(cat .agents/prompts/refine/r001-prompt.txt)" -m deepseek-v4-pro --yolo &
hermes -z "$(cat .agents/prompts/refine/r002-prompt.txt)" -m deepseek-v4-pro --yolo &
hermes -z "$(cat .agents/prompts/refine/r003-prompt.txt)" -m deepseek-v4-pro --yolo &
```

## Verification

After each batch, verify:
1. Output file line count >= input file line count (formatting may add lines, never remove)
2. All page numbers from input appear in output
3. No "ASD-STE100 Simplified Technical English" repeated as headings
4. All STE/non-STE pairs use the `> **STE:**` format
5. All tables have header rows and separator rows

## 🔴 MANDATORY: Progress Tracking

**After EVERY batch, update `ste-code/REFINE-PROGRESS.md` before launching the next batch.**
This is NOT optional. The execution auditor cross-references REFINE-PROGRESS.md against disk
evidence. A stale REFINE-PROGRESS.md is treated as a 🔴 CRITICAL tracking discrepancy.

To update:
1. Flip the batch's status to `✅` in REFINE-PROGRESS.md
2. Update the progress counter line at the bottom
3. Verify: `grep "✅" ste-code/REFINE-PROGRESS.md | wc -l` should reflect completed batches

```markdown
# Example: after completing Batch 4, change:
| 4 | r010(37-40), r011(41-44), r012(45-48) | 37-48 | ✅ |

# And update:
**Progress: 12/109 workers (11%) — 48/434 pages**
```

**Progress: 109/109 workers complete (ALL 37 batches, pages 1-434) ✨ REFINEMENT COMPLETE**

## Output Structure

```
ste-code/
├── extracted/          ← Raw extraction (input)
│   └── wNNN-pPPPP-PPPP.md
├── refined/            ← Refined output (this phase)
│   └── rNNN-pPPPP-PPPP.md
├── prompts-refine/     ← Worker prompts for refinement
│   └── rNNN-prompt.txt
└── refined-master.md   ← Concatenated refined master
```

## Single-Prompt Launch

To launch the entire refinement in a new session, paste this:

```
You are the STE-Code refinement orchestrator. Read this skill file:
.agents/skills/spec-extraction/ste-code-refine/SKILL.md

Your job: launch a worker swarm that reformats all files in ste-code/extracted/
into clean, standardized markdown in ste-code/refined/.

Steps:
1. Generate 109 worker prompts using the template in this skill
2. Save prompts to .agents/prompts/refine/
3. Launch workers in 37 batches of 3
4. Verify each batch using the checks in this skill
5. After all 109 complete, produce ste-code/refined-master.md

Rules: Zero content loss. Format only. 4 pages per worker. Batches of 3.
Start now: create ste-code/refined/ and .agents/prompts/refine/ directories,
then generate and launch batch 1 (r001, r002, r003).
```
