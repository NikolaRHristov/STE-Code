#!/usr/bin/env python3
"""Phase F — LLM FINAL-DISTILLATION pass for STE-Code ARTIFACTS.

HYBRID design (per project owner):
  - LEVEL SEPARATION + BASE/BOILERPLATE is DETERMINISTIC (levels_scaffold.py),
    emitted as PER-TIER DIRECTORIES of bounded SUB-DOCUMENTS so neither the LLM
    writer nor the LLM reader ever touches one huge file (critical for level 5).
  - This pass is the LLM FINAL step: it DISTILLS each sub-document into an
    LLM-optimized file adapted to the STE-Code spec, in the spirit of
    llms.txt / llms-full.txt. Each sub-doc is its own small session.

Outputs (under ste-code/artifacts/):
  level-2/..level5/        each a dir of distilled sub-docs + _index.md
  llms.txt                 concise index (H1 + blockquote + tier/sub-doc list)
  llms-full.txt            full concatenation of every distilled sub-doc
The deterministic assembler (artifact_batch.py) still owns ste-code-rules.md /
ste-code-system-prompt.md.

Mechanism: each sub-doc is a oneshot session that reads its base sub-doc + the
full standard chunks (lossless, .agents/vendor research) and WRITES the distilled
sub-doc (multiple write_file calls). r.stdout -> .agents/tmp/ (trajectory only).
Checkpoint + progress flag done sub-docs. Fallback ships the base sub-doc.

Usage:
  python3 synthesize_artifacts.py            # scaffold, then distill all sub-docs
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
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
BASE_DIR = ARTIFACTS_DIR / "_base"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "artifact-llm-checkpoint.json"
PROGRESS_PATH = STATE_DIR / "artifact-llm-progress.md"
BUNDLE_DIR = STATE_DIR / "artifact-bundle"
VENDOR_DIR = PROJECT / ".agents" / "vendor"

MODEL = CFG.model
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 600  # per-sub-doc distillation; healthy distills take 20-90s,
                        # large sub-docs a few min. Bounded so a stuck session
                        # fails fast (fallback) instead of hanging 30 min.

LEVELS = [
    ("level-2", "-2", "ultra-minimal: the 14 core principles only"),
    ("level-1", "-1", "minimal/core: 14 core principles + synonym table"),
    ("level0",  "0",  "baseline: core principles + short dictionary excerpt"),
    ("level1",  "1",  "+ doc templates (code review / PR feedback)"),
    ("level2",  "2",  "+ section-specific grammar rules"),
    ("level3",  "3",  "+ complete dictionary excerpt + all rules"),
    ("level4",  "4",  "+ extensions + reference catalogue"),
    ("level5",  "5",  "full standard (all rules + extensions + catalogue + provenance)"),
]

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import render_template


# ── chunked standard (no truncation) ──────────────────────────────────────────
def _prepare_bundle() -> tuple[int, str]:
    mkdir(BUNDLE_DIR)
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
    chunks, cur = [], []
    for part in parts:
        if sum(len(x) for x in cur) + len(part) > 60000 and cur:
            chunks.append("\n\n---\n\n".join(cur)); cur = []
        cur.append(part)
    if cur:
        chunks.append("\n\n---\n\n".join(cur))
    for i, c in enumerate(chunks):
        write_text((BUNDLE_DIR / f"chunk-{i:03d}.md"), c)
    manifest = "\n".join(
        f"- Read `{BUNDLE_DIR / f'chunk-{i:03d}.md'}` (part {i+1}/{len(chunks)})"
        for i in range(len(chunks)))
    return len(chunks), manifest


def _load_checkpoint():
    from ste_checkpoint import load
    return load(CHECKPOINT_PATH)

def _save_checkpoint(ck):
    from ste_checkpoint import save
    save(CHECKPOINT_PATH, ck)

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


SYNTH_PROMPT_MD = PROJECT / ".agents" / "tools" / "prompts" / "synthesize-artifacts-worker.md"


def _build_prompt(level_label, subdoc_name, desc, manifest, base_path):
    return render_template(
        SYNTH_PROMPT_MD,
        level_label=level_label,
        subdoc=subdoc_name,
        desc=desc,
        bundle=manifest,
        base_path=str(base_path),
    )


def _distill_subdoc(tier_dir, subdoc_name, level_label, desc, manifest) -> bool:
    base_path = BASE_DIR / tier_dir / subdoc_name
    out = ARTIFACTS_DIR / tier_dir / subdoc_name
    prompt = _build_prompt(level_label, subdoc_name, desc, manifest, base_path)
    tmp = PROJECT / ".agents" / "tmp"
    mkdir(tmp)
    pf = tmp / f"artifact-{tier_dir}-{subdoc_name}.txt"
    write_text(pf, prompt)
    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "1800", "STE_MODEL": MODEL}
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True, timeout=TIMEOUT_SECONDS,
                           env=env, cwd=str(PROJECT))
        write_text((tmp / f"artifact-traj-{tier_dir}-{subdoc_name}.txt"), r.stdout)
        if out.exists() and out.stat().st_size > 200:
            return True
        _fallback_subdoc(tier_dir, subdoc_name)
        return True
    except subprocess.TimeoutExpired:
        _fallback_subdoc(tier_dir, subdoc_name)
        return True


def _fallback_subdoc(tier_dir, subdoc_name):
    src = BASE_DIR / tier_dir / subdoc_name
    dst = ARTIFACTS_DIR / tier_dir / subdoc_name
    if src.exists():
        write_text(dst, src.read_text(errors="ignore"))
    else:
        write_text(dst, f"# {subdoc_name} (base only)\n")


def _assemble_llms_files():
    present_tiers = [(d, l) for d, l, _ in LEVELS if (ARTIFACTS_DIR / d).is_dir()]
    if not present_tiers:
        return
    idx = ["# STE-Code", "",
           "> STE-Code is a controlled-language variation of ASD-STE100 for software "
           "documentation, distilled here for LLM consumption as small sub-documents. "
           "Load the tier that matches your context window; each tier is a directory "
           "of focused files plus an _index.md.", "", "## Tiers", ""]
    for d, l in present_tiers:
        idx.append(f"- [{d}/]({d}/) — level {l} — {dict((x[1],x[2]) for x in LEVELS)[l]}")
    idx += ["", "## Full standard", "",
            "- [llms-full.txt](llms-full.txt) — concatenation of every distilled sub-document."]
    write_text((ARTIFACTS_DIR / "llms.txt"), "\n".join(idx) + "\n")

    full = []
    for d, _ in present_tiers:
        full.append(f"# tier {d}\n")
        ip = ARTIFACTS_DIR / d / "_index.md"
        if ip.exists():
            full.append(ip.read_text(errors="ignore"))
        for sf in sorted((ARTIFACTS_DIR / d).glob("*.md")):
            if sf.name == "_index.md":
                continue
            full.append(f"\n## {sf.name}\n\n" + sf.read_text(errors="ignore"))
    write_text((ARTIFACTS_DIR / "llms-full.txt"), "\n\n".join(full))
    print(f"  wrote llms.txt + llms-full.txt ({len(present_tiers)} tiers)", flush=True)


def _regen_progress():
    rows, done_n, total = [], 0, 0
    for d, l, desc in LEVELS:
        bdir = BASE_DIR / d
        adir = ARTIFACTS_DIR / d
        subs = [p.name for p in sorted(bdir.glob("*.md"))] if bdir.is_dir() else []
        for s in subs:
            total += 1
            ok = (adir / s).exists() and (adir / s).stat().st_size > 200
            if ok:
                done_n += 1
        status = "done" if adir.is_dir() and subs and all(
            (adir / s).exists() for s in subs) else "partial"
        rows.append((l, d, status, desc))
    lines = ["# STE-Code artifacts/ LLM-distill Progress Tracker", "",
             "> Generated from DISK EVIDENCE.", "",
             "## Tier status", "", "| Level | Dir | Status | Description |",
             "|-------|-----|--------|-------------|"]
    for l, d, status, desc in rows:
        lines.append(f"| {l} | {d}/ | {status} | {desc} |")
    lines += ["", "## Summary",
              f"- sub-docs done: {done_n} / {total}",
              f"- tiers: {sum(1 for _,_,s,_ in rows if s=='done')}/{len(LEVELS)} complete"]
    mkdir(PROGRESS_PATH.parent)
    write_text(PROGRESS_PATH, "\n".join(lines) + "\n")
    print(f"  progress regenerated: {done_n}/{total} sub-docs", flush=True)


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    verify = "--verify" in args
    regen = "--regen-progress" in args
    scaffold_only = "--scaffold-only" in args or "--scaffold" in args

    if verify:
        ok = all((ARTIFACTS_DIR / d).is_dir() for d, _, _ in LEVELS)
        print(f"artifact LLM-distill verify: {'PASS' if ok else 'FAIL'} "
              f"({sum((ARTIFACTS_DIR/d).is_dir() for d,_,_ in LEVELS)}/{len(LEVELS)} tiers)")
        sys.exit(0 if ok else 1)

    # Deterministic bases (per-tier sub-doc dirs).
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "lib"))
    from templater import load_local
    SCAFFOLD_PATH = (Path(__file__).resolve().parent / "levels_scaffold.py")
    scaffold = load_local("levels_scaffold", SCAFFOLD_PATH)
    print("scaffolding deterministic level bases (sub-doc dirs)", flush=True)
    saved = sys.argv
    sys.argv = ["levels_scaffold.py"]
    try:
        scaffold.main()
    finally:
        sys.argv = saved

    if scaffold_only:
        return

    if regen:
        _regen_progress()
        return

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    mkdir(ARTIFACTS_DIR)
    manifest = _prepare_bundle()[1]
    done = _checkpoint.setdefault("done", [])  # list of "tier/subdoc" keys
    total_ok = 0
    for d, l, desc in LEVELS:
        bdir = BASE_DIR / d
        if not bdir.is_dir():
            continue
        adir = ARTIFACTS_DIR / d
        mkdir(adir)
        subs = [p.name for p in sorted(bdir.glob("*.md")) if p.name != "_index.md"]
        for s in subs:
            key = f"{d}/{s}"
            if resume and key in done:
                total_ok += 1
                continue
            print(f"  DISTILL {d}/{s}...", flush=True)
            if _distill_subdoc(d, s, l, desc, manifest):
                if key not in done:
                    done.append(key)
                _save_checkpoint(_checkpoint)
                total_ok += 1
                print(f"    ✓ {d}/{s}", flush=True)
        # per-tier index
        idx = [f"# STE-Code Level {l} — distilled index", "",
               f"> {desc}", "", "## Sub-documents", ""]
        for s in subs:
            idx.append(f"- {s}")
        write_text((adir / "_index.md"), "\n".join(idx) + "\n")
        _git_commit_locked([str((adir).relative_to(PROJECT))],
                          f"Phase F: LLM-distill tier {d} ({len(subs)} sub-docs)")
        _regen_progress()

    print("assembling llms.txt / llms-full.txt", flush=True)
    _assemble_llms_files()
    print(f"\n{'='*60}\nArtifacts distilled: tiers complete -> ste-code/artifacts/\n{'='*60}", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
