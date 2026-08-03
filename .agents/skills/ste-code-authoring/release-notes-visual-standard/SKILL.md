---
name: release-notes-visual-standard
description: Normalize notes to a consistent markdown visual standard.
category: ste-code-authoring
---

# Release-notes visual standard

The working tree holds a family of release notes under
`.agents/tmp/remote-notes/` (also `ste-code/`): `STANDARD-1.x`,
`REPOSITORY-1.x`, `FLAVOR-1.x`. These live in gitignored scratch space
(`.agents/tmp/*` — see `.gitignore`) and are NOT shipped in the repository; they
are located/fetched per run, not version-controlled. When the user asks to bring
two or more of them to a _consistent visual standard_, the goal is formatting
parity, NOT content change. Every number, claim, filename, commit hash, and the
STANDARD/REPOSITORY split must survive intact.

## The visual standard (apply identically to every file)

1. **One idea/fact per line.** Long sentences may be split across lines/bullets.
   Blank line between every major section.
2. **Heading hierarchy.** `#` title → `##` top sections → `###` subsections.
   Keep the same section ORDER and the same heading WORDING across both files
   where the content parallels (e.g. both get a `## Headline stats`, a thematic
   chapter block, a `## Contradictions resolved`/`-corrected` table,
   `## Version boundary`).
3. **Element choice by data shape:**
    - Tables for anything tabular (stats, corrections, version deltas).
    - Bullets for enumerated facts or lists of items.
    - `>` **Blockquotes** for (a) the tag-family scope note and (b) key caveats
      ("be precise about…", load-bearing omissions).
4. **Preserve every fact.** Do NOT add, remove, or rephrase facts. You may only
   reorganize how they are presented. If the source splits one paragraph of
   claims, split it into bullets — but move nothing and alter no wording.
5. **Maximize scannability** without losing the source's precision.

## Workflow (incremental — never one giant write_file)

1. **Resolve the filenames first.** See Pitfall below — the on-disk name uses a
   hyphen and no `v` (`STANDARD-1.0.0.md`), even though prose/tags say
   `STANDARD-v1.1.0`.
2. **Read both source files fully** (`read_file`) before writing anything.
3. **Write chunk 1** to a `-REWRITE.md` working copy: title + tag-family
   blockquote + headline-stats table.
4. **`read_file` → `patch` (replace mode)** to append the next 1–2 sections.
   Repeat until the file is complete. Patch is safer than re-`write_file` (which
   overwrites the whole file).
5. **Verify** with terminal `wc -l` and `grep -nE '^#'` to confirm heading
   parity and that no section was dropped.

## Pitfalls

- **Filename vs tag mismatch.** Task text "STANDARD-v1.0.0" does NOT mean a file
  `STANDARD-v1.0.0.md`. On disk these are `STANDARD-1.0.0.md`,
  `REPOSITORY-1.1.0.md`, etc. (hyphen, no `v`). If `read_file` returns "File not
  found" for the `v`-named path, `search_files` the directory for `STANDARD*` /
  `REPOSITORY*` to find the real hyphenated file. Write the rewrite to a
  separate `-REWRITE.md` file; do not overwrite the source in place until
  verified.
- **Do not "fix" the source's own inconsistencies.** The v1.0.0/v1.1.0 notes
  deliberately preserve contradictory counts (e.g. `0cf59e4` used as both the
  REPOSITORY tag and, in the v1.1.0 note, as the STANDARD-v1.0.0 tag). That is
  content the note is _reporting_, not an error for you to correct. Preserve
  verbatim.
- **CJK / contamination tokens are content.** Strings like `超额` and diff
  blocks (` ```diff `) must be kept exactly. They are facts the note reports.
- **Footer is per-file.** v1.0.0 carries an `*Adapted from ASD-STE100…*` footer;
  v1.1.0 does not. Do not add a footer to a file that lacks one, and do not drop
  one that has it.

## References

- `references/visual-standard-template.md` — annotated skeleton of the target
  shape (tag-family blockquote → headline table → thematic chapters →
  contradictions table → version boundary) with the element-choice rules inline.
