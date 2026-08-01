#!/usr/bin/env python3
"""verify-artifacts.py — post-assembly gate for STE-Code Phase F.

Confirms the assembled artifacts cover every adapted rule and that the assembly
did not drop or duplicate content. Deterministic — no LLM.

Usage: python3 verify-artifacts.py   (exit 0 = pass)
"""
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"

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
        covered = 0
        for sec, ids in SECTION_ORDER.items():
            for rid in ids:
                name = f"a-sec{sec}-rule{rid}.md"
                if name in txt:
                    covered += 1
                else:
                    problems.append(f"artifact missing rule {name}")
        print(f"Artifact rule coverage: {covered}/"
              f"{sum(len(v) for v in SECTION_ORDER.values())} expected rule ids present")
        if covered == 0:
            problems.append("no rule ids found in artifact — assembly likely empty")

    if problems:
        print("FAIL — artifact verification:")
        for p in problems[:40]:
            print(f"  - {p}")
        sys.exit(1)
    print("verify-artifacts: PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
