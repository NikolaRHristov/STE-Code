# Grouping & Semantic Chunk Assembly

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to THIS skill.
> One session = one operation = one read + one write. No re-editing own output.

## Overview
Reads all 109 extracted worker outputs (`ste-code/extracted/wNNN-p*.md`), classifies each page by section type using the section-types reference, and re-groups pages into semantically coherent chunks for downstream refinement and adaptation agents.

## Input
- `ste-code/extracted/wNNN-p*.md` (109 raw extraction files)
- `spec/issue-09-2025/page-dir/MANIFEST.md` (position→page mapping)
- `references/section-types.md` (content signatures for 8 section types)

## Output
`ste-code/grouped/` directory containing:
- `group-001-front-matter.md` — FRONT matter + copyright + table of contents
- `group-002-introduction.md` — INTRO (pages 25-42)
- `group-003-rules-1.md` through `group-003-rules-9.md` — RULES section, grouped by section number
- `group-004-categories.md` — CATEGORIES (pages 47-66)
- `group-005-dict-A-C.md` through `group-005-dict-X-Z.md` — DICT entries grouped by alphabetical range
- `group-006-appendix.md` — APPENDIX (pages 361-434)

## Grouping Rules
1. **Never break a dictionary entry** — if a word's entry spans pages, group both pages together
2. **Never break a rule example pair** — if an STE/non-STE pair spans pages, keep together
3. **Never break a table** — use `<!-- TABLE CONTINUES ON NEXT PAGE -->` markers from extraction
4. **Group by logical section** — all RULES section pages grouped by rule number, all CATEGORIES grouped together, etc.
5. **Each group must have context** — include preceding section type header and metadata

## Execution Instructions

### Launch Group
```bash
python3 .agents/tools/runners/phase-c-run.py --agent hermes --model poolside/laguna-s-2.1:free --yolo
```

### What the Grouping Agent Does
1. Reads all 109 extracted files
2. For each page, determines section type (FRONT, RULES, DICT, etc.)
3. Groups pages into logical chunks (see grouping rules above)
4. Writes each group to `ste-code/grouped/` with a metadata header:
   ```markdown
   <!-- GROUP: 005-dict-A-C -->
   <!-- PAGES: 129-200 -->
   <!-- SECTION: DICT -->
   <!-- CATEGORY: A-C -->
   <!-- WORKERS: W033, W034, W035 -->
   ```
5. Writes a `groups-manifest.json` describing all groups, their pages, and worker sources

## Quality Checks
1. All 434 pages accounted for across groups (no missing, no duplicate)
2. No dictionary entry split across groups
3. No rule example pair split across groups
4. Each group > 500 bytes (empty groups are errors)
5. groups-manifest.json validates against schema

## Quality Checks (Automated)
- `python3 .agents/tools/quality/check-rails.py --dir ste-code/grouped/`
- `python3 .agents/tools/maintenance/verify-batch.sh` (updated for groups)

## Edge Cases
### EC1: Page boundary in the middle of a table
If a 4-column dictionary table spans workers W033 (pages 129-132) and W034 (pages 133-136):
- Merge the table into a single `group-005-dict-A-C.md` file
- Do NOT duplicate or truncate rows at the boundary

### EC2: Section type transition within a worker
If worker W016 (pages 61-64) contains both the end of CATEGORIES and the start of RULES:
- Split the worker's output at the section boundary
- Append page 61-63 to the CATEGORIES group
- Append page 64 to the appropriate RULES group

### EC3: Dictionary section is very large
The DICT section spans pages 129-360 (232 pages, ~58 groups of 4). Split into:
- A-B, C-D, E-F, ..., X-Z groups (26 groups for 26 letters)

## Recovery
If grouping fails for one group, the other groups remain intact. Re-launch with:
```bash
python3 .agents/tools/runners/phase-c-run.py --group 005-dict-A-C
```

## References
- Section types: `references/section-types.md`
- Page-to-worker mapping: `references/worker-grid.md`
- Formatting rails: `references/rails.md`
- Group naming convention: `group-NNN-<semantic-label>.md`