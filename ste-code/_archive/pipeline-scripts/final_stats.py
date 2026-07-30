import json

with open('/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/data/vocabulary/approved-verbs.json') as f:
    v = json.load(f)
with open('/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/data/vocabulary/approved-adjectives.json') as f:
    a = json.load(f)

# Counts
verb_count = len(v['entries'])
adj_count = len(a['entries'])

# Entry with most rules
top_verb = max(v['entries'], key=lambda e: len(e['rules']))
top_adj = max(a['entries'], key=lambda e: len(e['rules']))

# Entry with fewest rules
min_verb = min(v['entries'], key=lambda e: len(e['rules']))
min_adj = min(a['entries'], key=lambda e: len(e['rules']))

# Average rules per entry
avg_v = sum(len(e['rules']) for e in v['entries']) / verb_count
avg_a = sum(len(e['rules']) for e in a['entries']) / adj_count

print(f"APPROVED VERBS:        {verb_count}")
print(f"APPROVED ADJECTIVES:   {adj_count}")
print(f"TOTAL:                 {verb_count + adj_count}")
print()
print(f"Verb with most rules:  {top_verb['word']} ({len(top_verb['rules'])} rules)")
print(f"Verb with fewest:      {min_verb['word']} ({len(min_verb['rules'])} rule(s))")
print(f"Avg rules per verb:    {avg_v:.1f}")
print()
print(f"Adj with most rules:   {top_adj['word']} ({len(top_adj['rules'])} rules)")
print(f"Adj with fewest:       {min_adj['word']} ({len(min_adj['rules'])} rule(s))")
print(f"Avg rules per adj:     {avg_a:.1f}")
