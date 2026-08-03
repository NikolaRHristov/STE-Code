#!/usr/bin/env python3
"""Shared path computations — single source for agent runtime locations.

Nine scripts each declared the same two lines::

    VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
    WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")

Concentrating them here means the agent runtime location is defined once.

Usage
-----
::

    from ste_paths import venv_python, wrapper_path

    proc = subprocess.run([venv_python(), wrapper_path(), ...])
"""

from __future__ import annotations

from pathlib import Path

DEFAULT_VENV = Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3"


def venv_python() -> str:
    """Absolute path to the agent venv interpreter."""
    return str(DEFAULT_VENV)


def wrapper_path(project_root: Path | None = None) -> str:
    """Absolute path to the oneshot wrapper script.

    Args:
        project_root: repo root; resolved via the marker walk when omitted.
    """
    if project_root is None:
        from repo_root import repo_root

        project_root = repo_root()
    return str(
        Path(project_root) / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py"
    )


if __name__ == "__main__":
    print("venv_python:", venv_python())
    print("wrapper_path:", wrapper_path())
