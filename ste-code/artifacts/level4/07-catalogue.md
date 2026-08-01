# Level 4 — Reference Catalogue

This slice lists the external references that informed the STE-Code controlled
vocabulary: style guides, glossaries, and word lists.

Status of these references:

- They are **not** part of the STE-Code standard. No rule in this standard is
  defined by them, and no entry here overrides a rule in Levels 1–3.
- They are **evidence sources**. When a word, spelling, or term needs a check,
  read the reference instead of guessing.
- Their local copies live in `.agents/reference/`, outside `final/`, per the
  project rule that keeps pipeline material out of the shipped standard.

How an LLM should use this slice:

- Do **not** import vocabulary from a reference directly into generated text.
  Use the approved verbs, adjectives, and domain terms in the extension
  catalogue (slice `06-extensions.md`) instead.
- Use this slice only to answer the question "where did this word come from?"
  or "is this spelling attested?" — that is, for provenance and verification.
- Treat a `pointer` entry as an address only: there is no local copy to read.

## Catalogue

Column meanings:

- **Reference** — the name of the source.
- **Type** — `page` (rendered document captured locally), `raw` (plain text or
  word-list file captured locally), `pointer` (address only, no local copy).
- **Source** — the upstream address; the link target is the local copy under
  `.agents/reference/` when one exists.

| Reference | Type | Source |
|---|---|---|
| Microsoft Writing Style Guide | page | [https://learn.microsoft.com/en-us/style-guide/welcome/](.agents/reference/microsoft-writing-style-guide.md) |
| MicrosoftDocs/microsoft-style-guide (GitHub source) | page | [https://github.com/MicrosoftDocs/microsoft-style-guide](.agents/reference/microsoft-style-guide-github.md) |
| Google Style Guides | page | [https://google.github.io/styleguide/](.agents/reference/google-style-guides.md) |
| Kong/apiglossary | page | [https://github.com/Kong/apiglossary](.agents/reference/kong-apiglossary.md) |
| dwyl/technical-glossary | raw | [https://raw.githubusercontent.com/dwyl/technical-glossary/main/README.md](.agents/reference/dwyl-technical-glossary.txt) |
| jvalentino/glossary | page | [https://github.com/jvalentino/glossary](.agents/reference/jvalentino-glossary.md) |
| GitHub Official Glossary | page | [https://docs.github.com/en/get-started/learning-about-github/github-glossary](.agents/reference/github-official-glossary.md) |
| DevOps Style Guide Glossary | page | [https://tydukes.github.io/coding-style-guide/glossary/](.agents/reference/devops-style-guide-glossary.md) |
| ryanwi software-terms.dic | raw | [https://gist.githubusercontent.com/ryanwi/6135845/raw/software-terms.dic](.agents/reference/ryanwi-software-terms.txt) |
| OpenSTE.org | pointer | [https://openste.org/](https://openste.org/) |
| en-wl/wordlist (SCOWL) | page | [https://github.com/en-wl/wordlist](.agents/reference/en-wl-wordlist.md) |
| MichaelWehar 5000-more-common | raw | [https://raw.githubusercontent.com/MichaelWehar/Public-Domain-Word-Lists/master/5000-more-common.txt](.agents/reference/michaelwehar-5000-common.txt) |
| dwyl/english-words | pointer | — |

## What each reference is good for

| Question | Read this reference |
|---|---|
| Is this sentence style acceptable in product documentation? | Microsoft Writing Style Guide; MicrosoftDocs/microsoft-style-guide |
| Is this code-comment or API-doc convention acceptable? | Google Style Guides |
| What is the accepted meaning of an API term? | Kong/apiglossary; GitHub Official Glossary |
| What is the accepted meaning of a general software term? | dwyl/technical-glossary; jvalentino/glossary |
| What is the accepted meaning of a build, deploy, or operations term? | DevOps Style Guide Glossary |
| Is this software spelling attested? | ryanwi software-terms.dic; en-wl/wordlist (SCOWL) |
| Is this a common English word, safe for a general reader? | MichaelWehar 5000-more-common; dwyl/english-words |
| What does baseline Simplified Technical English do here? | OpenSTE.org |

## Rules for using the catalogue

1. Check the STE-Code rules first. A reference never overrides Levels 1–3.
2. Check the extension catalogue next. If the word is already approved or
   already rejected there, the decision is made.
3. Only then read a reference, and read the local copy in `.agents/reference/`
   when one exists.
4. Record the reference you used when you propose a new approved term. A
   proposal with no reference is an invention and must be rejected.
5. Do not copy a reference's prose into generated documentation. Take the
   meaning, then write it in STE-Code: short sentence, approved verb, one
   instruction per sentence.
6. Where two references disagree, prefer the one closest to the domain of the
   text: style guides for prose, glossaries for terms, word lists for spelling.
