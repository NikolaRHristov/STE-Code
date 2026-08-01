#!/usr/bin/env python3
"""Phase F — single-sub-document LLM distillation worker (self-contained).

Distills ONE sub-document of one tier: reads the deterministic base sub-doc,
runs ONE hermes-oneshot-wrapper session that writes the distilled sub-doc to
ste-code/artifacts/level<LABEL>/<SUBDOC>, and on any failure writes the base
content as fallback. Hard timeout via start_new_session so an orphan cannot
hang forever.

This worker is meant to be launched as ITS OWN background process (per the
project's "each worker = own bg proc" rule) — it does NOT depend on a parent
loop, so it survives parent reaping.

Usage:
  python3 distill_one.py <tier_dir> <subdoc> <level_label> [desc]
  e.g. python3 distill_one.py level-2 01-principles.md -2 "ultra-minimal ..."
"""
from __future__ import annotations

import os
import sys
import json
import signal
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
BASE_DIR = ARTIFACTS_DIR / "_base"
STATE_DIR = PROJECT / ".agents" / "state"
VENDOR_DIR = PROJECT / ".agents" / "vendor"

MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 300  # per sub-doc; healthy distills 20-90s, large a few min.

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import render_template

PROMPT_MD = PROJECT / ".agents" / "tools" / "prompts" / "synthesize-artifacts-worker.md"


def main():
    if len(sys.argv) < 4:
        print("usage: distill_one.py <tier_dir> <subdoc> <level_label> [desc]", file=sys.stderr)
        return 2
    tier_dir, subdoc, label = sys.argv[1], sys.argv[2], sys.argv[3]
    desc = sys.argv[4] if len(sys.argv) > 4 else ""

    base_path = BASE_DIR / tier_dir / subdoc
    out_path = ARTIFACTS_DIR / tier_dir / subdoc
    out_path.parent.mkdir(parents=True, exist_ok=True)

    prompt = render_template(
        PROMPT_MD, subdoc=subdoc, level_label=label, desc=desc, base_path=str(base_path))
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"distill-{tier_dir}-{subdoc}.txt"
    pf.write_text(prompt, encoding="utf-8")

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "300", "STE_MODEL": MODEL}
    traj_path = tmp / f"distill-traj-{tier_dir}-{subdoc}.txt"
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True,
                           timeout=TIMEOUT_SECONDS, env=env,
                           start_new_session=True, cwd=str(PROJECT))
        # Log the worker's reasoning trajectory locally (not staged) so we can
        # inspect WHY it chose this distillation path over another.
        traj_path.write_text(
            f"# distillation trajectory: {tier_dir}/{subdoc} (level {label})\n"
            f"# model: {MODEL}  timeout: {TIMEOUT_SECONDS}s\n\n"
            f"--- STDOUT ---\n{r.stdout}\n\n--- STDERR ---\n{r.stderr}\n",
            encoding="utf-8")
    except subprocess.TimeoutExpired as e:
        traj_path.write_text(
            f"# distillation trajectory: {tier_dir}/{subdoc}\n# TIMEOUT after {TIMEOUT_SECONDS}s\n",
            encoding="utf-8")
        print(f"  TIMEOUT {tier_dir}/{subdoc} (>{TIMEOUT_SECONDS}s) -> fallback", flush=True)
    except Exception as e:
        traj_path.write_text(
            f"# distillation trajectory: {tier_dir}/{subdoc}\n# ERROR: {e}\n",
            encoding="utf-8")
        print(f"  ERROR {tier_dir}/{subdoc}: {e} -> fallback", flush=True)

    # Verify / fallback: the worker writes the file; if missing or too small,
    # ship the deterministic base so nothing is lost.
    if out_path.exists() and out_path.stat().st_size > 200:
        print(f"  OK {tier_dir}/{subdoc} ({out_path.stat().st_size}B)", flush=True)
        return 0
    if base_path.exists():
        out_path.write_text(base_path.read_text(errors="ignore"), encoding="utf-8")
        print(f"  FALLBACK {tier_dir}/{subdoc} (base shipped, {out_path.stat().st_size}B)", flush=True)
    else:
        out_path.write_text(f"# {subdoc}\n\n(base unavailable)\n", encoding="utf-8")
        print(f"  FALLBACK-EMPTY {tier_dir}/{subdoc}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
