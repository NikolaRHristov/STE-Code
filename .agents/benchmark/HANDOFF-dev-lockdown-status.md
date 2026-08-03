# HANDOFF — child-launch lockdown: what to fix / verify (relay from dev-ste-code session)

Written by the `dev-ste-code` agent. Relay target: any session that can write
the canonical launcher files (the `benchmark-ste-code` profile's jail blocks
these, so only `dev-ste-code` or an out-of-band editor can apply them).

## VERIFIED STATUS (as of the dev-ste-code session that applied this)

The full child-launch lockdown from `HANDOFF-launch-lockdown.md` was applied AND
verified. The subsequent model refusal ("你好，我无法给到相关内容") + `/undo 1`
(undid 19 chat messages) only rewound the **chat history** — it did NOT revert
the on-disk files. The patches are present and were confirmed green:

- ✅ `.agents/tools/lib/hermes-oneshot-wrapper.py` EXISTS (the `_WRAPPER` target
  `launch_confined_child.py` referenced but the bench session never created).
- ✅ `.agents/benchmark/launch_confined_child.py` EXISTS (bench session's
  launcher).
- ✅ `orchestrator.py` — both launch sites (~L624 initial, ~L743 retry) patched
  to `build_command` + `build_child_env` + `execvpe`.
- ✅ `orchestrator-control.py` — both launch sites (~L206, ~L316) patched.
- ✅ `benchmark-ste-code/config.yaml` — `privacy-scrub` added to
  `plugins.enabled` and `entries.privacy-scrub.enabled: true`.
- ✅ `agent-runner.py` — opt-in `confined=` param present on
  `run_agent`/`launch_agent`.
- ✅ `launch-worker.sh` — `--confined` flag present.

Verification run at apply time: `python3 -B -m py_compile` on all 5 patched
`.py` → "all 5 compile OK"; `make jail` → "all policies passed (dev, user,
bench)"; `make check` → **180/180 checks passed** (was 179 before the wrapper
file existed).

**Conclusion: nothing to re-apply.** A fresh session only needs to re-confirm
with Step 6 and then commit granularly. The re-apply steps (1–5) below are kept
as a fallback in case a future edit or checkout reverts the tree — treat them as
recovery, not the primary path.

## Step 0 — re-confirm present state (read-only, safe)

Run these to confirm the patches are still on disk (they should be):

```
cd <repo>
git status --short
git log -3 --oneline
grep -rn 'os.execvp("hermes"' .agents/benchmark/orchestrator.py .agents/benchmark/orchestrator-control.py
test -f .agents/tools/lib/hermes-oneshot-wrapper.py && echo "wrapper EXISTS" || echo "wrapper MISSING"
grep -n 'privacy-scrub' .agents/hermes/profiles/benchmark-ste-code/config.yaml
```

- If the `grep os.execvp` finds lines → the patches WERE reverted (re-apply:
  Steps 1–5).
- If `hermes-oneshot-wrapper.py` is MISSING → re-create it (Step 2).
- If `privacy-scrub` is absent from the bench config → re-apply (Step 4).
- Otherwise: patches present → go straight to Step 6 (verify + commit).

## Step 1 — if patches were reverted, re-apply them

The four real child-launch sites are in `orchestrator.py` and
`orchestrator-control.py` (NOT `agent-runner.run_agent` — that is pipeline-only
and must stay opt-in, not blanket-confined). Each site currently looks like:

```python
os.execvp("hermes", ["hermes", "-z", full_prompt, "-m", args.model, "--yolo"])
os._exit(1)  # (sometimes with this comment, sometimes without)
```

Replace with (orchestrator uses `args.model`; control uses `MODEL`; both have a
`prompt_file` already written earlier in the same function):

```python
cmd = build_command(prompt_file, args.model, DEFAULT_TOOLSET) + ["--yolo"]
env = build_child_env(None)
os.execvpe(cmd[0], cmd, env)
os._exit(1)  # should not reach
```

And add the import near the top of each file (same directory → importable):

```python
from launch_confined_child import build_command, build_child_env, DEFAULT_TOOLSET
```

Sites: `orchestrator.py` ~L624 (initial) + ~L743 (retry);
`orchestrator-control.py` ~L206 (initial) + ~L316 (retry).

## Step 2 — create the missing wrapper (if absent)

`launch_confined_child.py` sets
`_WRAPPER = _AGENTS/"tools"/"lib"/"hermes-oneshot-wrapper.py"` and
`build_command` invokes it — but the file was never created by the bench session
(the hole in the original handoff). Create
`.agents/tools/lib/hermes-oneshot-wrapper.py` with this content:

```python
#!/usr/bin/env python3
"""Hardened Hermes oneshot wrapper — single entry point for confined child sessions.

Always invoked by launch_confined_child.build_command(), which has already
pinned STE_CODE_JAIL_POLICY + HERMES_PROFILE, stripped the environment, reset
HOME=/tmp, and wrapped the command in jail-exec.sh (Layer-2 kernel confinement).
Fails closed: refuses if policy unset or HOME not isolated; never hardcodes yolo.
"""
import argparse, os, subprocess, sys

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt_file")
    ap.add_argument("--model", default=os.environ.get("HERMES_MODEL", "tencent/hy3:free"))
    ap.add_argument("--toolsets", default="terminal,file")
    ap.add_argument("--profile", default=os.environ.get("HERMES_PROFILE"))
    ap.add_argument("--yolo", action="store_true")
    args = ap.parse_args()

    if not os.environ.get("STE_CODE_JAIL_POLICY"):
        sys.stderr.write("hermes-oneshot-wrapper: refusing — STE_CODE_JAIL_POLICY unset\n")
        return 1
    home = os.environ.get("HOME", "")
    if home.startswith(("/Users/", "/Volumes/", "/home/", "C:\\")):
        sys.stderr.write(f"hermes-oneshot-wrapper: refusing — HOME not isolated ({home})\n")
        return 1
    yolo = args.yolo or os.environ.get("HERMES_YOLO_MODE", "").lower() in ("1","true","yes")
    try:
        prompt = open(args.prompt_file, encoding="utf-8").read()
    except OSError as exc:
        sys.stderr.write(f"hermes-oneshot-wrapper: cannot read prompt: {exc}\n")
        return 1
    cmd = ["hermes", "-z", prompt, "-m", args.model, "--toolsets", args.toolsets]
    if args.profile:
        cmd += ["--profile", args.profile]
    if yolo:
        cmd.append("--yolo")
    return subprocess.run(cmd, env=os.environ).returncode

if __name__ == "__main__":
    sys.exit(main())
```

## Step 3 — opt-in confinement in the pipeline runner (secondary, dev-only)

In `.agents/tools/lib/agent-runner.py`, add a `confined: bool = False` parameter
to `run_agent` and `launch_agent`; when `True`, route through
`launch_confined_child.launch(prompt, model=..., label=..., timeout=...)`. This
keeps default pipeline behavior unchanged (dev workers stay dev) and only
confines callers that opt in. NOTE: `agent-runner.py` was CRLF — if re-editing,
preserve CRLF or convert via the prettier `.gitattributes` (it forces
`*.py eol=lf`).

## Step 4 — enable privacy-scrub in the bench profile config

In `.agents/hermes/profiles/benchmark-ste-code/config.yaml`, ensure:

```yaml
plugins:
    enabled:
        - ste-code-jail
        - privacy-scrub
    disabled: []
    entries:
        ste-code-jail:
            allow_tool_override: false
        privacy-scrub:
            enabled: true
```

## Step 5 — launch-worker.sh `--confined` flag (optional, already drafted)

`.agents/tools/shared/launch-worker.sh` gained a `--confined` flag that routes
through `launch_confined_child.py` instead of `agent-runner.py`. Re-apply if
reverted. Default (no flag) is unchanged.

## Step 6 — VERIFY (the real gate)

Run from the dev profile (bench profile cannot run `make test`/`make lint` — the
jail blocks `compileall`'s `.pyc` cache write; that is environmental, not a
defect). Use `-B` to avoid the cache pitfall:

```
cd <repo>
python3 -B -c "import py_compile; [py_compile.compile(f, doraise=True) for f in ['.agents/benchmark/orchestrator.py','.agents/benchmark/orchestrator-control.py','.agents/tools/lib/agent-runner.py','.agents/tools/lib/hermes-oneshot-wrapper.py','.agents/benchmark/launch_confined_child.py']]; print('all 5 compile OK')"
make jail            # expect: RESULT: all policies passed (dev, user, bench)
make check           # expect: 180/180 checks passed
```

Confinement spot-checks (per original handoff):

1. `bash .agents/hermes/jail/scripts/jail-exec.sh --check` → `ok`
   (policy=bench).
2. Confined child writing outside `.agents/benchmark/` → kernel
   `jail-fs refused`.
3. Child `os.environ["HOME"]` → `/tmp`.
4. Captured child output `grep -ciE "/Users/|/Volumes/|$HOME"` → `0`.

## Known caveats (carried from the bench session)

- `privacy-scrub-sanitize/_common.py` calls `hermes -p <profile> -z` for Tier-1
  classify; the env-strip sets `HOME=/tmp` and drops `HERMES_HOME`, so that
  subprocess may fail to locate the profile. It is wrapped in try/except →
  returns `None` (safe degrade). Forward `HERMES_HOME` for that one subprocess
  only if you want Tier-1 LLM classify on confined children.
- The Pyright "str not assignable to Path" diagnostics on `build_command` are
  false positives — the function does `str(prompt_file)` internally, so a path
  string is accepted at runtime.
- `make check` rose from 179 → 180 after the wrapper was added (the new file is
  picked up by the jail/skill scan); 180/180 is the expected post-patch count.

## Bottom line for whoever applies this

If Step 0 shows the patches are gone, re-apply Steps 1–5 in order, then run
Step 6. If Step 0 shows the patches are present, just run Step 6 to confirm,
then commit granularly. Do NOT commit the other agent's unrelated skill edits or
untracked skill dirs.
