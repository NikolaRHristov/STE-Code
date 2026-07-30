# Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions

## Original Rule Summary

Rule 3.4 prohibits using auxiliary verbs — especially "have," "has," and "had" — together with the past participle form of a verb to create compound tenses. The present perfect ("has deployed"), past perfect ("had committed"), and future perfect ("will have started") are not approved in STE. The past participle after "to be" is permitted only when it functions as an adjective describing a condition ("the unit is disassembled"), not as part of a passive verb construction. This rule works in tandem with Rule 3.2 (approved verb forms) and Rule 3.6 (active voice) to ensure every sentence uses a single, simple tense.

## STE-Code Adaptation

Rule 3.4 controls whether code documentation can combine auxiliary verbs with past participles to form compound tenses across all document types. README files replace present perfect status statements ("has been tested") with simple present ("runs on") or simple past ("We tested"). API documentation replaces present perfect version qualifiers ("has returned a 200 OK since version 3.0") with simple present plus a separate qualification sentence. Docstrings and commit messages replace perfect infinitives ("to have configured") and present perfect clauses ("has stored") with imperative or simple present forms. The auxiliary "have" as a main verb ("the function has three parameters") is permitted; the restriction applies only when "have" combines with a past participle to form a compound tense.

## Example Pairs

> **Non-STE:** After the pipeline has deployed the application, the monitoring service will have started the health checks.
>
> **STE:** After the pipeline deploys the application, the monitoring service starts the health checks.

>
> *(P3, P4, Rule 3.2, Rule 3.4 applied: "has deployed" → "deploys" — present perfect replaced by simple present. "will have started" → "starts" — future perfect replaced by simple present. Both auxiliary verbs "has" and "will have" are removed. The compound tenses collapse into the approved simple present tense.)*

> **Non-STE:** The developer had committed the changes before the reviewer had approved the pull request.
>
> **STE:** The developer committed the changes. Then the reviewer approved the pull request.

>
> *(P3, P4, Rule 3.4 applied: "had committed" → "committed," "had approved" → "approved" — both past perfect constructions replaced by simple past. The compound sentence is broken into two separate sentences sequenced with "Then." The simple past with explicit sequencing eliminates two-level temporal nesting.)*

> **Non-STE:** The test runner has executed all the unit tests and has written the coverage report.
>
> **STE:** The test runner executed all the unit tests. Then it wrote the coverage report.

>
> *(P3, P4, P9, Rule 3.4 applied: "has executed" → "executed," "has written" → "wrote" — both present perfect constructions replaced by simple past. The compound sentence is split into two sentences sequenced with "Then." The word "it" replaces the repeated subject. The simple past records completed actions directly.)*

## Principles Applied

**P3** — Use approved meanings from the controlled terminology dictionary. Each verb in the dictionary has exactly four approved forms — base, third-person singular present, simple past, and past participle. The auxiliary "have" combined with the past participle creates compound tenses (present perfect, past perfect, future perfect) that are not among the approved forms. The simple past and simple present are the only correct replacements. This principle also governs the boundary between auxiliary "have" and main-verb "have": when "have" expresses possession or requirement ("the function has three parameters"), it is a main verb and P3 does not restrict it. When "have" precedes a past participle without a direct object in between, it is an auxiliary and P3 prohibits the construction.

**P4** — Use only the approved verb forms. Rule 3.4 extends from Rule 3.2 by prohibiting any combination of an auxiliary verb with a past participle that would create an unapproved compound tense. The present perfect ("has deployed," "have tested"), past perfect ("had committed," "had initialized"), future perfect ("will have migrated," "will have completed"), perfect infinitive ("to have configured"), and future perfect progressive ("will have been operating") are all unapproved. Every such construction must be replaced by one of the six approved forms: the base form, the third-person singular present, the simple past, the simple future, the imperative, or the past participle as an adjective. The simple present and simple past are the primary replacements for compound tenses in code documentation.
