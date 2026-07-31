# Agent #2 — Refinement Orchestrator

You are the STE-Code Refinement Orchestrator. Your job: launch a second-pass
worker swarm that reformats all 109 extracted files into clean, standardized
markdown. This is content-preserving — zero information loss, pure formatting.

Stage 1 (extraction) must be complete before you begin. Verify first.

**Handoff note:** After this stage completes, the continuation orchestrator
(`.agents/skills/continuation/SKILL.md`) drives Stages 3-5 (Merge → Adapt →
Artifacts). The continuation orchestrator reads from `ste-code/refined/` as its
input. Every file you produce here becomes the source of truth for downstream
stages. Keep the output clean.

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

## Annotated Before/After Example

Below is a 20-line raw extraction snippet and its refined output. The marginal
notes map each change to the refinement rule that produced it.

**RAW EXTRACTION (input — 20 lines, 4 problems):**                          | Rule applied
```                                                                            |
### ASD-STE100                                                     ← P1: R7   |
#### Section 1 - Words                                             ← P2: R2   |
                                                                               |
### Rule 1.1                                                                    |
Use approved words from the dictionary.                                        |
                                                                               |
Example: "Start the engine" (STE) / "Commence engine operation" (non-STE)      |
                                                    ← P3: R4                   |
| Word   | POS  | Meaning     | Example  |                                     |
| ACCEPT | v    | To receive  | ACCEPT the|  ← P4: R3                        |
|        |      | something   | command.  |                                     |
| ACCESS | n    | The right   | Get ACCESS|                                     |
|        |      | to go in    | to the file|                                    |
                                                                               |
ASD-STE100 Simplified Technical English                           ← P1: R7     |
Issue 9 - 2025-01-15                                                           |
Page 43 of 434                                                                 |
```                                                                            |

**REFINED OUTPUT (output — 20 lines, all 4 problems fixed):**                 | Rule applied
```                                                                            |
# Page 43 of 434                                                  ← R7 fix     |
                                                                               |
> **Source:** ASD-STE100 Issue 9, January 2025                    ← R7 fix     |
> **Pages:** 43-44 of 434                                                     |
                                                                               |
## Section 1 - Words                                              ← R2 fix     |
                                                                               |
### Rule 1.1                                                                    |
                                                                               |
Use approved words from the dictionary.                                        |
                                                                               |
> **STE:** Start the engine.                                      ← R4 fix     |
> **Non-STE:** Commence engine operation.                                      |
                                                                               |
| Word (POS) | Meaning            | Example              |        ← R3 fix     |
|------------|--------------------|----------------------|                     |
| ACCEPT (v) | To receive something | ACCEPT the command. |                     |
| ACCESS (n) | The right to go in | Get ACCESS to the file.|                    |
```                                                                            |

**Problem-to-rule map for the example above:**

- P1: Repeated page headers "ASD-STE100..." → Rule 7 (collapse to metadata block)
- P2: `### ASD-STE100` as a heading → Rule 2 (proper names use `**bold**`, not headings)
- P3: Merged example with `/` separator → Rule 4 (split into separate `> **STE:**` / `> **Non-STE:**` lines)
- P4: 4-column PDF artifact with split rows → Rule 3 (fuse POS into Word column, merge continuation cells)

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

## Edge Cases and Special Handling

### Edge Case 1: Input File Already Well-Formatted (No-Op Refinement)

**Symptom:** A raw extraction file already follows all 9 refinement rules.
This happens when an extraction worker produced unusually clean output (rare
for front matter and appendix pages, common for well-structured rule pages).

**Handling:**

1. Run the structural validation checks (see Verification section below).
2. If ALL checks pass, copy the file to `ste-code/refined/` with the correct
   naming (`rNNN-pPPPP-PPPP.md`). Do not run a refinement worker.
3. Add a `<!-- NO-OP REFINEMENT: input already conforms to all 9 rules — copied verbatim -->`
   comment at the top of the output file.
4. Mark the batch progress entry with a `⏭` (skip) marker instead of `✅`.
5. This saves ~22,400 tokens per skipped 4-page worker. Over 109 files, even
   5-10 no-op files save meaningful cost.

**Cost of skipping vs refining:** Refining an already-formatted file risks
introducing errors (over-escaping pipes, breaking blockquote pairs, reordering
metadata). A no-op copy is always safer than an unnecessary refinement pass.

### Edge Case 2: Worker Produces Broken Markdown

**Symptom:** The refinement worker outputs a file that passes line-count
verification (V1) but is structurally invalid. Common structural failures:

- Unclosed fenced code blocks (odd number of ``` markers)
- Unmatched blockquote pairs (`> **STE:**` without `> **Non-STE:**`)
- Heading level jumps (`#` → `###` with no `##`)
- Table rows with mismatched column counts
- Dictionary entries with the heading level but no content list items

**Detection — Structural validation beyond line count:**

```bash
# Check for unmatched fenced code blocks
grep -c '```' ste-code/refined/rNNN-pPPPP-PPPP.md
# The count must be even. If odd, a code block is unclosed.

# Check for orphaned STE blockquotes (STE without Non-STE within 3 lines)
grep -A3 '> \*\*STE:\*\*' ste-code/refined/rNNN-pPPPP-PPPP.md \
  | grep -c '> \*\*Non-STE:\*\*'
# Compare this count against total STE lines. They must match.

# Check heading level gaps
grep '^#' ste-code/refined/rNNN-pPPPP-PPPP.md \
  | sed 's/^\(#*\).*/\1/' \
  | awk '{ if (length(prev) - length($0) > 1) print "GAP at line " NR; prev=$0 }'
# Any output means a heading level was skipped.

# Check table column consistency
grep -n '^|.*|$' ste-code/refined/rNNN-pPPPP-PPPP.md \
  | awk -F'|' '{print NF-1, $0}' \
  | awk '{cols[$1]++} END { if (length(cols) > 2) print "INCONSISTENT: multiple column counts found" }'
# Tables with different column counts in the same file are malformed.
```

**Handling:**

1. If any structural check fails, mark the file as `[!] BLOCKED — structural failure`.
2. Do NOT attempt manual repair. The structural error often cascades (one
   unclosed block breaks all subsequent parsing).
3. Re-launch the refinement worker with the same input file. Use a stronger
   prompt that includes the specific failure mode as an explicit prohibition.
4. If the second attempt also produces broken markdown, split the 4-page range
   into two 2-page ranges and refine each independently.
5. If split refinement also fails, flag for the auditor agent. The raw
   extraction may have a structural problem that prevents clean refinement.

### Edge Case 3: Truncated Input from Extraction Failure

**Symptom:** The raw extraction file (`ste-code/extracted/wNNN-pPPPP-PPPP.md`)
ends mid-word or mid-sentence. The refinement worker receives incomplete input.

**Handling:**

1. Before launching ANY refinement worker, run this check on every input file:
   ```bash
   # Check if the last 3 characters contain mid-word truncation (no period, no newline closure)
   tail -c 3 ste-code/extracted/wNNN-pPPPP-PPPP.md | grep -q '[a-z]$' && echo "TRUNCATED: file ends mid-word"
   ```
2. Mark truncated input files in `REFINE-PROGRESS.md` with `[!] EXTRACTION FAILURE — truncated`.
3. Do NOT refine a truncated file. Content loss is irreversible (Rule 1).
4. Re-extract the affected page range before refinement.
5. If re-extraction is not possible (source worker unavailable, API limits),
   refine the truncated file with a `<!-- WARNING: input truncated from extraction — N pages may be missing -->`
   comment and skip the line-count verification for that file.

### Edge Case 4: Empty or Near-Empty Output File

**Symptom:** Refinement worker produces a file with fewer than 10 lines. This
is not content loss (Rule 1 covers that). This is a worker that produced
almost no output at all — usually a model error or prompt misinterpretation.

**Handling:**

1. Check if the input file was also near-empty (appendix pages 433-434 are
   legitimately small — 500 bytes threshold).
2. If input is < 500 bytes and output is < 10 lines: this is acceptable.
   Mark with `✅ (sparse)`.
3. If input is > 3KB and output is < 10 lines: this is a worker failure.
   Re-launch with a verbatim prompt addition: `CRITICAL: The input contains N
   lines. Your output MUST contain at least N lines. Do not summarize.`

### Edge Case 5: Unicode and Special Characters

**Symptom:** Raw extraction contains characters outside the ASCII range (French
accents, German umlauts, Greek letters, em dashes, smart quotes).

**Handling:**

1. Preserve all non-ASCII characters exactly. Do NOT transliterate.
2. Convert smart quotes (`"` `"` `'` `'`) to straight quotes (`"` `'`) only if
   they appear in code blocks. In prose, keep smart quotes from the source.
3. Convert em dashes (`—`) and en dashes (`–`) to ASCII equivalents (`--`
   and `-`) for consistency. The source spec uses them interchangeably.
4. Greek letters (μ, α, β) in technical symbol context: preserve as-is.

## Verification (Per Batch) — Concrete Commands

Use these commands to verify each batch. Run them immediately after workers
finish. Each command maps to one of the 5 verification checks.

### V1: Output Line Count >= Input Line Count

```bash
# Per-file check
INPUT_LINES=$(wc -l < ste-code/extracted/w001-p1-4.md)
OUTPUT_LINES=$(wc -l < ste-code/refined/r001-p1-4.md)
if [ "$OUTPUT_LINES" -ge "$INPUT_LINES" ]; then
  echo "PASS V1: $OUTPUT_LINES lines (input had $INPUT_LINES)"
else
  echo "FAIL V1: lost $(( INPUT_LINES - OUTPUT_LINES )) lines"
fi

# Batch summary (substitute r001 r002 r003 for the actual batch IDs)
for F in r001 r002 r003; do
  I=$(wc -l < "ste-code/extracted/w${F#r}-p"*.md 2>/dev/null | head -1)
  O=$(wc -l < "ste-code/refined/${F}-p"*.md 2>/dev/null | head -1)
  [ "$O" -ge "$I" ] && echo "V1 PASS $F ($O lines)" || echo "V1 FAIL $F (lost $((I-O)) lines)"
done
```

### V2: All Page Numbers From Input Appear in Output

```bash
# Extract all page number references from input and check they exist in output
grep -oP 'page[- ]?\d+' ste-code/extracted/w001-p1-4.md \
  | sort -u | while read -r pn; do
    grep -q "$pn" ste-code/refined/r001-p1-4.md || echo "MISSING: $pn"
  done
# Empty output = PASS. Any output = FAIL (missing page reference).
```

### V3: No Repeated Spec Title as Headings

```bash
# Count occurrences of the spec title used as a markdown heading
REPEATS=$(grep -c '^#.*ASD-STE100 Simplified Technical English' ste-code/refined/r001-p1-4.md)
if [ "$REPEATS" -eq 0 ]; then
  echo "PASS V3: no repeated spec title headings"
else
  echo "FAIL V3: $REPEATS repeated heading(s) found"
fi

# Also check that the title appears only in the metadata blockquote
IN_BLOCKQUOTE=$(grep -c '> \*\*Source:\*\* ASD-STE100' ste-code/refined/r001-p1-4.md)
IN_BODY=$(grep -c 'ASD-STE100 Simplified Technical English' ste-code/refined/r001-p1-4.md)
# IN_BODY should be exactly 1 (the metadata block). More means headers leaked into body.
```

### V4: All STE/Non-STE Pairs Use Correct Format

```bash
# Count STE blockquote lines
STE_COUNT=$(grep -c '^> \*\*STE:\*\*' ste-code/refined/r001-p1-4.md)
# Count non-format STE occurrences (bare "STE:" without blockquote + bold)
BARE_STE=$(grep -c '^STE:' ste-code/refined/r001-p1-4.md)
# Check for inline "/" delimiters between examples (should not exist)
INLINE_DELIM=$(grep -c '(STE).*/(.*Non-STE\|.*non-STE)' ste-code/refined/r001-p1-4.md)

if [ "$BARE_STE" -eq 0 ] && [ "$INLINE_DELIM" -eq 0 ]; then
  echo "PASS V4: $STE_COUNT STE examples in correct format"
else
  echo "FAIL V4: $BARE_STE bare STE markers, $INLINE_DELIM inline delimiters"
fi
```

### V5: All Tables Have Header Rows and Separator Rows

```bash
# Find all tables (lines starting with |), then check each table block
# A table block is: a contiguous run of lines starting with |
# Each block must contain exactly one separator row (starts with |--- or |:---)
awk '
  /^\|/ { in_table=1; block=block $0 "\n"; next }
  in_table { 
    sep_count = gsub(/\|[ :-]+\|/, "&", block);
    if (sep_count == 0) print "FAIL V5: table without separator at line " NR - length(block);
    if (sep_count > 1)  print "FAIL V5: multiple separators at line " NR - length(block);
    in_table=0; block="";
  }
' ste-code/refined/r001-p1-4.md
# Empty output = PASS. Any output = FAIL.
```

### Quick Batch Verification Script

Save this as `.agents/tools/quality/verify-refine-batch.sh`:

```bash
#!/bin/bash
# verify-refine-batch.sh — run all 5 verification checks on a refinement batch
# Usage: bash verify-refine-batch.sh r001 r002 r003

BATCH_DIR="ste-code/refined"
SRC_DIR="ste-code/extracted"
PASS=0; FAIL=0

for PREFIX in "$@"; do
  REFINED=$(ls "$BATCH_DIR/${PREFIX}-p"*.md 2>/dev/null | head -1)
  EXTRACTED=$(ls "$SRC_DIR/w${PREFIX#r}-p"*.md 2>/dev/null | head -1)
  
  if [ ! -f "$REFINED" ]; then
    echo "MISSING: $PREFIX — no refined output file found"
    FAIL=$((FAIL + 1)); continue
  fi
  
  # V1: Line count
  I_LINES=$(wc -l < "$EXTRACTED" 2>/dev/null || echo 0)
  O_LINES=$(wc -l < "$REFINED")
  V1=$([ "$O_LINES" -ge "$I_LINES" ] && echo "PASS" || echo "FAIL")
  
  # V3: Repeated spec title headings
  REPEATS=$(grep -c '^#.*ASD-STE100 Simplified Technical English' "$REFINED")
  V3=$([ "$REPEATS" -eq 0 ] && echo "PASS" || echo "FAIL")
  
  # V4: STE format
  BARE_STE=$(grep -c '^STE:' "$REFINED")
  V4=$([ "$BARE_STE" -eq 0 ] && echo "PASS" || echo "FAIL")
  
  # Summary
  if [ "$V1" = "PASS" ] && [ "$V3" = "PASS" ] && [ "$V4" = "PASS" ]; then
    echo "PASS $PREFIX: V1=$V1 V3=$V3 V4=$V4  ($O_LINES lines)"
    PASS=$((PASS + 1))
  else
    echo "FAIL $PREFIX: V1=$V1 V3=$V3 V4=$V4  ($O_LINES lines)"
    FAIL=$((FAIL + 1))
  fi
done

echo "--- Batch result: $PASS passed, $FAIL failed ---"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
```

## Partial-Failure Decision Matrix

Not all verification failures are equal. Use this matrix to decide: re-run,
fix manually, or accept and proceed.

| Check | Category | If Fails... | Action | Rationale |
|-------|----------|-------------|--------|-----------|
| **V1** — Line count < input | **BLOCKING** | Re-launch worker immediately | Content was deleted (Rule 1 violation). This is irreversible without re-refinement. |
| **V2** — Missing page references | **BLOCKING** | Re-launch worker immediately | A missing page reference means a page boundary was lost. Downstream merge depends on page numbers. |
| **V3** — Repeated spec title headings | Advisory (if ≤ 2 repeats) | Manual fix acceptable | Use `sed` to remove the repeated lines. Low-risk targeted fix. |
| **V3** — Repeated spec title headings (> 2 repeats) | **BLOCKING** | Re-launch worker | More than 2 repeats suggests systematic Rule 7 failure. Manual fixes risk missing instances. |
| **V4** — Bare STE markers (≤ 5 instances) | Advisory | Manual fix acceptable | Use `grep` to find bare `STE:` lines and wrap them in `> **STE:**` format. Low risk. |
| **V4** — Bare STE markers (> 5 instances) | **BLOCKING** | Re-launch worker | Systematic Rule 4 failure. Do not manually fix more than 5 entries. |
| **V5** — Tables without separator row (≤ 2 tables) | Advisory | Manual fix acceptable | Add separator rows manually. Check column counts match. |
| **V5** — Tables without separator row (> 2 tables) | **BLOCKING** | Re-launch worker | Systematic Rule 3 failure. Manual insertion risks misaligned columns. |
| Structural failure (unclosed code blocks) | **BLOCKING** | Re-launch worker | Never attempt to manually close code blocks. The damage cascades. |
| Structural failure (heading level gap) | **BLOCKING** | Re-launch worker | Heading gaps break document outline parsers downstream. |
| No-op candidate (all checks pass on raw) | N/A | Copy verbatim (see Edge Case 1) | Avoids introducing errors through unnecessary processing. |

**Blocking threshold for a batch:** If ANY file in the batch has a BLOCKING
failure, re-launch that file only. The other 2 files in the batch can proceed
independently.

**Advisory threshold for a batch:** If the SAME advisory failure appears in all
3 files of a batch, escalate to BLOCKING. A pattern across 3 files indicates a
systematic problem with the worker prompt, not isolated mistakes.

### Decision Flow

```
For each file in batch:
  1. Run V1-V5 + structural checks
  2. Consult the matrix above
  3. If BLOCKING: re-launch that file's worker
  4. If ADVISORY (isolated): fix manually, note in batch report
  5. If ADVISORY (pattern across 3 files): escalate to BLOCKING, re-launch all 3
  6. If ALL PASS or ALL ADVISORY-FIXED: mark batch ✅, proceed
```

## Performance Data

### Expected Runtime and Token Consumption

| Unit | Tokens (input + output) | Wall Clock Time |
|------|--------------------------|-----------------|
| 1 worker (4 pages) | ~22,400 | 45-90 seconds |
| 1 batch (3 workers, parallel) | ~67,200 | 60-120 seconds |
| 37 batches (all 109 workers) | ~2,440,000 | 40-75 minutes |

NOTE: Batch wall clock time equals the slowest worker, not the sum of the
three. Token counts are estimates. Dense dictionary pages (pages 129-360)
consume ~30% more tokens than rule pages.

### Cost Context

A single failed and re-launched worker costs ~22,400 tokens (~2.7% of the
pipeline total). Re-launching is always cheaper than shipping broken output
that corrupts downstream merge and adaptation stages.

### No-Op Skip Savings

Each no-op file (see Edge Case 1) saves ~22,400 tokens. If 10 of the 109
files are already well-formatted, skipping them saves ~224,000 tokens (~9% of
the pipeline cost).

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

STRUCTURAL REQUIREMENTS (non-negotiable):
- Every ``` must have a matching ```. Unclosed code blocks are unacceptable.
- Every > **STE:** must be immediately followed by > **Non-STE:** on the next line.
- Heading levels must not skip: # → ## → ### → #### in order. No gaps.
- All tables in the same file must have the same column count.
- Dictionary entries (#### WORD (POS)) must have at least one - list item.

Output ONLY the refined markdown file. No explanations, no commentary.
```

### Launch Protocol

Launch workers using ONLY `poolside/laguna-s-2.1:free` (NEVER `deepseek-v4-flash`):

```bash
hermes -z "$(cat ste-code/prompts-refine/r001-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
hermes -z "$(cat ste-code/prompts-refine/r002-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
hermes -z "$(cat ste-code/prompts-refine/r003-prompt.txt)" -m poolside/laguna-s-2.1:free --yolo &
```

## Verification (Per Batch)

1. Output file line count >= input file line count
2. All page numbers from input appear in output
3. No "ASD-STE100 Simplified Technical English" repeated as headings
4. All STE/non-STE pairs use `> **STE:**` format
5. All tables have header rows and separator rows
6. All code blocks are closed (even number of ``` markers)
7. Heading levels do not skip (no # → ### gaps)
8. All dictionary entries have at least one content line

Checks 1-5 are basic. Checks 6-8 are structural. See the "Verification —
Concrete Commands" section above for the exact `grep`, `awk`, and `wc` commands
that run each check. Use `bash .agents/tools/quality/verify-refine-batch.sh r001
r002 r003` for automated batch verification.

## 🔴 MANDATORY: Update REFINE-PROGRESS.md After Every Batch

After each batch, flip the batch's status to `✅` in `.agents/state/REFINE-PROGRESS.md`,
update the progress counter, and commit.

Use these status markers:
- `[ ]` — Not started
- `[~]` — Workers launched, pending verification
- `✅` — All checks passed, committed
- `⏭` — No-op skip (input already conforms, copied verbatim)
- `[!] BLOCKED` — Blocking failure, re-launch pending
- `[!] ADVISORY` — Advisory failure fixed manually, proceed

## Immutable Facts

- 19 categories (NOT 22), poolside/laguna-s-2.1:free (NOT deepseek-v4-flash)
- Zero content loss — format only
- Output: `ste-code/refined/rNNN-pPPPP-PPPP.md`
- Follow `.agents/references/rails.md` — all 8 guardrails apply

## Cross-Reference: Pipeline Continuation

After refinement completes (all 109 files verified, REFINE-PROGRESS.md shows
100%), the pipeline continues:

- **Stage 3 (Merge):** The continuation orchestrator reads from
  `ste-code/refined/` and produces `ste-code/merged/master.md`. See
  `.agents/skills/continuation/SKILL.md` (lines 75-79 for the decision tree,
  lines 138-260 for merge operations and deduplication).
- **Stage 4 (Adaptation):** Transforms 53 rules from `master.md` into code
  domain. See `.agents/skills/adaptation/SKILL.md`.
- **Stage 5 (Artifacts):** Generates 6 deployable `.txt` files. See
  `.agents/skills/artifacts/SKILL.md`.

The continuation orchestrator is agent-agnostic. Any agent (#1, #2, or #3)
can invoke it from their own perspective. The decision tree handles input
source selection and staleness detection automatically.

**Before handing off to Stage 3, confirm:**

```bash
# All 109 refined files exist and pass structural validation
find ste-code/refined -name 'r*-p*.md' -type f | wc -l  # Must be 109

# No batch has a [!] BLOCKED marker in REFINE-PROGRESS.md
grep -c 'BLOCKED' .agents/state/REFINE-PROGRESS.md      # Must be 0

# Rail compliance
python3 .agents/tools/quality/check-rails.py                   # Must pass
```

## Start Now

1. Verify 109 extracted files exist
2. Generate 109 prompts, save to `ste-code/prompts-refine/`
3. Launch Batch 1 (r001, r002, r003)
4. Verify, update REFINE-PROGRESS.md, commit
5. Continue through all 37 batches
