#!/usr/bin/env python3
"""Self-test for the ste-code-jail plugin.

Two suites, no Hermes runtime required (the hook is called directly), so this
runs in CI:

  ALLOW    calls that must NOT be blocked (false-positive guard)
  ESCAPE   real bypass attempts that must ALL be blocked

The ESCAPE suite is adversarial by design. It was written by trying to defeat
the plugin, and the first run of it found 14 holes in a version that passed a
16-case happy-path suite. Add a case here whenever a new bypass is imagined.

    python3 .agents/hermes/plugins/ste-code-jail/selftest.py
    python3 .agents/hermes/plugins/ste-code-jail/selftest.py -v

Exit code 0 = every case behaved as required.
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
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    # The plugin logs every block at WARNING. Correct at runtime, noise here.
    logging.disable(logging.CRITICAL)

    jail = _load_plugin()
    cfg = jail._load_config()

    root = cfg.get("_project_root")
    if not root:
        print("FAIL: project root was not discovered")
        return 1

    parent = os.path.dirname(root)
    tmp = tempfile.gettempdir()

    print(f"project root : {root}")
    print(f"enforce      : {cfg.get('enforce')}")
    print(f"allowed roots: {len(cfg.get('_roots') or [])}")
    if verbose:
        for entry in cfg.get("_roots") or []:
            print(f"  - {entry}")
    print()

    # ---------------------------------------------------------------- ALLOW
    # Must NOT be blocked. These protect against a jail so strict it makes
    # ordinary work impossible.
    allow = [
        (
            "write_file",
            {"path": os.path.join(root, ".agents/state/ok.md"), "content": "x"},
            "absolute write inside repo",
        ),
        (
            "write_file",
            {"path": ".agents/state/ok.md", "content": "x"},
            "relative write inside repo",
        ),
        (
            "write_file",
            {"path": os.path.join(tmp, "scratch.txt"), "content": "x"},
            "write into temp",
        ),
        (
            "patch",
            {
                "mode": "replace",
                "path": os.path.join(root, "Makefile"),
                "old_string": "a",
                "new_string": "b",
            },
            "patch inside repo",
        ),
        (
            "terminal",
            {"command": "mkdir -p .agents/tmp/work"},
            "relative mkdir inside repo",
        ),
        (
            "terminal",
            {"command": f"mkdir -p {root}/.agents/tmp/work"},
            "absolute mkdir inside repo",
        ),
        (
            "terminal",
            {"command": "echo hi > .agents/tmp/out.txt"},
            "redirect inside repo",
        ),
        ("terminal", {"command": "make check"}, "plain build command"),
        ("terminal", {"command": "git status --short"}, "read-only git"),
        (
            "terminal",
            {"command": "git add -A && git commit -m x"},
            "git add/commit (no path operand)",
        ),
        ("terminal", {"command": f"cat {parent}/somefile.md"}, "READ outside repo"),
        ("terminal", {"command": "ls -la /etc"}, "read-only ls outside"),
        (
            "terminal",
            {"command": "grep -r pattern /usr/share"},
            "read-only grep outside",
        ),
        (
            "terminal",
            {"command": "cd .agents/tools && python3 -c 'print(1)'"},
            "cd inside repo then run",
        ),
        (
            "terminal",
            {"command": "curl -s https://example.com/api"},
            "network read, no output file",
        ),
        (
            "terminal",
            {"command": "chmod 755 .agents/tools/lib/repo_root.py"},
            "chmod inside repo",
        ),
        ("read_file", {"path": "/etc/hosts"}, "read_file is never gated"),
        (
            "search_files",
            {"pattern": "x", "path": "/usr"},
            "search_files is never gated",
        ),
        ("execute_code", {"code": "print(1 + 1)"}, "pure computation"),
        (
            "execute_code",
            {"code": "from hermes_tools import read_file\nread_file('/etc/hosts')"},
            "execute_code reading outside",
        ),
    ]

    # --------------------------------------------------------------- ESCAPE
    # Every one of these MUST be blocked.
    escape = [
        (
            "write_file",
            {"path": os.path.join(parent, ".agents/prompts/x.md"), "content": "x"},
            "absolute write into repo PARENT",
        ),
        (
            "write_file",
            {"path": "../direct-relative.md", "content": "x"},
            "relative ../ write",
        ),
        (
            "write_file",
            {"path": os.path.join(root, "../sibling/x.md"), "content": "x"},
            "dot-dot traversal",
        ),
        (
            "write_file",
            {"path": "~/Documents/escape.md", "content": "x"},
            "tilde write into home",
        ),
        (
            "write_file",
            {"path": os.path.join(root, ".git/config"), "content": "x"},
            "write into denied .git",
        ),
        (
            "patch",
            {
                "mode": "replace",
                "path": os.path.join(parent, "out.py"),
                "old_string": "a",
                "new_string": "b",
            },
            "patch outside repo",
        ),
        (
            "patch",
            {
                "mode": "patch",
                "patch": "*** Begin Patch\n*** Add File: "
                + os.path.join(parent, "x.py")
                + "\n+print(1)\n*** End Patch",
            },
            "V4A patch adding file outside",
        ),
        ("terminal", {"command": "mkdir -p ../escape-relative"}, "relative ../ mkdir"),
        (
            "terminal",
            {"command": "cd .. && mkdir -p .agents/prompts/x"},
            "cd .. then relative mkdir (the original escape)",
        ),
        (
            "terminal",
            {"command": "(cd /tmp/../Users && mkdir -p escape)"},
            "subshell cd then relative mkdir",
        ),
        ("terminal", {"command": "echo leak > ../leak.txt"}, "relative redirect"),
        (
            "terminal",
            {"command": "cat > ../heredoc.txt <<'EOF'\nx\nEOF"},
            "heredoc to relative path",
        ),
        ("terminal", {"command": "tee ../tee-leak.txt"}, "tee to relative path"),
        (
            "terminal",
            {"command": f"echo x > {parent}/abs-leak.txt"},
            "absolute redirect outside",
        ),
        (
            "terminal",
            {"command": "mkdir -p $HOME/env-escape"},
            "environment variable expansion",
        ),
        (
            "terminal",
            {"command": "mkdir -p ${HOME}/brace-escape"},
            "braced environment variable",
        ),
        ("terminal", {"command": "mv notes.md .."}, "mv into parent"),
        ("terminal", {"command": "cp secrets.txt ~/Desktop/"}, "cp to tilde path"),
        ("terminal", {"command": "rsync -a data/ ../mirror/"}, "rsync to parent"),
        ("terminal", {"command": "git -C .. init escaped-repo"}, "git -C parent"),
        ("terminal", {"command": "ln -s /etc/passwd ../link"}, "symlink into parent"),
        (
            "terminal",
            {"command": f"curl -o {parent}/dl.bin https://x.test/f"},
            "curl -o outside",
        ),
        (
            "terminal",
            {"command": "sed -i '' 's/a/b/' ../outside.md"},
            "sed in-place outside",
        ),
        (
            "terminal",
            {"command": f"python3 -c \"import os; os.makedirs('{parent}/py')\""},
            "python -c makedirs outside",
        ),
        (
            "terminal",
            {"command": "sh -c 'cd .. && mkdir -p nested-escape'"},
            "nested sh -c with cd ..",
        ),
        (
            "terminal",
            {"command": "make test", "workdir": parent},
            "workdir outside repo",
        ),
        (
            "terminal",
            {"command": "mkdir -p safe", "workdir": parent},
            "relative mkdir under an outside workdir",
        ),
        (
            "execute_code",
            {
                "code": "from hermes_tools import write_file\n"
                f"write_file('{parent}/x.md', 'x')"
            },
            "execute_code write_file outside",
        ),
        (
            "execute_code",
            {
                "code": "from hermes_tools import terminal\n"
                f"terminal('mkdir -p {parent}/y')"
            },
            "execute_code terminal mkdir outside",
        ),
        (
            "skill_manage",
            {
                "action": "write_file",
                "name": "s",
                "file_path": "../../../escape.md",
                "file_content": "x",
            },
            "skill_manage traversal out of skills dir",
        ),
    ]

    failures = 0

    print(f"ALLOW suite ({len(allow)} cases) — must NOT be blocked")
    for tool, args, label in allow:
        result = jail._on_pre_tool_call(tool_name=tool, args=args)
        blocked = isinstance(result, dict) and result.get("action") == "block"
        if blocked:
            failures += 1
            print(f"  [FAIL] {label}: blocked (false positive)")
            if verbose:
                print("         " + str(result.get("message", ""))[:400])
        elif verbose:
            print(f"  [ok]   {label}")
    if not verbose:
        print(f"  {len(allow) - failures}/{len(allow)} allowed correctly")

    print(f"\nESCAPE suite ({len(escape)} cases) — must ALL be blocked")
    escape_failures = 0
    for tool, args, label in escape:
        result = jail._on_pre_tool_call(tool_name=tool, args=args)
        blocked = isinstance(result, dict) and result.get("action") == "block"
        if not blocked:
            failures += 1
            escape_failures += 1
            print(f"  [HOLE] {label}: NOT blocked")
        elif verbose:
            print(f"  [ok]   {label}")
    if not verbose:
        print(f"  {len(escape) - escape_failures}/{len(escape)} escapes blocked")

    total = len(allow) + len(escape)
    print()
    if failures:
        print(f"{failures} of {total} case(s) FAILED")
        return 1
    print(
        f"all {total} case(s) passed "
        f"({len(allow)} allowed, {len(escape)} escapes blocked)"
    )
    print()
    print("NOTE: argument inspection cannot see inside an opaque subprocess")
    print("      (`python3 build.py` calling os.makedirs('../x')). Wrap those")
    print("      in scripts/jail-exec.sh for kernel-enforced confinement;")
    print("      verify with: scripts/jail-exec.sh --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
