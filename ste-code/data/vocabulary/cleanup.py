#!/usr/bin/env python3
"""Final cleanup of the JSON output."""
import json
from pathlib import Path

PATH = Path(__file__).resolve().with_name('unapproved-entries.json')

with open(PATH) as f:
    data = json.load(f)

cleaned = []
for entry in data:
    # Remove aerospace-only entries
    if entry['unapproved'] in ('acrid', 'adhesion'):
        continue
    
    # Clean approved alternatives: remove full sentences (> 4 words)
    entry['approved'] = [
        a for a in entry['approved']
        if len(a.split()) <= 4 and a.strip()
    ]
    
    # Fix swapped STE/Non-STE for "within" entry
    if entry['unapproved'] == 'within':
        orig_non = entry['example_non_ste']
        orig_ste = entry['example_ste']
        if 'wasn' in orig_non or 'reconnecting' in orig_non:
            # They're swapped - the non-STE has "wasn't" which is the non-STE version
            entry['example_non_ste'] = orig_ste
            entry['example_ste'] = orig_non
    
    cleaned.append(entry)

print(f'Before: {len(data)}, After: {len(cleaned)}')
print(f'Removed: {len(data) - len(cleaned)}')

# Stats
no_alt = sum(1 for e in cleaned if not e['approved'])
no_ex = sum(1 for e in cleaned if not e['example_non_ste'])
print(f'Without alternatives: {no_alt}')
print(f'Without examples: {no_ex}')

with open(PATH, 'w') as f:
    json.dump(cleaned, f, indent=2, ensure_ascii=False)

print(f'Wrote {len(cleaned)} cleaned entries')
