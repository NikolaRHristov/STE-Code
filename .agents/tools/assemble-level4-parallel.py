#!/usr/bin/env python3
"""Level 4 Assembly — PARALLEL: multiple workers batch-process rules + dictionary.

Each worker handles a small slice (~7-12 rules or ~800 dict lines).
All workers run in parallel, results combined at the end.
No single worker times out.

Usage: python3 .agents/tools/assemble-level4-parallel.py [--dry-run]
Output: ste-code/artifacts/level4/system-prompt.txt (~50K tokens)
"""

import os, sys, subprocess, time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"
LEVEL4_DIR = PROJECT / "ste-code" / "artifacts" / "level4"
TMP_DIR = PROJECT / ".agents" / "tmp"
OUTPUT = LEVEL4_DIR / "system-prompt.txt"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"
SYNONYM_TABLE = PROJECT / "ste-code" / "data" / "synonym-table.json"
DICTIONARY = PROJECT / "ste-code" / "adapted" / "a-dictionary.md"

os.makedirs(LEVEL4_DIR, exist_ok=True)
os.makedirs(TMP_DIR, exist_ok=True)


def get_rule_summaries(section_filter=None):
    """Get all Level 5 rule summaries, optionally filtered by section(s)."""
    summaries = sorted(LEVEL5_DIR.glob("sec*/a-sec*/summary.md"))
    sections = {}
    for sf in summaries:
        sec = sf.parent.parent.name  # sec1, sec2, etc.
        if section_filter and sec not in section_filter:
            continue
        if sec not in sections:
            sections[sec] = []
        sections[sec].append(str(sf.relative_to(PROJECT)))
    return sections


def launch_worker(prompt_text, output_file, label, timeout=300):
    """Launch a single oneshot worker. Returns subprocess.Popen."""
    tmp = TMP_DIR / f"level4-{label}.txt"
    tmp.write_text(prompt_text, encoding="utf-8")

    proc = subprocess.Popen(
        [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"],
        cwd=str(PROJECT),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={**os.environ, "HERMES_REASONING_EFFORT": "high"},
    )
    return proc, tmp, timeout


def build_rule_batch_prompt(sections, label, batch_name):
    """Build a prompt for a rule batch worker."""
    input_list = ""
    for sec in sorted(sections):
        input_list += f"\n## Section {sec.replace('sec', '')}\n"
        for s in sections[sec]:
            input_list += f"  {s}\n"

    rule_count = sum(len(v) for v in sections.values())

    return f"""You are STE-Code. Process ONLY the {rule_count} rule summaries listed below.

READ these files from the Level 5 directory tree:
{input_list}

For each rule, output a compact block with:
1. **Rule X.Y — Title** (bold header)
2. What the rule requires (2-3 sentences)
3. Two complete Non-STE/STE example pairs (each pair labeled with ``` blocks):

Format exactly:
```
### Section N — SectionName

**Rule X.Y — Rule Title**
Description paragraph (2-3 sentences explaining the rule).

> **Non-STE:** first non-ste example text.
> **STE:** first ste correction text.

> **Non-STE:** second non-ste example text.
> **STE:** second ste correction text.
```

CRITICAL:
- Every Non-STE MUST have a complete STE correction
- Use code-domain examples (APIs, functions, commits, README, etc.)
- Write ONLY the rules section — no header, no footer, no intro
- Save to: {LEVEL4_DIR / f'rules-{label}.md'}
- Use write_file tool
- Report: "{label} done: N rules" then STOP
"""


def build_dict_batch_prompt(line_start, line_end, label, batch_label):
    """Build a prompt for a dictionary batch worker."""
    return f"""You are STE-Code. Process a DICTIONARY SLICE from the STE-Code Adapted Dictionary.

READ the file ste-code/adapted/a-dictionary.md, lines {line_start}-{line_end}.
This is a 5,943-line dictionary of approved/unapproved words for code documentation.

EXTRACT all approved word entries (UPPERCASE words with definitions) from these lines.
For each approved word, output in this compact format:

```
**WORD (pos)** — Approved meaning (1 sentence). Code-domain example sentence. Unapproved: "alt1," "alt2."
```

Include ONLY approved words (UPPERCASE). Skip unapproved-only entries (lowercase).
Include the letter section headers (### A, ### B, etc.) as they appear.

CRITICAL:
- Be exhaustive — extract EVERY approved word in the given line range
- Each entry must be 1-2 lines maximum
- Code-domain examples (APIs, functions, commits, CLI, etc.)
- Save to: {LEVEL4_DIR / f'dict-{label}.md'}
- Use write_file tool
- When done, report: "{label} done: extracted N entries" then STOP
"""


def build_synonym_prompt():
    """Build a prompt for the synonym table worker."""
    return f"""You are STE-Code. Extract and format the synonym table.

READ ste-code/data/synonym-table.json — extract the complete synonym table.

Format as a markdown table:
```
| Approved | Avoid |
|---|---|
| about | concerning, regarding, with respect to |
...
```

Then also create the Output Rules section with:
- Active Voice rules
- Sentence Length rules
- Imperative Mood rules
- No Contractions
- No Semicolons
- No Slang or Jargon
- No Phrasal Verbs
- Consistent Terminology
- Anti-Patterns list (all of them)
- Formatting rules
- Word Count rules
- American English spelling rules
- Verification Checklist (10 items)

CRITICAL:
- Be thorough — every output rule from the STE-Code standard
- Save to: {LEVEL4_DIR / 'synonym-output.md'}
- Use write_file tool
- Report: "synonym/output done: N synonyms, M output rules" then STOP
"""


def combine_parts():
    """Combine all partial outputs into the final system-prompt.txt."""
    header = """## STE-Code Level 4 — Standard Compliance

STE-Code adapts ASD-STE100 Issue 9 (Simplified Technical English) to the code documentation domain. It provides a controlled vocabulary (approved words with restricted meanings), 51 grammar and style rules organized into 9 sections, and a synonym table mapping common unapproved coding terms to approved STE-Code replacements. The system ensures that every README file, API doc, docstring, commit message, error message, and inline comment is unambiguous, translatable, and understandable by developers of all English proficiency levels — without sacrificing technical precision.

---

## Rules (51 rules)

"""

    footer = """
---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. © ASD, 2025.
> STE is EU Trade Mark 017966390. Independent adaptation for code documentation.
> STE-Code Level 4 System Prompt — assembled from parallel batch workers.
"""

    parts = []
    # Rules parts in order
    for label in ["s1-3", "s4-6", "s7-9"]:
        f = LEVEL4_DIR / f"rules-{label}.md"
        if f.exists():
            parts.append(f.read_text(encoding="utf-8"))

    # Add separator before synonym/output
    parts.append("\n---\n\n## Synonym Table\n\n")
    sf = LEVEL4_DIR / "synonym-output.md"
    if sf.exists():
        parts.append(sf.read_text(encoding="utf-8"))

    # Dictionary parts in order
    for label in ["a-d", "e-l", "m-r", "s-z"]:
        f = LEVEL4_DIR / f"dict-{label}.md"
        if f.exists():
            if not parts[-1].startswith("\n## Dictionary"):
                parts.append("\n---\n\n## Dictionary Excerpt\n\n")
            parts.append(f.read_text(encoding="utf-8"))

    # Build final
    final = header + "\n".join(parts) + footer
    OUTPUT.write_text(final, encoding="utf-8")
    return final


def main():
    dry_run = "--dry-run" in sys.argv

    # ── Define batches ──
    rule_batches = [
        ("s1-3", ["sec1", "sec2", "sec3"], "Sections 1-3"),
        ("s4-6", ["sec4", "sec5", "sec6"], "Sections 4-6"),
        ("s7-9", ["sec7", "sec8", "sec9"], "Sections 7-9"),
    ]

    dict_batches = [
        ("a-d", 1, 800, "Dictionary A-D"),
        ("e-l", 801, 1800, "Dictionary E-L"),
        ("m-r", 1801, 3200, "Dictionary M-R"),
        ("s-z", 3201, 5943, "Dictionary S-Z"),
    ]

    # ── Generate prompts ──
    procs = []

    for label, sections, name in rule_batches:
        rule_sections = get_rule_summaries(section_filter=sections)
        prompt = build_rule_batch_prompt(rule_sections, label, name)
        print(f"[{label}] {sum(len(v) for v in rule_sections.values())} rules, {len(prompt)} chars")
        if not dry_run:
            proc, tmp, timeout = launch_worker(prompt, None, label, timeout=300)
            procs.append((label, proc, timeout, name))

    for label, l_start, l_end, name in dict_batches:
        prompt = build_dict_batch_prompt(l_start, l_end, label, name)
        print(f"[{label}] Dict lines {l_start}-{l_end}, {len(prompt)} chars")
        if not dry_run:
            proc, tmp, timeout = launch_worker(prompt, None, label, timeout=300)
            procs.append((label, proc, timeout, name))

    # Synonym/Output batch
    prompt = build_synonym_prompt()
    print(f"[syn] Synonym/Output rules, {len(prompt)} chars")
    if not dry_run:
        proc, tmp, timeout = launch_worker(prompt, None, "syn", timeout=300)
        procs.append(("syn", proc, timeout, "Synonym + Output Rules"))

    if dry_run:
        print(f"\nWould launch {len(procs)} workers in parallel")
        return

    # ── Launch all, wait for completion ──
    print(f"\nLaunched {len(procs)} workers. Waiting...\n")

    start_time = time.time()
    results = {}

    while procs:
        for label, proc, timeout, name in list(procs):
            elapsed = time.time() - start_time
            ret = proc.poll()
            if ret is not None:
                stdout = proc.stdout.read().decode("utf-8", errors="replace")
                stderr = proc.stderr.read().decode("utf-8", errors="replace")
                status = "OK" if ret == 0 else f"FAIL({ret})"
                print(f"[{label}] {status} ({elapsed:.0f}s) {name}")
                if stdout.strip():
                    print(f"  stdout: {stdout.strip()[-200:]}")
                if stderr.strip():
                    print(f"  stderr: {stderr.strip()[-200:]}")
                results[label] = {"exit": ret, "stdout": stdout, "stderr": stderr}
                procs.remove((label, proc, timeout, name))
            elif elapsed > timeout:
                print(f"[{label}] TIMEOUT ({elapsed:.0f}s) — killing {name}")
                proc.kill()
                try:
                    stdout, stderr = proc.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    stdout, stderr = b"", b""
                results[label] = {"exit": -1, "stdout": stdout.decode("utf-8", errors="replace"),
                                   "stderr": stderr.decode("utf-8", errors="replace")}
                procs.remove((label, proc, timeout, name))

        if procs:
            time.sleep(5)

    print(f"\n{'='*50}")
    print(f"All workers done in {time.time()-start_time:.0f}s")

    # ── Combine ──
    final = combine_parts()
    chars = len(final)
    print(f"\nCombined output: {chars:,} chars (~{chars//4:,} tokens)")
    print(f"Saved to: {OUTPUT}")

    # ── Check which parts exist ──
    for label in ["s1-3", "s4-6", "s7-9", "a-d", "e-l", "m-r", "s-z", "syn"]:
        prefix = "rules" if label.startswith("s") else "dict" if label[0].islower() else "synonym"
        if prefix == "synonym":
            f = LEVEL4_DIR / "synonym-output.md"
        elif prefix == "rules":
            f = LEVEL4_DIR / f"rules-{label}.md"
        else:
            f = LEVEL4_DIR / f"dict-{label}.md"
        size = f.stat().st_size if f.exists() else 0
        print(f"  {label:6s}: {'✓' if size else '✗'} {size:>8,} chars")


if __name__ == "__main__":
    main()
