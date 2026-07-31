#!/usr/bin/env python3
"""md_to_json.py — deterministic markdown→JSON derivation for STE-Code extensions.

The ONLY place JSON is produced for Phase E. Pure parsing, no LLM, no eval/exec
— eliminates the RCE surface that direct JSON generation introduced. Each input
is a markdown file where every entry is a `### <title>` block of
`- **field**: value` lines. We parse those into a list of dicts and write
<name>.json next to the markdown.

Usage:  python3 md_to_json.py ste-code/extensions/verbs.md
        python3 md_to_json.py ste-code/extensions/        (all *.md)
"""
import sys
import re
import json
from pathlib import Path


def parse_entry(block: str) -> dict:
    """Parse one '### title\\n- **field**: value' block into a dict."""
    lines = block.splitlines()
    entry = {}
    # Title = first line, with any leading '#' markers stripped.
    title = lines[0].strip().lstrip("#").strip() if lines else ""
    if title:
        entry["title"] = title
    field_re = re.compile(r"^\s*-\s*\*\*(.+?)\*\*:\s*(.*)$")
    for ln in lines[1:]:
        m = field_re.match(ln)
        if not m:
            continue
        key = m.group(1).strip().lower().replace(" ", "_")
        val = m.group(2).strip()
        # Booleans
        if val.lower() in ("true", "false"):
            val = val.lower() == "true"
        # Comma lists
        elif "," in val and not val.startswith("`"):
            parts = [p.strip() for p in val.split(",") if p.strip()]
            if parts and not any(c in val for c in "[]{}"):
                val = parts
        entry[key] = val
    return entry


def md_to_json(md_path: Path) -> Path:
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    # Split on level-3 headings.
    parts = re.split(r"\n###\s+", text)
    entries = []
    for p in parts:
        if not p.strip():
            continue
        # Skip a leading preamble before the first entry.
        if "**type**:" not in p and "**definition**:" not in p and "**pattern**:" not in p \
           and "**domain**:" not in p:
            # Could still be an entry without those exact keys; but require a field line.
            if not re.search(r"^\s*-\s*\*\*", p, re.M):
                continue
        entries.append(parse_entry(p))
    entries = [e for e in entries if e]
    out = md_path.with_suffix(".json")
    out.write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: md_to_json.py <file.md|dir>", file=sys.stderr)
        sys.exit(2)
    target = Path(sys.argv[1])
    if target.is_dir():
        files = sorted(target.glob("*.md"))
        for f in files:
            out = md_to_json(f)
            print(f"  {f.name} -> {out.name} ({len(json.loads(out.read_text()))} entries)")
    else:
        out = md_to_json(target)
        print(f"  {target.name} -> {out.name} ({len(json.loads(out.read_text()))} entries)")


if __name__ == "__main__":
    main()
