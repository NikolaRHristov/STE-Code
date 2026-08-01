#!/usr/bin/env python3
"""One-command release: verify, sync, changelog, commit, tag, publish.

Pipeline (each step is skippable, everything is dry-run by default):

  1. preflight  clean tree, on the release branch, remote reachable
  2. facts      measure the project from disk
  3. sync       rewrite drifted badges, versions, and counts
  4. changelog  regenerate CHANGELOG.md with the new version promoted
  5. verify     re-scan; refuse to continue while drift remains
  6. commit     one `chore(release): vX.Y.Z` commit
  7. tag        annotated tag on every configured track
  8. push       branch + tags
  9. publish    GitHub release with generated notes
 10. labels     reconcile repository labels and topics

Usage:
    python3 .agents/tools/release/release.py --version 1.1.0 --dry-run
    python3 .agents/tools/release/release.py --version 1.1.0 --execute
    python3 .agents/tools/release/release.py --bump minor --execute
    python3 .agents/tools/release/release.py --check          # verify only
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from facts import collect  # noqa: E402

TRACKS = {"core": "v{v}", "STANDARD": "STANDARD-{v}", "FLAVOR": "FLAVOR-{v}"}

# Paths a release owns. Multi-session safety: other Hermes sessions run
# concurrently in this repo (benchmark workers, refinement, grouping) and
# auto-commit their own directories. Staging `-A` would sweep up their
# in-flight, half-written files. Restrict staging to release artefacts and
# pass --paths to widen it deliberately.
OWNED_PATHS = [
    "CHANGELOG.md",
    "CITATION.cff",
    "README.md",
    "CONTRIBUTING.md",
    "docs",
    "mkdocs.yml",
    "ste-code/README.md",
    "ste-code/artifacts/README.md",
    "ste-code/linguistics",
    ".agents/AGENTS.md",
    ".agents/README.md",
    ".agents/tools/release",
    ".agents/skills/github",
    ".github/workflows",
    "translations/README.md",
    "Makefile",
]


class Runner:
    def __init__(self, execute: bool) -> None:
        self.execute = execute
        self.log: list[str] = []

    def run(self, *args: str, check: bool = True, capture: bool = False) -> str:
        printable = " ".join(args)
        if not self.execute:
            self.log.append(f"WOULD RUN  {printable}")
            print(f"  would run: {printable}")
            return ""
        self.log.append(f"RUN  {printable}")
        out = subprocess.run(
            args, cwd=PROJECT, capture_output=True, text=True
        )
        if check and out.returncode != 0:
            raise SystemExit(f"FAILED: {printable}\n{out.stderr.strip()}")
        return out.stdout.strip()


def git_out(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=PROJECT, capture_output=True, text=True
    ).stdout.strip()


def bump(current: str, part: str) -> str:
    major, minor, patch = (int(p) for p in current.split("."))
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def preflight(version: str, branch: str, allow_dirty: bool, paths: list[str]) -> list[str]:
    problems = []
    current = git_out("rev-parse", "--abbrev-ref", "HEAD")
    if current != branch:
        problems.append(f"on branch {current!r}, expected {branch!r}")
    # Only the paths this release stages need to be clean. Dirt elsewhere
    # belongs to a concurrent session and is none of our business.
    if not allow_dirty:
        dirty = git_out("status", "--porcelain", "--", *paths).splitlines()
        conflicted = [ln for ln in dirty if ln[:2] in ("UU", "AA", "DD")]
        if conflicted:
            problems.append(f"unresolved conflicts in {len(conflicted)} owned path(s)")
    for track, fmt in TRACKS.items():
        tag = fmt.format(v=version)
        if git_out("tag", "--list", tag):
            problems.append(f"tag {tag} already exists")
    if not shutil.which("gh"):
        problems.append("gh CLI not found — publishing and labels will be skipped")
    return problems


def step_sync(r: Runner, picks: list[str]) -> None:
    args = ["python3", str(HERE / "sync.py")]
    for p in picks:
        args += ["--pick", p]
    if not r.execute:
        args.append("--dry-run")
        print(subprocess.run(args, cwd=PROJECT, capture_output=True, text=True).stdout)
        return
    r.run(*args)


def step_changelog(r: Runner, version: str) -> None:
    args = ["python3", str(HERE / "changelog.py"), "--next", version]
    if not r.execute:
        args.append("--stdout")
        out = subprocess.run(args, cwd=PROJECT, capture_output=True, text=True).stdout
        print(f"  changelog preview: {len(out.splitlines())} lines")
        return
    r.run(*args)


def step_verify() -> int:
    out = subprocess.run(
        ["python3", str(HERE / "scan.py")], cwd=PROJECT, capture_output=True, text=True
    )
    print(out.stdout)
    return out.returncode


def step_labels(r: Runner) -> None:
    reg = json.loads((HERE / "registry.json").read_text(encoding="utf-8"))
    existing = {}
    if shutil.which("gh"):
        raw = subprocess.run(
            ["gh", "label", "list", "--limit", "200", "--json", "name,color,description"],
            cwd=PROJECT,
            capture_output=True,
            text=True,
        ).stdout
        try:
            existing = {x["name"]: x for x in json.loads(raw or "[]")}
        except json.JSONDecodeError:
            existing = {}
    for label in reg["labels"]:
        name, color, desc = label["name"], label["color"], label["description"]
        cur = existing.get(name)
        if cur and cur.get("color", "").lower() == color.lower() and cur.get("description") == desc:
            continue
        verb = "edit" if cur else "create"
        r.run("gh", "label", verb, name, "--color", color, "--description", desc, check=False)
    topics = reg["topics"]
    r.run(
        "gh", "repo", "edit", "--add-topic", ",".join(topics), check=False
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", help="explicit target version, e.g. 1.1.0")
    ap.add_argument("--bump", choices=["major", "minor", "patch"], help="derive the version")
    ap.add_argument("--branch", default="Current", help="release branch (default: Current)")
    ap.add_argument("--execute", action="store_true", help="apply changes (default: dry run)")
    ap.add_argument("--dry-run", action="store_true", help="explicit dry run")
    ap.add_argument("--check", action="store_true", help="run the drift scan only")
    ap.add_argument("--allow-dirty", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--no-publish", action="store_true")
    ap.add_argument("--pick", action="append", default=[], metavar="CLAIM=VALUE")
    ap.add_argument(
        "--paths",
        action="append",
        default=[],
        metavar="PATH",
        help="stage these paths instead of the owned set (repeatable)",
    )
    ap.add_argument("--tracks", default="core,STANDARD,FLAVOR")
    args = ap.parse_args()

    if args.check:
        return step_verify()

    facts = collect()
    current = facts["versions"]["core"]
    version = args.version or (bump(current, args.bump) if args.bump else None)
    if not version:
        raise SystemExit("Give --version X.Y.Z or --bump {major,minor,patch}")
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        raise SystemExit(f"Not a semver version: {version!r}")

    execute = args.execute and not args.dry_run
    # facts.py reads this: the new tag does not exist yet, so the release date
    # cannot be derived from git during this run.
    os.environ["STE_RELEASE_DATE"] = date.today().isoformat()
    r = Runner(execute)
    mode = "EXECUTE" if execute else "DRY RUN"
    print(f"STE-Code release {current} -> {version}   [{mode}]\n")

    print("1. preflight")
    owned = [p for p in (args.paths or OWNED_PATHS) if (PROJECT / p).exists()]
    problems = preflight(version, args.branch, args.allow_dirty, owned)
    hard = [p for p in problems if "gh CLI" not in p]
    for p in problems:
        print(f"   - {p}")
    if hard and execute:
        raise SystemExit("Preflight failed. Fix the items above or pass --allow-dirty.")
    if not problems:
        print("   clean")

    print("\n2. facts")
    print(
        f"   {facts['rules']} rules, {facts['categories']} categories, "
        f"{facts['tier_count']} tiers, {facts['benchmark_tests']} tests, "
        f"{facts['locales']} locales, {facts['unreleased_commits']} unreleased commits"
    )

    print("\n3. sync claims")
    step_sync(r, args.pick)

    print("\n4. changelog")
    step_changelog(r, version)

    print("\n5. verify")
    if execute:
        if step_verify() != 0:
            raise SystemExit(
                "Drift remains after sync. Resolve it (see --pick) and re-run."
            )
    else:
        step_verify()

    print("\n6. commit")
    # Recompute: earlier steps create files (CHANGELOG.md on a first release)
    # that did not exist when `owned` was resolved during preflight.
    to_stage = [p for p in (args.paths or OWNED_PATHS) if (PROJECT / p).exists()]
    for p in to_stage:
        r.run("git", "add", "--", p)
    r.run("git", "commit", "-m", f"chore(release): v{version}", check=False)

    print("\n7. tag")
    wanted = [t.strip() for t in args.tracks.split(",") if t.strip()]
    for track in wanted:
        fmt = TRACKS.get(track)
        if not fmt:
            print(f"   unknown track {track!r} — skipped")
            continue
        tag = fmt.format(v=version)
        r.run("git", "tag", "-a", tag, "-m", f"STE-Code {track} {version}")

    if args.no_push:
        print("\n8. push  (skipped)")
    else:
        print("\n8. push")
        r.run("git", "push", "origin", args.branch)
        r.run("git", "push", "origin", "--tags")

    if args.no_publish or not shutil.which("gh"):
        print("\n9. publish  (skipped)")
    else:
        print("\n9. publish")
        notes = subprocess.run(
            ["python3", str(HERE / "changelog.py"), "--notes", version],
            cwd=PROJECT,
            capture_output=True,
            text=True,
        ).stdout.strip()
        notes_file = PROJECT / ".agents/tmp/release-notes.md"
        if execute:
            notes_file.parent.mkdir(parents=True, exist_ok=True)
            notes_file.write_text(notes or f"STE-Code {version}", encoding="utf-8")
        r.run(
            "gh", "release", "create", f"v{version}",
            "--title", f"STE-Code v{version}",
            "--notes-file", str(notes_file),
            check=False,
        )

    print("\n10. labels and topics")
    step_labels(r)

    print(f"\nDone ({mode}). {len(r.log)} action(s).")
    if not execute:
        print("Re-run with --execute to apply.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
