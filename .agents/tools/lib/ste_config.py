#!/usr/bin/env python3
"""Per-purpose configuration: one file per unit, declaring its whole footprint.

Why per-unit and not one global file
------------------------------------
A single global config hides which unit actually uses a value: you cannot tell
from ``model:`` at the top of a 400-line file whether refinement reads it. Here
each unit owns ``config.yaml`` in its own directory, and that file declares
*everything* the unit touches — inputs, outputs, layout patterns, separators,
thresholds, and model settings. Reading one file tells you the unit's complete
footprint, and nothing outside that file changes its behaviour.

Shared defaults without a global config
---------------------------------------
Some values are genuinely shared (the model, the agent runtime). Those live in
``.agents/config/defaults.yaml`` and are merged UNDER a unit's own keys, so a
unit always wins. The distinction that keeps this from becoming the global
config we rejected: ``defaults.yaml`` may only carry keys under ``agent:``.
Paths, layout, separators, and thresholds are unit-local by construction and
are rejected if they appear in defaults.

Resolution order, lowest priority first
---------------------------------------
1. ``.agents/config/defaults.yaml``   (``agent:`` keys only)
2. ``<unit>/config.yaml``             (the unit's own declaration)
3. environment overrides              (``STE_MODEL`` and friends, opt-in)
4. explicit call arguments            (an ``--model`` flag)

Usage
-----
::

    from ste_config import load
    cfg = load(__file__)              # finds the unit config beside the script

    cfg.model                          # "tencent/hy3:free"
    cfg.path("inputs.extracted")       # absolute Path, guaranteed in-repo
    cfg.pattern("layout.worker_file")  # "w{worker:03d}-p{start}-{end}.md"
    cfg.get("thresholds.timeout_s")    # 600
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:  # pragma: no cover - yaml ships with the toolchain
    yaml = None  # type: ignore

_HERE = Path(__file__).resolve()
_R = next(
    p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
import sys as _sys  # noqa: E402

_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root, ensure_inside_repo  # noqa: E402

CONFIG_NAME = "config.yaml"
DEFAULTS_REL = Path(".agents") / "config" / "defaults.yaml"

# Only these top-level sections may appear in defaults.yaml. Everything else is
# unit-local by design; allowing paths here would recreate the global config.
# ``runtime:`` is the pre-flight knob set (retry/backoff/batch/encoding) owned by
# ste_runtime — it is not a path or footprint, so sharing it is intentional.
DEFAULTS_ALLOWED = {"agent", "runtime"}

# Environment overrides, applied after the unit file. Keep this list short and
# explicit: an unbounded env surface is another hidden configuration source.
ENV_OVERRIDES = {
    "STE_MODEL": "agent.model",
    "STE_AGENT": "agent.name",
    "STE_TIMEOUT": "agent.timeout_s",
}


class ConfigError(RuntimeError):
    """Raised when a unit config is missing, malformed, or out of bounds."""


def _read_yaml(path: Path) -> Dict[str, Any]:
    if not path.is_file():
        return {}
    if yaml is None:
        raise ConfigError("PyYAML is required to read configuration")
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top level must be a mapping")
    return data


def _deep_merge(base: Dict[str, Any], over: Dict[str, Any]) -> Dict[str, Any]:
    """Merge *over* onto *base*; the unit's own keys always win."""
    out = dict(base)
    for k, v in over.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _dig(data: Dict[str, Any], dotted: str) -> Any:
    node: Any = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(dotted)
        node = node[part]
    return node


def _plant(data: Dict[str, Any], dotted: str, value: Any) -> None:
    parts = dotted.split(".")
    node = data
    for part in parts[:-1]:
        node = node.setdefault(part, {})
    node[parts[-1]] = value


def find_unit_dir(start: os.PathLike | str) -> Path:
    """Return the nearest ancestor directory holding a ``config.yaml``."""
    origin = Path(start).resolve()
    current = origin if origin.is_dir() else origin.parent
    root = repo_root(origin)
    while True:
        if (current / CONFIG_NAME).is_file():
            return current
        if current == root or current.parent == current:
            raise ConfigError(
                f"No {CONFIG_NAME} found at or above {origin} (stopped at {root}). "
                f"Every unit must declare its own footprint."
            )
        current = current.parent


class Config:
    """A resolved unit configuration."""

    def __init__(self, data: Dict[str, Any], unit_dir: Path, root: Path) -> None:
        self._data = data
        self.unit_dir = unit_dir
        self.root = root

    # -- scalars ----------------------------------------------------------
    def get(self, dotted: str, default: Any = "__raise__") -> Any:
        try:
            return _dig(self._data, dotted)
        except KeyError:
            if default == "__raise__":
                raise ConfigError(
                    f"{self.unit_dir / CONFIG_NAME}: missing key '{dotted}'"
                ) from None
            return default

    @property
    def model(self) -> str:
        return self.get("agent.model")

    @property
    def name(self) -> str:
        return self.get("unit")

    # -- paths ------------------------------------------------------------
    def path(self, dotted: str) -> Path:
        """Resolve a declared path relative to the repository root.

        The result is checked against the repository boundary, so a typo in a
        config file cannot send a write outside the checkout.
        """
        raw = self.get(dotted)
        if not isinstance(raw, str):
            raise ConfigError(
                f"{dotted}: expected a path string, got {type(raw).__name__}"
            )
        candidate = Path(raw)
        resolved = candidate if candidate.is_absolute() else (self.root / candidate)
        return ensure_inside_repo(resolved, self.root)

    def paths(self, section: str) -> Dict[str, Path]:
        node = self.get(section)
        if not isinstance(node, dict):
            raise ConfigError(f"{section}: expected a mapping of name -> path")
        return {k: self.path(f"{section}.{k}") for k in node}

    # -- layout / separators ---------------------------------------------
    def pattern(self, dotted: str) -> str:
        return str(self.get(dotted))

    def regex(self, dotted: str) -> "re.Pattern[str]":
        return re.compile(self.get(dotted))

    def render(self, dotted: str, **fields: Any) -> str:
        """Format a declared layout pattern, e.g. ``w{worker:03d}-p{start}.md``."""
        return self.pattern(dotted).format(**fields)

    # -- introspection ----------------------------------------------------
    def footprint(self) -> str:
        """Human-readable summary of everything this unit reads and writes."""
        lines = [f"unit: {self.get('unit', self.unit_dir.name)}"]
        for section in ("inputs", "outputs"):
            node = self._data.get(section) or {}
            if node:
                lines.append(f"{section}:")
                for k in node:
                    lines.append(f"  {k}: {node[k]}")
        agent = self._data.get("agent") or {}
        if agent:
            lines.append("agent:")
            for k, v in agent.items():
                lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    def as_dict(self) -> Dict[str, Any]:
        return dict(self._data)


def load(
    start: os.PathLike | str,
    *,
    overrides: Optional[Dict[str, Any]] = None,
    use_env: bool = True,
) -> Config:
    """Load the unit config nearest to *start*.

    Args:
        start: Usually ``__file__`` from the calling script.
        overrides: Explicit values (e.g. parsed CLI flags) applied last.
        use_env: Apply the small allow-list of environment overrides.
    """
    unit_dir = find_unit_dir(start)
    root = repo_root(unit_dir)

    defaults = _read_yaml(root / DEFAULTS_REL)
    stray = set(defaults) - DEFAULTS_ALLOWED
    if stray:
        raise ConfigError(
            f"{root / DEFAULTS_REL}: only {sorted(DEFAULTS_ALLOWED)} may be shared; "
            f"found {sorted(stray)}. Paths, layout, separators and thresholds are "
            f"unit-local — declare them in the unit's {CONFIG_NAME}."
        )

    unit = _read_yaml(unit_dir / CONFIG_NAME)
    data = _deep_merge(defaults, unit)

    if use_env:
        for env_key, dotted in ENV_OVERRIDES.items():
            val = os.environ.get(env_key)
            if val:
                _plant(data, dotted, val)

    for dotted, val in (overrides or {}).items():
        if val is not None:
            _plant(data, dotted, val)

    return Config(data, unit_dir, root)


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Show a unit's configured footprint")
    ap.add_argument(
        "path", nargs="?", default=".", help="file or directory in the unit"
    )
    args = ap.parse_args()
    print(load(args.path).footprint())
