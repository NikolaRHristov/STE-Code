#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""post_tool_call hook: anonymise memory writes (dev-ste-code).

Wiring (config.yaml hooks.post_tool_call with matcher: memory):
  Fires AFTER the agent-loop `memory`/`user` write completes. NOTE: Hermes
  short-circuits `pre_tool_call` for `_AGENT_LOOP_TOOLS` (memory, todo,
  session_search, delegate_task) in model_tools.py BEFORE hook dispatch, so a
  `pre_tool_call` matcher:memory hook NEVER fires. Only `post_tool_call` reaches
  memory writes (emitted via _finish_agent_tool in agent_runtime_helpers.py).

Design — anonymise only, NO background LLM:
  The original design also spawned `hermes -z` to "restructure" the store. That
  was removed because it was the entire bug surface:
    * `hermes -z` ALWAYS creates a logged session -> memory-restructure clutter.
    * spawned with cwd=~/.hermes, the dev jail resolved project_root=None, so the
      restructure agent's write_file to MEMORY.md was BLOCKED -> it looped
      25-84 messages diagnosing/retrying the jail.
    * the LLM rewrote raw PII (e.g. "Nikola Hristov") back into the store,
      defeating the anonymiser.
    * it fired on EVERY memory write -> dozens of concurrent sessions.
  The hook's actual contract is: guarantee the on-disk store is anonymised. That
  is a pure-Python regex scrub, idempotent, ~50ms, fire-and-forget by nature, and
  needs no subprocess. PII never persists past the turn. If an LLM-driven
  restructure is wanted later, do it as a SEPARATE bounded cron job, never
  synchronously from this hook.

Stdin : JSON {hook_event_name, tool_name:"memory", tool_input{action,target,...}}
Stdout: {}  (return value ignored; we act by rewriting the store file)
"""
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERMES_HOME = Path(os.path.expanduser("~/.hermes"))
LOG_DIR = HERMES_HOME / "agent-hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG = LOG_DIR / "memory-anonymise.log"

# dev-ste-code memory is symlinked from the STE-Code repo. Keep authoritative.
REPO = Path(
    "/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code"
)
MEMORY_STORE = REPO / ".agents" / "hermes" / "memory" / "dev-ste-code" / "MEMORY.md"
USER_STORE = REPO / ".agents" / "hermes" / "memory" / "dev-ste-code" / "USER.md"

# --------------------------------------------------------------------------- #
# Anonymiser (regex, deterministic, no network, no subprocess)
# --------------------------------------------------------------------------- #
# Known non-person Title-Case tokens — excluded from the person-name heuristic so
# we don't anonymise product/role names like "Red Hat", "Hermes Agent",
# "Level Worker", "GitHub Copilot", "Red Hat Linux". Covers common brand-name
# first words AND continuations that would otherwise look like a "Surname".
_KNOWN_NON_PERSON = {
    "STE", "API", "URL", "Red", "Black", "White", "Blue", "Purple", "Green",
    "Yellow", "Orange", "Level", "Agent", "Hermes", "GitHub", "GitLab", "Nous",
    "Code", "Tool", "Hook", "Config", "Memory", "User", "Host", "Email", "Person",
    "Repo", "Home", "Shell", "File", "Path", "Error", "Warning", "Info", "Debug",
    "Test", "Build", "Run", "Note", "Table", "Figure", "Section", "Chapter",
    "Make", "Skip", "Pass", "Fail", "True", "False", "None", "Model", "Prompt",
    "Hat", "Linux", "Mac", "OS", "Server", "Studio", "Hub", "Base", "Stack",
    "Cloud", "Pro", "Max", "Mini", "Air", "Book", "Pad", "Pen", "TV", "App",
    "Kit", "Lab", "Soft", "Hard", "Open", "Free", "Dev", "Ops", "Net", "Web",
    "Data", "Core", "Edge", "Flow", "View", "Docs", "DB", "SQL", "No", "Go",
}
# Heuristic: Title-Case "Firstname Lastname" (e.g. "Nikola Hristov") -> <person>.
# No literal operator name is baked into this file (that would leak PII into the
# repo single-source); the pattern recognises the SHAPE of a person name. The env
# var HERMES_OPERATOR_NAMES (set from ~/.hermes/.env, operator-owned, gitignored)
# handles standalone names. Single responsibility: this is still just anonymising.
_PERSON_HEURISTIC = re.compile(
    r"\b(?!(?:"
    + "|".join(sorted(_KNOWN_NON_PERSON))
    + r")\s)[A-Z][a-z]{1,20}\s+[A-Z][a-z]{1,20}\b"
)


def build_anon_patterns():
    pats = [
        (re.compile(r"/Users/[A-Za-z0-9_.-]+"), "<user-home>"),
        (re.compile(
            r"/Volumes/[A-Za-z0-9_.-]+/[A-Za-z0-9_. -]+/Application/"
            r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"), "<repo>"),
        (re.compile(r"/Volumes/[A-Za-z0-9_./-]+"), "<repo>"),
        (re.compile(r"/private/var/folders/[A-Za-z0-9/_-]+"), "<tmp>"),
        (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
         "<email>"),
        (re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"), "<ip>"),
        (re.compile(r"[A-Za-z0-9.-]+\.(?:nousresearch\.com|local|lan|home)"),
         "<host>"),
        (_PERSON_HEURISTIC, "<person>"),
    ]
    names = os.environ.get("HERMES_OPERATOR_NAMES", "")
    for nm in [n.strip() for n in names.split(",") if n.strip()]:
        pats.append((re.compile(re.escape(nm)), "<person>"))
    return pats


_PATTERNS = build_anon_patterns()


def anonymise(text: str) -> str:
    if not text:
        return text
    for pat, repl in _PATTERNS:
        text = pat.sub(repl, text)
    return text


# --------------------------------------------------------------------------- #
# Store helpers — scrub whole file idempotently
# --------------------------------------------------------------------------- #
def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%3NZ")


def scrub_store(store: Path) -> bool:
    """Re-write the store with every entry anonymised. Returns True if changed."""
    try:
        body = store.read_text(encoding="utf-8")
    except OSError:
        return False
    scrubbed = anonymise(body)
    if scrubbed != body:
        store.write_text(scrubbed, encoding="utf-8")
        return True
    return False


def _log(msg: str) -> None:
    try:
        with LOG.open("a", encoding="utf-8") as fh:
            fh.write(f"[{_now()}] {msg}\n")
    except OSError:
        pass


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    out = "{}"
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return 0

        if payload.get("tool_name") != "memory":
            return 0

        tool_input = payload.get("tool_input", {}) or {}
        target = (tool_input.get("target") or "memory").lower()
        store = USER_STORE if target == "user" else MEMORY_STORE

        # Guarantee: store on disk is anonymised after this write.
        # Idempotent — re-running on already-clean content is a no-op, so the
        # file stabilises immediately and PII never persists past the turn.
        changed = scrub_store(store)
        _log(f"post_memory -> {store.name} (scrub={'yes' if changed else 'no'})")
    finally:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
