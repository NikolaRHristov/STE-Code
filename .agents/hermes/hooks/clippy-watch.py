#!/usr/bin/env python3
"""clippy-watch — profile-specific Hermes hook (dev-controlplane).

Runs after a file-edit tool call (write_file / patch). When the edited file is a
Rust source under the ControlPlane workspace, it runs `cargo clippy` on the
affected crate. If clippy reports warnings/errors, it AUTO-SPAWNS a background
`hermes -z` worker (no RFC) that fixes the issues and commits — without
interrupting the user's active session.

Profile gate: only active when HERMES_PROFILE == dev-controlplane. In any other
profile this hook is a no-op, so it never touches running user-controlplane
sessions.

Design notes:
- Fire-and-forget: this hook returns immediately. The clippy job and the fix
  worker both run in the background; nothing here blocks the session.
- The fix worker is a separate `hermes -z` process (isolated context), so it does
  not share the user's conversation and cannot interrupt it.
- We only ever spawn ONE fix worker per trigger to avoid worker storms; a lock
  file (`/tmp/clippy-watch.lock`) serializes and de-dupes.
"""

import os
import sys
import json
import subprocess
import time

# Self-contained: deliberately NO cross-repo import. The ControlPlane
# `hooks_common.is_controlplane_path` lives in the repo and is not on this
# hook's path; inline the one helper we need so the hook never hard-fails.
def log_hook(name, *a):
    print(f"[clippy-watch:{name}] {' '.join(str(x) for x in a)}", flush=True)


def is_controlplane_path(path: str) -> bool:
    """True when `path` is inside the ControlPlane crate source tree."""
    return "Crate/ControlPlane/Source" in path or "Crate/Library/Source" in path


def debounced() -> bool:
    """Return True if we should SUPPRESS this trigger (edit burst still active).

    A proper debounce: while edits keep arriving, every call extends the quiet
    timer (touches COOLDOWN_FILE). We only fire once COOLDOWN seconds have passed
    with no further edits.
    """
    now = time.time()
    try:
        if os.path.exists(COOLDOWN_FILE):
            last = os.path.getmtime(COOLDOWN_FILE)
            if now - last < COOLDOWN:
                os.utime(COOLDOWN_FILE, None)  # extend the burst window
                return True
    except OSError:
        pass
    return False


def mark_fired():
    """Record that we just fired, so the next burst starts a fresh quiet timer."""
    try:
        with open(COOLDOWN_FILE, "w") as f:
            f.write(str(int(time.time())))
    except OSError:
        pass

PROFILE = os.environ.get("HERMES_PROFILE", "")
LOCK = "/tmp/clippy-watch.lock"
# Debounce: only FIRE after COOLDOWN seconds of edit silence. While edits keep
# arriving (a worker batch), the burst is suppressed and the quiet timer is
# extended on every edit. This prevents a clippy fix-worker storm during bulk
# multi-RFC development.
COOLDOWN = 600  # 10 minutes of quiet before clippy fires
COOLDOWN_FILE = "/tmp/clippy-watch.cooldown"
REPO = "/Volumes/CORSAIR/Developer/macOS/Application/PlayForm/Cargo/Control"
FIX_WORKER_PROMPT = """You are an auto-dispatched fix worker for the ControlPlane repo.
A clippy run reported warnings/errors. Fix them and commit, WITHOUT interrupting
anything else and WITHOUT an RFC.

TASK:
1. `cd {repo} && export HERMES_PROFILE=dev-controlplane`
2. Run `cargo clippy -p controlplane-library -p controlplane-hermes -- -D warnings 2>&1 | tail -40`
   (if that crate set is not the one that failed, run `cargo clippy --workspace -- -D warnings`).
3. For EACH warning/error: fix the code (naming, types, borrow, unused, collapsible-if,
   etc.) by editing the exact file. Prefer minimal, correct fixes. Do NOT rewrite whole files.
4. After fixes: `cargo clippy -p controlplane-library -p controlplane-hermes -- -D warnings`
   must exit 0, then `cargo test --workspace` must pass.
5. Commit ONLY the fix with `git add <changed rust files>` then
   `git gcommit-hermes` (message from STDIN) — a short subject like
   "fix(clippy): <one line>". NEVER `git add -A`, NEVER `git reset`, NEVER touch
   `.agents/state/`.
6. Report compact: files_changed / clippy_exit / test_exit / Blockers.
No RFC, no chat, no interaction. Just fix and commit."""


def crate_for(path: str):
    """Map an edited Rust path to the crate to check."""
    if "Crate/Library/Source" in path:
        return "controlplane-library"
    if "Crate/ControlPlane/Source" in path:
        return "controlplane-hermes"
    return None


def run_clippy(crate: str) -> int:
    """Return clippy exit code for the crate (1 if it fired)."""
    try:
        r = subprocess.run(
            ["cargo", "clippy", "-p", crate, "--", "-D", "warnings"],
            cwd=REPO, capture_output=True, text=True, timeout=240,
        )
        return r.returncode
    except Exception as e:  # pragma: no cover
        log_hook("clippy", f"cargo clippy failed to launch: {e}")
        return 0


def maybe_spawn_fix_worker():
    """Spawn the background fix worker if not already running (lock-guarded)."""
    try:
        if os.path.exists(LOCK):
            # A worker is already queued/running; de-dupe.
            return
        with open(LOCK, "w") as f:
            f.write(str(int(time.time())))
    except OSError:
        return

    try:
        prompt = FIX_WORKER_PROMPT.format(repo=REPO)
        subprocess.Popen(
            ["hermes", "-z", prompt],
            cwd=REPO,
            stdout=open("/tmp/clippy-watch-fix.out", "a"),
            stderr=subprocess.STDOUT,
            env={**os.environ, "HERMES_PROFILE": "dev-controlplane"},
            start_new_session=True,
        )
        log_hook("spawn", "fix worker launched (background, no RFC)")
    except Exception as e:  # pragma: no cover
        log_hook("spawn", f"failed to launch fix worker: {e}")


def main():
    # Profile gate — only dev-controlplane.
    if PROFILE != "dev-controlplane":
        return

    # Hooks receive the tool call as JSON on stdin (pre/post variants).
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return

    # post_tool_call payload shape varies; gather any edited path we can find.
    paths = []
    for key in ("path", "file_path", "tool_input_path"):
        v = data.get(key)
        if isinstance(v, str):
            paths.append(v)
    # Also scan tool_input for a "path" field.
    ti = data.get("tool_input") or {}
    if isinstance(ti, dict) and isinstance(ti.get("path"), str):
        paths.append(ti["path"])

    rust_paths = [p for p in paths if p and p.endswith(".rs") and is_controlplane_path(p)]
    if not rust_paths:
        return

    # Check the most specific crate among edited files.
    crates = {crate_for(p) for p in rust_paths}
    crates.discard(None)
    if not crates:
        return

    # Prefer the hermes crate if both touched, else the single one.
    crate = "controlplane-hermes" if "controlplane-hermes" in crates else next(iter(crates))

    # Debounce: suppress while an edit burst is active (e.g. a worker batch).
    # We only fire after COOLDOWN seconds of silence.
    if debounced():
        log_hook("debounce", f"{crate}: burst active, suppressed (fires after {COOLDOWN}s quiet)")
        return

    rc = run_clippy(crate)
    mark_fired()  # record the fire so the next burst restarts the quiet timer
    if rc != 0:
        log_hook("clippy", f"{crate} reported issues (exit {rc}); dispatching fix worker")
        maybe_spawn_fix_worker()
    else:
        log_hook("clippy", f"{crate} clean")


if __name__ == "__main__":
    main()
