#!/usr/bin/env python3
"""verify_extensions.py — post-generation gate for STE-Code Phase E (markdown).

Runs the six deterministic gates from the extension-worker SKILL on every
ste-code/extensions/<area>.md file (and confirms the derived <area>.json matches).
No LLM. Workers emit MARKDOWN only; JSON is derived by md_to_json.py. We verify
the markdown (source of truth) and that the derived JSON parses and is consistent.

Gates:
  1 Markdown present + parses into >= 1 entry (and derived JSON valid)
  2 Required fields present per entry type
  3 Definition length >= 10 words where a definition exists
  4 No fabrication markers (TODO/TBD/FIXME/placeholder/???)
  5 Unique entry titles within a file
  6 STE/non-STE pair quality (verb/adjective: non-STE contains an avoided synonym)

Usage: python3 verify_extensions.py   (exit 0 = pass)
"""

import sys
import re
import json
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
EXT_DIR = PROJECT / "ste-code" / "extensions"

REQUIRED = {
    "verb": [
        "type",
        "category-id",
        "approved",
        "replaces",
        "definition",
        "code_example_ste",
        "code_example_non_ste",
        "source",
    ],
    "adjective": [
        "type",
        "approved",
        "definition",
        "code_example_ste",
        "code_example_non_ste",
        "source",
    ],
    "noun": ["category-id", "category", "term", "definition", "approved", "source"],
    "verb-example": [
        "category-id",
        "verb",
        "context",
        "example_ste",
        "example_non_ste",
        "source",
    ],
    "anti-pattern": [
        "id",
        "pattern",
        "non_ste",
        "ste",
        "violates",
        "severity",
        "context",
    ],
    "domain": ["domain", "term", "definition", "replaces", "source"],
}
AREA_TYPE = {
    "verbs.md": "verb",
    "adjectives.md": "adjective",
    "nouns.md": "noun",
    "verb-examples.md": "verb-example",
    "anti-patterns.md": "anti-pattern",
    "domains.md": "domain",
}
AVOIDED = [
    "utilize",
    "leverage",
    "employ",
    "commence",
    "terminate",
    "initiate",
    "bootstrap",
    "render",
    "generate",
    "obtain",
]


def _entries(md_text):
    parts = re.split(r"\n###\s+", md_text)
    out = []
    for p in parts:
        if not p.strip():
            continue
        if not re.search(r"^\s*-\s*\*\*", p, re.M) and "**type**:" not in p:
            continue
        out.append(p)
    return out


def main():
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", type=Path, default=EXT_DIR)
    args = ap.parse_args()
    ext_dir = args.dir
    problems = []
    files = sorted(ext_dir.glob("*.md")) if ext_dir.exists() else []
    if not files:
        print("verify_extensions: no extensions/ markdown found")
        sys.exit(1)

    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore")
        # Gate 4 (fabrication, checked on raw markdown)
        if re.search(
            r"TODO|TBD|FIXME|placeholder|<\s*PLACEHOLDER\s*>|\?\?\?", text, re.I
        ):
            problems.append(f"Gate4 {f.name}: fabrication marker")
        entries = _entries(text)
        if not entries:
            problems.append(f"Gate1 {f.name}: no entries parsed")
            continue
        etype = AREA_TYPE.get(f.name, "verb")
        required = REQUIRED.get(etype, [])
        seen = set()
        for i, e in enumerate(entries):
            # crude field extraction
            fields = dict(re.findall(r"\*\*(.+?)\*\*:\s*(.+)", e))
            fields = {
                k.strip().lower().replace(" ", "_"): v.strip()
                for k, v in fields.items()
            }
            missing = [k for k in required if k not in fields]
            if missing:
                problems.append(f"Gate2 {f.name}[{i}]: missing {missing}")
            if "definition" in fields and len(fields["definition"].split()) < 10:
                problems.append(f"Gate3 {f.name}[{i}]: definition < 10 words")
            if etype in ("verb", "adjective"):
                ns = fields.get("code_example_non_ste", "")
                if not any(s in ns.lower() for s in AVOIDED):
                    problems.append(
                        f"Gate6 {f.name}[{i}]: non-STE lacks avoided synonym"
                    )
            title = e.strip().splitlines()[0].strip()
            if title in seen:
                problems.append(f"Gate5 {f.name}: duplicate entry '{title}'")
            seen.add(title)
        # Derived JSON consistency (Gate 1b)
        jf = f.with_suffix(".json")
        if not jf.exists():
            problems.append(f"Gate1 {f.name}: derived JSON missing (run md_to_json.py)")
        else:
            try:
                data = json.loads(jf.read_text(encoding="utf-8"))
                if not isinstance(data, list) or len(data) != len(entries):
                    problems.append(
                        f"Gate1 {f.name}: JSON entry count {len(data)} != markdown {len(entries)}"
                    )
            except Exception as ex:
                problems.append(f"Gate1 {f.name}: invalid derived JSON ({ex})")

    print(f"Extension verification over {len(files)} markdown file(s)")
    if problems:
        print(f"FAIL — {len(problems)} problem(s):")
        for p in problems[:40]:
            print(f"  - {p}")
        sys.exit(1)
    print("verify-extensions: PASS (all gates)")
    sys.exit(0)


if __name__ == "__main__":
    main()
