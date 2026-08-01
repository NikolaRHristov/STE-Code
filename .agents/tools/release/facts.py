#!/usr/bin/env python3
"""Ground-truth project facts, measured from disk — never hand-written.

Every number that STE-Code claims in a badge, a table, or a sentence has one
authority: this module. `scan.py` compares documents against these values and
`release.py` writes them back.

Usage:
    python3 .agents/tools/release/facts.py           # table
    python3 .agents/tools/release/facts.py --json    # machine readable
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]


def _count(glob: str, pattern: str | None = None) -> int:
    files = sorted(PROJECT.glob(glob))
    if pattern is None:
        return len(files)
    rx = re.compile(pattern)
    return sum(1 for f in files if rx.search(f.name))


def _headings(path: Path, pattern: str) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    return len(re.findall(pattern, text, re.M))


def _tests() -> tuple[int, int]:
    """(test-case files, total tests) in the static benchmark suite."""
    files = sorted((PROJECT / ".agents/benchmark/test-cases").glob("*.json"))
    total = 0
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        total += len(data) if isinstance(data, list) else len(data.get("tests", []))
    return len(files), total


def _tiers() -> list[dict]:
    """Measured tier sizes, delegated to the canonical measuring tool."""
    tool = PROJECT / ".agents/tools/maintenance/measure_artifacts.py"
    if not tool.exists():
        return []
    out = subprocess.run(
        ["python3", str(tool), "--json"], capture_output=True, text=True, cwd=PROJECT
    )
    if out.returncode != 0:
        return []
    try:
        data = json.loads(out.stdout)
    except json.JSONDecodeError:
        return []
    tiers = []
    for t in data.get("tiers", []):
        b = t["distilled"]["bytes"]
        tiers.append(
            {
                "tier": t["tier"],
                "bytes": b,
                "kb": round(b / 1024),
                "tokens": t["distilled"]["tokens_o200k"],
                "tokens_k": round(t["distilled"]["tokens_o200k"] / 1000, 1),
                "complete": t.get("complete", False),
            }
        )
    return tiers


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True, cwd=PROJECT)
    return out.stdout.strip()


def _versions() -> dict:
    """Version per track, from tags.

    `release.py` exports STE_RELEASE_VERSION while cutting a release: the new
    tag does not exist when claims are synced, and stamps must carry the
    version being released, not the previous one.
    """
    override = os.environ.get("STE_RELEASE_VERSION")
    if override:
        return {"core": override, "STANDARD": override, "FLAVOR": override}
    tags = git("tag", "--list").splitlines()
    sem = re.compile(r"^(?:(?P<track>[A-Z]+)-)?v?(?P<v>\d+\.\d+\.\d+)$")
    tracks: dict[str, list[tuple[int, ...]]] = {}
    for tag in tags:
        m = sem.match(tag.strip())
        if not m:
            continue
        track = m.group("track") or "core"
        tracks.setdefault(track, []).append(tuple(int(p) for p in m.group("v").split(".")))
    return {k: ".".join(str(p) for p in max(v)) for k, v in tracks.items()}


def _release_date(core: str) -> str:
    """Date to stamp on the release.

    `release.py` exports STE_RELEASE_DATE when it cuts a version, because the
    new tag does not exist yet at sync time. Otherwise report the date of the
    newest core tag, so a plain scan compares against what actually shipped.
    """
    override = os.environ.get("STE_RELEASE_DATE")
    if override:
        return override
    if core != "0.0.0":
        dated = git("log", "-1", "--format=%ad", "--date=short", f"v{core}")
        if dated:
            return dated
    return date.today().isoformat()


def collect() -> dict:
    final_rules = PROJECT / "ste-code/final/rules"
    tc_files, tests = _tests()
    versions = _versions()
    core = versions.get("core", "0.0.0")
    return {
        "versions": {
            "core": core,
            "standard": versions.get("STANDARD", core),
            "flavor": versions.get("FLAVOR", core),
        },
        "release_date": _release_date(core),
        "rules": _count("ste-code/final/rules/a-sec*-rule*.md"),
        "general_rules": _count("ste-code/adapted/a-sec9-gr*.md"),
        "sections": 9,
        "categories": _headings(final_rules / "a-categories.md", r"^## Category \d+"),
        # The source PDF has 434 printed pages; the split produces 426 page
        # files (front matter and blank versos merge). Both numbers are true —
        # keep them separate so documents cite the right one.
        "spec_pdf_pages": 434,
        "spec_pages": _count("spec/issue-09-2025/page-dir/page-*.md"),
        "extracted": _count("ste-code/extracted/*.md"),
        "refined": _count("ste-code/refined/*.md"),
        "groups": _count("ste-code/grouped/group-*.md"),
        "adapted_files": _count("ste-code/adapted/*.md"),
        "extension_files": _count("ste-code/final/extensions/*"),
        "locales": len([p for p in (PROJECT / "translations").iterdir() if p.is_dir()])
        if (PROJECT / "translations").exists()
        else 0,
        "benchmark_categories": tc_files,
        "benchmark_tests": tests,
        "tiers": _tiers(),
        "tier_count": len(_tiers()),
        "adapted_rules": _count("ste-code/adapted/a-sec*-rule*.md"),
        "adapted_gr": _count("ste-code/adapted/a-sec9-gr*.md"),
        "unreleased_commits": int(git("rev-list", f"v{core}..HEAD", "--count") or 0)
        if core != "0.0.0"
        else 0,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true", help="emit JSON")
    args = ap.parse_args()
    f = collect()
    if args.json:
        print(json.dumps(f, indent=2))
        return 0
    print(f"{'fact':<24} value")
    print("-" * 48)
    for k, v in f.items():
        if k == "tiers":
            for t in v:
                mark = "" if t["complete"] else "  (distillation pending)"
                print(f"  {t['tier']:<20} {t['kb']} KB / ~{t['tokens_k']}K tokens{mark}")
            continue
        print(f"{k:<24} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
