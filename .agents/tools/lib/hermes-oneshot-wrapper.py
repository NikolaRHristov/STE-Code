#!/usr/bin/env python3
"""Hermes oneshot wrapper — the single entry point for confined benchmark child sessions.

Adapted from <maintain-repo>/Fn/HermesOneshotWrapper.py.real.bak (the
genuine Save/gcommit oneshot wrapper) for the STE-Code benchmark lockdown.

Always invoked by launch_confined_child.build_command(), which has already:
  * pinned STE_CODE_JAIL_POLICY + HERMES_PROFILE,
  * stripped the environment (only PATH/LANG/etc.; creds dropped),
  * reset HOME=/tmp,
  * wrapped the command in jail-exec.sh (Layer-2 kernel confinement).

Invoked as:
    python3 hermes-oneshot-wrapper.py <prompt_file> --model M --toolsets T [--profile P] [--yolo]

Fail-closed hardening (per the benchmark handoff):
  * refuses to start if STE_CODE_JAIL_POLICY is unset (no unconfined launch),
  * refuses if HOME still points at the operator's real home,
  * NEVER hardcodes HERMES_YOLO_MODE / HERMES_ACCEPT_HOOKS — honors a
    parent-set value or --yolo, defaulting OFF (the parent decides).

Runs the agent WITHOUT a session database (no history pollution), same as the
original oneshot design.
"""

import sys
import os

# Add hermes to the Python path (the confined child runs under the hermes venv).
HERMES_VENV = os.path.expanduser("~/.hermes/hermes-agent/venv")
HERMES_SITE = os.path.join(
    HERMES_VENV,
    "lib",
    f"python{sys.version_info.major}.{sys.version_info.minor}",
    "site-packages",
)
sys.path.insert(0, HERMES_SITE)

# Silence all logging for oneshot mode.
import logging

logging.disable(logging.CRITICAL)

from hermes_cli.config import load_config
from hermes_cli.models import detect_provider_for_model
from hermes_cli.runtime_provider import resolve_runtime_provider
from hermes_cli.tools_config import _get_platform_tools
from hermes_cli.fallback_config import get_fallback_chain
from hermes_cli.oneshot import _normalize_toolsets, _oneshot_clarify_callback
from run_agent import AIAgent


def _fail_closed(msg: str) -> int:
    sys.stderr.write(f"hermes-oneshot-wrapper: refusing to start — {msg}\n")
    return 1


def run() -> int:
    # ── Fail-closed guards (the parent is responsible for pinning these) ──
    if not os.environ.get("STE_CODE_JAIL_POLICY"):
        return _fail_closed(
            "STE_CODE_JAIL_POLICY is not set (unconfined launch blocked)"
        )
    home = os.environ.get("HOME", "")
    if home.startswith(("/Users/", "/Volumes/", "/home/", "C:\\")):
        return _fail_closed(f"HOME not isolated ({home})")
    # A bare wrapper invoked outside the confined launcher is rejected: the
    # caller must have arrived through jail-exec.sh / launch_confined_child.
    if os.environ.get("STE_CODE_JAIL_POLICY") != "bench" and not os.environ.get(
        "HERMES_PROFILE"
    ):
        return _fail_closed("no pinned profile — launched outside the confined path")

    # Read prompt from the temp file path passed as argument.
    if len(sys.argv) < 2:
        sys.stderr.write(
            "Usage: hermes_oneshot_wrapper.py <prompt_file> [--model M] [--toolsets T] [--profile P] [--yolo]\n"
        )
        return 1

    prompt_file = sys.argv[1]
    try:
        with open(prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read()
    except FileNotFoundError:
        sys.stderr.write(f"Prompt file not found: {prompt_file}\n")
        return 1

    # Delete the temp file immediately after reading.
    try:
        os.remove(prompt_file)
    except OSError:
        pass

    # Parse optional --model, --provider, --toolsets, --profile, --yolo.
    model = None
    provider = None
    toolsets = None
    profile = None
    yolo = False
    argv = sys.argv[2:]
    i = 0
    while i < len(argv):
        if argv[i] == "--model" and i + 1 < len(argv):
            model = argv[i + 1]
            i += 2
        elif argv[i] == "--provider" and i + 1 < len(argv):
            provider = argv[i + 1]
            i += 2
        elif argv[i] == "--toolsets" and i + 1 < len(argv):
            toolsets = argv[i + 1]
            i += 2
        elif argv[i] == "--profile" and i + 1 < len(argv):
            profile = argv[i + 1]
            i += 2
        elif argv[i] == "--yolo":
            yolo = True
            i += 1
        else:
            i += 1

    # Pin the profile if the parent passed one explicitly.
    if profile:
        os.environ["HERMES_PROFILE"] = profile

    # YOLO / hooks are NEVER hardcoded. Honor a parent-set value (from the
    # confined env) or the --yolo flag; default OFF. The parent (orchestrator)
    # decides; a bare child must not auto-approve.
    if yolo or os.environ.get("HERMES_YOLO_MODE", "").lower() in ("1", "true", "yes"):
        os.environ["HERMES_YOLO_MODE"] = "1"
    if os.environ.get("HERMES_ACCEPT_HOOKS", "").lower() in ("1", "true", "yes"):
        os.environ["HERMES_ACCEPT_HOOKS"] = "1"

    cfg = load_config()

    # Resolve effective model.
    model_cfg = cfg.get("model") or {}
    if isinstance(model_cfg, str):
        cfg_model = model_cfg
    else:
        cfg_model = model_cfg.get("default") or model_cfg.get("model") or ""

    env_model = os.getenv("HERMES_INFERENCE_MODEL", "").strip()
    effective_model = (model or "").strip() or env_model or cfg_model

    # Resolve effective provider.
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

    # Toolsets.
    toolsets_list = _normalize_toolsets(toolsets)
    if toolsets_list is None:
        toolsets_list = sorted(_get_platform_tools(cfg, "cli"))

    _fb = get_fallback_chain(cfg)

    # No session_db → nothing saved to session history (oneshot, no pollution).
    # Reasoning forced OFF — this is a cheap oneshot worker, not a reasoning session.
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
        save_trajectories=False,
        credential_pool=runtime.get("credential_pool"),
        fallback_model=_fb or None,
        clarify_callback=_oneshot_clarify_callback,
        reasoning_config={"enabled": False},
    )
    agent.suppress_status_output = True
    agent.stream_delta_callback = None
    agent.tool_gen_callback = None

    response = agent.chat(prompt) or ""
    sys.stdout.write(response)
    if not response.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.flush()

    try:
        import glob

        for f in glob.glob(os.path.expanduser("~/.hermes/data/*oneshot*")):
            try:
                os.remove(f)
            except OSError:
                pass
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(run())
