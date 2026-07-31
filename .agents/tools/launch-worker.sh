#!/usr/bin/env bash
# STE-Code Worker Launcher — agent-agnostic, pre-configured for Hermes
#
# Usage: .agents/tools/launch-worker.sh <prompt_file> [--agent AGENT] [--model MODEL] [output_file]
#
# Agents are configured in .agents/config/agents.yaml.
# Default: hermes with poolside/laguna-s-2.1:free.
# If output_file is provided, captures stdout to that file and backgrounds.
#
# Examples:
#   launch-worker.sh prompt.txt                           # hermes, foreground
#   launch-worker.sh prompt.txt --agent claude            # claude, foreground
#   launch-worker.sh prompt.txt --model gpt-4o out.txt    # hermes+gpt-4o, background

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

AGENT_RUNNER="$SCRIPT_DIR/agent-runner.py"
PROMPT_FILE="$1"; shift

# Parse optional flags
AGENT=""
MODEL=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent) AGENT="$2"; shift 2 ;;
        --model) MODEL="$2"; shift 2 ;;
        *) break ;;
    esac
done

OUTPUT_FILE="${1:-}"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "ERROR: Prompt file not found: $PROMPT_FILE" >&2
    exit 1
fi

if [ ! -f "$AGENT_RUNNER" ]; then
    echo "ERROR: Agent runner not found: $AGENT_RUNNER" >&2
    exit 1
fi

# Build agent-runner CLI args
RUNNER_ARGS=("$PROMPT_FILE")
[ -n "$AGENT" ] && RUNNER_ARGS+=(--agent "$AGENT")
[ -n "$MODEL" ] && RUNNER_ARGS+=(--model "$MODEL")

# Auto-detect Python (prefer hermes venv, fall back to system python3)
if [ -f "$HOME/.hermes/hermes-agent/venv/bin/python3" ]; then
    PYTHON="$HOME/.hermes/hermes-agent/venv/bin/python3"
elif [ -f "$PROJECT_ROOT/.hermes/hermes-agent/venv/bin/python3" ]; then
    PYTHON="$PROJECT_ROOT/.hermes/hermes-agent/venv/bin/python3"
else
    PYTHON="python3"
fi

if [ -n "$OUTPUT_FILE" ]; then
    # Background mode with output capture
    mkdir -p "$(dirname "$OUTPUT_FILE")"
    nohup "$PYTHON" "$AGENT_RUNNER" "${RUNNER_ARGS[@]}" > "$OUTPUT_FILE" 2>&1 &
    echo "Worker launched (PID: $!) → $OUTPUT_FILE"
else
    # Foreground mode
    "$PYTHON" "$AGENT_RUNNER" "${RUNNER_ARGS[@]}"
fi
