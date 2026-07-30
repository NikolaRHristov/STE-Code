# Rule 3.3 — Use the Past Participle Form as an Adjective

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.3

## Original Rule

Use the past participle form as an adjective.

When you use the past participle form as an adjective, it shows the condition of something. This is not passive voice. Use the past participle form of a verb as an adjective as follows:

- Before a noun
- After a verb form of the verbs "to be," "to become," or "to stay."

Do not use the past participle form if it is not in the dictionary.

Examples:

> **STE:** Examine all parts of the disassembled unit for damage.
> ("Disassembled" is an adjective before the noun "unit." It shows the condition of the unit.)

> **Source:** Issue 9, Part 1 — Writing rules, Page 1-3-2, 2025-01-15

> **STE:** When the unit is fully disassembled, clean all the parts.
> ("Disassembled" is an adjective after the verb "to be" that shows the condition of the unit.)

There are also approved adjectives in the dictionary that are the past participle form of verbs that are not approved. For example, "permitted," and "damaged." Their approved part of speech in the dictionary is "(adj)" and thus you can use them.

## STE-Code Adaptation

Use the past participle form of an approved verb only as an adjective. The past participle as an adjective describes the condition of a code entity (a file, a binary, a service, a module) and is not a verb form in a compound tense.

Use the past participle form as an adjective in these two positions:

- Before a noun: "the compiled binary," "the encrypted payload," "the deprecated endpoint"
- After a verb form of "to be," "to become," or "to stay": "When the binary is compiled," "After the module becomes initialized," "The service stays connected"

Do not use the past participle as part of a compound verb construction with "have" (Rule 3.4). If a past participle form is not listed in the approved vocabulary, do not use it.

> **See also:** Rule 3.4 — Do Not Use Auxiliary Verbs to Make Complex Verb Constructions

The STE-Code vocabulary also has approved adjectives that are the past participle form of verbs that are not approved as verbs. For example, "deprecated" is approved as an adjective (adj) even though "deprecate" is not an approved verb. You can use these adjectives when they describe a condition.

### Examples

The sentence below is already in STE because "compiled" is an adjective before the noun "binary," not a verb in a compound tense:

> **STE:** Examine all parts of the compiled binary for errors.

> *Adapted from spec pair: "Examine all parts of the disassembled unit for damage."* Just as "disassembled" is an adjective before the noun "unit" in STE, "compiled" is an adjective before the noun "binary" in STE-Code. Both describe the condition of the thing being examined.

The pairs below show transformations from non-compliant compound-verb constructions to compliant adjective usage:

> **Non-STE:** When you have compiled the binary, run the test suite.
> **STE:** When the binary is compiled, run the test suite.
> ("Compiled" is an adjective after the verb "to be" that shows the condition of the binary.)

> *Adapted from spec pair: "When the unit is fully disassembled, clean all the parts."* Just as "disassembled" after "is" describes the condition of the unit in STE, "compiled" after "is" describes the condition of the binary in STE-Code. This is an adjective, not a passive verb construction.

> **Non-STE:** Review all of the updated configuration settings that the script has generated.
> **STE:** Review all the updated configuration settings.
> ("Updated" is an adjective before the noun "configuration settings." It shows the condition of the settings.)

> *Adapted from spec pair: "Examine all parts of the disassembled unit for damage."* Just as "disassembled" is a past participle used as an adjective before the noun in STE, "updated" is a past participle used as an adjective before "configuration settings" in STE-Code. The compound verb construction "has generated" is removed entirely, leaving only the adjective "updated" to describe the condition.
