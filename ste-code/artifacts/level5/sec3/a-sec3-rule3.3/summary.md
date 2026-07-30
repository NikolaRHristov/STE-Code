# Rule 3.3 — Use the Past Participle Form as an Adjective

## Original Rule Summary

Rule 3.3 governs the past participle form of verbs, permitting it only when it functions as an adjective that describes a condition. The past participle as an adjective is not passive voice — it shows the state of something without naming an agent. The adjective may appear before a noun ("the disassembled unit") or after a form of "to be," "to become," or "to stay" ("the unit is disassembled"). The dictionary also contains standalone adjectives that are the past participle form of unapproved verbs (such as "permitted" and "damaged"), and these too may be used as adjectives.

## STE-Code Adaptation

Rule 3.3 in STE-Code uses the past participle form of an approved verb only as an adjective that describes the condition of a code entity — a file, a binary, a service, a module. The past participle as an adjective appears in two syntactic positions: before a noun ("the compiled binary," "the encrypted payload") or after "to be," "to become," or "to stay" ("When the binary is compiled," "The service stays connected"). The past participle must never form a compound verb with "have" — that construction is prohibited by Rule 3.4. The STE-Code dictionary also includes standalone adjectives that are the past participle form of unapproved verbs, such as "deprecated" (adj), which describe a condition without implying an action.

## Example Pairs

> **Non-STE:** When you have compiled the binary and have encrypted the payload, run the deployment script that has validated the configuration.
>
> **STE:** When the binary is compiled and the payload is encrypted, run the deployment script that validated the configuration.
>
> *(P2 applied: "compiled" and "encrypted" appear after "is" as adjectives describing conditions, not as parts of compound verbs. P1 applied: "compiled" and "encrypted" are the approved fourth forms of COMPILE and ENCRYPT, used in the adjective position.)*

>
> **Non-STE:** Review all of the updated configuration settings that the script has generated. The system has stored the processed data in the cache.
>
> **STE:** Review all the updated configuration settings. The system stores the processed data in the cache.
>
> *(P2 applied: "updated" and "processed" are adjectives before nouns describing conditions. P4 applied: the compound verb forms "has generated" and "has stored" are replaced with the simple present tense "stores." The redundant relative clause "that the script has generated" is removed entirely.)*

>
> **Non-STE:** /** This method has parsed the input, has filtered invalid entries, and has returned the validated result. */
>
> **STE:** /** This method parses the input, filters invalid entries, and gives the validated result. */
>
> *(P2 applied: "validated" is an adjective before "result" — it describes the condition of the result. P3 applied: the three compound verb forms "has parsed," "has filtered," and "has returned" are replaced with the simpler simple present tense. P1 applied: "returned" → "gives" uses the approved verb GIVE.)*

## Principles Applied

**P2** — Use approved words only as the specified part of speech. This is the primary principle for Rule 3.3. The past participle form must function as an adjective in the sentence, never as a verb in a compound tense with "have." The two approved syntactic positions for the adjective are before a noun (attributive: "the compiled binary") and after "to be," "to become," or "to stay" (predicative: "the binary is compiled"). When the past participle appears after "have," "has," or "had," it is a compound verb form prohibited by Rule 3.4.

**P1** — Use approved words from the controlled terminology. The past participle used as an adjective must be an approved word: either the fourth (past participle) form of an approved verb listed in the dictionary (BUILD → BUILT, COMPILE → COMPILED, ENCRYPT → ENCRYPTED), or a standalone adjective entry tagged "(adj)" that is the past participle form of an unapproved verb (DEPRECATED (adj), PERMITTED (adj)). If a word does not appear in either form in the dictionary, its past participle cannot be used as an adjective under Rule 3.3.

**P4** — Use only the approved forms of verbs and adjectives. Rule 1.4 is the general morphological rule; Rule 3.3 applies it to past participles specifically. Every approved verb has four listed forms, and the fourth is the past participle. Rule 3.3 permits this fourth form as an adjective. Rule 3.4 prohibits this same form as a verb in a compound tense. The two rules together define the boundary: the past participle form is approved only for the adjective role.

**P3** — Prefer the simpler construction. The adjective construction produces shorter, clearer sentences than the compound verb construction. "When the binary is compiled" (5 words) is simpler than "When you have compiled the binary" (6 words) and places the condition before any implied agent. The adjective form also eliminates the unnecessary action history — the reader needs to know the condition of the code entity, not who performed the action or when.
