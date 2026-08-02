#!/usr/bin/env python3
"""Self-test for the gated IO helper (ste_io).

Guards:
  - a write outside the repository is refused
  - the clean-run escape hatch CANNOT widen the repository boundary
  - make_parents and JSON round-trip work
  - reads are normalised and unrestricted
  - STE_CODE_CLEAN_RUN=1 is required for a clean write to be honoured
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_R = next(p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file())
sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))

import ste_io  # noqa: E402

_fail = 0


def check(ok, label):
    global _fail
    print(f"  [{'ok' if ok else 'FAIL'}]   {label}")
    if not ok:
        _fail += 1


def main() -> int:
    print("ste_io")
    root = ste_io._root()
    p = root / ".agents" / "tmp" / "_ste_io_test"
    ste_io.mkdir(p)

    # normal confined write
    ste_io.write_text(p / "a.txt", "hello", make_parents=True)
    check(ste_io.read_text(p / "a.txt") == "hello", "confined write + read")

    ste_io.write_json(p / "b.json", {"k": 2})
    check(ste_io.read_json(p / "b.json")["k"] == 2, "json round-trip")

    # escape attempt
    try:
        ste_io.write_text("/tmp/../../etc/ste_io_escape", "x")
        check(False, "write outside repo refused")
    except ste_io.GateError:
        check(True, "write outside repo refused")

    # clean escape hatch cannot widen boundary
    os.environ.pop("STE_CODE_CLEAN_RUN", None)
    try:
        ste_io.write_text("/etc/ste_io_clean_escape", "x", clean=True)
        check(False, "clean run cannot escape the repo")
    except ste_io.GateError:
        check(True, "clean run cannot escape the repo")

    # clean opt-in is honoured but still confined
    os.environ["STE_CODE_CLEAN_RUN"] = "1"
    try:
        ste_io.write_text(p / "clean.txt", "c", clean=True, make_parents=True)
        check(ste_io.read_text(p / "clean.txt") == "c", "clean opt-in write succeeds (still confined)")
    finally:
        del os.environ["STE_CODE_CLEAN_RUN"]

    print(f"\nRESULT: {'all checks passed' if not _fail else f'{_fail} failure(s)'}")
    return 1 if _fail else 0


if __name__ == "__main__":
    sys.exit(main())
