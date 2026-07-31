# Worker Prompts — ASD-STE100 Issue 9 Extraction

> **VERSION**: v2.0.0 (DEPRECATED)
> **DATE**: 2025-07 — initial extraction run
> **STATUS**: ⚠️ Historical reference only. Superseded by v3 (109 workers, 4 pages each).
> **SUPERSEDED BY**: [`../SKILL.md`](../SKILL.md) — v3.0.0 worker orchestration

---

## Table of Contents

1. [Overview](#overview)
2. [Version History](#version-history)
3. [Relationship to Current Skill](#relationship-to-current-skill)
4. [Why V2 Failed — Root Cause Analysis](#why-v2-failed--root-cause-analysis)
5. [Decision Log](#decision-log)
6. [V2 → V3 Migration Map](#v2--v3-migration-map)
7. [Quick Reference — V2 Worker Summary](#quick-reference--v2-worker-summary)
8. [Cross-References](#cross-references)
9. [How to Regenerate Prompts](#how-to-regenerate-prompts)
10. [Lessons Learned](#lessons-learned)
11. [Edge Cases and Failure Modes](#edge-cases-and-failure-modes)
12. [V2 Prompts (Historical — Do Not Use)](#v2-prompts-historical--do-not-use)
13. [Glossary](#glossary)

---

## Overview

These are the exact prompts used to extract the 434-page ASD-STE100 Issue 9 specification.
Each prompt is written to `ste-code/extracted/wN-prompt.txt` and launched via:
```bash
hermes -z "$(cat ste-code/extracted/wN-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo
```

This file is a **historical archive**. It documents the v2 extraction strategy (9 workers,
section-aligned page ranges) that preceded the current v3 strategy (109 workers,
4 pages each). The v2 prompts remain here for three purposes:

1. **Audit trail** — record what was attempted and why it failed
2. **Migration reference** — map v2 section boundaries to the v3 worker grid
3. **Design precedent** — inform future multi-worker extraction projects

NOTE: Do not use these 9 prompts for new extraction work. Use the v3 109-worker
approach defined in [`../SKILL.md`](../SKILL.md).

---

## Version History

| Version | Date | Workers | Pages/Worker | Strategy | Status |
|---------|------|---------|-------------|----------|--------|
| **v1** | 2025-06 | 1 | 434 | Single inline extraction | Failed (truncation) |
| **v2** | 2025-07 | 9 | 30–112 | Section-aligned batch extraction | Superseded |
| **v3** | 2025-07 | 109 | 4 | 37 batches of 3 workers | Current |

### Version Strategy Comparison

| Dimension | v1 (Single) | v2 (Section) | v3 (Fixed-Chunk) |
|-----------|-------------|--------------|-------------------|
| Worker count | 1 | 9 | 109 |
| Pages per worker | 434 | 14–112 | 4 |
| Batch size | 1 | 1 (sequential) | 3 (parallel) |
| Batch count | 1 | 9 | 37 |
| Truncation risk | Critical | High (W6: 112 pages) | None |
| Load balance | N/A | Poor (8× variance) | Perfect (all equal) |
| Parallelism | None | None (sequential discovery) | Full (3 concurrent) |
| Failure recovery | Full restart | 1 worker re-extract | 1 worker re-extract (4 pages) |
| Completion verification | Single file | 9 files, uneven sizes | 109 files, uniform ~3KB each |

## Relationship to Current Skill

The 9 prompts in this file are the **v2 extraction strategy**. They group pages by
logical section boundaries (Section 1 spans pages 1–30, Dictionary A–F spans pages
129–240). This approach caused two problems:

1. **Truncation**: Workers with 30+ pages often hit output limits. The v2 W6 worker
   (112 pages, dictionary A–F) was the worst case. It could not fit every entry in a
   single response.
2. **Uneven load**: W6 processed 112 pages while W5 processed only 14 pages. This
   made batch coordination impractical.

The v3 strategy (see [`../SKILL.md`](../SKILL.md)) replaced these 9 workers with
109 workers. Each worker processes exactly 4 pages. All 109 workers run in 37
batches of 3. This approach:

- Prevents truncation (4 pages fit easily in one response)
- Makes load predictable (every worker has the same page count)
- Enables parallel execution (3 concurrent workers per batch)

The v2 prompts in this file remain as **historical reference**. They document the
section-to-page mapping that informed the v3 worker grid. Do not use them for new
extraction work.

---

## Why V2 Failed — Root Cause Analysis

The v2 strategy assumed that section-aligned page ranges would produce cleaner output
files (one file per logical section). This assumption was incorrect for two reasons.

### Root Cause 1: Output Token Limits

The `hermes -z` worker has a practical output limit. When a worker processes 112 pages
of dictionary entries (W6, pages 129–240), the extracted text exceeds this limit.
The worker truncates mid-response. The truncated output is unusable without manual
repair. The exact truncation point is unpredictable. You cannot resume a truncated
worker reliably.

| Worker | Pages | Dictionary Entries (est.) | Pass/Fail |
|--------|-------|--------------------------|-----------|
| W1 | 30 | N/A (rules text) | Marginal |
| W2 | 36 | N/A (rules text) | Marginal |
| W3 | 28 | N/A (rules text) | Pass |
| W4 | 20 | N/A (rules text) | Pass |
| W5 | 14 | N/A (rules text) | Pass |
| **W6** | **112** | **~2,800** | **FAIL (truncation)** |
| W7 | 60 | ~1,500 | Marginal |
| W8 | 60 | ~1,500 | Marginal |
| W9 | 74 | N/A (appendices) | Marginal |

### Root Cause 2: Sequential Bottleneck

The v2 workers were launched sequentially. Each worker's page range depended on
discovering the previous worker's section boundary. You could not pre-compute the
full worker grid. This forced a serial execution pattern. Total wall-clock time was
the sum of all 9 worker runtimes (approximately 45–90 minutes).

### Root Cause 3: No Failure Isolation

When W6 failed (truncation at ~70% of dictionary A–F), there was no clean recovery
path. Options considered:

1. **Split W6 into sub-ranges** — would break the 9-worker naming scheme
2. **Re-extract W6 with a larger model** — not available at the time
3. **Manual repair of truncated output** — error-prone, slow

The v3 strategy solves all three root causes by design.

---

## Decision Log

| Date | Decision | Rationale | Outcome |
|------|----------|-----------|---------|
| 2025-06 | v1: Single worker, 434 pages | Simplest approach, test feasibility | Failed. Output truncated at ~25%. |
| 2025-07-01 | v2: Section-aligned, 9 workers | Logical grouping, one file per section | Partial. 3 workers marginal, W6 failed. |
| 2025-07-03 | v3: Fixed 4-page chunks, 109 workers | Uniform load, full parallelization, no truncation | Successful. 109/109 complete. |
| 2025-07-04 | Preserve v2 prompts as historical reference | Audit trail, migration map, design precedent | This file. |

---

## V2 → V3 Migration Map

This table shows how each v2 worker's page range was redistributed across the v3
109-worker grid. Use this to locate v3 output files that correspond to a v2 section.

| V2 Worker | Pages | Content | V3 Workers | V3 Batches |
|-----------|-------|---------|------------|------------|
| W1 | 1–30 | Front matter, TOC, Section 1 | W001–W008 | Batches 1–3 |
| W2 | 31–66 | Categories, Sections 1–3 | W009–W017 | Batches 3–6 |
| W3 | 67–94 | Sections 3–5 | W018–W024 | Batches 6–8 |
| W4 | 95–114 | Sections 6–8 | W025–W029 | Batches 9–10 |
| W5 | 115–128 | Section 9, General Recs | W030–W033 | Batch 11 |
| W6 | 129–240 | Dictionary A–F | W034–W061 | Batches 12–21 |
| W7 | 241–300 | Dictionary G–P | W062–W076 | Batches 21–26 |
| W8 | 301–360 | Dictionary Q–Z | W077–W091 | Batches 26–31 |
| W9 | 361–434 | Appendices | W092–W109 | Batches 31–37 |

NOTE: Batch boundaries are approximate. See [`worker-grid.md`](../../../../references/worker-grid.md) for
the exact page-to-worker mapping.

---

## Quick Reference — V2 Worker Summary

| Worker | Pages | Count | Content Description | Output File |
|--------|-------|-------|---------------------|-------------|
| W1 | 1–30 | 30 | Front matter, TOC, Section 1 Rules 1.1–1.6 | `w1-sec1-rules.md` |
| W2 | 31–66 | 36 | Rules 1.7–1.14, categories, Sections 2–3 | `w2-sec2-3-rules.md` |
| W3 | 67–94 | 28 | Rules 3.3–3.7, Sections 4–5 | `w3-sec3-5-rules.md` |
| W4 | 95–114 | 20 | Sections 6–8 (descriptive writing, safety, punctuation) | `w4-sec6-8-rules.md` |
| W5 | 115–128 | 14 | Section 9, General Recommendations GR-1–GR-8 | `w5-sec9-gr-rules.md` |
| W6 | 129–240 | 112 | Dictionary A–F (all entries) | `w6-dict-a-f.md` |
| W7 | 241–300 | 60 | Dictionary G–P (all entries) | `w7-dict-g-p.md` |
| W8 | 301–360 | 60 | Dictionary Q–Z (all entries) | `w8-dict-q-z.md` |
| W9 | 361–434 | 74 | Appendices, index, change form, references | `w9-appendices.md` |

**Load imbalance**: W6 (112 pages) is 8× larger than W5 (14 pages). Standard deviation: 29.3 pages.

---

## Cross-References

| Reference | Path | Description |
|-----------|------|-------------|
| Parent skill | [`../SKILL.md`](../SKILL.md) | v3 worker orchestration (109 workers, 37 batches) |
| Worker grid | [`worker-grid.md`](../../../../references/worker-grid.md) | Full 109-worker page assignment table |
| Section types | [`section-types.md`](../../../../references/section-types.md) | Content classification per page range |
| Progress tracker | [`../../state/PROGRESS.md`](../../../../state/PROGRESS.md) | Per-batch completion status |
| Rails | [`rails.md`](../../../../references/rails.md) | 8 immutable quality guardrails |
| Extraction skill | [`../../extraction/SKILL.md`](../../../../skills/extraction/SKILL.md) | Extraction stage definition |
| Refinement skill | [`../../refinement/SKILL.md`](../../../../skills/refinement/SKILL.md) | Post-extraction formatting rules |
| Agent definitions | [`../../../agent/`](../../../../agent/) | 9 agent role definitions |
| Pipeline master | [`../../../MASTER.md`](../../../../MASTER.md) | Full launch protocol and pipeline stages |

## How to Regenerate Prompts

NOTE: If the page splits change (for example, a new Issue 10 of ASD-STE100), you
must regenerate the 109 prompts. Do not reuse the 9 v2 prompts below.

### Prerequisites

Before you regenerate prompts, check these items:

- [ ] New spec pages exist in `spec/issue-XX-YYYY/` with consistent naming (`page-NNNN.md`)
- [ ] The page count is known (count files: `ls spec/issue-XX-YYYY/page-*.md | wc -l`)
- [ ] You have read access to the spec directory
- [ ] The output directory `.agents/prompts/refine/` exists (create if not: `mkdir -p .agents/prompts/refine/`)
- [ ] Worker count is calculated: `ceil(total_pages / 4)`
- [ ] Batch count is calculated: `ceil(worker_count / 3)`

### Generation Method

1. Split the new spec into 4-page chunks. Use a script:
   ```bash
   python3 .agents/tools/maintenance/split-pages.py \
     --input spec/issue-XX-YYYY/ \
     --pages-per-worker 4 \
     --output .agents/prompts/refine/
   ```

2. Write one prompt file per worker. Each prompt must include:
   - The exact page range (for example, `page-0001.md through page-0004.md`)
   - The exact output file path (for example, `ste-code/extracted/w001-p0001-0004.md`)
   - The instruction: "Extract ALL content. Do not summarize. Output ONLY the markdown file."

3. Update the worker grid at [`worker-grid.md`](../../../../references/worker-grid.md) with the new
   page-to-worker mapping.

4. Update [`../SKILL.md`](../SKILL.md) to use the new worker count.

### Template

```
Read spec/issue-XX-YYYY/page-<<START>>.md through page-<<END>>.md.
Extract ALL content exactly into ste-code/extracted/w<<NNN>>-p<<START>>-<<END>>.md.
Do not summarize. Include every word, every table, every example.
Output ONLY the markdown file.
```

### Validation Checklist (After Regeneration)

After you regenerate all prompts, run these checks:

1. **Count check**: `ls .agents/prompts/refine/w*-prompt.txt | wc -l` matches the expected worker count
2. **Content check**: Each prompt file is 150–300 bytes (short, precise instructions)
3. **Range check**: No gaps or overlaps in page ranges across all prompt files
4. **Path check**: All output paths point to `ste-code/extracted/` with consistent naming
5. **Format check**: All prompts end with "Output ONLY the markdown file."

---

## Lessons Learned

These lessons apply to any multi-worker extraction project. They come from the v1 → v2 → v3
evolution of the ASD-STE100 extraction pipeline.

### L1: Fixed Chunk Size Beats Logical Boundaries

Section-aligned page ranges seem intuitive. One file per section. But section lengths vary
wildly (14 to 112 pages in this spec). Fixed chunk sizes (4 pages each) give you:

- Predictable runtime (every worker finishes in about the same time)
- No truncation risk (4 pages is well within output limits)
- Simple verification (every output file should be about the same size)

BREAKING: Do not align workers to logical section boundaries. Align to fixed page counts.

### L2: Pre-Compute the Full Grid Before Launch

You must know every worker's page range before you launch the first worker. The v2 approach
(discover boundaries sequentially) forced serial execution. The v3 approach (pre-compute
109 ranges from a known page count) enables full parallelization.

### L3: Design for Failure Isolation

A single worker failure must not block the other workers. In v2, W6 failure blocked the
entire dictionary extraction. In v3, a W6 equivalent failure affects only 4 pages. You
re-extract those 4 pages. The other 105 workers are unaffected.

### L4: Batch Size of 3 Is the Sweet Spot

Testing showed that 3 concurrent `hermes -z` workers is the maximum safe batch size.
Larger batches (5+) cause resource contention and timeout cascades. Single-worker batches
underuse available parallelism. Three workers per batch balances throughput and stability.

### L5: Progress Tracking Is Not Optional

The v2 extraction had no formal progress tracking. You could not tell if W6 was still
running or had silently failed. The v3 extraction uses `.agents/state/PROGRESS.md` with
per-batch checkboxes. The execution auditor cross-references this file against disk
evidence. A stale progress file is a CRITICAL finding.

### L6: Preserve Failed Strategies as Reference

The v2 prompts in this file serve as a design precedent. Future extraction projects can
read this file and avoid the same mistakes. The cost of preserving 9 prompts (~300 lines)
is negligible. The cost of repeating the same mistakes is high.

---

## Edge Cases and Failure Modes

### Case 1: Page Count Not Divisible by 4

If the total page count is not a multiple of 4, the last worker gets fewer pages.
Example: 434 pages ÷ 4 = 108 workers with 4 pages + 1 worker with 2 pages (pages 433–434).
This is acceptable. A 2-page worker has zero truncation risk.

### Case 2: Dictionary Entry Spans a Page Boundary

A dictionary entry that starts on page 240 and continues on page 241 will be split
across v3 workers W061 and W062. The merge stage (see [`../../merging/SKILL.md`](../../../../skills/merging/SKILL.md))
handles this by concatenating adjacent files and removing duplicate entry headers.

### Case 3: Worker Output Is Empty or Corrupt

If a v3 worker produces an empty file or garbled output, re-extract only that worker's
4-page range. Do not re-extract the entire batch. Check the worker's prompt file for
syntax errors before retrying.

### Case 4: Spec Page Renumbering

If a new spec issue renumbers pages (for example, Issue 10 adds 20 pages to Section 1),
the v2 section-to-page mapping in this file becomes invalid. Use it only as a rough guide
for content location. Always regenerate prompts from the new spec's actual page count.

### Case 5: Dictionary Content Density Variance

Dictionary pages have higher information density than rules pages. A 4-page dictionary
chunk (letters A–B) may contain 80+ entries. A 4-page rules chunk may contain 2 rules.
Despite this variance, 4-page chunks still fit within output limits. The v3 strategy
accounts for worst-case density (dictionary pages).

### Case 6: Concurrent Worker Resource Contention

When 3 workers run in parallel, they share the same model endpoint. If the endpoint has
a rate limit, workers may receive 429 responses. The batch-of-3 design includes an
implicit rate limit buffer. If timeouts occur, reduce the batch size to 2 for the
affected batch only.

---

## V2 Prompts (Historical — Do Not Use)

The 9 prompts below are the v2 extraction strategy. They are preserved for reference
only. For current extraction work, use the v3 109-worker approach defined in
[`../SKILL.md`](../SKILL.md).

### W1: Pages 1–30 — Front Matter, TOC, Section 1 Rules

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0001.md through page-0030.md

TASK: Read every page and extract ALL content into ste-code/extracted/w1-sec1-rules.md

INCLUDE:
- Front matter (title, copyright, highlights)
- Table of Contents
- Subject-to-rule index
- General introduction
- Section 1 summary and Rules 1.1-1.6 FULL text with ALL example pairs

FORMAT: Markdown with ## headings. ALL example pairs as tables. Exact text. Output ONLY markdown.
```

---

### W2: Pages 31–66 — Categories, Sections 1–3

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0031.md through page-0066.md

TASK: Read every page and extract ALL content into ste-code/extracted/w2-sec2-3-rules.md

INCLUDE:
- Rules 1.7-1.14 FULL text with ALL example pairs
- ALL 19 technical noun categories with descriptions and examples
- ALL 4 technical verb categories with subcategories and examples
- Section 2 summary and Rules 2.1-2.2 FULL text
- Section 3 summary and Rules 3.1-3.2 FULL text

FORMAT: Markdown with ## headings. ALL examples as tables. Exact text. Output ONLY markdown.
```

---

### W3: Pages 67–94 — Sections 3–5 Rules

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0067.md through page-0094.md

TASK: Read every page and extract ALL content into ste-code/extracted/w3-sec3-5-rules.md

INCLUDE:
- Rules 3.3-3.7 FULL text with ALL example pairs
- Section 4 summary and Rules 4.1-4.5 FULL text
- Section 5 summary and Rules 5.1-5.5 FULL text

FORMAT: Markdown with ## headings. ALL examples as tables. Exact text. Output ONLY markdown.
```

---

### W4: Pages 95–114 — Sections 6–8 Rules

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0095.md through page-0114.md

TASK: Read every page and extract ALL content into ste-code/extracted/w4-sec6-8-rules.md

INCLUDE:
- Section 6: Rules 6.1-6.6 with ALL examples (descriptive writing, key words, paragraphs)
- Section 7: Rules 7.1-7.3 with ALL safety instruction examples (WARNING/CAUTION)
- Section 8: Rules 8.1-8.7 with ALL punctuation and word count examples

FORMAT: Markdown with ## headings. ALL examples as blockquotes. Exact text. Output ONLY markdown.
```

---

### W5: Pages 115–128 — Section 9 + General Recommendations

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0115.md through page-0128.md

TASK: Read every page and extract ALL content into ste-code/extracted/w5-sec9-gr-rules.md

INCLUDE:
- Section 9: Rules 9.1-9.4 FULL text with ALL example pairs
- GR-1 through GR-8: FULL text of each General Recommendation with ALL examples
- Word-for-word replacement and different sentence construction patterns

FORMAT: Markdown with ## headings. ALL examples as blockquotes. Exact text. Output ONLY markdown.
```

---

### W6: Pages 129–240 — Dictionary A–F

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0129.md through page-0240.md

TASK: Read every page and extract ALL content into ste-code/extracted/w6-dict-a-f.md

INCLUDE:
- Part 2 Dictionary title and full introduction
- EVERY dictionary entry A through F — do not skip any
- For each: word, POS, APPROVED/UNAPPROVED, meaning or alternatives, verb forms, STE example, non-STE example
- List of approved verbs, recurring errors

FORMAT: Markdown. ## for letters. ### for entries. Blockquotes for examples. Exact text. Output ONLY markdown.
```

---

### W7: Pages 241–300 — Dictionary G–P

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0241.md through page-0300.md

TASK: Read every page and extract ALL content into ste-code/extracted/w7-dict-g-p.md

INCLUDE: EVERY dictionary entry G through P. Do not skip any.
For each: word, POS, APPROVED/UNAPPROVED, meaning/alternatives, verb forms, examples.

FORMAT: Markdown. ## for letters. ### for entries. Exact text. Output ONLY markdown.
```

---

### W8: Pages 301–360 — Dictionary Q–Z

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0301.md through page-0360.md

TASK: Read every page and extract ALL content into ste-code/extracted/w8-dict-q-z.md

INCLUDE: EVERY dictionary entry Q through Z. Do not skip any.
For each: word, POS, APPROVED/UNAPPROVED, meaning/alternatives, verb forms, examples.

FORMAT: Markdown. ## for letters. ### for entries. Exact text. Output ONLY markdown.
```

---

### W9: Pages 361–434 — Appendices

```
EXHAUSTIVE SPEC EXTRACTION — OUTPUT AS MUCH TEXT AS POSSIBLE. DO NOT TRUNCATE. INCLUDE EVERY DETAIL.

PAGES: spec/issue-09-2025/page-0361.md through page-0434.md

TASK: Read every page and extract ALL content into ste-code/extracted/w9-appendices.md

INCLUDE: All appendices, index, issue evolution data, change form, reference documents.

FORMAT: Markdown with ## headings. Exact text. Output ONLY markdown.
```

---

## Glossary

| Term | Definition |
|------|------------|
| **Batch** | A group of workers launched together. v3 uses batches of 3. |
| **Chunk** | A fixed-size page range assigned to one worker. v3 chunks are 4 pages. |
| **Extraction** | Stage 1 of the pipeline. Workers read spec pages and write raw markdown. |
| **hermes -z** | Hermes Agent zero-shot mode. Runs a single prompt with no conversation context. |
| **Issue 9** | The ninth edition of ASD-STE100 (January 2025). The spec extracted by this pipeline. |
| **Load imbalance** | When workers have unequal page counts. v2 had 8× imbalance (14 vs 112 pages). |
| **Page range** | The start and end page numbers assigned to one worker. |
| **Prompt file** | A text file containing the exact `hermes -z` instruction for one worker. |
| **Section-aligned** | Grouping pages by spec section boundaries (v2 strategy). |
| **Fixed-chunk** | Grouping pages by count, not content (v3 strategy). |
| **Truncation** | When worker output is cut off before completion. Caused by exceeding output limits. |
| **Worker** | One `hermes -z` invocation that extracts a specific page range. |
| **Worker grid** | The complete table mapping worker IDs to page ranges. |
| **--yolo** | Hermes Agent flag that skips confirmation prompts for non-interactive execution. |
