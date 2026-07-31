#!/usr/bin/env python3
"""
Hermes oneshot stdin wrapper — reference implementation.

Calling convention:
    <venv-python3> hermes-oneshot-wrapper.py <prompt_file> [--model M] [--provider P] [--toolsets T] [--debug]

Reads the prompt from a file (not CLI arg), calls AIAgent directly with
session_db=None to avoid polluting Hermes's session history, and writes
the response to stdout.

Fixes applied:
- Set HERMES_REQUEST_TIMEOUT to prevent silent hangs
- Capture agent diagnostics to stderr for debugging failures
- Flush stdout immediately to prevent buffering issues
- Explicit agent cleanup
- --debug flag saves full trajectory to .agents/tmp/oneshot-debug/ for inspection
- save_trajectories=True when debugging to inspect tool calls and model responses
- Health probe watchdog: background thread that periodically probes the API
  endpoint. If the API is unresponsive for more than HEALTH_PROBE_TIMEOUT seconds,
  the wrapper sends SIGTERM to itself, preventing indefinite hangs when the
  API drops the connection without closing it.
"""
import sys
import os
import logging
import traceback
import threading
import signal
import time
import urllib.request
import urllib.error

logging.disable(logging.CRITICAL)

# ---------------------------------------------------------------------------
# Health probe watchdog — kills the wrapper if the API is unresponsive.
# ---------------------------------------------------------------------------

# How long to wait without API responsiveness before killing the wrapper.
# Default: 180 seconds. Override via HERMES_HEALTH_PROBE_TIMEOUT env var.
HEALTH_PROBE_TIMEOUT = int(os.environ.get("HERMES_HEALTH_PROBE_TIMEOUT", "120"))

# How often to probe the API (seconds).
HEALTH_PROBE_INTERVAL = int(os.environ.get("HERMES_HEALTH_PROBE_INTERVAL", "30"))

# Last successful API contact timestamp (updated by the probe thread).
_api_last_responsive = time.time()
_api_base_url = None  # set in run()


def _probe_api_health():
    """Background thread: periodically check if the API is responsive.

    Sends a lightweight HTTP HEAD request to the API base URL. If the API
    hasn't responded to a probe for HEALTH_PROBE_TIMEOUT seconds, sends
    SIGTERM to the current process to unstick the wrapper.
    """
    global _api_last_responsive
    while True:
        time.sleep(HEALTH_PROBE_INTERVAL)
        url = _api_base_url or "https://inference-api.nousresearch.com/v1"
        try:
            req = urllib.request.Request(url, method="HEAD")
            resp = urllib.request.urlopen(req, timeout=10)
            resp.read()
            _api_last_responsive = time.time()
        except Exception:
            # API probe failed — check if we've been unresponsive too long
            unresponsive_secs = time.time() - _api_last_responsive
            if unresponsive_secs > HEALTH_PROBE_TIMEOUT:
                # The API is unresponsive — kill ourselves
                pid = os.getpid()
                sys.stderr.write(
                    f"HEALTH PROBE: API unresponsive for {unresponsive_secs:.0f}s "
                    f"(timeout={HEALTH_PROBE_TIMEOUT}s). Sending SIGTERM to PID {pid}.\n"
                )
                sys.stderr.flush()
                os.kill(pid, signal.SIGTERM)

from hermes_cli.config import load_config
from hermes_cli.models import detect_provider_for_model
from hermes_cli.runtime_provider import resolve_runtime_provider
from hermes_cli.tools_config import _get_platform_tools
from hermes_cli.fallback_config import get_fallback_chain
from hermes_cli.oneshot import _normalize_toolsets, _oneshot_clarify_callback
from run_agent import AIAgent


def run() -> int:
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: hermes-oneshot-wrapper.py <prompt_file> [--model M] [--provider P] [--toolsets T]\n")
        return 1

    prompt_file = sys.argv[1]
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"Prompt file not found: {prompt_file}\n")
        return 1

    # Clean up immediately after reading
    try:
        os.remove(prompt_file)
    except OSError:
        pass

    # Parse optional flags from remaining args
    model = provider = toolsets = None
    debug = False
    argv = sys.argv[2:]
    i = 0
    while i < len(argv):
        if argv[i] == "--model" and i + 1 < len(argv):
            model = argv[i + 1]; i += 2
        elif argv[i] == "--provider" and i + 1 < len(argv):
            provider = argv[i + 1]; i += 2
        elif argv[i] == "--toolsets" and i + 1 < len(argv):
            toolsets = argv[i + 1]; i += 2
        elif argv[i] == "--debug":
            debug = True; i += 1
        else:
            i += 1

    # ── Build agent (mirrors _run_agent but without session_db) ──
    os.environ["HERMES_YOLO_MODE"] = "true"
    os.environ["HERMES_ACCEPT_HOOKS"] = "1"
    os.environ.setdefault("HERMES_REQUEST_TIMEOUT", "120")

    cfg = load_config()
    model_cfg = cfg.get("model") or {}
    cfg_model = model_cfg if isinstance(model_cfg, str) else model_cfg.get("default") or model_cfg.get("model") or ""
    env_model = os.getenv("HERMES_INFERENCE_MODEL", "").strip()
    effective_model = (model or "").strip() or env_model or cfg_model

    effective_provider = (provider or "").strip() or None
    explicit_base_url = None
    if effective_provider is None and (model or env_model):
        explicit_model = (model or "").strip() or env_model
        if explicit_model:
            try:
                from hermes_cli import model_switch as _ms
                _ms._ensure_direct_aliases()
                direct = _ms.DIRECT_ALIASES.get(explicit_model.strip().lower())
            except Exception:
                direct = None
            if direct is not None:
                effective_model = direct.model
                effective_provider = direct.provider
                if direct.base_url:
                    explicit_base_url = direct.base_url.rstrip("/")
            else:
                cfg_provider = ""
                if isinstance(model_cfg, dict):
                    cfg_provider = str(model_cfg.get("provider") or "").strip().lower()
                current_provider = (
                    cfg_provider
                    or os.getenv("HERMES_INFERENCE_PROVIDER", "").strip().lower()
                    or "auto"
                )
                detected = detect_provider_for_model(explicit_model, current_provider)
                if detected:
                    effective_provider, effective_model = detected

    runtime = resolve_runtime_provider(
        requested=effective_provider,
        target_model=effective_model or None,
        explicit_base_url=explicit_base_url,
    )

    toolsets_list = _normalize_toolsets(toolsets)
    if toolsets_list is None:
        toolsets_list = sorted(_get_platform_tools(cfg, "cli"))

    _fb = get_fallback_chain(cfg)

    # ═══ KEY: no session_db → nothing saved to Hermes history ═══
    # When --debug is active, save trajectory for inspection
    save_traj = debug

    global _api_base_url
    _api_base_url = runtime.get("base_url") or "https://inference-api.nousresearch.com/v1"

    # Start health probe watchdog thread (daemon so it doesn't block exit).
    probe_thread = threading.Thread(target=_probe_api_health, daemon=True)
    probe_thread.start()

    agent = AIAgent(
        api_key=runtime.get("api_key"),
        base_url=runtime.get("base_url"),
        provider=runtime.get("provider"),
        api_mode=runtime.get("api_mode"),
        model=effective_model,
        enabled_toolsets=toolsets_list,
        quiet_mode=True,
        platform="cli",
        session_db=None,
        save_trajectories=save_traj,
        credential_pool=runtime.get("credential_pool"),
        fallback_model=_fb or None,
        clarify_callback=_oneshot_clarify_callback,
    )
    agent.suppress_status_output = True
    agent.stream_delta_callback = None
    agent.tool_gen_callback = None

    try:
        response = agent.chat(prompt) or ""
        # Only write non-empty response to stdout — empty responses
        # are normal when the agent just calls tools without final text
        if response.strip():
            sys.stdout.write(response)
            if not response.endswith("\n"):
                sys.stdout.write("\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stderr.write(f"oneshot-wrapper error: {e}\n")
        sys.stderr.write(traceback.format_exc())
        sys.stderr.flush()
        sys.stdout.write(f"ERROR: {e}\n")
        sys.stdout.flush()
        return 1
    finally:
        try:
            agent.close()
        except Exception:
            pass

    return 0


if __name__ == "__main__":
    sys.exit(run())
