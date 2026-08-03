#!/usr/bin/env python3
"""Self-test for the per-purpose configuration loader.

Guards the properties that make the design worth having:

1. ``defaults.yaml`` cannot grow beyond ``agent:`` — the structural guarantee
   that shared defaults never become the global config we rejected.
2. A path declared in a config cannot escape the repository.
3. A missing key fails loudly instead of returning ``None``.
4. Resolution order holds: defaults < unit < environment < explicit argument.
5. A unit config declares its own footprint and the loader can print it.

Run:  python3 .agents/tools/lib/test_ste_config.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_R = next(
    p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))

import ste_config as sc  # noqa: E402

UNIT = _R / ".agents" / "tools" / "refinement" / "refine_batch.py"
DEFAULTS = _R / ".agents" / "config" / "defaults.yaml"

_failures = 0


def check(ok: bool, label: str) -> None:
    global _failures
    print(f"  [{'ok' if ok else 'FAIL'}]   {label}")
    if not ok:
        _failures += 1


def main() -> int:
    print("config loader")

    # 1. anti-global-config guard -------------------------------------------
    original = DEFAULTS.read_text(encoding="utf-8")
    try:
        DEFAULTS.write_text(
            original + "\ninputs:\n  sneaky: ste-code/extracted\n", encoding="utf-8"
        )
        try:
            sc.load(UNIT)
            check(False, "defaults.yaml rejects a non-agent section")
        except sc.ConfigError:
            check(True, "defaults.yaml rejects a non-agent section")
    finally:
        DEFAULTS.write_text(original, encoding="utf-8")

    cfg = sc.load(UNIT)

    # 2. repository boundary -------------------------------------------------
    cfg._data.setdefault("outputs", {})["_escape"] = "/".join(["..", "..", "..", "etc"])
    try:
        cfg.path("outputs._escape")
        check(False, "a path escaping the repository is refused")
    except Exception:
        check(True, "a path escaping the repository is refused")
    del cfg._data["outputs"]["_escape"]

    # 3. loud failure --------------------------------------------------------
    try:
        cfg.get("thresholds.does_not_exist")
        check(False, "a missing key raises instead of returning None")
    except sc.ConfigError:
        check(True, "a missing key raises instead of returning None")
    check(
        cfg.get("thresholds.does_not_exist", None) is None,
        "an explicit default is still honoured",
    )

    # 4. resolution order ----------------------------------------------------
    # The refinement unit overrides the shared default, so its model is poolside;
    # a unit without an override (extraction) inherits tencent from defaults.
    check(
        sc.load(_R / ".agents" / "tools" / "extraction" / "config.yaml").model
        == "tencent/hy3:free",
        "a unit without an override inherits the shared model default",
    )
    check(
        cfg.model == "poolside/laguna-s-2.1:free",
        "the refinement unit's own model override wins over the shared default",
    )

    os.environ["STE_MODEL"] = "env/model:test"
    try:
        check(sc.load(UNIT).model == "env/model:test", "environment overrides the unit")
    finally:
        del os.environ["STE_MODEL"]

    check(
        sc.load(UNIT, overrides={"agent.model": "cli/model"}).model == "cli/model",
        "an explicit argument wins over everything",
    )

    # 5. footprint -----------------------------------------------------------
    text = cfg.footprint()
    check(
        "inputs:" in text and "outputs:" in text, "footprint lists inputs and outputs"
    )
    check(
        cfg.render("layout.refined_file", worker=7, start=1, end=4) == "r007-p1-4.md",
        "layout patterns render from configuration",
    )
    check(
        bool(cfg.regex("layout.worker_re").match("w001-p1-4.md")),
        "declared filename regex matches a real source name",
    )

    # every declared path stays inside the repository
    inside = all(
        str(p).startswith(str(_R))
        for p in {**cfg.paths("inputs"), **cfg.paths("outputs")}.values()
    )
    check(inside, "every declared path resolves inside the repository")

    print(
        f"\nRESULT: {'all checks passed' if not _failures else f'{_failures} failure(s)'}"
    )
    return 1 if _failures else 0


if __name__ == "__main__":
    sys.exit(main())
