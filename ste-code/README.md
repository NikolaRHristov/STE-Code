# STE-Code

A controlled-language variation of **ASD-STE100** for software documentation —
rules for writing comments, commit messages, docs, error strings, and config in
plain, unambiguous English that LLMs and humans both follow reliably.

## Pipeline (6 stages, A → F)

| Stage | Dir | What it produces |
|-------|-----|-----------------|
| **A** Extraction | `ste-code/extracted/` | raw text pulled from the spec pages |
| **B** Refinement | `ste-code/refined/` | cleaned, section-aware markdown |
| **C** Grouping | `ste-code/grouped/` | deterministic regrouping into the 9 rule sections (no LLM) |
| **D** Adaptation | `ste-code/adapted/` | ASD-STE100 rules rewritten for the code domain |
| **E** Extensions | `ste-code/final/extensions/` | code-domain vocabulary + anti-pattern gap fillers |
| **F** Artifacts | `ste-code/artifacts/` | LLM-distilled, deployable tiers (this is the deliverable) |

`ste-code/final/` is the enriched consolidated standard that Stage F is built
from. `ste-code/spec/` holds the source spec pages.

## Artifacts (the deliverable)

`ste-code/artifacts/` ships **8 tiers** (`level-2` … `level5/`), each a
directory of small sub-documents plus a `system-prompt.txt` (the whole tier in
one file). `llms.txt` and `llms-full.txt` are the consolidated single-file
forms. See `ste-code/artifacts/README.md`.

## Benchmark

`.agents/benchmark/` runs the 59-test / 14-category suite against any tier:

```bash
python3 .agents/benchmark/benchmark-levels.py --levels -2,-1,0,1,2,3,4,5
python3 .agents/benchmark/orchestrator-control.py   # plain-assistant baseline
```

## Tooling

All pipeline tooling lives in `.agents/tools/` and is agent-agnostic —
backends (Hermes, Claude, Codex) are configured in `.agents/config/agents.yaml`.

## Templates

`ste-code/templates/` holds the externalized prompt templates consumed by the
trajectory system (`.agents/tools/trajectory/`). They are rendered at run time,
not hand-edited per run.
