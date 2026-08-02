#!/usr/bin/env python3
"""Telemetry wrapper for hermes -z oneshot workers.

Usage:
  python3 .agents/tools/shared/telemetry-worker.py <worker-id> <prompt-file> [--model MODEL] [--output OUTPUT_FILE]

Wraps `hermes -z "$(cat prompt.txt)" -m MODEL --yolo` with structured telemetry.
Writes telemetry to `.agents/telemetry/<worker-id>-<timestamp>.json`.

Output:
  {
    "worker_id": "b1-004",
    "invocation": "hermes -z $(cat .agents/prompts/expansion-pass1/pass1-batch-004.txt) -m poolside/laguna-s-2.1:free --yolo",
    "prompt_file": ".agents/prompts/expansion-pass1/pass1-batch-004.txt",
    "prompt_size_bytes": 11973,
    "model": "poolside/laguna-s-2.1:free",
    "reasoning_effort": "high",
    "start_time": "2026-07-30T07:15:00Z",
    "end_time": "2026-07-30T07:15:45Z",
    "duration_seconds": 45.2,
    "exit_code": 0,
    "output_file": "ste-code/adapted/expanded/pass1-batch-004.json",
    "output_exists": true,
    "output_size_bytes": 3847,
    "output_valid_json": true,
    "output_entry_count": 5,
    "self_healing": {
      "blacklist_hits": 0,
      "aerospace_terms_found": 0,
      "duplicate_entries": 0,
      "retries": 0,
      "status": "PASS"
    },
    "errors": [],
    "stderr_snippet": ""
  }
"""
import os, sys, json, time, subprocess, re
from datetime import datetime, timezone

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
TELEMETRY_DIR = os.path.join(PROJECT, ".agents", "telemetry")
os.makedirs(TELEMETRY_DIR, exist_ok=True)

def load_reasoning_effort():
    """Read reasoning_effort from hermes config."""
    config_path = os.path.expanduser("~/.hermes/config.yaml")
    try:
        with open(config_path) as f:
            for line in f:
                m = re.match(r'\s*reasoning_effort:\s*(\S+)', line)
                if m:
                    return m.group(1)
    except:
        pass
    return "unknown"

def validate_json_output(filepath):
    """Check if output file is valid JSON and count entries."""
    try:
        with open(filepath) as f:
            data = json.load(f)
        entries = data.get("entries", data) if isinstance(data, dict) else data
        count = len(entries) if isinstance(entries, list) else 1
        return True, count
    except:
        return False, 0

def check_self_healing(filepath):
    """Scan output for self-healing signals."""
    healing = {"blacklist_hits": 0, "aerospace_terms_found": 0, "duplicate_entries": 0, "retries": 0, "status": "PASS"}
    try:
        with open(filepath) as f:
            content = f.read().lower()
        aerospace = ["aircraft", "engine", "ream", "flange", "screw", "actuator", "fuselage", "landing gear", "aero plane", "aero engine"]
        for term in aerospace:
            if re.search(r'\b' + re.escape(term) + r'\b', content):
                healing["aerospace_terms_found"] += 1
        if healing["aerospace_terms_found"] > 0:
            healing["status"] = "WARN"
    except:
        healing["status"] = "UNREADABLE"
    return healing

def main():
    if len(sys.argv) < 3:
        print("Usage: telemetry-worker.py <worker-id> <prompt-file> [--model MODEL] [--output OUTPUT_FILE]")
        sys.exit(1)

    worker_id = sys.argv[1]
    prompt_file = sys.argv[2]
    model = "poolside/laguna-s-2.1:free"
    output_file = None

    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    # Read prompt
    try:
        with open(prompt_file) as f:
            prompt_content = f.read()
        prompt_size = len(prompt_content)
    except Exception as e:
        print(f"ERROR: Cannot read prompt file {prompt_file}: {e}")
        sys.exit(1)

    # Build invocation
    invocation = f"hermes -z \"$(cat {prompt_file})\" -m {model} --yolo"

    # Telemetry record
    reasoning = load_reasoning_effort()
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    telemetry = {
        "worker_id": worker_id,
        "invocation": invocation,
        "prompt_file": prompt_file,
        "prompt_size_bytes": prompt_size,
        "model": model,
        "reasoning_effort": reasoning,
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": None,
        "duration_seconds": None,
        "exit_code": None,
        "output_file": output_file,
        "output_exists": False,
        "output_size_bytes": 0,
        "output_valid_json": False,
        "output_entry_count": 0,
        "self_healing": {},
        "errors": [],
        "stderr_snippet": ""
    }

    print(f"[telemetry] worker={worker_id} model={model} reasoning={reasoning} prompt={prompt_size}B")

    # Launch worker
    start = time.time()
    telemetry_path = os.path.join(TELEMETRY_DIR, f"{worker_id}-{timestamp}.json")

    try:
        result = subprocess.run(
            ["hermes", "-z", prompt_content, "-m", model, "--yolo"],
            capture_output=True, text=True,
            cwd=PROJECT,
            timeout=600
        )
        duration = time.time() - start
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["exit_code"] = result.returncode
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()

        if result.stderr:
            telemetry["stderr_snippet"] = result.stderr[:500]

        if result.stdout:
            errors = [l for l in result.stdout.split("\n") if "error" in l.lower() or "fail" in l.lower() or "traceback" in l.lower()]
            if errors:
                telemetry["errors"] = errors[:10]

        # Verify output
        if output_file:
            full_output = os.path.join(PROJECT, output_file) if not os.path.isabs(output_file) else output_file
            if os.path.exists(full_output):
                telemetry["output_exists"] = True
                telemetry["output_size_bytes"] = os.path.getsize(full_output)
                valid, count = validate_json_output(full_output)
                telemetry["output_valid_json"] = valid
                telemetry["output_entry_count"] = count
                telemetry["self_healing"] = check_self_healing(full_output)
            else:
                telemetry["errors"].append(f"Output file not found: {full_output}")

        status = "PASS" if result.returncode == 0 and telemetry["output_exists"] else "FAIL"
        print(f"[telemetry] {status} duration={duration:.1f}s exit={result.returncode} output={'found' if telemetry['output_exists'] else 'MISSING'} size={telemetry['output_size_bytes']}B entries={telemetry['output_entry_count']}")

    except subprocess.TimeoutExpired:
        duration = time.time() - start
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["exit_code"] = -1
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()
        telemetry["errors"].append("TIMEOUT: worker exceeded 600s limit")
        print(f"[telemetry] TIMEOUT after {duration:.0f}s")

    except Exception as e:
        duration = time.time() - start
        telemetry["duration_seconds"] = round(duration, 1)
        telemetry["exit_code"] = -2
        telemetry["end_time"] = datetime.now(timezone.utc).isoformat()
        telemetry["errors"].append(f"EXCEPTION: {str(e)}")
        print(f"[telemetry] ERROR: {e}")

    # Write telemetry
    with open(telemetry_path, "w") as f:
        json.dump(telemetry, f, indent=2)

    return telemetry["exit_code"] if telemetry["exit_code"] and telemetry["exit_code"] > 0 else (1 if not telemetry["output_exists"] else 0)

if __name__ == "__main__":
    sys.exit(main())
