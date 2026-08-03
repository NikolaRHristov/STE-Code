#!/usr/bin/env python3
"""Phase 1 — Grounding: verify linguistic layer claims against adapted rules.

Divides the 55 adapted rules into 5 batches, launches parallel workers.
Each worker checks its batch for: CONFIRMED (claim matches rule),
CONTRADICTION (conflict), NOVEL (no counterpart in rules).

Usage: python3 .agents/tools/quality/ground-phase1.py [--dry-run]
Output: docs/roadmap/GROUNDING-REPORT.md
"""

import sys, json
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
from ste_io import write_text, mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())

import sys as _sys

_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater

TPL = Templater(__file__)

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
SEMANTICS = json.loads(
    (PROJECT / "ste-code" / "linguistics" / "semantics.json").read_text()
)
OUTPUT = PROJECT / "docs" / "roadmap" / "GROUNDING-REPORT.md"
TMP_DIR = PROJECT / ".agents" / "tmp" / "grounding"


def build_worker_prompt(batch_files, batch_num, total_batches):
    """Build prompt for one grounding worker."""
    file_list = "\n".join(f"  {f.name}" for f in batch_files)

    # Extract key claims to verify
    claims = []
    for term, data in SEMANTICS["semantic_roles"]["term_table"].items():
        claims.append(
            f"SR CLAIM: '{term}' is an {data['class']} term. Result form: {data.get('result', 'none')}. Referenced in: {', '.join(data.get('rule_refs', []))}"
        )

    for term, data in SEMANTICS["single_referent_rule"]["domain_collisions"][
        "entries"
    ].items():
        contexts = ", ".join(c["qualifier"] for c in data["contexts"])
        claims.append(
            f"SRR CLAIM: '{term}' has domain collisions requiring qualification: {contexts}"
        )

    claims_text = "\n".join(claims[:30])  # First 30 claims

    return TPL.render(
        "ground-worker",
        batch_num=batch_num,
        total_batches=total_batches,
        count=len(batch_files),
        file_list=file_list,
        claims_text=claims_text,
        report_dir=str(TMP_DIR / f"batch-{batch_num:02d}-grounding.md"),
    )


def main():
    dry_run = "--dry-run" in sys.argv
    mkdir(TMP_DIR)

    files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
    batch_size = max(1, len(files) // 5)
    batches = [files[i : i + batch_size] for i in range(0, len(files), batch_size)]

    print(f"Files: {len(files)} in {len(batches)} batches")
    if dry_run:
        for i, b in enumerate(batches):
            print(f"  Batch {i + 1}: {len(b)} files — {b[0].name} to {b[-1].name}")
        return

    processes = []
    for i, batch in enumerate(batches):
        prompt = build_worker_prompt(batch, i + 1, len(batches))
        proc = launch_agent(prompt, model=CFG.model, cwd=PROJECT)
        processes.append((i + 1, proc))
        print(
            f"Launched batch {i + 1}/{len(batches)} ({len(batch)} files, PID {proc.pid})"
        )

    print(f"\nWaiting for {len(processes)} grounding workers...")
    for batch_num, proc in processes:
        proc.communicate(timeout=900)
        print(f"  Batch {batch_num}: done")

    # Collect reports
    report_lines = ["# Phase 1 — Grounding Report\n", f"\nDate: 2026-07-30\n"]
    for report_file in sorted(TMP_DIR.glob("batch-*-grounding.md")):
        report_lines.append(report_file.read_text())
        report_lines.append("\n---\n")

    # Merge into final report
    write_text(OUTPUT, "\n".join(report_lines))
    print(f"\nGrounding report: {OUTPUT}")


if __name__ == "__main__":
    main()
