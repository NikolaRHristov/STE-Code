#!/usr/bin/env python3
"""One final cleanup pass."""
import json

with open('ste-code/data/synonym-table.json') as f:
    data = json.load(f)

pairs = data['pairs']

# "utilize" should NOT be an approved word - it's an avoid word for "use"
# Remove it as an approved entry
# Also remove other British-spelling approved entries that are just -ise → -ize variants
# when they're not the canonical American spelling
british_variants_as_approved = {
    'centralizes', 'customizable', 'initialized', 'initializes',
    'maximizes', 'minimizes', 'optimizes', 'recognized', 'recognizes',
    'synchronizes',
}

# Words that appear as both approved and avoid create contradictions
# Remove them from the approved entries
contradictions = {'utilize'}

cleaned = []
for p in pairs:
    approved = p["approved"]
    if approved in contradictions:
        continue
    # Clean avoid list: remove "ut", "feched" (misspellings), and other artifacts
    avoid_list = []
    for a in p["avoid"]:
        if len(a) <= 1:
            continue
        if a == 'ut':
            continue
        if a == 'feched':  # misspelling, not a real synonym
            continue
        avoid_list.append(a)
    if not avoid_list:
        continue
    avoid_list = sorted(set(avoid_list))
    cleaned.append({"approved": approved, "avoid": avoid_list})

data["pairs"] = cleaned

with open('ste-code/data/synonym-table.json', "w") as f:
    json.dump(data, f, indent=2)
    f.write("\n")

print(f"Final: {len(cleaned)} pairs")
print(f"Total avoid words: {sum(len(p['avoid']) for p in cleaned)}")
