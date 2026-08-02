#!/usr/bin/env python3
"""Phase D Orchestrator — STE→STE-Code adaptation (orchestrated, gated).

Reads the grouped spec (ste-code/grouped/*.md, produced by grouping) and adapts
each of the 9 rule sections (+ GR1-GR4) into code-domain STE-Code rule files
under ste-code/adapted/. Mirrors refine_batch.py's orchestration discipline
(checkpoint + per-section git commit + crash-safe resume) but, unlike grouping
(reflow only) or refinement (reformat only), adaptation is a genuine *writing*
task — so each section is handled by an LLM worker that creatively transforms
aerospace examples into code-domain examples while preserving rule numbers,
dictionary architecture, and the 6-pass transformation pipeline from the
embedded adaptation SKILL.md.

The creative transform is LLM-driven on purpose. What stays DETERMINISTIC and
truncation-safe (lesson #3 from refinement) is everything around it:
  - chunking by section (never re-types concatenated content),
  - externalized prompts (templates/*.md, edited without touching .py),
  - the verification gates (verify-adaptation.py) that BLOCK a section commit
    if aerospace terms leak through, non-approved synonyms slip in, rule files
    are missing, or example pairs are absent.

Usage:
  python3 adapt_batch.py [start_section] [num_sections] [--resume] [--force]
  python3 adapt_batch.py            # all 9 sections + GR, serial launch of parallel sections
  STE_MODEL=tencent/hy3:free python3 adapt_batch.py 1 9

Model: resolved via STE_MODEL env var (default tencent/hy3:free), matching
extract/refine.

Gate: refines only when ste-code/grouped/ is present and non-trivial; refuses
otherwise (the grouping agent produces it — see phase-c-run.py).
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
from datetime import datetime, timezone

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
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "adapt-checkpoint.json"

# ── Config ──────────────────────────────────────────────────────────────────
MODEL = CFG.model
WORKERS_PER_BATCH = int(os.environ.get("ADAPT_WORKERS_PER_BATCH", "1"))
TIMEOUT_SECONDS = 900

VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = RT.wrapper  # resolved by ste_runtime pre-flight

# 9 rule sections (number -> (title, expected rule count)). GR1-GR4 live in sec9.
SECTIONS = {
    1: ("Words", 14),
    2: ("Multi-word Nouns", 3),
    3: ("Verbs", 7),
    4: ("Sentences", 5),
    5: ("Procedural Writing", 5),
    6: ("Descriptive Writing", 6),
    7: ("Safety Instructions", 3),
    8: ("Punctuation", 7),
    9: ("Writing Practices", 4),   # plus GR1-GR4
}
TOTAL_SECTIONS = len(SECTIONS)

# Section heading patterns used to slice source text out of grouped/*.md.
#
# TWO shapes are accepted, in priority order:
#   1. The GROUP header that Phase C actually emits: `# Rules Sec N`. Grouping
#      names a group by its plan label, so the canonical spec titles
#      ("1. Words", "3. Verbs") do NOT survive into grouped/*.md — matching only
#      on them silently yielded 0/9 sections and every worker got the
#      "(section text not found)" fallback prompt.
#   2. The canonical spec heading `# N. Title`, kept as a fallback so this still
#      works against raw/refined text or a future grouping that preserves titles.
_SECTION_GROUP_RE = {
    n: re.compile(rf"^#+\s*Rules\s+Sec\s+{n}\b", re.I | re.M)
    for n in range(1, 10)
}
_SECTION_HEAD_RE = {
    1: re.compile(r"^#+\s*1[\.\s]+Words", re.I | re.M),
    2: re.compile(r"^#+\s*2[\.\s]+Multi-word\s+Nouns", re.I | re.M),
    3: re.compile(r"^#+\s*3[\.\s]+Verbs", re.I | re.M),
    4: re.compile(r"^#+\s*4[\.\s]+Sentences", re.I | re.M),
    5: re.compile(r"^#+\s*5[\.\s]+Procedural\s+Writing", re.I | re.M),
    6: re.compile(r"^#+\s*6[\.\s]+Descriptive\s+Writing", re.I | re.M),
    7: re.compile(r"^#+\s*7[\.\s]+Safety\s+Instructions", re.I | re.M),
    8: re.compile(r"^#+\s*8[\.\s]+Punctuation", re.I | re.M),
    9: re.compile(r"^#+\s*9[\.\s]+Writing\s+Practices", re.I | re.M),
}


def _find_section_head(section_num: int, text: str, pos: int = 0):
    """First match for a section heading in either accepted shape."""
    for table in (_SECTION_GROUP_RE, _SECTION_HEAD_RE):
        m = table[section_num].search(text, pos)
        if m:
            return m
    return None


# Terminator for the LAST rule section (9). Phase C emits one `# <Title>` header
# per group; the first of these that is not a rules group ends the rule text.
# Order in grouped/: … Rules Sec 9 → Dictionary Intro → Dict A B → … → Appendix.
_NON_RULES_GROUP_RE = re.compile(
    r"^#\s*(?:Dictionary\s+Intro|Dict\s+[A-Z]|Appendix)\b", re.I | re.M
)

# Aerospace terms that must NOT appear outside "## Original Rule" blocks.
AEROSPACE_TERMS = [
    "aircraft", "landing gear", "fuselage", "APU", "ECS",
    "ATA chapter", "lockwire", "avionics", "aileron", "rudder",
    "propeller", "thrust", "altimeter",
]
# "engine" excluded: legitimate code-domain word (search engine, game engine).
# "torque" and "cockpit" removed: code-domain-acceptable (mechanical build docs
# "torque the bolts"; "cockpit" only as a 'N words' spec example). Genuine
# aerospace-only leakage (aircraft, fuselage, APU, aileron, …) is still caught.

# Non-approved synonyms that must not appear outside "## Original Rule".
NON_APPROVED_SYNONYMS = ["utilize", "leverage", "employ", "commence", "terminate"]

import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import lib_import

engine = None  # lazy: only needed for slicing grouped text
_tpl = lib_import("templater")
TPL = _tpl.Templater(__file__)

# Embed the authoritative adaptation SKILL.md into every worker prompt.
_skill = lib_import("skill_prompt")


# ── readiness gate ───────────────────────────────────────────────────────────
def adaptation_ready() -> tuple[bool, str]:
    if not GROUPED_DIR.exists():
        return False, f"{GROUPED_DIR} missing — run grouping first (phase-c-run.py)"
    files = sorted(GROUPED_DIR.glob("*.md"))
    if not files:
        return False, f"{GROUPED_DIR} is empty"
    total = sum(f.stat().st_size for f in files)
    if total < 5000:
        return False, f"{GROUPED_DIR} looks unfinished ({total} bytes)"
    return True, f"{len(files)} grouped files, {total} bytes"


def _read_grouped_text() -> str:
    """Concatenate all grouped group files in group-id order."""
    files = sorted(GROUPED_DIR.glob("*.md"))
    return "\n\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in files)


def extract_section_source(section_num: int, grouped_text: str) -> str:
    """Slice the source rules for one adaptation section out of grouped text.

    Finds the section heading, then takes everything up to the next section
    heading (or end). Accepts both the `# Rules Sec N` group header that Phase C
    emits and the canonical `# N. Title` spec heading (see _find_section_head).

    Section 9 is special: it is the LAST rule section, so there is no section-10
    heading to stop at and a naive slice runs on through the whole dictionary
    (~570k chars — it would blow the worker's context and bury the rules). It is
    therefore terminated at the first non-rules group header that follows.
    """
    m = _find_section_head(section_num, grouped_text)
    if not m:
        return ""
    start = m.start()
    # Find the next section heading after this one.
    end = len(grouped_text)
    for nxt in range(section_num + 1, 10):
        nm = _find_section_head(nxt, grouped_text, m.end())
        if nm:
            end = nm.start()
            break
    else:
        # No later rule section (i.e. section 9): stop at the next group header
        # that is not part of the rules (dictionary, appendix, …).
        tail = _NON_RULES_GROUP_RE.search(grouped_text, m.end())
        if tail:
            end = tail.start()
    return grouped_text[start:end].strip()


# ── prompt construction ──────────────────────────────────────────────────────
def _build_prompt(section_num, title, source_text):
    """Section adaptation worker prompt = tight wrapper + embedded SKILL.md.

    The worker creatively transforms the injected source rules into code-domain
    STE-Code. The authoritative 6-pass pipeline + examples live in the embedded
    adaptation SKILL.md, so editing the SKILL changes behavior, not this script.
    """
    rule_ids = _expected_rule_ids(section_num)
    wrapper = TPL.render(
        "adapt-sec",
        section_num=section_num,
        section_title=title,
        rule_count=SECTIONS[section_num][1],
        rule_ids=", ".join(rule_ids),
        source_text=source_text or "(section text not found in grouped source — read ste-code/grouped/*.md for section "
        f"{section_num})",
    )
    skill = _skill.skill_section("adaptation")
    return wrapper + skill + (
        "\n\nOutput ONLY the adapted markdown rule files. No explanations, no "
        "commentary outside the files. Write each file with your file-write tool.\n"
    )


def _expected_rule_ids(section_num: int) -> list[str]:
    """Return the canonical rule ids for a section (for the prompt checklist)."""
    # sec9 also carries GR1-GR4.
    if section_num == 9:
        return [f"9.{i}" for i in range(1, 5)] + ["GR1", "GR2", "GR3", "GR4"]
    return [f"{section_num}.{i}" for i in range(1, SECTIONS[section_num][1] + 1)]


# ── verification gate (deterministic, no LLM) ────────────────────────────────
def _section_passed_gate(section_num, title) -> tuple[bool, str]:
    """Check the adapted output for one section against the deterministic gates.

    Returns (ok, reason). Mirrors verify-adaptation.py section checks but scoped
    to a single section so a bad section blocks only its own commit.
    """
    prefix = f"a-sec{section_num}-rule"
    rule_files = sorted(ADAPTED_DIR.glob(f"{prefix}*.md"))
    expected = SECTIONS[section_num][1]
    if len(rule_files) < expected:
        return False, f"missing rule files: have {len(rule_files)}, expected >= {expected}"

    problems = []
    for f in rule_files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Gate 2: source traceability
        if "Adapted from" not in text and "Source:" not in text:
            problems.append(f"{f.name}: no source reference")
        # Gate 3: example pair completeness (rules with examples need a pair)
        if "Non-STE:" in text and "STE:" not in text:
            problems.append(f"{f.name}: has Non-STE but no STE example")
        # Gate 6 + Gate 9: synonym / aerospace leakage — check only the ADAPTED
        # rule text, i.e. outside the '## Original Rule' block and outside any
        # '> **Non-STE:**' / '> **STE:**' example (both may legitimately show the
        # non-compliant / aerospace version), and outside pedagogical ban-list
        # lines ('use (not utilize, leverage, employ)') and mapping-teaching
        # lines that quote an aerospace term to explain the code-domain mapping.
        orig = text.split("## Original Rule")
        body = orig[0] if len(orig) == 1 else "".join(orig[1:])
        body = re.sub(r"(?m)^\s*>.*Non-STE:.*(?:\n\s*>.*)*", "", body)
        body = re.sub(r"(?m)^\s*>.*STE:.*(?:\n\s*>.*)*", "", body)
        body = re.sub(
            r"(?m)^\s*[-*]?\s*.*\bnot\s+(utilize|leverage|employ|commence|"
            r"terminate|initiate|bootstrap)\b.*$", "", body, flags=re.I)
        body = re.sub(
            r"(?m)^\s*[-*]?\s*.*(\u2192|->|\bis a technical noun\b|\bmaps to\b).*$",
            "", body)
        for sym in NON_APPROVED_SYNONYMS:
            if re.search(rf"\b{re.escape(sym)}\b", body, re.I):
                problems.append(f"{f.name}: non-approved synonym '{sym}' outside Original Rule/Non-STE")
        # Gate 9: aerospace leakage (outside Original Rule / Non-STE)
        for term in AEROSPACE_TERMS:
            if re.search(rf"\b{re.escape(term)}\b", body, re.I):
                problems.append(f"{f.name}: aerospace term '{term}' outside Original Rule/Non-STE")
        # Gate: minimum content
        if len(text) < 300:
            problems.append(f"{f.name}: too small ({len(text)} bytes)")

    if problems:
        return False, "; ".join(problems[:5])
    return True, "ok"


# ── checkpoint ───────────────────────────────────────────────────────────────
def _load_checkpoint():
    from ste_checkpoint import load
    return load(CHECKPOINT_PATH)

def _save_checkpoint(ckpt):
    from ste_checkpoint import save
    save(CHECKPOINT_PATH, ckpt)

_checkpoint = _load_checkpoint()


def git_commit_locked(files, msg):
    import time as _time
    lock = STATE_DIR / "adapt-git-lock"
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


def run_worker(section_num, title, source_text):
    """Run one section-adaptation worker (foreground, returns True/False)."""
    prompt = _build_prompt(section_num, title, source_text)
    tmp = PROJECT / ".agents" / "tmp"
    mkdir(tmp)
    pf = tmp / f"adapt-sec{section_num}.txt"
    write_text(pf, prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "180", "STE_MODEL": MODEL}
    cmd = [VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL]

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        print(f"  SEC{section_num}: Adapting '{title}' (attempt {attempt})...", flush=True)
        start_t = time.time()
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=TIMEOUT_SECONDS, env=env, cwd=str(PROJECT))
            dur = time.time() - start_t
            if result.stderr:
                sl = result.stderr.lower()
                if "error" in sl or "traceback" in sl:
                    print(f"  SEC{section_num}: [stderr] {result.stderr[:300]}", flush=True)
        except subprocess.TimeoutExpired:
            print(f"  SEC{section_num}: [TIMEOUT] after {TIMEOUT_SECONDS}s", flush=True)
            return False
        except Exception as e:
            print(f"  SEC{section_num}: [ERROR] {e}", flush=True)
            return False

        # Gate: only commit if the section's adapted output passes deterministically.
        ok, reason = _section_passed_gate(section_num, title)
        if ok:
            _checkpoint[str(section_num)] = {"passed": True, "duration": round(dur, 1)}
            _save_checkpoint(_checkpoint)
            print(f"  SEC{section_num}: [PASS] gate ok ({dur:.1f}s)", flush=True)
            return True
        else:
            print(f"  SEC{section_num}: [GATE FAIL] {reason} — retrying", flush=True)
            backoff = 15 * attempt
            print(f"  SEC{section_num}: sleeping {backoff}s before retry...", flush=True)
            time.sleep(backoff)

    print(f"  SEC{section_num}: [GIVEUP] after {max_attempts} attempts", flush=True)
    return False


def process_section(section_num, grouped_text):
    title = SECTIONS[section_num][0]
    ck = _checkpoint.get(str(section_num))
    if ck and ck.get("passed"):
        print(f"\n{'='*60}\nSection {section_num} — {title}\n{'='*60}", flush=True)
        print(f"  SEC{section_num}: ✓ Already adapted (checkpoint skip)", flush=True)
        return True

    print(f"\n{'='*60}\nSection {section_num} — {title}\n{'='*60}", flush=True)
    source_text = extract_section_source(section_num, grouped_text)
    ok = run_worker(section_num, title, source_text)
    if ok:
        rule_files = sorted(ADAPTED_DIR.glob(f"a-sec{section_num}-rule*.md"))
        files = [str(f.relative_to(PROJECT)) for f in rule_files]
        if files:
            msg = f"Adapt Section {section_num:02d} - {title} - PASS"
            if git_commit_locked(files, msg):
                print(f"  ✓ Committed: {msg}", flush=True)
            else:
                print(f"  ✗ Commit failed: {msg}", flush=True)
    return ok


def main():
    resume = "--resume" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start_section = int(args[0]) if len(args) > 0 else 1
    num_sections = int(args[1]) if len(args) > 1 else TOTAL_SECTIONS

    ready, msg = adaptation_ready()
    if not ready:
        print(f"ADAPTATION NOT READY: {msg}", flush=True)
        print("Run grouping first (phase-c-run.py). Refusing to launch workers.", flush=True)
        sys.exit(2)

    grouped_text = _read_grouped_text()
    print("STE-Code Adaptation Pipeline", flush=True)
    print(f"Model: {MODEL}", flush=True)
    print(f"Sections: {num_sections} (from {start_section})", flush=True)
    print(f"Resume: {'yes' if resume else 'no'}", flush=True)

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    all_ok = True
    for s in range(start_section, min(start_section + num_sections, TOTAL_SECTIONS + 1)):
        if s not in SECTIONS:
            continue
        if not process_section(s, grouped_text):
            all_ok = False

    final = len(list(ADAPTED_DIR.glob("a-sec*-rule*.md")))
    print(f"\n{'='*60}\nDone. Adapted rule files: {final}\n{'='*60}", flush=True)
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
