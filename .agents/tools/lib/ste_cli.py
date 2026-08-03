#!/usr/bin/env python3
"""Shared CLI scaffolding for the pipeline entrypoints.

The 61 ``add_argument`` calls and the ``ArgumentParser`` boilerplate repeat the
same shapes: a ``--model`` flag defaulting to the unit's configured model, a
``--workers`` flag, a ``--dry-run`` flag, and a standard epilog. Concentrating
them here keeps the entrypoints thin and guarantees the flags mean the same
thing everywhere.

Usage
-----
::

    from ste_cli import add_common_flags, parse_stage_args

    parser = argparse.ArgumentParser(prog="refine")
    add_common_flags(parser, unit="refinement")
    args = parse_stage_args(parser)
    # args.model, args.workers, args.dry_run are resolved from config + env
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

_HERE = Path(__file__).resolve()
_R = next(
    p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from ste_config import load  # noqa: E402


def add_common_flags(
    parser: argparse.ArgumentParser,
    *,
    unit: str,
    with_model: bool = True,
    with_workers: bool = True,
    with_dry_run: bool = True,
    extra: Optional[Sequence[str]] = None,
) -> None:
    """Attach the flags every stage shares.

    Args:
        unit: The unit key passed to :func:`ste_config.load`; supplies defaults.
        with_model/with_workers/with_dry_run: toggle individual flags.
        extra: additional argument strings to accept verbatim (e.g. positional
            batch ranges) — appended as ``nargs``-style positionals.
    """
    cfg = load(unit)
    if with_model:
        parser.add_argument(
            "--model",
            default=cfg.model,
            help=f"Agent model (default: {cfg.model}; override with STE_MODEL)",
        )
    if with_workers:
        parser.add_argument(
            "--workers",
            type=int,
            default=cfg.get("agent.workers_per_batch"),
            help="Concurrent workers per batch",
        )
    if with_dry_run:
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Print the planned work without writing anything",
        )
    if extra:
        for e in extra:
            parser.add_argument(e, nargs="?", default=None)


def parse_stage_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """Parse and resolve environment overrides (STE_MODEL) over CLI flags."""
    args = parser.parse_args()
    env_model = __import__("os").environ.get("STE_MODEL")
    if env_model and hasattr(args, "model"):
        args.model = env_model
    return args


if __name__ == "__main__":
    p = argparse.ArgumentParser(prog="demo")
    add_common_flags(p, unit="refinement")
    ns = parse_stage_args(p)
    print("model =", ns.model, "| workers =", ns.workers, "| dry_run =", ns.dry_run)
