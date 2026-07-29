# Rule 2.2 — Long Technical Nouns (Shorter Forms and Hyphens)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.2

## Original Rule

When a technical noun has more than three words, write it in full. Then, you can use one of these methods to make the technical noun clear:

- Give a shorter form of the technical noun.
- Use hyphens (-) between words that you use as one unit.

A long multi-word noun can be a long technical noun, or it can be a combination of shorter technical nouns. Frequently, it is not possible to divide technical nouns into smaller parts because they are the technical nouns that your company, industry, or subject field uses. Thus, you must write technical nouns as they are, in their approved form.

**Method 1 – Shorter form of technical nouns:** If a long technical noun comes from an official document (for example, an engineering drawing or an illustrated parts catalog), write it in full the first time that it occurs in the text. Then, if it is possible, explain the technical noun and in the remaining text of your document, use a shorter form or an approved abbreviation.

**Method 2 – Hyphens:** A hyphen is a punctuation mark that connects words or parts of words. You can use hyphens between words to show how related words operate as one unit. Hyphenated words always count as one word. Make sure that you do not connect words which are not related, because this hyphen will change the meaning of the multi-word noun. Do not use hyphens to make groups of more than three words. If an approved technical noun includes three words or less, it is not necessary to use hyphens. But, if an approved technical noun includes a hyphen, do not remove the hyphen.

## STE-Code Adaptation

In code documentation, some technical terms have more than three words and cannot be broken down because they are the official names used by your company, programming language, framework, or subject field. Examples include formal class names, design pattern names, official API names, or names from architecture diagrams.

**Method 1 – Shorter form:** Write the long technical noun in full the first time it occurs. Provide an explanation, then use a shorter form or the official abbreviation in the remaining text. Do not abbreviate technical nouns that already have three words or fewer.

**Method 2 – Hyphens:** Use hyphens to group related words that function as a single unit within a multi-word noun. A hyphenated group counts as one word. Do not hyphenate words that are not related, and do not create hyphenated groups of more than three words. If an official technical noun already contains a hyphen (for example, from the source code or framework documentation), keep the hyphen.

### Examples

**Method 1 – Shorter form with explanation:**

> **Non-STE:** The API request handler middleware authentication token validator processes each incoming request before it reaches the controller layer.
> **STE:** The API request handler middleware authentication token validator (the component that validates authentication tokens in the middleware layer, referred to in this document as the "authentication token validator") processes each incoming request before it reaches the controller layer.

**Method 1 – Shorter form with official abbreviation:**

> **Non-STE:** The Document Object Model event listener registration manager must track all active listeners for each node in the tree.
> **STE:** The Document Object Model (DOM) event listener registration manager must track all active listeners for each node in the tree. The DOM event listener manager operates in the browser rendering pipeline.

**Method 2 – Hyphens between related words:**

> **Non-STE:** Move the error handler timeout checker configuration to the environment variables file. (4 words in the multi-word noun, not correct)
> **STE:** Move the error-handler timeout-checker configuration to the environment variables file. (3 words: "error-handler," "timeout-checker," and "configuration")

**Method 2 – Keeping official hyphens:**

> **Non-STE:** The data-access layer query builder interface provides a fluent API for constructing SQL statements. (removes the official hyphen, "dataaccess" is not the approved term)
> **STE:** The data-access layer query builder interface provides a fluent API for constructing SQL statements. (keeps the official hyphen from the framework documentation)

**Do not abbreviate short technical nouns:**

> **Non-STE:** The primary parts of the system are the DTL (data transfer layer), the CR (command router), and the EB (event bus).
> **STE:** The primary parts of the system are the data transfer layer, the command router, and the event bus.
