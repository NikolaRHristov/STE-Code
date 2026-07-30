#!/usr/bin/env bash
# STE-Code Benchmark Runner v1.1.0 — sequential execution, Python-scored, JSON-safe
# Usage: bash .agents/benchmark/run-benchmark.sh [--category readme] [--test bench-001] [--model deepseek-v4-pro] [--dry-run] [--timeout 300]
# Agent #4 benchmarking orchestrator — runs test cases through hermes -z with STE-Code system prompt
#
# ══════════════════════════════════════════════════════════════════════════════
# NOTE: This is the SEQUENTIAL runner. Each of 59 tests runs one at a time
# through a single hermes invocation. Wall-clock time is ~59× slower than the
# parallel orchestrator. For production benchmarking, use the Python orchestrator:
#     python3 .agents/benchmark/orchestrator.py
# See also: orchestrator-control.py for the plain-assistant control group.
# ══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

CATEGORY_FILTER=""
TEST_FILTER=""
MODEL="deepseek-v4-pro"
DRY_RUN=false
TEST_TIMEOUT=300   # max seconds per hermes invocation

usage() {
    cat <<EOF
Usage: bash .agents/benchmark/run-benchmark.sh [FLAGS]

FLAGS:
  --category NAME    Run only tests in category NAME (e.g. readme, commit, error)
  --test ID          Run only a single test by ID (e.g. bench-001)
  --model NAME       Override the model passed to hermes (default: deepseek-v4-pro)
  --timeout SECONDS  Maximum seconds per hermes invocation (default: 300)
  --dry-run          Load test cases and print what would run, but do not execute

NOTE: This runner is sequential. For parallel execution with 59 concurrent
      workers, use:  python3 .agents/benchmark/orchestrator.py
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --category)
            CATEGORY_FILTER="$2"
            shift 2
            ;;
        --test)
            TEST_FILTER="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        --timeout)
            TEST_TIMEOUT="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "ERROR: Unknown flag: $1"
            usage
            exit 1
            ;;
    esac
done

# ---------------------------------------------------------------------------
# Prelude — paths, colors, prerequisites
# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SYSTEM_PROMPT="$PROJECT_ROOT/ste-code/artifacts/ste-code-distilled-system-prompt.txt"
TEST_DIR="$SCRIPT_DIR/test-cases"
RESULTS_DIR="$SCRIPT_DIR/results"
PYTHON_SCORER="$SCRIPT_DIR/_score_helper.py"
TIMESTAMP=$(date -u +"%Y%m%d-%H%M%S")
RUN_DIR="$RESULTS_DIR/run-$TIMESTAMP"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

echo "=== STE-Code Benchmark Runner (Sequential) ==="
echo "Model: $MODEL"
echo "Timestamp: $TIMESTAMP"
echo ""

# ── Pre-flight: warn about sequential vs parallel ──
ORCHESTRATOR_PY="$SCRIPT_DIR/orchestrator.py"
if [ -f "$ORCHESTRATOR_PY" ]; then
    echo -e "${YELLOW}NOTE: This is the sequential runner. For parallel execution (59 concurrent${NC}"
    echo -e "${YELLOW}      workers, proper JSON output, resume support), use:${NC}"
    echo -e "${YELLOW}        python3 $ORCHESTRATOR_PY${NC}"
    echo ""
fi

# ── Pre-flight: verify prerequisites ──
if [ ! -f "$SYSTEM_PROMPT" ]; then
    echo -e "${RED}ERROR: System prompt not found at $SYSTEM_PROMPT${NC}"
    exit 1
fi
echo -e "${GREEN}System prompt found${NC}"

if ! command -v hermes &>/dev/null; then
    echo -e "${RED}ERROR: hermes command not found in PATH${NC}"
    exit 1
fi
echo -e "${GREEN}hermes found: $(command -v hermes)${NC}"

if ! command -v python3 &>/dev/null; then
    echo -e "${RED}ERROR: python3 command not found in PATH${NC}"
    exit 1
fi
echo -e "${GREEN}python3 found: $(command -v python3)${NC}"

mkdir -p "$RUN_DIR"

# ── Pre-flight: validate test case JSON files ──
JSON_VALIDATION=$(python3 -c "
import json, glob, sys, os
test_dir = '$TEST_DIR'
files = sorted(glob.glob(os.path.join(test_dir, 'category-*.json')))
if not files:
    print('ERROR:no_files')
    sys.exit(1)
errors = []
for f in files:
    try:
        tests = json.load(open(f))
        if not isinstance(tests, list):
            errors.append(f'{os.path.basename(f)}: top-level must be a list')
            continue
        for t in tests:
            if not isinstance(t, dict):
                errors.append(f'{os.path.basename(f)}: each item must be a dict')
                continue
            if 'id' not in t:
                errors.append(f'{os.path.basename(f)}: missing \"id\" field')
            if 'expected_principles' not in t:
                errors.append(f'{os.path.basename(f)}/{t.get(\"id\",\"?\")}: missing \"expected_principles\"')
    except json.JSONDecodeError as e:
        errors.append(f'{os.path.basename(f)}: JSON parse error: {e}')
if errors:
    for e in errors:
        print(f'ERROR:{e}')
    sys.exit(1)
print('OK')
" 2>&1)
if [[ "$JSON_VALIDATION" != "OK" ]]; then
    echo -e "${RED}Test case validation failed:${NC}"
    echo "$JSON_VALIDATION"
    exit 1
fi
echo -e "${GREEN}All test case files are valid JSON${NC}"

# ---------------------------------------------------------------------------
# Cleanup trap — ensure partial results survive Ctrl+C
# ---------------------------------------------------------------------------

cleanup_partial() {
    echo ""
    echo -e "${YELLOW}Interrupted. Writing partial results...${NC}"
    # The aggregate JSON finalization happens in the trap if we are mid-run.
    # We write whatever we have collected so far.
    if [ -n "${RESULTS_JSON:-}" ] && [ -f "$RESULTS_JSON" ]; then
        python3 -c "
import json
with open('$RESULTS_JSON') as f:
    content = f.read()
# Append closing braces if incomplete
if not content.rstrip().endswith('}'):
    content = content.rstrip().rstrip(',')
    content += '\n  ]\n}'
    with open('$RESULTS_JSON', 'w') as f:
        f.write(content)
" 2>/dev/null || true
    fi
    echo "Partial results saved to $RUN_DIR/"
    exit 130
}
trap cleanup_partial INT TERM

# ---------------------------------------------------------------------------
# Write inline Python scoring helper (no external file dependency)
# ---------------------------------------------------------------------------

write_scoring_helper() {
    cat > "$PYTHON_SCORER" << 'PYEOF'
#!/usr/bin/env python3
"""STE-Code scoring helper — word-boundary grep, principle matching, JSON output."""
import json
import re
import sys

# Canonical principle-to-keyword mapping (mirrors orchestrator.py)
PRINCIPLE_KEYWORDS = {
    "P1":  ["approved word", "dictionary", "approved term", "approved vocabulary"],
    "P2":  ["part of speech", "noun", "verb", "adjective", "adverb", "preposition", "conjunction"],
    "P3":  ["approved meaning", "meaning", "definition", "defined sense", "single meaning"],
    "P4":  ["active voice", "passive voice", "imperative", "infinitive", "simple present", "simple past", "past participle"],
    "P5":  ["technical noun", "keyword", "framework", "library", "class name", "function name", "variable name"],
    "P6":  ["non-approved", "technical name", "technical term", "unapproved"],
    "P7":  ["noun as verb", "do not use noun as verb", "nominalization", "verbing"],
    "P8":  ["standard", "well-known", "recognized", "established term"],
    "P9":  ["short", "clear", "concise", "brief", "simple word"],
    "P10": ["slang", "jargon", "regional", "vague", "informal", "colloquial", "idiom"],
    "P11": ["one term", "consistent", "same term", "synonym", "do not use synonyms"],
    "P12": ["technical verb", "build", "deploy", "test", "lint", "compile", "debug", "install", "configure", "execute"],
    "P13": ["verb as noun", "do not use verb as noun", "gerund as noun"],
    "P14": ["american spelling", "american english", "color", "analyze", "organize", "standardize"],
}

def extract_compliance_section(output):
    """Extract compliance summary from output."""
    for marker in ['**Compliance Summary**', '## Compliance Summary', 'COMPLIANCE SUMMARY',
                   '# Compliance Summary', 'Compliance Summary']:
        if marker.startswith('**'):
            m = re.search(re.escape(marker) + r'\s*(.*)', output, re.DOTALL | re.IGNORECASE)
        else:
            m = re.search(marker + r'\s*\n(.*)', output, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() if m.lastindex else m.group(0)
    return ""

def check_principles(output, expected_principles):
    """Check principle coverage with word-boundary matching."""
    compliance = extract_compliance_section(output)
    full_lower = (compliance + " " + output).lower()

    satisfied = []
    missed = []

    for p in expected_principles:
        found = False
        # 1. Explicit principle number with word boundary in compliance
        if re.search(r'\b' + re.escape(p) + r'\b', compliance):
            found = True
        # 2. Keyword heuristics
        if not found and p in PRINCIPLE_KEYWORDS:
            for kw in PRINCIPLE_KEYWORDS[p]:
                if kw.lower() in full_lower:
                    found = True
                    break
        # 3. Principle number in full output
        if not found and re.search(r'\b' + re.escape(p) + r'\b', output):
            found = True

        if found:
            satisfied.append(p)
        else:
            missed.append(p)

    return satisfied, missed

def check_forbidden(text_lower, forbidden):
    """Check forbidden keywords with whole-word boundary matching."""
    found = []
    for fw in forbidden:
        if not fw.strip():
            continue
        # Use word boundary if the forbidden keyword is a single word (no spaces)
        if ' ' not in fw:
            if re.search(r'\b' + re.escape(fw) + r'\b', text_lower):
                found.append(fw)
        else:
            if fw.lower() in text_lower:
                found.append(fw)
    return found

def check_expected(text_lower, expected):
    """Check expected keywords (whole-word for single words, substring for phrases)."""
    found = []
    for ek in expected:
        if not ek.strip():
            continue
        if ' ' not in ek:
            if re.search(r'\b' + re.escape(ek) + r'\b', text_lower):
                found.append(ek)
        else:
            if ek.lower() in text_lower:
                found.append(ek)
    return found

def calc_correctness(expected_principles, satisfied, forbidden_found, total_forbidden,
                     expected_kw_found, total_expected_kw):
    """Weighted correctness score 0.0–1.0 (mirrors orchestrator.py)."""
    score = 0.4  # base
    if expected_principles:
        score += 0.6 * len(satisfied) / len(expected_principles)
    if total_forbidden > 0:
        score -= 0.3 * len(forbidden_found) / total_forbidden
    if total_expected_kw > 0:
        score += 0.1 * len(expected_kw_found) / total_expected_kw
    return round(max(0.0, min(1.0, score)), 2)

def extract_corrected_text(output):
    """Extract the corrected text from output."""
    for marker in [r'\*\*Corrected Text:\*\*', r'## Corrected Text', r'CORRECTED TEXT',
                   r'# Corrected Text', r'Corrected Text \(STE-Code Compliant\)',
                   r'# STE-Code Corrected Text']:
        m = re.search(marker + r'\s*\n+(.*?)(?:\n---\n|\n## Compliance|\n# Compliance|\nCOMPLIANCE|\n\*\*Compliance)', output, re.DOTALL | re.IGNORECASE)
        if m and m.group(1).strip():
            return m.group(1).strip()
    m = re.search(r'^(.*?)(?:\n---\n|\n#+\s*Compliance|\nCOMPLIANCE)', output, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
        text = re.sub(r'^#+\s*(?:Corrected|STE-Code).*?\n+', '', text, flags=re.IGNORECASE)
        if text:
            return text.strip()
    return output.strip()

# === Main scoring entry point ===
# Expects JSON on stdin: { "output": "...", "expected_principles": [...], "forbidden_keywords": [...],
#                          "expected_keywords": [...] }
# Returns JSON on stdout: { "satisfied": [...], "missed": [...], "forbidden_found": [...],
#                           "expected_found": [...], "correctness": 0.XX, "corrected_text": "..." }

if __name__ == "__main__":
    data = json.load(sys.stdin)
    output = data.get("output", "")
    expected_principles = data.get("expected_principles", [])
    forbidden = data.get("forbidden_keywords", [])
    expected_kw = data.get("expected_keywords", [])

    corrected = extract_corrected_text(output)
    corrected_lower = corrected.lower()

    satisfied, missed = check_principles(output, expected_principles)
    forbidden_found = check_forbidden(corrected_lower, forbidden)
    expected_found = check_expected(corrected_lower, expected_kw)

    correctness = calc_correctness(
        expected_principles, satisfied,
        forbidden_found, len(forbidden),
        expected_found, len(expected_kw)
    )

    result = {
        "satisfied": satisfied,
        "missed": missed,
        "forbidden_found": forbidden_found,
        "expected_found": expected_found,
        "correctness": correctness,
        "corrected_text": corrected,
    }
    print(json.dumps(result))
PYEOF
    chmod +x "$PYTHON_SCORER"
}
write_scoring_helper

# ---------------------------------------------------------------------------
# Load and filter test cases (read JSON once per category, not once per test)
# ---------------------------------------------------------------------------

# Build a flattened test list via Python — applies --category and --test filters
TEST_LIST=$(python3 -c "
import json, glob, sys, os

test_dir = '$TEST_DIR'
cat_filter = '$CATEGORY_FILTER'.strip()
test_filter = '$TEST_FILTER'.strip()

tests = []
for cat_file in sorted(glob.glob(os.path.join(test_dir, 'category-*.json'))):
    with open(cat_file) as f:
        cat_tests = json.load(f)
    cat_basename = os.path.basename(cat_file)
    category = cat_basename.replace('category-', '', 1)
    # Strip leading digit prefix: '1-readme' -> 'readme'
    import re as _re
    category = _re.sub(r'^\d+-', '', category)
    category = category.replace('.json', '')
    for t in cat_tests:
        t['_category'] = category
        t['_file'] = cat_file
        tests.append(t)

# Apply filters
if cat_filter:
    tests = [t for t in tests if t['_category'] == cat_filter]
if test_filter:
    tests = [t for t in tests if t['id'] == test_filter]

if not tests:
    print('NO_TESTS')
    sys.exit(0)

for t in tests:
    is_gen = 'prompt' in t
    print(f\"{t['id']}|{t['_category']}|{t['_file']}|{'gen' if is_gen else 'corr'}|{t.get('description','')}\")
")

if [ "$TEST_LIST" = "NO_TESTS" ]; then
    echo -e "${YELLOW}No test cases matched the given filters.${NC}"
    echo "Available categories:"
    python3 -c "
import json, glob, os, re
test_dir = '$TEST_DIR'
cats = set()
for f in sorted(glob.glob(os.path.join(test_dir, 'category-*.json'))):
    cat = os.path.basename(f).replace('category-', '').replace('.json', '')
    cat = re.sub(r'^\d+-', '', cat)
    cats.add(cat)
for c in sorted(cats):
    print(f'  {c}')
"
    exit 0
fi

TOTAL_TESTS=$(echo "$TEST_LIST" | wc -l | tr -d ' ')
echo "Test cases loaded: $TOTAL_TESTS"
if [ -n "$CATEGORY_FILTER" ]; then
    echo -e "${CYAN}  Filtered by category: $CATEGORY_FILTER${NC}"
fi
if [ -n "$TEST_FILTER" ]; then
    echo -e "${CYAN}  Filtered by test: $TEST_FILTER${NC}"
fi
echo ""

if $DRY_RUN; then
    echo -e "${CYAN}DRY RUN — no hermes invocations will be made.${NC}"
    echo "Tests that would run:"
    echo "$TEST_LIST" | while IFS='|' read -r tid cat file typ desc; do
        echo "  [$tid] $cat ($typ) — $desc"
    done
    echo ""
    echo "Would run $TOTAL_TESTS tests with --model=$MODEL"
    rm -f "$PYTHON_SCORER"
    exit 0
fi

# ---------------------------------------------------------------------------
# Initialize aggregate results (Python-built JSON — safe, no echo hacking)
# ---------------------------------------------------------------------------

PASSED=0; FAILED=0; TIMED_OUT=0; ERRORS=0
CAT_TRACKING="$RUN_DIR/.cat_tracking"
> "$CAT_TRACKING"
RESULTS_JSON="$RUN_DIR/aggregate-results.json"
RESULTS_ENTRIES="["   # we build entries array via Python at the end

# ---------------------------------------------------------------------------
# Pre-read all test case data into a Python lookup (one JSON parse per category)
# ---------------------------------------------------------------------------

# We store processed results as newline-delimited JSON (NDJSON) for final assembly.
NDJSON_FILE="$RUN_DIR/.results.ndjson"
> "$NDJSON_FILE"

# ---------------------------------------------------------------------------
# Run each test sequentially
# ---------------------------------------------------------------------------

TEST_INDEX=0
START_WALL_NS=$(python3 -c "import time; print(int(time.time() * 1e9))")

while IFS='|' read -r TEST_ID CATEGORY CAT_FILE TEST_TYPE TEST_DESC; do
    TEST_INDEX=$((TEST_INDEX + 1))

    # Compute ETA for progress display
    if [ $TEST_INDEX -gt 1 ]; then
        ELAPSED_S=$(( ( $(python3 -c "import time; print(int(time.time() * 1e9))") - START_WALL_NS ) / 1000000000 ))
        AVG_PER_TEST=$(( ELAPSED_S / (TEST_INDEX - 1) ))
        REMAINING=$(( TOTAL_TESTS - TEST_INDEX + 1 ))
        ETA_S=$(( AVG_PER_TEST * REMAINING ))
        ETA_STR=" (ETA: ${ETA_S}s)"
    else
        ETA_STR=""
    fi

    echo -n "  [$TEST_INDEX/$TOTAL_TESTS] $TEST_ID ($CATEGORY)... ${ETA_STR} "

    # Extract test case data via Python (single read from the category file)
    TEST_DATA=$(python3 -c "
import json
with open('$CAT_FILE') as f:
    tests = json.load(f)
t = next(t for t in tests if t['id'] == '$TEST_ID')
is_gen = 'prompt' in t
task = t.get('prompt', t.get('input', ''))
print(json.dumps({
    'input': task,
    'expected_principles': t['expected_principles'],
    'forbidden_keywords': t.get('forbidden_keywords', []),
    'expected_keywords': t.get('expected_keywords', []),
    'is_generation': is_gen,
    'difficulty': t.get('difficulty', 'unknown'),
    'max_tokens': t.get('max_tokens', 0),
}))
")

    INPUT=$(echo "$TEST_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin)['input'])")
    EXPECTED_PRINCIPLES=$(echo "$TEST_DATA" | python3 -c "import json,sys; print(','.join(json.load(sys.stdin)['expected_principles']))")
    FORBIDDEN=$(echo "$TEST_DATA" | python3 -c "import json,sys; print(','.join(json.load(sys.stdin)['forbidden_keywords']))")
    EXPECTED_KW=$(echo "$TEST_DATA" | python3 -c "import json,sys; print(','.join(json.load(sys.stdin)['expected_keywords']))")
    IS_GEN=$(echo "$TEST_DATA" | python3 -c "import json,sys; print(str(json.load(sys.stdin)['is_generation']).lower())")
    DIFFICULTY=$(echo "$TEST_DATA" | python3 -c "import json,sys; print(json.load(sys.stdin)['difficulty'])")

    # Build full prompt
    if [ "$IS_GEN" = "true" ]; then
        FULL_PROMPT="$(cat "$SYSTEM_PROMPT")

## TASK
$INPUT

IMPORTANT: Do NOT create any files. Output all code and documentation inline as text.
Use STE-Code principles (P1-P14) for all documentation and text you generate.
Apply the synonym table for all word choices.
Produce the requested output first, then a compliance summary table showing which principles you followed."
    else
        FULL_PROMPT="$(cat "$SYSTEM_PROMPT")

## TASK
Check the following text for STE-Code compliance. Apply all 14 principles (P1-P14). 
Replace unapproved terms using the synonym table. 
IMPORTANT: Do NOT create any files. Output the corrected text inline.
Produce the corrected text first, then a compliance summary table.

## TEXT TO CORRECT
$INPUT"
    fi

    # Save prompt for debugging
    echo "$FULL_PROMPT" > "$RUN_DIR/${TEST_ID}-prompt.txt"

    # ── Run benchmark with timeout, separate stdout/stderr ──
    START_NS=$(python3 -c "import time; print(int(time.time() * 1e9))")

    # Use a temp file for stdout, another for stderr
    STDOUT_FILE="$RUN_DIR/${TEST_ID}-stdout.txt"
    STDERR_FILE="$RUN_DIR/${TEST_ID}-stderr.txt"

    HERMES_EXIT_CODE=0
    if command -v timeout &>/dev/null; then
        timeout "$TEST_TIMEOUT" hermes -z "$FULL_PROMPT" -m "$MODEL" --yolo \
            >"$STDOUT_FILE" 2>"$STDERR_FILE" || HERMES_EXIT_CODE=$?
    else
        # macOS does not have `timeout` — use perl as fallback
        perl -e "alarm $TEST_TIMEOUT; exec @ARGV" -- hermes -z "$FULL_PROMPT" -m "$MODEL" --yolo \
            >"$STDOUT_FILE" 2>"$STDERR_FILE" || HERMES_EXIT_CODE=$?
    fi

    END_NS=$(python3 -c "import time; print(int(time.time() * 1e9))")
    LATENCY_MS=$(( (END_NS - START_NS) / 1000000 ))

    # Check for timeout (exit code 124 from `timeout`, 142 from perl alarm)
    IS_TIMED_OUT=false
    if [ "$HERMES_EXIT_CODE" -eq 124 ] || [ "$HERMES_EXIT_CODE" -eq 142 ]; then
        IS_TIMED_OUT=true
    fi

    # Merge stdout and stderr for scoring, but keep them separate on disk
    OUTPUT=$(cat "$STDOUT_FILE" 2>/dev/null || true)
    STDERR_OUTPUT=$(cat "$STDERR_FILE" 2>/dev/null || true)
    COMBINED_OUTPUT="${OUTPUT}
${STDERR_OUTPUT}"

    # Check if output is empty or an error
    if [ -z "$OUTPUT" ] && [ -z "$STDERR_OUTPUT" ]; then
        COMBINED_OUTPUT="HERMES_EMPTY_OUTPUT"
    fi

    # Save combined output
    echo "$COMBINED_OUTPUT" > "$RUN_DIR/${TEST_ID}-output.txt"

    # ── Score via the Python helper (word-boundary safe, JSON output) ──
    SCORE_JSON=$(echo "$COMBINED_OUTPUT" | python3 -c "
import json, sys
data = {
    'output': sys.stdin.read(),
    'expected_principles': '$EXPECTED_PRINCIPLES'.split(',') if '$EXPECTED_PRINCIPLES' else [],
    'forbidden_keywords': '$FORBIDDEN'.split(',') if '$FORBIDDEN' else [],
    'expected_keywords': '$EXPECTED_KW'.split(',') if '$EXPECTED_KW' else [],
}
print(json.dumps(data))
" | python3 "$PYTHON_SCORER" 2>/dev/null || echo '{"correctness": 0.0, "satisfied": [], "missed": [], "forbidden_found": [], "expected_found": [], "corrected_text": ""}')

    CORRECTNESS=$(echo "$SCORE_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['correctness'])")
    SATISFIED=$(echo "$SCORE_JSON" | python3 -c "import json,sys; p=json.load(sys.stdin); print(','.join(p['satisfied']) if p['satisfied'] else '')")
    MISSED=$(echo "$SCORE_JSON" | python3 -c "import json,sys; p=json.load(sys.stdin); print(','.join(p['missed']) if p['missed'] else '')")
    FOUND_FORBIDDEN=$(echo "$SCORE_JSON" | python3 -c "import json,sys; p=json.load(sys.stdin); print(','.join(p['forbidden_found']) if p['forbidden_found'] else '')")
    FOUND_EXPECTED=$(echo "$SCORE_JSON" | python3 -c "import json,sys; p=json.load(sys.stdin); print(','.join(p['expected_found']) if p['expected_found'] else '')")

    # ── Pass/fail ──
    TEST_PASSED=false
    PASSED_SCORE=0.7
    if python3 -c "exit(0 if $CORRECTNESS >= $PASSED_SCORE else 1)" 2>/dev/null; then
        TEST_PASSED=true
        PASSED=$((PASSED + 1))
        echo -e "${GREEN}PASS${NC} (score: $CORRECTNESS, ${LATENCY_MS}ms)"
    else
        FAILED=$((FAILED + 1))
        echo -e "${RED}FAIL${NC} (score: $CORRECTNESS, ${LATENCY_MS}ms)"
    fi

    # Track timed-out tests
    if $IS_TIMED_OUT; then
        TIMED_OUT=$((TIMED_OUT + 1))
    fi

    # Track errors (hermes crash)
    if echo "$COMBINED_OUTPUT" | head -1 | grep -qi "HERMES_EMPTY\|HERMES_ERROR\|Traceback"; then
        ERRORS=$((ERRORS + 1))
    fi

    # Track per-category
    echo "$CATEGORY $TEST_PASSED $CORRECTNESS $LATENCY_MS" >> "$CAT_TRACKING"

    # Write NDJSON entry for final assembly
    python3 -c "
import json, sys
entry = {
    'test_id': '$TEST_ID',
    'category': '$CATEGORY',
    'description': '$TEST_DESC',
    'test_type': 'generation' if '$IS_GEN' == 'true' else 'correction',
    'difficulty': '$DIFFICULTY',
    'correctness_score': $CORRECTNESS,
    'latency_ms': $LATENCY_MS,
    'passed': $TEST_PASSED,
    'timed_out': $IS_TIMED_OUT,
    'principles_satisfied': '$SATISFIED'.split(',') if '$SATISFIED' else [],
    'principles_missed': '$MISSED'.split(',') if '$MISSED' else [],
    'forbidden_found': '$FOUND_FORBIDDEN'.split(',') if '$FOUND_FORBIDDEN' else [],
    'expected_found': '$FOUND_EXPECTED'.split(',') if '$FOUND_EXPECTED' else [],
}
with open('$NDJSON_FILE', 'a') as f:
    f.write(json.dumps(entry) + '\n')
"

done <<< "$TEST_LIST"

# ---------------------------------------------------------------------------
# Compute by-category breakdown
# ---------------------------------------------------------------------------

echo ""
echo "--- Category Breakdown ---"

python3 -c "
import collections

cat_data = collections.defaultdict(lambda: {'passed': 0, 'failed': 0, 'scores': [], 'latencies': []})
with open('$CAT_TRACKING') as f:
    for line in f:
        parts = line.strip().split(' ')
        if len(parts) < 4:
            continue
        cat, passed, score, latency = parts[0], parts[1], parts[2], parts[3]
        if passed == 'true':
            cat_data[cat]['passed'] += 1
        else:
            cat_data[cat]['failed'] += 1
        cat_data[cat]['scores'].append(float(score))
        cat_data[cat]['latencies'].append(int(latency))

for cat in sorted(cat_data.keys()):
    d = cat_data[cat]
    total = d['passed'] + d['failed']
    avg = sum(d['scores']) / len(d['scores']) if d['scores'] else 0
    avg_lat = sum(d['latencies']) / len(d['latencies']) if d['latencies'] else 0
    pct = round(d['passed'] / total * 100, 1) if total else 0
    print(f'  {cat:<15} {total:>3} tests | {d[\"passed\"]:>2} passed, {d[\"failed\"]:>2} failed | avg score: {avg:.2f} | avg latency: {int(avg_lat)}ms')
"

# ---------------------------------------------------------------------------
# Finalize aggregate JSON (Python-built, guaranteed valid)
# ---------------------------------------------------------------------------

END_WALL_NS=$(python3 -c "import time; print(int(time.time() * 1e9))")
WALL_TIME_MS=$(( (END_WALL_NS - START_WALL_NS) / 1000000 ))

python3 << PYEOF
import json
from datetime import datetime, timezone

# Load NDJSON entries
entries = []
with open('$NDJSON_FILE') as f:
    for line in f:
        line = line.strip()
        if line:
            entries.append(json.loads(line))

# Build aggregate
all_scores = [e['correctness_score'] for e in entries]
all_latencies = [e['latency_ms'] for e in entries]

# Category stats
from collections import defaultdict
cat_stats = defaultdict(lambda: {'passed': 0, 'failed': 0, 'scores': [], 'latencies': []})
for e in entries:
    cat = e['category']
    if e['passed']:
        cat_stats[cat]['passed'] += 1
    else:
        cat_stats[cat]['failed'] += 1
    cat_stats[cat]['scores'].append(e['correctness_score'])
    cat_stats[cat]['latencies'].append(e['latency_ms'])

by_category = {}
for cat in sorted(cat_stats.keys()):
    d = cat_stats[cat]
    total = d['passed'] + d['failed']
    by_category[cat] = {
        'total': total,
        'passed': d['passed'],
        'failed': d['failed'],
        'pass_rate_pct': round(d['passed'] / total * 100, 1) if total else 0,
        'avg_correctness': round(sum(d['scores']) / len(d['scores']), 3) if d['scores'] else 0,
        'avg_latency_ms': round(sum(d['latencies']) / len(d['latencies'])) if d['latencies'] else 0,
    }

# Difficulty stats
diff_stats = defaultdict(lambda: {'passed': 0, 'failed': 0, 'scores': []})
for e in entries:
    d = e.get('difficulty', 'unknown')
    if e['passed']:
        diff_stats[d]['passed'] += 1
    else:
        diff_stats[d]['failed'] += 1
    diff_stats[d]['scores'].append(e['correctness_score'])

by_difficulty = {}
for diff in ['easy', 'medium', 'hard']:
    if diff in diff_stats:
        ds = diff_stats[diff]
        total = ds['passed'] + ds['failed']
        by_difficulty[diff] = {
            'total': total,
            'passed': ds['passed'],
            'failed': ds['failed'],
            'pass_rate_pct': round(ds['passed'] / total * 100, 1) if total else 0,
            'avg_correctness': round(sum(ds['scores']) / len(ds['scores']), 3) if ds['scores'] else 0,
        }

# Worker outcome counts
outcome_counts = defaultdict(int)
for e in entries:
    if e.get('timed_out'):
        outcome_counts['TIMEOUT'] += 1
    elif e['correctness_score'] == 0.0 and not e['passed']:
        outcome_counts['CRASH'] += 1
    elif e['correctness_score'] == 0.0:
        outcome_counts['EMPTY'] += 1
    else:
        outcome_counts['SUCCESS'] += 1

passed_count = sum(1 for e in entries if e['passed'])
failed_count = len(entries) - passed_count

aggregate = {
    'benchmark_id': 'ste-code-v1.1.0',
    'runner': 'sequential (shell)',
    'timestamp': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'model': '$MODEL',
    'total_tests': len(entries),
    'passed': passed_count,
    'failed': failed_count,
    'timed_out': $TIMED_OUT,
    'errors': $ERRORS,
    'pass_rate_pct': round(passed_count / len(entries) * 100, 1) if entries else 0,
    'wall_time_ms': $WALL_TIME_MS,
    'aggregates': {
        'avg_correctness': round(sum(all_scores) / len(all_scores), 3) if all_scores else 0,
        'min_correctness': min(all_scores) if all_scores else 0,
        'max_correctness': max(all_scores) if all_scores else 0,
        'avg_latency_ms': round(sum(all_latencies) / len(all_latencies)) if all_latencies else 0,
        'min_latency_ms': min(all_latencies) if all_latencies else 0,
        'max_latency_ms': max(all_latencies) if all_latencies else 0,
    },
    'worker_outcomes': dict(outcome_counts),
    'by_category': by_category,
    'by_difficulty': by_difficulty,
    'failures': [e for e in entries if not e['passed']],
    'results': entries,
    'recommendations': [],
}

# Add recommendations
if aggregate['aggregates']['avg_correctness'] < 0.7:
    aggregate['recommendations'].append(
        'System prompt needs improvement — avg correctness below 0.7'
    )
if aggregate['aggregates']['avg_latency_ms'] > 5000:
    aggregate['recommendations'].append(
        'Latency above 5s average — consider flash model for simple cases'
    )
for cat, data in aggregate['by_category'].items():
    if data['avg_correctness'] < 0.6:
        aggregate['recommendations'].append(
            f"Category '{cat}' underperforming (avg {data['avg_correctness']}) — review test design or prompt coverage"
        )
if $TIMED_OUT > len(entries) * 0.1:
    aggregate['recommendations'].append(
        f"{$TIMED_OUT} tests timed out — increase --timeout or simplify test inputs"
    )

with open('$RESULTS_JSON', 'w') as f:
    json.dump(aggregate, f, indent=2)
PYEOF

# ---------------------------------------------------------------------------
# Print final report
# ---------------------------------------------------------------------------

echo ""
echo "============================================"
echo "  STE-CODE BENCHMARK COMPLETE (Sequential)"
echo "============================================"
echo -e "  Total:    $TOTAL_TESTS"
echo -e "  ${GREEN}Passed:   $PASSED${NC}"
echo -e "  ${RED}Failed:   $FAILED${NC}"
if [ "$TIMED_OUT" -gt 0 ]; then
    echo -e "  ${YELLOW}Timed out: $TIMED_OUT${NC}"
fi
if [ "$ERRORS" -gt 0 ]; then
    echo -e "  ${RED}Errors:   $ERRORS${NC}"
fi
echo -e "  Pass rate: $(python3 -c "print(round($PASSED/$TOTAL_TESTS*100,1))")%"
echo -e "  Wall time: ${WALL_TIME_MS}ms ($(python3 -c "print(round($WALL_TIME_MS/1000,1))")s)"
echo ""
echo "  Run directory: $RUN_DIR/"
echo "  Aggregate:     $RESULTS_JSON"
echo "  Per-test outputs: $RUN_DIR/<test-id>-output.txt"
echo "  Per-test stderr:  $RUN_DIR/<test-id>-stderr.txt"
echo ""

# ── Hint: use the Python orchestrator for parallel runs ──
if [ "$TOTAL_TESTS" -gt 5 ] && [ -f "$ORCHESTRATOR_PY" ]; then
    PARALLEL_ESTIMATE=$(( WALL_TIME_MS / TOTAL_TESTS ))
    echo -e "${YELLOW}💡 Tip: This run took ${WALL_TIME_MS}ms for $TOTAL_TESTS tests."
    echo -e "   The Python orchestrator runs all tests in parallel (~${PARALLEL_ESTIMATE}ms). Run it with:"
    echo -e "     python3 $ORCHESTRATOR_PY${NC}"
    echo ""
fi

# Cleanup temporary scorer
rm -f "$PYTHON_SCORER"

echo "Done."
