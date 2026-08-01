#!/usr/bin/env python3
"""Deterministically add the missing `Source: master.md#secN-ruleX.Y` backlink
to adapted rule files that lack it. The backlink target is derived from the
filename (a-sec<N>-rule<X.Y>.md -> master.md#sec<N>-rule<X.Y>), so this is a
pure, lossless insert — no LLM, no content change. Idempotent: skips files
that already have the anchor.

Run from repo root: python3 .agents/tmp/hermes-add-backlinks.py
"""
import re, glob, os

def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    for _ in range(8):
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return cur

ROOT = _repo_root()
ADAPTED = os.path.join(ROOT, "ste-code", "adapted")

# a-sec{N}-rule{X.Y}.md  ->  sec{N}-rule{X.Y}
NAME_RE = re.compile(r"a-sec(\d+)-rule([\d.]+)\.md$")

added = 0
for path in sorted(glob.glob(os.path.join(ADAPTED, "a-sec*-rule*.md"))):
    name = os.path.basename(path)
    m = NAME_RE.search(name)
    if not m:
        continue
    sec, rule = m.group(1), m.group(2)
    anchor = f"master.md#sec{sec}-rule{rule}"
    text = open(path, encoding="utf-8", errors="ignore").read()
    if anchor in text:
        continue  # already has it
    # Insert a backlink line right after the existing '> **Source:** Adapted from...' line.
    src_line = "> **Source:** Adapted from ASD-STE100 Issue 9"
    backlink = f"> **Source:** [{anchor}](ste-code/grouped/)"
    if src_line in text:
        text = text.replace(src_line, src_line + "\n" + backlink, 1)
    else:
        # Fallback: prepend the backlink near the top (after the H1).
        lines = text.splitlines()
        insert_at = 1 if lines and lines[0].startswith("# ") else 0
        lines.insert(insert_at, backlink)
        text = "\n".join(lines)
    open(path, "w", encoding="utf-8").write(text)
    added += 1
    print(f"  + {name}: added {anchor}")

print(f"\nAdded backlinks to {added} file(s).")
