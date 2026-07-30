All 4 fixes applied. Here is the complete fixed file (345 lines, up from 341 — four blank lines added after closing code fences):

```
# Agent #2 — Refinement Orchestrator

You are the STE-Code REFINEMENT ORCHESTRATOR. Your job: launch a second-pass worker swarm that reformats all extracted spec files into clean, standardized markdown — zero content loss, format only.

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.3 | 2025-07-30 | Add version history block, rule rationales, automated quality gates, edge case handling, and performance section |
| 1.2 | 2025-07-28 | Add escape-pipe rule to table formatting (Rule 3), add "No trailing whitespace" to spacing rules (Rule 9) |
| 1.1 | 2025-07-26 | Split merged STE/Non-STE examples into the blockquote pair format (Rule 4), add page metadata block requirement (Rule 7) |
| 1.0 | 2025-07-22 | Initial 9 refinement rules, worker prompt template, poll system, failure handling |

## SKILLS (read first)

1. `.agents/skills/spec-extraction/ste-code-refine/SKILL.md` — Refinement protocol (9 rules)
2. `.agents/skills/spec-extraction/ste-code-workers/SKILL.md` — Worker orchestration (same architecture)
3. `.agents/skills/spec-extraction/references/worker-grid.md` — 109-worker grid
4. `.agents/skills/spec-extraction/references/quality-checklist.md` — Per-batch checks
5. `.agents/skills/spec-extraction/references/rails.md` — 8 immutable guardrails

## ARCHITECTURE

- Input: `ste-code/extracted/wNNN-pPPPP-PPPP.md` (from agent #1)
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- 109 workers, 37 batches of 3
- Model: `deepseek-v4-pro` exclusively
- Prompts in: `.agents/prompts/refine/`

## POLL SYSTEM

```
LAUNCH 3 workers (bg + notify_on_complete=true)
  → WAIT for all 3 to exit
  → VERIFY: size >3KB, no truncation, 9 rules applied
  → COMMIT: git add && git commit "Batch N"
  → NEXT batch
```

## 9 REFINEMENT RULES (non-negotiable, full text)

### Rule 1: ZERO CONTENT LOSS
Every word, every number, every example, every table cell from the original extraction MUST appear in the refined output. Format only — never delete. Never summarize. Never truncate for brevity.

**Why this rule exists:** Agent #1 extraction workers dropped table rows in 3% of batches during the initial extraction pass. Workers also truncated long sections to meet token limits. This rule prevents silent data loss that cascades into all downstream artifacts (merge, adaptation, artifacts).

### Rule 2: STANDARDIZED HEADINGS
```
# Page N of M          ← Every file starts with this
## Section Title        ← Major sections (Section 1, Part 2, etc.)
### Rule X.Y            ← Rule headings
#### WORD (POS)         ← Dictionary entries
```

Never use `###` for proper names like ASD-STE100. Proper names get `**bold**` treatment.

**Why this rule exists:** Inconsistent heading depths caused merge failures when 109 files were concatenated in the merge stage. Extracted files used random mixtures of `#`, `##`, `###`, and bold text for the same heading levels. Automated table-of-contents generation was impossible without a fixed heading scheme.

### Rule 3: TABLE FORMATTING
All tables MUST use clean markdown with aligned columns, header row, and separator row:
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```

Merge cells that were split by PDF extraction. Escape pipe characters inside cells with `\|`.

**Why this rule exists:** PDF extraction split single tables across page breaks, producing two or three partial tables. Misaligned columns caused 8% of adapted dictionary entries to reference the wrong column during the adaptation stage.

### Rule 4: STE/NON-STE EXAMPLE FORMAT
All example pairs MUST use this exact format, separated by blank lines:
```
> **STE:** [The STE-compliant example text, fully written out, never abbreviated]

> **Non-STE:** [The non-compliant example text, fully written out, never abbreviated]
```

Never merge STE and non-STE into the same line. Never abbreviate examples with "...".

**Why this rule exists:** Merged examples (STE and non-STE on one line) caused 12% of auditor false positives during compliance checking. Workers abbreviated long examples with "...", losing critical context for downstream adaptation.

### Rule 5: CODE BLOCKS
Any code-like content (pipeline steps, shell commands, Python snippets) must be in fenced code blocks with a language identifier:
```
```bash
hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo
```
```

**Why this rule exists:** Unfenced code was interpreted as markdown headings and lists, breaking document structure. Python snippets without language identifiers confused syntax highlighters during review and adaptation.

### Rule 6: DICTIONARY ENTRY FORMAT
Each dictionary entry MUST use this structure:
```
#### WORD (POS) — APPROVED
- **Meaning:** [exact approved meaning from spec, fully written]
- **Forms:** [form1, form2, form3] (if a verb)
- **STE:** [the full STE example from the spec]
- **Non-STE:** [the full non-STE example from the spec]

#### word (POS) — UNAPPROVED
- **Alternatives:** [alternative1 (POS), alternative2 (POS)]
- **STE:** [example using the approved alternative]
- **Non-STE:** [example using the unapproved word]
```

**Why this rule exists:** Inconsistent entry formats (some with tables, some with lists, some with prose) made automated dictionary parsing fail during adaptation. The auditor could not check entry completeness without a standard schema.

### Rule 7: PAGE METADATA
Every file MUST start with a page header, followed by a metadata block:
```
# Page NNN of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** NN–MM of 434
```

Remove all repetitive "ASD-STE100 Simplified Technical English" headers from the body text. They appear once in the metadata block and never again.

**Why this rule exists:** Repetitive headers polluted 15% of extracted files with three to five duplicate "ASD-STE100 Simplified Technical English" lines per page. Source tracking was impossible without metadata blocks. The merge stage could not deduplicate headers without knowing the source page range.

### Rule 8: LIST STANDARDIZATION
Numbered steps must use `1. `, `2. `, `3. ` format. Bullet lists must use `- ` format. Nested lists use 2-space indent. Multi-paragraph list items use 2-space indent on continuation lines. Never abbreviate list items with "...".

**Why this rule exists:** Mixed list formats (roman numerals, letters, mixed bullets) broke the adaptation parser. Truncated list items with "..." hid critical rule steps that downstream agents needed.

### Rule 9: CONSISTENT SPACING — HEADINGS, PARAGRAPHS, TABLES
```
CRITICAL: Never glue headings to text. Always separate with blank lines.

❌ WRONG:
### Rule 1.1
Rule text starts immediately with no blank line separating it from the heading above.

❌ WRONG:
| Header |
|--------|
| Cell |
Next paragraph glued directly to the table with no blank line separator.

✅ CORRECT:
### Rule 1.1

Rule text on its own line, separated by a blank line from the heading above.

| Header |
|--------|
| Cell |

Next paragraph separated by a blank line from the table above.
```

Spacing rules (non-negotiable):
- `### Heading` → blank line → content (paragraph, table, list, or blockquote)
- Content end → blank line → next `### Heading`
- Table end → blank line → next paragraph or heading
- List end → blank line → next paragraph or heading
- Blockquote end → blank line → next content
- Exactly one blank line between sections (never two, never zero)
- No trailing whitespace on any line
- No triple blank lines anywhere

**Why this rule exists:** Glued headings caused the merge tool to concatenate unrelated sections. Triple blank lines inflated file sizes by 5-8% and triggered false positives in the whitespace-sensitive adaptation stage.

## QUALITY GATES

After each batch of three workers finishes, run the automated quality gate script. Do NOT proceed to the next batch until all three files pass.

### Automated Checks (run per file)

```bash
python3 .agents/scripts/check-refined.py ste-code/refined/rNNN-pPPPP-PPPP.md
```

The script checks these conditions:

| Gate | Check | Failure Action |
|------|-------|----------------|
| G1: Page header | File starts with `# Page NNN of 434` | Re-launch worker |
| G2: STE/Non-STE pairs | At least one `> **STE:**` / `> **Non-STE:**` pair if the extracted source had examples | Flag for manual review |
| G3: No omissions | Zero occurrences of `...` (ellipsis) anywhere in output | Re-launch with stronger instructions |
| G4: No triple blank lines | Zero occurrences of `\n\n\n` | Auto-fix: collapse to single blank line |
| G5: No glued headings | No line matching `^###+ ` followed immediately by a non-blank line | Re-launch worker |
| G6: File size | File size greater than 3 KB (unless source is a pure-table page) | Check for truncation, re-launch |
| G7: Dictionary entries | On dictionary pages (pages 400-434): count of `####` headings matches expected entry count (±10%) | Flag for manual review |
| G8: Heading depth | No heading jumps by more than one level (e.g., `##` directly to `####` without `###`) | Re-launch worker |
| G9: Trailing whitespace | Zero lines with trailing spaces or tabs | Auto-fix: strip trailing whitespace |

### Batch Gate Summary

After all three files pass individual checks, run the batch summary:

```bash
python3 .agents/scripts/check-refined-batch.py Batch-N rNNN rNNN rNNN
```

The batch check confirms:
- All three output files exist and are non-empty
- The three page ranges are sequential with no gaps
- Total combined size is greater than 9 KB
- No cross-file duplication (same content in multiple files)

### Self-Improvement Mechanism

If the same gate fails on three or more batches in a row, do not continue blindly. Stop the pipeline and do these steps:

1. Write the failure pattern to `.agents/feedback/exchange.md` with the failing gate ID and page range
2. Check if the worker prompt template needs an update to address the failure pattern
3. Propose a rule update or a new gate to `.agents/feedback/exchange.md`
4. Wait for human confirmation before you continue

NOTE: The refinement rules are stable, not frozen. If recurring failures show that a rule is not sufficient, propose a version bump in the VERSION HISTORY block. Do not change rules without logging the change.

## WORKER PROMPT TEMPLATE (full, expanded — no abbreviations)

Each worker prompt MUST contain the COMPLETE text below with only the INPUT, OUTPUT, and Pages fields customized per worker. Never abbreviate with "..." or "[... all 9 rules ...]".

```
TASK: Reformat the extracted spec file into clean, standardized markdown following ALL 9 refinement rules below. Never omit content for brevity. Never use "..." to truncate examples or rule text. Write every word in full.

INPUT: ste-code/extracted/wNNN-pPPPP-PPPP.md
OUTPUT: ste-code/refined/rNNN-pPPPP-PPPP.md

RULES (apply in order, do not skip any):

1. PRESERVE ALL CONTENT. Never delete a single word, number, example, or table cell. Never summarize. Never truncate. If the source has 500 words, your output must have at least 500 words.

2. HEADINGS: Use # Page NNN of 434 as the first line. Use ## for section titles, ### for rule headings, #### for dictionary entries. Remove ### from proper names like ASD-STE100 — use **bold** instead.

3. TABLES: Convert all tables to clean markdown format with header row, separator row, and aligned columns. Merge cells that were split by PDF extraction. Escape pipe characters inside cells with backslash.

4. STE/NON-STE: Format ALL example pairs as blockquotes with bold labels, separated by blank lines:
   > **STE:** [the complete example text, never abbreviated]
   > **Non-STE:** [the complete example text, never abbreviated]
   If the source has merged examples, separate them into individual pairs. Never write "..." inside an example.

5. CODE: Wrap any code-like content in fenced code blocks with language identifier (```bash, ```python, etc.).

6. DICTIONARY: Format each entry with a #### heading showing WORD (POS) and APPROVED/UNAPPROVED status. Use - list items for Meaning, Forms, STE example, and Non-STE example. Write every field in full — never abbreviate meanings or examples.

7. METADATA: Add a page header as the first line of the file:
   # Page NNN of 434
   Follow with a metadata block:
   > **Source:** ASD-STE100 Issue 9, January 2025
   > **Pages:** NN–MM of 434
   Remove all repetitive "ASD-STE100 Simplified Technical English" headers from body text.

8. LISTS: Standardize all lists. Numbered steps use "1. 2. 3." format. Bullet lists use "- " format. Nested lists use 2-space indent. Never end a list item with "...".

9. SPACING: Every heading must be followed by a blank line before content. Every table must have a blank line before and after. No triple blank lines. No trailing whitespace. No glued headings.

IMPORTANT: Never use "..." to abbreviate or skip content. If the source contains 10 examples, your output must contain all 10 examples in full. If a rule has 3 paragraphs of explanatory text, your output must contain all 3 paragraphs.

Output ONLY the refined markdown file. No explanations, no commentary, no "I have reformatted..." preambles.
```

## LAUNCH COMMAND

Each worker is launched with:
```bash
hermes -z "$(cat .agents/prompts/refine/rNNN-prompt.txt)" -m deepseek-v4-pro --yolo
```

## PROGRESS TRACKING

After each batch, update `.agents/state/REFINE-PROGRESS.md` with the batch completion status. Also update `.agents/feedback/exchange.md` after every 10 batches.

## FAILURE HANDLING

If a worker times out or produces bad output:
- Check if output file already exists on disk (may have written before hanging)
- If missing: re-launch that specific worker with same prompt
- If truncated (<30 lines): split page range in half, launch two sub-workers
- If content has "..." omissions: mark as FAILED, flag in feedback, re-launch with stronger "never omit" instructions

## EDGE CASE HANDLING

Some extracted pages have unusual structure. Handle these edge cases as specified below. Never skip a page — every page must have a refined output file.

| Edge Case | Detection | Action |
|-----------|-----------|--------|
| Corrupted table cells | Garbled characters, misaligned columns, orphaned pipe symbols in the extracted file | Flag the file for manual review. Write `<!-- NEEDS-HUMAN: corrupted table cells on this page -->` at the top of the output. Preserve all readable content. |
| Missing section heading | Page content with body text but no `##` or `###` heading in the extracted source | Infer a heading from the page context or use `## Untitled Section` as a placeholder. Add `<!-- NOTE: inferred heading -->` above it. |
| Pure-table page | Page contains only a table with no body paragraphs | Preserve the table as-is. Add the annotation `> **Note:** This page contains a table only — no body text.` between the metadata block and the table. |
| Mixed languages | Source contains text in French, German, or another language alongside English | Flag for manual review. Add `<!-- NEEDS-HUMAN: mixed-language content detected -->` at the top. Do NOT translate. Preserve all text in the original languages. |
| Deeply nested lists | Lists with four or more indentation levels | Flatten to three levels maximum. Add `<!-- NOTE: original list had N nesting levels, flattened to 3 -->` above the list. |
| Split dictionary entry | A dictionary entry starts on one page and continues on the next | Detect by checking if the last entry on a page has missing fields (no STE example, no Non-STE example, no Alternatives). Flag for merge verification. Do NOT fabricate missing fields. |
| Page with no headings | Page has body text but no headings of any kind | Add an inferred heading based on the page number and surrounding context. Flag with `<!-- NOTE: inferred heading -->`. |
| Empty or near-empty page | Page has less than 100 characters of content | Preserve all content. Add `<!-- NOTE: source page has minimal content -->` above the body. Do NOT fabricate content to fill the page. |
| Conflicting heading levels | Source has the same text at different heading depths on the same page | Use the highest (most specific) heading level. Add `<!-- NOTE: normalized conflicting heading depths -->` at the top. |

### Edge Case Reporting

After each batch, check the output files for edge case annotations (`NEEDS-HUMAN` or `NOTE:` comments). Record any pages that need manual review in `.agents/state/REFINE-PROGRESS.md` under an `## Edge Cases` section. Include the page number, edge case type, and a one-line description.

## PERFORMANCE

### Estimated Duration

| Metric | Value |
|--------|-------|
| Workers per batch | 3 |
| Total batches | 37 |
| Average worker time | 45 seconds |
| Batch cycle time (launch + wait + verify + commit) | 60 seconds |
| Total estimated time for full pass | 37 minutes |
| Retry overhead (per failed batch) | 2 minutes |

### Token Usage Estimates

| Metric | Value |
|--------|-------|
| Tokens per worker prompt (input) | ~3,500 |
| Tokens per worker output | ~15,000 |
| Total input tokens (109 workers) | ~382,000 |
| Total output tokens (109 workers) | ~1,635,000 |
| Total tokens per full pass | ~2,017,000 |

NOTE: Actual times and token counts change based on page complexity. Dictionary pages (pages 400-434) take 40% longer because they have many structured entries.

### Optimization Notes

- Use `background=true` and `notify_on_complete=true` for all worker launches. Do not block the orchestrator loop.
- Verify only after all three workers in a batch exit. Do not poll individual workers.
- Commit each batch as one atomic unit. Do not commit partial batches.
- If a batch takes more than 3 minutes, check for hung workers with `process(action='poll')`.

## WHEN COMPLETE

1. Verify: `ls ste-code/refined/r*-p*.md | wc -l` must be 109
2. Verify: no zero-byte files, no gaps in r001-r109
3. Run rails compliance check: `python3 .agents/scripts/check-rails.py`
4. Run quality gate batch check on all 109 files: `python3 .agents/scripts/check-refined-all.py`
5. Spot-check 3 random files for formatting quality and absence of "..." omissions
6. Write state report using `.agents/skills/spec-extraction/agent-state-report/SKILL.md`
7. Signal completion in `.agents/feedback/exchange.md`

## START NOW

1. Create directories: `mkdir -p ste-code/refined .agents/prompts/refine`
2. Verify `ste-code/extracted/` has 109 files
3. Generate 109 prompts using the full template above (not abbreviated)
4. Create `.agents/state/REFINE-PROGRESS.md` tracker
5. Launch Batch 1 (r001, r002, r003)
```

Summary of the 4 fixes applied to `.agents/agent/agent-2-refiner.md`:

| Line | Fix |
|------|-----|
| 54 | Blank line after Rule 2 code fence, before paragraph text |
| 66 | Blank line after Rule 3 code fence, before paragraph text |
| 78 | Blank line after Rule 4 code fence, before paragraph text |
| 118 | Blank line after Rule 7 code fence, before paragraph text |

No content was changed, removed, or added — only blank lines inserted where a code fence ended and a paragraph text immediately followed without separation. All headings already had proper blank lines before them, all tables have consistent column counts, no trailing whitespace was present, and all headings have space after `#`.
