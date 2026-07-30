#!/usr/bin/env python3
"""Launch one Phase A batch: 3 enhanced hermes workers in background.

Usage:
  python3 .agents/tools/phase-a-batch.py <batch-number>

Batch numbers 1-21. Each batch is 3 workers (last batch has 1).
Enhances each prompt with creative license + write_file tool instruction.
Launches via terminal background with notify_on_complete.
"""

import os, sys, re, subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = PROJECT / ".agents" / "prompts" / "maturity-fixes"
TMP_DIR = PROJECT / ".agents" / "tmp"

CREATIVE_BLOCK = """## CREATIVE LICENSE

You are an expert documentation architect. Go BEYOND the suggested improvements.
Be creative, insightful, and thorough. Add your own edge cases, examples, and
structural improvements that make this file substantially stronger.
Think: "What would a senior engineer want to see that isn't listed?"
Add it. The suggested improvements are a floor, not a ceiling.
Be bold. Be precise. Be creative.

"""


def get_batch_prompts(batch_num):
    """Get the 3 prompt files for this batch number."""
    all_prompts = sorted(PROMPTS_DIR.glob("fix-*.txt"))
    start = (batch_num - 1) * 3
    return all_prompts[start:start + 3]


def enhance_prompt(prompt_text, prompt_file):
    """Add creative license and write_file tool instruction."""
    # Extract target file
    m = re.search(r'TARGET FILE:\s*(\S+)', prompt_text)
    target = m.group(1) if m else None
    if not target:
        print(f"  WARNING: No TARGET FILE found in {prompt_file.name}")
        return None, None
    
    tool_block = f"""## EXECUTION

Use the `write_file` tool to save the COMPLETE improved file to: {target}

Include ALL original content PLUS your improvements. Do not truncate.
After writing, confirm the file was saved and report line count + additions."""

    # Replace stdout-only instruction with tool instruction
    if 'Do NOT create files. Output the improved file content to stdout only.' in prompt_text:
        enhanced = prompt_text.replace(
            'Do NOT create files. Output the improved file content to stdout only.',
            CREATIVE_BLOCK + tool_block
        )
    else:
        # Insert before the last INSTRUCTIONS line or at end
        enhanced = prompt_text + "\n" + CREATIVE_BLOCK + tool_block
    
    return enhanced, target


def main():
    if len(sys.argv) < 2:
        print("Usage: phase-a-batch.py <batch-number>")
        sys.exit(1)
    
    batch_num = int(sys.argv[1])
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    
    prompts = get_batch_prompts(batch_num)
    if not prompts:
        print(f"Batch {batch_num}: No prompts found")
        sys.exit(1)
    
    print(f"═══ Phase A Batch {batch_num} — {len(prompts)} workers ═══")
    
    for prompt_file in prompts:
        worker_id = prompt_file.stem
        prompt_text = prompt_file.read_text()
        enhanced, target = enhance_prompt(prompt_text, prompt_file)
        
        if not enhanced:
            print(f"  ✗ {worker_id}: Could not enhance prompt")
            continue
        
        # Write enhanced prompt to temp file
        tmp_path = TMP_DIR / f"phase-a-{worker_id}.txt"
        tmp_path.write_text(enhanced)
        
        # Build command
        cmd = f'hermes -z "$(cat {tmp_path})" -m deepseek-v4-pro --yolo'
        
        print(f"  → {worker_id} → {target} ({len(enhanced)} chars)")
        
        # Launch via subprocess in background
        subprocess.Popen(
            ["hermes", "-z", enhanced, "-m", "deepseek-v4-pro", "--yolo"],
            cwd=str(PROJECT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    
    print(f"  Batch {batch_num}: All {len(prompts)} workers launched.")
    print(f"  Verify with: ls -la {PROJECT}/.agents/agent/agent-*-*.md")


if __name__ == "__main__":
    main()
