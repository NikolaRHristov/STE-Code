# Rule 3.7 — Use an Approved Verb to Describe an Action, Not a Noun or Other Parts of Speech

## Original Rule Summary

Rule 3.7 requires that every action in technical writing be carried by an approved verb rather than a noun or another part of speech. Verbs describe actions more clearly than nouns do, so the writer must prefer the direct verb construction over noun-based alternatives such as "gives an indication of" or "performs an analysis of." When the desired verb is not approved in the dictionary, the writer must not use it as a verb — instead, restructure the sentence with a support verb such as "do" or a different approved construction. The rule applies to all writing, but the solution depends on whether the word in question is approved as a verb: if it is approved, use it directly; if it is not approved, use the "do + noun" pattern or rephrase entirely.

## STE-Code Adaptation

Rule 3.7 in STE-Code applies the approved-verb requirement to all code documentation — README files, API documentation, docstrings, inline comments, and error messages. Every action must be carried by a verb approved in the STE-Code vocabulary; nominalized constructions such as "performs the initialization of" or "does the configuration of" must be replaced with the direct approved verb ("initializes," "configures"). When a code-domain technical noun such as "benchmark," "debug," or "docker" has no approved verb form, the writer must either pair it with an approved support verb ("do a benchmark," "run a debug session") or restructure the sentence to use a different approved verb. The two canonical patterns are: (1) nominalization → direct approved verb, and (2) verbing of an unapproved noun → "do/run + noun" or restructured sentence.

## Example Pairs

> **Non-STE:** The linter gives an indication of three errors in the source file.
>
> **STE:** The linter shows three errors in the source file.
>
> *(Pattern 1 applied: the noun-based construction "gives an indication of" is replaced with the direct approved verb "shows." P3 applied: the sentence becomes shorter and more direct. P1 applied: "shows" is the approved verb from the controlled vocabulary.)*

>
> **Non-STE:** Benchmark the application to measure the response time under load.
>
> **STE:** Do a benchmark of the application to measure the response time under load.
>
> *(Pattern 2 applied: "benchmark" is a technical noun that is not approved as a verb, so the support verb "do" introduces it. P1 applied: "do" is the approved support verb for actions carried by unapproved nouns. P3 applied: the "do + noun" pattern preserves the meaning while respecting vocabulary constraints.)*

>
> **Non-STE:** The `validateInput` function performs validation of the user input and gives an indication of success or failure.
>
> **STE:** The `validateInput` function validates the user input and shows success or failure.
>
> *(Pattern 1 applied twice: "performs validation of" becomes the direct verb "validates," and "gives an indication of" becomes the direct verb "shows." P3 applied: the sentence drops from 18 words to 11 words. P1 applied: both "validates" and "shows" are approved verbs from the controlled vocabulary. P8 applied: the direct verbs make the function's behavior immediately clear to the reader.)*

## Principles Applied

**P3** — Prefer the simpler construction. This is the primary principle for Rule 3.7. A direct verb construction is always shorter and simpler than a noun-based construction that wraps the action in a support verb plus a nominalization. "The function validates the input" (4 words) is simpler than "The function performs validation of the input" (7 words). The direct verb eliminates the "wrapper" support verb and the preposition "of" that nominalization requires. When the desired verb is not approved, the "do + noun" pattern is the simplest alternative that respects the controlled vocabulary.

**P1** — Use approved words from the controlled terminology. The core mechanic of Rule 3.7 depends on the STE-Code dictionary: if a word is approved as a verb, use it directly; if it is not approved as a verb, do not verb it — use it only as a noun. The dictionary tells the writer whether "validate" can stand as a verb (yes — use "validates") or whether "benchmark" must remain a noun (yes — use "do a benchmark"). Every substitution from a nominalized construction to a direct verb must land on an approved verb.

**P4** — Use only approved verb forms and tenses. When switching from a nominalized construction to a direct verb, the verb must appear in its approved form (simple present, simple past, imperative, or infinitive). "Performs validation" collapses to "validates" (simple present, third-person singular — an approved form). "Did a configuration of" collapses to "configured" (simple past — an approved form). The support verb "do" in "do a benchmark" must take the approved imperative or simple present form as the sentence context requires.

**P8** — Use clear, direct, unambiguous language. A noun-based construction such as "The system performs the authorization of the token" obscures the action behind two layers: the verb "performs" and the nominalization "authorization." The reader must mentally parse both layers to understand that the system authorizes the token. The direct verb "authorizes" removes both layers and presents the action immediately. In code documentation, this clarity is essential for debugging, for understanding system behavior, and for writing correct integration code against documented APIs.
