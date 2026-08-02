#!/usr/bin/env python3
"""
STE-Code Extraction Orchestrator — batch pipeline v2.

Launches hermes -z workers (via the oneshot wrapper) to extract spec pages
from spec/issue-09-2025/page-dir/ into ste-code/extracted/.

Pipeline:
  1. Read MANIFEST.md → position→(page_id, filename) mapping
  2. For each worker (109 total, 4 pages each), build a prompt that tells the
     agent to read each spec page file and write a combined markdown file.
  3. Run via run_agent() → hermes-oneshot-wrapper.py → AIAgent (no TUI)
  4. Verify output (size, page headers only — no commentary substring gating)
  5. Retry up to 2 times on failure (only if output file is missing/timed out)
  6. Commit each passed batch via git
  7. Update PROGRESS.md
  8. Checkpoint state after each worker — crash-safe resume via --resume flag

Usage:
  python3 .agents/tools/extraction/extract_batch.py [start_batch] [num_batches] [--resume]

Fast failover:
  The extractor writes a checkpoint file (.agents/state/extraction-checkpoint.json)
  after each worker completes. If the session is killed (SIGTERM/SIGINT/crash),
  the next run can resume with --resume to skip already-completed workers.
  Signal handlers (SIGTERM, SIGINT) also save the checkpoint on exit.
  The oneshot wrapper includes a health probe watchdog that self-terminates
  if the API is unresponsive for HERMES_HEALTH_PROBE_TIMEOUT (default 600s).

Environment:
  Read .agents/tools/.env if present for MODEL, MAX_WORKERS, etc.
"""

import os
import sys
import time
import re
import json
import signal
import subprocess
import atexit
from pathlib import Path
from datetime import datetime, timezone

# ── Resolve project root from script location (no hardcoded paths) ──────────
# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_io import write_text, mkdir, write_json  # noqa: E402
from ste_time import run_stamp  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402
CFG = _load_config(__file__)
PAGE_DIR = PROJECT / "spec" / "issue-09-2025" / "page-dir"
EXTRACTED_DIR = PROJECT / "ste-code" / "extracted"
MANIFEST_PATH = PAGE_DIR / "MANIFEST.md"
PROGRESS_PATH = PROJECT / ".agents" / "state" / "PROGRESS.md"
TELEMETRY_DIR = PROJECT / ".agents" / "telemetry"
LOG_DIR = PROJECT / ".agents" / "tmp" / "extraction-logs"
FEEDBACK_PATH = PROJECT / ".agents" / "feedback" / "exchange.md"

# ── Load .env (optional) ────────────────────────────────────────────────────
_env_path = Path(__file__).resolve().parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())

# ── Config ────────────────────────────────────────────────────────────────────
MODEL = CFG.model
MAX_WORKERS = int(os.environ.get("STE_MAX_WORKERS", "109"))
PAGES_PER_WORKER = int(os.environ.get("STE_PAGES_PER_WORKER", "4"))
WORKERS_PER_BATCH = int(os.environ.get("STE_WORKERS_PER_BATCH", "3"))
TOTAL_PAGES = int(os.environ.get("STE_TOTAL_PAGES", "434"))
MAX_ATTEMPTS = 2
TIMEOUT_SECONDS = 300

# ── State / checkpoint paths ──────────────────────────────────────────────────
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "extraction-checkpoint.json"

# ── Import agent runner (standard project pattern) ────────────────────────────
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

# ── Skill embedding: inject the extraction SKILL.md into every worker prompt ──
# The oneshot wrapper sub-agents do not auto-load the STE-Code profile skills,
# so we embed the authoritative skill text directly. This keeps the prompt and
# the skill in lockstep (edit the SKILL.md, not the baked prompt).

# Shared template loader ({{placeholder}} syntax — see lib/templater.py).
import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import lib_import, render_template

skill_prompt = lib_import("skill_prompt")
_EXTRACTION_PROMPT_PATH = PROJECT / ".agents" / "tools" / "prompts" / "extraction-worker.md"


def parse_manifest():
    """Parse MANIFEST.md: position (1-434) → (page_id, filename)."""
    mapping = {}
    with open(MANIFEST_PATH) as f:
        for line in f:
            line = line.strip()
            if line.startswith("| ") and "page-" in line:
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 5 and parts[1].isdigit():
                    pos = int(parts[1])
                    page_id = parts[2]
                    filename = parts[3]
                    mapping[pos] = (page_id, filename)
    return mapping


def worker_page_range(worker_num):
    """Get (start_pos, end_pos) for a worker number."""
    start_pos = (worker_num - 1) * PAGES_PER_WORKER + 1
    end_pos = min(worker_num * PAGES_PER_WORKER, TOTAL_PAGES)
    return start_pos, end_pos


def build_prompt(worker_num, start_pos, end_pos, mapping):
    """Build the hermes -z prompt.

    The agent reads spec page files via its read_file tool and writes the
    extraction output via write_file. No content is embedded in the prompt.
    The prompt template is read from .agents/prompts/extraction-worker.md
    so it can be edited on-the-fly without modifying this script.
    """
    pages = []
    for pos in range(start_pos, end_pos + 1):
        if pos in mapping:
            page_id, filename = mapping[pos]
            pages.append((pos, page_id, filename))

    file_refs = "\n".join(
        f"  {pos}. {page_id} → spec/issue-09-2025/page-dir/{filename}"
        for pos, page_id, filename in pages
    )

    # Full absolute path for write_file
    output_path = str(EXTRACTED_DIR / f"w{worker_num:03d}-p{start_pos}-{end_pos}.md")

    # Load prompt template from .md file for dynamic editing.
    # The template uses {{placeholder}} syntax (see lib/templater.py) and now
    # lives under prompts/ as extraction-worker.md — edit it to change wording
    # without touching this script.

    prompt = render_template(
        _EXTRACTION_PROMPT_PATH,
        num_pages=len(pages),
        file_refs=file_refs,
        start_pos=start_pos,
        pages_first_id=pages[0][1] if pages else "",
        output_path=output_path,
    )

    # Embed the authoritative extraction skill so the worker honors the pipeline
    # rules (verbatim extraction, R1-R6, quality gates) in lockstep with the
    # skill definition. Edit the SKILL.md to change behavior, not this script.
    prompt += skill_prompt.skill_section("extraction")

    return prompt, output_path


def verify_output(worker_num, start_pos, end_pos, output_path):
    """Run quality gates on extracted file. Returns (ok, message)."""
    output_file = Path(output_path)

    if not output_file.exists():
        return False, "File does not exist"

    try:
        content = output_file.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Read error: {e}"

    size = output_file.stat().st_size
    lines = content.splitlines()

    # Gate 1: Size — must have meaningful content
    is_last = (worker_num == MAX_WORKERS)
    min_size = 200 if is_last else 600
    if size < min_size:
        return False, f"Size {size}B below {min_size}B minimum"

    # Gate 2: First page header
    first_content = lines[0].strip() if lines else ""
    expected = f"# Page {start_pos} of 434"
    if expected not in first_content:
        return False, f"Header wrong: expected '{expected}', got '{first_content[:80]}'"

    # Gate 3: All expected page headers present
    for pos in range(start_pos, end_pos + 1):
        expected_header = f"# Page {pos} of 434"
        if expected_header not in content:
            return False, f"Missing header: {expected_header}"

    return True, f"OK — {size}B, {len(lines)} lines"


def run_worker(worker_num, start_pos, end_pos, mapping, attempt=1):
    """Run a single extraction worker with telemetry logging."""
    # Fast-failover: skip workers that already passed in a previous session.
    ckpt = _checkpoint.get(str(worker_num))
    if ckpt and ckpt.get("passed"):
        print(f"  W{worker_num:03d}: ✓ Already extracted (checkpoint skip)", flush=True)
        return True, f"Checkpoint skip — {ckpt.get('output_size', '?')}B", True

    prompt, output_path = build_prompt(worker_num, start_pos, end_pos, mapping)

    # Clean up any previous failed attempt for this worker
    output_file = Path(output_path)
    if output_file.exists():
        ok, msg = verify_output(worker_num, start_pos, end_pos, output_path)
        if ok:
            # Mark in checkpoint so future sessions skip it.
            _checkpoint[str(worker_num)] = {
                "passed": True, "attempt": 0,
                "output_size": output_file.stat().st_size,
            }
            _save_checkpoint(_checkpoint)
            return True, msg, True  # already extracted, skip
        output_file.unlink()

    mkdir(TELEMETRY_DIR)
    mkdir(LOG_DIR)
    timestamp = run_stamp()
    telemetry_path = TELEMETRY_DIR / f"w{worker_num:03d}-{timestamp}.json"

    start_time = time.time()
    print(f"  W{worker_num:03d} (attempt {attempt}): Extracting "
          f"{start_pos}-{end_pos}...", flush=True)

    telemetry = {
        "worker_id": f"W{worker_num:03d}",
        "batch": (worker_num - 1) // WORKERS_PER_BATCH + 1,
        "page_range": f"{start_pos}-{end_pos}",
        "model": MODEL,
        "attempt": attempt,
        "prompt_size_bytes": len(prompt),
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": None,
        "duration_seconds": None,
        "exit_code": None,
        "output_file": str(output_file.relative_to(PROJECT)),
        "output_exists": False,
        "output_size_bytes": 0,
        "output_lines": 0,
        "verification_status": None,
        "verification_message": None,
        "errors": [],
        "stderr_snippet": "",
    }

    try:
        result = run_agent(
            prompt,
            agent="hermes",
            model=MODEL,
            cwd=str(PROJECT),
            timeout=TIMEOUT_SECONDS,
        )

        duration = time.time() - start_time
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()
        telemetry["exit_code"] = result.returncode

        if result.stderr:
            telemetry["stderr_snippet"] = result.stderr[:500]
            stderr_lower = result.stderr.lower()
            if "error" in stderr_lower or "timeout" in stderr_lower:
                telemetry["errors"].append(result.stderr[:200])

        if result.stdout:
            stdout_lower = result.stdout.lower()
            if "http 400" in stdout_lower or "error" in stdout_lower:
                errors = [l for l in result.stdout.split("\n")
                           if "error" in l.lower() or "traceback" in l.lower()
                           or "http 400" in l.lower()]
                if errors:
                    telemetry["errors"].extend(errors[:5])

        # Check if output file was created
        if output_file.exists():
            telemetry["output_exists"] = True
            telemetry["output_size_bytes"] = output_file.stat().st_size
            telemetry["output_lines"] = len(
                output_file.read_text(encoding="utf-8").splitlines()
            )
            telemetry["verification_status"] = "PASS"
            telemetry["verification_message"] = f"OK — {telemetry['output_size_bytes']}B, {telemetry['output_lines']} lines"
            print(f"  W{worker_num:03d}: [PASS] {telemetry['verification_message']} ({duration:.1f}s)",
                  flush=True)
            _save_telemetry(telemetry_path, telemetry)
            # Checkpoint: mark this worker as passed.
            _checkpoint[str(worker_num)] = {
                "passed": True, "attempt": attempt,
                "output_size": telemetry["output_size_bytes"],
            }
            _save_checkpoint(_checkpoint)
            return True, telemetry["verification_message"], False
        else:
            print(f"  W{worker_num:03d}: [FAIL] No output file — retrying",
                  flush=True)
            telemetry["errors"].append("Output file not created by agent")
            # Save stdout for debugging
            if result.stdout:
                debug_file = LOG_DIR / f"w{worker_num:03d}-stdout.txt"
                write_text(debug_file, result.stdout[:1000])

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()
        telemetry["errors"].append(f"TIMEOUT after {duration:.0f}s")
        telemetry["exit_code"] = -1
        print(f"  W{worker_num:03d}: [TIMEOUT] after {duration:.0f}s — retrying",
              flush=True)

    except Exception as e:
        duration = time.time() - start_time
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()
        telemetry["errors"].append(f"EXCEPTION: {e}")
        telemetry["exit_code"] = -2
        print(f"  W{worker_num:03d}: [ERROR] {e}", flush=True)

    _save_telemetry(telemetry_path, telemetry)
    return False, "Failed", False


def _save_telemetry(path, data):
    """Save telemetry JSON."""
    try:
        write_json(path, data)
    except Exception:
        pass


# ── Checkpoint / fast-failover state ──────────────────────────────────────────

def _load_checkpoint():
    """Load the extraction checkpoint — a dict of worker_num → {"passed": bool, "attempt": int}."""
    if CHECKPOINT_PATH.exists():
        try:
            with open(CHECKPOINT_PATH) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_checkpoint(checkpoint):
    """Atomically write the checkpoint file for crash-safe resume."""
    try:
        write_json(CHECKPOINT_PATH, checkpoint)
    except Exception:
        pass


# Global checkpoint state — updated after each worker completes.
_checkpoint = _load_checkpoint()


def process_batch(batch_num, start_worker, mapping):
    """Process a batch of up to WORKERS_PER_BATCH workers."""
    workers = []
    for i in range(WORKERS_PER_BATCH):
        worker_num = start_worker + i
        if worker_num > MAX_WORKERS:
            break
        start_pos, end_pos = worker_page_range(worker_num)
        workers.append((worker_num, start_pos, end_pos))

    if not workers:
        return True

    batch_start = workers[0][1]
    batch_end = workers[-1][2]
    worker_ids = [f"W{w:03d}" for w, _, _ in workers]

    print(f"\n{'='*60}", flush=True)
    print(f"Batch {batch_num:02d} — {', '.join(worker_ids)} "
          f"(pages {batch_start}-{batch_end})", flush=True)
    print(f"{'='*60}", flush=True)

    # Process workers sequentially (shared model backend)
    results = []
    for worker_num, start_pos, end_pos in workers:
        ok = False
        msg = ""
        skipped = False
        for attempt in range(1, MAX_ATTEMPTS + 1):
            ok, msg, skipped = run_worker(
                worker_num, start_pos, end_pos, mapping, attempt
            )
            if ok:
                break
            # If commentary failed and not the last attempt, retry
            # (the model sometimes adds meta-commentary on retry attempts)

        results.append((worker_num, start_pos, end_pos, ok))

    all_passed = all(r[3] for r in results)
    passed = sum(1 for r in results if r[3])

    # Git commit passed workers
    for worker_num, start_pos, end_pos, ok in results:
        if ok:
            f = EXTRACTED_DIR / f"w{worker_num:03d}-p{start_pos}-{end_pos}.md"
            subprocess.run(
                ["git", "add", str(f.relative_to(PROJECT))],
                capture_output=True, text=True, cwd=str(PROJECT)
            )

    # Collect any passed worker files for this commit
    passed_files = [
        str(EXTRACTED_DIR / f"w{w:03d}-p{s}-{e}.md").replace(str(PROJECT) + "/", "")
        for w, s, e, ok in results if ok
    ]

    status_str = "PASS" if all_passed else f"PARTIAL ({passed}/{len(workers)})"
    commit_msg = (
        f"Batch {batch_num:02d} - {status_str} - "
        f"Workers {', '.join(worker_ids)} (pages {batch_start}-{batch_end})"
    )

    if passed_files:
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg] + passed_files,
            capture_output=True, text=True, cwd=str(PROJECT)
        )
        if result.returncode == 0:
            print(f"  ✓ Committed: {commit_msg}", flush=True)
        else:
            print(f"  ✗ Commit failed: {result.stderr[:200]}", flush=True)
    else:
        print(f"  ✗ No files to commit", flush=True)

    # Update PROGRESS.md
    _update_progress(batch_num, results)

    return all_passed


def _update_progress(batch_num, results):
    """Update PROGRESS.md batch status."""
    if not PROGRESS_PATH.exists():
        return

    content = PROGRESS_PATH.read_text(encoding="utf-8")
    all_ok = all(r[3] for r in results)
    status = "[x]" if all_ok else "[!]"

    worker_nums = [r[0] for r in results]
    start_pos = results[0][1]
    end_pos = results[-1][2]
    w_str = ", ".join([f"W{w:03d}" for w in worker_nums])

    lines = content.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith(f"| {batch_num:02d} |"):
            lines[i] = f"| {batch_num:02d} | {w_str} | {start_pos}-{end_pos} | {status} |"

    write_text(PROGRESS_PATH, "\n".join(lines))


def main():
    # Parse CLI args: start_batch, num_batches, optional --resume
    resume = "--resume" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start_batch = int(args[0]) if len(args) > 0 else 1
    num_batches = int(args[1]) if len(args) > 1 else 37

    print(f"STE-Code Batch Extraction Pipeline v2", flush=True)
    print(f"Model: {MODEL}", flush=True)
    print(f"Batches: {num_batches} (workers {start_batch}-{start_batch + num_batches - 1})", flush=True)
    print(f"Resume: {'yes (from checkpoint)' if resume else 'no'}", flush=True)
    print(f"Project: {PROJECT}", flush=True)

    # Register checkpoint save on exit (crash-safe resume).
    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    mapping = parse_manifest()
    print(f"Manifest: {len(mapping)} page mappings", flush=True)

    mkdir(EXTRACTED_DIR)
    mkdir(LOG_DIR)
    mkdir(TELEMETRY_DIR)

    # Report existing files
    existing = sorted(EXTRACTED_DIR.glob("w*.md"))
    if existing:
        last_w = max(
            int(f.stem.split("-")[0][1:]) for f in existing
            if f.stem.startswith("w") and f.stem[1:].split("-")[0].isdigit()
        )
        print(f"  Existing last: W{last_w:03d} ({len(existing)} files)", flush=True)

    # Report checkpoint status if resuming
    if resume and _checkpoint:
        passed = sum(1 for v in _checkpoint.values() if v.get("passed"))
        print(f"  Checkpoint: {passed} workers already passed", flush=True)

    total_workers = 0
    total_passed = 0
    for batch_num in range(start_batch, min(start_batch + num_batches, 38)):
        start_worker = (batch_num - 1) * WORKERS_PER_BATCH + 1
        if start_worker > MAX_WORKERS:
            print(f"\nAll {MAX_WORKERS} workers complete!", flush=True)
            break

        batch_passed = process_batch(batch_num, start_worker, mapping)
        workers_in_batch = min(WORKERS_PER_BATCH, MAX_WORKERS - start_worker + 1)
        total_workers += workers_in_batch
        total_passed += sum(
            1 for w in range(start_worker, start_worker + workers_in_batch)
            if (EXTRACTED_DIR / f"w{w:03d}-p{(w-1)*4+1}-{min(w*4, TOTAL_PAGES)}.md").exists()
        )

    final_count = len(list(EXTRACTED_DIR.glob("w*.md")))
    print(f"\n{'='*60}", flush=True)
    print(f"Done. Files in extracted/: {final_count}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == "__main__":
    main()
