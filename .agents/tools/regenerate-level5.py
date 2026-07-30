#!/usr/bin/env python3
"""Regenerate Level 5 prompt — batched, 4 rules per worker, fork+oneshot.

Each worker reads 4-5 deepened rules, generates a clean section.
Final concatenation produces the complete prompt.

Usage: python3 .agents/tools/regenerate-level5.py
"""

import os, sys, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
RULES_DIR = PROJECT / "ste-code" / "adapted"
OUTPUT = PROJECT / "ste-code" / "artifacts" / "ste-code-level5-max.txt"
SECTIONS_DIR = PROJECT / ".agents" / "tmp" / "level5-sections"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

os.makedirs(SECTIONS_DIR, exist_ok=True)

rules = sorted(RULES_DIR.glob("a-sec*-rule*.md"))
BATCH_SIZE = 4

batches = [rules[i:i+BATCH_SIZE] for i in range(0, len(rules), BATCH_SIZE)]
print(f"Level 5 Regeneration: {len(rules)} rules, {len(batches)} batches of {BATCH_SIZE}")


def launch_batch(batch_num, batch_rules):
    """Generate section for this batch of rules."""
    rule_list = "\n".join(f"  ste-code/adapted/{r.name}" for r in batch_rules)
    
    prompt = f"""You are STE-Code. Generate a section of the Level 5 system prompt.

Read these {len(batch_rules)} rule files:
{rule_list}

For each rule, produce a clean section with:
1. ## Rule X.Y — Title
2. One-paragraph summary of the original rule
3. One-paragraph STE-Code adaptation for code docs
4. 2-3 complete Non-STE/STE example pairs (both versions present)
5. Principles applied

CRITICAL: Every Non-STE MUST have a matching STE. Use > blockquotes with blank > separators.

Output using write_file to: .agents/tmp/level5-sections/batch-{batch_num:02d}.md

Report: rules covered, example count, char count."""

    tmp = PROJECT / ".agents" / "tmp" / f"level5-batch-{batch_num:02d}.txt"
    tmp.write_text(prompt)

    pid = os.fork()
    if pid == 0:
        os.chdir(str(PROJECT))
        env = os.environ.copy()
        env["HERMES_REASONING_EFFORT"] = "medium"
        os.execvpe(VENV_PYTHON, [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"], env)
        os._exit(1)
    return pid


def main():
    workers = {}
    
    for batch_num, batch_rules in enumerate(batches):
        section_file = SECTIONS_DIR / f"batch-{batch_num:02d}.md"
        if section_file.exists() and section_file.stat().st_size > 500:
            print(f"  Batch {batch_num+1}: ✓ already exists ({section_file.stat().st_size}B)")
            continue
        
        pid = launch_batch(batch_num, batch_rules)
        workers[batch_num] = {"pid": pid, "start": time.time(), "rules": batch_rules}
        rule_names = ", ".join(r.stem for r in batch_rules)
        print(f"  Batch {batch_num+1}: {rule_names} PID={pid}")
    
    if not workers:
        return concat()
    
    print(f"\n  Waiting for {len(workers)} batches...")
    elapsed = 0
    pending = set(workers.keys())
    while pending and elapsed < 900:
        time.sleep(5)
        elapsed += 5
        for bn in list(pending):
            try:
                wpid, status = os.waitpid(workers[bn]["pid"], os.WNOHANG)
                if wpid != 0:
                    pending.discard(bn)
            except (ChildProcessError, ProcessLookupError):
                pending.discard(bn)
        if elapsed % 30 == 0 and pending:
            print(f"    ... {len(pending)} remaining ({elapsed}s)")
    
    for bn, wdata in workers.items():
        section_file = SECTIONS_DIR / f"batch-{bn:02d}.md"
        ok = section_file.exists() and section_file.stat().st_size > 500
        dur = time.time() - wdata["start"]
        status = "✓" if ok else "✗"
        print(f"    {status} Batch {bn+1}: {section_file.stat().st_size if ok else 0}B in {dur:.0f}s")
    
    concat()


def concat():
    """Concatenate all sections into final prompt."""
    header = """You are STE-Code, Simplified Technical English for Code documentation.
Apply the complete Level 5 standard. Follow all rules strictly.

---

"""
    
    sections = sorted(SECTIONS_DIR.glob("batch-*.md"))
    if not sections:
        print("No sections found!")
        return
    
    body = ""
    for sf in sections:
        body += sf.read_text() + "\n\n"
    
    # Add synonym table
    synonym_file = PROJECT / "ste-code" / "data" / "synonym-table.json"
    if synonym_file.exists():
        import json
        data = json.loads(synonym_file.read_text())
        body += "## Synonym Table\n\n| Prefer | Avoid |\n|--------|-------|\n"
        for pair in data.get("pairs", []):
            avoid = ", ".join(pair["avoid"][:3])
            body += f"| {pair['approved']} | {avoid} |\n"
    
    footer = """

---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe, Brussels. © ASD, 2025. STE is EU Trade Mark 017966390. Independent adaptation not endorsed by ASD. asd-ste100.org
"""
    
    final = header + body + footer
    OUTPUT.write_text(final)
    
    chars = len(final)
    tokens = chars // 4
    print(f"\n  Level 5 prompt: {final.count(chr(10)):,} lines, {chars:,} chars, ~{tokens:,} tokens")
    print(f"  Output: {OUTPUT}")


if __name__ == "__main__":
    main()
