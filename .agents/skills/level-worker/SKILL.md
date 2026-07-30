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

## Comparison Use

The 4 outputs can be compared to measure how each adaptation level affects documentation quality. Higher levels add stricter rules, producing more formal but potentially more verbose output.

## Key Facts
- Uses Hermes oneshot wrapper (venv Python, no session DB, no tools)
- 4 levels, 4 parallel workers
- Output to `.agents/rewrites/level-{1,2,3,4}/output.txt`
- All output files gitignored — temporary worker results only
