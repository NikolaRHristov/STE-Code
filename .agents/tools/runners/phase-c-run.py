#!/usr/bin/env python3
"""Phase C Runner — Semantic Grouping (deterministic).

Groups the refined page files (ste-code/refined/rNNN-pA-B.md) into ~24
semantically coherent chunks under ste-code/grouped/, split by section and, for
the dictionary, by balanced alphabetical buckets.

WHY THIS NO LONGER DRIVES AN LLM
--------------------------------
The previous version handed the ENTIRE 109-file -> ~24-group concatenation
(~600 KB of output) to a single free-tier agent and asked it to re-emit every
byte. Per the Refinement agent's hard-won lessons (.agents/feedback/exchange.md),
that is a guaranteed mid-stream truncation — i.e. silent, corpus-wide content
loss (a Rule 1 breach). Grouping is a DETERMINISTIC re-organization (concatenate
+ split; no judgement), so it is now pure Python: bytes are MOVED, never
re-typed, and content cannot be lost. See:
    .agents/tools/grouping/group_engine.py   (plan + parity primitives)
    .agents/tools/grouping/group_batch.py    (assembler + gates)
    .agents/tools/grouping/verify-groups.py  (post-assembly verifier)

It also stops trusting the STALE section-types.md ranges the old prompt embedded
(they claimed DICT 129-360 / APPENDIX 361-434; the MANIFEST proves the dictionary
runs A..Y through page 426). The engine reads section membership from the
MANIFEST page-IDs, which are churn-proof ground truth.

CLI COMPATIBILITY
-----------------
The historical flags are preserved so existing scripts/wrappers keep working:
  --agent / --model : accepted but INFORMATIONAL only (grouping is deterministic;
                      there is no agent to select). A note is printed.
  --dry-run         : plan only, write nothing (delegates to group_batch --dry-run).
Additional:
  --force           : override the corpus-readiness guard + idempotence.
  --verify          : after assembly, run verify-groups.py.

Usage:
  python3 .agents/tools/runners/phase-c-run.py --dry-run   # safe preview
  python3 .agents/tools/runners/phase-c-run.py             # assemble (guarded)
  python3 .agents/tools/runners/phase-c-run.py --verify    # assemble + verify
"""
import subprocess
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
GROUPING_DIR = PROJECT / ".agents" / "tools" / "grouping"
GROUP_BATCH = GROUPING_DIR / "group_batch.py"
VERIFY = GROUPING_DIR / "verify-groups.py"
REFINED_DIR = PROJECT / "ste-code" / "refined"
GROUPED_DIR = PROJECT / "ste-code" / "grouped"


def main():
    argv = sys.argv[1:]
    dry_run = "--dry-run" in argv
    force = "--force" in argv
    do_verify = "--verify" in argv

    # Absorb the legacy agent/model flags (informational only now).
    agent = model = None
    for i, arg in enumerate(argv):
        if arg == "--agent" and i + 1 < len(argv):
            agent = argv[i + 1]
        elif arg == "--model" and i + 1 < len(argv):
            model = argv[i + 1]
    if agent or model:
        print(f"[note] --agent/--model are ignored: Phase C grouping is now "
              f"deterministic (pure Python), so there is no agent to select. "
              f"(got agent={agent!r} model={model!r})", flush=True)

    print(f"Phase C grouping (deterministic) — input {REFINED_DIR}", flush=True)
    print(f"                                    output {GROUPED_DIR}", flush=True)

    cmd = [sys.executable, str(GROUP_BATCH)]
    if dry_run:
        cmd.append("--dry-run")
    if force:
        cmd.append("--force")

    rc = subprocess.run(cmd, cwd=str(PROJECT)).returncode
    if rc != 0:
        sys.exit(rc)

    if do_verify and not dry_run:
        print("\nRunning post-assembly verification...", flush=True)
        rc = subprocess.run([sys.executable, str(VERIFY)], cwd=str(PROJECT)).returncode
        sys.exit(rc)


if __name__ == "__main__":
    main()
