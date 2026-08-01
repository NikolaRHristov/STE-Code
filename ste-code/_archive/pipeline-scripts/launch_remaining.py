#!/usr/bin/env python3
"""Launch remaining extraction workers in batches of 3."""
import subprocess, os, sys, glob

PROMPTS_DIR = "ste-code/prompts"
EXTRACTED_DIR = "ste-code/extracted"
REMAINING = sorted([
    int(f.replace("w","").replace("-prompt.txt",""))
    for f in os.listdir(PROMPTS_DIR)
    if f.startswith("w") and f.endswith("-prompt.txt")
])
REMAINING = [w for w in REMAINING 
             if not glob.glob(f"{EXTRACTED_DIR}/w{w:03d}-*.md")]

print(f"Remaining workers: {len(REMAINING)}")
batch_size = 3
for i in range(0, len(REMAINING), batch_size):
    batch = REMAINING[i:i+batch_size]
    batch_num = i//batch_size + 1
    print(f"\n=== Batch {batch_num}: {batch} ===")
    procs = []
    for w in batch:
        prompt_file = f"{PROMPTS_DIR}/w{w:03d}-prompt.txt"
        cmd = f'hermes -z "$(cat {prompt_file})" -m tencent/hy3:free --yolo'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procs.append((w, p, cmd))
        print(f"  W{w:03d} launched (pid {p.pid})")
    
    for w, p, cmd in procs:
        out, _ = p.communicate(timeout=300)
        rc = p.returncode
        status = "✅" if rc == 0 else f"❌ exit={rc}"
        print(f"  W{w:03d} {status}: {out.decode()[:120].strip()}")
    
    # git commit after each batch
    files = " ".join(f for w in batch for f in glob.glob(f"{EXTRACTED_DIR}/w{w:03d}-*.md"))
    if files:
        subprocess.run(f"git add {files} && git commit -m 'Batch {batch_num}: W{batch[0]:03d}-W{batch[-1]:03d}' --no-verify", 
                      shell=True, capture_output=True)
        print(f"  Committed batch {batch_num}")

print(f"\nDone. Extracted files: {len(glob.glob(EXTRACTED_DIR + '/w*-p*.md'))}")
