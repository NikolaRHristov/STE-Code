#!/usr/bin/env python3
"""Agent #8 — Enlarge ste-code from refined content using poll workers.
Takes refined files as input, generates code-domain enrichments in batches of 3."""
import subprocess, os, tempfile, time, sys

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REFINED_DIR = os.path.join(PROJECT, "ste-code", "refined")
OUT_DIR = os.path.join(PROJECT, "ste-code", "enriched-code")
MODEL = "deepseek-v4-pro"

os.makedirs(OUT_DIR, exist_ok=True)

# Load the extension worker agent prompt
with open(os.path.join(PROJECT, ".agents/agent/agent-8-extension-worker.md")) as f:
    AGENT_PROMPT = f.read()

# Get refined files sorted
refined_files = sorted([f for f in os.listdir(REFINED_DIR) if f.endswith('.md')])

# Enrichment areas — each worker batch gets one area + one section of refined content
AREAS = [
    {"name": "code-examples", "desc": "Generate 5 STE/non-STE code documentation example pairs for each rule in the refined content. Replace all aerospace examples with code-domain equivalents.", "output_prefix": "code-examples"},
    {"name": "dictionary-expand", "desc": "Expand the dictionary section with code-domain approved terms and their definitions. For each aerospace term, suggest a code-domain equivalent if applicable.", "output_prefix": "dict-expand"},
    {"name": "domain-adapt", "desc": "Adapt category descriptions from aerospace to code domain. For each technical noun category, list 10 concrete code-domain examples.", "output_prefix": "domain-adapt"},
]

# Process refined files in groups of 3
BATCH_SIZE = 3
batches = [refined_files[i:i+BATCH_SIZE] for i in range(0, min(len(refined_files), len(AREAS)*BATCH_SIZE), BATCH_SIZE)]

for batch_idx, (area, batch_files) in enumerate(zip(AREAS, batches)):
    print(f"\n=== Area: {area['name']} (batch {batch_idx+1}/{len(AREAS)}) ===")
    
    # Read the refined content for this batch
    refined_content = ""
    for rf in batch_files:
        with open(os.path.join(REFINED_DIR, rf)) as f:
            refined_content += f"\n### FILE: {rf}\n{f.read()}\n"
    
    worker_prompt = f"""{AGENT_PROMPT}

## ENRICHMENT TASK
Area: {area['name']}
Task: {area['desc']}

## REFINED CONTENT (INPUT)
{refined_content[:15000]}

## OUTPUT
Write ONLY the enrichment JSON to stdout. Format:
{{"area": "{area['name']}", "batch": {batch_idx+1}, "entries": [{{"rule": "...", "ste_example": "...", "non_ste_example": "..."}}, ...]}}
"""
    
    out_file = os.path.join(OUT_DIR, f"{area['output_prefix']}-batch-{batch_idx+1:03d}.json")
    
    # Write prompt to temp file
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, dir='/tmp')
    tmp.write(worker_prompt)
    tmp.close()
    
    print(f"  Launching worker → {os.path.basename(out_file)}")
    
    pid = os.fork()
    if pid == 0:
        os.chdir(OUT_DIR)
        with open(out_file, 'w') as outf:
            os.dup2(outf.fileno(), 1)
            os.dup2(outf.fileno(), 2)
        os.execvp("hermes", ["hermes", "-z", worker_prompt, "-m", MODEL, "--yolo"])
        os._exit(1)
    
    print(f"  PID: {pid}")
    time.sleep(0.5)

print(f"\nAll {len(AREAS)} enrichment workers launched.")
print(f"Output: {OUT_DIR}/")
print("Monitor: ps aux | grep hermes")
