# Rule 1.6 — Use a Word That Is Not Approved in the Dictionary, Only When It Is a Technical Noun or Part of a Technical Noun

## Original Rule Summary

Rule 1.6 is the exemption gate in Simplified Technical English. The dictionary includes words that are not approved, but if an unapproved word can be placed in an applicable category of technical nouns, you may use it as a technical noun in some contexts. The same word can belong to different technical noun categories when used with different meanings — "base" is unapproved when referring to a surface (use "bottom"), but permitted as a technical noun in mathematical and infrastructure categories. The rule distinguishes between standalone unapproved words (must be replaced) and unapproved words embedded in recognized compound technical nouns like "main landing gear" (permitted).

## STE-Code Adaptation

Rule 1.6 in STE-Code applies the same exemption model to code documentation. A word like "handler" is not approved in the controlled terminology (alternative: "function"), but it is permitted as part of the code-domain technical noun "event handler" (category 1, code components). The word "main" is not approved (alternative: "primary"), but it is permitted in recognized compound technical nouns like "main branch" (category 5, infrastructure). A word like "backup" is not approved (alternatives: "auxiliary" and "emergency"), but it is permitted in compound technical nouns like "backup file" (category 18, database/storage). The adaptation preserves the spec's three-part test: is the word unapproved, is it a recognized technical noun or part of one, and is it used as a noun in the sentence.

## Example Pairs

> **Non-STE:** The handler processes each incoming event and the base configuration is loaded first from the config file.
>
> **STE:** The function processes each incoming event and the primary configuration is loaded first from the config file.
>
> *(P6 applied: "handler" as standalone word → "function" [approved alternative]; "base" as general adjective → "primary" [approved alternative]. Neither "handler" nor "base" is part of a recognized compound technical noun here — both fail the Rule 1.6 gate.)*

> **Non-STE:** The event handler processes each request. Merge the feature branch into the main branch for deployment.
>
> **STE:** The event handler processes each request. Merge the feature branch into the main branch for deployment.
>
> *(P6 applied: no changes needed. "event handler" is a compound code-domain technical noun [category 1] — "handler" is permitted within it. "main branch" is a recognized Git convention [category 5, infrastructure] — "main" is permitted within it. Both unapproved words are embedded in recognized technical nouns.)*

> **Non-STE:** POST /api/backup — Backups the main database nightly. Handlers errors and returns a backup ID for reference.
>
> **STE:** POST /api/backup — Makes an auxiliary copy of the primary database each night. Processes errors and returns a backup ID for reference.
>
> *(P6 applied: "Backups" as a verb → "Makes an auxiliary copy" [backup is unapproved as a verb]. "Handlers" as a verb → "Processes." "main" as general adjective → "primary." The endpoint path `/api/backup` and the field name "backup ID" are compound technical nouns [category 18] and remain unchanged.)*

## Principles Applied

**P6** — Use a word that is not approved in the controlled terminology, only when it is a code-domain technical noun or part of a code-domain technical noun. This is the primary principle for Rule 1.6. Unapproved words like "handler," "main," and "backup" are permitted only when embedded in recognized compound technical nouns (e.g., "event handler," "main branch," "backup file") that fit one of the 19 code-domain categories. When these words stand alone as general prose, they must be replaced with their approved alternatives: "function," "primary," and "auxiliary."

**P1** — Use approved words from the controlled terminology. When an unapproved word fails the Rule 1.6 gate — it is not a technical noun and not part of one — it must be replaced with its approved alternative from the controlled terminology. "Handler" → "function," "main" → "primary," "backup" → "auxiliary" (for adjectives) or "auxiliary copy" (for the noun concept).

**P7** — Do not use technical nouns as verbs (Rule 1.7). A word that passes through the Rule 1.6 gate as a technical noun must remain a noun. "Backups" used as a verb ("Backups the database") is a violation — the technical noun "backup" (permitted as part of "backup file" or "backup ID") cannot be used in verb position. The same applies to "handler": permitted in "event handler" but not as the verb "handlers."

**P8** — Use standard, well-known technical nouns (Rule 1.8). To qualify as a code-domain technical noun under Rule 1.6, the compound must be recognized in the project glossary, framework documentation, an industry standard, or one of the 19 STE-Code categories. Ad hoc compounds like "handler pipeline" or "backup orchestrator" are not recognized technical nouns and must be rewritten with approved words.
