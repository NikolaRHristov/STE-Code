#!/usr/bin/env python3
"""Phase C — Populate structured data from deepened rule files.

Generates: vocabulary JSONs, synonym table, regenerated system prompts.
Uses oneshot wrapper, batches of 3, reasoning:high.

Usage:
  python3 .agents/tools/phase-c-run.py [--dry-run]
"""

import os, sys, json, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
SYSTEM_PROMPT_FILE = PROJECT / "ste-code" / "artifacts" / "ste-code-distilled-system-prompt.txt"
STATE_FILE = PROJECT / ".agents" / "state" / "PHASE-C-PROGRESS.json"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

SYSTEM_PROMPT = SYSTEM_PROMPT_FILE.read_text() if SYSTEM_PROMPT_FILE.exists() else ""

os.makedirs(STATE_FILE.parent, exist_ok=True)

# Phase C tasks: each is a worker
TASKS = [
    {
        "id": "vocab-approved",
        "desc": "Extract all APPROVED words from deepened rules and master dictionary into approved-verbs.json and approved-adjectives.json",
        "outputs": [
            "ste-code/data/vocabulary/approved-verbs.json",
            "ste-code/data/vocabulary/approved-adjectives.json",
        ],
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Extract Approved Vocabulary

Read ALL deepened rule files from ste-code/adapted/a-sec*-rule*.md and the master dictionary at ste-code/merged/master.md.

Extract every APPROVED word with:
- Word (lowercase)
- Part of speech (verb, adjective, noun)
- Approved meaning
- Example usage from a deepened rule file
- Related rule numbers

Output TWO files using write_file:

1. ste-code/data/vocabulary/approved-verbs.json
2. ste-code/data/vocabulary/approved-adjectives.json

Format as JSON arrays. Each entry: {{"word": "...", "pos": "verb", "meaning": "...", "example": "...", "rules": ["rule-1.1"]}}

Use write_file for each output file. Report entry counts.
""",
    },
    {
        "id": "vocab-unapproved",
        "desc": "Extract all UNAPPROVED words with approved alternatives from deepened rules and master dictionary",
        "outputs": ["ste-code/data/vocabulary/unapproved-entries.json"],
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Extract Unapproved Vocabulary

Read ALL deepened rule files from ste-code/adapted/a-sec*-rule*.md and the master dictionary at ste-code/merged/master.md.

Extract every UNAPPROVED word with:
- Unapproved word
- Approved alternative(s)
- Part of speech
- Why it is unapproved
- Example from a deepened rule showing the correction

Output using write_file to: ste-code/data/vocabulary/unapproved-entries.json

Format as JSON array. Each entry: {{"unapproved": "...", "approved": ["..."], "pos": "...", "reason": "...", "example_non_ste": "...", "example_ste": "..."}}

Report entry count.
""",
    },
    {
        "id": "synonym-table",
        "desc": "Regenerate the complete synonym table from all deepened rules and existing data",
        "outputs": ["ste-code/data/synonym-table.json"],
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate Synonym Table

Read ALL deepened rule files from ste-code/adapted/a-sec*-rule*.md. Extract every synonym pair (prefer/avoid) that appears in:
- Canonical synonym tables within the rules
- Non-STE/STE example pairs
- Code-domain explanation sections

Also read the existing ste-code/data/synonym-table.json for base pairs.

Output a COMPLETE updated synonym table using write_file to: ste-code/data/synonym-table.json

Format: {{"pairs": [{{"approved": "...", "avoid": ["...", "..."]}}]}}

Deduplicate. Sort alphabetically by approved word. Report pair count.
""",
    },
    {
        "id": "templates-regenerate",
        "desc": "Regenerate all 4 system prompt templates using deepened rule content",
        "outputs": [
            "ste-code/templates/ste-code-micro.md",
            "ste-code/templates/ste-code-full.md",
            "ste-code/templates/ste-code-agentic.md",
            "ste-code/templates/ste-code-developer.md",
        ],
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Regenerate System Prompt Templates

Read the deepened rule files from ste-code/adapted/a-sec*-rule*.md. Regenerate all 4 system prompt templates with updated content from the deepened rules:

1. ste-code/templates/ste-code-micro.md (~500 tokens) — 14 principles + synonym table only
2. ste-code/templates/ste-code-full.md (~4,000 tokens) — all 53 rules summarized + dictionary excerpt
3. ste-code/templates/ste-code-agentic.md (~2,500 tokens) — agent behavioral rules + compliance checking
4. ste-code/templates/ste-code-developer.md (~2,000 tokens) — full standard overview + extension guide

Each template must:
- PRESERVE the existing YAML frontmatter (id, version, tokens, use-when, source)
- Include the ASD-STE100 attribution
- Use examples from the deepened rules
- Reference specific rule numbers

Use write_file for each output file. Report token estimates and line counts.
""",
    },
    {
        "id": "data-code-dictionary",
        "desc": "Generate comprehensive code-domain dictionary JSON from all deepened rules",
        "outputs": ["ste-code/data/vocabulary/code-dictionary.json"],
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Generate Code-Domain Dictionary

Read ALL deepened rule files from ste-code/adapted/a-sec*-rule*.md. Extract every code-domain technical term that appears in:
- STE examples
- Paradigm-specific guidance sections
- Code-domain explanation sections
- Extended examples

Build a comprehensive code-domain dictionary with:
- Term
- Category (data structures, algorithms, infrastructure, development processes, etc.)
- Whether it is a technical noun, technical verb, or both
- Example usage from a deepened rule
- Related STE-Code rules

Output using write_file to: ste-code/data/vocabulary/code-dictionary.json

Format as JSON array. Each entry: {{"term": "...", "category": "...", "type": "technical-noun|technical-verb", "example": "...", "rules": ["rule-X.Y"]}}

Report entry count.
""",
    },
    {
        "id": "domain-extensions",
        "desc": "Generate domain extension entries for code-specific categories",
        "outputs": ["ste-code/data/vocabulary/domain-extensions.json"],
        "prompt": f"""{SYSTEM_PROMPT}

## TASK: Generate Domain Extensions

Read ALL deepened rule files from ste-code/adapted/a-sec*-rule*.md. Identify code-domain categories that extend the original 19 STE categories. For each:

- Category name (e.g., "Build and Package", "API Design", "Database Operations")
- Approved terms within the category
- Unapproved alternatives
- Example usage
- Related STE-Code rules

Output using write_file to: ste-code/data/vocabulary/domain-extensions.json

Format: {{"extensions": [{{"category": "...", "description": "...", "approved": ["..."], "unapproved_alternatives": ["..."], "rules": ["..."]}}]}}

Report category count and term count.
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
    tmp = PROJECT / ".agents" / "tmp" / f"phase-c-{task_id}.txt"
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

    print(f"Phase C — {len(TASKS)} structured data tasks")
    print(f"Done: {len(state['done'])}/{len(TASKS)}")
    print(f"Batch size: 3 | Reasoning: HIGH")

    # Process in batches of 3
    for batch_num in range(0, len(TASKS), 3):
        batch_tasks = TASKS[batch_num:batch_num + 3]
        real_batch = batch_num // 3 + 1

        if real_batch in state.get("batches_done", []):
            continue

        workers = {}
        print(f"\n═══ Phase C Batch {real_batch} — {len(batch_tasks)} tasks ═══")

        for task in batch_tasks:
            tid = task["id"]
            if tid in state["done"]:
                print(f"  {tid}: ✓ already done")
                continue

            if dry_run:
                print(f"  {tid}: {task['desc'][:80]}... ({len(task['prompt'])} chars) [DRY]")
                continue

            pid = launch_worker(tid, task["prompt"])
            workers[tid] = {"pid": pid, "start": time.time(), "outputs": task["outputs"]}
            print(f"  {tid}: {task['desc'][:70]}... PID={pid}")

        if dry_run or not workers:
            continue

        print(f"  Waiting...")
        elapsed = 0
        pending = set(workers.keys())
        while pending and elapsed < 900:
            time.sleep(5)
            elapsed += 5
            for tid in list(pending):
                try:
                    wpid, status = os.waitpid(workers[tid]["pid"], os.WNOHANG)
                    if wpid != 0:
                        pending.discard(tid)
                except ChildProcessError:
                    pending.discard(tid)
            if elapsed % 30 == 0 and pending:
                print(f"    ... {len(pending)} remaining ({elapsed}s)")

        ok_count = 0
        for tid, wdata in workers.items():
            all_ok = all((PROJECT / o).exists() for o in wdata["outputs"])
            dur = time.time() - wdata["start"]
            status = "✓" if all_ok else "✗"
            print(f"    {status} {tid}: {dur:.0f}s")
            if all_ok:
                ok_count += 1
                state["done"].append(tid)

        state["batches_done"].append(real_batch)
        save_state(state)

    print(f"\nDone. {len(state['done'])}/{len(TASKS)} complete.")


if __name__ == "__main__":
    main()
