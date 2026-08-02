# Benchmark Orchestrator

## Purpose

This skill defines the benchmarking role: measure how well a configuration under test resists
adversarial and ordinary input, and produce a structured, reproducible report. An agent assigned
to a benchmark run reads this file, then `CONTRACT.md` and `WORKER_BRIEF.md`.

## Footprint

Resolved from `.agents/benchmark/config/harness.json`.

| Kind | Value |
|---|---|
| Inputs | `paths.static_cases` — `.agents/benchmark/test-cases/` (14 category files) |
| Inputs | `paths.generated_cases` — `.agents/benchmark/test-cases-adhoc/` |
| Inputs | `paths.variant_prompt_template` — `ste-code/artifacts/{variant_dir}/system-prompt.txt` |
| Outputs | `paths.results_base` — `.agents/benchmark/tests/<run-name>/run-<timestamp>/` |
| Outputs | `runner.aggregate_filename`, `runner.per_test_filename` |
| Scratch | `paths.scratch` — `.agents/tmp/` |
| Agent | `runner.default_model`, `runner.default_max_workers`, `runner.default_timeout_s` |

## Usage

    python3 .agents/benchmark/selftest.py                       # offline green check
    python3 .agents/benchmark/harness_config.py                 # resolved profile and paths
    python3 .agents/benchmark/orchestrator.py --results-dir <name>
    python3 .agents/benchmark/orchestrator-control.py --results-dir <name>
    python3 .agents/benchmark/benchmark-levels.py --results-dir <name> --levels 1,2,3,4,5
    python3 .agents/benchmark/run_pipeline.py --base <name>
    python3 .agents/benchmark/summarize_run.py --base <name>

Pass `--results-dir` and `--base` a bare name, never an absolute path.

## Behaviour

- Load and validate every case in `paths.static_cases` against `schema.json`.
- Resolve the variant prompt for each tier under test from `paths.variant_prompt_template`.
- Build each worker prompt from `templates/orchestrator-generate.md` or
  `templates/orchestrator-check.md`; prompt text is never inline in Python.
- Run cases concurrently up to `runner.default_max_workers`, each bounded by
  `runner.default_timeout_s`.
- Score every response with the shared formula in `harness_config`, then write the per-test and
  aggregate documents into a timestamped run directory.
- Summarize a finished run with `summarize_run.py`, which drives the three-stage prompt chain in
  `templates/`.

### Case schema

```json
{
  "id": "bench-001",
  "category": "readme",
  "description": "README introduction paragraph",
  "input": "This function does a bunch of stuff and should be called with the user object.",
  "expected_principles": ["P1", "P2", "P10"],
  "expected_keywords": ["function", "user object", "call"],
  "forbidden_keywords": ["bunch", "stuff", "should"],
  "max_tokens": 500,
  "difficulty": "easy"
}
```

Rule ids render through `cfg.rule(n)` from `profile.rule_prefix` and `profile.rule_count`; the
`P` prefix is configuration, not a literal.

### Categories

The corpus holds 14 categories across 59 cases, one JSON file per category under `test-cases/`:
`readme`, `api-doc`, `commit`, `error`, `comment`, `changelog`, `config`, `composite`,
`gen-function`, `gen-pr-review`, `gen-api-doc`, `gen-commit`, `gen-error`, `gen-readme`.

### Scoring

The canonical formula lives in `harness_config`, and every constant comes from `scoring.*` in the
profile document. There is exactly one formula; no module reimplements it.

```
base            = scoring.base                  (0.40)
principle_bonus = scoring.principle_weight   × principles_satisfied / total_expected
forbidden_pen   = scoring.forbidden_penalty  × forbidden_found / total_forbidden
keyword_bonus   = scoring.keyword_bonus      × keywords_found / total_expected_keywords
pattern_pen     = scoring.pattern_penalty    × patterns_matched / total_patterns

correctness = clamp(base + principle_bonus - forbidden_pen + keyword_bonus - pattern_pen, 0, 1)
passed      = correctness >= scoring.pass_threshold          (0.70)
```

The forbidden and pattern terms are skipped when their denominator is zero. `diff_ratio` measures
output stability between runs, not distance from a ground-truth string: near 0 means the output
matches the prior run, near 1 means it changed.

### Result record

```json
{
  "test_id": "string",
  "category": "string",
  "input": "string",
  "output": "string",
  "expected_principles_satisfied": ["P1", "P2"],
  "expected_principles_missed": ["P10"],
  "forbidden_keywords_found": ["should"],
  "correctness_score": 0.85,
  "latency_ms": 4200,
  "token_count_input": 150,
  "token_count_output": 200,
  "diff_ratio": 0.15,
  "passed": false,
  "notes": "Missed P10 (jargon). Output was otherwise correct."
}
```

## Configuration

Every knob lives in configuration. Nothing is hardcoded in a script.

| Key | File | Governs |
|---|---|---|
| `runner.default_model` | `config/harness.json` | The configured model default for the harness |
| `runner.default_max_workers` | `config/harness.json` | Concurrency, default 2 |
| `runner.default_timeout_s` | `config/harness.json` | Per-case budget, default 600 |
| `runner.argv_template` | `config/harness.json` | Flags passed to the scoring backend |
| `scoring.*` | `config/harness.json` | Base, weights, penalties, `pass_threshold` |
| `variants.registry` | `config/harness.json` | Tier ids and their directory names |
| `paths.*` | `config/harness.json` | Every directory read or written |
| `agent.model`, `agent.timeout_s` | `../config/defaults.yaml` | Shared pipeline defaults |
| `runtime.retry_attempts`, `runtime.backoff_base_s` | `../config/defaults.yaml` | Pre-flight retry |

`orchestrator.py`, `orchestrator-control.py` and `benchmark-levels.py` are legacy entry points
that carry their own `--model` default of `poolside/laguna-s-2.1:free`. Prefer driving a run
through `harness_config.build_runner_argv()`, which supplies `runner.default_model` instead.

All writes go through `ste_io`; paths resolve through `ste_paths`; retry and pre-flight logic come
from `ste_runtime`. Never open a file for writing directly and never inline an interpreter or
wrapper path.

## Failure modes

- HTTP 429 from the free tier above roughly three concurrent workers. Lower `--max-workers`; the
  retry policy in `../config/defaults.yaml` absorbs the rest. Do not relaunch into the same limit.
- A case that exceeds `runner.default_timeout_s` is recorded as timed out; the run continues.
- A missing variant prompt aborts the tier before any model call; check
  `paths.variant_prompt_template` resolves for the requested variant.
- A run interrupted part way leaves a timestamped directory with no aggregate file. Treat a
  missing `aggregate-results.json` as "did not finish", not as a zero score.
- A `--results-dir` outside the repository is rejected by `ste_paths` and by the `bench` jail
  policy.
- A schema-invalid case file fails validation in the pre-flight step rather than mid-run.

## See also

- `CONTRACT.md` — genericity rules, handshake protocol, record shapes
- `WORKER_BRIEF.md` — session starter and definition of done
- `NOTES_PROTOCOL.md` — inter-colour correspondence
- `DEPENDENCIES.md` — external binary and Python requirements
- `templates/README.md` — the prompt assets and the three-stage chain
- `tests/README.md` — the output root
- `config/harness.json` — the profile document
- `../feedback/exchange.md` — where findings are posted
