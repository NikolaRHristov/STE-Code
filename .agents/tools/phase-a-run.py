#!/usr/bin/env python3
"""Phase A orchestrator — canonical: oneshot wrapper + telemetry, 3 per batch.

Pattern from benchmark orchestrator: fork + exec, but uses hermes-oneshot-wrapper.py
(AIAgent directly) instead of hermes -z CLI. Each worker writes its file via write_file tool.

Usage:
  python3 .agents/tools/phase-a-run.py [--batch N] [--dry-run]
"""

import os, sys, re, json, time, glob
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT / ".agents" / "prompts" / "maturity-fixes"
TMP_DIR = PROJECT / ".agents" / "tmp"
TELEMETRY_DIR = PROJECT / ".agents" / "telemetry"
STATE_FILE = PROJECT / ".agents" / "state" / "PHASE-A-PROGRESS.json"
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

CREATIVE_BLOCK = """## CREATIVE LICENSE

You are an expert documentation architect. Go BEYOND the suggested improvements.
Be creative, insightful, and thorough. Add your own edge cases, examples, and
structural improvements. The suggested improvements are a floor, not a ceiling.
Be bold. Be precise. Be creative.

"""

os.makedirs(TMP_DIR, exist_ok=True)
os.makedirs(TELEMETRY_DIR, exist_ok=True)
os.makedirs(STATE_FILE.parent, exist_ok=True)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"done": [], "batches_done": []}


def save_state(state):
    state["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_all_prompts():
    return sorted(PROMPTS_DIR.glob("fix-*.txt"))


def enhance_prompt(prompt_text):
    """Add creative block + write_file tool instruction."""
    m = re.search(r'TARGET FILE:\s*(\S+)', prompt_text)
    target = m.group(1) if m else None
    if not target:
        return None, None

    tool_block = f"""## EXECUTION

Use the `write_file` tool to save the COMPLETE improved file to: {target}

Include ALL original content PLUS your improvements. Do not truncate.
After writing, confirm the file was saved and report line count + additions."""

    enhanced = prompt_text.replace(
        'Do NOT create files. Output the improved file content to stdout only.',
        CREATIVE_BLOCK + tool_block
    )
    return enhanced, target


def launch_worker(worker_id, prompt_text, run_dir):
    """Fork + exec oneshot wrapper. Returns PID."""
    # Write prompt to temp file (oneshot wrapper reads from file)
    prompt_file = run_dir / f"{worker_id}-prompt.txt"
    prompt_file.write_text(prompt_text)

    out_file = run_dir / f"{worker_id}-output.txt"

    pid = os.fork()
    if pid == 0:
        # Child: isolate CWD
        worker_dir = run_dir / f"worker-{worker_id}"
        os.makedirs(worker_dir, exist_ok=True)
        os.chdir(worker_dir)

        # Redirect to output file
        with open(out_file, "w") as outf:
            os.dup2(outf.fileno(), 1)
            os.dup2(outf.fileno(), 2)

        # Find venv python
        venv_python = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
        if not os.path.exists(venv_python):
            venv_python = str(PROJECT / ".hermes/hermes-agent/venv/bin/python3")

        os.execvp(venv_python, [
            venv_python, str(WRAPPER),
            str(prompt_file), "--model", "deepseek-v4-pro"
        ])
        os._exit(1)

    return pid


def verify_worker(worker_id, target_file, out_file):
    """Check if target file was written. Returns (ok, size, lines)."""
    target_path = PROJECT / target_file
    ok = target_path.exists() and target_path.stat().st_size > 500
    size = target_path.stat().st_size if target_path.exists() else 0
    lines = len(target_path.read_text().splitlines()) if target_path.exists() else 0
    return ok, size, lines


def process_batch(batch_num, batch_prompts, state, dry_run=False):
    """Process one batch: launch 3 workers, wait, verify, record telemetry."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = TELEMETRY_DIR / f"phase-a-batch{batch_num:03d}-{timestamp}"
    os.makedirs(run_dir, exist_ok=True)

    workers = {}
    targets = {}

    print(f"\n═══ Batch {batch_num} — {len(batch_prompts)} workers ═══")

    # Phase 1: Prepare prompts and launch
    for pf in batch_prompts:
        wid = pf.stem
        if wid in state["done"]:
            print(f"  {wid}: ✓ already done")
            continue

        prompt_text = pf.read_text()
        enhanced, target = enhance_prompt(prompt_text)
        if not enhanced:
            print(f"  {wid}: ✗ no target in prompt")
            continue

        targets[wid] = target

        if dry_run:
            print(f"  {wid} → {target} ({len(enhanced)} chars) [DRY]")
            continue

        pid = launch_worker(wid, enhanced, run_dir)
        workers[wid] = {"pid": pid, "start": time.time(), "target": target}
        print(f"  {wid} → {target} PID={pid}")

    if dry_run:
        return

    if not workers:
        print("  No workers to launch")
        return

    # Phase 2: Wait for all workers
    print(f"  Waiting for {len(workers)} workers...")
    MAX_WAIT = 600
    elapsed = 0
    pending = set(workers.keys())

    while pending and elapsed < MAX_WAIT:
        time.sleep(3)
        elapsed += 3
        for wid in list(pending):
            pid = workers[wid]["pid"]
            try:
                wpid, status = os.waitpid(pid, os.WNOHANG)
                if wpid != 0:
                    pending.discard(wid)
            except ChildProcessError:
                pending.discard(wid)

        if elapsed % 15 == 0 and pending:
            print(f"    ... {len(pending)} remaining ({elapsed}s)")

    # Phase 3: Verify and record telemetry
    print(f"  Verifying...")
    ok_count = 0
    for wid, wdata in workers.items():
        out_file = run_dir / f"{wid}-output.txt"
        ok, size, lines = verify_worker(wid, wdata["target"], out_file)
        duration = time.time() - wdata["start"]

        telemetry = {
            "worker_id": wid,
            "batch": batch_num,
            "target": wdata["target"],
            "duration_s": round(duration, 1),
            "output_ok": ok,
            "output_size": size,
            "output_lines": lines,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        tele_file = TELEMETRY_DIR / f"{wid}-{timestamp}.json"
        tele_file.write_text(json.dumps(telemetry, indent=2))

        status = "✓" if ok else "✗"
        print(f"    {status} {wid}: {lines}L {size}B in {duration:.0f}s")
        if ok:
            ok_count += 1
            state["done"].append(wid)
        else:
            print(f"      ⚠ Target file MISSING or too small: {PROJECT / wdata['target']}")

    state["batches_done"].append(batch_num)
    save_state(state)

    print(f"  Batch {batch_num}: {ok_count}/{len(workers)} OK")
    return ok_count == len(workers)


def main():
    dry_run = "--dry-run" in sys.argv
    batch_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--batch" and i + 1 < len(sys.argv):
            batch_filter = int(sys.argv[i + 1])

    state = load_state()
    all_prompts = get_all_prompts()
    total_batches = (len(all_prompts) + 2) // 3

    print(f"Phase A Orchestrator — {len(all_prompts)} workers, {total_batches} batches")
    print(f"Done: {len(state['done'])}/{len(all_prompts)} ({', '.join(str(b) for b in state.get('batches_done', []))})")
    if dry_run:
        print("MODE: DRY RUN")
    print()

    for batch_num in range(1, total_batches + 1):
        if batch_filter and batch_num != batch_filter:
            continue
        if batch_num in state.get("batches_done", []):
            continue

        start = (batch_num - 1) * 3
        batch_prompts = all_prompts[start:start + 3]

        # Skip if all already done
        if all(pf.stem in state["done"] for pf in batch_prompts):
            continue

        process_batch(batch_num, batch_prompts, state, dry_run)

    print(f"\nDone. {len(state['done'])}/{len(all_prompts)} complete.")


if __name__ == "__main__":
    main()
