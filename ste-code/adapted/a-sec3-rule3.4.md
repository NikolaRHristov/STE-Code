# Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.4

## Original Rule

Do not use auxiliary verbs to make complex verb constructions.

Do not use the past participle form as a verb form together with the auxiliary verb "have." This construction will make a tense that is not approved.

Example:

> **STE:** When the unit is fully disassembled, clean all the parts.
> ("Disassembled" is an adjective after the verb "to be" that shows the condition of the unit.)
> (The simple past tense is approved.)

Some complex verb constructions include other auxiliary verbs with the past participle form as a verb. Sentences with these constructions become complex sentences in the passive voice.

## STE-Code Adaptation

Do not use auxiliary verbs ("have," "has," "had," "will have") together with the past participle form of a verb to make compound tenses. This construction creates verb forms that are not approved in STE-Code.

The auxiliary verb "have" with a past participle produces the present perfect or past perfect tense, which violates Rule 3.2. Instead, use one of the approved simple tenses.

> **See also:** Rule 3.2 — Use Only These Verb Forms and Tenses of Verbs

Complex verb constructions that combine auxiliary verbs with the past participle often also create passive voice constructions. Simplify these sentences by using the active voice (Rule 3.6) and the simple past tense.

> **See also:** Rule 3.6 — Use the Active Voice

A sentence that uses the past participle after "to be" is permitted only when the past participle functions as an adjective describing a condition (Rule 3.3), not as part of a passive verb construction.

> **See also:** Rule 3.3 — Use the Past Participle Form as an Adjective

### Examples

> **Non-STE:** After the pipeline has deployed the application, the monitoring service will have started the health checks.
> **STE:** After the pipeline deploys the application, the monitoring service starts the health checks.

> *Adapted from spec pair: "When the unit is fully disassembled, clean all the parts."* Just as STE avoids the present perfect ("has disassembled") by using the simple present/past, STE-Code avoids compound tenses ("has deployed," "will have started") by using the simple present tense. The auxiliary verbs "have" and "will have" are removed.

> **Non-STE:** The developer had committed the changes before the reviewer had approved the pull request.
> **STE:** The developer committed the changes. Then the reviewer approved the pull request.

> *Adapted from spec pair: the past perfect tense is not approved in STE.* Just as STE does not permit "had adjusted," STE-Code does not permit "had committed" or "had approved." Replace with simple past tense and break into separate sentences.

> **Non-STE:** The test runner has executed all the unit tests and has written the coverage report.
> **STE:** The test runner executed all the unit tests. Then it wrote the coverage report.

> *Adapted from spec pair: the present perfect tense is not approved in STE.* Just as STE does not permit "has adjusted," STE-Code does not permit "has executed" or "has written." Replace with simple past tense and use separate sentences sequenced with "Then."
