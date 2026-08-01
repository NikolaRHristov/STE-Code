#!/usr/bin/env python3
"""Collect every artifact the adversarial benchmark leaves on disk into one
machine-readable dossier, then render it as a human-readable report.

The harness (RED / BLUE / PURPLE / WHITE / BLACK) converges through the
filesystem. Every run writes under one root, .agents/benchmark/tests/:

    .agents/benchmark/tests/<tier>-<suite>/run-*/   scored tier runs
    .agents/benchmark/tests/control/run-*/          control (no-prompt) runs
    <pipe base>/variant<V>/round<N>/                the five-colour handshake
    <pipe base>/{knowledge,notes,remedies}/         WHITE's durable memory

Nothing in the harness reads all of it at once. This module does, and it marks
every number with its provenance: MEASURED (a model produced it) or SIMULATED
(a generator produced it offline). That distinction is the whole point --
CONTRACT.md section 6 requires that simulated numbers are never presented as
measured, and the offline pipeline produces almost nothing but simulated ones.

Usage:
    python3 summarize_run.py                       # newest run, markdown
    python3 summarize_run.py --json dossier.json   # also dump the raw dossier
    python3 summarize_run.py --base .agents/tmp/pipe
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

BENCH = Path(__file__).resolve().parent
PROJECT = BENCH.parent.parent

# Provenance labels. Every reported figure carries one.
MEASURED = "MEASURED"
SIMULATED = "SIMULATED"
UNKNOWN = "UNKNOWN"


def _read_json(path: Path, default=None):
    """Read JSON, returning ``default`` on any failure.

    A missing or half-written artifact is data (the phase did not run), never
    an error -- the same tolerance PURPLE applies in purple_stitch.py.
    """
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        pass
    return default


def _pct(num, den):
    if not den:
        return None
    return round(num / den * 100.0, 1)


def _mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def _iso(ts: float) -> str:
    if not ts:
        return "unknown"
    return datetime.fromtimestamp(ts, timezone.utc).isoformat(timespec="seconds")


def _latest_run(results_dir: Path) -> "Path | None":
    """Newest ``run-*`` directory under a results directory."""
    runs = sorted((p for p in results_dir.glob("run-*") if p.is_dir()),
                  key=lambda p: p.name)
    return runs[-1] if runs else None


# --------------------------------------------------------------- tier scoring

def collect_tier_runs(bench: Path) -> list:
    """Every scored suite under ``tests/``: the only MEASURED evidence there is.

    Directory names encode (tier, suite) as ``tier<T>-<suite>``. A suite that
    started but never produced an aggregate is reported as incomplete rather
    than dropped -- a timed-out tier is a finding about the harness, and the
    log tail says why.
    """
    out = []
    tests = bench / "tests"
    if not tests.exists():
        return out
    for d in sorted(p for p in tests.iterdir() if p.is_dir()):
        match = re.match(r"^tier(-?\d+)-(\w+)$", d.name)
        tier = match.group(1) if match else None
        suite = match.group(2) if match else "unknown"
        run = _latest_run(d)
        rec = {"name": d.name, "tier": tier, "suite": suite,
               "run_dir": str(run) if run else None,
               "started_utc": _iso(_mtime(d)), "status": "no-run",
               "provenance": MEASURED}
        log = tests / (d.name + ".log")
        if log.exists():
            rec["log"] = str(log)
            rec["log_bytes"] = log.stat().st_size
        if run is None:
            out.append(rec)
            continue
        agg = _read_json(run / "aggregate-results.json")
        per = _read_json(run / "per-test-results.json", []) or []
        prog = _read_json(run / "progress.json", {}) or {}
        rec["cases_attempted"] = len(prog)
        if not agg:
            # Started, never aggregated: reconstruct what we can from progress.
            outcomes = Counter(v.get("outcome") for v in prog.values()
                               if isinstance(v, dict))
            rec.update({"status": "incomplete",
                        "worker_outcomes": dict(outcomes),
                        "completed": outcomes.get("SUCCESS", 0)})
            out.append(rec)
            continue
        aggregates = agg.get("aggregates", {}) or {}
        rec.update({
            "status": "complete",
            "timestamp": agg.get("timestamp"),
            "model": agg.get("model"),
            "benchmark_id": agg.get("benchmark_id"),
            "total_tests": agg.get("total_tests"),
            "passed": agg.get("passed"),
            "failed": agg.get("failed"),
            "pass_rate_pct": agg.get("pass_rate_pct"),
            "avg_correctness": aggregates.get("avg_correctness"),
            "min_correctness": aggregates.get("min_correctness"),
            "avg_latency_ms": aggregates.get("avg_latency_ms"),
            "total_tokens_output": aggregates.get("total_tokens_output"),
            "worker_outcomes": agg.get("worker_outcomes"),
            "retries_total": agg.get("retries_total"),
            "by_category": agg.get("by_category", {}),
            "failures": [
                {"test_id": t.get("test_id"), "category": t.get("category"),
                 "score": t.get("correctness_score"),
                 "missed": t.get("expected_principles_missed", []),
                 "forbidden": t.get("forbidden_keywords_found", []),
                 "notes": (t.get("notes") or "")[:300]}
                for t in per if not t.get("passed")],
        })
        out.append(rec)
    return out


def collect_control(bench: Path) -> list:
    """Control runs: the plain-assistant baseline the tier numbers are read against."""
    out = []
    root = bench / "tests" / "control"
    if not root.exists():
        return out
    for run in sorted((p for p in root.glob("run-*") if p.is_dir()),
                      key=lambda p: p.name):
        agg = _read_json(run / "aggregate-results.json")
        if not agg:
            continue
        out.append({"run": run.name, "provenance": MEASURED,
                    "total_tests": agg.get("total_tests"),
                    "passed": agg.get("passed"),
                    "pass_rate_pct": agg.get("pass_rate_pct"),
                    "avg_correctness": (agg.get("aggregates", {}) or {})
                    .get("avg_correctness")})
    return out


# ------------------------------------------------------- five-colour handshake

def collect_pipeline(base: Path) -> dict:
    """Walk the variant/round handshake tree and the base-level artifacts.

    Everything here is produced by the offline driver unless a live model ran,
    so each block records whether the artifacts it read were flagged
    ``simulated``. A round is described by which sentinels landed, exactly as
    PURPLE's RoundView does, so "defended successfully" is never confused with
    "never ran".
    """
    doc = {"base": str(base), "exists": base.exists()}
    if not base.exists():
        return doc

    pipeline = _read_json(base / "pipeline-report.json", {}) or {}
    doc["pipeline_report"] = pipeline
    doc["skip_live"] = pipeline.get("skip_live")
    doc["provenance"] = SIMULATED if pipeline.get("skip_live") else MEASURED
    doc["cycles"] = pipeline.get("cycles")
    doc["rounds"] = pipeline.get("rounds")
    doc["tiers"] = pipeline.get("tiers", [])
    doc["confidence_trend"] = pipeline.get("confidence_trend", [])
    doc["cycles_report"] = pipeline.get("cycles_report", [])
    doc["generated_utc"] = _iso(_mtime(base / "pipeline-report.json"))

    doc["red_report"] = _read_json(base / "red-report.json", {}) or {}
    doc["blue_report"] = _read_json(base / "blue-report.json", {}) or {}
    doc["white_report"] = _read_json(base / "white-report.json", {}) or {}
    doc["attack_brief"] = _read_json(base / "attack-brief.json", []) or []
    doc["defended"] = _read_json(base / "defended.json", {}) or {}

    doc["knowledge"] = _summarize_knowledge(
        _read_json(base / "knowledge.json", {}) or {})
    doc["remedies"] = _summarize_remedies(base / "remedies")
    doc["notes"] = _summarize_notes(base / "notes")
    doc["rounds_detail"] = _walk_rounds(base)
    doc["verdicts"] = _summarize_verdicts(doc["rounds_detail"])
    return doc


def _walk_rounds(base: Path) -> list:
    """One record per variant/round: which sentinels landed and what they said."""
    out = []
    for vdir in sorted(base.glob("variant*")):
        if not vdir.is_dir():
            continue
        variant = vdir.name.replace("variant", "")
        for rdir in sorted(vdir.glob("round*")):
            red = _read_json(rdir / "purple.json")
            blue = _read_json(rdir / "blue-done.json")
            white = _read_json(rdir / "white-done.json")
            black = _read_json(rdir / "black-done.json")
            stitch = _read_json(rdir / "report.json", {}) or {}
            escapes = _read_json(rdir / "escapes.json", []) or []
            sides = [name for name, val in (("red", red), ("blue", blue),
                                            ("white", white), ("black", black))
                     if val is not None]
            simulated = any(e.get("simulated") for e in escapes
                            if isinstance(e, dict)) or stitch.get("simulated")
            rec = {
                "variant": variant, "round": rdir.name.replace("round", ""),
                "sides": sides,
                "status": "complete" if len(sides) == 4 else (
                    "absent" if not sides else "partial:" + "+".join(sides)),
                "escapes": len(escapes),
                "escapes_simulated": bool(simulated),
                "provenance": SIMULATED if simulated else MEASURED,
                "red_total": (red or {}).get("red_total"),
                "red_pass_rate_pct": (red or {}).get("red_pass_rate_pct"),
                "blue_probes": (blue or {}).get("blue_probes"),
                "blue_pass_rate_pct": (blue or {}).get("blue_pass_rate_pct"),
                "residual_escapes": len((blue or {}).get("residual_escape_ids", [])),
                "defense_timing": (blue or {}).get("defense_timing"),
                "white_status": (white or {}).get("status"),
                "white_ingested": (white or {}).get("escapes_ingested"),
                "white_proposed": (white or {}).get("remedies_proposed"),
                "white_adopted": (white or {}).get("adopted"),
                "white_rejected": (white or {}).get("rejected"),
                "stitch_resistance_pct": stitch.get("overall_resistance_pct"),
                "stitch_cycle": stitch.get("cycle"),
                "black_verdicts": (black or {}).get("n_verdicts", 0),
            }
            rec["escape_cells"] = sorted({
                (e.get("technique"), e.get("placement")) for e in escapes
                if isinstance(e, dict)})
            rec["resistance_table"] = (blue or {}).get("resistance_table", [])
            rec["verdict_records"] = (black or {}).get("verdicts", [])
            out.append(rec)
    return out


# ----------------------------------------------------- WHITE's durable memory

def _summarize_knowledge(kb: dict) -> dict:
    """Roll up knowledge.json: lessons, their confidence, and the patterns.

    Confidence is recomputed here with knowledge.py's documented rule
    (b / (a + b), b = corroborating failures) rather than trusted from disk,
    because the stored record holds the raw counts, not the derived value.
    """
    lessons = kb.get("lessons", {}) or {}
    rows = []
    for sig, L in lessons.items():
        if not isinstance(L, dict):
            continue
        a, b = L.get("a", 0), L.get("b", 0)
        conf = round(b / (a + b), 4) if (a + b) else 0.0
        scores = L.get("scores") or []
        mean_score = round(sum(scores) / len(scores), 3) if scores else None
        rows.append({
            "signature": sig[:8], "technique": L.get("technique"),
            "placement": L.get("placement"), "timing": L.get("timing"),
            "category": L.get("category"),
            "missed_principles": L.get("missed_principles", []),
            "forbidden_found": L.get("forbidden_found", []),
            "occurrences": L.get("occurrences", 0),
            "rounds_seen": L.get("rounds_seen", []),
            "variants_affected": L.get("variants_affected", []),
            "a": a, "b": b, "confidence": conf,
            "mean_correctness": mean_score,
            "severity": round((1.0 - (mean_score or 0.0)) *
                              (1.0 + 0.1 * L.get("occurrences", 0)), 3),
        })
    rows.sort(key=lambda r: (-r["confidence"], -r["occurrences"]))
    patterns = [p for p in (kb.get("patterns", {}) or {}).values()
                if isinstance(p, dict)]
    patterns.sort(key=lambda p: -p.get("support", 0))
    return {"schema_version": kb.get("schema_version"),
            "version": kb.get("version"), "updated_at": kb.get("updated_at"),
            "lesson_count": len(rows), "pattern_count": len(patterns),
            "lessons": rows, "patterns": patterns,
            "techniques": dict(Counter(r["technique"] for r in rows)),
            "placements": dict(Counter(r["placement"] for r in rows))}


def _summarize_remedies(root: Path) -> dict:
    """WHITE's proposals, split by whether the validation gate accepted them."""
    doc = {"adopted": [], "rejected": [], "adopted_count": 0,
           "rejected_count": 0}
    if not root.exists():
        return doc
    for dest in ("adopted", "rejected"):
        for path in sorted((root / dest).glob("*.json")) if (root / dest).exists() else []:
            rem = _read_json(path, {}) or {}
            doc[dest].append({
                "id": rem.get("id"), "kind": rem.get("remedy_kind"),
                "target": rem.get("target"),
                "diagnosis": rem.get("diagnosis"),
                "patch_text": (rem.get("patch_text") or "")[:240],
                "confidence": rem.get("confidence"),
                "delta_resistance_pct": rem.get("delta_resistance_pct"),
                "validated_by": rem.get("validated_by"),
                "provenance": (SIMULATED if rem.get("validated_by") == "simulated"
                               else MEASURED if rem.get("validated_by") else UNKNOWN),
            })
        doc[dest + "_count"] = len(doc[dest])
    doc["by_kind"] = dict(Counter(
        r["kind"] for r in doc["adopted"] + doc["rejected"]))
    doc["by_target"] = dict(Counter(r["target"] for r in doc["adopted"]))
    return doc


def _summarize_notes(root: Path) -> dict:
    """The correspondence bus, plus the driver's reverse-deduction notes.

    Two shapes coexist here. notes.py writes the full NOTES_PROTOCOL record
    (from_colour/to_colour/kind); run_pipeline.py writes a lighter
    reverse-deduction note (from/to/kind). Both are counted, and the split is
    reported, because a tree holding only the light shape means the protocol
    bus never actually ran.
    """
    doc = {"total": 0, "by_kind": {}, "matrix": {}, "protocol_notes": 0,
           "driver_notes": 0, "samples": []}
    if not root.exists():
        return doc
    for path in sorted(root.glob("*.json")):
        if path.name == "index.json":
            continue
        note = _read_json(path, {}) or {}
        frm = note.get("from_colour") or note.get("from") or "?"
        to = note.get("to_colour") or note.get("to") or "?"
        kind = note.get("kind", "?")
        doc["total"] += 1
        if note.get("from_colour"):
            doc["protocol_notes"] += 1
        else:
            doc["driver_notes"] += 1
        doc["by_kind"][kind] = doc["by_kind"].get(kind, 0) + 1
        doc["matrix"].setdefault(frm, {})
        doc["matrix"][frm][to] = doc["matrix"][frm].get(to, 0) + 1
        if len(doc["samples"]) < 6:
            doc["samples"].append({
                "id": note.get("id"), "from": frm, "to": to, "kind": kind,
                "subject": note.get("subject") or note.get("claim_id"),
                "message": (note.get("message") or note.get("body") or "")[:300]})
    return doc


def _summarize_verdicts(rounds: list) -> dict:
    """BLACK's rulings, grouped by verdict, by challenged colour, and by claim."""
    by_verdict = Counter()
    by_colour = Counter()
    by_claim = defaultdict(Counter)
    non_confirmed = []
    for rec in rounds:
        for v in rec.get("verdict_records", []):
            if not isinstance(v, dict):
                continue
            verdict = v.get("verdict", "?")
            colour = v.get("source_colour", "?")
            by_verdict[verdict] += 1
            by_colour[colour] += 1
            by_claim[str(v.get("claim_id"))][verdict] += 1
            if verdict != "confirmed" and len(non_confirmed) < 25:
                non_confirmed.append({
                    "claim_id": v.get("claim_id"), "variant": v.get("variant"),
                    "round": v.get("round"), "source": colour,
                    "verdict": verdict, "reason": (v.get("reason") or "")[:240]})
    return {"total": sum(by_verdict.values()),
            "by_verdict": dict(by_verdict), "by_challenged_colour": dict(by_colour),
            "by_claim": {k: dict(v) for k, v in by_claim.items()},
            "non_confirmed": non_confirmed}


# ------------------------------------------------------------ integrity checks

def integrity_checks(dossier: dict) -> list:
    """Findings about the HARNESS, not the subject under test.

    A benchmark that reports only its subject's score hides its own defects.
    Each check states what it observed, why that matters, and what it implies
    about how far the headline number can be trusted.
    """
    out = []
    pipe = dossier.get("pipeline", {}) or {}
    rounds = pipe.get("rounds_detail", []) or []
    verdicts = pipe.get("verdicts", {}) or {}
    kb = pipe.get("knowledge", {}) or {}
    trend = pipe.get("confidence_trend", []) or []
    cycles = pipe.get("cycles_report", []) or []

    def add(severity, title, detail, implication):
        out.append({"severity": severity, "title": title,
                    "detail": detail, "implication": implication})

    # 1. Offline mode: nothing here was produced by a model.
    if pipe.get("skip_live"):
        add("critical", "Pipeline ran offline (--skip-live)",
            "pipeline-report.json records skip_live=true, so RED emitted cases "
            "without scoring them, BLUE derived resistance from its offline "
            "estimator, WHITE validated remedies by simulation, and the "
            "resistance figures BLACK confirmed came from _write_stitch_reports.",
            "Every adversarial number in this run is SIMULATED. It demonstrates "
            "that the wiring converges; it measures nothing about the subject.")

    # 2. Seeded escapes: the escape corpus is synthetic by construction.
    seeded = [r for r in rounds if r.get("escapes_simulated")]
    if seeded:
        add("critical", "Escape ledger is seeded, not observed",
            "{} of {} rounds carry escapes flagged simulated:true, written by "
            "run_pipeline._seed_escapes rather than produced by a scored run."
            .format(len(seeded), len(rounds)),
            "The technique/placement pattern (forbidden_bait everywhere, nested "
            "defeating everything) is the pattern the seeder was told to draw. "
            "WHITE's lessons rediscover that assumption, not a property of the "
            "configuration under test.")

    # 3. BLACK confirmed everything: a verifier that never dissents.
    bv = verdicts.get("by_verdict", {}) or {}
    total_v = verdicts.get("total", 0)
    if total_v and bv.get("confirmed", 0) == total_v:
        add("high", "BLACK returned no dissenting verdict",
            "All {} verdicts are 'confirmed'; none are inflated, deflated, "
            "unsound or underpowered.".format(total_v),
            "BLACK's hypothesis test compares the brief's predicted lift "
            "(10%) against the stitch report's overall_resistance_pct, which "
            "the driver writes as a rising constant. The comparison is "
            "satisfied by construction, so confirmation carries no evidence.")

    # 4. The remedy challenge never fired.
    remedy_claims = [k for k in (verdicts.get("by_claim", {}) or {})
                     if k.startswith("remedy-")]
    if total_v and not remedy_claims:
        add("high", "Split-half remedy verification never ran",
            "No verdict carries a 'remedy-*' claim id, so BLACK's "
            "_challenge_remedies produced nothing. It reads "
            "white['remedies_adopted'], but white-done.json stores the count "
            "under 'adopted' and keeps no per-case outcomes.",
            "verification.py -- the split-half instrument that detects "
            "overfitting -- is present, self-tested, and never applied to a "
            "real remedy. Adopted remedies are unverified.")

    # 5. Reverse deduction: notes written, knowledge never pruned.
    pruned = max((c.get("pruned_lessons", 0) for c in cycles), default=0)
    notes_written = sum(c.get("reverse_notes_written", 0) for c in cycles)
    if notes_written and not pruned:
        add("high", "Reverse deduction wrote notes but pruned nothing",
            "{} reverse-deduction notes were written across cycles, yet "
            "pruned_lessons stayed 0. _collect_defended emits records keyed "
            "'brief_id'; _prune_knowledge reads d['claim_id'], which is never "
            "present, so the prefix match never runs.".format(notes_written),
            "The learning loop cannot converge: WHITE re-ingests the same "
            "lessons every cycle and the confidence curve stays flat.")

    # 6. Learning curve: flat (no convergence) or descending (converged).
    if len(trend) >= 2:
        counts = [t.get("lessons") for t in trend]
        if len(set(counts)) == 1:
            add("high", "Learning curve is flat across all cycles",
                "Lesson count stayed at {} for all {} cycles."
                .format(counts[0], len(counts)),
                "The design intent (each cycle hardens the base, shrinking the "
                "attack surface) is not observable. Either the exclusion set "
                "never reaches the seeder or the prune never fires.")
        elif counts[-1] == 0 and counts[0] > 0:
            add("info", "Learning loop converged to zero open lessons",
                "Lessons fell {} -> 0 across {} cycles; {} were pruned after "
                "BLACK confirmed the base already resisted them, and {} "
                "(technique, placement) pairs were excluded from the attack "
                "surface.".format(
                    counts[0], len(counts),
                    max((c.get("pruned_lessons", 0) for c in cycles), default=0),
                    max((c.get("excluded_pairs", 0) for c in cycles), default=0)),
                "The self-refutation mechanism works end to end: a claim that "
                "survives BLACK's challenge is retired rather than re-probed, "
                "so the loop reaches a fixed point instead of cycling. What it "
                "converged on is still the seeded corpus, so this validates "
                "the machinery, not the subject.")

    # 7. Defended count saturates without shrinking the surface.
    defended = [c.get("defended_confirmed", 0) for c in cycles]
    if len(defended) >= 2 and defended[-1] == defended[1] and defended[-1] > 0:
        add("medium", "Defended-claim count saturates immediately",
            "defended_confirmed jumps 0 -> {} at cycle 2 and never changes."
            .format(defended[1]),
            "Cycles 3 and 4 re-derive the identical conclusion. The extra "
            "cycles cost time and add no information.")

    # 8. The signature-set that gates WHITE is empty.
    sigs = (pipe.get("defended", {}) or {}).get("signatures", [])
    if notes_written and not sigs:
        add("medium", "defended.json carries no signatures",
            "WHITE is invoked with --defended pointing at a file whose "
            "'signatures' list is empty, so _defended_pairs_match resolves to "
            "an empty skip set.",
            "WHITE's reverse-deduction guard is wired but inert; it never "
            "skips a pair BLACK already cleared.")

    # 9. BLUE saw no escapes in its own report despite a full ledger.
    blue_rep = pipe.get("blue_report", {}) or {}
    per_tier = blue_rep.get("per_tier", {}) or {}
    no_escape_tiers = [t for t, v in per_tier.items()
                       if any(r.get("status") == "no-escapes"
                              for r in (v.get("rounds") or []))]
    if no_escape_tiers and any(r.get("escapes") for r in rounds):
        add("medium", "BLUE's own report disagrees with the round tree",
            "blue-report.json records status 'no-escapes' for tier(s) {} while "
            "the round directories hold seeded escapes and populated "
            "resistance tables.".format(", ".join(map(str, no_escape_tiers))),
            "BLUE ran before the seeder wrote the ledger for those tiers. The "
            "base-level BLUE report is a stale view; per-round blue-done.json "
            "is the reliable one.")

    # 10. Every lesson is P1: the principle axis is degenerate.
    princ = Counter(p for L in (kb.get("lessons") or [])
                    for p in (L.get("missed_principles") or []))
    if len(princ) == 1 and kb.get("lesson_count", 0) > 2:
        add("low", "All lessons cite a single principle",
            "Every one of the {} lessons names {} as the missed principle."
            .format(kb.get("lesson_count"), next(iter(princ))),
            "The seeder hardcodes that principle. Any rule-level conclusion is "
            "an artifact of the fixture.")

    # 11. Incomplete tier suites.
    tiers = dossier.get("tier_runs", []) or []
    stalled = [t for t in tiers if t.get("status") == "incomplete"]
    if stalled:
        add("high", "Scored tier suites did not finish",
            "{} of {} suites produced no aggregate: {}".format(
                len(stalled), len(tiers),
                ", ".join(t["name"] for t in stalled[:8])),
            "Tier comparison is only possible across the {} suite(s) that did "
            "complete; the rest hit the 3600s orchestrator cap."
            .format(len(tiers) - len(stalled)))

    order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
    out.sort(key=lambda f: order.get(f["severity"], 9))
    return out


# ------------------------------------------------------------------- assembly

def build_dossier(bench: Path, base: Path) -> dict:
    doc = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "project_root": str(PROJECT),
        "bench_dir": str(bench),
        "profile": _read_json(bench / "config" / "harness.json", {}) or {},
        "tier_runs": collect_tier_runs(bench),
        "control_runs": collect_control(bench),
        "pipeline": collect_pipeline(base),
    }
    doc["findings"] = integrity_checks(doc)
    return doc


# ------------------------------------------------------------------ rendering

def _row(cells) -> str:
    return "| " + " | ".join("" if c is None else str(c) for c in cells) + " |"


def _table(headers, rows) -> list:
    out = [_row(headers), "|" + "|".join("---" for _ in headers) + "|"]
    out.extend(_row(r) for r in rows)
    return out


def render_markdown(doc: dict) -> str:
    out = []
    add = out.append
    pipe = doc.get("pipeline", {}) or {}
    prof = (doc.get("profile", {}) or {}).get("profile", {}) or {}

    add("# Adversarial benchmark run report")
    add("")
    add("Generated {} · profile **{}** ({})".format(
        doc["generated_utc"], prof.get("display_name", "?"),
        prof.get("description", "")))
    add("")

    # ---- provenance banner: the single most important fact ----
    if pipe.get("skip_live"):
        add("> ## ⚠ Provenance: SIMULATED")
        add(">")
        add("> This pipeline ran with `--skip-live`. No model was called by "
            "RED, BLUE, WHITE or BLACK. The escape ledger was written by "
            "`_seed_escapes`, BLUE's resistance came from its offline "
            "estimator, WHITE's remedy deltas were simulated from lesson "
            "confidence, and the resistance figures BLACK checked were written "
            "by `_write_stitch_reports` as a rising constant.")
        add(">")
        add("> **Read every adversarial number below as a wiring check, not a "
            "measurement.** The only measured results in this report are the "
            "scored tier suites in the next section.")
        add("")

    add(_section_scope(doc))
    add("")
    out.extend(_render_measured(doc))
    out.extend(_render_pipeline(doc))
    out.extend(_render_knowledge(doc))
    out.extend(_render_verdicts(doc))
    out.extend(_render_findings(doc))
    return "\n".join(out)


def _section_scope(doc: dict) -> str:
    pipe = doc.get("pipeline", {}) or {}
    tiers = doc.get("tier_runs", []) or []
    done = [t for t in tiers if t.get("status") == "complete"]
    lines = ["## What this run tested", "",
             "| dimension | value |", "|---|---|"]
    lines.append(_row(["scored suites attempted", len(tiers)]))
    lines.append(_row(["scored suites completed", len(done)]))
    lines.append(_row(["adversarial variants", len(pipe.get("tiers", []) or [])]))
    lines.append(_row(["rounds per variant", pipe.get("rounds")]))
    lines.append(_row(["adversarial cycles", pipe.get("cycles")]))
    lines.append(_row(["handshake cells", len(pipe.get("rounds_detail", []) or [])]))
    lines.append(_row(["knowledge lessons",
                       (pipe.get("knowledge", {}) or {}).get("lesson_count")]))
    lines.append(_row(["remedies adopted",
                       (pipe.get("remedies", {}) or {}).get("adopted_count")]))
    lines.append(_row(["BLACK verdicts",
                       (pipe.get("verdicts", {}) or {}).get("total")]))
    lines.append(_row(["notes exchanged", (pipe.get("notes", {}) or {}).get("total")]))
    return "\n".join(lines)


def _render_measured(doc: dict) -> list:
    out = ["", "## Measured results (scored suites)", ""]
    tiers = doc.get("tier_runs", []) or []
    done = [t for t in tiers if t.get("status") == "complete"]
    if not done:
        out.append("_No suite produced an aggregate. Nothing here is measured._")
        out.append("")
    else:
        out.append("These ran a real model against the tier prompts. This is "
                   "the only MEASURED evidence in the report.")
        out.append("")
        rows = []
        for t in sorted(done, key=lambda x: -(x.get("pass_rate_pct") or 0)):
            rows.append([
                "`{}`".format(t["name"]), t.get("tier"), t.get("suite"),
                "{}/{}".format(t.get("passed"), t.get("total_tests")),
                "**{}%**".format(t.get("pass_rate_pct")),
                t.get("avg_correctness"),
                "{:,}".format(int(t["avg_latency_ms"] / 1000))
                if t.get("avg_latency_ms") else None,
                t.get("model")])
            
        out.extend(_table(["suite", "tier", "kind", "passed", "pass rate",
                           "avg correctness", "avg latency (s)", "model"], rows))
        out.append("")

        # per-category, from the best suite
        best = max(done, key=lambda x: x.get("pass_rate_pct") or 0)
        cats = best.get("by_category", {}) or {}
        if cats:
            out.append("### Category breakdown — `{}`".format(best["name"]))
            out.append("")
            rows = [[c, "{}/{}".format(v.get("passed"), v.get("total")),
                     v.get("avg_correctness"),
                     "✅" if not v.get("failed") else "❌ {}".format(v.get("failed"))]
                    for c, v in sorted(cats.items(),
                                       key=lambda kv: kv[1].get("avg_correctness") or 0)]
            out.extend(_table(["category", "passed", "avg correctness", ""], rows))
            out.append("")

        # what actually failed
        fails = [(t["name"], f) for t in done for f in t.get("failures", [])]
        if fails:
            out.append("### What failed")
            out.append("")
            rows = [[s, f.get("test_id"), f.get("category"), f.get("score"),
                     ", ".join(f.get("missed") or []) or "—",
                     ", ".join(f.get("forbidden") or []) or "—"]
                    for s, f in fails[:20]]
            out.extend(_table(["suite", "test", "category", "score",
                               "principles missed", "forbidden found"], rows))
            out.append("")

    stalled = [t for t in tiers if t.get("status") != "complete"]
    if stalled:
        out.append("### Suites that produced no result")
        out.append("")
        rows = [[ "`{}`".format(t["name"]), t.get("status"),
                  t.get("cases_attempted"), t.get("completed"),
                  (t.get("worker_outcomes") or {}) or "—"] for t in stalled]
        out.extend(_table(["suite", "status", "cases attempted",
                           "completed", "worker outcomes"], rows))
        out.append("")

    ctrl = doc.get("control_runs", []) or []
    if ctrl:
        out.append("### Control baseline (no tier prompt)")
        out.append("")
        rows = [[c["run"], "{}/{}".format(c.get("passed"), c.get("total_tests")),
                 "{}%".format(c.get("pass_rate_pct")), c.get("avg_correctness")]
                for c in ctrl]
        out.extend(_table(["run", "passed", "pass rate", "avg correctness"], rows))
        out.append("")
        sizes = {c.get("total_tests") for c in ctrl}
        tot = {t.get("total_tests") for t in done} or {None}
        if sizes and tot and max(sizes or [0]) < (max(x for x in tot if x) or 0):
            out.append("> The control ran {} case(s) against the tiers' {}. "
                       "It is a smoke test, not a comparable baseline — no "
                       "STE-Code-vs-plain claim can rest on it."
                       .format(max(sizes), max(x for x in tot if x)))
            out.append("")
    return out


def _render_pipeline(doc: dict) -> list:
    pipe = doc.get("pipeline", {}) or {}
    out = ["", "## The five-colour adversarial loop", ""]
    if not pipe.get("exists"):
        out.append("_No pipeline base found._")
        return out
    tag = SIMULATED if pipe.get("skip_live") else MEASURED
    out.append("Provenance of this whole section: **{}**".format(tag))
    out.append("")
    out.append("| colour | role | wrote | this run |")
    out.append("|---|---|---|---|")
    rd = pipe.get("rounds_detail", []) or []
    esc = sum(r.get("escapes", 0) for r in rd)
    prb = sum(r.get("blue_probes") or 0 for r in rd)
    rem = pipe.get("remedies", {}) or {}
    out.append(_row(["**RED**", "attacks the subject",
                     "`escapes.json` + `purple.json`",
                     "{} escapes across {} cells".format(esc, len(rd))]))
    out.append(_row(["**BLUE**", "relocates each escape, measures resistance",
                     "`blue-done.json`", "{} probes".format(prb)]))
    out.append(_row(["**PURPLE**", "stitches RED×BLUE into an interplay matrix",
                     "`report.json`",
                     "not run — driver wrote a synthetic stand-in"]))
    out.append(_row(["**WHITE**", "learns, proposes and validates remedies",
                     "`white-done.json`, `knowledge.json`",
                     "{} adopted / {} rejected".format(
                         rem.get("adopted_count"), rem.get("rejected_count"))]))
    out.append(_row(["**BLACK**", "attacks the *conclusion*, not the subject",
                     "`verdicts.json`, `black-done.json`",
                     "{} verdicts".format(
                         (pipe.get("verdicts", {}) or {}).get("total"))]))
    out.append("")

    trend = pipe.get("confidence_trend", []) or []
    cycles = pipe.get("cycles_report", []) or []
    if trend:
        out.append("### Learning curve across cycles")
        out.append("")
        rows = []
        for t, c in zip(trend, cycles):
            rows.append([t.get("cycle"), t.get("lessons"), t.get("defended"),
                         c.get("reverse_notes_written"), c.get("pruned_lessons"),
                         c.get("excluded_pairs"),
                         "✅" if all((c.get("phases") or {}).values()) else "⚠"])
        out.extend(_table(["cycle", "lessons", "defended confirmed",
                           "reverse notes", "pruned", "excluded pairs",
                           "phases ok"], rows))
        out.append("")
        counts = [t.get("lessons") for t in trend]
        if len(set(counts)) == 1:
            out.append("> The intent is a descending curve: BLACK confirms the "
                       "base resists a claim, the driver notes it, WHITE prunes "
                       "the lesson, and the next cycle's attack surface shrinks. "
                       "Here the count never moves — the loop closes structurally "
                       "but does not converge. See findings.")
            out.append("")

    if rd:
        out.append("### Per-variant handshake")
        out.append("")
        agg = defaultdict(lambda: {"esc": 0, "prb": 0, "res": [], "rounds": 0,
                                   "sides": set(), "adopted": 0})
        for r in rd:
            a = agg[r["variant"]]
            a["esc"] += r.get("escapes", 0)
            a["prb"] += r.get("blue_probes") or 0
            a["rounds"] += 1
            a["sides"].update(r.get("sides", []))
            a["adopted"] += r.get("white_adopted") or 0
            if r.get("blue_pass_rate_pct") is not None:
                a["res"].append(r["blue_pass_rate_pct"])
        rows = []
        for v, a in sorted(agg.items(), key=lambda kv: _vkey(kv[0])):
            res = round(sum(a["res"]) / len(a["res"]), 1) if a["res"] else None
            rows.append([v, a["rounds"], a["esc"], a["prb"],
                         "{}%".format(res) if res is not None else "—",
                         a["adopted"], "+".join(sorted(a["sides"]))])
        out.extend(_table(["variant", "rounds", "escapes", "probes",
                           "BLUE resistance", "remedies adopted",
                           "sides landed"], rows))
        out.append("")

        cells = Counter()
        for r in rd:
            for tech, place in r.get("escape_cells", []):
                cells[(tech, place)] += 1
        if cells:
            out.append("### Attack surface (technique × placement)")
            out.append("")
            techs = sorted({t for t, _ in cells})
            places = sorted({p for _, p in cells})
            out.append(_row(["technique \\ placement"] + places))
            out.append("|" + "|".join("---" for _ in range(len(places) + 1)) + "|")
            for t in techs:
                out.append(_row([t] + [cells.get((t, p), "·") for p in places]))
            out.append("")
    return out


def _vkey(v):
    try:
        return (0, int(v))
    except (TypeError, ValueError):
        return (1, str(v))


def _render_knowledge(doc: dict) -> list:
    pipe = doc.get("pipeline", {}) or {}
    kb = pipe.get("knowledge", {}) or {}
    rem = pipe.get("remedies", {}) or {}
    notes = pipe.get("notes", {}) or {}
    out = ["", "## What the system learned", ""]
    if not kb.get("lesson_count"):
        cycles = pipe.get("cycles_report") or []
        # pruned_lessons is a CUMULATIVE total per cycle, not a per-cycle
        # delta, so the run total is the last/max value -- never the sum.
        pruned = max((c.get("pruned_lessons", 0) for c in cycles), default=0)
        peak = max((c.get("knowledge", {}) or {}).get("lessons", 0)
                   for c in cycles) if cycles else 0
        if pruned or peak:
            out.append("The knowledge base is **empty at the end of the run — "
                       "by convergence, not by absence**. It peaked at {} "
                       "lessons in cycle 1 and {} were pruned once BLACK "
                       "confirmed the base already resisted them."
                       .format(peak, pruned))
            out.append("")
            out.append("That is the loop working as designed: WHITE learns a "
                       "lesson, BLACK independently confirms the configuration "
                       "already defends it, the driver writes a "
                       "reverse-deduction note, the lesson is retired, and the "
                       "next cycle's attack surface shrinks by that "
                       "(technique, placement) pair. {} pairs were excluded, "
                       "which is why RED's ledger is empty in the final cycle."
                       .format(max((c.get("excluded_pairs", 0)
                                    for c in cycles), default=0)))
            out.append("")
            out.append("> The caveat is what it converged *on*. The escape "
                       "corpus was seeded, so the system reached a fixed point "
                       "against a synthetic attack surface. The mechanism is "
                       "demonstrated; the fixed point is not a property of the "
                       "configuration under test.")
            out.append("")
        else:
            out.append("_No knowledge base._")
        return out
    out.append("`knowledge.json` v{} · {} lessons · {} patterns · updated {}"
               .format(kb.get("version"), kb.get("lesson_count"),
                       kb.get("pattern_count"), kb.get("updated_at")))
    out.append("")
    out.append("A *lesson* is content-addressed by (technique, placement, "
               "timing, category, missed principles, forbidden terms), so a "
               "repeat failure bumps a counter instead of adding a row. "
               "Confidence is `b / (a + b)` where `b` counts corroborating "
               "failures and `a` counts rounds the signature went quiet.")
    out.append("")
    rows = [[ "`{}`".format(L["signature"]), L["technique"], L["placement"],
              L["category"], L["occurrences"], L["confidence"], L["severity"],
              len(L.get("variants_affected", []))]
            for L in (kb.get("lessons") or [])[:15]]
    out.extend(_table(["sig", "technique", "placement", "category",
                       "occurrences", "confidence", "severity",
                       "variants hit"], rows))
    out.append("")

    pats = kb.get("patterns") or []
    if pats:
        out.append("### Generalizations")
        out.append("")
        rows = [[p.get("kind"), "`{}`".format(p.get("key")), p.get("support"),
                 p.get("lift")] for p in pats]
        out.extend(_table(["pattern kind", "key", "support", "lift"], rows))
        out.append("")
        out.append("> Every `lift` is 1.0. In `knowledge._regenerate_patterns` "
                   "the lift is `(support/total) / base_rate` where `base_rate` "
                   "is itself `support/total` — the ratio is 1.0 by "
                   "construction and carries no signal.")
        out.append("")

    if rem.get("adopted_count") or rem.get("rejected_count"):
        out.append("### Remedies proposed")
        out.append("")
        out.append("| kind | count | what it changes |")
        out.append("|---|---|---|")
        meaning = {
            "rule_clarification": "clarify a rule so a technique is handled in every placement",
            "placement_guard": "state that content in this location is not exempt",
            "example_pair": "add a non-compliant/compliant pair teaching the technique",
            "vocabulary_extension": "extend the approved word list",
            "precedence_rule": "order two rules that conflict",
        }
        for k, n in sorted((rem.get("by_kind") or {}).items(),
                           key=lambda kv: -kv[1]):
            out.append(_row([k, n, meaning.get(k, "—")]))
        out.append("")
        rows = [[ "`{}`".format(r["id"]), r["kind"], "`{}`".format(r["target"]),
                  r["confidence"], r["delta_resistance_pct"], r["provenance"]]
                for r in (rem.get("adopted") or [])[:12]]
        if rows:
            out.append("Adopted (top {}):".format(len(rows)))
            out.append("")
            out.extend(_table(["id", "kind", "target", "confidence",
                               "Δ resistance", "validation"], rows))
            out.append("")
            out.append("> `Δ resistance` is `simulate_validation`'s output: "
                       "`min(40, lesson_confidence × 35)`. It is a restatement "
                       "of how often the lesson recurred, not a re-measurement.")
            out.append("")

    if notes.get("total"):
        out.append("### Correspondence")
        out.append("")
        out.append("{} notes — {} protocol-shaped, {} driver reverse-deduction."
                   .format(notes["total"], notes.get("protocol_notes"),
                           notes.get("driver_notes")))
        out.append("")
        matrix = notes.get("matrix") or {}
        cols = sorted({to for row in matrix.values() for to in row})
        if cols:
            out.append(_row(["from \\ to"] + cols))
            out.append("|" + "|".join("---" for _ in range(len(cols) + 1)) + "|")
            for frm in sorted(matrix):
                out.append(_row([frm] + [matrix[frm].get(c, 0) for c in cols]))
            out.append("")
        if notes.get("protocol_notes") == 0:
            out.append("> No note carries a `from_colour` field, so the "
                       "NOTES_PROTOCOL bus (`notes.py` `NoteBus`) never ran. "
                       "Every note here is the driver's lighter "
                       "reverse-deduction record. Acknowledgements, rebuttals "
                       "and stale-note detection are unexercised.")
            out.append("")
    return out


def _render_verdicts(doc: dict) -> list:
    pipe = doc.get("pipeline", {}) or {}
    v = pipe.get("verdicts", {}) or {}
    out = ["", "## What BLACK ruled", ""]
    if not v.get("total"):
        out.append("_BLACK produced no verdicts._")
        return out
    out.append("BLACK does not attack the subject. It attacks the claim the "
               "other colours jointly produce, and rules on the benchmark "
               "itself.")
    out.append("")
    meaning = {
        "confirmed": "reproduces under BLACK's independent construction",
        "inflated": "reported number is optimistic",
        "deflated": "reported number is pessimistic",
        "unsound": "does not survive; methodology broken for this cell",
        "underpowered": "too few observations to support the claim",
    }
    rows = [[k, n, meaning.get(k, "—")]
            for k, n in sorted((v.get("by_verdict") or {}).items(),
                               key=lambda kv: -kv[1])]
    out.extend(_table(["verdict", "count", "meaning"], rows))
    out.append("")
    rows = [[k, n] for k, n in sorted(
        (v.get("by_challenged_colour") or {}).items(), key=lambda kv: -kv[1])]
    out.append("Whose claims were challenged:")
    out.append("")
    out.extend(_table(["colour challenged", "verdicts"], rows))
    out.append("")

    claims = v.get("by_claim") or {}
    known = {
        "challenge-scoring": "does the headline move under perturbed scoring weights",
        "challenge-selection": "did BLUE probe every technique RED used",
        "challenge-sparsity": "which interplay cells hold too few observations",
        "challenge-duplicates": "do near-identical inputs inflate the escape count",
    }
    rows = []
    for cid, counts in sorted(claims.items()):
        label = known.get(cid)
        if label is None:
            label = ("split-half of an adopted remedy"
                     if cid.startswith("remedy-")
                     else "WHITE hypothesis from the attack brief"
                     if cid.startswith("brief-") else "—")
        rows.append([ "`{}`".format(cid), sum(counts.values()),
                      ", ".join("{} {}".format(n, k) for k, n in counts.items()),
                      label])
    out.append("### Challenges run")
    out.append("")
    out.extend(_table(["claim", "n", "verdicts", "what it tests"], rows[:20]))
    out.append("")
    if not any(c.startswith("remedy-") for c in claims):
        out.append("> **The remedy challenge is missing.** `verification.py` "
                   "(split-half A/B, permutation test, bootstrap CI, five-rule "
                   "decision table) is the instrument that detects an overfit "
                   "remedy. It never ran: `_challenge_remedies` reads "
                   "`white['remedies_adopted']`, and `white-done.json` stores "
                   "the count under `adopted` with no per-case outcomes.")
        out.append("")

    nc = v.get("non_confirmed") or []
    if nc:
        out.append("### Dissenting verdicts")
        out.append("")
        rows = [[ "`{}`".format(r["claim_id"]), r["variant"], r["round"],
                  r["source"], "**{}**".format(r["verdict"]), r["reason"]]
                for r in nc]
        out.extend(_table(["claim", "variant", "round", "against",
                           "verdict", "reason"], rows))
        out.append("")
    else:
        out.append("_No dissenting verdict was returned._")
        out.append("")
    return out


def _render_findings(doc: dict) -> list:
    out = ["", "## Findings — what this run failed to establish", ""]
    findings = doc.get("findings") or []
    if not findings:
        out.append("_No integrity problems detected._")
        return out
    icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "⚪",
            "info": "🟢"}
    out.extend(_table(["", "severity", "finding"],
                      [[icon.get(f["severity"], "•"), f["severity"], f["title"]]
                       for f in findings]))
    out.append("")
    for i, f in enumerate(findings, 1):
        out.append("### {}. {} {}".format(i, icon.get(f["severity"], "•"),
                                          f["title"]))
        out.append("")
        out.append("**Observed.** {}".format(f["detail"]))
        out.append("")
        out.append("**Implication.** {}".format(f["implication"]))
        out.append("")
    return out


# ------------------------------------------------------------- LLM synthesis

def build_llm_brief(doc: dict, limit: int = 14000) -> str:
    """Compact the dossier into a prompt an LLM can reason over.

    The deterministic report already states every fact. The model's job is the
    part arithmetic cannot do: read the facts together and explain what the run
    means. So the brief carries the evidence, not the prose -- and it carries
    the provenance flags, because a model that does not know the numbers are
    simulated will confidently narrate them as measured.
    """
    pipe = doc.get("pipeline", {}) or {}
    kb = pipe.get("knowledge", {}) or {}
    brief = {
        "provenance": {
            "pipeline_offline": bool(pipe.get("skip_live")),
            "warning": ("All adversarial figures are SIMULATED: generators "
                        "produced them with no model in the loop."
                        if pipe.get("skip_live") else
                        "Adversarial figures came from live scoring."),
        },
        "measured_suites": [
            {k: t.get(k) for k in ("name", "tier", "suite", "status",
                                   "pass_rate_pct", "passed", "total_tests",
                                   "avg_correctness", "model")}
            for t in (doc.get("tier_runs") or [])],
        "measured_failures": [
            {"suite": t["name"], **{k: f.get(k) for k in
                                    ("test_id", "category", "score", "missed",
                                     "forbidden")}}
            for t in (doc.get("tier_runs") or [])
            for f in (t.get("failures") or [])][:25],
        "control_runs": doc.get("control_runs"),
        "pipeline": {
            "cycles": pipe.get("cycles"), "rounds": pipe.get("rounds"),
            "variants": pipe.get("tiers"),
            "confidence_trend": pipe.get("confidence_trend"),
            "cycles_report": pipe.get("cycles_report"),
            "handshake_cells": len(pipe.get("rounds_detail") or []),
            "total_escapes": sum(r.get("escapes", 0)
                                 for r in (pipe.get("rounds_detail") or [])),
            "total_probes": sum(r.get("blue_probes") or 0
                                for r in (pipe.get("rounds_detail") or [])),
        },
        "knowledge": {
            "lesson_count": kb.get("lesson_count"),
            "pattern_count": kb.get("pattern_count"),
            "techniques": kb.get("techniques"),
            "placements": kb.get("placements"),
            "top_lessons": (kb.get("lessons") or [])[:10],
            "patterns": kb.get("patterns"),
        },
        "remedies": {k: (pipe.get("remedies") or {}).get(k)
                     for k in ("adopted_count", "rejected_count", "by_kind",
                               "by_target")},
        "notes": {k: (pipe.get("notes") or {}).get(k)
                  for k in ("total", "by_kind", "matrix", "protocol_notes",
                            "driver_notes")},
        "black_verdicts": pipe.get("verdicts"),
        "integrity_findings": doc.get("findings"),
    }
    text = json.dumps(brief, indent=1, default=str)
    if len(text) > limit:
        brief["measured_failures"] = brief["measured_failures"][:8]
        brief["knowledge"]["top_lessons"] = brief["knowledge"]["top_lessons"][:5]
        text = json.dumps(brief, indent=1, default=str)
    return text[:limit]


LLM_INSTRUCTIONS = """\
You are reading the evidence dossier of an adversarial benchmark harness with \
five participants:

  RED    generates adversarial inputs and records which ones escaped
  BLUE   relocates each escaped payload and measures resistance
  PURPLE stitches RED x BLUE into an interplay matrix
  WHITE  learns from escapes, proposes remedies, validates them
  BLACK  attacks the CONCLUSION the other four produce, and rules on it

The design thesis is adversarial self-refutation: WHITE hands BLACK an attack \
brief describing the weakest links in the other colours' reasoning, so BLACK \
can disprove results that only looked correct. Claims that survive that \
process are the ones worth keeping.

Write a report for an engineer who did not run this. Requirements:

1. Lead with what is MEASURED versus SIMULATED. Never present a simulated \
   number as a measurement. If the pipeline ran offline, say so first.
2. Explain what the benchmark set out to test, what it actually established, \
   and what it failed to establish.
3. Use markdown tables for anything comparative.
4. Address the self-refutation loop explicitly: did BLACK genuinely challenge \
   the claims, or did it confirm them by construction? Did the learning curve \
   converge?
5. Ground every claim in a number from the dossier. Do not invent figures.
6. End with concrete next actions, ordered by what unblocks the most.

Dossier follows.

OUTPUT CONTRACT: reply with the report itself as markdown, and nothing else. Do \
not create, write or modify any file. Do not run any command. Do not preface the \
report with a summary of what you did. The report text IS the deliverable.
"""


def _strip_preamble(text: str) -> str:
    """Drop any chatter the model emitted before the report itself.

    The prompt forbids a preamble, but a model that ignores it would otherwise
    put "Report written to: ..." at the top of the artifact. The report always
    starts at its first markdown heading, so cut to there when one exists.
    """
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.lstrip().startswith("# "):
            return "\n".join(lines[i:]).strip()
    return text.strip()


def synthesize(doc: dict, model: str, timeout: int = 900) -> "str | None":
    """Send the dossier to a model and return its narrative report.

    Uses the `hermes` CLI already used by the harness's own runner. Returns
    None (never raises) if the CLI is absent or the call fails, so the
    deterministic report is always produced regardless.
    """
    import shutil
    import subprocess
    import tempfile

    exe = shutil.which("hermes")
    if not exe:
        return None
    prompt = LLM_INSTRUCTIONS + "\n```json\n" + build_llm_brief(doc) + "\n```\n"
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(prompt)
        prompt_path = fh.name
    try:
        proc = subprocess.run(
            [exe, "-z", "@" + prompt_path, "-m", model, "--yolo"],
            capture_output=True, text=True, timeout=timeout)
        text = (proc.stdout or "").strip()
        if not text:
            proc = subprocess.run([exe, "-z", prompt, "-m", model, "--yolo"],
                                  capture_output=True, text=True,
                                  timeout=timeout)
            text = (proc.stdout or "").strip()
        return _strip_preamble(text) if text else None
    except (OSError, subprocess.SubprocessError):
        return None
    finally:
        try:
            os.unlink(prompt_path)
        except OSError:
            pass


def _report_dir(bench: Path) -> Path:
    """Where daily reports live. Never the repo root."""
    return bench / "report"


def _run_fingerprint(doc: dict) -> str:
    """Stable id for the evidence a run rests on.

    Two invocations over the same artifacts must land on the same fingerprint,
    so a re-run replaces its own report instead of adding a near-duplicate.
    Derived from the inputs (which suites, which cycles, which knowledge
    version), never from the wall clock.
    """
    import hashlib

    pipe = doc.get("pipeline", {}) or {}
    parts = [
        sorted("{}:{}:{}".format(t.get("name"), t.get("status"),
                                 t.get("run_dir"))
               for t in (doc.get("tier_runs") or [])),
        str((pipe.get("knowledge") or {}).get("version")),
        str(pipe.get("cycles")), str(pipe.get("rounds")),
        str(len(pipe.get("rounds_detail") or [])),
        str((pipe.get("verdicts") or {}).get("total")),
        json.dumps(pipe.get("confidence_trend"), sort_keys=True, default=str),
    ]
    blob = json.dumps(parts, sort_keys=True, default=str)
    return hashlib.blake2s(blob.encode("utf-8"), digest_size=6).hexdigest()


def _archive(bench: Path, doc: dict, report: str,
             narrative: "str | None") -> dict:
    """Write this run's artifacts into the dated report tree.

    Layout keeps one directory per calendar day and one file set per distinct
    run, so a day of repeated runs stays browsable:

        report/YYYY-MM-DD/<fingerprint>-report.md
        report/YYYY-MM-DD/<fingerprint>-dossier.json
        report/YYYY-MM-DD/<fingerprint>-narrative.md
        report/latest-report.md          (pointer to the newest)
        report/index.json                (append-only run log)

    A repeated run over unchanged evidence rewrites its own fingerprint rather
    than accumulating copies -- that is the dedupe.
    """
    root = _report_dir(bench)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_dir = root / day
    day_dir.mkdir(parents=True, exist_ok=True)
    fp = _run_fingerprint(doc)

    written = {}
    targets = [("report", day_dir / "{}-report.md".format(fp), report),
               ("dossier", day_dir / "{}-dossier.json".format(fp),
                json.dumps(doc, indent=2, default=str))]
    if narrative:
        targets.append(("narrative", day_dir / "{}-narrative.md".format(fp),
                        narrative))
    for name, path, text in targets:
        existed = path.exists()
        path.write_text(text, encoding="utf-8")
        written[name] = {"path": str(path), "replaced": existed}

    (root / "latest-report.md").write_text(report, encoding="utf-8")
    if narrative:
        (root / "latest-narrative.md").write_text(narrative, encoding="utf-8")

    index_path = root / "index.json"
    index = _read_json(index_path, []) or []
    entry = {
        "fingerprint": fp, "day": day,
        "generated_utc": doc.get("generated_utc"),
        "suites_completed": sum(1 for t in (doc.get("tier_runs") or [])
                                if t.get("status") == "complete"),
        "suites_total": len(doc.get("tier_runs") or []),
        "findings": len(doc.get("findings") or []),
        "critical_high": sum(1 for f in (doc.get("findings") or [])
                             if f.get("severity") in ("critical", "high")),
        "simulated": bool((doc.get("pipeline") or {}).get("skip_live")),
        "narrative": bool(narrative),
        "files": {k: v["path"] for k, v in written.items()},
    }
    index = [e for e in index
             if not (isinstance(e, dict) and e.get("fingerprint") == fp
                     and e.get("day") == day)]
    index.append(entry)
    index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

    written["fingerprint"] = fp
    written["index"] = str(index_path)
    written["deduped"] = any(v.get("replaced") for v in written.values()
                             if isinstance(v, dict))
    return written


def _discover_base(bench: Path) -> Path:
    """Newest pipeline base: one holding a pipeline-report.json."""
    candidates = []
    scratch = bench.parent / "tmp"
    if scratch.exists():
        for d in scratch.iterdir():
            if d.is_dir() and (d / "pipeline-report.json").exists():
                candidates.append(d)
    if not candidates:
        return scratch / "pipe"
    return max(candidates, key=lambda d: _mtime(d / "pipeline-report.json"))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Summarize the latest adversarial benchmark run.")
    ap.add_argument("--base", default=None,
                    help="pipeline results base (default: newest under .agents/tmp)")
    ap.add_argument("--bench", default=str(BENCH),
                    help="benchmark directory")
    ap.add_argument("--out", default=None,
                    help="also write the markdown report here (the archived "
                         "copy under report/ is written regardless)")
    ap.add_argument("--json", default=None,
                    help="also write the raw dossier to this path")
    ap.add_argument("--no-archive", action="store_true",
                    help="skip the dated report/ tree; print to stdout only")
    ap.add_argument("--stdout", action="store_true",
                    help="print the report to stdout as well")
    ap.add_argument("--llm", action="store_true",
                    help="send the dossier to a model for a narrative report")
    ap.add_argument("--model", default="tencent/hy3:free")
    ap.add_argument("--llm-out", default=None,
                    help="write the model's narrative here (default: alongside --out)")
    ap.add_argument("--brief-out", default=None,
                    help="write the LLM prompt brief without calling a model")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    bench = Path(args.bench).resolve()
    base = Path(args.base).resolve() if args.base else _discover_base(bench)

    doc = build_dossier(bench, base)
    report = render_markdown(doc)

    if args.json:
        Path(args.json).write_text(json.dumps(doc, indent=2, default=str),
                                   encoding="utf-8")
    if args.brief_out:
        Path(args.brief_out).write_text(
            LLM_INSTRUCTIONS + "\n```json\n" + build_llm_brief(doc) + "\n```\n",
            encoding="utf-8")

    if args.out:
        Path(args.out).write_text(report, encoding="utf-8")
        if not args.quiet:
            print("wrote {}".format(args.out))
    else:
        print(report)

    if args.llm:
        narrative = synthesize(doc, args.model)
        if narrative is None:
            print("\n[llm] synthesis unavailable (hermes CLI missing or call "
                  "failed); the deterministic report above stands.")
        else:
            dest = args.llm_out or (
                str(Path(args.out).with_suffix(".narrative.md"))
                if args.out else None)
            if dest:
                Path(dest).write_text(narrative, encoding="utf-8")
                if not args.quiet:
                    print("wrote {}".format(dest))
            else:
                print("\n\n---\n\n# Model synthesis\n\n" + narrative)

    if not args.quiet and args.out:
        crit = [f for f in doc.get("findings", [])
                if f["severity"] in ("critical", "high")]
        print("  {} findings ({} critical/high)".format(
            len(doc.get("findings", [])), len(crit)))
        for f in crit[:5]:
            print("   - [{}] {}".format(f["severity"], f["title"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

