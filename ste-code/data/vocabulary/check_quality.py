#!/usr/bin/env python3
"""Check quality of the extracted unapproved entries."""
import json

with open('/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/data/vocabulary/unapproved-entries.json') as f:
    data = json.load(f)

print(f'Total entries: {len(data)}')
print(f'With examples: {sum(1 for e in data if e["example_non_ste"])}')
print(f'With alternatives: {sum(1 for e in data if e["approved"])}')
print(f'With both: {sum(1 for e in data if e["example_non_ste"] and e["approved"])}')
print()

no_ex = [e for e in data if not e['example_non_ste']]
print(f'Entries without examples ({len(no_ex)}):')
for e in no_ex[:20]:
    print(f'  {e["unapproved"]} ({e["pos"]}) -> {e["approved"]}  [{e["source"]}]')

print()
no_alt = [e for e in data if not e['approved']]
print(f'Entries without alternatives ({len(no_alt)}):')
for e in no_alt[:20]:
    print(f'  {e["unapproved"]} ({e["pos"]})  [{e["source"]}]')

# Show some entries from rule files with good examples
print()
print('Sample rule-file entries with examples:')
rf_entries = [e for e in data if 'rule-files' in e.get('source', '') and e['example_non_ste']]
for e in rf_entries[:10]:
    print(f'  {e["unapproved"]} -> {e["approved"]}')
    print(f'    Non-STE: {e["example_non_ste"][:120]}')
    print(f'    STE:     {e["example_ste"][:120]}')
