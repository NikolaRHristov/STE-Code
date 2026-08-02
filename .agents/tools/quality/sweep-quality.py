#!/usr/bin/env python3
"""Quality Sweep — parallel batch workers audit all STE-Code output files.

Divides all deliverable files into batches, launches parallel agent workers
to quality-check each batch for STE-Code compliance, formatting, and consistency.

Usage: python3 .agents/tools/quality/sweep-quality.py [--agent hermes|claude|codex] [--dry-run] [--batches N]
"""

import sys, time
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import write_text, mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)

TMP_DIR = PROJECT / ".agents" / "tmp" / "sweep"
SWEEP_REPORT = PROJECT / "ste-code" / "artifacts" / "sweep-report.md"

# Files to sweep
ARTIFACT_FILES = sorted(
    list((PROJECT / "ste-code" / "artifacts").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level1").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level2").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level3").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level4").glob("*.txt"))
)
ADAPTED_FILES = sorted((PROJECT / "ste-code" / "adapted").glob("a-sec*.md"))

# The quality checklist lives in templates/sweep-checklist.md (edit there).
CHECKLIST = TPL.load("sweep-checklist")


def build_worker_prompt(batch_files, batch_num, total_batches):
    """Build a worker prompt for one batch of files."""
    file_list = "\n".join(f"  {str(f.relative_to(PROJECT))}" for f in batch_files)
    return TPL.render(
        "sweep-worker",
        count=len(batch_files),
        batch_num=batch_num,
        total_batches=total_batches,
        file_list=file_list,
        checklist=CHECKLIST,
        report_path=str(TMP_DIR / f"batch-{batch_num:02d}-report.md"),
    )


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    num_batches = 5
    for i, arg in enumerate(sys.argv):
        if arg == "--batches" and i + 1 < len(sys.argv):
            num_batches = int(sys.argv[i + 1])

    all_files = ARTIFACT_FILES + ADAPTED_FILES
    all_files = sorted(set(f for f in all_files if f.exists() and f.is_file()))

    print(f"Files to sweep: {len(all_files)}")
    print(f"Batches: {num_batches} (~{len(all_files)//num_batches} files each)")

    # Divide into batches
    batch_size = max(1, len(all_files) // num_batches)
    batches = []
    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size if i < num_batches - 1 else len(all_files)
        batches.append(all_files[start:end])

    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}: {len(batch)} files")

    if dry_run:
        print("\nDry run complete. Use without --dry-run to execute.")
        return

    mkdir(TMP_DIR)

    # Launch all batches in parallel using agent_runner
    processes = []
    for i, batch in enumerate(batches):
        prompt = build_worker_prompt(batch, i + 1, num_batches)
        proc = launch_agent(prompt, agent=agent, model=CFG.model, cwd=PROJECT)
        processes.append((i + 1, proc))
        print(f"Launched batch {i+1}/{num_batches} (PID {proc.pid})")

    # Wait for all and collect results
    print(f"\nWaiting for {len(processes)} batches...")
    results = []
    for batch_num, proc in processes:
        stdout, stderr = proc.communicate(timeout=900)
        results.append((batch_num, proc.returncode, stdout, stderr))
        status = "OK" if proc.returncode == 0 else f"FAIL ({proc.returncode})"
        print(f"Batch {batch_num}: {status}")

    # Write sweep report
    report_lines = [
        "# Quality Sweep Report",
        f"\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Files swept: {len(all_files)}",
        f"Batches: {num_batches}",
        f"\n## Batch Results\n",
    ]
    for batch_num, rc, stdout, stderr in results:
        report_lines.append(f"\n### Batch {batch_num} (exit {rc})")
        if stdout:
            tail = stdout[-2000:] if len(stdout) > 2000 else stdout
            report_lines.append(f"```\n{tail}\n```")
        if stderr:
            report_lines.append(f"Errors:\n```\n{stderr[-500:]}\n```")

    write_text(SWEEP_REPORT, "\n".join(report_lines))
    print(f"\nSweep report: {SWEEP_REPORT}")

    print("\nBatch reports:")
    for report_file in sorted(TMP_DIR.glob("batch-*-report.md")):
        print(f"  {report_file}")


if __name__ == "__main__":
    main()
