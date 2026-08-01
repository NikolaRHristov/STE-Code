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

def test_notes(cfg, base: Path) -> None:
    """The correspondence bus: protocol rules, threading, staleness, races."""
    try:
        import notes as notes_mod
    except ImportError:
        return  # not built yet; other checks still apply

    bus = notes_mod.NoteBus(cfg, base)
    ev = {"escape_ids": ["red-0-nested_quote_bait-nested-003"]}

    handoff = bus.write("red", "blue", "handoff", "ledger ready for round 1",
                        variant="0", round_n=1, expects_ack=True)
    claim = bus.write("blue", "white", "claim", "resistance is placement-driven",
                      variant="0", round_n=1, evidence=ev, confidence=0.8,
                      expects_ack=True)
    ignored = bus.write("purple", "all", "warning", "attack and probe counts disagree",
                        variant="0", round_n=1, evidence=ev, expects_ack=True)
    brief = bus.write("white", "black", "handoff", "attack brief",
                      variant="0", round_n=2, expects_ack=True)

    check(handoff.id.startswith("red-blue-0-1-"), "note id encodes from/to/variant/round")
    check(bus.read(handoff.id) is not None, "note round-trips through disk")

    # evidence is required exactly for the kinds that assert a fact
    try:
        bus.write("red", "blue", "claim", "no evidence attached", variant="0", round_n=1)
        check(False, "evidence-free claim rejected")
    except notes_mod.NoteError:
        check(True, "evidence-free claim rejected")
    try:
        bus.write("red", "blue", "handoff", "handoff needs no evidence",
                  variant="0", round_n=1)
        check(True, "handoff exempt from evidence rule")
    except notes_mod.NoteError:
        check(False, "handoff exempt from evidence rule")

    # config and code cannot drift apart
    for bad in (("mauve", "blue", "handoff"), ("red", "mauve", "handoff"),
                ("red", "blue", "gossip")):
        try:
            bus.write(bad[0], bad[1], bad[2], "invalid", variant="0", round_n=1)
            check(False, "rejects unknown {}".format(bad))
        except notes_mod.NoteError:
            check(True, "rejects unknown value in {}".format(bad[2]))

    ack = bus.acknowledge(claim.id, "accepted", action_taken="remedy queued")
    check(ack.kind == "acknowledgement" and ack.in_reply_to == claim.id,
          "acknowledgement links to its note")
    reb = bus.acknowledge(handoff.id, "rejected", rebuttal="counts disagree",
                          evidence=ev)
    check(reb.kind == "rebuttal", "a rejection is recorded as a rebuttal")

    chain = bus.thread(claim.id)
    check([n.id for n in chain] == [claim.id, ack.id], "thread reconstructs the reply chain")

    unacked = [n.id for n in bus.inbox("black", unacked_only=True)]
    check(brief.id in unacked, "unacked inbox finds the open note addressed to the colour")
    check(ignored.id in unacked, "an unanswered broadcast is open for every colour")
    check(claim.id not in unacked, "a note addressed elsewhere stays out of this inbox")
    check(any(n.id == ignored.id for n in bus.inbox("black")),
          "broadcast reaches every colour's inbox")

    stale = bus.stale(current_round=3)
    check([n.id for n in stale] == [ignored.id],
          "stale finds exactly the ignored broadcast, not the answered notes")
    check(brief.id not in [n.id for n in stale], "recent unanswered note is not yet stale")

    correction = bus.write("purple", "all", "warning", "corrected: counts agree",
                           variant="0", round_n=1, evidence=ev, supersedes=ignored.id)
    check(all(n.id != ignored.id for n in bus.inbox("red")),
          "superseded note drops out of the inbox")
    check(correction.id not in [n.id for n in bus.stale(3)],
          "superseding a note clears its staleness")

    summary = bus.summary()
    check(summary["total"] >= 8, "summary counts every note")
    check(summary["matrix"]["red"]["blue"] >= 2, "correspondence matrix populated")
    check(summary["superseded"] == 1, "summary reports the supersession")

    anon = anonymize.Anonymizer("paths", root=cfg.root)
    leaky = bus.write("black", "all", "rebuttal", "see " + str(Path.home() / "x.json"),
                      variant="0", round_n=2,
                      evidence={"artifact_paths": [str(Path.home() / "x.json")]})
    exported = notes_mod.render_markdown(bus.all_notes(), anon, bus.summary())
    check(str(Path.home()) not in exported, "export redacts home directory")
    check("/Volumes/" not in exported, "export redacts absolute paths")
    check(str(Path.home()) in json.dumps(bus.read(leaky.id).to_dict()),
          "on-disk note keeps the raw path for machine use")

    check(bus.rebuild_index() == len(bus.all_notes()), "index rebuilds from note files")


def test_notes_concurrency(cfg, base: Path) -> None:
    """Independent processes appending at once must not lose or corrupt notes."""
    try:
        import notes  # noqa: F401
    except ImportError:
        return
    writers, per_writer = 4, 6
    script = (
        "import sys; sys.path.insert(0, {bench!r});\n"
        "from harness_config import load_config\n"
        "import notes\n"
        "cfg = load_config()\n"
        "bus = notes.NoteBus(cfg, {base!r})\n"
        "for i in range({n}):\n"
        "    bus.write('red', 'blue', 'handoff', 'from %s #%d' % (sys.argv[1], i),\n"
        "              variant='9', round_n=1)\n"
    ).format(bench=str(BENCH), base=str(base), n=per_writer)
    procs = [subprocess.Popen([sys.executable, "-c", script, "w{}".format(i)],
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
             for i in range(writers)]
    errors = []
    for proc in procs:
        _, err = proc.communicate(timeout=120)
        if proc.returncode != 0:
            errors.append(err.decode()[-300:])
    check(not errors, "all concurrent writers exited cleanly")
    if errors:
        print(errors[0])

    import notes as notes_mod
    bus = notes_mod.NoteBus(cfg, base)
    written = [n for n in bus.all_notes() if str(n.variant) == "9"]
    ids = [n.id for n in written]
    check(len(written) == writers * per_writer,
          "no note lost under concurrency ({} of {})".format(
              len(written), writers * per_writer))
    check(len(set(ids)) == len(ids), "no duplicate note ids under concurrency")


def test_verification(cfg, base: Path) -> None:
    """BLACK's split-half engine: partitioners, determinism, planted signals."""
    try:
        import verification as V
    except ImportError:
        return

    cases = V._demo_cases()
    # every declared strategy must produce non-empty, matching arms
    for strat in cfg.partition_strategies:
        split = V.partition(cases, strat, cfg)
        check(split.size_a > 0 and split.size_b > 0,
              "strategy {} yields both arms".format(strat))

    # determinism: same seed -> identical arm membership (no PYTHONHASHSEED leak)
    a1 = [c["id"] for c in V.partition(cases, "random_half", cfg).arm_a]
    a2 = [c["id"] for c in V.partition(cases, "random_half", cfg).arm_a]
    check(a1 == a2, "split is deterministic across calls")

    # planted signals
    r1 = V.evaluate([c for c in cases if c["remedy"] == "R1"],
                    lambda c: c["success"], cfg, strategy="stratified_half")
    check(r1.kind == "confirmed", "R1 (real fix) confirmed, got {}".format(r1.kind))

    r2 = V.evaluate([c for c in cases if c["remedy"] == "R2"],
                    lambda c: c["success"], cfg, strategy="technique_disjoint")
    check(r2.kind == "inflated", "R2 (overfit) inflated, got {}".format(r2.kind))

    rare = V.evaluate([c for c in cases if c["technique"] == "rare"],
                      lambda c: c["success"], cfg, strategy="stratified_half")
    check(rare.kind == "underpowered",
          "sparse cell underpowered, got {}".format(rare.kind))
    check(rare.effect.n_a < cfg.min_arm_size,
          "underpowered arm below the floor")

    # deflated: arm B genuinely stronger
    eff = V.Effect([0.4] * 20, [0.95] * 20, cfg)
    check(V.verdict(eff, cfg).kind == "deflated", "better-on-B reads deflated")

    # decision table is closed: every produced kind is a declared verdict kind
    seen = {r1.kind, r2.kind, rare.kind, V.verdict(eff, cfg).kind}
    check(seen <= set(cfg.verdict_kinds),
          "all verdicts are declared kinds")

    # the configuration knobs drive the table: a relaxed tolerance never hides
    # a real gap
    relaxed = V.verdict(V.Effect([0.4] * 20, [0.1] * 20, cfg), cfg)
    check(relaxed.kind == "inflated",
          "large gap inflates regardless of tolerance setting")


def test_scheduler(cfg, tmp: Path) -> None:
    """Scheduler: AIMD window, retry/breaker, checkpoint/resume (sim self-test)."""
    try:
        import scheduler as S
    except ImportError:
        check(False, "scheduler.py importable")
        return
    check(True, "scheduler.py importable")
    # AdaptiveWindow AIMD invariants
    w = S.AdaptiveWindow(floor=1, ceiling=8, backoff_factor=0.5, now=(lambda: 0.0))
    for _ in range(7):
        w.on_success()
    check(w.window == 8, "window reaches ceiling on success")
    for _ in range(3):
        w.on_rate_limited()
    check(w.window == 1, "window floors on rate-limit")
    # classify_failure table
    check(S.classify_failure("HTTP 429") == "retryable", "429 retryable")
    check(S.classify_failure("empty output") == "retryable", "empty output retryable")
    check(S.classify_failure("HTTP 400 bad request") == "terminal", "400 terminal")
    # CircuitBreaker opens under sustained failure
    cb = S.CircuitBreaker(failure_rate=0.5, min_sample=10, cooldown=0.0, now=(lambda: 0.0))
    for _ in range(12):
        cb.record(False)
    check(cb.state == S.CircuitBreaker.OPEN, "breaker opens under failure rate")
    # Checkpoint fsync durability + resume skip
    ck = S.Checkpoint(tmp / "ckpt.jsonl")
    ck.record_done("a", "ok", 1.0, 1)
    ck.record_done("b", "failed", 2.0, 2)
    check(ck.completed() == {"a"}, "checkpoint records only ok outcomes")
    check(ck.remaining(["a", "b", "c"]) == ["b", "c"], "remaining excludes completed")
    # Full simulation self-test must exit 0
    proc = subprocess.run([sys.executable, str(BENCH / "scheduler.py"), "--self-test"],
                          capture_output=True, text=True, timeout=120)
    check(proc.returncode == 0,
          "scheduler.py --self-test exits 0 ({} lines)".format(
              len(proc.stdout.splitlines())))


def test_white(cfg, tmp: Path) -> None:
    """WHITE: knowledge base + self-healing ingest/pattern (real execution)."""
    try:
        import knowledge as K
        import white as W
    except ImportError:
        check(False, "knowledge.py / white.py importable")
        return
    check(True, "knowledge.py / white.py importable")
    # knowledge self-test must pass
    proc = subprocess.run([sys.executable, str(BENCH / "knowledge.py"), "--self-test"],
                          capture_output=True, text=True, timeout=120)
    check(proc.returncode == 0, "knowledge.py --self-test exits 0")
    # ingest a few escapes and confirm a pattern rolls up
    kb = K.Knowledge(tmp / "white-knowledge.json")
    for place in ("head", "tail", "nested"):
        kb.record_failure("forbidden_bait", place, "immediate", "api_doc",
                          ["P1"], ["bunch"], "0", 1, 0.2, "x", 1)
    kb.flush()
    kb._regenerate_patterns()
    pats = kb.patterns(min_support=2)
    check(any(p["kind"] == "technique_across_placements" for p in pats),
          "knowledge rolls up technique_across_placements pattern")
    # confidence formula: failures raise confidence
    sig = list(kb.lessons.keys())[0]
    check(kb.confidence_of(sig, 1) > 0.0, "lesson confidence > 0 after failures")
    # white.py --help exercises the shared-arg CLI wiring without a live run
    h = subprocess.run([sys.executable, str(BENCH / "white.py"), "--help"],
                       capture_output=True, text=True, timeout=60)
    check(h.returncode == 0 and "await-timeout" in h.stdout,
          "white.py CLI wires shared args (--await-timeout present)")


def test_pipeline(cfg, tmp: Path) -> None:
    """End-to-end driver: RED->BLUE->WHITE->BLACK across cycles (offline).

    Verifies the five colours converge through the filesystem handshake and the
    4-turn reverse-deduction loop fires (notes written, knowledge pruned).
    """
    import run_pipeline as RP  # noqa: F401  (ensures module importable)
    base = tmp / "pipe"
    base.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(
        [sys.executable, str(BENCH / "run_pipeline.py"),
         "--base", str(base), "--skip-live", "--rounds", "1", "--cycles", "2",
         "--workers", "8", "--await-timeout", "120"],
        capture_output=True, text=True, timeout=300)
    check(proc.returncode == 0, "run_pipeline.py exits 0 (rc={})".format(proc.returncode))
    # sentinels from every colour must exist
    for sent in ("purple.json", "blue-done.json", "white-done.json", "black-done.json"):
        found = len(list(base.glob("**/" + sent)))
        check(found >= 1, "pipeline produced {} (found {})".format(sent, found))
    report = json.loads((base / "pipeline-report.json").read_text())
    check(len(report["cycles_report"]) == 2, "two cycles recorded")
    check(all(c["phases"].get("black") for c in report["cycles_report"]),
          "BLACK completed every cycle")
    # reverse-deduction: notes + pruning must have fired by cycle 2
    c2 = report["cycles_report"][1]
    check(c2["reverse_notes_written"] >= 1, "reverse-deduction notes written")
    check(c2["pruned_lessons"] >= 1, "WHITE knowledge pruned across cycles")
    # knowledge must converge downward (not grow unboundedly)
    check(report["cycles_report"][1]["knowledge"]["lessons"] <=
          report["cycles_report"][0]["knowledge"]["lessons"],
          "lessons do not grow across cycles (convergence)")


def test_red_blue(cfg, tmp: Path) -> None:
    """RED generator + BLUE defender: placement/timing, handshake, offline run."""
    try:
        import red as R
        import blue as B
    except ImportError:
        check(False, "red.py / blue.py importable")
        return
    check(True, "red.py / blue.py importable")

    # RED: full placement x timing spread, schema-conformant.
    cases = R.build_red_cases(0, 1, per_combo=1, seed=7)
    check(len(cases) == 10 * 8 * 6,  # 10 techniques x 8 placements x 6 timings
          "red case count = 480 (got {})".format(len(cases)))
    placements = {c["placement"] for c in cases}
    timings = {c["timing"] for c in cases}
    check(placements == set(R.PLACE_OPTIONS),
          "red all 8 placements present")
    check(timings == set(R.TIMING_OPTIONS),
          "red all 6 timings present")
    bad, _ = R._schema_check(cases)
    check(bad == 0, "red cases schema-valid ({} invalid)".format(bad))
    # new techniques present
    techs = {c["adversarial_technique"] for c in cases}
    check({"instruction_override", "unit_smuggle", "spelling_drift"} <= techs,
          "red new techniques present")

    # RED emit: write handshakes to a temp base.
    out = tmp / "redblue"
    rc = subprocess.run(
        [sys.executable, str(BENCH / "red.py"), "--emit-only",
         "--tiers", "0", "--rounds", "1", "--out-dir", str(out),
         "--per-combo", "1"], capture_output=True, text=True)
    check(rc.returncode == 0, "red.py --emit-only runs")
    check((out / "tier0" / "round1" / "purple.json").exists(),
          "red writes purple.json handshake")
    check((out / "tier0" / "round1" / "escapes.json").exists(),
          "red writes escapes.json ledger")

    # BLUE: build probes from a synthetic escape set.
    esc = [{"tier": 0, "round": 1, "test_id": "red-x-000",
            "technique": "forbidden_bait", "category": "api_doc",
            "placement": "head", "timing": "immediate",
            "missed_principles": ["P1"], "forbidden_found": ["bunch"],
            "correctness_score": 0.2, "input": "Please bunch it.",
            "violating_output": "Please bunch it."}]
    probes = B.build_blue_probes(esc, probe_placements=B.PROBE_PLACEMENTS,
                                 defense_timing="reactive", round_n=1)
    check(len(probes) == len(B.PROBE_PLACEMENTS),
          "blue builds one probe per placement")
    check(all(p["probe_placement"] in B.PROBE_PLACEMENTS for p in probes),
          "blue probes carry probe_placement")
    table = B._offline_resistance(probes)
    # verbatim should fail (residual), others pass
    verbatim = [t for t in table if t["placement"] == "verbatim"][0]
    check(verbatim["resistance_pct"] == 0.0, "blue verbatim residual = 0%")
    nonverb = [t for t in table if t["placement"] != "verbatim"]
    check(all(t["resistance_pct"] == 100.0 for t in nonverb),
          "blue non-verbatim placements = 100% (offline)")

    # BLUE await-timeout must be prompt, not hang.
    empty = tmp / "blue-empty"
    (empty / "tier0" / "round1").mkdir(parents=True)
    t0 = __import__("time").time()
    rc = subprocess.run(
        [sys.executable, str(BENCH / "blue.py"), "--skip-live",
         "--tiers", "0", "--rounds", "1", "--base", str(empty),
         "--await-timeout", "2", "--poll-interval", "1"],
        capture_output=True, text=True)
    dt = __import__("time").time() - t0
    check(rc.returncode == 0 and dt < 6.0,
          "blue await-timeout prompt ({}s)".format(round(dt, 1)))


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
        test_notes(cfg, tmp)
        test_notes_concurrency(cfg, tmp)
        test_verification(cfg, tmp)
        test_red_blue(cfg, tmp)
        test_scheduler(cfg, tmp)
        test_white(cfg, tmp)
        test_pipeline(cfg, tmp)
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
