#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path(__file__).resolve().with_name('unapproved-entries.json')

with open(PATH) as f:
    data = json.load(f)

no_ex = [e for e in data if not e['example_non_ste']]
print(f'Entries without examples ({len(no_ex)}):')
for e in no_ex:
    print(f'  {e["unapproved"]} ({e["pos"]}) -> {e["approved"]}  [{e["source"]}]')

print()
rf = [e for e in data if 'rule-files' in e.get('source', '')]
print(f'Rule-file entries: {len(rf)}')
for e in rf[:10]:
    print(f'  {e["unapproved"]} -> {e["approved"]}')
    n = e.get("example_non_ste", "")
    s = e.get("example_ste", "")
    print(f'    Non-STE: {n[:120]}')
    print(f'    STE:     {s[:120]}')
    print()
