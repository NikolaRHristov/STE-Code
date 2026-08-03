---
name: agent-session-triage
description: Triage a looping agent session; kill stale ones safely.
category: ste-code-dev
---

# Agent Session Triage

Diagnose a stuck, looping, or misconfigured agent session, and safely clean up a
fleet of stale sessions — **without killing yourself or the user's live
session.**

## When to use

- A session (yours or a child's) is stuck in a repeating loop: re-reading the
  same source file, re-running the same probe, re-deriving the same wrong
  conclusion.
- A session reports it "cannot locate", "cannot write to", or "lost" a project
  root / repo / working directory.
- Two or more sessions fail **identically** — a strong signal the cause is
  environment, not code.
- You are asked to kill, restart, or hand off stale sessions.

## Rule 0 — the session's own diagnosis is a hypothesis, not evidence

A looping session states its theory with total confidence ("`X()` returns `None`
because my cwd is wrong"). That confidence is generated, not measured. **Verify
the premise before investigating it.** In the case that produced this skill the
premise was false, and every subsequent step — hunting config files, searching
for stale installed copies — was wasted effort chasing a bug that did not exist.

Corollary: a function that "fails to resolve" may be returning a **wrong value**
rather than `None`. Print the actual value. A silent wrong answer produces no
exception, which is exactly why the session theorises instead of reading a stack
trace.

## Triage order — environment BEFORE source

Cheapest and highest-yield first. Most "code bugs" die at step 1.

1. **Read the process environment.**

   ```bash
   ps eww -p <pid>          # env is appended to the command column
   ```

   Look for the vars that select config/profile/policy (for Hermes:
   `HERMES_HOME`, `HERMES_PROFILE`, `STE_CODE_JAIL_POLICY`, `PWD`). A session
   pointed at the _wrong profile_ behaves exactly like a session hitting a _code
   bug_, and is far more common.

2. **Compare process start time against file mtime.**

   ```bash
   ps -Ao pid,lstart,command | grep <proc>
   stat -f "%Sm %N" -t "%Y-%m-%d %H:%M:%S" <edited-file>   # macOS
   ```

   A process started **before** your edit holds the old module in memory. Config
   loaders commonly memoise into a module global at first call, and plugins
   import once at registration — so re-reading the file changes nothing for a
   live process. No amount of in-session verification will show your fix.

3. **Check for leaked env across runs.** An env var that overrides a config map
   persists in a shell after the run that set it. Grep the log for the
   contradiction (e.g. a dev profile registering a bench policy):

   ```bash
   grep "profile=<expected> policy=<unexpected>" <logs>/agent.log
   ```

4. **Only now read the source** — and read the _whole_ expression (see below).

5. **Re-verify in a FRESH subprocess.** Never in-session; see step 2.

## Reading a multi-line fallback chain

A very common misread. Given:

```python
value = (
    cfg.get("thing")
    or new_resolver()        # <- runs FIRST
    or old_resolver(cwd)     # <- fallback only
)
```

A session skimming for a symbol finds `old_resolver(cwd)` on the last line and
concludes it is the live path. **Read the entire parenthesised expression before
deciding which branch is authoritative.** If you are about to report "the code
still calls the old function", check whether it calls it _first_ or _last_.

## A passing sibling process proves nothing

"The other worker resolves it fine" is not a control unless it uses the same
code path. A launcher that `cd`s into the right directory first, or that uses a
separate shell implementation of the same logic, is **structurally immune** to
the bug and its success carries no information about the failing path. Confirm
both paths before treating one as a control.

## Killing a session fleet safely

The genuine hazard: your own reporting path is in the process list.

1. **Compute your own ancestry live and exclude it.** Walk `getppid()` up to PID
   1 and add every hop to a keep-set. Do not hardcode it — a helper subprocess
   spawned mid-task gets a fresh PID that a static list will miss.
2. **Identify the supervisor.** A dashboard/gateway process is often the _parent
   of every UI session_, including yours. Killing it takes you down mid-report.
   Keep it unless explicitly told otherwise.
3. **Distinguish daemons from sessions.** Long-lived gateway/service processes
   deliver messaging and are not "sessions"; killing them silently breaks
   delivery. Keep them unless asked.
4. **Identify the process to PRESERVE explicitly.** When the user says "I
   launched a new session to take over", find it and confirm it by env (distinct
   config home, expected cwd) _before_ killing anything near it.
5. **SIGTERM → wait → verify → SIGKILL → re-verify.**
6. **Re-check apparent SIGKILL survivors after a few seconds.** Processes
   mid-teardown still appear in `ps`. Recheck before escalating or reporting
   failure — in practice they are simply gone.

Print a **WILL KILL / PRESERVED** table and reconcile it before pulling the
trigger.

## Handing off

When the user replaces a looping session, leave a written handoff the successor
can read, and **state the corrected diagnosis prominently** — otherwise the new
session re-derives the same wrong theory from the same source file. Include: the
false premise and why it is false, the real cause(s), the triage order, and a
re-runnable probe. Check whether the destination directory is gitignored and
tell the user (on-disk-only is usually correct for triage notes; it keeps the
tree clean).

## Pitfalls

- Do **not** conclude "stale installed copy" without running a filesystem-wide
  search for duplicates. Plugin loaders that resolve by marker and follow
  symlinks bind the source file, not a copy.
- `ps -o pid=,ppid=` can trip argument-inspecting security hooks that read `-o`
  values as write paths. Use `ps aux` / `ps -Ao pid,ppid,command` and parse, or
  do it in Python.
- Chained shell commands (`cd X && y; z`) may be rewritten by scrubbing hooks
  into a broken single line. Prefer one command per call with an explicit
  working directory.
- Report a corrected diagnosis **as a correction**, explicitly. If your first
  report emphasised the wrong cause, say so plainly rather than quietly
  reordering the causes in the final summary.

## Related

- `ste-code-jail-ops` — jail policy internals, confinement layers, and the
  profile/policy map that step 1 inspects. See its
  `references/project-root-resolution.md` for the worked STE-Code case.
