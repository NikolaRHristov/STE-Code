# Child-session launch lockdown — spec & patch

**Problem (confirmed by reading the code, 2026-08-02):** every benchmark child
session is launched through `agent-runner.run_agent()` / `launch-worker.sh` →
`hermes-oneshot-wrapper.py`, which hands the child the **inherited environment**
(`env = {**os.environ, **env_vars}`) and never pins a profile, a jail policy, a
toolset, or a kernel sandbox. The wrapper hardcodes `HERMES_YOLO_MODE=true` +
`HERMES_ACCEPT_HOOKS=1` and uses the **full cli toolset**. A "profile-less"
child therefore inherits the spawner's profile (often `dev` = wide open) and has
**no jail, no env-strip, no redaction**. This is the exact hole that must be
closed: child sessions must be launched into a _severely strict limited jail_,
data-privatized, with **environment strips and kernel jails applied
programmatically before launch** — not just `hermes -z`.

## Design (implemented in `launch_confined_child.py`)

`launch_confined_child.launch()` is the single choke point. It guarantees, for
every child:

1. **Force-pin policy + profile.** Sets `STE_CODE_JAIL_POLICY=bench` and
   `HERMES_PROFILE=benchmark-ste-code` in the child env. Because the wrapper
   (`hermes-oneshot-wrapper.py`) does not pin a profile, the child would
   otherwise inherit the spawner's — this closes the `HERMES_HOME`/profile
   inheritance leak documented in `core/policy.py:profile_home`.
2. **Strip the environment.** Only `PATH/LANG/LC_*/TMPDIR` are forwarded; `HOME`
   is reset to `/tmp`; credential vars, `HERMES_HOME`, `SSH_*`, `AWS_*`,
   `STE_CODE_JAIL_POLICY`, and all `*TOKEN/SECRET/KEY` patterns are dropped.
3. **Kernel confinement (Layer 2).** The child command is wrapped in
   `jail-exec.sh` (Seatbelt on macOS, bwrap on Linux) so the agent's own
   subprocesses are confined to the bench write roots — the gap `jail-exec-wrap`
   was built to close.
4. **Minimal toolset.** Default `--toolsets terminal,file` (override per
   worker); the child cannot reach `memory`/`cronjob`/`delegate_task`/network.
5. **Harness context injection.** Embeds the `adversarial-benchmark-harness`
   contract + a `WORKER_BRIEF.md` pointer into the prompt, because children do
   not auto-load `benchmark-ste-code` skills (per the harness skill §9).
6. **Output leak-scan.** Captured stdout/stderr are run through the harness
   anonymizer / inline redaction before return, so raw `/Users/<name>` /
   hostname never leaves the child as reportable identity.

If `jail-exec.sh` is missing, `build_command` **refuses to launch** (fail
closed) rather than spawn an unconfined child.

## Patch: wire it into the existing call sites

### A. `agent-runner.py` (`run_agent` / `launch_agent`)

Replace the `subprocess.run` / `subprocess.Popen` invocations (currently lines
~204-214 and ~244-254) with:

```python
from launch_confined_child import launch as _launch_confined

def run_agent(prompt, agent=None, model=None, cwd=None, timeout=600, skill=None):
    ...
    if skill:
        try:
            from templater import lib_import
            _m = lib_import("skill_prompt")
            prompt = prompt + _m.skill_section(skill)
        except Exception:
            pass
    # BEFORE: result = subprocess.run(cmd, cwd=..., capture_output=True, ...)
    # AFTER:
    result = _launch_confined(
        prompt,
        model=(model or agent_cfg.get("default_model", "tencent/hy3:free")),
        label=f"agent-{os.getpid()}",
        timeout=timeout,
    )
    return result
```

`launch_agent` (async) should import and call `_launch_confined` via
`subprocess.Popen` with the same wrapped command; expose
`launch_confined_child.build_command(...)` + `build_child_env(...)` for that.

### B. `hermes-oneshot-wrapper.py`

Even though the wrapper is now always launched _through_ `jail-exec.sh` by the
parent, harden it defensively (it must never be invoked bare):

- At the top of `run()`, **assert**
  `os.environ.get("STE_CODE_JAIL_POLICY") == "bench"` (or the intended child
  policy); if unset, refuse to start. This makes a bare
  `hermes-oneshot-wrapper.py` (e.g. via `hermes -z`) fail closed instead of
  spawning an unconfined agent.
- Replace the hardcoded `os.environ["HERMES_YOLO_MODE"] = "true"` with honoring
  an env var the parent sets, and default to `false` when no policy is pinned.
- Accept a `--profile` arg and pass it to `AIAgent(profile=...)` so the child is
  explicitly confined even without the wrapper-level assertion.

### C. `launch-worker.sh`

Replace the `nohup "$PYTHON" "$AGENT_RUNNER"` call with a call that routes
through `launch_confined_child.launch`, or pass the stripped env + wrapped
command. Minimal change: invoke
`python3 .agents/benchmark/launch_confined_child.py "$PROMPT_FILE" --model "$MODEL" --label worker`
instead of `agent-runner.py` directly.

### D. `config.yaml` (benchmark-ste-code)

Add the new jail plugins from the parallel privacy work and ensure the child
profile is locked:

```yaml
plugins:
    enabled:
        - ste-code-jail
        - privacy-scrub # guard memory writes (other agent's work)
    disabled: []
    entries:
        ste-code-jail:
            allow_tool_override: false
        privacy-scrub:
            enabled: true
```

(Set `HERMES_OPERATOR_NAMES` at runtime, never in the tracked file.)

## Verification

1. `python3 .agents/hermes/jail/scripts/jail-exec.sh --check` → `ok`
   (policy=bench).
2. Launch a confined child that tries to write outside `.agents/benchmark/`:
   expect `jail-fs refused` / `PermissionError` (kernel layer).
3. Launch a confined child that tries `hermes -z` or `os.environ["HOME"]`:
   expect `HOME=/tmp` and the agent-spawn command denied.
4. Inspect captured output for `/Users/` / hostname — expect 0 matches
   (leak-scan). Mirror the harness assertion:
   `grep -ciE "/Users/|/Volumes/|$HOME" out.txt` → `0`.

## Status

- `launch_confined_child.py` — written under `.agents/benchmark/` (writable by
  the bench profile; the canonical launcher files are NOT, by jail design).
- Canonical edits to `agent-runner.py` / `hermes-oneshot-wrapper.py` /
  `launch-worker.sh` must be applied by the `dev-ste-code` profile (or
  out-of-band), because the bench jail denies writes outside
  `.agents/benchmark/` and the jail must never be rewired by the confined
  session.
- The working tree was DIRTY at authoring time (another agent committing), so no
  in-place edits were made.
