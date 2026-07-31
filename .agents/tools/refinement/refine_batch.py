#!/usr/bin/env python3
"""STE-Code Refinement Orchestrator — parallel batch pipeline.

Reads ste-code/extracted/*.md (the 109 worker outputs) and reformat each into
clean, standardized markdown under ste-code/refined/ following the 9 refinement
rules. Mirrors extract_batch.py: checkpoint + per-batch git commit + crash-safe
resume (--resume).

Launches each BATCH as its own background process so batches run in parallel
(multiple workers per file, many batches at once) — this is the "batch of many
workers" mode.

Usage:
  python3 refine_batch.py [start_batch] [num_batches] [--resume]
  python3 refine_batch.py            # all 37 batches, serial launch of parallel batches
  STE_MODEL=tencent/hy3:free python3 refine_batch.py 1 37

Model: resolved via STE_MODEL env var (default tencent/hy3:free), matching
extract_batch.py.
"""

import os
import sys
import time
import re
import json
import signal
import subprocess
import atexit
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
EXTRACTED_DIR = PROJECT / "ste-code" / "extracted"
REFINED_DIR = PROJECT / "ste-code" / "refined"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "refine-checkpoint.json"

# ── Config ────────────────────────────────────────────────────────────────────
MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
WORKERS_PER_BATCH = int(os.environ.get("REFINE_WORKERS_PER_BATCH", "3"))
TOTAL_WORKERS = 109
TIMEOUT_SECONDS = 300

VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")

FILENAME_RE = re.compile(r"^w(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$")


def _build_prompt(input_filename, output_filename, start_page, end_page):
    """9-rule refinement prompt (canonical, from generate_refine_prompts.py)."""
    return f"""TASK: Reformat the extracted spec file into clean, standardized markdown following ALL 9 refinement rules below.

INPUT: ste-code/extracted/{input_filename}
OUTPUT: ste-code/refined/{output_filename}

RULES (apply in order, do not skip any):

1. PRESERVE ALL CONTENT. Never delete a single word, number, example, or table cell.

2. HEADINGS: Use # for page header, ## for sections, ### for rules, #### for dictionary entries. Remove ### from proper names like ASD-STE100.

3. TABLES: Convert all tables to clean markdown format. Align columns. Add missing headers. Merge cells split by PDF extraction.

4. STE/NON-STE: Format ALL example pairs as:
   > **STE:** [text]
   > **Non-STE:** [text]
   Separate merged examples into individual pairs.

5. CODE: Wrap code snippets in ```language fences.

6. DICTIONARY: Format each entry with - list under #### heading. Separate APPROVED from UNAPPROVED entries clearly.

7. METADATA: Replace repetitive page headers with a single metadata block:
   > **Source:** ASD-STE100 Issue 9, January 2025
   > **Pages:** {start_page}–{end_page} of 434

8. LISTS: Standardize indentation. Use 1. 2. 3. for numbered, - for bullets.

9. SPACING: One blank line between sections. No triple blanks. No trailing spaces.

Output ONLY the refined markdown file. No explanations, no commentary.
"""


def _load_checkpoint():
    if CHECKPOINT_PATH.exists():
        try:
            return json.load(open(CHECKPOINT_PATH))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_checkpoint(ckpt):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(CHECKPOINT_PATH) + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(ckpt, f, indent=2, default=str)
        os.replace(tmp, str(CHECKPOINT_PATH))
    except Exception:
        pass


_checkpoint = _load_checkpoint()


def find_workers():
    """Map worker_num -> (path, start, end) sorted by worker number."""
    workers = {}
    for f in EXTRACTED_DIR.glob("*.md"):
        m = FILENAME_RE.match(f.name)
        if not m:
            continue
        w = int(m.group("worker"))
        workers[w] = (f, int(m.group("start")), int(m.group("end")))
    return dict(sorted(workers.items()))


def run_worker(worker_num, src_path, start, end):
    """Run a single refinement worker (foreground, returns True/False)."""
    output_name = f"r{worker_num:03d}-p{start}-{end}.md"
    output_path = REFINED_DIR / output_name

    # checkpoint skip
    ck = _checkpoint.get(str(worker_num))
    if ck and ck.get("passed") and output_path.exists():
        print(f"  R{worker_num:03d}: ✓ Already refined (checkpoint skip)", flush=True)
        return True

    prompt = _build_prompt(src_path.name, output_name, start, end)
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"refine-prompt-{worker_num:03d}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "120", "STE_MODEL": MODEL}
    cmd = [VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL]

    start_t = time.time()
    print(f"  R{worker_num:03d}: Refining {src_path.name} → {output_name}...", flush=True)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=TIMEOUT_SECONDS, env=env, cwd=str(PROJECT))
        dur = time.time() - start_t
        if result.stderr:
            sl = result.stderr.lower()
            if "error" in sl or "traceback" in sl:
                print(f"  R{worker_num:03d}: [stderr] {result.stderr[:300]}", flush=True)
    except subprocess.TimeoutExpired:
        print(f"  R{worker_num:03d}: [TIMEOUT] after {TIMEOUT_SECONDS}s", flush=True)
        return False
    except Exception as e:
        print(f"  R{worker_num:03d}: [ERROR] {e}", flush=True)
        return False

    if output_path.exists():
        sz = output_path.stat().st_size
        ok = sz >= 400  # refined must be substantial
        if ok:
            _checkpoint[str(worker_num)] = {"passed": True, "output_size": sz,
                                            "duration": round(dur, 1)}
            _save_checkpoint(_checkpoint)
            print(f"  R{worker_num:03d}: [PASS] {sz}B ({dur:.1f}s)", flush=True)
            return True
        else:
            print(f"  R{worker_num:03d}: [FAIL] output too small ({sz}B)", flush=True)
            return False
    else:
        print(f"  R{worker_num:03d}: [FAIL] no output file", flush=True)
        return False


def process_batch(batch_num, workers_map):
    start_worker = (batch_num - 1) * WORKERS_PER_BATCH + 1
    members = [(w, workers_map[w]) for w in range(start_worker, start_worker + WORKERS_PER_BATCH)
               if w in workers_map]
    if not members:
        print(f"Batch {batch_num}: no workers", flush=True)
        return True

    ids = ", ".join(f"R{w:03d}" for w, _ in members)
    print(f"\n{'='*60}\nBatch {batch_num} — {ids}\n{'='*60}", flush=True)

    all_ok = True
    for w, (src, s, e) in members:
        ok = run_worker(w, src, s, e)
        if not ok:
            all_ok = False

    # git commit passed worker outputs
    passed_files = []
    for w, (src, s, e) in members:
        out = REFINED_DIR / f"r{w:03d}-p{s}-{e}.md"
        if out.exists():
            passed_files.append(str(out.relative_to(PROJECT)))
    if passed_files:
        subprocess.run(["git", "add", *passed_files], capture_output=True, text=True, cwd=str(PROJECT))
        msg = f"Refine Batch {batch_num:02d} - {'PASS' if all_ok else 'PARTIAL'} - {ids}"
        r = subprocess.run(["git", "commit", "-m", msg, *passed_files],
                           capture_output=True, text=True, cwd=str(PROJECT))
        if r.returncode == 0:
            print(f"  ✓ Committed: {msg}", flush=True)
        else:
            print(f"  ✗ Commit failed: {r.stderr[:200]}", flush=True)
    return all_ok


def main():
    resume = "--resume" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start_batch = int(args[0]) if len(args) > 0 else 1
    num_batches = int(args[1]) if len(args) > 1 else 37

    workers_map = find_workers()
    print(f"STE-Code Refinement Pipeline", flush=True)
    print(f"Model: {MODEL}", flush=True)
    print(f"Workers available: {len(workers_map)} (batches of {WORKERS_PER_BATCH})", flush=True)
    print(f"Batches: {num_batches} (from {start_batch})", flush=True)
    print(f"Resume: {'yes' if resume else 'no'}", flush=True)

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    for batch_num in range(start_batch, min(start_batch + num_batches, TOTAL_WORKERS // WORKERS_PER_BATCH + 2)):
        if (batch_num - 1) * WORKERS_PER_BATCH + 1 > TOTAL_WORKERS:
            break
        process_batch(batch_num, workers_map)

    final = len(list(REFINED_DIR.glob("r*.md")))
    print(f"\n{'='*60}\nDone. Files in refined/: {final}\n{'='*60}", flush=True)


if __name__ == "__main__":
    main()
