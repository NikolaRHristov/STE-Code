"""jail-cmd — gate which tools and shell commands the active policy permits.

One of three granular jail plugins:

    jail-fs    filesystem writes
    jail-cmd   tool and command use   (this plugin)
    jail-net   network egress

Two independent gates:

**Tool gating.** A policy may deny tools outright (``delegate_task``,
``cronjob``, ``skill_manage``, ``memory``) or specify an allow-list. Denying
delegation matters for the locked-down profiles: without it an adversarial
prompt could spawn a subagent and inherit a weaker context.

**Command gating.** Shell command basenames are checked against the policy's
deny list, including commands hidden inside ``sh -c '...'``. This stops
package installs and network clients that a filesystem jail alone would allow.

Policy comes from ``core.policy``.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    raise RuntimeError(
        "jail: cannot locate the shared core/ package above " + __file__
    )


_JAIL_ROOT = _find_jail_root()
if str(_JAIL_ROOT) not in sys.path:
    sys.path.insert(0, str(_JAIL_ROOT))

from core.analysis import command_basenames  # noqa: E402
from core.policy import load_context  # noqa: E402


def _refuse(ctx, reason: str, tool_name: str, extra: str = "") -> Dict[str, str]:
    policy = ctx.policy
    return {
        "action": "block",
        "message": (
            f"jail-cmd refused this {tool_name} call under the "
            f"'{policy.name}' policy (profile: {ctx.profile}).\n\n"
            f"{policy.description}\n\n"
            f"Reason: {reason}\n"
            f"{extra}\n"
            f"Reads and local computation are still available."
        ).rstrip()
        + "\n",
    }


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if not tool_name:
        return None

    ctx = load_context()
    policy = ctx.policy

    # --- gate 1: is this tool permitted at all? ---
    reason = policy.may_use_tool(tool_name)
    if reason:
        if not ctx.enforce:
            logger.warning("jail-cmd (dry run) would block tool %s", tool_name)
        else:
            logger.warning("jail-cmd blocked tool %s: %s", tool_name, reason)
            return _refuse(ctx, reason, tool_name)

    # --- gate 2: does a shell command invoke a denied binary? ---
    if tool_name != "terminal" or not isinstance(args, dict):
        return None
    command = args.get("command")
    if not isinstance(command, str) or not command:
        return None

    try:
        names = command_basenames(command)
    except Exception as exc:
        logger.error("jail-cmd: cannot parse command (%s)", exc)
        return None

    blocked: List[str] = []
    for name in names:
        why = policy.may_run_command(name)
        if why and why not in blocked:
            blocked.append(why)

    if not blocked:
        return None

    detail = "\n".join(f"  - {b}" for b in blocked)
    if not ctx.enforce:
        logger.warning("jail-cmd (dry run) would block command:\n%s", detail)
        return None

    logger.warning("jail-cmd blocked command:\n%s", detail)
    return _refuse(
        ctx,
        "the command invokes a binary this policy disallows",
        tool_name,
        extra=f"\nDisallowed:\n{detail}\n",
    )


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    jail = load_context()
    logger.info(
        "jail-cmd active (profile=%s policy=%s denied_tools=%d denied_cmds=%d)",
        jail.profile,
        jail.policy.name,
        len(jail.policy.denied_tools),
        len(jail.policy.denied_commands),
    )
