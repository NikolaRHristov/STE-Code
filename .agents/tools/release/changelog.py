#!/usr/bin/env python3
"""Build CHANGELOG.md from git history — past releases and unreleased work.

Reads every semver tag on the `core` track (`v1.2.3`), walks the commits
between each pair, groups them by Conventional Commit type, and writes a
Keep-a-Changelog document. Re-running is safe: the file is rebuilt from git,
so history never drifts from the commits that produced it.

Usage:
    python3 .agents/tools/release/changelog.py                 # rewrite CHANGELOG.md
    python3 .agents/tools/release/changelog.py --next 1.1.0    # unreleased -> 1.1.0
    python3 .agents/tools/release/changelog.py --stdout        # print, write nothing
    python3 .agents/tools/release/changelog.py --notes 1.1.0   # one release's notes
"""

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import date
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[3]
REPO = "https://github.com/NikolaRHristov/STE-Code"

SECTIONS = [
    ("feat", "Added"),
    ("fix", "Fixed"),
    ("perf", "Changed"),
    ("refactor", "Changed"),
    ("docs", "Documentation"),
    ("test", "Documentation"),
    ("build", "Tooling"),
    ("ci", "Tooling"),
    ("chore", "Tooling"),
]
TYPE_TO_HEADING = dict(SECTIONS)
HEADING_ORDER = ["Added", "Changed", "Fixed", "Documentation", "Tooling", "Other"]

# Commits that are pipeline bookkeeping, not user-facing change.
NOISE = re.compile(
    r"^(?:chore\(benchmark\): poll-commit|Phase [A-Z]: |wip\b|Merge branch|Merge pull request)",
    re.I,
)
CONVENTIONAL = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?: (?P<subject>.+)$"
)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], capture_output=True, text=True, cwd=PROJECT
    ).stdout.strip()


def core_tags() -> list[tuple[tuple[int, int, int], str]]:
    """Semver tags on the core track, oldest first."""
    rx = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
    found = []
    for tag in git("tag", "--list").splitlines():
        m = rx.match(tag.strip())
        if m:
            found.append((tuple(int(g) for g in m.groups()), tag.strip()))
    return sorted(found)


def commits(rev_range: str) -> list[dict]:
    raw = git("log", rev_range, "--no-merges", "--format=%H%x1f%s%x1f%b%x1e")
    out = []
    for record in raw.split("\x1e"):
        record = record.strip("\n")
        if not record:
            continue
        parts = record.split("\x1f")
        if len(parts) < 2:
            continue
        sha, subject, body = parts[0], parts[1], parts[2] if len(parts) > 2 else ""
        if NOISE.match(subject):
            continue
        m = CONVENTIONAL.match(subject)
        breaking = bool(m and m.group("bang")) or "BREAKING CHANGE" in body
        out.append(
            {
                "sha": sha[:7],
                "subject": subject,
                "type": m.group("type") if m else None,
                "scope": m.group("scope") if m else None,
                "text": m.group("subject") if m else subject,
                "breaking": breaking,
            }
        )
    return out


def group(items: list[dict]) -> dict[str, list[dict]]:
    buckets: dict[str, list[dict]] = {}
    for c in items:
        heading = "Other" if c["type"] is None else TYPE_TO_HEADING.get(c["type"], "Other")
        if c["breaking"]:
            heading = "Changed"
        buckets.setdefault(heading, []).append(c)
    return buckets


def render_section(version: str, when: str, items: list[dict], compare: str | None) -> str:
    lines = [f"## [{version}] — {when}", ""]
    if not items:
        lines += ["No user-facing changes.", ""]
        return "\n".join(lines)
    breaking = [c for c in items if c["breaking"]]
    if breaking:
        lines += ["### Breaking", ""]
        for c in breaking:
            lines.append(f"- {bullet(c)}")
        lines.append("")
    buckets = group(items)
    for heading in HEADING_ORDER:
        rows = [c for c in buckets.get(heading, []) if not c["breaking"]]
        if not rows:
            continue
        lines += [f"### {heading}", ""]
        for c in rows:
            lines.append(f"- {bullet(c)}")
        lines.append("")
    if compare:
        lines += [f"[{version}]: {compare}", ""]
    return "\n".join(lines)


def bullet(c: dict) -> str:
    scope = f"**{c['scope']}:** " if c["scope"] else ""
    text = c["text"] or c["subject"]
    text = text[0].upper() + text[1:]
    return f"{scope}{text} ([`{c['sha']}`]({REPO}/commit/{c['sha']}))"


def build(next_version: str | None) -> str:
    tags = core_tags()
    head = ["# Changelog", ""]
    head += [
        "All notable changes to STE-Code are documented here.",
        "",
        "The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)",
        "and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).",
        "",
        "This file is generated from git history by",
        "`.agents/tools/release/changelog.py` — edit the commits, not this file.",
        "",
    ]
    body: list[str] = []

    newest = tags[-1][1] if tags else None
    pending = commits(f"{newest}..HEAD") if newest else commits("HEAD")
    label = next_version or "Unreleased"
    when = date.today().isoformat() if next_version else "unreleased"
    compare = (
        f"{REPO}/compare/{newest}...{'v' + next_version if next_version else 'HEAD'}"
        if newest
        else None
    )
    body.append(render_section(label, when, pending, compare))

    for i in range(len(tags) - 1, -1, -1):
        tag = tags[i][1]
        prev = tags[i - 1][1] if i > 0 else None
        rng = f"{prev}..{tag}" if prev else tag
        when = git("log", "-1", "--format=%ad", "--date=short", tag)
        link = (
            f"{REPO}/compare/{prev}...{tag}" if prev else f"{REPO}/releases/tag/{tag}"
        )
        body.append(render_section(tag.lstrip("v"), when, commits(rng), link))

    return "\n".join(head + body).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--next", metavar="VERSION", help="promote unreleased to this version")
    ap.add_argument("--stdout", action="store_true", help="print instead of writing")
    ap.add_argument("--notes", metavar="VERSION", help="print one release's notes only")
    args = ap.parse_args()

    text = build(args.next)

    if args.notes:
        want = f"## [{args.notes.lstrip('v')}]"
        keep, out = False, []
        for line in text.splitlines():
            if line.startswith("## ["):
                keep = line.startswith(want)
                if keep:
                    continue
            if keep:
                out.append(line)
        print("\n".join(out).strip())
        return 0

    if args.stdout:
        print(text)
        return 0

    (PROJECT / "CHANGELOG.md").write_text(text, encoding="utf-8")
    print(f"Wrote CHANGELOG.md ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
