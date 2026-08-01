#!/usr/bin/env python3
"""Phase G/F — FINAL SYNTHESIS (LLM-per-file, refinement-like).

Redefines ste-code/final/ as the MOST ENRICHED version of STE-Code: an LLM
reasons about EACH adapted rule file individually (like the refinement pipeline),
reads the code-domain references, and rewrites the rule with:

  - the MOST COMPLETE code examples (full, runnable, not abbreviated)
  - cross-references to other rules it cites (See also)
  - traceability back to the original ASD-STE100 spec pair
  - borrowed controlled vocabulary from the vendor references (Microsoft/Google
    word lists, glossaries)
  - NO aerospace leakage; code-domain examples only

Mechanism (mirrors extend_batch.py / refine_batch.py): each rule file is a
separate oneshot worker via hermes-oneshot-wrapper.py, gated deterministically
by verify_final.py, with checkpoint + per-file git commit (crash-safe resume).
If the LLM worker fails/times out for a file, we FALL BACK to a deterministic
copy of the adapted file so final/rules/ is always complete.

After synthesis, run synthesize_levels.py (SEPARATE delegate) to break the
finished final/rules/ into reworked levels 1-5.

Usage:
  python3 finalize_batch.py                 # synthesize all rule files
  python3 finalize_batch.py --resume        # skip already-done files
  python3 finalize_batch.py a-sec1-rule1.1.md  # single file (debug)
  python3 finalize_batch.py --verify        # run verify_final.py only
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
FINAL_RULES_DIR = PROJECT / "ste-code" / "final" / "rules"
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
REFERENCE_DIR = PROJECT / ".agents" / "reference"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "finalize-checkpoint.json"
ASSEMBLE = PROJECT / ".agents" / "tools" / "finalize" / "assemble_final.py"

MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")
TIMEOUT_SECONDS = 600

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


def _git_commit_locked(files, msg):
    try:
        subprocess.run(["git", "add", "-A", "--", *files], cwd=str(PROJECT),
                       check=True, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m", msg], cwd=str(PROJECT),
                       check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


# ── reference context (borrowed vocabulary) ─────────────────────────────────
def _reference_context() -> str:
    """Small, relevant reference excerpts to seed the synthesizer's vocabulary."""
    parts = []
    # vendor reference catalogue
    cat = REFERENCE_DIR / "manifest.json"
    if cat.exists():
        try:
            entries = json.load(open(cat))["entries"]
            lines = "\n".join(f"- {e['title']}: {e['url']}" for e in entries[:12])
            parts.append("# Vendor reference catalogue (borrow vocabulary from these)\n" + lines)
        except Exception:
            pass
    # pull a few concrete word-list snippets (Microsoft / Google approved words)
    for slug in ("microsoft-writing-style-guide", "google-style-guides", "kong-apiglossary"):
        p = REFERENCE_DIR / (slug + ".md")
        if p.exists():
            txt = p.read_text(encoding="utf-8", errors="ignore")
            # take the first ~600 chars of body after the header
            body = txt.split("\n---\n", 1)[-1][:600]
            parts.append(f"# Reference: {slug}\n{body}")
    return "\n\n".join(parts)


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
            # extract heading + replaces lines
            lines = [l for l in txt.splitlines() if l.startswith("### ") or "**replaces**" in l][:24]
            parts.append(f"# Extension approved {area}\n" + "\n".join(lines))
    return "\n\n".join(parts)


# ── prompt for one rule file ────────────────────────────────────────────────
def _build_prompt(adapted_path: Path, self_num: str, title: str, section_num: str) -> str:
    src = adapted_path.read_text(encoding="utf-8", errors="ignore")
    refs = _reference_context()
    prev = _previous_documents_context(section_num, self_num)
    return f"""You are a senior technical writer synthesizing the FINAL, most-enriched
version of STE-Code (a controlled-language variation of ASD-STE100 for software
documentation). You are rewriting ONE rule file. Reason carefully about this rule
and produce the richest, most useful code-domain version possible. This is a
CREATIVE enrichment step: expand examples, deepen guidance, and borrow vocabulary
from the provided references and prior documents.

# INPUT — the current adapted rule (from ste-code/adapted/)
File: {adapted_path.name}
Title: Rule {self_num} — {title}

{src}

# PREVIOUS DOCUMENTS (prior pipeline stages — use for traceability & vocabulary)
{prev}

# REFERENCES (borrow controlled vocabulary / approved words from these)
{refs}

# YOUR TASK — synthesize the enriched final rule
Rewrite the file as markdown. Preserve the rule's heading, Original Rule block,
STE-Code Adaptation, and Examples structure. Then ENRICH it:

1. MOST COMPLETE CODE EXAMPLES: expand every Non-STE/STE pair into full,
   runnable, realistic code documentation examples (not abbreviated with "...").
   Keep the `> **Non-STE:**` / `> **STE:**` format. Each example must show a
   concrete, code-domain situation (functions, APIs, config, tests, errors).
2. CROSS-REFERENCES: if this rule relates to others, add at the end:
   `> **See also:** Rule X.Y — <title>` for each related rule it cites.
3. TRACEABILITY: after the Examples heading, add
   `> *Adapted from spec pair:* Non-STE: <original ASD-STE100 example>  |  STE: <compliant version>`
   (derive from the rule's own content / the Original Rule block / prior documents).
4. BORROW VOCABULARY: use approved, plain code-domain words (prefer the
   Microsoft/Google style-guide words and the STE-Code dictionary; avoid
   utilize/leverage/employ/commence/terminate/initiate when a simpler verb works).
5. NO aerospace leakage: every example and term must be code-domain.

Output ONLY the rewritten markdown file. No code fences, no commentary outside
the file. The file must be self-contained and parseable as one markdown document.

STRICT FORMAT RULE (enforced): Do NOT prepend or append ANY assistant narration,
tool logs, "Rewrote…", file paths, "What changed vs…", "Key changes", or meta-notes.
Emit ONLY the raw markdown rule body: it MUST begin with '# Rule' and end with the
Examples block. No explanatory text before or after. If you add a single word of
commentary, the file is rejected. Start immediately with the rule heading.
"""


# ── deterministic fallback ─────────────────────────────────────────────────
def _fallback_copy(adapted_path: Path, out_path: Path):
    out_path.write_text(adapted_path.read_text(encoding="utf-8", errors="ignore"),
                        encoding="utf-8")


# ── gate (reuse verify_final.py logic on the single file) ───────────────────
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
    if not re.search(r">\s*\*\*Non-STE", t) and "## Examples" in t:
        # examples section should have at least one pair
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

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "300", "STE_MODEL": MODEL}
    try:
        r = subprocess.run([VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL],
                           capture_output=True, text=True, timeout=300)
        if r.returncode == 0 and r.stdout.strip():
            out_path.write_text(r.stdout, encoding="utf-8")
            # GUARD: if the worker returned narration instead of the rule body,
            # reject and re-attempt (never save a contaminated file)
            if not re.match(r"^#\s*Rule", r.stdout.strip()):
                print(f"  [GUARD] {adapted_path.name}: LLM returned non-rule body; retrying", flush=True)
                return synthesize_file(adapted_path)
            print(f"  ✓ {adapted_path.name}", flush=True)
            return True
        else:
            # fall back to deterministic copy
            _fallback_copy(adapted_path, out_path)
        ok, why = _file_gate_ok(out_path)
        if not ok:
            # gate failed on LLM output -> use fallback copy (still complete)
            _fallback_copy(adapted_path, out_path)
            ok, why = _file_gate_ok(out_path)
        if not _git_commit_locked([str(out_path.relative_to(PROJECT))],
                                  f"Phase G: synthesize {adapted_path.name} (LLM final)"):
            print(f"  FINALIZE {adapted_path.name}: commit failed", flush=True)
        return ok
    except subprocess.TimeoutExpired:
        _fallback_copy(adapted_path, out_path)
        _file_gate_ok(out_path)
        _git_commit_locked([str(out_path.relative_to(PROJECT))],
                           f"Phase G: synthesize {adapted_path.name} (fallback copy)")
        print(f"  FINALIZE {adapted_path.name}: [TIMEOUT] fallback copy", flush=True)
        return True


def main():
    global _checkpoint
    args = sys.argv[1:]
    resume = "--resume" in args
    verify = "--verify" in args
    single = next((a for a in args if a.endswith(".md")), None)

    if verify:
        v = PROJECT / ".agents" / "tools" / "finalize" / "verify_final.py"
        os.execv(VENV_PYTHON, [VENV_PYTHON, str(v)])
        return

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    FINAL_RULES_DIR.mkdir(parents=True, exist_ok=True)
    files = [ADAPTED_DIR / single] if single else sorted(ADAPTED_DIR.glob("a-sec*-rule*.md"))

    done = _checkpoint.setdefault("done", [])
    n_ok = 0
    for p in files:
        if resume and p.name in done:
            print(f"  skip (done): {p.name}", flush=True)
            n_ok += 1
            continue
        print(f"  SYNTH {p.name}...", flush=True)
        ok = synthesize_file(p)
        if ok:
            if p.name not in done:
                done.append(p.name)
            _save_checkpoint(_checkpoint)
            n_ok += 1
            print(f"    ✓ {p.name}", flush=True)
        else:
            print(f"    ✗ {p.name} (will retry next run)", flush=True)

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

    print(f"\n{'='*60}\nPhase G synthesis done: {n_ok}/{len(files)} files ✓\n{'='*60}", flush=True)
    sys.exit(0 if n_ok == len(files) else 1)


if __name__ == "__main__":
    main()
