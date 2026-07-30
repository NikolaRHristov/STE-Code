#!/usr/bin/env bash
# STE-Code Worker Launcher — auto-detects hermes venv, uses local wrapper
# Usage: .agents/tools/launch-worker.sh <prompt_file> [--model MODEL] [output_file]
# If output_file is provided, captures stdout to that file and backgrounds.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Auto-detect venv Python (works on any machine with hermes installed)
if [ -f "$HOME/.hermes/hermes-agent/venv/bin/python3" ]; then
    VENV_PYTHON="$HOME/.hermes/hermes-agent/venv/bin/python3"
elif [ -f "$PROJECT_ROOT/.hermes/hermes-agent/venv/bin/python3" ]; then
    VENV_PYTHON="$PROJECT_ROOT/.hermes/hermes-agent/venv/bin/python3"
else
    echo "ERROR: Could not find hermes venv Python. Install hermes first." >&2
    exit 1
fi

WRAPPER="$SCRIPT_DIR/hermes-oneshot-wrapper.py"
PROMPT_FILE="$1"
MODEL="${2:-deepseek-v4-pro}"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
    exit 1
fi

if [ ! -f "$WRAPPER" ]; then
    echo "ERROR: Wrapper not found: $WRAPPER" >&2
    exit 1
fi

if [ -n "${3:-}" ]; then
    # Background mode with output capture
    OUTPUT_FILE="$3"
    nohup "$VENV_PYTHON" "$WRAPPER" "$PROMPT_FILE" --model "$MODEL" > "$OUTPUT_FILE" 2>&1 &
    echo "Worker launched (PID: $!) → $OUTPUT_FILE"
else
    # Foreground mode
    "$VENV_PYTHON" "$WRAPPER" "$PROMPT_FILE" --model "$MODEL"
fi
