# Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.2

## Original Rule

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective).

Use only the verb forms and the tenses of verbs that are approved.

Do not use other forms and tenses that are not approved, for example:

- The present perfect (have/has adjusted)
- The past perfect (had adjusted)
- The present/past progressive (is/was adjusting)
- And all other complex verb constructions.

## STE-Code Adaptation

Use only these verb forms and tenses of verbs in code documentation:

- The infinitive form (to build, to write, to deploy)
- The imperative form or command form (Build the project. Write the function. Deploy to staging.)
- The simple present tense (The function builds the output. The linter writes the report.)
- The simple past tense (The pipeline built the artifact. The test wrote the result.)
- The simple future tense (The next release will build all modules. The script will write the log.)
- The past participle form used only as an adjective (the built artifact, the written output)

Do not use complex verb constructions that are not approved. Specifically, never use:

- The present perfect (has built, have written)
- The past perfect (had built, had written)
- The present progressive (is building, is writing)
- The past progressive (was building, was writing)
- Any other compound tense that combines auxiliary verbs with the past participle or the "-ing" form.

### Examples

> **Non-STE:** The linter has found three errors in the source file.
> **STE:** The linter found three errors in the source file.

> **Non-STE:** The server was processing the request when the timeout occurred.
> **STE:** The server processed the request. Then the timeout occurred.

> **Non-STE:** The framework had already initialized the connection pool before the query started.
> **STE:** The framework initialized the connection pool. Then the query started.
