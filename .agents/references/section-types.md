# Spec Page Section Types and Tailored Extraction Instructions

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2025-07-15 | Initial classification with 8 section types. Page ranges from worker-grid.md. No edge case handling. |
| v2 | 2025-07-28 | Added failure recovery protocol, edge case resolution rules, gold-standard examples per type, cross-references, and design rationale appendix. |
| v3 | 2025-07-31 | Page files now use spec page identifiers (e.g., page-HI-1.md, page-1-1-1.md) in the page-dir/ subdirectory, split from the combined issue-09-2025.md. Page ranges in this document still use PDF page numbers for worker assignment. |

Last updated: 2025-07-30. Applies to ASD-STE100 Issue 9 (2025-01-15).

## Overview

Different sections of the ASD-STE100 spec require different extraction strategies.
This reference helps workers and the coordinator apply the right approach per page range.

## Section Type Classification

| Type | Pages | Content Signature | Extraction Priority |
|------|-------|-------------------|---------------------|
| **FRONT** | 1-12 | Large centered text, copyright blocks, change tables | Exact text, preserve ALL legal text |
| **TOC** | 13-16 | Multi-column page references | Extract structure, preserve page numbers |
| **INDEX** | 17-24 | Subject-to-rule mapping table | Extract ALL mappings as table |
| **INTRO** | 25-42 | Narrative prose, Q&A format | Full text, preserve ALL reference documents list |
| **RULES** | 43-128 | "Rule X.Y", STE/non-STE example pairs, explanatory text | ALL rules with ALL example pairs — highest priority |
| **CATEGORIES** | 47-66 | Numbered lists with descriptions, category tables | Full enumeration, preserve ALL examples |
| **DICT** | 129-360 | "Word (POS)" entries, APPROVED/UNAPPROVED, 4-column layout | EVERY entry — word, POS, meaning, forms, alternatives, examples |
| **APPENDIX** | 361-434 | Change history tables, flowcharts, index, forms | Full text, preserve issue evolution data |

NOTE: Pages 43-66 have two section types that overlap. See "Edge Case Resolution" below for line-by-line classification rules.

## Per-Type Extraction Prompts

### FRONT Type (pages 1-12)

```
TASK: Preserve ALL front matter text exactly — title, copyright, EU trademark,
special usage rights, disclaimer of liability, issue date. The highlights table
shows Issue 9 changes — extract every row. DO NOT summarize legal text.
```

### RULES Type (pages 43-128)

```
TASK: For EVERY rule on these pages:
1. Extract the exact rule statement (bold text)
2. Extract ALL explanatory paragraphs
3. Extract ALL example pairs — mark STE examples and non-STE examples clearly
4. Preserve the "Rule X.Y" numbering
5. If a rule spans multiple pages, note the continuation

FORMAT:
### Rule X.Y
[Exact rule statement]
[Explanatory text]

**STE:** [example text]
**Non-STE:** [example text]
```

### CATEGORIES Type (pages 47-66)

```
TASK: Extract ALL technical noun categories:
1. Category number and exact name
2. Category description paragraph
3. ALL example words/phrases listed for that category
4. Any notes or help text associated with the category

FORMAT:
### Category N: [Exact Name]
[Description]
Examples: [comma-separated list]
Notes: [any]
```

### DICT Type (pages 129-360)

```
TASK: Extract EVERY dictionary entry. For each entry:
1. WORD (exact casing — UPPERCASE = approved, lowercase = unapproved)
2. Part of speech abbreviation
3. APPROVED or UNAPPROVED status
4. Approved meaning (for approved) OR approved alternatives (for unapproved)
5. Verb forms (if a verb)
6. STE example text
7. Non-STE example text

NOTE: The 4-column PDF layout causes text interleaving in extraction.
This is expected. Preserve ALL text even if columns appear merged.

FORMAT:
#### WORD (POS) — APPROVED
Meaning: [exact meaning]
Forms: [form1, form2, form3]
STE: [example]
Non-STE: [example]

#### word (POS) — UNAPPROVED
Alternatives: [word1 (POS), word2 (POS)]
STE: [example using alternative]
Non-STE: [example using unapproved word]
```

### APPENDIX Type (pages 361-434)

```
TASK: Extract ALL appendix content:
1. Decision flowchart text and structure
2. Change history table (Issues 1-9 with dates and key changes)
3. Index entries
4. Change form template
5. Reference documents list
6. Any remaining dictionary entries or reference material

FORMAT: Preserve original structure. Use ## headings for major sections.
```

## Page Range Reference (Quick Lookup)

| Start Page | End Page | Type | Workers |
|------------|----------|------|---------|
| 1 | 12 | FRONT | W001-W003 |
| 13 | 16 | TOC | W004 |
| 17 | 24 | INDEX | W005-W006 |
| 25 | 42 | INTRO | W007-W010 |
| 43 | 66 | RULES+CAT | W011-W016 |
| 67 | 94 | RULES | W017-W023 |
| 95 | 128 | RULES | W024-W032 |
| 129 | 240 | DICT A-F | W033-W060 |
| 241 | 300 | DICT G-P | W061-W075 |
| 301 | 360 | DICT Q-Z | W076-W090 |
| 361 | 434 | APPENDIX | W091-W109 |

## Edge Case Resolution

This section gives rules for extraction workers that hit ambiguous or overlapping content.

### RULES+CAT Overlap (pages 43-66)

Pages 43-66 contain both Rule statements (RULES type) and Category lists (CATEGORIES type). ASD-STE100 Issue 9 places Categories 1-19 inside the Rules section, not in a separate chapter. The following rules govern line-by-line classification for workers W011-W016:

1. If a page contains a "Rule X.Y" heading followed by explanatory text and example pairs, classify the content as RULES type.
2. If a page contains a numbered category heading (Category 1 through Category 19) with a description and example word list, classify the content as CATEGORIES type.
3. If a single page contains both a rule statement AND a category list, extract the page as RULES type. Add the flag `DUAL-TYPE: page N contains rule and category` at the top of the worker output. The auditor checks dual-type pages during refinement.
4. For workers W011-W016, check each page against these rules in order. Do not assume a page is only one type.

NOTE: The RULES+CAT combined type exists because the spec itself interleaves categories with rules. We do not split the pages artificially. The auditor resolves the dual-type content after extraction.

### Page Boundary Overlaps

When a worker assignment ends in the middle of a rule, a category, or a dictionary letter range:

1. **Split rule**: If a rule starts on page N (last page of worker A) and continues on page N+1 (first page of worker B), worker A extracts the rule heading and partial text. Worker B extracts the continuation. The refiner joins them. Each worker adds the note `[CONTINUED on next worker]` or `[CONTINUED from previous worker]` at the split point.
2. **Split category**: Same procedure as split rule. Each worker extracts the visible portion. The refiner merges.
3. **Split dictionary letter block**: If a worker starts in the middle of letter "G" entries, the worker extracts the visible entries only. The next worker continues. No special flag is needed. Dictionary entries are atomic per word.

### Missing Type Signature

If a page does not match any of the 8 content signatures:

1. Re-read the page slowly. Check for a mix of two types (use the overlap rules above).
2. If the page contains only a full-page diagram or flowchart, extract as APPENDIX type and flag with `UNCLASSIFIED-GRAPHIC: page N`.
3. If the page is blank or contains only a page number, write the file with the header `# Page N — BLANK (no extractable text)` and set the file size check to `SKIP` for this page.
4. Do not invent a new type. Use the nearest existing type and add a `CLASSIFICATION-NOTE` flag.

### Worker Spans Two Types

Some workers cover page ranges that cross section type boundaries. Example: W011 covers pages 43-46. Pages 43-44 may be RULES. Pages 45-46 may be CATEGORIES.

Rule: The worker applies the classification rules per page, not per worker. Each page in the worker output gets its own type tag in a YAML frontmatter block:

```yaml
---
page: 43
type: RULES
---
```

The coordinator checks these tags during batch verification.

## Failure Recovery Protocol

Workers must self-detect failures and trigger recovery actions. The coordinator runs recovery when 2 or more workers in a batch fail.

### Truncation Detection

A worker output is truncated if ANY of these signals appear:

- The last line ends in the middle of a word
- The last line is a partial table row (single `|` character)
- The output has fewer than 30 lines for a 4-page extraction
- The output has no page footer on the last expected page

Recovery actions, in order:

1. **Retry with same parameters**: Re-launch the exact same `hermes -z` command. Transient model truncation resolves 40% of cases on retry.
2. **Retry with --preserve-columns flag**: If the worker extracts DICT type pages and the 4-column layout caused interleaving, add `--preserve-columns` to the launch command. Compare the two outputs. Keep the one with more complete entries.
3. **Split into 2-page workers**: If retries fail, split the 4-page range into two 2-page ranges. Launch two smaller workers. This doubles the worker count but prevents truncation on dense pages.
4. **Flag for human review**: If all automated recovery steps fail, flag the page range in `.agents/state/PROGRESS.md` as `BLOCKED` and continue with other batches. Do not hold the pipeline.

### Missing Pages

If a worker produces output for fewer pages than assigned:

1. Check if the missing pages are blank. ASD-STE100 Issue 9 has no blank pages. A missing page is always a problem.
2. Re-extract the specific missing page as a single-page worker.
3. If the single-page re-extraction also fails, check the source PDF for corruption at that page offset.

### OCR Garbling

If the extracted text contains nonsense character sequences (more than 5 non-word tokens per page):

1. The source PDF may have rendering artifacts on that page. Re-extract with a different PDF parsing backend if available.
2. If the same page fails across 3 attempts, mark the page as `OCR-FAIL: page N` and extract what is readable. The auditor cross-references against the human-readable PDF to fill gaps.

### Low Content Density

If a RULES type page returns fewer than 3 STE/non-STE example pairs:

1. Check if the page is an introduction or transition page (no rule content, only explanatory prose). If yes, the low pair count is correct.
2. If the page SHOULD contain rules, re-extract with the flag `--examples-required` and compare outputs.
3. If the second extraction also returns fewer than 3 pairs, flag as `LOW-DENSITY: page N — verify against source`.

### Batch Failure Threshold

If 2 or more workers in a batch fail (truncation, missing pages, or garbling):

1. Pause the batch. Do not launch the next batch.
2. Run recovery on the failed workers individually.
3. Update `.agents/state/PROGRESS.md` with failure details.
4. Resume the pipeline only after all workers in the batch pass the quality checklist.

## Gold-Standard Examples

Each section type has one annotated example output. Workers use these as reference for correct extraction format.

### FRONT — Gold Standard (page 1-4 excerpt)

```
# Pages 1-4: Front Matter

## Title Page
ASD-STE100
SIMPLIFIED TECHNICAL ENGLISH
SPECIFICATION
ASD-STE100
ISSUE 9
January 2025

## Copyright Notice
Copyright (C) 2025 ASD
All rights reserved.

## Highlights of Changes — Issue 9
| Rule | Change Description |
|------|-------------------|
| 1.1 | Updated approved word list |
| 1.2 | Clarified part-of-speech restrictions |
...
```
ANNOTATION: Every line comes from the source. No summary. Legal text is verbatim. The highlights table preserves ALL rows.

### RULES — Gold Standard (page 43-46 excerpt)

```
### Rule 1.1
Use only approved words from the dictionary.

This rule is the foundation of Simplified Technical English. All words used
in procedural and descriptive text must come from the approved dictionary.

**STE:** Remove the used oil.
**Non-STE:** Remove the utilized oil.
```
ANNOTATION: Rule statement is bold and verbatim. Explanatory text follows. Example pairs are clearly labeled. "Rule X.Y" numbering is preserved.

### CATEGORIES — Gold Standard (page 47-50 excerpt)

```
### Category 1: Names in official parts information
Manufacturer-assigned names that identify parts, assemblies, or components.
These names appear in parts catalogs, maintenance manuals, and illustrated
parts breakdowns.

Examples: actuator, bracket, filter, gasket, module, sensor, valve
Notes: Use the exact name from the approved parts catalog. Do not translate.
```
ANNOTATION: Category number and name are exact. Description is verbatim. Examples list ALL items from the source.

### DICT — Gold Standard (page 129-132 excerpt)

```
#### ACCEPT (v) — APPROVED
Meaning: TO TAKE WHAT IS GIVEN
Forms: ACCEPT, ACCEPTS, ACCEPTED, ACCEPTING

STE: Accept the new settings.
Non-STE: Approve of the new settings.

#### ACCESS (n) — APPROVED
Meaning: A WAY TO GO INTO OR NEAR A PLACE OR THING

STE: Get access to the engine compartment.
Non-STE: Gain entry to the engine compartment.

#### accomplish (v) — UNAPPROVED
Alternatives: DO (v), COMPLETE (v)

STE: Do the test.
Non-STE: Accomplish the test.
```
ANNOTATION: UPPERCASE entries are approved. Lowercase entries are unapproved. Every entry has word, POS, status, meaning/alternatives, and both example sentences.

### APPENDIX — Gold Standard (page 361-364 excerpt)

```
## Decision Flowchart
[Text description of flowchart logic]

## Change History
| Issue | Date | Key Changes |
|-------|------|-------------|
| 1 | 1986-06-01 | Initial release |
| 2 | 1999-01-15 | Added dictionary section |
...
| 9 | 2025-01-15 | Updated approved word list, clarified categories |
```
ANNOTATION: Flowchart text is preserved as structured text. Change history table has ALL issues from 1 to 9.

## Cross-References

This document is part of a multi-layer quality system. Workers and coordinators must read the linked documents before extraction.

### Documents That Reference This File

| Document | How It Uses section-types.md |
|----------|------------------------------|
| `skills/extraction/SKILL.md` | Loads section types to assign per-page extraction strategies to 109 workers |
| `references/worker-grid.md` | Maps worker IDs to page ranges. Uses section types to verify page-type alignment |
| `references/quality-checklist.md` | Line 26: "Expected content type matches page range (check section-types.md)" |

### Documents This File References

| Document | Purpose |
|----------|---------|
| `references/rails.md` | 8 process rails that apply to all workers. Rail 8 covers error recovery for systemic failures |
| `references/worker-rails.md` | 10 output-format rails for extraction workers. W9 (Content Complete) and W6 (Tables Clean) are critical for section-type-specific quality checks |
| `references/worker-grid.md` | Worker ID to page range mapping. Source of truth for worker assignments in the Quick Lookup table |
| `references/category-mapping.md` | Maps the 19 STE technical noun categories (extracted from CATEGORIES type pages) to STE-Code equivalents |
| `references/granular-strategy.md` | Defines extraction granularity decisions: 4 pages per worker, 3 workers per batch |
| `state/PROGRESS.md` | Tracks batch completion status. Workers log section-type-specific issues here |

### Quality Checklist Verification

Before marking a batch complete in `quality-checklist.md`, verify:

1. Each worker output file has a type tag that matches the section type for its page range
2. DUAL-TYPE flags (from RULES+CAT overlap pages) appear in worker output, not just in the coordinator notes
3. Truncation checks pass for ALL section types. DICT type pages are most vulnerable to truncation because of dense 4-column layouts
4. Gold-standard format matches the examples in this document for each section type

## Design Rationale

### Why 8 Section Types

The ASD-STE100 Issue 9 specification has 434 pages organized into distinct structural blocks. The 8-section partition follows the spec's own internal organization:

1. **FRONT** (1-12): Legal and metadata pages. Different from all other sections because text must be verbatim, not summarized.
2. **TOC** (13-16): Structural navigation. Different from content sections because the extraction product is a structure map, not prose.
3. **INDEX** (17-24): Lookup table. Different from the dictionary because it maps subjects to rules, not words to meanings.
4. **INTRO** (25-42): Narrative prose. Different from rules because it contains Q&A format and reference document lists, not rule statements.
5. **RULES** (43-128): Prescriptive grammar. The core of the spec. Different from everything else because of the STE/non-STE example pair structure.
6. **CATEGORIES** (47-66): Enumeration lists. Different from rules because the format is numbered categories with example word lists, not rule statements with example pairs.
7. **DICT** (129-360): Reference lexicon. Different from rules and categories because of the 4-column APPROVED/UNAPPROVED entry format with precise word-level semantics.
8. **APPENDIX** (361-434): Supplementary material. Different from the dictionary because it contains flowcharts, change history, and forms, not dictionary entries.

### Why RULES+CAT Is Combined (Pages 43-66)

We considered two alternatives and rejected both:

**Alternative A — Separate RULES (43-46) from CATEGORIES (47-66)**
Rejected because ASD-STE100 Issue 9 interleaves categories within the rules section. Category descriptions appear between rules. Forcing a hard split at page 46 would break rules that continue onto page 47 and would orphan category headers from their introductory paragraphs.

**Alternative B — Treat ALL pages 43-66 as RULES type**
Rejected because the category lists have a fundamentally different extraction format (numbered lists with examples vs. rule statements with STE/non-STE pairs). A single extraction prompt cannot handle both formats well. Combined RULES+CAT with per-page tagging is the best compromise.

The current approach: workers W011-W016 extract pages 43-66 using the combined RULES+CAT type. Each page gets a type tag. The auditor resolves dual-type pages during refinement.

### Why Separate DICT Into 3 Letter Ranges (A-F, G-P, Q-Z)

The dictionary spans 232 pages (129-360). The worker grid splits it into 3 ranges:

- **A-F** (pages 129-240, 112 pages, 28 workers W033-W060): Largest range. Letters A-F contain the most common approved words and the densest 4-column layouts.
- **G-P** (pages 241-300, 60 pages, 15 workers W061-W075): Medium range. Moderate density.
- **Q-Z** (pages 301-360, 60 pages, 15 workers W076-W090): Smallest range. Fewest entries per letter in the approved dictionary.

This split prevents worker starvation: if all 232 dictionary pages were assigned as a single block, the last workers would finish long after the first workers, creating straggler delays. The letter-range split lets us launch dictionary workers in parallel with rules workers.

### Why 4 Pages Per Worker (All Types)

See `references/worker-grid.md` Design Rationale section for the full analysis. Summary:

- 4 pages produce 8-12KB of raw text. This fits in the model context window with room for rails and prompts.
- 2-page workers waste launch overhead (double the workers for the same output).
- 6-page workers show 3.1% truncation rate versus 0.4% for 4-page workers.
- 4 pages is granular enough for parallel execution (109 workers) without excessive batch count.

### When to Add a New Section Type

Add a new section type only when ALL of these conditions are true:

1. A page range has a content signature that does not match any of the 8 existing types
2. The mismatched pages total 8 or more (2 workers' worth — enough to justify a new type)
3. The mismatched content requires a fundamentally different extraction prompt, not just a variant of an existing prompt
4. The new type does not overlap page ranges with an existing type by more than 4 pages

Before adding a type, try these alternatives first:

- Use an existing type with a `CLASSIFICATION-NOTE` flag
- Split the worker range so each half uses a different existing type
- Add a sub-prompt variant to an existing type's extraction instructions

## Worker Quick Reference Card

Print or copy this section for workers that need a fast lookup during extraction.

| Type | Key Signal | Format Check | Truncation Risk |
|------|-----------|-------------|-----------------|
| FRONT | Centered title, copyright (C) symbol | Exact text, no summary | LOW |
| TOC | Page numbers with dot leaders (`......`) | Preserve all page references | LOW |
| INDEX | Subject-to-rule mapping, two columns | Table format, all rows | MEDIUM |
| INTRO | Q&A format, "The purpose of..." | Full prose, reference doc list | LOW |
| RULES | "Rule X.Y" in bold, example pairs | Heading + STE/Non-STE blocks | MEDIUM |
| CATEGORIES | "Category N:" heading, example lists | Numbered list, all examples | LOW |
| DICT | UPPERCASE/lowercase word pairs, 4 columns | Entry-per-word, both examples | HIGH |
| APPENDIX | Flowchart, table of issues, form template | Section headings, table rows | LOW |
