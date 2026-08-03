"""privacy-scrub — refuse memory writes that contain sensitive data.

A ``pre_tool_call`` hook. When enabled for the active profile
(``plugins.entries.privacy-scrub.enabled: true`` in config.yaml), it inspects
every ``memory`` tool call and blocks the write if the content matches any
sensitive pattern (operator identity from HERMES_OPERATOR_NAMES, credentials,
machine-specific paths).

Design notes
------------
* The hook contract can BLOCK or ALLOW but cannot rewrite tool arguments, so the
  safe posture is refuse-and-instruct: the model is told which class of data
  leaked and must retry without it. This also makes leaks visible instead of
  silently rewritten.
* Patterns live in this plugin's ``config.yaml`` (single source of truth), not
  in code, so new sensitive cases are added by editing one file.
* Enablement is per-profile. The plugin is symlinked into every profile but
  returns ``None`` (no-op) unless its enable flag is set, so it is inert until
  switched on for a given profile.
* Location is found by MARKER walk, never parent-hop counting (same rule as the
  jail — see core.policy.resolve_project_root).

The background self-improvement review writes memory through the same ``memory``
tool, so this hook covers it: a review that tries to persist the operator's name
or a credential is blocked before anything hits MEMORY.md / USER.md.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_HERE = Path(__file__).resolve().parent

# Shared Tier-1 LLM classifier + backward-chain alert writer (kept in this dir so
# both privacy-scrub and privacy-scrub-sanitize reuse it without drift).
import sys as _sys

if str(_HERE) not in _sys.path:
    _sys.path.insert(0, str(_HERE))
from _common import classify_private, write_alert  # noqa: E402


def _load_patterns() -> Dict[str, List[str]]:
    """Load literal + regex patterns from this plugin's config.yaml.

    Plus an OPTIONAL operator-name list from the HERMES_OPERATOR_NAMES env var
    (comma-separated). Real identifiers are never stored in this tracked file —
    they are injected at runtime so the plugin stays anonymized in the repo.
    """
    cfg_path = _HERE / "config.yaml"
    literals: List[str] = []
    regexes: List[str] = []
    if not cfg_path.exists():
        logger.warning("privacy-scrub: config.yaml missing at %s", cfg_path)
        return {"literal": [], "regex": []}
    try:
        import yaml

        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        literals = [str(s).lower() for s in (data.get("literal") or [])]
        regexes = [str(s) for s in (data.get("regex") or [])]
    except Exception as exc:  # never let a bad pattern file break the agent
        logger.error("privacy-scrub: failed to load config: %s", exc)

    # Operator names come from the environment, NOT from the repo file.
    env_names = os.environ.get("HERMES_OPERATOR_NAMES", "")
    for raw in env_names.split(","):
        name = raw.strip().lower()
        if name:
            literals.append(name)
    return {"literal": literals, "regex": regexes}


_PATTERNS = _load_patterns()
_COMPILED_REGEX = []
for _rx in _PATTERNS.get("regex", []):
    try:
        _COMPILED_REGEX.append((_rx, re.compile(_rx, re.IGNORECASE)))
    except re.error as exc:
        logger.error("privacy-scrub: bad regex %r skipped: %s", _rx, exc)


def _is_enabled() -> bool:
    """Per-profile enablement from the agent's config.yaml.

    Returns False unless ``plugins.entries.privacy-scrub.enabled`` is true.
    Reads the live config file directly (lightweight, no CLI imports).
    """
    try:
        import yaml

        cfg_path = (
            Path.home() / ".hermes" / "profiles" / _active_profile() / "config.yaml"
        )
        if not cfg_path.exists():
            return False
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        entries = (data.get("plugins") or {}).get("entries") or {}
        spec = entries.get("privacy-scrub") or {}
        return bool(spec.get("enabled"))
    except Exception as exc:
        logger.debug("privacy-scrub: enablement check failed (%s)", exc)
        return False


def _active_profile() -> str:
    """Best-effort resolution of the active profile directory name."""
    import os

    # HERMES_PROFILE is the conventional env var the runtime exports.
    return os.getenv("HERMES_PROFILE") or os.getenv("HERMES_ACTIVE_PROFILE") or ""


def _extract_text(args: Any) -> List[str]:
    """Pull all candidate text from a memory tool call's arguments."""
    texts: List[str] = []
    if not isinstance(args, dict):
        return texts
    for key in ("content", "old_text", "new_text"):
        v = args.get(key)
        if isinstance(v, str) and v.strip():
            texts.append(v)
    ops = args.get("operations")
    if isinstance(ops, list):
        for op in ops:
            if isinstance(op, dict):
                for key in ("content", "old_text", "new_text"):
                    v = op.get(key)
                    if isinstance(v, str) and v.strip():
                        texts.append(v)
    return texts


def _find_match(text: str) -> Optional[str]:
    """Return a human-readable label for the first sensitive pattern hit."""
    low = text.lower()
    for lit in _PATTERNS.get("literal", []):
        if lit and lit in low:
            return f"literal term '{lit}'"
    for label, rx in _COMPILED_REGEX:
        if rx.search(text):
            return f"pattern '{label}'"
    return None


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **kwargs: Any,
) -> Optional[Dict[str, str]]:
    """Block memory writes containing sensitive data.

    Returns ``{"action": "block", "message": ...}`` on a hit, else ``None``.
    Inert (returns None) when not enabled for this profile.
    """
    if tool_name != "memory":
        return None
    if not _is_enabled():
        return None
    texts = _extract_text(args)
    if not texts:
        return None
    for text in texts:
        hit = _find_match(text)
        if hit:
            logger.info("privacy-scrub: blocked memory write (matched %s)", hit)
            write_alert("memory", f"regex:{hit}", text, tier="regex")
            return {
                "action": "block",
                "message": (
                    "privacy-scrub: refusing memory write — content matches "
                    f"sensitive-data {hit}. Remove the sensitive data and retry. "
                    "Persistent memory must not contain personal identifiers, "
                    "credentials, or machine-specific paths."
                ),
            }
    # Tier-1 (opt-in): LLM semantic classify for recall regex can't match.
    if os.environ.get("PRIVACY_LLM_CLASSIFY") == "1":
        for text in texts:
            try:
                verdict = classify_private(text)
            except Exception as exc:
                logger.debug("privacy-scrub: classify_private failed: %s", exc)
                verdict = None
            if verdict is True:
                logger.info("privacy-scrub: blocked memory write (LLM Tier-1)")
                write_alert("memory", "llm:semantic", text, tier="llm")
                return {
                    "action": "block",
                    "message": (
                        "privacy-scrub: refusing memory write — the content was "
                        "classified as containing private/sensitive data by the "
                        "privacy LLM. Remove or anonymize it and retry."
                    ),
                }
    return None


def register(ctx) -> None:
    """Register the pre_tool_call hook (called by the Hermes plugin loader)."""
    if not _PATTERNS.get("literal") and not _COMPILED_REGEX:
        logger.warning("privacy-scrub: no patterns loaded — hook will never block")
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    logger.info(
        "privacy-scrub registered: patterns=%d literal / %d regex, enabled=%s",
        len(_PATTERNS.get("literal", [])),
        len(_COMPILED_REGEX),
        _is_enabled(),
    )
