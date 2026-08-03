#!/usr/bin/env python3
"""post_tool_call hook: format edited files only. NO LLM.

Fires after write_file and patch. Runs the appropriate formatter
(black, prettier, shfmt, rustfmt) and exits in <2s total.

Design:
  - Fast: only runs local formatters, no network/LLM
  - Safe: skips generated dirs (node_modules, target, Generated)
  - Non-blocking: errors are silent
"""

import json
import os
import subprocess
import sys
from pathlib import Path

HERMES_HOME = Path(os.path.expanduser("~/.hermes"))
CACHE_DIR = HERMES_HOME / "cache" / "post-edit"
FORMAT_TIMEOUT = 5

# Extensions mapped to formatter
FORMATTERS = {
    'py': 'python',
    'js': 'javascript',
    'ts': 'typescript',
    'jsx': 'javascript',
    'tsx': 'typescript',
    'css': 'css',
    'json': 'json',
    'md': 'markdown',
    'yaml': 'yaml',
    'yml': 'yaml',
    'sh': 'shell',
    'bash': 'shell',
    'rs': 'rust',
    'html': 'html',
    'toml': 'toml',
}

# Formatter name mapped to tool
TOOL_MAP = {
    'python': 'black',
    'javascript': 'prettier',
    'typescript': 'prettier',
    'css': 'prettier',
    'json': 'prettier',
    'markdown': 'prettier',
    'yaml': 'prettier',
    'shell': 'shfmt',
    'rust': 'cargo_fmt',
    'html': 'prettier',
    'toml': 'prettier',
}

SKIP_DIRS = {"node_modules", "Target", "target", "dist", ".git", "Generated", "__pycache__"}


def find_binary(name):
    """Find a formatter binary in common locations."""
    search = subprocess.run(
        ["which", name],
        capture_output=True, text=True, timeout=3
    )
    if search.returncode == 0 and search.stdout.strip():
        return search.stdout.strip()

    # Fallback for cargo_fmt
    if name == "cargo_fmt":
        which = subprocess.run(
            ["which", "cargo"],
            capture_output=True, text=True, timeout=3
        )
        if which.returncode == 0:
            return "cargo_fmt"

    return None


def format_file(filepath, tool_name):
    """Run the formatter on the file. Returns (success, detail)."""
    try:
        if tool_name == "shfmt":
            subprocess.run(
                ["shfmt", "-w", filepath],
                capture_output=True, text=True, timeout=FORMAT_TIMEOUT
            )
            return (True, "shfmt")

        elif tool_name == "prettier":
            bin_path = find_binary("prettier")
            if not bin_path:
                return (False, "prettier not found")
            subprocess.run(
                [bin_path, "--write", filepath, "--log-level", "warn"],
                capture_output=True, text=True, timeout=FORMAT_TIMEOUT,
                cwd=os.path.dirname(filepath) or "."
            )
            return (True, "prettier")

        elif tool_name == "black":
            subprocess.run(
                ["black", "-q", filepath],
                capture_output=True, text=True, timeout=FORMAT_TIMEOUT
            )
            return (True, "black")

        elif tool_name == "cargo_fmt":
            # Find Cargo.toml in parent dirs
            parent = Path(filepath).parent
            for _ in range(8):
                if (parent / "Cargo.toml").exists():
                    subprocess.run(
                        ["cargo", "fmt", "--", filepath],
                        capture_output=True, text=True, timeout=FORMAT_TIMEOUT,
                        cwd=str(parent)
                    )
                    return (True, "cargo fmt")
                if parent == parent.parent:
                    break
                parent = parent.parent
            return (False, "no Cargo.toml found")

        return (False, f"unknown tool: {tool_name}")

    except subprocess.TimeoutExpired:
        return (False, "timed out")
    except Exception as e:
        return (False, str(e))


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return
        payload = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        return

    tool_input = payload.get("tool_input", {})

    # Extract file path (Hermes uses .path, not .file_path)
    filepath = tool_input.get("path", "")
    if not filepath:
        return

    filepath = os.path.expanduser(filepath)

    # Skip internal/generated files
    if ".hermes" in filepath:
        return
    for d in SKIP_DIRS:
        if d in filepath:
            return

    if not os.path.isfile(filepath):
        return

    ext = Path(filepath).suffix.lstrip(".")
    lang = FORMATTERS.get(ext)
    if not lang:
        return

    tool_name = TOOL_MAP.get(lang)
    if not tool_name:
        return

    bin_available = find_binary(tool_name) if tool_name != "cargo_fmt" else find_binary("cargo")
    if not bin_available:
        return

    success, detail = format_file(filepath, tool_name)

    # Log result for next turn
    if success:
        print(json.dumps({
            "action": "formatted",
            "tool": detail,
            "file": filepath,
        }))


if __name__ == "__main__":
    main()
