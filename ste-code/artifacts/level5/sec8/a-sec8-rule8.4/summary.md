# Rule 8.4 — Colon in a Vertical List (Level 5 Summary)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.4

---

## 1. Rule Title and Number

**Rule 8.4** — Colon in a Vertical List

---

## 2. Original Rule Summary

In a vertical list, a colon (:) has the same effect on word count as a period and marks the end of a sentence. The text before the colon must obey the sentence-length limits: a maximum of 20 words for procedural sentences and 25 words for descriptive sentences. Each item in the vertical list after the colon counts as a new sentence, with its own 20-word (procedural) or 25-word (descriptive) limit. The colon is a clean boundary between the introductory "setup" and the list "payload" — the introduction should state only what category the list contains, and each list item must deliver one complete, self-contained thought.

---

## 3. STE-Code Adaptation for Code Documentation

In code documentation, the colon-in-list rule applies to README prerequisites, API endpoint lists, configuration option tables, error-handler catalogues, and any procedural step list. A common violation in code docs is a long, clause-heavy introduction that embeds version numbers, compatibility caveats, and justification before the colon — forcing the reader to parse 30-plus words before reaching the list items. The fix is to move qualifiers into the list items themselves or into a separate sentence before the colon-bearing introduction. List items must be grammatically parallel (all noun phrases, all imperative clauses, or all full sentences) and each item must stand as an independent, simple sentence after the colon.

---

## 4. Example Pairs

> **Non-STE:** To handle all possible error conditions, the following exception types must be caught and processed by the error handler: database connection timeouts which occur when the primary node is unreachable, authentication failures caused by expired or invalid tokens, and validation errors due to malformed request payloads.
>
> **STE:** To handle possible error conditions, the error handler catches these exception types:
>
> - Database connection timeout
> - Authentication failure
> - Validation error.

> **Non-STE:** The configuration file, which is located in the project root, supports these environment profiles that you can use for deployment: a development profile for local testing and debugging, a staging profile for pre-production integration verification, and a production profile for the live customer-facing environment.
>
> **STE:** The configuration file supports these environment profiles:
>
> - Development
> - Staging
> - Production.

> **Non-STE:** The API exposes the following endpoints for user management which include creating new accounts, updating profile information, deleting accounts that are no longer active, and listing all users with optional filtering by role: POST /users, PATCH /users/:id, DELETE /users/:id, and GET /users.
>
> **STE:** The API exposes these endpoints for user management:
>
> - POST /users — creates a new account
> - PATCH /users/:id — updates profile information
> - DELETE /users/:id — removes an account
> - GET /users — lists all users.

---

## 5. Principles Applied

- **P1 — Use approved words:** All words in the introductory text before the colon and in each list item must come from the approved STE dictionary.

- **P2 — Use words only as their specified part of speech:** List items that are noun phrases must use nouns; list items that are imperative clauses must use verbs in their approved imperative form.

- **P3 — Use words with approved meanings:** The introductory sentence must state only the category of the list using words in their approved meanings — do not embed definitions, justifications, or caveats before the colon.

- **P4 — Use approved adjective forms:** When a list item includes a compound adjective (e.g., "database connection timeout"), use the approved adjective form only.

- **P6 — Technical nouns allowed:** Code-domain technical nouns (endpoint paths, class names, exception types) may appear in list items as approved technical nouns.

- **P7 — Do not use technical nouns as verbs:** Ensure that list items do not convert a technical noun into a verb.

- **P8 — Use standard technical nouns:** Use community-accepted names for exception types, endpoints, and configuration profiles in list items.

- **P9 — Prefer short nouns:** Each list item must be a short, scannable unit. A long descriptive phrase belongs in a separate sentence before the list, not crammed into a single list item.

- **P11 — One term per concept:** If a list introduces abbreviated terms, define each abbreviation in parentheses on first occurrence and use only that abbreviation throughout subsequent documentation.

- **P12 — Technical verbs allowed:** Command names, HTTP method names, and CLI verbs in list items are permitted as technical verbs.

---

*Generated from STE-Code adapted rule file: a-sec8-rule8.4.md*
