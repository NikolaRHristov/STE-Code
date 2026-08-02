#!/usr/bin/env python3
"""Phase E Orchestrator — STE-Code gap-fill extensions (markdown-first, gated).

Generates code-domain entries to fill documented gaps between ASD-STE100
(aerospace) and the code-documentation domain: approved verbs, adjectives,
noun-category examples, verb-category examples, code anti-patterns, and domain
extensions.

DESIGN (post-RCE-artifact cleanup): workers emit MARKDOWN only — never JSON.
JSON is a derived artifact, produced deterministically by md_to_json.py from the
markdown (no LLM, no eval/exec, no RCE surface). This matches the rest of the
pipeline, which is markdown end-to-end (refined/, adapted/, extracted/).

Orchestration mirrors the other stages (checkpoint + per-area git commit +
crash-safe resume). The generation is an LLM creative task; acceptance is
DETERMINISTIC (verify_extensions.py): markdown structure, required fields,
definition length, no fabrication markers, unique terms, STE/non-STE pair
quality. After a markdown area passes, md_to_json.py derives <area>.json.

Usage:
  python3 extend_batch.py [area] [--resume] [--dry-run]
  python3 extend_batch.py verbs
  STE_MODEL=tencent/hy3:free python3 extend_batch.py

Model: STE_MODEL env var (default tencent/hy3:free).
"""
from __future__ import annotations

import os
import sys
import re
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
from ste_paths import venv_python  # noqa: E402
from ste_io import write_text, mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
from ste_runtime import resolve as _resolve_runtime  # noqa: E402
RT = _resolve_runtime(__file__)
EXT_DIR = PROJECT / "ste-code" / "extensions"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "extend-checkpoint.json"
MD_TO_JSON = Path(__file__).resolve().parent / "md_to_json.py"

MODEL = CFG.model
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 600

# Gap areas: name -> (markdown file, target count, worker entry cap).
AREAS = {
    "verbs": ("verbs.md", 15, 20),
    "adjectives": ("adjectives.md", 19, 20),
    "nouns": ("nouns.md", 86, 20),
    "verb-examples": ("verb-examples.md", 20, 20),
    "anti-patterns": ("anti-patterns.md", 10, 20),
    "domains": ("domains.md", 47, 20),
}

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)


def _skill_text():
    import sys as _sys
    _sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
    from templater import lib_import
    m = lib_import("skill_prompt")
    return m.skill_section("extension-worker")


def _build_prompt(area, out_path, count):
    wrapper = TPL.render("extend-area", area=area, count=count, out_path=out_path)
    return wrapper + _skill_text() + (
        "\n\nOutput ONLY the markdown file. No JSON, no code fences around the file.\n"
    )


# ── checkpoint ───────────────────────────────────────────────────────────────
def _load_checkpoint():
    from ste_checkpoint import load
    return load(CHECKPOINT_PATH)

def _save_checkpoint(ckpt):
    from ste_checkpoint import save
    save(CHECKPOINT_PATH, ckpt)

_checkpoint = _load_checkpoint()


def git_commit_locked(files, msg):
    lock = STATE_DIR / "extend-git-lock"
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


def _gate_ok(md_path: Path) -> tuple[bool, str]:
    """Deterministic Gate 1-6 on the markdown area file (no LLM, no JSON parse)."""
    if not md_path.exists():
        return False, "file missing"
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    if not text.strip():
        return False, "empty"
    # Gate 4: fabrication markers
    if re.search(r"TODO|TBD|FIXME|placeholder|<\s*PLACEHOLDER\s*>|\?\?\?", text, re.I):
        return False, "Gate4 fabrication marker"
    entries = re.split(r"\n### ", text)
    entries = [e for e in entries if e.strip()]
    if not entries:
        return False, "no '### ' entries found"
    seen = set()
    for e in entries:
        # Gate 2/3: required fields + definition length
        if "**definition**:" in e:
            m = re.search(r"\*\*definition\*\*:\s*(.+)", e)
            if m and len(m.group(1).split()) < 10:
                return False, "Gate3 definition < 10 words"
        # Gate 6: verb/adjective need an avoided synonym in non_ste
        if "**type**: verb" in e or "**type**: adjective" in e:
            ns = re.search(r"\*\*code_example_non_ste\*\*:\s*(.+)", e)
            if ns and not re.search(r"utilize|leverage|employ|commence|terminate|initiate|bootstrap",
                                     ns.group(1), re.I):
                return False, "Gate6 non-STE lacks avoided synonym"
        # Gate 5: unique key per entry
        km = re.search(r"^([^\n]+)", e.strip())
        key = km.group(1).strip() if km else e[:40]
        if key in seen:
            return False, f"Gate5 duplicate entry '{key}'"
        seen.add(key)
    return True, f"ok ({len(entries)} entries)"


def run_area(area):
    fname, target, cap = AREAS[area]
    md_path = EXT_DIR / fname
    mkdir(EXT_DIR)
    prompt = _build_prompt(area, str(md_path), cap)
    tmp = PROJECT / ".agents" / "tmp"
    mkdir(tmp)
    pf = tmp / f"extend-{area}.txt"
    write_text(pf, prompt)

    for attempt in range(1, 4):
        print(f"  EXT {area}: launching worker (attempt {attempt})...", flush=True)
        env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "180", "STE_MODEL": MODEL}
        try:
            r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                               capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
                               env=env, cwd=str(PROJECT))
            if r.stderr and ("error" in r.stderr.lower() or "traceback" in r.stderr.lower()):
                print(f"  EXT {area}: [stderr] {r.stderr[:200]}", flush=True)
        except subprocess.TimeoutExpired:
            print(f"  EXT {area}: [TIMEOUT]", flush=True)
            return False
        ok, why = _gate_ok(md_path)
        if ok:
            _checkpoint[area] = {"passed": True, "n": len(re.split(r'\n### ', md_path.read_text()))}
            _save_checkpoint(_checkpoint)
            # Derive JSON deterministically (no LLM) — the ONLY JSON produced.
            try:
                subprocess.run([VENV_PYTHON, str(MD_TO_JSON), str(md_path)],
                               capture_output=True, text=True, cwd=str(PROJECT), check=True)
            except subprocess.CalledProcessError as ex:
                print(f"  EXT {area}: [md_to_json FAIL] {ex.stderr[:200]}", flush=True)
                return False
            print(f"  EXT {area}: [PASS] {why}", flush=True)
            return True
        print(f"  EXT {area}: [GATE FAIL] {why} — retry", flush=True)
        time.sleep(10 * attempt)
    print(f"  EXT {area}: [GIVEUP]", flush=True)
    return False


def main():
    resume = "--resume" in sys.argv
    dry = "--dry-run" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    areas = [args[0]] if args else list(AREAS.keys())

    print("STE-Code Extension (gap-fill) Pipeline — markdown-first", flush=True)
    print(f"Model: {MODEL} | areas: {', '.join(areas)}", flush=True)

    if dry:
        for a in areas:
            fn, tgt, cap = AREAS[a]
            print(f"  [dry-run] area={a} -> ste-code/extensions/{fn} (+ derived {fn[:-3]}.json)")
        return

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    all_ok = True
    for area in areas:
        if area not in AREAS:
            print(f"  unknown area: {area} (choose from {', '.join(AREAS)})")
            continue
        if resume and _checkpoint.get(area, {}).get("passed"):
            print(f"  EXT {area}: ✓ checkpoint skip", flush=True)
            continue
        print(f"\n{'='*60}\nExtension area: {area}\n{'='*60}", flush=True)
        if not run_area(area):
            all_ok = False
        else:
            files = [str((EXT_DIR / AREAS[area][0]).relative_to(PROJECT)),
                     str((EXT_DIR / (AREAS[area][0][:-3] + ".json")).relative_to(PROJECT))]
            msg = f"Extension batch: {area} - PASS"
            if git_commit_locked(files, msg):
                print(f"  ✓ committed {msg}", flush=True)
            else:
                print(f"  ✗ commit failed {msg}", flush=True)

    print(f"\n{'='*60}\nExtension done. Areas passed: "
          f"{sum(1 for a in areas if _checkpoint.get(a,{}).get('passed'))}/{len(areas)}\n{'='*60}",
          flush=True)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
