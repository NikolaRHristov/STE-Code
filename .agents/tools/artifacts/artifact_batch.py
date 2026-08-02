#!/usr/bin/env python3
"""Phase F Assembler — final STE-Code deliverables from the FINAL standard.

Consolidates ste-code/final/ (the enriched, vendor-grounded standard produced by
Phases D+G) into the canonical deployable artifacts:
  - ste-code/artifacts/ste-code-rules.md          (full rule corpus)
  - ste-code/artifacts/ste-code-system-prompt.md  (distilled, template-wrapped)

This is DETERMINISTIC assembly (no LLM): it concatenates the final rule files in
canonical order, wraps them in an externalized header/footer template, and
verifies coverage. The creative enrichment already happened in Phase G; here we
only *collect and package* — so there is no truncation or content-loss risk, and
the output is reproducible byte-for-byte from the same final/ input.

UPGRADED (bring-to-standard):
  - Source is now ste-code/final/ (was stale ste-code/adapted/).
  - Folds in final/rules/{a-categories,a-dictionary} + final/extensions/* +
    final/{README,provenance,reference-catalogue}.md.
  - VERSION bump: reads/writes ste-code/artifacts/VERSION; embeds it in headers.
  - Template placeholders kept as {{name}} (project templater standard).

Usage:
  python3 artifact_batch.py            # assemble both artifacts + bump VERSION
  python3 artifact_batch.py --dry-run  # plan only, write nothing
  python3 artifact_batch.py --verify    # run verify-artifacts.py only
  python3 artifact_batch.py --version 1.2.0   # force a specific version string
"""
from __future__ import annotations

import os
import sys
import re
import json
import argparse
from datetime import datetime
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import write_text, mkdir  # noqa: E402
FINAL_DIR = PROJECT / "ste-code" / "final"
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "artifact-checkpoint.json"
VERSION_PATH = ARTIFACTS_DIR / "VERSION"

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
    9: [f"9.{i}" for i in range(1, 5)],
}

sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import Templater
TPL = Templater(__file__)


def _bump_version(forced: str | None) -> str:
    """Return the version to stamp: forced > existing+patch > 1.0.0."""
    if forced:
        return forced
    if VERSION_PATH.exists():
        try:
            cur = VERSION_PATH.read_text(encoding="utf-8").strip()
            m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", cur)
            if m:
                maj, min_, pat = (int(x) for x in m.groups())
                return f"{maj}.{min_}.{pat + 1}"
        except OSError:
            pass
    return "1.0.0"


def _ordered_rule_files():
    """Return final rule files in canonical section/rule order."""
    out = []
    for sec, ids in SECTION_ORDER.items():
        for rid in ids:
            p = FINAL_DIR / "rules" / f"a-sec{sec}-rule{rid}.md"
            if p.exists():
                out.append(p)
    # Append any section-rule files not in the canonical list (forward-compat).
    seen = {p.name for p in out}
    for p in sorted((FINAL_DIR / "rules").glob("a-sec*-rule*.md")):
        if p.name not in seen:
            out.append(p)
    return out


def _read(name: str, *parts: str) -> str:
    p = FINAL_DIR.joinpath(*parts, name) if parts else FINAL_DIR / name
    if p.exists():
        return p.read_text(encoding="utf-8", errors="ignore")
    # also try directly under FINAL_DIR
    p2 = FINAL_DIR / name
    return p2.read_text(encoding="utf-8", errors="ignore") if p2.exists() else ""


def _collect_rule_text(files):
    blocks = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="ignore").strip()
        blocks.append(f"<!-- {f.name} -->\n\n{text}")
    return "\n\n---\n\n".join(blocks)


def _assemble(dry_run: bool, version: str) -> tuple[bool, dict]:
    rule_files = _ordered_rule_files()
    if not rule_files:
        print("No final rule files found — run Phase G (finalize) first.", flush=True)
        return False, {"reason": "no final rules"}

    rule_text = _collect_rule_text(rule_files)
    cats = _read("a-categories.md", "rules")
    dict_text = _read("a-dictionary.md", "rules")
    extensions = "\n\n---\n\n".join(
        f"# Extension: {p.stem}\n\n{p.read_text(encoding='utf-8', errors='ignore')}"
        for p in sorted((FINAL_DIR / "extensions").glob("*.md"))
    )
    provenance = _read("provenance.md")
    catalogue = _read("reference-catalogue.md")
    today = datetime.now().strftime("%Y-%m-%d")

    full = TPL.render(
        "artifact-rules",
        version=version,
        generated=today,
        rule_count=len(rule_files),
        rules=rule_text,
        categories=cats,
        dictionary=dict_text,
        extensions=extensions,
        provenance=provenance,
        catalogue=catalogue,
    )
    prompt = TPL.render(
        "artifact-system-prompt",
        version=version,
        generated=today,
        rule_count=len(rule_files),
        rules=rule_text,
    )

    if dry_run:
        print(f"[dry-run] would write {len(rule_files)} rules into 2 artifacts "
              f"(rules={len(full)}B, prompt={len(prompt)}B, version={version})")
        return True, {"rule_count": len(rule_files), "rules_bytes": len(full),
                      "prompt_bytes": len(prompt), "version": version}

    mkdir(ARTIFACTS_DIR)
    # Consolidated full corpus is llms-full.txt (ste-code-rules.md /
    # ste-code-system-prompt.md were retired; llms-full.txt is the single-file
    # consolidated artifact).
    write_text((ARTIFACTS_DIR / "llms-full.txt"), full)
    write_text(VERSION_PATH, version + "\n")
    mkdir(STATE_DIR)
    from ste_checkpoint import save
    save(CHECKPOINT_PATH, {"assembled": len(rule_files), "version": version})
    print(f"Wrote llms-full.txt ({len(rule_files)} rules, version {version})")
    return True, {"rule_count": len(rule_files), "version": version}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--version", default=None, help="force a specific version string")
    args = ap.parse_args()

    if args.verify:
        r = subprocess_run_verify()
        sys.exit(r.returncode)

    version = _bump_version(args.version)
    ok, stats = _assemble(args.dry_run, version)
    sys.exit(0 if ok else 1)


def subprocess_run_verify():
    import subprocess
    r = subprocess.run([sys.executable, str(Path(__file__).with_name("verify-artifacts.py"))])
    return r


if __name__ == "__main__":
    main()
