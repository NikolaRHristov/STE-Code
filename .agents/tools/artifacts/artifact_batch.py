#!/usr/bin/env python3
"""Phase F Assembler — final STE-Code deliverables from adapted rules.

Consolidates ste-code/adapted/ into the canonical deployable artifacts:
  - ste-code/artifacts/ste-code-rules.md          (full rule corpus)
  - ste-code/artifacts/ste-code-system-prompt.md  (distilled, template-wrapped)

This is DETERMINISTIC assembly (no LLM): it concatenates the adapted rule files
in canonical order, wraps them in an externalized header/footer template, and
verifies coverage. The creative adaptation already happened in Phase D; here we
only *collect and package* — so there is no truncation or content-loss risk, and
the output is reproducible byte-for-byte from the same adapted/ input.

Usage:
  python3 artifact_batch.py            # assemble both artifacts
  python3 artifact_batch.py --dry-run  # plan only, write nothing
  python3 artifact_batch.py --verify    # run verify-artifacts.py only
"""
from __future__ import annotations

import os
import sys
import re
import json
import argparse
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "artifact-checkpoint.json"

# Canonical rule ordering: section -> rule ids (mirrors adaptation EXPECTED).
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

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)


def _ordered_rule_files():
    """Return adapted rule files in canonical section/rule order."""
    out = []
    for sec, ids in SECTION_ORDER.items():
        for rid in ids:
            p = ADAPTED_DIR / f"a-sec{sec}-rule{rid}.md"
            if p.exists():
                out.append(p)
    # Append any section-rule files not in the canonical list (forward-compat).
    seen = {p.name for p in out}
    for p in sorted(ADAPTED_DIR.glob("a-sec*-rule*.md")):
        if p.name not in seen:
            out.append(p)
    return out


def _collect_rule_text(files):
    blocks = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore").strip()
        blocks.append(f"<!-- {f.name} -->\n\n{text}")
    return "\n\n---\n\n".join(blocks)


def _assemble(dry_run: bool) -> tuple[bool, dict]:
    rule_files = _ordered_rule_files()
    if not rule_files:
        print("No adapted rule files found — run Phase D first.", flush=True)
        return False, {"reason": "no adapted rules"}

    rule_text = _collect_rule_text(rule_files)
    cats = (ADAPTED_DIR / "a-categories.md").read_text(encoding="utf-8", errors="ignore") if (ADAPTED_DIR / "a-categories.md").exists() else ""
    dict_text = (ADAPTED_DIR / "a-dictionary.md").read_text(encoding="utf-8", errors="ignore") if (ADAPTED_DIR / "a-dictionary.md").exists() else ""

    full = TPL.render(
        "artifact-rules",
        rule_count=len(rule_files),
        generated=__import__("datetime").datetime.now().strftime("%Y-%m-%d"),
        rules=rule_text,
        categories=cats,
        dictionary=dict_text,
    )
    prompt = TPL.render(
        "artifact-system-prompt",
        rule_count=len(rule_files),
        generated=__import__("datetime").datetime.now().strftime("%Y-%m-%d"),
        rules=rule_text,
    )

    if dry_run:
        print(f"[dry-run] would write {len(rule_files)} rules into 2 artifacts "
              f"(rules={len(full)}B, prompt={len(prompt)}B)")
        return True, {"rule_count": len(rule_files), "rules_bytes": len(full),
                      "prompt_bytes": len(prompt)}

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "ste-code-rules.md").write_text(full, encoding="utf-8")
    (ARTIFACTS_DIR / "ste-code-system-prompt.md").write_text(prompt, encoding="utf-8")
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_PATH.write_text(json.dumps({"assembled": len(rule_files)}, indent=2))
    print(f"Wrote ste-code-rules.md and ste-code-system-prompt.md "
          f"({len(rule_files)} rules)")
    return True, {"rule_count": len(rule_files)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    if args.verify:
        import subprocess
        r = subprocess.run([sys.executable, str(Path(__file__).with_name("verify-artifacts.py"))])
        sys.exit(r.returncode)

    ok, stats = _assemble(args.dry_run)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
