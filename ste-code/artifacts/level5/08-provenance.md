# Level 5 — Provenance

Level 5 is the full STE-Code standard: every rule, the extension vocabulary, the
reference catalogue, and provenance. This sub-document is the **provenance**
slice. It records where the content of the standard comes from, which pipeline
stage produced each part, and what is inside the standard versus what is only an
external input.

Use this file when you must answer one of these questions:

- Which directory holds the authoritative form of a rule, a dictionary entry, or
  an extension term?
- Which stage created a given file, and from what input?
- Is a word list part of STE-Code, or only a reference that informed it?

## Trust order

When two files disagree, the later stage wins:

`extracted` → `refined` → `grouped` → `adapted` → `enriched (final/rules)` → `final`

`ste-code/final/` is the authoritative form of the standard. Every earlier
directory is kept for traceability, not for reuse in generation.

External references never win. They are inputs to vocabulary work only.

## Pipeline stages

| Stage | Source dir | Role |
|---|---|---|
| A Extraction | `ste-code/extracted/` | Specification PDF to structured pages |
| B Refinement | `ste-code/refined/` | Formatted dictionary and rule markdown |
| C Grouping | `ste-code/grouped/` | Semantic slice and concatenation of pages |
| D Adaptation | `ste-code/adapted/` | Code-domain rule rewrite |
| G Enrichment | `ste-code/final/rules/` | Cross-references and traceability |
| E Extension | `ste-code/extensions/` | Code-domain vocabulary gap-fills |
| References | `.agents/reference/` | Vendor and community vocabulary (catalogued) |

The stages are consolidated into `ste-code/final/` by `assemble_final.py`.

## Stage notes

- **A Extraction** reads the source specification and writes one markdown page
  per specification page. No rewriting occurs at this stage.
- **B Refinement** applies formatting rules only. Dictionary pages become
  tables; rule pages keep the original rule text and its examples.
- **C Grouping** is deterministic. It moves bytes: it slices and concatenates
  refined pages into semantic groups. It does not generate text, so no content
  can be lost or invented here.
- **D Adaptation** re-expresses each rule in the code domain. It keeps the
  original rule statement for traceability and adds a code-domain form and
  code-domain examples.
- **G Enrichment** adds cross-references between rules and the traceability
  links back to the adapted and refined sources.
- **E Extension** adds vocabulary that the code domain needs and the source
  standard does not supply. Extension entries are marked as extensions; they are
  not presented as original rules.

## Inside and outside the standard

| Item | Location | In the standard? |
|---|---|---|
| Rules | `ste-code/final/rules/` | Yes |
| Dictionary and extension vocabulary | `ste-code/extensions/` | Yes |
| Reference catalogue | `ste-code/final/reference-catalogue.md` | Yes, as a catalogue |
| Vendor and community word lists | `.agents/reference/` | No |
| Pipeline tools, state, and logs | `.agents/` | No |

The reference catalogue is part of the standard, but the referenced material is
not. The catalogue records what informed the controlled vocabulary so that a
reader can audit a term without the standard shipping third-party content.

## Reference catalogue (summary)

These external sources inform the STE-Code controlled vocabulary. They are not
part of the standard.

| Reference | Type | Use |
|---|---|---|
| Microsoft Writing Style Guide | page | Plain-language and terminology guidance |
| MicrosoftDocs/microsoft-style-guide | page | Source form of the style guide |
| Google Style Guides | page | Code and documentation conventions |
| Kong/apiglossary | page | API terminology |
| dwyl/technical-glossary | raw | General technical terms |
| jvalentino/glossary | page | General technical terms |
| GitHub Official Glossary | page | Repository and workflow terms |
| DevOps Style Guide Glossary | page | Build, deploy, and operations terms |
| ryanwi software-terms.dic | raw | Software spelling dictionary |
| OpenSTE.org | pointer | Simplified Technical English community work |
| en-wl/wordlist (SCOWL) | page | Word-list coverage checks |
| MichaelWehar 5000-more-common | raw | Common-word frequency checks |
| dwyl/english-words | pointer | Word-list coverage checks |
| freeDictionaryAPI english.txt | pointer | Word-list coverage checks |
| Vale linter | page | Rule enforcement tooling |
| errata-ai/Microsoft | page | Vale rule set |
| errata-ai/Google | page | Vale rule set |
| errata-ai/write-good | page | Vale rule set |
| GitHub topics: word-list, glossary-terms, technical-writing, controlled-vocabulary | pointer | Discovery of further vocabulary sources |

The full catalogue, with the retrieval URL and the local cached file for each
entry, is in `ste-code/final/reference-catalogue.md`.

## Traceability contract

Every rule in `ste-code/final/rules/` can be traced back through the stages:

1. The adapted rule keeps the **original rule statement**, so a reader can
   compare the code-domain form against the source form.
2. The refined page keeps the **source page identifier**, so the adapted rule
   maps to a specific page of the source specification.
3. The extracted page is the raw form of that same page.

If a rule cannot be traced to a refined page, it is an **extension**, not an
adapted rule, and it must be labelled as such.

## Rules for an LLM that uses this file

- Cite `ste-code/final/` when you quote the standard. Do not cite
  `ste-code/extracted/`, `ste-code/refined/`, or `ste-code/grouped/`.
- Do not present an extension term as a rule from the source specification.
- Do not add a word to the controlled vocabulary because it appears in a
  reference in `.agents/reference/`. A reference is evidence, not approval.
- If a term is not in the controlled terminology and not in the extensions, say
  that it is not approved. Do not invent an entry.
