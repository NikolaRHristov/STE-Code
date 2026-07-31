#!/usr/bin/env python3
"""Phase C Runner — Semantic Grouping Worker.

Reads all 109 extracted worker outputs and groups them into semantically
coherent chunks based on section type, for downstream refinement/adaptation.

Usage: python3 .agents/tools/runners/phase-c-run.py [--agent hermes|claude|codex] [--model MODEL] [--dry-run]

The agent receives the full prompt via stdin and the wrapper writes output.
This runner uses os.execvpe to self-exec into the Hermes runtime.
"""
import os, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command

EXTRACTED_DIR = PROJECT / "ste-code" / "extracted"
GROUPED_DIR = PROJECT / "ste-code" / "grouped"
MANIFEST_PATH = PROJECT / "spec" / "issue-09-2025" / "page-dir" / "MANIFEST.md"
SECTION_TYPES_PATH = PROJECT / ".agents" / "references" / "section-types.md"
WORKER_GRID_PATH = PROJECT / ".agents" / "references" / "worker-grid.md"


def build_grouping_prompt():
    """Build the prompt for the grouping agent."""
    # Read section types reference
    section_types = ""
    if SECTION_TYPES_PATH.exists():
        section_types = SECTION_TYPES_PATH.read_text()

    # Read manifest (first 30 lines for context)
    manifest_preview = ""
    if MANIFEST_PATH.exists():
        lines = MANIFEST_PATH.read_text().splitlines()
        manifest_preview = "\n".join(lines[:35])

    # List all extracted files with sizes
    file_list = []
    if EXTRACTED_DIR.exists():
        for f in sorted(EXTRACTED_DIR.glob("*.md")):
            file_list.append(f"  - {f.name} ({f.stat().st_size} bytes)")
    file_list_str = "\n".join(file_list) if file_list else "  (no files found)"

    prompt = f"""You are the STE-Code Grouping Worker (Phase C). Your task is to take 109 extracted spec page files and re-group them into semantically coherent chunks.

## Context

The ASD-STE100 Issue 9 spec has 434 pages divided into 8 section types:
- FRONT (pages 1-12): Cover, copyright, change history, highlights
- TOC (pages 13-16): Table of contents
- INDEX (pages 17-24): Subject-to-rule mapping
- INTRO (pages 25-42): How to use the standard
- RULES (pages 43-128): The 53 writing rules with STE/non-STE examples
- CATEGORIES (pages 47-66): 19 technical name categories
- DICT (pages 129-360): Dictionary entries (Word (POS), APPROVED/UNAPPROVED)
- APPENDIX (pages 361-434): Flowcharts, change forms, index

Each extracted file contains 4 consecutive pages: `{file_list_str}`

## Grouping Rules
1. NEVER break a dictionary entry across group boundaries
2. NEVER break a rule example pair (STE/non-STE) across groups
3. NEVER break a table — use <!-- TABLE CONTINUES ON NEXT PAGE --> markers
4. Group ALL dictionary pages into alphabetical sub-groups (A-B, C-D, etc.)
5. Group ALL rules pages by rule section (Sec 1, Sec 2, ..., Sec 9)
6. Each group file starts with a metadata header comment

## Output Format
For each group, create a file in `ste-code/grouped/`:

```markdown
<!-- GROUP: <NNN>-<semantic-label> -->
<!-- PAGES: <start>-<end> -->
<!-- SECTION: <type> -->
<!-- WORKERS: <comma-separated list> -->

# <Human-readable group label>

## Source Pages
<!-- This group contains pages <start>-<end> from workers <list> -->

<concatenated content from source pages, verbatim>
```

## Steps
1. Read all 109 extracted files
2. Parse the page number from each file header (`# Page N of 434`)
3. Read the MANIFEST to map page positions to page IDs
4. Classify each page by section type using the section-types table
5. Group pages into ~15-25 logical chunks following the grouping rules
6. For each group: concatenate the verbatim page content
7. Write each group to `ste-code/grouped/group-NNN-<label>.md`
8. Write `ste-code/grouped/groups-manifest.json` with the full mapping

## Manifest JSON Format
```json
{{
  "groups": [
    {{
      "group_id": "001-front-matter",
      "pages": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
      "section": "FRONT",
      "workers": ["W001", "W002", "W003"],
      "file": "group-001-front-matter.md",
      "pages_text": "pages 1-12"
    }}
  ],
  "total_pages": 434,
  "total_groups": 0
}}
```

## Quality Gate
- Every page (1-434) must appear in exactly one group
- No dictionary entry should span a group boundary
- No rule example pair should span a group boundary

Output the group files and manifest. Do NOT create commentary — just read the files and write the grouped output."""

    # Embed the authoritative grouping skill so the worker honors the pipeline
    # rules (edit the SKILL.md to change behavior, not this runner).
    try:
        import importlib.util as _ilu
        _sp = _ilu.spec_from_file_location(
            "skill_prompt", str(PROJECT / ".agents" / "tools" / "lib" / "skill_prompt.py"))
        _m = _ilu.module_from_spec(_sp)
        _sp.loader.exec_module(_m)
        prompt += _m.skill_section("grouping")
    except Exception:
        pass

    return prompt, GROUPED_DIR


def main():
    agent = None
    model = None
    dry_run = False

    for i, arg in enumerate(sys.argv):
        if arg == "--agent" and i + 1 < len(sys.argv):
            agent = sys.argv[i + 1]
        elif arg == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
        elif arg == "--dry-run":
            dry_run = True

    prompt, _ = build_grouping_prompt()
    print(f"Grouping prompt: {len(prompt)} chars", flush=True)

    if dry_run:
        print("DRY RUN — would execute grouping agent")
        print(f"Input: {EXTRACTED_DIR}")
        print(f"Output: {GROUPED_DIR}")
        return

    # Use the standard launch pattern
    tmp = PROJECT / ".agents" / "tmp" / "phase-c-prompt.txt"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(prompt)

    cmd, env = get_agent_command(agent=agent, model=model,
                                  cwd=PROJECT, prompt_file=str(tmp))
    os.execvpe(cmd[0], cmd, env)


if __name__ == "__main__":
    main()