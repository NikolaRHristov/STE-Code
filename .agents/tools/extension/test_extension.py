#!/usr/bin/env python3
"""Self-tests for the Phase E extension tooling (markdown-first, no LLM, no JSON gen).

Run: python3 .agents/tools/extension/test_extension.py
"""
import sys
import json
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "extension"))

from templater import Templater
EXT = __import__("extend_batch")
VR = __import__("verify_extensions")
MDJ = __import__("md_to_json")

_passed = _failed = 0


def check(name, cond, detail=""):
    global _passed, _failed
    if cond:
        _passed += 1
        print(f"  ok   {name}")
    else:
        _failed += 1
        print(f"  FAIL {name} — {detail}")


TPL = Templater(PROJECT / ".agents" / "tools" / "extension" / "extend_batch.py")


def t_prompt_render():
    print("E1 extension area prompt renders strict, no leftover {{}}, markdown-only")
    out = TPL.render("extend-area", area="verbs", count=20,
                     out_path="/tmp/x.md")
    check("renders", "Extension Worker" in out)
    check("no leftover {{", "{{" not in out)
    check("markdown-only (no 'Output ONLY a valid JSON')", "valid JSON" not in out)
    check("embeds area", "verbs" in out)
    try:
        TPL.render("extend-area", area="verbs")
        check("strict missing-var raises", False, "no raise")
    except KeyError:
        check("strict missing-var raises", True)


def _good_md():
    return (
        "### attach\n\n"
        "- **type**: verb\n- **category-id**: 3\n- **approved**: true\n"
        "- **replaces**: mount\n"
        "- **definition**: Connect one software component to another component so they can exchange data.\n"
        "- **code_example_ste**: Attach the logger to the service.\n"
        "- **code_example_non_ste**: Utilize the logger with the service.\n"
        "- **source**: generated-batch-001\n\n"
        "### leverage\n\n"
        "- **type**: verb\n- **category-id**: 1\n- **approved**: false\n"
        "- **replaces**: use\n"
        "- **definition**: A rejected synonym. Use the verb use instead when you write STE-Code docs.\n"
        "- **code_example_ste**: Use the cache layer to reduce load.\n"
        "- **code_example_non_ste**: Leverage the cache layer to decrease load.\n"
        "- **source**: generated-batch-001\n"
    )


def t_gate_logic():
    print("E2 gate accepts clean markdown, rejects bad markdown")
    d = Path(tempfile.mkdtemp())
    EXT.EXT_DIR = d
    VR.EXT_DIR = d
    good = d / "verbs.md"
    good.write_text(_good_md())
    ok, why = EXT._gate_ok(good)
    check("clean markdown passes", ok, why)
    # Bad: fabrication + short definition
    bad = d / "adjectives.md"
    bad.write_text("### x\n\n- **type**: adjective\n- **definition**: short\n- **source**: b\n")
    ok2, why2 = EXT._gate_ok(bad)
    check("bad fails", not ok2, why2)
    EXT.EXT_DIR = PROJECT / "ste-code" / "extensions"
    VR.EXT_DIR = PROJECT / "ste-code" / "extensions"


def t_md_to_json():
    print("E3 md_to_json derives JSON deterministically (no LLM)")
    d = Path(tempfile.mkdtemp())
    md = d / "verbs.md"
    md.write_text(_good_md())
    out = MDJ.md_to_json(md)
    data = json.loads(out.read_text())
    check("2 entries parsed", len(data) == 2, str(len(data)))
    check("booleans coerced", data[0].get("approved") is True)
    check("title captured", data[0].get("title") == "attach")
    check("replaces string kept", data[0].get("replaces") == "mount")


def t_verify_script():
    print("E4 verify_extensions.py on synthetic markdown dir")
    import subprocess
    d = Path(tempfile.mkdtemp())
    (d / "verbs.md").write_text(_good_md())
    MDJ.md_to_json(d / "verbs.md")  # produce derived JSON so Gate1b passes
    r = subprocess.run([sys.executable, str(PROJECT / ".agents" / "tools" / "extension" / "verify_extensions.py"),
                        "--dir", str(d)], capture_output=True, text=True, cwd=str(PROJECT))
    check("verify exits 0 on clean markdown+json", r.returncode == 0, r.stdout + r.stderr)


def main():
    for t in (t_prompt_render, t_gate_logic, t_md_to_json, t_verify_script):
        t()
    print(f"\n{'='*50}\n{_passed} passed, {_failed} failed\n{'='*50}")
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
