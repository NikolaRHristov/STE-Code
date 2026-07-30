#!/usr/bin/env python3
"""Improved Refinement Orchestrator — launches workers with pre/post quality gates."""
import os, subprocess, sys, time
from pathlib import Path

PROMPTS_DIR = ".agents/prompts/refine"
MODEL = "deepseek-v4-pro"
BATCH_SIZE = 3

def get_batches():
    """Get all prompt files, sorted."""
    prompt_files = sorted(Path(PROMPTS_DIR).glob("refine-*.txt"))
    batches = []
    for i in range(0, len(prompt_files), BATCH_SIZE):
        batches.append(prompt_files[i:i+BATCH_SIZE])
    return batches

def launch_batch(batch_files):
    """Launch a batch of workers in background."""
    processes = []
    for pf in batch_files:
        cmd = f'hermes -z "$(cat {pf})" -m {MODEL} --yolo'
        proc = subprocess.Popen(
            cmd, shell=True, cwd=os.getcwd(),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        processes.append((pf.name, proc))
        print(f"  Launched: {pf.name} (PID {proc.pid})")
    return processes

def wait_batch(processes, timeout=300):
    """Wait for all processes in batch to complete."""
    for name, proc in processes:
        try:
            proc.wait(timeout=timeout)
            if proc.returncode == 0:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name} (exit {proc.returncode})")
        except subprocess.TimeoutExpired:
            print(f"  ⏰ {name} TIMEOUT — killing")
            proc.kill()

def verify_batch(batch_num):
    """Run quality audit on refined files."""
    result = subprocess.run(
        ["python3", "ste-code/audit_refinement.py"],
        capture_output=True, text=True
    )
    if "Needs work (<80): 0" in result.stdout:
        print(f"  🟢 Batch {batch_num} quality: PASS")
        return True
    else:
        print(f"  🔴 Batch {batch_num} quality: ISSUES DETECTED")
        # Print the needs-work files
        for line in result.stdout.split('\n'):
            if '/100' in line:
                print(f"    {line.strip()}")
        return False

def main():
    batches = get_batches()
    print(f"Refinement Orchestrator — {len(batches)} batches of {BATCH_SIZE}")
    print(f"Model: {MODEL} | Prompts: {PROMPTS_DIR}")
    print()
    
    # Pre-flight: verify source files exist
    extracted = len(list(Path("ste-code/extracted").glob("w*-p*.md")))
    enriched = len(list(Path("ste-code/enriched").glob("w*-p*.md")))
    print(f"Pre-flight: {extracted} extracted, {enriched} enriched source files")
    if extracted < 100 and enriched < 100:
        print("❌ Not enough source files — aborting")
        sys.exit(1)
    print()
    
    for i, batch in enumerate(batches):
        batch_num = i + 1
        print(f"=== Batch {batch_num}/{len(batches)} ===")
        
        # Launch
        processes = launch_batch(batch)
        
        # Wait
        wait_batch(processes)
        
        # Verify
        verify_batch(batch_num)
        
        # Optional: commit after each batch
        if batch_num % 5 == 0:
            subprocess.run(["git", "add", "ste-code/refined/"], cwd=os.getcwd())
            subprocess.run(["git", "commit", "-m", f"refine-v2: Batch {batch_num} verified"], cwd=os.getcwd())
        
        print()
    
    print("=== ALL BATCHES COMPLETE ===")
    # Final audit
    subprocess.run(["python3", "ste-code/audit_refinement.py"], cwd=os.getcwd())

if __name__ == '__main__':
    main()
