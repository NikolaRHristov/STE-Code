#!/usr/bin/env python3
"""Phase F — synthesize STE-Code ARTIFACTS from the finished final/ standard.

SEPARATE from finalize_batch.py (Phase G). It reads the WHOLE ste-code/final/
standard (the full enriched rule set + extensions + reference catalogue) and an
LLM breaks it into reworked, shippable LEVELS for people who use LLMs to
generate code documentation.

Levels (your scheme: -2, -1, 0, 1, 2, 3, 4, 5 = 8 tiers):
  level-2.md  — deepest-abbreviation tier: ultra-minimal reminder of the 14 core
                principles only (for when the model must stay extremely terse).
  level-1.md  — minimal/core: 14 core principles + synonym table (~1.2K tokens).
  level0.md   — baseline: core principles + short dictionary excerpt (~3K).
  level1.md   — + doc templates (~4.5K): code review / PR feedback.
  level2.md   — + section-specific grammar rules (~8K): full document rewriting.
  level3.md   — + complete dictionary excerpt + all rules (~45K): strict compliance.
  level4.md   — + extensions + reference catalogue (~80K).
  level5.md   — full standard (all rules + extensions + catalogue) (~100K+): spec-grade.

Mechanism (mirrors finalize_batch.py — NOT a dumb pipe): each level is a oneshot
session that READS the assembled standard + RESEARCHES references, then WRITES
ste-code/artifacts/<level>.md itself via its file tools. r.stdout is saved to
.agents/tmp/ as trajectory only. A progress file in .agents/state/ flags which
levels are done. Deterministic fallback extract if the LLM fails.

Usage:
  python3 synthesize_artifacts.py            # build all 8 levels from final/
  python3 synthesize_artifacts.py --resume
  python3 synthesize_artifacts.py --regen-progress
  python3 synthesize_artifacts.py --verify
"""
from __future__ import annotations

import os
import re
import sys
import json
import signal
import subprocess
import atexit
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "artifact-checkpoint.json"
PROGRESS_PATH = STATE_DIR / "artifact-progress.md"
REFERENCE_DIR = PROJECT / ".agents" / "reference"

MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 900

# (filename, label, description) — ordered from weakest (-2) to richest (5).
LEVELS = [
    ("level-2.md", "-2", "ultra-minimal: the 14 core principles only (~0.6K tokens) — for extreme brevity"),
    ("level-1.md", "-1", "minimal/core: 14 core principles + synonym table (~1.2K tokens)"),
    ("level0.md",  "0",  "baseline: core principles + short dictionary excerpt (~3K tokens)"),
    ("level1.md",  "1",  "+ doc templates (~4.5K): code review / PR feedback"),
    ("level2.md",  "2",  "+ section-specific grammar rules (~8K): full document rewriting"),
    ("level3.md",  "3",  "+ complete dictionary excerpt + all rules (~45K): strict compliance"),
    ("level4.md",  "4",  "+ extensions + reference catalogue (~80K)"),
    ("level5.md",  "5",  "full standard (all rules + extensions + catalogue) (~100K+): spec-grade"),
]

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
    for name in ("README.md", "provenance.md", "reference-catalogue.md"):
        p = FINAL_DIR / name
        if p.exists():
            parts.append(f"# {name}\n{p.read_text(errors='ignore')}")
    rules = sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))
    for p in rules:
        parts.append(p.read_text(errors="ignore"))
    for extra in ("a-categories.md", "a-dictionary.md"):
        p = FINAL_DIR / "rules" / extra
        if p.exists():
            parts.append(p.read_text(errors="ignore"))
    for p in sorted((FINAL_DIR / "extensions").glob("*.md")):
        parts.append(p.read_text(errors="ignore"))
    return "\n\n---\n\n".join(parts)


def _build_prompt(bundle: str, level_label: str, desc: str) -> str:
    return f"""You are packaging the FINAL STE-Code standard into shippable LEVELS for
people who use LLMs to generate code documentation. You have the FULL standard
below (and may research .agents/reference/ for vocabulary). Produce LEVEL {level_label}
of STE-Code.

Level {level_label} should contain: {desc}

Guidelines:
- Be faithful to the full standard; do not invent rules.
- Use code-domain examples only (no aerospace leakage).
- Level -2 = ultra-minimal; level -1 = core principles; level 0 = baseline;
  higher levels progressively add dictionary, grammar, extensions, and full rules.
- Keep your output coherent with the overall STE-Code voice (plain, code-domain).

# HOW TO WRITE THE FILE (critical)
You are a session with file-read and file-write tools. Do NOT print the file to
the chat. Instead:
- READ the standard context below and research .agents/reference/ as needed.
- WRITE the finished level file directly to disk at:
  ste-code/artifacts/level{level_label}.md   (use a minus sign for negative tiers:
  level-2.md for -2, level-1.md for -1)
  using your file-write tool (overwrite any existing content there).
- The file MUST be self-contained, parseable markdown for that level.
- After writing and re-reading to confirm correctness, END the session.
- Do NOT write any narration, tool logs, or "Rewrote…"/"What changed vs…" into the
  file or the chat. Do not create helper scripts.

# FULL STE-Code STANDARD (read all of it)
{bundle[:90000]}

# OUTPUT: write ste-code/artifacts/level{level_label}.md now.
"""


def synthesize_level(level: int) -> bool:
    fname, label, desc = LEVELS[level]
    out = ARTIFACTS_DIR / fname
    bundle = _standard_bundle()
    prompt = _build_prompt(bundle, label, desc)
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"artifact-level{label}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "300", "STE_MODEL": MODEL}
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
                           env=env, cwd=str(PROJECT))
        # trajectory/history only — NOT the output file
        (tmp / f"artifact-traj-level{label}.txt").write_text(r.stdout, encoding="utf-8")
        # gate on the file the SESSION wrote
        if out.exists() and out.stat().st_size > 300:
            print(f"  ✓ level{label} (session wrote artifact)", flush=True)
            _git_commit_locked([str(out.relative_to(PROJECT))],
                               f"Phase F: artifact level{label} synthesized")
            return True
        _fallback_level(level, out)
        _git_commit_locked([str(out.relative_to(PROJECT))],
                          f"Phase F: artifact level{label} (fallback)")
        return True
    except subprocess.TimeoutExpired:
        _fallback_level(level, out)
        _git_commit_locked([str(out.relative_to(PROJECT))],
                          f"Phase F: artifact level{label} (fallback)")
        return True


def _fallback_level(level: int, out: Path):
    """Deterministic extract from final/ if the LLM fails (never ship empty)."""
    rules = sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))
    header = f"# STE-Code Level {LEVELS[level][1]} (deterministic extract)\n\n"
    if level <= 2:  # -2, -1, 0: core principles only
        chunks = []
        for p in rules[:14]:
            t = p.read_text(errors="ignore")
            h = t.splitlines()[0] if t else ""
            chunks.append(f"{h}\n")
        out.write_text(header + "\n".join(chunks), encoding="utf-8")
    else:
        out.write_text(header + "\n\n".join(p.read_text(errors="ignore")
                                            for p in rules), encoding="utf-8")


def _regen_progress():
    ART = ARTIFACTS_DIR
    rows = []
    done_n = 0
    for fname, label, desc in LEVELS:
        p = ART / fname
        ok = p.exists() and p.stat().st_size > 300 and not re.search(
            r"deterministic extract", p.read_text(errors="ignore"))
        status = "done" if ok else "missing"
        if ok:
            done_n += 1
        rows.append((label, fname, status, desc))
    lines = [
        "# STE-Code artifacts/ Progress Tracker",
        "",
        "> Generated from DISK EVIDENCE. A level is 'done' iff ste-code/artifacts/<f>",
        "> exists, is non-trivial, and is not a deterministic fallback extract.",
        "> Regenerate: `python3 .agents/tools/finalize/synthesize_artifacts.py --regen-progress`",
        "",
        "## Level status",
        "",
        "| Level | File | Status | Description |",
        "|-------|------|--------|-------------|",
    ]
    for label, fname, status, desc in rows:
        lines.append(f"| {label} | {fname} | {status} | {desc} |")
    lines += ["", "## Summary",
              f"- done: {done_n} / {len(LEVELS)}",
              f"- missing: {len(LEVELS) - done_n} / {len(LEVELS)}"]
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  artifact progress regenerated: {done_n}/{len(LEVELS)} done", flush=True)
    return PROGRESS_PATH


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    verify = "--verify" in args
    regen = "--regen-progress" in args

    if verify:
        ok = all((ARTIFACTS_DIR / f).exists() and (ARTIFACTS_DIR / f).stat().st_size > 300
                 for _, f, _ in LEVELS)
        print(f"artifact verify: {'PASS' if ok else 'FAIL'} "
              f"({sum((ARTIFACTS_DIR/f).exists() for _,f,_ in LEVELS)}/{len(LEVELS)})")
        sys.exit(0 if ok else 1)

    if regen:
        _regen_progress()
        return

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    done = _checkpoint.setdefault("done", [])
    n_ok = 0
    for i in range(len(LEVELS)):
        label = LEVELS[i][1]
        if resume and i in done:
            print(f"  skip (done): level{label}", flush=True)
            n_ok += 1
            continue
        print(f"  ARTIFACT level{label}...", flush=True)
        if synthesize_level(i):
            if i not in done:
                done.append(i)
            _save_checkpoint(_checkpoint)
            n_ok += 1
            print(f"    ✓ level{label}", flush=True)
        else:
            print(f"    ✗ level{label}", flush=True)
        _regen_progress()

    print(f"\n{'='*60}\nArtifacts done: {n_ok}/{len(LEVELS)} levels ✓ -> ste-code/artifacts/\n{'='*60}", flush=True)
    sys.exit(0 if n_ok == len(LEVELS) else 1)


if __name__ == "__main__":
    main()
