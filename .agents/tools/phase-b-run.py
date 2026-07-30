#!/usr/bin/env python3
"""Phase B — Deepen adapted rule files to match original ASD-STE100 density.

Generates prompts from adapted files, launches workers via oneshot wrapper.
Each worker deepens ONE rule file with: detailed code-domain explanations,
edge cases, paradigm-specific guidance, multiple example groups, and
grammatical analysis adapted from the original STE spec.

Usage:
  python3 .agents/tools/phase-b-run.py [--dry-run] [--batch N]
"""

import os, sys, re, json, time
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
STATE_FILE = PROJECT / ".agents" / "state" / "PHASE-B-PROGRESS.json"
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"

# Load system prompt
SYSTEM_PROMPT_FILE = PROJECT / "ste-code" / "artifacts" / "ste-code-distilled-system-prompt.txt"
SYSTEM_PROMPT = SYSTEM_PROMPT_FILE.read_text() if SYSTEM_PROMPT_FILE.exists() else ""

RULE_DEEPEN_INSTRUCTION = """## TASK: Deepen this rule to match the original ASD-STE100 standard density

The original ASD-STE100 Issue 9 has 4-5 pages per rule section with:
- Detailed grammatical analysis and justification
- Multiple example groups (3-5 pairs per rule)
- Edge cases and exceptions
- Cross-references to related rules

This adapted file is a skeleton (~50-60 lines). Deepen it to 200-400 lines by adding:

1. **Code-Domain Explanation** — What this rule means specifically for code documentation:
   - README files, API docs, docstrings, commit messages, error messages
   - How it applies differently to each documentation type

2. **Paradigm-Specific Guidance** — How the rule applies in:
   - Object-Oriented (Java, C++, C#, Python classes)
   - Functional (Haskell, Elixir, Clojure, Rust)
   - Procedural (C, Go, Bash)
   - Declarative (SQL, Terraform, Kubernetes YAML)
   - Systems (Rust ownership docs, C memory docs)

3. **Extended Examples (4-6 pairs)** — Each with:
   - Non-STE version (violating the rule, using real code documentation scenarios)
   - STE-Code compliant version (following the rule)
   - Which principle (P1-P14) was applied
   - Brief explanation of the fix

4. **Edge Cases** — 3-5 scenarios where the rule has nuance:
   - When a framework name is also an "unapproved" word
   - When a code keyword conflicts with the rule
   - When the rule should be relaxed for generated code

5. **Cross-References** — Link to related rules and the STE-Code dictionary

6. **Grammar Notes** — If the original STE rule has grammatical justification, adapt it for code documentation grammar

PRESERVE all existing content. Only ADD new sections. Use STE-Code approved vocabulary throughout.
Be as rigorous and detailed as the original ASD-STE100 specification.

## FORMATTING RULES (non-negotiable)

1. All STE/Non-STE example pairs MUST use this exact blockquote format with a blank > between pairs:
```
> **Non-STE:** [violating example]
>
> **STE:** [compliant example]
>
> *Principles applied: [P#], [explanation]*
```

2. NEVER put Non-STE and STE on consecutive > lines without a blank > separator — this breaks GitHub rendering.

3. Use 4-backtick fences when showing markdown code fence syntax inside examples.

## EXECUTION

Use the `write_file` tool to save the COMPLETE deepened file to: {target}

Include ALL original content PLUS your additions. Target: 200-400 lines total.
After writing, confirm the file was saved and report: line count, sections added, example count.
"""

CREATIVE = """## CREATIVE LICENSE

You are adapting aerospace technical English into code documentation standards.
Think like a senior technical writer at a major software company. Be thorough,
precise, and domain-aware. The original ASD-STE100 was crafted over decades by
aerospace engineers — match that level of rigor for software engineering.
"""

os.makedirs(STATE_FILE.parent, exist_ok=True)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"done": [], "batches_done": []}


def save_state(state):
    state["updated"] = datetime.now(timezone.utc).isoformat()
    STATE_FILE.write_text(json.dumps(state, indent=2))


def get_rule_files():
    """Get all adapted rule files (a-secN-ruleX.Y.md), sorted."""
    return sorted(ADAPTED_DIR.glob("a-sec*-rule*.md"))


def launch_worker(worker_id, prompt_text):
    tmp = PROJECT / ".agents" / "tmp" / f"phase-b-{worker_id}.txt"
    tmp.write_text(prompt_text)

    pid = os.fork()
    if pid == 0:
        os.chdir(str(PROJECT))
        env = os.environ.copy()
        env["HERMES_REASONING_EFFORT"] = "high"
        os.execvpe(VENV_PYTHON, [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"], env)
        os._exit(1)
    return pid


def process_batch(batch_num, batch_rules, state, dry_run=False):
    workers = {}
    print(f"\n═══ Phase B Batch {batch_num} — {len(batch_rules)} rules ═══")

    for rule_file in batch_rules:
        rule_id = rule_file.stem  # e.g., a-sec1-rule1.1
        if rule_id in state["done"]:
            print(f"  {rule_id}: ✓ already done")
            continue

        rule_content = rule_file.read_text()
        target = str(rule_file.relative_to(PROJECT))

        # Build prompt
        instruction = RULE_DEEPEN_INSTRUCTION.format(target=target)
        prompt = f"""{SYSTEM_PROMPT}

{CREATIVE}

{instruction}

═══════════════════════════════════════
CURRENT RULE FILE: {target}
═══════════════════════════════════════
{rule_content}
"""

        if dry_run:
            lines = len(rule_content.splitlines())
            print(f"  {rule_id}: {lines}L → target 200-400L ({len(prompt)} chars) [DRY]")
            continue

        pid = launch_worker(rule_id, prompt)
        workers[rule_id] = {"pid": pid, "start": time.time(), "file": rule_file}
        print(f"  {rule_id}: {len(rule_content.splitlines())}L → target 200-400L PID={pid}")

    if dry_run or not workers:
        return

    print(f"  Waiting for {len(workers)} workers...")
    elapsed = 0
    pending = set(workers.keys())
    while pending and elapsed < 900:
        time.sleep(3)
        elapsed += 3
        for rid in list(pending):
            try:
                wpid, status = os.waitpid(workers[rid]["pid"], os.WNOHANG)
                if wpid != 0:
                    pending.discard(rid)
            except ChildProcessError:
                pending.discard(rid)
        if elapsed % 30 == 0 and pending:
            print(f"    ... {len(pending)} remaining ({elapsed}s)")

    ok_count = 0
    for rid, wdata in workers.items():
        f = wdata["file"]
        ok = f.exists() and f.stat().st_size > 1000
        new_lines = len(f.read_text().splitlines()) if ok else 0
        dur = time.time() - wdata["start"]
        status = "✓" if ok else "✗"
        print(f"    {status} {rid}: {new_lines}L ({f.stat().st_size}B) in {dur:.0f}s")
        if ok:
            ok_count += 1
            state["done"].append(rid)

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
    rules = get_rule_files()

    # Group into batches of 3
    batches = []
    for i in range(0, len(rules), 3):
        batches.append(rules[i:i+3])

    print(f"Phase B Orchestrator — {len(rules)} rules, {len(batches)} batches")
    print(f"Done: {len(state['done'])}/{len(rules)}")
    print(f"Batch size: 3 | Reasoning: HIGH | Target: 200-400L per rule")

    for batch_num, batch_rules in enumerate(batches, 1):
        if batch_filter and batch_num != batch_filter:
            continue
        if batch_num in state.get("batches_done", []):
            continue
        process_batch(batch_num, batch_rules, state, dry_run)

    print(f"\nDone. {len(state['done'])}/{len(rules)} complete.")


if __name__ == "__main__":
    main()
