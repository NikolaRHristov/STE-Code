# Rule 2.1 — Multi-word Nouns (Maximum Three Words)

## Original Rule Summary

Rule 2.1 limits multi-word nouns — chains of nouns and adjectives that function as a single part of speech — to a maximum of three words. Long multi-word nouns create ambiguity because the reader must infer the relationship between each adjacent pair of words, and the head noun (the last word) is buried under many modifiers. Non-native English readers face an additional burden because many languages place the head noun first, not last. To help the reader, break multi-word nouns longer than three words into smaller units connected by prepositions such as "of," "for," "in," and "on."

## STE-Code Adaptation

Rule 2.1 in STE-Code applies the three-word limit to all code documentation prose — README files, API docs, docstrings, commit messages, error messages, and configuration descriptions. Code documentation frequently stacks technical nouns into long chains ("database connection pool timeout configuration," "API gateway request rate limiter") that are hard to parse, especially for non-native English readers. The adaptation breaks these chains into smaller multi-word noun units connected by prepositions, placing the head noun of each unit last. This rule applies to documentation prose only, not to code identifiers (variable names, function names, class names) inside backticks — those follow programming-language naming conventions, not English grammar rules.

## Example Pairs

> **Non-STE:** The project implements a distributed event sourcing aggregate root snapshot storage strategy.
>
> **STE:** The project implements a strategy for storage of snapshots of the aggregate roots in a distributed event sourcing system.
>
> *(P1 applied: "event sourcing," "aggregate root," and "distributed" are approved technical nouns; P9 applied: the 7-word multi-word noun is restructured into short units of 1 word, 1 word, 1 word, and 3 words, each at or below the limit)*

>
> **Non-STE:** feat: add GraphQL query response cache eviction strategy configuration
>
> **STE:** feat: add configuration of the strategy for eviction of the cache of the GraphQL query response
>
> *(P5 applied: "GraphQL" is a technical code noun; P9 applied: the 6-word chain is broken into units connected by "of" and "for," with each unit at most 3 words; P11 applied: "strategy" and "configuration" are used consistently as their approved noun forms)*

>
> **Non-STE:** ERROR: Authentication token validation failure recovery procedure initialization failed.
>
> **STE:** ERROR: Initialization of the procedure for recovery from failure of the validation of the authentication token failed.
>
> *(P2 applied: "recovery" is used only as a noun; P3 applied: the head noun "initialization" is placed first so the reader immediately knows what failed; P9 applied: the 7-word multi-word noun is decomposed into four preposition-connected units of 1, 2, 1, and 3 words)*

## Principles Applied

**P9** — Use short, clear technical nouns. This is the primary principle for Rule 2.1. A multi-word noun must not exceed three words. When a concept requires more than three words, break it into smaller multi-word noun units connected by prepositions ("of," "for," "in," "on," "from," "to"). Each preposition-separated group is an independent unit that must itself be three words or fewer. The goal is clarity, not minimal word count — a broken chain with prepositions will have more total words than the original noun chain, and this is acceptable because each unit is independently parseable.

**P3** — Keep sentences short and separate ideas. Long multi-word nouns force the reader to process many modifiers before reaching the head noun. Breaking a long multi-word noun into smaller units with prepositions moves the head noun of each unit earlier, making the sentence structure clearer. This aligns with P3's directive to separate ideas — each preposition-connected unit expresses one relationship (ownership, purpose, source, location) rather than burying all relationships in an undifferentiated chain.

**P1** — Use approved words from the controlled terminology. Every word within a multi-word noun must be an approved STE-Code word (Rule 1.1) or a registered code-domain technical noun from an approved category (Rule 1.5). When breaking a long multi-word noun, verify that each component word — including the prepositions — is approved. Non-approved synonyms within a multi-word noun (e.g., "fetch" instead of "acquisition") violate Rule 1.1 even if the structure follows Rule 2.1.

**P11** — Use one term per concept consistently. Within a document, the same multi-word noun structure must appear everywhere. Do not write "configuration of the timeout" in one section and "timeout configuration" in another for the same concept. The broken form established on first use becomes the canonical representation of that concept for the remainder of the document. Consistency in multi-word noun structure is part of the one-term-per-concept principle.
