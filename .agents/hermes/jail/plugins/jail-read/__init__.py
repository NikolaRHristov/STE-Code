"""jail-read - confine filesystem READS to the roots the active policy allows.

A fourth granular jail plugin, added alongside jail-fs / jail-cmd / jail-net:

    jail-fs    filesystem writes
    jail-cmd   tool and command use
    jail-net   network egress
    jail-read  filesystem reads   (this plugin)

Why this exists
--------------

The other layers leave READS open by design: a benchmark session must be able
to read the STE-Code standard and the benchmark harness to do its work. But
"open reads" also meant a bench delegate or poll worker could ``read_file`` the
host's kernel tree, another profile's ``.env`` / ``auth.json`` / ``config.yaml``,
or a sibling profile's session state. That is exactly the surrounding the
operator wants hidden from the contained mini-sessions.

This plugin gates the two read tools - ``read_file`` (its ``path`` argument) and
``search_files`` (its ``path`` argument, when given) - against
``Policy.may_read``. The deny list is built once per session in
``core.policy._read_deny_roots_for``: the OS / kernel tree, every profile's
control surface, and every *sibling* profile directory. The repository itself
(stock standard, benchmark harness) stays readable, because those are the
task's legitimate inputs.

Opacity is the point
-------------------

When a read is refused the returned message to the MODEL is deliberately
non-descriptive - "This read is not permitted in the current environment." It
does NOT name the jail, the policy, the denied path, or the writable roots. The
operator keeps full visibility through the log line (which records the plugin,
the policy, the path and the reason); the model only learns the action was
refused. That is what lets a contained mini-session run "blind" - it can adapt
to a refusal without ever learning there is a jail.

Scope: this plugin inspects tool ARGUMENTS, like jail-fs. For kernel-enforced
read denial of opaque subprocesses, extend ``scripts/jail-lib.sh`` (the
Seatbelt emitter) to add ``(deny file-read*)`` for the same roots; this plugin
covers the agent's direct read tools.

Policy comes from ``core.policy`` - the single source of truth.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


# The shared core lives beside the plugins, not inside them.
def _find_jail_root() -> Path:
    """Locate the jail root by MARKER, never by counting parent hops."""
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core" / "policy.py").exists():
            return candidate
    raise RuntimeError(
        "jail-read: cannot locate the shared core/ package above " + __file__
    )


_JAIL_ROOT = _find_jail_root()
if str(_JAIL_ROOT) not in sys.path:
    sys.path.insert(0, str(_JAIL_ROOT))

from core.policy import load_context, normalize  # noqa: E402

# Tools whose arguments can name a read target.
WATCHED_TOOLS = {"read_file", "search_files"}


def _current_cwd() -> str:
    """Best-effort live working directory of the agent's terminal session."""
    try:
        from tools import terminal_tools  # type: ignore

        for attr in ("get_current_cwd", "current_cwd", "get_cwd"):
            fn = getattr(terminal_tools, attr, None)
            if callable(fn):
                value = fn()
                if isinstance(value, str) and value:
                    return value
    except Exception:
        pass
    return os.getcwd()


# The neutral message the model receives. Deliberately omits jail / policy /
# path / roots. The log line carries the diagnostic detail instead.
_NEUTRAL_REFUSAL = "This read is not permitted in the current environment."


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if tool_name not in WATCHED_TOOLS or not isinstance(args, dict):
        return None

    path = args.get("path")
    if not isinstance(path, str) or not path.strip():
        return None

    ctx = load_context()
    policy = ctx.policy

    # dev has no read denies; short-circuit without noise.
    if not policy.read_deny_roots:
        return None

    base = _current_cwd()
    resolved = normalize(os.path.join(base, path) if not os.path.isabs(path) else path)

    reason = policy.may_read(resolved)
    if not reason:
        return None

    # Log stays verbose for the operator; the model gets the neutral text.
    logger.warning(
        "jail-read blocked %s: %s (resolved=%s, policy=%s profile=%s)",
        tool_name,
        reason,
        resolved,
        policy.name,
        ctx.profile,
    )

    if not ctx.enforce:
        logger.warning("jail-read (dry run) would block %s", tool_name)
        return None

    return {
        "action": "block",
        "message": _NEUTRAL_REFUSAL,
    }


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    jail = load_context()
    logger.info(
        "jail-read active (profile=%s policy=%s read_deny_roots=%d)",
        jail.profile,
        jail.policy.name,
        len(jail.policy.read_deny_roots),
    )
