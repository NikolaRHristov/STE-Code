#!/usr/bin/env python3
"""Print the jail context a *fresh* session would resolve for this profile.

Read-only probe. Mirrors exactly what `core.policy.load_context()` computes, so
it is safe to run while triaging a looping session: it imports the real jail core
and evaluates the live policy, project root, and write/deny roots. No cwd
assumptions, no in-session caching.

Usage:
    python3 show_jail_context.py
    HERMES_PROFILE=dev-ste-code HERMES_HOME=~/.hermes/profiles/dev-ste-code \
        python3 show_jail_context.py

Exit code 0 always (this is a diagnostic, never a gate). A healthy dev session
prints `policy=dev ... write_roots=6 ...` and lists the repo under `write:`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _jail_root() -> Path:
    """Locate the jail root, anchored to the repo (not by walking parents).

    This script lives under `.agents/skills/.../scripts/`, so the jail core
    (`core/policy.py`) is NOT a parent of it - it is a sibling under
    `.agents/hermes/jail/`. Walk up to the repo root (the dir containing
    `.agents/`) and join the known jail path. Hop-counting is banned in this
    project; the `.agents/` marker is the stable anchor.
    """
    here = Path(__file__).resolve()
    repo = here
    while not (repo / ".agents").is_dir() and repo.parent != repo:
        repo = repo.parent
    jail = repo / ".agents" / "hermes" / "jail"
    if (jail / "core" / "policy.py").exists():
        return jail
    raise RuntimeError(f"show_jail_context: jail core not found under {jail}")


def main() -> int:
    sys.path.insert(0, str(_jail_root()))
    import core.policy as p  # noqa: E402

    # Show which env knobs are in force, so an env-leak misconfiguration is
    # visible at a glance (the dominant cause of "cannot write to repo").
    print("env:")
    for var in ("HERMES_HOME", "HERMES_PROFILE", "STE_CODE_JAIL_POLICY"):
        val = os.environ.get(var)
        print(f"  {var:<22} = {val if val else '(unset)'}")

    ctx = p.load_context(force=True)
    print()
    print(f"profile : {ctx.profile}")
    print(f"policy  : {ctx.policy.name}")
    print(f"enforce : {ctx.enforce}")
    print(f"project_root: {ctx.project_root}")
    print(f"write_roots ({len(ctx.policy.write_roots)}):")
    for r in ctx.policy.write_roots:
        mark = "  <-- repo" if r == ctx.project_root else ""
        print(f"  write: {r}{mark}")
    print(f"deny_roots ({len(ctx.policy.deny_roots)}):")
    for r in ctx.policy.deny_roots:
        print(f"  deny:  {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
