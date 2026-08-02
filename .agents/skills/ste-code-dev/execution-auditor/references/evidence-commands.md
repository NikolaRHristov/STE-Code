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

### Cross-Reference Map

Use this map to connect each command section to the audit protocol steps.

| Command Section | SKILL.md Step | Relevant Rails | Output Feeds Into |
|-----------------|---------------|----------------|-------------------|
| Pre-Flight Readiness Check | Step 1 (Collect Claims) | RAIL 1 (Stage Isolation) | Claims ledger setup |
| Quick Evidence Sweep | Step 2 (Collect Evidence) | RAIL 3 (Completion Integrity) | Coverage map, agent trust scores |
| File-by-File Evidence | Step 2 (Collect Evidence) | RAIL 3 (Completion Integrity) | Discrepancy flags, trust scores |
| Page Coverage Audit | Step 2 (Collect Evidence) | RAIL 3 (Completion Integrity) | Coverage map |
| Fabrication Detection Sweep | Step 3 (Cross-Reference) | RAIL 4 (Content Fidelity) | Discrepancy flags |
| Timestamp Consistency Check | Step 3 (Cross-Reference) | RAIL 7 (Progress Tracking) | Chronology verification |
| Trust Score Calculation | Step 4 (Flag Discrepancies) | Quality Gates (SKILL.md) | Agent trust scores, audit quality score |

### Prerequisites

Before you run the commands in this file, make sure these are true:

1. The working directory is the project root.
2. The directory `ste-code/extracted/` exists.
3. The file `.agents/state/PROGRESS.md` exists.
4. The shell is `bash` or `zsh` on macOS.

NOTE: Some commands use macOS `stat` syntax (`stat -f '%Sm'`). On Linux, replace
`stat -f '%Sm'` with `stat -c '%y'`. Use the `uname` command to check your platform.

## Pre-Flight Readiness Check

Run this check before you run any evidence commands. A failed check means you must
fix the environment before the audit can start.

```bash
# Pre-flight: verify the audit environment is ready
echo "Pre-Flight Check"

# Check working directory
if [ -f ".agents/state/PROGRESS.md" ]; then
  echo "✅ Working directory is project root"
else
  echo "❌ PROGRESS.md not found — change to project root directory"
  echo "   Expected path: .agents/state/PROGRESS.md"
fi

# Check extracted directory exists
if [ -d "ste-code/extracted" ]; then
  count=$(ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "✅ ste-code/extracted/ exists with $count files"
elif [ -e "ste-code/extracted" ]; then
  echo "❌ ste-code/extracted exists but is not a directory"
  echo "   Remove the file at ste-code/extracted and create the directory"
else
  echo "❌ ste-code/extracted/ does not exist"
  echo "   The extraction stage has not run. See Recovery Procedure below."
fi

# Check PROGRESS.md exists and is readable
if [ -r ".agents/state/PROGRESS.md" ]; then
  echo "✅ PROGRESS.md is readable"
else
  echo "❌ PROGRESS.md is missing or not readable"
fi

# Check feedback exchange exists and is readable
if [ -r ".agents/feedback/exchange.md" ]; then
  echo "✅ feedback/exchange.md is readable"
else
  echo "⚠️  feedback/exchange.md is missing — claims may be incomplete"
fi

# Platform check for stat command
case "$(uname)" in
  Darwin) echo "✅ macOS — using stat -f '%Sm'" ;;
  Linux)  echo "✅ Linux — use stat -c '%y' instead of stat -f '%Sm'" ;;
  *)      echo "⚠️  Unknown platform — stat command may need adjustment" ;;
esac

echo ""
echo "Pre-flight complete. If any check failed, fix it before continuing."
echo "See Recovery Procedures at the end of this file for help."
```

### Interpreting the Pre-Flight Check

| Result | Meaning | Next Action |
|--------|---------|-------------|
| All ✅ | Environment is ready | Continue to Quick Evidence Sweep |
| ❌ PROGRESS.md not found | Wrong working directory or pipeline not initialized | Change to project root. If PROGRESS.md still missing, the pipeline has not been set up. |
| ❌ extracted/ does not exist | No extraction has been run | Launch extraction workers. See Recovery Procedure A. |
| ❌ extracted/ is a file, not a directory | A file with the same name blocks the directory | Remove the file and create the directory |
| ⚠️ exchange.md missing | Feedback channel not initialized | This is not fatal. Claims in PROGRESS.md are still usable. The audit may miss claims from agent messages. |

NOTE: A missing `ste-code/extracted/` directory is not a failure of the audit tool.
It means the extraction stage has not run or has been cleaned up. Run the extraction
stage before running the audit. See SKILL.md Step 1 (Collect Claims) for the full
claim sources.

## Interpretation of Results

### File-by-File Classifications

| Lines | Classification | Meaning | Action |
|-------|---------------|---------|--------|
| 0-29 | 🔴 SUSPICIOUS | File is empty or has very little content | The worker failed. Mark the batch as [!] in PROGRESS.md. Re-extract the page range. |
| 30-79 | 🟡 LIGHT | File exists but has less content than expected | The worker may have truncated output. Spot-check the first and last 5 lines. If content ends mid-sentence, re-extract with a smaller page range. |
| 80+ | ✅ OK | File has sufficient content | Content is likely complete. Continue to the next verification step. |

NOTE: The 30-line and 80-line thresholds assume 4 pages per worker at ~40-80 lines per page. A complete 4-page extraction usually has 160-320 lines. A LIGHT file is suspicious but not necessarily fabricated.

#### When a LIGHT File Is Acceptable

A LIGHT file (30-79 lines) is acceptable when all of these are true:

1. The file covers a page range that contains mostly short rule tables.
2. The last line ends with a complete sentence or a table row.
3. The file contains the ASD-STE100 boilerplate header.
4. No fabrication signals are present (see Fabrication Signals below).
5. The file passes a spot-check of 3 random lines against the spec.

If any of these conditions is false, treat the file as SUSPICIOUS and re-extract.

NOTE: Acceptable LIGHT files must still be flagged in the audit report under
a separate "LIGHT — Accepted" section. Do not silently pass them.

#### When an OK File Still Needs Review

An OK file (80+ lines) may still have problems. Check these edge cases:

- **Padded content**: A file with 85 lines where 50 lines repeat the same text
  passes the line threshold but contains no real content. Run the fabrication
  detection sweep even on OK files.
- **Wrong pages**: A file labeled `w001-p1-4.md` that contains content from
  pages 45-48 passes line checks but fails content verification. Cross-reference
  page references in the file against the claimed range.
- **Binary corruption**: A file that reports 80+ lines in `wc -l` but shows
  unreadable characters in `head` or `file` may be corrupted. Run `file <path>`
  on any file with unexpected output.

### Page Coverage

| Coverage | Classification | Action |
|----------|---------------|--------|
| < 80% | 🔴 CRITICAL | Most pages are missing. Extraction is incomplete. Do not proceed to refinement. |
| 80-95% | 🟡 WARNING | Some pages are missing. Identify the gaps and launch missing workers. |
| 95-99% | ✅ ACCEPTABLE | A small number of pages may be blank boilerplate or copyright pages in the spec. Verify the missing pages are non-content pages. |
| 100% | ✅ COMPLETE | All pages are accounted for. |

#### Coverage Calculation Example

```
Total spec pages: 434
Pages found on disk: 420
Coverage: 420 / 434 = 96.8% → ✅ ACCEPTABLE
Missing pages: 14 out of 434
```

If 14 pages are missing at 96.8%, check if they fall in known non-content ranges
(blank pages, copyright pages, table of contents). If all missing pages are
non-content, the coverage is effectively 100%. Document this finding in the
audit report with the specific page numbers.

### Fabrication Signals

| Signal | Severity | What It Means |
|--------|----------|---------------|
| Modern software term in extracted file | 🔴 CRITICAL | The worker generated content instead of extracting from the spec. Delete the file and re-extract. |
| Commentary pattern in extracted file | 🟡 WARNING | The worker summarized instead of extracting. Spot-check the file. If more than 3 commentary patterns exist, re-extract. |
| Missing ASD-STE100 boilerplate | 🔴 CRITICAL | The file does not contain the spec header. Content is likely fabricated. Delete and re-extract. |

#### Fabrication Signal Cross-Reference

These signals align with RAIL 4 (Content Fidelity) in rails.md. The full list
of fabrication patterns in SKILL.md (Step 5: Produce Audit Report, under
"Fabrication Detection Patterns") includes 6 additional signals beyond the 3
checked by the sweep commands in this file:

| Signal (from SKILL.md) | Checked by Sweep? | How to Verify |
|------------------------|-------------------|---------------|
| Modern software terms | ✅ Yes | Fabrication Detection Sweep |
| Commentary language | ✅ Yes | Fabrication Detection Sweep |
| Missing spec boilerplate | ✅ Yes | Fabrication Detection Sweep |
| Smooth flowing prose | ❌ No | Manual spot-check of file tone |
| Wrong page content | ❌ No | Cross-reference page markers |
| Identical content across workers | ❌ No | Run `diff` between worker files |

NOTE: The 3 unchecked signals need manual verification. Add a spot-check
section to the audit report for these. See Recovery Procedure C.

### Trust Score

| Score Range | Meaning |
|-------------|---------|
| 0.9 - 1.0 | ✅ High trust — almost all claims are verified |
| 0.7 - 0.89 | 🟡 Medium trust — some claims are unverified |
| < 0.7 | 🔴 Low trust — many claims are unverified, fabrication likely |

NOTE: A trust score below 0.80 blocks the phase gate. See SKILL.md Quality
Gates for the full gate decision matrix.

## Quick Evidence Sweep

This sweep gives a fast overview of the pipeline state. Run it first. The output
shows file counts, page counts, and PROGRESS.md status in a single pass.

Use the output to decide whether a full file-by-file audit is necessary. If the
sweep shows 109 extracted files and all batches complete, a partial audit may
be sufficient. If the sweep shows gaps, run the full file-by-file evidence check.

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

### Interpreting the Quick Sweep

| Output | Normal Range | Suspicious If | Cross-Reference |
|--------|-------------|---------------|-----------------|
| Extracted files | 109 (37 batches × 3 workers, minus 2 short batches) | < 50 or > 150 | RAIL 3: Completion Integrity |
| Refined files | 109 (one per extracted file) | Not equal to extracted count | RAIL 1: Stage Isolation |
| Pages covered | 434 | < 400 | Page Coverage table above |
| Completed batches | Varies by pipeline stage | 0 when extracted files > 0 | RAIL 7: Progress Tracking |
| Incomplete batches | Varies | > 0 when all files exist | RAIL 7: Progress Tracking |

NOTE: A mismatch between the extracted file count and the refined file count
is a RAIL 1 violation. A stage produced output for only some of the input files.
Investigate before continuing.

### What to Do With Quick Sweep Results

1. If all counts are within the normal ranges, proceed to a partial audit. Skip
   the File-by-File Evidence loop and go directly to the Fabrication Detection Sweep.
2. If any count is suspicious, run the File-by-File Evidence loop for a full audit.
3. If the extracted file count is 0, see Troubleshooting Empty Output below.

CROSS-REF: These counts feed into the audit report under "Coverage Map" and
"Claims Analyzed." See SKILL.md Step 5 (Produce Audit Report) for the template.

## File-by-File Evidence

This loop classifies each extracted file by line count. It also captures the byte
size and modification time. Use this for a full audit when the Quick Sweep shows
gaps or anomalies.

The `stat` command uses macOS format. On Linux, change `stat -f '%Sm'` to
`stat -c '%y'` throughout this loop.

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

### Interpreting the File-by-File Loop

| Output Pattern | What It Means | Action |
|----------------|---------------|--------|
| All ✅ with 80-350 lines each | All extractions are complete | Continue to Fabrication Detection Sweep |
| One or more 🔴 with 0 lines | The file exists but has no content | Delete and re-extract the page range |
| One or more 🔴 with 1-29 lines | The file is truncated or contains only headers | Re-extract with a smaller page range (2 pages per worker) |
| One or more 🟡 with 30-79 lines | Light files — may be acceptable | See "When a LIGHT File Is Acceptable" above |
| "unknown" for modification time | The `stat` command failed on a file | The file may be missing or have bad permissions. Run `ls -la "$f"` to check. |
| No output at all | No files match the `w*-p*.md` pattern | See Troubleshooting Empty Output below |

CROSS-REF: The file existence check aligns with RAIL 3 (Completion Integrity).
The line count threshold aligns with the Content Threshold Rationale in
SKILL.md Step 3 (Cross-Reference).

### Error Handling for the File-by-File Loop

The loop includes these fallbacks for common errors:

- `wc -l < "$f" 2>/dev/null || echo 0` — If `wc` fails (file not found, permission
  denied), the fallback produces 0 lines, which classifies the file as SUSPICIOUS.
- `stat -f "%Sm" "$f" 2>/dev/null || echo "unknown"` — If `stat` fails, the output
  shows "unknown" instead of an error message. This prevents confusing raw error
  text from appearing in audit output.
- The glob `ste-code/extracted/w*-p*.md` expands to nothing if no files match.
  In this case, the loop body never runs. The audit report must note this as
  "No extracted files found."

NOTE: If the glob produces no matches and the loop produces no output, do not
treat this as an error in the shell. It means the extraction stage has not
produced files. See Troubleshooting Empty Output.

## Page Coverage Audit

This command counts how many of the 434 spec pages appear in at least one
extracted file. It does not check for duplicate coverage (the same page in two
files). Run a duplicate check separately if coverage is above 100%.

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

### Interpreting the Page Coverage Audit

| Output | Meaning | Action |
|--------|---------|--------|
| Pages covered: 434/434 | All pages are accounted for | ✅ COMPLETE — proceed |
| Pages covered: 412-433/434 | 1-22 pages missing | ✅ ACCEPTABLE — verify missing pages are non-content |
| Pages covered: 347-411/434 | 23-87 pages missing | 🟡 WARNING — identify gaps and launch missing workers |
| Pages covered: < 347/434 | > 87 pages missing | 🔴 CRITICAL — extraction is incomplete. Do not proceed. |
| Pages covered: 0/434 | No page references found | Either no files exist, or files do not contain page markers. Check files first. |

NOTE: The coverage percentage alone does not tell the full story. Check if the
missing pages form contiguous ranges (a worker batch failed completely) or are
scattered (individual workers dropped random pages). Contiguous gaps are easier
to fix. Scattered gaps may indicate a systemic problem.

CROSS-REF: Page coverage feeds into the Coverage Map section of the audit
report. See SKILL.md Step 5 for the template. Coverage below 80% triggers
RAIL 8 (Error Recovery) — the pipeline must pause and fix the gaps.

### Checking for Duplicate Page Coverage

A page that appears in two files is a coverage anomaly. Run this check after the
page coverage audit if coverage is near or above 100%:

```bash
# Find pages covered by more than one file
echo "Duplicate page coverage check"
for pg in $(seq 1 434); do
  pg_fmt=$(printf "%04d" $pg)
  matches=$(grep -rl "page-${pg_fmt}" ste-code/extracted/w*-p*.md 2>/dev/null)
  count=$(echo "$matches" | grep -c "w" 2>/dev/null || echo 0)
  if [ "$count" -gt 1 ]; then
    echo "⚠️  Page $pg appears in $count files:"
    echo "$matches"
  fi
done
```

If any page appears in more than one file, flag it in the audit report. Two
workers may have extracted the same page due to overlapping page ranges. This
is not fabrication but wastes worker capacity.

## Fabrication Detection Sweep

This sweep checks for known fabrication patterns. It checks modern software
terms, commentary patterns, and missing boilerplate. Run this after the
file-by-file evidence loop.

```bash
# Modern terms that should NOT appear in ASD-STE100 spec text
echo "Fabrication signals"
for term in "React" "Docker" "npm" "API endpoint" "async/await" "TypeScript" "Kubernetes"; do
  count=$(grep -rl "$term" ste-code/extracted/w*-p*.md 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "🔴 '$term' found in $count extracted files — fabrication likely"
  fi
done

# Commentary patterns that indicate fabrication
echo "Commentary patterns"
for pattern in "This page describes" "The key point" "In summary" "As we can see"; do
  count=$(grep -rl "$pattern" ste-code/extracted/w*-p*.md 2>/dev/null | wc -l)
  if [ "$count" -gt 0 ]; then
    echo "🟡 '$pattern' in $count files — may be commentary, not extraction"
  fi
done

# Missing spec boilerplate
echo "Boilerplate check"
for f in ste-code/extracted/w*-p*.md; do
  if ! grep -q "ASD-STE100" "$f" 2>/dev/null; then
    echo "🔴 $f: missing ASD-STE100 boilerplate"
  fi
done
```

### Interpreting the Fabrication Sweep

| Output | Meaning | Action |
|--------|---------|--------|
| No matches found | No fabrication signals detected | This is expected for valid extractions. Continue to the next check. |
| Modern software terms found | The worker generated content instead of extracting | 🔴 CRITICAL — delete the flagged files and re-extract. Update SKILL.md remediation log. |
| Commentary patterns in 1-3 files | The worker summarized lightly | 🟡 WARNING — spot-check the files. If the commentary is minimal, accept with a note. |
| Commentary patterns in > 3 files | The worker summarized heavily | 🔴 CRITICAL — re-extract all flagged files |
| Missing boilerplate in a file | The file may be fabricated or corrupted | 🔴 CRITICAL — delete and re-extract |

CROSS-REF: These patterns align with RAIL 4 (Content Fidelity) in rails.md.
See also the Fabrication Detection Patterns section in SKILL.md for the full
list of 6 patterns plus known limitations.

### False Positive Guide

Some terms that look like fabrication signals may be legitimate. Check these
before deleting files:

| Term Found | May Be Legitimate If | Check |
|------------|---------------------|-------|
| "API" | The spec discusses application interfaces | Verify against the actual spec text for the page |
| "computer" | ASD-STE100 dictionary includes "computer" as an approved noun | Check if the usage matches a dictionary entry |
| "software" | ASD-STE100 dictionary includes "software" as an approved technical noun | Check if the context is a dictionary definition |
| "This page describes" | Rarely legitimate in extraction context | Almost always fabrication — delete and re-extract |

NOTE: Do not remove terms from the detection list because of a single false
positive. Document the false positive in the audit report instead.

## Timestamp Consistency Check

NOTE: The `stat` command uses macOS format (`stat -f '%Sm'`). On Linux, use `stat -c '%y'` instead. If a file is missing, the command shows an empty result. A file with a missing timestamp is not evidence of fabrication — check if the file exists first.

```bash
# Files created before claims were made are suspicious
echo "Chronology check"
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

### Interpreting the Timestamp Check

| Output | Meaning | Action |
|--------|---------|--------|
| PROGRESS.md and files have consistent timestamps | Timeline is coherent | ✅ Proceed |
| "FILE MISSING" for PROGRESS.md | PROGRESS.md does not exist | ❌ The pipeline tracking file is missing. This is a RAIL 7 violation. |
| "FILE MISSING" for exchange.md | Feedback file does not exist | ⚠️ Claims may be incomplete. See Pre-Flight Check. |
| "No extracted files found" | Extraction directory is empty | ❌ Run the extraction stage first |
| "unknown" for a file timestamp | The `stat` command failed on a specific file | The file may have bad permissions or be on a filesystem without timestamp support. Run `ls -la` on the file. |

### Chronology Anomaly Detection

A file with a modification time AFTER a claim about its completion may be
suspicious. A claim with a timestamp AFTER the file modification time may be
retroactive. Use these rules:

- **Normal**: File timestamp < Claim timestamp (file was created first, then
  the claim was made — normal workflow).
- **Suspicious**: Claim timestamp < File timestamp (the claim was made before
  the file existed — claim may be predictive or the file was recreated).
- **Critical**: Claim timestamp and file timestamp differ by more than 24 hours
  AND the claim is marked [x] in PROGRESS.md. This may be a retroactive claim.

NOTE: Timestamp checks rely on accurate system clocks. If the pipeline runs
across multiple machines with clock drift, timestamps may be unreliable.
Document any clock drift concerns in the audit report.

CROSS-REF: Timestamp verification aligns with RAIL 7 (Progress Tracking).
PROGRESS.md must reflect reality. An [x] checkbox with a timestamp discrepancy
is a tracking error.

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

### How to Compute the Trust Score Manually

1. Count the total claims from all sources (PROGRESS.md, exchange.md, agent messages).
2. For each claim, check the evidence using the File-by-File Evidence loop.
3. Mark each claim as verified (✅) or unverified (❌).
4. Divide verified claims by total claims.
5. Round to 2 decimal places.

Example:

```
Total claims: 109
Verified claims: 103 (6 files are LIGHT with suspicious content)
Trust score: 103 / 109 = 0.94 → ✅ High trust
```

NOTE: A trust score below 0.90 needs investigation. A trust score below 0.80
blocks the phase gate. See SKILL.md Quality Gates for the gate decision matrix.

### Trust Score per Agent

Compute a separate trust score for each agent. Use only the claims made by
that agent. This identifies which agent is the source of discrepancies.

```bash
# Quick per-agent trust score (manual classification needed)
echo "Per-agent claims from PROGRESS.md"
echo "Extraction claims (batches with [x]):"
grep -c '\[x\].*[Ww]\d\d\d' .agents/state/PROGRESS.md 2>/dev/null || echo "0"

echo "Extraction files on disk (w*-p*.md):"
ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l
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

### Using Expected Ranges to Detect Anomalies

When a measurement falls outside the expected range, use this decision table.

| Anomaly | Possible Causes | Investigation |
|---------|----------------|---------------|
| File count > 109 | Duplicate workers, renamed files, or files in wrong stage | Run the duplicate page coverage check |
| File count < 109 but > 0 | Some workers failed or were not launched | Check PROGRESS.md for incomplete batches. Check for [!] markers. |
| Lines > 500 | Worker extracted more than 4 pages, or fabricated verbose content | Check page markers in the file. Run fabrication sweep. |
| Lines < 30 | Worker failed, output was truncated, or page range was too small | Delete and re-extract with a smaller page range |
| Bytes > 50KB | File may contain embedded binary data or excessive whitespace | Run `file "$f"` to check the file type |
| Bytes < 1KB but lines > 30 | File may contain only blank lines or repeating whitespace | Run `grep -c '[a-zA-Z]' "$f"` to count meaningful content lines |

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

### Empty Output Diagnostic Script

Run this script if multiple commands produce empty output. It checks the
filesystem state and reports what is missing.

```bash
echo "Empty Output Diagnostic"
echo ""

# Directory structure check
echo "--- Directory Check ---"
[ -d "ste-code" ] && echo "✅ ste-code/ exists" || echo "❌ ste-code/ missing"
[ -d "ste-code/extracted" ] && echo "✅ ste-code/extracted/ exists" || echo "❌ ste-code/extracted/ missing"
[ -d "ste-code/refined" ] && echo "✅ ste-code/refined/ exists" || echo "⚠️  ste-code/refined/ missing"
[ -d ".agents" ] && echo "✅ .agents/ exists" || echo "❌ .agents/ missing"
[ -d ".agents/state" ] && echo "✅ .agents/state/ exists" || echo "❌ .agents/state/ missing"

# State file check
echo ""
echo "--- State File Check ---"
[ -f ".agents/state/PROGRESS.md" ] && echo "✅ PROGRESS.md exists" || echo "❌ PROGRESS.md missing"
[ -f ".agents/feedback/exchange.md" ] && echo "✅ exchange.md exists" || echo "⚠️  exchange.md missing"

# File count check
echo ""
echo "--- File Count Check ---"
extracted=$(ls ste-code/extracted/w*-p*.md 2>/dev/null | wc -l | tr -d ' ')
refined=$(ls ste-code/refined/r*-p*.md 2>/dev/null | wc -l | tr -d ' ')
echo "Extracted files: $extracted"
echo "Refined files: $refined"

# Claim count check
echo ""
echo "--- Claim Check ---"
completed=$(grep -c '\[x\]' .agents/state/PROGRESS.md 2>/dev/null || echo "0")
incomplete=$(grep -c '\[ \]' .agents/state/PROGRESS.md 2>/dev/null || echo "0")
failed=$(grep -c '\[!\]' .agents/state/PROGRESS.md 2>/dev/null || echo "0")
echo "Completed batches: $completed"
echo "Incomplete batches: $incomplete"
echo "Failed batches: $failed"

echo ""
echo "--- Diagnosis ---"
if [ "$extracted" = "0" ] && [ "$completed" != "0" ]; then
  echo "🔴 PROGRESS.md shows $completed completed batches but no extracted files exist."
  echo "   This is a tracking fabrication error (RAIL 7 violation)."
  echo "   Revert all [x] to [ ] for batches with no disk evidence."
elif [ "$extracted" = "0" ] && [ "$completed" = "0" ]; then
  echo "⚠️  No extracted files and no completed batches."
  echo "   The extraction stage has not been run. Launch extraction workers."
elif [ "$extracted" != "0" ] && [ "$completed" = "0" ]; then
  echo "⚠️  Extracted files exist but PROGRESS.md shows no completed batches."
  echo "   PROGRESS.md is out of sync. Update the tracker (RAIL 7)."
else
  echo "✅ File count and batch count are non-zero. Check individual files next."
fi
```

## Recovery Procedures

Use these procedures after the audit finds discrepancies. Each procedure
references the relevant audit step and rail.

### Procedure A: No Extracted Files Exist

**Trigger**: Pre-flight check shows `ste-code/extracted/` is missing or empty.

**Severity**: BLOCKING — pipeline cannot continue until extraction runs.

**Steps**:

1. Confirm the working directory is the project root.
2. Check if the spec source exists. The extraction stage needs spec pages as input.
3. Launch extraction workers. See the extraction orchestrator SKILL.md for the launch command.
4. Wait for extraction to complete. Run the Quick Evidence Sweep to confirm files exist.
5. Re-run the full audit.

**Cross-ref**: SKILL.md Step 1 (Collect Claims), RAIL 1 (Stage Isolation).

### Procedure B: Suspicious or LIGHT Files Found

**Trigger**: File-by-File Evidence loop shows 🔴 SUSPICIOUS or 🟡 LIGHT files.

**Severity**: BLOCKING for SUSPICIOUS. WARNING for LIGHT that fails acceptance criteria.

**Steps for SUSPICIOUS files**:

1. Note the file path and the batch it belongs to.
2. Delete the file.
3. Mark the batch as [!] in PROGRESS.md.
4. Re-extract the page range with a smaller batch size (2 pages per worker instead of 4).
5. Re-run the File-by-File Evidence loop on the new file.

**Steps for LIGHT files**:

1. Open the file and check the first 5 lines and last 5 lines.
2. If the content ends mid-sentence, the file is truncated. Treat as SUSPICIOUS.
3. Run the fabrication detection sweep on the file.
4. If no fabrication signals are present and the content is coherent, accept the file.
5. Document the acceptance in the audit report under "LIGHT — Accepted."

**Cross-ref**: SKILL.md Step 4 (Flag Discrepancies), RAIL 8 (Error Recovery).

### Procedure C: Fabrication Detected

**Trigger**: Fabrication Detection Sweep shows modern terms, commentary patterns,
or missing boilerplate.

**Severity**: CRITICAL — files with fabrication signals must be deleted and re-extracted.

**Steps**:

1. Record the file paths flagged by the sweep.
2. Delete each flagged file.
3. Mark the corresponding batch as [!] in PROGRESS.md.
4. Re-extract the page ranges for the deleted files.
5. Run the fabrication sweep again on the new files.
6. If the same files fail again, escalate to a human reviewer. The worker prompt
   may need adjustment.

NOTE: Do not attempt to edit fabricated files to remove the signals. A fabricated
file is not trustworthy in any part. Delete the entire file and re-extract.

**Cross-ref**: SKILL.md Step 3 (Cross-Reference), RAIL 4 (Content Fidelity).

### Procedure D: PROGRESS.md Tracking Error

**Trigger**: PROGRESS.md shows [x] for a batch with no files on disk, or shows
[ ] for a batch with files on disk.

**Severity**: ERROR — the tracker does not match reality. This is a RAIL 7 violation.

**Steps**:

1. List all batches with mismatched tracker states.
2. For each mismatched batch, determine the true state from disk evidence.
3. Update PROGRESS.md to match reality:
   - Change [x] to [ ] if files are missing.
   - Change [ ] to [x] if files exist and pass verification.
   - Change [ ] to [!] if files exist but are SUSPICIOUS or fabricated.
4. Add a timestamped note to PROGRESS.md explaining the correction.
5. Re-run the Quick Evidence Sweep to confirm the tracker is accurate.

**Cross-ref**: SKILL.md Step 4 (Flag Discrepancies), RAIL 7 (Progress Tracking).

### Procedure E: Coverage Gap

**Trigger**: Page Coverage Audit shows < 95% coverage.

**Severity**: BLOCKING if < 80%. WARNING if 80-95%.

**Steps**:

1. From the missing pages list, identify contiguous ranges. A range of 4 pages
   is likely one missing worker.
2. Check PROGRESS.md for the batch that covers the missing pages.
3. If the batch is marked [x] but files are missing: Procedure D (tracking error).
4. If the batch is marked [ ] or [!]: launch the missing workers.
5. Re-run the Page Coverage Audit to confirm the gaps are filled.

**Cross-ref**: SKILL.md Step 2 (Collect Evidence), RAIL 3 (Completion Integrity).

## Output Integration Guide

After you run all commands and interpret the results, feed the findings into the
audit report. Use this guide to map each section of this file to the report template.

### Report Section Mapping

| Evidence Section | Maps to Report Field | Format |
|-----------------|---------------------|--------|
| Quick Evidence Sweep | "Claims Analyzed" and "Evidence Files Checked" | Numeric counts |
| File-by-File Evidence | "Discrepancies Found" with per-file flags | List of flagged files with classification |
| Page Coverage Audit | "Coverage Map" | Percentage and page count |
| Fabrication Detection Sweep | "Critical (🔴)" and "Warnings (🟡)" under discrepancies | Per-signal counts with file paths |
| Timestamp Consistency Check | Agent trust scores (chronology factor) | Timestamps or anomaly notes |
| Trust Score Calculation | "Agent Trust Scores" table | Decimal scores per agent |

### Report Template (minimal)

Use this template as the starting structure. Expand each section with the
findings from the evidence commands.

```markdown
# Execution Audit — YYYY-MM-DD HH:MM:SS

## Claims Analyzed: [from Quick Sweep]
## Evidence Files Checked: [from Quick Sweep]
## Discrepancies Found: [from File-by-File + Fabrication Sweep]

### Critical (🔴)
[Files flagged as SUSPICIOUS or with fabrication signals]

### Warnings (🟡)
[Files flagged as LIGHT or with minor commentary]

### Verified Claims (✅)
[Files that passed all checks]

## Coverage Map
- Pages claimed extracted: [from Page Coverage Audit]
- Pages verified on disk: [from Page Coverage Audit]
- Verified percentage: [computed]

## Agent Trust Scores
| Agent | Claims Made | Claims Verified | Trust |
|-------|-------------|-----------------|-------|
| [agent name] | [count] | [count] | [score] |

## Auto-Fixes Applied
[If in fix mode: list each fix with file path and result]

## Recommendations
[Actionable next steps based on findings]
```

NOTE: The full report template is in SKILL.md Step 5 (Produce Audit Report).
This is a minimal version. Use the SKILL.md template for the complete report.

### Audit Quality Score Formula

After the report is complete, compute the audit quality score:

```
quality_score = (verified_claims / total_claims) × 0.6
              + (1.0 - (false_positives / total_claims)) × 0.2
              + (1.0 if no_criticals else 0.0) × 0.2
```

| Score Range | Quality | Action |
|-------------|---------|--------|
| ≥ 0.95 | Excellent | Pipeline is healthy. Proceed. |
| 0.85–0.94 | Good | Minor issues. Monitor. |
| 0.70–0.84 | Fair | Systemic issues. Investigate. |
| < 0.70 | Poor | Pipeline needs remediation before continuing. |

CROSS-REF: The quality score formula is defined in SKILL.md Quality Gates.
This does not override the critical discrepancy cap (0 criticals required).
A score of 0.99 with 1 critical discrepancy still blocks the phase gate.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-07-26 | Initial release |
| 1.1.0 | 2026-07-30 | Added Pre-Flight Readiness Check, Cross-Reference Map, per-section interpretation guidance, error handling notes, Recovery Procedures (A-E), Output Integration Guide, Duplicate Page Coverage check, Empty Output Diagnostic script, False Positive Guide, per-agent trust score script |
