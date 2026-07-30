#!/usr/bin/env python3
"""Generate enrichment prompts for adapted files — 6 batches."""
import os, re, glob

PROMPTS_DIR = ".agents/prompts/enrich-adapt"
os.makedirs(PROMPTS_DIR, exist_ok=True)

base_prompt = open(".agents/prompts/enrich-adapt.txt").read()

files = sorted(glob.glob("ste-code/adapted/a-*.md"))
BATCH_SIZE = 10
batches = [files[i:i+BATCH_SIZE] for i in range(0, len(files), BATCH_SIZE)]

for i, batch in enumerate(batches):
    file_list = "\n".join(f"- {f}" for f in batch)
    prompt = base_prompt.replace(
        "Read every adapted file (a-sec1-rule1.1.md through a-sec9-gr4.md).",
        f"Read these specific files:\n{file_list}"
    )
    path = os.path.join(PROMPTS_DIR, f"enrich-adapt-batch{i+1:02d}.txt")
    with open(path, 'w') as f:
        f.write(prompt)

print(f"Generated {len(batches)} batches in {PROMPTS_DIR}/")
for i in range(len(batches)):
    print(f"  Batch {i+1}: {len(batches[i])} files")
