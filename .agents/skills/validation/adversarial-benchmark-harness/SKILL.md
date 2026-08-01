---
name: adversarial-benchmark-harness
description: "Build RED/BLUE/PURPLE/WHITE/BLACK benchmark harnesses."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [benchmark, adversarial, red-team, blue-team, harness, anonymization, delegation, fan-out, verification, split-half, notes-protocol, selftest]
---

# Adversarial benchmark harness — design, build, verify

**Load this when** you are asked to build or extend a benchmark where independent
"colours" attack, defend, stitch, heal, or verify a configuration under test — or
when a user asks for RED / BLUE / PURPLE / WHITE / BLACK sides, adversarial
test generation, or A/B verification of a benchmark's own conclusions.

**Companion skills**: `gated-batch-orchestration` owns *watching* a long run
already in flight (throughput forensics, gate-failure triage, commit
attribution). This skill owns *designing and building* the harness and the
parallel-delegation pattern used to build it. `benchmarking` owns the STE-Code
scoring backend (`orchestrator.py`) that a harness like this drives.

---

## 1. The colour model

| Colour | Attacks | Owns | Question it answers |
|---|---|---|---|
| RED | the configuration | `red.py`, `adversarial.py` | what gets through? |
| BLUE | RED's escapes | `blue.py` | does a fix hold when the payload moves? |
| PURPLE | nothing — pure reader | `purple_stitch.py` | what do the sides jointly say? |
| WHITE | the failure history | `white.py`, `knowledge.py` | what should change, and did it work? |
| BLACK | **the conclusion** | `black.py`, `verification.py` | would this result survive scrutiny? |

The distinction that makes the model worth building: **RED attacks the system,
BLACK attacks the claim.** Without BLACK, a harness happily reports a number that
was derived and validated on the same data. BLACK is where a benchmark stops
flattering itself.

Support layers, each a separate module: config (`harness_config.py` +
`config/harness.json`), redaction (`anonymize.py`), correspondence (`notes.py`),
throughput (`scheduler.py`, `runner_pool.py`), and one canonical test
(`selftest.py`).

---

## 2. Convergence: filesystem only, never IPC

Colours run as independent processes launched at different times, sometimes in
different sessions. They must **never** import each other, await each other's
return values, or share memory. They agree on one thing: a set of filenames.

```
<base>/variant<V>/round<N>/
    escapes.json        RED's ledger      (the evidence)
    purple.json         RED's sentinel    (the "I'm done" marker + summary)
    blue-done.json      BLUE's sentinel
    white-done.json     WHITE's sentinel
    black-done.json     BLACK's sentinel
<base>/notes/           correspondence (crosses rounds — NOT per round)
<base>/report.json      PURPLE's stitch
```

Rules that make this work:

- **Ledger + sentinel, not one file.** The ledger is the evidence; the sentinel
  says the evidence is complete. A reader that sees only a ledger knows the
  writer is still going.
- **Every wait is bounded** by `--await-timeout`. On timeout, record
  `status: await-timeout` and move on. A colour that blocks forever takes the
  whole harness with it.
- **Readers tolerate absence.** PURPLE must produce a partial report from
  whatever exists — a missing BLUE is a `partial` cell, not a crash.
- **Atomic writes** (temp + rename). Other colours poll these paths live.
- Filenames live in config, never in code (see §3).

### Concurrency primitives that survive independent writers

Learned building `notes.py`, where five colours append to one directory:

- **Per-record files, not one shared file.** Each note is its own JSON file, so
  writers never contend on a single inode.
- **`O_EXCL` is the arbiter for id allocation.** Derive the next sequence from
  what is on disk, then `os.open(..., O_CREAT | O_EXCL)`. If it raises `EEXIST`
  another process won the race — take the next number and retry. This is what
  makes ids unique without a lock.
- **The index is a rebuildable cache, never the source of truth.** Read the
  record files themselves for queries; provide `rebuild_index()`. A writer
  killed mid-update must not corrupt the corpus.
- **Lock with `mkdir`, not a lock file.** Directory creation is atomic
  everywhere, and a stale directory can be detected by age and broken. Never
  block the pipeline on a lock — on timeout, skip the cache update and continue.
- Verify with **real concurrent processes** (`subprocess.Popen` × N), asserting
  zero lost records and zero duplicate ids. An assertion about thread-safety is
  not evidence.

---

## 3. Generic ≠ simple — the hardest constraint to hold

The recurring user directive on this class of work: *"make sure all scripts are
generic and generalized enough, **not simple**, but anonymized."*

Externalize every **noun**; keep every **algorithm** deep. Swapping the profile
document must retarget the harness at a different corpus with **zero code
edits**.

Into `config/harness.json`: project/standard/product name, path layout, variant
scheme, prompt template paths, word banks, technique/placement/timing lists,
handshake filenames, scoring constants, rule prefix, model identifiers, poll and
timeout defaults, partition strategies, verdict names.

Stays in code: the scheduling algorithm, the statistics, the matrix
construction, the detection heuristics.

**Verification trick that actually catches drift** — assert the config object
mirrors the document key-for-key, so a filename added to code but not to the
document fails the test:

```python
hs = {k: v for k, v in doc["handshake"].items() if not k.startswith("$")}
check(all(getattr(cfg.handshake, k) == v for k, v in hs.items()),
      "handshake mirrors the profile document key-for-key")
```

Write an audit tool (`audit_generic.py`) that greps for the violations rather
than trusting review — and make the audit itself generic by reading the strings
it searches for out of the config. Give it an inline pragma allowlist
(`# audit: allow <rule-id> <reason>`) so legitimate cases (the config layer is
*allowed* to know the layout) don't become permanent noise; report exemptions in
their own section so they stay visible.

---

## 4. Anonymization — redact on the way OUT

Benchmark output travels: into a repo, a PR, a paper, an issue. Three levels:

| Level | Removes | Use |
|---|---|---|
| `off` | nothing | local debugging only |
| `paths` (default) | username, hostname, home dir, absolute paths | everyday runs |
| `full` | `paths` + pseudonymizes profile id, variant labels, directory names | publication |

Design rules learned the hard way:

- **Deterministic pseudonyms, salted.** `blake2s(salt + value)[:4]` → `variant-a1b2`.
  Same salt ⇒ same alias, so two anonymized reports stay diffable and joinable.
  Change the salt ⇒ linkability breaks across publications. Not reversible
  without the salt.
- **Never touch the numbers.** Redaction changes how a result is reported, never
  what was measured. Test this explicitly: assert a count and a rate survive
  verbatim at every level.
- **`off` must be a true passthrough** (`report(x) is x`), so debugging sees
  exactly the raw document.
- **Reject an unknown level** with `ValueError` rather than silently degrading to
  no redaction — a typo'd level must never publish raw identity.
- **Machine-readable keeps raw, human-readable gets redacted.** An on-disk note
  or artifact keeps absolute paths so tools can resolve them; the *export* is
  what must be clean. Assert both halves.

### Pitfall: per-field redaction gated on the wrong level (real bug, caught by test)

A `coverage.missing` list of paths was redacted only inside the `if level ==
"full"` branch, so at the **default** `paths` level the report leaked
`/Users/<name>/...`. Filesystem identity must be redacted at **every active
level**; only *semantic* pseudonymization is `full`-only. When you add a field to
a report, ask which of the two buckets it is in — and add a leak-scan assertion,
not just a code review.

Always leak-scan the **output**, not only the source:

```bash
grep -ciE "<user>|<hostname>|/Users/|/Volumes/|$HOME" report.json report.md   # expect 0
```

---

## 5. Notes protocol — make silence visible

Independent processes still need to tell each other things. A note is a
**durable, addressed, evidence-bearing, acknowledged** message on disk — not
chatter.

Record: `id`, `from_colour`, `to_colour` (or `all`), `variant`, `round`, `kind`
(`claim|warning|request|acknowledgement|rebuttal|handoff`), `subject`, `body`,
`evidence{escape_ids, probe_ids, remedy_ids, artifact_paths}`, `confidence`,
`expects_ack`, `supersedes`, `created_at`.

- **Immutable.** A correction is a new note with `supersedes` set, never an edit.
- **Evidence enforcement.** `claim`/`warning`/`rebuttal` must carry ≥1 evidence
  item or the write is rejected; `handoff`/`request`/`acknowledgement` are
  exempt — they route work or answer an existing note rather than asserting a
  fact. Document the asymmetry.
- **Unacknowledged ≠ invisible.** Notes with `expects_ack` unanswered past N
  rounds surface as `stale_notes` in the stitch report.
- **Validate colour/kind against config** so code and config cannot drift apart.
- A rejection is a **rebuttal** and must carry counter-evidence; an acceptance is
  an **acknowledgement** carrying `action_taken`.
- Notes are free text written by agents plus artifact paths — a prime leak
  vector. The on-disk note keeps raw paths for machine use; the **export** goes
  through the anonymizer.

**Broadcast semantics bite the tests.** A note addressed to `all` with
`expects_ack` legitimately appears in *every* colour's unacked inbox. Assert
membership (`brief.id in unacked`), not list equality — see §7.

### The WHITE → BLACK handoff

WHITE holds the only cross-round, cross-variant model of *why* things fail —
which is exactly what an attacker would need to discredit the benchmark. So WHITE
writes that model down deliberately as an **attack brief**: falsifiable
hypotheses of the form *"if X were true, the reported result would be inflated by
roughly Y"*. BLACK's job is to test each one.

---

## 6. BLACK: split-half A/B verification

**Nothing may be concluded from the same data that produced it.** Arm A derives
(WHITE's remedies, BLUE's probes); arm B verifies, untouched until the claim is
fixed, then evaluated once.

Partition strategies, all deterministic given a seed — use a **stable hash of the
case id** (`hashlib`, *not* builtin `hash()`, which is salted per process, and
never `random.shuffle`), so the split reproduces without being stored:

| Strategy | Detects |
|---|---|
| `random_half` | ordinary sampling noise |
| `stratified_half` | confounding by cell composition |
| `technique_disjoint` | technique overfitting (a remedy that only fixes what it was shown) |
| `placement_disjoint` | placement overfitting |
| `temporal_half` | drift; remedies that only work on the round they came from |
| `variant_holdout` | whether a lesson transfers across configurations |

Verdicts: `confirmed` / `inflated` / `deflated` / `unsound` / `underpowered`,
assigned by an explicit documented decision table over (effect, A-vs-B gap,
power) — not ad-hoc `if`s scattered through the code. Enforce a minimum arm size;
an underpowered claim must **never** be presented as confirmed. Report the gap as
a number, and label anything measured on arm A alone `derivation-only`.

BLACK's own standing challenges, beyond WHITE's brief: scoring-artifact
sensitivity, selection bias (regions RED never generated), remedy overfit, cell
sparsity, and duplicate inflation (near-identical cases counted as independent
evidence).

---

## 7. Planted-signal fixtures — the acceptance test

A synthetic fixture must contain **signals you deliberately planted**, and the
test asserts the detector *found them and ranked them correctly*. Example: make
one technique escape in every placement and one placement defeat every technique,
then assert both rank first.

> **A fixture where everything comes back clean/confirmed means your detector is
> broken, not that your system is healthy.**

Plant one of each outcome the code can emit: a remedy that genuinely transfers
(`confirmed`), one that helps only on arm A (`inflated`, with a measured gap), a
cell too sparse to judge (`underpowered`), and a near-duplicate cluster.

Also assert **coverage bookkeeping** (complete vs partial cells) by leaving one
round deliberately incomplete — that exercises the tolerant-reader path §2
requires.

### Pitfall: a too-balanced fixture hides the overfit signal

When planting an overfit remedy in a split-half fixture, do **not** tie the
planted outcome to a *stratifying attribute* (e.g. `placement`). If each arm
contains the same mix of placements, every split reproduces the same aggregate
and the overfit never shows — the detector comes back `confirmed` and you
falsely conclude the system is healthy (see the §7 warning about clean fixtures).
Tie the planted outcome to **arm membership**: the derivation arm passes every
case, the verification arm passes **zero** (success is a function of which arm the
case landed in, not of any observable attribute). Then any split that separates
the arms surfaces a ~100-point gap → `inflated`. Verify the fixture by computing
the split you intend to assert on and confirming the gap is non-zero *before*
wiring the assertion.

### Pitfall: when the assertion and the code disagree, check which is wrong

Three times across this work a "failure" was a wrong assertion, not a bug: a
2-complete / 2-partial fixture asserted as 1/3; a subset relation asserted as
equality (2 variants, 1 timeline); and an unacked-inbox list asserted as exactly
one id when a broadcast correctly appears there too. Fix the assertion — but
never *weaken* a check to make it green. Re-derive the expected value from the
fixture by hand first, and prefer membership/subset assertions where the domain
genuinely allows extra members.

---

## 8. One canonical self-test, not throwaway probes

**Symptom that you need this**: you write a probe into scratch, run it, delete
it, and next turn you re-verify the same surface again. Deleting the probe also
deletes the evidence.

Promote it to `selftest.py` in the harness directory, committed:

```bash
python3 .agents/benchmark/selftest.py     # exit 0 = green
```

It should: assert config mirrors the document, exercise every redaction level
including leak scans, run the stitch against a planted-signal fixture, exercise
the notes protocol including a **real multi-process concurrency test**, and
`py_compile` **every** module in the directory — so modules being written
concurrently by other workers get compile-gated automatically as they land.

Use `tempfile.mkdtemp` + `shutil.rmtree` in a `finally` so fixtures never leak;
verify zero leftovers. Run it twice to prove idempotence. Add its invocation to
the worker brief as a gate: *no worker reports done until this exits 0*.

### Make it DISCOVERABLE, or it does not count as verified

A committed `selftest.py` is still invisible if nothing points at it. If the repo
has no `Makefile`, `pyproject.toml`, `pytest.ini`, `tests/`, or `AGENTS.md`,
there is **no canonical command**, and every session re-derives verification from
scratch. Check first:

```bash
for f in Makefile justfile pyproject.toml setup.cfg tox.ini pytest.ini \
         package.json AGENTS.md CLAUDE.md; do [ -e "$f" ] && echo "$f"; done
```

Fix the root cause with a small `Makefile` exposing `test` / `lint` / `audit` /
`check`, so `make check` is the one command.

**Scope `lint` to the files you actually hold to the standard.** A first
`make check` failed on ~65 line-length violations, ~56 of them pre-existing
legacy (`orchestrator*.py`, `purple.py`). Gating on those makes lint permanently
red, and a permanently-red gate is an ignored gate. List the clean modules in a
`CLEAN :=` variable, keep `compileall` across *everything*, and migrate legacy
opportunistically. Then **fix the violations in files you own** rather than
raising the limit — one of nine was a genuine DRY win (two identical
`defaultdict(lambda: {...})` literals collapsed into a shared `_tally()`).

---

## 9. Building it: parallel delegation with session starters

This class of harness is five modules that must not touch each other's files —
ideal for parallel subagents. The bottleneck is **model latency, not CPU**, so a
worker doing sequential turns wastes wall-clock time.

> **Delegation on this class of work fails silently.** On this exact project,
> four subagents across two batches all returned `status=completed` and wrote
> **zero files** — every module ended up built by the parent session. Read
> "Size the goal to the budget" and "Verify the batch on disk" below *before*
> dispatching a build fan-out.

**Raise the caps first** (defaults are conservative):

```bash
hermes config set delegation.max_concurrent_children 8   # from 3
hermes config set delegation.max_spawn_depth 3           # from 1 — lets workers delegate
hermes config set delegation.orchestrator_enabled true
hermes config set delegation.max_iterations 120          # from 50 — long builds
hermes config get delegation                             # verify
```

`max_spawn_depth: 1` is what silently prevents workers from fanning out further.
But raising it is **necessary, not sufficient**: the child also needs
`delegate_task` in its *toolset*. With `toolsets: [hermes-cli]` the children
could not delegate at all and burned turns discovering that
(`delegate_task is not exposed in this session's toolset`).

> **PITFALL — do NOT raise `max_concurrent_children` to 8 on this profile.**
> On the STE-Code free-tier endpoint, raising it 3 → 8 *caused* the HTTP 524
> (Cloudflare 120s read timeout) failures this skill warns about: every
> dispatched build batch returned `status=completed` with a 524 payload in the
> body and **wrote zero files**. The bottleneck is endpoint saturation, not the
> model. The working configuration here is **`max_concurrent_children=2`,
> `max_spawn_depth=1`** — small, serial fan-outs. If a batch 524s, do not
> re-raise the cap and re-dispatch (it 524s again); build the module directly in
> the parent session instead. notes.py, verification.py, black.py, red.py and
> blue.py were all built that way this session after two 524'd batches.

### Size the goal to the budget

Children exit with `exit_reason=max_iterations` when the goal is too big — they
spend the whole budget reading (`read_file` × 8, `search_files`, `execute_code`
probes) and never reach the first `write_file`. Antidote, stated verbatim in the
goal:

- **One file per child**, named absolutely: *"ONE FILE. Nothing else."*
- *"Read these two files only; do not explore the tree."*
- *"WRITE THE FILE EARLY, then refine. Do not spend more than 3 tool calls on
  reading before your first `write_file`."*
- **Quote the API inline** in the context block so the child never needs to open
  the config module.
- Paste the **real measured numbers** in, so the child doesn't rediscover them.
- If `delegate_task` isn't in the child's toolset: *"do the work yourself; do NOT
  use delegate_task."*
- Keep the dispatch short. ~4–6 KB of numbered requirements A–G reads as
  thorough and behaves as overhead: the child plans, re-plans, never writes.

**When in doubt, build it in the parent session.** A ~600-line concurrency-
critical module written directly (skeleton, then successive `patch` calls) passed
27/27 on its first probe — faster end-to-end than two failed delegation rounds.

### The WORKER_BRIEF.md pattern

A subagent knows nothing about your conversation. Rather than repeating context
in every goal, write **one brief on disk** and point every worker at it as its
session starter:

`.agents/benchmark/WORKER_BRIEF.md` — orientation (the colour table), the
non-negotiable rules (contract, genericity, anonymization, language version,
never block, verify with real execution, don't commit, scratch location),
**file ownership** (who owns what, "if you need a change in a file you don't own,
report it — do not edit it"), the delegation policy, orientation commands, and
the definition of done.

Then each dispatch carries: read these N files **in this order** → the state of
the problem with **real measured numbers** → explicit file ownership including
files that *don't exist yet* ("import defensively, they're being written right
now") → deliverable paths → an acceptance test that must fail on a broken
detector.

### Verify the batch on disk — never trust the summary

`status=completed` means the **loop ended**, not that the goal was met; the
summary field can contain an HTTP 5xx error payload sitting behind a `✓`.

```bash
ls -la <deliverable paths>                       # did the files land?
grep -nE "exit_reason|not exposed|Error|429|524" \
  ~/.hermes/profiles/<p>/cache/delegation/live/<id>/task-*.log
```

- `exit_reason=max_iterations` ⇒ the goal was too big; split it.
- `not exposed in this session's toolset` ⇒ toolset mismatch; fix the goal.
- `HTTP 5xx` ⇒ provider timeout; work may be partly done, so check disk first.

### Committing work (replaces the poll-commit worker)

**Do not run `.agents/tools/runners/poll-commit.sh`.** It auto-commits with junk
messages (`chore(benchmark): poll-commit N file(s)`) that the user has explicitly
rejected. Kill any running instance:

```bash
pkill -f poll-commit.sh
```

Commit with the intelligent tooling instead:

```bash
git gcommit-hermes        # Maintain/Save tool: writes a real, context-aware message
```

> **Caveat:** `git gcommit-hermes` calls a model backend (DeepSeek) that can be
> out of credits — observed `HTTP 402 Insufficient Balance`, aborting the commit.
> When it fails, **write an intelligent message yourself** (why + what, never the
> dumb auto format) and `git commit` directly. Do NOT fall back to poll-commit.

Scope every commit to session-owned paths — never `git add -A`; other sessions
own other directories.

---

## 10. Pitfalls index

- **`write_file` with a large body times out mid-stream.** Keep each tool call
  under ~8K tokens: write a skeleton with an `# __APPEND__` marker, then grow it
  with successive `patch` calls. Don't retry the same oversized call.
- **Assert the failure mode, not just the happy path.** Every detector needs a
  fixture where it *must* fire.
- **Redaction gated on the wrong level** — see §4.
- **`match` statements / `X | Y` at runtime** break on Python 3.9. Use
  `from __future__ import annotations` and quote annotations in dataclasses.
- **Config attribute guessing.** `cfg.variants` vs `cfg.all_variants()` cost a
  cycle; dump `[a for a in dir(cfg) if not a.startswith('_')]` once instead.
- **`write_file` refuses `/private/var/folders/...`** (sensitive-system-path
  guard). Put scratch probes under the repo's own scratch dir and let the
  *fixture* use `tempfile.mkdtemp`.
- **Don't interfere with a live run.** When orchestrators are mid-flight, build
  alongside them in scratch and never signal their pids.
- **Bare `ps` misses detached processes** — use `ps -axo` or explicit `-p`.
- **Don't re-declare args `add_common_arguments` already adds.** `harness_config.add_common_arguments(parser, config=...)` registers `--base, --profile, --rounds, --variants, --poll-interval, --skip-live, --model, --max-workers, --seed, --timeout`. Re-adding any of them makes argparse raise `ArgumentError: conflicting option string`. In `black.py` this surfaced as a launch-time crash; the fix was to delete the duplicate `parser.add_argument("--poll-interval" / "--rounds" / "--variants" / "--skip-live")` lines.
- **`cfg.scoring` is an object, not a dict.** `dict(cfg.scoring)` raises
  `TypeError: 'Scoring' object is not iterable`; use `dict(cfg.scoring.__dict__)`
  (or `vars(cfg.scoring)`). Hit in `black.py`'s scoring-artifact challenge.
- **Base-level vs per-round paths.** `cfg.attack_brief_path(base)` and
  `cfg.verdicts_path(base)` take **only** `base`; the attack brief is shared at
  the base, not per round. `cfg.black_sentinel_path(base, variant, round_n)` and
  `cfg.notes_index_path(base)` are likewise base-level. Per-round files live
  under `cfg.round_dir(base, variant, round_n)`. A wrong arg count is a runtime
  `TypeError`, not a syntax error — always check the signature before calling.
- **Schema vs runtime field requirements differ.** `schema.json`'s `TestCase.id`
  regex (`^bench-\d{3}$`) is NOT enforced by `orchestrator.py` at runtime; the
  runner merely passes `tc["id"]` through as `test_id`. But `category` IS
  restricted to the underscore enum (`api_doc`, not `api-doc`) and `expected_principles`
  needs `minItems: 1`. Keep generated cases schema-conformant (underscore
  categories) so a future schema-validation step won't reject them, but don't
  assume the orchestrator will crash on a non-`bench-` id.

---

## 11. User-preference notes for this class of work

Observed repeatedly on this profile — treat as defaults:

- **Terse.** Lead with the result. Don't re-summarize known state, don't re-poll
  the same status, don't narrate what you're about to do.
- **Never block.** `background=true` + poll. No foreground `sleep`/`wait`; keep
  the conversation moving and find other work while things run.
- **Anonymize by default**, both the report and the benchmark itself.
- **More workers.** When throughput is model-latency-bound the user wants the
  worker count raised, delegation used *inside* workers, and worker lifespan
  extended with richer starter context.
- **Prove it with real output.** Fresh tool output, not recollection; never
  fabricate a result you did not observe.
- Pipeline bookkeeping lives in `.agents/`, never in the shippable product dir.
- **Commit with `git gcommit-hermes`, not poll-commit.sh** (see §9). If it's
  out of credits, write the message yourself.
