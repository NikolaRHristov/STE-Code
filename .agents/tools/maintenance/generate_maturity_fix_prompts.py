#!/usr/bin/env python3
"""Generate maturity fix worker prompts — one per audit finding.
Each prompt: target file + gap description + improvement instructions."""
import os, glob

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROMPTS_DIR = os.path.join(PROJECT, ".agents", "prompts", "maturity-fixes")
AUDIT_DIR = os.path.join(PROJECT, ".agents", "audit")

os.makedirs(PROMPTS_DIR, exist_ok=True)

# Load system prompt
with open(os.path.join(PROJECT, "ste-code", "artifacts", "ste-code-distilled-system-prompt.txt")) as f:
    SYSTEM_PROMPT = f.read()

# Read all maturity audit files
maturity_files = sorted(glob.glob(os.path.join(AUDIT_DIR, "maturity-batch*-w*.md")))
print(f"Found {len(maturity_files)} maturity audit files")

prompt_count = 0
for mf in maturity_files:
    with open(mf) as f:
        content = f.read()
    
    # Parse findings — each starts with "### " followed by a file path
    import re
    findings = re.split(r'\n(?=### \.agents/)', content)
    
    for finding in findings:
        if not finding.strip() or not finding.startswith("### "):
            continue
        
        # Extract target file
        target_match = re.match(r'### (\.agents/[^\n]+)', finding)
        if not target_match:
            continue
        target_file = target_match.group(1).strip()
        target_path = os.path.join(PROJECT, target_file.replace("./", ""))
        
        # Extract gap summary
        gaps = []
        in_gaps = False
        for line in finding.split("\n"):
            if "**Gaps:**" in line or "**Gaps:**" in line:
                in_gaps = True
                continue
            if in_gaps and line.startswith("**"):
                in_gaps = False
            if in_gaps and line.strip().startswith("-"):
                gaps.append(line.strip())
        
        if not gaps:
            continue
        
        # Extract what level N+1 would add
        improvements = []
        in_improvements = False
        for line in finding.split("\n"):
            if "**What Level" in line:
                in_improvements = True
                continue
            if in_improvements and line.startswith("**"):
                in_improvements = False
            if in_improvements and line.strip().startswith("-"):
                improvements.append(line.strip())
        
        # Skip if target file doesn't exist
        if not os.path.exists(target_path):
            continue
        
        # Read target file content (first 4000 chars)
        try:
            with open(target_path) as f:
                target_content = f.read()[:4000]
        except:
            continue
        
        prompt_count += 1
        gaps_text = "\n".join(gaps[:5])
        improvements_text = "\n".join(improvements[:5])
        
        prompt = f"""{SYSTEM_PROMPT}

You are a documentation improvement worker. Your task: apply specific improvements to a single file based on a maturity audit finding.

═══════════════════════════════════════
TARGET FILE: {target_file}
═══════════════════════════════════════

═══════════════════════════════════════
CURRENT CONTENT (first 4000 chars):
═══════════════════════════════════════
{target_content}

═══════════════════════════════════════
GAPS TO FIX (from maturity audit):
═══════════════════════════════════════
{gaps_text}

═══════════════════════════════════════
SUGGESTED IMPROVEMENTS:
═══════════════════════════════════════
{improvements_text}

═══════════════════════════════════════
INSTRUCTIONS:
═══════════════════════════════════════
1. Apply ALL suggested improvements to the target file.
2. PRESERVE all existing content — only ADD missing sections.
3. Do NOT delete or rewrite existing text.
4. Use STE-Code approved vocabulary and active voice.
5. Output the COMPLETE improved file as markdown.

Do NOT create files. Output the improved file content to stdout only.
"""
        safe_name = target_file.replace("/", "-").replace(".", "-")
        prompt_file = os.path.join(PROMPTS_DIR, f"fix-{prompt_count:03d}-{safe_name[:40]}.txt")
        with open(prompt_file, "w") as f:
            f.write(prompt)

print(f"Generated {prompt_count} prompts in {PROMPTS_DIR}/")
