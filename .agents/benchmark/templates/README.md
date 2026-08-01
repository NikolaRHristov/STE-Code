# Benchmark prompt templates

Prompt text for `summarize_run.py`'s LLM analysis. Edit these to change how the
run is analysed — never the Python. See `.agents/tools/lib/PROMPTS.md`.

| template | used as | sent when |
|---|---|---|
| `llm-instructions.md` | `LLM_INSTRUCTIONS` | single-call synthesis (`synthesize()`) |
| `stage-1-extract.md` | `STAGE_EXTRACT` | stage 1 of `analyse()` |
| `stage-2-assess.md` | `STAGE_ASSESS` | stage 2 of `analyse()` |
| `stage-3-final.md` | `STAGE_FINAL` | stage 3 of `analyse()` |

## No placeholders

These are loaded verbatim by `_prompt()` — no `{{...}}` substitution. The
evidence is appended at call time as a fenced JSON block, so the prompt text
stays static and reviewable.

## The three-stage chain

```
stage 1 extract  dossier                → JSON: established / not_established / anomalies
stage 2 assess   goals + stage 1        → JSON: per-goal verdict, root causes, confidence
stage 3 final    goals + stages 1 and 2 → markdown report
```

Each stage sees the previous stage's **output**, never its reasoning. That is
deliberate: stage 3 writes prose over a settled record rather than re-litigating
the evidence.

## Two rules worth keeping

**Stage 2 must prefer evidence over the deterministic grade.** The instruction to
mark a goal `disputed` when the grader and the evidence disagree is not
decorative — on its first real run it caught two genuine bugs in the grader
(`tier_monotonic` sorting tier numbers as strings, and a mock control suite
inflating the measured pass rate). Removing that instruction removes the only
check on the grader.

**Every stage ends with an output contract.** Without "reply with the report and
nothing else", a sub-agent will use its tools and write stray files into the
repository root. This was observed, not hypothesised.

## Orchestrator worker prompts

`orchestrator.py` (legacy, excluded from `make lint`) had the same two prompts
duplicated in the launch and retry paths. They are now `build_full_prompt()` in
`orchestrator.py`, selecting between:

| template | when | placeholders |
|---|---|---|
| `orchestrator-generate.md` | generation task (`prompt` in test case) | `system_prompt`, `task_input` |
| `orchestrator-check.md` | check/correction task | `system_prompt`, `task_input` |
