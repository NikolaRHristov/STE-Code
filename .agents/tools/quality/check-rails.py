#!/usr/bin/env python3
"""Rails Compliance Checker — Scan output files against the 8 rails of STE-Code quality.

The 8-rail system checks every output file for structural integrity, formatting
consistency, and factual accuracy after each pipeline stage.

Auto-detects the project root from __file__ so the script runs from any working
directory without manual editing.  Accepts CLI overrides for all paths.

Exit codes:
  0 — clean (all files pass, zero issues)
  1 — warnings only (non-blocking issues found)
  2 — errors found (blocking issues, must fix before merge)
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# ---------------------------------------------------------------------------
# Path resolution — auto-detect or CLI override
# ---------------------------------------------------------------------------

def resolve_root(cli_root: Optional[str] = None) -> str:
    """Return the project root directory.

    Uses the CLI --root value when given.  Otherwise auto-detects from the
    location of this script, matching the convention used by benchmark
    orchestrators and other tool scripts in this repo.
    """
    if cli_root is not None:
        root = os.path.abspath(cli_root)
        if not os.path.isdir(root):
            print(f"ERROR: --root path does not exist: {root}", file=sys.stderr)
            sys.exit(2)
        return root

    # check-rails.py lives at .agents/tools/quality/ → four levels up is project root
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))


def ste_code_dir(root: str) -> str:
    """Return the ste-code output directory under the project root."""
    return os.path.join(root, "ste-code")


# ---------------------------------------------------------------------------
# Fact-check configuration — parameterized, not hardcoded
# ---------------------------------------------------------------------------

# Each entry maps a substring to match (case-insensitive) to a description of
# the expected correct value.  The check fires when the trigger string is found
# but the correction string is absent.  This avoids hardcoding a single claim
# and makes the fact rails extensible without editing source code.
DEFAULT_FACT_CHECKS = [
    {
        "trigger": "22 categor",
        "correction": "not 22",
        "desc": "Claims 22 categories (should be 19)",
    },
    {
        "trigger": "434 page",
        "correction": "not 434",
        "desc": "Claims 434 pages (verify against actual page count)",
    },
    {
        "trigger": "5 stage",
        "correction": "not 5",
        "desc": "Claims 5 pipeline stages (verify against current pipeline)",
    },
]


def load_fact_checks(config_path: Optional[str]) -> List[dict]:
    """Load fact-check rules from a JSON config file, or use built-in defaults.

    Config format:
      [
        {"trigger": "substring", "correction": "negation", "desc": "human label"},
        ...
      ]

    The trigger string is matched case-insensitively against file content.
    The correction string is also matched case-insensitively — if it appears
    anywhere in the file the check is considered self-corrected and does NOT
    fire.  This lets documents rebut a claim inline (e.g. "22 categories,
    not 22 but actually 19").
    """
    if config_path is not None:
        try:
            with open(config_path) as fh:
                loaded = json.load(fh)
            if isinstance(loaded, list):
                return loaded
            print(
                f"WARNING: facts config is not a list; using defaults. ({config_path})",
                file=sys.stderr,
            )
        except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
            print(
                f"WARNING: cannot load facts config ({exc}); using defaults.",
                file=sys.stderr,
            )
    return DEFAULT_FACT_CHECKS


def make_fact_check(trigger: str, correction: str, desc: str):
    """Return a rail check function for a single fact-check rule.

    The returned function scans file content for *trigger* (case-insensitive).
    When *trigger* is found AND *correction* is NOT found, the function returns
    1 (one issue).  Otherwise it returns 0.
    """

    def _check(content: str) -> int:
        low = content.lower()
        if trigger.lower() in low and correction.lower() not in low:
            return 1
        return 0

    _check.__doc__ = desc
    return _check


# ---------------------------------------------------------------------------
# Rail definitions — each rail is a named dict with a check function and a
# human-readable description.  Rails marked STATUS: UNIMPLEMENTED are
# documented but not yet active; they serve as a roadmap for future work.
# ---------------------------------------------------------------------------

def _build_rails(fact_checks: List[dict]) -> dict:
    """Assemble the complete rail dictionary.

    Fact checks are parameterized through the *fact_checks* argument so that
    callers can supply their own config without modifying this file.
    """
    rails: dict = {}

    # ── R1: Stage Isolation ──────────────────────────────────────────────
    # Every file must reside in a stage directory whose name matches the
    # file's expected pipeline stage.  The mapping is based on directory name
    # convention: extracted/ → extraction stage, refined/ → refinement, etc.
    rails["R1-Stage-Isolation"] = {
        "desc": "Files must reside in the correct stage directory",
        "check": _check_stage_isolation,
    }

    # ── R2: Naming Convention ────────────────────────────────────────────
    rails["R2-Naming"] = {
        "desc": "Files must follow [w|r]NNN-pPPPP-PPPP.md pattern",
        "pattern": r"^(w|r)\d{3}-p\d+-\d+\.md$",
        "check": lambda fname: (
            0
            if re.match(r"^(w|r)\d{3}-p\d+-\d+\.md$", fname)
            else 1
        ),
    }

    # ── R3: Content Completeness ─────────────────────────────────────────
    # STATUS: UNIMPLEMENTED — placeholder for future work.
    # Intended to verify that every expected section (Purpose, Syntax,
    # Examples, Notes) is present in each output file.  Requires a schema
    # definition of required sections per file type.
    rails["R3-Completeness"] = {
        "desc": "STATUS: UNIMPLEMENTED — verify all required sections are present",
        "check": lambda content: 0,  # no-op placeholder
    }

    # ── R4: Fabrication Detection ────────────────────────────────────────
    rails["R4-Fabrication"] = {
        "desc": "Fabrication signal phrases detected in content",
        "check": lambda content: sum(
            1
            for t in [
                "This page describes",
                "The key point",
                "In summary",
                "React",
                "Docker",
                "npm",
                "Kubernetes",
            ]
            if t in content
        ),
    }

    # ── R5: Formatting (sub-rails) ───────────────────────────────────────
    rails["R5-Headings"] = {
        "desc": "No glued headings — a blank line is required after a ### heading",
        "check": _check_glued_headings,
    }

    rails["R5-Blanks"] = {
        "desc": "No triple-or-more consecutive blank lines",
        "check": lambda content: 1 if "\n\n\n\n" in content else 0,
    }

    rails["R5-Boilerplate"] = {
        "desc": "Boilerplate header is repeated more than 4 times",
        "check": lambda content: max(
            0, content.count("ASD-STE100 Simplified Technical English") - 4
        ),
    }

    rails["R5-STE-Format"] = {
        "desc": "STE examples must use proper blockquote + bold format",
        "check": lambda content: (
            1
            if "STE:" in content
            and "**STE:**" not in content
            and "> **STE:**" not in content
            else 0
        ),
    }

    rails["R5-Page-Header"] = {
        "desc": "First line must be a # Page N of M header",
        "check": lambda content: (
            0
            if re.match(r"^# Page \d+ of \d+", content.split("\n")[0])
            else 1
        ),
    }

    # ── R6: Factual Accuracy ─────────────────────────────────────────────
    # Build one sub-rail per fact-check rule so each claim is reported
    # independently in the issues list.
    for idx, fc in enumerate(fact_checks):
        key = f"R6-Fact-{idx + 1:02d}"
        rails[key] = {
            "desc": fc["desc"],
            "check": make_fact_check(
                fc["trigger"], fc["correction"], fc["desc"]
            ),
        }

    # ── R7: Cross-Reference Validity ─────────────────────────────────────
    # STATUS: UNIMPLEMENTED — placeholder for future work.
    # Intended to verify that every intra-document link (e.g. "see Rule 2.3"
    # or "[Approved Word](#approved-word)") points to an existing anchor or
    # section heading within the same file or a known artifact.
    rails["R7-CrossReferences"] = {
        "desc": "STATUS: UNIMPLEMENTED — verify internal links resolve to real anchors",
        "check": lambda content: 0,  # no-op placeholder
    }

    # ── R8: Metadata Completeness ────────────────────────────────────────
    # STATUS: UNIMPLEMENTED — placeholder for future work.
    # Intended to verify that every output file carries required frontmatter
    # (source page range, extraction date, worker batch ID, adaptation level).
    rails["R8-Metadata"] = {
        "desc": "STATUS: UNIMPLEMENTED — verify required frontmatter fields are present",
        "check": lambda content: 0,  # no-op placeholder
    }

    return rails


# ---------------------------------------------------------------------------
# Rail check implementations — extracted functions for testability
# ---------------------------------------------------------------------------

def _check_stage_isolation(fname: str, stage_dir: str, _unused_content: str = "") -> int:
    """Verify the file prefix matches its stage directory.

    Convention:
      extracted/  → filenames start with 'w' (worker output)
      refined/    → filenames start with 'r' (refined output)

    Returns 0 when the prefix matches; 1 otherwise.
    """
    if stage_dir == "extracted" and fname.startswith("w"):
        return 0
    if stage_dir == "refined" and fname.startswith("r"):
        return 0
    # Other stage directories pass through without a check for now.
    return 1


def _check_glued_headings(content: str) -> int:
    """Count level-3 headings whose next line is NOT blank.

    A glued heading looks like:

        ### Some Title
        Content starts immediately...

    The correct form inserts a blank line:

        ### Some Title

        Content follows after a blank line.

    The regex matches a ### heading line followed by a non-blank, non-heading,
    non-code-fence line on the very next row.  The character class excludes
    newlines, hash marks, whitespace, pipe characters, backticks, angle
    brackets, and hyphens — if the next line starts with any of those it is
    either another heading, a code fence, a table, a list item, or a blank
    line, none of which constitute a "glued" heading.
    """
    # Character-by-character explanation of the negated class:
    #   \n  — newline (blank line → not glued)
    #   #   — hash (another heading → not glued)
    #   \s  — any whitespace (blank/indented → not glued)
    #   |   — pipe (table row → not glued)
    #   `   — backtick (code fence → not glued)
    #   >   — blockquote → not glued
    #   -   — list item or horizontal rule → not glued
    pattern = r"### [^\n]+\n[^\n#\s|`>\-]"
    matches = re.findall(pattern, content)
    return len(matches)


# ---------------------------------------------------------------------------
# Core scanning logic
# ---------------------------------------------------------------------------

def check_all(
    root: str,
    stages: Optional[List[str]] = None,
    rail_filter: Optional[List[str]] = None,
    fact_checks: Optional[List[dict]] = None,
) -> dict:
    """Run all rail checks against every .md file in the selected stage directories.

    Parameters
    ----------
    root : str
        Project root directory.
    stages : list[str] or None
        Stage directory names to scan (e.g. ["extracted", "refined"]).
        When None, defaults to ["extracted", "refined"].
    rail_filter : list[str] or None
        Rail keys to run.  When None, all rails run.  Use this to focus on a
        subset during development (e.g. ["R2-Naming", "R5-Headings"]).
    fact_checks : list[dict] or None
        Fact-check rules.  When None, DEFAULT_FACT_CHECKS is used.

    Returns
    -------
    dict with keys:
      files       — total .md files scanned
      passed      — files with zero issues
      issues      — total issue count across all files
      issue_list  — list of human-readable issue strings
      rail_stats  — dict of rail_key → count of issues found
      file_stats  — dict of relpath → list of issue strings
    """
    ste_code = ste_code_dir(root)

    if stages is None:
        stages = ["extracted", "refined"]

    if fact_checks is None:
        fact_checks = DEFAULT_FACT_CHECKS

    rails = _build_rails(fact_checks)

    # Filter rails to only the requested subset.
    if rail_filter is not None:
        rails = {k: v for k, v in rails.items() if k in rail_filter}
        if not rails:
            print(
                "ERROR: --rails filter matched zero rails.  "
                f"Available: {', '.join(sorted(_build_rails(fact_checks).keys()))}",
                file=sys.stderr,
            )
            sys.exit(2)

    issues: list[str] = []
    rail_stats: dict[str, int] = {k: 0 for k in rails}
    file_stats: dict[str, list[str]] = {}
    stats = {"files": 0, "passed": 0, "issues": 0}

    for stage_dir in stages:
        dir_path = os.path.join(ste_code, stage_dir)
        if not os.path.isdir(dir_path):
            print(
                f"WARNING: stage directory not found — skipped: {dir_path}",
                file=sys.stderr,
            )
            continue

        for fname in sorted(os.listdir(dir_path)):
            if not fname.endswith(".md"):
                continue

            fpath = os.path.join(dir_path, fname)
            relpath = f"{stage_dir}/{fname}"
            stats["files"] += 1
            file_ok = True
            file_issues: list[str] = []

            # ── R2: Naming check (operates on filename, not content) ──
            if "R2-Naming" in rails:
                if rails["R2-Naming"]["check"](fname):
                    msg = f"🔴 {relpath}: R2 — {rails['R2-Naming']['desc']}"
                    issues.append(msg)
                    file_issues.append(msg)
                    rail_stats["R2-Naming"] += 1
                    stats["issues"] += 1
                    file_ok = False

            # ── Read file content ──
            try:
                with open(fpath, encoding="utf-8") as fh:
                    content = fh.read()
            except (OSError, UnicodeDecodeError) as exc:
                msg = f"🔴 {relpath}: READ-ERROR — cannot read file ({exc})"
                issues.append(msg)
                file_issues.append(msg)
                stats["issues"] += 1
                file_ok = False
                file_stats[relpath] = file_issues
                continue

            # ── Content-based rail checks ──
            for rail_name, rail_def in rails.items():
                if "check" not in rail_def:
                    continue

                # R2 is handled before content-read (operates on filename).
                # R1 is handled with special context below.
                if rail_name in ("R2-Naming",):
                    continue

                # R1 receives extra context (filename + stage directory).
                if rail_name == "R1-Stage-Isolation":
                    count = rail_def["check"](fname, stage_dir, content)
                else:
                    count = rail_def["check"](content)

                if count > 0:
                    severity = "🟡"
                    desc = rail_def["desc"]
                    msg = f"{severity} {relpath}: {rail_name} — {desc} ({count}x)"
                    issues.append(msg)
                    file_issues.append(msg)
                    rail_stats[rail_name] = rail_stats.get(rail_name, 0) + count
                    stats["issues"] += 1
                    file_ok = False

            if file_ok:
                stats["passed"] += 1

            file_stats[relpath] = file_issues

    return {
        "files": stats["files"],
        "passed": stats["passed"],
        "issues": stats["issues"],
        "issue_list": issues,
        "rail_stats": rail_stats,
        "file_stats": file_stats,
    }


# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    """Produce a human-readable text report."""
    lines: list[str] = []
    lines.append(f"Files checked: {result['files']}")
    lines.append(f"Clean:        {result['passed']}")
    lines.append(f"Issues:       {result['issues']}")
    lines.append("")

    # Per-rail summary
    lines.append("Issues by Rail")
    for rail_name, count in sorted(result["rail_stats"].items()):
        if count > 0 or "UNIMPLEMENTED" not in str(count):
            marker = "⚠" if count > 0 else "✓"
            lines.append(f"  {marker} {rail_name}: {count}")
    lines.append("")

    # Per-file detail
    if result["issue_list"]:
        lines.append("Issues Found")
        for issue in result["issue_list"]:
            lines.append(f"  {issue}")
        lines.append("")
        lines.append(f"⚠️  {len(result['issue_list'])} issues need attention.")
    else:
        lines.append("✅ All files pass rails compliance.")

    return "\n".join(lines)


def format_json(result: dict) -> str:
    """Produce a machine-readable JSON report.

    Converts the internal result dict (which may contain non-serializable
    values like lambda functions in rail_stats) to plain JSON-safe types.
    """
    serializable = {
        "files": result["files"],
        "passed": result["passed"],
        "issues": result["issues"],
        "issue_list": result["issue_list"],
        "rail_stats": dict(result["rail_stats"]),
        "file_stats": dict(result["file_stats"]),
    }
    return json.dumps(serializable, indent=2)


def format_ci(result: dict) -> str:
    """Produce a minimal CI-friendly report: one issue per line, no decorations."""
    return "\n".join(result["issue_list"]) if result["issue_list"] else "OK"


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    p = argparse.ArgumentParser(
        description="STE-Code Rails Compliance Checker — scan output files against the 8 rails",
    )
    p.add_argument(
        "--root",
        default=None,
        help="Project root directory (auto-detected from script location when omitted)",
    )
    p.add_argument(
        "--stages",
        nargs="+",
        default=["extracted", "refined"],
        help="Stage directories to scan (default: extracted refined)",
    )
    p.add_argument(
        "--rails",
        nargs="+",
        default=None,
        help="Rail keys to run (default: all).  Example: --rails R2-Naming R5-Headings",
    )
    p.add_argument(
        "--format",
        choices=["text", "json", "ci"],
        default="text",
        help="Output format (default: text)",
    )
    p.add_argument(
        "--facts-config",
        default=None,
        help="Path to a JSON file with fact-check rules (default: built-in rules)",
    )
    p.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Print additional diagnostic information to stderr",
    )
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    """Entry point. Returns an exit code suitable for sys.exit()."""
    args = parse_args(argv)

    if args.verbose:
        print(f"Script location: {__file__}", file=sys.stderr)
        print(f"CLI --root:      {args.root}", file=sys.stderr)
        print(f"CLI --stages:    {args.stages}", file=sys.stderr)
        print(f"CLI --rails:     {args.rails}", file=sys.stderr)
        print(f"CLI --format:    {args.format}", file=sys.stderr)

    # Resolve paths
    root = resolve_root(args.root)
    if args.verbose:
        print(f"Resolved root:   {root}", file=sys.stderr)

    # Load fact checks
    fact_checks = load_fact_checks(args.facts_config)

    # Run checks
    result = check_all(
        root=root,
        stages=args.stages,
        rail_filter=args.rails,
        fact_checks=fact_checks,
    )

    # Format and print
    if args.format == "json":
        print(format_json(result))
    elif args.format == "ci":
        output = format_ci(result)
        if output:
            print(output)
    else:
        print(format_text(result))

    # Exit code: 0 = clean, 1 = warnings only, 2 = blocking errors
    if result["issues"] == 0:
        return 0

    # Check whether any issue is an error (🔴) vs warning (🟡).
    has_errors = any("🔴" in iss for iss in result["issue_list"])
    return 2 if has_errors else 1


if __name__ == "__main__":
    sys.exit(main())
