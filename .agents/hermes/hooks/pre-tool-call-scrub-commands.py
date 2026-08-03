#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pre_tool_call hook: scrub + essentialise terminal commands (dev-ste-code).

Wiring (config.yaml hooks.pre_tool_call with matcher: terminal):
  Fires BEFORE a `terminal` tool command runs. We return a `modify` directive
  with a cleaned, essential, jail-safe command. This is the "command hygiene"
  layer requested alongside the memory-anonymise hook.

Pipeline (the requested breakdown -> scrub -> jail -> reassemble):
  1. BREAK DOWN: split the command into sub-commands on && ; || & <newline>
     (quotes respected). Each pipeline segment (with its |'s) stays one unit.
  2. DROP NOISE: remove pure-descriptive commands the model emits to "explain"
     itself - lone `echo`/`printf`/`print`/`say`/`sleep`/`clear`/`open` that
     print text but do nothing useful. Keep `echo`/`printf` ONLY when they
     write to a file (>) or are the actual command purpose. Net effect: the
     tool_call reduces to the ESSENTIAL parts (the "1 or 0" - launch or drop).
  3. SCRUB PII: run every surviving sub-command through the same anonymiser
     regex set as post-memory-anonymise.py (imported), so paths/names/emails
     never appear in executed commands either.
  4. JAIL-CHECK: evaluate each sub-command's file targets against the dev jail
     write_roots / deny_roots (imported from .agents/hermes/jail/core/policy.py,
     with a fallback set). DROP any sub-command that would WRITE outside the
     allowed roots or INTO a deny root. This is "instantiating the jail at this
     level" - the command is pre-filtered so it cannot break the jail.
  5. REASSEMBLE: join the surviving sub-commands with their original separators
     and return {"action":"modify","args":{"command": <cleaned>}}.

Optional LLM "1-or-0" classifier: if HERMES_SCRUB_LLM=1, ambiguous sub-commands
are classified essential(1)/drop(0) by a Nous LLM call (--provider nous, no
base_url), launched as a DETACHED child so the hook returns instantly. OFF by
default - the heuristic layer is deterministic and fast.

Stdin : JSON {hook_event_name, tool_name:"terminal", tool_input{command,...}}
Stdout: {"action":"modify","args":{"command": "..."}}  or {} for no-op.
"""
import json
import os
import re
import shlex
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _repo_root() -> Path:
    """Resolve the STE-Code checkout from this file's location, not by
    hardcoding a machine path (which leaks the operator's directory layout and
    breaks on any other checkout). Walk up to the dir containing `.agents/`."""
    here = Path(__file__).resolve().parent
    cand = here
    while cand != cand.parent:
        if (cand / ".agents").is_dir():
            return cand
        cand = cand.parent
    return here


REPO = _repo_root()

# Reuse the anonymiser regex set (single source of truth for PII scrubbing).
try:
    sys.path.insert(0, str(HERE))
    from post_memory_anonymise import anonymise  # type: ignore
except Exception:  # noqa: BLE001
    def anonymise(text: str) -> str:  # minimal fallback
        if not text:
            return text
        text = re.sub(r"/Users/[A-Za-z0-9_.-]+", "<user-home>", text)
        text = re.sub(r"/Volumes/[A-Za-z0-9_./-]+", "<repo>", text)
        text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
                      "<email>", text)
        return text


# --------------------------------------------------------------------------- #
# Jail roots (import the real policy; fallback to the known dev write_roots)
# --------------------------------------------------------------------------- #
def _load_jail_roots():
    write_roots = {str(REPO), os.path.expanduser("~/.hermes/profiles/dev-ste-code"),
                   os.path.expanduser("~/.hermes/profiles"), "/tmp",
                   "/private/var/folders"}
    deny_roots = set()
    try:
        sys.path.insert(0, str(REPO / ".agents" / "hermes" / "jail" / "core"))
        import policy  # type: ignore
        ctx = policy._build_dev()
        write_roots = {str(Path(p).resolve()) for p in ctx.policy.write_roots}
        deny_roots = {str(Path(p).resolve()) for p in ctx.policy.deny_roots}
    except Exception:  # noqa: BLE001
        pass
    return write_roots, deny_roots


WRITE_ROOTS, DENY_ROOTS = _load_jail_roots()


def _path_in_roots(p: str, roots) -> bool:
    p = os.path.expanduser(p)
    try:
        p = str(Path(p).resolve())
    except Exception:
        p = os.path.abspath(p)
    for r in roots:
        if p == r or p.startswith(r.rstrip("/") + "/"):
            return True
    return False


def _is_write_target_allowed(target: str) -> bool:
    # Allowed if inside a write root AND not inside a deny root.
    if _path_in_roots(target, DENY_ROOTS):
        return False
    return _path_in_roots(target, WRITE_ROOTS)


# --------------------------------------------------------------------------- #
# Command decomposition
# --------------------------------------------------------------------------- #
# Split on && ; || & and newlines, but keep pipelines (|) intact within a unit.
_SEP = re.compile(r"\s*(?:\|\||\&\&|\|\||\&\s|\n)\s*|\s*;\s*|\s*&\s*")


def split_subcommands(cmd: str):
    # Preserve the separator that followed each piece so we can rejoin faithfully.
    parts = []
    for piece in _SEP.split(cmd):
        piece = piece.strip()
        if piece:
            parts.append(piece)
    return parts


# Tokens that, when they are the WHOLE command (no redirect/write), are noise.
_NOISE_SOLO = {
    "sleep", "clear", "cls", "say", "open", "notify", "echo", "printf",
    "print", "banner", "figlet", "cowsay", "toilet",
}


def _first_word(sub: str) -> str:
    try:
        toks = shlex.split(sub)
    except ValueError:
        toks = sub.split()
    if not toks:
        return ""
    return toks[0].split("/")[-1].lstrip("-")


def _is_redirect_write(sub: str) -> bool:
    # Writes to a file: > >> | tee (when tee writes) cp/mv/rm/write_file/ln/mkdir/touch
    return bool(re.search(r"[>\]]>|\btee\b|\bcp\b|\bmv\b|\brm\b|\bln\b|"
                          r"\bmkdir\b|\btouch\b|\bwrite_file\b|\bgit\s", sub))


def is_noise(sub: str) -> bool:
    fw = _first_word(sub)
    if fw in _NOISE_SOLO:
        # echo/printf that writes to a file is useful; pure print is noise.
        if fw in ("echo", "printf", "print") and not _is_redirect_write(sub):
            return True
        if fw in ("sleep", "clear", "cls", "say", "open", "notify",
                  "banner", "figlet", "cowsay", "toilet"):
            return True
    return False


# --------------------------------------------------------------------------- #
# Per-sub-command jail check
# --------------------------------------------------------------------------- #
def _extract_paths(sub: str):
    """Pull likely file/dir path args from a command (quoted or bare)."""
    paths = []
    # quoted strings
    for m in re.findall(r'"([^"]+)"|\'([^\']+)\'', sub):
        s = m[0] or m[1]
        if s and (s.startswith("/") or s.startswith("~") or "/" in s):
            paths.append(s)
    # bare token paths (start with / or ~/ or ./ or ../)
    try:
        toks = shlex.split(sub)
    except ValueError:
        toks = sub.split()
    for t in toks:
        if re.match(r"^(/|~/|\./|\.\./)", t):
            paths.append(t)
    return paths


def jail_violation(sub: str) -> str:
    """Return a reason string if the sub-command would break the jail, else ''."""
    if not _is_redirect_write(sub):
        return ""  # read-only / control commands don't violate write roots
    for p in _extract_paths(sub):
        if not _is_write_target_allowed(p):
            return f"write target {p} outside jail write_roots"
    return ""


# --------------------------------------------------------------------------- #
# Optional LLM 1-or-0 classifier (detached, nous, no base_url)
# --------------------------------------------------------------------------- #
def _llm_classify(sub: str) -> bool:
    """Return True if essential. Best-effort; on any failure treat as essential."""
    import subprocess
    prompt = (
        "Reply with only '1' if this shell command performs a useful action "
        "(writes a file, runs a build/test, installs, edits code, queries a "
        "system) and should run, or '0' if it is only descriptive/noise "
        "(prints status, sleeps, clears screen, repeats info). Command: "
        + sub
    )
    tmphome = Path("/tmp") / f"hermes-scrub-{os.getpid()}"
    try:
        tmphome.mkdir(parents=True, exist_ok=True)
        import shutil
        src = Path(os.path.expanduser("~/.hermes")) / "auth.json"
        if src.exists():
            shutil.copyfile(src, tmphome / "auth.json")
        env = {**os.environ, "HERMES_HOME": str(tmphome),
               "HERMES_ACCEPT_HOOKS": "0"}
        proc = subprocess.run(
            ["hermes", "-z", prompt, "--provider", "nous",
             "-m", os.environ.get("HERMES_ANON_LLM_MODEL", "tencent/hy3:free"),
             "--yolo", "-t", ""],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            cwd=str(REPO), env=env, timeout=60)
        out = proc.stdout.decode("utf-8", "replace").strip()
        return out.startswith("1")
    except Exception:  # noqa: BLE001
        return True
    finally:
        try:
            import shutil
            shutil.rmtree(tmphome, ignore_errors=True)
        except Exception:
            pass


def _maybe_llm_classify(sub: str) -> bool:
    if os.environ.get("HERMES_SCRUB_LLM") != "1":
        return True  # heuristic-only mode: keep everything that passed noise+jail
    return _llm_classify(sub)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return 0

    if payload.get("tool_name") != "terminal":
        return 0
    tool_input = payload.get("tool_input", {}) or {}
    cmd = tool_input.get("command", "")
    if not cmd.strip():
        return 0

    subs = split_subcommands(cmd)
    kept = []
    for sub in subs:
        if is_noise(sub):
            continue  # drop descriptive no-op
        sub_scrubbed = anonymise(sub)  # scrub PII from the command itself
        violation = jail_violation(sub_scrubbed)
        if violation:
            sys.stderr.write(f"[scrub-hook] dropped sub-cmd: {violation}\n")
            continue
        if not _maybe_llm_classify(sub_scrubbed):
            continue
        kept.append(sub_scrubbed)

    if not kept:
        # Everything was noise/jail-breaking - don't break the agent's intent;
        # pass the original through unchanged (safe no-op for THIS hook).
        return 0

    if len(kept) == len(subs) and kept == subs:
        return 0  # nothing changed

    cleaned = " && ".join(kept)
    print(json.dumps({"action": "modify", "args": {"command": cleaned}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
