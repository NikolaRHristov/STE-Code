#!/usr/bin/env python3
"""Quality Sweep — parallel batch workers audit all STE-Code output files.

Divides all deliverable files into batches, launches parallel agent workers
to quality-check each batch for STE-Code compliance, formatting, and consistency.

Usage: python3 .agents/tools/quality/sweep-quality.py [--agent hermes|claude|codex] [--dry-run] [--batches N]
"""

import sys, time
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

TMP_DIR = PROJECT / ".agents" / "tmp" / "sweep"
SWEEP_REPORT = PROJECT / "ste-code" / "artifacts" / "sweep-report.md"

# Files to sweep
ARTIFACT_FILES = sorted(
    list((PROJECT / "ste-code" / "artifacts").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level1").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level2").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level3").glob("*.txt"))
    + list((PROJECT / "ste-code" / "artifacts" / "level4").glob("*.txt"))
)
ADAPTED_FILES = sorted((PROJECT / "ste-code" / "adapted").glob("a-sec*.md"))

CHECKLIST = """
For each file, check and fix:

1. STE-Code COMPLIANCE:
   - All words are approved or code-domain technical terms
   - No unapproved synonyms (check against Level 2 synonym table)
   - Correct part-of-speech usage (nouns not used as verbs, etc.)
   - Active voice, no semicolons, no contractions
   - Sentence length: 20 words procedural, 25 words descriptive

2. FORMATTING:
   - Consistent heading hierarchy
   - Clean paragraph breaks
   - No mangled/malformed text
   - Proper code block formatting
   - Attribution footer present where applicable

3. CONSISTENCY:
   - Terminology matches across files
   - Rule numbers are correct
   - Example pairs have complete Non-STE and STE versions
   - No contradictions between files

4. COMPLETENESS:
   - All sections present where expected
   - No truncated content
   - Required elements present (attribution, rule references, etc.)

Fix any issues found. For each file, report: FILE OK or FILE FIXED with description of changes.
"""


def build_worker_prompt(batch_files, batch_num, total_batches):
    """Build a worker prompt for one batch of files."""
    file_list = "\n".join(f"  {str(f.relative_to(PROJECT))}" for f in batch_files)
    return f"""You are STE-Code Quality Auditor. Perform a maintenance sweep on {len(batch_files)} files (batch {batch_num}/{total_batches}).

FILES TO AUDIT:
{file_list}

QUALITY CHECKLIST:
{CHECKLIST}

PROCESS:
1. Read each file using read_file
2. Check against the checklist above
3. If issues found, fix them with patch or write_file
4. For each file, write a one-line result: "OK" or "FIXED: <what was fixed>"

CRITICAL:
- Do NOT make cosmetic-only changes — fix real issues only
- Preserve existing content unless it violates STE-Code rules
- If a file is fine, say OK — do not rewrite it
- Respect sentence length limits in any new text you write
- Use active voice, approved vocabulary, imperative mood for instructions

After processing ALL files, write a batch report to:
  {TMP_DIR}/batch-{batch_num:02d}-report.md

Include: batch number, files processed, files fixed, summary of fixes.
"""


def main():
    agent = None
    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]

    dry_run = "--dry-run" in sys.argv
    num_batches = 5
    for i, arg in enumerate(sys.argv):
        if arg == "--batches" and i + 1 < len(sys.argv):
            num_batches = int(sys.argv[i + 1])

    all_files = ARTIFACT_FILES + ADAPTED_FILES
    all_files = sorted(set(f for f in all_files if f.exists() and f.is_file()))

    print(f"Files to sweep: {len(all_files)}")
    print(f"Batches: {num_batches} (~{len(all_files)//num_batches} files each)")

    # Divide into batches
    batch_size = max(1, len(all_files) // num_batches)
    batches = []
    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size if i < num_batches - 1 else len(all_files)
        batches.append(all_files[start:end])

    for i, batch in enumerate(batches):
        print(f"  Batch {i+1}: {len(batch)} files")

    if dry_run:
        print("\nDry run complete. Use without --dry-run to execute.")
        return

    TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Launch all batches in parallel using agent_runner
    processes = []
    for i, batch in enumerate(batches):
        prompt = build_worker_prompt(batch, i + 1, num_batches)
        proc = launch_agent(prompt, agent=agent, model=os.environ.get("STE_MODEL", "poolside/laguna-s-2.1:free"), cwd=PROJECT)
        processes.append((i + 1, proc))
        print(f"Launched batch {i+1}/{num_batches} (PID {proc.pid})")

    # Wait for all and collect results
    print(f"\nWaiting for {len(processes)} batches...")
    results = []
    for batch_num, proc in processes:
        stdout, stderr = proc.communicate(timeout=900)
        results.append((batch_num, proc.returncode, stdout, stderr))
        status = "OK" if proc.returncode == 0 else f"FAIL ({proc.returncode})"
        print(f"Batch {batch_num}: {status}")

    # Write sweep report
    report_lines = [
        "# Quality Sweep Report",
        f"\nDate: {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"Files swept: {len(all_files)}",
        f"Batches: {num_batches}",
        f"\n## Batch Results\n",
    ]
    for batch_num, rc, stdout, stderr in results:
        report_lines.append(f"\n### Batch {batch_num} (exit {rc})")
        if stdout:
            tail = stdout[-2000:] if len(stdout) > 2000 else stdout
            report_lines.append(f"```\n{tail}\n```")
        if stderr:
            report_lines.append(f"Errors:\n```\n{stderr[-500:]}\n```")

    SWEEP_REPORT.write_text("\n".join(report_lines))
    print(f"\nSweep report: {SWEEP_REPORT}")

    print("\nBatch reports:")
    for report_file in sorted(TMP_DIR.glob("batch-*-report.md")):
        print(f"  {report_file}")


if __name__ == "__main__":
    main()
