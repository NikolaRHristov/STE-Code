"""ste-code-jail — confine Hermes tool writes to the project repository.

Motivation
----------
Agent sessions launched from this project created directories *outside* the
repository: an empty ``.agents/prompts/<batch>/`` tree one level up, and a
stray ``<sibling>/.agents/``. Root cause: pipeline scripts derive their
project root by counting parent hops (``Path(__file__).resolve().parent.parent
.parent``). The hop count encodes the script's depth; move the script and the
root silently becomes an *ancestor* of the repo, where ``os.makedirs`` happily
builds the tree. Hermes only *warns* about this
(``_path_resolution_warning`` in ``tools/file_tools.py``) — it never blocks.

Two enforcement layers
----------------------
**Layer 1 (this module) — argument inspection.** A ``pre_tool_call`` hook that
resolves every path a tool call would write to and blocks the call when any of
them lands outside the allowed roots. Cross-platform, no privileges required.

**Layer 2 — kernel confinement.** ``scripts/jail-exec.sh`` wraps a command in
``sandbox-exec`` (macOS) or ``bwrap`` (Linux) so the *kernel* refuses the
write. This is the only layer that can stop an opaque subprocess.

Layer 1 is honest about its ceiling: a shell command is not statically
analysable in general. ``python3 build.py`` may call ``os.makedirs("../x")``
and no argument inspection can know. Layer 1 catches every mistake that is
visible in the arguments — which is the whole observed failure class — and
layer 2 catches the rest. See ``README.md`` § Threat model.

What layer 1 checks
-------------------
``write_file``    ``path``
``patch``         ``path``; every ``*** Add/Update/Delete File:`` header
``skill_manage``  ``file_path`` under the profile skills dir
``execute_code``  path literals in ``code`` when it performs a write
``terminal``      ``workdir``; per-segment analysis of ``command`` that
                  tracks ``cd``, expands environment variables, follows
                  redirections, understands write verbs and their target
                  positions, and recurses into ``-c``/``-e`` inline scripts

Relative paths resolve against the live terminal cwd. Containment is tested on
the fully resolved ``realpath``, so symlinks cannot widen the jail.

Configuration lives in ``jail.yaml``. ``enforce: false`` gives a dry run.
"""

from __future__ import annotations

import logging
import os
import re
import shlex
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

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
    """Expand ``~``/variables and fully resolve symlinks to an absolute path."""
    expanded = os.path.expandvars(os.path.expanduser(str(path)))
    return os.path.realpath(os.path.abspath(expanded))


def _discover_project_root(markers: Iterable[str]) -> Optional[str]:
    """Nearest ancestor of this plugin holding a repository marker."""
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
        cfg.update({"_roots": [], "_deny": [], "_project_root": None})
        _config_cache = cfg
        return cfg

    markers = cfg.get("root_markers") or list(_DEFAULT_ROOT_MARKERS)
    project_root = _discover_project_root(markers)
    if not project_root:
        logger.error(
            "ste-code-jail: no project root above %s (markers: %s) — jail INACTIVE",
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

    deny: List[str] = []
    for entry in cfg.get("deny") or []:
        text = str(entry)
        if os.path.isabs(os.path.expanduser(text)):
            deny.append(_norm(text))
        elif project_root:
            deny.append(_norm(os.path.join(project_root, text)))

    # Never let a broad root (temp, $HERMES_HOME) make the repository's own
    # PARENT writable. Without this, a checkout under /tmp — or any allowed
    # tree — would silently permit the exact escape this plugin exists to
    # stop, because the parent sits inside that tree. Denies are evaluated
    # before allows, so this holds regardless of root ordering.
    if project_root:
        parent = os.path.dirname(project_root)
        if parent and parent != project_root:
            already_root = any(_norm(r) == parent for r in (cfg.get("extra_roots") or []))
            if not already_root:
                deny.append(parent)

    cfg["_project_root"] = project_root
    cfg["_roots"] = [r for r in dict.fromkeys(roots) if r and r != os.sep]
    cfg["_deny"] = list(dict.fromkeys(deny))
    _config_cache = cfg
    return cfg


# ---------------------------------------------------------------------------
# Containment
# ---------------------------------------------------------------------------

def _is_within(path: str, root: str) -> bool:
    if path == root:
        return True
    return path.startswith(root.rstrip(os.sep) + os.sep)


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


def _expand(raw: str) -> str:
    """Expand ``~`` and environment variables, including ``${VAR}`` form."""
    return os.path.expandvars(os.path.expanduser(str(raw)))


def _resolve_for_check(raw: str, base: str) -> str:
    """Resolve *raw* to an absolute realpath, anchoring relatives at *base*.

    ``realpath`` normalises ``..`` and resolves the symlinks of the ancestors
    that already exist — what containment needs for a not-yet-created file.
    """
    expanded = _expand(raw)
    if not os.path.isabs(expanded):
        expanded = os.path.join(base, expanded)
    return os.path.realpath(os.path.abspath(expanded))


def _violates(resolved: str, cfg: Dict[str, Any]) -> Optional[str]:
    """Return a reason when *resolved* is not writable, else ``None``.

    Precedence is **most-specific-match-wins**, not deny-all-first. A path is
    judged by the longest allowed root and the longest deny entry that contain
    it; the deeper of the two decides.

    This matters because the repository's own parent is denied (so a checkout
    inside ``/tmp`` cannot use the temp allowance to write one level up), yet
    the repository itself lives *inside* that denied parent. A naive
    deny-first rule would refuse every write in the project. Comparing depths
    resolves it: the repo root is a longer prefix than its parent, so writes
    inside the repo are allowed while writes to the parent are refused.
    """
    roots: List[str] = cfg.get("_roots") or []
    if not roots:
        return None

    best_allow = ""
    for root in roots:
        if _is_within(resolved, root) and len(root) > len(best_allow):
            best_allow = root

    best_deny = ""
    for denied in cfg.get("_deny") or []:
        if _is_within(resolved, denied) and len(denied) > len(best_deny):
            best_deny = denied

    if best_deny and len(best_deny) >= len(best_allow):
        return f"path is inside a denied directory ({best_deny})"

    if best_allow:
        return None

    return "path is outside every allowed root"


# ---------------------------------------------------------------------------
# Shell command analysis
# ---------------------------------------------------------------------------

_PATCH_FILE_RE = re.compile(
    r"^\*\*\*\s+(?:Add|Update|Delete)\s+File:\s*(.+?)\s*$", re.MULTILINE
)

# Command-name -> which arguments are write targets.
#   "all"  every non-flag operand
#   "last" only the final operand (cp/mv/install semantics)
_WRITE_COMMANDS: Dict[str, str] = {
    "mkdir": "all", "touch": "all", "rm": "all", "rmdir": "all",
    "truncate": "all", "chmod": "all", "chown": "all", "mkfifo": "all",
    "mktemp": "all", "unlink": "all", "shred": "all",
    "cp": "last", "mv": "last", "install": "last", "rsync": "last",
    "ln": "last", "tee": "all", "dd": "all", "zip": "all", "tar": "all",
    "unzip": "all", "curl": "all", "wget": "all", "git": "all",
    "sed": "all", "perl": "all", "ruby": "all", "awk": "all",
}

# Interpreters whose inline-script flag carries code we must look inside.
_INLINE_CODE_FLAGS = {
    "python": ("-c",), "python3": ("-c",), "node": ("-e", "--eval"),
    "ruby": ("-e",), "perl": ("-e",), "sh": ("-c",), "bash": ("-c",),
    "zsh": ("-c",), "dash": ("-c",),
}

# Shell operators that end a command segment.
_SEGMENT_SEPARATORS = {";", "&&", "||", "|", "&", "\n"}

# Redirection operators whose operand is written to.
_REDIRECT_TOKENS = {">", ">>", ">|", "&>", "&>>", "1>", "2>", "1>>", "2>>"}

# Flags that name a directory the command operates in.
_DIR_FLAGS = {"-C", "--directory", "--cd", "-o", "--output", "--output-dir"}

# A token that could denote a filesystem path.
_PATHLIKE_RE = re.compile(r"^(?:[~./]|[A-Za-z0-9_.\-]+/)")

# Quoted string literals inside embedded code.
_STRING_LITERAL_RE = re.compile(r"""(?:'([^']{1,400})'|"([^"]{1,400})")""")

# Write-performing calls inside embedded code.
_EMBEDDED_WRITE_RE = re.compile(
    r"\b(?:makedirs|mkdir|open|write_file|write_text|write_bytes|"
    r"writeFile|writeFileSync|mkdirSync|copyfile|copytree|move|rename|"
    r"rmtree|remove|unlink|touch|save|to_csv|to_json|dump)\b"
)


def _tokenize(command: str) -> List[str]:
    """Split a shell command into words and operators, quotes respected."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return command.split()


def _strip_grouping(tokens: List[str]) -> List[str]:
    """Drop subshell/group punctuation so ``(cd .. && mkdir x)`` is analysed.

    ``shlex`` emits ``(`` and ``)`` as standalone punctuation tokens. Left in
    place they become the segment's command word and the real command is never
    recognised. A subshell changes the cwd only for its own duration, but the
    writes inside it are still writes, so analysing the contents inline is the
    safe approximation.
    """
    return [t for t in tokens if t not in {"(", ")", "{", "}"}]


def _split_segments(tokens: Sequence[str]) -> List[List[str]]:
    """Break a token stream into individual command segments."""
    segments: List[List[str]] = []
    current: List[str] = []
    for token in tokens:
        if token in _SEGMENT_SEPARATORS or set(token) <= {";", "&", "|"} and token:
            if current:
                segments.append(current)
                current = []
            continue
        current.append(token)
    if current:
        segments.append(current)
    return segments


def _basename(command_word: str) -> str:
    return os.path.basename(_expand(command_word)).lower()


def _embedded_paths(code: str) -> List[str]:
    """Path-like string literals in embedded code that also performs a write."""
    if not _EMBEDDED_WRITE_RE.search(code):
        return []
    found: List[str] = []
    for match in _STRING_LITERAL_RE.finditer(code):
        literal = match.group(1) or match.group(2) or ""
        if literal and _PATHLIKE_RE.match(literal):
            found.append(literal)
    return found


def _analyze_segment(
    tokens: List[str], cwd: str
) -> Tuple[List[Tuple[str, str]], str]:
    """Return ``(targets, new_cwd)`` for one command segment.

    ``targets`` are ``(label, raw_path)`` pairs this segment writes to.
    ``new_cwd`` reflects a ``cd`` performed by the segment.
    """
    targets: List[Tuple[str, str]] = []
    if not tokens:
        return targets, cwd

    name = _basename(tokens[0])

    # `cd DIR` moves the cwd for every later segment. The destination itself
    # is not a write, so it is not reported as a target.
    if name == "cd":
        operands = [t for t in tokens[1:] if not t.startswith("-")]
        if operands:
            return targets, _resolve_for_check(operands[0], cwd)
        return targets, os.path.expanduser("~")

    # Redirections write regardless of the command (`cat x > ../y`).
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token in _REDIRECT_TOKENS:
            if index + 1 < len(tokens):
                operand = tokens[index + 1]
                if operand != "&" and not operand.isdigit():
                    targets.append(("terminal(redirect)", operand))
            index += 2
            continue
        # Attached form: `>../file`, `2>/tmp/log`
        match = re.match(r"^(?:[0-9&]?>{1,2}\|?)(?P<path>[^>|&].*)$", token)
        if match:
            targets.append(("terminal(redirect)", match.group("path")))
        index += 1

    # Directory-selecting flags (`git -C ..`, `curl -o ../x`).
    for index, token in enumerate(tokens):
        if token in _DIR_FLAGS and index + 1 < len(tokens):
            targets.append((f"terminal({token})", tokens[index + 1]))
        elif token.startswith("--output=") or token.startswith("--directory="):
            targets.append(("terminal(flag)", token.split("=", 1)[1]))

    # Inline interpreter code: recurse into the script body.
    flags = _INLINE_CODE_FLAGS.get(name)
    if flags:
        for index, token in enumerate(tokens):
            if token in flags and index + 1 < len(tokens):
                body = tokens[index + 1]
                for literal in _embedded_paths(body):
                    targets.append((f"terminal({name} {token})", literal))
                # A nested `sh -c 'cd .. && mkdir x'` is itself a command line.
                if name in {"sh", "bash", "zsh", "dash"}:
                    nested, _ = _analyze_command(body, cwd)
                    targets.extend(nested)

    # Known write commands: their operands are write targets.
    mode = _WRITE_COMMANDS.get(name)
    if mode:
        # `sed -i` / `perl -i` only write with the in-place flag.
        if name in {"sed", "perl", "ruby", "awk"}:
            if not any(re.match(r"^-[^-]*i", t) for t in tokens[1:]):
                mode = None
        # git only writes to a path for a subset of subcommands.
        if name == "git" and mode:
            sub = next((t for t in tokens[1:] if not t.startswith("-")), "")
            if sub not in {"init", "clone", "worktree"}:
                mode = None

    if mode:
        operands = [
            t for t in tokens[1:]
            if not t.startswith("-")
            and t not in _REDIRECT_TOKENS
            and "://" not in t
        ]
        # Drop the subcommand word for multiplexers.
        if name == "git" and operands:
            operands = operands[1:]
        if mode == "last" and operands:
            operands = operands[-1:]
        for operand in operands:
            # Every operand of a write command is a write target, including a
            # bare name (`mkdir escape` writes to <cwd>/escape). Filtering on
            # path-like syntax here would miss exactly that case. Non-path
            # operands (`chmod 755 f`) resolve under the cwd and are therefore
            # inside an allowed root anyway, so they cost nothing.
            targets.append((f"terminal({name})", operand))

    return targets, cwd


def _analyze_command(command: str, cwd: str) -> Tuple[List[Tuple[str, str]], str]:
    """Analyse a full shell command line, threading cwd across segments."""
    targets: List[Tuple[str, str]] = []
    current = cwd
    for segment in _split_segments(_strip_grouping(_tokenize(command))):
        found, current = _analyze_segment(segment, current)
        # Resolve each target against the cwd in force for its segment.
        for label, raw in found:
            targets.append((label, _resolve_for_check(raw, current)))
    return targets, current


# ---------------------------------------------------------------------------
# Per-tool write-target extraction
# ---------------------------------------------------------------------------

def _skill_root() -> str:
    hermes_home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    return os.path.join(hermes_home, "skills")


def _targets(tool_name: str, args: Dict[str, Any], base: str) -> List[Tuple[str, str]]:
    """Return ``(label, resolved_path)`` pairs this call would write to."""
    out: List[Tuple[str, str]] = []

    def add(label: str, raw: str) -> None:
        out.append((label, _resolve_for_check(raw, base)))

    if tool_name == "write_file":
        path = args.get("path")
        if isinstance(path, str) and path:
            add("write_file(path)", path)

    elif tool_name == "patch":
        if (args.get("mode") or "replace") == "patch":
            body = args.get("patch")
            if isinstance(body, str):
                for match in _PATCH_FILE_RE.finditer(body):
                    add("patch(*** File)", match.group(1))
        else:
            path = args.get("path")
            if isinstance(path, str) and path:
                add("patch(path)", path)

    elif tool_name == "skill_manage":
        file_path = args.get("file_path")
        if isinstance(file_path, str) and file_path:
            if os.path.isabs(_expand(file_path)):
                add("skill_manage(file_path)", file_path)
            else:
                name = str(args.get("name") or "")
                add(
                    "skill_manage(file_path)",
                    os.path.join(_skill_root(), name, file_path),
                )

    elif tool_name == "execute_code":
        code = args.get("code")
        if isinstance(code, str) and code:
            for literal in _embedded_paths(code):
                add("execute_code(path literal)", literal)
            # execute_code may drive the terminal tool; analyse those strings.
            for match in re.finditer(
                r"terminal\(\s*(?:command\s*=\s*)?['\"](.+?)['\"]", code, re.S
            ):
                nested, _ = _analyze_command(match.group(1), base)
                out.extend(("execute_code(terminal)", p) for _, p in nested)

    elif tool_name == "terminal":
        workdir = args.get("workdir")
        if isinstance(workdir, str) and workdir:
            add("terminal(workdir)", workdir)
        command = args.get("command")
        if isinstance(command, str) and command:
            cwd = _resolve_for_check(workdir, base) if isinstance(workdir, str) and workdir else base
            nested, _ = _analyze_command(command, cwd)
            out.extend(nested)

    return out


# ---------------------------------------------------------------------------
# Hook
# ---------------------------------------------------------------------------

_WATCHED_TOOLS = {"write_file", "patch", "skill_manage", "terminal", "execute_code"}


def _on_pre_tool_call(
    tool_name: str = "",
    args: Any = None,
    **_: Any,
) -> Optional[Dict[str, str]]:
    if tool_name not in _WATCHED_TOOLS or not isinstance(args, dict):
        return None

    cfg = _load_config()
    roots: List[str] = cfg.get("_roots") or []
    if not roots:
        return None

    base = _current_cwd()

    try:
        targets = _targets(tool_name, args, base)
    except Exception as exc:  # never break the agent on a parse bug
        logger.error("ste-code-jail: analysis failed for %s (%s)", tool_name, exc)
        return None

    seen: set = set()
    violations: List[str] = []
    for label, resolved in targets:
        if resolved in seen:
            continue
        seen.add(resolved)
        reason = _violates(resolved, cfg)
        if reason:
            violations.append(f"  - {label}: {resolved} ({reason})")

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
            f"This usually means a project-root variable was computed with the "
            f"wrong number of parent hops, or a path was guessed rather than "
            f"checked. Recompute it against the project root and retry. "
            f"Reads are not restricted — only writes."
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
