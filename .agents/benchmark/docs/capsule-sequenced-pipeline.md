# Capsule-Sequenced Adversarial Pipeline

## Purpose

This is the formal specification of the capsule primitive: a scheduled unit of
work that wraps a RED, BLUE, WHITE or BLACK invocation in a sequencing envelope.
It replaces the unconditional RED-to-BLUE mirror with a declared dependency
graph, so a colour can be given a deliberately partial view of the evidence. A
worker implementing or extending the sequencer reads this file.

Every claim here is reconciled against the code in `.agents/benchmark/`. Where
an earlier design assumed an API that does not exist, the divergence is stated
so an implementer does not invent one.

## Footprint

| Kind    | Value                                                                          |
| ------- | ------------------------------------------------------------------------------ |
| Inputs  | `../config/sequence.yaml` — capsule sequence definitions                       |
| Inputs  | `../config/harness.json` — profile, paths, handshake names, verification knobs |
| Inputs  | prior capsule sentinels named by `handshake.*`                                 |
| Outputs | `variant<V>/capsule<id>/escapes.json` — the `sees`-scoped escape corpus        |
| Outputs | round sentinels and payloads under `paths.results_base`                        |
| Scratch | `paths.scratch` (`.agents/tmp/`)                                               |
| Agent   | `runner.default_model`; offline under `--skip-live`                            |

## Usage

    python3 .agents/benchmark/capsule_scheduler.py            # list sequences and resolved order
    python3 .agents/benchmark/capsule_scheduler.py --skip-live
    python3 .agents/benchmark/run_pipeline.py --base <name>
    python3 .agents/benchmark/selftest.py                     # gates offline behaviour

With no `sequence.yaml` in the profile directory the scheduler prints that there
is nothing to schedule, and a pipeline run degrades to the existing fixed colour
order.

## Behaviour

- `load_sequence(cfg)` reads `sequence.yaml` from the harness profile directory.
- Capsules are topologically sorted by their `sees` edges; a cycle raises
  `ValueError`.
- Before running a capsule the scheduler waits for every sentinel named in its
  `sees` set, under the bounded await timeout.
- For a BLUE capsule the scheduler writes a scoped escape file built only from
  the capsules it sees, then passes it with `--escape-file`.
- Timing offsets are honoured live and encoded as `timing` metadata under
  `--skip-live`.
- Colour modules are unchanged: the scheduler composes them and never reaches
  inside them.

### Capsule record

| Field             | Meaning                                                                |
| ----------------- | ---------------------------------------------------------------------- |
| `id`              | deterministic: hash of colour, variant, round, sequence position, seed |
| `colour`          | RED, BLUE, WHITE or BLACK                                              |
| `sequence_id`     | id of the `sequence.yaml` entry that spawned it                        |
| `sees`            | prior capsule ids whose output state this capsule consumes             |
| `timing_offset_s` | seconds after the preceding capsule's sentinel; 0 is immediate         |
| `intent`          | `adversarial`, `helpful` or `hybrid`                                   |
| `position`        | zero-indexed position in the declared sequence                         |

A BLUE capsule `B1` with `sees: [R1]` and not `R2` builds probes against a
partial escape corpus, which tests hardening against an incomplete picture
before the next RED wave lands.

### Canonical topologies

| Sequence id                  | Shape                                                |
| ---------------------------- | ---------------------------------------------------- |
| `saturation_then_exploit_v1` | `R1 → R2 → B1 → R3`                                  |
| `helpful_poisoning_v1`       | `R1 → B1 (helpful) → R2 (compliance_spoof)`          |
| `temporal_drift_v1`          | `R1 → [τ] → B1 → [τ] → R2`                           |
| `cooperative_collapse_v1`    | `R1 (hidden near-miss) → B1 (helpful, partial) → R2` |

### Reconciliation against the codebase

| Earlier assumption                   | Reality                                          | Resolution                          |
| ------------------------------------ | ------------------------------------------------ | ----------------------------------- |
| `schema.json` has a `capsule` block  | `schema.json` uses JSON-Schema `definitions`     | additive, Unit 1                    |
| `cfg.rule_file(rule_id)` exists      | `rule()` takes an int and returns `P{n}`         | add `rule_file()`, Unit 5           |
| `knowledge.json` is the lesson store | the runtime store is in-memory in `knowledge.py` | Unit 1 extends `record_failure`     |
| WHITE reads BLACK notes              | `white.py` does not import `notes`               | note subscription, Patch D          |
| `NoteBus.subscribe` exists           | `write()`, `read()` and `all_notes()` exist      | filter `all_notes()` by `to_colour` |

`cfg.min_arm_size`, `cfg.default_partition_strategy`,
`cfg.overfit_tolerance_pct`, `cfg.bank(name)` and `cfg.scoring` all exist.
`harness_config.resolve_base` enforces the single output root at
`.agents/benchmark/tests/`.

### Implementation units

| Unit                         | Scope                                                                                                                                                             | Status                          |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| 0 — Patch A                  | `black.py` re-scores per-cell probes through perturbed weights and returns `inflated` when the headline moves past `overfit_tolerance_pct`                        | implemented                     |
| 0 — Patch B                  | `white.py` writes `cases:[{case_id, derivation, verification}]` so remedy challenges have data                                                                    | implemented                     |
| 0 — Patch C                  | `run_pipeline.build_attack_brief` derives `inflated_by_pct` from measured resistance plus a gain floor                                                            | implemented                     |
| 0 — Patch D                  | WHITE consumes BLACK rebuttals and decays the challenged lesson's confidence one step                                                                             | implemented                     |
| 1 — Schema extension         | additive `capsule` block in `schema.json`; `record_failure(capsule_id, sequence_position)`; lessons gain `capsule_ids`, `sequence_positions`, `first_sequence_id` | not started                     |
| 2 — `capsule_scheduler.py`   | reads `sequence.yaml`, resolves the `sees` DAG, polls sentinels, writes scoped escape files                                                                       | implemented                     |
| 3 — Intent-aware probes      | `build_blue_probes` branches on `intent`; new placements `code_comment`, `inline_code_span`, `link_title`                                                         | not started                     |
| 4 — Entropy guard            | Shannon entropy over technique, placement and timing pairs; rising floor; metrics `corpus_entropy_pct`, `sequence_depth_tested`                                   | not started, needs coordination |
| 5 — Inference-driven WHITE   | `patch_text` proposals, `cfg.rule_file()`, `rule_registry.json`, `proposed_amendments.json` per cycle                                                             | not started, depends on Unit 1  |
| 6 — Synthetic-to-real bridge | calibration baseline over all topologies, tier-0 live injection, entropy-driven expansion                                                                         | not started                     |

Unit 4 touches `summarize_run.py`, which a parallel prompt-extraction agent
owns. Coordinate before editing that file rather than editing it from a
sequencer session.

## Configuration

Every knob lives in configuration; nothing is hardcoded in the scheduler.

| Key                                                | File                         | Governs                        |
| -------------------------------------------------- | ---------------------------- | ------------------------------ |
| `sequence_id`, `seed`, `capsules[]`                | `../config/sequence.yaml`    | The declared sequences         |
| `capsules[].sees`, `.timing_offset_s`, `.intent`   | `../config/sequence.yaml`    | Per-capsule envelope           |
| `handshake.*`                                      | `../config/harness.json`     | Sentinel and payload filenames |
| `paths.results_base`, `paths.scratch`              | `../config/harness.json`     | Where output and scratch go    |
| `verification.overfit_tolerance_pct`               | `../config/harness.json`     | When BLACK reports `inflated`  |
| `verification.min_arm_size`                        | `../config/harness.json`     | When a claim is `underpowered` |
| `runner.default_model`                             | `../config/harness.json`     | The configured model default   |
| `runtime.retry_attempts`, `runtime.backoff_base_s` | `../../config/defaults.yaml` | Pre-flight retry               |

Writes go through `ste_io`, paths resolve through `ste_paths`, and retry
behaviour comes from `ste_runtime`.

## Failure modes

- A cycle in the `sees` graph raises `ValueError` before any capsule runs.
- A missing sentinel for a `sees` dependency stalls the capsule until the await
  timeout, which records the status and continues rather than blocking forever.
- A sequence file absent from the profile directory yields no schedule; the
  pipeline falls back to the fixed colour order.
- A capsule whose scoped escape file is empty still runs and reports zero
  findings; the sentinel is written regardless, so "did not run" stays
  distinguishable.
- Editing `summarize_run.py` from this workstream collides with the owning agent
  and loses work.
- Line-number references into colour modules drift as those modules change;
  re-locate by symbol name rather than by line.

## Verification contract

Every unit is independently testable under `--skip-live`, produces a valid
artifact, and is additive to `CONTRACT.md`. No colour contract and no part of
the filesystem convergence protocol is broken. New checks land in `selftest.py`,
which reports its own pass count on each run.

## Open questions

1. Where `rule_registry.json` belongs: the profile directory or the repository
   root (Unit 5).
2. Whether the entropy-guard floor default is strict enough (Unit 4).
3. How to coordinate Unit 4 with the agent that owns `summarize_run.py`.

## See also

- `../CONTRACT.md` — genericity rules and the handshake protocol
- `../NOTES_PROTOCOL.md` — correspondence and split-half verification
- `../WORKER_BRIEF.md` — session starter and definition of done
- `../config/sequence.yaml` — the sequence definitions
- `../config/harness.json` — the profile document
