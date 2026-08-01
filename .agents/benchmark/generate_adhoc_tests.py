#!/usr/bin/env python3
"""Generate AD-HOC benchmark test cases pre-run.

The static suite (test-cases/category-*.json, 59 cases) is fixed. To stress
every tier with FRESH inputs each run, this script generates variant cases
deterministically (seeded) from the static suite plus a small templated
corpus of realistic code-documentation snippets with injected STE-Code
violations. Output is written as category-adhoc-*.json into --out-dir so the
orchestrator can consume it via --test-dir.

Why ad-hoc generation: it exercises the rules on inputs not seen during the
static-suite design, catching overfitting and surfacing how each tier behaves
on novel jargon-heavy prose.

Generation strategy (deterministic, seeded):
  1. VARIANT-per-static: for each static case, emit 1-2 "rephrase" variants
     whose `input` is recomposed from a violation phrase bank (swaps in fresh
     slang/jargon/hedging + a different code-domain noun), while keeping the
     same expected_principles / forbidden_keywords so scoring is still valid.
  2. TEMPLATED: synthesize snippets from a category x phrase-bank matrix so
     every one of the 14 categories gets at least a couple of novel inputs.

Usage:
  python3 generate_adhoc_tests.py --out-dir .agents/benchmark/test-cases-adhoc
  python3 generate_adhoc_tests.py --out-dir DIR --seed 7 --per-static 2
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = PROJECT / ".agents" / "benchmark" / "test-cases"

# Violation phrase bank: jargon / hedging / passive / noun-as-verb to inject.
SLANG = ["a bunch of", "a ton of", "stuff", "things", "kinda", "sorta",
         "utilizes", "leverages", "orchestrates", "facilitates", "a whole host of"]
HEDGE = ["should probably", "might want to", "ideally", "generally", "basically",
         "for the most part", "more or less", "you may wish to"]
PASSIVE = ["can be processed", "are able to be converted", "will be displayed",
           "gets handled", "is being done", "was performed", "gets executed"]
NOUN_AS_VERB = ["Docker the application", "Kubernetes the deployment",
                "plugin the build", "containerize the service", "cache the result",
                "queue the message", "tokenize the input"]
WEAK_VERB = ["does", "makes", "handles", "does a", "performs a", "carries out a"]

# Per-category realistic code-domain noun to vary the input subject.
SUBJECTS = {
    "readme": "library", "api-doc": "endpoint", "commit": "commit message",
    "error": "error message", "comment": "code comment", "changelog": "changelog",
    "config": "config file", "composite": "module", "gen-function": "function",
    "gen-pr-review": "pull request", "gen-api-doc": "API reference",
    "gen-commit": "commit", "gen-error": "exception", "gen-readme": "README",
}

CATEGORIES = list(SUBJECTS.keys())


def _rephrase(static_case: dict, rng: random.Random, idx: int) -> dict:
    """Produce one variant of a static case with a fresh violating input."""
    cat = static_case.get("category", "readme")
    subject = SUBJECTS.get(cat, "component")
    slang = rng.choice(SLANG)
    hedge = rng.choice(HEDGE)
    weak = rng.choice(WEAK_VERB)
    passive = rng.choice(PASSIVE)
    nounverb = rng.choice(NOUN_AS_VERB)

    variants = [
        f"This {subject} {slang} and {hedge} {weak} everything set up properly.",
        f"Features include: data {passive} quickly, files {passive}, and results show in real-time.",
        f"To use the {subject}, first {nounverb} then run the setup script which configures everything for you.",
        f"The {subject} {weak} a bunch of stuff and should be called with the user object to get it all working.",
    ]
    new_input = rng.choice(variants)

    return {
        "id": f"adhoc-{cat}-{idx:03d}",
        "category": cat,
        "description": f"ad-hoc variant of {static_case.get('id')} (generated)",
        "input": new_input,
        "expected_principles": static_case.get("expected_principles", []),
        "expected_keywords": static_case.get("expected_keywords", []),
        # Flatten static forbidden keywords (may include multi-word phrases as lists).
        "forbidden_keywords": sorted(set(
            [w for kw in static_case.get("forbidden_keywords", [])
             for w in (kw if isinstance(kw, list) else [kw])
             if isinstance(w, str)] +
            [w for w in (slang.split(), hedge.split(), nounverb.split()) if w]
        )),
        "max_tokens": static_case.get("max_tokens", 300),
        "difficulty": static_case.get("difficulty", "medium"),
        "generated": True,
    }


def _templated(rng: random.Random, idx: int) -> list[dict]:
    """Synthesize novel inputs per category from the phrase bank."""
    out = []
    for cat in CATEGORIES:
        subject = SUBJECTS[cat]
        for k in range(2):
            slang = rng.choice(SLANG)
            hedge = rng.choice(HEDGE)
            passive = rng.choice(PASSIVE)
            new_input = (
                f"The {subject} {slang}. It {hedge} {rng.choice(WEAK_VERB)} the "
                f"work done, and the output {passive} automatically."
            )
            out.append({
                "id": f"adhoc-tpl-{cat}-{idx:03d}-{k}",
                "category": cat,
                "description": f"ad-hoc templated {cat} snippet (generated)",
                "input": new_input,
                "expected_principles": ["P1", "P10", "P4"],
                "expected_keywords": [subject],
                "forbidden_keywords": sorted(set(
                    slang.split() + hedge.split() + passive.split())),
                "max_tokens": 300,
                "difficulty": "medium",
                "generated": True,
            })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(PROJECT / ".agents" / "benchmark" / "test-cases-adhoc"))
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--per-static", type=int, default=2,
                    help="variants generated per static case")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Clear any previous adhoc output.
    for f in out_dir.glob("category-adhoc-*.json"):
        f.unlink()

    static_files = sorted(STATIC_DIR.glob("category-*.json"))
    idx = 0
    total = 0
    by_cat: dict[str, list] = {}
    for sf in static_files:
        cases = json.load(open(sf))
        for case in cases:
            for _ in range(args.per_static):
                v = _rephrase(case, rng, idx)
                by_cat.setdefault(v["category"], []).append(v)
                idx += 1
                total += 1

    # Templated novelty across all 14 categories.
    for t in _templated(rng, idx):
        by_cat.setdefault(t["category"], []).append(t)
        total += 1

    # Write one category-adhoc-<cat>.json per category (mirrors static layout).
    for cat, cases in by_cat.items():
        (out_dir / f"category-adhoc-{cat}.json").write_text(
            json.dumps(cases, indent=2), encoding="utf-8")

    print(f"Generated {total} ad-hoc cases across {len(by_cat)} categories "
          f"-> {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
