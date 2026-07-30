#!/usr/bin/env python3
"""Agent #8 — Enlarge ste-code from refined content using BATCHED POLL WORKERS.
Same pattern as Agent #1: 3 workers per batch, poll for completion, verify, save state."""
import subprocess, os, tempfile, time, sys, json, glob

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
REFINED_DIR = os.path.join(PROJECT, "ste-code", "refined")
OUT_DIR = os.path.join(PROJECT, "ste-code", "enriched-code")
STATE_FILE = os.path.join(PROJECT, ".agents", "state", "ENLARGE-PROGRESS.md")
MODEL = "deepseek-v4-pro"
BATCH_SIZE = 3

os.makedirs(OUT_DIR, exist_ok=True)

# Load the extension worker agent prompt
with open(os.path.join(PROJECT, ".agents/agent/agent-8-extension-worker.md")) as f:
    AGENT_PROMPT = f.read()

# Get refined files, group by section
refined_files = sorted([f for f in os.listdir(REFINED_DIR) if f.endswith('.md')])

# Enrichment passes — each pass processes a set of refined files in batches
PASSES = [
    {
        "name": "code-examples",
        "desc": "Read the refined content. For each rule found, generate 3 STE/non-STE code documentation example pairs. Replace all aerospace terms (engine, aircraft, ream, flange) with code-domain equivalents (server, API, function, endpoint). Output JSON with entries: [{rule, ste_example, non_ste_example}].",
        "output_prefix": "ce",
        "files_per_batch": 10
    },
    {
        "name": "dictionary-expand",
        "desc": "Read the refined content. Find every aerospace dictionary term. For each, suggest a code-domain equivalent or mark as N/A. Generate code-domain approved terms with definitions and STE/non-STE examples. Output JSON with entries: [{term, type, definition, ste_example, non_ste_example}].",
        "output_prefix": "de",
        "files_per_batch": 20
    },
    {
        "name": "domain-adapt",
        "desc": "Read the refined content. For each technical category and section, generate 5 concrete code-domain examples. Map the aerospace safety system (WARNING/CAUTION) to code equivalents (BREAKING/DEPRECATED/NOTE). Output JSON with entries: [{category, aerospace_term, code_term, ste_example}].",
        "output_prefix": "da",
        "files_per_batch": 15
    },
]

def launch_worker(pass_name, batch_num, refined_files_batch, out_file):
    """Launch a single poll worker. Returns PID."""
    # Read refined content for this batch
    refined_content = ""
    for rf in refined_files_batch:
        rpath = os.path.join(REFINED_DIR, rf)
        if os.path.exists(rpath):
            with open(rpath) as f:
                refined_content += f"\n### FILE: {rf}\n{f.read()[:3000]}\n"  # cap per file
    
    pass_def = next(p for p in PASSES if p["name"] == pass_name)
    
    worker_prompt = f"""{AGENT_PROMPT}

## ENRICHMENT PASS: {pass_name} (batch {batch_num})
{pass_def['desc']}

## REFINED CONTENT
{refined_content}

## OUTPUT
Write ONLY valid JSON to stdout. Format:
{{"pass": "{pass_name}", "batch": {batch_num}, "entries": [...]}}
"""
    
    # Write prompt to temp file
    prompt_file = os.path.join(OUT_DIR, f"prompt-{pass_name}-{batch_num:03d}.txt")
    with open(prompt_file, 'w') as f:
        f.write(worker_prompt)
    
    # Launch hermes worker — output to file
    with open(out_file, 'w') as outf:
        proc = subprocess.Popen(
            ["hermes", "-z", worker_prompt, "-m", MODEL, "--yolo"],
            stdout=outf, stderr=subprocess.STDOUT,
            start_new_session=True
        )
    
    return proc.pid

def wait_for_workers(pids, timeout=180):
    """Wait for all PIDs to complete."""
    start = time.time()
    remaining = set(pids)
    while remaining and (time.time() - start) < timeout:
        time.sleep(5)
        done = []
        for pid in list(remaining):
            try:
                wpid, status = os.waitpid(pid, os.WNOHANG)
                if wpid != 0:
                    done.append(pid)
            except ChildProcessError:
                done.append(pid)
        for pid in done:
            remaining.discard(pid)
        if done:
            print(f"    {len(pids)-len(remaining)}/{len(pids)} done")
    return len(remaining) == 0

def verify_output(out_file):
    """Check if output file contains valid JSON."""
    if not os.path.exists(out_file) or os.path.getsize(out_file) < 10:
        return False, "empty or missing"
    try:
        with open(out_file) as f:
            content = f.read()
            # Find JSON in output (hermes may add text around it)
            start = content.find('{')
            end = content.rfind('}') + 1
            if start >= 0 and end > start:
                json.loads(content[start:end])
                return True, f"{len(content)} chars"
            return False, "no JSON found"
    except json.JSONDecodeError as e:
        return False, str(e)

# Build batches for each pass
all_batches = []
for p in PASSES:
    files_per = p["files_per_batch"]
    for i in range(0, len(refined_files), files_per):
        batch_files = refined_files[i:i+files_per]
        batch_num = i // files_per + 1
        all_batches.append((p["name"], batch_num, batch_files, f"{p['output_prefix']}-{batch_num:03d}.json"))

total_batches = len(all_batches)
print(f"=== Agent #8 Enlargement — {total_batches} batches across {len(PASSES)} passes ===")
print(f"Input: {len(refined_files)} refined files from {REFINED_DIR}")
print(f"Output: {OUT_DIR}/")
print()

# Initialize state
with open(STATE_FILE, 'w') as f:
    f.write(f"# Enlargement Progress — {time.strftime('%Y-%m-%d %H:%M')}\n\n")

# Process batches in groups of BATCH_SIZE
for i in range(0, total_batches, BATCH_SIZE):
    batch_group = all_batches[i:i+BATCH_SIZE]
    print(f"=== Batch group {i//BATCH_SIZE + 1}/{(total_batches + BATCH_SIZE - 1)//BATCH_SIZE} ===")
    
    # Launch up to BATCH_SIZE workers
    pids = {}
    for pass_name, batch_num, batch_files, out_name in batch_group:
        out_file = os.path.join(OUT_DIR, out_name)
        pid = launch_worker(pass_name, batch_num, batch_files, out_file)
        pids[pid] = (pass_name, batch_num, out_file)
        print(f"  {pass_name}-{batch_num:03d}: pid={pid}")
    
    # Wait for completion
    all_ok = wait_for_workers(list(pids.keys()))
    
    # Verify output
    all_verified = True
    for pid, (pass_name, batch_num, out_file) in pids.items():
        ok, msg = verify_output(out_file)
        status = "✅" if ok else "❌"
        print(f"  {pass_name}-{batch_num:03d}: {status} {msg}")
        if not ok:
            all_verified = False
    
    # Save state
    with open(STATE_FILE, 'a') as f:
        f.write(f"## Group {i//BATCH_SIZE + 1} — {time.strftime('%H:%M')}\n")
        for pid, (pass_name, batch_num, out_file) in pids.items():
            ok, _ = verify_output(out_file)
            f.write(f"- {pass_name}-{batch_num:03d}: {'PASS' if ok else 'FAIL'}\n")
        f.write(f"- Workers: {len(pids)} launched\n\n")
    
    if not all_verified:
        print("  ⚠️ Some outputs failed verification. Continuing with next group.")
    
    print()

print(f"Done. {total_batches} batches processed.")
print(f"Output: {OUT_DIR}/")
print(f"State: {STATE_FILE}")
