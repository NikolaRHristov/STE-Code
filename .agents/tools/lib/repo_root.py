#!/usr/bin/env python3
"""Anchor the project root without counting parent directory hops.

Why this exists
---------------
Pipeline scripts historically derived the project root by counting ``parent``
hops from ``__file__``::

    PROJECT = Path(__file__).resolve().parent.parent.parent   # 3 hops

The hop count encodes the script's depth in the tree. Move the script one
directory deeper or shallower and the count is silently wrong: ``PROJECT``
then points at an ancestor of the real repository, ``os.makedirs`` happily
creates the missing tree, and the run scatters directories OUTSIDE the
checkout. That is exactly how an empty ``.agents/prompts/<batch>/`` tree ended
up one level above the repo.

``repo_root()`` removes the failure mode: it walks up from a starting path
until it finds a directory containing a repository marker, so the answer does
not depend on how deep the caller sits.

Usage
-----
::

    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
    from repo_root import repo_root

    PROJECT = repo_root(__file__)

Run directly to print the detected root::

    python3 .agents/tools/lib/repo_root.py
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Optional, Sequence, Union

# A directory holding any of these is treated as the repository root.
# ``.git`` first: it is the strongest signal and the one a clone always has.
DEFAULT_MARKERS: Sequence[str] = (".git", "Makefile")

# Hard ceiling on the upward walk so a detached path cannot climb to "/".
_MAX_DEPTH = 24


class RepoRootError(RuntimeError):
    """Raised when no repository root can be located above the start path."""


def repo_root(
    start: Union[str, os.PathLike, None] = None,
    markers: Optional[Iterable[str]] = None,
    strict: bool = True,
) -> Path:
    """Return the repository root at or above *start*.

    Args:
        start: File or directory to start from. Defaults to this module's
            location. Pass ``__file__`` from the calling script.
        markers: Directory entries identifying the root. Defaults to
            :data:`DEFAULT_MARKERS`.
        strict: When ``True`` (default) raise :class:`RepoRootError` if no
            marker is found. When ``False`` fall back to the start directory.

    Returns:
        Absolute, symlink-resolved :class:`Path` to the repository root.
    """
    marker_list = tuple(markers or DEFAULT_MARKERS)

    origin = Path(start).resolve() if start is not None else Path(__file__).resolve()
    current = origin if origin.is_dir() else origin.parent

    for _ in range(_MAX_DEPTH):
        for marker in marker_list:
            if (current / marker).exists():
                return current
        if current.parent == current:
            break
        current = current.parent

    if strict:
        raise RepoRootError(
            f"No repository root found above {origin} "
            f"(looked for: {', '.join(marker_list)})"
        )
    return origin if origin.is_dir() else origin.parent


def inside_repo(path: Union[str, os.PathLike], root: Optional[Path] = None) -> bool:
    """True when *path* resolves at or under the repository root.

    Use before any write whose target was built from caller-supplied or
    computed components.
    """
    base = (root or repo_root()).resolve()
    target = Path(os.path.expandvars(os.path.expanduser(str(path)))).resolve()
    return target == base or base in target.parents


def ensure_inside_repo(
    path: Union[str, os.PathLike], root: Optional[Path] = None
) -> Path:
    """Return *path* resolved, or raise if it escapes the repository.

    Drop-in guard for the line right before ``os.makedirs`` / ``open(..., "w")``
    in any script that builds an output path::

        out = ensure_inside_repo(PROJECT / ".agents" / "prompts" / batch)
        out.mkdir(parents=True, exist_ok=True)
    """
    base = (root or repo_root()).resolve()
    target = Path(os.path.expandvars(os.path.expanduser(str(path)))).resolve()
    if target != base and base not in target.parents:
        raise RepoRootError(
            f"Refusing to use {target}: it is outside the repository root {base}. "
            f"This usually means a project-root variable was computed with the "
            f"wrong number of parent hops — use repo_root(__file__) instead."
        )
    return target


if __name__ == "__main__":
    print(repo_root(__file__))
