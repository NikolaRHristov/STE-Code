#!/usr/bin/env python3
"""Collect every artifact the adversarial benchmark leaves on disk into one
machine-readable dossier, then render it as a human-readable report.

The harness (RED / BLUE / PURPLE / WHITE / BLACK) converges through the
filesystem, so its evidence is scattered across three unrelated trees:

    .agents/benchmark/tests/<tier>-<suite>/run-*/   scored tier runs
    .agents/benchmark/results-control/run-*/        control (no-prompt) runs
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
    root = bench / "results-control"
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


# __END__
