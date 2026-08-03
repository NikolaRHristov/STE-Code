#!/usr/bin/env python3
"""Shared timestamp helper — one format, one source.

Three scripts each built their own ``datetime.now().strftime("%Y%m%d-%H%M%S")``
(or a variant). That is a layout/separator decision that belongs in config, not
inline. This helper returns the canonical run-stamp and lets a unit declare its
own format in config.yaml under ``format.timestamp``.

Usage
-----
::

    from ste_time import run_stamp, now_iso

    stamp = run_stamp()                 # 20260802-203100
    iso = now_iso()                     # 2026-08-02T20:31:00+00:00
"""

from __future__ import annotations

from datetime import datetime, timezone

DEFAULT_STAMP = "%Y%m%d-%H%M%S"


def run_stamp(fmt: str = DEFAULT_STAMP) -> str:
    """Local wall-clock stamp for run directories and log filenames."""
    return datetime.now().strftime(fmt)


def now_iso() -> str:
    """UTC ISO-8601 timestamp (timezone-aware) for machine-readable logs."""
    return datetime.now(timezone.utc).isoformat()
