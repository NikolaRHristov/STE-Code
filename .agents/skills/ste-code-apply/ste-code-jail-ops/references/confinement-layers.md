# Confinement layers — proven facts & reproduction recipes

Verified empirically during the jail rework (2026-08-02), not from docs.

## Layer 2: opaque subprocess escape (the gap that was open)
Symptom: under `bench`, a bare
`python3 -c "open('<repo>/.agents/tmp/CANARY','w')"` **succeeded** — `jail-fs`
only inspects the `command` string, so `python3 build.py` is invisible.
Fix: `jail-exec-wrap` rewrites `terminal`/`execute_code` calls to run under
`scripts/jail-exec.sh` (Seatbelt on macOS, bubblewrap on Linux) using the same
policy roots.

Repro that proves the fix:
```python
import importlib.util, sys, os
JAIL="<repo>/.agents/hermes/jail"; sys.path.insert(0,JAIL)
os.environ.update(STE_CODE_JAIL_POLICY="bench",
                  HERMES_HOME="~/.hermes/profiles/benchmark-ste-code",
                  HERMES_PROFILE="benchmark-ste-code")
spec=importlib.util.spec_from_file_location("wrap", f"{JAIL}/plugins/jail-exec-wrap/__init__.py")
wrap=importlib.util.module_from_spec(spec); spec.loader.exec_module(wrap)
args={"command":'python3 -c "open(\'<repo>/.agents/tmp/CANARY\',\'w\')"'}
wrap._on_pre_tool_call(tool_name="terminal", args=args)
# run args["command"] via subprocess: now PermissionError (kernel-enforced)
```

## The `pre_tool_call` arg-mutation trick (how auto-wrap works)
`agent/tool_executor.py` builds `final_args` and passes that SAME dict object
both to `pre_tool_call` hooks and to the executor. Mutating `args` in place
changes what runs. Proven with:
```python
# hook:
def _on_pre_tool_call(tool_name="", args=None, **_):
    if tool_name=="terminal": args["command"]="WRAPPED::"+args["command"]
# executor-side print after dispatch:
print("final_args now:", args)  # -> {'command': 'WRAPPED::echo hello'}
# MUTATION PROPAGATES: True
```
This is the ONLY reliable way to enforce at layer 2 — there is no
"rewrite-and-return" hook API. Do not block-and-return when the goal is to
confine, only when refusing outright.

## Layer 5: child agent escape (the `hermes` binary)
Denying `delegate_task` is not enough — `hermes -z '...'` starts a fresh agent
that re-reads config; nothing inherits the policy. Deny the binary AND every
scheduler/GUI driver in `AGENT_SPAWN_COMMANDS` (hermes, claude, codex, osascript,
launchctl, cron, at, sudo, su, open, …). For `benchmark-ste-code` which MUST
spawn, instead force-confine: `jail-exec-wrap` sets `STE_CODE_JAIL_POLICY=bench`
+ `HERMES_PROFILE=benchmark-ste-code` on the child's `terminal` call.

## HERMES_HOME inheritance leak
`hermes_home()` trusts `$HERMES_HOME`. A bench run launched from a dev shell
resolved its writable profile dir to `dev-ste-code` (wrote into the WRONG
profile). Fix: `profile_home(profile)` derives the dir from the resolved
profile NAME, not the env var. The policy builder now calls it.

## Profile self-modification (control surface)
A locked session with write access to its own `config.yaml` can set
`plugins: {enabled: []}`, restart, and run unjailed. Deny the whole control
surface via `_profile_control_denies(home)`: config.yaml, jail.yaml, hooks/,
plugins/, skills/, memories/, cron/, auth.json, .env, hermes.db, commands/,
agents/. Telemetry (`logs/`) stays writable.

## Warm-restart blind spot
A session caches its policy at startup. After editing `core/policy.py`, an
in-session check uses STALE roots. Verify in a fresh subprocess
(`jail-install.sh --status`) or a new `hermes` invocation — never in-session.
