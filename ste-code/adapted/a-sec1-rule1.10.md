# Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.10

## Original Rule

**Rule 1.10** Do not use regional, slang, or jargon words as technical nouns.

There can be technical words that only persons in confined regions or geographical areas use. These words are not easy to understand for persons who are from a different region or area. When you select technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication.

Examples:

[The spec gives examples of regional and jargon terms:]

"Skid road" is a term used in some regions of North America and Canada, Northern Europe, and New Zealand. Its meaning is not immediately clear to the reader.

> **STE:** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

"Gear" is technical jargon that refers to tools and equipment, and its meaning is not immediately clear to the reader.

> **STE:** During logging operations, attach a cable to the heavy machinery to hold the logs in their position.

## STE-Code Adaptation

**Rule 1.10** Do not use regional, slang, or jargon words as code-domain technical nouns.

There can be technical words that only persons in confined communities or specific programming language ecosystems use. These words are not easy to understand for persons who are from a different background or use a different technology stack. When you select code-domain technical nouns, always use well-known words.

This rule is also applicable to technical slang or jargon words. If only a small number of persons understand a word, it will cause confusion and non-effective communication. Code documentation is read by developers with diverse backgrounds, including junior developers, developers from different language communities, and non-native English speakers.

### Examples

> **Non-STE:** Remove all the cruft from the legacy module.
> **STE:** Remove all the unnecessary code from the legacy module.

> *Adapted from spec example: "Gear" is technical jargon for "tools and equipment" — its meaning is not immediately clear to the reader. Just as "gear" is unclear to readers outside a specific community, "cruft" is hacker jargon that means "poorly designed or unnecessary code." Its meaning is not immediately clear to readers who are not familiar with the jargon. The STE version uses the approved words "unnecessary code," just as the spec example replaces "gear" with the clearer phrase "tools and equipment."*

> **Non-STE:** The function monkeys with the input data before validation.
> **STE:** The function changes the input data before validation.

> *Adapted from spec example: "Skid road" is a regional term not understood by readers from other areas. Just as "skid road" is a forestry term used only in specific regions, "monkey with" is slang used only in certain developer communities. Its meaning ("to tamper with or change in an uncontrolled way") is not clear to non-native English readers or developers from other backgrounds. The STE version uses the approved verb "change."*
