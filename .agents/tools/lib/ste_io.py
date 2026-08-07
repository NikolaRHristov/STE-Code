#!/usr/bin/env python3
"""Gated file IO: the ONLY write path scripts should use.

Why this exists
---------------
The user's requirement: the only ways a script may write a file are through a
gated helper that enforces confinement, or a ``write_file`` tool call that is
itself jailed inside a session. Free ``open(..., "w")`` / ``write_text`` /
``mkdir`` calls bypass that gate entirely, so a confused or malicious prompt can
scatter output anywhere on the machine. This module is the single funnel.

What it enforces
----------------
1. **Repository confinement** — every target must resolve inside the repo root
   (marker-walked, the same rule as :mod:`repo_root`). A path built from a wrong
   hop count, a ``..`` escape, or an absolute path outside the checkout is
   refused before anything is created.
2. **Explicit "clean" opt-out** — a run that must not be interrupted (large
   model passes) marks itself clean. The escape hatch is *scoped and audited*:
   a script may only set ``clean=True`` when ``STE_CODE_CLEAN_RUN=1`` is present
   in the environment, i.e. the operator opted in at launch, not the script
   deciding unilaterally. Even clean runs still cannot escape the repository.

The jail's ``policy.py`` does deeper confinement for *sessions*. This helper is
the in-process guard for *scripts*: it closes the gap where a script writes via
plain Python instead of a tool call.

Usage
-----
::

    from ste_io import write_text, write_json, mkdir, read_text, read_json

    write_text(cfg.path("outputs.refined") / "r001.md", body)   # confined
    write_json(path, data, make_parents=True)
    mkdir(cfg.path("outputs.state"))

    # Guarantee the parent tree exists before a raw write elsewhere in the
    # codebase (a plain ``open(..., "w")`` / ``Path.write_text`` raises
    # FileNotFoundError when the directory is missing — so an agent that runs
    # with no directories pre-created would crash exactly at output time):
    from pathlib import Path as _P
    ensure_parent_dir(_P("some/deep/new/tree/out.txt"))   # confined, tree made
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Optional, Union

import sys as _sys  # noqa: E402

_HERE = Path(__file__).resolve()
_R = next(
    p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root, ensure_inside_repo  # noqa: E402

DEFAULT_ENCODING = "utf-8"


class GateError(RuntimeError):
    """Raised when a write is refused (outside the repo, or unauthorised)."""


def _root() -> Path:
    try:
        return repo_root()
    except Exception:
        return _R


def _clean_opt_in() -> bool:
    """True only when the operator explicitly launched a clean (uninterrupted) run."""
    return os.environ.get("STE_CODE_CLEAN_RUN", "") == "1"


def _confine(target: Path, *, clean: Optional[bool] = None) -> Path:
    """Resolve *target* and refuse anything outside the repository.

    Args:
        clean: If True, the caller asserts an uninterrupted run. Honoured only
            when ``STE_CODE_CLEAN_RUN=1`` is set by the operator; otherwise the
            request is downgraded to a gated write and a warning is logged. The
            escape hatch can never widen the repository boundary.

    Raises:
        GateError: if *target* escapes the repository root.
    """
    try:
        resolved = ensure_inside_repo(target, _root())
    except Exception as exc:  # repo_root.RepoRootError or any boundary failure
        raise GateError(str(exc)) from exc
    if clean and not _clean_opt_in():
        # The script asked to run clean but the operator did not opt in.
        # Refuse the escalation: stay gated, but do not fail the write — the
        # operation itself is still confined and safe.
        import logging

        logging.getLogger("ste_io").warning(
            "clean run requested but STE_CODE_CLEAN_RUN is not set; "
            "writing through the normal gate"
        )
    return resolved


def ensure_parent_dir(
    path: Union[str, os.PathLike],
    clean: Optional[bool] = None,
) -> Path:
    """Guarantee the parent directory of *path* exists (confined to the repo).

    This is the single point that closes the "no directories existed" gap: a
    plain ``open(path, "w")`` / ``Path.write_text`` raises FileNotFoundError
    when the parent tree is missing, so an agent that starts with an empty
    checkout would crash exactly at the first output write. Call this *before*
    any raw write in the codebase, or let :func:`write_text`/:func:`write_json`
    do it for you via ``make_parents=True``.

    The target itself is NOT created — only its parent. The returned path is
    the confined, resolved target so callers can chain a raw write::

        p = ensure_parent_dir(PROJECT / ".agents" / "prompts" / batch / "x.md")
        p.write_text(...)   # parent now guaranteed to exist

    Refuses targets outside the repository (same gate as the writers).
    """
    target = _confine(Path(path), clean=clean)
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def write_text(
    path: Union[str, os.PathLike],
    text: str,
    *,
    encoding: str = DEFAULT_ENCODING,
    make_parents: bool = False,
    clean: Optional[bool] = None,
) -> Path:
    """Write *text* to *path*, confined to the repository.

    Refuses paths outside the repo. Creates parent directories only when
    *make_parents* is True. *clean* is an opt-in escape hatch (see module doc).
    """
    target = _confine(Path(path), clean=clean)
    if make_parents:
        target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding=encoding)
    return target


def write_json(
    path: Union[str, os.PathLike],
    data: Any,
    *,
    encoding: str = DEFAULT_ENCODING,
    make_parents: bool = False,
    clean: Optional[bool] = None,
) -> Path:
    """Write *data* as JSON, confined to the repository."""
    return write_text(
        path,
        json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True),
        encoding=encoding,
        make_parents=make_parents,
        clean=clean,
    )


def read_text(
    path: Union[str, os.PathLike],
    encoding: str = DEFAULT_ENCODING,
) -> str:
    """Read a file. Reads are unrestricted by the gate, but the path is still
    normalised so callers get a consistent absolute location."""
    return Path(path).read_text(encoding=encoding)


def read_json(path: Union[str, os.PathLike], encoding: str = DEFAULT_ENCODING) -> Any:
    """Read and parse a JSON file."""
    return json.loads(read_text(path, encoding=encoding))


def mkdir(path: Union[str, os.PathLike], clean: Optional[bool] = None) -> Path:
    """Create a directory (and parents), confined to the repository."""
    target = _confine(Path(path), clean=clean)
    target.mkdir(parents=True, exist_ok=True)
    return target


def is_clean_run() -> bool:
    """Whether this process was launched as an uninterrupted (clean) run."""
    return _clean_opt_in()


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Gated IO self-check")
    ap.parse_args()
    root = _root()
    p = root / ".agents" / "tmp" / "_ste_io_selfcheck"
    mkdir(p)
    write_text(p / "a.txt", "ok", make_parents=True)
    assert read_text(p / "a.txt") == "ok"
    write_json(p / "b.json", {"x": 1})
    assert read_json(p / "b.json")["x"] == 1
    print("ste_io self-check OK; clean_run =", is_clean_run())
