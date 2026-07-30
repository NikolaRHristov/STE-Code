# Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

## Original Rule Summary

When you use two words together, do not make phrasal verbs. A verb and one or more prepositions can go together to form a phrasal verb with a meaning that is different from the meanings of its parts. Phrasal verbs usually have two meanings: the original, concrete meaning, and a more general, abstract meaning. To prevent ambiguity, it is not permitted to use approved words together to make a new phrase unless the phrasal verb is specifically approved in the dictionary.

## STE-Code Adaptation

When you use two words together in code documentation, do not make phrasal verbs. A verb and one or more prepositions can go together to form a phrasal verb with a meaning that is different from the meanings of its individual parts. To prevent ambiguity, do not use approved words together to make a new phrase unless the phrasal verb is specifically approved in the controlled terminology. Replace the phrasal verb with a single approved verb that has the same meaning.

## Examples

> **Non-STE:** The compiler puts out a warning when the type annotation is missing.
>
> **STE:** The compiler emits a warning when the type annotation is missing.
>
> *"Put" and "out" are approved words individually. Together, "put out" forms a phrasal verb with a meaning different from the approved meanings of "put" and "out." The approved verb "emit" has the meaning "to send out" and is the word that is most usual in code documentation.*

> **Non-STE:** The function gives off an error code when the input is not valid.
>
> **STE:** The function returns an error code when the input is not valid.
>
> *"Give" and "off" are approved words individually. Together, "give off" forms a phrasal verb with a meaning different from the approved meanings of "give" and "off." The approved verb "return" has the meaning "to send back a value" and is the correct word for this context in code documentation.*

> **Non-STE:** The cleanup task carries out the memory deallocation after each request.
>
> **STE:** The cleanup task does the memory deallocation after each request.
>
> *"Carry" and "out" are approved words individually. Together, "carry out" forms a phrasal verb. The approved verb "do" replaces the phrasal verb and keeps the same meaning.*

## Principles Applied

- **P1:** Use approved words from the controlled terminology — replace each unapproved phrasal verb with a single approved verb.
- **P2:** Use approved words only as the specified part of speech — the preposition in a phrasal verb changes function from a preposition to a particle that modifies the verb.
- **P3:** Use approved words only with their approved meanings — a phrasal verb creates a meaning that is not in the dictionary entry for either word.
- **P11:** One term per concept — using "set up" in one section and "configure" in another for the same action violates consistency.

---

*Adapted from ASD-STE100 Issue 9, Rule 9.3. See also: Rule 9.1 (Different Sentence Construction), Rule 9.2 (Use Each Approved Word Correctly).*
