#!/usr/bin/env python3
"""Scan the repository for version, badge, and count claims that drifted.

Reads ground truth from `facts.py` and the claim sites from `registry.json`,
then reports every documented number that disagrees with disk.

Exit code 0 = clean, 1 = drift found (so CI can gate on it).

Usage:
    python3 .agents/tools/release/scan.py              # human table
    python3 .agents/tools/release/scan.py --json       # machine readable
    python3 .agents/tools/release/scan.py --all        # include matching claims
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
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
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from facts import collect  # noqa: E402


def registry() -> dict:
    return json.loads((HERE / "registry.json").read_text(encoding="utf-8"))


def resolve(facts: dict, dotted: str):
    cur = facts
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def tracked_files(reg: dict, wide: bool) -> list[str]:
    """Claim sites to scan: the curated sync set, or every tracked doc."""
    if not wide:
        return [f for f in reg["sync_files"] if (PROJECT / f).exists()]
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, cwd=PROJECT)
    excl = tuple(reg["scan_exclude"])
    keep = (".md", ".txt", ".json", ".yml", ".yaml", ".cff")
    return [f for f in out.stdout.split() if f.endswith(keep) and not f.startswith(excl)]


IGNORE = "release-scan:ignore"


def scan_counts(facts: dict, reg: dict, files: list[str]) -> list[dict]:
    findings = []
    for claim in reg["count_claims"]:
        allowed = {
            str(v) for v in (resolve(facts, f) for f in claim["facts"]) if v is not None
        }
        if not allowed:
            continue
        rx = re.compile(claim["pattern"])
        for rel in files:
            path = PROJECT / rel
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for n, line in enumerate(lines, 1):
                if IGNORE in line:
                    continue
                for m in rx.finditer(line):
                    value = m.group("value")
                    if value in allowed:
                        continue
                    findings.append(
                        {
                            "kind": "count",
                            "claim": claim["id"],
                            "file": rel,
                            "line": n,
                            "found": value,
                            "expected": " or ".join(sorted(allowed)),
                            "text": line.strip()[:110],
                        }
                    )
    return findings


def scan_stamps(facts: dict, reg: dict) -> list[dict]:
    findings = []
    for group in ("badges", "version_stamps"):
        for claim in reg[group]:
            if not claim.get("fact"):
                continue
            expected = resolve(facts, claim["fact"])
            if expected is None:
                if claim.get("optional"):
                    continue
                expected = None
            path = PROJECT / claim["file"]
            if not path.exists():
                findings.append(
                    {
                        "kind": group,
                        "claim": claim["id"],
                        "file": claim["file"],
                        "line": 0,
                        "found": None,
                        "expected": str(expected),
                        "text": "file missing",
                    }
                )
                continue
            rx = re.compile(claim["pattern"], re.M)
            text = path.read_text(encoding="utf-8", errors="replace")
            m = rx.search(text)
            if not m:
                if claim.get("optional"):
                    continue
                findings.append(
                    {
                        "kind": group,
                        "claim": claim["id"],
                        "file": claim["file"],
                        "line": 0,
                        "found": None,
                        "expected": str(expected),
                        "text": "claim site not found",
                    }
                )
                continue
            if "value" not in (m.groupdict() or {}):
                continue
            found = m.group("value")
            if expected is not None and found != str(expected):
                line = text[: m.start()].count("\n") + 1
                findings.append(
                    {
                        "kind": group,
                        "claim": claim["id"],
                        "file": claim["file"],
                        "line": line,
                        "found": found,
                        "expected": str(expected),
                        "text": m.group(0)[:110],
                    }
                )
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--counts-only", action="store_true")
    ap.add_argument("--stamps-only", action="store_true")
    ap.add_argument(
        "--wide",
        action="store_true",
        help="scan every tracked document, not just the curated sync set (advisory)",
    )
    args = ap.parse_args()

    facts = collect()
    reg = registry()
    findings: list[dict] = []
    if not args.counts_only:
        findings += scan_stamps(facts, reg)
    if not args.stamps_only:
        findings += scan_counts(facts, reg, tracked_files(reg, args.wide))

    if args.json:
        print(json.dumps({"facts": facts, "findings": findings}, indent=2))
        return 1 if findings else 0

    if not findings:
        print("No drift: every documented version, badge, and count matches disk.")
        return 0

    print(f"{len(findings)} drifted claim(s):\n")
    by_file: dict[str, list[dict]] = {}
    for f in findings:
        by_file.setdefault(f["file"], []).append(f)
    for rel, items in sorted(by_file.items()):
        print(f"  {rel}")
        for i in items:
            loc = f":{i['line']}" if i["line"] else ""
            print(f"    {i['claim']:<18} {loc:<7} found {i['found']!r} expected {i['expected']!r}")
            print(f"      {i['text']}")
        print()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
