#!/usr/bin/env python3
"""Phase B1 orchestrator — expansion workers via oneshot wrapper, batches of 3.

Usage:
  python3 .agents/tools/phase-b1-run.py [--batch N] [--dry-run]
"""

import os, sys, re, json, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT / ".agents" / "prompts" / "expansion-pass1"
OUTPUT_DIR = PROJECT / "ste-code" / "adapted" / "expanded"
STATE_FILE = PROJECT / ".agents" / "state" / "PHASE-B1-PROGRESS.json"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(STATE_FILE.parent, exist_ok=True)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"done": [], "batches_done": []}


def save_state(state):
    state["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_all_prompts():
    return sorted(PROMPTS_DIR.glob("pass1-batch-*.txt"))


def launch_worker(prompt_text, worker_id):
    """Fork + exec oneshot wrapper. Returns PID."""
    tmp = PROJECT / ".agents" / "tmp" / f"phase-b1-{worker_id}.txt"
    tmp.write_text(prompt_text)
    out_file = PROJECT / ".agents" / "tmp" / f"phase-b1-{worker_id}-output.txt"

    pid = os.fork()
    if pid == 0:
        os.chdir(str(PROJECT))
        with open(out_file, "w") as outf:
            os.dup2(outf.fileno(), 1)
            os.dup2(outf.fileno(), 2)
        env = os.environ.copy()
        env["HERMES_REASONING_EFFORT"] = "high"
        os.execvpe(VENV_PYTHON, [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"], env)
        os._exit(1)
    return pid


def process_batch(batch_num, batch_prompts, state, dry_run=False):
    workers = {}

    print(f"\n═══ Phase B1 Batch {batch_num} — {len(batch_prompts)} workers ═══")

    for pf in batch_prompts:
        wid = pf.stem
        output_file = OUTPUT_DIR / f"{wid}.json"
        if output_file.exists() and output_file.stat().st_size > 100:
            print(f"  {wid}: ✓ already done ({output_file.stat().st_size}B)")
            state["done"].append(wid)
            continue
        if wid in state["done"]:
            continue

        prompt_text = pf.read_text()
        if dry_run:
            print(f"  {wid} → {output_file.name} ({len(prompt_text)} chars) [DRY]")
            continue

        pid = launch_worker(prompt_text, wid)
        workers[wid] = {"pid": pid, "start": time.time(), "output": output_file}
        print(f"  {wid} → {output_file.name} PID={pid}")

    if dry_run or not workers:
        return

    print(f"  Waiting for {len(workers)} workers...")
    elapsed = 0
    pending = set(workers.keys())
    while pending and elapsed < 600:
        time.sleep(3)
        elapsed += 3
        for wid in list(pending):
            try:
                wpid, status = os.waitpid(workers[wid]["pid"], os.WNOHANG)
                if wpid != 0:
                    pending.discard(wid)
            except ChildProcessError:
                pending.discard(wid)
        if elapsed % 30 == 0 and pending:
            print(f"    ... {len(pending)} remaining ({elapsed}s)")

    ok_count = 0
    for wid, wdata in workers.items():
        ok = wdata["output"].exists() and wdata["output"].stat().st_size > 100
        dur = time.time() - wdata["start"]
        status = "✓" if ok else "✗"
        size = wdata["output"].stat().st_size if ok else 0
        print(f"    {status} {wid}: {size}B in {dur:.0f}s")
        if ok:
            ok_count += 1
            state["done"].append(wid)
        else:
            # Retry hint
            print(f"      ⚠ MISSING — will retry on next run")

    state["batches_done"].append(batch_num)
    save_state(state)
    print(f"  Batch {batch_num}: {ok_count}/{len(workers)} OK")


def main():
    dry_run = "--dry-run" in sys.argv
    batch_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--batch" and i + 1 < len(sys.argv):
            batch_filter = int(sys.argv[i + 1])

    state = load_state()
    all_prompts = get_all_prompts()
    total_batches = (len(all_prompts) + 2) // 3

    print(f"Phase B1 Orchestrator — {len(all_prompts)} workers, {total_batches} batches")
    print(f"Done: {len(state['done'])}/{len(all_prompts)}")
    print(f"Batch size: 3 | Reasoning: HIGH | Model: deepseek-v4-pro")
    print()

    for batch_num in range(1, total_batches + 1):
        if batch_filter and batch_num != batch_filter:
            continue
        start = (batch_num - 1) * 3
        batch_prompts = all_prompts[start:start + 3]
        if all(pf.stem in state["done"] for pf in batch_prompts):
            continue
        process_batch(batch_num, batch_prompts, state, dry_run)

    print(f"\nDone. {len(state['done'])}/{len(all_prompts)} complete.")


if __name__ == "__main__":
    main()
