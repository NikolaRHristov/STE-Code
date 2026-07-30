# Rule 3.1 — Use Only the Verb Forms That Are Given in the Dictionary

## Original Rule Summary

Rule 3.1 is the verb-form gate of Simplified Technical English. Every approved verb in the STE dictionary has exactly four listed forms: the base form (infinitive/imperative), the third-person singular present, the simple past, and the past participle. You must use only these listed forms in technical documentation. Never invent a form by adding a regular suffix to an irregular verb — for example, "builded" is not permitted because the dictionary lists only BUILT as the past tense and past participle of BUILD. The dictionary is the sole authority; the writer must not rely on analogy or pattern recognition.

## STE-Code Adaptation

Rule 3.1 applies directly to all code documentation by constraining every verb to its listed forms in the controlled terminology. README instructions use the base form (first listed form), API descriptions use the third-person singular (second listed form) for function behavior, and completed operations use the approved past tense (third listed form) or past participle (fourth listed form). The most frequent violations in code documentation are invented past-tense forms for irregular verbs — "runned" instead of RAN, "writed" instead of WROTE, "builded" instead of BUILT — and the use of the continuous "-ing" form, which is not a listed verb form in the controlled terminology. Docstrings use the imperative base form for the first line and the simple present for additional description; commit messages use the imperative base form exclusively.

## Example Pairs

> **Non-STE:** The compiler has builded the project with the new configuration. The builded binary is in the output directory.
>
> **STE:** The compiler built the project with the new configuration. The built binary is in the output directory.

>
> *(P1, Rule 3.1 applied: "builded" → "built" for past tense and past participle. BUILD, BUILDS, BUILT, BUILT — BUILT is the only listed past/past-participle form. The regular "-ed" pattern does not override the dictionary.)*

> **Non-STE:** The function writed the output to the log file and gived a status code.
>
> **STE:** The function wrote the output to the log file and gave a status code.

>
> *(P1, Rule 3.1 applied: "writed" → "wrote" — WRITE, WRITES, WROTE, WRITTEN. "Gived" → "gave" — GIVE, GIVES, GAVE, GIVEN. The regular "-ed" suffix is never applied to irregular approved verbs.)*

> **Non-STE:** After you have runned the setup script, the server will be running on port 8080. You can then beginned testing the endpoints.
>
> **STE:** After you run the setup script, the server runs on port 8080. You can then begin testing the endpoints.

>
> *(P1, Rule 3.1 applied: "runned" → "run" — RUN, RUNS, RAN, RUN; only RAN is the past tense. "Beginned" → "begin" — BEGIN, BEGINS, BEGAN, BEGUN; only BEGAN is the past tense. "Will be running" → "runs" — the continuous "-ing" form is not a listed verb form; the simple present replaces it.)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. The verb forms listed in the dictionary entry are the only approved forms. Every verb used in code documentation — in README files, API documentation, docstrings, inline comments, commit messages, and error messages — must be one of the four listed forms. Invented forms like "builded," "runned," "writed," "gived," "beginned," "catched," "finded," "setted," "putted," "keeped," "holded," and "sended" are never permitted. The dictionary is the sole authority, not intuition or regular-pattern analogy.

**P4** — Use only the approved verb forms. This is the primary principle for Rule 3.1. Each approved verb has exactly four forms: the base form (first listed), the third-person singular present (second listed), the simple past (third listed, followed by a comma in the dictionary), and the past participle (fourth listed). The continuous "-ing" form is explicitly not a listed form — the simple present replaces all continuous-aspect constructions. The simple past and past participle forms differ for some irregular verbs (WROTE vs. WRITTEN, GAVE vs. GIVEN, BEGAN vs. BEGUN) — the writer must use the correct form for the grammatical context and never confuse the two.
