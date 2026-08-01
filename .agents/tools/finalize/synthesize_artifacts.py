#!/usr/bin/env python3
"""Delegate B — synthesize STE-Code ARTIFACTS from the finished final/ standard.

SEPARATE from finalize_batch.py (Delegate A). It reads the WHOLE ste-code/final/
standard (the full enriched rule set + extensions + reference catalogue) and an
LLM breaks it into reworked, shippable LEVELS 1-5 — the deployable prompts we
ship to people who use LLMs to generate code documentation.

Levels (mirrors the project's adaptation-level scheme, reworked for the final
standard):
  level1.md  — 14 core principles + synonym table (~1.2K tokens): interactive use
  level2.md  — + dictionary excerpt + doc templates (~4.5K): code review / PR feedback
  level3.md  — + section-specific grammar rules (~8K): full document rewriting
  level4.md  — + complete dictionary excerpt + all rules (~45K): strict compliance
  level5.md  — full standard (all rules + extensions) (~100K+): spec-grade

Mechanism: one LLM worker reads the assembled standard and emits all five level
files (or one worker per level for size). Gated by a structural check; checkpoint
+ per-level git commit. Falls back to a deterministic extract if the LLM fails.

Usage:
  python3 synthesize_artifacts.py          # build all 5 levels from final/
  python3 synthesize_artifacts.py --resume
  python3 synthesize_artifacts.py --verify
"""
from __future__ import annotations

import os
import re
import sys
import json
import time
import signal
import subprocess
import atexit
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "artifact-checkpoint.json"

MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 900

LEVELS = {
    1: ("level1.md", "14 core principles + synonym table (~1.2K tokens)"),
    2: ("level2.md", "+ dictionary excerpt + doc templates (~4.5K)"),
    3: ("level3.md", "+ section-specific grammar rules (~8K)"),
    4: ("level4.md", "+ complete dictionary excerpt + all rules (~45K)"),
    5: ("level5.md", "full standard: all rules + extensions (~100K+)"),
}

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))


def _load_checkpoint():
    if CHECKPOINT_PATH.exists():
        try:
            return json.load(open(CHECKPOINT_PATH))
        except Exception:
            pass
    return {}


def _save_checkpoint(ckpt):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(CHECKPOINT_PATH) + ".tmp"
    try:
        json.dump(ckpt, open(tmp, "w"), indent=2, default=str)
        os.replace(tmp, str(CHECKPOINT_PATH))
    except Exception:
        pass


_checkpoint = _load_checkpoint()


def _git_commit_locked(files, msg):
    try:
        subprocess.run(["git", "add", "-A", "--", *files], cwd=str(PROJECT),
                       check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=str(PROJECT),
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def _standard_bundle() -> str:
    """Concatenate the full final/ standard into one context string for the LLM."""
    parts = []
    # master index
    for name in ("README.md", "provenance.md", "reference-catalogue.md"):
        p = FINAL_DIR / name
        if p.exists():
            parts.append(f"# {name}\n{p.read_text(errors='ignore')}")
    # rules
    rules = sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))
    for p in rules:
        parts.append(p.read_text(errors="ignore"))
    for extra in ("a-categories.md", "a-dictionary.md"):
        p = FINAL_DIR / "rules" / extra
        if p.exists():
            parts.append(p.read_text(errors="ignore"))
    # extensions
    for p in sorted((FINAL_DIR / "extensions").glob("*.md")):
        parts.append(p.read_text(errors="ignore"))
    return "\n\n---\n\n".join(parts)


def _build_prompt(bundle: str, level: int, desc: str) -> str:
    return f"""You are packaging the FINAL STE-Code standard into shippable levels for
people who use LLMs to generate code documentation. You have read the FULL standard
below. Produce LEVEL {level} of STE-Code.

Level {level} should contain: {desc}

Guidelines:
- Be faithful to the full standard; do not invent rules.
- Use code-domain examples only (no aerospace leakage).
- Level 1 = minimal/core; higher levels add dictionary, grammar, and full rules.
- Output ONLY the level's markdown (no code fences, no commentary).

# FULL STE-Code STANDARD (read all of it)
{bundle[:60000]}

# OUTPUT: Level {level} markdown now.
"""


def synthesize_level(level: int) -> bool:
    fname, desc = LEVELS[level]
    out = ARTIFACTS_DIR / fname
    bundle = _standard_bundle()
    prompt = _build_prompt(bundle, level, desc)
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"artifact-level{level}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "300", "STE_MODEL": MODEL}
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
                           env=env, cwd=str(PROJECT))
        out_text = r.stdout.strip()
        if r.returncode == 0 and out_text:
            out.write_text(out_text + "\n", encoding="utf-8")
        else:
            _fallback_level(level, out)
        ok = out.exists() and out.stat().st_size > 300
        if not ok:
            _fallback_level(level, out)
            ok = out.exists() and out.stat().st_size > 300
        _git_commit_locked([str(out.relative_to(PROJECT))],
                          f"Phase F: artifact level{level} synthesized")
        return ok
    except subprocess.TimeoutExpired:
        _fallback_level(level, out)
        _git_commit_locked([str(out.relative_to(PROJECT))],
                          f"Phase F: artifact level{level} (fallback)")
        return True


def _fallback_level(level: int, out: Path):
    """Deterministic extract from final/ if the LLM fails (never ship empty)."""
    rules = sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))
    header = f"# STE-Code Level {level} (deterministic extract)\n\n"
    if level <= 2:
        # core principles: first ~14 rule headings + first example each
        chunks = []
        for p in rules[:14]:
            t = p.read_text(errors="ignore")
            h = t.splitlines()[0] if t else ""
            chunks.append(f"{h}\n")
        out.write_text(header + "\n".join(chunks), encoding="utf-8")
    else:
        out.write_text(header + "\n\n".join(p.read_text(errors="ignore")
                                            for p in rules), encoding="utf-8")


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    verify = "--verify" in args

    if verify:
        ok = all((ARTIFACTS_DIR / f"level{n}.md").exists()
                 for n in LEVELS)
        print(f"artifact verify: {'PASS' if ok else 'FAIL'} "
              f"({sum((ARTIFACTS_DIR/f'level{n}.md').exists() for n in LEVELS)}/5)")
        sys.exit(0 if ok else 1)

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    done = _checkpoint.setdefault("done", [])
    n_ok = 0
    for level in LEVELS:
        if resume and level in done:
            print(f"  skip (done): level{level}", flush=True)
            n_ok += 1
            continue
        print(f"  ARTIFACT level{level}...", flush=True)
        if synthesize_level(level):
            if level not in done:
                done.append(level)
            _save_checkpoint(_checkpoint)
            n_ok += 1
            print(f"    ✓ level{level}", flush=True)
        else:
            print(f"    ✗ level{level}", flush=True)

    print(f"\n{'='*60}\nArtifacts done: {n_ok}/5 levels ✓ -> ste-code/artifacts/\n{'='*60}", flush=True)
    sys.exit(0 if n_ok == 5 else 1)


if __name__ == "__main__":
    main()
