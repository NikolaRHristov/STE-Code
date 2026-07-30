import re
from pathlib import Path

DICT_PATH = Path("/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/adapted/a-dictionary.md")
text = DICT_PATH.read_text(encoding="utf-8")

# Find the THICK section
sections = re.split(r'\n(?=## [A-Z])', text)
for section in sections:
    if section.startswith("## THICK"):
        print("FOUND THICK section")
        print(f"Has 'not commonly applicable': {'not commonly applicable' in section.lower()}")
        print(f"Has 'limited code-documentation': {'limited code-documentation' in section.lower()}")
        print(f"Has 'retained': {'retained' in section.lower()}")
        print(f"Has 'not applicable': {'not applicable' in section.lower()}")
        
        # Check the regex
        header_match = re.match(r'^## ([A-Z]+) \(([a-z]+)\)(?:\s*-\s*(.+))?', section)
        if header_match:
            print(f"Header match: word={header_match.group(1)}, pos={header_match.group(2)}, suffix='{header_match.group(3)}'")
        print()
        print("Section text:")
        print(section[:300])
        break
