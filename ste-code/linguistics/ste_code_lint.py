#!/usr/bin/env python3
"""STE-Code Linguistic Linter — reference implementation for FLAVOR-1.0.0.

Checks a document against the linguistic layer rules: semantic roles,
single referent, epistemic marking, quantifier precision, and register
conformance.

Usage:
    python3 ste_code_lint.py <document.md> [--flavor FLAVOR-1.0.0] [--json]

Output: line-by-line violations with rule references and suggested repairs.
"""

import json, re, sys
from pathlib import Path

LINGUISTICS_DIR = Path(__file__).resolve().parent
SEMANTICS = json.loads((LINGUISTICS_DIR / "semantics.json").read_text())
REGISTERS = json.loads((LINGUISTICS_DIR / "registers.json").read_text())


def load_document(path):
    """Read document and return list of (line_number, text) tuples."""
    lines = Path(path).read_text().split("\n")
    return [(i + 1, line) for i, line in enumerate(lines)]


# ── Step 1: Semantic Role Check ──────────────────────────────────
def check_semantic_roles(lines):
    """Check for Action terms used as nouns."""
    violations = []
    action_terms = SEMANTICS["semantic_roles"]["classes"]["Action"]["examples"]
    result_forms = {t: SEMANTICS["semantic_roles"]["term_table"].get(t, {}).get("result", "")
                    for t in action_terms}

    for lineno, text in lines:
        # Skip code blocks and comments
        if text.strip().startswith("```") or text.strip().startswith("#"):
            continue

        for action in action_terms:
            # Action as noun pattern: "the <action>" or "a <action>"
            pattern = re.compile(rf'\b(the|a|an)\s+{action}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                result = result_forms.get(action, "")
                repair = f"Replace '{match.group()}' with 'the {result}'" if result else "Restructure sentence"
                violations.append({
                    "line": lineno,
                    "rule": "SR",
                    "term": action,
                    "found": match.group(),
                    "repair": repair
                })
    return violations


# ── Step 2: Single Referent Rule ─────────────────────────────────
def check_single_referent(lines):
    """Check for unqualified collision terms and unresolved pronouns."""
    violations = []
    collisions = SEMANTICS["single_referent_rule"]["domain_collisions"]["entries"]

    for lineno, text in lines:
        if text.strip().startswith("```"):
            continue

        # Check for unqualified collision terms
        for term, data in collisions.items():
            pattern = re.compile(rf'\bthe\s+{term}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                # Is it qualified by any context qualifier?
                qualified = False
                for ctx in data["contexts"]:
                    if ctx["qualifier"].lower() in text.lower():
                        qualified = True
                        break
                if not qualified and len(data["contexts"]) > 1:
                    contexts = ", ".join(c["qualifier"] for c in data["contexts"])
                    violations.append({
                        "line": lineno,
                        "rule": "SRR",
                        "term": term,
                        "found": match.group(),
                        "repair": f"Qualify with one of: {contexts}"
                    })

        # Check for unresolved cross-sentence pronouns
        for pronoun in [" it ", " they ", " this ", " these ", " that ", " those "]:
            if pronoun in f" {text} ":
                # Simple heuristic: if pronoun appears without antecedent in same line
                # (A full implementation would track antecedents across sentences)
                pass  # Placeholder for full anaphora resolution

    return violations


# ── Step 4: Epistemic Marking ────────────────────────────────────
def check_epistemic(lines):
    """Check for bare performance claims and forbidden modals."""
    violations = []
    forbidden_modals = SEMANTICS["epistemic"]["forbidden_modals"]
    bare_adjectives = ["fast", "slow", "scalable", "reliable", "robust", "efficient",
                       "performant", "lightweight", "heavy", "responsive"]

    for lineno, text in lines:
        if text.strip().startswith("```"):
            continue

        # Check forbidden modals
        for modal in forbidden_modals:
            pattern = re.compile(rf'\b{modal}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                violations.append({
                    "line": lineno,
                    "rule": "EPI",
                    "term": modal,
                    "found": match.group(),
                    "repair": f"Replace '{modal}' with declarative present tense or 'is designed to'"
                })

        # Check bare performance adjectives
        for adj in bare_adjectives:
            pattern = re.compile(rf'\b(is|are|was|were)\s+{adj}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                # Check if followed by measurement within same sentence
                has_measurement = bool(re.search(r'\d+\s*(ms|s|rps|rpm|mb|gb|%)', text, re.IGNORECASE))
                has_expected = "designed to" in text.lower() or "expected to" in text.lower()
                if not has_measurement and not has_expected:
                    violations.append({
                        "line": lineno,
                        "rule": "EPI",
                        "term": adj,
                        "found": match.group(),
                        "repair": "Add measurement (with date) or mark as 'is designed to'"
                    })

    return violations


# ── Step 5: Quantifier Precision ─────────────────────────────────
def check_quantifiers(lines):
    """Check for vague quantifiers."""
    violations = []
    quant_table = SEMANTICS["quantifiers"]["table"]

    for lineno, text in lines:
        if text.strip().startswith("```"):
            continue

        for vague, data in quant_table.items():
            pattern = re.compile(rf'\b{vague}\b', re.IGNORECASE)
            for match in pattern.finditer(text):
                violations.append({
                    "line": lineno,
                    "rule": "QUANT",
                    "term": vague,
                    "found": match.group(),
                    "repair": f"Replace with: {data['replacement']}"
                })

    return violations


# ── Step 7: Register Check ───────────────────────────────────────
def check_register(lines, register="readme-prose"):
    """Check sentence length against register profile."""
    violations = []
    profile = REGISTERS["registers"].get(register, REGISTERS["registers"]["readme-prose"])
    max_words = profile.get("max_words", 25)

    # Simple sentence detection (splits on .!?)
    current_sentence = []
    current_line = 0

    for lineno, text in lines:
        if text.strip().startswith("```"):
            continue
        if not current_sentence:
            current_line = lineno
        current_sentence.append(text)

        if text.rstrip().endswith((".", "!", "?")):
            sentence = " ".join(current_sentence)
            words = len(sentence.split())
            if words > max_words:
                violations.append({
                    "line": current_line,
                    "rule": "REG",
                    "register": register,
                    "found": f"{words} words",
                    "limit": max_words,
                    "repair": f"Shorten to {max_words} words or split into multiple sentences"
                })
            current_sentence = []
            current_line = 0

    return violations


# ── Main ─────────────────────────────────────────────────────────
def main():
    if len(sys.argv) < 2:
        print("Usage: ste_code_lint.py <document.md> [--json]")
        sys.exit(1)

    doc_path = sys.argv[1]
    json_output = "--json" in sys.argv

    lines = load_document(doc_path)

    all_violations = []
    all_violations.extend(check_semantic_roles(lines))
    all_violations.extend(check_single_referent(lines))
    all_violations.extend(check_epistemic(lines))
    all_violations.extend(check_quantifiers(lines))
    all_violations.extend(check_register(lines))

    if json_output:
        print(json.dumps({
            "file": doc_path,
            "flavor": "FLAVOR-1.0.0",
            "total_violations": len(all_violations),
            "violations": all_violations
        }, indent=2))
    else:
        print(f"STE-Code Linguistic Linter — FLAVOR-1.0.0")
        print(f"File: {doc_path}")
        print(f"Violations: {len(all_violations)}")
        print()

        if not all_violations:
            print("  No violations found.")
        else:
            by_rule = {}
            for v in all_violations:
                by_rule.setdefault(v["rule"], []).append(v)

            for rule, violations in sorted(by_rule.items()):
                print(f"  [{rule}] {len(violations)} violation(s):")
                for v in violations[:5]:  # Show first 5 per rule
                    print(f"    Line {v['line']:>4}: {v.get('term', '')} — {v['repair']}")
                if len(violations) > 5:
                    print(f"    ... and {len(violations) - 5} more")
                print()


if __name__ == "__main__":
    main()
