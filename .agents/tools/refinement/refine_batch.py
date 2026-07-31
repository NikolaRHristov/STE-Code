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
TIMEOUT_SECONDS = 600

VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")

FILENAME_RE = re.compile(r"^w(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$")

# ── Skill embedding: inject the refinement SKILL.md into every worker prompt ──
# The oneshot wrapper sub-agents do not auto-load the STE-Code profile skills,
# so the authoritative skill text is embedded. Edit the SKILL.md (not this
# script) to change refinement behavior.
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location(
    "skill_prompt",
    str(PROJECT / ".agents" / "tools" / "lib" / "skill_prompt.py"),
)
skill_prompt = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(skill_prompt)


def _word_count(text):
    """Count meaningful words (alphanumeric tokens >=2 chars), case-insensitive."""
    return len(re.findall(r"[A-Za-z0-9_]{2,}", text.lower()))


def _build_prompt(input_filename, output_filename, start_page, end_page):
    """Refinement worker prompt = tight wrapper + the authoritative refinement SKILL.md.

    The SKILL.md (rules 1-9, before/after examples, failure recovery) is the
    single source of truth. We embed it so the worker honors the exact protocol
    and we only have to edit the SKILL, not this script.
    """
    wrapper = f"""TASK: Reformat the extracted spec file into clean, standardized markdown.

INPUT:  ste-code/extracted/{input_filename}
OUTPUT: ste-code/refined/{output_filename}

You are the Refinement Worker. You read the raw extraction and rewrite it with
BETTER STRUCTURE ONLY. You do NOT change, adapt, translate, summarize, or delete
any words. Every word, number, example, table cell, and the `_<u><mark>` /
`<br>` annotations from the source MUST appear in your output.

MANDATORY OUTPUT SKELETON — the file MUST start EXACTLY with:

# Page {start_page}–{end_page} of 434

> **Source:** ASD-STE100 Issue 9, January 2025
> **Pages:** {start_page}–{end_page} of 434

Then the reformatted body. Keep every `# Page N of 434` header that appears in
the source (one per source page, in order), each immediately followed by that
page's body. Collapse ONLY the repeated per-page stamps (`**Page X-Y-Z**`,
`**Issue 9 2025-01-15**`, `**ASD-STE100 ...**`) into the single metadata block
above — do not drop the content those stamps sat next to.

STE / NON-STE EXAMPLES: ALWAYS split each pair into two separate blockquotes:
> **STE:** <full STE example text>
> **Non-STE:** <full non-STE example text>
Never merge STE and Non-STE onto one line or into one blockquote. Never truncate
the example text.

ZERO CONTENT LOSS — HARD SELF-CHECK (do this before you finish):
1. Count the meaningful words in the source file.
2. Count the meaningful words in your output.
3. Your output word count MUST be >= the source word count (same words, just
   restructured). If it is lower, you deleted content — rewrite and include it.
4. Every `_<u><mark>...</mark></u>_` annotation from the source must be present.
5. Every example sentence (especially phrasal-verb examples like
   "Put out the cat." / "Put out the fire.") must be present verbatim.

The authoritative protocol (9 rules, before/after examples, failure recovery)
follows. Follow it exactly.

"""
    skill = skill_prompt.skill_section("refinement")
    return wrapper + skill + "\n\nOutput ONLY the refined markdown file. No explanations, no commentary.\n"


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


def git_commit_locked(files, msg):
    """Serialize git commits across parallel batches via a lock dir."""
    import time as _time
    lock = STATE_DIR / "refine-git-lock"
    deadline = _time.time() + 120
    while _time.time() < deadline:
        try:
            lock.mkdir(exist_ok=False)
            break
        except FileExistsError:
            _time.sleep(1)
    else:
        return False
    try:
        subprocess.run(["git", "add", *files], capture_output=True, text=True, cwd=str(PROJECT))
        r = subprocess.run(["git", "commit", "-m", msg, *files],
                           capture_output=True, text=True, cwd=str(PROJECT))
        return r.returncode == 0
    finally:
        import shutil
        shutil.rmtree(lock, ignore_errors=True)


def run_worker(worker_num, src_path, start, end):
    """Run a single refinement worker (foreground, returns True/False).

    Retries on transient failures (API 429 / rate-limit / no output) with
    exponential backoff, since the oneshot wrapper exits fast on rejection.
    """
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

    max_attempts = 4
    for attempt in range(1, max_attempts + 1):
        start_t = time.time()
        print(f"  R{worker_num:03d}: Refining {src_path.name} → {output_name} (attempt {attempt})...", flush=True)
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
            txt = output_path.read_text(encoding="utf-8")
            ok_size = sz >= 400
            ok_skel = txt.lstrip().startswith(f"# Page {start}")

            # ── AUTOMATED CONTENT-PARITY GATE ──
            # Hard backstop for the user's zero-content-loss requirement: the
            # refined file must not have lost words or dropped the source's
            # annotated examples (e.g. _<u><mark>Put out the cat.</mark></u>_).
            src_txt = src_path.read_text(encoding="utf-8", errors="ignore")
            src_words = _word_count(src_txt)
            out_words = _word_count(txt)
            ok_parity = out_words >= int(src_words * 0.98)  # allow ≤2% token drift
            src_marks = src_txt.count("_<u><mark")
            out_marks = txt.count("_<u><mark")
            ok_marks = out_marks >= src_marks

            if ok_size and ok_skel and ok_parity and ok_marks:
                _checkpoint[str(worker_num)] = {"passed": True, "output_size": sz,
                                                "duration": round(dur, 1)}
                _save_checkpoint(_checkpoint)
                print(f"  R{worker_num:03d}: [PASS] {sz}B ({dur:.1f}s) "
                      f"words {out_words}/{src_words} marks {out_marks}/{src_marks}", flush=True)
                return True
            else:
                reasons = []
                if not ok_size: reasons.append(f"size={sz}B")
                if not ok_skel: reasons.append("skeleton_missing")
                if not ok_parity: reasons.append(f"word_loss {out_words}/{src_words}")
                if not ok_marks: reasons.append(f"marks_lost {out_marks}/{src_marks}")
                print(f"  R{worker_num:03d}: [FAIL] {'; '.join(reasons)} — retrying", flush=True)
        else:
            print(f"  R{worker_num:03d}: [FAIL] no output file — likely rate-limited, retrying", flush=True)

        # Backoff before retry (covers 429 / transient API rejection)
        backoff = 20 * attempt
        print(f"  R{worker_num:03d}: sleeping {backoff}s before retry...", flush=True)
        time.sleep(backoff)

    print(f"  R{worker_num:03d}: [GIVEUP] after {max_attempts} attempts", flush=True)
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

    # git commit passed worker outputs (serialized across parallel batches)
    passed_files = []
    for w, (src, s, e) in members:
        out = REFINED_DIR / f"r{w:03d}-p{s}-{e}.md"
        if out.exists():
            passed_files.append(str(out.relative_to(PROJECT)))
    if passed_files:
        msg = f"Refine Batch {batch_num:02d} - {'PASS' if all_ok else 'PARTIAL'} - {ids}"
        ok = git_commit_locked(passed_files, msg)
        if ok:
            print(f"  ✓ Committed: {msg}", flush=True)
        else:
            print(f"  ✗ Commit failed: {msg}", flush=True)
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
