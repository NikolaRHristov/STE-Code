# Rule 3.2 — Use only these verb forms and tenses of verbs.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.2

> Source: master.md#sec3-rule3.2

## Original Rule

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective).

Use only the verbs forms and the tenses of verbs that are approved.

| Infinitive form (base form) | Imperative form (command form) | Simple present tense | Simple past tense | Simple future tense | Past participle form (as an adjective) |
|---|---|---|---|---|---|
| (To) Adjust (regular verb) | Adjust + object | You/we/they adjust It adjusts | You/we/they adjusted It adjusted | You/we/they will adjust It will adjust | The adjusted linkage |
| (To) Give (irregular verb) | Give + object | You/we/they give It gives | You/we/they gave It gave | You/we/they will give It will give | The given information |

Do not use other forms and tenses that are not approved, for example:

- The present perfect (have/has adjusted)
- The past perfect (had adjusted)
- The present/past progressive (is/was adjusting)
- And all other complex verb constructions.

## STE-Code Adaptation

Use only these verb forms and tenses of verbs:

- The infinitive form
- The imperative form (command form)
- The simple present tense
- The simple past tense
- The simple future tense
- The past participle form (as an adjective).

Use only the verb forms and the tenses of verbs that are approved in the STE-Code dictionary.

| Infinitive form (base form) | Imperative form (command form) | Simple present tense | Simple past tense | Simple future tense | Past participle form (as an adjective) |
|---|---|---|---|---|---|
| (To) Parse (regular verb) | Parse + object | You/we/they parse It parses | You/we/they parsed It parsed | You/we/they will parse It will parse | The parsed file |
| (To) Write (irregular verb) | Write + object | You/we/they write It writes | You/we/they wrote It wrote | You/we/they will write It will write | The written log |

Do not use other forms and tenses that are not approved, for example:

- The present perfect (have/has parsed)
- The past perfect (had parsed)
- The present/past progressive (is/was parsing)
- And all other complex verb constructions.

## Examples

> **Non-STE:** The linter has found three errors in the source file.
> **STE:** The linter found three errors in the source file.
>
> *Adapted from spec pair: present perfect "have/has adjusted" is not approved.*

> **Non-STE:** The server was processing the request when the timeout occurred.
> **STE:** The server processed the request. Then the timeout occurred.
>
> *Adapted from spec pair: past progressive "was adjusting" is not approved. Break the sentence into separate sentences.*

> **Non-STE:** The framework had already initialized the connection pool before the query started.
> **STE:** The framework initialized the connection pool. Then the query started.
>
> *Adapted from spec pair: past perfect "had adjusted" is not approved. Use the simple past tense and sequence with "Then."*

> **Non-STE:** The scheduler is deploying the build to production while the tests are running.
> **STE:** The scheduler deploys the build to production. The tests run at the same time.
>
> *Adapted from spec pair: present progressive "is deploying" / "are running" is not approved.*
