#!/usr/bin/env bash
# STE-Code Benchmark Runner v1.0.0
# Usage: bash .agents/benchmark/run-benchmark.sh [--category readme] [--test bench-001]
# Agent #4 benchmarking orchestrator — runs test cases through hermes -z with STE-Code system prompt

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYSTEM_PROMPT="$PROJECT_ROOT/ste-code/artifacts/ste-code-distilled-system-prompt.txt"
TEST_DIR="$SCRIPT_DIR/test-cases"
RESULTS_DIR="$SCRIPT_DIR/results"
TIMESTAMP=$(date -u +"%Y%m%d-%H%M%S")
RUN_DIR="$RESULTS_DIR/run-$TIMESTAMP"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

echo "=== STE-Code Benchmark Runner ==="
echo "Model: deepseek-v4-pro"
echo "Timestamp: $TIMESTAMP"
echo ""

# Verify prerequisites
if [ ! -f "$SYSTEM_PROMPT" ]; then
    echo -e "${RED}ERROR: System prompt not found at $SYSTEM_PROMPT${NC}"
    exit 1
fi
echo -e "${GREEN}System prompt found${NC}"

mkdir -p "$RUN_DIR"

# Load all test cases
TEST_FILES=$(ls "$TEST_DIR"/category-*.json 2>/dev/null)
TOTAL_TESTS=$(cat "$TEST_DIR"/category-*.json | grep -c '"id"' || echo 0)
echo "Test cases loaded: $TOTAL_TESTS"
echo ""

# Initialize aggregate results
PASSED=0; FAILED=0
CAT_TRACKING="$RUN_DIR/.cat_tracking"
> "$CAT_TRACKING"
RESULTS_JSON="$RUN_DIR/aggregate-results.json"

echo "{" > "$RESULTS_JSON"
echo "  \"benchmark_id\": \"ste-code-v1.0.0\"," >> "$RESULTS_JSON"
echo "  \"timestamp\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\"," >> "$RESULTS_JSON"
echo "  \"model\": \"deepseek-v4-pro\"," >> "$RESULTS_JSON"
echo "  \"total_tests\": $TOTAL_TESTS," >> "$RESULTS_JSON"
echo "  \"results\": [" >> "$RESULTS_JSON"

FIRST=true
TEST_INDEX=0

# Process each category
for CAT_FILE in "$TEST_DIR"/category-*.json; do
    CATEGORY=$(basename "$CAT_FILE" .json | sed 's/category-[0-9]-//')
    echo "--- Category: $CATEGORY ---"

    # Extract test IDs
    TEST_IDS=$(python3 -c "import json; [print(t['id']) for t in json.load(open('$CAT_FILE'))]")

    for TEST_ID in $TEST_IDS; do
        TEST_INDEX=$((TEST_INDEX + 1))
        echo -n "  [$TEST_INDEX/$TOTAL_TESTS] $TEST_ID... "

        # Extract test case data
        TEST_DATA=$(python3 -c "
import json, sys
tests = json.load(open('$CAT_FILE'))
t = next(t for t in tests if t['id'] == '$TEST_ID')
print(t['input'])
print('---PRINCIPLES---')
print(','.join(t['expected_principles']))
print('---FORBIDDEN---')
print(','.join(t.get('forbidden_keywords', [])))
")

        INPUT=$(echo "$TEST_DATA" | sed -n '1,/^---PRINCIPLES---$/p' | sed '$d')
        EXPECTED_PRINCIPLES=$(echo "$TEST_DATA" | sed -n '/^---PRINCIPLES---$/,/^---FORBIDDEN---$/p' | head -2 | tail -1)
        FORBIDDEN=$(echo "$TEST_DATA" | sed -n '/^---FORBIDDEN---$/,$ p' | tail -1)

        # Build full prompt
        FULL_PROMPT="Check the following text for STE-Code compliance. Apply all 14 principles (P1-P14). Replace unapproved terms using the synonym table. Produce ONLY the corrected text with a compliance summary.

$INPUT"

        # Run benchmark
        START_NS=$(python3 -c "import time; print(int(time.time() * 1e9))")
        OUTPUT=$(hermes -z "$FULL_PROMPT" -m deepseek-v4-pro --yolo 2>&1 || echo "HERMES_ERROR")
        END_NS=$(python3 -c "import time; print(int(time.time() * 1e9))")
        LATENCY_MS=$(( (END_NS - START_NS) / 1000000 ))

        # Save output
        echo "$OUTPUT" > "$RUN_DIR/${TEST_ID}-output.txt"

        # Score
        PRINCIPLES_FOUND=""; PRINCIPLES_MISSED=""; FORBIDDEN_FOUND=""
        CORRECTNESS=1.0

        for p in $(echo "$EXPECTED_PRINCIPLES" | tr ',' ' '); do
            # Simple heuristic: check if output mentions the principle or its keywords
            if echo "$OUTPUT" | grep -qi "$p"; then
                PRINCIPLES_FOUND="$PRINCIPLES_FOUND,$p"
            else
                PRINCIPLES_MISSED="$PRINCIPLES_MISSED,$p"
                CORRECTNESS=$(python3 -c "print(round($CORRECTNESS - 1.0/len('$EXPECTED_PRINCIPLES'.split(',')), 2))")
            fi
        done
        PRINCIPLES_FOUND="${PRINCIPLES_FOUND#,}"; PRINCIPLES_MISSED="${PRINCIPLES_MISSED#,}"

        for fw in $(echo "$FORBIDDEN" | tr ',' ' '); do
            if [ -n "$fw" ] && echo "$OUTPUT" | grep -qi "$fw"; then
                FORBIDDEN_FOUND="$FORBIDDEN_FOUND,$fw"
                CORRECTNESS=$(python3 -c "print(round(max(0, $CORRECTNESS - 0.1), 2))")
            fi
        done
        FORBIDDEN_FOUND="${FORBIDDEN_FOUND#,}"

        TEST_PASSED=false
        if python3 -c "exit(0 if $CORRECTNESS >= 0.7 else 1)" 2>/dev/null; then
            TEST_PASSED=true; PASSED=$((PASSED + 1))
            echo -e "${GREEN}PASS${NC} (score: $CORRECTNESS, ${LATENCY_MS}ms)"
        else
            FAILED=$((FAILED + 1))
            echo -e "${RED}FAIL${NC} (score: $CORRECTNESS, ${LATENCY_MS}ms)"
        fi

        # Track per-category (write to temp file)
        echo "$CATEGORY $TEST_PASSED $CORRECTNESS" >> "$CAT_TRACKING"

        # Write result to aggregate JSON
        if [ "$FIRST" = true ]; then FIRST=false; else echo "," >> "$RESULTS_JSON"; fi
        echo -n "    {\"test_id\": \"$TEST_ID\", \"category\": \"$CATEGORY\", \"correctness_score\": $CORRECTNESS, \"latency_ms\": $LATENCY_MS, \"passed\": $TEST_PASSED, \"principles_found\": \"$PRINCIPLES_FOUND\", \"principles_missed\": \"$PRINCIPLES_MISSED\", \"forbidden_found\": \"$FORBIDDEN_FOUND\"}" >> "$RESULTS_JSON"
    done
done

# Compute by-category breakdown using Python
python3 -c "
import json, collections

cat_data = collections.defaultdict(lambda: {'passed': 0, 'failed': 0, 'scores': []})
with open('$CAT_TRACKING') as f:
    for line in f:
        parts = line.strip().split(' ', 2)
        if len(parts) < 3:
            continue
        cat, passed, score = parts[0], parts[1], parts[2]
        if passed == 'true':
            cat_data[cat]['passed'] += 1
        else:
            cat_data[cat]['failed'] += 1
        cat_data[cat]['scores'].append(float(score))

print()
for cat in sorted(cat_data.keys()):
    d = cat_data[cat]
    avg = sum(d['scores']) / len(d['scores']) if d['scores'] else 0
    print(f'  Category {cat}: {d[\"passed\"]} passed, {d[\"failed\"]} failed, avg score: {avg:.2f}')
"

# Finalize aggregate JSON
echo "" >> "$RESULTS_JSON"
echo "  ]," >> "$RESULTS_JSON"
echo "  \"totals\": {\"passed\": $PASSED, \"failed\": $FAILED, \"pass_rate\": $(python3 -c "print(round($PASSED/$TOTAL_TESTS*100,1))")}" >> "$RESULTS_JSON"
echo "}" >> "$RESULTS_JSON"

echo ""
echo "============================================"
echo -e "BENCHMARK COMPLETE"
echo -e "Total: $TOTAL_TESTS | ${GREEN}Passed: $PASSED${NC} | ${RED}Failed: $FAILED${NC}"
echo -e "Pass rate: $(python3 -c "print(round($PASSED/$TOTAL_TESTS*100,1))")%"
echo "Results: $RUN_DIR/"
echo "Aggregate: $RESULTS_JSON"
