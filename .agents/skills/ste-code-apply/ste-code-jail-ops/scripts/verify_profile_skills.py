#!/usr/bin/env python3
"""Verify a STE-Code profile loads ONLY STE-Code skills (no default Hermes set).

Read-only. Reproduces what the Hermes TUI does at session start: it repins
SKILLS_DIR and HERMES_HOME to the profile directory, so the profile's
`skills/` dir is the only skill source — the bundled ~/.hermes/skills/ set is
NOT scanned. This script checks that every entry in that dir is a symlink into
the repo's .agents/skills/ tree (plus any STE consumer skill).

Usage:
    python3 verify_profile_skills.py [dev-ste-code|ste-code|benchmark-ste-code]
    python3 verify_profile_skills.py --all

Exit non-zero if any non-STE (default Hermes) skill entry is found.
"""

from __future__ import annotations

import os
import sys

H = os.path.expanduser("~/.hermes")
REPO = "/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code"
REPO_SKILLS = os.path.realpath(os.path.join(REPO, ".agents", "skills"))
STATE_FILES = {".bundled_manifest", ".usage.json", ".usage.json.lock"}


def check_profile(profile: str) -> int:
    skills_dir = os.path.join(H, "profiles", profile, "skills")
    if not os.path.isdir(skills_dir):
        print(f"[MISS] {profile}: no skills dir at {skills_dir}")
        return 1
    print(f"\n=== {profile} ===")
    bad = 0
    for name in sorted(os.listdir(skills_dir)):
        if name in STATE_FILES:
            continue
        path = os.path.join(skills_dir, name)
        if not os.path.islink(path):
            print(f"  [FAIL] {name}: not a symlink (real default skill?)")
            bad += 1
            continue
        tgt = os.path.realpath(os.readlink(path))
        if tgt.startswith(REPO_SKILLS) or tgt.startswith(os.path.realpath(REPO)):
            print(f"  [ok]   {name} -> {tgt}")
        else:
            print(f"  [FAIL] {name}: points outside the repo ({tgt})")
            bad += 1
    print(f"  result: {'OK — only STE skills' if bad == 0 else f'{bad} problem(s)'}")
    return 1 if bad else 0


def main() -> int:
    profiles = sys.argv[1:] or ["dev-ste-code", "ste-code", "benchmark-ste-code"]
    if profiles == ["--all"]:
        profiles = ["dev-ste-code", "ste-code", "benchmark-ste-code"]
    return max(check_profile(p) for p in profiles)


if __name__ == "__main__":
    sys.exit(main())
