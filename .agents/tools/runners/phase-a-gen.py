#!/usr/bin/env python3
"""Pre-generate enhanced Phase A prompts for a range of batches.

Usage:
  python3 .agents/tools/runners/phase-a-gen.py <start-batch> [end-batch]
  
Generates enhanced prompt files in .agents/tmp/phase-a-<worker-id>.txt
"""

import sys, re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
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


def enhance_prompt(prompt_text):
    """Add creative license and write_file tool instruction."""
    m = re.search(r'TARGET FILE:\s*(\S+)', prompt_text)
    target = m.group(1) if m else None
    if not target:
        return None, None
    
    tool_block = f"""## EXECUTION

Use the `write_file` tool to save the COMPLETE improved file to: {target}

Include ALL original content PLUS your improvements. Do not truncate.
After writing, confirm the file was saved and report line count + additions."""

    if 'Do NOT create files. Output the improved file content to stdout only.' in prompt_text:
        enhanced = prompt_text.replace(
            'Do NOT create files. Output the improved file content to stdout only.',
            CREATIVE_BLOCK + tool_block
        )
    else:
        enhanced = prompt_text + "\n" + CREATIVE_BLOCK + tool_block
    
    return enhanced, target


def main():
    if len(sys.argv) < 2:
        print("Usage: phase-a-gen.py <start-batch> [end-batch]")
        sys.exit(1)
    
    start = int(sys.argv[1])
    end = int(sys.argv[2]) if len(sys.argv) > 2 else start
    
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    all_prompts = sorted(PROMPTS_DIR.glob("fix-*.txt"))
    
    for batch_num in range(start, end + 1):
        start_idx = (batch_num - 1) * 3
        batch_prompts = all_prompts[start_idx:start_idx + 3]
        
        print(f"Batch {batch_num}:")
        for prompt_file in batch_prompts:
            worker_id = prompt_file.stem
            prompt_text = prompt_file.read_text()
            enhanced, target = enhance_prompt(prompt_text)
            
            if not enhanced:
                print(f"  ✗ {worker_id}: No target found")
                continue
            
            tmp_path = TMP_DIR / f"phase-a-{worker_id}.txt"
            tmp_path.write_text(enhanced)
            print(f"  ✓ {worker_id} → {target} ({len(enhanced)} chars)")
    
    print(f"\nAll prompts for batches {start}-{end} generated in {TMP_DIR}/")


if __name__ == "__main__":
    main()
