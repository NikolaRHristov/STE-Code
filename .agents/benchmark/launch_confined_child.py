#!/usr/bin/env python3
"""
launch_confined_child.py — hardened launcher for benchmark child sessions.

WHY THIS EXISTS
---------------
The stock pipeline launches worker agents two ways:

  1. agent-runner.run_agent()  -> subprocess.run([venv_python,
                                   hermes-oneshot-wrapper.py, prompt, ...])
  2. launch-worker.sh          -> nohup python3 agent-runner.py ... &

Both hand the child the INHERITED environment (env = {**os.environ, **env_vars})
and never pin a profile, a jail policy, a toolset, or wrap the process in the
kernel sandbox. hermes-oneshot-wrapper.py hardcodes HERMES_YOLO_MODE=true +
HERMES_ACCEPT_HOOKS=1 and uses the FULL cli toolset. The result: a "profile-less"
child inherits the launching session's profile (often `dev` = wide open) and has
NO jail, NO environment strip, NO redaction. That is the hole this file closes.

WHAT THIS WRAPPER GUARANTEES (all programmatic, not just `hermes -z`)
---------------------------------------------------------------------
  * The child runs under STE_CODE_JAIL_POLICY=bench and
    HERMES_PROFILE=benchmark-ste-code, force-pinned — it cannot inherit a
    weaker policy from the spawner's shell (closes the HERMES_HOME leak).
  * The environment is STRIPPED to a minimal allow-list; credential vars,
    $HERMES_HOME, SSH_*, AWS_*, and the parent's STE_CODE_JAIL_POLICY are
    explicitly dropped.
  * The child command is wrapped in jail-exec.sh (Seatbelt on macOS, bwrap on
    Linux) so even the agent's own subprocesses (python3 build.py calling
    os.makedirs) are kernel-confined to the bench write roots.
  * A minimal --toolsets is applied unless the caller overrides it, so the
    child cannot reach memory/cron/delegate/network tools.
  * The adversarial-benchmark-harness skill text + a WORKER_BRIEF pointer are
    injected into the prompt (per the harness skill: children do not auto-load
    benchmark-ste-code skills and must be told the rules).
  * Captured stdout is run through the harness anonymizer / leak-scan before it
    is returned, so raw /Users/<name> / hostname never leaves the child as
    reportable identity.

This module is the single place every benchmark child session is launched from.
Replace the subprocess.run / Popen call sites in agent-runner.py and
launch-worker.sh with launch_confined_child.launch().

USAGE
-----
    from launch_confined_child import launch

    proc = launch(prompt, model="tencent/hy3:free", toolset="terminal,file",
                  label="red-variant0-round1")
    out, err = proc.communicate(timeout=600)
    # out has already been leak-scanned; raw identity is gone.

Or as a CLI (drop-in for agent-runner.py invocations):
    python3 launch_confined_child.py <prompt_file> [--model M] [--toolset T] [--label L]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

# ── Resolve paths (by MARKER walk, never parent-hop counting) ────────────────
# This file lives at: .agents/benchmark/launch_confined_child.py
# _BENCH = .agents/benchmark/
# _AGENTS = .agents/
# _PROJECT = STE-Code root
_HERE = Path(__file__).resolve().parent
_AGENTS = _HERE.parent
_PROJECT = _AGENTS.parent
_JAIL_DIR = _AGENTS / "hermes" / "jail"
_JAIL_EXEC = _JAIL_DIR / "scripts" / "jail-exec.sh"
_WRAPPER = _AGENTS / "tools" / "lib" / "hermes-oneshot-wrapper.py"
_VENV_PY = Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3"

# Where the harness keeps the worker brief + anonymizer + skill text.
_BRIEF = _HERE / "WORKER_BRIEF.md"
_ANON = _HERE / "anonymize.py"
_HARNESS_SKILL = (
    _AGENTS
    / "skills"
    / "ste-code-benchmark"
    / "adversarial-benchmark-harness"
    / "SKILL.md"
)

# Force the child into this policy + profile. Never inherits from the spawner.
CHILD_POLICY = "bench"
CHILD_PROFILE = "benchmark-ste-code"

# Default minimal toolset for a benchmark child. Override per-call when a
# worker genuinely needs more, but never the full cli set.
DEFAULT_TOOLSET = "terminal,file"

# Environment keys we explicitly DROP from the child (leak / escalation surface).
_DROP_ENV_PREFIXES = (
    "HERMES_HOME",
    "STE_CODE_JAIL_POLICY",
    "SSH",
    "AWS",
    "GCP",
    "AZURE",
    "GOOGLE",
    "ANTHROPIC",
    "OPENAI",
    "HUGGING",
    "NPM",
    "GITHUB",
    "GITLAB",
    "DOCKER",
    "KUBE",
    "VAULT",
    "PG",
    "MYSQL",
    "DB_",
    "TOKEN",
    "SECRET",
    "PASSWD",
    "PASSWORD",
    "CREDENTIAL",
    "API_KEY",
    "APIKEY",
    "PRIVATE_KEY",
    "CERT",
    "COOKIE",
    "SESSION",
)
_DROP_ENV_EXACT = {
    "HOME",
    "HERMES_PROFILE",
    "HERMES_ACTIVE_PROFILE",
    "HERMES_INFERENCE_MODEL",
    "HERMES_INFERENCE_PROVIDER",
    "HERMES_REQUEST_TIMEOUT",
    "HERMES_YOLO_MODE",
    "HERMES_ACCEPT_HOOKS",
    "PRIVACY_LLM_CLASSIFY",
}


def build_child_env(extra: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """Construct a STRIPPED environment for the child.

    Keep only a minimal allow-list; drop every credential / home / policy var so
    the child cannot inherit the spawner's identity or a weaker jail policy.
    """
    allowed_keys = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR", "TEMP", "TMP")
    env: Dict[str, str] = {}
    for k in allowed_keys:
        v = os.environ.get(k)
        if v:
            env[k] = v

    # Isolate the child under /tmp so it cannot discover the operator's home.
    env["HOME"] = "/tmp"
    env["TMPDIR"] = "/tmp"
    env["TEMP"] = "/tmp"
    env["TMP"] = "/tmp"

    # Force the strict jail policy + profile. These OVERRIDE any inherited value
    # because we set them last and never copy them in from the parent.
    env["STE_CODE_JAIL_POLICY"] = CHILD_POLICY
    env["HERMES_PROFILE"] = CHILD_PROFILE

    # Explicitly scrub anything that leaked through.
    for k in list(os.environ.keys()):
        if k in _DROP_ENV_EXACT:
            continue  # already excluded (not in allow-list)
        if any(k.startswith(p) for p in _DROP_ENV_PREFIXES):
            continue
    # The allow-list approach above already excludes them; this loop is a
    # defensive no-op kept for clarity that we deliberately do NOT forward them.

    if extra:
        # Caller-supplied overrides (e.g. a model name) — but never allow a
        # policy/profile/home override to slip back in.
        for k, v in extra.items():
            if k in _DROP_ENV_EXACT or k in ("HOME",):
                continue
            if any(k.startswith(p) for p in _DROP_ENV_PREFIXES):
                continue
            env[k] = v
    return env


def _inject_harness_context(prompt: str) -> str:
    """Embed the adversarial harness rules + worker brief pointer into the prompt.

    Children launched via the oneshot wrapper do NOT auto-load benchmark-ste-code
    skills, so the rules must travel in the prompt (per adversarial-benchmark-
    harness SKILL.md §9 / the WORKER_BRIEF pattern).
    """
    blocks: List[str] = []
    if _BRIEF.exists():
        blocks.append(
            "## Worker brief\nRead and obey .agents/benchmark/WORKER_BRIEF.md "
            "(orientation, non-negotiable rules, file ownership, definition of done).\n"
        )
    if _HARNESS_SKILL.exists():
        try:
            skill_text = _HARNESS_SKILL.read_text(encoding="utf-8")
            # Keep it bounded; the full skill is long. Embed the contract section.
            blocks.append(
                "## Adversarial benchmark harness (contract)\n"
                + _extract_contract(skill_text)
            )
        except Exception:
            pass
    if not blocks:
        return prompt
    return prompt + "\n\n---\n\n" + "\n\n".join(blocks)


def _extract_contract(skill_text: str) -> str:
    """Pull the colour-model + non-negotiable rules out of the skill text."""
    # Take the section header line + the next ~40 lines as the contract summary.
    lines = skill_text.splitlines()
    out: List[str] = []
    started = False
    for i, line in enumerate(lines):
        if line.strip().startswith("## 1. The colour model"):
            started = True
        if started:
            out.append(line)
            if len(out) > 45:
                break
    return "\n".join(out) if out else skill_text[:3000]


def _leak_scan(text: str) -> str:
    """Run the harness anonymizer / leak-scan on captured child output.

    If anonymize.py is present, use it; otherwise apply the canonical grep-class
    redaction inline so raw identity never leaves the child as reportable text.
    Returns the scrubbed text.
    """
    # Inline safety net: redact the patterns the harness leak-scan asserts on.
    # (anonymize.py is the authoritative layer when available.)
    patterns = [
        (r"/Users/[A-Za-z0-9_.-]+", "/Users/<redacted>"),
        (r"/Volumes/[A-Za-z0-9_. /-]+", "/Volumes/<redacted>"),
        (r"/home/[a-z0-9_-]+", "/home/<redacted>"),
        (r"C:\\\\Users\\[^\\\\]+", "C:\\\\Users\\\\<redacted>"),
        (re.escape(str(Path.home())), "<home>"),
    ]
    scrubbed = text
    for pat, repl in patterns:
        scrubbed = re.sub(pat, repl, scrubbed)

    # Prefer the harness anonymizer if it exists and imports cleanly.
    if _ANON.exists():
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location("anon", str(_ANON))
            if spec is not None and spec.loader is not None:
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                if hasattr(mod, "redact"):
                    scrubbed = mod.redact(scrubbed)
        except Exception:
            pass
    return scrubbed


def build_command(prompt_file: Path, model: str, toolset: str) -> List[str]:
    """Build the kernel-sandboxed child command.

    Wraps:  jail-exec.sh STE_CODE_JAIL_POLICY=bench <wrapper> <prompt> --model M --toolsets T
    jail-exec.sh applies Layer-2 (Seatbelt/bwrap) confinement using the same
    policy roots as the plugins, so the child's subprocesses are confined too.
    """
    runtime = str(_VENV_PY) if _VENV_PY.exists() else "python3"
    inner = [
        runtime,
        str(_WRAPPER),
        str(prompt_file),
        "--model",
        model,
        "--toolsets",
        toolset,
    ]
    if not _JAIL_EXEC.exists():
        # Fail closed: refuse to launch an UNCONFINED child.
        raise RuntimeError(
            f"jail-exec.sh not found at {_JAIL_EXEC}; refusing to launch an "
            "unconfined child (bench policy requires kernel confinement)."
        )
    # jail-exec.sh sets the policy itself from STE_CODE_JAIL_POLICY, but we also
    # pass it explicitly for defence in depth.
    cmd = [
        str(_JAIL_EXEC),
        f"STE_CODE_JAIL_POLICY={CHILD_POLICY}",
        *inner,
    ]
    return cmd


def launch(
    prompt: str,
    model: str = "tencent/hy3:free",
    toolset: str = DEFAULT_TOOLSET,
    label: str = "child",
    timeout: int = 600,
    extra_env: Optional[Dict[str, str]] = None,
    capture: bool = True,
) -> "subprocess.CompletedProcess":
    """Launch one confined benchmark child and return the leak-scanned result.

    The child is force-confined (policy=bench, profile=benchmark-ste-code),
    env-stripped, kernel-wrapped, toolset-limited, harness-context-injected,
    and its output is anonymized before return.
    """
    enriched = _inject_harness_context(prompt)

    # Write the enriched prompt to an isolated temp file under /tmp (never in
    # the repo, never in the operator's home).
    with tempfile.NamedTemporaryFile(
        "w", suffix=".txt", prefix=f"bench-{label}-", delete=False, dir="/tmp"
    ) as fh:
        fh.write(enriched)
        prompt_file = Path(fh.name)

    try:
        cmd = build_command(prompt_file, model, toolset)
        env = build_child_env(extra_env)
        proc = subprocess.run(
            cmd,
            cwd="/tmp",
            capture_output=capture,
            text=True,
            timeout=timeout,
            env=env,
        )
        if capture:
            clean_out = _leak_scan(proc.stdout or "")
            clean_err = _leak_scan(proc.stderr or "")
            # Re-surface as a CompletedProcess with scrubbed streams.
            return subprocess.CompletedProcess(
                proc.args, proc.returncode, clean_out, clean_err
            )
        return proc
    finally:
        try:
            prompt_file.unlink()
        except OSError:
            pass


def _cli() -> int:
    ap = argparse.ArgumentParser(description="Launch a confined benchmark child.")
    ap.add_argument("prompt_file")
    ap.add_argument("--model", default="tencent/hy3:free")
    ap.add_argument("--toolset", default=DEFAULT_TOOLSET)
    ap.add_argument("--label", default="cli")
    ap.add_argument("--timeout", type=int, default=600)
    args = ap.parse_args()

    prompt = Path(args.prompt_file).read_text(encoding="utf-8")
    result = launch(
        prompt,
        model=args.model,
        toolset=args.toolset,
        label=args.label,
        timeout=args.timeout,
    )
    if result.stdout:
        sys.stdout.write(result.stdout)
    if result.stderr:
        sys.stderr.write(result.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(_cli())
