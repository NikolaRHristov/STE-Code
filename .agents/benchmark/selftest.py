#!/usr/bin/env python3
"""Canonical self-test for the adversarial harness.

    python3 .agents/benchmark/selftest.py

The harness has no external test framework and no network access in CI, so this
is the one command that proves the shared layers still hold. Colour modules
(red/blue/white/black/notes) are checked only if present — they are built by
independent workers and may legitimately be absent.

Exit 0 = green. Any failure prints the failing check and exits 1.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

BENCH = Path(__file__).resolve().parent
sys.path.insert(0, str(BENCH))

import anonymize  # noqa: E402
from harness_config import load_config  # noqa: E402

CHECKS: "list[tuple[bool, str]]" = []


def check(ok: object, label: str) -> None:
    CHECKS.append((bool(ok), label))


# --------------------------------------------------------------------- config

def test_config(cfg) -> None:
    """Every shared name must come from the profile document, not from code."""
    doc = json.loads((BENCH / "config" / "harness.json").read_text())

    hs = {k: v for k, v in doc["handshake"].items() if not k.startswith("$")}
    check(all(getattr(cfg.handshake, k) == v for k, v in hs.items()),
          "handshake mirrors the profile document key-for-key")
    check(len(cfg.variants) >= 2, "at least two configurations under test")
    check(cfg.techniques and cfg.placements and cfg.timings, "attack axes populated")
    check(cfg.default_partition_strategy in cfg.partition_strategies,
          "default partition strategy is one of the declared strategies")
    check(cfg.derivation_arm != cfg.verification_arm,
          "derivation and verification arms are distinct")
    check(set(cfg.note_colours) >= {"red", "blue", "purple", "white", "black"},
          "all five colours declared")
    check(set(cfg.ack_dispositions) == {"accepted", "deferred", "rejected"},
          "acknowledgement dispositions")
    check(len(cfg.verdict_kinds) == 5, "five verdict kinds")

    base = Path("/nonexistent-base")
    check(cfg.notes_dir(base).name == cfg.handshake.notes_dir, "notes dir path")
    check(cfg.notes_index_path(base).name == cfg.handshake.notes_index, "notes index path")
    check(cfg.black_sentinel_path(base, "0", 1).name == cfg.handshake.black_sentinel,
          "black sentinel path")
    check(cfg.attack_brief_path(base).name == cfg.handshake.attack_brief, "attack brief path")
    check(cfg.verdicts_path(base).name == cfg.handshake.verdicts, "verdicts path")


# ---------------------------------------------------------------- anonymizer

def test_anonymizer(cfg, root: Path) -> None:
    """Redaction must remove identity and preserve every measurement."""
    home = str(Path.home())
    sample = {
        "profile": {"id": cfg.profile_id, "display_name": cfg.display_name,
                    "source": str(BENCH / "config" / "harness.json")},
        "base": str(BENCH / "tests"),
        "variants": ["0", "1"],
        "variant_ranking": [{"variant": "0", "label": "baseline", "directory": "level0",
                             "total_escapes": 12, "blue_resistance_pct": 44.4}],
        "timelines": {"0": [{"round": 1, "escapes": 12}]},
        "coverage": {"missing": [home + "/secret/path"]},
    }
    leaks = (home, "/Volumes/", "/Users/")

    off = anonymize.Anonymizer("off", root=root)
    check(off.report(sample) is sample, "level=off is a passthrough, not a copy")

    for level in ("paths", "full"):
        anon = anonymize.Anonymizer(level, root=root,
                                    extra_terms=[cfg.profile_id, cfg.display_name])
        out = json.dumps(anon.report(sample))
        check(not any(leak in out for leak in leaks), f"level={level}: no filesystem identity")
        check('"total_escapes": 12' in out and "44.4" in out,
              f"level={level}: measurements preserved")

    paths = anonymize.Anonymizer("paths", root=root).report(sample)
    check(paths["profile"]["id"] == cfg.profile_id, "level=paths keeps semantics readable")

    full = anonymize.Anonymizer("full", root=root,
                                extra_terms=[cfg.profile_id, cfg.display_name]).report(sample)
    check(full["profile"]["id"] != cfg.profile_id, "level=full pseudonymizes the profile")
    check(full["variant_ranking"][0]["variant"].startswith("variant-"), "full aliases variants")
    check(full["variant_ranking"][0]["directory"].startswith("dir-"), "full aliases directories")
    check(set(full["timelines"]) == set(full["variants"]), "full keeps timelines joinable")

    a1 = anonymize.Anonymizer("full", root=root, salt="s1")
    a2 = anonymize.Anonymizer("full", root=root, salt="s1")
    a3 = anonymize.Anonymizer("full", root=root, salt="s2")
    check(a1.variant("0") == a2.variant("0"), "same salt -> stable alias (reports stay diffable)")
    check(a1.variant("0") != a3.variant("0"), "different salt -> unlinkable")
    check(a1.variant("0") != a1.variant("1"), "distinct inputs -> distinct aliases")

    try:
        anonymize.Anonymizer("bogus")
        check(False, "invalid level rejected")
    except ValueError:
        check(True, "invalid level rejected")
