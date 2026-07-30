# Rule 1.4 — Use Only the Approved Forms of Verbs and Adjectives

## Original Rule Summary

Rule 1.4 constrains every approved verb and adjective to only its dictionary-listed forms. The STE dictionary gives each approved verb with its four approved forms (infinitive/imperative, simple present, simple past, past participle) and each approved adjective with its base, comparative, and superlative forms where applicable. The continuous "-ing" form is never an approved main-verb form, and the future continuous ("will be running") and conditional forms are also excluded. Adjectives that form comparatives and superlatives with "more" and "most" do not have these forms listed in the dictionary because "more" and "most" are approved words.

## STE-Code Adaptation

Rule 1.4 in STE-Code applies the same morphological constraints to code documentation. Every approved verb from the controlled terminology must appear only in its four approved forms: the imperative base form (used in commit messages and procedural steps), the simple present third-person singular (used in API descriptions and class documentation), the simple past (used for completed actions), and the past participle (used as an adjective for state). The "-ing" form is permitted only when it is a code-domain technical noun (e.g., "logging," "caching," "routing") and never as a main verb. Adjective comparatives and superlatives must use either the approved "-er"/"-est" suffix forms from the controlled terminology or the "more"/"most" construction with the base form.

## Example Pairs

> **Non-STE:** After installing the dependencies, you can start compiling the project by running the build script. The compiler will be generating the output in the dist directory.
>
> **STE:** After you install the dependencies, compile the project with the build script. The compiler makes the output in the dist directory.
>
> *(P4 applied: "start compiling" → "compile" (imperative); "will be generating" → "makes"; P3 applied: continuous → simple present)*

> **Non-STE:** This method is returning a sorted list of users. It is accepting an optional filter parameter.
>
> **STE:** This method gives a sorted list of users. It accepts an optional filter parameter.
>
> *(P4 applied: "is returning" → "gives" (approved alternative to "return"); "is accepting" → "accepts"; P3 applied: continuous → simple present)*

> **Non-STE:** feat: adding user authentication middleware and updated the login endpoint
>
> **STE:** feat: add user authentication middleware and update the login endpoint
>
> *(P4 applied: "adding" → "add" (imperative mood); "updated" → "update" (imperative mood); P3 applied: mixed forms → consistent imperative)*

## Principles Applied

**P4** — Use only the approved forms of verbs and adjectives. This is the primary principle: every approved verb must appear in one of its four listed forms (infinitive/imperative, simple present, simple past, past participle), and never in the "-ing" form as a main verb. Every approved adjective must use its listed comparative and superlative forms or the "more"/"most" construction.

**P3** — Use the simplest verb form possible. The simple present tense ("compiles," "accepts," "makes") replaces the continuous aspect ("is compiling," "is accepting," "is making"). The imperative mood ("compile," "add," "update") replaces the "-ing" form in procedural writing and commit messages. The simple past ("compiled") replaces the past continuous ("was compiling").

**P1** — Use approved words from the controlled terminology. When a word like "return" is not approved, use its approved alternative ("give"). When an adjective like "better" (irregular comparative of unapproved "good") appears, replace it with an approved construction ("more correct"). The morphological constraints of Rule 1.4 work together with the vocabulary constraints of Rule 1.1.
