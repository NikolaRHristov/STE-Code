#!/usr/bin/env python3
"""Launch Agent #7 workers at multiple STE-Code levels using the Hermes oneshot wrapper.

This script is safe: no tools are exposed and no session pollution occurs.
"""
from __future__ import annotations

import argparse
import atexit
import os
import signal
import subprocess
import sys
import tempfile
import time

# ---------------------------------------------------------------------------
# Defaults (overridable via CLI)
# ---------------------------------------------------------------------------
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DOCS = ["README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "RELEASE-NOTES.md"]
DEFAULT_OUT = os.path.join(PROJECT, ".agents", "rewrites")
DEFAULT_MODEL = "deepseek-v4-pro"

DEFAULT_LEVELS = {
    1: "14 core principles only",
    2: "+ dictionary excerpt",
    3: "+ grammar rules",
    4: "+ full dictionary",
}

# Paths from hermes-background-workers skill
# Local tools (distributed with the project)
TOOLS_DIR = os.path.join(PROJECT, ".agents", "tools")
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = os.path.join(TOOLS_DIR, "hermes-oneshot-wrapper.py")

# ---------------------------------------------------------------------------
# Token budget constants
# ---------------------------------------------------------------------------
# Approximate token-to-character ratio for English text (GPT-family tokenizers).
# Safe lower bound: 1 token ≈ 4 characters.
CHARS_PER_TOKEN = 4

# DeepSeek v4 context window (conservative: 128K tokens).
MODEL_MAX_TOKENS = 128_000

# Reserve tokens for model response (output).
OUTPUT_RESERVE = 16_000

# ---------------------------------------------------------------------------
# Temp-file tracking and cleanup
# ---------------------------------------------------------------------------
_TEMP_FILES: list[str] = []


def _register_temp(path: str) -> None:
    """Register a temp file for cleanup at process exit."""
    _TEMP_FILES.append(path)


def _cleanup_temp_files() -> None:
    """Remove all registered temp files.  Best-effort; errors are ignored."""
    for path in _TEMP_FILES:
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass


atexit.register(_cleanup_temp_files)


# ---------------------------------------------------------------------------
# Token estimation
# ---------------------------------------------------------------------------
def estimate_tokens(text: str) -> int:
    """Return a conservative token count for the given text."""
    return max(1, len(text) // CHARS_PER_TOKEN)


def warn_if_over_budget(prompt: str, model_max: int = MODEL_MAX_TOKENS) -> bool:
    """Print a warning when the prompt exceeds the model context budget.

    Returns True when the prompt fits within the budget, False otherwise.
    """
    prompt_tokens = estimate_tokens(prompt)
    available = model_max - OUTPUT_RESERVE

    if prompt_tokens > available:
        print(
            f"WARNING: Estimated prompt size ({prompt_tokens:,} tokens) "
            f"exceeds the available budget ({available:,} tokens). "
            f"Model responses may be truncated."
        )
        return False
    else:
        print(
            f"Token estimate: {prompt_tokens:,} prompt tokens "
            f"(budget: {available:,} available of {model_max:,} total)"
        )
        return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Launch Agent #7 STE-Code level workers via the Hermes oneshot wrapper."
    )
    parser.add_argument(
        "--levels",
        type=str,
        default="1,2,3,4",
        help="Comma-separated level numbers to run (default: 1,2,3,4)",
    )
    parser.add_argument(
        "--docs",
        type=str,
        nargs="*",
        default=None,
        help=(
            "Project documents to rewrite "
            "(default: README.md CONTRIBUTING.md CODE_OF_CONDUCT.md RELEASE-NOTES.md)"
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Model name to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=DEFAULT_OUT,
        help=f"Output directory for rewrites (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="Timeout per worker in seconds (default: 900)",
    )
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    args = parse_args()

    # Resolve levels from CLI.
    requested = [int(x.strip()) for x in args.levels.split(",")]
    LEVELS = {lv: DEFAULT_LEVELS[lv] for lv in requested if lv in DEFAULT_LEVELS}
    if not LEVELS:
        print("ERROR: No valid levels requested.")
        sys.exit(1)

    DOCS = args.docs if args.docs is not None else DEFAULT_DOCS
    MODEL = args.model
    OUT = args.output_dir
    TIMEOUT = args.timeout

    # Validate the wrapper script exists.
    if not os.path.exists(WRAPPER):
        print(f"ERROR: Wrapper not found at {WRAPPER}")
        sys.exit(1)

    # Load the STE-Code rules file.
    rules_path = os.path.join(
        PROJECT, "ste-code/artifacts/ste-code-distilled-system-prompt.txt"
    )
    try:
        with open(rules_path) as f:
            rules = f.read()
    except FileNotFoundError:
        print(f"ERROR: Rules file not found at {rules_path}")
        sys.exit(1)
    except PermissionError:
        print(f"ERROR: Permission denied reading {rules_path}")
        sys.exit(1)
    except OSError as exc:
        print(f"ERROR: Cannot read rules file: {exc}")
        sys.exit(1)

    # Load document contents.
    docs_text = ""
    missing_docs: list[str] = []
    for d in DOCS:
        dpath = os.path.join(PROJECT, d)
        try:
            if os.path.exists(dpath):
                with open(dpath) as f:
                    docs_text += f"\n\n### DOCUMENT: {d}\n\n{f.read()}\n"
            else:
                missing_docs.append(d)
        except PermissionError:
            print(f"WARNING: Permission denied reading {dpath} -- skipping")
        except OSError as exc:
            print(f"WARNING: Cannot read {dpath}: {exc} -- skipping")

    if missing_docs:
        print(f"WARNING: Documents not found: {', '.join(missing_docs)}")

    if not docs_text.strip():
        print("ERROR: No document content loaded. Nothing to process.")
        sys.exit(1)

    # Launch workers.
    workers: list[tuple[int, subprocess.Popen, str]] = []
    for lv, desc in LEVELS.items():
        out_dir = os.path.join(OUT, f"level-{lv}")
        try:
            os.makedirs(out_dir, exist_ok=True)
        except OSError as exc:
            print(f"ERROR: Cannot create output directory {out_dir}: {exc}")
            sys.exit(1)

        prompt = f"""{rules}

Level {lv} ({desc}). You are Agent #7.

TASK: Rewrite all {len(DOCS)} documents below using only Level {lv} rules.
Output inline only -- do NOT create any files or use any tools.
For each document output: rewritten text, change log, compliance table.

{docs_text}"""

        # Token budget check (run once for the lowest level to avoid noise).
        if lv == min(LEVELS.keys()):
            warn_if_over_budget(prompt)

        # Write prompt to temp file (wrapper reads from file and deletes it).
        try:
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, dir="/tmp"
            )
            tmp.write(prompt)
            tmp.close()
        except OSError as exc:
            print(f"ERROR: Cannot write temp file for level {lv}: {exc}")
            sys.exit(1)
        _register_temp(tmp.name)

        log_file = os.path.join(out_dir, "output.txt")

        print(f"Level {lv}: launching -> {out_dir}/output.txt")

        # Fire-and-forget: Popen with start_new_session.
        try:
            proc = subprocess.Popen(
                [VENV_PYTHON, WRAPPER, tmp.name, "--model", MODEL],
                stdout=open(log_file, "w"),
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env={**os.environ, "HERMES_ACCEPT_HOOKS": "1"},
            )
        except FileNotFoundError:
            print(
                "ERROR: Cannot find Python or wrapper. "
                "Check VENV_PYTHON and WRAPPER paths."
            )
            sys.exit(1)
        except PermissionError:
            print(f"ERROR: Permission denied launching worker for level {lv}.")
            sys.exit(1)
        except OSError as exc:
            print(f"ERROR: Cannot launch worker for level {lv}: {exc}")
            sys.exit(1)

        workers.append((lv, proc, out_dir))
        time.sleep(0.5)

    print(
        f"\nAll {len(workers)} workers launched. "
        f"PIDs: {[w[1].pid for w in workers]}"
    )
    print("Monitor: ps aux | grep oneshot")
    print(
        f"Results: {OUT}/level-{{{','.join(str(lv) for lv in LEVELS)}}}/output.txt"
    )
    print(f"Timeout per worker: {TIMEOUT}s")

    # Wait for all workers with timeout handling.
    failed: list[int] = []
    timed_out: list[int] = []
    for lv, proc, out_dir in workers:
        try:
            proc.wait(timeout=TIMEOUT)
            log = os.path.join(out_dir, "output.txt")
            try:
                size = os.path.getsize(log) if os.path.exists(log) else 0
                print(f"  Level {lv}: done ({size} bytes)")
            except OSError as exc:
                print(f"  Level {lv}: done (cannot read output size: {exc})")
        except subprocess.TimeoutExpired:
            print(
                f"  Level {lv}: TIMED OUT after {TIMEOUT}s -- sending SIGTERM"
            )
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except OSError:
                pass
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print(f"  Level {lv}: SIGTERM ignored -- sending SIGKILL")
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except OSError:
                    pass
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print(f"  Level {lv}: process could not be killed")
            timed_out.append(lv)
        except OSError as exc:
            print(f"  Level {lv}: error ({exc})")
            failed.append(lv)

    if timed_out:
        print(f"\nTimed-out levels: {timed_out}")
    if failed:
        print(f"\nFailed levels: {failed}")

    if not timed_out and not failed:
        print("\nAll workers complete.")
    else:
        print("\nSome workers did not complete successfully.")


if __name__ == "__main__":
    main()
