---
name: gated-batch-orchestration
description: "Monitor gated self-committing batch orchestrator runs."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [orchestration, monitoring, gates, retry, git, attribution, pipeline, workers, forensics, timeout, throughput]
---

# Gated Batch Orchestration — launch, watch, triage

**Load this when**: you are told to launch an existing batch orchestrator that
(a) runs one LLM worker per unit of work, (b) scores each unit against a
**deterministic gate**, (c) **commits on its own** when the gate passes, and
(d) you must report status without fixing anything.

**Also load this when**: a long batch/benchmark run is *already in flight* and you
must reconstruct what it intended and where it actually got to (see §5b–§5c).

STE-Code examples: `adapt_batch.py` (Phase D), `refine_batch.py`, the extraction
batch runners, `.agents/benchmark/orchestrator.py`,
`.agents/benchmark/run_all_variations.py`. The protocol below is runner-agnostic.

Companion skill: `pipeline-output-attribution` owns *output-vs-source* attribution
and the general watcher protocol (its §7 mtime rule and §9 read-only protocol are
prerequisites for this skill). This skill owns the **gated-retry + self-committing**
layer on top: retry-loop pathology, commit attribution, and failure-mode triage.

---

## 1. Observer role: report, do not repair

When the brief says *"do not edit repo tooling, only launch and monitor"*, that is
the whole job. Diagnose freely, but ship the diagnosis as **text in your report**,
never as an edit.

- Do not modify the runner, the prompt templates, or the gate.
- Do not `git commit` anything yourself. The orchestrator commits its own units.
- Do not "help" a failing section by hand-fixing its output — that destroys the
  evidence of *why* the gate failed and makes the next run unreproducible.
- Explicitly state in the report: **"Files created/modified by me: none."**

Diagnosing the root cause and *not* fixing it is a complete, successful outcome
under this brief. Say what you would fix and stop.

When the brief also says *do not kill or interfere with running processes*, prove
you complied: re-run `ps` at the end and show the same pids still alive, and show
an unchanged mtime on the runner source. Compliance you can demonstrate beats
compliance you assert.

---

## 2. Pre-launch baseline (do this BEFORE you start the runner)

A self-committing orchestrator will run `git` inside a tree you did not clean.
Capture the baseline or you will not be able to attribute anything afterwards:

```bash
git rev-parse --short HEAD          # anchor SHA -- diff against this later
git status --short                  # PRE-EXISTING dirty files
git status --short | wc -l
```

Record the anchor SHA in your report. Everything in `git log <anchor>..HEAD` at the
end is attributable to the run — and anything in there that is *not* a per-unit
commit is a red flag (see §5).

Also confirm the runner's preconditions so a launch failure is not mistaken for a
content failure: input directory exists and is non-trivial, checkpoint state, and
the per-attempt timeout / max-attempts constants in the runner source.

---

## 3. Launch and poll — never block

Launch in the background with completion notification:

```
terminal(background=true, notify_on_complete=true)
```

**`process(action='wait')` clamps its timeout** (observed: a requested 300s was
clamped to a 180s configured limit). Do not assume a long wait actually waited —
read the `timeout_note` in the response. Poll in repeated bounded waits instead of
one long one.

Confirm the worker chain is genuinely alive, not just the parent:

```bash
ps -ef | grep -E "adapt_batch|oneshot|worker-wrapper" | grep -v grep
```

You want to see **the parent AND a child worker**. A parent with no child and no
advancing log is a hung run, not a slow one. Note the child's argv — it usually
names the exact prompt file / unit in flight.

Report a **trend**, not a snapshot: which units passed, which failed, elapsed per
unit, and what is currently running.

---

## 4. Gate-failure triage: two modes that look identical in the log

This is the core technique. A gate failure message tells you *what* is wrong with
the file, never *whether the worker actually wrote it*. Two very different faults
produce the same-looking log line.

### 4a. The signature: byte-identical failure text across every attempt

```
SEC1: [GATE FAIL] a-sec1-rule1.5.md: non-approved synonym 'leverage' ... — retrying
SEC1: sleeping 15s before retry...
SEC1: [GATE FAIL] a-sec1-rule1.5.md: non-approved synonym 'leverage' ... — retrying   <-- identical
SEC1: sleeping 30s before retry...
SEC1: [GATE FAIL] a-sec1-rule1.5.md: non-approved synonym 'leverage' ... — retrying   <-- identical
SEC1: [GIVEUP] after 3 attempts
```

An LLM is stochastic. Three attempts producing **character-for-character identical**
gate output is near-impossible if the worker is really rewriting the file each time.
The overwhelmingly likely explanation: **the worker's output never landed on disk**,
and the gate is re-scoring the same stale pre-existing file every attempt.

### 4b. Confirm with mtime — always

```bash
ls -la <failing-files> <a-file-from-a-PASSING-unit>
```

Compare against the run's launch time and against a unit that passed:

| Observation | Mode | Meaning |
|---|---|---|
| mtime **older than launch** | **PLUMBING** | Worker wrote nothing. Gate scored a stale file. Retrying is futile — it will loop forever. |
| mtime **during the run**, still fails | **CONTENT** | Worker really did rewrite it and the output genuinely violates the gate. A prompt/model-compliance problem. |

Same log shape, two completely different fixes. Reporting them as one bucket
("5 sections failed") sends the next session chasing prompt wording for what is
actually a write-path bug.

### 4c. Consequence for `--resume`

Checkpoints typically record only **passed** units:

```json
{ "2": {"passed": true}, "3": {"passed": true}, "4": {"passed": true}, "7": {"passed": true} }
```

So `--resume` correctly retries the failures — but a **plumbing**-mode unit will
fail identically forever. Never recommend a blind resume until the write path for
those specific units is fixed. State this explicitly in the report.

---

## 5. Commit attribution: watch for stray sweeps

A self-committing orchestrator's worker may stage more than its own unit. Observed
live: an LLM worker produced a commit titled *"Refactor dictionary entries ... for
clarity and consistency"* that swept **11 pre-existing dirty files** from an earlier,
unrelated phase into itself — **+2,483 / −10,828 lines** — under an LLM-authored
message nobody reviewed.

At the end of every run, classify each commit:

```bash
git log --oneline <anchor>..HEAD
git show --stat --oneline <suspect-sha> | head -20
```

- **Expected**: per-unit commits matching the runner's own message format
  (`Adapt Section 07 - Safety Instructions - PASS`).
- **Stray**: anything else. Report it loudly with its SHA, its diffstat, and which
  files it touched — cross-referenced against your §2 pre-existing dirty list to
  prove they predate the run.

This is why §2 is non-negotiable. Without the baseline you cannot tell a stray sweep
from legitimate output, and unreviewed content silently becomes committed history.

---

## 5b. Inheriting a run you did not launch (no baseline available)

§2 assumes you start the run. Often you do not: the brief is *"a benchmark is
already running — reconstruct what it was supposed to do and where it actually
got to."* You have no anchor SHA and no pre-launch snapshot. Recover the intent
from **session history**, then verify every claim against **disk**.

**Step 1 — recover the launch from session history.** `session_search` finds the
session that started it. Query the runner's distinctive tokens, not generic words:
script name (`run_all_variations`), CLI flags (`orchestrator max-orchestrators`),
domain nouns (`adhoc test cases`). Then scroll with
`session_search(session_id=..., around_message_id=...)` to the launch message.

**Step 2 — corroborate, never trust.** A session says what it *intended*; disk says
what *happened*. Confirm the recovered command is byte-identical to the live
process argv from `ps`. If they differ, the session you found is a stale earlier
attempt — keep looking. Watch for relaunch chains: a run killed and restarted
several times leaves earlier proc handles in the transcript, and an exit code of
**143** (128+15 = SIGTERM) marks a killed attempt, not a completed one.

**Step 3 — reconstruct the schedule from timestamps.** With a concurrency cap, each
job's start time should coincide with a predecessor's completion. Line up `ps`
start times against per-job elapsed values; if every handoff matches, you have
proven the scheduler behaved as designed and your job inventory is complete.

**Never-started is provable, not inferred.** If the runner's per-job function calls
`results_dir.mkdir()` as its first statement, an absent directory is positive
evidence the job was never dequeued. Check the runner source for such a marker
before writing "never-started" — it upgrades a guess into evidence.

**The benchmark may be a side quest.** The session that launched a run is often not
"the benchmark session" — here a README-cleanup session authored the runner
mid-stream and launched it as a validation sweep. Do not discard a search hit
because its title looks unrelated.

---

## 5c. Throughput forensics: will this job finish before its timeout?

The highest-value question about a long run is usually not *"is it alive"* but
*"will it finish before something kills it."* You can answer that from two numbers
per job — outputs on disk and elapsed seconds — with no instrumentation.

```
wall_s_per_test    = elapsed_s / outputs_on_disk
projected_job_s    = wall_s_per_test * expected_cases
verdict            = projected_job_s vs the per-job timeout
cases_before_kill  = timeout_s / wall_s_per_test
```

**Validate the model against an already-killed job.** If one job has already timed
out, `cases_before_kill` must match the outputs it actually left on disk. Observed:
predicted 125 of 146, found 122. A model that retrodicts the corpse is a model you
can trust for the jobs still running.

**Derive service time from wall time**, don't measure it:
`service_s = wall_s_per_test * max_workers`. Cross-check against the launching
session's own per-call estimate; agreement means their throughput model was right
and the defect is elsewhere — usually a cap they never compared it against.

**Take the rate from several independent jobs.** Three jobs giving 29.5 / 28.7 /
28.2 s per test is a stable rate, not a fluke; a single job's number could be a
warm-up artifact.

### Pitfall: `avg_latency_ms` is usually sojourn time, not service time

Do not size timeouts from a runner's reported latency without reading how it is
computed. Observed in `orchestrator.py`:

```python
latency_ms = int((time.time() - workers[tid]["start_time"]) * 1000)
```

Every worker is queued at t=0, so this measures **queue-to-completion sojourn
time** — it grows with queue depth and has little to do with how long a call takes.
The tell: `max_latency_ms` ≈ total job elapsed (2,060,384 ms vs a 2061 s job).
Sizing a timeout from a 1,108,386 ms "average latency" would be wildly wrong.
`outputs ÷ elapsed` is interpretation-independent; prefer it always.

### The defect class: constant timeout, variable suite size

Watch for a hardcoded per-job budget applied to suites of different sizes:

```python
r = subprocess.run(cmd, ..., timeout=60 * 60)   # same 3600s for 59 and 146 cases
```

A 59-case suite fits; a 146-case suite at the same rate needs ~70 min and is
killed at 60. The failure is silent and total: the runner writes its aggregate only
after the *whole* scoring phase, so a mid-flight kill discards every completed
output. Symptom is `rc=-1` with outputs on disk but no `aggregate-results.json`.

Standard recommendations to give:

1. Size the timeout from case count and expose it as a flag
   (`max(3600, cases * service_s * 1.5 / workers)`).
2. Raise worker fan-out — `ceil(cases * service_s / timeout_s)` is the minimum
   that fits.
3. Trap SIGTERM so the runner scores whatever exists and emits a
   `"partial": true` aggregate instead of discarding it.
4. Keep suite arms the same size when they are meant to be compared.
5. **Never recommend a blind rerun** — skip jobs whose aggregate already exists,
   or valid completed results are destroyed.

Also flag jobs that *passed* but only just: finishing 234 s under a 3600 s cap
(6.5%) is not a pass, it is the next failure.

### Pitfall: mock-based verification cannot catch wall-clock defects

A run may be pre-verified green (observed: "11/11 passed" against a mock binary)
and still carry a fatal timeout bug. A zero-latency mock proves *wiring* — job
list, concurrency cap, output paths — and is structurally blind to *timing*. When
a verified-green runner fails in production, check timing assumptions first, and
say plainly that the mock could not have caught it.

### Pitfall: bare `ps` misses background processes

`ps -o pid=,etime=,command=` lists only terminal-attached processes, so a detached
orchestrator is invisible and every job looks dead. Symptom: your report says
`running: 0` and a null parent elapsed while the work is plainly advancing. Always
use `ps -axo` (or pass explicit `-p <pids>`) when enumerating background workers.

---

## 6. Final report shape

Report only what you **observed**. Never round a partial run up to success.

1. **Launch confirmation** — session/proc id, pid, anchor SHA.
2. **Per-unit table** — PASS / GATE-FAIL / GIVEUP, duration, commit SHA, and the
   specific gate reason for failures.
3. **The runner's own final line**, quoted verbatim (e.g. `Done. Adapted rule
   files: 54`) plus its **exit code**. A non-zero exit with a "Done." line is still
   a failure — say so.
4. **Independent verification** — run the repo's verify script and quote its
   PASS/FAIL summary and problem count. Do not substitute the runner's internal
   gate for the external verifier.
5. **Root-cause triage** per §4, bucketed into plumbing vs content.
6. **Commit attribution** per §5, including strays.
7. **State left behind** — checkpoint contents, dirty tree, untracked files, and an
   explicit "files created/modified by me: none."
8. **Recommendation** — usually "do not proceed to the next phase", with the precise
   blocker per bucket.

For a mid-run forensic report (§5b), add a **gap table**: every planned job mapped
to `done / running / timed-out / never-started`, each with its own evidence string.
Derive the planned job list from the runner source (its tier/variant loops), not
from what the session claimed it would do — the two can differ.

When asked for a machine-readable companion, emit counts and rates as real numbers
(`outputs_written`, `expected`, `pass_rate_pct`, `elapsed_s`) so the next agent can
diff progress without re-deriving anything.

### Pitfall: a truncated verifier list

Verifier output often prints only the first N of M problems (observed: 40 of 62
lines). Quote the **total count** from the summary, not the number of lines you can
see, and say the list was truncated.

### Pitfall: gate constants differ between runner and verifier

The in-run gate and the standalone verifier may exclude different context blocks
(one excluded `## Original Rule`, the other `Original Rule/Non-STE`). Expect their
counts to disagree slightly; report both rather than reconciling them silently.

---

## Appendix A — reference case: STE-Code Phase D, 2026-08-01

Runner: `.agents/tools/runners/phase-d-run.py` → execs
`.agents/tools/adaptation/adapt_batch.py` (venv python), `STE_MODEL=tencent/hy3:free`.
Constants read from source before launch: `TIMEOUT_SECONDS = 900` per attempt,
`max_attempts = 3`, backoff 15s → 30s → 45s, checkpoint at
`.agents/state/adapt-checkpoint.json` (untracked), per-section commit on gate pass.

Worker chain: `adapt_batch.py` (pid 24217) → `hermes-oneshot-wrapper.py` (pid 24221)
reading `.agents/tmp/adapt-sec1.txt`.

**Result: exit code 1, ~51 min, 4/9 PASS.** Final line: `Done. Adapted rule files: 54`

| SEC | Title | Result | Detail |
|---|---|---|---|
| 1 | Words | GIVEUP ×3 | `utilize`, `leverage`, `landing gear` |
| 2 | Multi-word Nouns | PASS 87.2s | `88ea3d7` |
| 3 | Verbs | PASS 353.0s | `2e05b6f` |
| 4 | Sentences | PASS 260.6s | `4945816` |
| 5 | Procedural Writing | GIVEUP ×3 | `utilize/leverage/employ`, `torque` |
| 6 | Descriptive Writing | GIVEUP ×3 | `leverage`, `commence` |
| 7 | Safety Instructions | PASS 246.2s | `693eb7b` |
| 8 | Punctuation | GIVEUP ×3 | `torque`, `cockpit` |
| 9 | Writing Practices | GIVEUP ×3 | `utilize`, `leverage` |

The mtime triage that split the failures:

```
sec1: newest Jul 30 22:27   <-- STALE (two days pre-run)  => PLUMBING
sec2: newest Aug 01 06:05   <-- fresh, PASSED
sec5: newest Aug 01 06:24   <-- fresh, FAILED             => CONTENT
sec6: newest Aug 01 06:33   <-- fresh, FAILED             => CONTENT
sec8: newest Aug 01 06:44   <-- fresh, FAILED             => CONTENT
sec9: newest Jul 30 20:56   <-- STALE (two days pre-run)  => PLUMBING
```

Stray commit `eeeee8f` swept 11 already-dirty `ste-code/grouped/dict-*` files
(leftover Phase C work) into an LLM-authored message. Only the §2 pre-launch
baseline made it identifiable.

Verifier (`--verify`): `Rule files: 54 (expected >= 54)`, `FAIL — 62 problem(s)`
(first 40 shown). Gate6 synonyms 19 hits (sec 1/5/6/9); Gate9 aerospace 5 hits;
Gate8 missing `Source: master.md#` backlink on all 14 sec1 files + sec5-rule5.1/5.2.

## Appendix A2 — reference case: benchmark tier matrix timeout, 2026-08-01

Runner: `.agents/benchmark/run_all_variations.py`, launched from session
`20260801_144007_52c08e` (a README-cleanup session) as
`--max-orchestrators 3 --max-workers 2 --timeout 600 --seed 7`, model
`tencent/hy3:free`. Plan: 8 tiers (level-2..level5) × {static 59, adhoc 146} +
1 control = **17 jobs**. Third launch attempt; the prior one exited **143**.

Investigated ~79 min in, read-only, while still running. State: **2 done ·
1 timed-out · 3 running · 11 never-started**; 414/1699 outputs (24.4%);
2/17 aggregates.

Root cause: `subprocess.run(..., timeout=60*60)` hardcoded at line 54, applied to
both a 59-case and a 146-case suite. Measured 28.8 s/test wall across three adhoc
jobs → 146 × 28.8 = **4205 s vs a 3600 s cap** (16.8% over). Predicted 125 cases
before the kill; the timed-out job left **122**. All 8 adhoc jobs were therefore
doomed — 47% of the matrix — and `tier-2-static` passed with only 6.5% headroom.

Two traps this case surfaced: `avg_latency_ms` was sojourn time (max 2,060,384 ms
≈ 2061 s job elapsed), and a bare `ps` initially reported `running: 0` because it
omits detached processes — fixed with `ps -axo`.

## Appendix B — known defect in the `adaptation` skill

Its Gate 1 says *"Count adapted rule files (must be 53)"*, but its own per-section
list sums to **54** (14+3+7+5+5+6+3+7+4) and `verify-adaptation.py` asserts `>= 54`.
Using 53 as a file-count gate under-counts by one and can mask a genuinely missing
file. The "53 rules" figure elsewhere in that skill counts spec rule *numbers*, not
files — the two must not be conflated. Reported, not patched (see Appendix C).

## Appendix C — authoring constraint on this profile

`skill_manage` `patch` and `write_file` return *"Skill not found in active profile"*
for **every** skill tried in this profile — including the repo-derived pipeline
skills (`adaptation`, `grouping`, `refinement`, `artifacts`, `auditing`,
`state-report`, which have no YAML frontmatter and list with `category: null`),
the curator-authored `pipeline-output-attribution`, **and even a skill created
seconds earlier in the same session**. So the frontmatter-mismatch theory recorded
in `pipeline-output-attribution` is incomplete: resolution for non-`create` actions
is broken profile-wide, likely due to the nested layout
(`profiles/ste-code/profiles/ste-code/`).

Consequences: only `action='create'` works, and it overwrites — so **updates must
re-issue the full body**, and support files under `references/` / `scripts/` cannot
be added at all. Keep everything inline in SKILL.md. A genuine protection error
reads "pinned" or "not curator-managed", not "not found" — do not mistake this
quirk for protection.

**Re-probed 2026-08-01** on this very skill (v1.1.0 → v1.2.0): `patch` failed with
"not found", and `write_file` to `references/` failed with the same error plus
"Create it first with action='create'". Still accurate. Re-probe rather than
assume — if a future probe succeeds, delete this appendix. Pass the original
`category` on re-create (here `validation`) or the skill moves directory.
