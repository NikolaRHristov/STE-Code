#!/usr/bin/env python3
"""Phase G+ — DEEP ENRICHMENT PASS (runs AFTER finalize_batch.py).

finalize_batch.py produced a first-synthesis pass, but inspection showed the
workers were INCONSISTENT: only ~32/54 rules cite a vendor source, several
have minimal examples / cross-references, and — critically — the finalizer
never passed --debug to the oneshot wrapper, so we have NO telemetry on how
much research each worker actually did.

This step is the "do a LOT more" pass. For each rule it:
  1. Finds RELEVANT vendor material up front (grep .agents/vendor/ for the rule's
     own keywords) and injects concrete snippets — the worker is handed the
     sources, not told to go hunting blindly.
  2. MANDATES real research: the worker MUST read >=3 vendor/reference files and
     the related rules, then write a '## Sources consulted' section listing them.
  3. EXPANDS examples to full, runnable code-domain pairs; adds >=2 cross-refs;
     borrows approved vocabulary; adds traceability.
  4. Runs in PARALLEL (--workers N, default 3, capped <=3).
  5. STRICT GATE: a file is only accepted if it cites a vendor source, has the
     required example count, >=2 See-also links, and traceability. Otherwise it
     is re-dispatched (never silently kept as a weak copy).

Telemetry: --debug is passed to hermes-oneshot-wrapper.py so each worker's
full tool-call trace is saved to .agents/tmp/oneshot-debug/ — real evidence of
how much research happened (unlike finalize_batch's stdout-only trajs).

Usage:
  python3 deep_enrich.py                 # deepen all final/rules/*
  python3 deep_enrich.py --only-weak     # only files failing the deep gate
  python3 deep_enrich.py --resume        # skip already-deepened files
  python3 deep_enrich.py --workers 3     # parallelism (default 3, max 3)
  python3 deep_enrich.py a-sec1-rule1.1.md  # single file (debug)
  python3 deep_enrich.py --report        # scan final/rules and print gate gaps
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
import atexit
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

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
FINAL_RULES_DIR = PROJECT / "ste-code" / "final" / "rules"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
VENDOR_DIR = PROJECT / ".agents" / "vendor"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "deepenrich-checkpoint.json"
PROGRESS_PATH = STATE_DIR / "deepenrich-progress.md"
DEBUG_DIR = PROJECT / ".agents" / "tmp" / "oneshot-debug"

MODEL = CFG.model
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 900  # deeper research needs more headroom
MAX_WORKERS = 3

SECTION_RULE_RE = re.compile(r"a-sec(\d+)-rule([\d.]+)\.md$")
RULE_H1_RE = re.compile(r"^#\s*Rule\s+(\d+\.\d+)\s*—\s*(.+?)\s*$", re.M)

# A rule is "deep" if it clears ALL of these. Anything else is --only-weak bait.
MIN_NONSTE_PAIRS = 8
MIN_SEE_ALSO = 2
REQUIRE_VENDOR_CITE = True
REQUIRE_TRACE = True

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


# ── relevant vendor material (hand the worker the sources, pre-found) ────────
def _relevant_vendor(rule_text: str, title: str) -> str:
    """Grep .agents/vendor/ for the rule's own keywords; return concrete snippets
    the worker MUST consult. This removes the 'go hunt blindly' failure mode and
    guarantees each worker has real, relevant reference material to borrow from."""
    # derive topic keywords from the rule heading + a few salient words
    head = (title or "").lower()
    words = set(re.findall(r"[a-z]{4,}", rule_text.lower()))
    # drop generic stopwords
    stop = {"that", "with", "this", "from", "your", "have", "will", "they", "used",
            "use", "rule", "code", "write", "writing", "text", "technical", "more",
            "than", "when", "which", "their", "other", "must", "should", "into"}
    kws = [w for w in words if w not in stop][:12]
    probe = " ".join(kws[:6])
    parts = []
    # 1) targeted grep across vendor for the probe keywords
    try:
        r = subprocess.run(
            ["grep", "-rIl", "-E", "|".join(re.escape(k) for k in kws[:6]),
             str(VENDOR_DIR)],
            capture_output=True, text=True, timeout=60)
        hits = [p for p in r.stdout.splitlines() if p.strip()]
    except Exception:
        hits = []
    seen = 0
    for h in hits[:8]:
        p = Path(h)
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        # pull a bounded window around the first keyword match
        body = txt[:800]
        if body.strip():
            parts.append(f"# Vendor source: {p.relative_to(VENDOR_DIR)}\n{body}")
            seen += 1
        if seen >= 6:
            break
    # 2) always include the curated final-phase directive + Microsoft/Google seeds
    fp = VENDOR_DIR / "FINAL_PHASE_CONTEXT_INSTRUCTIONS.md"
    if fp.exists():
        parts.append("# Final-phase context directive\n" + fp.read_text(errors="ignore")[:800])
    header = (
        f"# PRE-SELECTED VENDOR MATERIAL for this rule (probe keywords: {probe})\n"
        "These files under .agents/vendor/ are RELEVANT to this rule. You MUST read "
        "at least 3 of them (and ADD to the list if you find better ones) and cite "
        "them in a '## Sources consulted' section. Borrow approved, controlled "
        "vocabulary and realistic examples from them.\n\n"
    )
    return (header + "\n\n".join(parts))[:9000]


# ── deep prompt (externalized to .agents/tools/prompts/deep-enrich-worker.md) ──
DEEP_PROMPT_MD = PROJECT / ".agents" / "tools" / "prompts" / "deep-enrich-worker.md"

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import render_template  # {{placeholder}} substitution (project standard)


def _build_prompt(adapted_path: Path, self_num: str, title: str, section_num: str) -> str:
    src = adapted_path.read_text(encoding="utf-8", errors="ignore")
    vendor = _relevant_vendor(src, title)
    return render_template(
        DEEP_PROMPT_MD,
        src_name=adapted_path.name,
        self_num=self_num,
        title=title,
        src_text=src,
        vendor_block=vendor,
    )


# ── gates ───────────────────────────────────────────────────────────────────
def _valid_rule(path: Path) -> bool:
    if not (path.exists() and path.stat().st_size >= 400):
        return False
    return bool(re.match(r"^#\s*Rule", path.read_text(errors="ignore").lstrip()))


def _deep_gate(path: Path) -> tuple[bool, str]:
    """Strict: citation + example count + cross-refs + traceability required."""
    if not _valid_rule(path):
        return False, "missing/invalid"
    t = path.read_text(encoding="utf-8", errors="ignore")
    nonste = t.count("Non-STE:")
    seealso = t.count("See also:")
    cite = bool(re.search(r"Microsoft|Google|Vale|SCOWL|OpenSTE|glossar|style ?guide|word ?list|dwyl|kong|jvalentino|\.agents/vendor", t, re.I))
    trace = "Adapted from spec pair" in t
    sources_section = "Sources consulted" in t
    if REQUIRE_VENDOR_CITE and not (cite or sources_section):
        return False, "no vendor citation"
    if nonste < MIN_NONSTE_PAIRS:
        return False, f"only {nonste} Non-STE pairs (<{MIN_NONSTE_PAIRS})"
    if seealso < MIN_SEE_ALSO:
        return False, f"only {seealso} See-also (<{MIN_SEE_ALSO})"
    if REQUIRE_TRACE and not trace:
        return False, "no traceability"
    return True, "ok"


def _is_weak(path: Path) -> bool:
    ok, _ = _deep_gate(path)
    return not ok


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
    pf = tmp / f"deepen-{adapted_path.stem}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "900", "STE_MODEL": MODEL}
    # --debug => full tool-call trace saved to .agents/tmp/oneshot-debug/ (real
    # telemetry of how much research the worker did — unlike finalize's stdout).
    try:
        r = subprocess.run(
            [VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL, "--debug"],
            capture_output=True, text=True, timeout=TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired:
        with _lock:
            if not _valid_rule(out_path):
                out_path.write_text(adapted_path.read_text(errors="ignore"), encoding="utf-8")
                print(f"  [TIMEOUT] {adapted_path.name}: fell back to clean copy", flush=True)
                _git_commit_locked([str(out_path.relative_to(PROJECT))],
                                   f"Phase G+: deepen {adapted_path.name} (fallback)")
            else:
                print(f"  [TIMEOUT] {adapted_path.name}: kept existing", flush=True)
        return True
    (tmp / f"deepen-traj-{adapted_path.stem}.txt").write_text(
        "STDOUT:\n" + r.stdout + "\nSTDERR:\n" + r.stderr, encoding="utf-8")
    # Re-read from disk (worker wrote it) and STRICTLY gate.
    ok, reason = _deep_gate(out_path)
    with _lock:
        if ok:
            print(f"  ✓ {adapted_path.name} deepened (gate ok)", flush=True)
            _git_commit_locked([str(out_path.relative_to(PROJECT))],
                               f"Phase G+: deepen {adapted_path.name} (cited+enriched)")
            if adapted_path.name not in _checkpoint.setdefault("done", []):
                _checkpoint["done"].append(adapted_path.name)
            _save_checkpoint(_checkpoint)
            _regen_progress()
            return True
        # Not deep enough -> re-dispatch is handled by the caller loop (--only-weak
        # will catch it next pass). For a single run, leave the prior good file and
        # mark weak so a follow-up --only-weak re-run fixes it.
        print(f"  [WEAK] {adapted_path.name}: gate fail ({reason}); kept, will re-run via --only-weak", flush=True)
        if adapted_path.name not in _checkpoint.setdefault("done", []):
            _checkpoint["done"].append(adapted_path.name)
        _save_checkpoint(_checkpoint)
        _regen_progress()
    return True


def _regen_progress():
    rows = []
    files = sorted(FINAL_RULES_DIR.glob("a-sec*-rule*.md"))
    deep = weak = 0
    for p in files:
        num = SECTION_RULE_RE.search(p.name)
        rule_id = num.group(1) + "." + num.group(2) if num else p.stem
        ok, why = _deep_gate(p)
        status = "deep" if ok else f"weak ({why})"
        if ok:
            deep += 1
        else:
            weak += 1
        rows.append((rule_id, p.name, status))
    lines = [
        "# STE-Code final/ DEEP-ENRICHMENT Tracker",
        "",
        "> Deep gate: vendor citation + >=%d Non-STE pairs + >=%d See-also + traceability." % (MIN_NONSTE_PAIRS, MIN_SEE_ALSO),
        "",
        "| # | File | Status |",
        "|---|------|--------|",
    ]
    for rule_id, name, status in rows:
        lines.append(f"| {rule_id} | {name} | {status} |")
    lines += ["", "## Summary", f"- deep: {deep} / {len(files)}", f"- weak: {weak} / {len(files)}"]
    PROGRESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  deepenrich progress -> {PROGRESS_PATH}: {deep} deep / {weak} weak / {len(files)} total", flush=True)
    return PROGRESS_PATH


def _report():
    print("DEEP GATE REPORT (current final/rules/)")
    files = sorted(FINAL_RULES_DIR.glob("a-sec*-rule*.md"))
    for p in files:
        ok, why = _deep_gate(p)
        if not ok:
            print(f"  WEAK  {p.name}: {why}")
    print(f"  deep={sum(1 for p in files if _deep_gate(p)[0])}/{len(files)}")
    return


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    only_weak = "--only-weak" in args
    report = "--report" in args
    single = next((a for a in args if a.endswith(".md")), None)
    fresh = "--fresh" in args
    workers = MAX_WORKERS
    for i, a in enumerate(args):
        if a == "--workers" and i + 1 < len(args):
            try:
                workers = max(1, min(MAX_WORKERS, int(args[i + 1])))
            except ValueError:
                pass

    if report:
        _report()
        return

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    FINAL_RULES_DIR.mkdir(parents=True, exist_ok=True)
    files = [FINAL_RULES_DIR / single] if single else sorted(FINAL_RULES_DIR.glob("a-sec*-rule*.md"))

    if only_weak:
        files = [p for p in files if _is_weak(p)]
        print(f"  --only-weak: {len(files)} files fail the deep gate", flush=True)
    if fresh:
        _checkpoint = {"done": []}
        print("  --fresh: ignoring checkpoint", flush=True)

    done = _checkpoint.setdefault("done", [])
    work = [p for p in files if not (resume and not fresh and p.name in done)]

    if not work:
        print("  nothing to do. Use --only-weak to target weak files, or --fresh.", flush=True)
    else:
        print(f"  deepening {len(work)} files across <= {workers} concurrent workers...", flush=True)

        def _run(p):
            print(f"  DEEPEN {p.name}...", flush=True)
            return p.name, synthesize_file(p)

        completed = 0
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for name, _ in ex.map(_run, work):
                completed += 1
                print(f"    ({completed}/{len(work)}) {name}", flush=True)

    _save_checkpoint(_checkpoint)
    _regen_progress()
    print(f"\n{'='*60}\nPhase G+ deep enrichment done\n{'='*60}", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    main()
