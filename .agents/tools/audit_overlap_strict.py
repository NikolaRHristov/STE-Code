#!/usr/bin/env python3
"""Strict re-verification: non-anchored headword extraction (handles rows
collapsed onto one line, as in w080). Compares refined vs extracted."""

import re, sys, glob, os


def _repo_root():
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    for _ in range(8):
        if os.path.isdir(os.path.join(cur, ".git")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            break
        cur = parent
    return cur


ROOT = os.path.join(_repo_root(), "ste-code")

# non-anchored: a headword is  |**word (pos)  or  |**WORD (pos)**  anywhere,
# plus #### WORD (pos) headings.
PIPE = re.compile(r"\|\s*\*{0,2}\s*([A-Za-z][A-Za-z\-]*)\s*\*{0,2}\s*\(")
HEAD = re.compile(r"^#{3,4}\s+\*{0,2}([A-Za-z][A-Za-z\-]*)\s*\(", re.M)

STOP = {"part", "page", "word", "issue", "adj", "adv", "n", "v", "prep", "tn"}


def hw(path):
    t = open(path, encoding="utf-8", errors="ignore").read()
    s = {m.group(1).lower() for m in PIPE.finditer(t)}
    s |= {m.group(1).lower() for m in HEAD.finditer(t)}
    return s - STOP


def find(kind, n):
    pre = "w" if kind == "extracted" else "r"
    g = glob.glob(f"{ROOT}/{kind}/{pre}{n:03d}-*.md")
    return g[0] if g else None


CONFLICT = [
    54,
    55,
    56,
    72,
    73,
    74,
    75,
    76,
    77,
    78,
    79,
    81,
    82,
    83,
    84,
    85,
    86,
    87,
    89,
    90,
    91,
    92,
    93,
    94,
    95,
    96,
    97,
    98,
    99,
    101,
    102,
    103,
    104,
    105,
    106,
]

if __name__ == "__main__":
    nums = [int(a) for a in sys.argv[1:]] or CONFLICT
    npass = 0
    rows = []
    for n in sorted(set(nums)):
        e, r = find("extracted", n), find("refined", n)
        if not e or not r:
            rows.append((n, None, "MISSING", 0, 0))
            continue
        he, hr = hw(e), hw(r)
        if not he:
            rows.append((n, 0.0, "EMPTY-SRC", 0, len(hr)))
            continue
        ov = len(he & hr) / len(he)
        st = "PASS" if ov >= 0.5 else "FAIL"
        if st == "PASS":
            npass += 1
        rows.append((n, ov, st, len(he), len(hr)))
    for n, ov, st, ne, nr in rows:
        ovs = f"{ov * 100:5.1f}%" if ov is not None else "  n/a"
        print(f"w{n:03d} {ovs} {st:10s} src_hw={ne:3d} ref_hw={nr:3d}")
    print(f"\nSTRICT: PASS={npass}/{len(rows)}")
