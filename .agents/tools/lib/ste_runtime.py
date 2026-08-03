#!/usr/bin/env python3
"""Pre-flight runtime resolution — the single place tunable knobs are computed.

Why this exists
---------------
Before a stage runs, it needs a handful of *runtime* parameters that are not
unit-footprint paths (those live in ``config.yaml``) but are nonetheless
re-derived independently in every batch script:

* the oneshot wrapper path (``WRAPPER``) — a literal in 9 files,
* the agent venv interpreter (``VENV_PYTHON``) — folded into ste_paths,
* retry / backoff counts for agent calls,
* the batch divisor used to split work,
* default text encoding.

Each script hard-coding these is the drift chain: change the wrapper location in
one place and eight others silently keep pointing at the old path. This module
computes every runtime knob once, from the repo root, so "pre-scripts" (the
pre-flight that builds the agent command) is the *only* source of these values.

Resolution order (lowest priority first)
----------------------------------------
1. ``.agents/config/defaults.yaml`` under ``runtime:`` (shared defaults)
2. ``<unit>/config.yaml`` under ``runtime:``     (unit wins)
3. explicit overrides passed to ``resolve()``

Usage
-----
::

    from ste_runtime import resolve
    rt = resolve(__file__)          # finds the unit config, merges runtime keys

    rt.wrapper                      # absolute path to hermes-oneshot-wrapper.py
    rt.venv_python                  # absolute path to the agent venv interpreter
    rt.retry_attempts               # int
    rt.backoff_base_s               # float
    rt.batch_divisor                # int
    rt.encoding                     # "utf-8"
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except ImportError:  # pragma: no cover - yaml ships with the toolchain
    yaml = None  # type: ignore

from repo_root import repo_root  # noqa: E402
from ste_paths import venv_python, wrapper_path  # noqa: E402

DEFAULTS_REL = Path(".agents") / "config" / "defaults.yaml"

# Fallbacks if neither defaults.yaml nor the unit config declares runtime keys.
_HARD = {
    "retry_attempts": 3,
    "backoff_base_s": 2.0,
    "batch_divisor": 5,
    "encoding": "utf-8",
}


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return data if isinstance(data, dict) else {}


def _dig(data: Dict[str, Any], dotted: str) -> Any:
    node: Any = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


class Runtime:
    """Resolved pre-flight runtime parameters for one unit."""

    def __init__(self, root: Path, unit_runtime: Dict[str, Any]) -> None:
        self.root = root
        self._rt = unit_runtime

    # -- server-side (computed from the repo, never configured) -------------
    @property
    def venv_python(self) -> str:
        return venv_python()

    @property
    def wrapper(self) -> str:
        return wrapper_path(self.root)

    # -- tunable knobs ------------------------------------------------------
    @property
    def retry_attempts(self) -> int:
        v = self._rt.get("retry_attempts")
        return int(v) if v is not None else _HARD["retry_attempts"]

    @property
    def backoff_base_s(self) -> float:
        v = self._rt.get("backoff_base_s")
        return float(v) if v is not None else _HARD["backoff_base_s"]

    @property
    def batch_divisor(self) -> int:
        v = self._rt.get("batch_divisor")
        return int(v) if v is not None else _HARD["batch_divisor"]

    @property
    def encoding(self) -> str:
        v = self._rt.get("encoding")
        return str(v) if v is not None else _HARD["encoding"]

    def as_dict(self) -> Dict[str, Any]:
        return {
            "venv_python": self.venv_python,
            "wrapper": self.wrapper,
            "retry_attempts": self.retry_attempts,
            "backoff_base_s": self.backoff_base_s,
            "batch_divisor": self.batch_divisor,
            "encoding": self.encoding,
        }


def resolve(start: Any, *, overrides: Dict[str, Any] | None = None) -> Runtime:
    """Resolve the pre-flight runtime parameters nearest to *start*.

    Merges ``runtime:`` from defaults.yaml (low) and the unit config (high),
    then applies *overrides* last. The wrapper/venv paths are always computed
    from the repo root — they are never read from config, because a configured
    absolute path is exactly the drift we are removing.
    """
    origin = Path(start).resolve()
    root = repo_root(origin)

    defaults = _read_yaml(root / DEFAULTS_REL).get("runtime", {}) or {}
    unit_dir = origin if origin.is_dir() else origin.parent
    unit = {}
    while True:
        cfg = unit_dir / "config.yaml"
        if cfg.is_file():
            unit = _read_yaml(cfg).get("runtime", {}) or {}
            break
        if unit_dir.parent == unit_dir or (root / ".git").is_dir() and unit_dir == root:
            break
        if unit_dir == root:
            break
        unit_dir = unit_dir.parent

    merged = dict(defaults)
    merged.update(unit)
    for k, v in (overrides or {}).items():
        if v is not None:
            merged[k] = v

    return Runtime(root, merged)


if __name__ == "__main__":
    import json
    import sys

    here = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(resolve(here).as_dict(), indent=2))
