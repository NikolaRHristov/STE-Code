#!/usr/bin/env python3
"""Single-worker diagnostic: capture full oneshot output and inspect."""
import os, sys, time, subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent

# Import extract_batch functions
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "extraction"))
from extract_batch import parse_manifest, worker_page_range, build_prompt, verify_output

# Import agent runner from venv site-packages
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from agent_runner import get_agent_config, _resolve_command

worker_num = int(sys.argv[1]) if len(sys.argv) > 1 else 54
start_pos, end_pos = worker_page_range(worker_num)
mapping = parse_manifest()
prompt, output_path = build_prompt(worker_num, start_pos, end_pos, mapping)

output_file = Path(output_path)
if output_file.exists():
    output_file.unlink()

model = "poolside/laguna-s-2.1:free"
agent_cfg = get_agent_config("hermes")

# Write prompt to temp file
tmp = PROJECT / ".agents" / "tmp"
tmp.mkdir(parents=True, exist_ok=True)
prompt_file = tmp / f"diag-prompt-{os.getpid()}.txt"
prompt_file.write_text(prompt)

runtime = os.path.expanduser(agent_cfg["runtime"])
tools_dir = PROJECT / ".agents" / "tools"
wrapper = str((tools_dir / agent_cfg["wrapper"]).resolve())

cmd = [runtime, wrapper, str(prompt_file), "--model", model]
env = {**os.environ, **agent_cfg.get("env", {})}

print(f"Worker: W{worker_num:03d}  Pages: {start_pos}-{end_pos}", flush=True)
print(f"Output: {output_path}", flush=True)
print(f"Prompt size: {len(prompt)} bytes", flush=True)
print(f"\n=== RUNNING ONESHOT ===", flush=True)

start = time.time()
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env, cwd=str(PROJECT))
duration = time.time() - start

print(f"\n=== DONE in {duration:.1f}s ===", flush=True)
print(f"Exit code: {result.returncode}", flush=True)
print(f"Stdout length: {len(result.stdout)} chars", flush=True)
print(f"Stderr length: {len(result.stderr)} chars", flush=True)

if result.stderr:
    print(f"\n--- STDERR ---\n{result.stderr[:3000]}", flush=True)

if result.stdout:
    print(f"\n--- STDOUT (first 6000 chars) ---\n{result.stdout[:6000]}", flush=True)

if output_file.exists():
    content = output_file.read_text()
    lines = content.splitlines()
    print(f"\n=== OUTPUT FILE EXISTS ===", flush=True)
    print(f"Size: {output_file.stat().st_size} bytes, Lines: {len(lines)}", flush=True)
    print(f"\n--- FIRST 10 LINES ---", flush=True)
    print('\n'.join(lines[:10]), flush=True)
    print(f"\n--- LAST 20 LINES ---", flush=True)
    print('\n'.join(lines[-20:]), flush=True)
    ok, msg = verify_output(worker_num, start_pos, end_pos, str(output_file))
    print(f"\nVerification: {'PASS' if ok else 'FAIL'} — {msg}", flush=True)
else:
    print(f"\n❌ OUTPUT FILE NOT CREATED", flush=True)
    if result.stdout:
        print(f"\n--- FULL STDOUT ---\n{result.stdout[:8000]}", flush=True)
