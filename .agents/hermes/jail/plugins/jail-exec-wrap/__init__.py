"""jail-exec-wrap - force opaque subprocesses through the kernel sandbox.

One of the granular jail plugins:

    jail-fs         filesystem writes      (argument inspection)
    jail-cmd        tool and command use   (argument inspection)
    jail-net        network egress         (argument inspection)
    jail-exec-wrap  opaque subprocesses    (kernel enforcement, this plugin)

Why this exists
---------------
``jail-fs`` inspects tool ARGUMENTS. It reads the ``command`` string and the
``path`` argument and decides from the text alone. That works for
``write_file(path="...")`` and for a plain ``echo x > y``, and it is blind to
everything a subprocess does after it starts:

    terminal(command="python3 build.py")

Nothing in that string names a write target. ``build.py`` may call
``os.makedirs("../../ste-code")`` and the argument inspector cannot know. A
live probe confirmed the gap: under the ``bench`` policy a bare
``python3 -c "open('<repo>/.agents/tmp/CANARY','w')"`` **succeeded**, while the
same command wrapped in ``jail-exec.sh`` raised ``PermissionError``.

So the kernel has to enforce it. ``scripts/jail-exec.sh`` runs a command under
Seatbelt (macOS) or bubblewrap (Linux) using the same policy roots the plugins
use. It already existed - but wrapping was OPT-IN, and an adversarial prompt
does not volunteer to jail itself.

This plugin removes the choice. Under a locked-down policy every ``terminal``
and ``execute_code`` call is rewritten in place to run inside the sandbox.

How the rewrite works
---------------------
``pre_tool_call`` hooks receive the same ``args`` dict the executor later runs
(``agent/tool_executor.py`` passes ``final_args`` to the hook, then executes
that same object). Mutating ``args`` in place therefore changes what runs. This
was verified directly rather than assumed.

The rewrite is a wrap, not a rejection: legitimate work still runs, it simply
runs confined. A command the kernel refuses fails with ``Operation not
permitted``, which is the correct and legible outcome.

Scope
-----
The ``dev`` policy is deliberately NOT wrapped. Authoring needs to build,
install, and run tools that write across the repository and the profile tree,
and wrapping dev would break the workflow this project is developed with.
Wrapping applies to ``user`` and ``bench`` - the policies that assume the
prompt may be hostile.
"""

from __future__ import annotations

import logging
import os
import shlex
import sys
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


def _find_jail_root() -> Path:
    """Locate the jail root by MARKER, never by counting parent hops."""
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "core" / "policy.py").exists():
            return candidate
    raise RuntimeError("jail: cannot locate the shared core/ package above " + __file__)


_JAIL_ROOT = _find_jail_root()
if str(_JAIL_ROOT) not in sys.path:
    sys.path.insert(0, str(_JAIL_ROOT))

from core.policy import load_context  # noqa: E402

# Policies whose prompts are assumed hostile. `dev` is excluded on purpose.
WRAPPED_POLICIES = {"user", "bench"}

# Marker proving a command is already wrapped, so a re-entrant hook call
# cannot nest sandboxes.
_MARKER = "STE_CODE_JAILED=1"

_WRAP_SCRIPT = _JAIL_ROOT / "scripts" / "jail-exec.sh"


def _wrap(command: str, policy_name: str) -> str:
    """Return *command* rewritten to execute inside the kernel sandbox."""
    inner = f"{_MARKER} exec {command}"
    return (
        f"STE_CODE_JAIL_POLICY={shlex.quote(policy_name)} "
        f"{shlex.quote(str(_WRAP_SCRIPT))} "
        f"/bin/sh -c {shlex.quote(inner)}"
    )


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if tool_name not in {"terminal", "execute_code"} or not isinstance(args, dict):
        return None

    ctx = load_context()
    policy = ctx.policy
    if policy.name not in WRAPPED_POLICIES or not ctx.enforce:
        return None

    if not _WRAP_SCRIPT.exists():
        # Fail closed: a locked-down policy that cannot reach its sandbox must
        # not silently downgrade to argument inspection alone.
        return {
            "action": "block",
            "message": "This action is not permitted in the current environment.",
        }

    # `execute_code` runs Python in-process on the Hermes side; it cannot be
    # wrapped by rewriting a shell string. Refuse it under locked policies -
    # its terminal() calls would otherwise escape argument inspection.
    if tool_name == "execute_code":
        return {
            "action": "block",
            "message": "This action is not permitted in the current environment.",
        }

    command = args.get("command")
    if not isinstance(command, str) or not command.strip():
        return None
    if _MARKER in command or "jail-exec.sh" in command:
        return None  # already confined

    # A `bench` session may spawn adversarial sub-sessions (delegate_task /
    # cronjob). Those children must inherit the SAME policy, not fall back to
    # whatever policy the spawner's shell happened to carry. Force it.
    policy_name = policy.name
    if policy_name == "bench":
        os.environ["STE_CODE_JAIL_POLICY"] = "bench"
        os.environ["HERMES_PROFILE"] = "benchmark-ste-code"

    original = command
    args["command"] = _wrap(command, policy_name)
    logger.info(
        "jail-exec-wrap: confined a %s call under the %s policy",
        tool_name,
        policy_name,
    )
    logger.debug("jail-exec-wrap: %s  ->  %s", original, args["command"])
    return None


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    jail = load_context()
    wrapped = jail.policy.name in WRAPPED_POLICIES
    logger.info(
        "jail-exec-wrap active (profile=%s policy=%s wrapping=%s)",
        jail.profile,
        jail.policy.name,
        "on" if wrapped else "off (dev is not wrapped)",
    )
