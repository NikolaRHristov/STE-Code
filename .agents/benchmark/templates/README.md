# Benchmark prompt templates

## Purpose

This directory holds the prompt text for the benchmark's LLM analysis and for
the orchestrator's worker prompts. The text lives here as data so that changing
how a run is analysed never means editing Python. Anyone tuning analysis or
worker behaviour edits these files, not the modules.

## Footprint

| Kind    | Value                                                 |
| ------- | ----------------------------------------------------- |
| Inputs  | none — these files are the input to the modules below |
| Read by | `../summarize_run.py` via `_prompt(name)`             |
| Read by | `../orchestrator.py` via `build_full_prompt()`        |
| Outputs | none — rendering happens in memory                    |

| Template                   | Loaded as          | Sent when                              |
| -------------------------- | ------------------ | -------------------------------------- |
| `llm-instructions.md`      | `LLM_INSTRUCTIONS` | single-call synthesis (`synthesize()`) |
| `stage-1-extract.md`       | `STAGE_EXTRACT`    | stage 1 of `analyse()`                 |
| `stage-2-assess.md`        | `STAGE_ASSESS`     | stage 2 of `analyse()`                 |
| `stage-3-final.md`         | `STAGE_FINAL`      | stage 3 of `analyse()`                 |
| `orchestrator-generate.md` | generation prompt  | the test case carries a `prompt` field |
| `orchestrator-check.md`    | check prompt       | check and correction tasks             |

## Usage

These files are not executed. They are consumed by:

    python3 .agents/benchmark/summarize_run.py --base <name>
    python3 .agents/benchmark/orchestrator.py --results-dir <name>

Edit a template in place to change prompt behaviour. Do not add front matter,
headings or section scaffolding to the six prompt files: they are payload, and
the model receives them verbatim.

## Behaviour

- `summarize_run._prompt(name)` reads `templates/<name>.md` verbatim. The four
  analysis prompts carry no `{{...}}` placeholders; the evidence is appended at
  call time as a fenced JSON block, so the prompt text stays static and
  reviewable.
- `orchestrator.build_full_prompt()` selects between the two orchestrator
  templates and renders their `{{system_prompt}}` and `{{task_input}}`
  placeholders.
- Rendering uses `.agents/tools/lib/templater.py`, which raises when a template
  references a placeholder the caller did not supply.
- Each analysis stage sees the previous stage's output, never its reasoning.

```
stage 1 extract  dossier                → JSON: established / not_established / anomalies
stage 2 assess   goals + stage 1        → JSON: per-goal verdict, root causes, confidence
stage 3 final    goals + stages 1 and 2 → markdown report
```

That separation is deliberate: stage 3 writes prose over a settled record rather
than re-litigating the evidence.

## Configuration

The templates themselves are the configuration; no knob controls their content.
Related knobs:

- `runner.default_model`, `runner.default_timeout_s` in `../config/harness.json`
  — the configured defaults for the calls these prompts feed.
- `limits.max_tokens_default` in `../config/harness.json` — response budget.
- `agent.retries`, `agent.backoff_s` in `../../config/defaults.yaml` — retry
  policy.
- Template lookup and rendering behaviour live in
  `.agents/tools/lib/templater.py`; the directory location is derived, never
  hardcoded in a caller.

## Two rules worth keeping

Stage 2 must prefer evidence over the deterministic grade. The instruction to
mark a goal `disputed` when the grader and the evidence disagree is not
decorative: on its first real run it caught two genuine bugs in the grader, a
tier comparison that sorted tier numbers as strings and a mock control suite
that inflated the measured pass rate. Removing that instruction removes the only
check on the grader.

Every stage ends with an output contract. Without "reply with the report and
nothing else", a sub-agent uses its tools and writes stray files into the
repository root. This was observed, not predicted.

## Failure modes

- Adding documentation scaffolding to a prompt file changes what the model
  receives and silently shifts every downstream verdict.
- A missing template file raises `FileNotFoundError` at import time in
  `summarize_run.py`, because the prompts load at module scope.
- A `{{placeholder}}` in an orchestrator template with no matching caller
  argument raises rather than rendering an empty string.
- Removing the stage-2 evidence-over-grade instruction removes the only
  cross-check on the grader.
- Removing a stage's output contract lets the sub-agent write stray files into
  the repository.

## See also

- `../SKILL.md` — the benchmarking role and scoring formula
- `../CONTRACT.md` — genericity rules and record shapes
- `../config/harness.json` — the profile document
- `../../tools/lib/templater.py` — template loading and rendering
