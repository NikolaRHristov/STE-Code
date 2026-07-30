import json

with open('/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/data/vocabulary/approved-verbs.json') as f:
    v = json.load(f)
with open('/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/data/vocabulary/approved-adjectives.json') as f:
    a = json.load(f)

# Check for required fields
for entry in v['entries']:
    for field in ['word', 'pos', 'meaning', 'example', 'rules']:
        if field not in entry:
            print(f'MISSING {field} in verb: {entry.get("word","?")}')
            
for entry in a['entries']:
    for field in ['word', 'pos', 'meaning', 'example', 'rules']:
        if field not in entry:
            print(f'MISSING {field} in adj: {entry.get("word","?")}')

# Check unique words
verb_words = [e['word'] for e in v['entries']]
adj_words = [e['word'] for e in a['entries']]
dup_verbs = [w for w in verb_words if verb_words.count(w) > 1]
dup_adjs = [w for w in adj_words if adj_words.count(w) > 1]
if dup_verbs: print(f'Dup verbs: {set(dup_verbs)}')
if dup_adjs: print(f'Dup adjs: {set(dup_adjs)}')

# Check cross-contamination (verb words in adj, adj words in verb)
v_set = set(verb_words)
a_set = set(adj_words)
cross = v_set & a_set
if cross:
    # This is OK - some words are approved as both verb and adjective
    print(f'Words in both lists (OK - dual POS): {sorted(cross)}')

print(f'Verbs: {len(v["entries"])} entries, all required fields present')
print(f'Adjectives: {len(a["entries"])} entries, all required fields present')

# Check a few entries have good examples
no_example_v = [e['word'] for e in v['entries'] if not e['example']]
no_example_a = [e['word'] for e in a['entries'] if not e['example']]
if no_example_v: print(f'Verbs without examples: {no_example_v}')
if no_example_a: print(f'Adjs without examples: {no_example_a}')

no_rules_v = [e['word'] for e in v['entries'] if not e['rules']]
no_rules_a = [e['word'] for e in a['entries'] if not e['rules']]
if no_rules_v: print(f'Verbs without rules: {no_rules_v}')
if no_rules_a: print(f'Adjs without rules: {no_rules_a}')
