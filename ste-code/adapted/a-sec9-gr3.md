# GR-3 — How to Use Pronouns

> **Source:** Adapted from ASD-STE100 Issue 9, General Recommendation GR-3

> **Source:** [master.md#sec9-gr3](ste-code/grouped/)

> Source: master.md#sec9-gr3

## Original Rule

Pronouns refer to a person, a location, or an item that is already in a text. Examples of pronouns are "it," "they," "that," "these," and "those." If you use the pronouns correctly, your text will be easy to read.

In STE, the approved pronouns are in the dictionary. Do not use a pronoun if it is not in the dictionary (for example, "she" or "he").

If a pronoun can refer to one or more nouns in a text, it can cause ambiguity in a sentence. If there is ambiguity, replace the pronoun with the word that it refers to. This will make the sentence clear and easier to read.

### Examples

> **Do not write:** If you engage the pins incorrectly with the seats, they can become damaged.
>
> **WRITE:** If you engage the pins incorrectly with the seats, the pins can become damaged.
>
> Or: If you engage the pins incorrectly with the seats, the seats can become damaged.
>
> Or: If you engage the pins incorrectly with the seats, the pins and seats can become damaged.

## Adapted Rule

Pronouns refer to a person, a location, or an item that is already in a text. Examples of pronouns are "it," "they," "that," "these," and "those." If you use the pronouns correctly, your text will be easy to read.

In code documentation, the approved pronouns are in the controlled terminology. Do not use a pronoun if it is not in the controlled terminology (for example, "she" or "he").

If a pronoun can refer to one or more nouns in a text, it can cause ambiguity in a sentence. If there is ambiguity, replace the pronoun with the word that it refers to. This will make the sentence clear and easier to read.

### Examples

> **Non-STE:** If you call the API incorrectly with the credentials, they can become invalid.
>
> **STE:** If you call the API incorrectly with the credentials, the credentials can become invalid.
>
> Or: If you call the API incorrectly with the credentials, the API can become invalid.
>
> Or: If you call the API incorrectly with the credentials, the API and the credentials can become invalid.

(Without the repetition, "they" could mean the API, the credentials, or both. State the referent so the reader knows what becomes invalid.)

> **Non-STE:** When you update the record and the index, make sure that it is consistent.
>
> **STE:** When you update the record and the index, make sure that the index is consistent.
>
> Or: When you update the record and the index, make sure that the record is consistent.

("It" refers to either "the record" or "the index." Replace "it" with the correct noun.)

> **Non-STE:** The function returns a value. If it is null, log a warning.
>
> **STE:** The function returns a value. If the value is null, log a warning.

("It" could refer to the function or the value. State "the value" to remove the ambiguity.)

## Code-Domain Explanation

GR-3 prevents pronoun ambiguity, which is common in code documentation because sentences frequently name two or more technical items (a function and its argument, a service and its dependency, a record and its index). When a pronoun like "it" or "they" sits between two possible referents, the reader must guess.

Two practices remove the ambiguity:

1. **Repeat the noun.** When the referent is unclear, write the noun again. This adds words but removes doubt. In code documentation, clarity wins over brevity.
2. **Keep the referent close.** When you must use a pronoun, put the noun it refers to in the same sentence or the immediately preceding one.

The rule also restricts pronouns to the approved set. Gender-specific pronouns ("he," "she") are not permitted (see GR-7, Inclusive Language). Use "you" for the reader, "it" for a single item, and "they" or "these"/"those" for plural items that are already named.

## Edge Cases

### Pronouns that refer to code symbols

When a pronoun refers to a code symbol in code font, the symbol is a technical noun (Rule 1.5). The pronoun still must be approved, and it still must have a clear referent. "The function `parse()` returns a token. If it is empty, stop." — here "it" clearly refers to "a token," not to `parse()`. Keep the distance short.

### "They" as a plural technical noun

"The modules can fail. If they fail, retry." is clear because "they" refers to "the modules" in the preceding sentence. When the preceding sentence names both modules and a server, repeat the noun: "If the modules fail, retry."

## Cross-References

- **GR-4 (The Pronoun "this"):** A special case of pronoun clarity. "This" at the start of a sentence must have an unambiguous referent.
- **Rule 9.2 (Use Each Approved Word Correctly):** Use only approved pronouns. Do not introduce "he," "she," or other non-approved pronouns.
- **Rule 4.1 (Sentence Structure):** Short sentences with the noun and its pronoun close together reduce ambiguity.
- **GR-7 (Inclusive Language):** Gender-specific pronouns are not permitted; use neutral constructions.
