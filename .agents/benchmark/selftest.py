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
    check(len(cfg.all_variants()) >= 2, "at least two configurations under test")
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
    check(set(full["timelines"]) <= set(full["variants"]),
          "full aliases timelines consistently with variants (stays joinable)")

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


# --------------------------------------------------------------------- stitch

TECHNIQUES = ("forbidden_bait", "nested_quote_bait", "spelling_drift")
PLACEMENTS = ("head", "nested", "table_cell")


def _plant_fixture(cfg, base: Path) -> None:
    """Two variants x two rounds, with signals deliberately planted.

    `nested_quote_bait` escapes in every placement and `nested` defeats every
    technique, so a detector that cannot rank those two to the top is broken.
    Variant 1 round 2 is RED-only, to exercise the partial-cell path.
    """
    for variant in ("0", "1"):
        for rnd in (1, 2):
            rdir = cfg.round_dir(base, variant, rnd)
            rdir.mkdir(parents=True, exist_ok=True)
            escapes = []
            for tech in TECHNIQUES:
                for place in PLACEMENTS:
                    if tech != "nested_quote_bait" and place != "nested":
                        continue
                    n = len(escapes) + 1
                    escapes.append({
                        "variant": variant, "round": rnd,
                        "test_id": "red-{}-{}-{}-{:03d}".format(variant, tech, place, n),
                        "technique": tech, "placement": place,
                        "timing": ("immediate", "escalating")[n % 2],
                        "missed_principles": [cfg.rule(1)],
                        "correctness_score": 0.55,
                    })
            (rdir / cfg.handshake.red_ledger).write_text(json.dumps(escapes))
            (rdir / cfg.handshake.red_sentinel).write_text(json.dumps({
                "variant": variant, "round": rnd,
                "red_total": 36, "red_passed": 36 - len(escapes),
                "red_pass_rate_pct": round((36 - len(escapes)) / 36 * 100, 1),
                "escapes": len(escapes),
                "attack_matrix": [{"technique": t, "placement": p, "cases": 4}
                                  for t in TECHNIQUES for p in PLACEMENTS],
            }))
            if variant == "1" and rnd == 2:
                continue
            resistance = [{"technique": t, "placement": p, "probes": 3,
                           "passed": 0 if p == "nested" else (1 if t == "nested_quote_bait" else 3),
                           "resistance_pct": 0.0 if p == "nested" else 100.0}
                          for t in TECHNIQUES for p in PLACEMENTS]
            probes = sum(r["probes"] for r in resistance)
            passed = sum(r["passed"] for r in resistance)
            (rdir / cfg.handshake.blue_sentinel).write_text(json.dumps({
                "variant": variant, "round": rnd, "blue_probes": probes,
                "blue_passed": passed,
                "blue_pass_rate_pct": round(passed / probes * 100, 1),
                "residual_escapes": len(escapes) // 2, "resistance": resistance,
            }))
            if rnd == 1:
                (rdir / cfg.handshake.white_sentinel).write_text(json.dumps({
                    "variant": variant, "round": rnd, "status": "done",
                    "remedies_proposed": 4, "remedies_adopted": 2}))
    (base / cfg.handshake.knowledge_base).write_text(json.dumps({
        "schema_version": 1, "lessons": [{"id": "l1"}, {"id": "l2"}],
        "patterns": [{"id": "p1"}]}))


def test_stitch(cfg, base: Path) -> None:
    """PURPLE must recover the planted signals and redact its own output."""
    _plant_fixture(cfg, base)
    proc = subprocess.run(
        [sys.executable, str(BENCH / "purple_stitch.py"), "--variants", "0,1",
         "--rounds", "2", "--base", str(base), "--quiet"],
        capture_output=True, text=True)
    check(proc.returncode == 0, "purple_stitch runs clean")
    if proc.returncode != 0:
        print(proc.stderr[-800:])
        return

    report = json.loads((base / cfg.handshake.stitch_report).read_text())
    cov = report["coverage"]
    check(cov["cells_with_data"] == cov["planned_cells"] == 4, "all four cells stitched")
    check((cov["complete"], cov["partial"]) == (2, 2), "partial rounds reported as partial")

    by_tech = {r["technique"]: r for r in report["by_technique"]}
    by_place = {r["placement"]: r for r in report["by_placement"]}
    check(max(by_tech, key=lambda k: by_tech[k]["escapes"]) == "nested_quote_bait",
          "planted omni-technique ranked first")
    check(max(by_place, key=lambda k: by_place[k]["escapes"]) == "nested",
          "planted omni-placement ranked first")
    check(by_place["nested"]["resistance_pct"] == 0.0, "defeated placement shows zero resistance")
    check(all(r["durability"]["durable"] > 0 for r in report["variant_ranking"]),
          "repeat escapes across rounds detected as durable")
    check(report["knowledge_summary"]["lessons"] == 2, "knowledge base read")
    check(report["timing_profile"], "timing profile populated")

    emitted = json.dumps(report) + (base / "report.md").read_text()
    check("Interplay matrix" in (base / "report.md").read_text(), "markdown renders the matrix")
    check(str(Path.home()) not in emitted and "/Volumes/" not in emitted,
          "emitted report carries no filesystem identity")


# -------------------------------------------------------------- colour modules

def test_modules_compile() -> None:
    """Every module present must import under the interpreter that runs it."""
    for path in sorted(BENCH.glob("*.py")):
        if path.name == "selftest.py":
            continue
        proc = subprocess.run([sys.executable, "-m", "py_compile", str(path)],
                              capture_output=True, text=True)
        check(proc.returncode == 0, "compiles: {}".format(path.name))


def main() -> int:
    cfg = load_config(reload=True)
    root = cfg.root
    test_config(cfg)
    test_anonymizer(cfg, root)
    tmp = Path(tempfile.mkdtemp(prefix="harness-selftest-"))
    try:
        test_stitch(cfg, tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    test_modules_compile()

    failed = [label for ok, label in CHECKS if not ok]
    for ok, label in CHECKS:
        if not ok:
            print("FAIL  {}".format(label))
    print("{}/{} checks passed".format(len(CHECKS) - len(failed), len(CHECKS)))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
