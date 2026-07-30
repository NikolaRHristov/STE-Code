# GR-3 — How to Use Pronouns

> **Source:** Adapted from ASD-STE100 Issue 9, GR-3

## Original Rule

How to use pronouns (general recommendation, not an STE rule).

Pronouns refer to a person, a location, or an item that is already in a text. Examples of pronouns are "it," "they," "that," "these," and "those." If you use the pronouns correctly, your text will be easy to read.

In STE, the approved pronouns are in the dictionary. Do not use a pronoun if it is not in the dictionary (for example, "she" or "he").

If a pronoun can refer to one or more nouns in a text, it can cause ambiguity in a sentence. If there is ambiguity, replace the pronoun with the word that it refers to. This will make the sentence clear and easier to read.

## STE-Code Adaptation

In code documentation, pronouns refer to an item, a concept, or an entity that is already in the text. Examples of approved pronouns include "it," "they," "that," "these," and "those." Do not use pronouns that are not in the controlled terminology.

If a pronoun can refer to one or more nouns in a text, it can cause ambiguity. In code documentation, this is especially important because the reader must understand precisely which component, function, module, or parameter is affected. If there is ambiguity, replace the pronoun with the specific word that it refers to. This makes the sentence clear and prevents the reader from taking the wrong action.

### Examples

> **Non-STE:** If you configure the middleware before the route handler, it can block the request.
> **STE:** If you configure the middleware before the route handler, the middleware can block the request.
>
> *Adapted from spec rule: "If a pronoun can refer to one or more nouns in a text, it can cause ambiguity... replace the pronoun with the word that it refers to." — "it" replaced by "the middleware."*
>
> (The pronoun "it" can refer to either "the middleware" or "the route handler." Replacing "it" with "the middleware" makes the sentence clear.)

Or:

> **STE:** If you configure the middleware before the route handler, the route handler can block the request.

Or:

> **STE:** If you configure the middleware before the route handler, the middleware and the route handler can block the request.

> **Non-STE:** If you pass the socket to the handler function before it is initialized, it can fail.
> **STE:** If you pass the socket to the handler function before the socket is initialized, the handler function can fail.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — both ambiguous "it" pronouns are resolved to their specific referents.*
>
> (The first "it" refers to "the socket"; the second "it" is ambiguous. Replace both pronouns with the specific nouns to make the sentence clear.)
