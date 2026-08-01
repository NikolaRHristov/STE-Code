# Worker Brief — adversarial benchmark harness

Read this file **first**. It is the session starter for every worker, nested or
top-level. It replaces the context a fresh subagent does not have.

## 0. Orientation

You are working inside a benchmark harness that measures how well a
*configuration under test* resists adversarial input. Four independent colours
converge on disk:

| Colour | Role | Owns |
|---|---|---|
| RED | attacker — generates adversarial cases, records escapes | `adversarial.py`, `red.py` |
| BLUE | defender — re-probes escapes, measures resistance | `blue.py` |
| PURPLE | stitch — merges all sides into one report | `purple_stitch.py` (legacy: `purple.py`) |
| WHITE | self-healing — learns, proposes remedies, validates them | `white.py`, `knowledge.py` |
| BLACK | verifier — attacks the *conclusion*, split-half A/B | `black.py`, `verification.py` |

Support modules: `harness_config.py` (all configuration), `anonymize.py` (report
redaction), `notes.py` (inter-colour correspondence), `scheduler.py` /
`runner_pool.py` (throughput), `config/harness.json` (the profile document —
every project noun).

The colours leave each other **notes**: durable, addressed, evidence-bearing
messages on disk that must be acknowledged. See `NOTES_PROTOCOL.md`. WHITE hands
BLACK an *attack brief* — the weakest links in the other three colours, stated
as falsifiable hypotheses — and BLACK tries to break the result with split-half
A/B verification. Nothing may be concluded from the same data that produced it.

## 1. Non-negotiable rules

1. **Read `CONTRACT.md` before writing code.** It defines genericity and the
   handshake. Violating it breaks the other three colours.
2. **No hardcoded nouns.** No project name, path layout, variant scheme, word
   bank, technique list, handshake filename, scoring constant, or rule prefix
   in code. All of it comes from `harness_config`. Swap the profile document and
   the harness must run against a different corpus with zero code edits.
3. **Generic ≠ simple.** Externalize the nouns; keep the algorithms deep.
4. **Anonymize outbound reports.** Anything written for human consumption goes
   through `anonymize.py`. Never emit a home directory, username, hostname, or
   absolute path into a report.
5. **Python 3.9.** No `match`, no runtime `X | Y`. Use
   `from __future__ import annotations`.
6. **Never block forever.** Every wait is bounded by `--await-timeout`; on
   timeout, record the status and move on.
7. **Verify with real execution.** A change is not done until you have run it
   and read the actual output. Never report a result you did not observe.
8. **Do not `git commit`.** A poll worker commits and pushes on a timer.
9. **Scratch goes in `paths.scratch`** (`.agents/tmp/`) and is deleted when you
   finish. Never write scratch into the results tree.

## 2. File ownership

Multiple workers run concurrently. Touch only the files your task names. If you
need a change in a file you do not own, report it — do not edit it. Concurrent
edits to the same file lose work.

## 3. Delegate and poll — you are expected to fan out

Nested delegation is enabled (`max_spawn_depth: 3`, `max_concurrent_children: 8`).
The bottleneck is model latency, not CPU: a single worker doing sequential LLM
turns wastes wall-clock time. So:

- **Split your task** into independent subtasks and dispatch them with
  `delegate_task` in one batch. Give each child the full context it needs — a
  child knows nothing about your conversation.
- **Point every child at this brief** (`.agents/benchmark/WORKER_BRIEF.md`) plus
  `CONTRACT.md` as its starter context.
- **Poll, do not block.** Launch long work with `terminal(background=true,
  notify_on_complete=true)` and keep working. Never sit in a foreground `sleep`
  or `wait`.
- **Keep a todo list** with the `todo` tool so a long session stays coherent.

Good split axes: one child per colour, per variant, per technique family, per
placement family, per timing strategy, or per verification concern
(functionality / genericity audit / anonymization audit / determinism audit).

## 4. Orientation commands

```bash
python3 .agents/benchmark/harness_config.py     # profile, variants, prompt paths
python3 .agents/benchmark/anonymize.py          # redaction levels demo
python3 .agents/benchmark/purple_stitch.py --help
```

## 5. Definition of done

- Real command output pasted into your report, not a description of it.
- `--skip-live` self-test executed against a synthetic fixture, fixture deleted.
- No hardcoded nouns (grep your own file for the project name and for absolute
  paths before reporting).
- Reports pass a leak scan: no username, hostname, or home directory.
