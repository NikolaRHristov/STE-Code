#!/usr/bin/env python3
import json
with open('ste-code/data/synonym-table.json') as f:
    data = json.load(f)
pairs = data['pairs']
print(f'Pairs: {len(pairs)}')
print(f'Avoid words: {sum(len(p["avoid"]) for p in pairs)}')
for p in pairs:
    for a in p['avoid']:
        if len(a) <= 1 or (len(a) == 2 and a not in ('as','in','if','do','by')):
            print(f'SHORT: {p["approved"]} -> "{a}"')
approveds = [p['approved'] for p in pairs]
if len(approveds) != len(set(approveds)):
    print('DUPLICATE approved words!')
else:
    print('All approved words unique.')
