# Execution Audit — Evidence Collection Commands

> Run these commands during each audit. Output feeds into the audit report.

## About This Reference

This reference is part of the Execution Auditor skill. Read the parent skill at
`../SKILL.md` for the full audit protocol. Read `../references/rails.md` for the
8 guardrails that all workers must follow.

The commands in this file collect evidence from disk. Use this evidence with the
cross-reference procedure in SKILL.md (Step 3: Cross-Reference). The fabrication
detection patterns align with RAIL 4 (Content Fidelity) in rails.md.

NOTE: This file is a tool, not a tutorial. Run the commands. Use the sections
below to interpret the results and to know the expected ranges.

## Interpretation of Results

### File-by-File Classifications

| Lines | Classification | Meaning | Action |
|-------|---------------|---------|--------|
| 0-29 | 🔴 SUSPICIOUS | File is empty or has very little content | The worker failed. Mark the batch as [!] in PROGRESS.md. Re-extract the page range. |
| 30-79 | 🟡 LIGHT | File exists but has less content than expected | The worker may have truncated output. Spot-check the first and last 5 lines. If content ends mid-sentence, re-extract with a smaller page range. |
| 80+ | ✅ OK | File has sufficient content | Content is likely complete. Continue to the next verification step. |

NOTE: The 30-line and 80-line thresholds assume 4 pages per worker at ~40-80 lines per page. A complete 4-page extraction usually has 160-320 lines. A LIGHT file is suspicious but not necessarily fabricated.

### Page Coverage

| Coverage | Classification | Action |
|----------|---------------|--------|
| < 80% | 🔴 CRITICAL | Most pages are missing. Extraction is incomplete. Do not proceed to refinement. |
| 80-95% | 🟡 WARNING | Some pages are missing. Identify the gaps and launch missing workers. |
| 95-99% | ✅ ACCEPTABLE | A small number of pages may be blank boilerplate or copyright pages in the spec. Verify the missing pages are non-content pages. |
| 100% | ✅ COMPLETE | All pages are accounted for. |

### Fabrication Signals

| Signal | Severity | What It Means |
|--------|----------|---------------|
| Modern software term in extracted file | 🔴 CRITICAL | The worker generated content instead of extracting from the spec. Delete the file and re-extract. |
| Commentary pattern in extracted file | 🟡 WARNING | The worker summarized instead of extracting. Spot-check the file. If more than 3 commentary patterns exist, re-extract. |
| Missing ASD-STE100 boilerplate | 🔴 CRITICAL | The file does not contain the spec header. Content is likely fabricated. Delete and re-extract. |

### Trust Score

| Score Range | Meaning |
|-------------|---------|
| 0.9 - 1.0 | ✅ High trust — almost all claims are verified |
| 0.7 - 0.89 | 🟡 Medium trust — some claims are unverified |
| < 0.7 | 🔴 Low trust — many claims are unverified, fabrication likely |

## Quick Evidence Sweep

```bash
# Count all extracted files
echo "Extracted files: $(ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l)"

# Count all refined files
echo "Refined files: $(ls ste-code/refined/r*-p*.md 2>/dev/null | wc -l)"

# Total pages covered
echo "Page ranges covered:"
grep -oh "page-[0-9]*" ste-code/extracted/w*-p*.md 2>/dev/null | sort -u | wc -l

# Check PROGRESS.md checkbox status
echo "Completed batches in PROGRESS.md:"
grep -c '\[x\]' .agents/state/PROGRESS.md 2>/dev/null
echo "Incomplete batches:"
grep -c '\[ \]' .agents/state/PROGRESS.md 2>/dev/null
```

## File-by-File Evidence

```bash
for f in ste-code/extracted/w*-p*.md; do
  lines=$(wc -l < "$f" 2>/dev/null || echo 0)
  bytes=$(wc -c < "$f" 2>/dev/null || echo 0)
  mod=$(stat -f "%Sm" "$f" 2>/dev/null || echo "unknown")
  if [ "$lines" -lt 30 ]; then
    echo "🔴 $f: $lines lines — SUSPICIOUS"
  elif [ "$lines" -lt 80 ]; then
    echo "🟡 $f: $lines lines — LIGHT"
  else
    echo "✅ $f: $lines lines, $bytes bytes, $mod"
  fi
done
```

## Page Coverage Audit

```bash
covered=0
missing=""
for pg in $(seq 1 434); do
  pg_fmt=$(printf "%04d" $pg)
  if grep -rq "page-${pg_fmt}" ste-code/extracted/w*-p*.md 2>/dev/null; then
    covered=$((covered + 1))
  else
    missing="$missing $pg"
  fi
done
echo "Pages covered: $covered/434"
if [ -n "$missing" ]; then
  echo "Missing pages: $missing"
fi
```

## Fabrication Detection Sweep

```bash
# Modern terms that should NOT appear in ASD-STE100 spec text
echo "=== Fabrication signals ==="
for term in "React" "Docker" "npm" "API endpoint" "async/await" "TypeScript" "Kubernetes"; do
  count=$(grep -rl "$term" ste-code/extracted/w*-p*.md 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "🔴 '$term' found in $count extracted files — fabrication likely"
  fi
done

# Commentary patterns that indicate fabrication
echo "=== Commentary patterns ==="
for pattern in "This page describes" "The key point" "In summary" "As we can see"; do
  count=$(grep -rl "$pattern" ste-code/extracted/w*-p*.md 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "🟡 '$pattern' in $count files — may be commentary, not extraction"
  fi
done

# Missing spec boilerplate
echo "=== Boilerplate check ==="
for f in ste-code/extracted/w*-p*.md; do
  if ! grep -q "ASD-STE100" "$f" 2>/dev/null; then
    echo "🔴 $f: missing ASD-STE100 boilerplate"
  fi
done
```

## Timestamp Consistency Check

NOTE: The `stat` command uses macOS format (`stat -f '%Sm'`). On Linux, use `stat -c '%y'` instead. If a file is missing, the command shows an empty result. A file with a missing timestamp is not evidence of fabrication — check if the file exists first.

```bash
# Files created before claims were made are suspicious
echo "=== Chronology check ==="
echo "PROGRESS.md last modified: $(stat -f '%Sm' .agents/state/PROGRESS.md 2>/dev/null || echo 'FILE MISSING')"
echo "Feedback last modified: $(stat -f '%Sm' .agents/feedback/exchange.md 2>/dev/null || echo 'FILE MISSING')"

# Earliest and latest extracted files — handle empty glob gracefully
if ls ste-code/extracted/w*-p*.md 2>/dev/null | head -1 > /dev/null 2>&1; then
  echo "Earliest extracted file: $(ls -t ste-code/extracted/w*-p*.md 2>/dev/null | tail -1 | xargs stat -f '%Sm' 2>/dev/null || echo 'unknown')"
  echo "Latest extracted file: $(ls -t ste-code/extracted/w*-p*.md 2>/dev/null | head -1 | xargs stat -f '%Sm' 2>/dev/null || echo 'unknown')"
else
  echo "No extracted files found in ste-code/extracted/"
fi
```

## Trust Score Calculation

```
trust = verified_claims / total_claims

verified_claims = count of claims where:
  - Claimed file exists
  - File has real content (>30 lines)
  - File timestamp is after claim timestamp (or within 5 min before)
  - Content matches expected page range

total_claims = count of all [x] checkboxes + explicit claims in feedback
```

## Expected Output Ranges

Use these ranges to check if the audit results are normal.

### Extracted Files

| Stage | Expected File Count | Notes |
|-------|--------------------|-------|
| Extraction | 109 files (37 batches × 3 workers, minus 2 short batches) | Covers 434 pages at 4 pages per worker |
| Refinement | 109 files | One refined file per extracted file |

### File Sizes

| Measurement | Expected Range | Suspicious If |
|-------------|---------------|---------------|
| Lines per extracted file | 80-350 lines | < 30 or > 500 |
| Bytes per extracted file | 3KB-30KB | < 1KB or > 50KB |
| Lines per refined file | 60-300 lines | < 20 or > 400 |

### Page Coverage

| Measurement | Target |
|-------------|--------|
| Pages covered | 434 of 434 (100%) |
| Acceptable minimum | 412 of 434 (95%) |

### Trust Score

| Measurement | Target |
|-------------|--------|
| Minimum acceptable trust score | 0.90 |

## Troubleshooting Empty Output

If a command in this reference produces no output, use this table to diagnose the cause.

| Symptom | Cause | Action |
|---------|-------|--------|
| `ls ste-code/extracted/w*-p*.md` returns nothing | No extracted files exist | The extraction stage has not run. Launch extraction workers before running the audit. |
| `grep -c '\[x\]' .agents/state/PROGRESS.md` returns 0 | No completed batches in PROGRESS.md | Either no batches are complete, or PROGRESS.md does not exist. Check if PROGRESS.md exists. |
| `grep -c '\[ \]' .agents/state/PROGRESS.md` returns 0 | All batches are marked complete, or PROGRESS.md is missing | Check if files exist on disk to confirm. An all-complete tracker with no files is a tracking error. |
| Fabrication sweep shows no matches | No fabrication signals detected | This is expected for valid extractions. Continue to the next check. |
| Page coverage shows 0/434 | No extracted files, or no page references in files | Check if extracted files exist. If files exist but coverage is 0, the files may not contain page markers. |
| Timestamp check shows "unknown" | The `stat` command failed on a file | The file may be missing. Use `ls` to check if the file exists. |
| File-by-file loop shows no output | No files match the `w*-p*.md` pattern | No extracted files exist. See the first symptom in this table. |

BREAKING: If ALL commands produce empty output and no `ste-code/extracted/` directory exists, the pipeline has not started. Do not fabricate results. Run the extraction stage first.
