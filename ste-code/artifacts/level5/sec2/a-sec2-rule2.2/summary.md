# Rule 2.2 — Long Technical Nouns (Shorter Forms and Hyphens)

## Original Rule Summary

Rule 2.2 addresses technical nouns that exceed three words — the maximum allowed by Rule 2.1. When a technical noun has more than three words, you write it in full the first time it occurs, then use one of two methods: give a shorter form (or an approved abbreviation) for the remaining text, or use hyphens to join related words so the hyphenated group counts as one word. Do not use abbreviations for technical nouns of three words or fewer, because those already obey Rule 2.1. Do not create hyphenated groups of more than three words, and do not hyphenate words that are not related, as this changes the meaning of the multi-word noun.

## STE-Code Adaptation

Rule 2.2 applies the same two methods to code documentation for long technical nouns that cannot be broken down — formal class names, design pattern names, official API names, and names from architecture diagrams. Method 1: write the long technical noun in full the first time it occurs with an explanation, then use a shorter form or the official abbreviation in the remaining text. Method 2: use hyphens to join related words that function as a single unit within a multi-word noun, so the hyphenated group counts as one word toward the three-word limit. Do not abbreviate technical nouns that already have three words or fewer, do not hyphenate words that are not related, and do not create hyphenated groups of more than three words.

## Example Pairs

> **Non-STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler. The HTTP request pipeline middleware authentication handler must be configured with the correct credentials.
>
> **STE:** Before you run this script, configure the HTTP request pipeline middleware authentication handler (the component that checks requests in the middleware pipeline, referred to in this document as the "authentication handler"). The authentication handler must be configured with the correct credentials.

>
> *(Method 1 — Shorter form: the long technical noun "HTTP request pipeline middleware authentication handler" is written in full, explained, then shortened to "authentication handler" (three words) for the remaining text. P6, P9 applied.)*

> **Non-STE:** The primary parts of the system are:
> - The CM (8)
> - The EB (15)
> - The CR (17)
> - The DTL (20).
>
> **STE:** The primary parts of the system are:
> - The cache manager (8)
> - The event bus (15)
> - The command router (17)
> - The data transfer layer (20).

>
> *(Method 1 — Do not abbreviate short nouns: "cache manager," "event bus," "command router," and "data transfer layer" each have three words or fewer and already obey Rule 2.1. Using abbreviations like "CM" or "EB" makes the text harder to read. P6, P9 applied.)*

> **Non-STE:** Move the data-access-layer-query-builder handle. Set the main-menu-configuration-file path.
>
> **STE:** Move the data-access-layer query-builder handle. Set the main-menu configuration-file path.

>
> *(Method 2 — Hyphens: hyphenated groups of more than three words are not permitted. The non-STE version uses "data-access-layer-query-builder" as a single hyphenated group of four words, which is not correct. The STE version splits the noun at the correct boundary: "data-access-layer" (counts as one word) modifies "query-builder handle." Similarly, "configuration-file" counts as one word modified by "main-menu." P9 applied.)*

## Principles Applied

**P6** — Use non-approved words only when they are technical nouns. Long multi-word technical nouns like "HTTP request pipeline middleware authentication handler" contain non-approved words but are permitted because each word is part of a code-domain technical noun. The same applies to hyphenated nouns like "data-access-layer" and "query-builder" — the individual words may not be approved, but the whole noun is a code-domain technical noun.

**P8** — Use standard, well-known technical nouns. When choosing a shorter form for a long technical noun, use a standard, well-known term from the subject field. "Authentication handler" is a recognized term in web middleware documentation. "Cache manager," "event bus," "command router," and "data transfer layer" are standard terms in software architecture.

**P9** — Prefer short, clear technical nouns. This is the primary principle for Rule 2.2. When a technical noun exceeds three words, you must reduce it — either by giving a shorter form (Method 1) or by using hyphens to group related words into single-word units (Method 2). Both methods serve the same goal: bringing the multi-word noun into compliance with the three-word limit of Rule 2.1 while preserving the approved technical meaning.
