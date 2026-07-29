#!/usr/bin/env python3
"""Extract text from ASD-STE100 Conversation.pdf into markdown files."""

import pdfplumber
import os

PDF_PATH = "/Volumes/CORSAIR/Developer/macOS/Application/Manual/ASD-STE100 Conversation.pdf"
OUT_DIR = "/Volumes/CORSAIR/Developer/macOS/Application/Manual/extracted"

os.makedirs(OUT_DIR, exist_ok=True)

pdf = pdfplumber.open(PDF_PATH)
total_pages = len(pdf.pages)
print(f"Total pages: {total_pages}")

all_text = []
for i, page in enumerate(pdf.pages):
    text = page.extract_text() or ""
    all_text.append(f"## Page {i+1} of {total_pages}\n\n{text}\n")
    print(f"Page {i+1}: {len(text)} chars")

pdf.close()

# Write full text as single file
full_path = os.path.join(OUT_DIR, "asd_ste100_full.txt")
with open(full_path, "w", encoding="utf-8") as f:
    for section in all_text:
        f.write(section)
        f.write("\n---\n\n")

print(f"\nFull text written to: {full_path}")
print(f"Total chars: {sum(len(s) for s in all_text)}")

# Also split into chunks of 10 pages for easier handling
chunk_size = 10
for chunk_start in range(0, len(all_text), chunk_size):
    chunk_end = min(chunk_start + chunk_size, len(all_text))
    chunk = all_text[chunk_start:chunk_end]
    chunk_path = os.path.join(OUT_DIR, f"asd_ste100_pages_{chunk_start+1:03d}_to_{chunk_end:03d}.txt")
    with open(chunk_path, "w", encoding="utf-8") as f:
        for section in chunk:
            f.write(section)
            f.write("\n---\n\n")
    print(f"Chunk written: {chunk_path} ({len(''.join(chunk))} chars)")
