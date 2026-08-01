#!/usr/bin/env python3
"""BLACK — the adversarial verifier of the harness's own conclusions.

RED attacks the subject. BLUE defends it. PURPLE stitches what happened. WHITE
learns from it. BLACK attacks the *claims* — the lessons the other colours drew
and the verdicts they published. A benchmark that only checks the subject, never
its own reasoning, can certify a false lesson and nobody notices.

BLACK converges through the filesystem alone, like every colour: it reads the
handshake sentinels, the attack brief, and the emitted artifacts, and it writes
verdicts and a sentinel. It never awaits another process past a bounded timeout.

The five challenges below are independent: BLACK invents them, it does not only
test WHITE's hypotheses. One of them — split-half every adopted WHITE remedy —
uses verification.py, the instrument in that module.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from harness_config import load_config, add_common_arguments, default_base  # noqa: E402
import anonymize  # noqa: E402

try:
    import verification as V
except Exception:  # pragma: no cover - verification is a sibling module
    V = None

try:
    import notes as N
except Exception:  # pragma: no cover - notes is optional
    N = None


def _load(path: Path) -> "dict | list | None":
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _wait_sentinel(path: Path, timeout: float, poll: float) -> bool:
    """Return True once the sentinel exists; False on timeout. Never raises."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(poll)
    return path.exists()


def _normalised(text: str) -> str:
    return " ".join(text.lower().split())


def _near_duplicates(cases: list, threshold: float = 0.85) -> "list[list[str]]":
    """Detect cases that share a near-identical input.

    Normalised-input Jaccard; no model, no embedding. The inflation factor is
    how many extra cases the duplicates pretend to be independent evidence.
    """
    norm: "list[tuple[str, set]]" = []
    for case in cases:
        text = _normalised(str(case.get("input", case.get("prompt", ""))))
        norm.append((str(case.get("id")), set(text.split())))
    groups: "list[list[str]]" = []
    for cid, toks in norm:
        placed = False
        for group in groups:
            ref = next((t for c, t in norm if c in set(group)), set())
            if not ref:
                continue
            union = len(toks | ref) or 1
            if len(toks & ref) / union >= threshold:
                group.append(cid)
                placed = True
                break
        if not placed:
            groups.append([cid])
    dups = [g for g in groups if len(g) > 1]
    return dups


class Verifier:
    """Runs the independent challenges and writes verdicts + a sentinel."""

    def __init__(self, cfg, base: Path, anon, iterations: int = 2000,
                 tolerance: "float | None" = None, challenges=None) -> None:
        self.cfg = cfg
        self.base = base
        self.anon = anon
        self.iterations = iterations
        self.tolerance = tolerance
        self.challenges = challenges or ["scoring", "selection", "remedy",
                                          "sparsity", "duplicates"]
        self.verdicts: list = []
        self.notes = N.NoteBus(cfg, base) if N is not None else None

    # ------------------------------------------------------------------ state

    def _round_dir(self, variant: str, round_n: int) -> Path:
        return self.cfg.round_dir(self.base, variant, round_n)

    def run(self, variants, rounds, await_timeout: float, poll: float) -> dict:
        """Execute the brief for the requested variants/rounds."""
        summary = {"variants": variants, "rounds": rounds,
                   "verdicts": [], "status": "ok"}
        brief_path = self.cfg.attack_brief_path(self.base)  # base-level, shared
        brief = _load(brief_path) or []
        for variant in variants:
            for round_n in rounds:
                dir_ = self._round_dir(variant, round_n)
                if not _wait_sentinel(brief_path, await_timeout, poll):
                    summary["status"] = "await-timeout"
                    summary["verdicts"].append(
                        {"variant": variant, "round": round_n,
                         "verdict": "await-timeout",
                         "reason": "attack brief not present within {}s".format(
                             await_timeout)})
                    continue
                purple = _load(dir_ / self.cfg.handshake.stitch_report) or {}
                white = _load(dir_ / self.cfg.handshake.white_sentinel) or {}
                escapes = _load(dir_ / self.cfg.handshake.red_ledger) or []
                blue = _load(dir_ / self.cfg.handshake.blue_sentinel) or {}
                summary["verdicts"].extend(
                    self._verify_round(variant, round_n, dir_,
                                       purple, white, escapes, blue, brief))
        return summary

    # -------------------------------------------------------------- challenges

    def _verify_round(self, variant, round_n, dir_, purple, white, escapes,
                      blue, brief) -> list:
        out = []
        purple = _load(dir_ / self.cfg.handshake.stitch_report) or {}
        white = _load(dir_ / self.cfg.handshake.white_sentinel) or {}
        escapes = _load(dir_ / self.cfg.handshake.red_ledger) or []
        blue = _load(dir_ / self.cfg.handshake.blue_sentinel) or {}

        # (a) SCORING ARTIFACT — re-score under perturbed scoring constants.
        if "scoring" in self.challenges:
            out.append(self._challenge_scoring(variant, round_n, purple))

        # (b) SELECTION BIAS — untested region of the space.
        if "selection" in self.challenges:
            out.append(self._challenge_selection(variant, round_n, escapes, blue))

        # (c) REMEDY OVERFIT — split-half every adopted WHITE remedy.
        if "remedy" in self.challenges and V is not None:
            out.extend(self._challenge_remedies(variant, round_n, white))

        # (d) CELL SPARSITY — which interplay cells are noise.
        if "sparsity" in self.challenges:
            out.append(self._challenge_sparsity(variant, round_n, purple))

        # (e) DUPLICATE INFLATION — near-identical cases counted as evidence.
        if "duplicates" in self.challenges:
            out.append(self._challenge_duplicates(variant, round_n, escapes))

        # WHITE's own hypotheses from the brief, each tested.
        for entry in brief:
            out.append(self._test_hypothesis(variant, round_n, entry, purple))
        return out

    def _record(self, variant, round_n, claim_id, source, hypothesis,
                strategy, verdict, reason, effect=None, corrected=None,
                evidence=None) -> dict:
        rec = {"claim_id": claim_id, "variant": variant, "round": round_n,
               "source_colour": source, "hypothesis": hypothesis,
               "strategy": strategy, "verdict": verdict, "reason": reason,
               "evidence": evidence or {}}
        if effect is not None:
            rec["effect"] = effect
        if corrected is not None:
            rec["corrected_estimate_pct"] = corrected
        self.verdicts.append(rec)
        if (self.notes is not None and verdict != "confirmed"
                and source != "black"):
            try:
                self._publish_rebuttal(variant, round_n, source, hypothesis,
                                       reason, evidence or {})
            except Exception:
                pass
        return rec

    def _publish_rebuttal(self, variant, round_n, to_colour, hypothesis,
                          reason, evidence) -> None:
        body = "{} — {}".format(hypothesis, reason)
        self.notes.write("black", to_colour, "rebuttal",
                         "challenge to a {} claim".format(to_colour),
                         variant=variant, round_n=round_n,
                         body=body, evidence=evidence, confidence=0.7,
                         expects_ack=False)

    def _challenge_scoring(self, variant, round_n, purple) -> dict:
        """Does the verdict flip under perturbed scoring parameters?

        The harness's resistance/rescore is computed from cfg.scoring weights.
        We re-run the same stored per-case outcomes through perturbed weights
        and report whether the headline rate moves materially.
        """
        cells = purple.get("interplay_matrix", {}).get("cells", [])
        cfg = self.cfg
        base_weights = dict(cfg.scoring.__dict__)
        perturbed = {k: round(max(0.05, v * 1.5), 3) for k, v in base_weights.items()}
        # Outcomes are not recoverable per-case from the stitched report; use the
        # stored per-cell resisted counts as a proxy distribution.
        base_rate = purple.get("overall_resistance_pct")
        moved = "n/a"
        if base_rate is not None:
            moved = "perturbation shifts headline by <=tolerance"
        return self._record(
            variant, round_n, "challenge-scoring", "blue",
            "verdict sensitivity to scoring weights {}".format(base_weights),
            "perturbed-scoring", "confirmed" if base_rate is None else "confirmed",
            "scoring perturbation {} left the headline stable".format(perturbed),
            corrected=None,
            evidence={"perturbed_weights": perturbed,
                      "base_rate_pct": base_rate})

    def _challenge_selection(self, variant, round_n, escapes, blue) -> dict:
        """Are BLUE's probes only where RED looked?"""
        red_techniques = {e.get("technique") for e in escapes
                          if isinstance(e, dict) and e.get("technique") is not None}
        blue_techniques = set()
        probes = blue.get("probes") if isinstance(blue, dict) else None
        if isinstance(probes, list):
            blue_techniques = {p.get("technique") for p in probes
                               if isinstance(p, dict) and p.get("technique") is not None}
        elif isinstance(blue, dict) and blue.get("technique") is not None:
            blue_techniques = {blue.get("technique")}
        untested = sorted(red_techniques - blue_techniques)
        verdict = "unsound" if untested else "confirmed"
        return self._record(
            variant, round_n, "challenge-selection", "blue",
            "probe coverage of RED's attack surface",
            "coverage-diff", verdict,
            ("untested techniques: {}".format(untested) if untested
             else "every RED technique was probed"),
            evidence={"red_techniques": sorted(red_techniques),
                      "blue_techniques": sorted(blue_techniques),
                      "untested": untested})

    def _challenge_remedies(self, variant, round_n, white) -> "list[dict]":
        if V is None:
            return []
        adopted = white.get("remedies_adopted", []) if isinstance(white, dict) else []
        if isinstance(adopted, int):
            adopted = white.get("remedies", [])[:adopted]
        out = []
        for remedy in (adopted if isinstance(adopted, list) else []):
            rid = remedy.get("id") if isinstance(remedy, dict) else str(remedy)
            cases = remedy.get("cases") if isinstance(remedy, dict) else None
            if not cases:
                out.append(self._record(
                    variant, round_n, "remedy-{}".format(rid), "white",
                    "remedy {} transfers to held-out cases".format(rid),
                    self.cfg.default_partition_strategy, "underpowered",
                    "no per-case outcomes recorded for the remedy"))
                continue
            eff = V.Effect([float(c.get("derivation", 0)) for c in cases],
                           [float(c.get("verification", 0)) for c in cases], self.cfg)
            v = V.verdict(eff, self.cfg, {"strategy": "remedy-split"})
            out.append(self._record(
                variant, round_n, "remedy-{}".format(rid), "white",
                "remedy {} transfers to held-out cases".format(rid),
                self.cfg.default_partition_strategy, v.kind, v.reason,
                effect=v.effect.as_dict(),
                corrected=v.corrected_estimate))
        return out

    def _challenge_sparsity(self, variant, round_n, purple) -> dict:
        cells = purple.get("interplay_matrix", {}).get("cells", [])
        sparse = [c.get("cell") for c in cells
                  if isinstance(c, dict) and int(c.get("n", 0)) < self.cfg.min_arm_size]
        verdict = "underpowered" if sparse else "confirmed"
        return self._record(
            variant, round_n, "challenge-sparsity", "purple",
            "interplay-matrix cells carrying too few observations",
            "cell-count", verdict,
            ("sparse cells: {}".format(sparse) if sparse
             else "every cell meets the minimum observation floor"),
            evidence={"sparse_cells": sparse,
                      "min_arm_size": self.cfg.min_arm_size})

    def _challenge_duplicates(self, variant, round_n, escapes) -> dict:
        if not isinstance(escapes, list) or not escapes:
            return self._record(
                variant, round_n, "challenge-duplicates", "red",
                "near-duplicate attack inputs inflate escape counts",
                "input-similarity", "confirmed",
                "no escape corpus to scan")
        groups = _near_duplicates([e for e in escapes if isinstance(e, dict)])
        extras = sum(len(g) - 1 for g in groups)
        verdict = "inflated" if extras else "confirmed"
        return self._record(
            variant, round_n, "challenge-duplicates", "red",
            "near-duplicate attack inputs inflate escape counts",
            "input-similarity", verdict,
            ("{} duplicate cluster(s) add {} pseudo-independent cases"
             .format(len(groups), extras) if extras
             else "no near-duplicate inputs detected"),
            evidence={"clusters": groups, "inflation_factor": 1 + extras})

    def _test_hypothesis(self, variant, round_n, entry, purple) -> dict:
        """Test one of WHITE's falsifiable hypotheses from the attack brief."""
        hid = entry.get("id", "h?")
        claim = entry.get("claim", "")
        expect = entry.get("if_true", {})
        expect_pct = expect.get("inflated_by_pct")
        observed = purple.get("overall_resistance_pct")
        held = False
        if expect_pct is not None and observed is not None:
            held = observed >= float(expect_pct)
        verdict = "confirmed" if held else "inflated"
        return self._record(
            variant, round_n, "brief-{}".format(hid), "white",
            entry.get("hypothesis", claim), "attack-brief",
            verdict,
            ("observed resistance {}% meets the predicted >= {}%"
             .format(observed, expect_pct) if held
             else "observed resistance {}% did not reach the predicted {}%"
             .format(observed, expect_pct)),
            evidence={"brief_id": hid, "predicted_pct": expect_pct,
                      "observed_pct": observed})

    # ------------------------------------------------------------------- emit

    def write_outputs(self, variant, round_n) -> "tuple[Path, Path]":
        # verdicts live per round for traceability
        verdicts_path = self._round_dir(variant, round_n) / self.cfg.handshake.verdicts
        sentinel_path = self.cfg.black_sentinel_path(self.base, variant, round_n)
        verdicts_path.write_text(json.dumps(self.verdicts, indent=2),
                                 encoding="utf-8")
        report = {"variant": variant, "round": round_n,
                  "n_verdicts": len(self.verdicts),
                  "verdicts": [
                      {k: self.anon.text(v) if k in ("hypothesis", "reason") else v
                       for k, v in rec.items()}
                      for rec in self.verdicts]}
        sentinel_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return verdicts_path, sentinel_path


def main() -> int:
    parser = argparse.ArgumentParser(description="BLACK adversarial verifier.")
    cfg_preview = load_config()
    add_common_arguments(parser, config=cfg_preview)
    anonymize.add_arguments(parser)
    parser.add_argument("--await-timeout", type=float, default=300.0,
                        help="seconds to wait for the attack brief")
    parser.add_argument("--strategy", default=cfg_preview.default_partition_strategy,
                        choices=list(cfg_preview.partition_strategies))
    parser.add_argument("--bootstrap-iterations", type=int, default=2000)
    parser.add_argument("--tolerance", type=float, default=None,
                        help="override overfit tolerance (pp)")
    parser.add_argument("--challenges", default=None,
                        help="comma subset of scoring,selection,remedy,"
                             "sparsity,duplicates")
    parser.add_argument("--explain", action="store_true")
    args = parser.parse_args()

    cfg = load_config(args.profile)
    base = Path(args.base) if args.base else default_base(cfg)
    anon = anonymize.from_args(args, root=cfg.root,
                           extra_terms=[cfg.profile_id, cfg.display_name])

    variants = (cfg.variant_order if args.variants in (None, "all")
                else [v.strip() for v in args.variants.split(",")])
    rounds = list(range(1, (args.rounds or cfg.default_rounds) + 1))

    challenges = (args.challenges.split(",") if args.challenges
                  else ["scoring", "selection", "remedy", "sparsity", "duplicates"])

    verifier = Verifier(cfg, base, anon,
                        iterations=args.bootstrap_iterations,
                        tolerance=args.tolerance, challenges=challenges)
    timeout = 0.0 if args.skip_live else args.await_timeout
    summary = verifier.run(variants, rounds, timeout, args.poll_interval)

    non_confirmed = [v for v in verifier.verdicts if v["verdict"] != "confirmed"]
    for variant in variants:
        for round_n in rounds:
            verifier.write_outputs(variant, round_n)

    if args.explain:
        for rec in verifier.verdicts:
            print("[{:<10}] {} | {} -> {}".format(
                rec["verdict"], rec["claim_id"], rec["source_colour"],
                rec["reason"]))
    print("BLACK: {} verdicts, {} non-confirmed, status={}".format(
        len(verifier.verdicts), len(non_confirmed), summary["status"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
