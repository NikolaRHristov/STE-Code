#!/usr/bin/env python3
"""
Generic Agent Runner — execute prompts through any AI agent backend.

Pre-configured for Hermes Agent as default. Supports Claude, Codex, and
custom backends via a simple YAML config.

Usage:
    from agent_runner import run_agent, launch_agent, get_agent_config

    # Synchronous (blocks until done)
    result = run_agent(prompt, agent="hermes", model="tencent/hy3:free")
    print(result.stdout)

    # Async (returns Popen)
    proc = launch_agent(prompt, agent="hermes")
    stdout, stderr = proc.communicate(timeout=600)

    # Use default agent/model from config
    result = run_agent(prompt)

Config: .agents/config/agents.yaml (auto-created with Hermes defaults if missing)

Add a new agent by appending to agents.yaml:
    agents:
      my-agent:
        command: /path/to/binary
        args: ["--prompt", "{prompt_file}"]
        default_model: my-model
"""

import os, sys, subprocess, json
from pathlib import Path

# ── Resolve paths ───────────────────────────────────────────────
# File is at: .agents/tools/lib/agent-runner.py
# _TOOLS = .agents/tools/ (parent of lib/)
# _AGENTS = .agents/ (parent of tools/)
# _PROJECT = STE-Code root (parent of .agents/)
_TOOLS = Path(__file__).resolve().parent.parent  # tools/lib → tools/
_AGENTS = _TOOLS.parent  # tools/ → .agents/
_PROJECT = _AGENTS.parent  # .agents/ → STE-Code root
_CONFIG_DIR = _AGENTS / "config"
_CONFIG_FILE = _CONFIG_DIR / "agents.yaml"
_TMP_DIR = _AGENTS / "tmp"

# ── Default configuration (Hermes pre-configured) ─────────────────
_DEFAULT_CONFIG = {
    "default_agent": "hermes",
    "agents": {
        "hermes": {
            "runtime": "~/.hermes/hermes-agent/venv/bin/python3",
            "wrapper": "lib/hermes-oneshot-wrapper.py",
            "default_model": "tencent/hy3:free",
            "env": {
                "HERMES_REASONING_EFFORT": "high",
                "HERMES_YOLO_MODE": "1",
                "HERMES_ACCEPT_HOOKS": "1",
            },
        },
        "claude": {
            "command": "claude",
            "args": ["-p", "--print", "--output-format", "text"],
            "default_model": "claude-sonnet-4-20250514",
            "env": {},
            "prompt_arg": "--prompt-file",
        },
        "codex": {
            "command": "codex",
            "args": ["exec"],
            "default_model": "gpt-4o",
            "env": {},
            "prompt_arg": "--prompt-file",
        },
        "generic": {
            "command": None,
            "args": [],
            "default_model": None,
            "env": {},
            "prompt_arg": None,
        },
    },
}


def _load_config():
    """Load agent config, creating default if missing."""
    if _CONFIG_FILE.exists():
        try:
            import yaml
            with open(_CONFIG_FILE) as f:
                return yaml.safe_load(f)
        except ImportError:
            # Fallback to JSON if yaml not available
            json_file = _CONFIG_DIR / "agents.json"
            if json_file.exists():
                with open(json_file) as f:
                    return json.load(f)

    # Auto-create default config
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        import yaml
        with open(_CONFIG_FILE, "w") as f:
            yaml.dump(_DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False)
    except ImportError:
        json_file = _CONFIG_DIR / "agents.json"
        with open(json_file, "w") as f:
            json.dump(_DEFAULT_CONFIG, f, indent=2)

    return dict(_DEFAULT_CONFIG)


def get_agent_config(agent=None):
    """Get configuration for a specific agent (default from config if None)."""
    cfg = _load_config()
    agent = agent or cfg.get("default_agent", "hermes")
    agent_cfg = cfg.get("agents", {}).get(agent)
    if not agent_cfg:
        raise ValueError(f"Unknown agent: {agent}. Available: {list(cfg.get('agents', {}).keys())}")
    return agent_cfg


def _resolve_command(agent_cfg, prompt_file, model=None, cwd=None):
    """Build the command line for an agent backend."""
    cwd = Path(cwd) if cwd else _PROJECT
    cmd = []

    agent_type = None
    cfg = _load_config()
    for name, acfg in cfg.get("agents", {}).items():
        if acfg == agent_cfg:
            agent_type = name
            break

    if agent_type == "hermes":
        # Hermes uses its venv + oneshot wrapper
        runtime = os.path.expanduser(str(agent_cfg["runtime"]))
        # Wrapper path in config is relative to .agents/tools/
        wrapper = str((_TOOLS / agent_cfg["wrapper"]).resolve())
        effective_model = model or agent_cfg.get("default_model", "tencent/hy3:free")
        cmd = [runtime, wrapper, str(prompt_file), "--model", effective_model]
    else:
        # Generic agent CLI
        command = agent_cfg.get("command")
        if not command:
            raise ValueError(f"Agent '{agent_type}' has no command configured.")
        cmd = [command]

        # Add prompt argument
        prompt_flag = agent_cfg.get("prompt_arg", "--prompt-file")
        if prompt_flag:
            cmd.extend([prompt_flag, str(prompt_file)])
        else:
            # Read prompt into stdin
            pass  # handled by stdin below

        # Add extra args
        if agent_cfg.get("args"):
            cmd.extend(agent_cfg["args"])

    return cmd, agent_cfg.get("env", {})


def run_agent(prompt, agent=None, model=None, cwd=None, timeout=600, skill=None):
    """
    Run a prompt through an agent synchronously.

    Args:
        prompt: The prompt text to send
        agent: Agent name (default from config)
        model: Model override (default from agent config)
        cwd: Working directory (default: project root)
        timeout: Max seconds to wait
        skill: Optional STE-Code pipeline skill name (e.g. "grouping",
               "adaptation"). When provided, the authoritative SKILL.md text is
               embedded into the prompt so the worker honors the pipeline rules
               even though the oneshot wrapper sub-agents do not auto-load the
               STE-Code profile skills. Edit the SKILL.md (not callers) to
               change behavior.

    Returns:
        subprocess.CompletedProcess with .stdout and .stderr
    """
    cwd = Path(cwd) if cwd else _PROJECT

    # Embed the authoritative skill text (keeps prompt + skill in lockstep).
    if skill:
        try:
            import importlib.util as _ilu
            _sp = _ilu.spec_from_file_location(
                "skill_prompt", str(_TOOLS / "lib" / "skill_prompt.py"))
            _m = _ilu.module_from_spec(_sp)
            _sp.loader.exec_module(_m)
            prompt = prompt + _m.skill_section(skill)
        except Exception:
            pass  # skill embedding is best-effort; prompt still runs

    agent_cfg = get_agent_config(agent)
    _TMP_DIR.mkdir(parents=True, exist_ok=True)

    # Write prompt to temp file
    prompt_file = _TMP_DIR / f"agent-prompt-{os.getpid()}.txt"
    prompt_file.write_text(prompt)

    try:
        cmd, env_vars = _resolve_command(agent_cfg, prompt_file, model, cwd)
        env = {**os.environ, **env_vars}

        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        return result
    finally:
        # Clean up temp file
        try:
            prompt_file.unlink()
        except OSError:
            pass


def launch_agent(prompt, agent=None, model=None, cwd=None):
    """
    Launch a prompt through an agent asynchronously (non-blocking).

    Args:
        prompt: The prompt text to send
        agent: Agent name (default from config)
        model: Model override (default from agent config)
        cwd: Working directory (default: project root)

    Returns:
        subprocess.Popen
    """
    cwd = Path(cwd) if cwd else _PROJECT
    agent_cfg = get_agent_config(agent)
    _TMP_DIR.mkdir(parents=True, exist_ok=True)

    prompt_file = _TMP_DIR / f"agent-prompt-{os.getpid()}.txt"
    prompt_file.write_text(prompt)

    cmd, env_vars = _resolve_command(agent_cfg, prompt_file, model, cwd)
    env = {**os.environ, **env_vars}

    return subprocess.Popen(
        cmd,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )


def get_agent_command(agent=None, model=None, cwd=None, prompt_file=None):
    """
    Get the command and environment for self-exec (os.execvpe) usage.

    Returns (cmd_list, env_dict). The caller can pass cmd_list to os.execvpe.

    Args:
        agent: Agent name (default from config)
        model: Model override
        cwd: Working directory
        prompt_file: Path to prompt file (required for exec mode)
    """
    cwd = Path(cwd) if cwd else _PROJECT
    agent_cfg = get_agent_config(agent)

    # Write prompt to temp file if not provided
    if prompt_file is None:
        _TMP_DIR.mkdir(parents=True, exist_ok=True)
        prompt_file = _TMP_DIR / f"agent-prompt-{os.getpid()}.txt"

    cmd, env_vars = _resolve_command(agent_cfg, Path(prompt_file), model, cwd)
    env = {**os.environ, **env_vars}
    return cmd, env


# ── CLI mode (for testing / direct invocation) ────────────────────
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generic Agent Runner")
    parser.add_argument("prompt_file", nargs="?", help="File containing the prompt")
    parser.add_argument("--agent", default=None, help="Agent backend (default from config)")
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument("--list", action="store_true", help="List available agents")
    args = parser.parse_args()

    if args.list:
        cfg = _load_config()
        print(f"Default agent: {cfg.get('default_agent', 'hermes')}")
        print("Available agents:")
        for name, acfg in cfg.get("agents", {}).items():
            model = acfg.get("default_model", "none")
            print(f"  {name}: model={model}")
        sys.exit(0)

    prompt = Path(args.prompt_file).read_text()
    result = run_agent(prompt, agent=args.agent, model=args.model)
    sys.stdout.write(result.stdout or "")
    if result.stderr:
        sys.stderr.write(result.stderr)
    sys.exit(result.returncode)
