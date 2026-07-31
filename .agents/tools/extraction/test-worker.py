#!/usr/bin/env python3
"""Test a single worker extraction with full verbose output."""
import os, sys, time, json, subprocess
from pathlib import Path

PROJECT = Path("/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code")
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))

# Import
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())

# Now import from extract_batch
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "extraction"))
from extract_batch import parse_manifest, worker_page_range, build_prompt, verify_output

worker_num = int(sys.argv[1]) if len(sys.argv) > 1 else 52
start_pos, end_pos = worker_page_range(worker_num)
mapping = parse_manifest()

prompt, output_path = build_prompt(worker_num, start_pos, end_pos, mapping)
print(f"=== TEST WORKER ===", flush=True)
print(f"Worker: W{worker_num:03d}", flush=True)
print(f"Pages: {start_pos}-{end_pos}", flush=True)
print(f"Output: {output_path}", flush=True)
print(f"Prompt size: {len(prompt)} bytes", flush=True)
print(f"Prompt preview:\n{prompt[:500]}...", flush=True)

# Remove existing file
output_file = Path(output_path)
if output_file.exists():
    output_file.unlink()

# Run via agent-runner's run_agent
start = time.time()
print(f"\n=== STARTING AGENT RUN ===", flush=True)
result = run_agent(
    prompt,
    agent="hermes",
    model="poolside/laguna-s-2.1:free",
    cwd=str(PROJECT),
    timeout=300,
)
duration = time.time() - start

print(f"\n=== AGENT COMPLETED in {duration:.1f}s ===", flush=True)
print(f"Exit code: {result.returncode}", flush=True)
print(f"Stdout size: {len(result.stdout or '')} chars", flush=True)
print(f"Stderr size: {len(result.stderr or '')} chars", flush=True)
if result.stderr:
    print(f"\n=== STDERR ===\n{result.stderr[:2000]}", flush=True)
if result.stdout:
    print(f"\n=== STDOUT ===\n{result.stdout[:2000]}", flush=True)

# Check output file
if output_file.exists():
    content = output_file.read_text()
    print(f"\n=== OUTPUT FILE ===", flush=True)
    print(f"Size: {output_file.stat().st_size} bytes", flush=True)
    print(f"Lines: {len(content.splitlines())}", flush=True)
    print(f"\n=== FIRST 5 LINES ===", flush=True)
    print('\n'.join(content.splitlines()[:5]), flush=True)
    print(f"\n=== LAST 15 LINES ===", flush=True)
    print('\n'.join(content.splitlines()[-15:]), flush=True)
    
    ok, msg = verify_output(worker_num, start_pos, end_pos, str(output_file))
    print(f"\n=== VERIFICATION ===", flush=True)
    print(f"Result: {'PASS' if ok else 'FAIL'}", flush=True)
    print(f"Message: {msg}", flush=True)
else:
    print(f"\n❌ OUTPUT FILE NOT CREATED", flush=True)
    print(f"\n=== Full stdout ===", flush=True)
    if result.stdout:
        print(result.stdout[:5000], flush=True)
