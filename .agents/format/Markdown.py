#!/usr/bin/env python3
"""
Markdown.py - Enforce the STE-Code markdown visual standard.

STE-Code analogue of CodeEditorLand/Land/Maintain/Format/Markdown.py. The
upstream tool reindents HTML <table> blocks; this repository has none (verified:
`grep -rl '<table' ste-code .agents --include=*.md` is empty). What STE-Code
documents and release notes actually use is *markdown* structure, so this tool
enforces the house visual standard instead, using the same read -> parse -> tree
-> re-emit shape and the same --DryRun / --All switches.

Runs BEFORE prettier, exactly like upstream's TypeScript.py / Rust.py: it fixes
block structure, prettier then normalizes prose width and table alignment.

The visual standard (see the `release-notes-visual-standard` skill)
------------------------------------------------------------------
  1. One fact per line; a blank line between every major section.
  2. Heading hierarchy: `#` title -> `##` sections -> `###` subsections,
     with no skipped levels and exactly one `#` per file.
  3. Element choice by data shape: tables for tabular data, bullets for
     enumerated facts, `>` blockquotes for caveats and scope notes.
  4. Every fact preserved. Presentation may be reorganised; content may not.

What this tool CHANGES (whitespace only, fence-aware)
-----------------------------------------------------
  - CRLF / CR -> LF.
  - Trailing whitespace removed, except a two-space markdown hard break.
  - Runs of two or more blank lines collapsed to one.
  - Exactly one blank line before and after every ATX heading.
  - Exactly one blank line before and after every fenced code block and
    every markdown table block.
  - Exactly one trailing newline; no leading blank lines.

What this tool NEVER changes
----------------------------
  - Any non-whitespace character. Numbers, commit hashes, filenames, tag
    names, CJK contamination tokens, diff blocks, and the STANDARD /
    REPOSITORY split are byte-identical after a rewrite.
  - Anything inside a fenced code block (content is copied verbatim).
  - YAML front matter (copied verbatim).
  - Files under any excluded path (see `Exclude`), which mirrors
    .prettierignore: .agents/hermes, .agents/tmp, .agents/skills,
    ste-code/artifacts, node_modules, run output, caches.

The guarantee is enforced, not just documented: `ContentSignature()` strips all
whitespace from the before and after text and the rewrite is REFUSED if the two
signatures differ. A structural bug can only ever produce a skipped file, never
a corrupted one.

Usage
-----
    # Dry-run everything (default target of Format.sh dryrun):
    python3 .agents/format/Markdown.py --DryRun --All

    # Apply to every eligible file:
    python3 .agents/format/Markdown.py --All

    # Report visual-standard violations without changing anything:
    python3 .agents/format/Markdown.py --Audit --All

    # One file:
    python3 .agents/format/Markdown.py --DryRun ste-code/README.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent
# hops. `.git` is the AUTHORITATIVE marker (mirrors .agents/benchmark/
# harness_config.py `_find_root` and .agents/hermes/jail/scripts/jail-lib.sh
# `jail_find_root`). package.json is deliberately NOT a marker: the tooling
# monorepo lives at .agents/package.json and would resolve the root one level
# too deep.
RootMarker = (".git", "Makefile")


def FindRoot(Start: Path) -> Path:
    for Candidate in (Start, *Start.parents):
        if (Candidate / ".git").is_dir():
            return Candidate
    for Candidate in (Start, *Start.parents):
        if (Candidate / "Makefile").is_file():
            return Candidate
    raise SystemExit("Markdown.py: cannot locate repository root (.git/Makefile)")


# Path components that are never formatted anywhere in the tree.
Exclude = frozenset(
    {
        ".git",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".venv",
        "venv",
    }
)

# Repository-relative directory prefixes that are never formatted. These
# mirror .prettierignore entry for entry; a bare component set would be wrong
# here, because e.g. `.agents/tools/artifacts/` IS formatted while
# `ste-code/artifacts/` is not.
ExcludePrefix = (
    # PROTECTED: the concurrently-edited jail / profile surface.
    ".agents/hermes",
    # PROTECTED: per-run scratch (gitignored, ships nothing).
    ".agents/tmp",
    # PROTECTED: live Hermes skill surface, symlinked into every profile.
    ".agents/skills",
    # PROTECTED: generated pipeline artifacts, rebuilt by assemble-level*.py.
    "ste-code/artifacts",
    "ste-code/audit",
    # Gitignored run state, scratch, vendored corpora, generated reports.
    ".agents/_scratch",
    ".agents/archive",
    ".agents/audit",
    ".agents/telemetry",
    ".agents/vendor",
    ".agents/benchmark/tests",
    ".agents/benchmark/report",
    ".agents/benchmark/sample-session",
    ".agents/benchmark/test-cases-adhoc",
    ".agents/tools/linkcheck/reports",
)

TargetExtension = frozenset({".md", ".markdown"})

FenceRegex = re.compile(r"^(\s*)(`{3,}|~{3,})(.*)$")
HeadingRegex = re.compile(r"^(#{1,6})\s+(\S.*)$")
TableRowRegex = re.compile(r"^\s*\|.*\|\s*$")
BulletRegex = re.compile(r"^\s*([-*+])\s+\S")
UrlRegex = re.compile(r"https?://\S+")


# ===========================================================================
# Content preservation
# ===========================================================================


def ContentSignature(Text: str) -> str:
    """Every non-whitespace character, in order.

    Two texts with the same signature differ only in whitespace. This is the
    invariant every transformation in this file must hold.
    """

    return re.sub(r"\s+", "", Text)


# ===========================================================================
# Parse: split a document into typed blocks
# ===========================================================================


class Block:
    """One structural unit of a markdown document."""

    __slots__ = ("Kind", "Lines")

    def __init__(self, Kind: str, Lines: list[str]) -> None:
        # Kind is one of: frontmatter, heading, fence, table, blank, text.
        self.Kind = Kind
        self.Lines = Lines


def StripTrailing(Line: str) -> str:
    """Remove trailing whitespace, preserving a markdown hard break."""

    Stripped = Line.rstrip(" \t")
    if Stripped and Line.endswith("  "):
        return Stripped + "  "
    return Stripped


def Parse(Text: str) -> list[Block]:
    Lines = Text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    Blocks: list[Block] = []
    Index = 0
    Total = len(Lines)

    # YAML front matter is copied verbatim, including its `#` comment lines,
    # which would otherwise look like ATX headings.
    if Total and Lines[0].strip() == "---":
        Close = None
        for Probe in range(1, Total):
            if Lines[Probe].strip() == "---":
                Close = Probe
                break
        if Close is not None:
            Blocks.append(Block("frontmatter", Lines[: Close + 1]))
            Index = Close + 1

    while Index < Total:
        Line = Lines[Index]

        FenceMatch = FenceRegex.match(Line)
        if FenceMatch:
            Marker = FenceMatch.group(2)
            Char = Marker[0]
            Width = len(Marker)
            Body = [Line]
            Index += 1
            while Index < Total:
                Body.append(Lines[Index])
                Close = FenceRegex.match(Lines[Index])
                Index += 1
                if (
                    Close
                    and Close.group(2)[0] == Char
                    and len(Close.group(2)) >= Width
                    and not Close.group(3).strip()
                ):
                    break
            Blocks.append(Block("fence", Body))
            continue

        if Line.strip() == "":
            Blocks.append(Block("blank", [""]))
            Index += 1
            continue

        if HeadingRegex.match(Line):
            Blocks.append(Block("heading", [StripTrailing(Line)]))
            Index += 1
            continue

        if TableRowRegex.match(Line):
            Body: list[str] = []
            while Index < Total and TableRowRegex.match(Lines[Index]):
                Body.append(StripTrailing(Lines[Index]))
                Index += 1
            Blocks.append(Block("table", Body))
            continue

        Body = []
        while Index < Total:
            Probe = Lines[Index]
            if (
                Probe.strip() == ""
                or HeadingRegex.match(Probe)
                or FenceRegex.match(Probe)
                or TableRowRegex.match(Probe)
            ):
                break
            Body.append(StripTrailing(Probe))
            Index += 1
        Blocks.append(Block("text", Body))

    return Blocks


# ===========================================================================
# Emit: re-render blocks with standard separation
# ===========================================================================

# Block kinds that must be surrounded by exactly one blank line.
Separated = frozenset({"heading", "fence", "table"})


def Emit(Blocks: list[Block]) -> str:
    Out: list[str] = []
    # Kind of the last non-blank block emitted; blank blocks never overwrite it.
    Previous: str | None = None

    for Current in Blocks:
        if Current.Kind == "blank":
            # Collapse any run of blank lines to a single separator, and drop
            # leading blank lines entirely.
            if Out and Out[-1] != "":
                Out.append("")
            continue

        # A separator is required when either side of the join is a block that
        # the visual standard isolates: headings, fenced code, tables, and the
        # YAML front matter.
        Isolated = Current.Kind in Separated or Previous in Separated
        if Out and Out[-1] != "" and (Isolated or Previous == "frontmatter"):
            Out.append("")

        Out.extend(Current.Lines)
        Previous = Current.Kind

    while Out and Out[-1] == "":
        Out.pop()

    return "\n".join(Out) + "\n" if Out else ""


def Normalize(Text: str) -> str:
    Result = Emit(Parse(Text))
    if ContentSignature(Result) != ContentSignature(Text):
        raise ValueError("content signature changed")
    return Result


# ===========================================================================
# Audit: report visual-standard violations without changing anything
# ===========================================================================


def Audit(FilePath: Path, Text: str) -> list[str]:
    Findings: list[str] = []
    Blocks = Parse(Text)

    Headings = [
        (len(HeadingRegex.match(B.Lines[0]).group(1)), B.Lines[0])  # type: ignore[union-attr]
        for B in Blocks
        if B.Kind == "heading"
    ]

    TitleCount = sum(1 for Level, _ in Headings if Level == 1)
    if TitleCount == 0 and Headings:
        Findings.append("no `#` title heading")
    if TitleCount > 1:
        Findings.append(f"{TitleCount} `#` title headings (expected 1)")

    Previous = 0
    for Level, Line in Headings:
        if Previous and Level > Previous + 1:
            Findings.append(
                f"heading level jumps h{Previous} -> h{Level}: {Line.strip()[:60]}"
            )
        Previous = Level

    for Current in Blocks:
        if Current.Kind != "table":
            continue
        Widths = {Row.count("|") for Row in Current.Lines}
        if len(Widths) > 1:
            Findings.append(f"table has inconsistent column counts: {sorted(Widths)}")

    Markers = {
        BulletRegex.match(Line).group(1)  # type: ignore[union-attr]
        for Current in Blocks
        if Current.Kind == "text"
        for Line in Current.Lines
        if BulletRegex.match(Line)
    }
    if len(Markers) > 1:
        Findings.append(f"mixed bullet markers: {sorted(Markers)}")

    return [f"{FilePath}: {Finding}" for Finding in Findings]


# ===========================================================================
# Traversal
# ===========================================================================


def ShouldProcess(FilePath: Path, Root: Path) -> bool:
    if FilePath.suffix.lower() not in TargetExtension:
        return False
    # A symlink is owned by whatever it points at (the Hermes profiles
    # symlink INTO this repo); never rewrite through one.
    if FilePath.is_symlink():
        return False
    if any(Part in Exclude for Part in FilePath.parts):
        return False
    try:
        Relative = FilePath.resolve().relative_to(Root).as_posix()
    except ValueError:
        return False
    return not any(
        Relative == Prefix or Relative.startswith(Prefix + "/")
        for Prefix in ExcludePrefix
    )


def CollectTargets(Roots: list[Path], Root: Path) -> list[Path]:
    Files: list[Path] = []
    Seen: set[Path] = set()
    for Base in Roots:
        if not Base.exists():
            continue
        for Candidate in sorted(Base.rglob("*")):
            if not Candidate.is_file():
                continue
            if not ShouldProcess(Candidate, Root):
                continue
            Resolved = Candidate.resolve()
            if Resolved in Seen:
                continue
            Seen.add(Resolved)
            Files.append(Candidate)
    return Files


def ProcessFile(FilePath: Path, DryRun: bool) -> int:
    """Return 1 if the file changed (or would change), 0 otherwise."""

    try:
        Text = FilePath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0

    try:
        NewText = Normalize(Text)
    except ValueError as Error:
        print(
            f"REFUSED (content would change: {Error}): {FilePath}",
            file=sys.stderr,
        )
        return 0

    if NewText == Text:
        return 0

    if DryRun:
        print(f"[DRY RUN] Would modify: {FilePath}")
    else:
        FilePath.write_text(NewText, encoding="utf-8")
        print(f"Modified: {FilePath}")
    return 1


def Main() -> None:
    Parser = argparse.ArgumentParser(
        description="Enforce the STE-Code markdown visual standard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    Parser.add_argument("Files", nargs="*", help="Markdown file paths")
    Parser.add_argument(
        "--All",
        action="store_true",
        help="Process every eligible .md / .markdown file under ste-code/ and .agents/",
    )
    Parser.add_argument(
        "--DryRun",
        action="store_true",
        help="Report what would change without writing",
    )
    Parser.add_argument(
        "--Audit",
        action="store_true",
        help="Report visual-standard violations; never writes",
    )
    Parser.add_argument(
        "--Strict",
        action="store_true",
        help="With --Audit, exit non-zero when findings exist",
    )
    Arguments = Parser.parse_args()

    Root = FindRoot(Path(__file__).resolve().parent)
    Targets: list[Path] = []

    if Arguments.All:
        Targets = CollectTargets([Root / "ste-code", Root / ".agents"], Root)
    else:
        for Pattern in Arguments.Files:
            Candidate = Path(Pattern)
            if Candidate.is_file():
                Targets.append(Candidate)
            else:
                print(f"Warning: file not found: {Pattern}", file=sys.stderr)

    if not Targets:
        Parser.print_help()
        sys.exit(1)

    if Arguments.Audit:
        Findings: list[str] = []
        for Target in Targets:
            try:
                Findings.extend(Audit(Target, Target.read_text(encoding="utf-8")))
            except (UnicodeDecodeError, OSError):
                continue
        for Finding in Findings:
            print(f"[audit] {Finding}")
        print(f"\nAudit - {len(Findings)} finding(s) across {len(Targets)} file(s).")
        sys.exit(1 if (Arguments.Strict and Findings) else 0)

    Changed = sum(ProcessFile(Target, Arguments.DryRun) for Target in Targets)
    Verb = "would change" if Arguments.DryRun else "changed"
    print(f"\nDone - {Verb} {Changed}/{len(Targets)} file(s).")


if __name__ == "__main__":
    Main()
