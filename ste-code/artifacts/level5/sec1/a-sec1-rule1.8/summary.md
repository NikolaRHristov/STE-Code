# Rule 1.8 — Use Technical Nouns That Are Approved in Your Company, Industry, or Subject Field

## Original Rule Summary

Rule 1.8 requires that you use the standard, approved technical noun for each concept in your documentation. This rule is not about whether a word is a technical noun (Rule 1.5 covers that) — it is about which technical noun to choose when more than one name exists for the same concept. If your company, industry, or subject field has an approved technical noun for a system, component, part, or process, you must use that exact term rather than inventing a substitute. The authority for approved technical nouns comes from official parts information, company documentation, and industry standards — not from the writer's preference.

## STE-Code Adaptation

Rule 1.8 in STE-Code requires that you use the approved code-domain technical noun for every class, module, function, method, component, variable, or process you reference in documentation. The approved name is the one that appears in the project glossary, API documentation, coding standards, or the source code itself — never a descriptive phrase or an invented variant that seems clearer. When an industry-standard term exists (such as "observer pattern," "JWT," or "REST"), use that exact term rather than a homegrown description. Consistency with the approved terminology ensures that every reader can map documentation references to the actual codebase elements and industry concepts.

## Example Pairs

> **Non-STE:** The data display widget shows user information in a table format.
>
> **STE:** The `UserTable` component shows user information.
>
> *(P8 applied: use standard, well-known technical nouns. P11 applied: one term per concept. "UserTable" is the approved code-domain technical noun from the codebase — readers can find it in the source code. "Data display widget" is an invented description that no reader can map to any code element.)*

> **Non-STE:** The user retrieval endpoint sends back a user data object.
>
> **STE:** The `GET /users/:id` endpoint returns a `User` object.
>
> *(P8 applied: `GET /users/:id` and `User` are the approved technical nouns from the API spec and type system. P11 applied: one term per concept. P5 applied: code-domain technical nouns are allowed. "User retrieval endpoint" and "user data object" are invented phrases — readers who search for "user retrieval" will not find the endpoint.)*

> **Non-STE:** Refactor the auth helper to use the new token validator.
>
> **STE:** Refactor `AuthService` to use `JwtValidator`.
>
> *(P8 applied: `AuthService` and `JwtValidator` are the approved file and class names from the project. P11 applied: one term per concept. P5 applied: code-domain technical nouns are allowed. "Auth helper" and "token validator" are imprecise descriptions — a developer reading the commit log must be able to map the message to the actual code change.)*

## Principles Applied

**P8** — Use standard, well-known technical nouns. This is the primary principle for Rule 1.8. When a concept has an approved name in the project glossary, API documentation, coding standards, or the source code itself, use that exact name. Do not substitute a descriptive phrase, a synonym, or an invented variant — even if your version seems clearer. The standard name is the one readers will search for and recognize.

**P11** — One term per concept (Rule 1.11). Each concept in code documentation must have exactly one approved name across all documentation types — README files, API docs, docstrings, commit messages, and error messages. Using "UserTable" in one file and "data display widget" in another for the same component violates this principle and breaks traceability.

**P1** — Use approved words from the controlled terminology. While Rule 1.8 governs which technical noun to use, the surrounding words must still come from the approved STE-Code dictionary. The framework around the approved technical noun (verbs, prepositions, adjectives) must follow Rule 1.1 through Rule 1.4.

**P5** — Use code-domain technical nouns only in their approved categories. Rule 1.8 works together with Rule 1.5: once a code-domain technical noun is recognized under Rule 1.5 (fits a category), Rule 1.8 ensures the writer uses the exact approved form of that noun as registered in the project glossary.
