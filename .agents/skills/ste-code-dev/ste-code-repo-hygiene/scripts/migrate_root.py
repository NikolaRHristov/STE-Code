#!/usr/bin/env python3
"""Migrate hop-counted project-root derivation to the tested repo_root helper.

Rewrites the three fragile forms

    PROJECT = Path(__file__).resolve().parent.parent.parent.parent
    PROJECT = Path(__file__).resolve().parents[3]
    PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

into a depth-independent bootstrap that delegates to .agents/tools/lib/repo_root.py:

    # _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
    import sys as _sys
    from pathlib import Path as _Path
    _R = next(p for p in _Path(__file__).resolve().parents
              if (p / ".git").is_dir() or (p / "Makefile").is_file())
    _sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
    from repo_root import repo_root as _repo_root  # noqa: E402

    PROJECT = _repo_root(__file__)

Run from the repository root:

    python3 scripts/migrate_root.py            # dry run, lists every derivation
    python3 scripts/migrate_root.py --apply    # rewrite all three forms
    python3 scripts/migrate_root.py --only "bench/adversarial.py"

Exclusions: .agents/tools/lib/repo_root.py (the helper itself), .agents/hermes/jail/
(owned by another live session), and vendor/__pycache__/ste-code/tmp. Files already
carrying the _STE_REPO_ROOT_BOOTSTRAP marker are skipped.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
SKIP = ("/vendor/", "__pycache__", "/.git/", "/ste-code/", "/.venv/", "/tmp/")
EXCLUDE_FILES = {".agents/tools/lib/repo_root.py"}
EXCLUDE_DIRS = (".agents/hermes/jail/",)

HOP = re.compile(
    r"^(?P<name>[A-Z_][A-Z0-9_]*)[ \t]*=[ \t]*Path\(__file__\)\.resolve\(\)"
    r"(?P<hops>(?:\.parent){2,})[ \t]*\r?$",
    re.M,
)
PARENTS_N = re.compile(
    r"^(?P<name>[A-Z_][A-Z0-9_]*)[ \t]*=[ \t]*Path\(__file__\)\.resolve\(\)"
    r"\.parents\[(?P<n>[1-9])\][ \t]*\r?$",
    re.M,
)
OSPATH = re.compile(
    r"^(?P<name>[A-Z_][A-Z0-9_]*)[ \t]*=[ \t]*os\.path\.abspath\([ \t]*os\.path\.join\("
    r"[ \t]*os\.path\.dirname\(__file__\)[ \t]*,(?P<dots>(?:[ \t]*[\"']\.\.[\"'][ \t]*,?)+)"
    r"[ \t]*\)[ \t]*\)[ \t]*\r?$",
    re.M,
)

MARKER = "_STE_REPO_ROOT_BOOTSTRAP"
BOOT = (
    "# {marker}: locate the repo by marker, not by counting parent hops.\n"
    "import sys as _sys\n"
    "from pathlib import Path as _Path\n"
    "_R = next(p for p in _Path(__file__).resolve().parents\n"
    '          if (p / ".git").is_dir() or (p / "Makefile").is_file())\n'
    '_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))\n'
    "from repo_root import repo_root as _repo_root  # noqa: E402\n"
    "\n"
    "{name} = _repo_root(__file__)"
)


def relevant(p: pathlib.Path) -> bool:
    rel = str(p.relative_to(ROOT)).replace("\\", "/")
    if rel in EXCLUDE_FILES or any(rel.startswith(d) for d in EXCLUDE_DIRS):
        return False
    return not any(s in "/" + rel for s in SKIP)


def migrate(text: str) -> tuple[str, list[str]]:
    if MARKER in text:
        return text, []
    changed: list[str] = []

    def rep(label: str):
        def _f(m: re.Match) -> str:
            changed.append(f"{m.group('name')} ({label})")
            return BOOT.format(marker=MARKER, name=m.group("name"))

        return _f

    out = HOP.sub(lambda m: rep(f"{m.group('hops').count('.parent')} hops")(m), text)
    out = PARENTS_N.sub(lambda m: rep(f"parents[{m.group('n')}]")(m), out)
    out = OSPATH.sub(lambda m: rep(f"os.path x{m.group('dots').count('..')}")(m), out)
    if not changed:
        return text, []
    return out, changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", help="substring filter on path")
    args = ap.parse_args()
    touched = total = 0
    for p in sorted(x for x in ROOT.rglob("*.py") if relevant(x)):
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        if args.only and args.only not in rel:
            continue
        try:
            txt = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        new, changed = migrate(txt)
        if not changed:
            continue
        touched += 1
        total += len(changed)
        print(f"{'APPLY' if args.apply else 'DRY  '} {rel}: {', '.join(changed)}")
        if args.apply:
            p.write_text(new, encoding="utf-8")
    print(f"\n{touched} file(s), {total} derivation(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
