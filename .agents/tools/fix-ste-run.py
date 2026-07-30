#!/usr/bin/env python3
"""Fix empty STE lines in adapted rule files — batched like Phase A/B.

Usage: python3 .agents/tools/fix-ste-run.py [--dry-run]
"""

import os, sys, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
ADAPTED = PROJECT / "ste-code" / "adapted"
STATE_FILE = PROJECT / ".agents" / "state" / "FIX-STE-PROGRESS.json"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

os.makedirs(STATE_FILE.parent, exist_ok=True)


def find_broken_files():
    """Find files with empty STE lines after Non-STE."""
    broken = []
    for f in sorted(ADAPTED.glob("a-sec*-rule*.md")):
        lines = f.read_text().split("\n")
        has_broken = False
        i = 0
        while i < len(lines):
            if "**Non-STE:**" in lines[i]:
                found_ste = False
                for j in range(i + 1, min(i + 10, len(lines))):
                    if "**STE:**" in lines[j]:
                        ste_content = lines[j].split("**STE:**")[-1].strip()
                        if not ste_content or ste_content == ">":
                            has_broken = True
                        found_ste = True
                        break
                if not found_ste:
                    has_broken = True
                i = j if found_ste else i + 1
            i += 1
        if has_broken:
            broken.append(f)
    return broken


def load_state():
    if STATE_FILE.exists():
        import json
        return json.loads(STATE_FILE.read_text())
    return {"done": [], "batches_done": []}


def save_state(state):
    import json
    state["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def launch_worker(rule_file):
    """Fork + oneshot wrapper to fix one file's STE gaps."""
    content = rule_file.read_text()
    target = str(rule_file.relative_to(PROJECT))

    prompt = f"""You are STE-Code. Fix ONE specific issue. Do NOT change anything else.

FILE: {target}

ISSUE: Some Non-STE examples have EMPTY or MISSING STE corrections.
The pattern looks like:
  > **Non-STE:** [example text]
  >
or:
  > **Non-STE:** [example text]
  > **STE:** 

The STE line after the blank > separator has no correction text, or the STE line is missing entirely.

YOUR EXACT JOB:
1. Read the file
2. Find ONLY lines where Non-STE exists but STE is empty or missing after the next > separator
3. For each one, write the correct STE-Code compliant version
4. Use write_file to save the file

CRITICAL RULES:
- Do NOT change any complete Non-STE/STE pairs
- Do NOT delete, move, restructure, or rewrite ANY existing content
- Do NOT change headings, sections, formatting, or examples
- ONLY add the missing STE correction text after "> **STE:**"
- The STE correction must be a single line: > **STE:** [corrected text]

{content}"""


    tmp = PROJECT / ".agents" / "tmp" / f"fix-ste-{rule_file.stem}.txt"
    tmp.write_text(prompt)

    pid = os.fork()
    if pid == 0:
        os.chdir(str(PROJECT))
        env = os.environ.copy()
        env["HERMES_REASONING_EFFORT"] = "medium"
        os.execvpe(VENV_PYTHON, [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"], env)
        os._exit(1)
    return pid


def main():
    dry_run = "--dry-run" in sys.argv
    state = load_state()
    broken = find_broken_files()

    print(f"STE Gap Fix — {len(broken)} files, {len(broken)//3+1} batches")

    for batch_num in range(0, len(broken), 3):
        batch_files = broken[batch_num:batch_num + 3]
        real_batch = batch_num // 3 + 1

        if real_batch in state.get("batches_done", []):
            continue

        workers = {}
        print(f"\n═══ Batch {real_batch} — {len(batch_files)} files ═══")

        for rule_file in batch_files:
            rid = rule_file.stem
            if rid in state["done"]:
                print(f"  {rid}: ✓ already done")
                continue
            if dry_run:
                print(f"  {rid} [DRY]")
                continue
            pid = launch_worker(rule_file)
            workers[rid] = {"pid": pid, "start": time.time(), "file": rule_file}
            print(f"  {rid} PID={pid}")

        if dry_run or not workers:
            continue

        print(f"  Waiting...")
        elapsed = 0
        pending = set(workers.keys())
        while pending and elapsed < 600:
            time.sleep(5)
            elapsed += 5
            for rid in list(pending):
                try:
                    wpid, status = os.waitpid(workers[rid]["pid"], os.WNOHANG)
                    if wpid != 0:
                        pending.discard(rid)
                except ChildProcessError:
                    pending.discard(rid)

        for rid, wdata in workers.items():
            f = wdata["file"]
            # Verify: count empty STE after fix
            lines = f.read_text().split("\n")
            remaining = 0
            i = 0
            while i < len(lines):
                if "**Non-STE:**" in lines[i]:
                    for j in range(i + 1, min(i + 10, len(lines))):
                        if "**STE:**" in lines[j]:
                            ste = lines[j].split("**STE:**")[-1].strip()
                            if not ste or ste == ">":
                                remaining += 1
                            break
                    i = j
                i += 1
            dur = time.time() - wdata["start"]
            status = "✓" if remaining == 0 else f"✗ {remaining} left"
            print(f"    {status} {rid}: {dur:.0f}s")
            if remaining == 0:
                state["done"].append(rid)

        state["batches_done"].append(real_batch)
        save_state(state)

    print(f"\nDone. {len(state['done'])}/{len(broken)} fixed.")


if __name__ == "__main__":
    main()
