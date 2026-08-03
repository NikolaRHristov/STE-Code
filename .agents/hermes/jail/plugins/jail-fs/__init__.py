"""jail-fs - confine filesystem writes to the roots the active policy allows.

One of three granular jail plugins. Each guards a single concern and can be
enabled independently:

    jail-fs    filesystem writes      (this plugin)
    jail-cmd   tool and command use
    jail-net   network egress

``ste-code-jail`` is the group plugin that enables all three together. Enable
the group for normal use; enable the parts individually to debug a policy or
to build a profile with unusual requirements.

Policy comes from ``core.policy`` - the single source of truth shared by every
plugin and by the shell script packet.

Scope: this plugin inspects tool ARGUMENTS. It cannot see inside an opaque
subprocess (``python3 build.py`` calling ``os.makedirs("../x")``). Wrap those
in ``scripts/jail-exec.sh`` for kernel-enforced confinement.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# The shared core lives beside the plugins, not inside them.
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

from core.analysis import (  # noqa: E402
    containment_violations,
    is_passthrough_device,
    write_targets,
)
from core.policy import load_context  # noqa: E402

# Tools whose arguments can name a write destination.
WATCHED_TOOLS = {"write_file", "patch", "skill_manage", "terminal", "execute_code"}


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


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if tool_name not in WATCHED_TOOLS or not isinstance(args, dict):
        return None

    ctx = load_context()
    policy = ctx.policy
    base = _current_cwd()

    try:
        targets = write_targets(tool_name, args, base)
    except Exception as exc:  # never break the agent on a parse bug
        logger.error("jail-fs: analysis failed for %s (%s)", tool_name, exc)
        return None

    seen: set = set()
    violations: List[str] = []

    # Structural invariants first: these hold regardless of the write roots.
    # A skill traversal that lands inside an allowed directory is still an
    # escape from the skill's own sandbox.
    for label, reason in containment_violations(tool_name, args, base):
        violations.append(f"  - {label}: {reason}")

    for label, resolved in targets:
        if resolved in seen:
            continue
        seen.add(resolved)
        # `2>/dev/null` and friends write to a character device, not a file.
        # Gating them blocks ordinary read commands and teaches the operator
        # to distrust the jail, which is worse than the risk it removes.
        if is_passthrough_device(resolved):
            continue
        reason = policy.may_write(resolved)
        if reason:
            violations.append(f"  - {label}: {resolved} ({reason})")

    if not violations:
        return None

    detail = "\n".join(violations)
    allowed = "\n".join(f"  - {r}" for r in policy.write_roots) or "  (none)"

    if not ctx.enforce:
        logger.warning("jail-fs (dry run) would block %s:\n%s", tool_name, detail)
        return None

    logger.warning("jail-fs blocked %s:\n%s", tool_name, detail)
    # The returned message is deliberately non-descriptive: it must NOT name
    # the jail, the policy, the writable roots, or the offending path. The
    # operator sees all of that in the log line above; the model only learns
    # the action was refused, so a contained mini-session stays "blind" to the
    # existence of the jail.
    return {
        "action": "block",
        "message": "This action is not permitted in the current environment.",
    }


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    jail = load_context()
    logger.info(
        "jail-fs active (profile=%s policy=%s enforce=%s roots=%d)",
        jail.profile,
        jail.policy.name,
        jail.enforce,
        len(jail.policy.write_roots),
    )
