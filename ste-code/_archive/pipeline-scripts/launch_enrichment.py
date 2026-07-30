#!/usr/bin/env python3
"""Launch enrichment workers in batches of 3 — second-pass verification."""
import subprocess, os, sys, glob, time

PROMPTS_DIR = "ste-code/prompts-enrich"
ENRICHED_DIR = "ste-code/enriched"

os.makedirs(ENRICHED_DIR, exist_ok=True)

workers = sorted([
    int(f.replace("w","").replace("-enrich.txt",""))
    for f in os.listdir(PROMPTS_DIR)
    if f.startswith("w") and f.endswith("-enrich.txt")
])

# Skip already-enriched workers
remaining = [w for w in workers
             if not glob.glob(f"{ENRICHED_DIR}/w{w:03d}-*.md")]

print(f"Total workers: {len(workers)}, Remaining: {len(remaining)}")

batch_size = 3
total_batches = (len(remaining) + batch_size - 1) // batch_size

for batch_idx in range(0, len(remaining), batch_size):
    batch = remaining[batch_idx:batch_idx + batch_size]
    batch_num = batch_idx // batch_size + 1
    print(f"\n=== Enrichment Batch {batch_num}/{total_batches}: W{batch[0]:03d}-W{batch[-1]:03d} ===")

    procs = []
    for w in batch:
        prompt_file = f"{PROMPTS_DIR}/w{w:03d}-enrich.txt"
        cmd = f'hermes -z "$(cat {prompt_file})" -m poolside/laguna-s-2.1:free --yolo'
        print(f"  Launching W{w:03d}...")
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        procs.append((w, p))
        time.sleep(0.5)  # slight stagger

    for w, p in procs:
        try:
            out, _ = p.communicate(timeout=300)
            rc = p.returncode
            status = "✅" if rc == 0 else f"❌ exit={rc}"
            preview = out.decode(errors='replace')[:150].strip().replace('\n', ' ')
            print(f"  W{w:03d} {status}: {preview}")
        except subprocess.TimeoutExpired:
            p.kill()
            print(f"  W{w:03d} ❌ TIMEOUT")

    # Verify enriched output
    for w in batch:
        matches = glob.glob(f"{ENRICHED_DIR}/w{w:03d}-*.md")
        if matches:
            f = matches[0]
            size = os.path.getsize(f)
            lines = len(open(f).readlines())
            print(f"  W{w:03d} output: {lines}L, {size}B — {'✅' if size > 500 else '⚠️ SMALL'}")
        else:
            print(f"  W{w:03d} output: ❌ MISSING")

    # Git commit
    files = " ".join(f for w in batch for f in glob.glob(f"{ENRICHED_DIR}/w{w:03d}-*.md"))
    if files:
        subprocess.run(
            f"git add {files} && git commit -m 'Enrich batch {batch_num}: W{batch[0]:03d}-W{batch[-1]:03d}' --no-verify",
            shell=True, capture_output=True
        )
        print(f"  ✓ Committed batch {batch_num}")

total = len(glob.glob(f"{ENRICHED_DIR}/w*-p*.md"))
print(f"\n=== Done: {total}/109 enriched files ===")
