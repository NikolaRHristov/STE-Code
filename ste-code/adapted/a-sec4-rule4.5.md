# Rule 4.5 — When Applicable, Use an Article (the, a, an) or a Demonstrative Adjective (this, these) Before a Noun or a Multi-Word Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.5

## Original Rule

Articles and demonstrative adjectives show the position of nouns and multi-word nouns in the sentence. Use articles and demonstrative adjectives correctly and do not omit them to make the text shorter.

It is not always correct English to put an article before a noun. Do not use articles in general statements or concepts.

In short sentences, it can be clearer to use articles before all nouns.

But sentences that contain a long series of items are clearer when you use the article only before the first noun in the series.

When you use the article in a series of items, always make sure that adjectives do not cause ambiguity.

A definite article is incorrect before a noun when an alphanumeric identifier comes after it. This is because the alphanumeric identifier shows that it is a proper noun.

## STE-Code Adaptation

Articles (the, a, an) and demonstrative adjectives (this, these) show the position of nouns and multi-word nouns in code documentation. Use them correctly and do not omit them to make the text shorter.

Do not use articles in general statements or when referring to abstract concepts in code (for example, "performance," "scalability," "error handling").

In short sentences, use articles before all nouns to make the text clear.

In sentences that contain a long series of items, use the article only before the first noun in the series. This keeps the text clear without unnecessary repetition.

When you use an article in a series of items, always make sure that adjectives do not cause ambiguity. If an adjective applies only to the first noun, the reader must know this from the article placement.

Do not use a definite article before a noun when a code identifier (function name, class name, variable name) comes after it. The identifier is a proper noun and does not need an article.

### Examples

**Using an article before a noun in a short instruction:**

> **Non-STE:** Call callback function.
>
> **STE:** Call the callback function.
>
> *Adapted from original rule principle — in short sentences, use articles before all nouns; no direct spec pair*

**Omitting articles in general statements:**

> **STE:** You can use equivalent alternatives for these middleware functions.
>
> *(No articles before "performance" or "scalability." The context does not give a specified metric.)*
>
> *Adapted from original rule principle — do not use articles in general statements or concepts; no direct spec pair*

**Using the article only before the first noun in a long series:**

> **STE:** Install the new configuration file, the log directory, the environment variables, and the startup script.
>
> *Adapted from original rule principle — use the article only before the first noun in a series; no direct spec pair*

**Using articles before each noun when an adjective applies to only one item:**

> **STE:** Install the new configuration file, the log directory, the environment variables, and the startup script.
>
> *(The article "the new" applies only to the configuration file. The remaining items are not described as new.)*
>
> *Adapted from original rule principle — make sure that adjectives do not cause ambiguity; no direct spec pair*

**No article before a noun with a code identifier:**

> **Non-STE:** Call the function `validateInput`.
>
> **STE:** Call function `validateInput`.
>
> *Adapted from original rule principle — a definite article is incorrect before a noun when an alphanumeric identifier comes after it; no direct spec pair*

> **Non-STE:** Configure the module `AuthService`.
>
> **STE:** Configure module `AuthService`.
>
> *Adapted from original rule principle — a definite article is incorrect before a noun when an alphanumeric identifier comes after it; no direct spec pair*
