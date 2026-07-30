import json, sys

with open(sys.argv[1]) as f:
    data = json.load(f)

print(f"Count: {data['count']}")
print()
for e in data['entries'][:5]:
    print(f"  {e['word']} ({e['pos']})")
    print(f"    meaning: {e['meaning'][:80]}")
    print(f"    example: {e['example'][:80]}")
    print(f"    rules: {e['rules']}")
    print()
