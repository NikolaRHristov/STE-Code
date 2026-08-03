---
name: level-worker
description: STE-Code skill — load when its trigger matches; see body for workflow.
category: dev
capability: developing-and-changing-the-standard
source: .agents/skills/level-worker
layout: ste-code-canonical-v1
---

# Level Worker Launcher — Agent-Agnostic

> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to
> THIS skill. One session = one operation = one read + one write. No re-editing
> own output.

Launch 4 parallel Agent #7 workers, each at a different STE-Code adaptation
level (1-4). Workers use the Hermes oneshot wrapper (`session_db=None`, no
history pollution, no tool access). Each worker rewrites the same set of
documents and outputs to its own isolated directory.

## Architecture

```
.agents/rewrites/
├── level-1/  ← 14 core principles only (~500 tokens)
├── level-2/  ← + dictionary excerpt (~5K tokens)
├── level-3/  ← + grammar rules (~20K tokens)
└── level-4/  ← + full dictionary (~50K tokens)
```

Each directory contains:

- `prompt.txt` — the full prompt sent to the LLM (gitignored)
- `output.txt` — the LLM's rewritten documents + compliance report (gitignored)

## Quick Start

Run this command from the project root:

```bash
python3 .agents/benchmark/launch-levels.py
```

The launcher writes output to `.agents/rewrites/level-{1,2,3,4}/output.txt`.
Check the results:

```bash
wc -l .agents/rewrites/level-*/output.txt
```

Each output file contains rewritten text, a change log, and a P1-P14 compliance
table for every target document.

## Agent #7 Role Contract

Agent #7 is a parameterized STE-Code worker. This skill is its full definition.

Key facts about the agent:

- Agent #7 receives `level` (1-5), `action` (test/rewrite/benchmark), and
  `target` parameters.
- It loads only the rule files for the specified level. Level 1 loads ~500
  tokens. Level 5 loads ~100K+ tokens.
- It produces three output sections per document: rewritten text, a change log,
  and a P1-P14 compliance table.
- The agent can rewrite its own Level 1 system prompt using Level 3 rules.
- Source files: `ste-code/artifacts/ste-code-distilled-system-prompt.txt` (Level
  1), `ste-code/adapted/a-dictionary.md` (Levels 2+4), and
  `ste-code/adapted/a-sec1-*` through `a-sec9-*` (Levels 3+).

The level worker launcher wraps Agent #7 in a Hermes oneshot subprocess. The
wrapper is at
[`.agents/tools/lib/hermes-oneshot-wrapper.py`](../../tools/hermes-oneshot-wrapper.py).
The wrapper:

- Reads a prompt from a temp file and deletes it after reading.
- Creates `AIAgent` with `session_db=None` and `tool_gen_callback=None`.
- Writes the LLM response to stdout, which the launcher captures into
  `output.txt`.
- Exits with code 0 on success or code 1 on failure (missing prompt file, import
  error, or API error).

### Agent #7 Capability Summary

| Capability      | Description                                                                                          |
| --------------- | ---------------------------------------------------------------------------------------------------- |
| Level selection | Loads rules at 1 of 5 adaptation depths                                                              |
| Actions         | `rewrite` (produce compliant text), `test` (find violations), `benchmark` (score against test cases) |
| Output sections | REWRITTEN (new text), CHANGES (diff table), COMPLIANCE (P1-P14 status)                               |
| Fallback levels | If rule files are missing at requested level, falls back to highest available level                  |
| Self-audit      | Can rewrite its own Level 1 prompt using Level 3+ rules                                              |
| Token budget    | Level 1: ~500, Level 2: ~5K, Level 3: ~20K, Level 4: ~50K, Level 5: ~100K+                           |

## Launch

```bash
python3 .agents/benchmark/launch-levels.py
```

This uses the canonical Hermes oneshot wrapper pattern:

1. Writes prompt to temp file
2. Launches
   `~/.hermes/hermes-agent/venv/bin/python3 hermes-oneshot-wrapper.py <prompt_file> --model poolside/laguna-s-2.1:free`
3. Workers run with `session_db=None` — no session pollution
4. Workers have `tool_gen_callback=None` — no file creation tools
5. Output captured to `output.txt` in each level directory

The launcher accepts these CLI flags:

```bash
python3 .agents/benchmark/launch-levels.py \
	--levels 1,2,3,4 \
	--docs README.md CONTRIBUTING.md \
	--model poolside/laguna-s-2.1:free \
	--output-dir .agents/rewrites \
	--timeout 900
```

| Flag           | Default                                                       | Description                          |
| -------------- | ------------------------------------------------------------- | ------------------------------------ |
| `--levels`     | `1,2,3,4`                                                     | Comma-separated level numbers to run |
| `--docs`       | README.md CONTRIBUTING.md CODE_OF_CONDUCT.md RELEASE-NOTES.md | Documents to rewrite                 |
| `--model`      | `poolside/laguna-s-2.1:free`                                  | LLM model name                       |
| `--output-dir` | `.agents/rewrites`                                            | Output root directory                |
| `--timeout`    | `900`                                                         | Timeout per worker in seconds        |

## Parameters

| Parameter | Values                                                           | Description                              |
| --------- | ---------------------------------------------------------------- | ---------------------------------------- |
| Level     | 1-4                                                              | Adaptation depth (5 not yet implemented) |
| Documents | README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, RELEASE-NOTES.md | Which docs to rewrite                    |
| Model     | poolside/laguna-s-2.1:free                                       | LLM model                                |

## Results Format

Each worker produces for every document:

1. `### REWRITTEN: <filename>` — The rewritten text
2. `### CHANGES: <filename>` — Change log with rule references
3. `### COMPLIANCE: <filename>` — P1-P14 compliance table

## Complete Output Example — Level 3 Rewrite of README.md

This section shows a full output. It comes from a real Level 3 run against the
project README.md. The output shows all three sections: REWRITTEN, CHANGES, and
COMPLIANCE.

```
### REWRITTEN: README.md

STE-Code applies the ASD-STE100 Simplified Technical English standard
to code documentation. The standard was first made for aerospace
maintenance documentation. STE-Code supplies 53 writing rules and
19 technical noun categories. It also supplies 4 technical verb
categories and a controlled vocabulary. The vocabulary removes
ambiguity, jargon, and hedging from READMEs, API documents, code
comments, commit messages, and error messages. All output is clear,
unambiguous, and machine-readable.

The standard was adapted from ASD-STE100 Issue 9 (January 2025).
It replaces the original aerospace terminology with code-domain
equivalents. The adaptation keeps the grammar, the controlled
vocabulary, and the procedural writing rules.

---

### CHANGES: README.md

| Change | Original | Rewritten | Rule |
|--------|----------|-----------|------|
| 1 | utilizes | applies | Synonym table (utilize→use→apply) |
| 2 | leverages | supplies | Synonym table (leverage→use→supply) |
| 3 | API docs | API documents | P3 — no abbreviations |
| 4 | makes your docs | All output is | P10 — no personal pronouns |
| 5 | performing the following | (removed) | P1 — use approved words |
| 6 | initiate | (removed) | Synonym table (initiate→start) |
| 7 | Long sentence (42 words) | Split into 2 sentences | Grammar rule — max 25 words descriptive |
| 8 | "it's" | "it is" | P14 — no contractions |

Summary: 8 changes. 4 synonym replacements. 2 grammar fixes. 1 abbreviation expansion. 1 contraction fix.

---

### COMPLIANCE: README.md

| Principle | Status | Details |
|-----------|--------|---------|
| P1 — Approved words | PASS | All words checked against Level 3 dictionary |
| P2 — Part of speech | PASS | Words used as approved part of speech |
| P3 — Approved meanings | PASS | Abbreviation "docs" expanded to "documents" |
| P4 — Verb/adjective forms | PASS | Imperative mood in procedures, no -ing main verbs |
| P5 — Technical nouns | PASS | "ASD-STE100" is a valid technical noun |
| P6 — Non-approved words | PASS | 4 non-approved words replaced with synonyms |
| P7 — Nouns as verbs | PASS | No technical nouns used as verbs |
| P8 — Standard nouns | PASS | "STE-Code" is well-known in this codebase |
| P9 — Short nouns | PASS | Noun clusters do not exceed 3 words |
| P10 — No slang/jargon | PASS | Personal pronoun "your" removed |
| P11 — One term per concept | PASS | "supplies" used consistently, not mixed with "provides" |
| P12 — Technical verbs | PASS | "apply", "supply", "remove" are approved |
| P13 — Verbs as nouns | PASS | No technical verbs used as nouns |
| P14 — American English | PASS | Contraction "it's" expanded to "it is" |

Overall: 14/14 principles pass. Level 3 compliance: 100%.
```

This example shows the full output format. The REWRITTEN section contains the
compliant text. The CHANGES section lists each edit with the rule that caused
it. The COMPLIANCE section assigns a PASS or FAIL status to each of the 14
principles.

## Output Examples — Multi-Level Comparison

The same paragraph from README.md ("What Is STE-Code?") shows how each level
changes the output.

### Level 1 — Core Principles Only

```
STE-Code changes the ASD-STE100 Simplified Technical English standard
for the code documentation domain. The standard was first made for
aerospace maintenance documentation. STE-Code has 53 writing rules.
It has 19 technical noun categories. It has 4 technical verb categories.
It uses a controlled vocabulary. This vocabulary removes ambiguity,
jargon, and hedging from READMEs, API docs, comments, commit messages,
and error messages. Each output is clear, unambiguous, and machine-readable.
```

Sentences are short. Verbs come from the synonym table ("made," "has," "uses,"
"removes").

### Level 2 — + Dictionary Excerpt

```
STE-Code changes the ASD-STE100 standard for use with code documentation.
The original standard was made for aerospace maintenance documents.
STE-Code gives you 53 writing rules, 19 technical noun categories,
4 technical verb categories, and a controlled vocabulary. It removes
ambiguity, jargon, and hedging from READMEs, API docs, comments, commit
messages, and error messages. Every output is clear, unambiguous,
and machine-readable.
```

Dictionary-aware word choices appear ("gives you" over "has," "original
standard" over "standard").

### Level 3 — + Grammar Rules

```
STE-Code applies the ASD-STE100 Simplified Technical English standard
to code documentation. The standard was first made for aerospace
maintenance documentation. STE-Code supplies 53 writing rules,
19 technical noun categories, and 4 technical verb categories.
It also supplies a controlled vocabulary. The vocabulary removes
ambiguity, jargon, and hedging from READMEs, API documents, code
comments, commit messages, and error messages. All output is clear
and machine-readable.
```

Grammar rules enforce shorter sentences. "Supplies" replaces the Level 2
"gives." "API documents" replaces "API docs" (no abbreviations, P3).

### Level 4 — + Full Dictionary

```
STE-Code changes the ASD-STE100 Simplified Technical English standard
for use with code documentation. The ASD-STE100 standard was first
written for aerospace maintenance documents. STE-Code gives you 53
writing rules and 19 technical noun categories. It also gives you 4
technical verb categories and a controlled vocabulary. The vocabulary
removes ambiguity, jargon, and hedging from your documents. This
includes READMEs, API documents, comments, commit messages, and error
messages. Each output is clear and unambiguous. Each output is also
machine-readable.
```

Full dictionary access produces the most precise word choices ("written" over
"made," full list of document types with "This includes"). Level 4 is the most
verbose and the most formal.

## Quantitative Comparison

These numbers come from a real run against all 4 target documents. The benchmark
runner is at
[`.agents/benchmark/launch-levels.py`](../../benchmark/launch-levels.py).

| Metric                 | Level 1 | Level 2      | Level 3      | Level 4      |
| ---------------------- | ------- | ------------ | ------------ | ------------ |
| Total output lines     | 1,039   | 1,008        | 1,243        | 1,026        |
| Total output bytes     | 58,912  | 57,643       | 94,026       | 66,077       |
| README words (before)  | 832     | 832          | 832          | 832          |
| README words (after)   | 792     | Not measured | Not measured | Not measured |
| Word reduction         | 4.8%    | Similar      | Similar      | Similar      |
| All 4 docs reduction   | 6.8%    | Not measured | Not measured | Not measured |
| P10 violations removed | 19      | Similar      | Similar      | Similar      |
| P11 violations removed | 25      | Similar      | Similar      | Similar      |
| Synonym table fixes    | 28      | Similar      | Similar      | Similar      |
| Long sentences split   | 36      | Similar      | Similar      | Similar      |
| -ing main verbs fixed  | 9       | Similar      | Similar      | Similar      |
| Contractions fixed     | 2       | Similar      | Similar      | Similar      |

NOTE: Detailed metrics (word counts, violation counts) were captured only for
Level 1 and Level 3. The Level 2 and Level 4 runs produced the same document
content with different word choices. A full metric sweep across all 4 levels is
a planned improvement.

Level 3 produced the largest output (94 KB) because it includes the most
detailed change logs. Each change references a specific rule (P1-P14) and
explains the reason for the change.

## Comparison Use

The 4 outputs can be compared to measure how each adaptation level affects
documentation quality. Higher levels add stricter rules, producing more formal
but potentially more verbose output.

## Pre-Flight Checks

Run these checks before you launch the workers. If any check fails, stop and fix
the problem. Do not proceed.

```
□ Venv Python exists:       [ -x ~/.hermes/hermes-agent/venv/bin/python3 ]
□ Wrapper script exists:    [ -f .agents/tools/lib/hermes-oneshot-wrapper.py ]
□ Rules file exists:        [ -f ste-code/artifacts/ste-code-distilled-system-prompt.txt ]
□ Target documents exist:   Check each document path resolves
□ Output directory writable: mkdir -p .agents/rewrites && [ -w .agents/rewrites ]
□ No stale workers running: ps aux | grep oneshot | grep -v grep
□ Disk space available:     df -h .agents/rewrites (at least 1 GB recommended)
□ Model configured:         hermes status (check that poolside/laguna-s-2.1:free is listed)
```

The launcher script (`launch-levels.py`) runs some of these checks
automatically. The manual checks above catch environment problems before the
script starts.

### Token Budget Check

The launcher estimates the prompt token count and warns if it exceeds the model
context window. The budget is:

| Component              | Tokens           |
| ---------------------- | ---------------- |
| Level 1 rules          | ~500             |
| 4 target documents     | ~3,000-5,000     |
| Task instructions      | ~200             |
| **Total prompt**       | **~3,700-5,700** |
| Model context window   | 128,000          |
| Output reserve         | 16,000           |
| **Available headroom** | **~106,000+**    |

All 4 levels fit comfortably within the model context window. Level 5 (100K+
tokens) is the only level that approaches the budget limit.

## Edge Cases

This section describes what happens when the launcher or the oneshot wrapper
fails in specific ways.

### EC1 — Temp File Write Fails

**Symptom:** The launcher cannot write the prompt to a temp file in `/tmp`.

**Cause:** Disk full, `/tmp` not writable, or permission denied.

**Recovery:**

1. Check disk space: `df -h /tmp`
2. Check write permissions: `touch /tmp/test-write && rm /tmp/test-write`
3. If `/tmp` is full, set `TMPDIR` to an alternative location before running the
   launcher.

The launcher will exit with an error message. No workers will start.

### EC2 — Venv Python Not Executable

**Symptom:** The launcher prints "Cannot find Python or wrapper."

**Cause:** The Hermes Agent virtual environment is missing or the Python binary
is not executable.

**Recovery:**

1. Check that the venv exists: `ls -la ~/.hermes/hermes-agent/venv/bin/python3`
2. If the venv is missing, reinstall Hermes Agent: `hermes setup`
3. Do not use system Python. The oneshot wrapper needs `hermes_cli` modules from
   the venv.

### EC3 — Oneshot Wrapper Import Error

**Symptom:** The worker exits with code 1. The output.txt file contains a Python
traceback with `ModuleNotFoundError`.

**Cause:** The venv Python cannot find `hermes_cli` modules (run_agent, config,
models, etc.).

**Recovery:**

1. Confirm you used the venv Python. Run:
   `~/.hermes/hermes-agent/venv/bin/python3 -c "from run_agent import AIAgent"`.
   If this fails, the venv is corrupted.
2. Reinstall Hermes Agent: `hermes setup`
3. Do not modify the wrapper to use different import paths. The wrapper is
   tested only with the venv Python.

### EC4 — Worker Produces Empty output.txt

**Symptom:** The worker finishes (exit code 0 or 1) but `output.txt` has size 0.

**Cause:** The LLM returned an empty response, the prompt file was empty, or the
wrapper crashed before writing output.

**Recovery:**

1. Check the prompt file. The wrapper deletes it after reading, but the launcher
   keeps a copy only during the run. Check the launcher output for token budget
   warnings.
2. Check the Hermes agent logs for API errors:
   `ls -lt ~/.hermes/hermes-agent/logs/`
3. Run the worker again. If the problem continues, reduce the document count
   with the `--docs` flag.

### EC5 — Worker Produces output.txt Without REWRITTEN Headers

**Symptom:** The output.txt file has text but no `### REWRITTEN:` headers.

**Cause:** The LLM did not follow the output format instructions. This is a
prompt adherence failure.

**Recovery:**

1. Run `grep -c "### REWRITTEN:" .agents/rewrites/level-*/output.txt` to count
   headers.
2. If the count is 0, the LLM ignored the output format. Run the worker again.
3. If the problem continues on the same level, the prompt may be too complex for
   the model at that level. Try a lower level or split the target into one
   document at a time.

### EC6 — Worker Hangs and Never Finishes

**Symptom:** The launcher waits for a worker and the timeout expires (default:
900 seconds). The launcher sends SIGTERM, then SIGKILL.

**Cause:** The LLM API is slow, the model is overloaded, or the oneshot wrapper
has a deadlock.

**Recovery:**

1. Run `ps aux | grep oneshot` to list running wrapper processes.
2. If the process is still running after SIGKILL, use `kill -9 <PID>` manually.
3. Check the partial output: `cat .agents/rewrites/level-N/output.txt`. If the
   output is truncated, the LLM may have hit a token limit.
4. Increase the timeout: `--timeout 1800`. Or reduce the document count.

### EC7 — Two Launcher Runs Write to the Same Output Directory

**Symptom:** Two concurrent runs of `launch-levels.py` write to the same
`.agents/rewrites/` directory.

**Consequence:** Workers from different runs overwrite each other's `output.txt`
files. Results are corrupted.

**Prevention:** Run `ps aux | grep launch-levels` before starting a new run. Do
not run two launchers at the same time. If you need isolated runs, use different
output directories: `--output-dir .agents/rewrites-run2`.

### EC8 — API Rate Limit or Authentication Failure

**Symptom:** The worker exits with code 1. The output.txt file contains an API
error message (HTTP 429, 401, or 403).

**Cause:** The model provider rate-limited the API key or the key is invalid.

**Recovery:**

1. Check your API key configuration: `hermes status`
2. Wait for the rate limit window to reset (usually 60 seconds).
3. Run the launcher again. The oneshot wrapper has no built-in retry logic for
   API errors.

### EC9 — Token Budget Exceeded

**Symptom:** The launcher prints "WARNING: Estimated prompt size exceeds the
available budget."

**Cause:** The prompt (rules + documents + instructions) is larger than the
model context window minus the output reserve.

**Recovery:**

1. The warning is conservative (it uses a 4-chars-per-token estimate). The
   actual token count may be lower.
2. If the output is truncated, reduce the document count: `--docs README.md`
   (one document only).
3. For Level 5, this warning will always fire. See the Level 5 Feasibility
   section for strategies.

### EC10 — Disk Full During Worker Run

**Symptom:** The worker exits with code 1 or produces a truncated output.txt
file. The file size is smaller than expected.

**Cause:** The disk partition containing `.agents/rewrites/` is full.

**Recovery:**

1. Check disk space: `df -h .`
2. Remove old output: `rm -rf .agents/rewrites/level-*`
3. Free space elsewhere on the partition.
4. Run the launcher again.

### EC11 — Output.txt Contains Only Stderr, No Stdout

**Symptom:** The output.txt file contains error messages from the wrapper but no
LLM response.

**Cause:** The wrapper wrote an error to stderr, which was merged into stdout
(the launcher uses `stderr=subprocess.STDOUT`). The LLM never produced output.

**Recovery:**

1. Read the output.txt file. Look for Python tracebacks or "Prompt file not
   found" messages.
2. Fix the error based on the traceback (see EC3 for import errors, EC2 for venv
   issues).
3. Run the launcher again.

## Troubleshooting

| Symptom                                                            | Likely Cause                                                                                               | Recovery                                                                                                                                                                                                                                        |
| ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ERROR: Wrapper not found at ...`                                  | The `hermes-oneshot-wrapper.py` file is missing from `.agents/tools/`.                                     | Run `git status` in the project root. If the tools directory is missing, check out the `Current` branch. The wrapper ships with the project.                                                                                                    |
| Worker exits with code 1, `output.txt` is empty                    | The Hermes venv Python is missing or the model is not available.                                           | Check that `~/.hermes/hermes-agent/venv/bin/python3` exists. If it does not exist, reinstall Hermes Agent. Check that the model `poolside/laguna-s-2.1:free` is configured in your Hermes profile.                                              |
| Worker exits with code 1, `output.txt` has a Python traceback      | A Python import error in the oneshot wrapper (missing `hermes_cli` modules).                               | The venv Python must be used. Do not use system Python. The wrapper imports `run_agent.AIAgent` and other `hermes_cli` modules that exist only inside the Hermes venv.                                                                          |
| Worker runs but `output.txt` has only a partial response           | The LLM hit a token limit or the API timed out.                                                            | The oneshot wrapper has no retry logic. Run the launcher again. If the problem continues, the prompt may be too long for the model context window. Check the prompt file in the level directory.                                                |
| Worker produces `output.txt` with no `### REWRITTEN:` headers      | The LLM did not follow the output format instructions.                                                     | This is a prompt adherence failure. The launcher prompt includes explicit output format instructions. Run the worker again. If the problem continues on the same level, reduce the document count or increase the model capacity.               |
| `launch-levels.py` hangs and does not print "All workers complete" | One or more workers are still running or have crashed silently.                                            | Run `ps aux                                                                                                                                                                                                                                     | grep oneshot`to list running wrapper processes. If a worker is stuck, kill it with`kill <PID>`. Then check its `output.txt` for error messages. |
| `output.txt` has size 0 after the worker finishes                  | The LLM returned an empty response. This can happen if the prompt is too short or the model is overloaded. | Check the `prompt.txt` file in the level directory. It should contain the STE-Code rules, the task instructions, and the document text. If the prompt is empty or truncated, the launcher script has a file read error. Run the launcher again. |
| Two runs overwrite each other's output                             | Concurrent launcher runs write to the same directory.                                                      | Run `ps aux                                                                                                                                                                                                                                     | grep launch-levels`before starting. Use`--output-dir` to isolate runs. See Edge Case EC7.                                                       |
| Worker times out after 900 seconds                                 | The model response is slow or the prompt is very large.                                                    | Increase the timeout: `--timeout 1800`. Or reduce the document count: `--docs README.md`.                                                                                                                                                       |

## Post-Execution Verification

After all workers finish, verify the output files.

### Quick Verification

```bash
# Check all output files exist and are non-empty
for L in 1 2 3 4; do
	F=".agents/rewrites/level-${L}/output.txt"
	if [ -s "$F" ]; then
		echo "Level ${L}: $(wc -l < "$F") lines, $(wc -c < "$F") bytes"
	else
		echo "Level ${L}: MISSING or EMPTY"
	fi
done
```

### Section Completeness Check

```bash
# Count REWRITTEN, CHANGES, and COMPLIANCE headers per level
for L in 1 2 3 4; do
	F=".agents/rewrites/level-${L}/output.txt"
	R=$(grep -c "^### REWRITTEN:" "$F" 2> /dev/null || echo 0)
	C=$(grep -c "^### CHANGES:" "$F" 2> /dev/null || echo 0)
	P=$(grep -c "^### COMPLIANCE:" "$F" 2> /dev/null || echo 0)
	echo "Level ${L}: ${R} REWRITTEN, ${C} CHANGES, ${P} COMPLIANCE sections"
done
```

A correct run with 4 target documents produces 4 of each section per level.

### Quality Gate

| Gate                      | Check                                          | Command                                      |
| ------------------------- | ---------------------------------------------- | -------------------------------------------- |
| Non-empty output          | File size > 0                                  | `[ -s .agents/rewrites/level-*/output.txt ]` |
| Section headers present   | Count of `### REWRITTEN:` headers              | `grep -c "^### REWRITTEN:" ...`              |
| No glued headings         | No heading immediately followed by text        | `grep -c $'### [^\\n]\\n[^ \\n#]' ...`       |
| No triple blanks          | Max 2 consecutive blank lines                  | `grep -c $'\\n\\n\\n\\n' ...`                |
| Output differs from input | Rewritten text is not byte-identical to source | Manual comparison                            |

### Regression Detection

Compare outputs between runs to detect regressions:

```bash
diff .agents/rewrites/level-3/output.txt .agents/rewrites-run2/level-3/output.txt
```

If the model or prompt changes, the output may change. Large differences between
runs with the same parameters may indicate a non-deterministic model or a prompt
regression.

## Level 5 Feasibility

Level 5 loads the full standard: all 57 adapted files from
`ste-code/adapted/*.md` plus the merged master document. The total size is
approximately 100K tokens.

### What Blocks Level 5

| Blocker             | Details                                                                                                                                                                                                                                    |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Token budget        | The full standard is ~100K tokens. With 4 target documents (~4K words total), the prompt exceeds 100K tokens. The model `poolside/laguna-s-2.1:free` has a large context window, but the output may degrade with very long system prompts. |
| Prompt construction | Level 5 needs to load all 57 adapted files. The current `launch-levels.py` script loads only the Level 1 prompt file plus the target documents. Loading 57 files needs a new prompt assembly step.                                         |
| Output volume       | At Level 3, one document produces ~1,200 lines of output (rewritten text, change log, compliance table). Four documents at Level 5 may produce 5,000+ lines. This may exceed the model output token limit.                                 |
| Cost                | A 100K token prompt with 4 documents costs approximately 4× more than Level 4. Running all 4 levels in parallel at Level 5 increases cost further.                                                                                         |
| Diminishing returns | Benchmark results show that Level 1 (96.6% pass rate) already outperforms a plain assistant (11.9%). Level 5 may add only marginal compliance gains at high cost.                                                                          |

### What Level 5 Needs

1. A prompt assembly script that reads all 57 adapted files and concatenates
   them into a single prompt.
2. A test run with one document (not four) to measure output quality and token
   cost.
3. A split-output strategy: rewrite one document per worker call instead of all
   four in one call.
4. A cost-benefit analysis comparing Level 4 compliance (full dictionary)
   against Level 5 compliance (full standard).

### Current Status

Level 5 is defined in the Agent #7 contract and the adaptation levels table. The
rule files exist on disk (55-57 adapted files in `ste-code/adapted/`). The
launcher and the oneshot wrapper can handle Level 5 prompts. The main blocker is
the prompt assembly step. No Level 5 run data exists yet.

## Cross-References

### Core Components

| Component           | Path                                                                                   | Role                                                                                           |
| ------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Agent #7 definition | This skill (`SKILL.md`)                                                                | Worker identity, levels, task parameters, execution protocol, edge cases, pre-flight checklist |
| Oneshot wrapper     | [`.agents/tools/lib/hermes-oneshot-wrapper.py`](../../tools/hermes-oneshot-wrapper.py) | Hermes AIAgent caller with `session_db=None`, no tool access                                   |
| Launcher script     | [`.agents/benchmark/launch-levels.py`](../../benchmark/launch-levels.py)               | Parallel worker launcher with token budget checks, temp file cleanup, timeout handling         |

### Benchmark Pipeline

| Component              | Path                                                                                   | Role                                                  |
| ---------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Benchmark orchestrator | [`.agents/benchmark/orchestrator.py`](../../benchmark/orchestrator.py)                 | Runs 59 parallel tests across 14 categories           |
| Control group runner   | [`.agents/benchmark/orchestrator-control.py`](../../benchmark/orchestrator-control.py) | Runs same 59 tests without STE-Code rules             |
| Benchmark results      | [`.agents/AGENTS.md`](../../AGENTS.md)                                                 | Pass rate 96.6% (STE-Code) vs 11.9% (plain assistant) |
| Test cases             | `.agents/benchmark/test-cases/category-*.json`                                         | 14 category files, 59 test inputs                     |

### Quality Assurance

| Component                 | Path                                                                     | Role                                         |
| ------------------------- | ------------------------------------------------------------------------ | -------------------------------------------- |
| Agent #3 — Auditor        | [`.agents/skills/auditing/SKILL.md`](../auditing/SKILL.md)               | Verifies worker output against disk evidence |
| Worker rails              | [`.agents/references/worker-rails.md`](../../references/worker-rails.md) | 10-rail self-validation checklist            |
| Execution auditor reports | `.agents/audit/`                                                         | Auditor run results                          |

### STE-Code Source Files

| Component        | Path                                                      | Lines  | Purpose                                |
| ---------------- | --------------------------------------------------------- | ------ | -------------------------------------- |
| Distilled prompt | `ste-code/artifacts/ste-code-distilled-system-prompt.txt` | 50     | Level 1 system prompt                  |
| Full dictionary  | `ste-code/adapted/a-dictionary.md`                        | 5,943  | Approved word dictionary               |
| Section rules    | `ste-code/adapted/a-sec1-*` through `a-sec9-*`            | ~3,400 | Grammar rules per ASD-STE100 section   |
| Merged master    | `ste-code/grouped/master.md`                              | —      | Complete standard, all sections merged |

## Key Facts

- Uses Hermes oneshot wrapper (venv Python, no session DB, no tools)
- 4 levels, 4 parallel workers
- Output to `.agents/rewrites/level-{1,2,3,4}/output.txt`
- All output files gitignored — temporary worker results only
- Benchmark results: STE-Code 96.6% pass rate vs plain assistant 11.9%
- Level 3 produces the most detailed change logs (94 KB output)
- Level 5 not yet launched — blocked on prompt assembly for 57 files
- Agent #3 (Auditor) can verify worker output after a run
- The launcher handles timeouts, temp file cleanup, and token budget warnings
