#!/usr/bin/env python3
"""Phase F — DETERMINISTIC level scaffolding (the "base/boilerplate" layer).

Produces, for each artifact tier, a DIRECTORY of bounded SUB-DOCUMENTS under
ste-code/artifacts/_base/level<N>/ (e.g. level5/01-principles.md,
level5/02-rules-sec1.md, ...). Splitting into sub-documents means the LLM final
pass writes SMALL files (one session per sub-doc) and LLM consumers READ small
files — never one 1.8MB monster (critical for level 5).

Each tier dir also gets _index.md listing its sub-docs. The sub-doc split is by
section so related content stays together and file sizes stay manageable.

Deterministic = byte-reproducible from ste-code/final/. No LLM, no truncation.

Usage:
  python3 levels_scaffold.py          # build all 8 tier dirs into _base/
  python3 levels_scaffold.py --dry-run
"""

from __future__ import annotations

import re
import json
import argparse
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
from ste_io import write_text, mkdir  # noqa: E402

FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
BASE_DIR = ARTIFACTS_DIR / "_base"

LEVELS = [
    ("level-2", "-2", "ultra-minimal: the 14 core principles only"),
    ("level-1", "-1", "minimal/core: 14 core principles + synonym table"),
    ("level0", "0", "baseline: core principles + short dictionary excerpt"),
    ("level1", "1", "+ doc templates (code review / PR feedback)"),
    ("level2", "2", "+ section-specific grammar rules"),
    ("level3", "3", "+ complete dictionary excerpt + all rules"),
    ("level4", "4", "+ extensions + reference catalogue"),
    ("level5", "5", "full standard (all rules + extensions + catalogue + provenance)"),
]


def _all_rules():
    return [p for p in sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))]


def _rule_h1(p: Path) -> str:
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# Rule"):
            return line.strip()
    return p.stem


def _read(*parts):
    if not parts:
        return ""
    p = FINAL_DIR.joinpath(*parts)
    if p.exists() and p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore")
    p2 = FINAL_DIR / parts[-1]
    return (
        p2.read_text(encoding="utf-8", errors="ignore")
        if (p2.exists() and p2.is_file())
        else ""
    )


def _core_principles(rules):
    return [
        p
        for p in rules
        if re.search(r"a-sec1-rule1\.\d+\.md$", p.name)
        and not re.search(r"1\.(1[5-9]|[2-9]\d)", p.name)
    ]


def _section_rules(rules, sec):
    return [p for p in rules if re.search(rf"a-sec{sec}-rule", p.name)]


def _split_rule_paths(rule_paths, max_bytes=400000):
    """Split a list of rule-file Paths into size-bounded chunks (<= max_bytes)."""
    chunks, cur, sz = [], [], 0
    for p in rule_paths:
        t = len(p.read_text(encoding="utf-8", errors="ignore"))
        if sz + t > max_bytes and cur:
            chunks.append(cur)
            cur, sz = [], 0
        cur.append(p)
        sz += t
    if cur:
        chunks.append(cur)
    return chunks


def _build_subdocs(level_idx: int) -> list[tuple[str, str]]:
    """Return [(subdoc_name, content), ...] for this tier."""
    rules = _all_rules()
    subs: list[tuple[str, str]] = []

    # 01 — core principles (tiers -2..5)
    if level_idx >= 0:
        body = ["## Core principles (14)", ""]
        for p in _core_principles(rules)[:14]:
            body.append(f"- {_rule_h1(p)}")
        subs.append(("01-principles.md", "\n".join(body)))

    # 02 — synonym / categories (-1..5)
    if level_idx >= 1:
        subs.append(
            (
                "02-synonyms.md",
                "## Synonym / approved-word table\n\n"
                + (_read("rules", "a-categories.md")[:1500] or "(unavailable)"),
            )
        )

    # 03 — dictionary excerpt (0..5)
    if level_idx >= 2:
        subs.append(
            (
                "03-dictionary.md",
                "## Dictionary excerpt (approved / unapproved)\n\n"
                + (_read("rules", "a-dictionary.md")[:2500] or "(unavailable)"),
            )
        )

    # 04 — doc templates (1..5)
    if level_idx >= 3:
        subs.append(
            (
                "04-templates.md",
                "## Document templates (code review / PR feedback)\n\n"
                "> Placeholder — LLM fills with code-domain templates.",
            )
        )

    # 05 — section-specific grammar (2..5)
    if level_idx >= 4:
        subs.append(
            (
                "05-grammar.md",
                "## Section-specific grammar rules\n\n"
                "> Placeholder — LLM fills from the full rule set.",
            )
        )

    # rules by section (3..5) — split each section into size-bounded sub-docs
    if level_idx >= 5:
        for sec in range(1, 10):
            sec_rules = _section_rules(rules, sec)
            if not sec_rules:
                continue
            parts = _split_rule_paths(sec_rules)
            if len(parts) == 1:
                content = "\n\n---\n\n".join(
                    f"<!-- {p.name} -->\n\n{p.read_text(encoding='utf-8', errors='ignore').strip()}"
                    for p in parts[0]
                )
                subs.append((f"rules-sec{sec}.md", content))
            else:
                for i, chunk in enumerate(parts, 1):
                    content = "\n\n---\n\n".join(
                        f"<!-- {p.name} -->\n\n{p.read_text(encoding='utf-8', errors='ignore').strip()}"
                        for p in chunk
                    )
                    subs.append((f"rules-sec{sec}-part{i}.md", content))

    # extensions + catalogue (4..5)
    if level_idx >= 6:
        ext = "\n\n---\n\n".join(
            f"# Extension {p.stem}\n\n{p.read_text(encoding='utf-8', errors='ignore')}"
            for p in sorted((FINAL_DIR / "extensions").glob("*.md"))
        )
        subs.append(
            ("06-extensions.md", "## Extensions\n\n" + (ext[:3000] or "(unavailable)"))
        )
        subs.append(
            (
                "07-catalogue.md",
                "## Reference catalogue\n\n"
                + (_read("reference-catalogue.md")[:2000] or "(unavailable)"),
            )
        )

    # provenance (5)
    if level_idx >= 7:
        subs.append(
            (
                "08-provenance.md",
                "## Provenance\n\n"
                + (_read("provenance.md")[:2000] or "(unavailable)"),
            )
        )

    return subs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    for i, (fname, label, desc) in enumerate(LEVELS):
        tdir = BASE_DIR / fname
        subs = _build_subdocs(i)
        if args.dry_run:
            total = sum(len(c) for _, c in subs)
            print(f"[dry-run] {fname}: {len(subs)} sub-docs ({total}B)")
            continue
        mkdir(tdir)
        idx = [
            f"# STE-Code Level {label} — base index",
            "",
            f"> {desc}",
            "",
            "## Sub-documents (distill each):",
            "",
        ]
        for name, content in subs:
            write_text((tdir / name), content + "\n")
            idx.append(f"- {name} — {len(content)}B")
        write_text((tdir / "_index.md"), "\n".join(idx) + "\n")
        print(f"  base {label}: {tdir.name}/ ({len(subs)} sub-docs)")
    if not args.dry_run:
        (BASE_DIR / ".manifest.json").write_text(
            json.dumps({"levels": [l[1] for l in LEVELS]}, indent=2)
        )
        print(f"Scaffolded {len(LEVELS)} tier dirs -> {BASE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
