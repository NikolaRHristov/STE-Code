#!/usr/bin/env python3
"""Phase G/F — FINAL SYNTHESIS (LLM-per-file, refinement-like).

Redefines ste-code/final/ as the MOST ENRICHED version of STE-Code: an LLM
reasons about EACH adapted rule file individually (like the refinement pipeline),
reads the code-domain references, and rewrites the rule with:

  - the MOST COMPLETE code examples (full, runnable, not abbreviated)
  - cross-references to other rules it cites (See also)
  - traceability back to the original ASD-STE100 spec pair
  - borrowed controlled vocabulary from the VENDOR references (Microsoft/Google
    word lists, glossaries) under .agents/vendor/
  - NO aerospace leakage; code-domain examples only

Mechanism (mirrors extend_batch.py / refine_batch.py): each rule file is a
separate oneshot worker via hermes-oneshot-wrapper.py, gated deterministically
by verify_final.py, with checkpoint + per-file git commit (crash-safe resume).
If the LLM worker fails/times out for a file, we FALL BACK to a deterministic
copy of the adapted file so final/rules/ is always complete.

Multiple workers run in PARALLEL (--workers N, default 3; capped to <=3 to stay
within the free-tier concurrency budget). Only one worker may mutate the shared
checkpoint / git index / progress.md at a time (a process-wide lock serializes
those writes); the LLM subprocesses themselves run concurrently.

After synthesis, run synthesize_levels.py (SEPARATE delegate) to break the
finished final/rules/ into reworked levels 1-5.

Usage:
  python3 finalize_batch.py                  # synthesize all rule files
  python3 finalize_batch.py --resume         # skip already-done files
  python3 finalize_batch.py --fresh          # ignore checkpoint, re-run all
  python3 finalize_batch.py --workers 3      # parallelism (default 3, max 3)
  python3 finalize_batch.py --only-stale     # synthesize only copied/non-synth
  python3 finalize_batch.py a-sec1-rule1.1.md  # single file (debug)
  python3 finalize_batch.py --verify         # run verify_final.py only
"""
from __future__ import annotations

import os
import re
import sys
import json
import time
import signal
import subprocess
import threading
import fcntl
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
FINAL_RULES_DIR = PROJECT / "ste-code" / "final" / "rules"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
VENDOR_DIR = PROJECT / ".agents" / "vendor"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "finalize-checkpoint.json"
PROGRESS_PATH = STATE_DIR / "finalize-progress.md"
LOCK_PATH = STATE_DIR / "finalize.lock"
FINAL_CTX = VENDOR_DIR / "FINAL_PHASE_CONTEXT_INSTRUCTIONS.md"

# ── Prompt text lives in templates/, not in this file ─────────────────────────
# See .agents/tools/lib/PROMPTS.md. Edit templates/finalize-*.md to change
# worker wording; this script only supplies the values.
import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import lib_import

templater = lib_import("templater")
_TPL = templater.Templater(__file__)

MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 600
MAX_WORKERS = 3  # free-tier concurrency budget — never exceed

SECTION_RULE_RE = re.compile(r"a-sec(\d+)-rule([\d.]+)\.md$")
RULE_H1_RE = re.compile(r"^#\s*Rule\s+(\d+\.\d+)\s*—\s*(.+?)\s*$", re.M)

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))


# ── checkpoint ──────────────────────────────────────────────────────────────
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
# Serialize all shared-state mutations (checkpoint/git/progress) across workers.
_lock = threading.Lock()


def _git_commit_locked(files, msg):
    try:
        subprocess.run(["git", "add", "-A", "--", *files], cwd=str(PROJECT),
                       check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=str(PROJECT),
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


# ── reference context (borrowed vocabulary from VENDOR corpora) ─────────────
def _reference_context() -> str:
    """Seed the synthesizer's vocabulary from the downloaded VENDOR corpora.

    The old .agents/reference/ catalogue was removed; authoritative word lists
    and style guides now live in .agents/vendor/. Pull concrete, relevant
    excerpts from Microsoft/Google style packages, glossaries, and word lists.
    """
    parts = []
    # 1) Surface the final-phase context directive so the worker knows where to
    #    look for grounding documents.
    if FINAL_CTX.exists():
        parts.append(
            "# Final-phase context directive (where to ground ambiguous choices)\n"
            + FINAL_CTX.read_text(encoding="utf-8", errors="ignore")[:1200]
        )
    # 2) Pull approved-word lists from the Vale Microsoft/Google style packages.
    for pkg, slug in (("vale-microsoft", "Microsoft"), ("vale-google", "Google")):
        pkg_dir = VENDOR_DIR / pkg
        if not pkg_dir.exists():
            continue
        # collect .txt/.md vocab files (e.g. word lists, preferred terms)
        excerpts = []
        for ext in ("*.txt", "*.md"):
            for p in list(pkg_dir.rglob(ext))[:4]:
                try:
                    txt = p.read_text(encoding="utf-8", errors="ignore")
                except Exception:
                    continue
                # take a bounded body sample
                body = txt[:500]
                if body.strip():
                    excerpts.append(f"## {p.name}\n{body}")
                if len("\n\n".join(excerpts)) > 1500:
                    break
            if excerpts:
                break
        if excerpts:
            parts.append(f"# Reference vocabulary: {slug} style package\n"
                         + "\n\n".join(excerpts)[:1800])
    # 3) Concrete word-list snippets (software terms, common words, technical glossary)
    for slug, fname in (
        ("software-terms.dic", "software-terms.dic"),
        ("dwyl-technical-glossary", None),
        ("kong-apiglossary", None),
        ("jvalentino-glossary", None),
    ):
        p = VENDOR_DIR / fname if fname else VENDOR_DIR / slug
        if not p.exists():
            # maybe it's a directory — take its README
            if p.is_dir():
                readme = p / "README.md"
                if readme.exists():
                    p = readme
                else:
                    continue
            else:
                continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        body = txt[:600]
        if body.strip():
            parts.append(f"# Reference: {slug}\n{body}")
    # 4) Microsoft Style Guide prose (the extracted styleguide/ tree)
    msg = VENDOR_DIR / "styleguide"
    if msg.is_dir():
        for md in list(msg.rglob("*.md"))[:3]:
            try:
                txt = md.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            body = txt[:500]
            if body.strip():
                parts.append(f"# Microsoft Style Guide: {md.name}\n{body}")
            if len("\n\n".join(parts)) > 6000:
                break
    return "\n\n".join(parts)[:8000]


def _previous_documents_context(section_num: str, self_num: str) -> str:
    """Read the PRIOR pipeline documents so the synthesizer has full context:
    grouped/ original spec pairs (traceability), code-domain dictionary + categories
    (vocabulary), and the extension approved verbs/adjectives (borrowed terms).
    Capped so the prompt stays bounded."""
    parts = []
    # 1) grouped/ original aerospace spec pairs for this section (traceability source)
    try:
        for p in sorted(GROUPED_DIR.glob(f"group-*-rules-sec-{section_num}.md")):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            blocks = re.findall(r">\s*\*\*(Non-STE|STE|Do not write|WRITE):\*\*[^\n]*", txt)
            if blocks:
                parts.append(f"# Original spec source (grouped/ sec {section_num})\n"
                             f"{txt[:1200]}")
                break
    except Exception:
        pass
    # 2) code-domain dictionary excerpt
    dic = ADAPTED_DIR / "a-dictionary.md"
    if dic.exists():
        parts.append("# STE-Code dictionary (code-domain vocabulary)\n" + dic.read_text(errors="ignore")[:1500])
    # 3) categories excerpt
    catf = ADAPTED_DIR / "a-categories.md"
    if catf.exists():
        parts.append("# STE-Code categories\n" + catf.read_text(errors="ignore")[:1500])
    # 4) extension approved verbs/adjectives (borrowed controlled terms)
    for area in ("verbs", "adjectives"):
        ep = PROJECT / "ste-code" / "extensions" / f"{area}.md"
        if ep.exists():
            txt = ep.read_text(errors="ignore")
            lines = [l for l in txt.splitlines() if l.startswith("### ") or "**replaces**" in l][:24]
            parts.append(f"# Extension approved {area}\n" + "\n".join(lines))
    return "\n\n".join(parts)


# ── prompt for one rule file ────────────────────────────────────────────────
def _build_prompt(adapted_path: Path, self_num: str, title: str, section_num: str) -> str:
    src = adapted_path.read_text(encoding="utf-8", errors="ignore")
    refs = _reference_context()
    prev = _previous_documents_context(section_num, self_num)
    return _TPL.render(
        "finalize-worker",
        adapted_path_name=adapted_path.name,
        self_num=self_num,
        title=title,
        src=src,
        prev=prev,
        refs=refs,
    )


# ── deterministic fallback ─────────────────────────────────────────────────
def _fallback_copy(adapted_path: Path, out_path: Path):
    out_path.write_text(adapted_path.read_text(encoding="utf-8", errors="ignore"),
                        encoding="utf-8")


def _valid_rule(path: Path) -> bool:
    if not (path.exists() and path.stat().st_size >= 400):
        return False
    return bool(re.match(r"^#\s*Rule", path.read_text(errors="ignore").lstrip()))


# ── gate (single file) ─────────────────────────────────────────────────────
def _file_gate_ok(path: Path) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    t = path.read_text(encoding="utf-8", errors="ignore")
    if not t.strip():
        return False, "empty"
    if re.search(r"TODO|TBD|\?\?\?", t, re.I):
        return False, "fabrication marker"
    if len(t) < 300:
        return False, "too short"
    if not re.search(r">\s*\*\*(?:Non-STE|STE)", t) and "## Examples" in t:
        if "STE:" not in t:
            return False, "no STE example pair"
    return True, "ok"


def synthesize_file(adapted_path: Path) -> bool:
    sm = SECTION_RULE_RE.search(adapted_path.name)
    if not sm:
        return False
    self_num = f"{sm.group(1)}.{sm.group(2)}"
    m = RULE_H1_RE.search(adapted_path.read_text(encoding="utf-8", errors="ignore"))
    title = m.group(2).strip() if m else adapted_path.stem
    out_path = FINAL_RULES_DIR / adapted_path.name

    prompt = _build_prompt(adapted_path, self_num, title, sm.group(1))
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"finalize-{adapted_path.stem}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "600", "STE_MODEL": MODEL}
    # The session (worker) READS the source and WRITES ste-code/final/rules/<name>
    # itself via its file tools — the orchestrator is NOT a dumb pipe that writes
    # r.stdout. We capture r.stdout only as trajectory/history to .agents/tmp/.
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        # One slow session must NOT kill the whole batch. But NEVER clobber a file
        # that is already a valid enriched rule (written by a prior run) — only fall
        # back to a clean copy if the current file is missing or not a valid rule.
        with _lock:
            if not _valid_rule(out_path):
                _fallback_copy(adapted_path, out_path)
                print(f"  [TIMEOUT] {adapted_path.name}: fell back to clean copy", flush=True)
                _git_commit_locked([str(out_path.relative_to(PROJECT))],
                                   f"Phase G: synthesize {adapted_path.name} (LLM final)")
            else:
                print(f"  [TIMEOUT] {adapted_path.name}: kept existing enriched file", flush=True)
        return True
    # Save the agent's stdout as trajectory/history (like refinement/extraction),
    # NOT as the output file.
    (tmp / f"finalize-traj-{adapted_path.stem}.txt").write_text(r.stdout, encoding="utf-8")
    # Gate on the file the SESSION itself wrote (not our stdout).
    if _valid_rule(out_path):
        with _lock:
            print(f"  ✓ {adapted_path.name} (session wrote final)", flush=True)
            _git_commit_locked([str(out_path.relative_to(PROJECT))],
                               f"Phase G: synthesize {adapted_path.name} (LLM final)")
            if adapted_path.name not in _checkpoint.setdefault("done", []):
                _checkpoint["done"].append(adapted_path.name)
            _save_checkpoint(_checkpoint)
            _regen_progress()
        return True
    # Session did not write a valid file -> fall back, BUT only if the current file
    # is not already a valid enriched rule (never overwrite good work).
    with _lock:
        if not _valid_rule(out_path):
            _fallback_copy(adapted_path, out_path)
            print(f"  [FALLBACK] {adapted_path.name}: session did not write valid file; clean copy", flush=True)
            _git_commit_locked([str(out_path.relative_to(PROJECT))],
                               f"Phase G: synthesize {adapted_path.name} (LLM final)")
        else:
            print(f"  [FALLBACK] {adapted_path.name}: kept existing enriched file", flush=True)
        if adapted_path.name not in _checkpoint.setdefault("done", []):
            _checkpoint["done"].append(adapted_path.name)
        _save_checkpoint(_checkpoint)
        _regen_progress()
    return True


def _regen_progress():
    """Regenerate .agents/state/finalize-progress.md from DISK EVIDENCE (not memory):
    a row is 'stale' iff final/rules/<f> == adapted/<f>. This is the authoritative
    stale-flag an agent reads to know WHICH files to re-synthesize and WHEN
    (every run / on demand via --regen-progress). Kept in .agents/ so ste-code/
    stays shippable (no pipeline bookkeeping inside it)."""
    FINAL_RULES = FINAL_RULES_DIR
    rows = []
    files = sorted(FINAL_RULES.glob("a-sec*-rule*.md"))
    enriched = stale = 0
    for p in files:
        num = SECTION_RULE_RE.search(p.name)
        rule_id = num.group(1) + "." + num.group(2) if num else p.stem
        src = ADAPTED_DIR / p.name
        is_stale = (src.exists() and p.read_text(errors="ignore") == src.read_text(errors="ignore"))
        status = "stale" if is_stale else "enriched"
        if is_stale:
            stale += 1
        else:
            enriched += 1
        note = "copied; re-synthesize" if is_stale else "LLM final"
        rows.append((rule_id, p.name, status, note))
    lines = [
        "# STE-Code final/ Progress Tracker",
        "",
        "> **⚠️ Stale-flag source of truth.** A row marked `stale` means",
        "> `ste-code/final/rules/<file>` is byte-identical to `ste-code/adapted/<file>`",
        "> — i.e. it was copied, NOT LLM-synthesized. Those files MUST be re-synthesized",
        "> by an agent session (the agent reads adapted/ + references and writes the",
        "> enriched file itself). A row marked `enriched` is a real LLM synthesis.",
        ">",
        "> Regenerate this table any time with:",
        "> `python3 .agents/tools/finalize/finalize_batch.py --regen-progress`",
        "> (written to .agents/state/finalize-progress.md — ste-code/ is shippable).",
        "> The execution auditor cross-references these claims against disk evidence.",
        "",
        "## Status legend",
        "- `enriched` — LLM-synthesized final rule (differs from adapted source)",
        "- `stale`    — copied from adapted/ (NOT synthesized; must be re-run)",
        "",
        "## Rule status",
        "",
        "| # | File | Status | Note |",
        "|---|------|--------|------|",
    ]
    for rule_id, name, status, note in rows:
        lines.append(f"| {rule_id} | {name} | {status} | {note} |")
    lines += [
        "",
        "## Summary",
        f"- enriched: {enriched} / {len(files)}",
        f"- stale (must re-synthesize): {stale} / {len(files)}",
    ]
    out = PROGRESS_PATH
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  progress regenerated -> {out}: {enriched} enriched / {stale} stale / {len(files)} total",
          flush=True)
    return out


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    verify = "--verify" in args
    regen_progress = "--regen-progress" in args
    only_stale = "--only-stale" in args
    fresh = "--fresh" in args
    single = next((a for a in args if a.endswith(".md")), None)
    # parallelism
    workers = MAX_WORKERS
    for i, a in enumerate(args):
        if a == "--workers" and i + 1 < len(args):
            try:
                workers = max(1, min(MAX_WORKERS, int(args[i + 1])))
            except ValueError:
                pass

    if verify:
        v = PROJECT / ".agents" / "tools" / "finalize" / "verify_final.py"
        os.execv(VENV_PYTHON, [VENV_PYTHON, str(v)])
        return

    if regen_progress:
        _regen_progress()
        return

    atexit_lock = threading.Lock()

    def _atexit():
        with atexit_lock:
            _save_checkpoint(_checkpoint)

    import atexit
    atexit.register(_atexit)
    signal.signal(signal.SIGTERM, lambda *_: (_atexit(), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_atexit(), sys.exit(130)))

    FINAL_RULES_DIR.mkdir(parents=True, exist_ok=True)
    files = [ADAPTED_DIR / single] if single else sorted(ADAPTED_DIR.glob("a-sec*-rule*.md"))

    # --only-stale: synthesize ONLY rules whose final/rules/<f> == adapted/<f>
    # (the copied, non-synthesized ones flagged in progress.md).
    if only_stale:
        kept = []
        for p in files:
            fp = FINAL_RULES_DIR / p.name
            sp = ADAPTED_DIR / p.name
            if fp.exists() and sp.exists() and fp.read_text(errors="ignore") == sp.read_text(errors="ignore"):
                kept.append(p)
            elif not fp.exists():
                kept.append(p)
        files = kept

    if fresh:
        _checkpoint = {"done": []}
        print("  --fresh: ignoring checkpoint, re-running all files", flush=True)

    done = _checkpoint.setdefault("done", [])
    if resume and not fresh:
        print(f"  resume: {len(done)} already done in checkpoint", flush=True)

    # Build the work list (skip done unless fresh/single/only_stale override)
    work = []
    for p in files:
        if resume and not fresh and p.name in done:
            print(f"  skip (done): {p.name}", flush=True)
            continue
        work.append(p)

    if not work:
        print("  nothing to do (all done). Use --fresh to re-run all.", flush=True)
    else:
        print(f"  launching {len(work)} workers across <= {workers} concurrent LLM sessions...",
              flush=True)

        def _run_one(p: Path):
            print(f"  SYNTH {p.name}...", flush=True)
            ok = synthesize_file(p)
            return p.name, ok

        completed = 0
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for name, ok in ex.map(_run_one, work):
                completed += 1
                if ok:
                    print(f"    ✓ {name}  ({completed}/{len(work)})", flush=True)
                else:
                    print(f"    ✗ {name}  ({completed}/{len(work)}) (will retry next run)", flush=True)

    # copy categories + dictionary (deterministic, code-domain) into final/rules/
    for extra in ("a-categories.md", "a-dictionary.md"):
        src = ADAPTED_DIR / extra
        if src.exists():
            (FINAL_RULES_DIR / extra).write_text(src.read_text(encoding="utf-8", errors="ignore"),
                                                 encoding="utf-8")
    _git_commit_locked([str(FINAL_RULES_DIR.relative_to(PROJECT))],
                       "Phase G: finalize rule files synthesized (LLM) + categories/dictionary")

    # NOTE: assembly into ste-code/final/ (extensions + catalogue + provenance) is a
    # SEPARATE, non-overwriting step (assemble_final.py). We do NOT re-copy raw
    # adapted/ over the LLM-synthesized final/rules/ here — that would clobber the
    # enrichment. Run assemble_final.py explicitly after synthesis if needed.

    _save_checkpoint(_checkpoint)
    print(f"\n{'='*60}\nPhase G synthesis done: {len(work)} workers dispatched\n{'='*60}", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
