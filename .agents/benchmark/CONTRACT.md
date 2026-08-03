# Harness Contract

## Purpose

This contract binds every participant in the adversarial benchmark: RED, BLUE,
PURPLE, WHITE and BLACK. It exists so that independently launched processes
converge on disk without knowing about each other, and so that the whole harness
retargets at a different standard, product or corpus by editing one profile
document. Harness authors and any worker that adds a colour module read it
before they write code.

## Footprint

Resolved from `.agents/benchmark/config/harness.json`.

| Kind    | Value                                                                                   |
| ------- | --------------------------------------------------------------------------------------- |
| Inputs  | `config/harness.json` (profile document), `paths.static_cases`, `paths.generated_cases` |
| Inputs  | `paths.variant_prompt_template` — the configuration under test                          |
| Outputs | `paths.results_base` (`.agents/benchmark/tests`), `paths.state`                         |
| Scratch | `paths.scratch` (`.agents/tmp`), deleted after a run                                    |
| Agent   | `runner.default_model`, `runner.default_max_workers`, `runner.default_timeout_s`        |

## Usage

This document is read, not executed. Verify that the harness still honours it:

    python3 .agents/benchmark/selftest.py
    python3 .agents/benchmark/harness_config.py

## Behaviour

- `harness_config.py` loads the profile document and is the only module allowed
  to know that a variant is a prompt tier and that the runner is an orchestrator
  subprocess.
- Each colour writes its payload file, then its sentinel file, into the round
  directory.
- A consumer polls for a sentinel under a bounded `--await-timeout` and moves on
  when it expires.
- Payload files are written atomically (temp file plus rename), so a poller
  never reads half a document.
- Generation is deterministic for a given profile, seed, variant and round, so
  reruns are diffable.
- Only the runner touches a model; every generator is offline, which makes
  `--skip-live` complete.

## Configuration

Every knob lives in `.agents/benchmark/config/harness.json`; the shared agent
defaults live in `.agents/config/defaults.yaml`. Knobs are never hardcoded in a
module.

| Key                                                                 | Governs                                       |
| ------------------------------------------------------------------- | --------------------------------------------- |
| `profile.display_name`, `profile.rule_prefix`, `profile.rule_count` | Project nouns and rule ids                    |
| `paths.*`                                                           | Every directory the harness reads or writes   |
| `variants.registry`, `variants.order`                               | Variant ids and their on-disk directory names |
| `runner.argv_template`, `runner.entrypoint`                         | How the scoring backend is invoked            |
| `runner.default_model`                                              | The configured model default for the harness  |
| `handshake.*`                                                       | Every convergence filename                    |
| `scoring.*`                                                         | Base, weights, penalties and `pass_threshold` |
| `vocabulary.*`                                                      | Word banks, read through `cfg.bank(name)`     |
| `techniques.enabled`, `placements.enabled`, `timings.enabled`       | Enabled generator dimensions                  |
| `verification.*`                                                    | BLACK's split-half strategy and tolerance     |

### Genericity rules

A module must not contain any of these as a literal:

| Forbidden literal                                       | Where it belongs                                  |
| ------------------------------------------------------- | ------------------------------------------------- |
| A project, standard or product name                     | `profile.display_name`                            |
| A directory layout such as `ste-code/artifacts/levelN/` | `paths.variant_prompt_template`                   |
| A variant identifier scheme                             | `variants.registry`                               |
| A word bank                                             | `vocabulary.*`, read via `cfg.bank(name)`         |
| A technique, placement or timing list                   | `techniques.enabled` and siblings                 |
| A scoring-backend flag name                             | `runner.argv_template`                            |
| A handshake filename                                    | `handshake.*`                                     |
| A scoring constant                                      | `scoring.*`                                       |
| A rule identifier prefix                                | `profile.rule_prefix`, rendered via `cfg.rule(n)` |

The compliance test is simple: swap the profile document and the harness runs
against a different domain with no code edit. Generic does not mean simple —
only the nouns are externalized.

### Vocabulary

| Neutral term | What it is in this deployment              |
| ------------ | ------------------------------------------ |
| variant      | one prompt tier (`-2` … `5`)               |
| round        | one iteration of the adversarial loop      |
| runner       | `orchestrator.py`, invoked as a subprocess |
| case         | one scored test input                      |
| escape       | a case the variant failed to handle        |
| probe        | a BLUE-constructed re-test of an escape    |
| remedy       | a WHITE-proposed change to the variant     |
| handshake    | the filesystem convergence protocol        |

### Entry point

```python
from harness_config import load_config, add_common_arguments, default_base

cfg      = load_config(args.profile)           # path, $BENCH_HARNESS_PROFILE, or default
variants = cfg.parse_variants(args.variants)   # validates keys, expands "all"
prompt   = cfg.variant_prompt(key)             # Path to the configuration under test
rdir     = cfg.round_dir(base, key, n)         # Path to variant<slug>/round<n>
argv     = cfg.build_runner_argv(test_dir, prompt, results_dir, model=..., ...)
agg, per = cfg.read_run_artifacts(results_dir) # backend-agnostic result read
score    = cfg.scoring.score(...)              # the shared formula
```

`add_common_arguments(parser)` supplies
`--profile --variants --rounds --seed --base --model --max-workers --timeout --poll-interval --skip-live`,
so the flags never drift apart.

### Handshake protocol

Convergence is filesystem-only: no pipes, no shared memory, no parent/child
relationship. A participant may be a background process, a scheduled job, or a
run on another machine against a shared volume.

```
<base>/variant<slug>/round<N>/
    escapes.json      RED   ledger of failures
    purple.json       RED   sentinel: "round N ledger is ready"
    blue-done.json    BLUE  probe results and resistance tables
    white-done.json   WHITE remedies and knowledge-base delta
    report.json       stitch output (at <base> root)
    knowledge.json    WHITE cumulative knowledge base (at <base> root)
```

1. A sentinel is written last, after its payload, and always — including for a
   round with zero findings. A missing sentinel means "did not run", never "ran
   and found nothing".
2. A consumer polls under a bounded `--await-timeout`, records
   `status: "await-timeout"` on expiry, and continues. Blocking forever violates
   this contract.
3. Payload files are written atomically.
4. Filenames come from `cfg.handshake.*` and are never inlined.

All writes go through the shared `ste_io` helpers; paths resolve through
`ste_paths`, which keeps a write inside the checkout.

### Record shapes

Case (RED output, BLUE probe, WHITE regression):

```
id, category, description, input,
expected_principles[], expected_keywords[], forbidden_keywords[],
max_tokens, difficulty,
adversarial_technique, placement, timing, round,
red|blue_probe|white_regression: true
```

Ids are unique and stable for a given (variant, round, seed).

Escape (RED ledger entry):

```
variant, round, test_id, technique, placement, timing, category,
missed_principles[], forbidden_found[], correctness_score,
input, violating_output
```

Resistance row (BLUE):

```
technique, placement, probes, passed, resistance_pct, residual_ids[]
```

Remedy (WHITE):

```
id, trigger (escape ids), diagnosis, remedy_kind, target, patch_text,
confidence, validated_by (regression case ids), delta_resistance_pct
```

## Failure modes

- A missing sentinel stalls the consumer until `--await-timeout`, which then
  records `await-timeout` for that round and continues.
- A non-atomic write lets a poller read a truncated JSON document and abort the
  round.
- A hardcoded noun silently binds the harness to this deployment; the profile
  swap then fails.
- An unbounded wait deadlocks the pipeline, because no colour supervises
  another.
- The free-tier backend returns HTTP 429 above roughly three concurrent workers;
  lower `--max-workers` and rely on the retry policy in
  `.agents/config/defaults.yaml`.
- A participant that writes outside `paths.results_base` is refused by the
  `bench` jail policy.

## Self-test obligation

Every participant ships a `--skip-live` path that exercises its full logic
against synthetic fixtures under `paths.scratch`. A change is not done until
that path has run and its real output has been read. Scratch fixtures are
deleted afterwards.

## See also

- `NOTES_PROTOCOL.md` — inter-colour correspondence, the WHITE→BLACK brief,
  split-half A/B
- `WORKER_BRIEF.md` — session starter for every harness worker
- `DEPENDENCIES.md` — external binary and Python requirements
- `docs/capsule-sequenced-pipeline.md` — capsule scheduling specification
- `config/harness.json` — the profile document
- `../config/defaults.yaml` — shared agent defaults
