"""privacy-scrub-sanitize — FEAT-ONLY in-place redaction for memory writes.

This hook complements ``privacy-scrub`` (the main-compatible, block-only guard).
Where privacy-scrub refuses the entire memory write when it detects sensitive
data, this hook uses the ``modify`` action from Hermes PR #28953
(feat/pre-tool-call-content-transform) to REDACT the sensitive substring in
place and let the rest of the entry save.

WHY A SEPARATE, FEAT-ONLY HOOK
------------------------------
The ``modify`` action does not exist on main/standard Hermes builds. Returning
``{"action": "modify", ...}`` there would be silently ignored at best. Per
project policy this hook must NOT run on a standard release, so it:

  1. Self-probes for the feat capability at registration and on every call. If
     the ``modify`` action is unavailable (main build), it returns ``None`` and
     does nothing — privacy-scrub remains the active guard.
  2. Is NOT linked into any profile and NOT enabled in any config.yaml by
     default. It only activates when the user explicitly enables it AND is
     running a feat/ build.

Detection
---------
The reliable probe is the presence of ``_dispatch_pre_tool_call_hooks`` in
``hermes_cli.plugins`` — that symbol is introduced by the feat branch and is
absent on main. We import lazily and cache the result.

Behavior
--------
On a ``memory`` tool call (target=memory/user) while enabled + on feat:
  * Scan content / operations for the same patterns as privacy-scrub
    (operator names from HERMES_OPERATOR_NAMES, email, phone, keys, home paths).
  * Replace each match with a typed placeholder (``<REDACTED:email>`` etc.).
  * Return ``{"action": "modify", "args": {scrubbed fields}}`` so Hermes merges
    the sanitized content back into the call.

The hook never rewrites the on-disk memory files itself — it transforms the
tool arguments, so the model's own write path persists the redacted text.
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

_HERE = Path(__file__).resolve().parent

# Shared Tier-1 LLM classifier + backward-chain alert writer (lives in the sibling
# privacy-scrub dir; reused so the two plugins never drift).
import sys as _sys

if str(_HERE) not in _sys.path:
    _sys.path.insert(0, str(_HERE.parent / "privacy-scrub"))
from _common import classify_private, write_alert  # noqa: E402


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


# Placeholders used when redacting a matched span. Keeping them typed makes the
# redaction self-documenting in the persisted memory entry.
_PLACEHOLDER = {
    "name": "<REDACTED:name>",
    "email": "<REDACTED:email>",
    "phone": "<REDACTED:phone>",
    "key": "<REDACTED:credential>",
    "home": "<REDACTED:home-path>",
}


def _feat_supports_modify() -> bool:
    """Probe whether the running Hermes build supports the `modify` action.

    True only on feat/pre-tool-call-content-transform (PR #28953), where
    ``hermes_cli.plugins._dispatch_pre_tool_call_hooks`` exists.
    """
    try:
        from hermes_cli import plugins as _p  # type: ignore

        return hasattr(_p, "_dispatch_pre_tool_call_hooks")
    except Exception as exc:
        logger.debug("privacy-scrub-sanitize: capability probe failed (%s)", exc)
        return False


_FEAT_OK = _feat_supports_modify()


def _load_patterns() -> Dict[str, List[str]]:
    """Load patterns from the sibling privacy-scrub config (single source).

    Operator names come from HERMES_OPERATOR_NAMES, never hard-coded here.
    """
    cfg_path = _HERE.parent / "privacy-scrub" / "config.yaml"
    literals: List[str] = []
    regexes: List[str] = []
    if cfg_path.exists():
        try:
            import yaml

            data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
            literals = [str(s).lower() for s in (data.get("literal") or [])]
            regexes = [str(s) for s in (data.get("regex") or [])]
        except Exception as exc:
            logger.error("privacy-scrub-sanitize: failed to load patterns: %s", exc)
    for raw in os.environ.get("HERMES_OPERATOR_NAMES", "").split(","):
        name = raw.strip().lower()
        if name:
            literals.append(name)
    return {"literal": literals, "regex": regexes}


_PATTERNS = _load_patterns()
_COMPILED: List[tuple] = []
for _rx in _PATTERNS.get("regex", []):
    try:
        _COMPILED.append((_rx, re.compile(_rx, re.IGNORECASE)))
    except re.error as exc:
        logger.error("privacy-scrub-sanitize: bad regex %r skipped: %s", _rx, exc)


def _is_enabled() -> bool:
    try:
        import yaml

        cfg_path = (
            Path.home() / ".hermes" / "profiles" / _active_profile() / "config.yaml"
        )
        if not cfg_path.exists():
            return False
        data = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
        spec = (data.get("plugins") or {}).get("entries", {}).get(
            "privacy-scrub-sanitize"
        ) or {}
        return bool(spec.get("enabled"))
    except Exception as exc:
        logger.debug("privacy-scrub-sanitize: enablement check failed (%s)", exc)
        return False


def _active_profile() -> str:
    return os.getenv("HERMES_PROFILE") or os.getenv("HERMES_ACTIVE_PROFILE") or ""


def _redact(text: str) -> str:
    """Return text with any sensitive span replaced by a typed placeholder."""
    out = text
    # Literal operator-name substrings (case-insensitive).
    for lit in _PATTERNS.get("literal", []):
        if lit:
            out = re.sub(re.escape(lit), _PLACEHOLDER["name"], out, flags=re.IGNORECASE)
    # Regex classes.
    for label, rx in _COMPILED:
        kind = _kind_for(label)
        out = rx.sub(_PLACEHOLDER[kind], out)
    return out


def _kind_for(label: str) -> str:
    low = label.lower()
    # Credential-shaped signatures take precedence over the generic phone regex,
    # which would otherwise also match the digit run inside a key.
    if "sk-" in low or "akia" in low or "ghp_" in low or "eyj" in low:
        return "key"
    if "home" in low or "users" in low or "users\\\\" in low:
        return "home"
    if "@" in low or "email" in low:
        return "email"
    if "\\d" in low or "digit" in low:
        return "phone"
    return "key"


def _scrub_args(args: Any) -> Optional[Dict[str, Any]]:
    """Build the `modify` partial dict for a memory call, or None if clean."""
    if not isinstance(args, dict):
        return None
    changed = False
    new_args = dict(args)  # shallow copy; we only overwrite dirty fields

    for key in ("content", "old_text", "new_text"):
        v = new_args.get(key)
        if isinstance(v, str) and v.strip():
            red = _redact(v)
            if red != v:
                new_args[key] = red
                changed = True

    ops = new_args.get("operations")
    if isinstance(ops, list):
        new_ops = []
        for op in ops:
            if isinstance(op, dict):
                op = dict(op)
                for key in ("content", "old_text", "new_text"):
                    v = op.get(key)
                    if isinstance(v, str) and v.strip():
                        red = _redact(v)
                        if red != v:
                            op[key] = red
                            changed = True
                new_ops.append(op)
            else:
                new_ops.append(op)
        if changed:
            new_args["operations"] = new_ops

    return new_args if changed else None


def _on_pre_tool_call(
    tool_name: str = "", args: Any = None, **kwargs: Any
) -> Optional[Dict[str, Any]]:
    """Redact sensitive data from memory writes in place (feat-only).

    Tier-0 (regex) produces a precise in-place scrub via the ``modify`` action.
    Tier-1 (LLM, opt-in): when regex is silent but the privacy LLM flags the
    content, we cannot locate the exact span, so we conservatively BLOCK the
    write (nothing leaks) and write a backward-chain alert.
    """
    if not _FEAT_OK:
        return None  # standard/main build: do nothing, privacy-scrub handles it
    if tool_name != "memory":
        return None
    if not _is_enabled():
        return None
    modified = _scrub_args(args)
    if modified is not None:
        return {"action": "modify", "args": modified}
    # Tier-1 (opt-in): LLM semantic classify for recall regex can't match.
    if os.environ.get("PRIVACY_LLM_CLASSIFY") == "1":
        texts = _extract_text(args)
        for text in texts:
            try:
                verdict = classify_private(text)
            except Exception as exc:
                logger.debug("privacy-scrub-sanitize: classify_private failed: %s", exc)
                verdict = None
            if verdict is True:
                logger.info("privacy-scrub-sanitize: blocked memory write (LLM Tier-1)")
                write_alert("memory", "llm:semantic", text, tier="llm")
                return {
                    "action": "block",
                    "message": (
                        "privacy-scrub-sanitize: the privacy LLM classified this "
                        "memory write as containing sensitive data and no precise "
                        "span could be located for in-place redaction, so the write "
                        "is refused. Anonymize the content and retry."
                    ),
                }
    return None


def register(ctx) -> None:
    if not _FEAT_OK:
        logger.info(
            "privacy-scrub-sanitize: modify action NOT available on this build "
            "(standard/main?) — hook disabled. Enable on feat/ build only."
        )
        return
    if not _PATTERNS.get("literal") and not _COMPILED:
        logger.warning("privacy-scrub-sanitize: no patterns loaded — hook inert")
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    logger.info(
        "privacy-scrub-sanitize registered (feat modify action): enabled=%s",
        _is_enabled(),
    )
