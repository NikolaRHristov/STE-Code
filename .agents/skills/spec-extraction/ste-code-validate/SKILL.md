---
name: ste-code-validate
description: "Validate worker extraction quality with per-batch checks and spot-checks against original spec pages."
version: 1.1.0
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

This skill integrates with the extraction orchestrator (`ste-code-workers/SKILL.md`).
The orchestrator launches 3 workers, waits for completion, then hands control to this
validation protocol. If validation passes, the orchestrator proceeds to the next batch.
If validation fails, the recovery procedures in this document run before any new workers
launch.

> **RAILS**: Before any action, validate against `references/rails.md`.
> All 8 rails apply: stage isolation, naming, completion integrity, content fidelity,
> formatting standards, factual correctness, progress tracking, error recovery.

## Cross-Reference: Where Validation Fits

This skill is called from the extraction orchestrator's batch loop. The orchestrator
(`ste-code-workers/SKILL.md`) manages 109 workers in 37 batches of 3. After each batch,
the orchestrator must run per-batch validation before proceeding.

| Document | Relationship |
|----------|-------------|
| `ste-code-workers/SKILL.md` | Orchestrator that calls this validation after each batch |
| `references/rails.md` | 8 guardrails — RAIL 3 (Completion Integrity) and RAIL 4 (Content Fidelity) drive this skill |
| `references/quality-checklist.md` | Printable checklist mirroring Checks 1-4 for manual tracking |
| `references/worker-grid.md` | Worker-to-page-range mapping used by Check 2 and the coverage audit |
| `references/section-types.md` | Content signal expectations per page range |
| `ste-code-workers/references/worker-prompts.md` | Prompt templates — faulty prompts cause validation failures |

## Per-Batch Validation (After Every 3 Workers)

Run after launching and waiting for each batch of 3 workers.

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

## Threshold Rationale

Every numeric threshold in this skill has a specific reason. These values come from
empirical measurement of the 434-page ASD-STE100 Issue 9 spec.

### Line Count Thresholds (Check 1)

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| FAIL | < 30 lines | A 4-page spec extraction produces approximately 100-200 lines. An output under 30 lines means at most 7 lines per page — this is never a valid extraction. 30 is the smallest observed partial output from a context-overflow truncation (worker produced page 1 headers then cut). |
| WARN | 30-79 lines | 30-79 lines could be a valid but thin extraction (front matter pages, appendix pages, or index pages can be sparse). Requires manual inspection. The upper bound of 79 is half of the minimum expected output for a normal 4-page extraction. |
| PASS | ≥ 80 lines | 80+ lines is the baseline for a complete 4-page extraction. The shortest valid 4-page span in the spec (appendix material) produces approximately 85 lines. |

### Dictionary Entry Count (Full-Extraction Check)

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Minimum | > 2000 | The ASD-STE100 Issue 9 dictionary contains 875 approved words plus approximately 1,400 unapproved words with usage examples. The `^| \*\*` pattern matches table-format dictionary entry lines. Fewer than 2,000 matches means at least 275 entries are missing — a gap too large to attribute to formatting variance. |

### Total Extraction Size (Full-Extraction Check)

| Threshold | Value | Rationale |
|-----------|-------|-----------|
| Minimum | > 500 KB | A single spec page produces approximately 1.2-1.5 KB of extracted markdown. 434 pages × 1.2 KB = 520 KB minimum. Content under 500 KB means at least 15 pages are missing or severely truncated. |

### Content Signal Count (Check 2)

| Page Range | Signal | Minimum | Rationale |
|------------|--------|---------|-----------|
| 129-360 | "APPROVED" or "UNAPPROVED" | > 5 | Dictionary pages contain approximately 8-12 approved/unapproved entries each. 4 pages × 8 entries = 32 minimum. Threshold of 5 allows for sparse appendix-adjacent pages while catching empty files. |
| 13-66 | "Section 1" or "Rule 1." | > 1 | These pages describe writing rules. A single mention confirms the file is on-topic. Zero mentions with > 30 lines means the wrong content was extracted. |

## Edge Case Catalog

The standard Checks 1-4 cover normal failure modes. The edge cases below cover
rare but critical failure scenarios. Each includes a detection method and a recovery
procedure.

### E1: Full Batch Failure (All 3 Workers Produce Empty Output)

**Symptom**: All 3 files are missing, empty, or under 10 lines.

**Detection**: Check 1 reports FAIL for all 3 workers in the batch.

**Root causes** (in order of likelihood):
1. `hermes -z` process crashed or was killed during launch
2. Model API returned errors for all 3 requests (rate limit, auth failure, outage)
3. Prompt file was missing or empty at launch time
4. Output directory `ste-code/extracted/` does not exist or is not writable

**Recovery procedure**:
1. Check that `ste-code/extracted/` exists and is writable:
   ```bash
   ls -ld ste-code/extracted/
   touch ste-code/extracted/.write-test && rm ste-code/extracted/.write-test
   ```
2. Check that the prompt file exists and is not empty:
   ```bash
   wc -l .agents/prompts/refine/wNNN.txt
   ```
3. Run a single diagnostic worker on the first page of the failed range:
   ```bash
   hermes -z "Read spec/issue-09-2025/page-XXXX.md. Write first 10 lines to ste-code/extracted/diag-test.md." -m poolside/laguna-s-2.1:free --yolo
   ```
4. If the diagnostic worker succeeds, re-launch the full batch.
5. If the diagnostic worker fails, the problem is systemic (API or environment).
   Do not launch more workers. Log the error and wait for resolution.

### E2: Timeout During Validation

**Symptom**: A validation command (grep, wc, diff) hangs or exceeds 60 seconds.

**Detection**: The validation script blocks. The process monitor shows a stuck command.

**Recovery procedure**:
1. Kill the stuck validation command.
2. Check if the target file is a named pipe or socket instead of a regular file:
   ```bash
   stat -f "%HT" ste-code/extracted/wNNN-p*.md
   ```
3. If the file is not a regular file, delete it and re-extract.
4. If the file is extremely large (> 500 KB for a single worker), the worker
   may have entered an infinite loop. Check the first and last 20 lines. If the
   content repeats, delete the file and re-extract with a fresh prompt.

### E3: File System Errors

**Symptom**: "No space left on device", "Read-only file system", "Permission denied".

**Detection**: Any validation command exits with a non-zero status containing these strings.

**Recovery procedure**:
1. Check available disk space:
   ```bash
   df -h ste-code/extracted/
   ```
2. If disk is full (< 100 MB free), stop all workers. Free space before resuming.
3. Check file permissions:
   ```bash
   ls -la ste-code/extracted/wNNN-p*.md
   ```
4. If permissions are wrong, correct them:
   ```bash
   chmod 644 ste-code/extracted/wNNN-p*.md
   ```

### E4: Worker Produced Output But Content Is Wrong

**Symptom**: File exists, passes size check (> 30 lines, > 80 lines), but content
does not match the expected page range. For example, a worker assigned pages 100-103
produces content from pages 200-203 instead.

**Detection**:
- Check 2 fails: expected content signals are absent.
- The diff against the original spec page shows no overlap.
- The page headers in the output reference wrong page numbers.

**Recovery procedure**:
1. Confirm the content is wrong (not a content signal false negative):
   ```bash
   head -5 ste-code/extracted/wNNN-p*.md
   # Compare page header to expected page range from worker-grid.md
   ```
2. If confirmed wrong: delete the file and re-extract.
3. If the re-extracted file is also wrong: the prompt may contain a wrong page
   reference. Check the prompt file against `references/worker-grid.md`.
4. If the prompt is correct but output is still wrong: the model is misreading
   page references. Add an explicit instruction to the prompt:
   ```
   CONFIRM: you are reading spec/issue-09-2025/page-0100.md through page-0103.md.
   Output the page number in each page header.
   ```

### E5: Fabrication Confirmed

**Symptom**: Check 4 flags fabrication signals AND the diff against the original
page confirms non-matching content.

**Detection**: The diff command in Check 4 shows zero matching lines across the
first 20 lines. Manual inspection confirms commentary or invented content.

**Recovery procedure**:
1. Do NOT attempt to salvage a fabricated file. Fabrication is rarely localized —
   if the first 20 lines are fabricated, the rest of the file is unreliable.
2. Delete the fabricated file immediately.
3. Re-extract the same page range with a hardened prompt. Add this preamble:
   ```
   IMPORTANT: Extract ONLY the text that appears on the spec pages.
   Do not add any commentary, interpretation, or examples not in the source.
   If you are uncertain about a word, leave it blank — do not guess.
   ```
4. Run a spot-check on the re-extracted output before marking the batch complete.
5. If fabrication recurs on the same page range with a hardened prompt, the spec
   page may contain content the model cannot process (scanned image, corrupted text).
   Flag the page for manual extraction and skip it in the automated pipeline.
6. Record the fabrication event in `ste-code/validation-log.md`:
   ```
   ## Fabrication Event — Batch N, Worker wNNN
   - Pages: XXXX-YYYY
   - Signal: "This page describes..." commentary detected
   - Action: deleted, re-extracted with hardened prompt
   - Result after re-extraction: PASS / FAIL (if FAIL, page flagged for manual)
   ```

### E6: Partial Batch Failure (1 or 2 Workers Fail)

**Symptom**: 1 or 2 workers in the batch pass Check 1-4, but the remaining
worker(s) fail.

**Recovery procedure**:
1. Do NOT re-launch the passed workers. Their output is valid.
2. Re-launch ONLY the failed worker(s) using the same prompt.
3. If the re-launched worker fails again, apply the appropriate edge case
   recovery (E1, E4, or E5).
4. If the re-launched worker passes, merge its output into the batch and proceed.

## Recovery Decision Tree

Use this decision tree when a worker fails validation. Check conditions in order.

```
Worker fails validation
│
├─ File does not exist ──────────────────► E1: Full or partial batch failure
│
├─ File exists, < 30 lines
│   ├─ All 3 workers in batch also fail ─► E1: Full batch failure
│   └─ Only this worker fails ───────────► Split page range, re-extract (Check 3 recovery)
│
├─ File exists, 30-79 lines
│   ├─ Content signals match ────────────► WARN: flag for manual review, proceed
│   └─ Content signals absent ───────────► E4: Wrong content recovery
│
├─ File exists, ≥ 80 lines
│   ├─ Content signals match
│   │   ├─ Truncation check passes ──────► PASS
│   │   └─ Truncation check fails ───────► Split page range, re-extract (Check 3 recovery)
│   └─ Content signals absent ───────────► E4: Wrong content recovery
│
├─ Fabrication signals detected
│   ├─ Diff confirms fabricated ─────────► E5: Fabrication confirmed
│   └─ Diff shows partial match ─────────► Flag for spot-check, proceed with caution
│
└─ Validation command hangs ─────────────► E2: Timeout during validation
```

## Known Limitations

This section documents the inherent limits of the validation protocol. Operators
must understand these limits to interpret validation results correctly.

### L1: Grep-Based Content Signal Check Can Produce False Negatives

The Check 2 content signal scan uses grep to match literal strings. This approach
fails when:

- The spec uses variant formatting for the expected signal. For example, "APPROVED"
  might appear as "Approved" in some dictionary entries (case-sensitive grep).
- The worker extracted correct content but used unexpected markdown formatting.
  For example, "Section 1" might appear as `**Section 1**` in the worker output,
  which grep matches, but "Rule 1." embedded in a table cell could be missed if
  the grep pattern assumes a line-start anchor.
- Page ranges near section boundaries (pages 64-67) may contain signals from two
  different expected sets, diluting the count for any single signal.

**Mitigation**: When Check 2 fails but the file size is > 80 lines, run a manual
inspection before marking the worker as FAIL. Use `head -30` and `tail -30` to
visually confirm the content type.

### L2: Fabrication Detection Cannot Catch Subtle Paraphrasing

Check 4 detects overt fabrication (commentary language, modern terms, missing
boilerplate). It cannot detect:

- Subtle paraphrasing: the worker rewrites spec sentences in its own words while
  keeping the same meaning. This passes the content signal check and the diff
  command (if using fuzzy matching).
- Semantic drift: the worker changes a rule from "Use approved words" to "Use
  only the approved words" — a small addition that changes the rule's strictness.
- Omission of qualifiers: the worker drops conditional phrases like "when possible"
  or "unless specified otherwise" from rule text.

**Mitigation**: The spot-check protocol (every 10th batch) is the primary defense
against subtle fabrication. For high-risk page ranges (writing rules, Section 1-5),
increase spot-check frequency to every 5th batch.

### L3: Truncation Check Only Examines Last 3 Lines

Check 3 looks at the last 3 lines for clean termination. A worker can produce a
valid-looking ending (page footer present, sentence ends with period) while still
having dropped content from the middle pages.

**Mitigation**: The coverage audit (full-extraction validation) catches mid-file
gaps by counting unique page references. A worker that drops page 2 of 4 will have
a gap in the page sequence.

### L4: Thresholds Are Calibrated for ASD-STE100 Issue 9

All numeric thresholds (30 lines, 80 lines, 500 KB, 2000 dictionary entries) are
calibrated against the 434-page ASD-STE100 Issue 9 specification dated 2025-01-15.
If the source specification changes (different edition, different page count,
different formatting), all thresholds must be recalibrated.

**Mitigation**: Before applying this validation protocol to a new specification,
extract 3 sample page ranges and measure the output characteristics. Adjust
thresholds based on the sample measurements.

### L5: Validation Does Not Check Semantic Correctness

All checks in this protocol operate on structural and signal-level properties
(file size, line count, string presence). None verify that Rule 5.1's text is
semantically correct — only that the string "Rule 5.1" appears in the output.

**Mitigation**: The downstream refinement stage (`ste-code-refine/SKILL.md`) and
adaptation stage (`ste-code-adaptation/SKILL.md`) include their own correctness
checks. Validation ensures the raw material is present and not obviously wrong.
Correction of content errors happens in later stages.

## Validation Log Entry Format

Record all validation results in `ste-code/validation-log.md`. Use this format
for normal batches and edge cases.

### Normal Batch Entry

```
## Batch N — Workers wNNN-wNNN (Pages XXXX-YYYY)
- Date: YYYY-MM-DD HH:MM
- Check 1 (Size):       PASS — wNNN (142L/8.1K), wNNN (138L/7.9K), wNNN (151L/8.4K)
- Check 2 (Signals):    PASS — all 3 workers match expected page range signals
- Check 3 (Truncation): PASS — all 3 workers end cleanly
- Check 4 (Fabrication): PASS — no fabrication signals detected
- Spot-check:           N/A (not a spot-check batch)
- Status:               BATCH COMPLETE
```

### Edge Case Entry

```
## E5 Fabrication — Batch N, Worker wNNN
- Date: YYYY-MM-DD HH:MM
- Detection: Check 4 flagged "This page describes..." in line 12
- Confirmation: diff against spec/page-XXXX.md shows 0/20 lines match
- Action: deleted file, re-extracted with hardened prompt
- Re-extraction result: PASS (148L/8.2K, all 4 checks pass)
- Resolution time: 3 minutes
```

### Spot-Check Entry

```
## Spot-Check: Batch 10 (W028-W030)
- Worker: w028
- Page checked: 111
- Result: PASS — exact match, all 4 pages preserved
- Notes: None
```

---

## Quick Reference Card

```
┌──────────────────────────────────────────────────────────┐
│ VALIDATION QUICK REFERENCE                               │
├──────────────────────────────────────────────────────────┤
│ PER BATCH (every 3 workers):                             │
│   Check 1: File exists? > 30L?                           │
│   Check 2: Expected signals present?                     │
│   Check 3: Last 3 lines end cleanly?                     │
│   Check 4: No fabrication signals?                       │
│                                                          │
│ IF FAIL: follow Recovery Decision Tree                   │
│                                                          │
│ EVERY 10TH BATCH (spot-check):                           │
│   + manual diff against original spec page               │
│                                                          │
│ AFTER ALL 109 WORKERS:                                   │
│   Coverage: all 434 pages present?                       │
│   Volume:   total > 500KB? entries > 2000?               │
│   Rules:    all 57 rules referenced?                     │
│                                                          │
│ EDGE CASES:                                              │
│   E1: Full batch failure → diagnostic worker             │
│   E2: Timeout → check file type, delete if corrupt       │
│   E3: File system error → check disk, permissions        │
│   E4: Wrong content → delete, check prompt               │
│   E5: Fabrication → delete, hardened prompt              │
│   E6: Partial failure → re-launch failed only            │
│                                                          │
│ LOG: ste-code/validation-log.md                          │
└──────────────────────────────────────────────────────────┘
```
