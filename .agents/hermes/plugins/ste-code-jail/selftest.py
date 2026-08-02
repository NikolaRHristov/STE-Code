#!/usr/bin/env python3
"""Self-test for the ste-code-jail plugin.

Exercises the containment logic directly (no Hermes runtime needed) so the
jail can be verified in CI and after any edit:

    python3 .agents/hermes/plugins/ste-code-jail/selftest.py

Exit code 0 = all cases pass.
"""

from __future__ import annotations

import importlib.util
import logging
import os
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent


def _load_plugin():
    spec = importlib.util.spec_from_file_location(
        "ste_code_jail_under_test", _HERE / "__init__.py"
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    # The plugin logs every block at WARNING. That is right at runtime and
    # pure noise here, where blocking is the expected outcome.
    logging.disable(logging.CRITICAL)

    jail = _load_plugin()
    cfg = jail._load_config()

    root = cfg.get("_project_root")
    if not root:
        print("FAIL: project root was not discovered")
        return 1

    print(f"project root : {root}")
    print(f"enforce      : {cfg.get('enforce')}")
    print(f"allowed roots: {len(cfg.get('_roots') or [])}")
    for entry in cfg.get("_roots") or []:
        print(f"  - {entry}")
    print()

    parent = os.path.dirname(root)
    tmp = tempfile.gettempdir()

    # (tool, args, expect_blocked, label)
    cases = [
        (
            "write_file",
            {"path": os.path.join(root, ".agents/state/ok.md"), "content": "x"},
            False,
            "write inside repo",
        ),
        (
            "write_file",
            {"path": ".agents/state/ok-relative.md", "content": "x"},
            False,
            "relative write inside repo",
        ),
        (
            "write_file",
            {"path": os.path.join(parent, ".agents/prompts/escape.md"), "content": "x"},
            True,
            "write into repo PARENT (the real-world escape)",
        ),
        (
            "write_file",
            {"path": os.path.join(root, "../sibling/.agents/x.md"), "content": "x"},
            True,
            "dot-dot traversal out of repo",
        ),
        (
            "write_file",
            {"path": "~/Documents/escape.md", "content": "x"},
            True,
            "write into home directory",
        ),
        (
            "write_file",
            {"path": os.path.join(root, ".git/config"), "content": "x"},
            True,
            "write into denied .git",
        ),
        (
            "write_file",
            {"path": os.path.join(tmp, "scratch.txt"), "content": "x"},
            False,
            "write into temp (allowed)",
        ),
        (
            "patch",
            {"mode": "replace", "path": os.path.join(parent, "outside.py"),
             "old_string": "a", "new_string": "b"},
            True,
            "patch a file outside the repo",
        ),
        (
            "patch",
            {"mode": "patch",
             "patch": "*** Begin Patch\n*** Add File: " + os.path.join(parent, "x.py")
                      + "\n+print(1)\n*** End Patch"},
            True,
            "V4A patch adding a file outside the repo",
        ),
        (
            "terminal",
            {"command": f"mkdir -p {parent}/.agents/prompts/expansion-pass1"},
            True,
            "mkdir outside the repo",
        ),
        (
            "terminal",
            {"command": f"echo hi > {parent}/leak.txt"},
            True,
            "shell redirect outside the repo",
        ),
        (
            "terminal",
            {"command": f"mkdir -p {root}/.agents/tmp/work"},
            False,
            "mkdir inside the repo",
        ),
        (
            "terminal",
            {"command": f"cat {parent}/somefile.md"},
            False,
            "READ outside the repo stays allowed",
        ),
        (
            "terminal",
            {"command": "ls -la /etc"},
            False,
            "read-only ls outside the repo stays allowed",
        ),
        (
            "terminal",
            {"command": "make test", "workdir": parent},
            True,
            "terminal workdir outside the repo",
        ),
        (
            "read_file",
            {"path": "/etc/hosts"},
            False,
            "read_file is never gated",
        ),
    ]

    failures = 0
    for tool, args, expect_blocked, label in cases:
        result = jail._on_pre_tool_call(tool_name=tool, args=args)
        blocked = isinstance(result, dict) and result.get("action") == "block"
        ok = blocked == expect_blocked
        status = "PASS" if ok else "FAIL"
        verdict = "BLOCKED" if blocked else "allowed"
        want = "BLOCKED" if expect_blocked else "allowed"
        print(f"[{status}] {label}: {verdict} (want {want})")
        if not ok:
            failures += 1
            if isinstance(result, dict):
                print("        " + str(result.get("message", ""))[:300])

    print()
    if failures:
        print(f"{failures} case(s) FAILED")
        return 1
    print(f"all {len(cases)} case(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
