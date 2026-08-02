#!/usr/bin/env python3
"""Phase B1 Orchestrator — continuation / redo refinement of refined pages.

B1 continues refinement where a prior worker left off: it re-processes specific
refined pages that a verifier flagged as truncated, orphaned, or mid-batch
continuation text. Unlike the other stages, B1 writes into ste-code/refined/ —
the SAME directory the Refinement agent owns. To avoid two sessions colliding on
that directory, this orchestrator NEVER picks targets on its own: it requires an
explicit --queue FILE listing the refined page paths to redo. The queue is
produced by verify-continuation.py (read-only scan of refined/) and reviewed by a
human/session before B1 runs.

Mirrors the other stages' discipline: checkpoint + per-item git commit +
crash-safe resume + a content gate (the refined page must not be truncated and
must carry the canonical page header). Embeds the continuation SKILL so editing
the SKILL changes worker behavior.

Usage:
  python3 verify-continuation.py              # read-only scan -> queue JSON
  python3 continue_batch.py --queue Q.json    # redo listed pages
  python3 continue_batch.py --queue Q.json --resume
Do NOT run while the Refinement agent is actively writing refined/.
"""
from __future__ import annotations

import os
import sys
import json
import time
import signal
import subprocess
import atexit
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
REFINED_DIR = PROJECT / "ste-code" / "refined"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "continue-checkpoint.json"

MODEL = CFG.model
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 600

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)


def _skill_text():
    import sys as _sys
    _sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
    from templater import lib_import
    m = lib_import("skill_prompt")
    return m.skill_section("continuation")


def _build_prompt(target_rel: str) -> str:
    wrapper = TPL.render("continue-worker", target=target_rel)
    return wrapper + _skill_text() + "\n\nRewrite ONLY the file above. No commentary outside it.\n"


def _load_checkpoint():
    from ste_checkpoint import load
    return load(CHECKPOINT_PATH)

def _save_checkpoint(ckpt):
    from ste_checkpoint import save
    save(CHECKPOINT_PATH, ckpt)

_checkpoint = _load_checkpoint()


def git_commit_locked(files, msg):
    lock = STATE_DIR / "continue-git-lock"
    deadline = time.time() + 120
    while time.time() < deadline:
        try:
            lock.mkdir(exist_ok=False)
            break
        except FileExistsError:
            time.sleep(1)
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


def _gate_ok(target: Path) -> tuple[bool, str]:
    if not target.exists():
        return False, "missing after worker"
    text = target.read_text(encoding="utf-8", errors="ignore")
    if len(text) < 200:
        return False, f"too small ({len(text)}B) — likely truncated"
    if "truncat" in text.lower().split("\n")[0:3] and "continued" not in text.lower():
        return False, "still looks truncated"
    if not text.lstrip().startswith("#"):
        return False, "missing page header"
    return True, "ok"


def run_one(target_rel: str) -> bool:
    target = PROJECT / target_rel
    if not target.exists():
        # Fallback: queue stored a bare name; resolve under refined/.
        target = REFINED_DIR / Path(target_rel).name
    if not target.exists():
        print(f"  B1 {target_rel}: target not found", flush=True)
        return False
    prompt = _build_prompt(str(target.relative_to(PROJECT)))
    tmp = PROJECT / ".agents" / "tmp"
    mkdir(tmp)
    pf = tmp / "continue-prompt.txt"
    write_text(pf, prompt)
    for attempt in range(1, 4):
        print(f"  B1 {target_rel}: redo (attempt {attempt})...", flush=True)
        env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "180", "STE_MODEL": MODEL}
        try:
            r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                               capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
                               env=env, cwd=str(PROJECT))
            if r.stderr and ("error" in r.stderr.lower() or "traceback" in r.stderr.lower()):
                print(f"  B1: [stderr] {r.stderr[:200]}", flush=True)
        except subprocess.TimeoutExpired:
            print(f"  B1 {target_rel}: [TIMEOUT]", flush=True)
            return False
        ok, why = _gate_ok(target)
        if ok:
            _checkpoint[target_rel] = {"passed": True}
            _save_checkpoint(_checkpoint)
            print(f"  B1 {target_rel}: [PASS] {why}", flush=True)
            return True
        print(f"  B1 {target_rel}: [GATE FAIL] {why} — retry", flush=True)
        time.sleep(10 * attempt)
    print(f"  B1 {target_rel}: [GIVEUP]", flush=True)
    return False


def main():
    argv = sys.argv[1:]
    resume = "--resume" in argv
    queue_args = [a for a in argv if a.startswith("--queue")]
    if not queue_args:
        print("Usage: continue_batch.py --queue QUEUE.json [--resume]", flush=True)
        print("The queue must be produced by verify-continuation.py and reviewed "
              "before running, so B1 never overwrites the Refinement agent's live "
              "refined/ output unilaterally.", flush=True)
        sys.exit(2)
    queue_path = Path(queue_args[0].split("=", 1)[1] if "=" in queue_args[0] else argv[argv.index("--queue") + 1])
    if not queue_path.exists():
        print(f"Queue not found: {queue_path}", flush=True)
        sys.exit(2)
    queue = json.loads(queue_path.read_text(encoding="utf-8"))
    if not isinstance(queue, list) or not queue:
        print("Queue must be a non-empty JSON list of refined-page paths", flush=True)
        sys.exit(2)

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    print(f"STE-Code B1 continuation — {len(queue)} page(s) to redo", flush=True)
    all_ok = True
    for target_rel in queue:
        if resume and _checkpoint.get(target_rel, {}).get("passed"):
            print(f"  B1 {target_rel}: ✓ checkpoint skip", flush=True)
            continue
        if not run_one(target_rel):
            all_ok = False
        else:
            msg = f"B1 continuation: {Path(target_rel).name} - PASS"
            if git_commit_locked([target_rel], msg):
                print(f"  ✓ committed {msg}", flush=True)
            else:
                print(f"  ✗ commit failed {msg}", flush=True)
    print(f"\n{'='*60}\nB1 done. Passed {sum(1 for t in queue if _checkpoint.get(t,{}).get('passed'))}/{len(queue)}\n{'='*60}", flush=True)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
