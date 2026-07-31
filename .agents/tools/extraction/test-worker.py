#!/usr/bin/env python3
"""Single-worker diagnostic: run oneshot wrapper directly with full output capture.
Usage: python3 test-worker.py <worker_num>
"""
import os, sys, time, subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "extraction"))
from extract_batch import parse_manifest, worker_page_range, build_prompt, verify_output

worker_num = int(sys.argv[1]) if len(sys.argv) > 1 else 54
start_pos, end_pos = worker_page_range(worker_num)
mapping = parse_manifest()
prompt, output_path = build_prompt(worker_num, start_pos, end_pos, mapping)

output_file = Path(output_path)
if output_file.exists():
    output_file.unlink()

model = "poolside/laguna-s-2.1:free"
venv_python = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
wrapper = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")

tmp = PROJECT / ".agents" / "tmp"
tmp.mkdir(parents=True, exist_ok=True)
prompt_file = tmp / f"diag-prompt-{os.getpid()}.txt"
prompt_file.write_text(prompt)

cmd = [venv_python, wrapper, str(prompt_file), "--model", model]
env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "120"}

print(f"W{worker_num:03d}  Pages: {start_pos}-{end_pos}  Prompt: {len(prompt)}B", flush=True)
print(f"Running oneshot wrapper...", flush=True)

start = time.time()
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=150, env=env, cwd=str(PROJECT))
    duration = time.time() - start
    print(f"\nDone in {duration:.1f}s  Exit: {result.returncode}", flush=True)
    print(f"Stdout: {len(result.stdout)} chars  Stderr: {len(result.stderr)} chars", flush=True)
    if result.stderr:
        print(f"\n--- STDERR ---\n{result.stderr[:2000]}", flush=True)
    if result.stdout:
        print(f"\n--- STDOUT ---\n{result.stdout[:2000]}", flush=True)

    if output_file.exists():
        content = output_file.read_text()
        lines = content.splitlines()
        print(f"\n=== OUTPUT FILE ===\n{output_file.stat().st_size}B, {len(lines)} lines", flush=True)
        print(f"\n--- FIRST 5 ---\n{chr(10).join(lines[:5])}", flush=True)
        print(f"\n--- LAST 10 ---\n{chr(10).join(lines[-10:])}", flush=True)
        ok, msg = verify_output(worker_num, start_pos, end_pos, str(output_file))
        print(f"\nVerification: {'PASS' if ok else 'FAIL'} — {msg}", flush=True)
    else:
        print(f"\n❌ OUTPUT FILE NOT CREATED", flush=True)
        if result.stdout:
            print(f"stdout: {result.stdout[:3000]}", flush=True)
        if result.stderr:
            print(f"stderr: {result.stderr[:3000]}", flush=True)
except subprocess.TimeoutExpired as e:
    duration = time.time() - start
    print(f"\n⏰ TIMEOUT after {duration:.1f}s", flush=True)
    out = e.stdout or ""
    err = e.stderr or ""
    if isinstance(out, bytes): out = out.decode('utf-8', errors='replace')
    if isinstance(err, bytes): err = err.decode('utf-8', errors='replace')
    if out: print(f"Stdout: {out[:2000]}", flush=True)
    if err: print(f"Stderr: {err[:2000]}", flush=True)
