#!/usr/bin/env python3
"""Level 5 (~100K tokens) — clean cut: original rule + adaptation + top 3 examples."""

from pathlib import Path
import json, re

PROJECT = Path(__file__).resolve().parent.parent.parent
RULES_DIR = PROJECT / "ste-code" / "adapted"
OUTPUT = PROJECT / "ste-code" / "artifacts" / "ste-code-level5-max.txt"

prompt = """You are STE-Code, Simplified Technical English for Code documentation.
Apply the complete Level 5 standard. Follow all 51 rules strictly.

---

"""

rules = sorted(RULES_DIR.glob("a-sec*-rule*.md"))

for r in rules:
    content = r.read_text()
    
    # Title
    title = content.split("\n")[0].strip("# ").strip()
    prompt += f"### {title}\n\n"
    
    # Extract: Original Rule text
    m = re.search(r'## Original Rule\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
    if m:
        orig = m.group(1).strip()
        # Take first 3 sentences
        sentences = re.split(r'(?<=[.!?])\s+', orig)
        prompt += " ".join(sentences[:10]) + "\n\n"
    
    # Extract: STE-Code Adaptation (first 5 sentences)
    m = re.search(r'## STE-Code Adaptation\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
    if m:
        adapt = m.group(1).strip()
        sentences = re.split(r'(?<=[.!?])\s+', adapt)
        prompt += " ".join(sentences[:15]) + "\n\n"
    
    # Extract: up to 5 example pairs
    examples = 0
    for m in re.finditer(r'> \*\*Non-STE:\*\*(.*?)(?=\n> \*\*Non-STE:\*\*|\n> \*\*STE:\*\*|\n## |\n---|\Z)', content, re.DOTALL):
        if examples >= 5:
            break
        ex = m.group(0).strip()
        prompt += ex + "\n\n"
        examples += 1
    
    prompt += "---\n\n"

# GR rules
for r in sorted(RULES_DIR.glob("a-sec*-gr*.md")):
    content = r.read_text()
    title = content.split("\n")[0].strip("# ").strip()
    prompt += f"### {title}\n\n"
    m = re.search(r'## Original Rule\n(.*?)(?=\n## |\n---|\Z)', content, re.DOTALL)
    if m:
        prompt += m.group(1).strip()[:500] + "\n\n"
    prompt += "---\n\n"

# Synonym table
synonym_file = PROJECT / "ste-code" / "data" / "synonym-table.json"
if synonym_file.exists():
    data = json.loads(synonym_file.read_text())
    prompt += "## Synonym Table\n\n| Prefer | Avoid |\n|--------|-------|\n"
    for pair in data.get("pairs", []):
        avoid = ", ".join(pair["avoid"][:3])
        prompt += f"| {pair['approved']} | {avoid} |\n"

prompt += """

---

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. © ASD, 2025. Independent adaptation. asd-ste100.org
"""

OUTPUT.write_text(prompt)
chars = len(prompt)
tokens = chars // 4
print(f"Level 5: {prompt.count(chr(10)):,} lines, {chars:,} chars, ~{tokens:,} tokens")
