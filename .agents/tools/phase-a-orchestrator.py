#!/usr/bin/env python3
"""Phase A orchestrator: Launch maturity-fix workers in batches of 3.

Reads 61 pre-generated prompts, enhances each with creative license and
write_file tool instruction, launches via hermes -z --yolo in background,
and tracks completion.

Usage:
  python3 .agents/tools/phase-a-orchestrator.py [--batch N] [--dry-run]
  
  --batch N    Launch only batch N (1-21). Default: all.
  --dry-run    Print what would be launched without executing.
"""

import os, sys, re, subprocess, json, time
from pathlib import Path
from datetime import datetime

PROJECT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT / ".agents" / "prompts" / "maturity-fixes"
STATE_FILE = PROJECT / ".agents" / "state" / "PHASE-A-PROGRESS.json"

CREATIVE_PREAMBLE = """## CREATIVE LICENSE

You are an expert documentation architect. Go BEYOND the suggested improvements.
Be creative, insightful, and thorough. Add your own edge cases, examples, and
structural improvements that would make this file substantially stronger.
Think: "What would a senior engineer want to see in this agent definition that
isn't listed below?" Add it. The suggested improvements are a floor, not a ceiling.

This is your chance to elevate these agent files from "adequate" to "exemplary."
Be bold. Be precise. Be creative.

"""

TOOL_INSTRUCTION_TEMPLATE = """## EXECUTION

Use the `write_file` tool to save the COMPLETE improved file to:
  {target_file}

Include ALL original content PLUS your improvements. Do not truncate.
After writing, confirm the file was saved and report line count + additions.
"""


def extract_target_file(prompt_text):
    """Extract TARGET FILE path from prompt."""
    m = re.search(r'TARGET FILE:\s*(\S+)', prompt_text)
    return m.group(1) if m else None


def enhance_prompt(prompt_text, creative=True):
    """Enhance prompt with creative preamble and tool instruction."""
    target = extract_target_file(prompt_text)
    if not target:
        return None, None
    
    # Find the INSTRUCTIONS section and insert creative preamble before it
    instructions_marker = "═══════════════════════════════════════\nINSTRUCTIONS:"
    if instructions_marker in prompt_text:
        # Insert creative preamble before INSTRUCTIONS
        parts = prompt_text.split(instructions_marker, 1)
        enhanced = parts[0] + instructions_marker + "\n"
    else:
        enhanced = prompt_text + "\n"
    
    if creative:
        enhanced += CREATIVE_PREAMBLE
    
    tool_instruction = TOOL_INSTRUCTION_TEMPLATE.format(target_file=target)
    
    # Replace the old instruction about stdout with new tool instruction
    enhanced = re.sub(
        r"Do NOT create files\. Output the improved file content to stdout only\.",
        tool_instruction,
        enhanced
    )
    
    return enhanced, target


def launch_worker(prompt_text, worker_id, dry_run=False):
    """Launch one hermes -z worker with the enhanced prompt."""
    if dry_run:
        target = extract_target_file(prompt_text)
        print(f"  [DRY] {worker_id} → {target}")
        return {"worker_id": worker_id, "dry_run": True}
    
    # Write prompt to temp file to avoid shell quoting issues
    tmp_prompt = PROJECT / ".agents" / "tmp" / f"phase-a-{worker_id}.txt"
    tmp_prompt.parent.mkdir(exist_ok=True)
    tmp_prompt.write_text(prompt_text)
    
    # Launch
    cmd = f'hermes -z "$(cat {tmp_prompt})" -m deepseek-v4-pro --yolo'
    print(f"  Launching {worker_id}...")
    
    try:
        result = subprocess.run(
            ["hermes", "-z", prompt_text, "-m", "deepseek-v4-pro", "--yolo"],
            capture_output=True, text=True,
            cwd=str(PROJECT),
            timeout=600
        )
        return {
            "worker_id": worker_id,
            "exit_code": result.returncode,
            "stdout_len": len(result.stdout),
            "stderr_snippet": result.stderr[:200] if result.stderr else "",
            "dry_run": False
        }
    except subprocess.TimeoutExpired:
        return {"worker_id": worker_id, "timeout": True, "dry_run": False}
    except Exception as e:
        return {"worker_id": worker_id, "error": str(e), "dry_run": False}
    finally:
        if tmp_prompt.exists():
            tmp_prompt.unlink()


def load_progress():
    """Load batch progress from state file."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"completed_batches": [], "completed_workers": [], "last_run": None}


def save_progress(progress):
    """Save batch progress."""
    progress["last_run"] = datetime.now().isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(progress, indent=2))


def get_batches():
    """Group 61 prompts into 21 batches of 3 (last batch has 1)."""
    prompts = sorted(PROMPTS_DIR.glob("fix-*.txt"))
    batches = []
    for i in range(0, len(prompts), 3):
        batches.append(prompts[i:i+3])
    return batches


def main():
    dry_run = "--dry-run" in sys.argv
    batch_arg = None
    for i, arg in enumerate(sys.argv):
        if arg == "--batch" and i + 1 < len(sys.argv):
            batch_arg = int(sys.argv[i + 1])
    
    progress = load_progress()
    all_batches = get_batches()
    
    print(f"Phase A Orchestrator — {len(all_batches)} batches, {sum(len(b) for b in all_batches)} workers")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
    if batch_arg:
        print(f"Batch filter: {batch_arg} only")
    print(f"Completed: {progress['completed_batches']}")
    print()
    
    for batch_idx, batch_files in enumerate(all_batches, 1):
        if batch_arg and batch_idx != batch_arg:
            continue
        if batch_idx in progress["completed_batches"]:
            print(f"Batch {batch_idx}: SKIPPED (already complete)")
            continue
        
        print(f"═══ Batch {batch_idx}/{len(all_batches)} ═══")
        workers = []
        
        for prompt_file in batch_files:
            worker_id = prompt_file.stem
            if worker_id in progress["completed_workers"]:
                print(f"  {worker_id}: SKIPPED (already complete)")
                continue
            
            prompt_text = prompt_file.read_text()
            enhanced, target = enhance_prompt(prompt_text, creative=True)
            
            if not enhanced:
                print(f"  {worker_id}: SKIPPED (no target file found)")
                continue
            
            # Launch (synchronous per batch for verification)
            result = launch_worker(enhanced, worker_id, dry_run=dry_run)
            workers.append(result)
            
            if not dry_run:
                target_path = PROJECT / target
                file_exists = target_path.exists()
                status = "✓" if result.get("exit_code") == 0 and file_exists else "✗"
                print(f"    {status} exit={result.get('exit_code')} file={'exists' if file_exists else 'MISSING'}")
        
        if not dry_run and workers:
            progress["completed_batches"].append(batch_idx)
            for w in workers:
                progress["completed_workers"].append(w["worker_id"])
            save_progress(progress)
        
        print()
        
        # Small pause between batches
        if not dry_run and not batch_arg:
            time.sleep(2)
    
    print("Done.")
    print(f"Complete: {len(progress['completed_batches'])}/{len(all_batches)} batches")
    
    # Show remaining
    remaining = [i for i in range(1, len(all_batches) + 1) if i not in progress["completed_batches"]]
    if remaining:
        print(f"Remaining batches: {remaining}")


if __name__ == "__main__":
    main()
