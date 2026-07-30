# Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

## Original Rule Summary

A code-domain technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field. The controlled terminology does not include all code-domain technical verbs because there are too many, and each project or subject field uses different technical verbs. You can use code-domain technical verbs in procedural and descriptive texts if you can include them in one of four categories: development processes, computer processes and applications, instructions for applicable subject fields, or law and regulations. If an approved verb in the dictionary accurately gives the instruction or the information, use the approved verb instead of a technical verb.

## STE-Code Adaptation

Code-domain technical verbs name precise software operations that have no single approved-verb equivalent — words like "transpile," "refactor," "deploy," "serialize," and "authenticate." You may use these verbs if they fit one of the four STE-Code categories, but you must verify that no approved verb works in its place first. Do not use a technical noun as a technical verb (for example, do not use "Docker" as a verb; write "put the application in a Docker container"). When you use a code-domain technical verb, it must obey the same rules as other approved verbs in the controlled terminology, and it must be correct and specific to your context — not general or vague.

## Examples

> **Non-STE:**
> The static analyzer detects null pointer dereferences in the source code.
>
> **STE:**
> The static analyzer finds null pointer dereferences in the source code.

> *Principle: P1. "Detect" is not approved in the controlled terminology. The approved verb "find" gives the same information. Do not use a technical verb when an approved verb is available and equally accurate.*

> **Non-STE:**
> Run the TypeScript source through the converter to get JavaScript output.
>
> **STE:**
> Transpile the TypeScript source to JavaScript.

> *Principle: P12. "Transpile" is a code-domain technical verb in category 1a (development processes — write and modify code). No single approved verb describes source-to-source compilation precisely. The technical verb is necessary and correct in this context.*

> **Non-STE:**
> Docker the application and then ship the image to the registry.
>
> **STE:**
> Put the application in a Docker container and then push the image to the registry.

> *Principles: P1, P12. "Docker" is a technical noun (a proper name for a container platform). Do not use a technical noun as a technical verb. The approved verb "put" with the technical noun "Docker container" gives the instruction clearly. "Ship" is also replaced with the approved verb "push."*

## Principles Applied

- **P1:** Use approved words from the controlled terminology when they are available ("find" instead of "detect," "put" instead of "Docker" as a verb, "push" instead of "ship")
- **P12:** Code-domain technical verbs are permitted only when they belong to a recognized category and no approved verb gives the same information ("transpile" is category 1a; no approved equivalent exists)
