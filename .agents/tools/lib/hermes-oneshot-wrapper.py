#!/usr/bin/env python3
"""Hardened Hermes oneshot wrapper — the single entry point for confined child sessions.

This is the "oneshot wrapper" the benchmark harness launches every child worker
through. It is ALWAYS invoked by launch_confined_child.build_command(), which
has already pinned STE_CODE_JAIL_POLICY + HERMES_PROFILE, stripped the
environment, reset HOME=/tmp, and wrapped the command in jail-exec.sh (Layer-2
kernel confinement).

Because a child MUST never run unconfined, this wrapper fails closed:
  * refuses to start if STE_CODE_JAIL_POLICY is unset (bare invocation),
  * refuses to start if HOME still points at the operator's real home,
  * never hardcodes HERMES_YOLO_MODE — it honors a parent-supplied --yolo /
    HERMES_YOLO_MODE and defaults OFF.

Usage (constructed by build_command):
    python3 hermes-oneshot-wrapper.py <prompt_file> --model M --toolsets T [--yolo]
"""

import argparse
import os
import subprocess
import sys


def main() -> int:
    ap = argparse.ArgumentParser(description="Hardened Hermes oneshot wrapper.")
    ap.add_argument("prompt_file", help="Path to the prompt text file.")
    ap.add_argument(
        "--model", default=os.environ.get("HERMES_MODEL", "tencent/hy3:free")
    )
    ap.add_argument("--toolsets", default="terminal,file")
    ap.add_argument("--profile", default=os.environ.get("HERMES_PROFILE"))
    ap.add_argument(
        "--yolo",
        action="store_true",
        help="Auto-approve (only honored when the parent sets it).",
    )
    args = ap.parse_args()

    # Fail closed: a bare wrapper (no pinned jail policy) must not spawn an
    # unconfined agent. The parent (launch_confined_child) always sets this.
    if not os.environ.get("STE_CODE_JAIL_POLICY"):
        sys.stderr.write(
            "hermes-oneshot-wrapper: refusing to start — "
            "STE_CODE_JAIL_POLICY is not set (unconfined launch blocked)\n"
        )
        return 1

    # Fail closed: HOME must be isolated by the parent (build_child_env sets
    # HOME=/tmp). A leaked real home would expose the operator's identity.
    home = os.environ.get("HOME", "")
    if home.startswith(("/Users/", "/Volumes/", "/home/", "C:\\")):
        sys.stderr.write(
            f"hermes-oneshot-wrapper: refusing to start — HOME not isolated ({home})\n"
        )
        return 1

    # YOLO is NEVER hardcoded. Honor a parent-set value; default OFF.
    yolo = args.yolo or os.environ.get("HERMES_YOLO_MODE", "").lower() in (
        "1",
        "true",
        "yes",
    )

    try:
        prompt = open(args.prompt_file, encoding="utf-8").read()
    except OSError as exc:
        sys.stderr.write(f"hermes-oneshot-wrapper: cannot read prompt: {exc}\n")
        return 1

    cmd = ["hermes", "-z", prompt, "-m", args.model, "--toolsets", args.toolsets]
    if args.profile:
        cmd += ["--profile", args.profile]
    if yolo:
        cmd.append("--yolo")

    return subprocess.run(cmd, env=os.environ).returncode


if __name__ == "__main__":
    sys.exit(main())
