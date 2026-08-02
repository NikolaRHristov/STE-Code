#!/usr/bin/env python3
"""Level 4 Parallel Assembly — spawns multiple parallel workers for dictionary,
synonym table, and rule groups. Designed for large-scale assembly.

Usage: python3 .agents/tools/refinement/assemble-level4-parallel.py [--agent hermes|claude|codex] [--dry-run]
"""

import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"
LEVEL4_DIR = PROJECT / "ste-code" / "artifacts" / "level4"
TMP_DIR = PROJECT / ".agents" / "tmp"


def build_worker_prompt(task_name, files, output_path, extra_instructions=""):
    file_list = "\n".join(f"  {f}" for f in files)
    return f"""You are STE-Code. Task: {task_name}

Read these files:
{file_list}

{extra_instructions}

Save output to: {output_path}
Use write_file. Report character count when done.
"""


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    LEVEL4_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    summaries = sorted(LEVEL5_DIR.glob("sec*/a-sec*/summary.md"))
    sections = {}
    for sf in summaries:
        sec = sf.parent.parent.name
        sections.setdefault(sec, []).append(str(sf.relative_to(PROJECT)))

    tasks = [
        ("Rules S1-3", sections.get("sec1", []) + sections.get("sec2", []) + sections.get("sec3", []),
         LEVEL4_DIR / "rules-s1-3.md", "Extract compact rule summaries for sections 1-3."),
        ("Rules S4-6", sections.get("sec4", []) + sections.get("sec5", []) + sections.get("sec6", []),
         LEVEL4_DIR / "rules-s4-6.md", "Extract compact rule summaries for sections 4-6."),
        ("Rules S7-9", sections.get("sec7", []) + sections.get("sec8", []) + sections.get("sec9", []),
         LEVEL4_DIR / "rules-s7-9.md", "Extract compact rule summaries for sections 7-9."),
    ]

    if dry_run:
        for name, files, out, _ in tasks:
            print(f"  {name}: {len(files)} files → {out}")
        return

    processes = []
    for name, files, out, instructions in tasks:
        prompt = build_worker_prompt(name, files, out, instructions)
        proc = launch_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
        processes.append((name, proc))
        print(f"Launched {name} ({len(files)} files, PID {proc.pid})")

    print(f"\nWaiting for {len(processes)} workers...")
    for name, proc in processes:
        proc.communicate(timeout=600)
        print(f"  {name}: done")

    # Check outputs
    for name, _, out, _ in tasks:
        if out.exists():
            print(f"  {out.name}: {out.stat().st_size:,} bytes")
        else:
            print(f"  {out.name}: NOT CREATED")


if __name__ == "__main__":
    main()
