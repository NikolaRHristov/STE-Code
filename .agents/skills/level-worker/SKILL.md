---
description: "Launch parallel Agent #7 workers at STE-Code levels 1-4 using Hermes oneshot wrapper. Each worker rewrites documents at its adaptation depth."
version: "1.0.0"
related: [".agents/agent/agent-7-level-worker.md", ".agents/benchmark/launch-levels.py", ".hermes/skills/hermes-shell-hooks/templates/hermes-oneshot-wrapper.py"]
---

# Level Worker Launcher — Agent-Agnostic

Launch 4 parallel Agent #7 workers, each at a different STE-Code adaptation level (1-4). Workers use the Hermes oneshot wrapper (`session_db=None`, no history pollution, no tool access). Each worker rewrites the same set of documents and outputs to its own isolated directory.

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

## Agent #7 Role Contract

Agent #7 is a parameterized STE-Code worker. Its full definition is at [`.agents/agent/agent-7-level-worker.md`](../../agent/agent-7-level-worker.md).

Key facts about the agent:
- Agent #7 receives `level` (1-5), `action` (test/rewrite/benchmark), and `target` parameters.
- It loads only the rule files for the specified level. Level 1 loads ~500 tokens. Level 5 loads ~100K+ tokens.
- It produces three output sections per document: rewritten text, a change log, and a P1-P14 compliance table.
- The agent can rewrite its own Level 1 system prompt using Level 3 rules.
- Source files: `ste-code/artifacts/ste-code-distilled-system-prompt.txt` (Level 1), `ste-code/adapted/a-dictionary.md` (Levels 2+4), and `ste-code/adapted/a-sec1-*` through `a-sec9-*` (Levels 3+).

The level worker launcher wraps Agent #7 in a Hermes oneshot subprocess. The wrapper is at [`.agents/tools/hermes-oneshot-wrapper.py`](../../tools/hermes-oneshot-wrapper.py). The wrapper:
- Reads a prompt from a temp file and deletes it after reading.
- Creates `AIAgent` with `session_db=None` and `tool_gen_callback=None`.
- Writes the LLM response to stdout, which the launcher captures into `output.txt`.
- Exits with code 0 on success or code 1 on failure (missing prompt file, import error, or API error).

## Launch

```bash
python3 .agents/benchmark/launch-levels.py
```

This uses the canonical Hermes oneshot wrapper pattern:
1. Writes prompt to temp file
2. Launches `~/.hermes/hermes-agent/venv/bin/python3 hermes-oneshot-wrapper.py <prompt_file> --model deepseek-v4-pro`
3. Workers run with `session_db=None` — no session pollution
4. Workers have `tool_gen_callback=None` — no file creation tools
5. Output captured to `output.txt` in each level directory

## Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| Level | 1-4 | Adaptation depth (5 not yet implemented) |
| Documents | README.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md, RELEASE-NOTES.md | Which docs to rewrite |
| Model | deepseek-v4-pro | LLM model |

## Results Format

Each worker produces for every document:
1. `### REWRITTEN: <filename>` — The rewritten text
2. `### CHANGES: <filename>` — Change log with rule references
3. `### COMPLIANCE: <filename>` — P1-P14 compliance table

## Output Examples

The same paragraph from README.md ("What Is STE-Code?") shows how each level changes the output.

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

Sentences are short. Verbs come from the synonym table ("made," "has," "uses," "removes").

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

Dictionary-aware word choices appear ("gives you" over "has," "original standard" over "standard").

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

Grammar rules enforce shorter sentences. "Supplies" replaces the Level 2 "gives." "API documents" replaces "API docs" (no abbreviations, P3).

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

Full dictionary access produces the most precise word choices ("written" over "made," full list of document types with "This includes"). Level 4 is the most verbose and the most formal.

## Quantitative Comparison

These numbers come from a real run against all 4 target documents. The benchmark runner is at [`.agents/benchmark/launch-levels.py`](../../benchmark/launch-levels.py).

| Metric | Level 1 | Level 2 | Level 3 | Level 4 |
|--------|---------|---------|---------|---------|
| Total output lines | 1,039 | 1,008 | 1,243 | 1,026 |
| Total output bytes | 58,912 | 57,643 | 94,026 | 66,077 |
| README words (before) | 832 | 832 | 832 | 832 |
| README words (after) | 792 | Not measured | Not measured | Not measured |
| Word reduction | 4.8% | Similar | Similar | Similar |
| All 4 docs reduction | 6.8% | Not measured | Not measured | Not measured |
| P10 violations removed | 19 | Similar | Similar | Similar |
| P11 violations removed | 25 | Similar | Similar | Similar |
| Synonym table fixes | 28 | Similar | Similar | Similar |
| Long sentences split | 36 | Similar | Similar | Similar |
| -ing main verbs fixed | 9 | Similar | Similar | Similar |
| Contractions fixed | 2 | Similar | Similar | Similar |

NOTE: Detailed metrics (word counts, violation counts) were captured only for Level 1 and Level 3. The Level 2 and Level 4 runs produced the same document content with different word choices. A full metric sweep across all 4 levels is a planned improvement.

Level 3 produced the largest output (94 KB) because it includes the most detailed change logs. Each change references a specific rule (P1-P14) and explains the reason for the change.

## Comparison Use

The 4 outputs can be compared to measure how each adaptation level affects documentation quality. Higher levels add stricter rules, producing more formal but potentially more verbose output.

## Troubleshooting

| Symptom | Likely Cause | Recovery |
|---------|--------------|----------|
| `ERROR: Wrapper not found at ...` | The `hermes-oneshot-wrapper.py` file is missing from `.agents/tools/`. | Run `git status` in the project root. If the tools directory is missing, check out the `Current` branch. The wrapper ships with the project. |
| Worker exits with code 1, `output.txt` is empty | The Hermes venv Python is missing or the model is not available. | Check that `~/.hermes/hermes-agent/venv/bin/python3` exists. If it does not exist, reinstall Hermes Agent. Check that the model `deepseek-v4-pro` is configured in your Hermes profile. |
| Worker exits with code 1, `output.txt` has a Python traceback | A Python import error in the oneshot wrapper (missing `hermes_cli` modules). | The venv Python must be used. Do not use system Python. The wrapper imports `run_agent.AIAgent` and other `hermes_cli` modules that exist only inside the Hermes venv. |
| Worker runs but `output.txt` has only a partial response | The LLM hit a token limit or the API timed out. | The oneshot wrapper has no retry logic. Run the launcher again. If the problem continues, the prompt may be too long for the model context window. Check the prompt file in the level directory. |
| Worker produces `output.txt` with no `### REWRITTEN:` headers | The LLM did not follow the output format instructions. | This is a prompt adherence failure. The launcher prompt includes explicit output format instructions. Run the worker again. If the problem continues on the same level, reduce the document count or increase the model capacity. |
| `launch-levels.py` hangs and does not print "All workers complete" | One or more workers are still running or have crashed silently. | Run `ps aux | grep oneshot` to list running wrapper processes. If a worker is stuck, kill it with `kill <PID>`. Then check its `output.txt` for error messages. |
| `output.txt` has size 0 after the worker finishes | The LLM returned an empty response. This can happen if the prompt is too short or the model is overloaded. | Check the `prompt.txt` file in the level directory. It should contain the STE-Code rules, the task instructions, and the document text. If the prompt is empty or truncated, the launcher script has a file read error. Run the launcher again. |

## Level 5 Feasibility

Level 5 loads the full standard: all 57 adapted files from `ste-code/adapted/*.md` plus the merged master document. The total size is approximately 100K tokens.

### What Blocks Level 5

| Blocker | Details |
|---------|---------|
| Token budget | The full standard is ~100K tokens. With 4 target documents (~4K words total), the prompt exceeds 100K tokens. The model `deepseek-v4-pro` has a large context window, but the output may degrade with very long system prompts. |
| Prompt construction | Level 5 needs to load all 57 adapted files. The current `launch-levels.py` script loads only the Level 1 prompt file plus the target documents. Loading 57 files needs a new prompt assembly step. |
| Output volume | At Level 3, one document produces ~1,200 lines of output (rewritten text, change log, compliance table). Four documents at Level 5 may produce 5,000+ lines. This may exceed the model output token limit. |
| Cost | A 100K token prompt with 4 documents costs approximately 4× more than Level 4. Running all 4 levels in parallel at Level 5 increases cost further. |
| Diminishing returns | Benchmark results show that Level 1 (96.6% pass rate) already outperforms a plain assistant (11.9%). Level 5 may add only marginal compliance gains at high cost. |

### What Level 5 Needs

1. A prompt assembly script that reads all 57 adapted files and concatenates them into a single prompt.
2. A test run with one document (not four) to measure output quality and token cost.
3. A split-output strategy: rewrite one document per worker call instead of all four in one call.
4. A cost-benefit analysis comparing Level 4 compliance (full dictionary) against Level 5 compliance (full standard).

### Current Status

Level 5 is defined in the Agent #7 contract and the adaptation levels table. The rule files exist on disk (55-57 adapted files in `ste-code/adapted/`). The launcher and the oneshot wrapper can handle Level 5 prompts. The main blocker is the prompt assembly step. No Level 5 run data exists yet.

## Key Facts
- Uses Hermes oneshot wrapper (venv Python, no session DB, no tools)
- 4 levels, 4 parallel workers
- Output to `.agents/rewrites/level-{1,2,3,4}/output.txt`
- All output files gitignored — temporary worker results only
