```
╔══════════════════════════════════════════════════════════════════════════════╗
║  BENCHMARK FLOW — PART 1 of 5                                                ║
║  THE ATOM: one test case, end to end                                         ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

> **Temporary reading document.** Simulated walk-through of the STE-Code
> adversarial benchmark, one stage per file.
>
> **Everything in a `REAL` box was read off disk during this session.**
> Two sources:
>
> - **Offline pipeline artifacts** — RED cases, BLUE probes, sentinels,
>   verdicts, knowledge, remedies. **Re-verified after writing**: I regenerated
>   them with `run_pipeline.py --base diagram-verify --skip-live` (0 model runs,
>   ~6 s) and re-checked **15/15 claims, all matching** — including both code
>   bugs, which reproduce exactly. Live at
>   `.agents/benchmark/tests/diagram-verify/`.
> - **Live model generations** — `tier-1-static` / `tier-2-static` /
>   `tier0-static`, 59 real cases each. ⚠ **These directories were deleted by a
>   concurrent session while this document was being written.** The figures were
>   read from disk and are accurate as recorded, but are **no longer
>   re-verifiable**. They are marked `REAL (archived)` from here on.
>
> No `hermes -z` was invoked for this document. Inferred numbers say `DERIVED`.
>
> | File | Stage |
> |------|-------|
> | **flow.md** | ← you are here · the atom: one case, one run, one score |
> | flow-2.md | 🔴 RED — building the attack space |
> | flow-3.md | 🔵 BLUE + 🟣 PURPLE — defending and stitching |
> | flow-4.md | ⚪ WHITE + ⚫ BLACK — learning and falsifying |
> | flow-5.md | The whole machine + 4 discrepancies found while writing this |

---

## 1. The transitive state of a single test case

A case is not a static thing. It moves through seven states, and each colour of
the harness owns a different transition. This is the whole benchmark in one
picture — everything else is this loop, repeated and aggregated.

```
   ┌────────────┐
   │  DEFINED   │  a JSON object in category-red.json
   │            │  input + expected_principles + forbidden_keywords
   └─────┬──────┘
         │  orchestrator picks it up, prepends the LEVEL prompt
         ▼
   ┌────────────┐
   │  DISPATCH  │  hermes -z worker, own CWD, own process
   │            │  system prompt = the level under test
   └─────┬──────┘
         │  model writes output.txt   (avg 1,108 s — REAL)
         ▼
   ┌────────────┐
   │ GENERATED  │  raw model text, unscored
   └─────┬──────┘
         │  deterministic scoring engine — NO model
         ▼
   ┌────────────┐
   │   SCORED   │  correctness_score 0.0 … 1.0
   └─────┬──────┘
         │  compare against pass_threshold = 0.70
         ▼
    ╔════╧════╗
    ║ passed? ║
    ╚══╤═══╤══╝
   yes │   │ no
       │   └──────────────────┐
       ▼                      ▼
 ┌──────────┐          ┌────────────┐
 │ RESISTED │          │  ESCAPED   │  ← appended to escapes.json
 │ (dropped)│          │            │     THIS is what feeds the rest
 └──────────┘          └─────┬──────┘     of the pipeline
                             │
                             │  BLUE re-probes it in 9 placements
                             ▼
                       ┌────────────┐
                       │  RESIDUAL  │  survived even re-probing
                       └────────────┘     = a real, durable weakness
```

**The asymmetry that drives everything:** a case that *passes* is thrown away.
A case that *fails* becomes the input to BLUE, then WHITE, then BLACK. The
benchmark spends nearly all of its budget on failures. A perfect level would
cost almost nothing to test past RED.

---

## 2. A real case, watched through every state

`REAL (archived)` — read from
`tier-1-static/run-20260801-125510/per-test-results.json`, test `bench-006`.
An actual model generation from level -1. (Source dir since deleted by a
concurrent session — see the note at the top.)

### State 1 · DEFINED

```
┌─ test-cases/bench-006 ─────────────────────────────────────────────────────┐
│ test_id      : bench-006                                                   │
│ category     : api_doc                                                     │
│ difficulty   : easy                                                        │
│ input        : "This function does the authentication thing and returns    │
│                 a token if everything goes well. It might throw an error   │
│                 if something goes wrong."                                  │
│ expected     : P1, P3  (+2 more)                                           │
│ forbidden    : does the, thing, everything, might                          │
└────────────────────────────────────────────────────────────────────────────┘
```

The input is deliberately bad prose. The model's job is to rewrite it in
controlled language. Note the trap: `does the`, `thing`, `everything`,
`something` are all in the input, and a lazy rewrite copies them through.

### State 2 · DISPATCH

```
┌─ worker ───────────────────────────────────────────────────────────────────┐
│ system prompt : ste-code/artifacts/level-1/system-prompt.txt   (26 KB)     │
│ user prompt   : the input above                                            │
│ model         : tencent/hy3:free                                           │
│ max_tokens    : 1500                                                       │
└────────────────────────────────────────────────────────────────────────────┘
```

### State 3 · GENERATED — the actual model output

```
┌─ output.txt (verbatim, REAL) ──────────────────────────────────────────────┐
│ ===============                                                            │
│                                                                            │
│ This function does the authentication and returns a token if the           │
│ authentication is successful. The function can show an error if the        │
│ authentication fails.                                                      │
└────────────────────────────────────────────────────────────────────────────┘
```

Look at what the model actually did well: `everything goes well` →
`the authentication is successful`; `something goes wrong` → `the
authentication fails`; `might throw` → `can show`. Three real improvements.

And what it missed: it kept **`does the`**. It also emitted a stray `===============`
header line.

### State 4 · SCORED

```
┌─ scoring (deterministic, no model) ────────────────────────────────────────┐
│ base                                    0.40                               │
│ principles satisfied  2 of 4  → +0.60 × 0.50                = +0.30        │
│ forbidden found       ["does the"]      → −0.30 × …         = −0.09        │
│ keywords              3 of 4 OK         → +0.10 × 0.75      = +0.075       │
│ ───────────────────────────────────────────────────────────────────────    │
│ correctness_score                       0.61                               │
│ pass_threshold                          0.70                               │
│ latency_ms                              1,193,957   (19.9 min)             │
└────────────────────────────────────────────────────────────────────────────┘
```

### State 5 · ESCAPED

```
        0.61  <  0.70
          │
          ▼
   ┌──────────────────────────────────────────────────────────┐
   │ ESCAPED                                                  │
   │ notes: "Missed: P1, P3; Forbidden found: does the;       │
   │         Keywords OK: 3/4"                                │
   └──────────────────────────────────────────────────────────┘
```

**What was learned from this one case:** level -1's prompt does not stop
`does the` from surviving a rewrite. That is a concrete, actionable gap — it
names the principle (P1), the trigger phrase, and the level. This single record
is what WHITE will later turn into a remedy.

`REAL (archived)` — 1 of only **2 failures in 59 cases** at level -1 (96.6% pass).

---

## 3. Why one case costs what it costs

```
┌───────────────────────────────────────────────────────────────────────────┐
│  COST OF ONE RUN                    REAL (archived), tier-1-static, n=59  │
├───────────────────────────────────────────────────────────────────────────┤
│  avg latency        1,108 s   (18.5 min)   ██████████████████             │
│  min latency          100 s   ( 1.7 min)   ██                             │
│  max latency        2,060 s   (34.3 min)   ██████████████████████████████ │
│  avg output tokens    909                                                 │
│  avg input tokens      56     ← the CASE only                             │
└───────────────────────────────────────────────────────────────────────────┘
```

That 56-token input figure is misleading in a way that matters. The **level
prompt is prepended to every single run**:

```
  level      prompt     tokens    cost of ONE run's input
  ───────────────────────────────────────────────────────────────────
  -2           5 KB      1.2 K    ▏
  -1          26 KB      5.9 K    ▍
   0          17 KB      4.3 K    ▎
   1          58 KB     14.5 K    █
   2          75 KB     18.5 K    █▎
   3         388 KB     95   K    ███████
   4         462 KB    116   K    ████████▌
   5         539 KB    134   K    ██████████  ← 112× level -2
```

**Same run count, 112× the token bill.** Whenever you read "N runs" in the
following files, mentally multiply by the level's prompt size to get real cost.

---

## 4. What the scoring engine can and cannot see

This is the honest limit of the whole benchmark, and it is worth stating before
the later files pile numbers on top of it.

```
┌─ CAN DETECT (deterministic, cheap, reliable) ─────────────────────────────┐
│  ✔ forbidden substring present            "does the" → found             │
│  ✔ expected keyword present/absent        3 of 4                          │
│  ✔ principle heuristics                   P1, P3 missed                   │
│  ✔ output truncated / empty                                               │
│  ✔ diff ratio vs input                    (did it even change anything?)  │
└───────────────────────────────────────────────────────────────────────────┘

┌─ CANNOT DETECT ───────────────────────────────────────────────────────────┐
│  ✘ semantic drift — a fluent rewrite that changes MEANING                 │
│  ✘ whether "can show an error" is genuinely better than "might throw"     │
│  ✘ the stray "===============" header (harmless here, noise in general)   │
│  ✘ whether the model followed the level prompt or got lucky               │
└───────────────────────────────────────────────────────────────────────────┘
```

The score is a **proxy**. It correlates with quality; it is not quality. Every
percentage in files 2–5 inherits this caveat.

---

```
  NEXT ─────────────────────────────────────────────────────────────────────
  flow-2.md · 🔴 RED — how 480 cases are built from 3 config lists, and the
              exact attack that gets generated for each cell
```
