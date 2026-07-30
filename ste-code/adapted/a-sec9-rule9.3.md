# Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 9.3

## Original Rule

When you use two words together, do not make phrasal verbs.

In English, a verb and one or more prepositions can go together to form a "phrasal verb." This phrasal verb has a meaning that is different from the meanings of its parts. Phrasal verbs usually have two meanings: the original, more concrete meaning, and a more general and abstract meaning.

To prevent ambiguity, it is not permitted in STE to use approved words together to make a new phrase (phrasal verb).

You will not usually find phrasal verbs listed as "not approved" in the dictionary. When you write a standard English sentence in STE, always make sure that the new sentence is grammatically correct. And make sure that you use the approved words with the meaning that they have in the dictionary.

Only a small number of phrasal verbs are approved in the dictionary. They all have a restricted meaning.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.2 — Use Each Approved Word Correctly

When you use two words together in code documentation, do not make phrasal verbs.

A verb and one or more prepositions can go together to form a phrasal verb with a meaning that is different from the meanings of its individual parts. Phrasal verbs usually have two meanings: the original, concrete meaning, and a more general, abstract meaning. To prevent ambiguity, do not use approved words together to make a new phrase unless the phrasal verb is specifically approved in the controlled terminology.

Replace the phrasal verb with a single approved verb that has the same meaning. When you write a standard English sentence in the controlled terminology, always make sure that the new sentence is grammatically correct and that you use the approved words with the meaning that they have in the controlled terminology.

Only a small number of phrasal verbs are approved. They all have a restricted meaning.

### Examples

> **Non-STE:** The compiler puts out a warning when the type annotation is missing.
>
> **STE:** The compiler emits a warning when the type annotation is missing.

("Put" and "out" are approved words individually. Together, "put out" forms a phrasal verb with a meaning different from the approved meanings of "put" and "out." The approved verb "emit" has the meaning "to send out" and is the word that is most usual in code documentation.)
*Adapted from spec pair: "Put out the fire." (abstract) / "Extinguish the fire." — "put" and "out" are approved individually, but together they form a phrasal verb; the approved verb "extinguish" replaces it.*

> **Non-STE:** The function gives off an error code when the input is not valid.
>
> **STE:** The function returns an error code when the input is not valid.

("Give" and "off" are approved words individually. Together, "give off" forms a phrasal verb with a meaning different from the approved meanings of "give" and "off." The approved verb "return" has the meaning "to send back a value" and is the correct word for this context in code documentation.)
*Adapted from spec pair: "Give off gas." / "Release gas." — "give" and "off" are approved individually, but together they form a phrasal verb; the approved verb "release" replaces it.*

> **Non-STE:** The cleanup task carries out the memory deallocation after each request.
>
> **STE:** The cleanup task does the memory deallocation after each request.

("Carry" and "out" are approved words individually. Together, "carry out" forms a phrasal verb. The approved verb "do" replaces the phrasal verb and keeps the same meaning.)
*Adapted from spec pattern: replace unapproved phrasal verbs with a single approved verb that has the same meaning.*
