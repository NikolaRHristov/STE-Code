#!/usr/bin/env python3
"""Split-half A/B verification. The instrument BLACK runs on.

The failure this prevents
-------------------------
A harness that derives a remedy from a set of cases and then measures that
remedy on the same cases will report an effect even when the remedy learned
nothing general. The number is real; the conclusion is not.

So every claim is evaluated twice. Arm A is the *derivation* set: remedies,
probes and thresholds may be built from it. Arm B is the *verification* set,
untouched until the claim is fixed, evaluated once. An effect that appears on A
and vanishes on B is overfitting, and this module says so with the measured gap
rather than leaving it to be noticed.

Determinism
-----------
Splits use blake2s over the case id, never `random.shuffle` and never Python's
builtin `hash()` (PYTHONHASHSEED-salted, so it differs per process). The same
corpus and seed therefore produce byte-identical arms on any machine, which is
what makes a split reproducible without storing it.
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness_config import load_config  # noqa: E402

DEFAULT_ITERATIONS = 2000
ALPHA = 0.05


def _stable_bits(value: str, seed: int) -> int:
    """A reproducible integer for a case id. blake2s, not hash()."""
    digest = hashlib.blake2s("{}:{}".format(seed, value).encode("utf-8"),
                             digest_size=8).digest()
    return int.from_bytes(digest, "big")


def _case_id(case: dict, index: int) -> str:
    for key in ("test_id", "id", "case_id"):
        if case.get(key):
            return str(case[key])
    return "case-{:05d}".format(index)


def _axis(case: dict, axis: str) -> str:
    return str(case.get(axis, "-"))


class Partition:
    """Two arms plus the evidence that the split did not distort the corpus."""

    def __init__(self, strategy: str, seed: int, arm_a: list, arm_b: list,
                 note: str = "") -> None:
        self.strategy = strategy
        self.seed = seed
        self.arm_a = arm_a
        self.arm_b = arm_b
        self.note = note
        self.balance = self._balance()

    def _balance(self) -> dict:
        """Marginal distribution per axis in each arm, plus the worst skew.

        A stratified split that quietly degenerates -- every case of some
        technique landing in one arm -- is invisible in the totals but obvious
        here, which is the point.
        """
        report = {}
        for axis in ("technique", "placement", "timing", "variant", "round"):
            keys = sorted({_axis(c, axis) for c in self.arm_a + self.arm_b})
            if keys == ["-"]:
                continue
            rows = {}
            worst = 0.0
            for key in keys:
                in_a = sum(1 for c in self.arm_a if _axis(c, axis) == key)
                in_b = sum(1 for c in self.arm_b if _axis(c, axis) == key)
                total = in_a + in_b
                share_a = (in_a / total * 100) if total else 0.0
                rows[key] = {"a": in_a, "b": in_b,
                             "a_share_pct": round(share_a, 1)}
                worst = max(worst, abs(share_a - 50.0))
            report[axis] = {"cells": rows, "max_skew_pct": round(worst, 1)}
        return report

    def degenerate(self) -> "list[str]":
        """Axes where one arm holds everything. Disjoint splits do this by
        design; for the balanced strategies it is a defect."""
        out = []
        for axis, data in self.balance.items():
            if data["max_skew_pct"] >= 50.0:
                out.append(axis)
        return out

    def as_dict(self) -> dict:
        return {"strategy": self.strategy, "seed": self.seed,
                "size_a": len(self.arm_a), "size_b": len(self.arm_b),
                "balance": self.balance, "degenerate_axes": self.degenerate(),
                "note": self.note}


# ------------------------------------------------------------- partitioners

def _split_random(cases: list, seed: int) -> tuple:
    a, b = [], []
    for index, case in enumerate(cases):
        target = a if _stable_bits(_case_id(case, index), seed) % 2 == 0 else b
        target.append(case)
    return a, b, "stable hash of case id, mod 2"


def _split_stratified(cases: list, seed: int) -> tuple:
    """Alternate within each (technique, placement) cell.

    Ordering inside a cell is by stable hash rather than input order, so the
    split does not inherit whatever sequence the ledger happened to be written
    in. Alternating guarantees the arms differ by at most one case per cell.
    """
    cells: "dict[tuple, list]" = {}
    for index, case in enumerate(cases):
        key = (_axis(case, "technique"), _axis(case, "placement"))
        cells.setdefault(key, []).append((_stable_bits(_case_id(case, index), seed), case))
    a, b = [], []
    for key in sorted(cells):
        ordered = [case for _, case in sorted(cells[key], key=lambda pair: pair[0])]
        for position, case in enumerate(ordered):
            (a if position % 2 == 0 else b).append(case)
    return a, b, "alternating within every (technique, placement) cell"


def _split_by_axis(cases: list, seed: int, axis: str) -> tuple:
    """Hold out half the values of one axis entirely.

    This is the strategy that detects a remedy which only fixes the exact
    techniques it was shown: arm B contains values arm A never saw.
    """
    values = sorted({_axis(c, axis) for c in cases})
    ordered = sorted(values, key=lambda v: _stable_bits(v, seed))
    half = len(ordered) // 2 or 1
    group_a = set(ordered[:half])
    a = [c for c in cases if _axis(c, axis) in group_a]
    b = [c for c in cases if _axis(c, axis) not in group_a]
    return a, b, "{} in A: {}".format(axis, ", ".join(sorted(group_a)) or "(none)")


def _split_temporal(cases: list, seed: int) -> tuple:
    """Early rounds derive, late rounds verify.

    Catches a remedy that only works on the round it was derived from, and
    drift in the configuration under test.
    """
    rounds = sorted({int(c.get("round", 0) or 0) for c in cases})
    if len(rounds) < 2:
        return list(cases), [], "only one round present; no temporal split possible"
    cut = rounds[len(rounds) // 2]
    a = [c for c in cases if int(c.get("round", 0) or 0) < cut]
    b = [c for c in cases if int(c.get("round", 0) or 0) >= cut]
    return a, b, "rounds < {} derive, >= {} verify".format(cut, cut)


def _split_variant_holdout(cases: list, seed: int) -> tuple:
    """Hold out one whole configuration: does the lesson transfer at all?"""
    variants = sorted({_axis(c, "variant") for c in cases})
    if len(variants) < 2:
        return list(cases), [], "only one variant present; nothing to hold out"
    held = min(variants, key=lambda v: _stable_bits(v, seed))
    a = [c for c in cases if _axis(c, "variant") != held]
    b = [c for c in cases if _axis(c, "variant") == held]
    return a, b, "variant {} held out".format(held)


_STRATEGIES = {
    "random_half": _split_random,
    "stratified_half": _split_stratified,
    "technique_disjoint": lambda cases, seed: _split_by_axis(cases, seed, "technique"),
    "placement_disjoint": lambda cases, seed: _split_by_axis(cases, seed, "placement"),
    "temporal_half": _split_temporal,
    "variant_holdout": _split_variant_holdout,
}


def partition(cases: list, strategy: str, cfg, seed: "int | None" = None) -> Partition:
    """Split a corpus into a derivation arm and a verification arm."""
    if strategy not in cfg.partition_strategies:
        raise ValueError("unknown strategy {!r}; declared strategies are {}"
                         .format(strategy, list(cfg.partition_strategies)))
    if strategy not in _STRATEGIES:
        raise ValueError("strategy {!r} is declared in config but not implemented"
                         .format(strategy))
    use_seed = cfg.split_seed if seed is None else int(seed)
    arm_a, arm_b, note = _STRATEGIES[strategy](list(cases), use_seed)
    return Partition(strategy, use_seed, arm_a, arm_b, note)


# ---------------------------------------------------------------- statistics

def _mean(values: list) -> float:
    return sum(float(v) for v in values) / len(values) if values else 0.0


def permutation_p(sample_a: list, sample_b: list, seed: int,
                  iterations: int = DEFAULT_ITERATIONS) -> float:
    """Two-sided permutation test on the difference of means.

    Chosen over a t-test because outcomes here are pass/fail indicators and
    bounded scores -- not normal, often skewed, sometimes tiny. A permutation
    test assumes only exchangeability under the null, which is exactly the
    claim being tested ("the arm a case landed in does not matter"), and it is
    exact rather than asymptotic, so it stays honest at the arm sizes this
    harness actually produces.

    Returns the fraction of relabellings whose |difference| reaches the
    observed one, with the standard +1 correction so a p-value is never zero.
    """
    if not sample_a or not sample_b:
        return 1.0
    observed = abs(_mean(sample_a) - _mean(sample_b))
    pooled = [float(v) for v in sample_a] + [float(v) for v in sample_b]
    cut = len(sample_a)
    rng = random.Random(seed)
    hits = 0
    for _ in range(iterations):
        rng.shuffle(pooled)
        if abs(_mean(pooled[:cut]) - _mean(pooled[cut:])) >= observed - 1e-12:
            hits += 1
    return (hits + 1) / (iterations + 1)


def bootstrap_ci(sample: list, seed: int, iterations: int = DEFAULT_ITERATIONS,
                 alpha: float = ALPHA) -> tuple:
    """Percentile bootstrap interval for the mean. Empty sample -> (0, 0)."""
    if not sample:
        return (0.0, 0.0)
    values = [float(v) for v in sample]
    rng = random.Random(seed)
    size = len(values)
    means = []
    for _ in range(iterations):
        means.append(_mean([values[rng.randrange(size)] for _ in range(size)]))
    means.sort()
    low = means[max(0, int(alpha / 2 * iterations) - 1)]
    high = means[min(iterations - 1, int((1 - alpha / 2) * iterations))]
    return (round(low * 100, 2), round(high * 100, 2))


class Effect:
    """The measured comparison between the two arms, in percentage points."""

    def __init__(self, arm_a: list, arm_b: list, cfg,
                 iterations: int = DEFAULT_ITERATIONS) -> None:
        self.n_a = len(arm_a)
        self.n_b = len(arm_b)
        self.mean_a_pct = round(_mean(arm_a) * 100, 2)
        self.mean_b_pct = round(_mean(arm_b) * 100, 2)
        self.delta_pct = round(self.mean_b_pct - self.mean_a_pct, 2)
        self.gap_pct = round(abs(self.delta_pct), 2)
        self.iterations = iterations
        self.p_value = round(permutation_p(arm_a, arm_b, cfg.split_seed, iterations), 4)
        self.ci_a = bootstrap_ci(arm_a, cfg.split_seed, iterations)
        self.ci_b = bootstrap_ci(arm_b, cfg.split_seed + 1, iterations)

    def as_dict(self) -> dict:
        return {"n_a": self.n_a, "n_b": self.n_b,
                "mean_a_pct": self.mean_a_pct, "mean_b_pct": self.mean_b_pct,
                "delta_pct": self.delta_pct, "gap_pct": self.gap_pct,
                "p_value": self.p_value, "ci_a_pct": list(self.ci_a),
                "ci_b_pct": list(self.ci_b), "iterations": self.iterations}


# ------------------------------------------------------------ decision table

def _rule_underpowered(eff: Effect, cfg) -> "str | None":
    if eff.n_a < cfg.min_arm_size or eff.n_b < cfg.min_arm_size:
        return ("arm sizes {}/{} below the floor of {}; too few observations to "
                "support any claim".format(eff.n_a, eff.n_b, cfg.min_arm_size))
    return None


def _rule_inflated(eff: Effect, cfg) -> "str | None":
    if eff.gap_pct > cfg.overfit_tolerance_pct and eff.mean_b_pct < eff.mean_a_pct:
        return ("verification arm is {} pp weaker than the derivation arm "
                "(tolerance {} pp); the result did not transfer"
                .format(eff.gap_pct, cfg.overfit_tolerance_pct))
    return None


def _rule_deflated(eff: Effect, cfg) -> "str | None":
    if eff.gap_pct > cfg.overfit_tolerance_pct and eff.mean_b_pct > eff.mean_a_pct:
        return ("verification arm is {} pp stronger than the derivation arm; "
                "the reported figure understates the effect".format(eff.gap_pct))
    return None


def _rule_unsound(eff: Effect, cfg) -> "str | None":
    if eff.p_value > ALPHA and eff.gap_pct > 0.0:
        return ("arms differ by {} pp but p={} exceeds {}; the difference is "
                "indistinguishable from chance".format(eff.gap_pct, eff.p_value, ALPHA))
    return None


# Evaluated in order; the first rule that fires decides. Order encodes
# precedence: power before effect, transfer before significance.
DECISION_TABLE = (
    ("underpowered", _rule_underpowered),
    ("inflated", _rule_inflated),
    ("deflated", _rule_deflated),
    ("unsound", _rule_unsound),
)


class Verdict:
    def __init__(self, kind: str, reason: str, effect: Effect,
                 partition_info: dict, corrected_estimate: "float | None" = None) -> None:
        self.kind = kind
        self.reason = reason
        self.effect = effect
        self.partition = partition_info
        self.corrected_estimate = corrected_estimate

    def as_dict(self) -> dict:
        return {"verdict": self.kind, "reason": self.reason,
                "corrected_estimate_pct": self.corrected_estimate,
                "effect": self.effect.as_dict(), "partition": self.partition}

    def __repr__(self) -> str:
        return "<Verdict {} gap={}pp p={}>".format(
            self.kind, self.effect.gap_pct, self.effect.p_value)


def verdict(effect: Effect, cfg, partition_info: "dict | None" = None) -> Verdict:
    """Apply the decision table. Unmatched means the claim survived."""
    for kind, rule in DECISION_TABLE:
        reason = rule(effect, cfg)
        if reason is not None:
            if kind not in cfg.verdict_kinds:
                raise ValueError("decision table produced {!r}, which is not a "
                                 "declared verdict kind".format(kind))
            corrected = effect.mean_b_pct if kind in ("inflated", "deflated") else None
            return Verdict(kind, reason, effect, partition_info or {}, corrected)
    return Verdict("confirmed",
                   "effect holds on the untouched verification arm "
                   "(gap {} pp within tolerance {} pp, p={})".format(
                       effect.gap_pct, cfg.overfit_tolerance_pct, effect.p_value),
                   effect, partition_info or {})


def evaluate(cases: list, outcome_of, cfg, strategy: "str | None" = None,
             seed: "int | None" = None,
             iterations: int = DEFAULT_ITERATIONS) -> Verdict:
    """Partition, measure, and rule on a claim in one call.

    `outcome_of` maps a case to a float in 0..1 (or a bool).
    """
    strat = strategy or cfg.default_partition_strategy
    split = partition(cases, strat, cfg, seed)
    eff = Effect([float(outcome_of(c)) for c in split.arm_a],
                 [float(outcome_of(c)) for c in split.arm_b], cfg, iterations)
    return verdict(eff, cfg, split.as_dict())
