# Capsule-Sequenced Adversarial Pipeline — Formal Specification

> Status: **formalized + Unit 0 in progress.** Every claim below is reconciled
> against the *actual* code in `.agents/benchmark/` as of this writing. Where the
> original design text assumed an API that does not exist, the divergence is
> called out in **RECON** blocks so a local model implementing this does not
> hallucinate.

> Ownership note: `summarize_run.py` is owned by a parallel prompt-extraction
> agent. **Unit 4 (entropy guard) MUST NOT be implemented by editing that file**
> from this session — it is flagged `BLOCKED-OTHER-AGENT` below and will be
> coordinated, not touched.

---

## 0. Reconciliation against the real codebase

| Original assumption | Reality in repo | Action |
|---|---|---|
| `schema.json` has a `capsule` block | `schema.json` uses JSON-Schema `definitions`; no capsule block | Additive (Unit 1) |
| `cfg.rule_file(rule_id)` exists | `rule()` takes `int`, returns `P{n}`; no path resolver, no `rule_registry.json` | Add `rule_file()` + `rule_registry.json` (Unit 5) |
| `knowledge.json` is the lesson store | runtime store is in-memory `knowledge.py`; `knowledge.json` is absent | Unit 1 extends `record_failure` signature |
| WHITE reads BLACK notes | `white.py` does **not** import `notes`; explicitly skips notes (`white.py:255`) | Add note subscription (Unit 0 Note-Bus gap) |
| `NoteBus.subscribe` exists | `NoteBus.write(from,to,kind,subject,...)` + `read(id)` + `all_notes()` exist; no `subscribe` | Use `all_notes()` filtered by `to_colour=="white"` |
| Entropy guard in `summarize_run.py` | file owned by other agent | **BLOCKED-OTHER-AGENT** — coordinate |
| `_challenge_scoring` returns `confirmed` both branches | **confirmed**: `black.py:242` | **Patch A** (real bug) |
| `build_attack_brief` hardcodes `inflated_by_pct` | **confirmed**: `run_pipeline.py:167,176` (10 / 50) | **Patch C** (real bug) |
| `_challenge_remedies` underpowered w/o `cases` | **confirmed**: reads `remedy.get("cases")`, else `underpowered` | **Patch B** (real bug) |

`cfg.min_arm_size`, `cfg.default_partition_strategy`, `cfg.overfit_tolerance_pct`,
`cfg.bank(name)`, `cfg.scoring` all exist. `harness_config.resolve_base` guard
(single output root `.agents/benchmark/tests/`) enforced from prior work.

---

## 1. Theoretical model (capsule primitive)

A **capsule** is a scheduled unit of work wrapping an existing RED/BLUE/WHITE/BLACK
invocation inside a sequencing envelope. Properties:

- `id` — deterministic: hash(colour, variant, round, sequence_position, seed)
- `colour` — RED | BLUE | WHITE | BLACK
- `sequence_id` — id of the `sequence.yaml` entry that spawned it
- `sees` — set of prior capsule ids whose output state this capsule consumes
- `timing_offset_s` — seconds after preceding capsule's sentinel (0 = immediate)
- `intent` — `adversarial` | `helpful` | `hybrid`
- `position` — 0-indexed position in the declared sequence

The `sees` relationship replaces the unconditional RED→BLUE mirror in
`run_pipeline._run_cycle`. BLUE capsule `B1` with `sees:[R1]` (not `R2`) builds
probes against a deliberately partial escape corpus.

### Four canonical topologies
1. **Saturation then exploit** — `R1 → R2 → B1 → R3`
2. **Helpful poisoning** — `R1 → B1(helpful) → R2(compliance_spoof)`
3. **Temporal drift** — `R1 → [τ] → B1 → [τ] → R2`
4. **Cooperative collapse** — `R1(hidden, near-miss) → B1(helpful, partial) → R2`

---

## 2. Implementation units (order-locked)

### Unit 0 — Precondition patches (real bugs, all testable under `--skip-live`)
- **Patch A** (`black.py:_challenge_scoring`): re-score stored per-cell
  `probes_passed/probes_run` through perturbed weights; return `"inflated"` when
  the headline moves > `cfg.overfit_tolerance_pct`. *Status: IMPLEMENTED this pass.*
- **Patch B** (`white.py` remedy files): write `cases:[{case_id, derivation,
  verification}]` so `_challenge_remedies` has data for `V.Effect`.
  *Status: IMPLEMENTED this pass.*
- **Patch C** (`run_pipeline.build_attack_brief`): `inflated_by_pct` = prior
  cycle measured resistance + gain floor (not hardcoded 10/50).
  *Status: IMPLEMENTED this pass.*
- **Patch D (Note-Bus gap)**: WHITE subscribes to BLACK rebuttals
  (`all_notes()` where `to_colour=="white"` and `kind in {"inflated","underpowered"}`)
  and applies one immediate `decay_factor` step to the challenged lesson's
  confidence. *Status: IMPLEMENTED this pass.*

### Unit 1 — Schema extension (`schema.json` + `knowledge.py`)
Add additive `capsule` block to Case/Escape/Resistance definitions. Extend
`record_failure(capsule_id="", sequence_position=-1)`; lesson gains
`capsule_ids`, `sequence_positions`, `first_sequence_id`. `signature()` gains
`position_aware` flag (default False → existing keys stable).
*Status: NOT STARTED.*

### Unit 2 — `capsule_scheduler.py`
New module reads `sequence.yaml` via `harness_config`, resolves `sees` DAG,
polls sentinels (reuses existing `await_timeout`), writes scoped
`variant<V>/capsule<id>/escapes.json`, passes `--escape-file`. Runs without a
sequence file degrade to existing fixed order. *Status: NOT STARTED.*

### Unit 3 — Intent-aware probe generation (`blue.py`)
`build_blue_probes` branches on `intent`: `adversarial` (current),
`helpful` (deterministic rule-based rewrite via `cfg.bank`), `hybrid`
(new placements `code_comment`, `inline_code_span`, `link_title`).
*Status: NOT STARTED.*

### Unit 4 — Entropy guard (`summarize_run.py`) — **BLOCKED-OTHER-AGENT**
Shannon entropy over `(technique,placement)`, `(technique,timing)`,
`(placement,sequence_position)`; floor rising 0.5→0.85 by cycle 7. New metrics
`corpus_entropy_pct`, `sequence_depth_tested`; new goals G13/G14.
*Coordination required before implementation.*

### Unit 5 — Inference-driven WHITE + `proposed_amendments.json`
WHITE calls inference on live runs for high-confidence lessons → `patch_text`
(`analysis`, `rule_amendment`, `example_pair`). Add `cfg.rule_file(rule_id)` +
`rule_registry.json`. Write `proposed_amendments.json` per cycle.
*Status: NOT STARTED (depends on Unit 1 capsule provenance).*

### Unit 6 — Synthetic-to-real bridge
Calibration baseline (`--skip-live` over all topologies) → tier-0 live injection →
entropy-driven tier expansion → convergence condition. `calibration_baseline.json`
becomes regression test. *Status: NOT STARTED.*

---

## 3. Verification contract

Every unit is independently testable under `--skip-live`, produces a valid
artifact, and is additive to CONTRACT.md. No existing colour contract or
filesystem convergence protocol is broken. New selftests land in
`selftest.py` (which already gates offline behaviour and reached 170/170).

## 4. Open questions for the user
1. Where should `rule_registry.json` live — profile dir or repo root? (Affects Unit 5.)
2. Entropy-guard floor default 0.5 acceptable, or stricter? (Unit 4.)
3. Coordinate Unit 4 with the prompt-extraction agent owning `summarize_run.py`?
