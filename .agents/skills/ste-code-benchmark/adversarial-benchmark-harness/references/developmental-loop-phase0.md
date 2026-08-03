# The developmental loop (RED-obsolescence) — Phase 0 plan

This is the class of work where the five colours are not a fixed red/blue system
but a **developmental adversarial pipeline**: early-underdeveloped agents help
discover the failure space, WHITE+BLACK mature first (they are deterministic
meta-processes), which DELINEATES RED's full generation space. Once BLACK has
confirmed every (technique, placement) pair as covered/equivalent/invalid, RED
becomes **obsolete** — the attack space is closed and frozen as a taxonomy. The
driver (`run_pipeline.py`) loops cycles until that happens.

> Source of truth for this plan: `.agents/tmp/next/INSTRUCTIONS.md` §3/§5/§6 and
> `.agents/tmp/remote/10.md` (the "corrected, reality-grounded" plan). The
> `remote/1`–`10.md` files are a REMOTE RESEARCH AGENT's spec — treat its
> _ideas_ as sound but its _provenance_ (arxiv 2602.x, NIST, ACM citations) as
> UNVERIFIED. Several look like future-dated placeholders.

## Entity model (the benchmark is a small set of distinct things)

- **TEST CASE** — static input data in `test-cases/category-*.json`. Does
  nothing.
- **RED** — adversarial generator. DETERMINISTIC (no LLM call); mutates inputs
  across technique × placement × timing. In `red.py` / `adversarial.py`.
- **BLUE** — defender/scorer. Reads RED's escapes, builds probes, calls the
  orchestrator which invokes the MODEL per case, scores. `blue.py`.
- **WHITE** — knowledge synthesizer. Deterministic Python (no LLM). Reads
  probes/scores, writes `lessons.json`, prunes. `white.py` / `knowledge.py`.
- **BLACK** — verifier/closure engine. Deterministic Python (no LLM). Reads
  lessons, writes `verdicts.json` (confirmed / inflated / underpowered / unsound
  / equivalent). `black.py` / `verification.py`.
- **PURPLE** — STUB in the current code: `_write_stitch_reports()` writes
  `simulated:True` with a hardcoded rising curve (5,35,65,95). It is the
  intended provenance/attestation layer, NOT a separate orchestrator.
- **`run_pipeline.py` IS the orchestrator (driver)**, not a data entity.

## Key distinction (user's framing, confirmed correct)

A test case is **DATA**. RED and BLUE are **DRIVERS** that launch/transform it.
BLUE must NEVER grade its own generated attacks — adversarial input must come
from RED (the **provenance bond**). PURPLE's job is to ATTEST that BLUE's input
came from RED, not from BLUE (`provenance.generator == "RED"`).

## What was actually broken (verified against the real code)

- (a) RED emits 0 escapes live: `_run_cycle()` launches RED with `--emit-only`,
  and RED's `--emit-only` path records escapes ONLY from a model run's
  `per-test-results.json` (which never happens) → `escapes.json` is `[]`.
- (b) BLUE is hardcoded `--skip-live` (`run_pipeline.py` ~line 242) → never
  calls the model on RED's escapes; short-circuits to `no-escapes` / offline.
- (c) WHITE + BLACK hardcoded `--skip-live` (~lines 254, 268) → fragile
  simulated verdicts. BLACK can "confirm a claim built from empty evidence"
  (`black.py` ~lines 178-189 already guard this — preserve the guard).
- (d) `excluded_pairs` pruning edge exists in the driver (`main()` builds
  `excluded_pairs` from BLACK-confirmed defended claims) but RED has NO
  `--exclude-pairs` flag to receive it → the BLACK→RED feedback edge is dead.
- (e) No closure detector: `main()` loops a FIXED cycle count (default 4); the
  RED-obsolete endpoint has no detector.

## The Phase 0 fix set (do these FIRST)

1. **Remove hardcoded `--skip-live` on BLUE/WHITE/BLACK** in `_run_cycle()`;
   propagate the real `live` flag
   (`live = [] if skip_live else ["--model", model]`). Keep RED as `--emit-only`
   (RED never calls a model — that is correct).
2. **Make RED's escapes reach BLUE for real.** In `red.py` `_emit_round`, when
   `--emit-only`, map RED's GENERATED cases into the escape record shape BLUE
   expects (`test_id`, `technique`, `category`, `placement`, `timing`,
   `missed_principles`, `forbidden_found`, `correctness_score` low, `input`,
   `violating_output`) with `"simulated": False`, `"generator": "RED"`, and
   `provenance{"generator":"RED","session_id":...}`. Preserve the model-run
   escape-population branch as an alternative. `escapes.json` must be NON-EMPTY
   after `--emit-only`.
3. **Add `--exclude-pairs <file>` to `red.py`** (JSON
   `{"exclude":[["tech","place"],...]}`). `build_red_cases` SKIPS any
   (technique, placement) pair in that set. Driver writes `excluded_pairs.json`
   and passes its path into the NEXT cycle's RED launch — this is the BLACK→RED
   pruning edge that makes RED obsolete.
4. **Minimal closure detector in `run_pipeline.py` `main()`**: track
   `coverage = len(excluded_pairs) / total_pairs` where
   `total_pairs = len(techniques) * len(placements)` (RED's 10 techniques × 8
   placements = 80; import `red._adv.TECHNIQUES + red.NEW_TECHNIQUES` and
   `red.PLACE_OPTIONS`, wrapped in try/except). Append `closure` to each
   `cycles_report`:
   `{"total_pairs", "excluded_pairs", "coverage", "red_obsolete": coverage >= 0.95}`.
   **Early-stop the cycle loop when `coverage >= 0.95`** (keep `--cycles` as a
   max). Write `closure-report.json`.

## HARD CONSTRAINTS (do NOT violate)

- **DO NOT add an LLM call/generator to RED.** Its generator (`build_red_cases`)
  is already deterministic and correct; the bug is the `--emit-only`
  empty-escapes handoff + hardcoded `--skip-live`, NOT a missing generator.
  Injecting an LLM into RED breaks the "WHITE/BLACK deterministic" invariant the
  spec wants. Preserve RED's determinism (id = pure fn of tier, round, seed,
  technique, placement, timing, sequence).
- **Respect `harness_config.py`.** Never hardcode sentinel filenames or dir
  layouts; read via `cfg.handshake` / `cfg.round_dir` / `cfg.red_ledger_path`.
- **Keep `--skip-live` offline path working** so `selftest.py` still passes
  (178/178).
- **Preserve BLACK's empty-evidence guard** (`brief-coverage` → `underpowered`
  when WHITE publishes no falsifiable hypotheses). Don't weaken it.

## REJECT the remote spec's priority order (over-engineered for this risk profile)

The remote agent front-loads: differential-perplexity watermarking / 4-tier
contamination taxonomy; LLM-as-judge calibration (Cohen's kappa, swap-and-
aggregate); CUPED / Bonferroni / Pareto cost modeling; OpenTelemetry spans.
REJECT all of these for NOW — the pipeline can't even run a live adversarial
pass (RED emitted 0 escapes), so you can't variance-reduce data you don't have.
These are defenses for a mature pipeline; fix the foundational handoff first.
Adopt the remote spec's _philosophy_ + schemas (provenance, separation, 4-dim
closure score ≥0.9) as target-state, implement the 2 foundational fixes, then
the closure detector.

## Validation (real output, not recollection)

1. Offline still works:
   `python3 .agents/benchmark/run_pipeline.py --base .agents/benchmark/tests/redblue --skip-live --rounds 2 --cycles 2 --tiers 2`
   → "PIPELINE COMPLETE", `pipeline-report.json` written.
2. RED handoff (no model):
   `python3 .agents/benchmark/red.py --tiers 2 --rounds 1 --out-dir .agents/benchmark/tests/redblue --emit-only`
   then `wc -c .agents/benchmark/tests/redblue/tier2/round1/escapes.json` → MUST
   be > 2 bytes, non-empty JSON array.
3. `python3 -m py_compile .agents/benchmark/run_pipeline.py .agents/benchmark/red.py .agents/benchmark/blue.py`
4. `python3 .agents/benchmark/selftest.py` → target 178/178 (check
   `selftest.py --help` first for flags).
