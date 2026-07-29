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

Systematic validation of worker extraction output. Run after each batch (every 3 workers)
and after the full merge. Catches fabrication, truncation, and incompleteness.

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
