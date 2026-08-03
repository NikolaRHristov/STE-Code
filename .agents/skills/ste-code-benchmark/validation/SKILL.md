---
name: validation
description: > **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
category: benchmark
capability: running-the-adversarial-benchmark
source: .agents/skills/validation
layout: ste-code-canonical-v1
---

# STE-Code Validation Protocol

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to
> THIS skill. One session = one operation = one read + one write. No re-editing
> own output.

## Overview

> **RAILS**: Validate every action against `references/rails.md` — 8 immutable
> guardrails.

Systematic validation of worker extraction output. Run after each batch (every 3
workers) and after the full merge. Catches fabrication, truncation, and
incompleteness.

> **RAILS**: Before any action, validate against . All 8 rails apply: stage
> isolation, naming, completion integrity, content fidelity, formatting
> standards, factual correctness, progress tracking, error recovery.

## Severity Levels: PASS, WARN, and FAIL

Each check in the validation protocol assigns one of three severity levels. Know
what each level means and what action it requires.

### PASS

The check found no problems. The worker output meets all criteria. Continue to
the next check. No action is necessary.

### WARN

The check found a possible problem that is not severe enough to block the batch.
A WARN result means these things:

- The file is smaller than the ideal threshold but not empty (30-79 lines for
  Check 1).
- The content signals match count is close to the boundary (3-5 matches for a
  zone that expects 6+).
- The last line does not end with a page footer but does end with a complete
  sentence.

**Action for WARN**: Record the warning in `ste-code/validation-log.md`. Mark
the batch as PASS with warnings. Flag the worker for manual review during the
spot-check rotation. If the same worker gets 2 or more WARN results across
different batches (for example, a split half that stays at WARN after
re-extraction), promote the WARN to FAIL and re-extract.

### FAIL

The check found a definite problem. The worker output is not usable. A FAIL
result means these things:

- The file is missing or has fewer than 30 lines (empty extraction).
- The content signals match count is 0 or only generic keywords appear.
- The last line is truncated mid-word or mid-sentence with no page footer.
- Fabrication flags appear: modern software terms, commentary language, missing
  spec boilerplate.

**Action for FAIL**: Stop the batch. Record the failure in
`ste-code/validation-log.md`. Start the re-extraction procedure for the failed
worker. Do not launch the next batch until the failed worker is replaced and the
batch result shows all PASS.

## Worked Example — Batch Validation Output

This section shows real output from a batch validation run. Use these patterns
to know what PASS, WARN, and FAIL results look like.

### Example: Batch 4 (w010-w012) — All Passing

```
Batch 4 Validation (w010-w012, pages 37-48)

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

Batch 4 Result: ALL PASS
```

### Example: Batch 7 (w019-w021) — Mixed Results

```
Batch 7 Validation (w019-w021, pages 73-84)

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

Batch 7 Result: 1 FAIL (w020), 2 PASS
Action: Split w020 page range (77-80) into two halves and re-extract.
See "Re-Extraction Procedure" below.
```

### Example: Batch 12 (w034-w036) — WARN Result

This example shows a WARN result. The worker output is usable but has a minor
problem. The batch continues after recording the warning.

```
Batch 12 Validation (w034-w036, pages 133-144)

--- Check 1: File Existence and Size ---
PASS w034: 192 lines, 13801 bytes
WARN w035: 58 lines — may be light content (check manually)
PASS w036: 201 lines, 15102 bytes

--- Check 2: Content Signals ---
w034: 19 matches (APPROVED, UNAPPROVED, Word) — PASS
w035: 4 matches (APPROVED) — WARN (expected Section 4/5 or Dictionary zone, low match count)
w036: 22 matches (APPROVED, UNAPPROVED, Part 2) — PASS

--- Check 3: Truncation Detection ---
w034: "Page 136\n2025-01-15\nIssue 9" — PASS
w035: "Refer to the dictionary for approved words.\nPage 140\n2025-01-15" — PASS (clean footer)
w036: "Page 144\n2025-01-15\nIssue 9" — PASS

--- Check 4: Fabrication Detection ---
w034: no fabrication flags — PASS
w035: no fabrication flags — PASS
w036: no fabrication flags — PASS

Batch 12 Result: ALL PASS (1 WARN: w035)
Action: Flag w035 for spot-check review. No re-extraction needed.
```

## Per-Batch Validation (After Every 3 Workers)

Run after launching and waiting for each batch of 3 workers.

### Edge Case: Remainder Batches (Fewer Than 3 Workers)

The last batch of the pipeline may contain 1 or 2 workers. Also, a failed worker
replacement may run solo. Handle these cases:

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

When a worker page range crosses two content-signal zones (refer to the Content
Signals table in Check 2), the worker must match signals from both zones. The
check uses an OR condition:

- If page range crosses 64-67 (Section 1 → Section 4 boundary), the worker must
  show at least one signal from BOTH sides. For example, a worker with pages
  62-69 must match "Rule 1." AND "Section 4".
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

#### Edge Case: Triple-Boundary Workers

A 4-page worker that spans pages 64-67 crosses BOTH the Section 1→Section 4
boundary AND the Section 4→Section 5 boundary in a single range. This is rare
but possible with the 4-page granularity.

When a worker page range covers three zones, the content signal check must match
at least one signal from EACH of the three zones. For example, a worker with
pages 64-67 must show:

- At least one signal from the Section 1 zone (pages 13-66): "Rule 1.", "Part 1"
- At least one signal from the Section 4 zone (pages 67-128): "Section 4", "Rule
  4."
- At least one signal from the Section 5 zone (pages within 67-128, after
  Section 4): "Section 5", "Rule 5."

If the worker matches only two of three zones, assign a WARN. If it matches only
one zone, assign a FAIL. Triple-boundary workers are high-risk for truncation.
Prioritize them for spot-checks.

#### Edge Case: Content Signal False Positives

A content signal check can show a false positive when these conditions are true:

- The worker output contains the expected signal string but in a wrong context.
  For example, "Section 1" appears in a cross-reference ("Refer to Section 1")
  instead of as a section heading.
- The signal count is high but all matches come from the same source line
  repeated in a table of contents or index.

To detect false positives:

```bash
# Check uniqueness of signal matches — each match should come from a different line
grep -n "Section 1\|Rule 1\." ste-code/extracted/wNNN-p*.md | cut -d: -f1 | sort -u | wc -l
# If unique_line_count < total_match_count / 2, suspect false positive
```

A false positive that inflates the match count does not automatically fail the
worker. If the other checks (1, 3, 4) all pass and the file has reasonable size,
mark the worker as PASS with a note about the signal quality.

### Edge Case: Cascading Failures in a Single Batch

When 2 or 3 workers in the same batch fail validation, do not re-extract all of
them in parallel. A cascading failure often points to a systemic problem:

- **API rate limiting**: The batch launch exceeded the model provider rate
  limit. All workers in the batch got truncated or empty responses.
- **Prompt corruption**: The batch prompt file had an error. All workers
  received the same bad instructions.
- **Source page corruption**: The source spec pages for this range have encoding
  problems or are missing.

**Procedure for cascading failures (2+ FAIL in one batch)**:

1. Stop. Do not launch replacement workers yet.
2. Check the source pages on disk:
    ```bash
    # Verify source pages exist and have content
    for pg in $(seq START END); do
    	f="spec/issue-09-2025/page-$(printf '%04d' $pg).md"
    	[ -f "$f" ] && echo "OK: $f ($(wc -l < "$f") lines)" || echo "MISSING: $f"
    done
    ```
3. Check the batch prompt file for corruption:
    ```bash
    wc -l .agents/prompts/extraction/batch-prompt.txt
    # Should be >10 lines. If empty or truncated, restore from git.
    ```
4. If source pages and prompt are correct, wait 60 seconds for rate limit
   recovery. Then re-extract each failed worker one at a time, not in parallel.
5. If source pages are missing or the prompt is corrupted, fix the root cause
   first. Do not re-extract until the systemic problem is resolved.
6. Record the cascading failure in `ste-code/validation-log.md` with a `CASCADE`
   marker so the auditor knows to investigate the root cause.

## Content Signal Reference Table

Verify the file contains expected markers for its page range:

| Page Range | Zone         | Expected Content Signal                                              |
| ---------- | ------------ | -------------------------------------------------------------------- |
| 1-12       | Front Matter | "Copyright", "Highlights", "ASD-STE100 Simplified Technical English" |
| 13-66      | Section 1    | "Section 1", "Rule 1.", "Part 1"                                     |
| 67-128     | Sections 4-9 | "Section 4", "Section 5", "Rule 5.", "WARNING"                       |
| 129-360    | Dictionary   | "Part 2", "Dictionary", "Word", "APPROVED", "UNAPPROVED"             |
| 361-434    | Appendix     | "Appendix", "Index", "Issue", "Change"                               |

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

```bash
# Example: check a dictionary-range worker
grep -c "APPROVED\|UNAPPROVED" ste-code/extracted/wNNN-p*.md
# Should be >5 for dictionary pages
```

### Check 3: Truncation Detection

The most common failure mode: worker context fills up and output is cut
mid-sentence.

```bash
# Last 3 lines of output should end cleanly (period, page footer, or table row)
tail -3 ste-code/extracted/wNNN-p*.md
```

Red flags:

- Last line ends mid-word ("The procedure for remo")
- Last line is a partial table row
- No page footer on last page ("2025-01-15", "Issue 9", "Page NNN")

If truncated, split the worker's page range in half and re-extract both halves.

#### Truncation Recovery: When Re-Extraction Fails Repeatedly

A worker that fails truncation checks after two rounds of re-extraction
(original → 2 halves → 4 quarters) signals one of these problems:

- The page content is too dense for the model context window at any split size.
- The source page has a very large table or code block that cannot fit.
- The model consistently drops content at the same position.

**Escalation path for persistent truncation**:

1. After the second re-extraction failure (4 split workers), stop splitting.
2. Flag the page for manual extraction. Write a `MANUAL` entry to
   `ste-code/validation-log.md` with the page number and the reason.
3. Extract the page content yourself using `read_file` and write it directly to
   the expected output file path. This bypasses the model context limit.
4. After manual extraction, run all 4 checks on the manually written file.
   Record the result as `PASS (MANUAL)` in the validation log.
5. Continue the batch pipeline. Manual extraction entries do not block the next
   batch launch.

```
## Manual Extraction — YYYY-MM-DD HH:MM
- Page: 77
- Reason: Persistent truncation after 2 re-extraction rounds (4 split workers all truncated)
- Action: Manual extraction via read_file + write_file
- Result: PASS (MANUAL)
```

### Check 4: Fabrication Detection

Fabricated output shows these patterns:

- Modern software examples in spec extraction ("React", "Docker" in page
  content)
- Commentary language ("This page describes...", "The key point is...")
- Missing spec boilerplate (no "ASD-STE100 Simplified Technical English" header)
- Smooth, flowing prose instead of spec's terse rule format

If fabrication suspected, compare against original page:

```bash
diff <(head -20 spec/issue-09-2025/page-NNNN.md) <(head -20 ste-code/extracted/wNNN-p*.md)
```

## Re-Extraction Procedure (Truncation and Fabrication Recovery)

When a worker fails validation (truncation, fabrication, or missing file),
follow this procedure to replace the worker output. For full orchestration of
multi-agent re-extraction workflows including continuation and error recovery,
refer to `.agents/skills/continuation/SKILL.md`.

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

#### Minimum Split Size

A 1-page worker is the minimum split size. If a 2-page worker fails truncation
checks, split it into two 1-page workers. If a 1-page worker fails, do not split
further. Flag the page for manual extraction instead. See "Truncation Recovery:
When Re-Extraction Fails Repeatedly" above.

#### Split Size Calculator

Use this shell function to compute split ranges:

```bash
split_range() {
	# Usage: split_range START END
	# Outputs: HALF1_START HALF1_END HALF2_START HALF2_END
	local start=$1 end=$2 total=$((end - start + 1))
	local half=$((total / 2))
	local half1_end=$((start + half - 1))
	local half2_start=$((half1_end + 1))
	if [ $((total % 2)) -eq 1 ]; then
		half1_end=$((half1_end + 1))
		half2_start=$((half2_start + 1))
	fi
	echo "$start $half1_end $half2_start $end"
}
```

### Step 2: Launch Replacement Workers

Use new worker IDs to avoid overwriting the failed output. Append a split suffix
to the original worker ID:

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

#### Race Condition: Next Batch Launch During Re-Extraction

Do not launch the next batch (for example, Batch 8) while re-extraction workers
for Batch 7 are still running. This prevents these problems:

- Output file name collisions if the replacement worker uses a suffix that
  matches a future batch worker ID.
- Validation log confusion when entries from two different batch contexts
  interleave.
- Rate limit exhaustion from too many concurrent worker launches.

**Procedure**:

1. Mark the current batch as BLOCKED in `ste-code/validation-log.md`.
2. Wait for ALL re-extraction workers to finish.
3. Validate the replacement outputs.
4. Mark the batch as RECOVERED.
5. Then launch the next batch.

```
## Batch 7 Recovery — YYYY-MM-DD HH:MM
- Status: BLOCKED (re-extraction in progress)
- Failed worker: w020 (pages 77-80)
- Replacement workers: w020a (pages 77-78), w020b (pages 79-80)
- Replacement workers launched at HH:MM. Waiting for completion.

## Batch 7 Recovery — YYYY-MM-DD HH:MM
- Status: RECOVERED
- w020a: PASS (all 4 checks)
- w020b: PASS (all 4 checks)
- Merged result: w020-p077-080.md — PASS (all 4 checks)
- Next batch (Batch 8) can now launch.
```

#### Re-Extraction Worker Naming Convention

When a split half fails again and needs a second split, use the naming scheme:

| Round                   | Original | Split Workers   |
| ----------------------- | -------- | --------------- |
| 1st split               | w020     | w020a, w020b    |
| 2nd split (w020a fails) | w020a    | w020a1, w020a2  |
| 3rd split               | —        | FLAG FOR MANUAL |

Do not go deeper than 2 levels of suffix. A worker ID like `w020a1b2` is too
complex. After two split rounds, escalate to manual extraction.

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

Run all 4 checks (Check 1-4) on the merged file. Treat it as a new single-worker
batch. If it passes, update the batch result. If it fails, check each split half
individually for the source of the failure.

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

### Spot-Check Targeting

Prioritize these workers for spot-checks:

1. Workers flagged with WARN in any check during batch validation.
2. Workers whose page range crosses a content-signal zone boundary.
3. Workers that were re-extracted (split and merged). Spot-check at least one
   split half before grouping.
4. The first worker of each new content-signal zone (w001 for pages 1-4, w004
   for pages 13-16, w017 for pages 67-70, w033 for pages 129-132, w091 for pages
   361-364). These workers sit at zone transitions and are most likely to have
   content signal mismatches.

### Spot-Check Failure Response

If a spot-check finds fabrication or content mismatch in a worker that passed
batch validation:

1. Mark the worker as FAIL in the validation log with a `SPOT-FAIL` marker.
2. Re-extract the worker using the procedure above.
3. After re-extraction, spot-check the replacement again.
4. If the replacement also fails spot-check, flag the page range for manual
   extraction.
5. Audit the previous batch validation to understand why Check 4 (fabrication
   detection) did not catch the problem.

## Validation-Log.md Lifecycle

The validation log at `ste-code/validation-log.md` is the canonical record of
all batch and full-extraction validation results. Other agents read this log to
know which workers passed, which failed, and what recovery actions were taken.

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

#### Worked Example: Complete Log Entry for a FAIL with Recovery

This example shows a real validation log entry for Batch 7 (from the worked
example above) with the full recovery cycle recorded.

```markdown
## Batch 7 Validation — 2025-07-30 14:22

- Workers: w019, w020, w021
- Page range: 73-84
- Result: FAIL (2/3 workers passed)

### Check 1: File Existence and Size

PASS w019: 201 lines, 14823 bytes FAIL w020: only 24 lines — possible truncation
or empty extraction PASS w021: 192 lines, 13901 bytes

### Check 2: Content Signals

w019: 14 matches (Section 4, Section 5) — PASS w020: 1 match (APPROVED) — FAIL
(0 section signals for expected Section 4/5 zone) w021: 12 matches (Section 5,
Rule 5.) — PASS

### Check 3: Truncation Detection

w019: "Page 76\n2025-01-15\nIssue 9" — PASS w020: "The procedure for remo" —
FAIL (truncated mid-word, no page footer) w021: "Page 84\n2025-01-15\nIssue 9" —
PASS

### Check 4: Fabrication Detection

w019: no fabrication flags — PASS w020: SKIP (too few lines for fabrication
check) w021: no fabrication flags — PASS

### Recovery Actions

- Worker w020 (pages 77-80) failed Check 1, Check 2, Check 3
- Action: Split page range 77-80 into two halves
    - w020a: pages 77-78
    - w020b: pages 79-80
- Replacement workers launched at 14:24

## Batch 7 Recovery — 2025-07-30 14:27

- Status: RECOVERED
- w020a (pages 77-78): PASS — 112 lines, 8145 bytes, 6 content signals, clean
  footer
- w020b (pages 79-80): PASS — 108 lines, 7902 bytes, 5 content signals, clean
  footer
- Merged result (w020-p077-080.md): PASS — 220 lines, 16047 bytes, all 4 checks
- Original w020 output (24 lines) preserved at
  ste-code/extracted/w020-p077-080.md.failed
- Batch 7 final result: ALL PASS (3/3 after recovery)
- Next batch (Batch 8, w022-w024) cleared to launch.
```

### Append-Only Rule

The validation log is append-only. Do not delete or rewrite old entries. When a
worker is re-extracted and passes, add a new entry for the replacement batch. Do
not remove the original FAIL entry. This keeps a complete history of all
validation actions.

#### Preserving Failed Output

When a worker fails validation, do not delete the failed output file. Rename it
with a `.failed` suffix:

```bash
mv ste-code/extracted/w020-p077-080.md ste-code/extracted/w020-p077-080.md.failed
```

This keeps the failed output for the auditor to examine. The auditor uses failed
output files to detect patterns in fabrication or truncation. If you delete the
failed output, the auditor cannot learn from the failure.

### Rotation

If `ste-code/validation-log.md` grows past 500 lines, archive the old entries:

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

| Agent                      | How It Uses the Log                                                                                                     |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| **Agent #3 (Auditor)**     | Cross-references validation results against disk evidence. Uses FAIL entries to target its fabrication checks.          |
| **Agent #4 (Continuator)** | Reads the most recent batch result to know where to resume. Uses recovery-action entries to skip already-fixed workers. |
| **Agent #1 (Extractor)**   | Checks validation log before launching new batches. Does not re-extract pages that already have a PASS entry.           |

The continuator (Agent #4) is the primary consumer. When the continuator runs
Stage 3 (Merge) or higher, it reads the validation log to confirm that all 109
workers passed extraction validation before it proceeds. See
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

## Integration with Continuation Skill

The validation skill and the continuation skill work together across the
pipeline. Here is how they connect.

### Stage Gate: Extraction → Refinement

Before the continuator starts Stage 2 (Refinement), it reads the validation log
to confirm these conditions:

```bash
# Check: all 109 workers have a PASS entry (including recovered workers)
grep -c "ALL PASS" ste-code/validation-log.md
# Should equal the number of batches launched (37 for 109 workers, fewer if remainder batches)

# Check: no unrecovered FAIL entries
grep "Result: FAIL" ste-code/validation-log.md | grep -v "RECOVERED"
# Should be empty
```

If unrecovered FAIL entries exist, the continuator does NOT start Stage 2. It
reports the blocked stage and waits for the extractor (Agent #1) to resolve the
failures.

### Progress Synchronization

The continuator uses the validation log to build a worker completion map:

```
Batch 1: PASS (w001, w002, w003)          ✓
Batch 2: PASS (w004, w005, w006)          ✓
...
Batch 7: FAIL → RECOVERED (w019, w020→w020a+w020b, w021)  ✓
...
Batch 37: (not yet in log)                ✗
```

This map tells the continuator exactly which page ranges are complete and which
stages can proceed. Without the validation log, the continuator must re-inspect
all 109 output files, which duplicates work.

### State File Updates

After each batch validation, update the pipeline state file:

```bash
# ste-code/state/extraction-state.md
echo "## Batch 7 — $(date '+%Y-%m-%d %H:%M')" >> ste-code/state/extraction-state.md
echo "- Status: VALIDATED" >> ste-code/state/extraction-state.md
echo "- Workers: w019 (PASS), w020 (RECOVERED via w020a+w020b), w021 (PASS)" >> ste-code/state/extraction-state.md
```

The continuator reads `ste-code/state/extraction-state.md` as a fast index. It
does not need to parse the full validation log for every stage check.

## End-to-End Validation Lifecycle

This section shows the complete lifecycle of validation from batch launch
through final extraction sign-off. Use it as a checklist.

### Phase 1: Per-Batch (After Each 3-Worker Batch)

1. Wait for all 3 workers to finish producing output files.
2. Run Check 1: Confirm each file exists and has >30 lines.
3. Run Check 2: Confirm content signals match the expected zone.
4. Run Check 3: Confirm the last 3 lines end cleanly.
5. Run Check 4: Scan for fabrication flags (commentary, modern terms).
6. Assign PASS, WARN, or FAIL for each worker.
7. Write the batch result to `ste-code/validation-log.md`.
8. If all workers PASS (or PASS with WARN), launch the next batch.
9. If any worker FAILS, start the re-extraction procedure. Block the next batch.
10. After re-extraction and merge, re-validate. Mark RECOVERED. Launch the next
    batch.

### Phase 2: Spot-Check (Every 10th Batch)

1. After Batch 10, 20, 30, select at least one worker for spot-check.
2. Prioritize WARN-flagged workers, boundary-crossing workers, and re-extracted
   workers.
3. Compare the worker output against the original spec page.
4. Record the spot-check result in `ste-code/validation-log.md`.
5. If spot-check finds a problem, re-extract and re-validate.

### Phase 3: Full Extraction Sign-Off (After All 109 Workers)

1. Run the coverage audit: confirm 434 pages are covered.
2. Run the content volume check: confirm >500KB total.
3. Run the rule completeness check: confirm all 53 rules are present.
4. Count PASS vs FAIL in the validation log. All entries must show PASS or
   RECOVERED.
5. Write the final sign-off entry to `ste-code/validation-log.md`:

```markdown
## Full Extraction Validation — YYYY-MM-DD HH:MM

- Coverage: 434/434 pages ✓
- Content volume: 612384 bytes (>500KB threshold) ✓
- Rule completeness: 53/53 rules present ✓
- Batch validation: 37/37 batches VALIDATED (0 unrecovered FAIL) ✓
- Spot-checks: 4/4 spot-checks passed ✓
- Manual extractions: 2 pages (flagged as MANUAL) ✓

### Sign-Off

Stage 1 (Extraction) is complete. All 109 workers produced valid output. The
validation log at ste-code/validation-log.md is the canonical record. Stage 2
(Refinement) can begin.
```

### Phase 4: Continuous Validation (During Stages 2-5)

Even after Stage 1 completes, the validation log continues to be used:

- **Stage 2 (Refinement)**: The continuator reads the validation log as a gate
  before starting refinement. No new extraction validation runs.
- **Stage 3 (Merge)**: The continuator validates the merged output against the
  extraction validation log entries. It checks that no page content was lost
  during concatenation.
- **Stage 4 (Adaptation)**: The auditor reads the validation log to target
  fabrication checks on workers that had WARN or RECOVERED markers.
- **Stage 5 (Artifacts)**: The final artifact quality gate cross-references the
  validation log to confirm all source material passed extraction checks.
