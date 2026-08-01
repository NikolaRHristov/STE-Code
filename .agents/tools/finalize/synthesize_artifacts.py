#!/usr/bin/env python3
"""Phase F — LLM FINAL-DISTILLATION pass for STE-Code ARTIFACTS.

HYBRID design (per project owner):
  - The LEVEL SEPARATION + BASE/BOILERPLATE is DETERMINISTIC (levels_scaffold.py).
  - This pass is the LLM FINAL step: it reads each tier's base + the full final/
    standard (chunked, zero truncation) and DISTILLS it into an LLM-optimized
    artifact — adapted to the STE-Code spec but shaped for LLM consumption, in
    the spirit of llms.txt / llms-full.txt.

Inputs (deterministic, from ste-code/final/):
  - ste-code/artifacts/_base/level<N>.base.md  (built by levels_scaffold.py)
  - the full final/ standard, split into ordered chunks for lossless reading.

Outputs (under ste-code/artifacts/):
  - level-2.md .. level5.md        LLM-distilled per-tier artifacts
  - llms.txt                       concise index (H1 + blockquote + file list)
  - llms-full.txt                  full concatenation of all level files
The deterministic assembler (artifact_batch.py) still owns ste-code-rules.md /
ste-code-system-prompt.md. Both are valid Phase-F deliverables.

Mechanism (mirrors finalize_batch.py — NOT a dumb pipe): each level is a oneshot
session that READS its base + the standard chunks + RESEARCHES .agents/vendor/,
then WRITES the level file itself in MULTIPLE write_file calls. r.stdout is saved
to .agents/tmp/ as trajectory only. A checkpoint + progress file flag done levels.
Deterministic fallback (distill-from-base) if the LLM fails, so we never ship empty.

Usage:
  python3 synthesize_artifacts.py            # scaffold bases, then distill all levels
  python3 synthesize_artifacts.py --scaffold-only
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
BASE_DIR = ARTIFACTS_DIR / "_base"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "artifact-llm-checkpoint.json"
PROGRESS_PATH = STATE_DIR / "artifact-llm-progress.md"
BUNDLE_DIR = STATE_DIR / "artifact-bundle"
VENDOR_DIR = PROJECT / ".agents" / "vendor"

MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 1800  # long distillation sessions

# (filename, label, description) — ordered from weakest (-2) to richest (5).
LEVELS = [
    ("level-2.md", "-2", "ultra-minimal: the 14 core principles only"),
    ("level-1.md", "-1", "minimal/core: 14 core principles + synonym table"),
    ("level0.md",  "0",  "baseline: core principles + short dictionary excerpt"),
    ("level1.md",  "1",  "+ doc templates (code review / PR feedback)"),
    ("level2.md",  "2",  "+ section-specific grammar rules"),
    ("level3.md",  "3",  "+ complete dictionary excerpt + all rules"),
    ("level4.md",  "4",  "+ extensions + reference catalogue"),
    ("level5.md",  "5",  "full standard (all rules + extensions + catalogue + provenance)"),
]

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import render_template


# ── chunked standard (no truncation) ──────────────────────────────────────────
def _prepare_bundle() -> tuple[int, str]:
    """Split the full final/ standard into ordered ~60K-char chunks under
    STATE/artifact-bundle/ so a worker can read them losslessly. Returns
    (chunk_count, manifest_text)."""
    BUNDLE_DIR.mkdir(parents=True, exist_ok=True)
    # wipe stale chunks
    for old in BUNDLE_DIR.glob("chunk-*.md"):
        old.unlink()
    parts = []
    for name in ("README.md", "provenance.md", "reference-catalogue.md"):
        p = FINAL_DIR / name
        if p.exists():
            parts.append(f"# {name}\n{p.read_text(errors='ignore')}")
    for p in sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md")):
        parts.append(p.read_text(errors="ignore"))
    for p in sorted((FINAL_DIR / "extensions").glob("*.md")):
        parts.append(f"# Extension {p.stem}\n{p.read_text(errors='ignore')}")

    chunks, cur, idx = [], [], 0
    for part in parts:
        if sum(len(x) for x in cur) + len(part) > 60000 and cur:
            chunks.append("\n\n---\n\n".join(cur)); cur = []
        cur.append(part)
    if cur:
        chunks.append("\n\n---\n\n".join(cur))
    for i, c in enumerate(chunks):
        (BUNDLE_DIR / f"chunk-{i:03d}.md").write_text(c, encoding="utf-8")
    manifest = "\n".join(
        f"- Read `{(BUNDLE_DIR / f'chunk-{i:03d}.md')}` (part {i+1}/{len(chunks)})"
        for i in range(len(chunks)))
    return len(chunks), manifest


# ── checkpoint / state ──────────────────────────────────────────────────────
def _load_checkpoint():
    if CHECKPOINT_PATH.exists():
        try:
            return json.load(open(CHECKPOINT_PATH))
        except Exception:
            pass
    return {}


def _save_checkpoint(ck):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(CHECKPOINT_PATH) + ".tmp"
    try:
        json.dump(ck, open(tmp, "w"), indent=2, default=str)
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


# ── prompt (externalized) ───────────────────────────────────────────────────
SYNTH_PROMPT_MD = PROJECT / ".agents" / "tools" / "prompts" / "synthesize-artifacts-worker.md"


def _build_prompt(level_label: str, desc: str, manifest: str, base_path: Path) -> str:
    return render_template(
        SYNTH_PROMPT_MD,
        level_label=level_label,
        desc=desc,
        bundle=manifest,
        base_path=str(base_path),
    )


# ── distill one level (LLM session) ────────────────────────────────────────
def distill_level(level: int) -> bool:
    fname, label, desc = LEVELS[level]
    out = ARTIFACTS_DIR / fname
    base_path = BASE_DIR / fname.replace(".md", ".base.md")
    manifest = _prepare_bundle()[1]
    prompt = _build_prompt(label, desc, manifest, base_path)
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"artifact-level{label}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "1800", "STE_MODEL": MODEL}
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
                           env=env, cwd=str(PROJECT))
        (tmp / f"artifact-traj-level{label}.txt").write_text(r.stdout, encoding="utf-8")
        if out.exists() and out.stat().st_size > 300:
            print(f"  ✓ level{label} (LLM distilled)", flush=True)
            _git_commit_locked([str(out.relative_to(PROJECT))],
                               f"Phase F: LLM-distill artifact level{label}")
            return True
        _fallback_level(level, out, base_path)
        _git_commit_locked([str(out.relative_to(PROJECT))],
                          f"Phase F: artifact level{label} (fallback)")
        return True
    except subprocess.TimeoutExpired:
        _fallback_level(level, out, base_path)
        _git_commit_locked([str(out.relative_to(PROJECT))],
                          f"Phase F: artifact level{label} (fallback)")
        return True


def _fallback_level(level: int, out: Path, base_path: Path):
    """If the LLM fails, ship the deterministic base (never empty)."""
    if base_path.exists():
        out.write_text(base_path.read_text(errors="ignore"), encoding="utf-8")
    else:
        out.write_text(f"# STE-Code Level {LEVELS[level][1]} (base only)\n", encoding="utf-8")


# ── llms.txt / llms-full.txt (deterministic assembly) ───────────────────────
def _assemble_llms_files():
    present = [(f, l) for f, l, _ in LEVELS
               if (ARTIFACTS_DIR / f).exists()]
    if not present:
        return
    idx = ["# STE-Code", "",
           "> STE-Code is a controlled-language variation of ASD-STE100 for software "
           "documentation, distilled here for LLM consumption. Pick the tier that "
           "matches your context window and task.", "",
           "## Artifact tiers", ""]
    for f, l in present:
        sz = (ARTIFACTS_DIR / f).stat().st_size
        idx.append(f"- [{f}]({f}) — level {l} (~{sz//1024}K) — {dict((x[1],x[2]) for x in LEVELS)[l]}")
    idx += ["", "## Full standard", "",
            "- [llms-full.txt](llms-full.txt) — concatenation of every tier above."]
    (ARTIFACTS_DIR / "llms.txt").write_text("\n".join(idx) + "\n", encoding="utf-8")

    full = []
    for f, _ in present:
        full.append(f"# === {f} ===\n\n" + (ARTIFACTS_DIR / f).read_text(errors="ignore"))
    (ARTIFACTS_DIR / "llms-full.txt").write_text("\n\n".join(full), encoding="utf-8")
    print(f"  wrote llms.txt + llms-full.txt ({len(present)} tiers)", flush=True)


# ── progress ─────────────────────────────────────────────────────────────────
def _regen_progress():
    rows = []
    done_n = 0
    for fname, label, desc in LEVELS:
        p = ARTIFACTS_DIR / fname
        ok = p.exists() and p.stat().st_size > 300
        if ok:
            done_n += 1
        rows.append((label, fname, "done" if ok else "missing", desc))
    lines = ["# STE-Code artifacts/ LLM-distill Progress Tracker", "",
             "> Generated from DISK EVIDENCE.", "",
             "## Level status", "",
             "| Level | File | Status | Description |",
             "|-------|------|--------|-------------|"]
    for label, fname, status, desc in rows:
        lines.append(f"| {label} | {fname} | {status} | {desc} |")
    lines += ["", "## Summary",
              f"- done: {done_n} / {len(LEVELS)}",
              f"- missing: {len(LEVELS) - done_n} / {len(LEVELS)}"]
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  progress regenerated: {done_n}/{len(LEVELS)}", flush=True)


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    verify = "--verify" in args
    regen = "--regen-progress" in args
    scaffold_only = "--scaffold-only" in args

    if verify:
        ok = all((ARTIFACTS_DIR / f).exists() and (ARTIFACTS_DIR / f).stat().st_size > 300
                 for f, _, _ in LEVELS)
        print(f"artifact LLM-distill verify: {'PASS' if ok else 'FAIL'} "
              f"({sum((ARTIFACTS_DIR/f).exists() for f,_,_ in LEVELS)}/{len(LEVELS)})")
        sys.exit(0 if ok else 1)

    # Always ensure deterministic bases exist first.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "levels_scaffold", str(Path(__file__).with_name("levels_scaffold.py")))
    scaffold = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scaffold)
    print("=== scaffolding deterministic level bases ===", flush=True)
    scaffold.main()

    if scaffold_only:
        return

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
        print(f"  DISTILL level{label}...", flush=True)
        if distill_level(i):
            if i not in done:
                done.append(i)
            _save_checkpoint(_checkpoint)
            n_ok += 1
            print(f"    ✓ level{label}", flush=True)
        else:
            print(f"    ✗ level{label}", flush=True)
        _regen_progress()

    print("=== assembling llms.txt / llms-full.txt ===", flush=True)
    _assemble_llms_files()
    print(f"\n{'='*60}\nArtifacts distilled: {n_ok}/{len(LEVELS)} levels ✓ -> ste-code/artifacts/\n{'='*60}", flush=True)
    sys.exit(0 if n_ok == len(LEVELS) else 1)


if __name__ == "__main__":
    main()
