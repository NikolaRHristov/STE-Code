#!/usr/bin/env python3
"""Dogfood audit: check our own docs against STE-Code standard.

Scans selected project files for common violations:
- Unapproved words (leverage, utilize, basically, etc.)
- Slang/jargon (stuff, kinda, gotta, etc.)
- Hedging (maybe, perhaps, basically, sort of)
- Passive voice patterns
- Contractions (don't, can't, won't, etc.)
- Long sentences (>25 words)
- Synonym drift (using multiple terms for same concept)
"""

import re
from pathlib import Path
from collections import Counter

PROJECT = Path(__file__).resolve().parent.parent.parent

# STE-Code synonym table — prefer these, avoid those
SYNONYMS = {
    "utilize": "use",
    "leverage": "use",
    "employ": "use",
    "initiate": "start",
    "commence": "start",
    "bootstrap": "start",
    "terminate": "stop",
    "halt": "stop",
    "kill": "stop",
    "display": "show",
    "render": "show",
    "present": "show",
    "create": "make",
    "generate": "make",
    "produce": "make",
    "retrieve": "get",
    "fetch": "get",
    "obtain": "get",
    "configure": "set",
    "assign": "set",
    "establish": "set",
    "verify": "check",
    "validate": "check",
    "ensure": "check",
    "perform": "do",
    "execute": "do",
    "carry out": "do",
    "transmit": "send",
    "dispatch": "send",
    "forward": "send",
    "delete": "remove",
    "eliminate": "remove",
    "purge": "remove",
    "retain": "keep",
    "preserve": "keep",
    "maintain": "keep",
    "demonstrate": "show",
    "facilitate": "help",
    "implement": "build",
    "require": "need",
    "additional": "more",
    "numerous": "many",
    "sufficient": "enough",
    "approximately": "about",
    "regarding": "about",
    "prior to": "before",
    "subsequent": "after",
    "in order to": "to",
    "due to the fact that": "because",
    "at this point in time": "now",
    "in the event that": "if",
}

# Slang/jargon/hedging to flag
BANNED_TERMS = [
    "stuff", "kinda", "sorta", "gotta", "wanna", "basically",
    "actually", "literally", "obviously", "clearly", "just",
    "really", "very", "quite", "rather", "somewhat",
    "maybe", "perhaps", "possibly", "probably", "generally",
    "essentially", "fundamentally", "inherently",
    "thing", "things", "stuff", "a lot", "lots of",
    "super", "mega", "ultra", "hyper",
]

# Passive voice indicators
PASSIVE_PATTERNS = [
    r"\bis (being |getting )?\w+ed\b",
    r"\bare (being |getting )?\w+ed\b",
    r"\bwas (being )?\w+ed\b",
    r"\bwere (being )?\w+ed\b",
    r"\bhas been \w+ed\b",
    r"\bhave been \w+ed\b",
    r"\bhad been \w+ed\b",
    r"\bwill be \w+ed\b",
]

CONTRACTIONS = [
    "don't", "can't", "won't", "isn't", "aren't", "wasn't",
    "weren't", "haven't", "hasn't", "hadn't", "shouldn't",
    "wouldn't", "couldn't", "mightn't", "mustn't",
    "it's", "that's", "there's", "here's", "what's",
    "let's", "who's", "he's", "she's", "we're", "they're",
    "I'm", "you're", "I've", "you've", "we've", "they've",
    "I'll", "you'll", "we'll", "they'll", "he'll", "she'll",
    "I'd", "you'd", "we'd", "they'd", "he'd", "she'd",
]

FILES_TO_AUDIT = [
    "README.md",
    ".agents/agent/agent-1-extractor.md",
    ".agents/agent/agent-6-phi-sce.md",
    ".agents/MASTER.md",
    ".agents/skills/refinement/SKILL.md",
    ".agents/feedback/exchange.md",
]


def audit_file(filepath):
    try:
        content = filepath.read_text()
    except:
        return None

    lines = content.split("\n")
    words = content.split()
    result = {
        "file": str(filepath.relative_to(PROJECT)),
        "words": len(words),
        "lines": len(lines),
        "violations": [],
        "score": 100.0,
    }

    # Check 1: Unapproved synonyms
    content_lower = content.lower()
    for bad, good in sorted(SYNONYMS.items()):
        pattern = r"\b" + re.escape(bad) + r"\b"
        matches = re.findall(pattern, content_lower)
        if matches:
            result["violations"].append({
                "type": "unapproved word",
                "detail": f"'{bad}' → use '{good}'",
                "count": len(matches),
                "severity": "warning",
            })

    # Check 2: Slang/jargon
    for term in BANNED_TERMS:
        pattern = r"\b" + re.escape(term) + r"\b"
        matches = re.findall(pattern, content_lower)
        if matches:
            result["violations"].append({
                "type": "slang/jargon/hedging",
                "detail": f"'{term}'",
                "count": len(matches),
                "severity": "warning",
            })

    # Check 3: Passive voice
    passive_count = 0
    for pat in PASSIVE_PATTERNS:
        passive_count += len(re.findall(pat, content_lower))
    if passive_count > 3:
        result["violations"].append({
            "type": "passive voice",
            "detail": f"{passive_count} passive constructions detected",
            "count": passive_count,
            "severity": "advisory",
        })

    # Check 4: Contractions
    contraction_count = 0
    for c in CONTRACTIONS:
        pattern = r"\b" + re.escape(c) + r"\b"
        contraction_count += len(re.findall(pattern, content_lower))
    if contraction_count > 0:
        result["violations"].append({
            "type": "contractions",
            "detail": f"{contraction_count} contraction(s) found",
            "count": contraction_count,
            "severity": "warning",
        })

    # Check 5: Long sentences (>25 words)
    long_sentences = 0
    for line in lines:
        stripped = line.strip()
        # Skip code blocks, headings, tables
        if stripped.startswith(("```", "#", "|", ">", "-", "*", "[")):
            continue
        if not stripped:
            continue
        wc = len(stripped.split())
        if wc > 25:
            long_sentences += 1
    if long_sentences > 2:
        result["violations"].append({
            "type": "long sentences",
            "detail": f"{long_sentences} sentences exceed 25 words",
            "count": long_sentences,
            "severity": "advisory",
        })

    # Calculate score
    penalty = 0
    warning_count = sum(1 for v in result["violations"] if v["severity"] == "warning")
    advisory_count = sum(1 for v in result["violations"] if v["severity"] == "advisory")
    penalty = warning_count * 5 + advisory_count * 2
    result["score"] = max(0, 100 - penalty)

    return result


def main():
    results = []
    for f in FILES_TO_AUDIT:
        path = PROJECT / f
        if not path.exists():
            print(f"SKIP: {f} (not found)")
            continue
        r = audit_file(path)
        if r:
            results.append(r)

    print("=" * 70)
    print("  STE-CODE DOGFOOD AUDIT — Our Docs vs Our Standard")
    print("=" * 70)
    print()

    total_score = 0
    for r in results:
        status = "✓" if r["score"] >= 90 else ("⚠" if r["score"] >= 70 else "✗")
        print(f"  {status} {r['file']}: {r['score']:.0f}/100 ({r['words']} words)")
        for v in r["violations"]:
            print(f"      [{v['severity']}] {v['type']}: {v['detail']} ({v['count']}×)")
        total_score += r["score"]
        print()

    avg = total_score / len(results) if results else 0
    print(f"  Average: {avg:.0f}/100 across {len(results)} files")
    print()

    # Top issues across all files
    all_violations = Counter()
    for r in results:
        for v in r["violations"]:
            all_violations[v["type"]] += v["count"]

    print("  Top violations project-wide:")
    for vtype, count in all_violations.most_common(5):
        print(f"    {vtype}: {count} occurrences")


if __name__ == "__main__":
    main()
