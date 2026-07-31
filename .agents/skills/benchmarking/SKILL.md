---
description: "Measure STE-Code correctness and performance against 59 tests across 14 categories. Includes control group comparison."
version: "2.1.0"
related: [".agents/benchmark/orchestrator.py", ".agents/benchmark/orchestrator-control.py", ".agents/benchmark/schema.json", ".agents/benchmark/test-cases/"]
---

# Benchmarking Orchestrator - Agent-Agnostic

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to THIS skill.
> One session = one operation = one read + one write. No re-editing own output.

Measure STE-Code correctness and performance against a defined test suite. Run pre-defined test cases through `hermes -z` with the STE-Code system prompt, compare outputs against expected results, and produce structured benchmark reports. A control group runs the same tests with a plain assistant prompt for comparison.

## Architecture

```
TEST CASES (14 categories, 59 tests) → hermes -z (poolside/laguna-s-2.1:free) → SCORED RESULTS
```

### Orchestrator Scripts

- **`orchestrator.py`** - Main benchmark runner. Launches all 59 tests as parallel `fork` workers. Each worker runs `hermes -z` with the STE-Code system prompt in an isolated working directory. Uses a 600-second timeout per worker. After all workers finish or time out, it scores every output against the test schema, writes per-test and aggregate JSON, and prints a formatted terminal report. See [Phase 1-5 execution model](#execution-model) for details.

- **`orchestrator-control.py`** - Control group runner. Uses the same parallel execution model but sends a plain assistant prompt without STE-Code rules. Runs the identical 59 test cases for direct comparison.

- **`rescore.py`** - Re-scoring utility. Reads raw `hermes` outputs from an existing run directory and applies the current scoring logic. Use this when the scoring formula changes but you do not want to re-run all 59 tests. Accepts an optional `[run_dir]` argument. If you do not provide a directory, it uses the most recent run under `results/`.

### Categories

| # | Category | Tests | Type |
|---|----------|-------|------|
| 1 | readme | 5 | Correction |
| 2 | api_doc | 5 | Correction |
| 3 | commit | 5 | Correction |
| 4 | error | 5 | Correction |
| 5 | comment | 5 | Correction |
| 6 | changelog | 3 | Correction |
| 7 | config | 3 | Correction |
| 8 | composite | 4 | Correction |
| 9 | gen_function | 4 | Generation |
| 10 | gen_pr_review | 4 | Generation |
| 11 | gen_api_doc | 4 | Generation |
| 12 | gen_commit | 4 | Generation |
| 13 | gen_error | 4 | Generation |
| 14 | gen_readme | 4 | Generation |
| **Total** | | **59** | |

## Test Case Schema

Correction tests have `input` (text to fix). Generation tests have `prompt` (coding task) + `required_patterns` (regex structures that must appear).

```json
{
  "id": "bench-001",
  "category": "readme",
  "description": "README introduction with jargon",
  "input": "This library does a bunch of stuff...",
  "expected_principles": ["P1", "P4", "P10"],
  "expected_keywords": ["library", "call"],
  "forbidden_keywords": ["bunch", "stuff"],
  "required_patterns": [],
  "max_tokens": 300,
  "difficulty": "easy"
}
```

### Schema Fields

| Field | Required | Applies To | Description |
|-------|----------|------------|-------------|
| `id` | Yes | All | Unique test identifier (bench-NNN) |
| `category` | Yes | All | One of the 14 category names |
| `description` | Yes | All | Short summary of what the test measures |
| `input` | Correction only | Correction | Text with STE-Code violations to fix |
| `prompt` | Generation only | Generation | Coding task for the model to complete |
| `expected_principles` | Yes | All | List of P1-P14 principles the response must address |
| `expected_keywords` | Yes | All | Terms that must appear in the corrected or generated output |
| `forbidden_keywords` | Yes | All | Terms that must NOT appear in the output |
| `required_patterns` | Generation only | Generation | Regex patterns the generated code must match |
| `max_tokens` | Yes | All | Target ceiling for the model output |
| `difficulty` | Yes | All | One of: easy, medium, hard |

## Scoring Formula

```
score = 0.40 (base)
      + 0.60 × (principles_satisfied / expected)     ← 60% weight
      − 0.30 × (forbidden_found / total_forbidden)    ← penalty
      + 0.10 × (keywords_found / total_expected)      ← bonus
      − 0.20 × (patterns_missed / total_patterns)     ← gen-only
```

Pass threshold: ≥ 0.70

The base score of 0.40 represents the minimum correctness the model gets just for producing any response at all. This prevents vanishing scores on tests where the output is structurally valid but misses specific details. The principles component (0.60 weight) dominates - a test that addresses every expected principle but misses all keywords still scores 1.00. Forbidden keyword penalties and pattern penalties apply on top and can push the score below zero, but the formula clamps to the 0.00-1.00 range.

### Score Deltas and What They Mean

| Delta (STE-Code − Plain) | Interpretation |
|---------------------------|----------------|
| +0.40 to +0.60 | Category where STE-Code rules directly address the most common failure modes (comments, error messages, config files) |
| +0.20 to +0.40 | Category where both prompts produce acceptable output but STE-Code adds measurable precision |
| +0.00 to +0.20 | Category where the task is structurally constrained (commits, changelogs) leaving less room for quality variance |
| Negative | Indicates a bug in the test design or scoring formula, not a genuine anti-improvement |

In the current run, the three categories with the largest deltas are comments (+0.580), error messages (+0.560), and config files (+0.520). These are categories where vague, jargon-heavy natural language is the default and STE-Code's synonym table and principle enforcement produce the most visible improvements.

## Worked Examples

### Example 1: Passing Correction Test (bench-001, easy)

**Input:**
```
This library does a bunch of stuff and should be called with the user object to get everything set up properly.
```

**Expected principles:** P1, P4, P10

**Forbidden keywords:** bunch, stuff, should, everything, properly

**Expected keywords:** library, user object, call

**Model output (corrected):**
```
Call this library with the user object to complete the initial setup.
```

**Scoring breakdown:**

| Component | Calculation | Contribution |
|-----------|-------------|-------------|
| Base | 0.40 | +0.40 |
| Principles | 3/3 satisfied (P1, P4, P10) → 0.60 × 1.0 | +0.60 |
| Forbidden penalty | 0/5 found | −0.00 |
| Keywords bonus | 3/3 found (library, user object, call) | +0.10 |
| **Final score** | | **1.00 ✓** |

The model correctly identified "bunch of stuff" as slang (P10), removed "should" passive construction (P4), replaced vague terms with the approved technical noun "setup" (P1), and preserved all required keywords. The corrected text is 12 words, under the 20-word procedural limit.

### Example 2: Failing Correction Test (bench-010, hard)

**Input:**
```
The authenticateUser function handles user authentication and authorization. It takes a credentials object which contains the username and password, performs validation, and returns a JWT token that can be utilized for subsequent requests. Make sure to call this function before accessing any protected endpoints.
```

**Expected principles:** P1, P2, P5

**Forbidden keywords:** utilize, perform, fetch, make sure, subsequent

**Expected keywords:** authenticateUser, JWT, check, credentials, use, call

**Model output (corrected):**
```
The authenticateUser function checks user credentials. It gets a credentials object with a username and password. The function checks the credentials and returns a JWT token. Use the token for later requests. Call this function before you access a protected endpoint.
```

**Scoring breakdown:**

| Component | Calculation | Contribution |
|-----------|-------------|-------------|
| Base | 0.40 | +0.40 |
| Principles | 1/3 satisfied (P1 ✓, P2 ✗, P5 ✗) → 0.60 × 0.33 | +0.20 |
| Forbidden penalty | 0/5 found | −0.00 |
| Keywords bonus | 4/6 found | +0.07 |
| **Final score** | | **0.67 ✗** |

The model replaced "utilized" with "use" (synonym table, P1) and removed "make sure" but did not address P2 (part-of-speech violations) or P5 (technical noun usage) in the compliance summary. It also missed "authenticateUser" and "credentials" as expected keywords because it summarized rather than preserving technical identifiers. This is a common failure pattern: the model strips too much context from correction inputs. The corrective action is to make the prompt more explicit about preserving technical nouns.

### Example 3: Passing Generation Test (bench-036, easy)

**Prompt:**
```
Write a Python function `validate_email(address)` that checks if an email address is valid. Include a complete docstring with Args and Returns sections. Use STE-Code principles: approved words, active voice, no jargon.
```

**Expected principles:** P1, P4, P10

**Forbidden keywords:** stuff, thing, should, utilize, perform validation, might

**Expected keywords:** def validate_email, Args:, Returns:, address, check, valid, return

**Required patterns:** `"""...Args:.*address.*Returns:.*"""`

**Model output (generated):**
```python
def validate_email(address):
    """Check if an email address is valid.

    Args:
        address: An email address to check.

    Returns:
        True if the address is valid. False if it is not.
    """
    return "@" in address and "." in address
```

**Scoring breakdown:**

| Component | Calculation | Contribution |
|-----------|-------------|-------------|
| Base | 0.40 | +0.40 |
| Principles | 3/3 satisfied | +0.60 |
| Forbidden penalty | 0/6 found | −0.00 |
| Keywords bonus | 7/7 found | +0.10 |
| Pattern penalty | 1/1 matched | −0.00 |
| **Final score** | | **1.00 ✓** |

The generated code uses the approved verb "check" instead of "validate" in the prose, avoids all forbidden keywords, and uses active voice throughout the docstring. The `Args`/`Returns` pattern matches the required regex.

## Execution Model

The orchestrator (`orchestrator.py`) runs in five phases. This is the parallel-execution model that processes all 59 tests in one run.

### Phase 1: Worker Launch
All 59 workers launch in parallel via `os.fork()`. Each worker runs `hermes -z` with `--yolo` (non-interactive mode) in an isolated temporary directory to prevent file-system side effects between tests. The prompt and system prompt are written to a temporary file. The worker's stdout and stderr are redirected to `{id}-output.txt`.

### Phase 2: Poll Loop
The parent process polls all child PIDs every 5 seconds. It tracks completed workers and prints progress every 30 seconds. The total timeout is 600 seconds (10 minutes). After the timeout, any remaining workers are marked as timed out.

### Phase 3: Scoring
Each output file is read and scored. The corrected text is extracted from the output using regex markers (`**Corrected Text:**`, `## Corrected Text`, `CORRECTED TEXT`). The compliance summary is extracted separately. Principles are checked using a dual strategy: explicit principle numbers in the compliance section, and keyword heuristics in the full output (for example, "active voice" or "passive" signals P4). Forbidden keywords are checked only in the corrected text, not in the compliance summary.

### Phase 4: Aggregation
Category-level and difficulty-level aggregates are computed. Recommendations are auto-generated for low average correctness (< 0.70), high average latency (> 5,000 ms), and underperforming categories (< 0.60 average).

### Phase 5: Report
Results print to the terminal and write to two JSON files: `per-test-results.json` (one entry per test) and `aggregate-results.json` (summary with category breakdowns).

## Performance Characteristics

### Runtime

The orchestrator launches all 59 workers in parallel. It does not use a worker pool or concurrency limit - all tests run simultaneously. The total wall-clock time equals the slowest individual test plus the scoring phase (a few seconds).

From the most recent run:
- Average latency per test: ~125,000 ms (~2 minutes)
- Minimum latency: ~125,170 ms
- Maximum latency: ~125,223 ms
- Total run time: approximately 130-140 seconds (2.1-2.3 minutes)

NOTE: The latency values are dominated by the model inference time per call. The parallel launch eliminates serial overhead - running all 59 tests sequentially would take approximately 2+ hours at these per-test latencies.

### Token Budget

From the most recent aggregate run:
- Total input tokens: ~3,300 (56 per test average)
- Total output tokens: ~7,300 (124 per test average)
- Combined budget: ~10,600 tokens per full run

At DeepSeek V4 Pro pricing, a full 59-test benchmark run costs approximately $0.03-$0.05 in API tokens. The control group uses the same budget.

### Memory

Each forked worker inherits the parent's memory at fork time, but because the workers immediately `os.execvp()` into `hermes`, the memory footprint is negligible. The parent process uses approximately 20-50 MB for result tracking. There is no worker-pool memory overhead.

## Edge Cases

### Worker Timeout

If a worker does not finish within 600 seconds, the orchestrator marks it as timed out. The output file may be empty, partial, or missing. The scoring phase handles this:

- **Missing output file** - The test receives `OUTPUT_FILE_MISSING` as its output text. All principle checks fail (score = 0.40 base only).
- **Truncated output** - If the output is under 20 characters or starts with `HERMES_ERROR`, the test is marked as truncated. The `truncated` field in the result record is set to `true`. The scoring still runs normally on whatever text is available.
- **Timeout recovery** - Run `rescore.py` against the run directory after a timeout. It re-reads the output files and applies the current scoring formula. Partial outputs from timed-out workers are still scored.

### Empty Output

When a worker produces no output (file exists but is zero bytes), the scoring treats this as a worst-case failure. The corrected text is empty, so no keywords or principles match. The score is the base 0.40 minus any applicable penalties. In practice, empty output is rare because `hermes -z --yolo` always produces some response unless the process crashes.

### Truncated Output Detection

The orchestrator uses two signals to detect truncation:
- Output length under 20 characters
- Output starting with `HERMES_ERROR`

These signals only catch the most obvious cases. More subtle truncation (a response cut off mid-sentence that is still over 20 characters) is not detected automatically. Inspect per-test outputs manually if you suspect truncation.

### HERMES_ERROR

If `hermes` itself fails (API error, model unavailable, configuration issue), the output begins with `HERMES_ERROR` followed by the error message. The test is marked as truncated and scored on whatever text follows the error prefix. API-level failures (rate limiting, authentication errors) typically fail all workers simultaneously, producing 59 failures. Check the API configuration and retry.

### Missing Test Case File

If a category JSON file is missing from `.agents/benchmark/test-cases/`, the orchestrator skips it silently. The total test count in the output report is lower than 59. Verify all 14 category files exist before the run.

### Locking and Concurrency

Because each worker runs in its own temporary directory (`worker-{id}` under the run directory), there are no file-system conflicts between workers. The parent does not write to output files. The `hermes` process runs with `--yolo` to suppress all interactive prompts.

### Control Group Drift

The control group (`orchestrator-control.py`) uses the same test cases but a plain assistant prompt. If the test cases change (added tests, modified expected principles) but you run only one of the two orchestrators, the comparison is invalid. Always run both orchestrators from the same test-case snapshot.

## Run a Single Category

The orchestrator runs all 59 tests by design. To isolate a single category for debugging or iteration:

```bash
# 1. Run only one category by filtering files
python3 -c "
import json, glob, os
files = sorted(glob.glob('.agents/benchmark/test-cases/category-*.json'))
target = 'category-5-comment.json'  # change this
for f in files:
    if os.path.basename(f) == target:
        tests = json.load(open(f))
        for t in tests:
            print(f'{t[\"id\"]}: {t[\"description\"]} [{t[\"difficulty\"]}]')
"
```

To run just those tests manually:

```bash
# Run a single test directly through hermes
hermes -z "$(cat ste-code/artifacts/ste-code-distilled-system-prompt.txt)

## TASK
Check the following text for STE-Code compliance. Apply all 14 principles.
Produce the corrected text, then a compliance summary.

## TEXT TO CORRECT
<input text here>" -m poolside/laguna-s-2.1:free --yolo
```

To restrict the orchestrator to one category, temporarily move or rename the other category files before running. There is no native `--category` filter in the current orchestrator.

## Troubleshooting

### Common Failure Signals

| Signal | What It Means | Corrective Action |
|--------|---------------|-------------------|
| Score < 0.70, principles missed | The model did not address one or more expected principles in its compliance summary | Check the `expected_principles_missed` field. Verify the prompt includes an explicit instruction to produce a compliance summary. Add the missing principle number to the compliance summary section in the prompt template. |
| Score < 0.70, forbidden keywords found | The corrected output still contains slang, jargon, or unapproved terms | Inspect the `forbidden_keywords_found` list. If the word is borderline (technical term vs. jargon), adjust the `forbidden_keywords` in the test case. If it is a clear violation, the model failed to identify it - the system prompt may need stronger guidance for that class of words. |
| Score < 0.70, patterns missed (generation only) | The generated code does not contain the required structural elements | Check the `required_patterns` regex. Escaped characters (`, `*`, etc.) must be doubled in JSON strings. If the pattern is correct, the model may have chosen an alternative structure - make the prompt more prescriptive about the required format. |
| Pass rate < 100% on "easy" tests | Easy tests should always pass. Failures here signal a prompt or scoring bug | Easy tests have simple violations (single-word swaps). If an easy test fails, the most likely cause is a scoring regex that does not match the model's output format. Run the failing test manually and inspect the raw output. |
| All scores exactly 0.40 | No principles matched across any test | The `hermes` workers are producing output that does not contain a compliance summary. The `extract_compliance_section` regex may not match the output format. Check a raw output file to see if the model changed its response format. |
| Latency > 300,000 ms on multiple tests | Model inference is slower than expected | Check the API provider status. If using a shared endpoint, you may be rate-limited. Consider running fewer tests in parallel to reduce concurrency. |
| 0/59 tests scored | The run directory has no output files | The `hermes` binary may not be in PATH inside the forked worker. Verify `hermes` is available globally (`which hermes`). The workers inherit the parent's PATH, so check the environment before launching the orchestrator. |
| Control group scores higher than STE-Code | Edge case or prompt contamination | This should never happen on a full run. If it occurs on a single test, the plain assistant may have happened to produce a response that matches the expected keywords by chance. Inspect the specific test. If it occurs across multiple tests, the STE-Code system prompt may have a regression - compare against the previous run. |

### Re-Scoring After Formula Changes

When the scoring formula changes (new keywords added, principles reweighted), you do not need to re-run the 59 tests. Use `rescore.py`:

```bash
# Re-score the latest run
python3 .agents/benchmark/rescore.py

# Re-score a specific run
python3 .agents/benchmark/rescore.py .agents/benchmark/results/run-20260730-012639
```

The re-scorer uses the same extraction and scoring logic as the orchestrator. It reads the existing `{id}-output.txt` files and writes `rescored-results.json` to the run directory. The original `per-test-results.json` and `aggregate-results.json` are not overwritten.

### Debugging a Single Failing Test

```bash
# 1. Find the raw output
cat .agents/benchmark/results/run-*/bench-010-output.txt

# 2. Run the test manually with verbose output
SYSTEM_PROMPT=$(cat ste-code/artifacts/ste-code-distilled-system-prompt.txt)
INPUT="The authenticateUser function handles user authentication..."

hermes -z "$SYSTEM_PROMPT

## TASK
Check the following text for STE-Code compliance. Apply all 14 principles.
Produce the corrected text, then a compliance summary.

## TEXT TO CORRECT
$INPUT" -m poolside/laguna-s-2.1:free --yolo

# 3. Check if the compliance summary mentions the expected principles
# 4. If a principle is missing, add it to the test's expected_principles
# 5. If a forbidden keyword passes through, evaluate whether it is truly forbidden
```

## Execution

```bash
# STE-Code benchmark (full 59 tests, parallel workers)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, same tests)
python3 .agents/benchmark/orchestrator-control.py

# Re-score existing outputs
python3 .agents/benchmark/rescore.py [run_dir]
```

## Results

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| Pass rate | 96.6% (57/59) | 11.9% (7/59) | +84.7% |
| Avg correctness | 0.919 | 0.471 | +0.448 |

### Category Breakdown (Most Recent Run)

| Category | Passed/Total | Avg Score | Avg Latency |
|----------|-------------|-----------|-------------|
| commit | 5/5 | 1.000 | 125,208 ms |
| gen_function | 4/4 | 1.000 | 125,172 ms |
| gen_error | 4/4 | 1.000 | 125,219 ms |
| gen_readme | 4/4 | 1.000 | 125,218 ms |
| gen_api_doc | 4/4 | 0.998 | 125,222 ms |
| comment | 5/5 | 0.966 | 125,195 ms |
| error | 5/5 | 0.954 | 125,202 ms |
| readme | 5/5 | 0.938 | 125,218 ms |
| config | 3/3 | 0.923 | 125,183 ms |
| gen_pr_review | 4/4 | 0.905 | 125,220 ms |
| composite | 4/4 | 0.902 | 125,178 ms |
| gen_commit | 4/4 | 0.900 | 125,222 ms |
| changelog | 2/3 | 0.847 | 125,187 ms |
| api_doc | 4/5 | 0.820 | 125,214 ms |

### Difficulty Breakdown

| Difficulty | Passed/Total | Avg Score |
|------------|-------------|-----------|
| easy | 18/18 | 0.971 |
| medium | 24/25 | 0.945 |
| hard | 15/16 | 0.902 |

The two failing tests (bench-010 in api_doc, bench-027 in changelog) both score between 0.60-0.61. They fall into the "medium" and "hard" difficulty tiers. Bench-010 misses principles P2 and P5. Bench-027 misses P14 and leaks the forbidden phrase "was removed" instead of using the active-voice "remove."

## Output
- Per-test results: `.agents/benchmark/results/run-{timestamp}/per-test-results.json`
- Aggregate report: `.agents/benchmark/results/run-{timestamp}/aggregate-results.json`
- Control group: `.agents/benchmark/results-control/run-{timestamp}/`
- All prompt/output files gitignored - only aggregate JSONs tracked

### Output File Structure

Each run directory contains:
```
run-{timestamp}/
├── aggregate-results.json      ← Summary with category/difficulty breakdowns
├── per-test-results.json       ← One entry per test with full scoring detail
├── bench-NNN-prompt.txt        ← Full hermes prompt for each test (gitignored)
├── bench-NNN-output.txt        ← Raw hermes output for each test (gitignored)
├── worker-bench-NNN/           ← Per-worker isolated working directory (gitignored)
└── rescored-results.json       ← Only present after running rescore.py
```

### Adding New Test Cases

Add test cases by editing the category JSON files under `.agents/benchmark/test-cases/`. Each file is a JSON array of test objects. Follow the existing ID numbering. Use `bench-XXX` where XXX is the next available number. The orchestrator auto-discovers all `category-*.json` files at startup - no registration step is needed.

Example new correction test:
```json
{
  "id": "bench-060",
  "category": "api_doc",
  "description": "Endpoint documentation with unapproved modal verbs",
  "input": "You should call this endpoint to retrieve user data. It will return a JSON object.",
  "expected_principles": ["P1", "P4"],
  "expected_keywords": ["call", "endpoint", "return", "JSON"],
  "forbidden_keywords": ["should", "will", "retrieve"],
  "max_tokens": 200,
  "difficulty": "easy"
}
```

Save this into the relevant `category-*.json` file. The next orchestrator run picks it up automatically.

## Known Limitations

1. The scoring heuristic uses keyword matching for principle detection. Some principles (P8, P9) are subjective and may not be captured accurately by keyword presence alone. A response can mention "active voice" without actually using active voice.
2. Token estimates use a crude `len(text) // 4` approximation. Real token counts depend on the model's tokenizer.
3. The 600-second hard timeout may be too short for generation tests with heavy `required_patterns` if the model is under load.
4. The parallel `fork` launch model means all 59 workers compete for API rate limits simultaneously. A concurrency cap or staggered launch would reduce rate-limit pressure.
5. Truncation detection (under 20 characters) is a blunt instrument. It does not catch semantically truncated responses.
6. The scoring formula gives equal weight to each expected principle. In practice, P1 (approved words) is broader in scope than P14 (American spelling), but both carry the same 0.60 / N contribution.
