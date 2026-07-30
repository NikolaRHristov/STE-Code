# Rule 1.9 — When You Must Select a Technical Noun, Use One Which Is Short and Easy to Understand

## Original Rule Summary

Rule 1.9 directs writers to select technical nouns that are short (not more than three words) and easy to understand. When no approved technical noun exists in the company, industry, or subject field, the writer must select the shortest term that is unambiguous in context rather than constructing a long descriptive phrase. The original ASD-STE100 example demonstrates the principle: "stainless steel pan head machine screws" becomes simply "screws" because the index number and illustration already identify the part. If the context does not provide enough identification, the writer may add one or two adjectives to the noun to help the reader understand — but no more than necessary for disambiguation.

## STE-Code Adaptation

Rule 1.9 in STE-Code applies the same brevity principle to code documentation: select code-domain technical nouns that are short and easy to understand. Documentation writers often construct long noun phrases by stacking modifiers, embedding type information, or chaining synonyms — "the asynchronous JavaScript XML HTTP request wrapper utility function" — when the shortest unambiguous term is sufficient: "the fetch utility." The adaptation directs writers to rely on context sources such as line numbers, code snippets, API references, diagrams, and preceding definitions to carry the identifying detail, so the noun phrase itself can remain lean. When context alone is not enough, add one or two adjectives for disambiguation, but never more than three words total unless the term is an established multi-word standard like "abstract syntax tree" or "continuous integration pipeline."

## Example Pairs

> **Non-STE:** This is a high-performance, event-driven, non-blocking I/O model JavaScript runtime environment built on Chrome's V8 JavaScript engine that uses an asynchronous, single-threaded event loop architecture for building scalable network applications.
>
> **STE:** Node.js is a JavaScript runtime. It uses an event-driven, non-blocking I/O model. Use it to build scalable network applications.
>
> *(P9 applied: the 42-word noun phrase collapses to "Node.js" [2 words] and "JavaScript runtime" [2 words]; P3 applied: architecture details move into separate short sentences instead of stacking inside the noun phrase)*

>
> **Non-STE:** Refactor the authentication and authorization middleware layer to extract the JSON Web Token validation and user permission role resolution logic into separate composable utility functions.
>
> **STE:** Refactor auth middleware: extract JWT validation and role resolution into separate utilities.
>
> *(P9 applied: "authentication and authorization middleware layer" → "auth middleware" [2 words]; "JSON Web Token validation" → "JWT validation" [2 words]; "user permission role resolution logic" → "role resolution" [2 words — "user permission" is redundant in auth context]; "composable utility functions" → "utilities"; P11 applied: consistent abbreviations — "auth" and "JWT" are recognized forms used throughout)*

>
> **Non-STE:** The operation to establish a connection to the primary relational database management system server instance located at the network address 192.168.1.100 on the default Transmission Control Protocol port number 5432 has failed due to a network timeout condition after waiting for the configured connection timeout duration of 30 seconds.
>
> **STE:** Connection to the primary database at 192.168.1.100:5432 timed out after 30 seconds.
>
> *(P9 applied: "relational database management system server instance" → "database" [1 word]; "Transmission Control Protocol port number 5432" → ":5432" [port number alone suffices]; "failed due to a network timeout condition after waiting for the configured connection timeout duration of 30 seconds" → "timed out after 30 seconds"; P3 applied: the 55-word sentence becomes a 13-word sentence conveying identical actionable information)*

## Principles Applied

**P9** — Use short technical nouns: select the shortest term that is unambiguous in context. This is the primary principle for Rule 1.9. A technical noun must be short (not more than three words) and easy to understand. Long noun phrases built from stacked modifiers, embedded type information, synonym chains, or implementation details must be reduced to their essential identifying words. The precision lives in the context — code references, diagrams, preceding definitions, and API specs — not in the noun phrase itself. When the context identifies the item clearly, the shortest term is sufficient.

**P3** — Keep sentences short and separate ideas. Long noun phrases in code documentation often embed architecture details, safety guarantees, and configuration options that belong in separate sentences. When you shorten a noun phrase under Rule 1.9, move the removed details into their own short sentences — one idea per sentence. This follows the pattern demonstrated in the original ASD-STE100 specification: rather than describing every attribute of a screw in the noun phrase, state the screw's identity briefly and let the illustration carry the detail.

**P11** — Use one term per concept consistently. When you select a shortened form of a technical noun under Rule 1.9, use that same form everywhere in the document. Do not use "auth service" in one paragraph and "authentication module" in the next for the same component. The shortened form becomes the canonical term for that concept within the document scope, and consistency throughout the document is essential for readability and precision.

**P8** — Use standard, well-known technical nouns. The shortened form selected under Rule 1.9 must be a recognized term — a standard abbreviation like "JWT" or "API," an established short name like "Node.js," or a project-glossary-registered short form. Do not invent new abbreviations or short forms to satisfy the three-word limit. An abbreviation you invent today is a word nobody recognizes and fails the "easy to understand" criterion. The short form must already exist in the community's vocabulary.
