"""ste-code-jail-core — shared policy engine for every jail plugin.

Single source of truth. The granular plugins (``jail-fs``, ``jail-cmd``,
``jail-net``) and the shell script packet all resolve their rules through this
module, so a policy change lands in one place.

Profiles
--------
The active profile selects a policy. Resolution order:

1. ``STE_CODE_JAIL_POLICY`` environment variable (explicit override)
2. ``policy:`` in the profile's ``jail.yaml``
3. the profile name mapped through ``PROFILE_POLICY_MAP``
4. ``strict`` — fail closed when nothing matches

+---------------------+----------+------------------------------------------+
| Profile             | Policy   | Intent                                   |
+=====================+==========+==========================================+
| ``dev-ste-code``    | ``dev``  | Author the methodology. Writes anywhere  |
|                     |          | in the repo and the Hermes profile. Full |
|                     |          | tool access. Network allowed.            |
+---------------------+----------+------------------------------------------+
| ``ste-code``        | ``user`` | The shipped product. A reader: consume   |
|                     |          | the standard and artifacts, apply them   |
|                     |          | to the user's OWN project. No writes into|
|                     |          | the STE-Code checkout. No network.       |
+---------------------+----------+------------------------------------------+
| ``benchmark-``      |``bench`` | Run benchmarks under adversarially       |
| ``ste-code``        |          | generated prompts. Writes confined to the|
|                     |          | benchmark output tree only. No network.  |
|                     |          | Telemetry stays inspectable.             |
+---------------------+----------+------------------------------------------+

``user`` and ``bench`` are locked down: a malicious or confused prompt cannot
reach the rest of the machine. ``dev`` is deliberately permissive — it is the
profile you author from.

Reads are unrestricted under every policy. Confinement targets writes,
dangerous commands, and network egress.
"""

from __future__ import annotations

import fnmatch
import logging
import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

logger = logging.getLogger(__name__)

__all__ = [
    "Policy",
    "JailContext",
    "load_context",
    "resolve_project_root",
    "is_within",
    "normalize",
]

# A directory holding one of these marks a project root.
DEFAULT_ROOT_MARKERS: Sequence[str] = (".git", "Makefile", "pyproject.toml",
                                       "package.json")

PROFILE_POLICY_MAP: Dict[str, str] = {
    "dev-ste-code": "dev",
    "ste-code": "user",
    "benchmark-ste-code": "bench",
}

_MAX_WALK_DEPTH = 24


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def normalize(path: str) -> str:
    """Expand ``~``/variables and fully resolve symlinks to an absolute path."""
    expanded = os.path.expandvars(os.path.expanduser(str(path)))
    return os.path.realpath(os.path.abspath(expanded))


def is_within(path: str, root: str) -> bool:
    """True when *path* is *root* itself or lives underneath it."""
    if not root:
        return False
    if path == root:
        return True
    return path.startswith(root.rstrip(os.sep) + os.sep)


def resolve_project_root(
    start: Optional[str] = None,
    markers: Iterable[str] = DEFAULT_ROOT_MARKERS,
) -> Optional[str]:
    """Nearest ancestor of *start* containing a repository marker."""
    marker_list = [m for m in markers if m]
    origin = Path(start).resolve() if start else Path(__file__).resolve()
    current = origin if origin.is_dir() else origin.parent
    for _ in range(_MAX_WALK_DEPTH):
        for marker in marker_list:
            if (current / marker).exists():
                return normalize(str(current))
        if current.parent == current:
            break
        current = current.parent
    return None


def temp_roots() -> List[str]:
    roots = ["/tmp", "/private/tmp", "/var/folders", "/private/var/folders"]
    try:
        roots.append(tempfile.gettempdir())
    except Exception:
        pass
    return [normalize(r) for r in roots]


def hermes_home() -> str:
    return normalize(os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes"))


def active_profile() -> str:
    """Profile name derived from ``$HERMES_HOME`` (``profiles/<name>``)."""
    explicit = os.environ.get("HERMES_PROFILE")
    if explicit:
        return explicit.strip()
    home = Path(hermes_home())
    if home.parent.name == "profiles":
        return home.name
    return "default"


# ---------------------------------------------------------------------------
# Policy
# ---------------------------------------------------------------------------

@dataclass
class Policy:
    """Declarative rule set for one profile.

    Attributes:
        name: Policy identifier (``dev`` / ``user`` / ``bench``).
        write_roots: Absolute roots that may be written to.
        deny_roots: Absolute roots refused even inside a write root.
        allow_network: Whether network-capable tools may run.
        allowed_tools: When set, ONLY these tools may run (allow-list).
        denied_tools: Tools that may never run (deny-list).
        denied_commands: Shell command basenames that may never run.
        description: Human summary used in block messages.
    """

    name: str
    write_roots: List[str] = field(default_factory=list)
    deny_roots: List[str] = field(default_factory=list)
    allow_network: bool = True
    allowed_tools: Optional[List[str]] = None
    denied_tools: List[str] = field(default_factory=list)
    denied_commands: List[str] = field(default_factory=list)
    description: str = ""

    def may_write(self, resolved: str) -> Optional[str]:
        """Return a refusal reason for a write to *resolved*, else ``None``.

        Most-specific-match-wins: the longest matching write root is compared
        against the longest matching deny root. This lets a policy deny a
        parent while still allowing a directory nested inside it — needed
        because the repository's own parent is denied while the repository is
        allowed.
        """
        if not self.write_roots:
            return "no write root is permitted under this policy"

        best_allow = ""
        for root in self.write_roots:
            if is_within(resolved, root) and len(root) > len(best_allow):
                best_allow = root

        best_deny = ""
        for root in self.deny_roots:
            if is_within(resolved, root) and len(root) > len(best_deny):
                best_deny = root

        if best_deny and len(best_deny) >= len(best_allow):
            return f"path is inside a denied directory ({best_deny})"
        if best_allow:
            return None
        return "path is outside every allowed write root"

    def may_use_tool(self, tool_name: str) -> Optional[str]:
        """Return a refusal reason for running *tool_name*, else ``None``."""
        for pattern in self.denied_tools:
            if fnmatch.fnmatch(tool_name, pattern):
                return f"tool '{tool_name}' is disabled by the {self.name} policy"
        if self.allowed_tools is not None:
            if not any(fnmatch.fnmatch(tool_name, p) for p in self.allowed_tools):
                return (
                    f"tool '{tool_name}' is not in the {self.name} policy "
                    f"allow-list"
                )
        return None

    def may_run_command(self, basename: str) -> Optional[str]:
        """Return a refusal reason for running *basename*, else ``None``."""
        for pattern in self.denied_commands:
            if fnmatch.fnmatch(basename, pattern):
                return (
                    f"command '{basename}' is disabled by the {self.name} policy"
                )
        return None


# ---------------------------------------------------------------------------
# Policy construction
# ---------------------------------------------------------------------------

# Tools that reach the network. Blocked wholesale under locked-down policies.
NETWORK_TOOLS = [
    "web_search", "web_extract", "browser_*", "image_generate",
    "text_to_speech", "vision_analyze",
]

# Tools that spawn further agents or mutate agent state. Locked-down profiles
# must not be able to escalate by delegating to a less restricted context.
ESCALATION_TOOLS = ["delegate_task", "cronjob", "skill_manage", "memory"]

# Commands that reach the network or install software.
NETWORK_COMMANDS = [
    "curl", "wget", "nc", "ncat", "telnet", "ssh", "scp", "sftp", "rsync",
    "pip", "pip3", "npm", "pnpm", "yarn", "brew", "apt", "apt-get", "gem",
    "cargo", "go", "docker", "kubectl",
]


def _build_dev(project_root: Optional[str], cfg: Dict[str, Any]) -> Policy:
    """Permissive authoring policy: the repo plus this Hermes profile."""
    write: List[str] = []
    deny: List[str] = []
    if project_root:
        write.append(project_root)
        parent = os.path.dirname(project_root)
        if parent and parent != project_root:
            deny.append(parent)
    write.append(hermes_home())
    write.extend(temp_roots())
    if project_root:
        deny.append(normalize(os.path.join(project_root, ".git")))
    return Policy(
        name="dev",
        write_roots=write,
        deny_roots=deny,
        allow_network=True,
        allowed_tools=None,
        denied_tools=[],
        denied_commands=[],
        description=(
            "Development profile: full authoring access to the STE-Code "
            "repository and this Hermes profile."
        ),
    )


def _build_user(project_root: Optional[str], cfg: Dict[str, Any]) -> Policy:
    """Locked-down consumer policy.

    The user reads the standard and artifacts and applies them to their OWN
    project. The STE-Code checkout is read-only: a downloaded methodology must
    not be able to rewrite itself. Writes are confined to the workspace the
    user launched Hermes in, and network/escalation tools are off.
    """
    workspace = normalize(cfg.get("workspace") or os.getcwd())
    write: List[str] = [hermes_home()]
    write.extend(temp_roots())

    deny: List[str] = []
    # The STE-Code checkout itself is never writable under this policy, even
    # when the user launched Hermes from inside it.
    if project_root:
        deny.append(project_root)

    # Only grant the workspace when it is NOT inside the STE-Code checkout.
    # Most-specific-match-wins would otherwise let a workspace nested in the
    # repo override the repo-wide deny and make the shipped product writable
    # by itself. A user who launches from inside the checkout gets no project
    # write root at all — which is the correct locked-down outcome, and the
    # block message tells them to run from their own project directory.
    workspace_inside_repo = bool(project_root and is_within(workspace, project_root))
    if not workspace_inside_repo:
        write.insert(0, workspace)
        deny.append(normalize(os.path.join(workspace, ".git")))

    hint = (
        " Launch Hermes from your own project directory to get a writable "
        "workspace."
        if workspace_inside_repo
        else ""
    )

    return Policy(
        name="user",
        write_roots=write,
        deny_roots=deny,
        allow_network=False,
        allowed_tools=None,
        denied_tools=NETWORK_TOOLS + ESCALATION_TOOLS,
        denied_commands=NETWORK_COMMANDS,
        description=(
            "User profile: read the STE-Code standard and artifacts and apply "
            "them to your own project. The STE-Code checkout is read-only and "
            "network access is disabled." + hint
        ),
    )


def _build_bench(project_root: Optional[str], cfg: Dict[str, Any]) -> Policy:
    """Locked-down benchmark policy.

    Benchmarks execute adversarially generated prompts. Assume the prompt is
    hostile: writes are confined to the benchmark output tree, nothing else in
    the repository is writable, and network and escalation tools are off.
    Telemetry under ``$HERMES_HOME`` stays writable so runs remain inspectable.
    """
    out_dir = cfg.get("benchmark_output")
    if out_dir:
        bench_root = normalize(out_dir)
    elif project_root:
        bench_root = normalize(os.path.join(project_root, ".agents", "benchmark",
                                            "tests"))
    else:
        bench_root = normalize(os.path.join(tempfile.gettempdir(),
                                            "ste-code-benchmark"))

    write: List[str] = [bench_root, hermes_home()]
    write.extend(temp_roots())

    deny: List[str] = []
    if project_root:
        # Everything in the repo except the benchmark output tree.
        deny.append(project_root)
        parent = os.path.dirname(project_root)
        if parent and parent != project_root:
            deny.append(parent)

    return Policy(
        name="bench",
        write_roots=write,
        deny_roots=deny,
        allow_network=False,
        allowed_tools=None,
        denied_tools=NETWORK_TOOLS + ESCALATION_TOOLS,
        denied_commands=NETWORK_COMMANDS,
        description=(
            "Benchmark profile: adversarial prompts run here. Writes are "
            "confined to the benchmark output tree; the rest of the repository "
            "and the machine are read-only. Network access is disabled."
        ),
    )


_BUILDERS = {"dev": _build_dev, "user": _build_user, "bench": _build_bench}

# Unknown profiles fail closed onto the most restrictive policy.
_STRICT_FALLBACK = "bench"


# ---------------------------------------------------------------------------
# Context
# ---------------------------------------------------------------------------

@dataclass
class JailContext:
    """Everything a jail plugin needs, resolved once per session."""

    policy: Policy
    project_root: Optional[str]
    profile: str
    enforce: bool
    config: Dict[str, Any]


_context_cache: Optional[JailContext] = None


def _read_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore

        with open(path, "r", encoding="utf-8") as fh:
            loaded = yaml.safe_load(fh) or {}
        return loaded if isinstance(loaded, dict) else {}
    except FileNotFoundError:
        return {}
    except Exception as exc:
        logger.error("ste-code-jail-core: cannot read %s (%s)", path, exc)
        return {}


def _find_config() -> Dict[str, Any]:
    """Load ``jail.yaml``: profile copy first, then the shared default."""
    candidates = [
        Path(hermes_home()) / "jail.yaml",
        Path(__file__).resolve().parent / "jail.yaml",
    ]
    merged: Dict[str, Any] = {}
    for candidate in reversed(candidates):
        merged.update(_read_yaml(candidate))
    return merged


def load_context(force: bool = False) -> JailContext:
    """Resolve the policy for this session. Cached after the first call."""
    global _context_cache
    if _context_cache is not None and not force:
        return _context_cache

    cfg = _find_config()
    profile = active_profile()

    policy_name = (
        os.environ.get("STE_CODE_JAIL_POLICY")
        or cfg.get("policy")
        or PROFILE_POLICY_MAP.get(profile)
    )
    if not policy_name:
        policy_name = _STRICT_FALLBACK
        logger.warning(
            "ste-code-jail-core: profile '%s' has no policy mapping — "
            "failing closed to '%s'",
            profile,
            policy_name,
        )

    project_root = resolve_project_root(
        cfg.get("project_root") or os.getcwd(),
        cfg.get("root_markers") or DEFAULT_ROOT_MARKERS,
    )

    builder = _BUILDERS.get(str(policy_name))
    if builder is None:
        logger.error(
            "ste-code-jail-core: unknown policy '%s' — failing closed to '%s'",
            policy_name,
            _STRICT_FALLBACK,
        )
        builder = _BUILDERS[_STRICT_FALLBACK]

    policy = builder(project_root, cfg)

    # Config may widen or narrow the computed roots.
    for extra in cfg.get("extra_write_roots") or []:
        policy.write_roots.append(normalize(str(extra)))
    for extra in cfg.get("extra_deny_roots") or []:
        policy.deny_roots.append(normalize(str(extra)))

    policy.write_roots = list(dict.fromkeys(
        r for r in policy.write_roots if r and r != os.sep
    ))
    policy.deny_roots = list(dict.fromkeys(policy.deny_roots))

    _context_cache = JailContext(
        policy=policy,
        project_root=project_root,
        profile=profile,
        enforce=bool(cfg.get("enforce", True)),
        config=cfg,
    )
    return _context_cache
