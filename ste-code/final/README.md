# STE-Code — Consolidated Standard (`final/`)

STE-Code is a controlled-language variation of ASD-STE100 for software
documentation. This `final/` directory is the **canonical enriched standard**
that every downstream artifact is built from.

## Contents

- `rules/` — **56 adapted rule files** across 9 sections (Sections 1–9), plus:
  - `a-categories.md` — rule categories
  - `a-dictionary.md` — approved-word dictionary excerpt
- `extensions/` — code-domain vocabulary + anti-pattern gap fillers
  (`nouns.md`, `verbs.md`, `adjectives.md`, `verb-examples.md`,
  `anti-patterns.md`, `domains.md`, plus their `.json` forms)
- `reference-catalogue.md` — vendor / community references the standard draws on
- `provenance.md` — stage-by-stage audit trail (extraction → refinement →
  grouping → adaptation → finalize)

## Use

Load `rules/` as the canonical rule set and `extensions/` as the approved
vocabulary. `ste-code/artifacts/` is the LLM-distilled, deployable form of this
directory — regenerate it with `finalize_artifacts.py` rather than editing it
by hand.
