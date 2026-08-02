#!/usr/bin/env python3
"""Retry-with-backoff helper — one implementation for the whole corpus.

The retry loops that do exist are hand-rolled; others should use one. A single
helper keeps the policy in config (``agent.retries`` / ``agent.backoff_s``) and
makes the behaviour identical everywhere.

Usage
-----
::

    from ste_retry import retry

    result = retry(call_api, retries=3, backoff_s=5, label="expand")
"""
from __future__ import annotations

import time
from typing import Any, Callable, Tuple, Type

DEFAULT_EXCEPTIONS: Tuple[Type[BaseException], ...] = (Exception,)


def retry(
    fn: Callable[[], Any],
    *,
    retries: int = 3,
    backoff_s: float = 5.0,
    exceptions: Tuple[Type[BaseException], ...] = DEFAULT_EXCEPTIONS,
    label: str = "call",
) -> Any:
    """Run *fn*; on failure retry up to *retries* times, sleeping *backoff_s*.

    Raises the last exception if all attempts fail.
    """
    import logging
    log = logging.getLogger("ste_retry")
    last: BaseException | None = None
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except exceptions as exc:  # type: ignore[misc]
            last = exc
            log.warning("%s attempt %d/%d failed: %s", label, attempt, retries, exc)
            if attempt < retries:
                time.sleep(backoff_s)
    assert last is not None
    raise last


if __name__ == "__main__":
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 2:
            raise ValueError("boom")
        return "ok"

    print("result =", retry(flaky, retries=3, backoff_s=0))
