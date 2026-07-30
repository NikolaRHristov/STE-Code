#!/usr/bin/env python3
"""Phase D — Regenerate 6 deployable artifacts from deepened rules + structured data.

Usage:
  python3 .agents/tools/phase-d-run.py [--dry-run]
"""

import os, sys, json, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
SYSTEM_PROMPT_FILE = PROJECT / "ste-code" / "artifacts" / "ste-code-distilled-system-prompt.txt"
STATE_FILE = PROJECT / ".agents" / "state" / "PHASE-D-PROGRESS.json"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

SYSTEM_PROMPT = SYSTEM_PROMPT_FILE.read_text() if SYSTEM_PROMPT_FILE.exists() else ""
os.makedirs(STATE_FILE.parent, exist_ok=True)

TASKS = [
    {
        "id": "distilled-prompt",
        "desc": "Regenerate the Level 1 system prompt from deepened rules",
        "output": "ste-code/artifacts/ste-code-distilled-system-prompt.txt",
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Distilled System Prompt (Level 1)

Read the deepened rule files from ste-code/adapted/a-sec*-rule*.md. Regenerate the Level 1 system prompt (~1,200 tokens) with:

1. 14 core principles — each with a one-line summary from the deepened rules
2. Canonical synonym table — top 15 code-domain pairs
3. Output format rules — imperative mood, sentence length, structure
4. Anti-patterns — 5 most critical

PRESERVE the ASD-STE100 attribution line at the top.

Output using write_file to: ste-code/artifacts/ste-code-distilled-system-prompt.txt

Target: ~1,200 tokens. Report final token estimate.
""",
    },
    {
        "id": "self-reading-manual",
        "desc": "Regenerate the self-reading manual with full rule summaries",
        "output": "ste-code/artifacts/ste-code-self-reading-manual.txt",
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Self-Reading Manual

Read ALL deepened rule files from ste-code/adapted/a-sec*-rule*.md. Generate a comprehensive manual (~7,000 tokens) with:

1. Introduction — what STE-Code is and why it exists
2. All 53 rules — each summarized in 3-5 sentences with key examples
3. 4 GR rules — grammar guidance for code documentation
4. Dictionary excerpt — top 50 approved words with meanings
5. Synonym table — complete code-domain synonym mapping
6. Quick reference — checklist for documentation review

Include the ASD-STE100 attribution. Use examples from the deepened rules.

Output using write_file to: ste-code/artifacts/ste-code-self-reading-manual.txt

Target: ~7,000 tokens. Report sections and token estimate.
""",
    },
    {
        "id": "methodology",
        "desc": "Regenerate the extraction/adaptation methodology document",
        "output": "ste-code/artifacts/ste-code-extraction-methodology.txt",
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Methodology Document

Read the agent definitions from .agents/agent/ and the deepened rules. Generate a methodology document (~2,000 tokens) covering:

1. How STE-Code was adapted from ASD-STE100 Issue 9
2. The 5-stage pipeline: Extract → Refine → Merge → Adapt → Artifacts
3. How aerospace terms were mapped to code-domain equivalents
4. How the 19 categories were adapted for code documentation
5. Quality assurance process (audit, validation, rails)
6. Benchmark methodology

Include the ASD-STE100 attribution.

Output using write_file to: ste-code/artifacts/ste-code-extraction-methodology.txt

Target: ~2,000 tokens. Report sections.
""",
    },
    {
        "id": "example-turn",
        "desc": "Regenerate the example turn showing before/after transformation",
        "output": "ste-code/artifacts/ste-code-example-turn.txt",
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Example Turn

Create an example turn (~600 tokens) showing a real documentation transformation. Pick a complex docstring, README section, or API doc that violates multiple STE-Code rules. Show:

1. The non-compliant original
2. The STE-Code compliant version
3. A compliance table showing which principles (P1-P14) were applied
4. What changed and why

Use examples from the deepened rule files as reference.

Output using write_file to: ste-code/artifacts/ste-code-example-turn.txt

Target: ~600 tokens. Report violation count and principles applied.
""",
    },
    {
        "id": "deployment-guide",
        "desc": "Regenerate the deployment guide with integration instructions",
        "output": "ste-code/artifacts/ste-code-deployment-guide.txt",
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Deployment Guide

Generate a deployment guide (~1,500 tokens) covering:

1. How to use STE-Code with different LLMs (ChatGPT, Claude, Gemini, local models)
2. System prompt integration (copy-paste, API, Modelfile)
3. The 5 adaptation levels (-2 through 5) and when to use each
4. Integration with CI/CD documentation pipelines
5. Customization — how to extend the standard for specific domains
6. Benchmark — how to test compliance

Include the ASD-STE100 attribution and references to the GitHub repository.

Output using write_file to: ste-code/artifacts/ste-code-deployment-guide.txt

Target: ~1,500 tokens. Report sections.
""",
    },
    {
        "id": "artifact-readme",
        "desc": "Regenerate the artifacts README with index and usage notes",
        "output": "ste-code/artifacts/README.md",
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Artifacts README

Generate an artifacts README for ste-code/artifacts/ listing all 6 files with:

1. File descriptions and token estimates
2. Which adaptation level each serves
3. Quick-start usage instructions
4. Integration guide for common LLM platforms

Include the ASD-STE100 attribution.

Output using write_file to: ste-code/artifacts/README.md

Target: ~400 tokens. Report file count.
""",
    },
]


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"done": [], "batches_done": []}


def save_state(state):
    state["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def launch_worker(task_id, prompt_text):
    tmp = PROJECT / ".agents" / "tmp" / f"phase-d-{task_id}.txt"
    tmp.write_text(prompt_text)

    pid = os.fork()
    if pid == 0:
        os.chdir(str(PROJECT))
        env = os.environ.copy()
        env["HERMES_REASONING_EFFORT"] = "high"
        os.execvpe(VENV_PYTHON, [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"], env)
        os._exit(1)
    return pid


def main():
    dry_run = "--dry-run" in sys.argv
    state = load_state()

    print(f"Phase D — {len(TASKS)} artifact regeneration tasks")
    print(f"Done: {len(state['done'])}/{len(TASKS)}")

    for batch_num in range(0, len(TASKS), 3):
        batch_tasks = TASKS[batch_num:batch_num + 3]
        real_batch = batch_num // 3 + 1

        if real_batch in state.get("batches_done", []):
            continue

        workers = {}
        print(f"\n═══ Phase D Batch {real_batch} — {len(batch_tasks)} tasks ═══")

        for task in batch_tasks:
            tid = task["id"]
            if tid in state["done"]:
                print(f"  {tid}: ✓ already done")
                continue
            if dry_run:
                print(f"  {tid}: {task['desc'][:80]}... [DRY]")
                continue
            pid = launch_worker(tid, task["prompt"])
            workers[tid] = {"pid": pid, "start": time.time(), "output": task["output"]}
            print(f"  {tid} → {Path(task['output']).name} PID={pid}")

        if dry_run or not workers:
            continue

        print(f"  Waiting...")
        elapsed = 0
        pending = set(workers.keys())
        while pending and elapsed < 600:
            time.sleep(5)
            elapsed += 5
            for tid in list(pending):
                try:
                    wpid, status = os.waitpid(workers[tid]["pid"], os.WNOHANG)
                    if wpid != 0:
                        pending.discard(tid)
                except ChildProcessError:
                    pending.discard(tid)

        ok_count = 0
        for tid, wdata in workers.items():
            ok = (PROJECT / wdata["output"]).exists()
            dur = time.time() - wdata["start"]
            status = "✓" if ok else "✗"
            print(f"    {status} {tid}: {dur:.0f}s")
            if ok:
                ok_count += 1
                state["done"].append(tid)

        state["batches_done"].append(real_batch)
        save_state(state)

    print(f"\nDone. {len(state['done'])}/{len(TASKS)} complete.")


if __name__ == "__main__":
    main()
