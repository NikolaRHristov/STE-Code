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
>
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
>
> **STE:** If you pass the socket to the handler function before the socket is initialized, the handler function can fail.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — both ambiguous "it" pronouns are resolved to their specific referents.*
>
> (The first "it" refers to "the socket"; the second "it" is ambiguous. Replace both pronouns with the specific nouns to make the sentence clear.)

> **Non-STE:** The cache stores results from the database query. They expire after one hour.
>
> **STE:** The cache stores results from the database query. The cached results expire after one hour.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "They" replaced by "The cached results."*
>
> (The pronoun "They" can refer to "results" or "the database query." Replacing "They" with "The cached results" makes the sentence clear.)

> **Non-STE:** When you call this endpoint, it returns the user profile with their permissions.
>
> **STE:** When you call this endpoint, the endpoint returns the user profile with the user's permissions.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "it" replaced by "the endpoint," and the unapproved pronoun "their" replaced by "the user's."*
>
> (The pronoun "it" is ambiguous — it can refer to "this endpoint" or to the act of calling. The pronoun "their" is not in the controlled vocabulary.)

> **Non-STE:** The parser scans the input stream and tokenizes it. That makes it available to the compiler pass.
>
> **STE:** The parser scans the input stream and tokenizes the input stream. The tokenization makes the tokenized stream available to the compiler pass.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — all three ambiguous pronouns are resolved to their specific referents.*
>
> (The first "it" refers to "the input stream." "That" refers to the tokenization process. The second "it" refers to the tokenized stream. Replace each pronoun with the specific noun.)

> **Non-STE:** These variables control the connection timeout. Set them before you start the application.
>
> **STE:** These variables control the connection timeout. Set the timeout variables before you start the application.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "them" replaced by "the timeout variables."*
>
> (The pronoun "them" can refer to "These variables" or to some other variables in an earlier sentence. Repeating the noun prevents ambiguity.)

> **Non-STE:** The module exports two functions. Use those when you process user input.
>
> **STE:** The module exports two functions. Use the exported functions when you process user input.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "those" replaced by "the exported functions."*
>
> (The pronoun "those" can refer to "two functions" or to other items in the surrounding text. The explicit noun removes the ambiguity.)

> **Non-STE:** The API key is stored in the configuration file. Make sure it is valid before you deploy.
>
> **STE:** The API key is stored in the configuration file. Make sure the API key is valid before you deploy.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "it" replaced by "the API key."*
>
> (The pronoun "it" can refer to "The API key" or to "the configuration file." Replacing "it" with the specific noun makes the instruction unambiguous.)

> **Non-STE:** The loop iterates over the array and the index. When it reaches the last element, the loop stops.
>
> **STE:** The loop iterates over the array and the index. When the loop reaches the last element, the loop stops.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "it" replaced by "the loop."*
>
> (The pronoun "it" can refer to "the loop," "the array," or "the index." Replacing "it" with "the loop" removes the ambiguity.)

> **Non-STE:** If the configuration uses the default settings, it will override your custom values.
>
> **STE:** If the configuration uses the default settings, the default configuration will override your custom values.
>
> *Adapted from spec rule: "replace the pronoun with the word that it refers to" — "it" replaced by "the default configuration."*
>
> (The pronoun "it" can refer to "the configuration" or to "the default settings." The corrected sentence specifies that the default configuration does the overriding.)
