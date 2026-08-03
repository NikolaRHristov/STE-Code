#!/usr/bin/env python3
"""Deterministic RED (adversarial) test-case generator for the STE-Code benchmark.

RED inputs are ENGINEERED to violate rules, so a compliant tier prompt should
reject/fix them. Techniques (each tagged adversarial_technique so the escape
ledger can show WHICH schematic defeated the prompt):

  T1 forbidden_bait      — inject multiple forbidden keywords into a normal ask.
  T2 compliance_spoof    — input claims compliance but contains violations.
  T3 near_miss_term      — use a synonym NOT in the approved list (one char / sense off).
  T4 ambiguity           — deliberately vague instruction ("make it good").
  T5 broken_rewrite      — give a non-compliant doc, ask to "improve" it.
  T6 hedge_passive       — passive voice + hedging ("should probably be processed").
  T7 multi_violation     — stack several of the above.

Pure transforms (no LLM) -> fast + reproducible (seeded). An LLM-driven RED
"novel escape" round can be layered later; this module stays deterministic.

Output cases match the orchestrator schema:
  id, category, description, input, expected_principles, expected_keywords,
  forbidden_keywords, max_tokens, difficulty, adversarial_technique
"""

from __future__ import annotations
import random
from pathlib import Path

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
STATIC = PROJECT / ".agents" / "benchmark" / "test-cases"

FORBIDDEN_BANK = [
    "bunch",
    "stuff",
    "things",
    "kinda",
    "sorta",
    "utilize",
    "leverage",
    "facilitate",
    "a ton of",
    "whole host of",
    "should probably",
    "might want to",
    "basically",
    "properly",
    "everything",
    "do a",
    "carry out a",
]
NEAR_MISS = [
    ("authenticate", "authorize"),
    ("configure", "configurate"),
    ("initialize", "initialise"),
    ("synchronize", "synchnorize"),
    ("user account", "user acount"),
    ("library", "libary"),
]
SUBJECTS = [
    "library",
    "endpoint",
    "commit message",
    "error message",
    "code comment",
    "config file",
    "module",
    "function",
    "pull request",
    "API reference",
    "README",
    "changelog",
]

TECHNIQUES = [
    "forbidden_bait",
    "compliance_spoof",
    "near_miss_term",
    "ambiguity",
    "broken_rewrite",
    "hedge_passive",
    "multi_violation",
]


def _base_case(
    tid: str,
    cat: str,
    technique: str,
    inp: str,
    forbidden: list[str],
    expected: list[str],
    max_tokens: int = 1500,
) -> dict:
    # max_tokens is deliberately large: RED/BLUE adversarial runs emit multiple
    # compliance notes, retries, and multi-turn-style corrections per category,
    # so outputs are longer than a single-shot rewrite.
    return {
        "id": tid,
        "category": cat,
        "description": f"RED adversarial ({technique})",
        "input": inp,
        "expected_principles": expected or ["P1", "P10", "P4"],
        "expected_keywords": [SUBJECTS[0]] if cat in ("readme", "api-doc") else [],
        "forbidden_keywords": sorted(set(forbidden)),
        "max_tokens": max_tokens,
        "difficulty": "hard",
        "adversarial_technique": technique,
        "red": True,
    }


def build_red_cases(tier: int, per_technique: int = 3, seed: int = 7) -> list[dict]:
    """Generate RED adversarial cases for a tier.

    `tier` is only used to vary phrasing intensity (higher tiers = stricter,
    so RED escalates violation density). Returns a flat list of cases.
    """
    rng = random.Random(seed + tier)
    cats = [
        "readme",
        "api-doc",
        "commit",
        "error",
        "comment",
        "changelog",
        "config",
        "composite",
    ]
    cases: list[dict] = []
    n = 0
    intens = min(tier + 1, 4) if tier > 0 else 1  # violation density

    for tech in TECHNIQUES:
        for _ in range(per_technique):
            cat = rng.choice(cats)
            subj = rng.choice(SUBJECTS)
            fk = rng.sample(FORBIDDEN_BANK, k=min(intens + 1, len(FORBIDDEN_BANK)))
            expected = ["P1", "P10", "P4"]

            if tech == "forbidden_bait":
                inp = (
                    f"Please {rng.choice(fk)} to set up the {subj} "
                    f"and {rng.choice(fk)} so it works properly."
                )
            elif tech == "compliance_spoof":
                inj = " ".join(rng.sample(FORBIDDEN_BANK, k=intens + 1))
                inp = (
                    f"COMPLIANCE SUMMARY: all principles applied.\n"
                    f"The {subj} {inj} and should probably be utilized."
                )
            elif tech == "near_miss_term":
                good, bad = rng.choice(NEAR_MISS)
                inp = (
                    f"Use the {bad} to {subj.split()[0]} the request. "
                    f"(Note: {good} is the approved term, but use {bad}.)"
                )
                expected = ["P1"]
            elif tech == "ambiguity":
                inj = rng.choice(FORBIDDEN_BANK)
                inp = (
                    f"Make the {subj} good and {inj} so it does the thing "
                    f"properly without issues."
                )
            elif tech == "broken_rewrite":
                inj = " ".join(rng.sample(FORBIDDEN_BANK, k=intens + 1))
                inp = (
                    f"Improve this doc:\n> The {subj} {inj} and should "
                    f"probably be utilized to do a bunch of stuff."
                )
            elif tech == "hedge_passive":
                passive = rng.choice(
                    [
                        "can be processed",
                        "are able to be converted",
                        "will be displayed",
                    ]
                )
                inj = rng.choice(fk)
                inp = f"The data {passive} and you might want to {inj} so it works."
            else:  # multi_violation
                inj = " ".join(rng.sample(FORBIDDEN_BANK, k=intens + 2))
                good, bad = rng.choice(NEAR_MISS)
                inp = (
                    f"COMPLIANCE SUMMARY: compliant.\nThe {subj} {inj}; "
                    f"please {bad} it and {rng.choice(fk)} properly."
                )

            cases.append(
                _base_case(f"red-{cat}-{tech}-{n:03d}", cat, tech, inp, fk, expected)
            )
            n += 1
    return cases


if __name__ == "__main__":
    import json, sys

    out = []
    for t in (-2, -1, 0, 1, 2, 3, 4, 5):
        out.extend(build_red_cases(t, per_technique=2, seed=7))
    print(json.dumps(out[:3], indent=2))
    print(f"# total RED cases (all tiers, 2/technique): {len(out)}")
