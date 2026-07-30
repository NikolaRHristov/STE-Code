#!/usr/bin/env python3
"""STE-Code Rails Compliance Checker — verifies pipeline integrity."""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
EXTRACTED = os.path.join(ROOT, "extracted")
REFINED = os.path.join(ROOT, "refined")

def check_r1_extraction():
    files = [f for f in os.listdir(EXTRACTED) if f.startswith("w") and f.endswith(".md")]
    return len(files) == 109, f"{len(files)}/109 files"

def check_r2_refinement():
    files = [f for f in os.listdir(REFINED) if f.startswith("r") and f.endswith(".md")]
    return len(files) == 109, f"{len(files)}/109 files"

def check_r3_page_coverage():
    files = sorted([f for f in os.listdir(EXTRACTED) if f.startswith("w")])
    pages = []
    for f in files:
        parts = f.replace(".md","").split("-p")
        if len(parts) == 2:
            try: pages.append((int(parts[1].split("-")[0]), int(parts[1].split("-")[1])))
            except: pass
    if not pages: return False, "no files found"
    pages.sort()
    gaps = []
    expected = 1
    for s, e in pages:
        if s != expected: gaps.append(f"gap at {expected} (file starts at {s})")
        expected = e + 1
    return len(gaps) == 0, f"pages 1-{pages[-1][1]}, {len(gaps)} gaps" if gaps else f"pages 1-{pages[-1][1]}, no gaps"

def check_r4_size():
    small = [f for f in os.listdir(EXTRACTED) if f.endswith(".md") and os.path.getsize(os.path.join(EXTRACTED, f)) < 500]
    return len(small) == 0, f"{len(small)} files under 500 bytes" if small else "all > 500 bytes"

CHECKS = [
    ("R1 — Extraction Count", check_r1_extraction),
    ("R2 — Refinement Count", check_r2_refinement),
    ("R3 — Page Coverage", check_r3_page_coverage),
    ("R4 — File Size", check_r4_size),
]

if __name__ == "__main__":
    all_pass = True
    for name, fn in CHECKS:
        ok, detail = fn()
        status = "✅ PASS" if ok else "❌ FAIL"
        print(f"{status}  {name}: {detail}")
        if not ok: all_pass = False
    sys.exit(0 if all_pass else 1)
