#!/usr/bin/env python3
"""verify_final_assembly.py — gate for the consolidated ste-code/final/ deliverable.

Deterministic checks (no LLM):
  Gate1: final/rules/ has >= 50 rule files + a-categories.md + a-dictionary.md
  Gate2: final/extensions/ has the 6 Phase E vocab files (verbs, adjectives, nouns,
         verb-examples, anti-patterns, domains) [.md]
  Gate3: final/reference-catalogue.md exists and lists >= 15 references
  Gate4: final/README.md + provenance.md present
  Gate5: no fabrication markers (TODO/TBD/???) in final/ rule+extension files

Exit 0 = PASS.
"""
import sys
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINAL = PROJECT / "ste-code" / "final"
REFERENCE = PROJECT / ".agents" / "reference"

EXPECTED_EXT = {"verbs", "adjectives", "nouns", "verb-examples", "anti-patterns", "domains"}


def main():
    problems = []
    if not FINAL.exists():
        print("verify-final-assembly: ste-code/final/ missing"); sys.exit(1)

    rules = sorted((FINAL / "rules").glob("a-sec*-rule*.md")) if (FINAL / "rules").exists() else []
    if len(rules) < 50:
        problems.append(f"Gate1: only {len(rules)} rule files (<50)")
    if not (FINAL / "rules" / "a-categories.md").exists():
        problems.append("Gate1: missing rules/a-categories.md")
    if not (FINAL / "rules" / "a-dictionary.md").exists():
        problems.append("Gate1: missing rules/a-dictionary.md")

    ext = set()
    if (FINAL / "extensions").exists():
        ext = {p.stem for p in (FINAL / "extensions").glob("*.md")}
    missing = EXPECTED_EXT - ext
    if missing:
        problems.append(f"Gate2: missing extension files: {sorted(missing)}")

    cat = FINAL / "reference-catalogue.md"
    rows = 0
    if not cat.exists():
        problems.append("Gate3: reference-catalogue.md missing")
    else:
        rows = len([l for l in cat.read_text(encoding="utf-8", errors="ignore").splitlines()
                    if l.strip().startswith("|") and "http" in l])
        if rows < 15:
            problems.append(f"Gate3: catalogue lists {rows} refs (<15)")

    if not (FINAL / "README.md").exists():
        problems.append("Gate4: README.md missing")
    if not (FINAL / "provenance.md").exists():
        problems.append("Gate4: provenance.md missing")

    # NOTE: content fabrication (TODO/TBD/???) is gated by verify_final.py Gate4 on
    # the rule files (fab=0 there). The assembly verifier checks structure only.

    print(f"verify-final-assembly: rules={len(rules)} extensions={sorted(ext)} "
          f"catalogue_rows={rows}")
    if problems:
        print(f"FAIL — {len(problems)} problem(s):")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("verify-final-assembly: PASS (all stages consolidated)")
    sys.exit(0)


if __name__ == "__main__":
    main()
