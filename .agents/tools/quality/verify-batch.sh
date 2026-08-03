#!/bin/bash
# Batch Verification Script — Run after each batch of 3 workers
# Usage: bash .agents/tools/quality/verify-batch.sh <directory> <prefix> <worker1> <worker2> <worker3>
# Example: bash .agents/tools/quality/verify-batch.sh extracted w w007 w008 w009

DIR="${1:-extracted}"
PREFIX="${2:-w}"
shift 2

PASS=0
FAIL=0

for worker in "$@"; do
	# Find the file matching this worker
	FILE=$(ls ste-code/$DIR/${worker}-p*.md 2>/dev/null | head -1)

	if [ -z "$FILE" ]; then
		echo "🔴 $worker: FILE NOT FOUND"
		FAIL=$((FAIL + 1))
		continue
	fi

	LINES=$(wc -l <"$FILE" | tr -d ' ')
	BYTES=$(wc -c <"$FILE" | tr -d ' ')
	HEADER=$(head -1 "$FILE")
	LAST3=$(tail -3 "$FILE")

	# Check 1: Size
	if [ "$LINES" -lt 15 ]; then
		echo "🔴 $worker: $LINES lines — EMPTY or TRUNCATED"
		FAIL=$((FAIL + 1))
		continue
	elif [ "$LINES" -lt 30 ]; then
		echo "🟡 $worker: $LINES lines — LIGHT (may be OK for content-light pages)"
	fi

	# Check 2: Page header
	if ! echo "$HEADER" | grep -qE '^# Page [0-9]+ of 434'; then
		echo "🟡 $worker: Missing/wrong page header: ${HEADER:0:60}"
	fi

	# Check 3: Truncation
	if echo "$LAST3" | grep -qE '[a-z]$'; then
		echo "🟡 $worker: Last line ends mid-word — possible truncation"
	fi

	# Check 4: Fabrication signals
	if grep -q "This page describes\|The key point\|In summary" "$FILE" 2>/dev/null; then
		echo "🔴 $worker: FABRICATION DETECTED — commentary language"
		FAIL=$((FAIL + 1))
		continue
	fi

	# Check 5: Boilerplate repetition
	BOILER=$(grep -c "ASD-STE100 Simplified Technical English" "$FILE" 2>/dev/null)
	if [ "$BOILER" -gt 4 ]; then
		echo "🟡 $worker: Boilerplate repeated $BOILER times (should be ≤1 in refined)"
	fi

	# Check 6: Glued headings
	GLUED=$(grep -c $'### [^\n]\n[^ \n#|`>-]' "$FILE" 2>/dev/null || echo 0)
	if [ "$GLUED" -gt 0 ]; then
		echo "🟡 $worker: $GLUED glued headings (no blank line after ###)"
	fi

	# Check 7: Triple blanks
	if grep -q $'\n\n\n\n' "$FILE" 2>/dev/null; then
		echo "🟡 $worker: Triple+ blank lines"
	fi

	echo "✅ $worker: $LINES lines, $BYTES bytes — PASS"
	PASS=$((PASS + 1))
done

echo ""
echo "Results: $PASS passed, $FAIL failed"
if [ "$FAIL" -gt 0 ]; then
	echo "⚠️  Do NOT proceed to next batch until failures are fixed."
	exit 1
else
	echo "✅ Batch verified. Safe to proceed."
fi
