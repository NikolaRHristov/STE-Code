#!/usr/bin/env python3
"""Extract approved verbs and adjectives from STE-Code adapted dictionary and rule files."""

import re
import json
from pathlib import Path

BASE = Path("/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code")
DICT_PATH = BASE / "adapted" / "a-dictionary.md"
RULES_DIR = BASE / "adapted"
OUT_DIR = BASE / "data" / "vocabulary"
OUT_VERBS = OUT_DIR / "approved-verbs.json"
OUT_ADJ = OUT_DIR / "approved-adjectives.json"

def parse_dictionary(path):
    """Parse a-dictionary.md into list of approved entries."""
    text = path.read_text(encoding="utf-8")
    entries = []
    
    # Each entry starts with "## WORD (pos)" possibly followed by "- UNNAPROVED" or "- (retained..."
    # Pattern matches: ## WORD (pos) [optional suffix]
    # We split by the "## " header markers
    sections = re.split(r'\n(?=## [A-Z])', text)
    
    for section in sections:
        # Extract header
        header_match = re.match(r'^## ([A-Z]+(?:-[A-Z]+)*) \(([a-z]+)\)(?:\s*-\s*(.+))?', section)
        if not header_match:
            header_match = re.match(r'^## ([A-Z]+) \(([a-z]+)\)(?:\s*-\s*(.+))?', section)
        if not header_match:
            continue
        
        word = header_match.group(1).lower()
        pos = header_match.group(2)
        suffix = header_match.group(3) or ""
        
        # Skip unapproved entries
        if "UNNAPROVED" in suffix.upper():
            continue
        # Skip entries that are retained but not adapted for code domain
        section_lower = section.lower()
        if "retained" in section_lower or "not applicable" in section_lower:
            if "not applicable to code" in section_lower or "not adapted" in section_lower:
                continue
            if "not commonly applicable" in section_lower:
                continue
            if "limited code-documentation" in section_lower:
                continue
        # Skip articles, prepositions, conjunctions, adverbs, pronouns
        if pos not in ("v", "adj", "verb", "adjective"):
            continue
        
        # Normalize pos
        if pos in ("v", "verb"):
            pos = "verb"
        elif pos in ("adj", "adjective"):
            pos = "adjective"
        
        # Extract the Code-domain meaning (the first "- **Code-domain:**" line)
        meaning_match = re.search(r'\*\*Code-domain:\*\*\s*(.+?)(?:\n|$)', section)
        meaning = meaning_match.group(1).strip() if meaning_match else ""
        # Clean up meaning - remove trailing period, truncate
        meaning = meaning.rstrip(".")
        
        # Extract an STE example (prefer the first STE example line from dictionary)
        dict_example = ""
        ste_examples = re.findall(r'> \*\*STE:\*\*\s*(.+?)(?:\n|$)', section)
        if ste_examples:
            dict_example = ste_examples[0].strip()
        
        entries.append({
            "word": word,
            "pos": pos,
            "meaning": meaning,
            "example": dict_example,  # fallback if rule files have no example
            "_dict_example": dict_example,
        })
    
    return entries


def find_rules_for_word(word, rules_dir):
    """Search all rule files for references to this word, return list of rule IDs."""
    rules = []
    for rule_file in sorted(rules_dir.glob("a-sec*-rule*.md")):
        text = rule_file.read_text(encoding="utf-8")
        # Check for the word in the file
        word_pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        if word_pattern.search(text):
            # Extract rule number from filename: a-sec1-rule1.1.md -> rule-1.1
            m = re.search(r'(rule\d+\.\d+)', rule_file.name)
            if m:
                rules.append("rule-" + m.group(1).replace("rule", ""))
    return sorted(set(rules))


def find_examples_in_rules(word, pos, rules_dir):
    """Find usage examples of the word in rule files."""
    examples = []
    word_lower = word.lower()
    
    for rule_file in sorted(rules_dir.glob("a-sec*-rule*.md")):
        text = rule_file.read_text(encoding="utf-8")
        lines = text.split("\n")
        
        for i, line in enumerate(lines):
            # Look for lines containing the word in context
            if re.search(r'\b' + re.escape(word_lower) + r'\b', line, re.IGNORECASE):
                stripped = line.strip()
                # Skip headers, metadata lines
                if stripped.startswith("#") or stripped.startswith("*Ref:"):
                    continue
                    
                # Capture STE/Non-STE example lines
                if stripped.startswith(">") and ("**STE:**" in stripped or "**Non-STE:**" in stripped):
                    cleaned = re.sub(r'> \*\*(?:STE|Non-STE):\*\*\s*', '', stripped)
                    if 15 < len(cleaned) < 250:
                        examples.append(("ste", cleaned))
                        
                # Capture code blocks and inline examples
                elif stripped.startswith("`") or stripped.startswith("```"):
                    continue
                elif 15 < len(stripped) < 250 and not stripped.startswith("-") and not stripped.startswith("**"):
                    examples.append(("text", stripped))
    
    # Prefer STE examples over general text
    ste_examples = [e for t, e in examples if t == "ste"]
    text_examples = [e for t, e in examples if t == "text"]
    
    # From STE examples, prefer one where the word appears in the STE (not Non-STE) version
    for ex in ste_examples:
        if re.search(r'\b' + re.escape(word_lower) + r'\b', ex, re.IGNORECASE):
            return ex
    
    if ste_examples:
        return ste_examples[0]
    if text_examples:
        # Prefer a clean, short example
        for ex in text_examples:
            if len(ex) < 150 and re.search(r'[.!?]$', ex):
                return ex
        return text_examples[0]
    return ""


def main():
    print("Parsing dictionary...")
    entries = parse_dictionary(DICT_PATH)
    print(f"  Found {len(entries)} approved verb/adjective entries")
    
    print("Searching rule files for references...")
    for entry in entries:
        rules = find_rules_for_word(entry["word"], RULES_DIR)
        entry["rules"] = rules if rules else ["rule-1.1"]  # default to rule-1.1
        
        # Try to find a better example from rule files
        rule_example = find_examples_in_rules(entry["word"], entry["pos"], RULES_DIR)
        if rule_example:
            entry["example"] = rule_example
        elif not entry["example"] and entry.get("_dict_example"):
            entry["example"] = entry["_dict_example"]
        
        # Remove internal fields
        entry.pop("_dict_example", None)
    
    verbs = [e for e in entries if e["pos"] == "verb"]
    adjectives = [e for e in entries if e["pos"] == "adjective"]
    
    print(f"\nVerbs: {len(verbs)}")
    print(f"Adjectives: {len(adjectives)}")
    
    # Write verbs JSON
    out_verbs = {
        "version": "3.0.0",
        "source": "ASD-STE100 Issue 9 (January 2025), adapted to code domain — extracted from a-dictionary.md and deepened rule files",
        "domain": "code",
        "count": len(verbs),
        "entries": verbs
    }
    OUT_VERBS.parent.mkdir(parents=True, exist_ok=True)
    OUT_VERBS.write_text(json.dumps(out_verbs, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {OUT_VERBS}")
    
    # Write adjectives JSON
    out_adj = {
        "version": "3.0.0",
        "source": "ASD-STE100 Issue 9 (January 2025), adapted to code domain — extracted from a-dictionary.md and deepened rule files",
        "domain": "code",
        "count": len(adjectives),
        "entries": adjectives
    }
    OUT_ADJ.write_text(json.dumps(out_adj, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {OUT_ADJ}")
    
    # Print sample
    print("\n--- Sample verbs ---")
    for v in verbs[:5]:
        print(f"  {v['word']}: {v['meaning'][:60]}... rules={v['rules']}")
    
    print("\n--- Sample adjectives ---")
    for a in adjectives[:5]:
        print(f"  {a['word']}: {a['meaning'][:60]}... rules={a['rules']}")
    
    print(f"\nDone. Verbs: {len(verbs)}, Adjectives: {len(adjectives)}")


if __name__ == "__main__":
    main()
