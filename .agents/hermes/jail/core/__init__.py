"""ste-code-jail-core — shared policy engine and path analysis for the jail.

Single source of truth. The granular plugins (``jail-fs``, ``jail-cmd``,
``jail-net``) and the shell script packet all import from here, so a rule
change lands in exactly one place.

Layout::

    core/
      policy.py     profile -> Policy resolution, containment decisions
      analysis.py   extract write targets from tool arguments
      jail.yaml     shared defaults (a profile copy may override)

Typical use from a plugin::

    from core.policy import load_context
    from core.analysis import write_targets

    ctx = load_context()
    for label, path in write_targets(tool_name, args, cwd):
        reason = ctx.policy.may_write(path)
"""

from __future__ import annotations

from .policy import (  # noqa: F401
    JailContext,
    Policy,
    is_within,
    load_context,
    normalize,
    resolve_project_root,
)

__all__ = [
    "JailContext",
    "Policy",
    "is_within",
    "load_context",
    "normalize",
    "resolve_project_root",
]
