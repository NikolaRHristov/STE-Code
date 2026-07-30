# Rule 1.13 — Do Not Use Technical Verbs as Nouns

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.13
> **See also:** Rule 1.12, Rule 1.5, Rule 1.7

## Original Rule Summary

Rule 1.13 prohibits using technical verbs as nouns in Simplified Technical English. Words that share identical spellings can serve different grammatical functions; a word approved as a technical verb must not be forced into a noun role. The spec allows for cases where the same word appears in both a technical verb category (Rule 1.12) and a technical noun category (Rule 1.5), such as "plate" functioning as both a manufacturing-process verb and a material noun. The spec example "Enter your password" illustrates correct verb-only usage of a word that could otherwise be nominalized.

## STE-Code Adaptation for Code Documentation

Rule 1.13 adapts to code documentation by requiring code-domain technical verbs — words like build, compile, parse, deploy, filter, map, and allocate — to be used only as verbs, never as nouns in instructional or descriptive prose. When a word serves as a method name, class name, or API resource identifier, it functions as a code-domain technical noun under Rule 1.5 and is exempt from this restriction. Documentation types carry different risk profiles: README instructions and error messages demand imperative verb forms, while type signatures and API reference tables may legitimately use function names as noun references. The rule ensures that every action in documentation has a clear, active verb so that readers immediately understand what a function does, what a commit changes, or what a log entry records.

## Examples

### Example 1 — README / Build Instructions

> **Non-STE:** Do a build of the project before you do a deploy to production.
>
> **STE:** Build the project before you deploy to production.

### Example 2 — API Docstring / Function Description

> **Non-STE:** This function does a parse of the input string and does a validate of the tokens.
>
> **STE:** This function parses the input string and validates the tokens.

### Example 3 — Commit Message / Change Description

> **Non-STE:** Addition of rate limiter and refactor of the auth middleware.
>
> **STE:** Add rate limiter and refactor the auth middleware.

## Principles Applied

| Principle | Description |
|-----------|-------------|
| P1 — Use Approved Words Only | Use technical verbs only in their approved verb form. Do not invent noun forms from verbs unless the word is also approved as a technical noun (Rule 1.5). |
| P3 — Use Verbs in Approved Forms | Every action in documentation must have an explicit, active verb. Nominalizing a verb hides the action and weakens the sentence. |
| P7 — Do Not Use Technical Verbs as Nouns | The core principle: a word approved as a code-domain technical verb (build, parse, deploy, filter, allocate) must only fill a verb slot in the sentence. |
| P10 — Write Short, Clear Sentences | Nominalized verbs force extra words ("do a build of" instead of "build"). Removing them produces shorter, clearer sentences. |
| P12 — Use Consistent Style Across Documentation Types | Commit messages, README instructions, docstrings, and error messages all benefit from the same verb-first rule. Consistency helps tooling and human readers alike. |
