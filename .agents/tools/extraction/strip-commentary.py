#!/usr/bin/env python3
"""
Commentary stripping post-processor.
Usage: python3 .agents/tools/extraction/strip-commentary.py <worker_num>
"""

import sys
import os
import subprocess
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
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "extraction"))
from extract_batch import parse_manifest, worker_page_range, EXTRACTED_DIR, MODEL

exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())

TEMPLATE_PATH = PROJECT / ".agents" / "tools" / "prompts" / "strip-commentary.md"

DEFAULT_TEMPLATE = """You are a Refinement Agent. Read the file at {output_path}.
Remove ONLY meta-commentary (preamble, summary, narrative). Preserve all raw page content.
Write cleaned content to: {output_path}
Worker: W{worker_num:03d} (pages {start_pos}-{end_pos})"""


def build_clean_prompt(worker_num, start_pos, end_pos, output_path):
    try:
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
    except FileNotFoundError:
        template = DEFAULT_TEMPLATE
    if "---" in template:
        template = template.split("---", 1)[1].strip()
    return template.format(
        worker_num=worker_num,
        start_pos=start_pos,
        end_pos=end_pos,
        output_path=output_path,
    )


def clean_worker(worker_num):
    start_pos, end_pos = worker_page_range(worker_num)
    output_path = str(EXTRACTED_DIR / f"w{worker_num:03d}-p{start_pos}-{end_pos}.md")
    prompt = build_clean_prompt(worker_num, start_pos, end_pos, output_path)
    print(f"Cleaning W{worker_num:03d} (pages {start_pos}-{end_pos})...", flush=True)
    result = run_agent(
        prompt, agent="hermes", model=MODEL, cwd=str(PROJECT), timeout=300
    )
    output_file = Path(output_path)
    if output_file.exists():
        print(f"  File exists: {output_file.stat().st_size}B", flush=True)
    else:
        print(f"  File not created!", flush=True)
        if result.stdout:
            print(f"  stdout: {result.stdout[:500]}", flush=True)
        if result.stderr:
            print(f"  stderr: {result.stderr[:500]}", flush=True)
    return output_file.exists()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 strip-commentary.py <worker_num>")
        sys.exit(1)
    worker_num = int(sys.argv[1])
    success = clean_worker(worker_num)
    sys.exit(0 if success else 1)
