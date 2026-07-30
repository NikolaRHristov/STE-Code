# Rule 4.4 — Use Connecting Words and Connecting Phrases to Connect Sentences That Contain Related Topics

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.4

## Original Rule

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows.

In a descriptive text, connecting words and connecting phrases give your writing a logical structure and give information that is easy to understand.

Some of the connecting words that are approved in the dictionary are "and," "but," "then," and "thus."

"As a result" and "at the same time" are examples of connecting phrases that you can use.

You can also use demonstrative adjectives as connecting words to connect ideas in related sentences.

In procedures, you can use these connecting words when an explanation is necessary after a work step. Connecting words can also be necessary in safety instructions to connect related sentences or make the text clear.

## STE-Code Adaptation

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows. In code documentation, they give your writing a logical structure and make technical information easy to understand.

Use approved connecting words such as "and," "but," "then," and "thus."

Use connecting phrases such as "as a result" and "at the same time."

You can also use demonstrative adjectives (this, these) as connecting words to connect ideas in related sentences. They refer back to a topic introduced in the previous sentence.

In procedural documentation (function and method descriptions), use connecting words when an explanation is necessary after a work step. In warning and caution statements, use connecting words to connect related sentences and make the text clear.

### Examples

**Using "and" to connect two related descriptions:**

> **STE:** The `parseInput` function validates the request payload. **And** the `formatOutput` function serializes the response data.
>
> *Adapted from original rule principle — approved connecting word "and"; no direct spec pair*

**Using "but" to show an exception or alternative:**

> **STE:** These error-handling rules are the minimum necessary for the API layer. **But** the local project conventions can give other necessary error-handling rules.
>
> *Adapted from original rule principle — approved connecting word "but"; no direct spec pair*

**Using "thus" to show a logical consequence:**

> **STE:** If the validation step fails, the middleware sets an error code on the response object. **Thus**, the downstream handler receives the error code and skips the processing step.
>
> *Adapted from original rule principle — approved connecting word "thus"; no direct spec pair*

**Using "as a result" to show cause and effect:**

> **STE:** When the cache eviction policy runs, expired entries are removed from the cache. **As a result**, the cache has free capacity for new entries.
>
> *Adapted from original rule principle — connecting phrase "as a result"; no direct spec pair*

**Using demonstrative adjectives as connecting words in procedures:**

> **STE:** Tag the deprecated methods with the `@deprecated` annotation. **This** annotation will help developers during the migration to the new API.
>
> *Adapted from original rule principle — demonstrative adjectives as connecting words; no direct spec pair*

**Using demonstrative adjectives in safety instructions:**

> **STE:**
>
> **WARNING:** ALWAYS VALIDATE USER INPUT IN THIS MODULE. **THIS** PRECAUTION WILL PREVENT INJECTION ATTACKS.
>
> *Adapted from original rule principle — connecting words in safety instructions; no direct spec pair*
