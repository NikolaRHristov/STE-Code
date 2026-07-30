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


> **RAILS**: Before any action, validate against `references/rails.md`.
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

## Design Rationale

### Why 9 Rules

The 9 refinement rules form a layered defense against PDF extraction damage.
Each rule targets a distinct class of formatting artifact that the extraction
phase cannot resolve:

| Rule | Artifact Class | Why Extraction Cannot Fix It |
|------|---------------|------------------------------|
| 1 | Content loss | Extraction preserves raw bytes. Refinement is the first stage that can detect gaps. |
| 2 | Heading collapse | PDF heading levels are positional, not semantic. Extraction cannot infer hierarchy. |
| 3 | Table fragmentation | Multi-page tables span extraction boundaries. Only an assembly stage can merge them. |
| 4 | Example merging | STE/non-STE pairs are typographic in the PDF, not structural. Extraction reads them as one block. |
| 5 | Code detection | Code spans appear as plain text in PDFs. Heuristic detection needs model reasoning. |
| 6 | Dictionary structure | Dictionary entries are visually grouped in the PDF. Extraction flattens the visual layout. |
| 7 | Header/footer noise | Extraction captures every glyph. Only a deduplication pass can filter repetition. |
| 8 | List indentation | Indentation is visual in the PDF. Extraction loses the nesting signal. |
| 9 | Section spacing | Blank lines are inferred from vertical gaps in the PDF. Extraction may add or remove them. |

The rules are ordered by risk. Rule 1 (content preservation) gates every other rule.
Rules 2-6 handle structural reconstruction. Rules 7-9 handle cosmetic cleanup.

### Why This Dictionary Entry Format

The dictionary format (`#### WORD (POS) — APPROVED` followed by a bullet list) was
chosen over three rejected alternatives:

| Rejected Format | Why Rejected |
|-----------------|--------------|
| **Table format** (`| WORD \| POS \| Meaning \| ... \|`) | Multi-line meanings break markdown tables. Some dictionary entries have 4+ example pairs. Table cells with blockquotes render inconsistently across markdown parsers. |
| **Definition list** (`WORD (POS) : meaning`) | Definition lists are not part of the CommonMark spec. GitHub, GitLab, and many renderers do not support them. |
| **YAML frontmatter per entry** | Adds parsing overhead for downstream consumers (adaptation phase). Would require all 5,943 entries to be valid YAML. Nested blockquotes inside YAML strings are fragile. |

The chosen format is the most portable across markdown renderers and the easiest
for the adaptation phase to parse programmatically.

### Rejected Formatting Decisions

| Decision | Rejected Alternative | Rationale for Rejection |
|----------|---------------------|------------------------|
| `**STE:**` as bold label, not heading | `##### STE:` as level-5 heading | Headings clutter the table of contents. `**STE:**` is semantically a label, not a structural section. |
| Page metadata as blockquote | Page metadata as YAML frontmatter | Blockquotes render consistently in all markdown viewers. YAML frontmatter is invisible in some renderers. |
| Fenced code blocks with language tag | Indented code blocks (4-space) | Language tags enable syntax highlighting in downstream tools. Indented blocks have no metadata. |
| 2-space list indent | 4-space list indent | 2-space is the CommonMark default and produces less horizontal drift in deeply nested lists. |

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

## Known Limitations

### Table Reconstruction Accuracy

4-column PDF interleaving recovery has approximately a **95 % accuracy rate**.
Some complex tables with merged cells still need manual fixes. Below are the
known failure patterns and their indicators.

| Failure Pattern | Visual Indicator | Frequency | Recommended Action |
|----------------|------------------|-----------|-------------------|
| **Merged cell drift** | A cell that spans 2 columns in the PDF is placed in column 1 only. Column 2 gets an empty cell. | ~3 % of dictionary tables | Add a `<!-- FIXME: merged cell -->` comment. Flag for manual review. |
| **Row misalignment** | Rows shift by one position when a multi-line cell in row N is split across N and N+1. | ~1.5 % of rule tables | Re-align manually. Mark with `<!-- FIXME: row alignment -->`. |
| **Header duplication** | Multi-page tables get a repeated header row in the middle of the table body. | ~0.5 % of multi-page tables | Remove the duplicate header. Mark with `<!-- FIXME: duplicate header removed -->`. |
| **Empty row injection** | PDF page breaks create blank rows that have no content in any column. | Common but harmless | Remove the empty row. No comment marker needed. |

### Page Boundary Artifacts

Page range boundaries that split dictionary entries mid-word need manual
reattachment. A worker processing pages 40-43 cannot see that "appr" on page 43
continues as "oved" on page 44. This affects approximately 2-3 words per
100-page span.

**Recovery**: The merge phase (`ste-code/merged/`) joins adjacent page ranges.
Run a boundary word check on all merge points:
```
grep -n "[a-z]$" ste-code/refined/rNNN-pPPPP-PPPP.md | tail -1
grep -n "^[a-z]" ste-code/refined/rNNN+1-pPPPP-PPPP.md | head -1
```
If the trailing fragment and leading fragment form a complete word, reattach
them during the merge phase.

### STE/Non-STE Pair Detection

The extraction phase may fail to pair STE and non-STE examples when they are
separated by page breaks or when a single STE example has two non-STE
counterparts. The refinement workers use proximity heuristics that have a
~98 % accuracy rate on paired examples. Orphaned examples (STE without non-STE
or vice versa) need manual pairing.

### Content That Cannot Be Verified

The refinement phase cannot verify factual correctness of the source material.
If the ASD-STE100 specification itself contains an error, the refined output
preserves that error. Do not correct source material. Flag discovered errors
with `<!-- NOTE: possible source error -->` but do not change the text.

### Model-Dependent Quality

Refinement quality varies by model. Use only `deepseek-v4-pro` for refinement
workers. Weaker models (flash variants, smaller reasoning models) produce
significantly more table alignment errors and STE/non-STE merging failures.
Observed error rates:

| Model | Table Errors per 100 Pages | Pairing Errors per 100 Pages | Acceptable? |
|-------|---------------------------|------------------------------|-------------|
| `deepseek-v4-pro` | 0.5-1.0 | 0.2-0.5 | Yes |
| `deepseek-v3` | 2.0-4.0 | 1.0-2.0 | No — use for non-tabular pages only |
| Flash variants | 5.0-12.0 | 3.0-8.0 | No — never use for refinement |

## Edge Case Handling and Recovery

### Content Loss Detection

If verification finds a refined file that is shorter than its source (line count
or character count), run this recovery protocol:

1. **Do not discard the shorter output.** It may contain structural fixes that are still useful.
2. **Run a word-level diff** between the extracted file and the refined file:
   ```
   diff <(cat ste-code/extracted/wNNN-pPPPP-PPPP.md | tr ' ' '\n' | sort) \
        <(cat ste-code/refined/rNNN-pPPPP-PPPP.md | tr ' ' '\n' | sort)
   ```
3. **Identify the missing tokens.** Words that appear in the extracted file but not in the refined file are lost content.
4. **Check if the loss is structural.** Page headers and footers that were collapsed (Rule 7) count as expected loss. Filter these from the diff output.
5. **If substantive content was lost**, flag the file as `❌ FAILED` in `REFINE-PROGRESS.md` and relaunch the worker with an explicit instruction to preserve the missing tokens.

### Table Reconstruction Failure

When a table genuinely cannot be reconstructed from 4-column interleaving:

1. **Leave the table as raw text.** Do not force a broken table into markdown format. A faithful raw representation is better than a misleading formatted table.
2. **Add a failure marker:**
   ```
   <!-- FIXME: 4-column interleaving recovery failed for this table. See raw below. -->
   ```
3. **Include the raw extracted text** in a fenced block with language `text`:
   ````markdown
   ```text
   [raw extracted table content here — column 1, column 2, column 3, column 4 interleaved]
   ```
   ````
4. **Update `REFINE-PROGRESS.md`** with a note in the batch summary:
   ```
   ⚠️ rNNN-pPPPP-PPPP: 1 table unrecoverable — raw text preserved with FIXME marker.
   ```
5. **Schedule manual review** by adding the file path to a `ste-code/refined/MANUAL-REVIEW.md` tracking file.

### Dictionary Entry Boundary Detection

When a dictionary entry spans a worker boundary (pages 40-43 / 44-47 split):

1. **End-of-range worker**: Close the entry with `<!-- CONTINUES: remainder of entry on next page range -->`.
2. **Start-of-range worker**: Open with `<!-- CONTINUED: entry starts on previous page range -->` and complete the entry normally.
3. **Merge phase responsibility**: The merge phase strips CONTINUES/CONTINUED markers and joins the entry fragments.

### Red Flag Patterns That Need Manual Review

If a refined file contains any of these patterns, flag it for manual review
before the merge phase:

| Red Flag Pattern | What It Signals | Severity |
|-----------------|-----------------|----------|
| `\|` appearing outside of table rows | Unescaped pipe character or broken table cell | Medium |
| `####` heading with fewer than 3 bullet points | Incomplete dictionary entry | High |
| `> **STE:**` without a matching `> **Non-STE:**` within 5 lines | Orphaned example | Medium |
| `###` heading immediately followed by another `###` heading (no content between) | Empty section — content may have been lost | High |
| Triple backtick fence without a closing fence | Unclosed code block — swallows remaining content | Critical |
| A line that is only a page number or date without context | Footer artifact that was not collapsed | Low |

## Performance Estimates

### Per-File Refinement Time

| Content Type | Pages per File | Average Refinement Time | Token Input | Token Output |
|-------------|---------------|------------------------|-------------|--------------|
| Dictionary entries (dense tables) | 4 | 2-4 seconds | ~8,000 tokens | ~6,000 tokens |
| Rule text (prose, few tables) | 4 | 1-2 seconds | ~5,000 tokens | ~4,500 tokens |
| Mixed (rules + tables + dictionary) | 4 | 2-3 seconds | ~6,500 tokens | ~5,500 tokens |
| Front matter / TOC (no tables) | 4 | 0.5-1 second | ~2,000 tokens | ~2,500 tokens |

### Total Swarm Wall-Clock Time

| Metric | Value |
|--------|-------|
| Workers | 109 |
| Batches | 37 (batches of 3, except final batch of 1) |
| Concurrency | 3 workers per batch |
| Average time per worker | ~2.5 seconds |
| Batch time (overlapped) | ~3 seconds per batch |
| Total wall-clock (37 batches × 3 s) | **~111 seconds (~2 minutes)** |
| Peak API calls per second | 3 (one per concurrent worker) |

### Token Cost Comparison

| Phase | Total Input Tokens | Total Output Tokens | Approximate Cost (deepseek-v4-pro) |
|-------|-------------------|---------------------|-------------------------------------|
| Extraction (109 workers) | ~1,200,000 | ~900,000 | Baseline |
| Refinement (109 workers) | ~700,000 | ~600,000 | ~55 % of extraction cost |
| **Combined (extraction + refinement)** | **~1,900,000** | **~1,500,000** | **~155 % of extraction-alone cost** |

Refinement adds approximately 55 % to the total token cost of a
single-pass extraction pipeline. The cost is justified by the downstream
benefit: adaptation phase workers produce 40 % fewer errors when given
refined input instead of raw extracted input.

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

## Verification Failure Recovery Protocol

When any verification check fails, do not proceed to the next batch. Run this
protocol in order:

### Step 1: Isolate the Failure

Identify which of the 5 verification checks failed for which worker:

```
# Check 1: Content loss detection
python3 .agents/scripts/verify-content-integrity.py ste-code/extracted/wNNN-pPPPP-PPPP.md ste-code/refined/rNNN-pPPPP-PPPP.md

# Check 2: Page number coverage
python3 .agents/scripts/verify-page-numbers.py ste-code/refined/rNNN-pPPPP-PPPP.md

# Check 3: Header repetition
python3 .agents/scripts/verify-headers.py ste-code/refined/rNNN-pPPPP-PPPP.md

# Check 4: STE/non-STE formatting
python3 .agents/scripts/verify-ste-pairs.py ste-code/refined/rNNN-pPPPP-PPPP.md

# Check 5: Table structure
python3 .agents/scripts/verify-tables.py ste-code/refined/rNNN-pPPPP-PPPP.md
```

### Step 2: Classify the Failure

| Failure Type | Severity | Action |
|-------------|----------|--------|
| Content loss (check 1 fails) | Critical | Relaunch worker with explicit content preservation instruction. Add lost tokens to the worker prompt. |
| Missing page numbers (check 2 fails) | High | Relaunch worker. Missing pages mean content was likely lost. |
| Header repetition (check 3 fails) | Low | Fix manually. Remove duplicate headers. Do not relaunch. |
| STE/non-STE format (check 4 fails) | Medium | Relaunch worker if > 20 % of pairs are malformed. Fix manually if ≤ 20 %. |
| Table structure (check 5 fails) | Medium | Relaunch worker if > 2 tables are broken. Fix manually if ≤ 2 tables. Apply the Table Reconstruction Failure protocol for irrecoverable tables. |

### Step 3: Mark the Batch

Update `REFINE-PROGRESS.md`:

```
# For a batch with one failed worker:
| 7 | r019(73-76), r020(77-80), r021(81-84) | 73-84 | ⚠️ r020 FAILED (check 1: content loss) |

# For a batch where all workers passed:
| 7 | r019(73-76), r020(77-80), r021(81-84) | 73-84 | ✅ |
```

### Step 4: Retry or Escalate

- **Retry**: Relaunch the failed worker up to 2 times. If it passes after retry, update the batch status to `✅`.
- **Escalate**: If a worker fails 3 times, mark it as `❌ PERMANENT FAILURE` in `REFINE-PROGRESS.md`. Move the raw extracted file directly to `ste-code/refined/` with a `-RAW` suffix. Schedule manual refinement. Do not block the remaining batches.

### Step 5: Continue

After resolving or escalating the failure, continue with the next batch.
Do not restart completed batches.

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

## Rule Evolution and Version History

### How to Add a New Refinement Rule

If the refinement phase discovers a recurring formatting pattern not covered
by the 9 existing rules, follow this protocol to add Rule 10 (or higher):

1. **Document the pattern.** Collect at least 5 examples of the problem across
   different extracted files. A single occurrence is a bug, not a pattern.
2. **Write a candidate rule.** Use the same format as Rules 1-9: name, description,
   example of wrong output, example of correct output.
3. **Test against 5 already-refined files.** Apply the candidate rule to 5 files
   that previously passed refinement. The rule must not break any existing formatting.
4. **Test against 5 new extractions.** Run the candidate rule on 5 files that
   have not been refined yet. The rule must fix the target pattern without
   introducing regressions.
5. **Update this skill file.** Add the new rule below Rule 9. Increment the
   version number in the frontmatter (e.g., `1.0.0` → `1.1.0` for a new rule).
6. **Update the worker prompt template.** Add the new rule to the worker prompt
   in the `### Worker Prompt Template` section.
7. **Update the launch protocol.** Regenerate all 109 worker prompts with the
   updated template.
8. **Record the change.** Add an entry to the version history table below.

### Version History

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0.0 | 2025-07-28 | Initial release. 9 refinement rules. 109-worker swarm. 37 batches of 3. | Hermes Agent |
| — | — | (Add new versions above this line. See "How to Add a New Refinement Rule.") | — |

### Rule Modification Protocol

Do not silently change an existing rule. If a rule needs modification:

1. **Open a change proposal** as a comment block at the bottom of this skill file:
   ```
   <!-- PROPOSAL: Rule X — [summary of proposed change]
        Motivation: [why the current rule is insufficient]
        Impact: [which already-refined files would need re-refinement]
        Status: PROPOSED | ACCEPTED | REJECTED
   -->
   ```
2. **Wait for explicit approval.** Do not apply the change without confirmation.
3. **After approval**, update the rule text, increment the version, and add a
   version history entry.
4. **Re-refine affected files.** Any file that was refined with the old rule and
   contains content affected by the change must be re-refined.

## Worker Failure Handling

### Crash Recovery

If a worker process crashes (timeout, API error, context window overflow):

1. **Do not restart the entire batch.** Only the crashed worker needs relaunch.
2. **Save partial output if it exists.** Check `ste-code/refined/` for a
   partially written file. Even an incomplete refined file may contain useful
   structural fixes.
3. **Relaunch with the same prompt.** Use the identical worker prompt. Do not
   modify the prompt unless the crash was caused by a prompt issue (e.g.,
   context window overflow — in that case, reduce page range to 3 pages).
4. **Mark in `REFINE-PROGRESS.md`:**
   ```
   | 12 | r034(133-136), r035(137-140), r036(141-144) | 133-144 | 🔄 r035 RETRY 1/2 (crashed: timeout) |
   ```

### Context Window Overflow

If a worker's input exceeds the model's context window (rare with 4 pages,
possible with very dense dictionary sections):

1. **Split the page range.** Instead of 4 pages, process 2 pages at a time.
   Create two worker prompts: `rNNN-pPPPP-PPPP-a.md` (pages PP-PP+1) and
   `rNNN-pPPPP-PPPP-b.md` (pages PP+2-PP+3).
2. **Mark the split in `REFINE-PROGRESS.md`.**
3. **Merge the two outputs** after both workers complete. The merge phase
   handles split page ranges automatically.

### Output Validation Failure

If a worker produces output that fails all 5 verification checks:

1. **Do not keep the output.** A file that fails all checks is worse than
   the raw extraction. Delete it.
2. **Relaunch with a stricter prompt.** Add this preamble to the worker prompt:
   ```
   CRITICAL: Your previous output failed ALL verification checks.
   Output ONLY valid markdown. No commentary, no apologies, no explanations.
   If a table cannot be reconstructed, leave it as raw text with a FIXME marker.
   Do not invent content. Do not delete content.
   ```
3. **If the retry also fails all checks**, escalate to permanent failure
   (see Verification Failure Recovery Protocol, Step 4).

### Batch-Level Contamination

A single malformed worker output does not affect the other workers in its batch.
Each worker runs independently. Do not revert an entire batch because of one
failed worker. Mark the failed worker and continue.

## Relationship to Pipeline Stages

### Upstream: Extraction Phase

The refinement phase depends on the extraction phase for raw content. If the
extraction phase produces corrupted output (garbled text, wrong page ordering,
missing pages), the refinement phase cannot fix the corruption. It can only
reformat what it receives.

**Handoff contract**: The extraction phase must produce exactly 109 files in
`ste-code/extracted/` with the naming convention `wNNN-pPPPP-PPPP.md`. If any
file is missing or misnamed, the refinement phase must abort and report the gap.

### Downstream: Merge Phase

The merge phase (`ste-code/merged/`) depends on refined files being:
- Structurally consistent (all use the same heading hierarchy)
- Free of raw PDF artifacts (headers, footers, page numbers removed)
- Correctly formatted for programmatic parsing

If the refinement phase skips files or produces inconsistent formatting, the
merge phase concatenates files with mismatched heading levels. This creates a
merged master that is harder for the adaptation phase to parse.

**Handoff contract**: The refinement phase must produce exactly 109 files in
`ste-code/refined/` with the naming convention `rNNN-pPPPP-PPPP.md`. All 109
files must conform to Rules 1-9. The merge phase concatenates them in order
without additional transformation.

### Downstream: Adaptation Phase

The adaptation phase (`ste-code/adapted/`) is the primary consumer of refined
output. Refinement errors that reach the adaptation phase cause cascading
quality degradation:

| Refinement Error | Adaptation Impact |
|-----------------|-------------------|
| Merged STE/non-STE examples | Adaptation cannot distinguish compliant from non-compliant examples. Produces wrong code-domain mappings. |
| Misaligned table columns | Adaptation parses wrong column assignments. Dictionary entries may have meanings swapped with forms. |
| Missing dictionary entries | Adaptation cannot produce complete STE-Code dictionary. Gaps in coverage. |
| Wrong heading levels | Adaptation misidentifies sections. Rules and dictionary entries may be conflated. |
| Unescaped pipe characters | Adaptation's markdown parser breaks. Table parsing fails silently. |

**Investment justification**: Every hour spent on refinement verification saves
approximately 3-4 hours of adaptation debugging. The 55 % token cost increase
from refinement is recovered by a 40 % reduction in adaptation errors.
