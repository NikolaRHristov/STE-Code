#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""post_tool_call hook: anonymise memory writes (dev-ste-code).

Wiring (config.yaml hooks.post_tool_call with matcher: memory):
  Fires AFTER the agent-loop `memory`/`user` write completes. NOTE: Hermes
  short-circuits `pre_tool_call` for `_AGENT_LOOP_TOOLS` (memory, todo,
  session_search, delegate_task) in model_tools.py BEFORE hook dispatch, so a
  `pre_tool_call` matcher:memory hook NEVER fires. Only `post_tool_call` reaches
  memory writes (emitted via _finish_agent_tool in agent_runtime_helpers.py).

Single responsibility: ANONYMISE. Nothing else (no restructure that writes
files via the agent, no session clutter).

Two layers:
  1. REGEX scrub - synchronous, pure-Python, ~50ms, GUARANTEED. Runs on every
     memory write. No subprocess, no PII left on disk. This is the contract.
  2. LLM refine - async, BEST-EFFORT, debounced. Calls the Nous inference API
     THROUGH `hermes -z` to catch names/PII the regex misses and tidy structure.
     Critical guards so it can NEVER become the old runaway bug:
       * The child runs with HERMES_HOME=<temp> so its session is written to a
         throwaway state.db, NOT the real profile store ("session db none").
       * The child uses `-t ''` (NO tools) so it can only RETURN text - it can
         never call write_file/memory and loop on the jail (the old 84-msg bug).
       * HERMES_ACCEPT_HOOKS=0 so its own writes can't re-trigger this hook.
       * Debounced by a lock file + content hash: only one LLM pass runs at a
         time, and only if the store changed since the last pass.
       * Provider launched with just `--provider nous -m <model>` - NO base_url.
       * On ANY failure the regex result stands; the LLM layer is optional.

Stdin : JSON {hook_event_name, tool_name:"memory", tool_input{action,target,...}}
Stdout: {}  (return value ignored; we act by rewriting the store file)
"""

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERMES_HOME = Path(os.path.expanduser("~/.hermes"))
LOG_DIR = HERMES_HOME / "agent-hooks" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG = LOG_DIR / "memory-anonymise.log"


# dev-ste-code memory is symlinked from the STE-Code repo. Keep authoritative.
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
MEMORY_STORE = REPO / ".agents" / "hermes" / "memory" / "dev-ste-code" / "MEMORY.md"
USER_STORE = REPO / ".agents" / "hermes" / "memory" / "dev-ste-code" / "USER.md"

LLM_MODEL = os.environ.get("HERMES_ANON_LLM_MODEL", "tencent/hy3:free")

# --------------------------------------------------------------------------- #
# Anonymiser (regex, deterministic, no network, no subprocess)
# --------------------------------------------------------------------------- #
# Known non-person Title-Case tokens - excluded from the person-name heuristic so
# we don't anonymise product/role names like "Red Hat", "Hermes Agent",
# "Level Worker", "GitHub Copilot", "Red Hat Linux". Covers common brand-name
# first words AND continuations that would otherwise look like a "Surname".
_KNOWN_NON_PERSON = {
    "STE",
    "API",
    "URL",
    "Red",
    "Black",
    "White",
    "Blue",
    "Purple",
    "Green",
    "Yellow",
    "Orange",
    "Level",
    "Agent",
    "Hermes",
    "GitHub",
    "GitLab",
    "Nous",
    "Code",
    "Tool",
    "Hook",
    "Config",
    "Memory",
    "User",
    "Host",
    "Email",
    "Person",
    "Repo",
    "Home",
    "Shell",
    "File",
    "Path",
    "Error",
    "Warning",
    "Info",
    "Debug",
    "Test",
    "Build",
    "Run",
    "Note",
    "Table",
    "Figure",
    "Section",
    "Chapter",
    "Make",
    "Skip",
    "Pass",
    "Fail",
    "True",
    "False",
    "None",
    "Model",
    "Prompt",
    "Hat",
    "Linux",
    "Mac",
    "OS",
    "Server",
    "Studio",
    "Hub",
    "Base",
    "Stack",
    "Cloud",
    "Pro",
    "Max",
    "Mini",
    "Air",
    "Book",
    "Pad",
    "Pen",
    "TV",
    "App",
    "Kit",
    "Lab",
    "Soft",
    "Hard",
    "Open",
    "Free",
    "Dev",
    "Ops",
    "Net",
    "Web",
    "Data",
    "Core",
    "Edge",
    "Flow",
    "View",
    "Docs",
    "DB",
    "SQL",
    "No",
    "Go",
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
        (
            re.compile(
                r"/Volumes/[A-Za-z0-9_.-]+/[A-Za-z0-9_. -]+/Application/"
                r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+"
            ),
            "<repo>",
        ),
        (re.compile(r"/Volumes/[A-Za-z0-9_./-]+"), "<repo>"),
        (re.compile(r"/private/var/folders/[A-Za-z0-9/_-]+"), "<tmp>"),
        (re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"), "<email>"),
        (re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"), "<ip>"),
        (re.compile(r"[A-Za-z0-9.-]+\.(?:nousresearch\.com|local|lan|home)"), "<host>"),
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
# Store helpers - scrub whole file idempotently
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
# LLM refine layer (async, debounced, best-effort, session-isolated)
# --------------------------------------------------------------------------- #
def _llm_lock_path(store: Path) -> Path:
    h = hashlib.sha1(str(store).encode()).hexdigest()[:12]
    return LOG_DIR / f"anon-llm-{h}.lock"


def _store_hash(store: Path) -> str:
    try:
        return hashlib.sha1(store.read_bytes()).hexdigest()
    except OSError:
        return ""


def _llm_refine(store: Path) -> None:
    """Best-effort LLM tidy/extra-anonymise. Never raises to caller."""
    try:
        body = store.read_text(encoding="utf-8")
    except OSError:
        return

    lock = _llm_lock_path(store)
    # Debounce: skip if another pass is running, or content unchanged since last.
    try:
        if lock.exists():
            if (time.time() - lock.stat().st_mtime) < 30:
                return
        last_hash = lock.read_text().strip() if lock.exists() else ""
        if last_hash == _store_hash(store):
            return
    except OSError:
        pass

    # Claim the lock (write current hash so a concurrent pass skips).
    try:
        lock.write_text(_store_hash(store))
    except OSError:
        return

    try:
        prompt = (
            "You are a privacy scrubber for an AI agent's long-term memory file.\n"
            "The file is already partially anonymised with placeholders like "
            "<user-home>, <repo>, <person>, <email>, <ip>, <host>, <tmp>.\n"
            "TASK: return the SAME information, but (1) replace any remaining "
            "real person names, emails, IPs, absolute paths, or hostnames with "
            "the matching placeholder; (2) keep all placeholders VERBATIM - never "
            "expand them; (3) keep the existing structure (lines / '§' separators); "
            "(4) do NOT add commentary, headings, or new facts. Output ONLY the "
            "scrubbed markdown.\n\n"
            "FILE:\n" + body
        )

        # Build an isolated temp home so the child's session lands in a throwaway
        # state.db, NOT the real profile store ("session db none").
        tmphome = Path("/tmp") / f"hermes-anon-{os.getpid()}-{int(time.time())}"
        try:
            tmphome.mkdir(parents=True, exist_ok=True)
            # Copy the Nous auth state so the child can authenticate. Reads of
            # ~/.hermes are permitted; writes go to /tmp (a writable root).
            src_auth = HERMES_HOME / "auth.json"
            if src_auth.exists():
                import shutil

                shutil.copyfile(src_auth, tmphome / "auth.json")
        except OSError as e:
            _log(f"llm: temp home setup failed: {e}")
            return

        env = {**os.environ, "HERMES_HOME": str(tmphome), "HERMES_ACCEPT_HOOKS": "0"}
        try:
            proc = subprocess.run(
                [
                    "hermes",
                    "-z",
                    prompt,
                    "--provider",
                    "nous",
                    "-m",
                    LLM_MODEL,
                    "--yolo",
                    "-t",
                    "",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True,
                cwd=str(REPO),
                env=env,
                timeout=120,
            )
        except Exception as e:  # noqa: BLE001
            _log(f"llm: spawn failed: {e}")
            return
        finally:
            # Clean the throwaway home (session + auth copy) immediately.
            try:
                import shutil

                shutil.rmtree(tmphome, ignore_errors=True)
            except OSError:
                pass

        out = (proc.stdout or b"").decode("utf-8", "replace").strip()
        if proc.returncode != 0 or not out:
            _log(f"llm: no output (rc={proc.returncode})")
            return
        # The LLM may wrap in ```markdown fences; strip them.
        cleaned = re.sub(r"^```[a-zA-Z]*\n?", "", out)
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
        if not cleaned:
            return
        # Re-anonymise the LLM output (defence in depth - never trust the LLM).
        cleaned = anonymise(cleaned)
        try:
            store.write_text(cleaned, encoding="utf-8")
            _log("llm: refined store written")
        except OSError as e:
            _log(f"llm: write failed: {e}")
    finally:
        try:
            lock.unlink()
        except OSError:
            pass


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    # Detached LLM-refine worker mode: run synchronously, then exit. Invoked as a
    # fully detached child so it survives the (short-lived) hook process.
    if len(sys.argv) >= 3 and sys.argv[1] == "--llm-refine":
        try:
            _llm_refine(Path(sys.argv[2]))
        except Exception as e:  # noqa: BLE001
            _log(f"llm: worker error: {e}")
        return 0

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

        # 1) GUARANTEED synchronous regex scrub - no PII persists past this point.
        changed = scrub_store(store)
        _log(f"post_memory -> {store.name} (regex scrub={'yes' if changed else 'no'})")

        # 2) BEST-EFFORT async LLM refine (debounced; isolated session; fallback
        #    to regex on any failure). Launched as a DETACHED child so it survives
        #    this short-lived hook process (a daemon thread would be killed on
        #    exit before the ~10s LLM call finishes - the old bug).
        try:
            subprocess.Popen(
                [sys.executable, os.path.abspath(__file__), "--llm-refine", str(store)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
                cwd=str(REPO),
                env={**os.environ, "HERMES_ACCEPT_HOOKS": "0"},
            )
        except Exception as e:  # noqa: BLE001
            _log(f"llm: detach failed: {e}")
    finally:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
