# Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs

## Original Rule Summary

Rule 3.2 restricts all documentation to six approved verb forms and tenses: the infinitive form, the imperative form, the simple present tense, the simple past tense, the simple future tense, and the past participle used only as an adjective. Compound tenses that combine auxiliary verbs with past participles or "-ing" forms — such as the present perfect (have/has adjusted), past perfect (had adjusted), and present/past progressive (is/was adjusting) — are prohibited. The rule ensures that every verb in the text is direct, unambiguous, and free of the temporal layering that complex tenses introduce. All other verb constructions beyond these six approved forms must be rewritten using only the permitted tenses.

## STE-Code Adaptation

Rule 3.2 in STE-Code applies the same six-form restriction to all code documentation: the infinitive (to build, to write), the imperative (Build the project. Run the tests.), the simple present (The function returns a string.), the simple past (The build failed.), the simple future (The next release will include.), and the past participle as an adjective (the compiled output, the written log). Compound verb constructions — present perfect (has compiled, have deployed), past perfect (had initialized, had processed), present progressive (is building, is writing), past progressive (was running, was deploying), and future perfect (will have migrated) — are not permitted. The rule interacts with documentation type: README files use the imperative and simple present, API docs use the simple present, docstrings use the simple present with third-person singular, commit messages use the imperative, and error messages use the simple present or simple past.

## Example Pairs

> **Non-STE:** The CI pipeline has completed the build and is deploying the artifacts to staging.
>
> **STE:** The CI pipeline completed the build. It deploys the artifacts to staging.

>
> *(Present perfect "has completed" → simple past "completed"; present progressive "is deploying" → simple present "deploys." P4 applied: only approved verb forms are permitted. P3 applied: split the compound sentence into two simple sentences.)*

> **Non-STE:** The parser was reading the input file when the error occurred, and it had already consumed the first 200 tokens.
>
> **STE:** The parser read the input file. Then the error occurred. The parser consumed the first 200 tokens before the error.

>
> *(Past progressive "was reading" → simple past "read"; past perfect "had consumed" → simple past "consumed" with "before" to sequence events. P4, P3 applied.)*

> **Non-STE:** The service is caching responses to improve performance, and it has reduced average latency by 40 percent.
>
> **STE:** The service caches responses to improve performance. This change decreased average latency by 40 percent.

>
> *(Present progressive "is caching" → simple present "caches"; present perfect "has reduced" → simple past "decreased." P4 applied. P12 applied: "caches" is a technical verb used in the approved simple present form.)*

## Principles Applied

**P4** — Use only approved verb and adjective forms. This is the primary principle for Rule 3.2. Only six verb forms and tenses are approved: infinitive, imperative, simple present, simple past, simple future, and past participle as an adjective. Any verb that appears in a compound construction — present perfect (has/have + past participle), past perfect (had + past participle), progressive (is/was + -ing), or future perfect (will have + past participle) — must be rewritten to use one of the six approved forms.

**P3** — Use approved words only with their approved meanings. When a compound tense is replaced with a simple tense, the replacement verb must carry the same approved meaning as the original. For example, "has completed" becomes "completed" — both describe a finished action, but the simple past does so without the auxiliary verb "have." Splitting compound sentences into separate simple sentences often requires ensuring each sentence has a clear, approved meaning on its own.

**P2** — Use approved words only as the specified part of speech. The past participle form is approved only as an adjective (the built artifact, the written output), never as part of a compound verb with "have" or "had." The "-ing" form is not approved as a verb form at all — Rule 3.5 permits "-ing" only as a technical noun or modifier. When removing a compound tense, ensure each word's part of speech matches its approved role.

**P12** — Technical verbs are allowed. Code-domain technical verbs such as compile, deploy, parse, serialize, cache, render, and query are permitted in documentation when used in one of the six approved verb forms. A technical verb in the present progressive ("is compiling") violates Rule 3.2. The same technical verb in the simple present ("compiles") is correct. The rule does not restrict which verbs you can use — it restricts which forms of any verb you can use.
