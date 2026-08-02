"""ste-code-jail — group plugin assembling the three granular jail plugins.

    jail-fs    filesystem writes
    jail-cmd   tool and command use
    jail-net   network egress

Enable THIS plugin for normal use and all three components activate together
under one policy. Enable the components individually only to debug a policy or
to assemble a profile with unusual requirements.

The group imports each component's hook rather than duplicating logic, so
there is exactly one implementation of every rule and no drift between the
grouped and granular paths.

Policy is selected from the active profile by ``core.policy``:

    dev-ste-code        -> dev    permissive authoring
    ste-code            -> user   locked down, read the standard
    benchmark-ste-code  -> bench  locked down, adversarial prompts

An unmapped profile fails closed to ``bench``.
"""

from __future__ import annotations

import importlib.util
import logging
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

_HERE = Path(__file__).resolve().parent
_PLUGINS_DIR = _HERE.parent


def _find_jail_root() -> Path:
    """Locate the jail root by MARKER, never by counting parent hops.

    Hop counting encodes this file's depth in the tree: move the plugin and
    the path silently points somewhere else. That is the exact bug class this
    jail exists to prevent, so the jail must not contain it.
    """
    for candidate in _HERE.parents:
        if (candidate / "core" / "policy.py").exists():
            return candidate
    raise RuntimeError(
        "ste-code-jail: cannot locate the shared core/ package above " + __file__
    )


_JAIL_ROOT = _find_jail_root()
if str(_JAIL_ROOT) not in sys.path:
    sys.path.insert(0, str(_JAIL_ROOT))

from core.policy import load_context  # noqa: E402

# Order matters: cheapest and broadest checks first, so a denied tool is
# refused before its arguments are parsed.
COMPONENTS = ("jail-net", "jail-cmd", "jail-fs")


def _load_component(name: str):
    """Import a sibling component plugin by directory name."""
    path = _PLUGINS_DIR / name / "__init__.py"
    if not path.exists():
        logger.error("ste-code-jail: component %s not found at %s", name, path)
        return None
    spec = importlib.util.spec_from_file_location(f"ste_code_jail_{name}", path)
    if not spec or not spec.loader:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:
        logger.error("ste-code-jail: cannot load component %s (%s)", name, exc)
        return None
    return module


def _build_chain() -> List[Callable]:
    chain: List[Callable] = []
    for name in COMPONENTS:
        module = _load_component(name)
        hook = getattr(module, "_on_pre_tool_call", None) if module else None
        if callable(hook):
            chain.append(hook)
        else:
            logger.error("ste-code-jail: component %s exposes no hook", name)
    return chain


_chain: List[Callable] = []


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **kwargs: Any,
) -> Optional[Dict[str, str]]:
    """Run every component; the first refusal wins."""
    for hook in _chain:
        try:
            result = hook(tool_name=tool_name, args=args, **kwargs)
        except Exception as exc:  # a broken component must not break the agent
            logger.error("ste-code-jail: component raised (%s)", exc)
            continue
        if isinstance(result, dict) and result.get("action") == "block":
            return result
    return None


def register(ctx) -> None:
    global _chain
    _chain = _build_chain()
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)

    jail = load_context()
    logger.info(
        "ste-code-jail active: profile=%s policy=%s enforce=%s "
        "components=%d/%d write_roots=%d network=%s",
        jail.profile,
        jail.policy.name,
        jail.enforce,
        len(_chain),
        len(COMPONENTS),
        len(jail.policy.write_roots),
        "allowed" if jail.policy.allow_network else "blocked",
    )
    if len(_chain) != len(COMPONENTS):
        logger.error(
            "ste-code-jail: only %d of %d components loaded — the jail is "
            "INCOMPLETE",
            len(_chain),
            len(COMPONENTS),
        )
