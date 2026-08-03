"""Shared privacy logic for the privacy-scrub family of jail plugins.

Contains the Tier-1 LLM classifier and the backward-chain alert writer used by
both ``privacy-scrub`` (block on main) and ``privacy-scrub-sanitize`` (modify
on feat). Tier-0 is the regex/literal scan in each plugin's own __init__.

Design — two-tier guard
-----------------------
* Tier-0 (regex/literal): fast, free, high-precision. Always on.
* Tier-1 (LLM classify): semantic recall the regex can't match (e.g. "my real
  name is …" without the exact string). OPT-IN via PRIVACY_LLM_CLASSIFY=1 so it
  never surprises a standard build. Calls ``hermes -z`` (reuses the current
  model, zero new infra), cached by content hash, with a hard timeout.

Backward-chain alert
--------------------
When either tier flags private content, an alert line is appended to a SHARED
LOG FILE that the launching/orchestrator agent polls — NOT into the child
session's context. The child session therefore never learns it was detected;
the parent (you) gets the signal out-of-band. This is the "backward chain"
you described: the hook → alert-log → parent, invisible to the writing child.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import subprocess
import threading
import time
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Opt-in: set PRIVACY_LLM_CLASSIFY=1 to enable the LLM Tier-1 classifier.
LLM_ENABLED = os.environ.get("PRIVACY_LLM_CLASSIFY") == "1"


def _profile() -> str:
    return (
        os.getenv("HERMES_PROFILE")
        or os.getenv("HERMES_ACTIVE_PROFILE")
        or "dev-ste-code"
    )


def _alert_log_path() -> Path:
    return Path.home() / ".hermes" / "profiles" / _profile() / "privacy_alerts.log"


# ---------------------------------------------------------------------------
# Tier-1: LLM semantic classifier (opt-in, cached, time-boxed)
# ---------------------------------------------------------------------------

_CLASSIFY_PROMPT = (
    "You are a privacy classifier. Answer ONLY 'true' or 'false'.\n"
    "true = the text contains personal identifiers, credentials/secrets, "
    "API keys, passwords, tokens, home-directory paths, phone numbers, "
    "emails, or other sensitive/private data that should NOT be persisted "
    "to long-term memory.\n"
    "false = the text is benign, generic, or work-related with no private data.\n"
    "Text: "
)

_CACHE: Dict[str, bool] = {}
_CACHE_LOCK = threading.Lock()
_CLASSIFY_TIMEOUT = 15  # seconds hard cap per classification


def classify_private(text: str) -> Optional[bool]:
    """Return True/False if the text is private, or None on error/disabled.

    Uses ``hermes -z`` (oneshot) with the current model — no new infra.
    Result is cached by content hash so identical text is never classified twice.
    """
    if not LLM_ENABLED:
        return None
    if not text or not text.strip():
        return False
    key = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    with _CACHE_LOCK:
        if key in _CACHE:
            return _CACHE[key]
    try:
        # Route the Tier-1 classify through the hardened confined launcher so it
        # runs under STE_CODE_JAIL_POLICY=bench with a stripped env, HOME=/tmp,
        # and leak-scanned output — never as a bare, unconfined `hermes -z`.
        import sys
        _bench = Path(__file__).resolve().parents[4] / "benchmark"
        if str(_bench) not in sys.path:
            sys.path.insert(0, str(_bench))
        from launch_confined_child import launch as _launch_confined

        result = _launch_confined(
            _CLASSIFY_PROMPT + text,
            model="tencent/hy3:free",
            label="privacy-classify",
            timeout=_CLASSIFY_TIMEOUT,
        )
        out = (result.stdout or "").strip().lower()
        verdict = out.startswith("true")
        if not (verdict or out.startswith("false")):
            logger.warning("privacy: unparseable LLM verdict %r", out[:80])
            return None
    except subprocess.TimeoutExpired:
        logger.warning("privacy: LLM classify timed out after %ss", _CLASSIFY_TIMEOUT)
        return None
    except Exception as exc:
        logger.debug("privacy: LLM classify failed: %s", exc)
        return None
    with _CACHE_LOCK:
        _CACHE[key] = verdict
    return verdict


# ---------------------------------------------------------------------------
# Backward-chain alert: append to a log the PARENT polls (child never sees it)
# ---------------------------------------------------------------------------


def write_alert(tool_name: str, reason: str, snippet: str, tier: str) -> None:
    """Append an out-of-band privacy alert the orchestrator agent can poll.

    The child session that triggered this never reads this file, so it cannot
    know it was detected — the signal travels backward to the parent only.
    """
    try:
        path = _alert_log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": time.time(),
            "profile": _profile(),
            "tool": tool_name,
            "tier": tier,  # "regex" or "llm"
            "reason": reason,
            "snippet": snippet[:200],
        }
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
        logger.info("privacy: alert written to %s", path)
    except Exception as exc:
        logger.error("privacy: failed to write alert: %s", exc)
