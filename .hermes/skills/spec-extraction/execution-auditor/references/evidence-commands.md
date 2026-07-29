# Execution Audit — Evidence Collection Commands

> Run these commands during each audit. Output feeds into the audit report.

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
grep -c '\[x\]' .hermes/state/PROGRESS.md 2>/dev/null
echo "Incomplete batches:"
grep -c '\[ \]' .hermes/state/PROGRESS.md 2>/dev/null
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

```bash
# Files created before claims were made are suspicious
echo "=== Chronology check ==="
echo "PROGRESS.md last modified: $(stat -f '%Sm' .hermes/state/PROGRESS.md 2>/dev/null)"
echo "Feedback last modified: $(stat -f '%Sm' .hermes/feedback/exchange.md 2>/dev/null)"
echo "Earliest extracted file: $(ls -t ste-code/extracted/w*-p*.md 2>/dev/null | tail -1 | xargs stat -f '%Sm')"
echo "Latest extracted file: $(ls -t ste-code/extracted/w*-p*.md 2>/dev/null | head -1 | xargs stat -f '%Sm')"
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
