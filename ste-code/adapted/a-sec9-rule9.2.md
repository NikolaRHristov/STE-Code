# Rule 9.2 — Use Each Approved Word Correctly

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 9.2

## Original Rule

Use each approved word correctly.

Some STE-approved words have meanings that are applicable only in some contexts (restricted meaning). Before you use a word, read its definition in the approved meaning column of the dictionary. Words frequently have many different meanings in standard English. In STE, approved words usually only have one approved meaning. Other meanings that the word can have in standard English are not approved.

Always make sure that the word that you select has the correct meaning in the applicable context.

Also, make sure that you use approved words as their approved part of speech. In English, words usually do not have different forms that immediately show their function in a sentence. Thus, readers can frequently think differently about the same word. To make sentences clearer, an approved word can usually only have one function (part of speech). In STE, use each approved word as the approved part of speech.

There are a small number of words that are approved as more than one part of speech and have more than one meaning. These words are important and frequently occur in technical English.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

Use each approved word correctly in code documentation.

Some words in the controlled terminology have restricted meanings that apply only in specific contexts. Before you use a word, read its definition in the approved meaning column of the controlled terminology. Words frequently have many different meanings in standard English. In the controlled terminology, approved words usually have only one approved meaning. Other meanings that the word can have in standard English are not approved.

Always make sure that the word that you select has the correct meaning in the applicable code documentation context.

Also, make sure that you use approved words as their approved part of speech. In English, words do not usually have different forms that immediately show their function. Thus, use each approved word as the approved part of speech only.

A small number of words are approved as more than one part of speech and have more than one meaning. These words are important and occur frequently in software development documentation.

### Examples

> **Non-STE:** Execute the initialization script before you start the server.
> **STE:** Run the initialization script before you start the server.

(The word "execute" has the restricted meaning "to carry out a death sentence" in standard English. In the controlled terminology, "execute" is not approved. Use "run" for this context.)
*Adapted from spec pair: "Wear protective clothing." / "Use (or put on) protective clothing." — "wear" is approved only with the meaning "to become damaged by friction," not "to have on one's body."*

> **Non-STE:** When the error count goes down, restart the service.
> **STE:** When the error count decreases, restart the service.

(The verb "goes" together with the preposition "down" is a phrase that refers to a physical movement. "Decrease" is better because it refers to the error count, not to a physical indicator that monitors the count.)
*Adapted from spec pair: "When the pressure goes down, lift the cover." / "When the pressure decreases, lift the cover."*

> **Non-STE:** Log the exception details to the output stream.
> **STE:** Write the exception details to the log.

(The word "log" is approved as a noun, but not as a verb. Use the approved noun "log" with the approved verb "write.")
*Adapted from spec pair about part of speech: use each word only in its approved part of speech. "Log" as a verb is not approved; use the approved noun form.*

> **Non-STE:** The config help shows all available command-line options.
> **STE:** The configuration help text shows all available command-line options.

(The word "help" is approved as a verb, but not as a noun. Use the approved noun "help text" or rewrite the sentence.)
*Adapted from spec pair about part of speech: "help" is approved as a verb, not as a noun.*

> **Non-STE:** The recursive call damaged the call stack.
> **STE:** The recursive call caused damage to the call stack.

(The word "damage" is approved as a noun, but not as a verb. Use "cause damage" or "do damage" instead of the verb form.)
*Adapted from spec pair about part of speech: "damage" is approved as a noun, not as a verb.*

> **STE:** Flush the output buffer before you close the file handle.

("Flush" is a verb here with the approved meaning "to remove remaining data from a buffer.")
*Adapted from spec pair: "Flush the pipes with a disinfectant solution." — "flush" as a verb with the approved meaning "to remove something or to operate with a flow of liquid."*

> **STE:** Make sure that the connector is flush with the port.

("Flush" is an adjective here with the approved meaning "where one surface fully touches a different surface." The word "flush" is approved as both a verb and an adjective because the different positions and contexts make it easy to see their function.)
*Adapted from spec pair: "Make sure that the surface is flush with the mating surface." — "flush" as an adjective with the approved meaning "a condition where one surface fully touches a different surface."*
