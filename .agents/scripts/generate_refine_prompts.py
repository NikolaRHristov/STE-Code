#!/usr/bin/env python3
"""Generate refinement worker prompts for all extracted specification files.

This script reads extracted STE-Code specification files and produces
a refinement prompt for each one. Each prompt instructs a worker to
reformat the extracted content into standardized markdown following
nine refinement rules.

Usage:
    python generate_refine_prompts.py
    python generate_refine_prompts.py --input-dir /path/to/extracted
    python generate_refine_prompts.py --output-dir /path/to/prompts-refine
    python generate_refine_prompts.py --force
    python generate_refine_prompts.py --dry-run
"""

import argparse
import logging
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Logging ───────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    stream=sys.stderr,
)
log = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

# Expected filename pattern: wNNN-pSTART-END.md
#   wNNN  = worker number (three digits)
#   p     = page marker
#   START = first page number
#   END   = last page number
FILENAME_RE = re.compile(
    r"^w(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$"
)

# Prompt file naming: rNNN-prompt.txt where NNN matches the worker number.
PROMPT_NAME_TEMPLATE = "r{worker}-prompt.txt"

# ── Path resolution ───────────────────────────────────────────────────────────

def _resolve_project_root() -> Path:
    """Auto-detect the project root directory from the location of this script.

    Returns:
        Path to the project root (two levels up from .agents/scripts/).

    Raises:
        RuntimeError: If the expected directory structure is not found.
    """
    script_dir = Path(__file__).resolve().parent          # .agents/scripts/
    project_root = script_dir.parent.parent               # project root

    # Sanity check: the root should contain these known directories.
    expected_markers = ["ste-code", ".agents"]
    missing = [m for m in expected_markers if not (project_root / m).exists()]
    if missing:
        raise RuntimeError(
            f"Cannot detect project root from {script_dir}. "
            f"Missing expected directories: {', '.join(missing)}. "
            f"Use --input-dir and --output-dir to set paths manually."
        )
    return project_root


def _resolve_default_dirs() -> Tuple[Path, Path]:
    """Return default input and output directory paths.

    Returns:
        Tuple of (extracted_dir, prompts_dir) resolved relative to
        the auto-detected project root.
    """
    root = _resolve_project_root()
    extracted = root / "ste-code" / "extracted"
    prompts = root / "ste-code" / "prompts-refine"
    return extracted, prompts

# ── Validation ────────────────────────────────────────────────────────────────

def _validate_directory(path: Path, label: str) -> None:
    """Check that a directory exists and is readable. Exit on failure.

    Args:
        path: The directory path to validate.
        label: Human-readable label for error messages (e.g. 'input').
    """
    if not path.exists():
        log.error("%s directory does not exist: %s", label.capitalize(), path)
        sys.exit(1)
    if not path.is_dir():
        log.error("%s path is not a directory: %s", label.capitalize(), path)
        sys.exit(1)
    if not os.access(path, os.R_OK):
        log.error("%s directory is not readable: %s", label.capitalize(), path)
        sys.exit(1)


def _ensure_directory(path: Path, label: str) -> None:
    """Create a directory if it does not exist. Exit on permission errors.

    Args:
        path: The directory path to ensure.
        label: Human-readable label for error messages (e.g. 'output').
    """
    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        log.error(
            "Cannot create %s directory: %s — permission denied.",
            label,
            path,
        )
        sys.exit(1)
    except OSError as exc:
        log.error("Cannot create %s directory: %s — %s", label, path, exc)
        sys.exit(1)

# ── File scanning ─────────────────────────────────────────────────────────────

def _find_extracted_files(extracted_dir: Path) -> List[Path]:
    """Find all extracted specification files matching the expected pattern.

    Only files matching FILENAME_RE are returned. Backup files, temporary
    files, and non-conforming names are silently skipped with a debug log.

    Args:
        extracted_dir: Directory to scan for extracted files.

    Returns:
        Sorted list of Path objects, ordered by worker number then page range.
    """
    matched: List[Dict] = []

    try:
        all_files = os.listdir(extracted_dir)
    except PermissionError:
        log.error("Cannot read input directory: %s — permission denied.", extracted_dir)
        sys.exit(1)

    if not all_files:
        log.warning("Input directory is empty: %s", extracted_dir)
        return []

    for name in all_files:
        m = FILENAME_RE.match(name)
        if m:
            matched.append({
                "path": extracted_dir / name,
                "worker": int(m.group("worker")),
                "page_start": int(m.group("start")),
            })
        else:
            log.debug("Skipping non-conforming file: %s", name)

    # Sort by worker number, then by start page.
    matched.sort(key=lambda d: (d["worker"], d["page_start"]))
    return [d["path"] for d in matched]

# ── Prompt generation ────────────────────────────────────────────────────────

def _build_prompt(
    input_filename: str,
    output_filename: str,
    start_page: str,
    end_page: str,
) -> str:
    """Build the refinement worker prompt for a single file.

    Args:
        input_filename:  Name of the extracted input file.
        output_filename: Name of the refined output file.
        start_page:      First page number (string).
        end_page:        Last page number (string).

    Returns:
        The complete prompt string.
    """
    return f"""TASK: Reformat the extracted spec file into clean, standardized markdown following ALL 9 refinement rules below.

INPUT: ste-code/extracted/{input_filename}
OUTPUT: ste-code/refined/{output_filename}

RULES (apply in order, do not skip any):

1. PRESERVE ALL CONTENT. Never delete a single word, number, example, or table cell.

2. HEADINGS: Use # for page header, ## for sections, ### for rules, #### for dictionary entries. Remove ### from proper names like ASD-STE100.

3. TABLES: Convert all tables to clean markdown format. Align columns. Add missing headers. Merge cells split by PDF extraction.

4. STE/NON-STE: Format ALL example pairs as:
   > **STE:** [text]
   > **Non-STE:** [text]
   Separate merged examples into individual pairs.

5. CODE: Wrap code snippets in ```language fences.

6. DICTIONARY: Format each entry with - list under #### heading. Separate APPROVED from UNAPPROVED entries clearly.

7. METADATA: Replace repetitive page headers with a single metadata block:
   > **Source:** ASD-STE100 Issue 9, January 2025
   > **Pages:** {start_page}–{end_page} of 434

8. LISTS: Standardize indentation. Use 1. 2. 3. for numbered, - for bullets.

9. SPACING: One blank line between sections. No triple blanks. No trailing spaces.

Output ONLY the refined markdown file. No explanations, no commentary.
"""

# ── Main logic ────────────────────────────────────────────────────────────────

def generate_prompts(
    extracted_dir: Path,
    prompts_dir: Path,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> int:
    """Generate refinement worker prompts for all extracted files.

    Args:
        extracted_dir: Directory containing extracted specification files.
        prompts_dir:   Directory where prompt files will be written.
        force:         If True, overwrite existing prompt files.
        dry_run:       If True, print what would be done without writing.

    Returns:
        Number of prompt files generated.
    """
    # Validate input.
    _validate_directory(extracted_dir, "input")
    _ensure_directory(prompts_dir, "output")

    # Find matching files.
    files = _find_extracted_files(extracted_dir)

    if not files:
        log.warning("No files matched the expected pattern (%s).", FILENAME_RE.pattern)
        log.info("Expected pattern: wNNN-pSTART-END.md  (example: w001-p1-2.md)")
        return 0

    generated = 0
    skipped = 0

    for filepath in files:
        m = FILENAME_RE.match(filepath.name)
        if not m:
            # Should never happen after filtering, but guard anyway.
            log.debug("Unexpected non-match after filtering: %s", filepath.name)
            continue

        worker = m.group("worker")
        start_page = m.group("start")
        end_page = m.group("end")

        # Build filenames.
        input_name = filepath.name
        refined_name = f"r{worker}-p{start_page}-{end_page}.md"
        prompt_name = PROMPT_NAME_TEMPLATE.format(worker=worker)

        prompt_path = prompts_dir / prompt_name

        # Idempotency: skip existing prompt files unless --force is set.
        if prompt_path.exists() and not force:
            log.info("SKIP (already exists): %s", prompt_path.name)
            skipped += 1
            continue

        # Build the prompt content.
        prompt = _build_prompt(input_name, refined_name, start_page, end_page)

        if dry_run:
            log.info("DRY-RUN would write: %s", prompt_path)
            generated += 1
            continue

        # Write the prompt file.
        try:
            with open(prompt_path, "w", encoding="utf-8") as pf:
                pf.write(prompt)
        except OSError as exc:
            log.error("Cannot write prompt file: %s — %s", prompt_path, exc)
            continue

        log.info("GENERATED: %s", prompt_path.name)
        generated += 1

    # Summary.
    log.info("── Summary ──")
    log.info("  Total input files found:  %d", len(files))
    log.info("  Prompts generated:        %d", generated)
    log.info("  Prompts skipped (idem):   %d", skipped)

    if files and generated == 0 and skipped == 0 and not dry_run:
        log.warning("No prompts were written. Check permissions and paths.")

    return generated

# ── CLI ───────────────────────────────────────────────────────────────────────

def _build_argparser() -> argparse.ArgumentParser:
    """Build and return the argument parser for this script.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Generate refinement worker prompts for extracted "
            "STE-Code specification files."
        ),
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=None,
        help=(
            "Directory containing extracted specification files. "
            "Defaults to auto-detected <project-root>/ste-code/extracted."
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help=(
            "Directory where prompt files will be written. "
            "Defaults to auto-detected <project-root>/ste-code/prompts-refine."
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing prompt files (default: skip them).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be generated without writing any files.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress informational messages; only errors go to stderr.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Parse arguments and run prompt generation.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    parser = _build_argparser()
    args = parser.parse_args(argv)

    # Adjust logging level.
    if args.quiet:
        log.setLevel(logging.WARNING)
    elif args.verbose:
        log.setLevel(logging.DEBUG)

    # Resolve directories.
    if args.input_dir and args.output_dir:
        extracted_dir = args.input_dir.resolve()
        prompts_dir = args.output_dir.resolve()
    else:
        try:
            default_extracted, default_prompts = _resolve_default_dirs()
        except RuntimeError as exc:
            log.error("%s", exc)
            return 1
        extracted_dir = args.input_dir.resolve() if args.input_dir else default_extracted
        prompts_dir = args.output_dir.resolve() if args.output_dir else default_prompts

    log.debug("Input directory:  %s", extracted_dir)
    log.debug("Output directory: %s", prompts_dir)

    generated = generate_prompts(
        extracted_dir,
        prompts_dir,
        force=args.force,
        dry_run=args.dry_run,
    )

    return 0 if generated >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
