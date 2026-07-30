# Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

## Original Rule Summary

Rule 1.5 permits the use of technical nouns that are not in the approved STE dictionary when they belong to one of twenty-two recognized categories. A technical noun is a noun term that refers to a specified concept within a subject field — the dictionary does not list them because there are too many and each field uses its own set. Writers must be able to place every technical noun into at least one category, such as "Official parts information," "Tools and support equipment," "Systems and components," "Mathematical and scientific terms," or "Professional roles." The rule serves as the gateway for all domain-specific vocabulary: without it, aerospace documentation would become unusable because no set of approved words can name every aircraft part, tool, or procedure.

## STE-Code Adaptation

Rule 1.5 in STE-Code is the primary mechanism for introducing code-domain vocabulary into documentation. It defines nineteen categories — adapted from the original twenty-two — that cover all software development concepts: code components (category 1), data structures (category 4), infrastructure (category 5), algorithms (category 7), interface elements (category 8), quoted text such as error messages and code keywords (category 10), defects and errors (category 15), computer science concepts (category 16), database terms (category 18), network protocols (category 19), and more. A word may appear in STE-Code documentation only if it is an approved dictionary word (Rule 1.1) or a code-domain technical noun that fits into at least one of these nineteen categories (Rule 1.5) — there is no third category. Every technical noun a project uses must be registered in the project glossary with its category, its approved meaning, and an example sentence; without glossary registration, the noun violates Rule 1.6.

## Example Pairs

> **Non-STE:** The dev spun up the thing on the cloud and it barfed because the DB connector was busted.
>
> **STE:** The developer deployed the application to AWS. The deployment failed because the PostgreSQL connection pool had a timeout defect.
>
> *(P5 applied: "dev" → "developer" is a professional role in category 11; "cloud" → "AWS" is an infrastructure/platform in category 5; "DB connector" → "PostgreSQL connection pool" is a database term in category 18; "barfed" / "busted" replaced with "failed" and "timeout defect" — the defect is a category 15 technical noun; P10 applied: slang removed)*

>
> **Non-STE:** feat: added a bunch of stuff to make the auth faster and less crashy
>
> **STE:** feat: add a Redis cache layer to reduce authentication latency and prevent race conditions
>
> *(P5 applied: "stuff" replaced with precise technical nouns — "Redis" (category 18), "cache layer" (category 6), "authentication" (category 16), "latency" (category 7), "race conditions" (category 15); P10 applied: "a bunch of," "crashy" are informal; P11 applied: one term per concept — "race conditions" names a specific defect)*

>
> **Non-STE:** The endpoint expects the payload to have a user object with a nested array of things.
>
> **STE:** The `POST /users` endpoint expects a JSON body with a `user` object that contains an array of `permission` objects.
>
> *(P5 applied: "payload" → "JSON body" — JSON is a data format in category 4; "things" replaced with "`permission` objects" — `permission` is a code component in category 1 and quoted text in category 10; P11 applied: "things" is vague — the specific technical noun "permission" names the concept; P3 applied: "nested array" clarified as "array of `permission` objects")*

## Principles Applied

**P5** — Use code-domain technical nouns only in their approved categories. This is the primary principle for Rule 1.5. Every word that is not in the approved STE-Code dictionary must belong to at least one of the nineteen code-domain technical noun categories. A word that does not fit any category — such as informal jargon, made-up terms, or vague placeholder words ("stuff," "thing") — is not permitted.

**P1** — Use approved words from the controlled terminology. Rule 1.5 works as the complement to Rule 1.1: when a concept can be expressed with an approved word, use the approved word. Technical nouns fill the gap when no approved word names the concept precisely. The two rules together ensure that every word in the documentation is either approved or categorized.

**P10** — Do not use slang, jargon, or informal language. Words like "spun up," "barfed," "busted," "a bunch of," "crashy," and "stuff" have no place in code documentation. They cannot be placed in any technical noun category and are therefore forbidden by the combined effect of Rules 1.5 and 1.6. Replace them with precise technical nouns from the appropriate category.

**P11** — Use one term per concept (Rule 1.11). A code-domain technical noun must refer to exactly one concept in the project. Using the same noun for two different concepts, or using multiple nouns for the same concept, violates this principle. The project glossary enforces the one-to-one mapping between terms and concepts.
