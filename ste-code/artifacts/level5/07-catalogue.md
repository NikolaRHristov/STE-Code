# Level 5 — Reference Catalogue (vendor / community)

This document catalogues the **external references** that informed STE-Code's
controlled vocabulary. These references are **NOT part of the standard**. They
are vendor and community sources that the dictionary and rules were checked
against. Use them when you need to resolve a word, a term, or a style question
that the STE-Code rules and dictionary do not settle.

Status note for readers: each entry is either bundled locally as a mirror under
`.agents/reference/` (type `page` or `raw`) or is a live external pointer (type
`pointer`). Local mirrors are stored outside `final/` per project rule, so they
do not ship inside the standard itself — only this catalogue does.

How to use this catalogue:
- Need a style decision (voice, capitalization, sentence length)? → Style guides.
- Need a definition of a code-domain term (API, commit, idempotent)? → Glossaries.
- Need to confirm a word is a real English word / spelled right? → Word lists.
- Need to automate checking in CI? → Linters.
- Need to discover more sources? → Pointer / topic indexes.

## Style guides

These set the **voice and conventions** STE-Code inherits: short sentences,
active voice, plain words, consistent terminology.

| Reference | Type | Source | Use for |
|---|---|---|---|
| Microsoft Writing Style Guide | page | [learn.microsoft.com](https://learn.microsoft.com/en-us/style-guide/welcome/) (mirror: `.agents/reference/microsoft-writing-style-guide.md`) | Voice, capitalization, tone, word choice |
| MicrosoftDocs/microsoft-style-guide (GitHub source) | page | [github.com/MicrosoftDocs/microsoft-style-guide](https://github.com/MicrosoftDocs/microsoft-style-guide) (mirror: `.agents/reference/microsoft-style-guide-github.md`) | Same content as above, source repo |
| Google Style Guides | page | [google.github.io/styleguide](https://google.github.io/styleguide/) (mirror: `.agents/reference/google-style-guides.md`) | Technical writing conventions, API docs, capitalization |
| DevOps Style Guide Glossary | page | [tydukes.github.io/coding-style-guide/glossary](https://tydukes.github.io/coding-style-guide/glossary/) (mirror: `.agents/reference/devops-style-guide-glossary.md`) | DevOps and coding style terms |

## Code-domain glossaries

These supply **definitions of terms used in software and code documentation**.
Prefer them over general dictionaries when a word has a code-specific meaning.

| Reference | Type | Source | Use for |
|---|---|---|---|
| Kong/apiglossary | page | [github.com/Kong/apiglossary](https://github.com/Kong/apiglossary) (mirror: `.agents/reference/kong-apiglossary.md`) | API and REST terminology |
| dwyl/technical-glossary | raw | [raw.githubusercontent.com/dwyl/technical-glossary/main/README.md](https://raw.githubusercontent.com/dwyl/technical-glossary/main/README.md) (mirror: `.agents/reference/dwyl-technical-glossary.txt`) | Broad technical terms |
| jvalentino/glossary | page | [github.com/jvalentino/glossary](https://github.com/jvalentino/glossary) (mirror: `.agents/reference/jvalentino-glossary.md`) | Software engineering terms |
| GitHub Official Glossary | page | [docs.github.com/.../github-glossary](https://docs.github.com/en/get-started/learning-about-github/github-glossary) (mirror: `.agents/reference/github-official-glossary.md`) | Git and GitHub terms (commit, fork, pull request) |

## Word lists (spelling & allowed vocabulary)

These are the **authority for whether a word is a real English word and how it is
spelled**. STE-Code also uses them to seed and verify its approved dictionary.

| Reference | Type | Source | Use for |
|---|---|---|---|
| ryanwi software-terms.dic | raw | [gist.githubusercontent.com/ryanwi/6135845/raw/software-terms.dic](https://gist.githubusercontent.com/ryanwi/6135845/raw/software-terms.dic) (mirror: `.agents/reference/ryanwi-software-terms.txt`) | Software-domain word list |
| en-wl/wordlist (SCOWL) | page | [github.com/en-wl/wordlist](https://github.com/en-wl/wordlist) (mirror: `.agents/reference/en-wl-wordlist.md`) | Spell-check word lists (many sizes/levels) |
| MichaelWehar 5000-more-common | raw | [raw.githubusercontent.com/MichaelWehar/Public-Domain-Word-Lists/master/5000-more-common.txt](https://raw.githubusercontent.com/MichaelWehar/Public-Domain-Word-Lists/master/5000-more-common.txt) (mirror: `.agents/reference/michaelwehar-5000-common.txt`) | Common-word supplement |
| OpenSTE.org | pointer | [openste.org](https://openste.org/) | Reference implementation of Simplified Technical English |
| dwyl/english-words (POINTER) | pointer | [raw.githubusercontent.com/dwyl/english-words/master/words.txt](https://raw.githubusercontent.com/dwyl/english-words/master/words.txt) | Large general English word list |
| freeDictionaryAPI english.txt (POINTER) | pointer | [raw.githubusercontent.com/meetDeveloper/freeDictionaryAPI/master/meta/wordList/english.txt](https://raw.githubusercontent.com/meetDeveloper/freeDictionaryAPI/master/meta/wordList/english.txt) | General English word list |

## Linters (automated checking)

Use these to **enforce STE-Code-like rules in CI** (prose lints, not compiler
errors). They are the basis for the style checks STE-Code recommends.

| Reference | Type | Source | Use for |
|---|---|---|---|
| Vale linter | page | [github.com/errata-ai/vale](https://github.com/errata-ai/vale) (mirror: `.agents/reference/vale.md`) | Pluggable prose linter for docs/CI |
| errata-ai/Microsoft | page | [github.com/errata-ai/Microsoft](https://github.com/errata-ai/Microsoft) (mirror: `.agents/reference/vale-microsoft.md`) | Microsoft style rules for Vale |
| errata-ai/Google | page | [github.com/errata-ai/Google](https://github.com/errata-ai/Google) (mirror: `.agents/reference/vale-google.md`) | Google style rules for Vale |
| errata-ai/write-good | page | [github.com/errata-ai/write-good](https://github.com/errata-ai/write-good) (mirror: `.agents/reference/vale-write-good.md`) | write-good style rules for Vale |

## Discovery pointers (topic indexes)

Starting points for **finding more word lists and glossaries** if the above do
not cover a term.

| Reference | Type | Source | Use for |
|---|---|---|---|
| GitHub topic: word-list | pointer | [github.com/topics/word-list](https://github.com/topics/word-list) | More word-list repositories |
| GitHub topic: glossary-terms | pointer | [github.com/topics/glossary-terms](https://github.com/topics/glossary-terms) | More glossary repositories |
| GitHub topic: technical-writing | pointer | [github.com/topics/technical-writing](https://github.com/topics/technical-writing) | More technical-writing resources |
| GitHub topic: controlled-vocabulary | pointer | [github.com/topics/controlled-vocabulary](https://github.com/topics/controlled-vocabulary) | More controlled-vocabulary resources |
