# Rule 3.6 — Use the Active Voice

## Original Rule Summary

Rule 3.6 mandates the active voice as the default for all technical writing. In the active voice, the subject does the action ("A" does "B"), so the grammatical subject and the logical agent are the same. The passive voice is permitted only in descriptive writing when the agent is unknown — for example, when the cause of data corruption cannot be identified. When the agent is known but appears after "by," the sentence must be rewritten with the agent as the subject. When the agent is not given, the writer can use "you" or "we" as the subject, or in procedural writing, convert the verb to the imperative form. 

## STE-Code Adaptation

Rule 3.6 in STE-Code applies the active-voice requirement to all code documentation. In the active voice, the subject of the sentence performs the action, so the reader immediately knows which component, function, service, or person does what. The passive voice is permitted only when the agent — the service, component, process, or author — is genuinely unknown and cannot be reasonably substituted with "the system," "the runtime," "the compiler," or "you." Four methods convert passive to active: move the "by" agent to the subject position, change an infinitive to an active verb, use the imperative in procedural writing, and insert "you" or "we" when the agent is the reader or the organization. Every docstring, README sentence, API description, and error message must survive the test "by whom or by what?" — if an answer exists, the sentence must be rewritten with that answer as the subject.

## Example Pairs

> **Non-STE:** The API response is parsed by the middleware layer before it is forwarded to the client handler.
>
> **STE:** The middleware layer parses the API response before it sends the response to the client handler.
>
> *(Method 1 applied: the "by" agent "the middleware layer" moves to the subject position. P3 applied: active voice produces a shorter, more direct sentence. P1 applied: "forwarded" → "sends" uses the approved verb SEND.)*

>
> **Non-STE:** The configuration file can be edited with a text editor to change the database connection settings.
>
> **STE:** You can edit the configuration file with a text editor to change the database connection settings.
>
> *(Method 4 applied: the agent is the reader, so "you" is the subject. P3 applied: the active construction with "you" makes the instruction immediate and personal. P4 applied: the modal "can" combines with the active verb "edit" in the simple present form.)*

>
> **Non-STE:** The dependencies are installed by running the command `npm install` from the project root directory.
>
> **STE:** Install the dependencies: run `npm install` from the project root directory.
>
> *(Method 3 applied: the procedural sentence uses the imperative form. P3 applied: the imperative eliminates the passive wrapper entirely and speaks directly to the reader. P4 applied: "Install" and "run" are both approved verbs in the approved imperative form.)*

## Principles Applied

**P3** — Prefer the simpler construction. This is the primary principle for Rule 3.6. The active voice produces shorter, more direct sentences than the passive voice. "The middleware parses the response" (4 words) is simpler than "The response is parsed by the middleware" (7 words) and places the doer of the action first. Every conversion from passive to active reduces word count and removes the auxiliary verb "to be" that the passive voice requires. Simpler constructions also reduce the cognitive distance between the reader and the action described — the reader sees the agent first, then the action, then the object, which mirrors natural English word order.

**P4** — Use only approved verb forms and tenses. The passive voice often combines "to be" with a past participle (is parsed, was built, are configured), which pushes verb forms toward compound constructions that Rule 3.2 and Rule 3.4 restrict. Converting to the active voice eliminates the "to be" auxiliary and collapses the verb into a single-word approved form: "is parsed" becomes "parses" (simple present), "was deployed" becomes "deployed" (simple past), "are validated" becomes "validates" (simple present). The imperative form used in procedural writing is also an approved verb form under Rule 3.2.

**P1** — Use approved words from the controlled terminology. When converting from passive to active, the replacement active verb must be an approved word from the STE-Code dictionary. A passive construction like "The data is forwarded to the service" must become "The middleware sends the data to the service" — not "The middleware forwards the data" — because "forward" is not an approved verb. The active-voice conversion is an opportunity to also substitute stronger, approved verbs for weaker or unapproved ones that the passive construction may have concealed.

**P8** — Use clear, direct, unambiguous language. The passive voice obscures responsibility: "The request was rejected" does not say who or what rejected it. The active voice demands that the writer name the agent, which forces clarity. "The authentication service rejected the request" tells the reader exactly which component made the decision. In code documentation, knowing the agent is critical for debugging, for understanding control flow, and for tracing errors. The passive voice is permitted only when the agent is genuinely unknown — a condition that should be rare in software systems where every action has a traceable origin.
