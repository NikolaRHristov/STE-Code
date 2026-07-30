#!/usr/bin/env python3
"""Shared benchmark scoring library — single source of truth for extraction,
principle keywords, and scoring logic used by orchestrator.py, rescore.py,
and orchestrator-control.py.

Rationale:
  All three scripts need identical extraction and scoring logic to produce
  comparable results. Duplication caused divergence in PRINCIPLE_KEYWORDS
  and extraction regexes across files. This library eliminates that.
"""

import json
import os
import re
from typing import Dict, List, Optional, Tuple

# =============================================================================
# Canonical principle-to-keyword mapping.
# =============================================================================
# Each principle maps to a list of term stems that, when found in the
# output or compliance section, indicate the worker discussed that principle.
#
# NOTE: This is a heuristic. Keyword presence does NOT guarantee real
# compliance — the worker might just mention "passive voice" while still
# using it. True compliance measurement requires an LLM-as-judge step.
# These keywords are designed to catch explicit discussion of each
# principle, which is the primary signal in this benchmark.
#
# CANONICAL SOURCE: this file (benchmark_lib.py).
# orchestrator.py, rescore.py, and orchestrator-control.py all import
# PRINCIPLE_KEYWORDS from here. Update here only.
PRINCIPLE_KEYWORDS: Dict[str, List[str]] = {
    "P1":  ["approved word", "dictionary", "approved term", "approved vocabulary"],
    "P2":  ["part of speech", "noun", "verb", "adjective", "adverb", "preposition", "conjunction"],
    "P3":  ["approved meaning", "meaning", "definition", "defined sense", "single meaning"],
    "P4":  ["active voice", "passive voice", "imperative", "infinitive", "simple present", "simple past", "past participle"],
    "P5":  ["technical noun", "keyword", "framework", "library", "class name", "function name", "variable name"],
    "P6":  ["non-approved", "technical name", "technical term", "unapproved"],
    "P7":  ["noun as verb", "do not use noun as verb", "nominalization", "verbing"],
    "P8":  ["standard", "well-known", "recognized", "established term"],
    "P9":  ["short", "clear", "concise", "brief", "simple word"],
    "P10": ["slang", "jargon", "regional", "vague", "informal", "colloquial", "idiom"],
    "P11": ["one term", "consistent", "same term", "synonym", "do not use synonyms"],
    "P12": ["technical verb", "build", "deploy", "test", "lint", "compile", "debug", "install", "configure", "execute"],
    "P13": ["verb as noun", "do not use verb as noun", "gerund as noun"],
    "P14": ["american spelling", "american english", "color", "analyze", "organize", "standardize"],
}


# =============================================================================
# Path resolution
# =============================================================================

def resolve_project_root() -> str:
    """Return the absolute project root (two levels above this file)."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def resolve_path(cli_val: Optional[str], default_rel: str) -> str:
    """Return CLI override, or compute the default relative to the project root."""
    if cli_val is not None:
        return os.path.abspath(cli_val)
    return os.path.join(resolve_project_root(), default_rel)


# =============================================================================
# Text extraction functions
# =============================================================================

def extract_corrected_text(output: str) -> str:
    """Extract corrected text from worker output — handle multiple formats.

    Tries a series of known marker patterns.  Falls back to stripping the
    entire output when no marker is recognised.
    """
    markers: List[str] = [
        r'\*\*Corrected Text:\*\*',
        r'## Corrected Text',
        r'CORRECTED TEXT',
        r'# Corrected Text',
        r'Corrected Text \(STE-Code Compliant\)',
        r'# STE-Code Corrected Text',
    ]
    # Boundary patterns that end the corrected-text block.
    boundaries = r'(?:\n---\n|\n## Compliance|\n# Compliance|\nCOMPLIANCE|\n\*\*Compliance)'

    for marker in markers:
        m = re.search(
            marker + r'\s*\n+(.*?)' + boundaries,
            output, re.DOTALL | re.IGNORECASE,
        )
        if m and m.group(1).strip():
            return m.group(1).strip()

    # Fallback: everything before the first Compliance heading.
    m = re.search(
        r'^(.*?)(?:\n---\n|\n#+\s*Compliance|\nCOMPLIANCE)',
        output, re.DOTALL | re.IGNORECASE,
    )
    if m:
        text = m.group(1).strip()
        text = re.sub(
            r'^#+\s*(?:Corrected|STE-Code).*?\n+',
            '', text, flags=re.IGNORECASE,
        )
        if text:
            return text.strip()

    return output.strip()


def extract_compliance_section(output: str) -> str:
    """Extract compliance summary section from worker output."""
    markers = [
        "**Compliance Summary**",
        "## Compliance Summary",
        "COMPLIANCE SUMMARY",
        "# Compliance Summary",
        "Compliance Summary",
    ]
    for marker in markers:
        escaped = re.escape(marker)
        m = re.search(escaped + r'\s*\n(.*)', output, re.DOTALL | re.IGNORECASE)
        if m and m.group(1).strip():
    """Extract compliance summary section from worker output.

    Attempts several known heading markers in priority order.
    Returns empty string when no compliance section is found.

    All markers use the same capture-group branch: match the heading,
    then capture everything after it.  Bold markers (** **) are handled
    by stripping bold syntax from the output before matching so the
    same regex path applies uniformly.
    """
    # Normalise bold markdown headings to plain text for matching.
    # e.g. "**Compliance Summary**" -> "Compliance Summary"
    normalised = re.sub(r'\*\*([^*]+)\*\*', r'\1', output)

    markers: List[str] = [
        r'## Compliance Summary',
        r'COMPLIANCE SUMMARY',
        r'# Compliance Summary',
        r'Compliance Summary',
    ]
    for marker in markers:
        m = re.search(
            marker + r'\s*\n(.*)',
            normalised, re.DOTALL | re.IGNORECASE,
        )
        if m:
            return m.group(1).strip()
    return ""


# =============================================================================
# Scoring functions
# =============================================================================

def check_principles(
    output: str, expected_principles: List[str],
) -> Tuple[List[str], List[str]]:
    """Check which expected principles are satisfied.

    Searches in BOTH the compliance section AND the full output for
    principle numbers and associated keywords.

    Returns (satisfied, missed) lists.
    """
    compliance = extract_compliance_section(output)
    full_lower = (compliance + " " + output).lower()

    satisfied: List[str] = []
    missed: List[str] = []

    for p in expected_principles:
        found = False
        # 1. Explicit principle number mention in compliance.
        if re.search(r'\b' + re.escape(p) + r'\b', compliance):
            found = True
        # 2. Keyword heuristics.
        if not found and p in PRINCIPLE_KEYWORDS:
            for kw in PRINCIPLE_KEYWORDS[p]:
                if kw.lower() in full_lower:
                    found = True
                    break
        # 3. Also check full output for principle number.
        if not found and re.search(r'\b' + re.escape(p) + r'\b', output):
            found = True

        if found:
            satisfied.append(p)
        else:
            missed.append(p)

    return satisfied, missed


def check_keywords(text_lower: str, keywords: List[str]) -> List[str]:
    """Return the subset of *keywords* found (case-insensitive) in *text_lower*."""
    return [kw for kw in keywords if kw.lower() in text_lower]


def calc_correctness(
    expected_principles: List[str],
    satisfied: List[str],
    forbidden_found: List[str],
    total_forbidden: int,
    expected_kw_found: List[str],
    total_expected_kw: int,
) -> float:
    """Calculate correctness score 0–1 using the weighted formula.

    Weight design rationale:
      base        = 0.4   Floor: even a non-compliant answer is worth 0.4.
                           This distinguishes "wrong" from "no answer at all".
      principles  = 0.6   Primary signal. 60 % of score comes from covering
                           expected principles.
      forbidden   =-0.3   Maximum penalty for forbidden keywords. Capped so
                           one bad word cannot zero out an otherwise good
                           response.  Skipped when total_forbidden == 0.
      expected    =+0.1   Small bonus for using approved vocabulary.
                           Deliberately low because a worker may choose
                           different but equally valid terms.
    """
    score = 0.4  # base

    if expected_principles:
        score += 0.6 * len(satisfied) / len(expected_principles)

    if total_forbidden > 0:
        score -= 0.3 * len(forbidden_found) / total_forbidden

    if total_expected_kw > 0:
        score += 0.1 * len(expected_kw_found) / total_expected_kw

    return round(max(0.0, min(1.0, score)), 2)


# =============================================================================
# Aggregate helpers
# =============================================================================

def build_recommendations(
    avg_correctness: float,
    avg_latency_ms: float,
    category_scores: Dict[str, float],
    total_tests: int,
    retry_count: int = 0,
    timed_out_count: int = 0,
    truncated_count: int = 0,
) -> List[str]:
    """Build a list of actionable recommendations from aggregate metrics.

    Recommendations are rule-based and cover quality, latency, category
    underperformance, and infrastructure issues.
    """
    recs: List[str] = []

    if avg_correctness < 0.7:
        recs.append(
            "System prompt needs improvement — avg correctness below 0.7"
        )
    if avg_latency_ms > 5000:
        recs.append(
            "Latency above 5 s average — consider a flash model for simple cases"
        )
    for cat, score in sorted(category_scores.items()):
        if score < 0.6:
            recs.append(
                f"Category '{cat}' underperforming (avg {score:.3f}) — review test design or prompt coverage"
            )

    if retry_count > total_tests * 0.3:
        recs.append(
            f"High retry rate ({retry_count} retries across {total_tests} tests) — check API reliability or increase timeout"
        )
    if timed_out_count > total_tests * 0.1:
        recs.append(
            f"{timed_out_count} workers timed out — increase timeout or reduce concurrency to avoid API congestion"
        )
    if truncated_count > 0:
        recs.append(
            f"{truncated_count} truncated outputs detected — these workers likely crashed or timed out"
        )

    return recs


# =============================================================================
# I/O helpers
# =============================================================================

def load_test_cases(test_dir: str) -> Dict[str, dict]:
    """Load all test cases from category-*.json files in *test_dir*.

    Returns a dict mapping test_id -> test_case (with _file field added).
    """
    import glob as _glob

    test_map: Dict[str, dict] = {}
    cat_files = sorted(_glob.glob(os.path.join(test_dir, "category-*.json")))
    if not cat_files:
        raise FileNotFoundError(
            f"No category-*.json files found in {test_dir}"
        )
    for cat_file in cat_files:
        with open(cat_file) as f:
            for t in json.load(f):
                t["_file"] = cat_file
                test_map[t["id"]] = t
    return test_map


def load_previous_results(run_dir: str) -> Optional[Dict[str, dict]]:
    """Load per-test-results.json from *run_dir* if it exists.

    Returns a dict mapping test_id -> previous result dict, or None.
    """
    prev_file = os.path.join(run_dir, "per-test-results.json")
    if not os.path.isfile(prev_file):
        return None
    with open(prev_file) as f:
        raw = json.load(f)
    return {r["test_id"]: r for r in raw}
