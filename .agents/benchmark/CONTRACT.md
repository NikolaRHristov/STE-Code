# Harness Contract — RED / BLUE / PURPLE / WHITE

Every participant in the adversarial benchmark obeys this contract. It exists so
that four independently-launched processes converge on disk without ever knowing
about each other, and so that the whole harness can be retargeted at a different
standard, product, or corpus by editing one JSON document.

## 1. Genericity rules (hard requirements)

A module in this harness **must not** contain, as a literal:

| Forbidden literal | Where it belongs instead |
|---|---|
| A project, standard, or product name | `profile.display_name` in the profile document |
| A directory layout such as `ste-code/artifacts/levelN/` | `paths.variant_prompt_template` |
| A variant identifier scheme (tier numbers, level names) | `variants.registry` |
| A word bank (forbidden terms, near misses, subjects, carriers) | `vocabulary.*`, read via `cfg.bank(name)` |
| A technique / placement / timing list | `techniques.enabled`, `placements.enabled`, `timings.enabled` |
| A scoring-backend flag name (`--test-dir`, `--model`, …) | `runner.argv_template` |
| A handshake filename (`escapes.json`, `purple.json`, …) | `handshake.*` |
| A scoring constant (0.40 base, 0.70 threshold, …) | `scoring.*` |
| A rule identifier prefix (`P1`…`P14`) | `profile.rule_prefix`, rendered via `cfg.rule(n)` |

The test for compliance is simple: **swap the profile document and the harness
must run against a completely different domain without a single code edit.**

Generic does not mean simple. The transformations, scheduling strategies, and
scoring logic stay as sophisticated as the problem demands — only the *nouns*
are externalized.

## 2. Vocabulary of the harness

The harness deliberately avoids the project's own terminology in its own code:

| Neutral term | What it happens to be in this deployment |
|---|---|
| **variant** | one prompt tier (`-2` … `5`) |
| **round** | one iteration of the adversarial loop |
| **runner** | `orchestrator.py`, invoked as a subprocess |
| **case** | one scored test input |
| **escape** | a case the variant failed to handle |
| **probe** | a BLUE-constructed re-test of an escape |
| **remedy** | a WHITE-proposed change to the variant |
| **handshake** | the filesystem convergence protocol |

`harness_config.py` is the only module allowed to know that a variant is a
prompt tier or that the runner is an orchestrator subprocess.

## 3. Configuration entry point

```python
from harness_config import load_config, add_common_arguments, default_base

cfg = load_config(args.profile)          # explicit path, $BENCH_HARNESS_PROFILE, or default
variants = cfg.parse_variants(args.variants)   # validates keys, expands "all"
prompt   = cfg.variant_prompt(key)             # Path to the configuration under test
rdir     = cfg.round_dir(base, key, n)         # Path to variant<slug>/round<n>
argv     = cfg.build_runner_argv(test_dir, prompt, results_dir, model=..., ...)
agg, per = cfg.read_run_artifacts(results_dir) # backend-agnostic result read
score    = cfg.scoring.score(...)              # the shared formula
```

`add_common_arguments(parser)` supplies `--profile --variants --rounds --seed
--base --model --max-workers --timeout --poll-interval --skip-live`. Every
participant uses it, so the flags never drift apart.

## 4. Handshake protocol

Convergence is **filesystem-only**. No pipes, no shared memory, no parent/child
relationship. Any participant may be a background process, a cron job, or a run
on a different machine against a shared volume.

```
<base>/variant<slug>/round<N>/
    escapes.json      RED   writes the ledger of failures
    purple.json       RED   writes the sentinel: "round N ledger is ready"
    blue-done.json    BLUE  writes probe results + resistance tables
    white-done.json   WHITE writes remedies + knowledge-base delta
    report.json       stitch output (at <base> root)
    knowledge.json    WHITE's cumulative knowledge base (at <base> root)
```

Rules:

1. A sentinel is written **last**, after its payload file, and **always** —
   including when the round produced zero findings. A missing sentinel means
   "did not run", never "ran and found nothing".
2. A consumer polls for the sentinel with a bounded `--await-timeout`. On
   timeout it records `status: "await-timeout"` for that round and **moves on**.
   Blocking forever is a contract violation.
3. Payload files are written atomically (temp file + rename) so a polling
   consumer never reads a half-written JSON document.
4. Filenames come from `cfg.handshake.*`. Never inline them.

## 5. Record shapes

### Case (RED output, BLUE probe, WHITE regression)

```
id, category, description, input,
expected_principles[], expected_keywords[], forbidden_keywords[],
max_tokens, difficulty,
adversarial_technique, placement, timing, round,
red|blue_probe|white_regression: true
```

IDs must be unique and **stable for a given (variant, round, seed)** so that
reruns are diffable.

### Escape (RED ledger entry)

```
variant, round, test_id, technique, placement, timing, category,
missed_principles[], forbidden_found[], correctness_score,
input, violating_output
```

### Resistance row (BLUE)

```
technique, placement, probes, passed, resistance_pct, residual_ids[]
```

### Remedy (WHITE)

```
id, trigger (escape ids), diagnosis, remedy_kind, target, patch_text,
confidence, validated_by (regression case ids), delta_resistance_pct
```

## 6. Determinism

Given the same profile, seed, variant, and round, generation is byte-identical.
Generators perform no network access and no model calls. Only the *runner*
touches a model. This makes `--skip-live` a complete, meaningful offline mode
for every participant, and makes self-tests fast and reproducible.

## 7. Self-test obligation

Every participant ships a `--skip-live` path that exercises its full logic
against synthetic fixtures under `paths.scratch`. A change is not done until
that path has been executed and its real output inspected. Scratch fixtures are
deleted afterward.
