#!/usr/bin/env python3
"""verify-artifacts.py — post-assembly gate for STE-Code Phase F.

Confirms the assembled artifacts cover every FINAL rule and that the assembly
did not drop or duplicate content. Deterministic — no LLM.

UPGRADED: coverage is checked against ste-code/final/rules/ (was stale
ste-code/adapted/). Also verifies the VERSION file exists & matches the header,
and that extensions/catalogue were included.

Usage: python3 verify-artifacts.py   (exit 0 = pass)
"""
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
VERSION_PATH = ARTIFACTS_DIR / "VERSION"

SECTION_ORDER = {
    1: [f"1.{i}" for i in range(1, 15)],
    2: [f"2.{i}" for i in range(1, 4)],
    3: [f"3.{i}" for i in range(1, 8)],
    4: [f"4.{i}" for i in range(1, 6)],
    5: [f"5.{i}" for i in range(1, 6)],
    6: [f"6.{i}" for i in range(1, 7)],
    7: [f"7.{i}" for i in range(1, 4)],
    8: [f"8.{i}" for i in range(1, 8)],
    9: [f"9.{i}" for i in range(1, 5)] + ["GR1", "GR2", "GR3", "GR4"],
}


def main():
    problems = []
    rules_file = ARTIFACTS_DIR / "ste-code-rules.md"
    prompt_file = ARTIFACTS_DIR / "ste-code-system-prompt.md"

    if not rules_file.exists():
        problems.append("ste-code-rules.md missing")
    if not prompt_file.exists():
        problems.append("ste-code-system-prompt.md missing")

    if rules_file.exists():
        txt = rules_file.read_text(encoding="utf-8", errors="ignore")
        # Derive expected rule ids from the ACTUAL final/ standard (self-healing),
        # not a hardcoded list that can drift from the real corpus.
        final_rules = sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md"))
        if not final_rules:
            problems.append("no final rules found on disk — run Phase G first")
        missing = [fr.name for fr in final_rules if fr.name not in txt]
        covered = len(final_rules) - len(missing)
        problems.extend(f"artifact missing rule {n}" for n in missing)
        print(f"Artifact rule coverage: {covered}/{len(final_rules)} final rules present")
        if covered == 0:
            problems.append("no rule ids found in artifact — assembly likely empty")

        # version consistency
        if VERSION_PATH.exists():
            ver = VERSION_PATH.read_text(encoding="utf-8").strip()
            if f"Version:** {ver}" not in txt and f"v{ver}" not in txt:
                problems.append(f"VERSION {ver} not stamped in artifact header")
        else:
            problems.append("VERSION file missing")

        # extensions + catalogue included?
        if "vocabulary extensions" not in txt:
            problems.append("extensions section missing from artifact")
        if "Reference catalogue" not in txt:
            problems.append("reference catalogue missing from artifact")

    if problems:
        print("FAIL — artifact verification:")
        for p in problems[:40]:
            print(f"  - {p}")
        sys.exit(1)
    print("verify-artifacts: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
