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

## Before/After Examples

Each transformation rule has a concrete example. Workers must match these patterns.
Examples 1–8 map directly to the 8 problem rows in the table above.

### Example 1: STE/Non-STE pair merging

**Before (raw extraction):**
```
| STE | Make sure that the valve is open. | Non-STE | Verify that the valve is open. |
```

**After (refined):**
```
> **STE:** Make sure that the valve is open.
> **Non-STE:** Verify that the valve is open.
```

### Example 2: 4-column PDF interleaving

**Before (raw extraction):**
```
| ACCESS (n) | APPROVED | You can get access to the | ACCESS (v) | UNAPPROVED | Do not access the panel. |
```

**After (refined):**
```
#### ACCESS (n) — APPROVED

- You can get access to the

#### ACCESS (v) — UNAPPROVED

- Do not access the panel.
```

### Example 3: Repeated page headers

**Before (raw extraction):**
```
ASD-STE100 Simplified Technical English
Page 15 of 434

## Section 2 — Dictionary

ASD-STE100 Simplified Technical English
Page 16 of 434

### Rule 2.1 — Word usage
```

**After (refined):**
```
# Page 15 of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** 15–16 of 434

## Section 2 — Dictionary

### Rule 2.1 — Word usage
```

### Example 4: Rule examples inconsistent

**Before (raw extraction):**
```
STE: Set the switch to ON.
Non-STE: Move the switch to the ON position.

STE: Make sure that the pin is locked. Non-STE: Verify that the pin is locked.
```

**After (refined):**
```
> **STE:** Set the switch to ON.
> **Non-STE:** Move the switch to the ON position.

> **STE:** Make sure that the pin is locked.
> **Non-STE:** Verify that the pin is locked.
```

### Example 5: Table without headers

**Before (raw extraction):**
```
| approved | You can use this word. |
| unapproved | ACCESS (v) |
```

**After (refined):**
```
| Status | Meaning |
|--------|---------|
| approved | You can use this word. |
| unapproved | ACCESS (v) |
```

### Example 6: Proper names as headings

**Before (raw extraction):**
```
### ASD-STE100

ASD-STE100 is the European standard for Simplified Technical English.
### ASD

The ASD is the Aerospace, Security and Defence Industries Association of Europe.
```

**After (refined):**
```
**ASD-STE100** is the European standard for Simplified Technical English.

**ASD** is the Aerospace, Security and Defence Industries Association of Europe.
```

NOTE: Never use `###`, `##`, or `#` for proper names. Use `**bold**` for inline emphasis of organization names, standard names, and product names. Headings (`#` through `####`) are only for document structure (pages, sections, rules, dictionary entries).

### Example 7: Page footers

**Before (raw extraction):**
```
### Rule 1.5 — Technical names

Technical names are words that refer to a system or a part of a system.

Issue 9
2025-01-15
```

**After (refined):**
```
### Rule 1.5 — Technical names

Technical names are words that refer to a system or a part of a system.

> **Source:** ASD-STE100 Issue 9, January 2025
```

NOTE: Page footers in the source PDF repeat "Issue 9" and a date stamp on most pages. These are PDF printing artifacts, not content. Collapse ALL footer lines into a single metadata line. If the footer date varies across pages within a batch, use the earliest date found and note the range: `January–February 2025`.

### Example 8: List indentation

**Before (raw extraction):**
```
1. First item
    - sub item one
        * sub sub item
2. Second item
   - sub item two
```

**After (refined):**
```
1. First item
   - sub item one
     - sub sub item
2. Second item
   - sub item two
```

NOTE: Use 2-space indent for all list nesting. Replace `*` bullet markers with `-`. Do not mix numbered lists and bullet lists at the same nesting level — choose one style per level.

## 9 Refinement Rules (NON-NEGOTIABLE)

1. **ZERO CONTENT LOSS** — Every word, number, example, table cell preserved. Redundant page headers (repeated "ASD-STE100 Simplified Technical English" text that appears on every page of the source PDF) are NOT content — they are PDF printing artifacts. Removing them is safe. Rule examples, dictionary entries, section text, table data, and rule numbers ARE content — never remove these.
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

### Rule 1 Boundary: Redundant vs. Content

The boundary between "redundant PDF artifact" and "content" must be clear. Use this decision table when unsure:

| Element | Classification | Action | Reason |
|---------|---------------|--------|--------|
| "ASD-STE100 Simplified Technical English" on every page | Redundant artifact | Remove from body, keep in metadata block | PDF header repeated 434 times. Source captured once in metadata. |
| "Page N of 434" on every page | Redundant artifact | Collapse to page range in metadata block | Source captured as `# Page NNN–MMM of 434`. |
| "Issue 9" / "2025-01-15" footer on every page | Redundant artifact | Collapse to single metadata line | PDF footer. Issue and date are constant across the spec. |
| Rule text: "STE: Set the switch to ON." | Content | NEVER remove | Specification content. |
| Dictionary entry: "ACCESS (n) — APPROVED" | Content | NEVER remove | Specification content. |
| Table data: word lists, meanings, examples | Content | NEVER remove | Specification content. |
| Section headings: "Section 2 — Dictionary" | Content | NEVER remove | Document structure. |
| Page number in a cross-reference: "See page 23" | Content | Keep as-is in body text | This is part of the specification text, not a page artifact. It was written by the spec authors. |
| Running header: "ASD-STE100" at the top of every page | Redundant artifact | Remove from body | Same text on 434 pages. Keep once in metadata. |
| Distinct page content: a diagram caption, a unique footnote | Content | NEVER remove | Only appears once in the spec. |

**Decision rule**: If the text repeats identically on 3+ consecutive pages and is not part of the specification body (rules, dictionary, examples), it is a PDF artifact. Remove it. If in doubt, keep it — content loss is worse than extra metadata.

## Rule Rationale and Priority

The 9 rules address the 8 problem patterns from the extraction stage. They are ordered by priority:

| Priority | Rule | Why It Matters |
|----------|------|----------------|
| **Highest** | Rule 1 — Zero Content Loss | Data integrity. If content is lost here, all downstream stages (merge, adapt, artifacts) produce wrong output. |
| **High** | Rule 2 — Standardized Headings | Structural consistency. Without this, the merge stage cannot reassemble pages in order. |
| **High** | Rule 3 — Table Formatting | Dictionary correctness. The dictionary is the largest section (pages 15–434). Bad tables make it unusable. |
| **High** | Rule 4 — STE/Non-STE Format | Rule clarity. Every rule in the spec references example pairs. Wrong format breaks rule understanding. |
| **Medium** | Rule 5 — Code Blocks | Technical fidelity. Some rules reference code or markup. Lost fences break syntax examples. |
| **Medium** | Rule 6 — Dictionary Entries | Dictionary navigation. Consistent entry format enables the merge stage to deduplicate entries. |
| **Medium** | Rule 7 — Page Metadata | Source traceability. Every refined page must link back to its source page range. |
| **Low** | Rule 8 — List Standardization | Readability. Indentation noise from PDF extraction makes lists hard to parse. |
| **Low** | Rule 9 — Consistent Spacing | Clean diff output. Extra blank lines cause noisy diffs in version control. |

### Why 9 Rules, Not 8 or 10

There are exactly 8 problem patterns (see "What You Fix" table above). Rules 1–8 each target one problem pattern. Rule 9 (Consistent Spacing) is a cross-cutting rule that affects all output — it does not map to one problem pattern but improves every file. The count is 8 problem-specific rules + 1 global formatting rule = 9.

### Rules That Interact

Some rules can conflict when applied to the same text. Apply them in this fixed order to prevent conflicts:

**Transformation priority (apply in this exact order):**

1. Rule 1 — Identify what to keep vs. remove (redundant artifact detection)
2. Rule 7 — Build the page metadata block FIRST (sets the file header)
3. Rule 2 — Normalize all headings (page, section, rule, dictionary levels)
4. Rule 3 — Reformat tables (header rows, separator rows, aligned columns)
5. Rule 4 — Convert STE/Non-STE pairs to blockquote format
6. Rule 6 — Format dictionary entries (word headings + bullet lists)
7. Rule 8 — Standardize list indentation
8. Rule 5 — Wrap code blocks in fences
9. Rule 9 — Apply consistent spacing (blank lines, no trailing spaces)

Applying rules in this order prevents a later rule from undoing an earlier rule's work. For example: apply heading normalization (Rule 2) before STE/Non-STE formatting (Rule 4) so that `###` in "### ASD-STE100" is removed before the STE/Non-STE scanner tries to parse it.

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

### Edge Case Handling

Workers must handle these edge cases:

**Empty or near-empty input files:**
If the input file has 0 lines or only whitespace, write a single metadata block with a warning:
```
# Page NNN of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** N–M of 434
> **Warning:** Source page contained no extractable text.

*No content to refine.*
```
Do not create an empty output file. The verification step expects output lines >= input lines. An empty output file fails verification even when the input was also empty.

**Content that matches no problem patterns:**
If the extracted file is already clean (proper headings, tables, STE/non-STE formatting), copy the content to the output file unchanged. Do not force transformations on content that does not need them. The rules are corrective, not destructive.

**Metadata block conflicts:**
If the extracted file already contains a metadata block or a source citation that conflicts with the standard format, use the standard format (Rule 7) and keep the original citation on a separate line below:
```
# Page NNN of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** N–M of 434
> **Original citation:** [text from extracted file]
```

**Ambiguous STE/Non-STE pairs:**
If a line contains both STE and Non-STE text without a clear separator (e.g., merged by PDF extraction), split at the first occurrence of "Non-STE:" or "Not approved:" and format as separate blockquote lines. If no separator exists, keep the text in a single code block with a note:
```
```
[Could not separate STE/Non-STE pair:]
[original text]
```
```

**Page number mismatch:**
If the page numbers in the input filename (`wNNN-pPPPP-PPPP.md`) do not match the page numbers found in the extracted content, trust the FILENAME. The extraction worker may have read the correct pages but the PDF page numbers may differ from the spec's internal numbering (e.g., cover pages, table of contents). Set the page header from the filename and add a note:
```
> **Note:** Page numbers in content differ from filename range. Using filename range.
```

**Corrupted or mixed-encoding characters:**
If the extracted file contains non-UTF-8 characters, replacement characters (`�`), or mixed encodings (common in PDF extraction of special characters like em-dashes, smart quotes, or diacritics):
1. Replace `�` with the most likely ASCII equivalent based on context:
   - `�` before a word → likely an em-dash → use `—`
   - `�` around a word → likely a smart quote → use `"` or `'`
   - `�` in a word → check the STE-Code dictionary for the expected word
2. If the character cannot be resolved, keep `�` and add a warning line:
   ```
   > **Warning:** N unresolved replacement characters in this file.
   ```

**Duplicate dictionary entries across pages:**
If the same dictionary entry (same word + part of speech) appears on two different pages in the same batch, keep the entry on the page where it FIRST appears. On subsequent pages, add a cross-reference note:
```
*See page [N] for full entry.*
```
Do not merge or deduplicate content across pages — that is the merge stage's job.

**Nested transformation conflicts:**
A single block of text can match multiple problem patterns. Example: a dictionary entry table (pattern 2: 4-column interleaving) that also contains merged STE/Non-STE pairs (pattern 1). Apply transformations in order: first split the 4-column interleaving into separate dictionary entries, then format the STE/Non-STE pairs within each entry. The transformation priority order in the "Rules That Interact" section above is authoritative.

### Pre-Flight Checklist (Orchestrator Only)

Before launching a batch of workers, check these items:

- [ ] Input file exists: `ste-code/extracted/wNNN-pPPPP-PPPP.md`
- [ ] Input file is > 0 bytes (`wc -c` confirms non-empty, even if only whitespace)
- [ ] Output directory exists: `ste-code/refined/`
- [ ] Prompt file exists: `.agents/prompts/refine/rNNN-prompt.txt`
- [ ] Prompt file references the correct input and output paths
- [ ] Model is `poolside/laguna-s-2.1:free` (NEVER `deepseek-v4-flash`)
- [ ] No more than 3 workers launched simultaneously
- [ ] Previous batch verification is complete (if not batch 1)

### Launch Protocol

Launch workers using ONLY `poolside/laguna-s-2.1:free` (NEVER `deepseek-v4-flash`):

```bash
hermes -z "$(cat .agents/prompts/refine/r001-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
hermes -z "$(cat .agents/prompts/refine/r002-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
hermes -z "$(cat .agents/prompts/refine/r003-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
```

## Verification (Per Batch)

1. Output file line count >= input file line count
2. All page numbers from input appear in output
3. No "ASD-STE100 Simplified Technical English" repeated as headings
4. All STE/non-STE pairs use `> **STE:**` format
5. All tables have header rows and separator rows

### Post-Refinement Sanity Check

After verification passes, run these additional checks before marking a batch complete:

- [ ] Output file is valid markdown (no broken fences, no unclosed code blocks)
- [ ] Output file does not contain raw PDF artifacts: no "Issue 9" on its own line without metadata context, no orphaned dates
- [ ] No heading level is skipped (e.g., `## Section` directly followed by `#### Entry` without an intervening `### Rule`)
- [ ] The metadata block is the FIRST block after the `# Page NNN of 434` heading (nothing between them)
- [ ] File ends with a trailing newline
- [ ] No line exceeds 200 characters (signals a table row that was not split correctly by the PDF extractor)
- [ ] The word count of the output is within 5% of the input word count (a difference > 5% signals content loss or fabrication)

### Failure Recovery

If any verification check fails, use this recovery procedure:

**Check 1 fails (output line count < input line count):**
1. Compare input and output files. Identify the missing lines.
2. If the missing lines are page headers only (Rule 1), the check is a false positive. Mark the batch as passed with a note.
3. If the missing lines are content (rule text, examples, dictionary entries), re-run the worker with a stronger prompt that starts with: "CRITICAL: The previous run lost content. You MUST preserve every single line of the input file."
4. If the re-run fails again, mark the file in REFINE-PROGRESS.md as `❌ CONTENT LOSS` and escalate to the Auditor agent.

**Check 2 fails (page numbers missing):**
1. Re-run the worker. The prompt already mandates page metadata preservation.
2. If the re-run fails, manually extract the page numbers from the input filename and insert the metadata block.

**Check 3 fails (repeated headers present):**
1. Run a scripted pass to strip all lines matching exactly "ASD-STE100 Simplified Technical English" from the output file.
2. Re-run verification.

**Check 4 fails (wrong STE/non-STE format):**
1. Search the output for "STE:" and "Non-STE:" patterns not in blockquote format.
2. Run a scripted pass to convert these to `> **STE:**` / `> **Non-STE:**` format.
3. Re-run verification.

**Check 5 fails (tables missing headers):**
1. If the table has 2+ columns but no separator row, the worker failed to add headers. Re-run with a prompt that lists the expected table columns explicitly.
2. If the re-run fails, mark the file as `⚠️ TABLE` and note the missing headers in REFINE-PROGRESS.md.

**Sanity check failures (post-verification):**
- **Broken markdown fences**: If the output has an unclosed code fence, add the closing fence at the end of the file and note the fix.
- **Heading level skip**: Add a bridging heading if the content warrants it. If the skip is from an original PDF structure quirk (e.g., a sub-sub-rule under a rule with no intervening section), mark the file as `⚠️ STRUCTURE`.
- **Word count deviation > 5%**: This is a serious signal. Do not mark the batch complete. Run a diff between input and output to identify added or removed content. Re-extract the page range if necessary.
- **Line > 200 characters**: Split the line manually at a logical column boundary. Mark the file as `⚠️ WIDE`.

After recovery, increment the retry counter in REFINE-PROGRESS.md. After 3 retries for the same batch, escalate to the Auditor agent.

### Common Failure Patterns and Their Root Causes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Output is significantly shorter than input | Worker summarized instead of reformatting | Re-run with "CRITICAL: no summarization" prefix |
| Table columns are misaligned after refinement | PDF extraction merged cells from adjacent pages | Split the page range and re-extract with 2 pages per worker |
| STE/Non-STE pairs appear as a single blockquote line | PDF extracted two examples as one line | Re-run with explicit instruction to split at "Non-STE:" marker |
| Dictionary entry has wrong part of speech | PDF page boundary split the entry across pages | Cross-reference with the previous page in the batch |
| Metadata block appears mid-file instead of at top | Worker applied Rule 7 after processing content | Move block to top manually. The transformation order in "Rules That Interact" prevents this in correct execution. |
| Consecutive runs produce different output for the same input | Model non-determinism | Accept the first run that passes all checks. Do not re-run for cosmetic differences. |

## 🔴 MANDATORY: Update REFINE-PROGRESS.md After Every Batch

After each batch, flip the batch's status to `✅` in `.agents/state/REFINE-PROGRESS.md`,
update the progress counter, and commit.

## Immutable Facts

- 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-v4-flash)
- Zero content loss — format only
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- Follow `.agents/skills/spec-extraction/references/rails.md` — all 8 guardrails apply
- Particularly RAIL 4 — Content Fidelity: never fabricate, summarize, or adapt. Reformat only.
- Particularly RAIL 5 — Formatting Standards: heading levels, spacing, tables, STE/Non-STE examples, dictionary entries must match the approved patterns.

## Start Now

1. Verify 109 extracted files exist
2. Generate 109 prompts, save to `.agents/prompts/refine/`
3. Launch Batch 1 (r001, r002, r003)
4. Verify, update REFINE-PROGRESS.md, commit
5. Continue through all 37 batches
