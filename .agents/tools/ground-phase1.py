#!/usr/bin/env python3
"""Phase 1 — Grounding: verify linguistic layer claims against adapted rules.

Divides the 55 adapted rules into 5 batches, launches parallel workers.
Each worker checks its batch for: CONFIRMED (claim matches rule), 
CONTRADICTION (conflict), NOVEL (no counterpart in rules).

Usage: python3 .agents/tools/ground-phase1.py [--dry-run]
Output: docs/roadmap/GROUNDING-REPORT.md
"""

import sys, json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "_import_runner.py").read())

ADAPTED_DIR = PROJECT / "ste-code" / "adapted"
SEMANTICS = json.loads((PROJECT / "ste-code" / "linguistics" / "semantics.json").read_text())
OUTPUT = PROJECT / "docs" / "roadmap" / "GROUNDING-REPORT.md"
TMP_DIR = PROJECT / ".agents" / "tmp" / "grounding"


def build_worker_prompt(batch_files, batch_num, total_batches):
    """Build prompt for one grounding worker."""
    file_list = "\n".join(f"  {f.name}" for f in batch_files)

    # Extract key claims to verify
    claims = []
    for term, data in SEMANTICS["semantic_roles"]["term_table"].items():
        claims.append(f"SR CLAIM: '{term}' is an {data['class']} term. Result form: {data.get('result', 'none')}. Referenced in: {', '.join(data.get('rule_refs', []))}")

    for term, data in SEMANTICS["single_referent_rule"]["domain_collisions"]["entries"].items():
        contexts = ", ".join(c["qualifier"] for c in data["contexts"])
        claims.append(f"SRR CLAIM: '{term}' has domain collisions requiring qualification: {contexts}")

    claims_text = "\n".join(claims[:30])  # First 30 claims

    return f"""You are STE-Code Grounding Auditor (batch {batch_num}/{total_batches}).

Verify these linguistic layer claims against the adapted rule files.

FILES TO CHECK ({len(batch_files)} files):
{file_list}

CLAIMS TO VERIFY:
{claims_text}

For each claim:
1. Read the referenced rule file(s)
2. Check if the rule already covers this concept
3. Classify as:
   A. CONFIRMED — rule already addresses this (cite file:line)
   B. CONTRADICTION — linguistic claim conflicts with rule (quote both)
   C. NOVEL — no counterpart found in rules (this is net-new value)

Also check:
- Do all 10 semantic role terms have corresponding rule references?
- Do all 10 collision domains have examples in adapted rules?
- Are any rule references wrong (pointing to non-existent rules)?

CRITICAL:
- Read the actual files — do not assume content
- For CONTRADICTIONS: quote both sides verbatim, do not resolve
- For CONFIRMED: cite exact file and line number

Write findings to: {TMP_DIR}/batch-{batch_num:02d}-grounding.md

Format:
## Batch {batch_num} — {len(batch_files)} files

### CONFIRMED
| Claim | Rule File | Line | Notes |
|-------|-----------|------|-------|

### CONTRADICTION  
| Claim | Rule Says | Layer Says |
|-------|-----------|------------|

### NOVEL
| Claim | Description |
|-------|-------------|
"""


def main():
    dry_run = "--dry-run" in sys.argv
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(ADAPTED_DIR.glob("a-sec*.md"))
    batch_size = max(1, len(files) // 5)
    batches = [files[i:i+batch_size] for i in range(0, len(files), batch_size)]

    print(f"Files: {len(files)} in {len(batches)} batches")
    if dry_run:
        for i, b in enumerate(batches):
            print(f"  Batch {i+1}: {len(b)} files — {b[0].name} to {b[-1].name}")
        return

    processes = []
    for i, batch in enumerate(batches):
        prompt = build_worker_prompt(batch, i + 1, len(batches))
        proc = launch_agent(prompt, model="poolside/laguna-s-2.1:free", cwd=PROJECT)
        processes.append((i + 1, proc))
        print(f"Launched batch {i+1}/{len(batches)} ({len(batch)} files, PID {proc.pid})")

    print(f"\nWaiting for {len(processes)} grounding workers...")
    for batch_num, proc in processes:
        proc.communicate(timeout=900)
        print(f"  Batch {batch_num}: done")

    # Collect reports
    report_lines = ["# Phase 1 — Grounding Report\n", f"\nDate: 2026-07-30\n"]
    for report_file in sorted(TMP_DIR.glob("batch-*-grounding.md")):
        report_lines.append(report_file.read_text())
        report_lines.append("\n---\n")

    # Merge into final report
    OUTPUT.write_text("\n".join(report_lines))
    print(f"\nGrounding report: {OUTPUT}")


if __name__ == "__main__":
    main()
