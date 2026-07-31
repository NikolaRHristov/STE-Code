# Refinement Protocol - 9 Rules (Full Protocol)

Reformat extracted spec files into clean, standardized markdown. Zero content loss - format only. Agent-agnostic.

## When to Use
- After extraction phase complete (all 109 raw files exist)
- When extracted tables show PDF 4-column interleaving artifacts
- When heading hierarchy is inconsistent
- When STE/non-STE examples are not clearly delineated
- Before adaptation phase (clean input = better adaptation)

## What This Fixes

| Problem in Raw Extraction | Refined Output |
|---------------------------|----------------|
| STE examples merged with non-STE in dictionary tables | `**STE:**` / `**Non-STE:**` line separation |
| 4-column PDF interleaving in dictionary entries | Clean 2-column layout |
| `###` used for proper names ("ASD-STE100") | `**bold**` for names, `###` only for real headings |
| Page headers repeated | Collapsed to once per section |
| Rule examples inconsistent | Standardized blockquote format |
| Page footers ("Issue 9", "2025-01-15") | Single page metadata line |
| Missing or inconsistent code blocks | Fenced with language identifier |
| Tables without headers | Headers added where detectable |
| Lists with inconsistent indentation | Standardized 2-space indent |

## 9 Refinement Rules (NON-NEGOTIABLE)

### Rule 1: ZERO CONTENT LOSS
Every word, number, example, table cell from the original extraction MUST appear in the refined output. Format only - never delete.

### Rule 2: STANDARDIZED HEADINGS
```
# Page N of M          ← Every file starts with this
## Section Title        ← Major sections (Section 1, Part 2, etc.)
### Rule X.Y            ← Rule headings
#### WORD (POS)         ← Dictionary entries
```

### Rule 3: TABLE FORMATTING
Clean markdown with header row + separator row:
```
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
```
Align columns. Escape pipe chars with `\|`. Merge split cells.

### Rule 4: STE/NON-STE EXAMPLE FORMAT
```
> **STE:** [The STE-compliant example text, fully written]
> **Non-STE:** [The non-compliant example text, fully written]
```
Separated by blank line. Never merge STE/non-STE into same line.

### Rule 5: CODE BLOCKS
Fenced with language identifier. Never bare ```.

### Rule 6: DICTIONARY ENTRY FORMAT
```
#### WORD (POS) - APPROVED
- **Meaning:** [exact approved meaning]
- **Forms:** [form1, form2, form3]
- **STE:** [example]
- **Non-STE:** [example]

#### word (POS) - UNAPPROVED
- **Alternatives:** [alternative1 (POS), alternative2 (POS)]
- **STE:** [example using alternative]
- **Non-STE:** [example using unapproved word]
```

### Rule 7: PAGE METADATA
```
# Page NNN of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** NN-MM of 434
```
Remove repetitive "ASD-STE100 Simplified Technical English" headers from body.

### Rule 8: LIST STANDARDIZATION
- Numbered: `1. `, `2. ` (not `1)` or `1-`)
- Bullets: `- ` (not `* ` or `• `)
- Nested: 2-space indent

### Rule 9: CONSISTENT SPACING
- `### Heading` → blank line → content
- Content end → blank line → next heading
- Table end → blank line → next content
- Exactly one blank line between sections (never two, never zero)
- No trailing whitespace
- No triple blank lines

## Before/After Examples

Each rule below shows a raw extraction artifact paired with its correct refined output. Use these as the reference pattern during refinement work.

### Rule 2 Example: Heading Hierarchy

**❌ Raw Extraction (incorrect):**
```
### ASD-STE100
#### Section 1 - Words
### Rule 1.1
Use approved words only.
```

**✅ Refined Output (correct):**
```
# Page 12 of 434

## Section 1 - Words

### Rule 1.1
Use approved words only.
```
NOTE: `**ASD-STE100**` moves to page metadata. Only structural headings get `#`/`##`/`###`. Proper names use bold inline.

### Rule 3 Example: 4-Column PDF Interleaving

**❌ Raw Extraction (4-column artifact):**
```
| Word | POS | Meaning | Example |
| ACCEPT | v | To receive | ACCEPT the |
|        |   | something  | command.   |
| ACCESS | n | The right  | Get ACCESS |
|        |   | to go in   | to the file.|
```

**✅ Refined Output (2-column merge):**
```
| Word (POS) | Meaning | Example |
|------------|---------|---------|
| ACCEPT (v) | To receive something | ACCEPT the command. |
| ACCESS (n) | The right to go in | Get ACCESS to the file. |
```
NOTE: The PDF extraction often splits one logical row across two physical rows. Merge the continuation cells into their parent row. The POS column fuses into the Word column as `WORD (POS)`.

### Rule 4 Example: STE/Non-STE Delineation

**❌ Raw Extraction (merged):**
```
Example: "Start the engine" (STE) / "Commence engine operation" (non-STE)
```

**✅ Refined Output (separated):**
```
> **STE:** Start the engine.
> **Non-STE:** Commence engine operation.
```
NOTE: The `/` separator in raw extraction is the delimiter signal. Split on it. Keep each example on its own `>` blockquote line. End each example with a period.

### Rule 6 Example: Dictionary Entry Cleanup

**❌ Raw Extraction (no structure):**
```
ABOUT (adv) - APPROVED
Concerned with. "The manual is about safety." (STE) / "The manual concerns safety procedures." (non-STE)
```

**✅ Refined Output (structured):**
```
#### ABOUT (adv) - APPROVED
- **Meaning:** Concerned with
- **STE:** The manual is about safety.
- **Non-STE:** The manual concerns safety procedures.
```
NOTE: Extract meaning, STE example, and non-STE example into separate list items. Drop the `/` delimiter. Capitalize the word entry in the heading.

### Rule 7 Example: Page Header Collapse

**❌ Raw Extraction (repeated headers):**
```
ASD-STE100 Simplified Technical English
Issue 9 - 2025-01-15
Page 34 of 434

### Rule 1.4

ASD-STE100 Simplified Technical English
Issue 9 - 2025-01-15
Page 35 of 434

### Rule 1.5
```

**✅ Refined Output (single metadata block):**
```
# Page 34 of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** 34-35 of 434

### Rule 1.4

...

### Rule 1.5
```
NOTE: Collapse all repeated page headers into one metadata block at the top. Merge the page range when content spans multiple pages.

## Failure Recovery Protocol

If a verification check fails, follow this decision path. Do not skip steps or guess.

### Verification Check Failures

#### V1: Output line count < input line count
**Symptom:** Refined file has fewer lines than the raw extraction.
**Root cause:** Content was deleted during refinement (Rule 1 violation).
**Recovery:**
1. Run `diff` between raw and refined files to find missing lines.
2. Re-refine ONLY the pages with missing content.
3. Do not re-extract the source pages. The raw extraction is correct.
4. Re-run verification after re-refinement.
5. If the same pages fail twice, escalate to the auditor agent with the diff output.

#### V2: Page numbers from input do not appear in output
**Symptom:** A page range declared in metadata does not match the content.
**Root cause:** Page boundary was misplaced during refinement or header collapse merged wrong pages.
**Recovery:**
1. Check the raw extraction for the missing page numbers.
2. Confirm the page exists in the raw file.
3. If the page exists but was skipped, re-refine that page range.
4. If the page does not exist in the raw file, the extraction phase failed. Escalate to auditor with the missing page numbers.

#### V3: "ASD-STE100 Simplified Technical English" appears as a heading
**Symptom:** The spec title appears as `#` or `##` in the body.
**Root cause:** Page header was not collapsed (Rule 7 violation).
**Recovery:**
1. Find all occurrences of the spec title in the refined file.
2. Remove them from the body and consolidate into the metadata block.
3. Keep one instance only - inside the `> **Source:**` blockquote.
4. Re-run verification.

#### V4: STE/non-STE pairs do not use `> **STE:**` format
**Symptom:** Examples use inline `/` separators or no blockquote at all.
**Root cause:** Rule 4 was not applied to those pairs.
**Recovery:**
1. Search the refined file for `/` characters between examples.
2. For each hit, split into separate `> **STE:**` and `> **Non-STE:**` lines.
3. If the boundary between STE and non-STE is ambiguous, use this heuristic: the example BEFORE `/` is STE, the example AFTER `/` is non-STE.
4. Re-run verification.

#### V5: Tables without header rows
**Symptom:** A markdown table has no `|---|---|` separator row.
**Root cause:** Table was not formatted (Rule 3 violation) or header row was lost during extraction.
**Recovery:**
1. If the table has an obvious first row that names columns, promote it to a header row and add a separator.
2. If no header row is detectable, inspect the raw extraction for column names.
3. If the raw extraction also lacks headers, use the nearest preceding sentence that describes the table columns as the header source.
4. If no header source exists anywhere, mark the table with a `<!-- WARNING: no detectable header -->` comment above it.
5. Re-run verification.

### Escalation Thresholds

| Condition | Action |
|-----------|--------|
| Same batch fails verification twice | Escalate to auditor agent |
| Same page fails verification three times | Re-extract that page range from source |
| More than 10% of a batch fails V1 (line count) | Re-extract the entire batch |
| V2 (missing pages) affects > 2 pages per batch | Escalate to auditor agent |
| Ambiguous STE/non-STE boundary in > 5 entries per batch | Flag for manual review, continue with best-effort split |

### Escalation Message Format
When escalating, send this exact format to the auditor agent:
```
ESCALATION: Refinement failure
Batch: [batch number]
Pages: [page range]
Failed check: [V1/V2/V3/V4/V5]
Evidence: [diff output, line counts, or specific file paths]
Action taken: [what was attempted before escalation]
```

## Edge Cases and Special Handling

### Corrupted Dictionary Entries
**Symptom:** A dictionary entry in the raw extraction has missing fields (no meaning, no example, or garbled text).
**Handling:**
1. Check if the corruption is limited to one entry or affects a sequence.
2. For a single corrupted entry: preserve the raw text AS-IS inside a `<!-- CORRUPTED: reason -->` comment. Do not guess the missing content.
3. For a sequence of > 3 corrupted entries: re-extract that page range. The PDF parse likely failed.
4. Flag all corrupted entries in the batch progress report.

### Dictionary Entries Spanning Multiple Raw Pages
**Symptom:** A dictionary entry starts at the bottom of page N and continues at the top of page N+1.
**Handling:**
1. Detect by checking if the last entry on a page has no closing blank line or the first entry on the next page has no heading.
2. Merge the split entry into one continuous entry in the refined output.
3. Place the merged entry on the page where it starts.
4. Add a `<!-- continued from page N -->` comment at the continuation point.

### Tables Spanning Multiple Raw Pages
**Symptom:** A table's header row is on page N, data rows continue on page N+1, and the header row repeats on page N+1.
**Handling:**
1. Merge into one continuous table in the refined output.
2. Keep only the FIRST occurrence of the header row.
3. Remove repeated header rows from continuation pages.
4. Add a `<!-- table continues from page N -->` comment above the merged table.

### Ambiguous STE/Non-STE Boundaries
**Symptom:** An example block has no clear `/` separator or uses an unusual delimiter (e.g., `vs.`, `compared to`, `or`).
**Heuristic:**
1. If the text contains "instead of", "rather than", or "not": the first clause is non-STE, the second is STE.
2. If the text contains "use X, not Y": X is STE, Y is non-STE.
3. If the text contains only one example with no contrast: treat it as an STE example. Add `<!-- WARNING: no non-STE counterpart found -->`.
4. If the heuristic is uncertain, flag for manual review and use best-effort placement.

### Special Characters in Code Examples
**Symptom:** Raw extraction contains backticks, pipes, angle brackets, or other markdown-sensitive characters inside code examples.
**Handling:**
1. Escape pipe `|` as `\|` ONLY inside table cells, not inside code blocks.
2. For inline code with backticks: use double backticks `` ` ``code` `` `` if the code itself contains a single backtick.
3. For angle brackets `<` and `>` inside code: they are safe inside fenced code blocks. Do not escape them.
4. For HTML-like strings (`<div>`, `<T>`) in non-code context: wrap in inline code backticks.

### Empty or Whitespace-Only Dictionary Entries
**Symptom:** A heading like `####  ( )` appears with no word or POS.
**Handling:**
1. Check if the preceding entry was truncated and this is orphaned continuation text.
2. If orphaned: merge the content into the preceding entry.
3. If genuinely empty: preserve with a `<!-- EMPTY ENTRY: no content in raw extraction -->` comment. Do not invent content.

### Multi-Line Example Text
**Symptom:** An STE or non-STE example spans multiple lines in the raw extraction.
**Handling:**
1. Join continuation lines with a space to form one logical line.
2. If the example is a multi-sentence paragraph, keep it on one `>` line.
3. If the example exceeds 120 characters, it is acceptable to keep it on one line. Markdown renderers will wrap it.

### Conflicting Formatting Signals
**Symptom:** Raw text has both a table delimiter `|` and a blockquote `>` in the same region.
**Priority order:**
1. If the content is structured as rows/columns → treat as a table. Remove spurious `>` markers.
2. If the content is prose with pipe characters → treat as blockquote text. Escape pipes as `\|`.
3. If ambiguous: prefer table format. Tables are the harder structure to reconstruct.

### Nested Lists with Mixed Numbering
**Symptom:** A list has `1.` then `a)` then `-` at different nesting levels.
**Handling:**
1. Flatten to uniform numbering: top level gets `1.`, `2.`, `3.`.
2. Second level gets `- ` bullets with 2-space indent.
3. Third level gets `- ` bullets with 4-space indent.
4. Drop alphabetical markers (`a)`, `b)`) entirely. Replace with numbered or bulleted equivalents.

## Design Rationale

### Why 9 Rules?
The 9 rules address the 9 distinct classes of formatting degradation observed during the extraction phase. Each rule targets one class. Combining rules would create ambiguity about which fix applies when a file has multiple issues. Keeping rules separate makes verification targeted: each check in the verification step maps 1:1 to a rule.

| Rule | Degradation Class | Root Cause |
|------|-------------------|------------|
| R1 | Content loss | Worker truncation or premature output end |
| R2 | Heading chaos | PDF heading extraction without level metadata |
| R3 | Table fragmentation | 4-column PDF grid misaligned with 2-column logical table |
| R4 | Example grouping | `/` delimiter in prose not recognized as boundary |
| R5 | Bare code fences | Language metadata lost in text extraction |
| R6 | Dictionary flattening | Key-value structure flattened to prose during PDF parse |
| R7 | Header repetition | PDF page headers extracted as body content |
| R8 | List inconsistency | Mixed bullet styles in source document |
| R9 | Spacing entropy | Variable blank line counts from PDF layout engine |

### Why Zero Content Loss Is Rule 1
Formatting can be fixed. Missing content cannot be recovered without re-extraction. Content loss is a one-way error - once a word is dropped, no downstream phase can restore it. Formatting errors are two-way - they can be fixed in refinement or caught in adaptation. Rule 1 is first because it is the only irreversible failure mode.

### Why Blockquote Format for Examples
The `> **STE:**` format was chosen over alternatives for three reasons:
1. **Visual distinction.** Blockquotes render with an indent and left border in most markdown viewers. This makes examples instantly distinguishable from rule text.
2. **Searchability.** `grep '> \*\*STE:\*\*'` finds all STE examples in one command. Inline formats require context-aware parsing.
3. **Machine readability.** Downstream adaptation workers can split on `> **Non-STE:**` to extract example pairs for transformation. No regex ambiguity.

### Why 2-Space Indent for Nested Lists
Commonmark and GitHub Flavored Markdown both treat 2-space indent as a list continuation. 4-space indent creates a code block in some parsers. 2-space indent is the minimum unambiguous indent that works across all major renderers.

### Why `#### WORD (POS)` for Dictionary Entries
The `####` (h4) level was chosen because:
- `#` = page-level metadata
- `##` = section-level grouping
- `###` = rule-level heading
- `####` = individual entry

This 4-level hierarchy matches the logical structure of the spec: page → section → rule → entry. Using `####` also enables table-of-contents generation that drills down to individual words.

### Why 4 Pages per Worker
The source PDF has 434 pages. At 4 pages per worker, that is 109 workers (108 × 4 + 1 × 2). This was chosen because:
- 4 pages fit comfortably in a single LLM context window with room for the 9 rules and output formatting.
- 109 workers parallelize well in batches of 3 (36 batches + 1 remainder).
- Fewer pages per worker (2) would double the worker count and batch overhead. More pages (6+) would risk context truncation on dense dictionary pages with many entries.

## Performance and Resource Considerations

### Token Usage Estimates

| Refinement Pass | Input Tokens (approx.) | Output Tokens (approx.) | Total |
|-----------------|------------------------|------------------------|-------|
| Dictionary page (dense, ~15 entries) | 3,500 | 2,800 | 6,300 |
| Rule page (prose-heavy) | 2,800 | 2,200 | 5,000 |
| Mixed page (rules + table) | 3,200 | 2,500 | 5,700 |
| **Average per page** | **3,100** | **2,500** | **5,600** |
| **Per 4-page worker** | **12,400** | **10,000** | **22,400** |
| **Per batch (3 workers)** | **37,200** | **30,000** | **67,200** |
| **Full pipeline (109 workers)** | **~1,350,000** | **~1,090,000** | **~2,440,000** |

### Time Estimates

| Unit | Wall Clock Time (approx.) |
|------|---------------------------|
| Single worker (4 pages) | 45-90 seconds |
| Batch of 3 workers (parallel) | 60-120 seconds |
| Full pipeline (37 batches) | 40-75 minutes |

NOTE: Times are estimates for `poolside/laguna-s-2.1:free` under normal API load. Peak hours may add 20-40% latency. Workers run in parallel within a batch, so the batch time is the slowest worker, not the sum.

### Context Window Safety
`poolside/laguna-s-2.1:free` has a large context window. At ~12,400 input tokens per worker, we use approximately 10% of available context. This leaves ample room for:
- The 9 rules embedded in the prompt (~1,500 tokens)
- Multi-turn corrections if verification fails (~3,000 tokens per correction round)
- Dense pages with unusually large tables (up to 3× normal token count)

### Memory Management for Large Batches
If a batch exceeds expected token usage by > 50%:
1. Split the batch into 2 smaller batches.
2. Re-run the affected workers with 2 pages each instead of 4.
3. Update `REFINE-PROGRESS.md` to reflect the split.
4. Do not split mid-batch arbitrarily. Only split when a worker reports output truncation or when token count exceeds 18,000 input tokens.

### Cost Awareness
At approximate API pricing, the full refinement pipeline costs roughly:
- Input: ~1.35M tokens
- Output: ~1.09M tokens
- Total pipeline cost is modest. Re-running a single failed batch costs ~2.7% of the full pipeline. Prefer re-refinement over manual fixes for speed and consistency.

## Common Pitfalls and Quick Fixes

### Pitfall 1: Over-Escaping Pipes
**Problem:** Worker escapes ALL pipe characters, including those inside code blocks.
**Fix:** Check if the pipe is inside a fenced code block. If yes, do not escape it. Only escape pipes in table cells and prose.
**Detection:** `grep '\\\\|' refined-file.md` - if hits appear inside ``` fences, over-escaping occurred.

### Pitfall 2: Heading Level Skipping
**Problem:** Worker jumps from `#` to `###` without a `##` in between.
**Fix:** Insert the missing `##` level. If no natural section title exists, use `## Continuation` as a placeholder heading.
**Detection:** Parse the file for heading levels. Any gap of 2+ levels (e.g., `#` → `###`) is a skip.

### Pitfall 3: Blank Line Between Blockquote Lines
**Problem:** Worker inserts a blank line between `> **STE:**` and `> **Non-STE:**`.
**Fix:** Remove the blank line. These two lines form a pair and must be adjacent.
**Detection:** Search for `> \*\*STE:\*\*.*\n\n> \*\*Non-STE:\*\*` - if found, a blank line separates the pair.

### Pitfall 4: Trailing Whitespace in Tables
**Problem:** Table cells have trailing spaces that cause alignment issues in some renderers.
**Fix:** Trim trailing whitespace from all table cells after column alignment.
**Detection:** `grep ' |$' refined-file.md` - any hit is trailing whitespace in a table row.

### Pitfall 5: Metadata Block Not at Top
**Problem:** The `> **Source:**` block appears after content instead of at the top of the file.
**Fix:** Move the metadata block to immediately after the `# Page N of M` heading.
**Detection:** Check if line 2 or 3 is not `> **Source:**`. If content appears before the metadata block, it is misplaced.

### Pitfall 6: Dictionary Entry Missing Forms Field
**Problem:** An APPROVED entry has meaning and examples but no `- **Forms:**` line.
**Fix:** If the raw extraction includes verb forms, add them. If the raw extraction has no forms data, add `- **Forms:** (not specified in source)`.
**Detection:** Search for `#### .* - APPROVED` headings and check the following 5 lines for `**Forms:**`.

## Quality Heuristics for Spot-Checks

After each batch, pick 1 random file and apply these 30-second checks:

### 30-Second Spot-Check Protocol
1. **Line 1 check:** Does the file start with `# Page N of 434`? (1 second)
2. **Metadata check:** Is `> **Source:**` within the first 5 lines? (2 seconds)
3. **Heading scan:** Do heading levels go `#` → `##` → `###` → `####` without skipping? (10 seconds - scan visually)
4. **Example check:** Pick any `> **STE:**` block. Is there a `> **Non-STE:**` block immediately after? (5 seconds)
5. **Table check:** Pick any table. Does it have a `|---|---|` separator row? (5 seconds)
6. **Spacing check:** Are there any triple blank lines? (5 seconds - `grep -n '^$' file | uniq -c` or visual scan)
7. **Trailing whitespace check:** Run `grep -c '[[:space:]]$' refined-file.md`. Result must be 0. (2 seconds)

### Spot-Check Pass/Fail
- **PASS:** All 7 checks pass. Batch is within expected quality range.
- **SOFT FAIL:** 1 check fails. Note it in batch progress. Fix in next batch cycle if pattern repeats.
- **HARD FAIL:** 2+ checks fail. Re-refine the affected pages before proceeding to the next batch.

### Sampling Strategy
- Batch 1: Check file 1 (establish baseline)
- Batch 2-10: Check the last file in the batch (catches drift)
- Batch 11-20: Check the middle file (catches mid-batch fatigue)
- Batch 21-37: Rotate: first, middle, last, repeat

## Worker Setup

109 workers, 4 pages each. Batches of 3. Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`

### Launch Protocol
```bash
hermes -z "$(cat prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
```
Use ONLY poolside/laguna-s-2.1:free. 3 workers per batch.

## Verification (Per Batch)
1. Output line count >= input line count
2. All page numbers from input appear in output
3. No "ASD-STE100 Simplified Technical English" repeated as headings
4. All STE/non-STE pairs use `> **STE:**` format
5. All tables have header rows

## 🔴 MANDATORY: Progress Tracking
Update REFINE-PROGRESS.md after EVERY batch. Flip batch status to ✅. Update counter. Git commit. The auditor cross-references this against disk.

References: `.agents/references/rails.md`, `.agents/references/quality-checklist.md`
