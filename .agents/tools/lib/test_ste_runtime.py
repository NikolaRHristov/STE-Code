#!/usr/bin/env python3
"""Self-test for ste_runtime — pre-flight runtime resolution."""
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_R = next(p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file())
sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))

from ste_runtime import resolve, Runtime, _HARD  # noqa: E402

# 1. resolution from a real unit (artifacts) produces all knobs
rt = resolve(_R / ".agents" / "tools" / "artifacts" / "config.yaml")
d = rt.as_dict()
assert d["wrapper"].endswith("hermes-oneshot-wrapper.py"), d["wrapper"]
assert d["venv_python"].endswith("python3"), d["venv_python"]
assert isinstance(d["retry_attempts"], int) and d["retry_attempts"] == _HARD["retry_attempts"]
assert isinstance(d["batch_divisor"], int) and d["batch_divisor"] == _HARD["batch_divisor"]
assert d["encoding"] == "utf-8"
print("ste_runtime: artifacts-knobs OK", json.dumps(d))

# 2. unit override wins over the hard default
rt2 = resolve(_R / ".agents" / "tools" / "artifacts" / "config.yaml",
              overrides={"retry_attempts": 5})
assert rt2.retry_attempts == 5, rt2.retry_attempts
print("ste_runtime: override OK")

# 3. wrapper path is repo-relative, not absolute-configured (no drift)
assert "hermes-oneshot-wrapper.py" in rt.wrapper
print("ste_runtime: wrapper computed from repo OK")
print("ste_runtime self-check OK")
