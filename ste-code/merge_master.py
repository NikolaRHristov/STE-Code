#!/usr/bin/env python3
"""Stage 3: Merge enriched files into master.md with dedup and section organization."""
import os, re, glob

INPUT_DIR = "ste-code/enriched"
MERGED_DIR = "ste-code/merged"
os.makedirs(MERGED_DIR, exist_ok=True)

# Fall back to extracted if enriched not complete
enriched_count = len(glob.glob(f"{INPUT_DIR}/w*-p*.md"))
if enriched_count < 109:
    INPUT_DIR = "ste-code/extracted"
    print(f"Enriched incomplete ({enriched_count}/109), using {INPUT_DIR}")

# Step 1: Concatenate in page order
files = sorted(glob.glob(f"{INPUT_DIR}/w*-p*.md"))
print(f"Concatenating {len(files)} files from {INPUT_DIR}...")

with open(f"{MERGED_DIR}/master-raw.md", "w") as out:
    for f in files:
        with open(f) as inf:
            content = inf.read()
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")
            out.write("\n---\n\n")

raw_size = os.path.getsize(f"{MERGED_DIR}/master-raw.md")
print(f"master-raw.md: {raw_size:,} bytes")

# Step 2: Read raw, deduplicate, organize
with open(f"{MERGED_DIR}/master-raw.md") as f:
    text = f.read()

# Remove page separators
text = re.sub(r'\n---\n+', '\n', text)

# Remove duplicate metadata headers
text = re.sub(r'(<!-- section:.*?verified: true -->\n?)+', '', text)

# Count content
rule_count = len(re.findall(r'(?:^|\n)(?:#{1,4}\s*)?Rule\s+\d+\.\d+', text))
cat_count = len(re.findall(r'(?:^|\n)(?:#{1,4}\s*)?Category\s+\d+', text))

# Write organized master
with open(f"{MERGED_DIR}/master.md", "w") as out:
    out.write("# ASD-STE100 Issue 9 — Master Extraction\n\n")
    out.write(f"> **Source:** {len(files)} enriched files from {INPUT_DIR}/\n")
    out.write(f"> **Pages:** 1-434 | **Rules:** ~{rule_count} | **Categories:** ~{cat_count}\n")
    out.write(f"> **Generated:** 2026-07-30 by Agent #1 continuation\n\n")
    out.write(text)

master_size = os.path.getsize(f"{MERGED_DIR}/master.md")
print(f"master.md: {master_size:,} bytes")
print(f"Rules detected: {rule_count}, Categories detected: {cat_count}")
print("Merge complete.")
