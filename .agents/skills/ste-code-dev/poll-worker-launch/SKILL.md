---
name: poll-worker-launch
description: Launch background poll workers for parallel jobs.
---

# Poll Worker Launch (STE-Code)

## When to use

- Launching **background/parallel Hermes work** where the job is large,
  API-fragile (sessions die at 429/Cloudflare 524), or needs an isolated,
  independently configurable runtime.
- User's STANDING DEFAULT: **prefer a poll worker over `delegate_task`** for
  these jobs, but **keep `delegate_task` for quick small sub-tasks** (it runs
  in-process with a narrower tool surface). Treat poll workers as the _delegate
  substitute_ for heavy work.
- A poll worker is a **background terminal process that launches a Hermes
  oneshot session FROM A PROMPT FILE** (not an inline CLI arg), with output
  captured to a file.

## The repo machinery (call chain)

`launch-worker.sh <prompt_file> [--agent hermes] [--model M] [out_file]` →
backgrounds:
`nohup python3 agent-runner.py <prompt_file> --model M > out_file 2>&1 &` →
`agent-runner.py` writes the prompt to a temp file and calls
`.agents/tools/lib/hermes-oneshot-wrapper.py <prompt_file> --model M` → wrapper
**reads the prompt from the file**, builds `AIAgent(session_db=None)`, and
writes the response to stdout (captured to `out_file`).

Key source pointers (verify if the repo drifts):

- `launch-worker.sh` - arg parsing, `nohup … &` backgrounding, output capture.
- `agent-runner.py` - `_resolve_command()` builds the Hermes wrapper invocation;
  `run_agent`/`launch_agent` manage the temp prompt file.
- `hermes-oneshot-wrapper.py` - line ~95 reads the prompt file; line ~127-128
  sets `HERMES_YOLO_MODE=true` + `HERMES_ACCEPT_HOOKS=1`; builds
  `AIAgent(session_db=None)`.

## Why poll workers beat delegate_task here

- HARDENING context: `delegate_task` strips `delegate_task`, `clarify`,
  `memory`, `send_message`, `cronjob` from the child and caps depth at 1 - a
  NARROW surface.

1. **Brief travels by file-reference, not the child system-prompt.** An inline
   `delegate_task` brief becomes the child's _system prompt_, incompressible and
   never reclaimed by auto-compression. A file-referenced brief lives in
   compressible conversation history. (ASCII ≈ 4 chars/token; the
   `tencent/hy3:free` child window is 262,144 tokens - a brief near that size
   risks a first-call failure inline but fits fine when read from a file.)
2. **Output is on disk → 429/524 death loses only the last chunk.** Mirrors the
   `delegation-verification` rule: write the deliverable EARLY and IN PARTS; the
   final chat message is a one-line DONE, not the payload. Treat the on-disk
   file, not completion status, as proof of work.
3. **Process + Hermes-session isolation, independently configurable.** Separate
   OS process, `session_db=None` (no parent-history pollution), and
   profile/toolsets/ cwd/env are constrainable "whichever way we want it."

## ⚠️ CRITICAL CORRECTION - stock wrapper is LESS confined than delegate_task

The current `hermes-oneshot-wrapper.py` **hardcodes `HERMES_YOLO_MODE=true` +
`HERMES_ACCEPT_HOOKS=1` and uses the FULL CLI toolset**
(`_get_platform_tools(cfg,"cli")`). So a default poll worker auto-approves every
dangerous command and has a _wider_ tool surface than a `delegate_task` child.

User directive: **"make more strict."** For the agent-as-delegate use case,
HARDEN:

- Launch with **minimal `--toolsets`** (or a confined profile) - do NOT inherit
  the full CLI set.
- Set **YOLO only when the task genuinely needs terminal/file writes**;
  otherwise keep approvals on or constrain the toolset so nothing dangerous is
  reachable.
- The STE-Code _pipeline_ workers may keep intentional YOLO via `agents.yaml`
  env - that is a separate, deliberate case, not the agent-substitute default.

## How to launch (patterns)

- Pipeline/file-driven:
  `bash .agents/tools/shared/launch-worker.sh prompt.txt --model tencent/hy3:free out.txt`
- Direct background:
  `nohup ~/.hermes/hermes-agent/venv/bin/python3 .agents/tools/lib/agent-runner.py prompt.txt --model M > out.txt 2>&1 &`
- Confined: add `--toolsets "terminal,file"` (or narrower) so the worker can't
  touch memory/cron/delegate/etc.

## Jailed poll-worker launch (STE-Code profiles) ⚠️

When the worker must run a STE-Code profile under the jail, the **kernel
confinement layer (`jail-exec.sh`) computes its Seatbelt/bwrap roots from
`HERMES_HOME`**. A common failure: the launcher `export`s `HERMES_HOME` _inside_
the launcher shell but does NOT prefix it on the `jail-exec.sh` command itself,
so `jail_init` runs with the _parent_ profile's home and the worker's
`logs/agent.log` write is denied (`Operation not permitted`).

**Correct recipe** (flags BEFORE `-z`; prompt last; `HERMES_HOME` prefix on the
jailed command, not only exported inside the launcher):

```bash
# 1) base64 the prompt (macOS needs -i) so it travels as one token-safe blob
base64 -i prompt.md -o prompt.b64
# 2) launcher reads it back via `base64 -d -i`
read -r PROMPT
PROMPT=$(base64 -d -i prompt.b64)

# 3) HERMES_HOME is PREFIXED on the jail-exec.sh invocation (not just exported)
HERMES_HOME=~/.hermes/profiles/ < target-profile > \
.agents/hermes/jail/scripts/jail-exec.sh \
	hermes -p M --yolo \
	-z "$PROMPT" < profile > -m
#                                   ^ prompt LAST - else `argument -z: expected
#                                     one argument`
```

Rules:

- **Flags before `-z`**, prompt as the final positional.
  `hermes -p X -m M -z "$PROMPT"` - never `hermes -z "$PROMPT" -p X` (parser
  errors).
- **Do not `cd` into the repo inside the launcher** - let `HERMES_HOME` +
  `jail-exec.sh` resolve roots from the profile dir.
- The **prompt carries NO textual confinement**; confinement comes from the
  profile's `config.yaml` (`plugins.enabled: [ste-code-jail]`) + the
  `jail-exec-wrap` force-confine on children.
- For `benchmark-ste-code` workers, `jail-exec-wrap` re-asserts
  `STE_CODE_JAIL_POLICY=bench` + `HERMES_PROFILE=benchmark-ste-code` on every
  child terminal call, so spawned adversarial sessions stay `bench`.
- Verify the worker actually confined: check its `logs/agent.log` first line
  reads `profile=<target> policy=<expected>`; a `policy=bench` under a dev
  launch means `HERMES_HOME` leaked from the parent shell (env -u HERMES_HOME
  before launch).

See `ste-code-jail-ops` (`references/profile-layout.md`,
`references/project-root-resolution.md`) for the profile single-source model and
the anchored project-root resolver.

## Verification pattern (parent side)

- **Poll the output file**, not the process status. A backgrounded session that
  exits 0 but wrote nothing, or dies mid-write, must be caught by reading
  `out.txt`.
- Re-run a "verification-only" pass: re-measure the worker's claims against disk
  evidence before trusting the summary.

## Pitfalls

- **Never pass a large brief inline to `delegate_task`.** Write it to `brief.md`
  and pass the path; inline briefs become an incompressible system-prompt tax.
- The wrapper **deletes the temp prompt file after reading** - keep the
  authoritative brief under version control (e.g. `.agents/tmp/` or the task
  dir), not only in the temp file, so a re-launch is reproducible.
- `hermes -z` (oneshot) itself sets `HERMES_YOLO_MODE=1` at
  `hermes_cli/oneshot.py` ~line 221 - the wrapper layer multiplies this.
  Confinement must be applied at the `--toolsets`/profile layer, not assumed
  from the subprocess boundary.

## References

- `references/worker-architecture.md` - full call-chain map, key file:line
  anchors, and the confinement comparison table (poll worker vs delegate_task
  tool surface).
