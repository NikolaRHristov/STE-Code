#!/usr/bin/env python3
"""
STE-Code Extraction Orchestrator — launches hermes -z workers for spec page extraction.

Follows existing project patterns:
- Uses _import_runner.py to get run_agent/launch_agent from agent-runner.py
- Telemetry logging like telemetry-worker.py
- Path resolution like launch-worker.sh (PROJECT from __file__)
- Batch processing with git commits like extract_batch scripts

Usage:
  python3 .agents/tools/extract_batch.py [start_batch] [num_batches]

The orchestrator launches 3 workers per batch (W001-W003, W004-W006, etc.),
each extracting 4 consecutive pages from spec/issue-09-2025/page-dir/.
Workers use hermes -z with --yolo to read spec pages and write extraction output.
Git commits after each verified batch.

Workers read spec pages using their read_file tool and write output via write_file.
No content is embedded in the prompt — the model reads files directly.
"""

import os
import sys
import subprocess
import time
import re
import json
from pathlib import Path
from datetime import datetime, timezone

# ── Resolve project root from script location ──────────────────────────
PROJECT = Path(__file__).resolve().parent.parent.parent
PAGE_DIR = PROJECT / "spec" / "issue-09-2025" / "page-dir"
EXTRACTED_DIR = PROJECT / "ste-code" / "extracted"
MANIFEST_PATH = PAGE_DIR / "MANIFEST.md"
PROGRESS_PATH = PROJECT / ".agents" / "state" / "PROGRESS.md"
TELEMETRY_DIR = PROJECT / ".agents" / "telemetry"
LOG_DIR = PROJECT / ".agents" / "tmp" / "extraction-logs"
FEEDBACK_PATH = PROJECT / ".agents" / "feedback" / "exchange.md"

MODEL = "poolside/laguna-s-2.1:free"
MAX_WORKERS = 109
PAGES_PER_WORKER = 4
WORKERS_PER_BATCH = 3
TOTAL_PAGES = 434

# ── Import agent runner (standard project pattern) ──────────────────────
exec(open(PROJECT / ".agents" / "tools" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command


def parse_manifest():
    """Parse MANIFEST.md: position (1-434) -> (page_id, filename)"""
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
    """Get (start_pos, end_pos) for a worker number"""
    start_pos = (worker_num - 1) * PAGES_PER_WORKER + 1
    end_pos = min(worker_num * PAGES_PER_WORKER, TOTAL_PAGES)
    return start_pos, end_pos


def build_prompt(worker_num, start_pos, end_pos, mapping):
    """Build hermes -z prompt for extraction.

    Tells the agent to read spec page files and write the extraction output.
    No content is embedded in the prompt — the agent reads files via its tools.
    """
    pages = []
    for pos in range(start_pos, end_pos + 1):
        if pos in mapping:
            page_id, filename = mapping[pos]
            pages.append((pos, page_id, filename))

    file_refs = "\n".join(
        f"- Page {pos} ({page_id}): spec/issue-09-2025/page-dir/{filename}"
        for pos, page_id, filename in pages
    )

    output_path = f"ste-code/extracted/w{worker_num:03d}-p{start_pos}-{end_pos}.md"

    prompt = f"""Extract ALL content from these {len(pages)} spec pages and write to a markdown file.

STEPS:
1. Read each of these files:
{file_refs}

2. Extract every word, table, list, and example verbatim into:
   {output_path}

3. Start the file with `# Page {start_pos} of 434`
4. For each page boundary, add `# Page N of 434` heading
5. Output ONLY raw markdown — no commentary, no preamble, no summaries
6. Preserve all formatting exactly
7. If a table spans pages, add `<!-- TABLE CONTINUES ON NEXT PAGE -->`

Do not add "This page describes" or "In summary" or any meta-commentary.
Just read the files and write the output. Use write_file to save."""

    return prompt


def verify_output(worker_num, start_pos, end_pos):
    """Run quality gates on extracted file. Returns (ok, message)."""
    output_file = EXTRACTED_DIR / f"w{worker_num:03d}-p{start_pos}-{end_pos}.md"

    if not output_file.exists():
        return False, "File does not exist"

    try:
        content = output_file.read_text(encoding="utf-8")
    except Exception as e:
        return False, f"Read error: {e}"

    size = output_file.stat().st_size
    lines = len(content.splitlines())

    # Strip TUI banner lines for analysis
    content_lines = [l for l in content.splitlines()
                     if not (l.startswith("╭") or l.startswith("╰") or l.startswith("│")
                             or l.startswith("\x1b[") or "Hermes Agent v" in l
                             or "Available Tools" in l or "Welcome to" in l
                             or "The boulder" in l or "Session:" in l)]

    if not content_lines:
        return False, "Only banner output — no extraction content"

    # Gate 2: No commentary in last 5 content lines
    bad_patterns = [
        "i've written", "the file contains", "output file:",
        "here is", "here's", "saved to", "i saved",
        "this page describes", "in summary", "the key point",
        "let me check", "i will now extract", "wait, actually",
        "shutting down", "the boulder",
    ]
    last_5 = "\n".join(content_lines[-5:]).lower()
    for pattern in bad_patterns:
        if pattern in last_5:
            return False, f"Commentary: '{pattern}' in last lines"

    # Gate 2: Page header
    first_content = content_lines[0].strip()
    expected = f"# Page {start_pos} of 434"
    if expected not in first_content:
        return False, f"Header wrong: expected '{expected}', got '{first_content[:80]}'"

    # Gate 1: Size
    is_last = (worker_num == MAX_WORKERS)
    min_size = 200 if is_last else 600

    if size < min_size:
        return False, f"Size {size}B below {min_size}B"

    return True, f"OK - {size}B, {lines} lines"


def run_worker_telemetry(worker_num, start_pos, end_pos, mapping, attempt=1):
    """Run a single extraction worker with telemetry logging.

    Uses run_agent() from agent-runner.py, which calls hermes-oneshot-wrapper.py
    via the Hermes Python API (no TUI banner issues).
    """
    output_file = EXTRACTED_DIR / f"w{worker_num:03d}-p{start_pos}-{end_pos}.md"

    # Clean up any previous failed attempt
    if output_file.exists():
        ok, msg = verify_output(worker_num, start_pos, end_pos)
        if ok:
            return True, msg, True  # already extracted
        output_file.unlink()

    prompt = build_prompt(worker_num, start_pos, end_pos, mapping)

    # Clean up old prompt files
    for old_prompt in Path("/tmp").glob(f"w{worker_num:03d}-p*.txt"):
        old_prompt.unlink(missing_ok=True)

    # Telemetry
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    telemetry_path = TELEMETRY_DIR / f"w{worker_num:03d}-{timestamp}.json"

    start_time = time.time()
    print(f"  W{worker_num:03d} (attempt {attempt}): Extracting {start_pos}-{end_pos}...", flush=True)

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
        # Use run_agent from agent-runner.py — calls hermes-oneshot-wrapper.py
        result = run_agent(
            prompt,
            agent="hermes",
            model=MODEL,
            cwd=PROJECT,
            timeout=600,
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

        # Check stdout for error patterns
        if result.stdout:
            stdout_lower = result.stdout.lower()
            if "error" in stdout_lower:
                errors = [l for l in result.stdout.split("\n")
                          if "error" in l.lower() or "traceback" in l.lower()]
                if errors:
                    telemetry["errors"].extend(errors[:5])

        # Check if output file was created
        if output_file.exists():
            telemetry["output_exists"] = True
            telemetry["output_size_bytes"] = output_file.stat().st_size
            telemetry["output_lines"] = len(output_file.read_text(encoding="utf-8").splitlines())
            ok, msg = verify_output(worker_num, start_pos, end_pos)
            telemetry["verification_status"] = "PASS" if ok else "FAIL"
            telemetry["verification_message"] = msg

            if ok:
                print(f"  W{worker_num:03d}: [PASS] {msg} ({duration:.1f}s)", flush=True)
                _save_telemetry(telemetry_path, telemetry)
                return True, msg, False
            else:
                print(f"  W{worker_num:03d}: [FAIL] {msg} — retrying", flush=True)
                # Save bad output for debugging
                log_file = LOG_DIR / f"w{worker_num:03d}-bad.txt"
                LOG_DIR.mkdir(parents=True, exist_ok=True)
                log_file.write_text(output_file.read_text(encoding="utf-8")[:500], encoding="utf-8")
                output_file.unlink()
        else:
            print(f"  W{worker_num:03d}: [FAIL] No output file created — retrying", flush=True)
            telemetry["errors"].append("Output file not created by agent")
            # Save stdout for debugging
            if result.stdout:
                LOG_DIR.mkdir(parents=True, exist_ok=True)
                debug_file = LOG_DIR / f"w{worker_num:03d}-stdout.txt"
                debug_file.write_text(result.stdout[:1000], encoding="utf-8")

    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()
        telemetry["errors"].append(f"TIMEOUT after {duration:.0f}s")
        telemetry["exit_code"] = -1
        print(f"  W{worker_num:03d}: [TIMEOUT] after {duration:.0f}s — retrying", flush=True)

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
    """Save telemetry JSON"""
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def process_batch(batch_num, start_worker, mapping):
    """Process a batch of up to 3 workers."""
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
    print(f"Batch {batch_num:02d} — {', '.join(worker_ids)} (pages {batch_start}-{batch_end})", flush=True)
    print(f"{'='*60}", flush=True)

    # Process workers sequentially (shared model backend)
    results = []
    for worker_num, start_pos, end_pos in workers:
        ok = False
        msg = ""
        skipped = False
        for attempt in range(1, 4):
            ok, msg, skipped = run_worker_telemetry(
                worker_num, start_pos, end_pos, mapping, attempt
            )
            if ok:
                break

        results.append((worker_num, start_pos, end_pos, ok))

    all_passed = all(r[3] for r in results)
    passed = sum(1 for r in results if r[3])

    # Commit
    for worker_num, start_pos, end_pos, ok in results:
        if ok:
            f = EXTRACTED_DIR / f"w{worker_num:03d}-p{start_pos}-{end_pos}.md"
            subprocess.run(["git", "add", str(f.relative_to(PROJECT))],
                         capture_output=True, text=True, cwd=str(PROJECT))

    status_str = "PASS" if all_passed else f"PARTIAL ({passed}/{len(workers)})"
    commit_msg = f"Batch {batch_num:02d} - {status_str} - Workers {', '.join(worker_ids)} (pages {batch_start}-{batch_end})"
    result = subprocess.run(["git", "commit", "-m", commit_msg],
                            capture_output=True, text=True, cwd=str(PROJECT))
    if result.returncode == 0:
        print(f"  ✓ Committed: {commit_msg}", flush=True)
    else:
        print(f"  ✗ Commit failed: {result.stderr[:200]}", flush=True)

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

    PROGRESS_PATH.write_text("\n".join(lines), encoding="utf-8")


def _write_feedback(batch_num, issue):
    """Write failure info to feedback exchange log."""
    FEEDBACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not FEEDBACK_PATH.exists():
        FEEDBACK_PATH.write_text("# Feedback Exchange Log\n\n", encoding="utf-8")

    timestamp = datetime.now(timezone.utc).isoformat()
    entry = f"\n## Batch {batch_num:02d} - {timestamp}\n"
    entry += f"- **Issue:** {issue}\n"
    entry += f"- **Action:** Check telemetry logs in .agents/telemetry/\n\n"

    content = FEEDBACK_PATH.read_text(encoding="utf-8")
    content += entry
    FEEDBACK_PATH.write_text(content, encoding="utf-8")


def main():
    start_batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    num_batches = int(sys.argv[2]) if len(sys.argv) > 2 else 37

    print(f"STE-Code Batch Extraction Pipeline", flush=True)
    print(f"Model: {MODEL}", flush=True)
    print(f"Starting batch: {start_batch}, batches: {num_batches}", flush=True)
    print(f"Project: {PROJECT}", flush=True)

    mapping = parse_manifest()
    print(f"Manifest: {len(mapping)} page mappings", flush=True)

    EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    TELEMETRY_DIR.mkdir(parents=True, exist_ok=True)

    # Check existing
    existing = sorted(EXTRACTED_DIR.glob("w*.md"))
    if existing:
        last_w = max(int(f.stem.split("-")[0][1:]) for f in existing)
        print(f"  Existing last: W{last_w:03d}", flush=True)

    for batch_num in range(start_batch, min(start_batch + num_batches, 38)):
        start_worker = (batch_num - 1) * WORKERS_PER_BATCH + 1
        if start_worker > MAX_WORKERS:
            print(f"\nAll {MAX_WORKERS} workers complete!", flush=True)
            break

        process_batch(batch_num, start_worker, mapping)

    final_count = len(list(EXTRACTED_DIR.glob("w*.md")))
    print(f"\n{'='*60}", flush=True)
    print(f"Done. Files in extracted/: {final_count}", flush=True)
    print(f"{'='*60}", flush=True)


if __name__ == "__main__":
    main()
