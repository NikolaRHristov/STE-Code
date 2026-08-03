#!/usr/bin/env python3
"""assemble_final.py — consolidate EVERY pipeline stage into ste-code/final/.

This is the true final step: it gathers the output of all stages into one
canonical deliverable directory:

  ste-code/final/
    README.md                master index (what STE-Code is, how to use)
    provenance.md            where each layer came from (audit trail)
    rules/                   enriched adapted rules (Phase D) + cross-refs/traceability (Phase G)
                             + a-categories.md, a-dictionary.md
    extensions/              code-domain vocabulary gap-fills (Phase E)
    reference-catalogue.md   index of vendor/community references (.agents/reference/)
                             — links only, vendor files stay in .agents/reference/

Design: deterministic consolidation (no LLM). References are CATALOGUED, not
copied, per the rule that vendor reference files live outside final/.

Usage:
  python3 assemble_final.py          # consolidate all into ste-code/final/
  python3 assemble_final.py --verify # run verify_final_assembly.py only
"""

import os
import sys
import json
import shutil
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
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
REFINED_DIR = PROJECT / "ste-code" / "refined"
EXT_DIR = PROJECT / "ste-code" / "extensions"
REFERENCE_DIR = PROJECT / ".agents" / "reference"
STATE_DIR = PROJECT / ".agents" / "state"


def _git_commit_locked(files, msg):
    try:
        subprocess.run(
            ["git", "add", "-A", "--", *files],
            cwd=str(PROJECT),
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-q", "-m", msg],
            cwd=str(PROJECT),
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


import subprocess


def consolidate():
    mkdir(FINAL_DIR)
    # 1) rules/ — enriched adapted rules (re-run enrichment deterministically)
    rules_dir = FINAL_DIR / "rules"
    rules_dir.mkdir(exist_ok=True)
    for p in sorted(ADAPTED_DIR.glob("a-sec*-rule*.md")):
        shutil.copy2(p, rules_dir / p.name)
    for extra in ("a-categories.md", "a-dictionary.md"):
        src = ADAPTED_DIR / extra
        if src.exists():
            shutil.copy2(src, rules_dir / extra)
    n_rules = len(list(rules_dir.glob("a-sec*-rule*.md")))

    # 2) extensions/ — Phase E code-domain vocabulary
    ext_dir = FINAL_DIR / "extensions"
    if EXT_DIR.exists():
        ext_dir.mkdir(exist_ok=True)
        for p in sorted(EXT_DIR.glob("*.md")) + sorted(EXT_DIR.glob("*.json")):
            shutil.copy2(p, ext_dir / p.name)
    n_ext = len(list(ext_dir.glob("*.md"))) if ext_dir.exists() else 0

    # 3) reference-catalogue.md — link vendor refs (do NOT copy vendor files)
    cat_lines = [
        "# Reference Catalogue (vendor / community)\n",
        "> These external references inform STE-Code's controlled vocabulary. "
        "They are NOT part of the standard and are kept in `.agents/reference/` "
        "(outside final/) per project rule. Listed here as a catalogue.\n",
        "\n| Reference | Type | Source |\n|---|---|---|",
    ]
    man = REFERENCE_DIR / "manifest.json"
    if man.exists():
        for e in json.load(open(man))["entries"]:
            kind = e.get("kind", "page")
            loc = e.get("local_path") or e.get("url")
            cat_lines.append(f"| {e['title']} | {kind} | [{e['url']}]({loc}) |")
    write_text((FINAL_DIR / "reference-catalogue.md"), "\n".join(cat_lines) + "\n")

    # 4) provenance.md — audit trail of every layer
    prov = [
        "# Provenance — STE-Code pipeline stages\n",
        "\n| Stage | Source dir | Role |",
        "|---|---|---|",
        "| A Extraction | ste-code/extracted/ | PDF spec -> structured pages |",
        "| B Refinement | ste-code/refined/ | formatted dict/rule markdown |",
        "| C Grouping | ste-code/grouped/ | semantic slice+concat of pages |",
        "| D Adaptation | ste-code/adapted/ | code-domain rule rewrite |",
        "| G Enrichment | ste-code/final/rules/ | cross-refs + traceability |",
        "| E Extension | ste-code/extensions/ | code-domain vocabulary gap-fills |",
        "| References | .agents/reference/ | vendor/community vocab (catalogued) |",
        "\nConsolidated into ste-code/final/ by assemble_final.py.\n",
    ]
    write_text((FINAL_DIR / "provenance.md"), "\n".join(prov))

    # 5) README.md — master index
    readme = [
        "# STE-Code — Consolidated Standard (final/)\n",
        "\nSTE-Code is a controlled-language variation of ASD-STE100 for software "
        "documentation. This `final/` directory consolidates every pipeline stage.\n",
        "\n## Contents\n",
        f"- `rules/` — {n_rules} enriched adapted rules + categories + dictionary (Phases D+G)\n",
        f"- `extensions/` — {n_ext} code-domain vocabulary files (Phase E)\n",
        "- `reference-catalogue.md` — vendor/community references (kept in .agents/reference/)\n",
        "- `provenance.md` — stage-by-stage audit trail\n",
        "\n## Use\n",
        "Load `rules/` as the canonical rule set; `extensions/` as the approved "
        "vocabulary; consult `reference-catalogue.md` for external authority.\n",
    ]
    write_text((FINAL_DIR / "README.md"), "\n".join(readme))

    print(f"  ASSEMBLE: rules={n_rules} extensions={n_ext} -> ste-code/final/")
    if not _git_commit_locked(
        [str(FINAL_DIR.relative_to(PROJECT))],
        "Phase G/F: consolidate all stages into ste-code/final/ (rules+extensions+refs+provenance)",
    ):
        print("  ASSEMBLE: commit failed", flush=True)
        return False
    return True


def main():
    if "--verify" in sys.argv:
        v = PROJECT / ".agents" / "tools" / "finalize" / "verify_final_assembly.py"
        os.execv(sys.executable, [sys.executable, str(v)])
        return
    ok = consolidate()
    print(f"\n{'=' * 60}\nAssemble final: {'OK' if ok else 'FAIL'}\n{'=' * 60}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
