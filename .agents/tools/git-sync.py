#!/usr/bin/env python3
"""
Periodic git sync for the STE-Code repo — runs continuously in the background
(one pass every ~8 minutes) to keep the local branch in sync with origin/Current
and push committed work. SAFE: never auto-commits uncommitted changes, never
force-pushes, never merges conflicting branches — it only fast-forwards and
pushes already-committed work, and reports status.

Design per project convention:
  - fetch + fast-forward pull (no rebase of dirty tree)
  - push committed work to origin/Current
  - if a fast-forward is not possible (diverged), it STOPs and reports (no force)
  - never touches in-flight Phase D files (ste-code/adapted/*) or scratch dirs
    (.agents/tmp, .agents/state/adapt-checkpoint.json) — those are committed by
    their own orchestrators / the human, not by this sync loop.

Run via Hermes cronjob (every 8m) OR as a long-lived background process.
"""

import subprocess, time, sys, os


def _repo_root():
    """Resolve the repo root without hardcoding any local path."""
    here = os.path.dirname(os.path.abspath(__file__))
    # walk up to the dir that contains .git
    cur = here
    for _ in range(6):
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    # fallback: ask git
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            cwd=here,
        )
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except Exception:
        pass
    return here


REPO = _repo_root()
BRANCH = "Current"
REMOTE = "origin"
INTERVAL = 480  # seconds (8 min)


def run(cmd, check=True):
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def safe_git(args):
    return run(["git"] + args)


def sync_once():
    log = []
    # 1. fetch
    rc, out, err = safe_git(["fetch", REMOTE, "--quiet"])
    if rc != 0:
        return f"[sync] fetch FAILED: {err}"
    # 2. status of local vs remote
    rc, out, err = safe_git(
        ["rev-list", "--left-right", "--count", f"{REMOTE}/{BRANCH}...{BRANCH}"]
    )
    if rc != 0:
        return f"[sync] rev-list FAILED: {err}"
    behind, ahead = (out.split() + ["0", "0"])[:2]
    behind, ahead = int(behind), int(ahead)
    # 3. pull (fast-forward only) if behind
    if behind > 0 and ahead == 0:
        rc, out, err = safe_git(["merge", "--ff-only", f"{REMOTE}/{BRANCH}"])
        log.append(f"pulled {behind} commit(s): {out or err}")
    elif behind > 0 and ahead > 0:
        # diverged — do NOT force; report and wait for human
        return (
            f"[sync] DIVERGED behind={behind} ahead={ahead} — "
            f"not auto-merging. Run manually: git pull --rebase"
        )
    # 4. push committed work
    if ahead > 0:
        rc, out, err = safe_git(["push", REMOTE, BRANCH])
        if rc == 0:
            log.append(f"pushed {ahead} commit(s)")
        else:
            return f"[sync] push FAILED: {err}"
    if not log:
        return f"[sync] ok — in sync (behind={behind}, ahead={ahead})"
    return "[sync] " + "; ".join(log)


def main():
    one_shot = "--once" in sys.argv
    if one_shot:
        print(sync_once())
        return
    while True:
        try:
            msg = sync_once()
            # keep last line concise for cron delivery
            print(time.strftime("%Y-%m-%d %H:%M") + " " + msg)
        except Exception as e:
            print(time.strftime("%Y-%m-%d %H:%M") + f" [sync] ERROR: {e}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
