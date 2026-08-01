#!/usr/bin/env python3
"""One-shot readiness watcher for STE-Code Phase C grouping.

Polls corpus_ready() every 20s (import-only, no writes, no churn) until the
refined corpus resolves cleanly, then exits 0 printing READY. Exits 2 on timeout.
Runs as a background process (poll-vs-wait.md: sleep loop lives INSIDE a bg proc,
never a foreground blocker) with notify_on_complete so the agent is told the
instant the other agent's marker repair lands.
"""
import importlib
import sys
import time
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]  # .agents/state/x.py -> repo root
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "grouping"))

MAX_SECONDS = 45 * 60
INTERVAL = 20


def check():
    import group_engine as ge
    importlib.reload(ge)
    man = ge.parse_manifest()
    id2pos = ge.id_to_position(man)
    idx = ge.index_refined()
    ready, problems = ge.corpus_ready(idx, id2pos)
    return ready, problems


start = time.time()
last = None
while time.time() - start < MAX_SECONDS:
    try:
        ready, problems = check()
    except Exception as e:  # engine mid-edit / transient
        ready, problems = False, [f"transient: {e}"]
    n_flagged = "?"
    for p in problems:
        if "refined files whose" in p:
            n_flagged = p.split()[0]
    stamp = time.strftime("%H:%M:%S")
    if ready:
        print(f"[{stamp}] READY — corpus resolves cleanly. Launch grouping now.")
        sys.exit(0)
    msg = f"[{stamp}] not ready ({n_flagged} files flagged)"
    if msg != last:
        print(msg, flush=True)
        last = msg
    time.sleep(INTERVAL)

print(f"[{time.strftime('%H:%M:%S')}] TIMEOUT after {MAX_SECONDS}s — still not ready.")
sys.exit(2)
