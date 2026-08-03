# Per-Batch Quality Checklist

> Run after each batch of 3 workers completes.
> Check off items before launching the next batch.

## Cross-References

This checklist works with three companion documents. Read them before you start:

| Reference | Path | What It Provides |
|-----------|------|------------------|
| Section Types | `.agents/references/section-types.md` | Page range to content type mapping, per-type extraction prompts, size expectations |
| Extraction SKILL | `.agents/skills/extraction/SKILL.md` | Worker launch protocol, 109-worker grid, batch serialization rules |
| Progress State | `.agents/state/PROGRESS.md` | Batch completion markers, blocked/degraded flags, pipeline state machine |

## Pre-Flight Requirements

Before you run this checklist on a batch, make sure these conditions are true:

- [ ] The batch has been launched. All 3 workers have exited.
- [ ] The output directory `ste-code/extracted/` is accessible.
- [ ] The `shuf` command is available (coreutils; included with macOS).
- [ ] You know the page range for each worker in the batch. Get this from `.agents/references/worker-grid.md`.

## Section-Type Size Thresholds

Different section types produce different file sizes. A single threshold causes false positives and false negatives. Use these per-type thresholds instead:

| Section Type | Pages | Threshold | Rationale |
|-------------|-------|-----------|-----------|
| FRONT | 1-12 | > 2 KB | Sparse pages. Large centered text blocks produce small output. A 4-page front matter extraction at 1.8 KB can be correct. |
| TOC | 13-16 | > 2 KB | Multi-column reference pages. Low text density. |
| INDEX | 17-24 | > 3 KB | Dense subject-to-rule tables. Moderate output size. |
| INTRO | 25-42 | > 3 KB | Narrative prose. Q&A format generates moderate output. |
| RULES | 43-128 | > 5 KB | Dense content. Rule statements, example pairs, and explanatory text. This is the highest-value content. The threshold is higher. |
| CATEGORIES | 47-66 | > 4 KB | Numbered lists with descriptions. Moderate density. |
| DICT | 129-360 | > 8 KB | Very dense. Four-column layout. Every entry contains word, POS, status, meaning, forms, alternatives, and examples. The threshold is highest. |
| APPENDIX | 361-434 | > 3 KB | Mixed content. Change history tables, flowcharts, index. Variable density. |

NOTE: The last batch (Batch 37, W109) contains only 2 pages. All thresholds for a 2-page worker are half the 4-page threshold. For W109, use the APPENDIX threshold at > 1.5 KB.

Determine the section type for each worker from `.agents/references/section-types.md`. Use the page range lookup table at the bottom of that file. Then apply the correct threshold from this table.

## Batch __ (Workers W___ through W___)

### Section-Type Identification (do this first)

Look up each worker's page range in `.agents/references/section-types.md` (Page Range Reference table):

- [ ] W___ covers pages ______ (type: ______, threshold: > ___ KB)
- [ ] W___ covers pages ______ (type: ______, threshold: > ___ KB)
- [ ] W___ covers pages ______ (type: ______, threshold: > ___ KB)

If a worker page range crosses a section boundary, use the higher threshold. For example, a worker covering pages 125-128 (RULES) plus pages 129-132 (DICT) uses the DICT threshold (> 8 KB).

### File Integrity

- [ ] All 3 output files exist in `ste-code/extracted/`
- [ ] File sizes: W___ (___KB), W___ (___KB), W___ (___KB)
- [ ] Each size exceeds its section-type threshold (see table above)

### Truncation Check

- [ ] W___ last 3 lines end cleanly
- [ ] W___ last 3 lines end cleanly
- [ ] W___ last 3 lines end cleanly

Red flags (if ANY checked, re-extract):
- [ ] Last line ends mid-word
- [ ] Last line is partial table row (single `|`)
- [ ] No page footer on last page extracted ("Issue 9", "2025-01-15", "Page NNN")

### Content Signals (spot-check with `shuf`)

Use the automated spot-check procedure. Do not pick lines by hand.

**Procedure for each worker file:**

```bash
# Step 1: Sample 3 random non-blank lines
FILE="ste-code/extracted/wNNN-pPPPP-PPPP.md"
shuf -n 50 "$FILE" | grep -v '^$' | head -n 3
```

**Why 50 before filtering:** `shuf -n 3` on the raw file often returns blank lines. Sampling 50 and filtering blanks guarantees 3 meaningful lines.

**Step 2:** Check each sampled line against the expected content signals for the section type. See the Signal Reference Table below.

**Step 3:** Evaluate the result:
- 3 of 3 lines match expected signals → PASS
- 2 of 3 lines match → PASS (WARN if the line count is also low)
- 1 of 3 lines match → Expand with 5 more lines. If 3+ of 8 total match → PASS with WARN. If fewer than 3 of 8 match → FAIL.
- 0 of 3 lines match → FAIL immediately. Do not expand.

If any sampled line is a header or footer boilerplate ("ASD-STE100 Simplified Technical English", "Issue 9", "2025-01-15"), count it as a structural signal match. These lines are valid content signals for all section types.

**Signal Reference Table:**

| Section Type | Expected Signals |
|-------------|-----------------|
| FRONT | "Copyright", "Highlights", "ASD-STE100 Simplified Technical English", "Special Usage Rights", "Disclaimer" |
| TOC | "Rule", "Section", page number references (digits following a topic) |
| INDEX | Subject-to-rule mappings, "Rule" with numbers, category names |
| INTRO | "Introduction", "How to use", "Q:", "Reference Documents", "Issue 9" |
| RULES | "Rule" followed by number (e.g., "Rule 1.1"), "STE:" and "Non-STE:" example pairs, "Section" headings |
| CATEGORIES | "Category" followed by number, numbered lists with descriptions, "Examples:" |
| DICT | "APPROVED", "UNAPPROVED", "Word (POS)", part-of-speech abbreviations (n., v., adj., adv., prep., conj.) |
| APPENDIX | "Appendix", "Index", "Change History", "Issue", "Flowchart", "Change Form" |

**Boundary-crossing page ranges:** If a worker covers pages from two content-signal zones (for example, pages 125-132 crosses RULES→DICT), the spot-check must find at least one signal from each zone across the 3 sampled lines. If signals from only one zone appear, expand to 8 lines. If still only one zone detected, assign a FAIL. See `.agents/skills/validation/SKILL.md` (Boundary-Crossing Page Ranges section) for the full protocol.

- [ ] W___ spot-check result: ___ (PASS / WARN / FAIL)
- [ ] W___ spot-check result: ___ (PASS / WARN / FAIL)
- [ ] W___ spot-check result: ___ (PASS / WARN / FAIL)

### Content Header and Footer Check

- [ ] "ASD-STE100 Simplified Technical English" header present in at least one file of the batch (FRONT sections require it. For RULES/DICT/APPENDIX sections, it may only appear on first pages.)
- [ ] Page footers present ("Issue 9", "2025-01-15") on final page of each file
- [ ] Expected content type matches page range (verify with `.agents/references/section-types.md` Page Range Reference table)

### Fabrication Detection

- [ ] No modern software terms in spec text ("React", "Docker", "API", "npm", "async/await", "git", "JSON")
- [ ] No commentary language ("This page describes...", "The key point is...", "In summary...", "Essentially...")
- [ ] Worker output reads like a spec, not a summary
- [ ] Exact text matches source when spot-checked

### State Management

- [ ] `.agents/state/PROGRESS.md` updated with [x] for this batch
- [ ] `git gcommit-hermes "Batch N: workers W___-W___ (pages ___-___)"` executed
- [ ] Feedback in `.agents/feedback/exchange.md` if issues found

## Notes

- Worker: ___
- Issues found: ___
- Actions taken: ___

## Escalation Protocol

### When to Escalate

Do not loop on re-extraction. Follow this protocol:

| Attempt | Action | After Failure |
|---------|--------|---------------|
| 1st extraction | Standard 4-page worker | If fails → Split page range in half (2+2 pages), re-extract both halves |
| 2nd extraction (split) | Two 2-page workers | If either half fails → Split that half to 1-page workers. If 1-page worker fails again → MANUAL |
| 3rd escalation | STOP. Flag for manual extraction. | See below. |

### Degraded Batch Procedure

If re-extraction fails twice for the same worker:

1. Log full details in `.agents/feedback/exchange.md`:

   ```
   ## DEGRADED: Worker W___ (Batch ___, pages ___-___)
   - Section type: ___
   - Failure mode: ___ (F1-F10 from worker-grid.md Failure Mode Matrix)
   - Attempt 1: Standard 4-page extraction — FAILED (reason)
   - Attempt 2: Split into W___a (pages ___-___) and W___b (pages ___-___)
     - W___a: ___ (PASS / FAIL)
     - W___b: ___ (PASS / FAIL)
   - Disposition: DEGRADED. Auditor will triage at pipeline end.
   ```

2. Mark the batch as DEGRADED in `.agents/state/PROGRESS.md`:

   ```
   Batch NN: DEGRADED — W___ failed after 2 re-extraction rounds. Awaiting auditor triage.
   ```

3. Proceed to the next batch. Do not block the pipeline.

4. After all 37 batches complete, the auditor reviews all DEGRADED batches. The auditor will:
   - Manually extract the failed pages using `read_file` and `write_file`.
   - Run all 4 checks (File Integrity, Truncation, Content Signals, Fabrication) on the manual output.
   - Mark the batch as RECOVERED with a `PASS (MANUAL)` entry in the validation log.

### Cascading Failures (2+ Workers Fail in One Batch)

When 2 or 3 workers in the same batch fail validation, stop. A cascading failure usually indicates a systemic problem. Follow this diagnostic sequence before retrying:

1. Check that source pages exist and have content:

   ```bash
   for pg in $(seq START END); do
     f="spec/issue-09-2025/page-dir/page-$(printf '%04d' $pg).md"
     [ -f "$f" ] && echo "OK: $f ($(wc -l < "$f") lines)" || echo "MISSING: $f"
   done
   ```

2. Check the batch prompt file for corruption:

   ```bash
   wc -l .agents/prompts/extraction/batch-prompt.txt
   ```

3. If source pages and prompt are intact, wait 60 seconds for rate limit recovery. Then re-extract each failed worker one at a time.

4. If source pages are missing or the prompt is corrupted, fix the root cause first. Do not re-extract until resolved.

5. Record the cascading failure in `.agents/feedback/exchange.md` with a `CASCADE` marker.

See `.agents/skills/validation/SKILL.md` (Cascading Failures in a Single Batch section) for the full diagnostic protocol.

## Worked Example: Batch 12 (Workers W034-W036, Pages 133-144)

This is a fully filled-out example from a real dictionary-zone batch. Use this as a reference for what a passing batch looks like.

### Section-Type Identification

- [x] W034 covers pages 133-136 (type: DICT, threshold: > 8 KB)
- [x] W035 covers pages 137-140 (type: DICT, threshold: > 8 KB)
- [x] W036 covers pages 141-144 (type: DICT, threshold: > 8 KB)

### File Integrity

- [x] All 3 output files exist in `ste-code/extracted/`
- [x] File sizes: W034 (11.2 KB), W035 (4.1 KB), W036 (12.8 KB)
- [x] W034 exceeds DICT threshold (> 8 KB). PASS.
- [!] W035 is below DICT threshold (> 8 KB). WARN — possible light dictionary page.
- [x] W036 exceeds DICT threshold (> 8 KB). PASS.

### Truncation Check

- [x] W034 last 3 lines: end with "Page 136 / 2025-01-15 / Issue 9"
- [x] W035 last 3 lines: end with complete dictionary entry, then "Page 140 / 2025-01-15 / Issue 9"
- [x] W036 last 3 lines: end with "Page 144 / 2025-01-15 / Issue 9"

Red flags:
- [ ] No red flags detected. All three files end on clean page footers.

### Content Signals (spot-check with `shuf`)

W034 spot-check:

```bash
$ shuf -n 50 ste-code/extracted/w034-p133-136.md | grep -v '^$' | head -n 3
APPROVED Meaning: To move forward or onward. Forms: advance, advances, advanced, advancing
Word (adj.) — UNAPPROVED. Alternatives: correct (adj.), right (adj.)
STE: Make sure that the valve is fully open. Non-STE: Ensure that the valve is fully open.
```

Result: 3 of 3 lines match DICT signals (APPROVED, Word (POS), UNAPPROVED, STE/Non-STE). **PASS.**

W035 spot-check:

```bash
$ shuf -n 50 ste-code/extracted/w035-p137-140.md | grep -v '^$' | head -n 3
Word (n.) — APPROVED. Meaning: A device that measures something.
Part 2 — Dictionary. ASD-STE100 Simplified Technical English.
The approved word is "close." Do not use "shut" as a verb.
```

Result: 2 of 3 lines match DICT signals. Line 2 is a structural header — count it as a signal match. **PASS with note: structural header in sample.**

W036 spot-check:

```bash
$ shuf -n 50 ste-code/extracted/w036-p141-144.md | grep -v '^$' | head -n 3
UNAPPROVED. Alternatives: find (v.), get (v.).
STE: The temperature must not be more than 100°C. Non-STE: The temperature shall not exceed 100°C.
Word (v.) — APPROVED. Meaning: To move something to a different position. Forms: move, moves, moved, moving.
```

Result: 3 of 3 lines match DICT signals. **PASS.**

### Fabrication Detection

- [x] No modern software terms in spec text. Grep for "React\|Docker\|API\|npm\|async" returned 0 matches.
- [x] No commentary language. Grep for "This page describes\|The key point is\|In summary" returned 0 matches.
- [x] Worker output reads like a spec. Dictionary entries use the standard 4-column format.
- [x] Spot-check against source: diff of first 20 lines of W034 output vs spec/page-0133.md shows exact match.

### State Management

- [x] `.agents/state/PROGRESS.md` updated with [x] for Batch 12.
- [x] `git gcommit-hermes "Batch 12: workers W034-W036 (pages 133-144)"` executed.
- [x] Feedback in `.agents/feedback/exchange.md`: flagged W035 for manual review due to small file size. No re-extraction needed — content is complete but page range is light.

### Batch 12 Disposition: ALL PASS (1 WARN: W035)

W035 has 58 lines and 4.1 KB. The content is complete. The page range (137-140) falls on dictionary pages with fewer entries. The file passes truncation and fabrication checks. Flag for spot-check review during the next audit cycle. No action required.

## Results Summary Template

After each batch, copy and fill this template in your notes:

```
=== Batch __ Validation (W___-W___, pages ___-___) ===

--- Check 1: File Existence and Size ---
W___: ___ lines, ___ bytes — ___ (PASS/WARN/FAIL) [section type: ___, threshold > ___ KB]
W___: ___ lines, ___ bytes — ___ (PASS/WARN/FAIL) [section type: ___, threshold > ___ KB]
W___: ___ lines, ___ bytes — ___ (PASS/WARN/FAIL) [section type: ___, threshold > ___ KB]

--- Check 2: Content Signals (shuf spot-check) ---
W___: ___ of 3 lines match expected signals — ___ (PASS/WARN/FAIL)
W___: ___ of 3 lines match expected signals — ___ (PASS/WARN/FAIL)
W___: ___ of 3 lines match expected signals — ___ (PASS/WARN/FAIL)

--- Check 3: Truncation Detection ---
W___: last 3 lines — ___ (PASS/FAIL)
W___: last 3 lines — ___ (PASS/FAIL)
W___: last 3 lines — ___ (PASS/FAIL)

--- Check 4: Fabrication Detection ---
W___: ___ (PASS/FAIL)
W___: ___ (PASS/FAIL)
W___: ___ (PASS/FAIL)

=== Batch __ Result: ___ PASS, ___ WARN, ___ FAIL ===
Action: ___
```

## Quick Decisions

| Situation | Do This |
|-----------|---------|
| File passes size threshold but matches 0 content signals | FAIL. File may contain wrong page range. Spot-check 3 lines against source spec page. If mismatch, delete and re-extract. |
| File is 10% below size threshold but passes all other checks | WARN. Flag for manual review. Do not re-extract. |
| File is 50%+ below size threshold | FAIL. Possible truncation. Check last 3 lines. If clean, suspect empty source pages. Verify source first, then re-extract. |
| Spot-check finds fabrication signals in 1 line of 3 | Expand to 8 lines. If 3+ of 8 show fabrication, FAIL. Delete file and re-extract with anti-fabrication prompt. |
| Same worker fails twice after split re-extraction | DEGRADED. Log in exchange.md. Mark batch as DEGRADED in PROGRESS.md. Proceed to next batch. |
| 2+ workers fail in same batch | CASCADE. Run diagnostic on source pages and prompt. Fix root cause before retrying. |
| Last batch (W109) has only 2 pages | Halve all thresholds. Use APPENDIX type. Accept > 1.5 KB and > 15 lines. |

## Companion Script: Automated Verification

This script runs checks 1-4 for a single worker. Supply the worker ID, page range, and expected section type. It reports PASS, WARN, or FAIL for each check.

```bash
#!/bin/bash
# Usage: verify-worker.sh WORKER_ID START_PAGE END_PAGE SECTION_TYPE THRESHOLD_KB
# Example: verify-worker.sh w034 133 136 DICT 8

WORKER=$1
START=$2
END=$3
TYPE=$4
THRESHOLD=$5
FILE="ste-code/extracted/${WORKER}-p$(printf '%03d' $START)-$(printf '%03d' $END).md"

echo "=== Worker $WORKER (pages $START-$END, type: $TYPE) ==="

# Check 1: Existence and Size
if [ ! -f "$FILE" ]; then
  echo "FAIL: File not found: $FILE"
  exit 1
fi
LINES=$(wc -l < "$FILE")
BYTES=$(wc -c < "$FILE")
KB=$((BYTES / 1024))
if [ "$KB" -ge "$THRESHOLD" ]; then
  echo "PASS: $LINES lines, $KB KB (threshold: > $THRESHOLD KB)"
else
  echo "WARN: $LINES lines, $KB KB (threshold: > $THRESHOLD KB)"
fi

# Check 2: Content Signals (shuf spot-check)
echo "--- Spot-check (3 random non-blank lines) ---"
SAMPLES=$(shuf -n 50 "$FILE" | grep -v '^$' | head -n 3)
echo "$SAMPLES"
echo ""
echo "MANUAL: Compare these lines to the Signal Reference Table for $TYPE."
echo "MANUAL: Determine PASS/WARN/FAIL based on the spot-check protocol."

# Check 3: Truncation Detection
echo "--- Last 3 lines ---"
tail -3 "$FILE"
echo ""
LAST_LINE=$(tail -1 "$FILE")
if echo "$LAST_LINE" | grep -qE '^[A-Za-z]' && ! echo "$LAST_LINE" | grep -qE '[.!?]$|Page [0-9]'; then
  echo "WARN: Last line may be incomplete (no sentence ending or page footer)."
else
  echo "PASS: Last line appears to end cleanly."
fi

# Check 4: Fabrication Detection
FAB_TERMS=$(grep -ci 'React\|Docker\|npm\|async.await\|git commit\|JSON\.parse\|This page describes\|In summary\|The key point' "$FILE" 2>/dev/null || echo 0)
COMMENTARY=$(grep -ci 'This page describes\|The key point is\|In summary\|Essentially' "$FILE" 2>/dev/null || echo 0)
if [ "$FAB_TERMS" -gt 0 ] || [ "$COMMENTARY" -gt 0 ]; then
  echo "FAIL: Fabrication signals detected. Software terms: $FAB_TERMS. Commentary: $COMMENTARY."
else
  echo "PASS: No fabrication signals detected."
fi

echo "=== End $WORKER ==="
```

Save this script as `.agents/tools/quality/verify-worker.sh`. Make it executable. Run it on each worker in the batch before filling out the manual checklist above.

NOTE: The script automates checks 1, 3, and 4. Check 2 (content signals) still requires human judgment — the script prints the sampled lines for manual review. Full automation of content signal matching is unreliable because it depends on section-type context and boundary-crossing detection.
