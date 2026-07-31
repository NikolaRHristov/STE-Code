#!/usr/bin/env python3
"""Launch Agent #7 workers at multiple STE-Code levels.

Uses the Hermes oneshot wrapper. This script does not expose tools
and does not pollute Hermes session history. The orchestrator starts
all level workers, waits for completion with timeouts, and reports results.
"""
from __future__ import annotations

import argparse
import atexit
import datetime
import fcntl
import json
import logging
import os
import shutil
import signal as _signal
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Defaults (overridable via CLI)
# ---------------------------------------------------------------------------
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DOCS = ["README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "RELEASE-NOTES.md"]
DEFAULT_OUT = os.path.join(PROJECT, ".agents", "rewrites")
DEFAULT_MODEL = "poolside/laguna-s-2.1:free"

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
    # ── New: extended CLI options ──
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate all inputs and print the launch plan. Do not start any workers.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show debug-level log messages during execution.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output. Show only errors and the final summary.",
    )
    parser.add_argument(
        "--json-summary",
        type=str,
        default=None,
        metavar="PATH",
        help="Write a machine-readable JSON summary to this file after all workers finish.",
    )
    parser.add_argument(
        "--tmp-dir",
        type=str,
        default="/tmp",
        help="Directory for temporary prompt files (default: /tmp)",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=0,
        help="Number of retry attempts for workers that fail (default: 0)",
    )
    parser.add_argument(
        "--stagger",
        type=float,
        default=0.5,
        help="Delay in seconds between parallel worker launches (default: 0.5)",
    )
    parser.add_argument(
        "--no-lock",
        action="store_true",
        help="Skip the lock-file check. Use with care — allows concurrent orchestrator runs.",
    )
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """Set the root logger level based on verbosity flags.

    Quiet mode suppresses everything below ERROR.
    Verbose mode enables DEBUG.
    Default mode shows INFO and above.
    """
    if quiet:
        level = logging.ERROR
    elif verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)-7s] %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stderr,
    )


# ---------------------------------------------------------------------------
# Signal handling — clean shutdown of child processes
# ---------------------------------------------------------------------------
# Global registry of active child PIDs.  The signal handler iterates this set
# and sends SIGTERM (then SIGKILL after a grace period) to every registered
# child so we never leave orphaned workers behind.
_CHILD_PIDS: set[int] = set()
_CHILD_PIDS_LOCK = threading.Lock()


def _register_child(pid: int) -> None:
    """Add a child PID to the active registry."""
    with _CHILD_PIDS_LOCK:
        _CHILD_PIDS.add(pid)


def _unregister_child(pid: int) -> None:
    """Remove a child PID from the active registry."""
    with _CHILD_PIDS_LOCK:
        _CHILD_PIDS.discard(pid)


def _kill_all_children() -> None:
    """Send SIGTERM to all registered children.  Then wait 3 s and send SIGKILL."""
    with _CHILD_PIDS_LOCK:
        pids = list(_CHILD_PIDS)
    if not pids:
        return
    logging.warning("Sending SIGTERM to %d child process(es)...", len(pids))
    for pid in pids:
        try:
            os.killpg(os.getpgid(pid), _signal.SIGTERM)
        except OSError:
            pass
    time.sleep(3)
    for pid in pids:
        try:
            os.killpg(os.getpgid(pid), _signal.SIGKILL)
        except OSError:
            pass
    logging.warning("All children killed.")


def _handle_termination_signal(signum: int, frame: Any) -> None:
    """Handle SIGINT or SIGTERM for the orchestrator.

    Kills all child processes and exits with code 130 (SIGINT) or 143 (SIGTERM).
    """
    sig_name = _signal.Signals(signum).name
    print(f"\nReceived {sig_name}. Cleaning up child processes...")
    _kill_all_children()
    _cleanup_temp_files()
    sys.exit(128 + signum)


def _install_signal_handlers() -> None:
    """Install SIGINT and SIGTERM handlers for the orchestrator process."""
    _signal.signal(_signal.SIGINT, _handle_termination_signal)
    _signal.signal(_signal.SIGTERM, _handle_termination_signal)


# ---------------------------------------------------------------------------
# Lock file — prevent concurrent orchestrator runs
# ---------------------------------------------------------------------------
def acquire_lock(lock_path: str, no_lock: bool = False) -> bool:
    """Try to acquire an exclusive lock file.

    Returns True on success.  Returns False when another instance
    already holds the lock.  When no_lock is True, always returns True.
    """
    if no_lock:
        logging.debug("Lock check skipped (--no-lock).")
        return True
    try:
        _LOCK_FD = open(lock_path, "w")
        fcntl.flock(_LOCK_FD, fcntl.LOCK_EX | fcntl.LOCK_NB)
        _LOCK_FD.write(f"pid={os.getpid()}\ntime={datetime.datetime.now().isoformat()}\n")
        _LOCK_FD.flush()
        # Keep the fd open for the lifetime of the process.
        atexit.register(lambda: os.remove(lock_path) if os.path.exists(lock_path) else None)
        return True
    except (IOError, OSError):
        print("ERROR: Another orchestrator instance is already running.")
        print(f"  If this is a stale lock, remove: {lock_path}")
        return False


# ---------------------------------------------------------------------------
# Worker result tracking
# ---------------------------------------------------------------------------
@dataclass
class WorkerResult:
    """Track the outcome of a single level worker."""

    level: int
    description: str
    output_dir: str
    pid: int | None = None
    status: str = "pending"
    start_time: datetime.datetime | None = None
    end_time: datetime.datetime | None = None
    exit_code: int | None = None
    output_size: int = 0
    error_message: str = ""

    @property
    def elapsed(self) -> datetime.timedelta | None:
        """Return the wall-clock duration of this worker."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    @property
    def succeeded(self) -> bool:
        """Return True when the worker finished with exit code 0 within timeout."""
        return self.status == "complete" and self.exit_code == 0

    def summary_line(self) -> str:
        """Return a one-line status string for the summary table."""
        status_icon = {"complete": "✓", "timeout": "⏱", "error": "✗", "pending": "…"}.get(
            self.status, "?"
        )
        elapsed_str = f"{self.elapsed}" if self.elapsed else "—"
        size_str = f"{self.output_size:,} B" if self.output_size else "—"
        pid_str = f"PID {self.pid}" if self.pid else "—"
        return (
            f"  {status_icon} Level {self.level:<2}  {elapsed_str:<16}  "
            f"{size_str:<12}  {pid_str:<10}  {self.error_message}"
        )


# ---------------------------------------------------------------------------
# Pre-flight validation
# ---------------------------------------------------------------------------
def validate_environment(
    venv_python: str,
    wrapper: str,
    docs: list[str],
    output_dir: str,
    tmp_dir: str,
    rules_path: str,
) -> list[str]:
    """Check that all required paths and resources exist before launching workers.

    Returns a list of warning messages.  Halts with sys.exit(1) on fatal errors.
    """
    warnings: list[str] = []

    # Check venv Python.
    if not os.path.isfile(venv_python) or not os.access(venv_python, os.X_OK):
        print(f"ERROR: Python not found or not executable: {venv_python}")
        print("  Set the HERMES_LAUNCH_VENV environment variable to override.")
        sys.exit(1)

    # Check wrapper script.
    if not os.path.isfile(wrapper):
        print(f"ERROR: Wrapper not found at {wrapper}")
        sys.exit(1)

    # Check rules file.
    if not os.path.isfile(rules_path):
        print(f"ERROR: Rules file not found at {rules_path}")
        sys.exit(1)

    # Check each document.
    missing: list[str] = []
    for doc in docs:
        dpath = os.path.join(PROJECT, doc)
        if not os.path.isfile(dpath):
            missing.append(doc)
    if missing:
        warnings.append(f"Documents not found: {', '.join(missing)}")

    # Check output directory (try to create it).
    try:
        os.makedirs(output_dir, exist_ok=True)
    except PermissionError:
        print(f"ERROR: Cannot create output directory (permission denied): {output_dir}")
        sys.exit(1)
    except OSError as exc:
        print(f"ERROR: Cannot create output directory: {exc}")
        sys.exit(1)

    # Check that output directory is writable.
    test_file = os.path.join(output_dir, ".write-test")
    try:
        with open(test_file, "w") as f:
            f.write("ok")
        os.remove(test_file)
    except OSError as exc:
        print(f"ERROR: Output directory is not writable: {exc}")
        sys.exit(1)

    # Check temp directory.
    if not os.path.isdir(tmp_dir):
        print(f"ERROR: Temp directory not found: {tmp_dir}")
        sys.exit(1)
    if not os.access(tmp_dir, os.W_OK):
        print(f"ERROR: Temp directory is not writable: {tmp_dir}")
        sys.exit(1)

    # Check available disk space (warn below 100 MB).
    try:
        usage = shutil.disk_usage(output_dir)
        free_mb = usage.free // (1024 * 1024)
        if free_mb < 100:
            warnings.append(f"Low disk space: {free_mb} MB free on output volume")
    except OSError:
        pass  # Not all filesystems support disk_usage.

    return warnings


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    args = parse_args()

    # Setup logging.
    setup_logging(verbose=args.verbose, quiet=args.quiet)

    # Install signal handlers early so we can clean up on Ctrl-C.
    _install_signal_handlers()

    # Acquire lock to prevent concurrent orchestrator runs.
    lock_path = os.path.join(tempfile.gettempdir(), "ste-code-launch-levels.lock")
    if not acquire_lock(lock_path, no_lock=args.no_lock):
        sys.exit(1)

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
    TMP_DIR = args.tmp_dir
    RETRIES = args.retries

    # Allow environment variable overrides.
    VENV: str = os.environ.get("HERMES_LAUNCH_VENV") or VENV_PYTHON
    USE_MODEL: str = os.environ.get("HERMES_LAUNCH_MODEL") or MODEL

    # Validate the wrapper script exists.
    if not os.path.exists(WRAPPER):
        print(f"ERROR: Wrapper not found at {WRAPPER}")
        sys.exit(1)

    # Load the STE-Code rules file.
    rules_path = os.path.join(
        PROJECT, "ste-code/artifacts/ste-code-distilled-system-prompt.txt"
    )

    # ── Pre-flight validation ──
    logging.info("Running pre-flight validation...")
    warnings = validate_environment(
        venv_python=VENV,
        wrapper=WRAPPER,
        docs=DOCS,
        output_dir=OUT,
        tmp_dir=TMP_DIR,
        rules_path=rules_path,
    )
    for w in warnings:
        print(f"WARNING: {w}")

    # Load rules file.
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

    # ── Token budget estimate for the smallest level ──
    min_level = min(LEVELS.keys())
    sample_prompt = f"""{rules}

Level {min_level} ({LEVELS[min_level]}). You are Agent #7.

TASK: Rewrite all {len(DOCS)} documents below using only Level {min_level} rules.
Output inline only -- do NOT create any files or use any tools.
For each document output: rewritten text, change log, compliance table.

{docs_text}"""
    budget_ok = warn_if_over_budget(sample_prompt)

    # ── Dry-run mode: print plan and exit ──
    if args.dry_run:
        print("\n=== DRY RUN — no workers will start ===")
        print(f"Model:         {USE_MODEL}")
        print(f"Levels:        {', '.join(str(lv) for lv in sorted(LEVELS))}")
        print(f"Documents:     {', '.join(DOCS)}")
        print(f"Output dir:    {OUT}")
        print(f"Timeout:       {TIMEOUT}s per worker")
        print(f"Retries:       {RETRIES}")
        print(f"Stagger:       {args.stagger}s between launches")
        print(f"Rules file:    {rules_path} ({estimate_tokens(rules):,} estimated tokens)")
        print(f"Docs text:     {estimate_tokens(docs_text):,} estimated tokens")
        print(f"Total prompt:  {estimate_tokens(sample_prompt):,} estimated tokens")
        print(f"Budget check:  {'OK' if budget_ok else 'OVER BUDGET — responses may be truncated'}")
        print(f"Warnings:      {len(warnings)}")
        for w in warnings:
            print(f"  - {w}")
        print("=== Plan validated. Use without --dry-run to launch. ===")
        return

    # ── Launch workers in parallel ──
    if not args.quiet:
        print(f"\nLaunching {len(LEVELS)} level workers...")
        print(f"  Model:   {USE_MODEL}")
        print(f"  Timeout: {TIMEOUT}s per worker")
        print(f"  Output:  {OUT}")
        print()

    # Prepare worker configurations.  Each item is (level, description, prompt_text).
    worker_configs: list[tuple[int, str, str]] = []
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
        worker_configs.append((lv, desc, prompt))

    # ── Launch workers via thread pool ──
    # Each thread writes a temp file and starts a subprocess.
    # The main thread collects results and waits for completion.
    results: dict[int, WorkerResult] = {}

    def _launch_one(lv: int, desc: str, prompt: str, attempt: int = 1) -> WorkerResult:
        """Launch a single worker and return its result.

        Writes the prompt to a temp file, starts the subprocess, registers
        the child PID for signal cleanup, and returns a WorkerResult.
        """
        result = WorkerResult(
            level=lv,
            description=desc,
            output_dir=os.path.join(OUT, f"level-{lv}"),
            start_time=datetime.datetime.now(),
        )

        # Write prompt to temp file (wrapper reads from file and deletes it).
        try:
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", delete=False, dir=TMP_DIR
            )
            tmp.write(prompt)
            tmp.close()
        except OSError as exc:
            result.status = "error"
            result.error_message = f"Cannot write temp file: {exc}"
            return result
        _register_temp(tmp.name)

        log_file = os.path.join(result.output_dir, "output.txt")
        attempt_suffix = f" (attempt {attempt})" if attempt > 1 else ""
        logging.info("Level %d%s: launching -> %s", lv, attempt_suffix, log_file)

        # Fire-and-forget: Popen with start_new_session.
        # Use local variables to satisfy the type checker.
        _venv: str = VENV
        _wrapper: str = WRAPPER
        _model: str = USE_MODEL
        try:
            _stdout_fd = open(log_file, "w")  # noqa: SIM115
            proc = subprocess.Popen(
                [_venv, _wrapper, tmp.name, "--model", _model],
                stdout=_stdout_fd,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                env={**os.environ, "HERMES_ACCEPT_HOOKS": "1"},
            )
        except FileNotFoundError:
            result.status = "error"
            result.error_message = "Python or wrapper not found"
            return result
        except PermissionError:
            result.status = "error"
            result.error_message = "Permission denied"
            return result
        except OSError as exc:
            result.status = "error"
            result.error_message = f"Launch failed: {exc}"
            return result

        result.pid = proc.pid
        _register_child(proc.pid)

        # Wait for the subprocess with timeout.
        try:
            proc.wait(timeout=TIMEOUT)
            result.exit_code = proc.returncode
            result.status = "complete"
        except subprocess.TimeoutExpired:
            result.status = "timeout"
            result.error_message = f"Timed out after {TIMEOUT}s"
            logging.warning("Level %d: timeout — sending SIGTERM to pgid %d", lv, proc.pid)
            try:
                os.killpg(os.getpgid(proc.pid), _signal.SIGTERM)
            except OSError:
                pass
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logging.warning("Level %d: SIGTERM ignored — sending SIGKILL", lv)
                try:
                    os.killpg(os.getpgid(proc.pid), _signal.SIGKILL)
                except OSError:
                    pass
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    result.error_message += " (process could not be killed)"
            result.exit_code = proc.returncode
        except OSError as exc:
            result.status = "error"
            result.error_message = f"Wait error: {exc}"

        _unregister_child(proc.pid)
        result.end_time = datetime.datetime.now()

        # Collect output file size.
        try:
            if os.path.exists(log_file):
                result.output_size = os.path.getsize(log_file)
        except OSError:
            pass

        # ── Output content validation ──
        if result.status == "complete":
            if result.exit_code != 0:
                result.error_message = f"Exit code {result.exit_code}"
            elif result.output_size == 0:
                result.error_message = "Output file is empty"
            elif result.output_size < 100:
                result.error_message = (
                    f"Output file is too small ({result.output_size} B) — possible truncation"
                )

        return result

    # Launch all workers using a thread pool.
    with ThreadPoolExecutor(max_workers=len(worker_configs)) as executor:
        future_map: dict[Any, int] = {}
        for lv, desc, prompt in worker_configs:
            future = executor.submit(_launch_one, lv, desc, prompt, 1)
            future_map[future] = lv
            time.sleep(args.stagger)  # Stagger launches to avoid API rate spikes.

        # Collect results as they finish.
        for future in as_completed(future_map):
            lv = future_map[future]
            try:
                result = future.result()
            except Exception as exc:
                result = WorkerResult(
                    level=lv,
                    description=LEVELS.get(lv, "unknown"),
                    output_dir=os.path.join(OUT, f"level-{lv}"),
                    status="error",
                    error_message=f"Thread exception: {exc}",
                )
            results[lv] = result

    # ── Retry failed workers ──
    if RETRIES > 0:
        for lv, result in list(results.items()):
            if result.succeeded:
                continue
            for attempt in range(2, RETRIES + 2):
                if not args.quiet:
                    print(f"  Level {lv}: retry {attempt - 1}/{RETRIES}...")
                desc = LEVELS.get(lv, "unknown")
                # Rebuild the prompt from configs.
                prompt = next((p for l, d, p in worker_configs if l == lv), "")
                if not prompt:
                    break
                retry_result = _launch_one(lv, desc, prompt, attempt)
                results[lv] = retry_result
                if retry_result.succeeded:
                    break

    # ── Print summary ──
    print()
    print("=" * 72)
    print("RESULTS")
    print("=" * 72)
    if not args.quiet:
        for lv in sorted(results):
            print(results[lv].summary_line())

    succeeded = sum(1 for r in results.values() if r.succeeded)
    timed_out = sum(1 for r in results.values() if r.status == "timeout")
    failed = sum(1 for r in results.values() if r.status == "error")
    total = len(results)

    print()
    if succeeded == total:
        print(f"All {total} workers complete.")
    else:
        parts: list[str] = []
        if succeeded:
            parts.append(f"{succeeded} complete")
        if timed_out:
            parts.append(f"{timed_out} timed out")
        if failed:
            parts.append(f"{failed} failed")
        print(f"Summary: {', '.join(parts)} (of {total} total)")
        print(f"Results: {OUT}/level-{{level}}/output.txt")
        print("Check the output files listed above for details.")
        sys.exit(1)

    # ── JSON summary ──
    if args.json_summary:
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "model": USE_MODEL,
            "levels_requested": sorted(LEVELS),
            "documents": DOCS,
            "output_dir": OUT,
            "timeout": TIMEOUT,
            "results": {
                str(lv): {
                    "status": r.status,
                    "exit_code": r.exit_code,
                    "output_size": r.output_size,
                    "elapsed_seconds": r.elapsed.total_seconds() if r.elapsed else None,
                    "error": r.error_message or None,
                    "pid": r.pid,
                }
                for lv, r in sorted(results.items())
            },
        }
        try:
            with open(args.json_summary, "w") as f:
                json.dump(summary_data, f, indent=2)
            if not args.quiet:
                print(f"JSON summary written to: {args.json_summary}")
        except OSError as exc:
            print(f"ERROR: Cannot write JSON summary: {exc}")


if __name__ == "__main__":
    main()
