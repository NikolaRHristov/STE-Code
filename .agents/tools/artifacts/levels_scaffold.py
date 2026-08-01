#!/usr/bin/env python3
"""Phase F — DETERMINISTIC level scaffolding (the "base/boilerplate" layer).

Produces one BASE markdown file per artifact tier under
ste-code/artifacts/_base/level<N>.base.md. These are the structural skeletons /
deterministic extracts the LLM final-distillation pass (synthesize_artifacts.py)
reads and turns into LLM-optimized artifacts. Keeping the level separation and
boilerplate deterministic means the ONLY thing the LLM does is DISTILL — it never
has to reconstruct structure or decide what belongs in each tier.

Tiers (weakest -> richest), identical scheme to synthesize_artifacts.py:
  -2  ultra-minimal: 14 core principles only
  -1  minimal/core: 14 core principles + synonym table
   0  baseline: core principles + short dictionary excerpt
   1  + doc templates (code review / PR feedback)
   2  + section-specific grammar rules
   3  + complete dictionary excerpt + all rules
   4  + extensions + reference catalogue
   5  full standard (all rules + extensions + catalogue + provenance)

Deterministic = byte-reproducible from ste-code/final/. No LLM, no truncation,
no content-loss risk.

Usage:
  python3 levels_scaffold.py          # build all 8 bases into _base/
  python3 levels_scaffold.py --dry-run
"""
from __future__ import annotations

import re
import json
import argparse
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
BASE_DIR = ARTIFACTS_DIR / "_base"

LEVELS = [
    ("level-2.md", "-2", "ultra-minimal: the 14 core principles only"),
    ("level-1.md", "-1", "minimal/core: 14 core principles + synonym table"),
    ("level0.md",  "0",  "baseline: core principles + short dictionary excerpt"),
    ("level1.md",  "1",  "+ doc templates (code review / PR feedback)"),
    ("level2.md",  "2",  "+ section-specific grammar rules"),
    ("level3.md",  "3",  "+ complete dictionary excerpt + all rules"),
    ("level4.md",  "4",  "+ extensions + reference catalogue"),
    ("level5.md",  "5",  "full standard (all rules + extensions + catalogue + provenance)"),
]


def _all_rules():
    return [p for p in sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))]


def _rule_h1(p: Path) -> str:
    for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("# Rule"):
            return line.strip()
    return p.stem


def _core_principles(rules):
    """Extract the 14 core-principle rules (sec1 rules 1.1..1.14)."""
    return [p for p in rules if re.search(r"a-sec1-rule1\.\d+\.md$", p.name)
            and not re.search(r"1\.(1[5-9]|[2-9]\d)", p.name)]


def _read(*parts):
    """Read FINAL_DIR/<parts[0]>/<parts[1]>/.../<parts[-1]>; fall back to
    FINAL_DIR/<parts[-1]> if that exists; else empty string."""
    if not parts:
        return ""
    p = FINAL_DIR.joinpath(*parts)
    if p.exists() and p.is_file():
        return p.read_text(encoding="utf-8", errors="ignore")
    p2 = FINAL_DIR / parts[-1]
    return p2.read_text(encoding="utf-8", errors="ignore") if (p2.exists() and p2.is_file()) else ""


def _build_base(level_idx: int) -> str:
    rules = _all_rules()
    lines = [f"<!-- BASE scaffold for tier {LEVELS[level_idx][1]} — deterministic; LLM distills this -->",
             "", f"# STE-Code — Level {LEVELS[level_idx][1]} (base)", "",
             f"> Base/boilerplate for: {LEVELS[level_idx][2]}", "",
             "This file is the DETERMINISTIC base. The LLM final pass distills it",
             "into an LLM-optimized artifact adapted to the STE-Code spec.", "", "---", ""]

    # core principles for -2..5
    if level_idx >= 0:
        lines += ["## Core principles (14)", ""]
        for p in _core_principles(rules)[:14]:
            lines.append(f"- {_rule_h1(p)}")
        lines.append("")

    if level_idx >= 1:  # -1 +
        lines += ["## Synonym / approved-word table",
                  "", _read("rules", "a-categories.md")[:1500] or "(categories unavailable)", ""]
    if level_idx >= 2:  # 0 +
        lines += ["## Dictionary excerpt (approved / unapproved)", "",
                  _read("rules", "a-dictionary.md")[:2500] or "(dictionary unavailable)", ""]
    if level_idx >= 3:  # 1 +
        lines += ["## Document templates (code review / PR feedback)",
                  "", "> Placeholder section — LLM fills with code-domain templates.", ""]
    if level_idx >= 4:  # 2 +
        lines += ["## Section-specific grammar rules",
                  "", "> Placeholder section — LLM fills from the full rule set.", ""]
    if level_idx >= 5:  # 3 +
        lines += ["## All rules (full)", ""]
        for p in rules:
            lines.append(f"<!-- {p.name} -->")
            lines.append(p.read_text(encoding="utf-8", errors="ignore").strip())
            lines.append("")
        lines.append("")
    if level_idx >= 6:  # 4 +
        lines += ["## Code-domain vocabulary extensions",
                  "", _read("extensions", "adjectives.md")[:2000] or "(extensions unavailable)", "",
                  "## Reference catalogue", "",
                  _read("reference-catalogue.md")[:2000] or "(catalogue unavailable)", ""]
    if level_idx >= 7:  # 5
        lines += ["## Provenance", "", _read("provenance.md")[:2000] or "(provenance unavailable)", ""]

    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    BASE_DIR.mkdir(parents=True, exist_ok=True)
    for i, (fname, label, desc) in enumerate(LEVELS):
        base = _build_base(i)
        out = BASE_DIR / fname.replace(".md", ".base.md")
        if args.dry_run:
            print(f"[dry-run] would write {out.name} ({len(base)}B)")
            continue
        out.write_text(base, encoding="utf-8")
        print(f"  base {label}: {out.name} ({len(base)}B)")
    if not args.dry_run:
        (BASE_DIR / ".manifest.json").write_text(
            json.dumps({"levels": [l[1] for l in LEVELS]}, indent=2))
        print(f"Scaffolded {len(LEVELS)} bases -> {BASE_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
