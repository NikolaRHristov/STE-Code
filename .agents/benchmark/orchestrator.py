#!/usr/bin/env python3
"""STE-Code Benchmark Orchestrator — parallel workers, proper scoring, full reports.

Design rationale:
  Scoring formula:  score = 0.4 + 0.6*(met/total_principles) - 0.3*(found/total_forbidden) + 0.1*(found/total_expected)
  
  The 0.4 BASE ensures even a worker that addresses zero principles gets a floor above zero,
  because some output is better than no output. Without a base, a worker that produces valid
  content but misses all principle tags would score 0.0 — indistinguishable from a crash.

  The 0.6 PRINCIPLE weight is the dominant term: 60% of the score comes from explicit principle
  compliance. This is the primary signal.

  The -0.3 FORBIDDEN penalty caps the damage from forbidden keywords at 0.3 points. A single
  forbidden word in a small test case should not zero out an otherwise good response.

  The +0.1 EXPECTED bonus is a small reward for using approved vocabulary. It is deliberately
  small (10%) because expected keywords are a soft signal — their absence may mean the worker
  chose different but still valid terminology.

  Pass threshold: 0.7. This was calibrated against the 59-test suite. At 0.6, many borderline
  outputs passed that humans rated as "needs improvement." At 0.8, well-scoring outputs that
  missed only one principle would fail. 0.7 struck the best balance.

Worker lifecycle:  LAUNCH -> RUNNING -> {SUCCESS | TIMEOUT | CRASH | EMPTY}
                    EMPTY -> {RETRY_1..RETRY_N} -> {SUCCESS | FINAL_FAILURE}

Resume protocol:  Each run writes a PROGRESS state file tracking every worker outcome.
  On --resume, the orchestrator loads the previous state and skips workers whose
  output files exist and are non-empty. This preserves partial runs across crashes.
"""

import argparse
import atexit
import json
import logging
import os
import re
import signal
import sys
import tempfile
import time
import difflib
import glob
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, Optional

# ---------------------------------------------------------------------------
# CLI argument parsing — all magic numbers become overridable
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="STE-Code Benchmark Orchestrator — run 59+ tests in parallel workers"
    )
    p.add_argument(
        "--model", "-m",
        default="poolside/laguna-s-2.1:free",
        help="Model name passed to hermes (default: poolside/laguna-s-2.1:free)"
    )
    p.add_argument(
        "--test-dir",
        default=None,
        help="Directory containing category-*.json test case files (default: auto-detect)"
    )
    p.add_argument(
        "--results-dir",
        default=None,
        help="Directory to write run results (default: auto-detect)"
    )
    p.add_argument(
        "--system-prompt-file",
        default=None,
        help="File containing the STE-Code system prompt (default: auto-detect)"
    )
    p.add_argument(
        "--timeout", "-t",
        type=int, default=600,
        help="Maximum seconds to wait for all workers (default: 600)"
    )
    p.add_argument(
        "--poll-interval", "-p",
        type=int, default=5,
        help="Seconds between worker-completion polls (default: 5)"
    )
    p.add_argument(
        "--max-workers", "-w",
        type=int, default=0,
        help="Maximum concurrent workers. 0 = unlimited (one per test case). "
             "Use to avoid API rate limits (default: 0)"
    )
    p.add_argument(
        "--retries", "-r",
        type=int, default=2,
        help="Maximum retry attempts per worker if output is empty/missing (default: 2)"
    )
    p.add_argument(
        "--retry-delay",
        type=float, default=2.0,
        help="Seconds to wait before retrying a failed worker (default: 2.0)"
    )
    p.add_argument(
        "--stagger",
        type=float, default=0.0,
        help="Seconds to wait between launching each worker. "
             "Use > 0 to avoid API burst rate limits (default: 0)"
    )
    p.add_argument(
        "--resume",
        action="store_true",
        help="Resume a previous run — skip workers whose output files already exist"
    )
    p.add_argument(
        "--resume-run-dir",
        default=None,
        help="Explicit run directory to resume from (required if multiple previous runs exist)"
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Load test cases and print what would run, but do not launch workers"
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO)"
    )
    return p.parse_args()


# ---------------------------------------------------------------------------
# Signal handling — prevent orphaned child processes on kill/crash
# ---------------------------------------------------------------------------

# Global registry so signal handlers and cleanup can reach all workers.
_child_pids: Dict[str, int] = {}        # test_id -> pid
_run_dir: Optional[str] = None
_atexit_registered: bool = False

def _kill_all_children(signum: Optional[int] = None):
    """Send SIGKILL to every tracked child process, then SIGTERM for good measure."""
    if not _child_pids:
        return
    pids = list(_child_pids.values())
    # First pass: SIGTERM (polite)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    time.sleep(0.5)
    # Second pass: SIGKILL (forceful)
    for pid in pids:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    _child_pids.clear()


def _emergency_cleanup():
    """Write a partial progress file so the run can be resumed."""
    if not _run_dir or not os.path.isdir(_run_dir):
        return
    state = {
        "cleaned_up_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "remaining_children": list(_child_pids.keys()),
    }
    state_file = os.path.join(_run_dir, "emergency-state.json")
    try:
        with open(state_file, "w") as f:
            json.dump(state, f, indent=2)
        print(f"\nEmergency state saved to {state_file}", file=sys.stderr)
    except OSError:
        pass


def _signal_handler(signum, frame):
    """Handle SIGTERM/SIGINT: kill children, write emergency state, exit."""
    sig_name = signal.Signals(signum).name
    print(f"\nReceived {sig_name}. Killing {len(_child_pids)} workers...", file=sys.stderr)
    _kill_all_children(signum)
    _emergency_cleanup()
    sys.exit(128 + signum)


def install_signal_handlers():
    """Register signal handlers for clean shutdown."""
    signal.signal(signal.SIGTERM, _signal_handler)
    signal.signal(signal.SIGINT, _signal_handler)
    global _atexit_registered
    if not _atexit_registered:
        atexit.register(_emergency_cleanup)
        _atexit_registered = True


# ---------------------------------------------------------------------------
# Auto-detect project paths
# ---------------------------------------------------------------------------

def _resolve_path(cli_val: Optional[str], default_rel: str) -> str:
    """Return CLI override, or compute the default relative to the project root."""
    if cli_val is not None:
        return os.path.abspath(cli_val)
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    return os.path.join(project_root, default_rel)


# ---------------------------------------------------------------------------
# Scoring engine (extracted so it can be re-used by rescore.py)
# ---------------------------------------------------------------------------

# Canonical principle-to-keyword mapping.
# Each principle maps to a list of term stems that, when found in the
# output or compliance section, indicate the worker discussed that principle.
#
# NOTE: This is a heuristic. Keyword presence does NOT guarantee real
# compliance — the worker might just mention "passive voice" while still
# using it. True compliance measurement requires an LLM-as-judge step.
# These keywords are designed to catch explicit discussion of each
# principle, which is the primary signal in this benchmark.
PRINCIPLE_KEYWORDS = {
    "P1":  ["approved word", "dictionary", "approved term", "approved vocabulary"],
    "P2":  ["part of speech", "noun", "verb", "adjective", "adverb", "preposition", "conjunction"],
    "P3":  ["approved meaning", "meaning", "definition", "defined sense", "single meaning"],
    "P4":  ["active voice", "passive voice", "imperative", "infinitive", "simple present", "simple past", "past participle"],
    "P5":  ["technical noun", "keyword", "framework", "library", "class name", "function name", "variable name"],
    "P6":  ["non-approved", "technical name", "technical term", "unapproved"],
    "P7":  ["noun as verb", "do not use noun as verb", "nominalization", "verbing"],
    "P8":  ["standard", "well-known", "recognized", "established term"],
    "P9":  ["short", "clear", "concise", "brief", "simple word"],
    "P10": ["slang", "jargon", "regional", "vague", "informal", "colloquial", "idiom"],
    "P11": ["one term", "consistent", "same term", "synonym", "do not use synonyms"],
    "P12": ["technical verb", "build", "deploy", "test", "lint", "compile", "debug", "install", "configure", "execute"],
    "P13": ["verb as noun", "do not use verb as noun", "gerund as noun"],
    "P14": ["american spelling", "american english", "color", "analyze", "organize", "standardize"],
}


def extract_corrected_text(output):
    """Extract corrected text - handle multiple output formats."""
    for marker in [r'\*\*Corrected Text:\*\*', r'## Corrected Text', r'CORRECTED TEXT',
                   r'# Corrected Text', r'Corrected Text \(STE-Code Compliant\)',
                   r'# STE-Code Corrected Text']:
        m = re.search(marker + r'\s*\n+(.*?)(?:\n---\n|\n## Compliance|\n# Compliance|\nCOMPLIANCE|\n\*\*Compliance)', output, re.DOTALL | re.IGNORECASE)
        if m and m.group(1).strip():
            return m.group(1).strip()
    m = re.search(r'^(.*?)(?:\n---\n|\n#+\s*Compliance|\nCOMPLIANCE)', output, re.DOTALL | re.IGNORECASE)
    if m:
        text = m.group(1).strip()
        text = re.sub(r'^#+\s*(?:Corrected|STE-Code).*?\n+', '', text, flags=re.IGNORECASE)
        if text: return text.strip()
    return output.strip()


def extract_compliance_section(output):
    """Extract compliance summary - handle multiple formats."""
    for marker in [r'\*\*Compliance Summary\*\*', r'## Compliance Summary', r'COMPLIANCE SUMMARY',
                   r'# Compliance Summary', r'Compliance Summary']:
        m = re.search(re.escape(marker) if '**' in marker else marker + r'\s*\n(.*)', output, re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip() if m.lastindex else m.group(0)
    return ""


def check_principles(output, expected_principles):
    """Check principles in BOTH compliance section AND full output."""
    compliance = extract_compliance_section(output)
    full_lower = (compliance + " " + output).lower()

    satisfied = []
    missed = []

    for p in expected_principles:
        found = False
        # 1. Explicit principle number mention in compliance
        if re.search(r'\b' + re.escape(p) + r'\b', compliance):
            found = True
        # 2. Keyword heuristics
        if not found and p in PRINCIPLE_KEYWORDS:
            for kw in PRINCIPLE_KEYWORDS[p]:
                if kw.lower() in full_lower:
                    found = True
                    break
        # 3. Also check full output for principle number
        if not found and re.search(r'\b' + re.escape(p) + r'\b', output):
            found = True

        if found:
            satisfied.append(p)
        else:
            missed.append(p)

    return satisfied, missed


def check_keywords(text_lower, keywords):
    """Check which keywords appear in text."""
    found = []
    for kw in keywords:
        if kw.lower() in text_lower:
            found.append(kw)
    return found


def calc_correctness(expected_principles, satisfied, forbidden_found, total_forbidden, expected_kw_found, total_expected_kw):
    """
    Calculate correctness score 0-1 using weighted formula.

    Weight design rationale:
      base        = 0.4   Floor: even a non-compliant answer is worth 0.4.
                           This distinguishes "wrong" from "no answer at all" (which would be NaN).
      principles  = 0.6   Primary signal. 60% of score comes from covering expected principles.
      forbidden   =-0.3   Maximum penalty for forbidden keywords. Capped so one bad word
                           cannot zero out a response that otherwise complies with 13/14 principles.
      expected    =+0.1   Small bonus for using approved vocabulary. Deliberately low
                           because a worker may choose different but equally valid terms.
    """
    score = 0.4  # base

    # Principle compliance: 60% weight
    if expected_principles:
        score += 0.6 * len(satisfied) / len(expected_principles)

    # Forbidden keywords penalty: deduct up to 0.3
    if total_forbidden > 0:
        score -= 0.3 * len(forbidden_found) / total_forbidden

    # Expected keywords bonus: add up to 0.1
    if total_expected_kw > 0:
        score += 0.1 * len(expected_kw_found) / total_expected_kw

    return round(max(0.0, min(1.0, score)), 2)


# ---------------------------------------------------------------------------
# Worker result classification
# ---------------------------------------------------------------------------

# Worker outcome enum — used for progress tracking and retry decisions.
WORKER_SUCCESS = "SUCCESS"
WORKER_TIMEOUT = "TIMEOUT"
WORKER_CRASH = "CRASH"
WORKER_EMPTY = "EMPTY"
WORKER_MISSING = "MISSING"


def classify_worker_result(output_path: str, was_timed_out: bool) -> str:
    """
    Classify a worker's result based on output file state.

    Returns one of: SUCCESS, TIMEOUT, CRASH, EMPTY, MISSING
    """
    if was_timed_out:
        return WORKER_TIMEOUT
    if not os.path.isfile(output_path):
        return WORKER_MISSING
    try:
        size = os.path.getsize(output_path)
    except OSError:
        return WORKER_MISSING
    if size == 0:
        return WORKER_EMPTY
    # Read first few bytes to detect crash markers.
    try:
        with open(output_path) as f:
            head = f.read(200)
    except OSError:
        return WORKER_CRASH
    if head.startswith("HERMES_ERROR") or "Traceback (most recent call last)" in head:
        return WORKER_CRASH
    if size < 20:
        return WORKER_EMPTY
    return WORKER_SUCCESS


# ---------------------------------------------------------------------------
# Main orchestration
# ---------------------------------------------------------------------------

def main():
    global _child_pids, _run_dir

    args = parse_args()

    # Setup logging.
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    log = logging.getLogger("orchestrator")

    # Resolve paths.
    test_dir = _resolve_path(args.test_dir, ".agents/benchmark/test-cases")
    results_dir = _resolve_path(args.results_dir, ".agents/benchmark/results")
    sys_prompt_file = _resolve_path(
        args.system_prompt_file,
        "ste-code/artifacts/llms-full.txt",
    )

    # Load system prompt.
    try:
        with open(sys_prompt_file) as f:
            system_prompt = f.read()
    except FileNotFoundError:
        log.error("System prompt file not found: %s", sys_prompt_file)
        sys.exit(1)

    # Load all test cases.
    test_cases = []
    cat_files = sorted(glob.glob(os.path.join(test_dir, "category-*.json")))
    if not cat_files:
        log.error("No category-*.json files found in %s", test_dir)
        sys.exit(1)
    for cat_file in cat_files:
        with open(cat_file) as f:
            tests = json.load(f)
        for t in tests:
            t["_file"] = cat_file
            test_cases.append(t)

    # Print banner.
    print(f"=== STE-Code Benchmark Orchestrator ===")
    print(f"Model:       {args.model}")
    print(f"Test cases:  {len(test_cases)}")
    print(f"Max workers: {'unlimited' if args.max_workers == 0 else args.max_workers}")
    print(f"Timeout:     {args.timeout}s")
    print(f"Retries:     {args.retries}")
    print(f"Resume:      {'yes' if args.resume else 'no'}")
    if args.dry_run:
        print("DRY RUN — no workers will be launched.")
        for tc in test_cases:
            is_gen = "prompt" in tc
            print(f"  [{tc['id']}] {tc['category']} ({'gen' if is_gen else 'corr'}) — {tc.get('description','')[:60]}")
        print(f"\nWould run {len(test_cases)} workers with --model={args.model}")
        return

    # Create or resume run directory.
    if args.resume:
        if args.resume_run_dir:
            run_dir = os.path.abspath(args.resume_run_dir)
        else:
            # Find the most recent run.
            existing = sorted(glob.glob(os.path.join(results_dir, "run-*")))
            if not existing:
                log.error("No previous run found to resume. Use --resume-run-dir to point at one.")
                sys.exit(1)
            run_dir = existing[-1]
        print(f"Resuming run: {run_dir}")
        if not os.path.isdir(run_dir):
            log.error("Run directory does not exist: %s", run_dir)
            sys.exit(1)
    else:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        run_dir = os.path.join(results_dir, f"run-{timestamp}")
        os.makedirs(run_dir, exist_ok=True)

    _run_dir = run_dir
    install_signal_handlers()

    # -----------------------------------------------------------------------
    # Progress state file — enables resume and tracks worker lifecycle.
    # -----------------------------------------------------------------------
    progress_file = os.path.join(run_dir, "progress.json")
    progress: Dict[str, dict] = {}

    # Load existing progress when resuming.
    if args.resume and os.path.isfile(progress_file):
        with open(progress_file) as f:
            progress = json.load(f)
        log.info("Loaded progress: %d workers from previous session", len(progress))

    def save_progress():
        """Atomically write progress state to disk."""
        tmp = progress_file + ".tmp"
        with open(tmp, "w") as f:
            json.dump(progress, f, indent=2, default=str)
        os.replace(tmp, progress_file)

    # -----------------------------------------------------------------------
    # Phase 1: Launch all workers in parallel (or batched by max-workers).
    # When resuming, skip workers that already have non-empty output files.
    # -----------------------------------------------------------------------
    workers: Dict[str, dict] = {}  # test_id -> {pid, out_file, start_time, attempt}

    # Determine which test cases need launching.
    to_launch = []
    for tc in test_cases:
        tid = tc["id"]
        out_file = os.path.join(run_dir, f"{tid}-output.txt")
        if args.resume and tid in progress:
            prev = progress[tid]
            if prev.get("outcome") == WORKER_SUCCESS and os.path.isfile(out_file) and os.path.getsize(out_file) > 0:
                log.info("Skipping %s — already completed in previous run", tid)
                # Re-register with pid=-1 (already done) so scoring can pick it up.
                workers[tid] = {
                    "pid": -1,
                    "out_file": out_file,
                    "start_time": prev.get("start_time", time.time()),
                    "attempt": prev.get("attempt", 1),
                    "completed": True,
                }
                continue
        to_launch.append(tc)

    if to_launch:
        print(f"Launching {len(to_launch)} workers...")
    else:
        print("All workers already completed. Scoring only.")

    max_workers = args.max_workers if args.max_workers > 0 else len(to_launch)
    launch_index = 0

    while launch_index < len(to_launch):
        # Count currently running workers (pid > 0 and not yet completed).
        running = sum(
            1 for w in workers.values()
            if w.get("pid", -1) > 0 and not w.get("completed", False)
        )
        slots = max_workers - running

        for _ in range(min(slots, len(to_launch) - launch_index)):
            tc = to_launch[launch_index]
            launch_index += 1

            tid = tc["id"]
            is_generation = "prompt" in tc
            task_input = tc.get("prompt", tc.get("input", ""))

            # Build full prompt based on type.
            if is_generation:
                full_prompt = f"""{system_prompt}

## TASK
{task_input}

IMPORTANT: Do NOT create any files. Output all code and documentation inline as text.
Use STE-Code principles (P1-P14) for all documentation and text you generate.
Apply the synonym table for all word choices.
Produce the requested output first, then a compliance summary table showing which principles you followed."""
            else:
                full_prompt = f"""{system_prompt}

## TASK
Check the following text for STE-Code compliance. Apply all 14 principles (P1-P14). 
Replace unapproved terms using the synonym table. 
IMPORTANT: Do NOT create any files. Output the corrected text inline.
Produce the corrected text first, then a compliance summary table.

## TEXT TO CORRECT
{task_input}"""

            # Write prompt to temp file (useful for debugging).
            prompt_file = os.path.join(run_dir, f"{tid}-prompt.txt")
            with open(prompt_file, "w") as f:
                f.write(full_prompt)

            out_file = os.path.join(run_dir, f"{tid}-output.txt")

            # Launch fire-and-forget worker in isolated temp dir.
            pid = os.fork()
            if pid == 0:
                # Child: isolate CWD to prevent root file leaks.
                worker_dir = os.path.join(run_dir, f"worker-{tid}")
                os.makedirs(worker_dir, exist_ok=True)
                os.chdir(worker_dir)
                # Redirect stdout/stderr to output file.
                with open(out_file, "w") as outf:
                    os.dup2(outf.fileno(), 1)
                    os.dup2(outf.fileno(), 2)
                os.execvp("hermes", ["hermes", "-z", full_prompt, "-m", args.model, "--yolo"])
                os._exit(1)  # should not reach

            _child_pids[tid] = pid
            start_ts = time.time()
            workers[tid] = {
                "pid": pid,
                "out_file": out_file,
                "start_time": start_ts,
                "attempt": 1,
            }
            progress[tid] = {
                "pid": pid,
                "out_file": out_file,
                "start_time": start_ts,
                "attempt": 1,
                "outcome": "LAUNCHED",
            }
            save_progress()

            # Optional stagger to avoid API burst rate limits.
            if args.stagger > 0:
                time.sleep(args.stagger)

        # Brief sleep between batch-check loops so we do not busy-wait.
        if launch_index < len(to_launch):
            time.sleep(0.5)

    print(f"All {len(workers)} workers launched. Waiting for completion...")
    print()

    # -----------------------------------------------------------------------
    # Phase 2: Wait for all workers with timeout and retry support.
    # -----------------------------------------------------------------------
    poll_interval = args.poll_interval
    max_wait = args.timeout
    elapsed = 0

    pending = {tid for tid, w in workers.items() if not w.get("completed", False)}

    while pending and elapsed < max_wait:
        time.sleep(poll_interval)
        elapsed += poll_interval

        just_finished = []
        for tid in list(pending):
            pid = workers[tid]["pid"]
            if pid <= 0:
                # Already completed (pid=-1 for resumed workers).
                just_finished.append(tid)
                continue
            try:
                wpid, status = os.waitpid(pid, os.WNOHANG)
                if wpid != 0:
                    just_finished.append(tid)
                    # Remove from child PID registry so cleanup skips it.
                    _child_pids.pop(tid, None)
            except ChildProcessError:
                just_finished.append(tid)
                _child_pids.pop(tid, None)

        for tid in just_finished:
            pending.discard(tid)
            # Classify the result for progress tracking.
            is_timed_out = False  # worker finished, not timed out globally (yet)
            outcome = classify_worker_result(workers[tid]["out_file"], is_timed_out)
            progress[tid]["outcome"] = outcome
            progress[tid]["end_time"] = time.time()
            save_progress()

        if just_finished:
            print(f"  [{len(workers)-len(pending)}/{len(workers)}] Completed: {', '.join(just_finished)}")
        elif elapsed % 30 == 0:
            print(f"  ... still waiting ({len(pending)} remaining, {elapsed}s elapsed)")

    # Mark timed-out workers.
    timed_out = set()
    if pending:
        for tid in pending:
            timed_out.add(tid)
            _child_pids.pop(tid, None)
            progress[tid]["outcome"] = WORKER_TIMEOUT
            progress[tid]["end_time"] = time.time()
        save_progress()
        print(f"WARNING: {len(pending)} workers timed out: {', '.join(sorted(pending))}")

    # -----------------------------------------------------------------------
    # Phase 2b: Retry workers that produced empty or missing output.
    # Retries are limited to args.retries; only EMPTY and MISSING are retried.
    # TIMEOUT and CRASH are NOT retried (they indicate infrastructure issues).
    # -----------------------------------------------------------------------
    if args.retries > 0:
        retryable_outcomes = {WORKER_EMPTY, WORKER_MISSING}
        for tid in list(workers.keys()):
            attempt = workers[tid].get("attempt", 1)
            out_file = workers[tid]["out_file"]
            outcome = progress[tid].get("outcome", classify_worker_result(out_file, tid in timed_out))

            while outcome in retryable_outcomes and attempt <= args.retries:
                attempt += 1
                log.warning("Retrying %s (attempt %d/%d) — previous outcome: %s",
                            tid, attempt, args.retries + 1, outcome)
                print(f"  Retrying {tid} (attempt {attempt}/{args.retries + 1})...")
                time.sleep(args.retry_delay)

                # Relaunch the worker.
                tc = next(t for t in test_cases if t["id"] == tid)
                is_generation = "prompt" in tc
                task_input = tc.get("prompt", tc.get("input", ""))
                if is_generation:
                    full_prompt = f"""{system_prompt}

## TASK
{task_input}

IMPORTANT: Do NOT create any files. Output all code and documentation inline as text.
Use STE-Code principles (P1-P14) for all documentation and text you generate.
Apply the synonym table for all word choices.
Produce the requested output first, then a compliance summary table showing which principles you followed."""
                else:
                    full_prompt = f"""{system_prompt}

## TASK
Check the following text for STE-Code compliance. Apply all 14 principles (P1-P14). 
Replace unapproved terms using the synonym table. 
IMPORTANT: Do NOT create any files. Output the corrected text inline.
Produce the corrected text first, then a compliance summary table.

## TEXT TO CORRECT
{task_input}"""

                pid = os.fork()
                if pid == 0:
                    worker_dir = os.path.join(run_dir, f"worker-{tid}")
                    os.makedirs(worker_dir, exist_ok=True)
                    os.chdir(worker_dir)
                    with open(out_file, "w") as outf:
                        os.dup2(outf.fileno(), 1)
                        os.dup2(outf.fileno(), 2)
                    os.execvp("hermes", ["hermes", "-z", full_prompt, "-m", args.model, "--yolo"])
                    os._exit(1)

                _child_pids[tid] = pid
                workers[tid]["pid"] = pid
                workers[tid]["attempt"] = attempt
                progress[tid]["attempt"] = attempt
                progress[tid]["pid"] = pid
                progress[tid]["start_time"] = time.time()
                save_progress()

                # Wait for this individual retry.
                retry_elapsed = 0
                retry_timeout = 120  # per-retry timeout: 2 minutes
                done = False
                while retry_elapsed < retry_timeout:
                    time.sleep(poll_interval)
                    retry_elapsed += poll_interval
                    try:
                        wpid, st = os.waitpid(pid, os.WNOHANG)
                        if wpid != 0:
                            done = True
                            _child_pids.pop(tid, None)
                            break
                    except ChildProcessError:
                        done = True
                        _child_pids.pop(tid, None)
                        break

                if not done:
                    # Retry timed out.
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    _child_pids.pop(tid, None)
                    outcome = WORKER_TIMEOUT
                else:
                    outcome = classify_worker_result(out_file, False)

                progress[tid]["outcome"] = outcome
                progress[tid]["end_time"] = time.time()
                save_progress()

                if outcome == WORKER_SUCCESS:
                    print(f"  {tid} retry succeeded on attempt {attempt}")
                    break

            # Final outcome after all retries.
            progress[tid]["outcome"] = outcome
            save_progress()

    print()
    print("=== All workers finished. Scoring... ===")
    print()

    # -----------------------------------------------------------------------
    # Phase 3: Score each output.
    # -----------------------------------------------------------------------
    results = []
    category_stats = defaultdict(lambda: {"passed": 0, "failed": 0, "scores": [], "latencies": []})

    for tc in test_cases:
        tid = tc["id"]
        cat = tc["category"]
        is_generation = "prompt" in tc
        task_text = tc.get("prompt", tc.get("input", ""))
        out_file = workers[tid]["out_file"]

        # Read output.
        try:
            with open(out_file) as f:
                output = f.read()
        except FileNotFoundError:
            output = "OUTPUT_FILE_MISSING"

        latency_ms = int((time.time() - workers[tid]["start_time"]) * 1000)

        # Extract corrected text.
        corrected = extract_corrected_text(output)
        corrected_lower = corrected.lower()

        # Check principles.
        satisfied, missed = check_principles(output, tc["expected_principles"])

        # Check forbidden keywords (only in corrected text, not compliance summary).
        forbidden = tc.get("forbidden_keywords", [])
        forbidden_found = check_keywords(corrected_lower, forbidden)

        # Check expected keywords in corrected text.
        expected_kw = tc.get("expected_keywords", [])
        expected_found = check_keywords(corrected_lower, expected_kw)

        # Check required patterns (for generation tests).
        required_patterns = tc.get("required_patterns", [])
        patterns_found = []
        patterns_missed = []
        for pat in required_patterns:
            if re.search(pat, output, re.IGNORECASE | re.DOTALL):
                patterns_found.append(pat)
            else:
                patterns_missed.append(pat)

        # Calculate correctness (single call with all params).
        correctness = calc_correctness(tc["expected_principles"], satisfied, forbidden_found, len(forbidden),
                                       expected_found, len(expected_kw))

        # Penalty for missing required patterns.
        if required_patterns:
            pattern_penalty = 0.2 * len(patterns_missed) / len(required_patterns)
            correctness = round(max(0.0, correctness - pattern_penalty), 2)

        # Token estimation (full output, not just corrected text).
        token_input = len(task_text) // 4
        token_output = len(output) // 4  # Full output, not truncated corrected text.

        # Compute actual diff ratio (input vs corrected output).
        if corrected and task_text:
            diff_ratio = difflib.SequenceMatcher(None, task_text.lower(), corrected.lower()).ratio()
            diff_ratio = round(1.0 - diff_ratio, 2)  # 0 = identical, 1 = completely different
        else:
            diff_ratio = 0.0

        # Detect truncated/stub output (worker timeout or crash).
        is_truncated = len(output) < 20 or output.startswith("HERMES_ERROR")

        # Pass/fail threshold.
        # Threshold 0.7 rationale: calibrated against 59-test human review.
        # At 0.6, borderline outputs pass that humans flag as needing improvement.
        # At 0.8, well-scoring outputs that miss one principle fail incorrectly.
        # 0.7 strikes the best balance between precision and recall.
        passed = correctness >= 0.7

        # Notes.
        notes_parts = []
        if missed:
            notes_parts.append(f"Missed: {', '.join(missed)}")
        if forbidden_found:
            notes_parts.append(f"Forbidden found: {', '.join(forbidden_found)}")
        if expected_found:
            notes_parts.append(f"Keywords OK: {len(expected_found)}/{len(expected_kw)}")
        if patterns_missed:
            notes_parts.append(f"Patterns missed: {', '.join(patterns_missed)}")
        # Include retry info.
        worker_attempts = workers[tid].get("attempt", 1)
        if worker_attempts > 1:
            notes_parts.append(f"Retries: {worker_attempts - 1}")

        result = {
            "test_id": tid,
            "category": cat,
            "description": tc.get("description", ""),
            "input": task_text,
            "test_type": "generation" if is_generation else "correction",
            "output": corrected,
            "compliance_summary": extract_compliance_section(output),
            "expected_principles_satisfied": satisfied,
            "expected_principles_missed": missed,
            "forbidden_keywords_found": forbidden_found,
            "expected_keywords_found": expected_found,
            "correctness_score": correctness,
            "latency_ms": latency_ms,
            "token_count_input": token_input,
            "token_count_output": token_output,
            "diff_ratio": diff_ratio,
            "truncated": is_truncated,
            "passed": passed,
            "notes": "; ".join(notes_parts) if notes_parts else "All checks passed",
            "difficulty": tc.get("difficulty", "unknown"),
            "worker_outcome": progress.get(tid, {}).get("outcome", "UNKNOWN"),
            "worker_attempts": worker_attempts,
        }
        results.append(result)

        # Track category stats.
        if passed:
            category_stats[cat]["passed"] += 1
        else:
            category_stats[cat]["failed"] += 1
        category_stats[cat]["scores"].append(correctness)
        category_stats[cat]["latencies"].append(latency_ms)

    # -----------------------------------------------------------------------
    # Phase 4: Aggregate.
    # -----------------------------------------------------------------------
    passed_count = sum(1 for r in results if r["passed"])
    failed_count = len(results) - passed_count

    scores = [r["correctness_score"] for r in results]
    latencies = [r["latency_ms"] for r in results]
    tokens_in = [r["token_count_input"] for r in results]
    tokens_out = [r["token_count_output"] for r in results]

    # Worker outcome summary.
    outcome_counts = defaultdict(int)
    for r in results:
        outcome_counts[r["worker_outcome"]] += 1

    aggregate = {
        "benchmark_id": "ste-code-v1.1.0",
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "model": args.model,
        "total_tests": len(results),
        "passed": passed_count,
        "failed": failed_count,
        "pass_rate_pct": round(passed_count / len(results) * 100, 1),
        "aggregates": {
            "avg_correctness": round(sum(scores) / len(scores), 3),
            "min_correctness": min(scores),
            "max_correctness": max(scores),
            "avg_latency_ms": round(sum(latencies) / len(latencies)),
            "min_latency_ms": min(latencies),
            "max_latency_ms": max(latencies),
            "avg_token_input": round(sum(tokens_in) / len(tokens_in)),
            "avg_token_output": round(sum(tokens_out) / len(tokens_out)),
            "total_tokens_input": sum(tokens_in),
            "total_tokens_output": sum(tokens_out),
        },
        "worker_outcomes": dict(outcome_counts),
        "retries_total": sum(r["worker_attempts"] for r in results) - len(results),
        "by_category": {},
        "by_difficulty": {},
        "failures": [r for r in results if not r["passed"]],
        "recommendations": [],
    }

    # By category.
    for cat in sorted(category_stats.keys()):
        s = category_stats[cat]
        aggregate["by_category"][cat] = {
            "passed": s["passed"],
            "failed": s["failed"],
            "total": s["passed"] + s["failed"],
            "avg_correctness": round(sum(s["scores"]) / len(s["scores"]), 3),
            "avg_latency_ms": round(sum(s["latencies"]) / len(s["latencies"])),
        }

    # By difficulty.
    diff_stats = defaultdict(lambda: {"passed": 0, "failed": 0, "scores": []})
    for r in results:
        d = r["difficulty"]
        if r["passed"]:
            diff_stats[d]["passed"] += 1
        else:
            diff_stats[d]["failed"] += 1
        diff_stats[d]["scores"].append(r["correctness_score"])

    for diff in ["easy", "medium", "hard"]:
        if diff in diff_stats:
            s = diff_stats[diff]
            aggregate["by_difficulty"][diff] = {
                "passed": s["passed"],
                "failed": s["failed"],
                "total": s["passed"] + s["failed"],
                "avg_correctness": round(sum(s["scores"]) / len(s["scores"]), 3),
            }

    # Recommendations.
    if aggregate["aggregates"]["avg_correctness"] < 0.7:
        aggregate["recommendations"].append(
            "System prompt needs improvement — avg correctness below 0.7"
        )
    if aggregate["aggregates"]["avg_latency_ms"] > 5000:
        aggregate["recommendations"].append(
            "Latency above 5s average — consider flash model for simple cases"
        )
    for cat, data in aggregate["by_category"].items():
        if data["avg_correctness"] < 0.6:
            aggregate["recommendations"].append(
                f"Category '{cat}' underperforming (avg {data['avg_correctness']}) — review test design or prompt coverage"
            )
    # New: retry recommendations.
    retry_count = aggregate["retries_total"]
    if retry_count > len(results) * 0.3:
        aggregate["recommendations"].append(
            f"High retry rate ({retry_count} retries across {len(results)} tests) — check API reliability or increase timeout"
        )
    # New: outcome-based recommendations.
    timed_out_count = outcome_counts.get(WORKER_TIMEOUT, 0)
    if timed_out_count > len(results) * 0.1:
        aggregate["recommendations"].append(
            f"{timed_out_count} workers timed out — increase --timeout or reduce --max-workers to avoid API congestion"
        )

    # Write results.
    agg_file = os.path.join(run_dir, "aggregate-results.json")
    with open(agg_file, "w") as f:
        json.dump(aggregate, f, indent=2)

    details_file = os.path.join(run_dir, "per-test-results.json")
    with open(details_file, "w") as f:
        json.dump(results, f, indent=2)

    # Final progress save.
    save_progress()

    # -----------------------------------------------------------------------
    # Phase 5: Print report.
    # -----------------------------------------------------------------------
    print()
    print("=" * 70)
    print("  STE-CODE BENCHMARK RESULTS")
    print("=" * 70)
    print(f"  Model:       {args.model}")
    print(f"  Timestamp:   {aggregate['timestamp']}")
    print(f"  Total:       {aggregate['total_tests']} tests")
    print(f"  Passed:      {aggregate['passed']} ({aggregate['pass_rate_pct']}%)")
    print(f"  Failed:      {aggregate['failed']}")
    print(f"  Retries:     {aggregate['retries_total']}")
    print()
    print(f"  Worker outcomes:")
    for outcome, count in sorted(aggregate["worker_outcomes"].items()):
        print(f"    {outcome:<10} {count}")
    print()
    print(f"  Averages:")
    print(f"    Correctness:  {aggregate['aggregates']['avg_correctness']:.3f}  (range: {aggregate['aggregates']['min_correctness']:.2f}–{aggregate['aggregates']['max_correctness']:.2f})")
    print(f"    Latency:      {aggregate['aggregates']['avg_latency_ms']}ms  (range: {aggregate['aggregates']['min_latency_ms']}–{aggregate['aggregates']['max_latency_ms']}ms)")
    print(f"    Tokens in:    {aggregate['aggregates']['avg_token_input']} avg  ({aggregate['aggregates']['total_tokens_input']} total)")
    print(f"    Tokens out:   {aggregate['aggregates']['avg_token_output']} avg  ({aggregate['aggregates']['total_tokens_output']} total)")
    print()

    # Category breakdown table.
    print("-" * 70)
    print(f"  {'Category':<15} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Rate':>7} {'Avg Score':>10} {'Avg Lat':>8}")
    print("-" * 70)
    for cat in sorted(aggregate["by_category"].keys()):
        d = aggregate["by_category"][cat]
        rate = round(d["passed"] / d["total"] * 100) if d["total"] else 0
        print(f"  {cat:<15} {d['total']:>6} {d['passed']:>7} {d['failed']:>7} {rate:>6}% {d['avg_correctness']:>10.3f} {d['avg_latency_ms']:>7}ms")
    print("-" * 70)

    # Difficulty breakdown.
    print()
    print(f"  {'Difficulty':<12} {'Tests':>6} {'Passed':>7} {'Failed':>7} {'Avg Score':>10}")
    print("-" * 45)
    for diff in ["easy", "medium", "hard"]:
        if diff in aggregate["by_difficulty"]:
            d = aggregate["by_difficulty"][diff]
            print(f"  {diff:<12} {d['total']:>6} {d['passed']:>7} {d['failed']:>7} {d['avg_correctness']:>10.3f}")

    # Per-test detail.
    print()
    print("-" * 70)
    print(f"  {'ID':<12} {'Category':<12} {'Score':>6} {'Latency':>8} {'Result':>7}  Notes")
    print("-" * 70)
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  {r['test_id']:<12} {r['category']:<12} {r['correctness_score']:>6.2f} {r['latency_ms']:>7}ms {status:>7}  {r['notes'][:60]}")
    print("-" * 70)

    # Failures detail.
    failures = [r for r in results if not r["passed"]]
    if failures:
        print()
        print(f"=== FAILURES ({len(failures)}) ===")
        for r in failures:
            print(f"  {r['test_id']} ({r['category']}, {r['difficulty']}): score={r['correctness_score']}")
            print(f"    Input:  {r['input'][:80]}...")
            print(f"    Output: {r['output'][:80]}...")
            print(f"    Missed principles: {r['expected_principles_missed']}")
            print(f"    Forbidden found:   {r['forbidden_keywords_found']}")
            print()

    # Recommendations.
    if aggregate["recommendations"]:
        print("=== RECOMMENDATIONS ===")
        for rec in aggregate["recommendations"]:
            print(f"  • {rec}")

    print()
    print(f"Full results: {run_dir}/")
    print(f"Aggregate:    {agg_file}")
    print(f"Per-test:     {details_file}")
    print(f"Progress:     {progress_file}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
