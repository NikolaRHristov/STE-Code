# Rule 4.5 — Use an Article or a Demonstrative Adjective Before a Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.5
> **Source:** [master.md#sec4-rule4.5](ste-code/grouped/)
> Source: master.md#sec4-rule4.5

## Original Rule

Articles and demonstrative adjectives show the position of nouns and multi-word nouns in the sentence. Use articles and demonstrative adjectives correctly and do not omit them to make the text shorter.

It is not always correct English to put an article before a noun. Do not use articles in general statements or concepts.

In short sentences, it can be clearer to use articles before all nouns.

But sentences that contain a long series of items are clearer when you use the article only before the first noun in the series.

When you use the article in a series of items, always make sure that adjectives do not cause ambiguity.

A definite article is incorrect before a noun when an alphanumeric identifier comes after it. This is because the alphanumeric identifier shows that it is a proper noun.


> *Adapted from spec pair:* Non-STE: The side stay assembly has two folding toggles hinged together and attached with hinges between the main gear strut and the side stay bracket. (This sentence contains more than one topic. To make this information clearer, you can write a new sentence for each topic.)  |  STE: <u>The side stay assembly has two folding toggles. The folding toggles are attached</u> together with hinges. These folding toggles are also attached with hinges between the main gear strut and the side stay bracket. (The new text has three sentences, and each sentence has its topic. Refer to the underlined text for the specified subjects in each sentence.)
### Examples (from source):

> **Non-STE:** Turn shaft assembly.
>
> **STE:** Turn the shaft assembly.
>
> **Non-STE:** Data module tells you how to operate unit.
>
> **STE:** This data module tells you how to operate the unit.
>
> **STE:** Install the nuts (2) and the bolts (3).
>
> **STE:** Discard the O-rings (3), gaskets (4), seals (7), and washers (9).
>
> **STE:** Install the new O-rings (15), spacers (14), nut (13), and safety pin (12).
>
> **Incorrect:** Tag the circuit breaker 36L7
>
> **Correct:** Tag circuit breaker 36L7.

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 4.1 — One Topic Per Sentence, No Abstract Text
> **See also:** Rule 4.2 — Do Not Omit Words or Use Contractions
> **See also:** Rule 4.5 — Use an Article or a Demonstrative Adjective Before a Noun

## STE-Code Adaptation

Articles (the, a, an) and demonstrative adjectives (this, these) show the position of nouns and multi-word nouns in code documentation. Use them correctly and do not omit them to make the text shorter.

Do not use articles in general statements or when referring to abstract concepts in code (for example, "performance," "scalability," "error handling").

In short sentences, use articles before all nouns to make the text clear.

In sentences that contain a long series of items, use the article only before the first noun in the series. This keeps the text clear without unnecessary repetition.

When you use an article in a series of items, always make sure that adjectives do not cause ambiguity. If an adjective applies only to the first noun, the reader must know this from the article placement.

Do not use a definite article before a noun when a code identifier (function name, class name, variable name) comes after it. The identifier is a proper noun and does not need an article.

### Code-Domain Examples

**Article before a noun in a short instruction:**

> **Non-STE:** Call callback function.
>
> **STE:** Call the callback function.

**No article in a general statement:**

> **STE:** Error handling is important for production applications. The function throws an error when the input is not valid.

**Article only before the first noun in a long series:**

> **Non-STE:** Discard O-rings, gaskets, seals, and washers.
>
> **STE:** Discard the O-rings, gaskets, seals, and washers.

**Article before each noun when an adjective applies to only one item:**

> **Non-STE:** Install new O-rings, spacers, nut, and safety pin.
>
> **STE:** Install the new O-rings, the spacers, the nut, and the safety pin. (Only the O-rings are new.)

**No article before a noun with a code identifier:**

> **Non-STE:** Call the function `validateInput`.
>
> **STE:** Call function `validateInput`.
>
> **Non-STE:** Configure the module `AuthService`.
>
> **STE:** Configure module `AuthService`.

**Demonstrative adjective for sentence linking:**

> **Non-STE:** The function returns a configuration object. Configuration object has three fields: host, port, and timeout.
>
> **STE:** The function returns a configuration object. This object has three fields: host, port, and timeout.

### Paradigm-Specific Guidance

- **Object-Oriented:** Use articles to distinguish a class (type) from an instance. "The `ConnectionPool` class manages a pool of database connections." No article directly before a bare identifier used as a proper noun: "Call `connect`."
- **Functional:** Use articles to distinguish a type constructor from a value. "The `Ok(value)` pattern represents a successful result."
- **Procedural (C, Go, Bash):** Use articles to distinguish a pointer (address) from the pointed-to value. "The function receives a pointer to a buffer."
- **Declarative (SQL, Terraform, YAML):** Use articles to distinguish a resource type from a resource instance. "A `Deployment` resource manages a set of pods."
- **Systems (Rust, C memory):** Use articles to make ownership and lifetime relationships unambiguous. "The pointer must point to an initialized region of memory."

### Edge Cases

- **Identifier as proper noun vs concept:** `ConnectionPool` used alone is a proper noun (no article). "The `ConnectionPool` class" uses "the" because "class" is the noun. "Call `initialize`" has no article; "The `initialize` function" has "the" because "function" is the noun.
- **"a" vs "an":** Use "an" before a vowel sound (an SQL query, an HTML element, an XML parser). Use "a" before a consonant sound (a URL, a Unix system). Choose the form that matches the common pronunciation.
- **Headings and titles:** Headings may omit articles for brevity. The first sentence below a heading must use the full article rule.
- **Framework names with "The":** Treat a name such as `TheMovieDB` as a proper noun. The leading "The" is part of the identifier.

### Grammar Notes

- **Definite vs indefinite:** "A" refers to any instance of a type. "The" refers to a specific, identifiable item. No article refers to the type as a whole.
- **First mention vs later mention:** Use "a" on first introduction ("throws a `ValidationError`"). Use "the" on later reference ("the `ValidationError` contains a message").
- **Proper noun exception:** A code identifier is a proper noun. Do not place a definite article directly before it. "Call `connect`" is correct; "Call the `connect`" is not.

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 4.1** — Use short sentences and one topic per sentence.
- **Rule 4.2** — Do not omit articles to make the sentence shorter.
- **Section 5 (Procedural Writing)** — Article use in instructions.
- **Section 6 (Descriptive Writing)** — Article use in descriptions.

## Summary Checklist

- [ ] Articles and demonstrative adjectives are used correctly.
- [ ] No article appears in general statements or abstract concepts.
- [ ] Short sentences use articles before all nouns.
- [ ] Long series use the article only before the first noun, unless an adjective applies to one item only.
- [ ] No definite article appears directly before a code identifier used as a proper noun.
