#!/usr/bin/env python3
"""Launch 4 Agent #7 workers using Hermes oneshot wrapper (safe, no tools, no session pollution)."""
import subprocess, os, tempfile, time, sys

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DOCS = ["README.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "RELEASE-NOTES.md"]
OUT = os.path.join(PROJECT, ".agents", "rewrites")
MODEL = "deepseek-v4-pro"

# Paths from hermes-background-workers skill
VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = os.path.expanduser("~/.hermes/skills/hermes-shell-hooks/templates/hermes-oneshot-wrapper.py")

if not os.path.exists(WRAPPER):
    print(f"ERROR: Wrapper not found at {WRAPPER}")
    sys.exit(1)

LEVELS = {
    1: "14 core principles only",
    2: "+ dictionary excerpt",
    3: "+ grammar rules",
    4: "+ full dictionary",
}

with open(os.path.join(PROJECT, "ste-code/artifacts/ste-code-distilled-system-prompt.txt")) as f:
    rules = f.read()

docs_text = ""
for d in DOCS:
    dpath = os.path.join(PROJECT, d)
    if os.path.exists(dpath):
        with open(dpath) as f:
            docs_text += f"\n\n### DOCUMENT: {d}\n\n{f.read()}\n"

workers = []
for lv, desc in LEVELS.items():
    out_dir = os.path.join(OUT, f"level-{lv}")
    os.makedirs(out_dir, exist_ok=True)

    prompt = f"""{rules}

Level {lv} ({desc}). You are Agent #7.

TASK: Rewrite all 4 documents below using only Level {lv} rules.
Output inline only — do NOT create any files or use any tools.
For each document output: rewritten text, change log, compliance table.

{docs_text}"""

    # Write prompt to temp file (wrapper reads from file and deletes it)
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, dir="/tmp")
    tmp.write(prompt)
    tmp.close()
    
    log_file = os.path.join(out_dir, "output.txt")
    
    print(f"Level {lv}: launching → {out_dir}/output.txt")
    
    # Fire-and-forget: Popen with start_new_session
    proc = subprocess.Popen(
        [VENV_PYTHON, WRAPPER, tmp.name, "--model", MODEL],
        stdout=open(log_file, "w"),
        stderr=subprocess.STDOUT,
        start_new_session=True,
        env={**os.environ, "HERMES_ACCEPT_HOOKS": "1"},
    )
    workers.append((lv, proc.pid, out_dir))
    time.sleep(0.5)

print(f"\nAll {len(workers)} workers launched. PIDs: {[w[1] for w in workers]}")
print(f"Monitor: ps aux | grep oneshot")
print(f"Results: {OUT}/level-{{1,2,3,4}}/output.txt")

# Wait for all
for lv, pid, out_dir in workers:
    try:
        os.waitpid(pid, 0)
        log = os.path.join(out_dir, "output.txt")
        size = os.path.getsize(log) if os.path.exists(log) else 0
        print(f"  Level {lv}: done ({size} bytes)")
    except:
        print(f"  Level {lv}: error")

print("\nAll workers complete.")
