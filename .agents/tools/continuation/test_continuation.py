#!/usr/bin/env python3
"""Self-tests for the Phase B1 continuation tooling (no LLM, no network).

Run: python3 .agents/tools/continuation/test_continuation.py
"""
import sys
import json
import subprocess
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "continuation"))

from templater import Templater
CB = __import__("continue_batch")
VC = __import__("verify_continuation")

_passed = _failed = 0


def check(name, cond, detail=""):
    global _passed, _failed
    if cond:
        _passed += 1
        print(f"  ok   {name}")
    else:
        _failed += 1
        print(f"  FAIL {name} — {detail}")


TPL = Templater(PROJECT / ".agents" / "tools" / "continuation" / "continue_batch.py")


def t_prompt_render():
    print("C1 continue-worker prompt renders strict, embeds target")
    out = TPL.render("continue-worker", target="ste-code/refined/r001-p1-4.md")
    check("renders", "Continuation" in out)
    check("no leftover {{", "{{" not in out)
    check("embeds target", "r001-p1-4.md" in out)


def t_queue_parse():
    print("C2 verify_continuation builds a queue from flagged refined pages")
    import subprocess
    d = Path(tempfile.mkdtemp())
    qp = d / ".continue-queue.json"
    # A truncated page
    (d / "bad.md").write_text("# Page 1 of 434\nThis text is cut off mid sent")
    # A healthy page (large enough to pass the size gate, valid header)
    (d / "good.md").write_text(
        "# Page 2 of 434\n\n"
        "The service starts the worker and logs the result to the output stream. "
        "Each worker reads its configuration from the environment and writes a "
        "status file when it finishes. The supervisor checks the status file and "
        "restarts the worker if the file is older than the timeout. Use short "
        "sentences and active voice in all procedure documentation.\n")
    r = subprocess.run([sys.executable, str(PROJECT / ".agents" / "tools" / "continuation" / "verify_continuation.py"),
                        "--dir", str(d), "--queue", str(qp)],
                       capture_output=True, text=True, cwd=str(PROJECT))
    check("verifier exits 0", r.returncode == 0, r.stderr)
    data = json.loads(qp.read_text())
    check("queue flags truncated page", any("bad.md" in e for e in data), str(data))
    check("queue skips healthy page", all("good.md" not in e for e in data), str(data))


def t_runner_guard():
    print("C3 continue_batch refuses without --queue (exit 2)")
    r = subprocess.run([sys.executable, str(PROJECT / ".agents" / "tools" / "continuation" / "continue_batch.py")],
                       capture_output=True, text=True, cwd=str(PROJECT))
    check("exit 2 without queue", r.returncode == 2, str(r.returncode))


def main():
    for t in (t_prompt_render, t_queue_parse, t_runner_guard):
        t()
    print(f"\n{'='*50}\n{_passed} passed, {_failed} failed\n{'='*50}")
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
