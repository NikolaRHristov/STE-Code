#!/usr/bin/env python3
"""Fix remaining FIXME markers by generating missing STE corrections.

Targets files with FIXME content gaps. Launches parallel agent workers
to read each file, generate STE corrections for all FIXMEs, and apply them.

Usage: python3 .agents/tools/maintenance/fix-fixmes.py [--agent hermes|claude|codex] [--dry-run]
"""

import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

import sys as _sys

_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater

TPL = Templater(__file__)

TMP_DIR = PROJECT / ".agents" / "tmp" / "fixme"

# Files known to have FIXME markers — edit this list as needed
FILES_WITH_FIXMES = [
    "ste-code/adapted/a-sec6-rule6.4.md",
    "ste-code/adapted/a-sec6-rule6.5.md",
    "ste-code/adapted/a-sec4-rule4.4.md",
    "ste-code/adapted/a-sec4-rule4.5.md",
]


def build_worker_prompt(relpath):
    return TPL.render(
        "fix-fixmes-worker",
        relpath=relpath,
        report_path=str(TMP_DIR / f"{Path(relpath).stem}-fixme-report.md"),
    )


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    mkdir(TMP_DIR)

    if dry_run:
        print(f"Would process {len(FILES_WITH_FIXMES)} files:")
        for f in FILES_WITH_FIXMES:
            print(f"  {f}")
        return

    processes = []
    for relpath in FILES_WITH_FIXMES:
        prompt = build_worker_prompt(relpath)
        proc = launch_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
        processes.append((relpath, proc))
        print(f"Launched: {relpath} (PID {proc.pid})")

    print(f"\nWaiting for {len(processes)} workers...")
    for relpath, proc in processes:
        stdout, stderr = proc.communicate(timeout=600)
        status = "OK" if proc.returncode == 0 else f"FAIL ({proc.returncode})"
        print(f"{relpath}: {status}")

    # Verify — check remaining FIXMEs
    print("\nPOST-FIX CHECK")
    for relpath in FILES_WITH_FIXMES:
        abspath = PROJECT / relpath
        if abspath.exists():
            count = abspath.read_text().count("[FIXME:")
            print(f"  {relpath}: {count} FIXME(s) remaining")


if __name__ == "__main__":
    main()
