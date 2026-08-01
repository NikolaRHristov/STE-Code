```
╔══════════════════════════════════════════════════════════════════════════════╗
║  BENCHMARK FLOW — PART 5 of 5                                                ║
║  THE WHOLE MACHINE  ·  and five discrepancies found while writing this       ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

> Previous: [flow-4.md](flow-4.md) · ⚪ WHITE + ⚫ BLACK
> Series start: [flow.md](flow.md)

---

## 1. The complete pipeline, one level, one round

```
  ╔═══════════════════════════════════════════════════════════════════════╗
  ║  config/harness.json — all naming and dimensions live here as DATA    ║
  ╚═══════════════════════╤═══════════════════════════════════════════════╝
                          │  10 techniques × 8 placements × 6 timings
                          ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ 🔴 RED                                                    480 runs    │
  │    enumerate the full attack space                                    │
  └───────────────────────────────┬───────────────────────────────────────┘
                                  │  writes escapes.json
                                  │  writes purple.json ◄── SENTINEL
                                  ▼
                        ┌─────────────────────┐
                        │ FILESYSTEM HANDSHAKE│  no pipes · no sockets
                        │ poll for a filename │  no shared memory
                        └─────────┬───────────┘
                                  ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ 🔵 BLUE                                                   864 runs    │
  │    re-probe each escape from 9 placements                             │
  └───────────────────────────────┬───────────────────────────────────────┘
                                  │  writes blue-done.json ◄── SENTINEL
                                  ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ 🟣 PURPLE                                                   0 runs    │
  │    stitch RED × BLUE into the interplay table                         │
  └───────────────────────────────┬───────────────────────────────────────┘
                                  │  writes report.json
                                  ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ ⚪ WHITE                                                    8 runs    │
  │    ingest → diagnose → synthesize → validate                          │
  │    knowledge.json persists ACROSS rounds and cycles                   │
  └───────────────────────────────┬───────────────────────────────────────┘
                                  │  writes white-done.json ◄── SENTINEL
                                  │  writes attack-brief.json
                                  ▼
  ┌───────────────────────────────────────────────────────────────────────┐
  │ ⚫ BLACK                                                 0–41 runs    │
  │    5 structural challenges + one test per hypothesis                  │
  └───────────────────────────────┬───────────────────────────────────────┘
                                  │  writes verdicts.json
                                  │  writes black-done.json ◄── SENTINEL
                                  │  writes notes/  ─────────┐
                                  ▼                          │
                        ┌─────────────────────┐              │
                        │  1,393 model runs   │              │
                        └─────────────────────┘              │
                                                             │
     ┌───────────────────────────────────────────────────────┘
     │  reverse-deduction: BLACK → WHITE
     ▼
  next cycle starts with a SMALLER attack surface
```

**Why the filesystem handshake matters:** every stage can be run by hand, in a
different shell, hours apart. Nothing holds a connection. A crashed stage leaves
its inputs intact, so you resume rather than restart. The sentinel files are the
entire coordination protocol.

---

## 2. Level ladder — what changes as the prompt grows

`REAL (archived)` — the three tiers that completed live runs (of 17
attempted). ⚠ These result dirs were deleted by a concurrent session mid-write;
figures are as recorded but no longer re-verifiable:

```
  level  prompt  pass    corr    avg latency
  ──────────────────────────────────────────────────────────────────
   -1     26 KB  96.6%   0.901   1,108 s   ████████████████████ 57/59
   -2      5 KB  93.2%   0.914   2,409 s   ███████████████████  55/59
    0     17 KB  84.7%   0.847     968 s   █████████████████    50/59
    1     58 KB    —       —         —     timed out
    2     75 KB    —       —         —     timed out
    3    388 KB    —       —         —     timed out
    4    462 KB    —       —         —     timed out
    5    539 KB    —       —         —     timed out
```

> ⚠ **The ladder is not monotonic, and the ordering is not what you would
> expect.** Level -1 (26 KB) beats level -2 (5 KB) — fine, more prompt helps.
> But level 0 (17 KB, *more* than -2) scores **worst** at 84.7%. And level -2
> has the *highest* average correctness (0.914) while having a lower pass rate
> than -1.
>
> With n=59 and 2–9 failures per tier, these gaps are inside the noise floor.
> **No ranking claim is supportable from this data.** The 5 completed-tier
> figures are a smoke test, not a measurement.

---

## 3. The five discrepancies

Found by reading artifacts against the code that wrote them. Ordered by
severity.

---

### ⚠ 1 · `blue_passed` is always 0 offline — REAL BUG

```
  observed   blue-done.json:  blue_passed = 0
                              blue_pass_rate_pct = 88.9
  computed   sum(resistance_table): 96 passed of 108 = 88.9%
  verdict    the RATE is right, the COUNT is wrong
```

**Cause** — `blue.py:289-296` (offline branch):

```
  289  per_test = []
  290  bp = 0                             ← initialised
  291  bt = len(probes)
  292  if args.skip_live:
  293      table = _offline_resistance(probes)
  294      blue_rate = round(sum(passed)/sum(run) * 100, 1)
  295                                     ← `bp` NEVER reassigned here
  296
  297  else:
  298      agg = _run_orchestrator(...)
  302      bp = agg.get("passed", 0)      ← live branch sets it correctly
  ...
  312  "blue_passed": bp,                 ← writes 0 offline, always
```

**Impact** — any consumer reading `blue_passed` instead of
`blue_pass_rate_pct` concludes the defense failed completely. The summarizer
being built in the other session is exactly such a consumer.

**Fix** — in the offline branch, set
`bp = sum(t["probes_passed"] for t in table)` before the write.

---

### ⚠ 2 · Offline runs are indistinguishable from catastrophic failure

```
  purple.json:  red_total 480 · red_passed 0 · red_pass_rate_pct 0.0 · escapes 0
                                    ▲                                      ▲
                     "nothing passed"                     "nothing escaped"
                                    └──────── cannot both be true ─────────┘
```

Under `--skip-live` RED never calls a model, so nothing is scored and both
counters stay at their initial zero. But **`purple.json` carries no
`simulated` flag** — unlike PURPLE's `report.json`, which does
(`"simulated": true`).

**Impact** — a 0.0% pass rate reads as total failure of the level. The
distinction between "measured zero" and "never measured" is invisible to any
downstream reader.

**Fix** — write `"mode": "offline"` / `"simulated": true` into `purple.json`
and `blue-done.json` whenever `--skip-live` is set. PURPLE already models the
right behaviour; copy it.

---

### ⚠ 3 · BLACK confirmed a tautology 40 times

```
  verdicts.json:  40 verdicts · 40 confirmed · 0 challenged
                  across 5 independent strategies
  on a run where:  escapes.json was EMPTY
                   blue_passed was PROVABLY WRONG (§1)
```

**Cause** — WHITE pruned all lessons (correct, per reverse-deduction), so it
published no hypotheses. `attack-brief.json` fell back to a single entry:

```
  "Baseline: the configuration under test shows no escapes."
```

Which was **trivially true** — escapes.json was empty. BLACK verified an empty
claim against empty data and confirmed it 40 times.

**Impact** — a verifier that cannot detect a known-broken input is not
verifying. The 40/40 result *looks* like strong validation and is worth nothing.

**Fix** — BLACK should emit `underpowered` (not `confirmed`) when the evidence
set is empty, and the run summary should surface "0 hypotheses tested" rather
than "40 confirmed".

---

### ⚠ 4 · `timing` is inert at `--rounds 1`

```
  480 cases generated   =  10 techniques × 8 placements × 6 timings
  80 DISTINCT attacks   =  10 × 8
  400 cases are the same 80, relabelled with a timing that never fires
```

All six timings (`immediate`, `escalating`, `decaying`, `burst`, `drip`,
`oscillating`) describe behaviour *across rounds*. In a single-round run they
are identical.

**Impact** — a 1-round run costs 6× what its information content justifies. At
the measured ~19 runs/hour, that is **21 wasted hours per level**.

**Fix** — either default `--rounds` to 6 so timings mean something, or collapse
timings to `immediate` when `rounds == 1` (480 → 80 runs, same information).
The second is the cheap win.

---

### ⚠ 5 · `--defense-timing delayed` silently does nothing

```
  build_blue_probes(10 escapes, timing="delayed", round_n=1)  →  0 probes
```

By design `delayed` defers to even rounds. But the default is `--rounds 1`, so
it produces 0 probes, 0 findings — **and still writes a `blue-done.json`
sentinel**. WHITE then proceeds on empty input and reports `status: done`.

**Impact** — a silently empty stage that looks successful at every downstream
checkpoint.

**Fix** — refuse the combination at argument-parse time, or have BLUE write
`status: deferred` instead of a success sentinel.

---

## 4. Discrepancy summary

```
  #  finding                                   kind          severity
  ────────────────────────────────────────────────────────────────────
  1  blue_passed always 0 offline              code bug      HIGH
  2  offline runs look like total failure      missing flag  HIGH
  3  BLACK confirms tautologies                design gap    HIGH
  4  timing inert at rounds=1                  6× waste      MEDIUM
  5  delayed writes a false success sentinel   design gap    MEDIUM
```

**The common thread:** every one of these makes a *non-result look like a
result*. None of them causes a crash; all of them survive into the reports.
That is the failure mode this harness is most exposed to — and, given that
BLACK exists precisely to catch it, the most important class to fix first.

---

## 5. What a real run costs

```
  throughput (REAL, measured)
  ──────────────────────────────────────────────────────────
  6 effective workers  (3 orchestrators × 2 max-workers)
  avg run 1,108 s
  → ~19 runs / hour

  scope                        runs      wall clock
  ──────────────────────────────────────────────────────────
  offline wiring test             0      6 seconds
  static suite, 1 level          59      ~3 hours
  full pipeline, 1 level      1,393      ~3 days
  verified, 1 level          12,243      ~27 days
  all 8 levels, verified     97,944      ~7 months
```

`REAL (archived)` — the last full attempt: **3 of 17 jobs completed, 14 timed
out** at the 3,600 s ceiling.

> The 60-minute per-job timeout is a **blocking defect**, not a tuning
> preference. A 480-case RED phase at 19 runs/hour needs 25 hours. It will
> *always* hit the wall. RED must be sharded, or `--timeout` raised past 90,000 s.

---

## 6. What each stage actually proves

```
  ┌──────────┬────────────────────────────┬───────────────────────────────┐
  │ stage    │ PROVES                     │ DOES NOT PROVE                │
  ├──────────┼────────────────────────────┼───────────────────────────────┤
  │ 🔴 RED   │ every attack cell was tried│ that the cells are realistic  │
  │ 🔵 BLUE  │ position vs technique split│ anything, if offline (88.9%   │
  │          │                            │ is a fixed placeholder)       │
  │ 🟣 PURPLE│ the two views are consistent│ nothing new — pure derivation│
  │ ⚪ WHITE │ a concrete prompt fix exists│ that it works (offline valid- │
  │          │                            │ ation is self-confirming)     │
  │ ⚫ BLACK │ conclusions survive re-      │ anything when the evidence   │
  │          │ weighting                  │ set is empty (see §3)         │
  └──────────┴────────────────────────────┴───────────────────────────────┘
```

---

## 7. Provenance

```
  REAL — re-verified after writing (fresh regeneration, 15/15 claims matched)
  ──────────────────────────────────────────────────────────────────────────
  tests/diagram-verify/                       regenerated offline pipeline
    run_pipeline.py --skip-live               0 model runs · ~6 seconds
    → 480 RED cases, 108 BLUE probes, sentinels, verdicts, knowledge,
      remedies, notes — ALL claims below re-checked and matching,
      INCLUDING both code bugs (§1, §2), which reproduce exactly

  REAL (archived) — read from disk, source since DELETED by a concurrent
  session mid-write; accurate as recorded, no longer re-verifiable
  ──────────────────────────────────────────────────────────────────────────
  tests/tier-1-static/run-20260801-125510/    59 live model generations
    per-test-results.json                     bench-006 verbatim output
    aggregate-results.json                    pass rates, latency, tokens
  tests/tier-2-static/, tests/tier0-static/   2 more completed tiers
  .agents/tmp/pipe/                           offline 4-cycle, 8 tiers
    tier-2/round1/red/…/category-red.json     480 RED cases
    tier-2/round1/blue/…/category-blue.json   108 BLUE probes
    tier-2/round1/purple.json, blue-done.json sentinels
    variant-2/round1/white-done.json          WHITE counters
    variant-2/round1/verdicts.json            40 BLACK verdicts
    knowledge.json, defended.json             3 patterns, 12 signatures
    notes/note-C-2a7c056b.json                reverse-deduction note
    remedies/adopted/rem-forbidden_bait-…     adopted remedy
    pipeline-report.json                      4-cycle convergence trend
  config/harness.json                         all dimensions
  red.py, blue.py, white.py, black.py         builder logic + the bugs

  DERIVED — computed, labelled at each use
  ──────────────────────────────────────────────────────────────────────────
  864 BLUE runs          96 escapes × 9, at an assumed 20% escape rate
  19 runs/hour           6 workers × 3600 s ÷ 1,108 s
  all wall-clock figures runs ÷ 19

  NOT DONE
  ──────────────────────────────────────────────────────────────────────────
  no hermes -z invoked · no model called · nothing generated for this document
```

---

```
  ═══════════════════════════════════════════════════════════════════════════
  flow.md → flow-2.md → flow-3.md → flow-4.md → flow-5.md
  ═══════════════════════════════════════════════════════════════════════════
```
