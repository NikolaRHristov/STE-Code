#!/usr/bin/env python3
"""Populate Level 5 directories — one summary per rule, batched by section.

Usage: python3 .agents/tools/populate-level5.py [--section N]
"""

import os, sys, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
RULES_DIR = PROJECT / "ste-code" / "adapted"
LEVEL5_DIR = PROJECT / "ste-code" / "artifacts" / "level5"
STATE_FILE = PROJECT / ".agents" / "state" / "LEVEL5-PROGRESS.json"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

os.makedirs(STATE_FILE.parent, exist_ok=True)

SECTIONS = {f"sec{n}": n for n in range(1, 10)}


def load_state():
    import json
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"done": [], "batches_done": []}


def save_state(state):
    import json
    state["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def launch_worker(rule_file, section):
    """Generate summary for one rule into level5/<section>/<rule>/summary.md."""
    rule_id = rule_file.stem
    content = rule_file.read_text()
    output_path = LEVEL5_DIR / section / rule_id / "summary.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    prompt = f"""You are STE-Code. Generate a Level 5 summary for this rule.

Read the rule file and produce a clean summary markdown file with:

1. Rule title and number
2. Original rule summary (3-4 sentences)
3. STE-Code adaptation for code documentation (3-4 sentences)
4. 3 complete Non-STE/STE example pairs with proper > blockquote format
5. Principles applied (P1-P14)

CRITICAL: Every Non-STE MUST have a complete STE correction.
Use blank > separators between Non-STE and STE lines.

Source rule:
{content[:6000]}

Use write_file to save to: {output_path}
Report: example count, char count."""

    tmp = PROJECT / ".agents" / "tmp" / f"level5-{rule_id}.txt"
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
    section_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--section" and i + 1 < len(sys.argv):
            section_filter = arg

    state = load_state()
    rules = sorted(RULES_DIR.glob("a-sec*-rule*.md"))

    # Group by section
    from collections import defaultdict
    by_section = defaultdict(list)
    for r in rules:
        sec = r.stem.split("-")[1]  # sec1, sec2, etc.
        by_section[sec].append(r)

    for sec in sorted(by_section):
        if section_filter and sec != section_filter:
            continue

        section_rules = by_section[sec]
        # Process 3 rules per batch
        for batch_num in range(0, len(section_rules), 3):
            batch_rules = section_rules[batch_num:batch_num + 3]
            real_batch = f"{sec}-{batch_num//3+1}"

            if real_batch in state.get("batches_done", []):
                continue

            workers = {}
            print(f"\n═══ {sec} batch {batch_num//3+1} — {len(batch_rules)} rules ═══")

            for r in batch_rules:
                rid = r.stem
                if rid in state["done"]:
                    print(f"  {rid}: ✓")
                    continue
                if dry_run:
                    print(f"  {rid} [DRY]")
                    continue
                pid = launch_worker(r, sec)
                workers[rid] = {"pid": pid, "start": time.time()}
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
                    except (ChildProcessError, ProcessLookupError):
                        pending.discard(rid)

            for rid in workers:
                out = LEVEL5_DIR / sec / rid / "summary.md"
                ok = out.exists() and out.stat().st_size > 200
                dur = time.time() - workers[rid]["start"]
                status = "✓" if ok else "✗"
                size = out.stat().st_size if ok else 0
                print(f"    {status} {rid}: {size}B in {dur:.0f}s")
                if ok:
                    state["done"].append(rid)

            state["batches_done"].append(real_batch)
            save_state(state)

    print(f"\nDone. {len(state['done'])}/{len(rules)} rules.")


if __name__ == "__main__":
    main()
