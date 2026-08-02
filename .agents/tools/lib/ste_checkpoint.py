#!/usr/bin/env python3
"""Checkpoint load/save helper — one confined funnel for resume state.

Seven scripts hand-roll the same pattern::

    try:
        return json.loads(CHECKPOINT_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}

This module replaces them with a single confined, atomic implementation. Writes
go through :mod:`ste_io`, so a checkpoint can never land outside the repo, and a
partial write can never corrupt the resume point (the file is written to a
``.tmp`` sibling and atomically renamed).

Usage
-----
::

    from ste_checkpoint import load, save

    state = load(cfg.path("outputs.checkpoint"))          # {} when absent
    state["done"] = 3
    save(cfg.path("outputs.checkpoint"), state)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

_HERE = Path(__file__).resolve()
_R = next(p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file())
sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))

from ste_io import write_text, read_text  # noqa: E402


def load(path: Path) -> Dict[str, Any]:
    """Return the checkpoint dict, or ``{}`` if absent or unreadable.

    A corrupt checkpoint must never abort a resume; we degrade to empty state.
    """
    p = Path(path)
    if not p.is_file():
        return {}
    try:
        return json.loads(read_text(p, encoding="utf-8"))
    except (json.JSONDecodeError, OSError, ValueError):
        return {}


def save(path: Path, data: Dict[str, Any]) -> Path:
    """Atomically write *data* as the checkpoint, confined to the repo."""
    p = Path(path)
    # Atomic: write to a sibling tmp file, then rename over the target.
    tmp = p.with_suffix(p.suffix + ".tmp")
    write_text(tmp, json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True),
               encoding="utf-8", make_parents=True)
    tmp.replace(p)
    return p


if __name__ == "__main__":
    from ste_io import _root
    d = _root() / ".agents" / "tmp" / "_ste_checkpoint_selfcheck"
    d.mkdir(parents=True, exist_ok=True)
    cp = d / "cp.json"
    assert load(cp) == {}
    save(cp, {"done": 1})
    assert load(cp) == {"done": 1}
    save(cp, {"done": 2})
    assert load(cp) == {"done": 2}
    print("ste_checkpoint self-check OK")
