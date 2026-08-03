---
name: ste-code-release-notes
description:
    Reformat STE-Code release notes to the house visual standard.
---

# STE-Code Release Notes - House Visual Standard

## Trigger

- "Rewrite / normalize / reformat the REPOSITORY/STANDARD/FLAVOR vX.Y.Z notes to
  a consistent standard"
- "Make these release notes match" / "same visual standard as the other note"
- Any task whose goal is structure/whitespace only, with **content preserved**.

## Hard rules (content preserved)

Never rewrite sentences, never add facts, never drop a number, commit hash,
filename, or tag. The job is **structure and whitespace only**:

- All measurements, counts, hashes (`0cf59e4`, `830d06c`…), percentages, and the
  STANDARD/REPOSITORY split stay verbatim.
- Keep every caveat and "framing boundary" warning from the source.

## The visual standard

1. **One idea / fact per line.** Blank line between every major section, and
   between a heading and its first paragraph (also blank lines around tables and
   lists).
2. **Heading hierarchy:** `#` = title, `##` = top section, `###` = subsection.
3. **Parallel structure across versions.** Same section ORDER and same heading
   WORDING in every file where the content parallels, so the notes read as
   siblings:
    - `# STE-Code REPOSITORY vX.Y.Z`
    - `> **Tag family.** …` blockquote at the very top (the scope note).
    - `## Headline stats (all at \`<hash>\`)` - a table.
    - thematic `##` chapters (these differ per version - that is fine).
    - `## Contradictions resolved (repository view)` (or the v1.0.0 equivalent
      `## Known repository-level limitations`) - a table, near the end.
    - `## Version boundary` - bullets.
4. **Choose the right container:**
    - TABLE for tabular / comparison data (stats, commit ranges,
      contradictions).
    - Bullets (`-`) for enumerated facts.
    - Numbered list ONLY for genuine ordered steps (e.g. a model-arc timeline,
      migration fix sequence).
    - BLOCKQUOTE (`>`) for the tag-family scope note AND for key caveats /
      framing boundaries (e.g. "born, not hardened").
5. **Keep these structural anchors intact** - they appear in both notes and a
   future reviewer expects them: the tag-family blockquote, the headline-stats
   table, the contradictions/limitations table, the version-boundary section. If
   a version lacks one (v1.0.0 has no contradictions table), use its natural
   equivalent (Known repository-level limitations) as a table so the two stay
   visually parallel.

## Write-incremental technique (avoids truncation)

Large markdown files read back truncated at ~100 lines, which corrupts a
single-shot `write_file` + later `read_file` verification. Instead:

1. `write_file` the FIRST chunk only: title + tag-family blockquote +
   headline-stats table (≈10-30 lines).
2. `read_file` the file to confirm it landed.
3. `patch` (mode=replace, match the last line) to APPEND the next 1-2 sections.
4. Repeat until done. Small, reviewable diffs and no truncation.

For a 2-file batch, do file A fully (chunk by chunk) then file B - or
interleave; either way each `write_file`/`patch` stays under the truncation
boundary.

## Verification

- Line counts: both rewritten files land near 90-100 lines (dense but
  untruncated). Report both counts to the user.
- Diff-check: every hash, percentage, and filename from the source is present in
  the rewrite. No new sentences introduced.
- Structure check: tag-family blockquote at top, headline-stats table present,
  contradictions/limitations table present, `## Version boundary` last.

## Pitfalls

- Do NOT flatten a table into prose "for readability" - tables are the standard
  for stats and contradictions.
- Do NOT move the tag-family note out of the top blockquote; v1.1.0 already uses
  a top blockquote, and v1.0.0 must be converted to match.
- Do NOT "improve" wording. Content-preservation is the entire point; the parent
  grades structure/whitespace only.
- Watch the ~100-line read-back truncation: a single `write_file` of a 130-line
  note will come back cropped, silently losing the tail. Write incrementally.
