# Worker Brief

## Purpose

This is the session starter for every worker in the adversarial benchmark harness, nested or
top-level. It supplies the context a fresh subagent does not have. Read it first, then read
`CONTRACT.md` before writing code.

## Footprint

| Kind | Value |
|---|---|
| Inputs | `CONTRACT.md`, `NOTES_PROTOCOL.md`, `config/harness.json` |
| Inputs | the variant prompt named by `paths.variant_prompt_template` |
| Outputs | round directories under `paths.results_base` (`.agents/benchmark/tests`) |
| Scratch | `paths.scratch` (`.agents/tmp`), deleted when the task finishes |
| Agent | `runner.default_model` and the `agent:` block of `../config/defaults.yaml` |

## Usage

    python3 .agents/benchmark/selftest.py           # canonical green check, run before reporting
    python3 .agents/benchmark/harness_config.py     # profile, variants, prompt paths
    python3 .agents/benchmark/anonymize.py          # redaction levels demo
    python3 .agents/benchmark/purple_stitch.py --help

`selftest.py` proves the shared layers (config, redaction, stitch) still hold and compiles every
module in the directory, including a new one. It must exit 0 before a task is reported complete.
A new colour module adds its planted-signal test to `selftest.py` rather than leaving a throwaway
probe behind.

## Behaviour

- Five colours converge on disk; none supervises another.
- Each colour writes its payload, then its sentinel, into the round directory.
- Colours leave each other notes: durable, addressed, evidence-bearing messages that must be
  acknowledged.
- WHITE hands BLACK an attack brief; BLACK tries to break the result with split-half A/B
  verification.
- Nothing is concluded from the same data that produced it.
- Reports for human consumption pass through `anonymize.py` before they leave the repository.

| Colour | Role | Owns |
|---|---|---|
| RED | attacker — generates adversarial cases, records escapes | `adversarial.py`, `red.py` |
| BLUE | defender — re-probes escapes, measures resistance | `blue.py` |
| PURPLE | stitch — merges all sides into one report | `purple_stitch.py`, `purple.py` |
| WHITE | self-healing — learns, proposes remedies, validates them | `white.py`, `knowledge.py` |
| BLACK | verifier — attacks the conclusion, split-half A/B | `black.py`, `verification.py` |

Support modules: `harness_config.py` (all configuration), `anonymize.py` (report redaction),
`notes.py` (correspondence), `scheduler.py` and `capsule_scheduler.py` (throughput and sequencing),
`generate_adhoc_tests.py` (case generation), `summarize_run.py` (analysis),
`config/harness.json` (the profile document — every project noun).

## Configuration

Every knob comes from configuration. Nothing is hardcoded in a module.

- `.agents/benchmark/config/harness.json` — profile, paths, variants, runner, handshake, notes,
  verification, scoring, vocabulary, techniques, placements, timings, defense, limits.
- `.agents/benchmark/config/sequence.yaml` — capsule sequence definitions.
- `.agents/config/defaults.yaml` — shared `agent.model`, `agent.timeout_s`,
  `agent.workers_per_batch`, `agent.retries`, `agent.backoff_s`, and the `runtime:` block
  (`retry_attempts`, `backoff_base_s`, `batch_divisor`, `encoding`).
- File writes go through `ste_io`; paths resolve through `ste_paths`; retry and pre-flight logic
  come from `ste_runtime`. Never open a file for writing directly and never inline an interpreter
  or wrapper path.

## Non-negotiable rules

1. Read `CONTRACT.md` before writing code. It defines genericity and the handshake, and violating
   it breaks the other colours.
2. No hardcoded nouns. No project name, path layout, variant scheme, word bank, technique list,
   handshake filename, scoring constant or rule prefix in code.
3. Generic is not simple. Externalize the nouns; keep the algorithms deep.
4. Anonymize outbound reports through `anonymize.py`. Never emit a home directory, username,
   hostname or absolute path into a report; write `<repo-root>` instead.
5. Target Python 3.9. No `match`, no runtime `X | Y`. Use `from __future__ import annotations`.
6. Never block forever. Every wait is bounded by `--await-timeout`; on timeout, record the status
   and move on.
7. Verify with real execution. A change is not done until it has run and its real output has been
   read.
8. Do not commit. Commits are the operator's decision, and a commit made from a worker session
   sweeps other sessions' in-flight edits into it. Report what is ready instead.
9. Scratch goes in `paths.scratch` (`.agents/tmp/`) and is deleted at the end. Never write scratch
   into the results tree.

## File ownership

Workers run concurrently. Touch only the files the task names. When a change is needed in a file
the task does not own, report it rather than edit it; concurrent edits to one file lose work.

## Delegate and poll

Nested delegation is enabled (`max_spawn_depth: 3`, `max_concurrent_children: 8`). The bottleneck
is model latency, not CPU.

- Split the task into independent subtasks and dispatch them in one batch. Each child needs full
  context, because it knows nothing about the parent conversation.
- Point every child at this brief and at `CONTRACT.md`.
- Poll, do not block. Launch long work in the background with completion notification and keep
  working. Never sit in a foreground sleep or wait.
- Keep a todo list so a long session stays coherent.

Good split axes: one child per colour, per variant, per technique family, per placement family,
per timing strategy, or per verification concern.

## Failure modes

- HTTP 429 from the free tier above roughly three concurrent workers. Lower the worker count and
  let `agent.retries` and `agent.backoff_s` absorb the rest; do not relaunch into the same limit.
- A missing sentinel stalls a consumer until `--await-timeout`, which records the status and
  continues.
- A concurrent edit to a file another worker owns loses one side of the work.
- A hardcoded noun passes the local run and fails the profile swap.
- A report that leaks an absolute path fails the leak scan and cannot be published.
- A task reported complete without a green `selftest.py` is not complete.

## Definition of done

- Real command output pasted into the report, not a description of it.
- The `--skip-live` self-test executed against a synthetic fixture, and the fixture deleted.
- No hardcoded nouns: grep the changed file for the project name and for absolute paths.
- Reports pass a leak scan: no username, hostname or home directory.
- `python3 .agents/benchmark/selftest.py` exits 0.

## See also

- `CONTRACT.md` — genericity rules and the handshake protocol
- `NOTES_PROTOCOL.md` — inter-colour correspondence and split-half verification
- `DEPENDENCIES.md` — external binary and Python requirements
- `docs/capsule-sequenced-pipeline.md` — capsule scheduling specification
- `tests/README.md` — where run output goes
- `../config/defaults.yaml` — shared agent defaults
