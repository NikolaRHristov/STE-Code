#!/usr/bin/env python3
"""Generate 109 extraction worker prompts for the STE-Code pipeline."""
import os

OUTPUT_DIR = "ste-code/prompts"
SPEC_DIR = "spec/issue-09-2025"
WORKERS = 109
PAGES_PER_WORKER = 4

os.makedirs(OUTPUT_DIR, exist_ok=True)

template = (
    "Read {spec}/page-{start:04d}.md through page-{end:04d}.md. "
    "Extract ALL content exactly into ste-code/extracted/w{wnum:03d}-p{start}-{end}.md. "
    "Do not summarize. Include every word, every table, every example. "
    "Output ONLY the markdown file."
)

count = 0
for wnum in range(1, WORKERS + 1):
    start = (wnum - 1) * PAGES_PER_WORKER + 1
    end = min(start + PAGES_PER_WORKER - 1, 434)
    if start > 434:
        break
    prompt = template.format(spec=SPEC_DIR, start=start, end=end, wnum=wnum)
    outfile = os.path.join(OUTPUT_DIR, f"w{wnum:03d}-prompt.txt")
    with open(outfile, "w") as f:
        f.write(prompt + "\n")
    count += 1

print(f"Generated {count} prompt files in {OUTPUT_DIR}/")
