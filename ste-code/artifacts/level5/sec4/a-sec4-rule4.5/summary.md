# Rule 4.5 — When Applicable, Use an Article (the, a, an) or a Demonstrative Adjective (this, these) Before a Noun or a Multi-Word Noun

## Original Rule Summary

Rule 4.5 requires writers to use articles (the, a, an) and demonstrative adjectives (this, these) before nouns and multi-word nouns when they show the position of the noun in the sentence. Do not omit articles to make the text shorter. Do not use articles in general statements or when referring to concepts. In short sentences, use articles before all nouns for clarity, but in sentences with a long series of items, use the article only before the first noun. Never use a definite article before a noun when an alphanumeric identifier follows it, because the identifier shows that it is a proper noun.

## STE-Code Adaptation

Rule 4.5 in STE-Code applies article and demonstrative adjective rules to code documentation. Use articles to show whether a noun refers to a specific instance (the configuration file) or a general concept (configuration). Do not omit articles to make documentation text shorter — missing articles cause ambiguity about what the reader must act on. Do not use a definite article before a noun that is immediately followed by a code identifier such as a function name, class name, or variable name, because the identifier is a proper noun. In sentences that contain a long series of items, use the article only before the first noun to avoid unnecessary repetition.

## Example Pairs

> **Non-STE:** Call callback function after request completes.
>
> **STE:** Call the callback function after the request completes.
>
> *(P4 applied: short instruction with articles before all nouns. The Non-STE omits articles for brevity, but the STE version adds "the" before "callback function" and "request" to show these are specific items the reader must identify.)*

> **Non-STE:** Call the function `validateInput` with the parameter `userId`.
>
> **STE:** Call function `validateInput` with parameter `userId`.
>
> *(Rule 4.5 applied: no definite article before a noun with a code identifier. The identifiers `validateInput` and `userId` are proper nouns. The Non-STE incorrectly places "the" before them. The STE version removes the articles.)*

> **Non-STE:** The performance is critical. The scalability requires the caching layer.
>
> **STE:** Performance is critical. Scalability requires a caching layer.
>
> *(P1 applied: no article before general concepts. "Performance" and "scalability" are abstract concepts — they do not take a definite article. The Non-STE incorrectly treats them as specific items. The STE version omits the article for concepts and uses "a" for "caching layer" because it is one possible instance, not a previously identified layer.)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. Articles are function words that connect approved nouns. Every noun that takes an article must be an approved word from the STE-Code dictionary. When a noun is a general concept, omit the article to signal that it is abstract, not a specific instance.

**P4** — Write short sentences (maximum 20 words for procedures, 25 for descriptions). Articles help short sentences remain grammatical and clear. When a sentence is short, use articles before all nouns so the reader can identify each item quickly. Do not omit articles to save space in short instructions — the clarity gain from each article is greater than the space cost.

**P9** — Use correct article placement before nouns and multi-word nouns. Rule 4.5 is itself the P9 principle. An article before a noun tells the reader that the noun refers to a specific, identified instance. No article before a noun tells the reader that the noun refers to a general concept or category. Do not use a definite article before a noun followed by a code identifier, because the identifier already acts as a proper noun.

**P11** — One term per concept. Apply consistent article patterns across the documentation. When a noun takes an article in one section, use the same article pattern for that noun in other sections. If a noun is introduced with "a" (indefinite, first mention), use "the" (definite, known reference) on subsequent mentions of that same instance.
