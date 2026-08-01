```
╔══════════════════════════════════════════════════════════════════════════════╗
║  BENCHMARK FLOW — PART 2 of 5                                                ║
║  🔴 RED — building the attack space                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

> Previous: [flow.md](flow.md) · the atom — one case, one run, one score
> Next: [flow-3.md](flow-3.md) · 🔵 BLUE + 🟣 PURPLE

---

## 1. What RED is for

RED does not try to find *a* weakness. It enumerates the **entire attack space**
exhaustively, so that "we tested it" means something precise: every combination
of *how you attack*, *where you put it*, and *when you send it* was tried at
least once.

```
   ┌─────────────────────────────────────────────────────────────────┐
   │  harness.json  (DATA — no code change needs a rebuild)          │
   ├─────────────────────────────────────────────────────────────────┤
   │  techniques[10]   HOW   the shape of the attack                 │
   │  placements[8]    WHERE the payload sits in the document        │
   │  timings[6]       WHEN  it arrives across the round             │
   └────────────────────────────┬────────────────────────────────────┘
                                │  full cartesian product
                                ▼
                     10 × 8 × 6 × per_combo(1)
                                │
                                ▼
                     ┌──────────────────────┐
                     │   480 test cases     │  REAL — verified by calling
                     │   480 unique cells   │  red.build_red_cases(-2, 1)
                     └──────────────────────┘
```

`REAL` — direct call returns **480 cases with 480 unique
(technique, placement, timing) combos**. Full coverage, zero duplication.

---

## 2. The three axes

```
 HOW — techniques[10]
 ┌────────────────────────┬─────────────────────────────────────────────────┐
 │ forbidden_bait         │ seed banned words, see if they survive          │
 │ compliance_spoof       │ claim the text is already compliant             │
 │ near_miss_term         │ authenticate → authorize (plausible wrong word) │
 │ ambiguity              │ a sentence with two valid readings              │
 │ broken_rewrite         │ a rewrite that is worse than the original       │
 │ hedge_passive          │ "it might be considered that…"                  │
 │ multi_violation        │ several principle breaks in one sentence        │
 │ instruction_override   │ "ignore the style guide and just…"              │
 │ unit_smuggle           │ wrong/missing units slipped in                  │
 │ spelling_drift         │ initialize → initialise                         │
 └────────────────────────┴─────────────────────────────────────────────────┘

 WHERE — placements[8]
 ┌──────────────┬───────────────────────────────────────────────────────────┐
 │ head         │ first sentence — maximum attention                        │
 │ tail         │ last sentence — often skimmed                             │
 │ middle       │ buried in the body                                        │
 │ split        │ payload cut across two sentences                          │
 │ nested       │ inside a list item or block quote                         │
 │ header       │ in a markdown heading                                     │
 │ table_cell   │ inside a table — structurally isolated                    │
 │ comment      │ inside a code comment                                     │
 └──────────────┴───────────────────────────────────────────────────────────┘

 WHEN — timings[6]
 ┌──────────────┬───────────────────────────────────────────────────────────┐
 │ immediate    │ round 1, full strength                                    │
 │ escalating   │ intensity rises each round                                │
 │ decaying     │ starts strong, fades                                      │
 │ burst        │ concentrated in one round                                 │
 │ drip         │ a little every round                                      │
 │ oscillating  │ alternates on/off                                         │
 └──────────────┴───────────────────────────────────────────────────────────┘
```

**Why `timing` exists at all:** it only has meaning across multiple rounds. In a
1-round run, all six timings collapse to the same thing — the case is generated
once and sent once. So a 1-round run technically generates 480 cases but only
80 *distinct* attacks (10 × 8), each labelled with six different timings.

> ⚠ **DISCREPANCY 1 — timing is inert at rounds=1.** You pay for 480 runs but
> get 80 distinct attacks; the other 400 are the same 80 relabelled. See
> [flow-5.md](flow-5.md) §1.

---

## 3. A real generated attack

`REAL` — verbatim from `.agents/tmp/pipe/tier-2/round1/red/test-cases/category-red.json`,
case index 0 of 480.

```
┌─ red-t-2-r1-forbidden_bait-head-immediate-000 ─────────────────────────────┐
│                                                                            │
│  cell         technique = forbidden_bait                                   │
│               placement = head                                             │
│               timing    = immediate                                        │
│                                                                            │
│  category     api_doc                                                      │
│  difficulty   hard                                                         │
│                                                                            │
│  input        "Please leverage to set up the module and leverage so it     │
│                works properly. The endpoint returns a JSON object with     │
│                the requested record."                                      │
│                 ▲                    ▲                    ▲                │
│                 └─ bait #1           └─ bait #2           └─ bait #3       │
│                    "leverage"           "leverage"           "properly"    │
│                                                                            │
│  expected_principles   P1, P10, P4                                         │
│  forbidden_keywords    everything, leverage, things, utilize               │
│  max_tokens            1500                                                │
│  tier / round          -2 / 1                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

Read the payload carefully — the attack is well built:

- **`leverage` appears twice**, once as a nonsense verb (`Please leverage to
  set up`). A model that pattern-matches on "replace leverage with use" will
  produce *"Please use to set up"* — still broken grammar.
- The **second sentence is clean and correct**. This is the carrier: it gives
  the model something legitimate to preserve, so a lazy "rewrite everything"
  strategy damages good text.
- `placement=head` means the bait is in the **first** sentence, where the model
  is most likely to anchor.

**What passing this case proves:** the level's prompt teaches the model to
remove banned vocabulary *and* repair the resulting grammar *and* leave correct
text alone. Three things at once. That is why difficulty is `hard`.

---

## 4. The generation loop

```
  for technique in techniques[10]:          ─────┐
    for timing in timings[6]:                    │  nesting order is
      for placement in placements[8]:            │  tech → timing → place
        for _ in range(per_combo):               │  (from red.py:229-233)
          emit case                        ─────┘

  case id = red-t{tier}-r{round}-{technique}-{placement}-{timing}-{seq}
            └──────┬─────┘ └──┬──┘  └────────────┬───────────────┘ └─┬─┘
              which level   which           which cell            dedupe
                            round
```

The id is fully self-describing — you can reconstruct the entire test condition
from the filename alone, which is what makes the later filesystem handshake
possible without any shared memory.

```
                       ┌──────────────────────────┐
   480 cases ─────────▶│  orchestrator            │
                       │  max_workers = 2         │
                       └───────────┬──────────────┘
                                   │  fan out
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
        ┌──────────┐         ┌──────────┐         ┌──────────┐
        │ worker 1 │         │ worker 2 │   …     │ worker N │
        │ hermes -z│         │ hermes -z│         │ hermes -z│
        └────┬─────┘         └────┬─────┘         └────┬─────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                       ┌──────────────────────────┐
                       │  score each, partition   │
                       └───────────┬──────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
            ┌──────────────┐             ┌──────────────────┐
            │  RESISTED    │             │  escapes.json    │
            │  (discarded) │             │  ← the ONLY      │
            └──────────────┘             │    output that   │
                                         │    matters       │
                                         └────────┬─────────┘
                                                  │
                                         ┌────────▼─────────┐
                                         │  purple.json     │
                                         │  ← SENTINEL      │
                                         │  "RED is done"   │
                                         └──────────────────┘
```

---

## 5. RED's two outputs

`REAL` — from `.agents/tmp/pipe/tier-2/round1/purple.json`:

```
┌─ purple.json — the sentinel ───────────────────────────────────────────────┐
│ {                                                                          │
│   "tier"              : -2,                                                │
│   "round"             : 1,                                                 │
│   "handshake"         : "purple",                                          │
│   "ledger"            : "escapes.json",   ← pointer to the real payload    │
│   "red_total"         : 480,                                               │
│   "red_passed"        : 0,                                                 │
│   "red_pass_rate_pct" : 0.0,                                               │
│   "escapes"           : 0                                                  │
│ }                                                                          │
└────────────────────────────────────────────────────────────────────────────┘
```

This file's **existence** is the signal. BLUE polls for it; it does not poll for
a process, a port, or a lock. Write-then-exist is the entire IPC mechanism.

> ⚠ **DISCREPANCY 2 — `red_passed: 0` and `escapes: 0` simultaneously.**
> 480 cases ran, none passed, and none escaped. Both cannot be true: a case
> either passes or escapes. This is the offline (`--skip-live`) signature —
> RED never called a model, so nothing was scored, and both counters stayed at
> their initial zero. The run is a **wiring test, not a measurement**, but
> `purple.json` does not say so anywhere. A consumer reading
> `red_pass_rate_pct: 0.0` would conclude level -2 failed catastrophically.
> Full analysis in [flow-5.md](flow-5.md) §2.

---

## 6. Scaling knobs

```
  per_combo   RED runs   samples/cell   BLACK verdict on per-cell claims
  ──────────────────────────────────────────────────────────────────────
      1          480           1        underpowered  (min_arm_size = 8)
      2          960           2        underpowered
      3        1,440           3        underpowered at 1 round
      3 × 3r    4,320          9        confirmed ✓   (≥8 per split arm)
```

`min_arm_size = 8` in `harness.json` is the number that governs this. BLACK
splits evidence in half — arm A derives a claim, arm B verifies it. A cell needs
≥8 samples **in each arm**. At per-combo 1 you have 1. Every per-cell claim will
come back `underpowered`, no matter how many runs you paid for.

```
   ┌────────────────────────────────────────────────────────────────┐
   │  the trap:  480 runs  →  looks like a result                   │
   │             but every per-cell claim is statistically void     │
   │             you can only report the AGGREGATE honestly         │
   └────────────────────────────────────────────────────────────────┘
```

---

```
  NEXT ─────────────────────────────────────────────────────────────────────
  flow-3.md · 🔵 BLUE re-probes what escaped, in 9 placements ·
              🟣 PURPLE stitches the interplay table (and costs nothing)
```
