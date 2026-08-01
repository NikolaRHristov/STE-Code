#!/usr/bin/env python3
"""PURPLE — the stitch. Converges independently-produced RED, BLUE and WHITE
artifacts into one interplay report.

PURPLE runs no attacks and no defenses of its own. It is a pure reader: it walks
the handshake tree written by the other participants, tolerates missing or
partial rounds, and produces the cross-cutting matrices that no single
participant can see on its own.

Genericity: every noun (variant, round, runner, handshake filename, scoring
constant) comes from the harness profile via ``harness_config``. See
CONTRACT.md. Nothing in this module knows what standard is under test.

Outputs, all under ``<base>``:

    report.json          full machine-readable stitch
    report.md            human-readable summary with the interplay matrices
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness_config import (  # noqa: E402
    HarnessConfig,
    add_common_arguments,
    default_base,
    load_config,
)

UNKNOWN = "unknown"


def _read_json(path: Path, default=None):
    """Read a JSON document, returning ``default`` on any failure.

    PURPLE must never crash on a half-written or absent artifact: a missing
    round is data, not an error.
    """
    try:
        if path.exists():
            return json.loads(path.read_text())
    except (ValueError, OSError):
        pass
    return default


def _write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(str(tmp), str(path))


def _pct(numerator: int, denominator: int) -> "float | None":
    if not denominator:
        return None
    return round(numerator / denominator * 100.0, 1)


class RoundView:
    """Everything three independent processes wrote about one (variant, round).

    Any of the three may be absent. ``status`` summarizes which sides landed so
    the report can distinguish "defended successfully" from "never ran".
    """

    def __init__(self, cfg: HarnessConfig, base: Path, variant: str, round_n: int) -> None:
        self.variant = variant
        self.round = round_n
        self.dir = cfg.round_dir(base, variant, round_n)
        self.escapes = _read_json(cfg.red_ledger_path(base, variant, round_n), []) or []
        self.red = _read_json(cfg.red_sentinel_path(base, variant, round_n))
        self.blue = _read_json(cfg.blue_sentinel_path(base, variant, round_n))
        self.white = _read_json(cfg.white_sentinel_path(base, variant, round_n))

    @property
    def exists(self) -> bool:
        return self.dir.exists() or self.red is not None

    @property
    def status(self) -> str:
        sides = []
        if self.red is not None:
            sides.append("red")
        if self.blue is not None:
            sides.append("blue")
        if self.white is not None:
            sides.append("white")
        if not sides:
            return "absent"
        if len(sides) == 3:
            return "complete"
        return "partial:" + "+".join(sides)

    def escape_keys(self) -> "set[str]":
        return {str(e.get("test_id")) for e in self.escapes if e.get("test_id")}

    def resistance_rows(self) -> list:
        """BLUE's per-(technique, placement) resistance table, if it landed."""
        if not isinstance(self.blue, dict):
            return []
        rows = self.blue.get("resistance") or self.blue.get("resistance_table") or []
        return rows if isinstance(rows, list) else []


class Stitcher:
    """Builds the cross-cutting view from a tree of RoundViews."""

    def __init__(self, cfg: HarnessConfig, base: Path, variants: "list[str]", rounds: int) -> None:
        self.cfg = cfg
        self.base = base
        self.variants = variants
        self.rounds = rounds
        self.views: "dict[str, list[RoundView]]" = {}
        for key in variants:
            self.views[key] = [RoundView(cfg, base, key, n) for n in range(1, rounds + 1)]

    # ------------------------------------------------------------ per-variant

    def variant_timeline(self, key: str) -> list:
        """Round-by-round trajectory for one configuration under test."""
        timeline = []
        for view in self.views[key]:
            if not view.exists:
                timeline.append({"round": view.round, "status": "absent"})
                continue
            red = view.red or {}
            blue = view.blue or {}
            white = view.white or {}
            timeline.append({
                "round": view.round,
                "status": view.status,
                "red_total": red.get("red_total"),
                "red_passed": red.get("red_passed"),
                "red_pass_rate_pct": red.get("red_pass_rate_pct"),
                "escapes": len(view.escapes),
                "blue_probes": blue.get("blue_probes"),
                "blue_pass_rate_pct": blue.get("blue_pass_rate_pct"),
                "residual_escapes": blue.get("residual_escapes"),
                "white_remedies": white.get("remedies_proposed"),
                "white_adopted": white.get("remedies_adopted"),
                "white_status": white.get("status"),
            })
        return timeline

    def durability(self, key: str) -> dict:
        """Which escapes persisted across rounds versus which were closed.

        An escape id seen in round N and absent in round N+1 is treated as
        closed; one that reappears is durable. Durable failures are the ones
        worth spending a remedy on.
        """
        seen_first: "dict[str, int]" = {}
        seen_last: "dict[str, int]" = {}
        for view in self.views[key]:
            for eid in view.escape_keys():
                seen_first.setdefault(eid, view.round)
                seen_last[eid] = view.round
        durable = {e: (seen_first[e], seen_last[e])
                   for e in seen_first if seen_last[e] > seen_first[e]}
        closed = {e: seen_first[e] for e in seen_first if e not in durable}
        return {
            "total_distinct_escapes": len(seen_first),
            "durable": len(durable),
            "closed": len(closed),
            "durability_pct": _pct(len(durable), len(seen_first)),
            "durable_ids": sorted(durable)[:40],
        }

    # ------------------------------------------------------------- matrices

    def interplay_matrix(self) -> dict:
        """technique x placement -> attack volume, escape count, BLUE resistance.

        This is the artifact that justifies the whole four-colour split: RED
        alone knows what it threw, BLUE alone knows what held, and only the
        stitch can divide one by the other.
        """
        attacks: "dict[tuple, int]" = defaultdict(int)
        escapes: "dict[tuple, int]" = defaultdict(int)
        probes: "dict[tuple, int]" = defaultdict(int)
        held: "dict[tuple, int]" = defaultdict(int)

        for key in self.variants:
            for view in self.views[key]:
                red = view.red or {}
                for cell in red.get("attack_matrix", []) or []:
                    coord = (cell.get("technique", UNKNOWN), cell.get("placement", UNKNOWN))
                    attacks[coord] += int(cell.get("cases", 0))
                for esc in view.escapes:
                    coord = (esc.get("technique", UNKNOWN), esc.get("placement", UNKNOWN))
                    escapes[coord] += 1
                    attacks[coord] += 0
                for row in view.resistance_rows():
                    coord = (row.get("technique", UNKNOWN), row.get("placement", UNKNOWN))
                    probes[coord] += int(row.get("probes", 0))
                    held[coord] += int(row.get("passed", 0))

        coords = set(attacks) | set(escapes) | set(probes)
        cells = []
        for technique, placement in sorted(coords):
            coord = (technique, placement)
            cells.append({
                "technique": technique,
                "placement": placement,
                "attacks": attacks.get(coord, 0),
                "escapes": escapes.get(coord, 0),
                "escape_rate_pct": _pct(escapes.get(coord, 0), attacks.get(coord, 0)),
                "blue_probes": probes.get(coord, 0),
                "blue_held": held.get(coord, 0),
                "resistance_pct": _pct(held.get(coord, 0), probes.get(coord, 0)),
            })
        return {"cells": cells, "coordinates": len(cells)}

    def timing_profile(self) -> list:
        """Escape counts grouped by RED's timing strategy and round index.

        Answers: does escalating pressure actually find more than immediate
        pressure, and does the configuration relax under a decaying schedule?
        """
        grid: "dict[tuple, int]" = defaultdict(int)
        for key in self.variants:
            for view in self.views[key]:
                for esc in view.escapes:
                    grid[(esc.get("timing", UNKNOWN), view.round)] += 1
        by_timing: "dict[str, dict]" = defaultdict(dict)
        for (timing, round_n), count in grid.items():
            by_timing[timing][str(round_n)] = count
        rows = []
        for timing in sorted(by_timing):
            per_round = by_timing[timing]
            total = sum(per_round.values())
            ordered = [per_round.get(str(n), 0) for n in range(1, self.rounds + 1)]
            trend = "flat"
            if len(ordered) >= 2:
                if ordered[-1] > ordered[0]:
                    trend = "worsening"
                elif ordered[-1] < ordered[0]:
                    trend = "improving"
            rows.append({"timing": timing, "total_escapes": total,
                         "per_round": ordered, "trend": trend})
        return sorted(rows, key=lambda r: -r["total_escapes"])

    def variant_ranking(self) -> list:
        """Rank configurations under test by how well they actually held."""
        rows = []
        for key in self.variants:
            variant = self.cfg.variant(key)
            total_escapes = sum(len(v.escapes) for v in self.views[key])
            probes = 0
            held = 0
            for view in self.views[key]:
                for row in view.resistance_rows():
                    probes += int(row.get("probes", 0))
                    held += int(row.get("passed", 0))
            red_rates = [float(v.red["red_pass_rate_pct"]) for v in self.views[key]
                         if isinstance(v.red, dict) and v.red.get("red_pass_rate_pct") is not None]
            rows.append({
                "variant": key,
                "label": variant.label,
                "directory": variant.directory,
                "intensity": variant.intensity,
                "rounds_present": sum(1 for v in self.views[key] if v.exists),
                "total_escapes": total_escapes,
                "mean_red_pass_rate_pct": round(sum(red_rates) / len(red_rates), 1) if red_rates else None,
                "blue_resistance_pct": _pct(held, probes),
                "durability": self.durability(key),
            })
        return sorted(rows, key=lambda r: (r["total_escapes"], -(r["intensity"])))

    def coverage(self) -> dict:
        """How much of the planned (variant x round) grid actually produced data."""
        planned = len(self.variants) * self.rounds
        present = complete = partial = 0
        missing = []
        for key in self.variants:
            for view in self.views[key]:
                if not view.exists:
                    missing.append(f"{key}/r{view.round}")
                    continue
                present += 1
                if view.status == "complete":
                    complete += 1
                else:
                    partial += 1
        return {"planned_cells": planned, "cells_with_data": present,
                "complete": complete, "partial": partial,
                "coverage_pct": _pct(present, planned),
                "missing": missing[:40]}

    # --------------------------------------------------------------- report

    def build_report(self) -> dict:
        matrix = self.interplay_matrix()
        cells = matrix["cells"]
        by_technique: "dict[str, dict]" = defaultdict(lambda: {"escapes": 0, "probes": 0, "held": 0})
        by_placement: "dict[str, dict]" = defaultdict(lambda: {"escapes": 0, "probes": 0, "held": 0})
        for cell in cells:
            for bucket, key in ((by_technique, cell["technique"]), (by_placement, cell["placement"])):
                bucket[key]["escapes"] += cell["escapes"]
                bucket[key]["probes"] += cell["blue_probes"]
                bucket[key]["held"] += cell["blue_held"]

        def _rollup(bucket: dict, name: str) -> list:
            rows = []
            for key in sorted(bucket):
                entry = bucket[key]
                rows.append({name: key, "escapes": entry["escapes"],
                             "blue_probes": entry["probes"],
                             "resistance_pct": _pct(entry["held"], entry["probes"])})
            return sorted(rows, key=lambda r: -r["escapes"])

        knowledge = _read_json(self.base / self.cfg.handshake.knowledge_base, {}) or {}
        white_report = _read_json(self.base / "white-report.json", {}) or {}

        return {
            "schema_version": 2,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "profile": {"id": self.cfg.profile_id, "display_name": self.cfg.display_name,
                        "source": str(self.cfg.source)},
            "base": str(self.base),
            "variants": self.variants,
            "rounds": self.rounds,
            "coverage": self.coverage(),
            "variant_ranking": self.variant_ranking(),
            "timelines": {key: self.variant_timeline(key) for key in self.variants},
            "interplay_matrix": matrix,
            "by_technique": _rollup(by_technique, "technique"),
            "by_placement": _rollup(by_placement, "placement"),
            "timing_profile": self.timing_profile(),
            "knowledge_summary": {
                "lessons": len(knowledge.get("lessons", []) or []),
                "patterns": len(knowledge.get("patterns", []) or []),
                "schema_version": knowledge.get("schema_version"),
            },
            "white_summary": {
                "remedies_proposed": white_report.get("remedies_proposed"),
                "remedies_adopted": white_report.get("remedies_adopted"),
                "convergence": white_report.get("convergence"),
            },
        }


def render_markdown(report: dict) -> str:
    """Human-readable summary. Tables are capped so the file stays readable."""
    out = []
    add = out.append
    add(f"# Adversarial stitch — {report['profile']['display_name']}")
    add("")
    add(f"Generated {report['generated_at']} · base `{report['base']}`")
    cov = report["coverage"]
    add(f"Coverage: {cov['cells_with_data']}/{cov['planned_cells']} cells "
        f"({cov['coverage_pct']}%) — {cov['complete']} complete, {cov['partial']} partial")
    add("")

    add("## Configurations under test")
    add("")
    add("| variant | label | escapes | mean RED pass % | BLUE resistance % | durable |")
    add("|---|---|---|---|---|---|")
    for row in report["variant_ranking"]:
        dur = row["durability"]
        add(f"| `{row['variant']}` | {row['label']} | {row['total_escapes']} | "
            f"{row['mean_red_pass_rate_pct']} | {row['blue_resistance_pct']} | "
            f"{dur['durable']}/{dur['total_distinct_escapes']} |")
    add("")

    add("## Escapes by technique")
    add("")
    add("| technique | escapes | probes | resistance % |")
    add("|---|---|---|---|")
    for row in report["by_technique"][:20]:
        add(f"| {row['technique']} | {row['escapes']} | {row['blue_probes']} | {row['resistance_pct']} |")
    add("")

    add("## Escapes by placement")
    add("")
    add("| placement | escapes | probes | resistance % |")
    add("|---|---|---|---|")
    for row in report["by_placement"][:20]:
        add(f"| {row['placement']} | {row['escapes']} | {row['blue_probes']} | {row['resistance_pct']} |")
    add("")

    add("## Timing profile")
    add("")
    add("| timing | total escapes | per round | trend |")
    add("|---|---|---|---|")
    for row in report["timing_profile"]:
        add(f"| {row['timing']} | {row['total_escapes']} | {row['per_round']} | {row['trend']} |")
    add("")

    add("## Interplay matrix (technique × placement)")
    add("")
    add("| technique | placement | attacks | escapes | escape % | probes | resistance % |")
    add("|---|---|---|---|---|---|---|")
    hot = sorted(report["interplay_matrix"]["cells"], key=lambda c: -c["escapes"])[:40]
    for cell in hot:
        add(f"| {cell['technique']} | {cell['placement']} | {cell['attacks']} | "
            f"{cell['escapes']} | {cell['escape_rate_pct']} | {cell['blue_probes']} | "
            f"{cell['resistance_pct']} |")
    add("")

    know = report["knowledge_summary"]
    white = report["white_summary"]
    add("## Self-healing")
    add("")
    add(f"- knowledge base: {know['lessons']} lessons, {know['patterns']} patterns")
    add(f"- remedies proposed: {white['remedies_proposed']} · adopted: {white['remedies_adopted']}")
    add(f"- convergence: {white['convergence']}")
    add("")
    return "\n".join(out)


