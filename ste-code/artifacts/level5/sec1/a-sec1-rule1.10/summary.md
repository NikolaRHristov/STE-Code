# Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

## Original Rule Summary

Do not use regional, slang, or jargon words as technical nouns. There can be technical words that only persons in confined regions or geographical areas use. These words are not easy to understand for persons who are from a different region or area. If only a small number of persons understand a word, it will cause confusion and non-effective communication.

## STE-Code Adaptation

Do not use regional, slang, or jargon words as code-domain technical nouns. There can be technical words that only persons in confined communities or specific programming language ecosystems use. These words are not easy to understand for developers who are from a different background or use a different technology stack. Code documentation is read by developers with diverse backgrounds, including junior developers, developers from different language communities, and non-native English speakers. Use well-known, approved words that are clear to a global audience.

## Examples

> **Non-STE:** Remove all the cruft from the legacy module.
>
> **STE:** Remove all the unnecessary code from the legacy module.

> *Principle: P10. "Cruft" is hacker jargon that means "poorly designed or unnecessary code." Its meaning is not immediately clear to readers who are not familiar with hacker culture. The STE version uses the approved words "unnecessary code," which are clear to all readers.*

> **Non-STE:** Bikeshedding delayed the API design by two weeks.
>
> **STE:** Unnecessary discussion about small details delayed the API design by two weeks.

> *Principle: P10. "Bikeshedding" is jargon from Parkinson's Law of Triviality. It means "spending disproportionate time on trivial details." Only developers familiar with the history of this term understand it. The STE version uses the approved adjective "unnecessary" with the noun "discussion" to describe the actual activity without metaphor.*

> **Non-STE:** Take time to grok the authentication module before making changes.
>
> **STE:** Take time to understand the authentication module before making changes.

> *Principles: P1, P10. "Grok" is a term from Robert Heinlein's 1961 novel "Stranger in a Strange Land." It entered hacker vocabulary through early computing culture. It means "to understand deeply and intuitively." The approved verb "understand" is clear to all readers. "Grok" is not an approved word and its literary origin makes it opaque to developers unfamiliar with the reference.*

## Principles Applied

- **P1:** Use approved words from the controlled terminology ("understand" instead of "grok")
- **P10:** No slang, jargon, or regional terms ("cruft," "bikeshedding," "grok" are all removed)
