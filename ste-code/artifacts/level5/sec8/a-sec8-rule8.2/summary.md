## Rule 8.2 — Use Hyphens (-) to Connect Words That Are Directly Related

**Rule 8.2** Use hyphens (-) to connect words that are directly related. A hyphen is a punctuation mark that connects words or parts of words. Use the hyphen for technical nouns to show that two or more words are directly related. This construction helps the reader to understand words and phrases more easily.

**Rule 8.2** In code documentation, use hyphens (-) to connect words that are directly related. A hyphen is a punctuation mark that connects words or parts of words. Use the hyphen for code-domain technical nouns to show that two or more words are directly related. This construction helps the reader to understand words and phrases more easily in code comments, API documentation, and README files.

---

> **Non-STE:** The high priority task must acquire the write lock before it can modify the shared data structure.
>
> **STE:** The high-priority task must get the write lock before it can change the shared data structure.
>
> *Principles applied: P1, P2, P3. "High-priority" is a compound adjective before the noun "task." Added hyphen to show direct relationship. Replaced "acquire" with "get" and "modify" with "change" per STE vocabulary.*

> **Non-STE:** Use a read only file descriptor to open the configuration for parsing.
>
> **STE:** Use a read-only file descriptor to open the configuration for parsing.
>
> *Principles applied: P1, P2. "Read-only" is a compound adjective before the noun "file descriptor." Hyphen connects the words to prevent ambiguity about what "only" modifies.*

> **Non-STE:** The end to end test covers the entire data flow from server side rendering to client side hydration.
>
> **STE:** The end-to-end test covers the entire data flow from server-side rendering to client-side hydration.
>
> *Principles applied: P1, P2, P11. "End-to-end" is a three-word compound adjective before "test." "Server-side" and "client-side" are two-word compound adjectives before "rendering" and "hydration." Consistent hyphenation across all three compounds makes the sentence parse correctly on first reading.*

Key principles: P1, P2, P3, P11
