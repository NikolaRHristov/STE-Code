#!/usr/bin/env python3
"""Phase F finalize — assemble the consolidated + per-tier artifacts.

The LLM distill pass (synthesize_artifacts.py) already populated every tier
directory under ste-code/artifacts/ with distilled sub-documents. This script
performs ONLY the deterministic final-assembly step that was interrupted
before it ran:

  - per-tier  <tier>/_index.md          (sub-doc list for humans)
  - per-tier  <tier>/system-prompt.txt  (concatenated tier = one file the
                                          benchmark can feed as --system-prompt-file)
  - llms.txt                                (tier index, llms.txt standard)
  - llms-full.txt                          (full concatenation of every tier)

Deterministic, no LLM, reproducible byte-for-byte from the distilled tiers.
"""
from __future__ import annotations

import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import write_text  # noqa: E402
ARTIFACTS_DIR = PROJECT / "ste-code" / "artifacts"

# Mirrors synthesis.LEVELS: (tier_dir, level_label, description)
LEVELS = [
    ("level-2", "-2", "ultra-minimal: the 14 core principles only"),
    ("level-1", "-1", "minimal/core: 14 core principles + synonym table"),
    ("level0",  "0",  "baseline: core principles + short dictionary excerpt"),
    ("level1",  "1",  "+ doc templates (code review / PR feedback)"),
    ("level2",  "2",  "+ section-specific grammar rules"),
    ("level3",  "3",  "+ complete dictionary excerpt + all rules"),
    ("level4",  "4",  "+ extensions + reference catalogue"),
    ("level5",  "5",  "full standard (all rules + extensions + catalogue + provenance)"),
]


def _tier_subdocs(tier_dir: Path) -> list[Path]:
    return sorted(p for p in tier_dir.glob("*.md") if p.name != "_index.md")


def _write_tier_index(tier_dir: Path, level_label: str, desc: str, subs: list[Path]) -> None:
    lines = [
        f"# STE-Code Level {level_label} — distilled index",
        "",
        f"> {desc}",
        "",
        "## Sub-documents",
        "",
    ]
    for s in subs:
        lines.append(f"- {s.name}")
    write_text((tier_dir / "_index.md"), "\n".join(lines) + "\n")


def _write_tier_system_prompt(tier_dir: Path, subs: list[Path]) -> None:
    """Concatenate the distilled sub-docs into one system-prompt.txt per tier."""
    blocks = []
    for s in subs:
        text = s.read_text(encoding="utf-8", errors="ignore").strip()
        blocks.append(f"<!-- {s.name} -->\n\n{text}")
    (tier_dir / "system-prompt.txt").write_text(
        "\n\n---\n\n".join(blocks) + "\n", encoding="utf-8"
    )


def _assemble_llms_files(present: list[tuple[str, str, str]]) -> None:
    idx = [
        "# STE-Code",
        "",
        "> STE-Code is a controlled-language variation of ASD-STE100 for software "
        "documentation, distilled here for LLM consumption as small sub-documents. "
        "Load the tier that matches your context window; each tier is a directory "
        "of focused files plus an _index.md.",
        "",
        "## Tiers",
        "",
    ]
    for d, l, desc in present:
        idx.append(f"- [{d}/]({d}/) — level {l} — {desc}")
    idx += [
        "",
        "## Full standard",
        "",
        "- [llms-full.txt](llms-full.txt) — concatenation of every distilled sub-document.",
    ]
    write_text((ARTIFACTS_DIR / "llms.txt"), "\n".join(idx) + "\n")

    full = []
    for d, _, _ in present:
        full.append(f"# tier {d}\n")
        ip = ARTIFACTS_DIR / d / "_index.md"
        if ip.exists():
            full.append(ip.read_text(errors="ignore"))
        for sf in _tier_subdocs(ARTIFACTS_DIR / d):
            full.append(f"\n## {sf.name}\n\n" + sf.read_text(errors="ignore"))
    write_text((ARTIFACTS_DIR / "llms-full.txt"), "\n\n".join(full))


def main() -> int:
    present = []
    for d, l, desc in LEVELS:
        tdir = ARTIFACTS_DIR / d
        if not tdir.is_dir():
            print(f"SKIP {d}/ (missing)")
            continue
        subs = _tier_subdocs(tdir)
        if not subs:
            print(f"SKIP {d}/ (no sub-docs)")
            continue
        _write_tier_index(tdir, l, desc, subs)
        _write_tier_system_prompt(tdir, subs)
        present.append((d, l, desc))
        sp_size = (tdir / "system-prompt.txt").stat().st_size
        print(f"  {d}/: {len(subs)} sub-docs -> _index.md + system-prompt.txt "
              f"({sp_size:,}B)")

    if not present:
        print("No tiers present to assemble.")
        return 1

    _assemble_llms_files(present)
    llf = (ARTIFACTS_DIR / "llms-full.txt").stat().st_size
    print(f"  wrote llms.txt + llms-full.txt ({len(present)} tiers, "
          f"llms-full.txt {llf:,}B)")
    print(f"\nArtifacts finalized -> {ARTIFACTS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
