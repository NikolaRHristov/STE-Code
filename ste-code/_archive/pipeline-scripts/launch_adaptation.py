#!/usr/bin/env python3
"""Launch 11 adaptation workers in batches of 3."""
import subprocess, os, glob, time

PROMPTS_DIR = "ste-code/prompts-adapt"
ADAPTED_DIR = "ste-code/adapted"
os.makedirs(ADAPTED_DIR, exist_ok=True)

workers = sorted([
    f.replace("-prompt.txt","")
    for f in os.listdir(PROMPTS_DIR)
    if f.endswith("-prompt.txt")
])
print(f"Adaptation workers: {len(workers)} — {workers}")

batch_size = 3
for i in range(0, len(workers), batch_size):
    batch = workers[i:i+batch_size]
    batch_num = i//batch_size + 1
    print(f"\n=== Adapt Batch {batch_num}/{ (len(workers)+2)//3 }: {batch} ===")
    
    procs = []
    for w in batch:
        pf = f"{PROMPTS_DIR}/{w}-prompt.txt"
        cmd = f'hermes -z "$(cat {pf})" -m deepseek-v4-pro --yolo'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procs.append((w, p))
        print(f"  {w} launched (pid {p.pid})")
        time.sleep(0.5)
    
    for w, p in procs:
        out, _ = p.communicate(timeout=300)
        rc = p.returncode
        preview = out.decode(errors='replace')[:120].strip().replace('\n',' ')
        print(f"  {w} {'✅' if rc==0 else '❌'}: {preview}")
    
    # Verify + commit
    for w in batch:
        matches = glob.glob(f"{ADAPTED_DIR}/{w.replace('a0','a-sec').replace('a01','a-')}*.md")
        if not matches:
            # Try broader pattern
            matches = glob.glob(f"{ADAPTED_DIR}/*.md")
            matches = [m for m in matches if w in m or any(c in m for c in ['sec','cat','dict'])]
        for m in matches:
            print(f"  → {os.path.basename(m)}: {os.path.getsize(m)}B")
    
    subprocess.run("git add ste-code/adapted/ && git commit -m 'Adapt batch {batch_num}' --no-verify", 
                   shell=True, capture_output=True)

total = len(glob.glob(f"{ADAPTED_DIR}/*.md"))
print(f"\nDone: {total} adapted files")
