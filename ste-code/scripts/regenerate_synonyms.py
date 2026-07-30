#!/usr/bin/env python3
"""Extract synonym pairs from all STE-Code rule files and merge with existing synonym table.
Regenerates ste-code/data/synonym-table.json"""

import json
import re
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAPTED = os.path.join(BASE, "adapted")
SYNONYM_PATH = os.path.join(BASE, "data", "synonym-table.json")

# Load existing base pairs
with open(SYNONYM_PATH) as f:
    existing = json.load(f)

# ---- Extract arrow pairs from rule files: "avoid"  "approved" ----
cmd = f'cd "{ADAPTED}" && grep -ohE \'"([a-z]+)" *→ *"([a-zA-Z0-9 \\\\-]+)"\' *.md | sort -u'
output = subprocess.check_output(cmd, shell=True, text=True)

pairs_map = {}  # approved -> set(avoid_words)

for line in output.strip().split('\n'):
    if not line.strip():
        continue
    m = re.match(r'"([a-z]+)" *→ *"(.+?)"', line)
    if not m:
        continue
    avoid_word = m.group(1).strip()
    approved = m.group(2).strip()
    if avoid_word == approved:
        continue
    # Skip morphological variants (irregular conjugations like builded→built, sended→sent)
    morphemes = {
        'applied', 'applies', 'begin', 'builds', 'built', 'burned',
        'catches', 'caught', 'chosen', 'counts', 'evicts', 'found',
        'freed', 'given', 'gives', 'got', 'held', 'kept', 'learned',
        'linked', 'put', 'ran', 'run', 'sent', 'set', 'showed',
        'spent', 'splits', 'stopped', 'takes', 'triggers', 'written',
        'writes', 'wrote', 'duplicate', 'compile', 'update',
        'drop handler', 'copies', 'makes auxiliary copies', 'can cause',
    }
    if approved in morphemes:
        continue
    # Skip -ing forms as approved targets (these are anti-patterns)
    if approved.endswith('ing'):
        # But allow known multi-word phrases
        if approved not in ('to connect again', 'try again', 'speak to', 'makes sure',
                           'gives an error', 'not correct', 'with', 'live longer than',
                           'does not have', 'does not complete', 'did not complete',
                           'that do not complete', 'goes back', 'makes', 'turn on',
                           'make sure', 'log in', 'writes to the log'):
            continue
    pairs_map.setdefault(approved, set()).add(avoid_word)

# ---- Merge existing pairs ----
for ep in existing.get("pairs", []):
    approved = ep["approved"]
    for avoid_word in ep["avoid"]:
        pairs_map.setdefault(approved, set()).add(avoid_word)

# ---- Canonical core pairs from the 14 principles table ----
canonical_extras = {
    "use": ["utilize", "leverage", "employ", "harness"],
    "start": ["initiate", "commence", "bootstrap", "spin up", "fire up"],
    "stop": ["terminate", "halt", "kill", "abort", "shut down", "nuke"],
    "show": ["display", "render", "present", "output", "dump", "print"],
    "make": ["create", "generate", "produce", "fabricate", "instantiate"],
    "get": ["retrieve", "fetch", "obtain", "pull", "grab", "acquire"],
    "set": ["configure", "assign", "establish", "specify", "define", "declare"],
    "check": ["verify", "validate", "ensure", "confirm", "assert", "audit", "inspect"],
    "do": ["perform", "execute", "carry out", "invoke", "trigger"],
    "send": ["transmit", "dispatch", "forward", "push", "post", "submit"],
    "remove": ["delete", "eliminate", "purge", "erase", "wipe", "destroy", "drop"],
    "keep": ["retain", "preserve", "maintain", "store", "persist", "save", "cache"],
    "read": ["fetch", "retrieve", "obtain", "load", "pull", "import"],
    "write": ["save", "persist", "commit", "flush"],
    "build": ["compile", "assemble", "construct"],
    "test": ["verify", "validate", "confirm", "prove", "exercise"],
    "deploy": ["release", "ship", "roll out", "push to production", "go live"],
    "connect": ["attach", "link", "bind", "associate", "wire up"],
    "copy": ["clone", "duplicate", "replicate", "mirror", "fork", "shadow"],
    "move": ["transfer", "shift", "migrate", "relocate", "port", "rename"],
    "find": ["search", "locate", "discover", "detect", "scan", "query"],
    "call": ["invoke", "execute", "trigger", "fire", "dispatch"],
    "return": ["output", "yield", "produce", "send back", "respond with"],
    "handle": ["process", "manage", "deal with", "take care of", "address"],
    "change": ["modify", "update", "alter", "mutate", "edit", "revise", "patch"],
    "combine": ["merge", "unify", "consolidate", "join", "aggregate", "squash"],
    "split": ["divide", "separate", "partition", "break apart", "shard", "chunk"],
    "include": ["contain", "hold", "embed", "nest", "wrap", "bundle"],
    "cause": ["trigger", "induce", "provoke", "result in", "lead to"],
    "prevent": ["block", "prohibit", "disallow", "forbid", "reject"],
}

for approved, avoid_words in canonical_extras.items():
    pairs_map.setdefault(approved, set()).update(avoid_words)

# ---- Additional pairs from deep rule analysis ----
additional_pairs = {
    "give": ["furnish", "provide", "supply", "yield", "hand over"],
    "run": ["execute", "perform", "carry out"],
    "correct": ["rectify", "fix", "repair"],
    "try again": ["retry", "reattempt"],
    "examine": ["analyze", "analyse", "inspect", "study"],
    "free": ["deallocate", "release", "liberate"],
    "speak to": ["contact", "reach out to", "get in touch with"],
    "increase": ["raise", "elevate", "boost", "maximize", "ramp up"],
    "decrease": ["reduce", "lower", "minimize", "diminish"],
    "many": ["multiple", "numerous", "various", "several"],
    "necessary": ["needed", "required", "mandatory", "essential"],
    "given": ["specified", "provided", "supplied"],
    "largest": ["maximum", "biggest", "greatest"],
    "first": ["original", "initial"],
    "new": ["additional", "extra", "further"],
    "time": ["duration", "period", "interval"],
    "defect": ["bug", "flaw", "fault", "issue"],
    "unnecessary": ["cruft", "bloat", "dead code"],
    "understand": ["grok", "comprehend", "grasp"],
    "fail": ["crash", "break", "malfunction"],
    "make sure": ["ensure", "insure", "guarantee", "assure"],
    "because": ["since", "as", "due to the fact that"],
    "about": ["regarding", "concerning", "with respect to"],
    "can": ["be able to", "have the capability to", "is capable of"],
    "must": ["shall", "should", "ought to", "needs to"],
    "if": ["in the event that", "in case of", "should it happen that"],
    "before": ["prior to", "preceding", "in advance of"],
    "although": ["even though", "despite the fact that", "notwithstanding"],
    "control": ["orchestrate", "direct", "govern"],
    "administrator": ["admin", "sysadmin", "root"],
    "detailed": ["verbose", "comprehensive", "exhaustive"],
    "turn on": ["enable", "activate", "switch on"],
    "hide": ["abstract away", "obscure", "conceal"],
    "personal": ["personalized", "customized"],
    "not correct": ["invalid", "invalidating", "malformed"],
    "defense": ["defence"],
    "license": ["licence"],
    "program": ["programme"],
    "meter": ["metre"],
    "center": ["centre"],
    "color": ["colour"],
    "behavior": ["behaviour"],
    "organize": ["organise"],
    "centralize": ["centralise"],
    "standardize": ["standardise"],
    "synchronize": ["synchronise"],
    "minimize": ["minimise"],
    "recognize": ["recognise"],
    "initialize": ["initialise"],
    "serialize": ["serialise"],
    "customize": ["customise"],
    "optimize": ["optimise"],
    "canceled": ["cancelled"],
    "usage": ["utilisation"],
    "analyze": ["analyse"],
    "bottom": ["base"],
    "primary": ["main"],
    "split": ["break"],
    "join": ["combine"],
    "stop": ["crash"],
}

for approved, avoid_words in additional_pairs.items():
    pairs_map.setdefault(approved, set()).update(avoid_words)

# ---- Post-process: remove noise ----
# Remove self-references
for approved in list(pairs_map.keys()):
    if approved in pairs_map[approved]:
        pairs_map[approved].remove(approved)
    if not pairs_map[approved]:
        del pairs_map[approved]

# ---- Build final output ----
result_pairs = []
for approved in sorted(pairs_map.keys()):
    avoid_list = sorted(pairs_map[approved])
    result_pairs.append({"approved": approved, "avoid": avoid_list})

output_data = {
    "version": "3.0.0",
    "source": "ASD-STE100 Issue 9 (January 2025), adapted to code domain — regenerated from all deepened rules",
    "domain": "code",
    "canonical": True,
    "description": (
        "Complete code-domain synonym table — every common unapproved coding term mapped to "
        "an approved STE-Code replacement. Regenerated from 51 deepened rule files "
        "(a-sec*-rule*.md) plus the canonical 14-principle synonym table."
    ),
    "pairs": result_pairs
}

with open(SYNONYM_PATH, "w") as f:
    json.dump(output_data, f, indent=2)
    f.write("\n")

print(f"Written {len(result_pairs)} pairs to {SYNONYM_PATH}")
print(f"Total avoid words: {sum(len(p['avoid']) for p in result_pairs)}")
