#!/usr/bin/env python3
"""Corrected-regex overlap audit for STE-Code refined vs extracted dict pages."""
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

def hw(path):
    t = open(path, encoding='utf-8', errors='ignore').read()
    s = set()
    for m in re.finditer(r'^\|+\s*\*{0,2}\s*([A-Za-z][A-Za-z\-]*)\s*\(', t, re.M):
        s.add(m.group(1).lower())
    for m in re.finditer(r'^#{3,4}\s+\*{0,2}([A-Za-z][A-Za-z\-]*)\s*\(', t, re.M):
        s.add(m.group(1).lower())
    return s

def find(kind, n):
    g = glob.glob(f"{ROOT}/{kind}/{'w' if kind=='extracted' else 'r'}{n:03d}-*.md")
    return g[0] if g else None

def audit(n):
    e = find("extracted", n)
    r = find("refined", n)
    if not e:
        return (n, None, "NO-EXTRACTED", 0, 0, None, None)
    if not r:
        return (n, None, "NO-REFINED", 0, 0, e, None)
    he, hr = hw(e), hw(r)
    if not he:
        return (n, 0.0, "EMPTY-SRC", 0, len(hr), e, r)
    ov = len(he & hr) / len(he)
    return (n, ov, "PASS" if ov >= 0.5 else "FAIL", len(he), len(hr), e, r)

if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        nums = [int(a) for a in args]
    else:
        nums = [54,55,56,72,73,74,75,76,77,78,79,81,82,83,84,85,86,87,89,90,
                91,92,93,94,95,96,97,98,99,101,102,103,104,105,106,52,53,57]
    npass = nfail = nempty = 0
    for n in sorted(set(nums)):
        num, ov, st, ne, nr, e, r = audit(n)
        ovs = f"{ov*100:5.1f}%" if ov is not None else "  n/a"
        print(f"{num:03d} {ovs} {st:12s} src_hw={ne:3d} ref_hw={nr:3d} {os.path.basename(e) if e else '-'}")
        if st == "PASS": npass += 1
        elif st == "EMPTY-SRC": nempty += 1
        else: nfail += 1
    print(f"\nPASS={npass} FAIL={nfail} EMPTY_SRC={nempty} TOTAL={len(set(nums))}")
