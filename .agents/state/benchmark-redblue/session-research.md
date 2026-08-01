# STE-Code Benchmark — Session Research & State Report

**Generated:** 2026-08-01T14:13:59Z (17:13 local, +0300)
**Repo:** `/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code` (branch `Current`)
**Machine-readable companion:** `.agents/state/benchmark-redblue/progress.json`
**Method:** read-only. No process was killed, restarted, or signalled. Nothing under `.agents/benchmark/` was modified.

---

## (a) Which Hermes session started the run, and what it intended

| Field | Value |
|---|---|
| Session | @session:ste-code/20260801_144007_52c08e |
| Title | "Rewriting stale README and cleaning artifacts" |
| Source / profile | `tui` / `ste-code` |
| Session model | `tencent/hy3:free` |
| Launching message | id **8229** — "Clean. Now relaunch the full live benchmark into `tests/`." |
| Background handle | `proc_2a53c5526acf` (an earlier attempt, `proc_4045f9d015cf`, exited **143** = SIGTERM) |

The benchmark was **not** the session's original purpose. The session began as a README/artifact cleanup task (msg 7365). Mid-session it authored two new scripts — `generate_adhoc_tests.py` and `run_all_variations.py` — and then launched the full tier matrix as a validation sweep.

Launch command recovered from session msg 8229, byte-identical to the live `ps` entry for **pid 80955**:

```bash
python3 .agents/benchmark/run_all_variations.py \
  --model tencent/hy3:free \
  --max-orchestrators 3 \
  --max-workers 2 \
  --timeout 600 \
  --seed 7 > .agents/benchmark/tests-run.log 2>&1
```

Launch history — the run was started, killed, and relaunched three times:
1. `proc_bb6d4875daf7` — first launch; deliberately killed so a verification script could temporarily swap `test-cases/` and `test-cases-adhoc/` aside.
2. `proc_4045f9d015cf` — exited **143** (SIGTERM, 128+15).
3. **Current run, pid 80955, started 15:55:10 local.** This is the process on disk now.

### Intent, in the session's own words (msg 7734)

> "It runs all 8 tiers × 2 (static + adhoc = 16 orchestrators) + 1 control = 17 jobs, capped at 3 concurrent. With ~2 workers each at ~60s/call on the free model, 59 static + 146 adhoc per tier... At 3 concurrent orchestrators × 2 workers = 6 simultaneous calls, ~6 cases/min → 17 jobs × ~100 cases avg / 6 ≈ 280 min."

The session pre-verified the runner with a mock `hermes` binary and reported **11/11 checks passing**, including "creates all 17 variation dirs" and "writes `aggregate-results.json` for every job". That verification used an instant mock, so **it could not surface the wall-clock timeout defect** — the defect only exists under real model latency.

---

## (b) The ORIGINAL PLAN as stated in that session

Taken from `run_all_variations.py` (lines 42–130) and the session narrative.

| Parameter | Planned value |
|---|---|
| Tier list | `TIERS = [-2, -1, 0, 1, 2, 3, 4, 5]` — 8 tiers |
| Prompt per tier | `ste-code/artifacts/level<N>/system-prompt.txt` |
| Variants | **static** (`test-cases/`, 59 cases) and **adhoc** (`test-cases-adhoc/`, generated pre-run, seed 7) |
| Control | 1 × `orchestrator-control.py` (plain assistant, no STE-Code prompt) on the static suite |
| Total jobs | 8 × 2 + 1 = **17** |
| Orchestrator concurrency cap | 3 (global, `ThreadPoolExecutor(max_workers=3)`) |
| Worker fan-out per orchestrator | 2 (`--max-workers 2`) → 6 simultaneous model calls |
| Per-test timeout | 600 s (`--timeout 600`, passed to the orchestrator) |
| **Per-job timeout** | **3600 s — hardcoded `subprocess.run(..., timeout=60*60)` at line 54, no CLI flag** |
| Model | `tencent/hy3:free` |
| Seed | 7 |
| Output | `.agents/benchmark/tests/<job>/run-*/`, final `tests/comparison.json` |

**Naming convention:** `tier-1` = level **minus one**, `tier-2` = level **minus two**. `tier0`..`tier5` are the non-negative levels.

**Plan-vs-reality discrepancy #1:** the plan assumed the adhoc suite was comparable in size to the static suite. `generate_adhoc_tests.py --seed 7` actually emitted **146 cases across 21 categories** (confirmed in `tests-run.log`) against a 59-case static suite — **2.47×** larger. Job scheduling and the timeout were never adjusted for this.

---

## (c) ACTUAL progress from disk evidence

Evidence sources: `ps -axo`, `.agents/benchmark/tests-run.log`, per-job `*.log`, `run-*/aggregate-results.json`, and counts of `run-*/*-output.txt`.

### Live processes (verified via `ps`)

| PID | Job | Started (local) | Elapsed at report |
|---|---|---|---|
| 80955 | `run_all_variations.py` (parent) | 15:55:10 | 4729 s (78.8 min) |
| 94297 | orchestrator `tier-1-adhoc` (level-1) | 16:29:31 | 2668 s |
| 2574 | orchestrator `tier0-static` (level0) | 16:51:16 | 1363 s |
| 3421 | orchestrator `tier0-adhoc` (level0) | 16:55:10 | 1129 s |

The scheduler chain is fully consistent with cap=3 and the job ordering in the source:

- 15:55:10 — first 3 jobs dispatched: `tier-2-static`, `tier-2-adhoc`, `tier-1-static`.
- 16:29:31 — `tier-1-static` finished (2061 s) → slot freed → **`tier-1-adhoc` started**. ✓
- 16:51:16 — `tier-2-static` finished (3366 s) → slot freed → **`tier0-static` started**. ✓
- 16:55:10 — `tier-2-adhoc` hit the 3600 s cap → slot freed → **`tier0-adhoc` started**. ✓

### `tests-run.log` (verbatim)

```
[gen] generating ad-hoc tests (seed=7) ...
Generated 146 ad-hoc cases across 21 categories -> .../test-cases-adhoc
[run] 17 orchestrator jobs, cap=3 concurrent, model=tencent/hy3:free
  done tier-1-static: rc=0 pass=96.6% (57/59) in 2061s
  done tier-2-static: rc=0 pass=93.2% (55/59) in 3366s
  done tier-2-adhoc: rc=-1 (no aggregate) in 3600s
```

`tests/tier-2-adhoc.log` contains exactly one line: `TIMEOUT after 60m`.

### Measured throughput

| Job | Status | Outputs | Elapsed | s/test (wall) | Projected full job | Verdict vs 3600 s |
|---|---|---|---|---|---|---|
| `tier-2-static` | done | 59/59 | 3366 s | 57.1 | 3366 s (56.1 min) | FITS — by only 234 s |
| `tier-2-adhoc` | **timed-out** | 122/146 | 3600 s | 29.5 | 4308 s (71.8 min) | **EXCEEDS** |
| `tier-1-static` | done | 59/59 | 2061 s | 34.9 | 2061 s (34.4 min) | FITS |
| `tier-1-adhoc` | running | 93/146 | 2668 s | 28.7 | 4188 s (69.8 min) | **EXCEEDS** |
| `tier0-static` | running | 41/59 | 1363 s | 33.2 | 1961 s (32.7 min) | FITS |
| `tier0-adhoc` | running | 40/146 | 1129 s | 28.2 | 4121 s (68.7 min) | **EXCEEDS** |

**Totals: 414 of 1699 expected outputs written (24.4%). Only 2 of 17 aggregates exist (11.8%).**

Completed, valid results — the only trustworthy science produced so far:

- **`tier-1-static` (level-1): 96.6% pass, 57/59**, avg correctness 0.901, 59/59 workers SUCCESS.
- **`tier-2-static` (level-2): 93.2% pass, 55/59**, avg correctness 0.914, 58 SUCCESS / 1 TIMEOUT.

### Caution on a misleading metric

`aggregates.avg_latency_ms` (1,108,386 ms for `tier-1-static`) is **not** per-call service time. `orchestrator.py:811` computes `latency_ms = time.time() - workers[tid]["start_time"]`, and all workers are queued at t=0, so it measures **queue-to-completion sojourn time**. Proof: `tier-1-static` `max_latency_ms` = 2,060,384 ms = 2060 s versus a job elapsed of 2061 s. Sizing any timeout from this field would be wrong. All figures in this report are derived from `outputs ÷ elapsed`, which is interpretation-independent.

---

## (d) Gap table: planned job → status

17 planned jobs, in dispatch order.

| # | Planned job | Level | Suite | Status | Evidence |
|---|---|---|---|---|---|
| 1 | `tier-2-static` | -2 | 59 | **done** | `aggregate-results.json`, 93.2% (55/59), 3366 s |
| 2 | `tier-2-adhoc` | -2 | 146 | **timed-out** | rc=-1, `tier-2-adhoc.log` = "TIMEOUT after 60m"; 122/146 outputs orphaned, no aggregate |
| 3 | `tier-1-static` | -1 | 59 | **done** | `aggregate-results.json`, 96.6% (57/59), 2061 s |
| 4 | `tier-1-adhoc` | -1 | 146 | **running → will time out** | pid 94297, 93/146 at 2668 s; 932 s of budget left, ~125/146 reachable |
| 5 | `tier0-static` | 0 | 59 | **running → will complete** | pid 2574, 41/59 at 1363 s; projected 1961 s |
| 6 | `tier0-adhoc` | 0 | 146 | **running → will time out** | pid 3421, 40/146 at 1129 s; ~127/146 reachable |
| 7 | `tier1-static` | 1 | 59 | never-started | no `tests/tier1-static/` directory |
| 8 | `tier1-adhoc` | 1 | 146 | never-started | no directory |
| 9 | `tier2-static` | 2 | 59 | never-started | no directory |
| 10 | `tier2-adhoc` | 2 | 146 | never-started | no directory |
| 11 | `tier3-static` | 3 | 59 | never-started | no directory |
| 12 | `tier3-adhoc` | 3 | 146 | never-started | no directory |
| 13 | `tier4-static` | 4 | 59 | never-started | no directory |
| 14 | `tier4-adhoc` | 4 | 146 | never-started | no directory |
| 15 | `tier5-static` | 5 | 59 | never-started | no directory |
| 16 | `tier5-adhoc` | 5 | 146 | never-started | no directory |
| 17 | `control-static` | n/a | 59 | never-started | no directory |

**Summary: 2 done · 1 timed-out · 3 running · 11 never-started.**

`_run_one` calls `results_dir.mkdir()` as its first statement, so absence of a directory is positive proof the job was never dequeued by the thread pool.

---

## (e) Diagnosis: why jobs are timing out

### Root cause

`run_all_variations.py` line 53–54:

```python
r = subprocess.run(cmd, cwd=str(PROJECT), capture_output=True,
                    text=True, timeout=60 * 60)          # <-- hardcoded 3600 s
```

A single constant 3600 s budget is applied to every job regardless of suite size — but the adhoc suite is 146 cases while the static suite is 59.

### The arithmetic

Measured wall-clock throughput at `--max-workers 2`, from three independent adhoc jobs:

```
tier-2-adhoc   122 outputs / 3600 s = 29.5 s per test
tier-1-adhoc    93 outputs / 2668 s = 28.7 s per test
tier0-adhoc     40 outputs / 1129 s = 28.2 s per test
                                    -----------------
                              mean  = 28.8 s per test
```

Time required for a full 146-case adhoc job:

```
146 cases x 28.8 s = 4205 s = 70.1 minutes
Hard cap                     = 3600 s = 60.0 minutes
Overshoot                    =  605 s = 10.1 minutes  (16.8% over budget)
```

Cases completable before the kill:

```
3600 s / 28.8 s = 125 of 146   (86%)
tier-2-adhoc actually produced 122.   <- prediction matches observation
```

Implied per-test **service** time (what one worker actually spends):

```
28.8 s wall x 2 workers = 57.6 s per call
```

This matches the launching session's own "~60 s/call" estimate almost exactly. **The session's throughput model was correct.** Its single error was never comparing *per-job* wall time against the *per-job* 3600 s cap — it only reasoned about aggregate campaign time (~280 min).

### Consequences

1. **All 8 adhoc jobs will time out.** Every one is a 146-case suite at ~28.8 s/test = ~70 min > 60 min. That silently voids **8 of 17 matrix cells (47%)** — half the experiment produces no aggregate.
2. **~124 scored outputs are discarded per timed-out job.** `orchestrator.py` writes `aggregate-results.json` only after the whole scoring phase completes; `subprocess.run` kills it mid-flight. The 122 `tier-2-adhoc` outputs sit on disk unscored and invisible to `comparison.json`.
3. **Static jobs are also near the cliff.** `tier-2-static` finished in 3366 s — only **234 s (6.5%)** under the cap. Note the smallest prompt (level-2, 5113 bytes) was the *slowest* static job while level-1 (26206 bytes) took 2061 s, so latency here is dominated by free-endpoint queueing variance, not prompt size. That variance alone can push a static job over.
4. **Tiers 3/4/5 are at severe risk and have not started.** Prompt sizes step up sharply:

   | Level | system-prompt.txt | approx tokens |
   |---|---|---|
   | -2 | 5,113 B | ~1.2 K |
   | -1 | 26,206 B | ~5.9 K |
   | 0 | 17,731 B | ~4.3 K |
   | 1 | 59,502 B | ~14.5 K |
   | 2 | 77,450 B | ~18.5 K |
   | **3** | **398,221 B** | **~95 K** |
   | **4** | **474,023 B** | **~116 K** |
   | **5** | **552,382 B** | **~134 K** |

   Levels 3–5 carry 5–9× the input of level 2. Those 6 jobs face both far slower calls and possible context-window failures. At current pace the run is 78.8 min in with 11 of 17 jobs not yet dequeued; the campaign will run many more hours and the majority of its adhoc output will be thrown away.

### Recommended fix

**Fix 1 — make the per-job timeout proportional to suite size (smallest change, unblocks immediately).**
Replace the constant at `run_all_variations.py:54` with a computed budget and expose it as a CLI flag:

```python
ap.add_argument("--job-timeout", type=int, default=0,
                help="per-job seconds; 0 = auto-size from case count")
...
budget = args.job_timeout or max(3600, int(n_cases * 60 * 2 / args.max_workers * 1.5))
r = subprocess.run(cmd, ..., timeout=budget)
```

For 146 cases at 2 workers this yields ~6570 s (109 min), giving ~56% headroom over the measured 4205 s.

**Fix 2 — raise worker fan-out.** Minimum workers for a 146-case job to fit in 3600 s:

```
ceil(146 x 57.6 / 3600) = ceil(2.34) = 3 workers
```

Use `--max-workers 4` for ~35 min per adhoc job with comfortable headroom. Keep `--max-orchestrators 3`, giving 12 concurrent calls — watch for 429s on the free tier and back off to 3 workers if they appear.

**Fix 3 — stop discarding completed work.** On `subprocess.TimeoutExpired`, send `SIGTERM` instead of `SIGKILL` and have `orchestrator.py` trap it to run the scoring phase over whatever `*-output.txt` files exist, emitting a partial aggregate flagged `"partial": true`. This alone would have salvaged 122/146 `tier-2-adhoc` results.

**Fix 4 — restore static/adhoc symmetry.** `generate_adhoc_tests.py` emits 146 cases against a 59-case static suite, so the two arms are not directly comparable *and* the larger arm is the one that breaks. Add `--limit 59`.

**Fix 5 — never restart blindly.** `tier-1-static` (96.6%) and `tier-2-static` (93.2%) are complete and valid. Any rerun must skip jobs whose `aggregate-results.json` already exists, or ~90 minutes of good results are lost.

**Suggested relaunch, after applying fixes 1–3 (do not run until the current process is intentionally stopped):**

```bash
python3 .agents/benchmark/run_all_variations.py \
  --model tencent/hy3:free \
  --max-orchestrators 3 --max-workers 4 \
  --timeout 600 --job-timeout 7200 --seed 7
```
