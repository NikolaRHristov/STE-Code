"""jail-net — block network egress when the active policy forbids it.

One of three granular jail plugins:

    jail-fs    filesystem writes
    jail-cmd   tool and command use
    jail-net   network egress        (this plugin)

Why this is separate from ``jail-cmd``: a filesystem jail stops data being
written to disk, but says nothing about data leaving the machine. For the
benchmark profile in particular — where adversarial prompts are executed by
design — exfiltration is the primary risk, and blocking egress is the control
that addresses it. Keeping it in its own plugin means it can be reasoned
about, tested, and toggled on its own.

Three gates:

1. Network-capable tools (``web_search``, ``browser_*``, ``image_generate``...)
2. URLs embedded in shell commands, catching a network client this plugin's
   basename list does not know about
3. Network calls inside ``execute_code`` (``requests``, ``urllib``, sockets)

Policy comes from ``core.policy``.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _find_jail_root() -> Path:
    """Locate the jail root by MARKER, never by counting parent hops.

    Hop counting (``parent.parent.parent``) encodes this file's depth in the
    tree: move the plugin and the path silently points somewhere else. That is
    the exact bug class this jail exists to prevent, so the jail must not
    contain it. Walk up until the shared ``core/`` package appears instead.
    """
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core" / "policy.py").exists():
            return candidate
    raise RuntimeError("jail: cannot locate the shared core/ package above " + __file__)


_JAIL_ROOT = _find_jail_root()
if str(_JAIL_ROOT) not in sys.path:
    sys.path.insert(0, str(_JAIL_ROOT))

from core.policy import load_context  # noqa: E402

# A URL or bare host:port in a shell command.
_URL_RE = re.compile(
    r"\b(?:https?|ftps?|ssh|scp|sftp|git|ws|wss)://[^\s'\"]+"
    r"|\b(?:\d{1,3}\.){3}\d{1,3}:\d+\b",
    re.IGNORECASE,
)

# Network primitives inside embedded Python/JS.
_CODE_NET_RE = re.compile(
    r"\b(?:requests\.(?:get|post|put|patch|delete|head|request)"
    r"|urllib\.request|urlopen|httpx\.|aiohttp\.|socket\.socket"
    r"|fetch\s*\(|XMLHttpRequest|axios\.|http\.client)\b"
)

# Tools that may legitimately carry a URL argument yet do not fetch it.
_EXEMPT_TOOLS = {"read_file", "search_files", "todo", "clarify"}


def _refuse(ctx, tool_name: str, evidence: str) -> Dict[str, str]:
    policy = ctx.policy
    return {
        "action": "block",
        "message": (
            f"jail-net refused this {tool_name} call under the "
            f"'{policy.name}' policy (profile: {ctx.profile}).\n\n"
            f"{policy.description}\n\n"
            f"Network access is disabled for this profile.\n"
            f"Evidence: {evidence}\n\n"
            f"Local reads and computation are still available."
        ),
    }


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if not tool_name or tool_name in _EXEMPT_TOOLS:
        return None

    ctx = load_context()
    if ctx.policy.allow_network:
        return None

    def maybe_block(evidence: str) -> Optional[Dict[str, str]]:
        if not ctx.enforce:
            logger.warning("jail-net (dry run) would block %s: %s", tool_name, evidence)
            return None
        logger.warning("jail-net blocked %s: %s", tool_name, evidence)
        return _refuse(ctx, tool_name, evidence)

    # --- gate 1: network-capable tool ---
    reason = ctx.policy.may_use_tool(tool_name)
    if reason and "disabled" in reason:
        return maybe_block(reason)

    if not isinstance(args, dict):
        return None

    # --- gate 2: a URL inside a shell command ---
    command = args.get("command")
    if isinstance(command, str):
        match = _URL_RE.search(command)
        if match:
            return maybe_block(f"command contains a network address: {match.group(0)}")

    # --- gate 3: network primitives inside embedded code ---
    code = args.get("code")
    if isinstance(code, str):
        match = _CODE_NET_RE.search(code)
        if match:
            return maybe_block(f"code performs a network call: {match.group(0)}")

    return None


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    jail = load_context()
    logger.info(
        "jail-net active (profile=%s policy=%s network=%s)",
        jail.profile,
        jail.policy.name,
        "allowed" if jail.policy.allow_network else "BLOCKED",
    )
