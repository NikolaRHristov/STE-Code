# Rule 1.2 — Use Approved Words Only as the Specified Part of Speech

## Original Rule Summary

Rule 1.2 enforces part-of-speech discipline on every approved word in the STE dictionary. Each word carries a grammatical label — noun, verb, adjective, and so on — and writers must use it only in that role. "Test" is an approved noun but not an approved verb, so "Do a test" is correct while "Test the system" is a violation. Some words like "clean" are approved in multiple roles, where sentence position determines the active part of speech. The rule also governs word replacement: when an unapproved word has only an approved alternative with a different part of speech, the writer must restructure the entire sentence rather than performing a simple word swap.

## STE-Code Adaptation

Rule 1.2 applies the same grammatical gate to code documentation. Every approved word in the project controlled terminology carries a part-of-speech label, and writers must respect that label. A word like "query" is an approved noun — "Send a query to the database" is correct, but "Query the database" is a violation because "query" cannot be used as a verb. An adjective like "static" cannot be forced into verb service — "Make the variable static" is correct, but "Static the variable" is a violation. The adaptation mirrors the spec's three most common violation patterns: noun-as-verb, adjective-as-verb, and the special case of words approved in multiple roles where context determines which role is active.

## Example Pairs

> **Non-STE:** Query the database for user records.
>
> **STE:** Send a query to the database for user records.
>
> *(P2 applied: "query" is an approved noun, not a verb — "Send a query" uses the approved verb "send" with the noun "query." This adapts the spec pair "Test the system for leaks" → "Do the leak test of the system.")*

> **Non-STE:** Static the variable to prevent modification.
>
> **STE:** Make the variable static to prevent modification.
>
> *(P2 applied: "static" is an approved adjective, not a verb — "Make the variable static" uses the approved verb "make" with the adjective "static." This adapts the spec example where "dim" is an adjective that cannot be used as a verb.)*

> **Non-STE:** fix: cache the query results to speed up the dashboard
>
> **STE:** fix: add a cache for query results to make the dashboard faster
>
> *(P2 applied: "cache" is a noun, not a verb — "add a cache" uses the approved verb "add" with the noun "cache." P1 applied: "speed up" uses "speed" as a verb — restructured to "make faster" using the approved adjective "fast." This adapts the spec example where a noun is used as a verb for brevity in technical prose.)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. Words like "speed" (verb form), "utilize," and "execute" are replaced with their approved counterparts: "make," "use," and "run." The dictionary gives the complete list of approved words and their unapproved alternatives.

**P2** — Use approved words only as the specified part of speech. This is the primary principle for Rule 1.2. Every approved word carries a grammatical label in the controlled terminology — verb (v), noun (n), adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun (pron), or article (art). The word must be used only in the role that its label permits.

**P7** — Do not use technical nouns as verbs (Rule 1.7). A code-domain technical noun like "cache," "query," "Docker," or "endpoint" cannot be used as a verb. The fix uses an approved verb with the technical noun as its object: "Send a query," "Add a cache," "Use Docker," "Handle traffic at the endpoint."

**P12** — Technical verbs are allowed (Rule 1.12). When a word is a code-domain technical verb — like "serialize," "compile," or "marshal" — Rule 1.12 overrides Rule 1.2's part-of-speech constraint for that specific word in that specific technical context. The override does not extend to non-technical uses of the same word.

**P13** — Do not use technical verbs as nouns (Rule 1.13). This is the inverse of P7 and a consequence of Rule 1.2 applied to technical verbs. A word permitted as a technical verb under Rule 1.12 — such as "serialize" — must not be used as a noun: "The serialize failed" is a violation; use "The serialization failed" instead.
