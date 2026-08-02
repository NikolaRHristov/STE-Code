"""ste-code-jail — confine Hermes tool writes to the project repository.

Motivation
----------
Agent sessions launched from the project were creating directories *outside*
the repository — an empty ``.agents/prompts/<batch>/`` tree one level up in
the parent directory, and a stray ``<sibling>/.agents/``. Root cause: pipeline
scripts derive their project root with a fixed number of ``parent`` hops
(``Path(__file__).resolve().parent.parent.parent``); when a script moves one
directory deeper or shallower, the root silently points at the *parent* of the
repository and every write lands there. Hermes itself only *warns* about
workspace escapes (``_path_resolution_warning`` in ``tools/file_tools.py``) —
it never blocks.

This plugin blocks them.

Design
------
* Hooks ``pre_tool_call`` and returns ``{"action": "block", "message": ...}``
  for any tool call whose **write target** resolves outside the jail.
* **Reads are never restricted.** The agent may still read anything on the
  machine — that access is deliberate and stays.
* **No machine-specific paths.** The project root is discovered by walking up
  from this plugin directory until an ancestor contains a repository marker
  (``.git``, ``Makefile``, ... — configurable). Clone the repo anywhere and
  the jail anchors itself correctly.
* Write targets are extracted per tool:

  ``write_file``    -> ``path``
  ``patch``         -> ``path`` (replace mode) and every
                       ``*** Add/Update/Delete File:`` header in a V4A body
  ``skill_manage``  -> ``file_path`` resolved under the profile skills dir
  ``terminal``      -> ``workdir`` plus every absolute-looking path token in
                       ``command``, but only when the command contains a write
                       verb (``mkdir``, ``>``, ``tee``, ``cp``, ``mv``, ``rm``,
                       ``sed -i``, ...)

* Relative paths are resolved against the live terminal cwd when Hermes can
  report it, else ``os.getcwd()``.
* Containment is checked on the **fully resolved** path (``os.path.realpath``),
  so a symlink pointing out of the jail does not widen it.

Configuration lives in ``jail.yaml`` next to this file. Set ``enforce: false``
for a dry run (violations are logged, nothing is blocked).
"""

from __future__ import annotations

import logging
import os
import re
import shlex
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

logger = logging.getLogger(__name__)

_HERE = Path(__file__).resolve().parent
_CONFIG_PATH = _HERE / "jail.yaml"

_DEFAULT_ROOT_MARKERS = (".git", "Makefile", "pyproject.toml", "package.json")


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

_DEFAULT_CONFIG: Dict[str, Any] = {
    "enforce": True,
    "root_markers": list(_DEFAULT_ROOT_MARKERS),
    "extra_roots": [],
    "allow_hermes_home": True,
    "allow_temp": True,
    "deny": [],
}

_config_cache: Optional[Dict[str, Any]] = None


def _norm(path: str) -> str:
    """Expand ``~``/vars and fully resolve symlinks to an absolute path."""
    expanded = os.path.expandvars(os.path.expanduser(str(path)))
    return os.path.realpath(os.path.abspath(expanded))


def _discover_project_root(markers: Iterable[str]) -> Optional[str]:
    """Walk up from this plugin dir to the nearest ancestor holding a marker.

    Returns the deepest-first match so a nested checkout anchors to itself
    rather than to an outer repository.
    """
    marker_list = [m for m in markers if m]
    for candidate in _HERE.parents:
        for marker in marker_list:
            if (candidate / marker).exists():
                return _norm(str(candidate))
    return None


def _temp_roots() -> List[str]:
    roots = ["/tmp", "/private/tmp", "/var/folders", "/private/var/folders"]
    try:
        roots.append(tempfile.gettempdir())
    except Exception:
        pass
    return roots


def _load_config() -> Dict[str, Any]:
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    cfg = dict(_DEFAULT_CONFIG)
    try:
        import yaml  # type: ignore

        with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
            loaded = yaml.safe_load(fh) or {}
        if isinstance(loaded, dict):
            cfg.update(loaded)
    except FileNotFoundError:
        logger.warning("ste-code-jail: %s not found — using defaults", _CONFIG_PATH)
    except Exception as exc:
        logger.error(
            "ste-code-jail: cannot read %s (%s) — jail is INACTIVE", _CONFIG_PATH, exc
        )
        cfg["_roots"] = []
        cfg["_deny"] = []
        cfg["_project_root"] = None
        _config_cache = cfg
        return cfg

    markers = cfg.get("root_markers") or list(_DEFAULT_ROOT_MARKERS)
    project_root = _discover_project_root(markers)
    if not project_root:
        logger.error(
            "ste-code-jail: no project root found above %s (markers: %s) — "
            "jail is INACTIVE",
            _HERE,
            ", ".join(markers),
        )

    roots: List[str] = []
    if project_root:
        roots.append(project_root)
    roots += [_norm(r) for r in (cfg.get("extra_roots") or [])]

    if cfg.get("allow_hermes_home", True):
        hermes_home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
        roots.append(_norm(hermes_home))

    if cfg.get("allow_temp", True):
        roots += [_norm(r) for r in _temp_roots()]

    # Deny entries may be relative to the project root.
    deny: List[str] = []
    for entry in cfg.get("deny") or []:
        text = str(entry)
        if os.path.isabs(os.path.expanduser(text)):
            deny.append(_norm(text))
        elif project_root:
            deny.append(_norm(os.path.join(project_root, text)))

    cfg["_project_root"] = project_root
    cfg["_roots"] = [r for r in dict.fromkeys(roots) if r and r != os.sep]
    cfg["_deny"] = list(dict.fromkeys(deny))
    _config_cache = cfg
    return cfg


# ---------------------------------------------------------------------------
# Containment
# ---------------------------------------------------------------------------

def _is_within(path: str, root: str) -> bool:
    """True when *path* is *root* itself or lives underneath it."""
    if path == root:
        return True
    return path.startswith(root.rstrip(os.sep) + os.sep)


def _current_cwd() -> str:
    """Best-effort live working directory for the agent's terminal session."""
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


def _resolve_for_check(raw: str, base: Optional[str] = None) -> str:
    """Resolve *raw* to an absolute realpath, anchoring relatives at *base*.

    ``realpath`` on a path that does not exist yet still normalises ``..`` and
    resolves the symlinks of the ancestors that *do* exist — exactly what a
    containment check needs for a file about to be created.
    """
    expanded = os.path.expandvars(os.path.expanduser(str(raw)))
    if not os.path.isabs(expanded):
        expanded = os.path.join(base or _current_cwd(), expanded)
    return os.path.realpath(os.path.abspath(expanded))


def _violates(resolved: str, cfg: Dict[str, Any]) -> Optional[str]:
    """Return a human reason when *resolved* is not writable, else ``None``."""
    roots: List[str] = cfg.get("_roots") or []
    if not roots:
        return None  # No jail configured — allow everything.

    for denied in cfg.get("_deny") or []:
        if _is_within(resolved, denied):
            return f"path is inside an explicitly denied directory ({denied})"

    if any(_is_within(resolved, root) for root in roots):
        return None

    return "path is outside every allowed root"


# ---------------------------------------------------------------------------
# Write-target extraction
# ---------------------------------------------------------------------------

# V4A patch headers naming a file the patch will create or modify.
_PATCH_FILE_RE = re.compile(
    r"^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+?)\s*$",
    re.MULTILINE,
)

# Commands that can create or modify something on disk.
_WRITE_VERBS = (
    "mkdir", "touch", "cp", "mv", "rm", "rmdir", "ln", "tee", "dd", "rsync",
    "install", "truncate", "chmod", "chown", "unzip", "tar", "git clone",
    "git init", "git worktree add",
)

# Shell redirections that write (excludes 2>&1-style fd duplication).
_REDIRECT_RE = re.compile(r"(?<![0-9<>])>>?(?!&)")

# A token that looks like an absolute POSIX path (not a flag, not a URL).
_ABS_PATH_TOKEN_RE = re.compile(r"^(?:~|/)[^\s]*$")


def _command_writes(command: str) -> bool:
    """Heuristic: does this shell command create or modify files?"""
    lowered = command.lower()
    if _REDIRECT_RE.search(command):
        return True
    if re.search(r"\bsed\b[^|;]*\s-[^\s]*i\b", lowered):
        return True
    if re.search(r"\b(?:perl|ruby)\b[^|;]*\s-[^\s]*i\b", lowered):
        return True
    for verb in _WRITE_VERBS:
        if re.search(r"(?:^|[\s;&|(])" + re.escape(verb) + r"(?:[\s;&|)]|$)", lowered):
            return True
    return False


def _iter_command_paths(command: str) -> Iterable[str]:
    """Yield absolute-looking path tokens from a shell command string."""
    try:
        tokens = shlex.split(command, comments=True)
    except ValueError:
        tokens = command.split()
    for token in tokens:
        token = token.strip()
        if not token or token.startswith("-"):
            continue
        if "://" in token:  # URL, not a filesystem path
            continue
        if _ABS_PATH_TOKEN_RE.match(token):
            yield token


def _skill_root() -> str:
    hermes_home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    return os.path.join(hermes_home, "skills")


def _targets(tool_name: str, args: Dict[str, Any]) -> List[Tuple[str, str]]:
    """Return ``(label, raw_path)`` pairs this call would write to."""
    out: List[Tuple[str, str]] = []

    if tool_name == "write_file":
        path = args.get("path")
        if isinstance(path, str) and path:
            out.append(("write_file(path)", path))

    elif tool_name == "patch":
        mode = args.get("mode") or "replace"
        if mode == "patch":
            body = args.get("patch")
            if isinstance(body, str):
                for match in _PATCH_FILE_RE.finditer(body):
                    out.append(("patch(*** File)", match.group(1)))
        else:
            path = args.get("path")
            if isinstance(path, str) and path:
                out.append(("patch(path)", path))

    elif tool_name == "skill_manage":
        file_path = args.get("file_path")
        if isinstance(file_path, str) and file_path:
            if os.path.isabs(os.path.expanduser(file_path)):
                out.append(("skill_manage(file_path)", file_path))
            else:
                name = str(args.get("name") or "")
                out.append((
                    "skill_manage(file_path)",
                    os.path.join(_skill_root(), name, file_path),
                ))

    elif tool_name == "terminal":
        workdir = args.get("workdir")
        if isinstance(workdir, str) and workdir:
            out.append(("terminal(workdir)", workdir))
        command = args.get("command")
        if isinstance(command, str) and command and _command_writes(command):
            for token in _iter_command_paths(command):
                out.append(("terminal(command)", token))

    return out


# ---------------------------------------------------------------------------
# Hook
# ---------------------------------------------------------------------------

_WATCHED_TOOLS = {"write_file", "patch", "skill_manage", "terminal"}


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if tool_name not in _WATCHED_TOOLS:
        return None
    if not isinstance(args, dict):
        return None

    cfg = _load_config()
    roots: List[str] = cfg.get("_roots") or []
    if not roots:
        return None

    base = _current_cwd()
    violations: List[str] = []

    for label, raw in _targets(tool_name, args):
        try:
            resolved = _resolve_for_check(raw, base)
        except Exception:
            continue
        reason = _violates(resolved, cfg)
        if reason:
            violations.append(f"  - {label}: {raw!r} -> {resolved} ({reason})")

    if not violations:
        return None

    allowed = "\n".join(f"  - {r}" for r in roots)
    detail = "\n".join(violations)

    if not cfg.get("enforce", True):
        logger.warning("ste-code-jail (dry run) would block %s:\n%s", tool_name, detail)
        return None

    logger.warning("ste-code-jail blocked %s:\n%s", tool_name, detail)
    return {
        "action": "block",
        "message": (
            f"ste-code-jail refused this {tool_name} call: the write target "
            f"resolves OUTSIDE the allowed roots.\n\n"
            f"Offending target(s):\n{detail}\n\n"
            f"Allowed write roots:\n{allowed}\n\n"
            f"Working directory used to resolve relative paths: {base}\n\n"
            f"This almost always means a project-root variable was computed with "
            f"the wrong number of parent hops, or an absolute path was guessed "
            f"rather than checked. Recompute the path relative to the project "
            f"root and retry. Reads are not restricted — only writes."
        ),
    }


def register(ctx) -> None:
    ctx.register_hook("pre_tool_call", _on_pre_tool_call)
    cfg = _load_config()
    logger.info(
        "ste-code-jail active (enforce=%s, root=%s, %d allowed root(s))",
        cfg.get("enforce", True),
        cfg.get("_project_root"),
        len(cfg.get("_roots") or []),
    )
