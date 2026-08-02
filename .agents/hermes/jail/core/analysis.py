"""ste-code-jail-core.analysis — extract write targets from tool arguments.

Shared by every granular jail plugin and by the shell script packet, so the
parsing rules live in exactly one place.

The hard part is ``terminal``. A shell command is not statically analysable in
general, but the overwhelming majority of real writes are visible in the
argument text. This module performs a per-segment analysis that tracks ``cd``,
expands environment variables, follows redirections, understands write verbs
and their target positions, and recurses into ``-c``/``-e`` inline scripts.

Known ceiling: an opaque subprocess (``python3 build.py`` that itself calls
``os.makedirs("../x")``) is invisible here. That case is covered by the kernel
layer in ``scripts/jail-exec.sh``, not by argument inspection. The adversarial
suite in ``tests/`` documents which shapes each layer catches.
"""

from __future__ import annotations

import os
import re
import shlex
from typing import Dict, List, Optional, Sequence, Tuple

from .policy import normalize

__all__ = ["write_targets", "analyze_command", "expand", "resolve_against"]


def expand(raw: str) -> str:
    """Expand ``~`` and environment variables, including the ``${VAR}`` form."""
    return os.path.expandvars(os.path.expanduser(str(raw)))


def resolve_against(raw: str, base: str) -> str:
    """Resolve *raw* to an absolute realpath, anchoring relatives at *base*."""
    expanded = expand(raw)
    if not os.path.isabs(expanded):
        expanded = os.path.join(base, expanded)
    return os.path.realpath(os.path.abspath(expanded))


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
    return os.path.basename(expand(command_word)).lower()


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
            return targets, resolve_against(operands[0], cwd)
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
            targets.append((label, resolve_against(raw, current)))
    return targets, current




# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_command(command: str, cwd: str) -> List[Tuple[str, str]]:
    """Return ``(label, resolved_path)`` write targets for a shell command."""
    targets, _ = _analyze_command(command, cwd)
    return targets


def command_basenames(command: str) -> List[str]:
    """Return the executable basename of every segment in *command*.

    Used by the command-gating plugin to decide whether a disallowed binary
    (``curl``, ``pip``, ...) appears anywhere in a pipeline.
    """
    names: List[str] = []
    for segment in _split_segments(_strip_grouping(_tokenize(command))):
        if not segment:
            continue
        name = _basename(segment[0])
        if name:
            names.append(name)
        # `sh -c '<inner>'` hides its real command inside the script body.
        flags = _INLINE_CODE_FLAGS.get(name)
        if flags and name in {"sh", "bash", "zsh", "dash"}:
            for index, token in enumerate(segment):
                if token in flags and index + 1 < len(segment):
                    names.extend(command_basenames(segment[index + 1]))
    return names


def _skill_root() -> str:
    hermes_home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    return os.path.join(hermes_home, "skills")


def write_targets(
    tool_name: str, args: Dict[str, object], base: str
) -> List[Tuple[str, str]]:
    """Return ``(label, resolved_path)`` pairs this tool call would write to."""
    out: List[Tuple[str, str]] = []

    def add(label: str, raw: str) -> None:
        out.append((label, resolve_against(raw, base)))

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
            if os.path.isabs(expand(file_path)):
                add("skill_manage(file_path)", file_path)
            else:
                name = str(args.get("name") or "")
                add("skill_manage(file_path)",
                    os.path.join(_skill_root(), name, file_path))

    elif tool_name == "execute_code":
        code = args.get("code")
        if isinstance(code, str) and code:
            for literal in _embedded_paths(code):
                add("execute_code(path literal)", literal)
            for match in re.finditer(
                r"terminal\(\s*(?:command\s*=\s*)?['\"](.+?)['\"]", code, re.S
            ):
                out.extend(("execute_code(terminal)", p)
                           for _, p in analyze_command(match.group(1), base))

    elif tool_name == "terminal":
        workdir = args.get("workdir")
        if isinstance(workdir, str) and workdir:
            add("terminal(workdir)", workdir)
        command = args.get("command")
        if isinstance(command, str) and command:
            cwd = (resolve_against(workdir, base)
                   if isinstance(workdir, str) and workdir else base)
            out.extend(analyze_command(command, cwd))

    return out
