---
name: ste-code-validate
description: "Validate worker extraction quality with per-batch checks and spot-checks against original spec pages."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [ste-code, validation, quality, spot-check, workers]
---

# STE-Code Validation Protocol

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable guardrails.

Systematic validation of worker extraction output. Run after each batch (every 3 workers)
and after the full merge. Catches fabrication, truncation, and incompleteness.


> **RAILS**: Before any action, validate against .
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## Worked Example — Batch Validation Output

This section shows real output from a batch validation run. Use these patterns
to know what PASS, WARN, and FAIL results look like.

### Example: Batch 4 (w010-w012) — All Passing

```
=== Batch 4 Validation (w010-w012, pages 37-48) ===

--- Check 1: File Existence and Size ---
PASS w010: 187 lines, 12432 bytes
PASS w011: 195 lines, 13108 bytes
PASS w012: 178 lines, 11945 bytes

--- Check 2: Content Signals ---
w010: 8 matches (Section 1, Rule 1.) — PASS (page range 37-48, expected Section 1/Rule 1.)
w011: 11 matches (Rule 1.) — PASS
w012: 7 matches (Rule 1., Part 1) — PASS

--- Check 3: Truncation Detection ---
w010 last 3 lines: "Page 40\n2025-01-15\nIssue 9" — PASS (clean page footer)
w011 last 3 lines: "The approved word is \"test.\"\nPage 44\n2025-01-15" — PASS
w012 last 3 lines: "apply to all parts.\nPage 48\nIssue 9" — PASS

--- Check 4: Fabrication Detection ---
w010: no modern software terms found — PASS
w011: no commentary language found — PASS
w012: no fabrication flags — PASS

=== Batch 4 Result: ALL PASS ===
```

### Example: Batch 7 (w019-w021) — Mixed Results

```
=== Batch 7 Validation (w019-w021, pages 73-84) ===

--- Check 1: File Existence and Size ---
PASS w019: 201 lines, 14823 bytes
FAIL w020: only 24 lines — possible truncation or empty extraction
PASS w021: 192 lines, 13901 bytes

--- Check 2: Content Signals ---
w019: 14 matches (Section 4, Section 5) — PASS (page range 73-84, expected Section 4/5)
w020: 1 match (APPROVED) — FAIL (expected Section 4/5 in pages 73-84, got dictionary keyword)
w021: 12 matches (Section 5, Rule 5.) — PASS

--- Check 3: Truncation Detection ---
w019: "Page 76\n2025-01-15\nIssue 9" — PASS
w020: "The procedure for remo" — FAIL (truncated mid-word, no page footer)
w021: "Page 84\n2025-01-15\nIssue 9" — PASS

--- Check 4: Fabrication Detection ---
w019: no fabrication flags — PASS
w020: SKIP (too few lines for fabrication check)
w021: no fabrication flags — PASS

=== Batch 7 Result: 1 FAIL (w020), 2 PASS ===
Action: Split w020 page range (77-80) into two halves and re-extract.
See "Re-Extraction Procedure" below.
```

## Per-Batch Validation (After Every 3 Workers)

Run after launching and waiting for each batch of 3 workers.

### Edge Case: Remainder Batches (Fewer Than 3 Workers)

The last batch of the pipeline may contain 1 or 2 workers. Also, a failed
worker replacement may run solo. Handle these cases:

- **1-worker batch**: Run all 4 checks on the single file. Skip the batch
  aggregation header. Mark the batch as complete when the single worker passes.
- **2-worker batch**: Run all 4 checks on both files. The batch result counts
  both workers. Two PASS results make a passing batch. Two FAIL results make a
  failing batch. Mixed results (1 PASS, 1 FAIL) trigger re-extraction for the
  failed worker only.
- **Empty extraction directory**: If `ste-code/extracted/` has no files when
  validation runs, the batch cannot be checked. Write an error entry to
  `ste-code/validation-log.md` and stop. The extraction stage must complete
  before validation can run. See `.agents/skills/extraction/SKILL.md` for
  extraction protocol.

### Edge Case: Boundary-Crossing Page Ranges

When a worker page range crosses two content-signal zones (refer to the
Content Signals table in Check 2), the worker must match signals from both
zones. The check uses an OR condition:

- If page range crosses 64-67 (Section 1 → Section 4 boundary), the worker
  must show at least one signal from BOTH sides. For example, a worker with
  pages 62-69 must match "Rule 1." AND "Section 4".
- If page range crosses 128-129 (Section 9 → Dictionary boundary), the worker
  must match "Rule 9." or "GR" AND "APPROVED" or "UNAPPROVED".
- If page range crosses 360-361 (Dictionary → Appendix boundary), the worker
  must match "APPROVED" or "UNAPPROVED" AND "Appendix" or "Index".

A worker that covers only one side of a boundary is not a failure if its page
range sits entirely within one zone. The boundary check applies only when the
worker page range includes pages from two different content-signal zones.

Run this check for boundary-crossing workers:

```bash
# Detect boundary crossing: check if worker page range includes pages from two zones
# Zones: 1-12, 13-66, 67-128, 129-360, 361-434
# If worker_start <= zone_end AND worker_end >= next_zone_start, check both signals
```

### Check 1: File Existence and Size

```bash
for w in w007 w008 w009; do
  f="ste-code/extracted/${w}-p*.md"
  if [ -f "$f" ]; then
    lines=$(wc -l < "$f")
    bytes=$(wc -c < "$f")
    if [ "$lines" -lt 30 ]; then
      echo "FAIL $w: only $lines lines — possible truncation or empty extraction"
    elif [ "$lines" -lt 80 ]; then
      echo "WARN $w: $lines lines — may be light content (check manually)"
    else
      echo "PASS $w: $lines lines, $bytes bytes"
    fi
  else
    echo "FAIL $w: file not found — worker did not produce output"
  fi
done
```

### Check 2: Content Signals

Verify the file contains expected markers for its page range:

| Page Range | Expected Content Signal |
|------------|------------------------|
| 1-12 | "Copyright", "Highlights", "ASD-STE100 Simplified Technical English" |
| 13-66 | "Section 1", "Rule 1.", "Part 1" |
| 67-128 | "Section 4", "Section 5", "Rule 5.", "WARNING" |
| 129-360 | "Part 2", "Dictionary", "Word", "APPROVED", "UNAPPROVED" |
| 361-434 | "Appendix", "Index", "Issue", "Change" |

```bash
# Example: check a dictionary-range worker
grep -c "APPROVED\|UNAPPROVED" ste-code/extracted/wNNN-p*.md
# Should be >5 for dictionary pages
```

### Check 3: Truncation Detection

The most common failure mode: worker context fills up and output is cut mid-sentence.

```bash
# Last 3 lines of output should end cleanly (period, page footer, or table row)
tail -3 ste-code/extracted/wNNN-p*.md
```

Red flags:
- Last line ends mid-word ("The procedure for remo")
- Last line is a partial table row
- No page footer on last page ("2025-01-15", "Issue 9", "Page NNN")

If truncated, split the worker's page range in half and re-extract both halves.

### Check 4: Fabrication Detection

Fabricated output shows these patterns:
- Modern software examples in spec extraction ("React", "Docker" in page content)
- Commentary language ("This page describes...", "The key point is...")
- Missing spec boilerplate (no "ASD-STE100 Simplified Technical English" header)
- Smooth, flowing prose instead of spec's terse rule format

If fabrication suspected, compare against original page:
```bash
diff <(head -20 spec/issue-09-2025/page-NNNN.md) <(head -20 ste-code/extracted/wNNN-p*.md)
```

## Re-Extraction Procedure (Truncation and Fabrication Recovery)

When a worker fails validation (truncation, fabrication, or missing file),
follow this procedure to replace the worker output. For full orchestration
of multi-agent re-extraction workflows including continuation and error
recovery, refer to `.agents/skills/continuation/SKILL.md`.

### Step 1: Compute Half-Range Splits

Get the failed worker's page range from the worker grid at
`.agents/references/worker-grid.md`. Split the range into two equal halves:

```bash
# Example: w020 covers pages 77-80 (4 pages)
# Half 1: pages 77-78 (2 pages)
# Half 2: pages 79-80 (2 pages)

# Example: w042 covers pages 165-172 (8 pages)
# Half 1: pages 165-168 (4 pages)
# Half 2: pages 169-172 (4 pages)

# Odd page count: give the extra page to the first half
# Example: w055 covers pages 215-221 (7 pages)
# Half 1: pages 215-218 (4 pages)
# Half 2: pages 219-221 (3 pages)
```

### Step 2: Launch Replacement Workers

Use new worker IDs to avoid overwriting the failed output. Append a split
suffix to the original worker ID:

```bash
# Original worker: w020
# Replacement workers: w020a (first half), w020b (second half)

# Launch w020a with pages 77-78
hermes -p "$(cat .agents/prompts/extraction/batch-prompt.txt)" \
  -z "worker_id=w020a start_page=77 end_page=78 output=ste-code/extracted/w020a-p077-078.md"

# Launch w020b with pages 79-80
hermes -p "$(cat .agents/prompts/extraction/batch-prompt.txt)" \
  -z "worker_id=w020b start_page=79 end_page=80 output=ste-code/extracted/w020b-p079-080.md"
```

NOTE: If a split half still fails validation (still truncated at 2 pages),
split again. A 1-page worker is the minimum. If a 1-page worker fails,
flag the page for manual review.

### Step 3: Merge Split Results

After both replacement workers pass validation, merge their output:

```bash
# Concatenate split results into the original worker filename
cat ste-code/extracted/w020a-p077-078.md \
    ste-code/extracted/w020b-p079-080.md \
    > ste-code/extracted/w020-p077-080.md

# Remove the intermediate split files
rm ste-code/extracted/w020a-p077-078.md
rm ste-code/extracted/w020b-p079-080.md
```

### Step 4: Re-Validate Merged Result

Run all 4 checks (Check 1-4) on the merged file. Treat it as a new
single-worker batch. If it passes, update the batch result. If it fails,
check each split half individually for the source of the failure.

## Full-Extraction Validation (After All 109 Workers)

### Coverage Audit

```bash
# Count total unique pages covered
grep -oh "page-[0-9]*" ste-code/extracted/w*-p*.md | sort -u | wc -l
# Should be 434

# Find gaps
for pg in $(seq 1 434); do
  if ! grep -q "page-$(printf '%04d' $pg)" ste-code/extracted/w*-p*.md; then
    echo "MISSING: page $pg"
  fi
done
```

### Content Volume

```bash
# Total extraction size
cat ste-code/extracted/w*-p*.md | wc -c
# Should be >500KB for 434 pages of text

# Dictionary entries
grep -c "^| \*\*" ste-code/extracted/w*-p*.md
# Should be >2000 (875 approved + ~1400 unapproved with examples)
```

### Rule Completeness

```bash
for rule in 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 1.10 1.11 1.12 1.13 1.14 \
            2.1 2.2 2.3 \
            3.1 3.2 3.3 3.4 3.5 3.6 3.7 \
            4.1 4.2 4.3 4.4 \
            5.1 5.2 5.3 5.4 5.5 \
            6.1 6.2 6.3 6.4 6.5 6.6 \
            7.1 7.2 7.3 \
            8.1 8.2 8.3 8.4 8.5 8.6 8.7 \
            9.1 9.2 9.3 9.4; do
  if ! grep -q "Rule $rule" ste-code/extracted/w*-p*.md; then
    echo "MISSING: Rule $rule"
  fi
done
```

## Spot-Check Protocol

For every 10th batch (every 30 workers), run a manual spot-check:

1. Pick a worker's output file at random
2. Pick a page number from that worker's range
3. Read the original spec page directly
4. Compare first 50 lines of worker output vs spec page
5. Check for: exact text match, no paraphrasing, no omission, no fabrication

Record results in `ste-code/validation-log.md`:

```
## Spot-Check: Batch 10 (W028-W030)
- Worker: w028
- Page checked: 111
- Result: PASS — exact match, all 4 pages preserved
- Notes: None
```

## Validation-Log.md Lifecycle

The validation log at `ste-code/validation-log.md` is the canonical record
of all batch and full-extraction validation results. Other agents read this
log to know which workers passed, which failed, and what recovery actions
were taken.

### Format

Every entry follows this structure:

```markdown
## Batch N Validation — YYYY-MM-DD HH:MM

- Workers: wNNN, wNNN, wNNN
- Page range: PPP-ppp
- Result: PASS | FAIL (X/Y workers passed)

### Check 1: File Existence and Size
PASS/FAIL/WARN for each worker

### Check 2: Content Signals
PASS/FAIL for each worker with match counts

### Check 3: Truncation Detection
PASS/FAIL for each worker with last-line excerpt

### Check 4: Fabrication Detection
PASS/FAIL for each worker with notes

### Recovery Actions (if FAIL)
- Worker wNNN failed Check N: split page range and re-extracted as wNNNa, wNNNb
- Replacement result: PASS (wNNNa), PASS (wNNNb)
- Merged result: PASS
```

### Append-Only Rule

The validation log is append-only. Do not delete or rewrite old entries.
When a worker is re-extracted and passes, add a new entry for the
replacement batch. Do not remove the original FAIL entry. This keeps a
complete history of all validation actions.

### Rotation

If `ste-code/validation-log.md` grows past 500 lines, archive the old
entries:

```bash
# Archive old entries before the current extraction run
head -n 500 ste-code/validation-log.md > ste-code/validation-log-archive-1.md
tail -n +501 ste-code/validation-log.md > ste-code/validation-log-current.md
mv ste-code/validation-log-current.md ste-code/validation-log.md
```

Keep all archive files in `ste-code/` with the pattern
`validation-log-archive-N.md`. The current log starts fresh after rotation.

### Consumer Agents

These agents read `ste-code/validation-log.md`:

| Agent | How It Uses the Log |
|-------|-------------------|
| **Agent #3 (Auditor)** | Cross-references validation results against disk evidence. Uses FAIL entries to target its fabrication checks. |
| **Agent #4 (Continuator)** | Reads the most recent batch result to know where to resume. Uses recovery-action entries to skip already-fixed workers. |
| **Agent #1 (Extractor)** | Checks validation log before launching new batches. Does not re-extract pages that already have a PASS entry. |

The continuator (Agent #4) is the primary consumer. When the continuator
runs Stage 3 (Merge) or higher, it reads the validation log to confirm that
all 109 workers passed extraction validation before it proceeds. See
`.agents/skills/continuation/SKILL.md` for the full continuation workflow.

### Quick Status Check

Any agent can get the current validation status with:

```bash
# Count pass/fail batches
grep -c "Result: ALL PASS" ste-code/validation-log.md
grep -c "Result: FAIL" ste-code/validation-log.md

# List workers that failed validation
grep "FAIL w" ste-code/validation-log.md

# Show most recent batch result
grep -A1 "^## Batch" ste-code/validation-log.md | tail -2
```
