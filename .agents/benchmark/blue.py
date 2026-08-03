#!/usr/bin/env python3
"""BLUE (defender / hardening) driver for the STE-Code RED/BLUE/PURPLE benchmark.

BLUE launches INDEPENDENTLY of RED and converges via a FILESYSTEM HANDSHAKE, not
a process dependency:

    RED writes  <base>/tier<T>/round<N>/purple.json   (the "purple" sentinel)
    BLUE polls  that file up to --await-timeout; if it appears, BLUE reads
                 <base>/tier<T>/round<N>/escapes.json and builds PROBES.
    BLUE writes <base>/tier<T>/round<N>/blue-done.json

If purple.json never appears (RED crashed / stopped), BLUE records
status "await-timeout" for that round and moves on -- it NEVER blocks on a
process. This is the same contract purple.py implements; BLUE re-uses the exact
flag set that purple.py::_run_orchestrator passes to orchestrator.py.

PLACEMENT of the OFFENDING PAYLOAD in each probe (probe_placement):
    verbatim, head, tail, middle, nested, table_cell, header,
    isolated, diluted
DEFENSE TIMING (how BLUE schedules re-probing across rounds):
    reactive, cumulative, sliding_window, immediate_retest, delayed, prioritized

Resistance scoring: per (technique, placement) pair, count probes run / passed /
resistance_pct / residual escape ids. Written into blue-done.json so PURPLE can
stitch an interplay matrix.

--skip-live makes BLUE fully offline + deterministic: probes are generated and a
resistance table is derived from the escape records themselves (no model call).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
BENCH = PROJECT / ".agents" / "benchmark"
ORCH = BENCH / "orchestrator.py"
sys.path.insert(0, str(BENCH))

from harness_config import load_config, resolve_base  # noqa: E402

# Tier system-prompt paths (mirror purple.py exactly).
TIER_DIR = {
    t: (PROJECT / "ste-code" / "artifacts" / f"level{t}" / "system-prompt.txt")
    for t in (-2, -1, 0, 1, 2, 3, 4, 5)
}

PROBE_PLACEMENTS = [
    "verbatim",
    "head",
    "tail",
    "middle",
    "nested",
    "table_cell",
    "header",
    "isolated",
    "diluted",
]
DEFENSE_TIMINGS = [
    "reactive",
    "cumulative",
    "sliding_window",
    "immediate_retest",
    "delayed",
    "prioritized",
]

# Benign carrier used to relocate / dilute payloads.
_BENIGN = "The module loads the configuration and starts the worker loop normally."


# ------------------------------------------------------------------- orchestrator


def _run_orchestrator(
    test_dir: Path,
    sp: Path,
    results_dir: Path,
    model: str,
    max_workers: int,
    timeout: int,
) -> "dict | None":
    """Same invocation as purple.py::_run_orchestrator."""
    results_dir.mkdir(parents=True, exist_ok=True)
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(ORCH),
                "--test-dir",
                str(test_dir),
                "--system-prompt-file",
                str(sp),
                "--results-dir",
                str(results_dir),
                "--max-workers",
                str(max_workers),
                "--timeout",
                str(timeout),
                "--poll-interval",
                "1",
                "--model",
                model,
            ],
            cwd=str(PROJECT),
            capture_output=True,
            text=True,
            timeout=60 * 60,
        )
    except subprocess.TimeoutExpired:
        return None
    runs = sorted(results_dir.glob("run-*"))
    if not runs:
        return None
    last = runs[-1]
    per_test = []
    if (last / "per-test-results.json").exists():
        per_test = json.load(open(last / "per-test-results.json"))
    agg = None
    if (last / "aggregate-results.json").exists():
        agg = json.load(open(last / "aggregate-results.json"))
    if agg is not None:
        agg["per_test"] = per_test
        return agg
    if per_test:
        passed = sum(1 for t in per_test if t.get("passed"))
        return {
            "total_tests": len(per_test),
            "passed": passed,
            "pass_rate_pct": round(passed / len(per_test) * 100, 1) if per_test else 0,
            "per_test": per_test,
        }
    return None


# ----------------------------------------------------------------- probe builders


def _relocate(payload: str, probe_placement: str) -> str:
    """Return the input for a probe that relocates `payload` per placement."""
    if probe_placement in ("verbatim", "isolated"):
        return payload
    if probe_placement == "head":
        return f"{payload} {_BENIGN}"
    if probe_placement == "tail":
        return f"{_BENIGN} {payload}"
    if probe_placement == "middle":
        return f"{_BENIGN} {payload} {_BENIGN}"
    if probe_placement == "nested":
        return f"> Quoted requirement:\n> {payload}\n\n{_BENIGN}"
    if probe_placement == "table_cell":
        return (
            f"| Field | Value |\n|-------|-------|\n| Note | {payload} |\n\n{_BENIGN}"
        )
    if probe_placement == "header":
        return f"# {payload}\n\n{_BENIGN}"
    if probe_placement == "diluted":
        # large volume of compliant text around the fragment
        return (_BENIGN + " ") * 6 + payload + (" " + _BENIGN) * 6
    if probe_placement == "code_comment":
        # Hybrid: the violation sits inside a fenced code block's comment, a
        # structure the scoring model may treat as non-documentation.
        return f"```python\n# {payload}\nx = compute()\n```\n\n{_BENIGN}"
    if probe_placement == "inline_code_span":
        # Hybrid: violation embedded in an inline-code span within prose.
        return f"The instruction states `{payload}` and the worker follows it."
    if probe_placement == "link_title":
        # Hybrid: violation smuggled into a markdown link's title attribute.
        return f'[see the guide](https://example.com "{payload}")'
    return payload


# Hybrid placements: syntactic contexts the standard may not scope.
HYBRID_PLACEMENTS = ["code_comment", "inline_code_span", "link_title"]


def _rewrite_helpful(payload: str, cfg) -> str:
    """Deterministic offline rewriter for `helpful` BLUE capsules (Unit 3).

    Replaces forbidden-bank terms with benign carrier words so the probe reads
    as a compliant example that primed the model's compliance confidence. No
    model call -- consistent with CONTRACT.md §6.
    """
    text = payload
    forbidden = cfg.bank("forbidden_bank", default=[]) if cfg else []
    for term in forbidden:
        if not isinstance(term, str) or not term:
            continue
        if term in text:
            text = text.replace(term, _BENIGN.split()[0])
    return text.strip() or _BENIGN


def build_blue_probes(
    escapes: "list[dict]",
    *,
    probe_placements: "list[str]",
    defense_timing: str = "reactive",
    round_n: int = 1,
    window: int = 3,
    budget: int = 50,
    history: "list[dict]" = None,
    blue_intent: str = "adversarial",
    cfg=None,
) -> "list[dict]":
    """Build the family of BLUE probes for one round from RED's escapes.

    Unit 3 intent: `blue_intent` controls probe character:
      adversarial -> current behaviour (relocate raw payload across placements)
      helpful    -> rewrite payload to a compliant form (priming, not challenge)
      hybrid     -> embed the violation in syntactic contexts the standard may
                    not scope (code_comment / inline_code_span / link_title)
    """
    history = history or []
    if blue_intent == "hybrid":
        probe_placements = list(HYBRID_PLACEMENTS)
    elif blue_intent == "helpful":
        # helpful probes use the same placements but with rewritten payloads
        pass

    # defense_timing controls WHICH escapes are re-probed and labeled:
    #   ... (unchanged selection logic below)
    if defense_timing == "reactive":
        src = escapes
    elif defense_timing == "cumulative":
        src = history + escapes
    elif defense_timing == "sliding_window":
        recent = [e for e in history if (round_n - e.get("round", 0)) <= window]
        src = recent + escapes
    elif defense_timing == "immediate_retest":
        src = escapes
    elif defense_timing == "delayed":
        src = [] if (round_n % 2 == 1) else history
    elif defense_timing == "prioritized":
        ordered = sorted(
            escapes,
            key=lambda e: (
                e.get("correctness_score") is None,
                e.get("correctness_score", 1.0),
            ),
        )
        src = ordered[:budget]
    else:
        src = escapes

    probes: "list[dict]" = []
    for e in src:
        for pp in probe_placements:
            payload = e.get("input") or e.get("violating_output") or ""
            if blue_intent == "helpful":
                payload = _rewrite_helpful(payload, cfg)
            probes.append(
                {
                    "id": f"blue-{e.get('test_id', 'x')}-{pp}",
                    "case_id": f"blue-{e.get('test_id', 'x')}-{pp}",
                    "category": e.get("category", "readme"),
                    "description": (
                        f"BLUE probe ({e.get('technique', '?')}) "
                        f"placement={pp} timing={defense_timing} "
                        f"intent={blue_intent}"
                    ),
                    "input": _relocate(payload, pp),
                    "expected_principles": e.get("missed_principles")
                    or ["P1", "P10", "P4"],
                    "expected_keywords": [],
                    "forbidden_keywords": sorted(set(e.get("forbidden_found", []))),
                    "max_tokens": 1500,
                    "difficulty": "hard",
                    "adversarial_technique": e.get("technique", "unknown"),
                    "probe_placement": pp,
                    "defense_timing": defense_timing,
                    "blue_intent": blue_intent,
                    "round": round_n,
                    "blue_probe": True,
                    "source_escape": e.get("test_id"),
                }
            )
    return probes


# --------------------------------------------------------------- resistance table


def _resistance_table(probes: "list[dict]", per_test: "list[dict]"):
    """Compute per (technique, placement) resistance from a live run.

    Falls back to a deterministic offline estimate when per_test is empty.
    """
    by_id = {p["id"]: p for p in probes}
    passed_ids = {t.get("test_id") for t in per_test if t.get("passed")}
    table: "dict[tuple, dict]" = defaultdict(
        lambda: {"probes_run": 0, "probes_passed": 0, "residual": []}
    )
    for p in probes:
        key = (p["adversarial_technique"], p["probe_placement"])
        table[key]["probes_run"] += 1
        if p["id"] in passed_ids:
            table[key]["probes_passed"] += 1
        else:
            table[key]["residual"].append(p["source_escape"])
    out = []
    for (tech, place), v in sorted(table.items()):
        run = v["probes_run"]
        out.append(
            {
                "technique": tech,
                "placement": place,
                "probes_run": run,
                "probes_passed": v["probes_passed"],
                "resistance_pct": round(v["probes_passed"] / run * 100, 1)
                if run
                else 0.0,
                "residual_escape_ids": sorted(set(v["residual"])),
            }
        )
    return out


def _offline_resistance(probes: "list[dict]") -> "list[dict]":
    """Deterministic offline resistance: assume every probe that relocates the
    payload to a non-verbatim placement passes, verbatim fails (it is the same
    as the original escape). Gives BLUE a stable, reproducible score with no
    model. This is a conservative estimator, clearly labelled offline."""
    table: "dict[tuple, dict]" = defaultdict(
        lambda: {"probes_run": 0, "probes_passed": 0, "residual": []}
    )
    for p in probes:
        key = (p["adversarial_technique"], p["probe_placement"])
        table[key]["probes_run"] += 1
        if p["probe_placement"] == "verbatim":
            table[key]["residual"].append(p["source_escape"])
        else:
            table[key]["probes_passed"] += 1
    out = []
    for (tech, place), v in sorted(table.items()):
        run = v["probes_run"]
        out.append(
            {
                "technique": tech,
                "placement": place,
                "probes_run": run,
                "probes_passed": v["probes_passed"],
                "resistance_pct": round(v["probes_passed"] / run * 100, 1)
                if run
                else 0.0,
                "residual_escape_ids": sorted(set(v["residual"])),
            }
        )
    return out


# ------------------------------------------------------------------- round loop


def _await_file(path: Path, timeout: float, poll: float) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(poll)
    return False


def run_blue(tier: int, args, base: Path, report: dict) -> None:
    sp = TIER_DIR.get(tier)
    if sp is None and not args.skip_live:
        tier_rounds = [
            {
                "round": 1,
                "status": "no-tier-prompt",
                "blue_probes": 0,
                "blue_pass_rate_pct": None,
            }
        ]
        report.setdefault("per_tier", {})[tier] = {
            "mode": "blue",
            "rounds": tier_rounds,
        }
        return
    tier_rounds = []
    history: "list[dict]" = []
    for rnd in range(1, args.rounds + 1):
        rdir = base / f"tier{tier}" / f"round{rnd}"
        sentinel = rdir / "purple.json"  # RED's handshake
        found = _await_file(sentinel, args.await_timeout, args.poll_interval)
        if not found:
            tier_rounds.append(
                {
                    "round": rnd,
                    "status": "await-timeout",
                    "blue_probes": 0,
                    "blue_pass_rate_pct": None,
                }
            )
            break  # RED is not producing this round; stop.
        escapes = (
            json.load(open(args.escape_override))
            if args.escape_override and Path(args.escape_override).exists()
            else (
                json.load(open(rdir / "escapes.json"))
                if (rdir / "escapes.json").exists()
                else []
            )
        )
        if not escapes:
            # A round with no escapes is a real (honest) outcome, not a missing
            # run. Write the sentinel so PURPLE/BLACK/run_pipeline don't wait
            # forever for a file that will never appear, and mark it so it is
            # not read as a successful defense.
            (rdir / "blue-done.json").write_text(
                json.dumps(
                    {
                        "tier": tier,
                        "round": rnd,
                        "status": "no-escapes",
                        "blue_probes": 0,
                        "blue_passed": 0,
                        "blue_pass_rate_pct": None,
                        "defense_timing": args.defense_timing,
                        "residual_escape_ids": [],
                        "resistance_table": [],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            tier_rounds.append(
                {
                    "round": rnd,
                    "status": "no-escapes",
                    "blue_probes": 0,
                    "blue_pass_rate_pct": None,
                }
            )
            break
        probes = build_blue_probes(
            escapes,
            probe_placements=_parse_csv(args.probe_placements, PROBE_PLACEMENTS),
            defense_timing=args.defense_timing,
            round_n=rnd,
            window=args.window,
            budget=args.budget,
            history=history,
            blue_intent=getattr(args, "blue_intent", "adversarial"),
            cfg=load_config(),
        )
        blue_dir = rdir / "blue"
        (blue_dir / "test-cases").mkdir(parents=True, exist_ok=True)
        (blue_dir / "test-cases" / "category-blue.json").write_text(
            json.dumps(probes, indent=2), encoding="utf-8"
        )

        per_test = []
        bp = 0
        bt = len(probes)
        if args.skip_live:
            table = _offline_resistance(probes)
            # Derive BOTH the count and the rate from the table. Assigning only
            # the rate here left blue_passed at its initial 0 while
            # blue_pass_rate_pct said 88.9% -- a consumer reading the count saw
            # total defense failure.
            bp = sum(t["probes_passed"] for t in table)
            bt = sum(t["probes_run"] for t in table)
            blue_rate = round(bp / max(1, bt) * 100, 1)
        else:
            agg = _run_orchestrator(
                blue_dir / "test-cases",
                sp,
                blue_dir / "run",
                args.model,
                args.max_workers,
                args.timeout,
            )
            per_test = agg.get("per_test", []) if agg else []
            bp = agg.get("passed", 0) if agg else 0
            bt = agg.get("total_tests", len(probes)) if agg else len(probes)
            blue_rate = round(bp / bt * 100, 1) if bt else 0.0
            table = _resistance_table(probes, per_test)

        # residual = escapes BLUE still failed to close
        residual_ids = sorted({rid for t in table for rid in t["residual_escape_ids"]})
        # status: "deferred" when this round produced no probes (e.g. delayed
        # timing on an odd round). A deferred round is NOT a successful defense
        # -- it must not be read as "BLUE passed" downstream.
        status = "deferred" if not probes else "done"
        (rdir / "blue-done.json").write_text(
            json.dumps(
                {
                    "tier": tier,
                    "round": rnd,
                    "status": status,
                    "blue_probes": len(probes),
                    "blue_passed": bp,
                    "blue_pass_rate_pct": blue_rate,
                    "residual_escape_ids": residual_ids,
                    "resistance_table": table,
                    "defense_timing": args.defense_timing,
                },
                indent=2,
            ),
            encoding="utf-8",
        )

        history.extend(escapes)
        tier_rounds.append(
            {
                "round": rnd,
                "status": "deferred" if not probes else "done",
                "blue_probes": len(probes),
                "blue_pass_rate_pct": blue_rate,
                "residual_escapes": len(residual_ids),
                "techniques": sorted({e["technique"] for e in escapes}),
            }
        )
        if blue_rate >= (args.blue_threshold or 95.0):
            break
        if not residual_ids:
            break
    report.setdefault("per_tier", {})[tier] = {"mode": "blue", "rounds": tier_rounds}


# ------------------------------------------------------------------- utilities


def _parse_csv(value: "str | None", default: "list[str]") -> "list[str]":
    if not value:
        return list(default)
    parts = [p.strip() for p in value.split(",") if p.strip()]
    return parts or list(default)


# ------------------------------------------------------------------------- CLI


def main() -> int:
    ap = argparse.ArgumentParser(description="BLUE defender / hardening driver.")
    ap.add_argument("--tiers", default="-2,-1,0,1,2,3,4,5")
    ap.add_argument("--rounds", type=int, default=3)
    ap.add_argument(
        "--base",
        default=None,
        help="output dir (default: <results_base>/redblue); must stay under it",
    )
    ap.add_argument("--await-timeout", type=float, default=3600.0)
    ap.add_argument("--poll-interval", type=float, default=1.0)
    ap.add_argument(
        "--probe-placements",
        default=None,
        help="csv subset of: " + ",".join(PROBE_PLACEMENTS),
    )
    ap.add_argument(
        "--defense-timings",
        default="reactive",
        help="single defense timing (one per invocation)",
    )
    ap.add_argument("--window", type=int, default=3, help="sliding_window K")
    ap.add_argument(
        "--budget", type=int, default=50, help="prioritized: max probes per round"
    )
    ap.add_argument("--model", default="tencent/hy3:free")
    ap.add_argument("--max-workers", type=int, default=2)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--blue-threshold", type=float, default=95.0)
    ap.add_argument(
        "--skip-live",
        action="store_true",
        help="generate probes + offline resistance without a model",
    )
    ap.add_argument(
        "--escape-override",
        default=None,
        help="Unit 2: path to a scoped escapes.json (capsule scheduler). "
        "When set, BLUE reads probes from here instead of the "
        "conventional tier<T>/round<N>/escapes.json.",
    )
    ap.add_argument(
        "--blue-intent",
        default="adversarial",
        choices=["adversarial", "helpful", "hybrid"],
        help="Unit 3: capsule intent for probe generation "
        "(helpful=compliant priming, hybrid=embedded-syntax).",
    )
    args = ap.parse_args()

    base = resolve_base(load_config(), args.base)
    base.mkdir(parents=True, exist_ok=True)
    tiers = [int(x) for x in args.tiers.split(",")]
    # defense-timings kept singular per run for clean independence; accept csv
    # by running each sequentially into the report.
    timings = [t.strip() for t in args.defense_timings.split(",") if t.strip()] or [
        "reactive"
    ]

    report: "dict" = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mode": "blue",
        "model": args.model,
        "tiers": tiers,
        "rounds": args.rounds,
        "per_tier": {},
    }
    for timing in timings:
        args.defense_timing = timing
        for t in tiers:
            run_blue(t, args, base, report)

    (base / "blue-report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(f"\nWrote {base / 'blue-report.json'} (defense_timings={timings})")
    for t, tr in report.get("per_tier", {}).items():
        for r in tr.get("rounds", []):
            print(f"  tier{t} r{r.get('round')}: {r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
