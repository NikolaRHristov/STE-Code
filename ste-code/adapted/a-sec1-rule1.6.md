# Rule 1.6 — Use a Word That Is Not Approved in the Dictionary, Only When It Is a Technical Noun or Part of a Technical Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.6

## Original Rule

**Rule 1.6** Use a word that is not approved in the dictionary, only when it is a technical noun or part of a technical noun.

The dictionary includes some words that you cannot use because they are not approved. But if you can put these words in an applicable category of technical nouns, you can use them as technical nouns in some contexts.

Examples:

The word "base" is not approved in the dictionary and its alternative is "bottom (n)."

> **Non-STE:** Make sure that the two spigots at the base of the unit engage.

("Base" is not permitted when it is related to a surface.)

> **STE:** Make sure that the two spigots at the bottom of the unit engage.

But you can use "base" as a technical noun.

("Base" is a technical noun, category 7, mathematical, scientific, engineering terms, and formulas.)

The same word "base" can go into different categories of technical nouns. This condition occurs when you use the word "base" with different meanings in different contexts.

("Base" is a technical noun, category 5, facilities, infrastructure, and logistic procedures.)

"Backup" is not approved in the dictionary and its alternatives are "emergency (n)" and "auxiliary (adj)." But you can use "backup" as a technical noun.

("Backup" is a technical noun, category 19, computer science, information and communication technology.)

"Backup" is a one-word technical noun. But you can also write "backup file," a two-word technical noun.

("Backup file" is a technical noun, category 19, computer science, information and communication technology.)

"Main" is a word that is not approved, and its alternative is "primary (adj)."

("Main part" is not a technical noun, and it is correct to replace "main" with "primary.")

But you can use "main" as part of a technical noun.

("Main landing gear" is a technical noun. It is incorrect to replace "main" with "primary" here, because "primary landing gear" is not the technical noun that is approved in your company, industry, or subject field.)

If a word is not in the dictionary, you can use it if it is part of a technical noun. In the example that follows, "angular" and "position" are approved but "relative" is not in the dictionary.

(You can use "relative" as part of a technical noun, category 7, mathematical, scientific, engineering terms, and formulas.)

## STE-Code Adaptation

**Rule 1.6** Use a word that is not approved in the controlled terminology, only when it is a code-domain technical noun or part of a code-domain technical noun.

The controlled terminology includes some words that you cannot use because they are not approved. But if you can put these words in an applicable category of code-domain technical nouns, you can use them as code-domain technical nouns in some contexts.

"Handler" is not approved in the controlled terminology and its alternative is "function (n)." This adapts the spec example where "base" is not approved and its alternative is "bottom." Just as you must use "bottom" instead of "base" when referring to a surface, you must use "function" instead of "handler" when referring to a general processing function.

> **Non-STE:** The handler processes each incoming event.
> **STE:** The function processes each incoming event.

> *Adapted from spec pair: "Make sure that the two spigots at the base of the unit engage" / "Make sure that the two spigots at the bottom of the unit engage."* Just as "base" (unapproved) must be replaced with "bottom" (approved) when referring to a surface, "handler" (unapproved) must be replaced with "function" (approved) when referring to a general processing function.

But you can use "handler" as part of a code-domain technical noun. This is the same principle as the spec example where "base" can be used as a technical noun in certain categories.

> **STE:** The event handler processes each incoming event.

> *Adapted from spec pair: "base" can be used as a technical noun in categories 7 and 5.* Just as "base" transitions from unapproved word to technical noun when part of a recognized compound term, "handler" transitions from unapproved word to code-domain technical noun when part of "event handler."

("Event handler" is a code-domain technical noun, category 1, code components, modules, and libraries.)

"Main" is not approved in the controlled terminology and its alternative is "primary (adj)." This adapts the spec example directly: "main" is the same word with the same alternative in both STE and STE-Code.

> **Non-STE:** The main branch of the repository has the latest code.
> **STE:** The primary branch of the repository has the latest code.

> *Adapted from spec pair: "main" is not approved and its alternative is "primary (adj)."* The same word "main" with the same alternative "primary" appears in both STE and STE-Code. When "main" is used as a general adjective, it must be replaced with "primary."

But you can use "main" as part of a code-domain technical noun. This adapts the spec example where "main landing gear" is a technical noun.

> **STE:** Merge the feature branch into the main branch.

> *Adapted from spec pair: "Main landing gear" is a technical noun and it is incorrect to replace "main" with "primary."* Just as "primary landing gear" is not the approved technical name, "primary branch" is not the approved code-domain technical noun. The official term "main branch" must be used.

("Main branch" is a code-domain technical noun, category 5, infrastructure, deployment, and platforms. It is incorrect to replace "main" with "primary" here, because "primary branch" is not the technical noun that is approved in your project, industry, or subject field. This is the same principle as the spec example: "primary landing gear" is not the approved technical noun.)

### Examples

> **Non-STE:** Make sure that the two connectors at the base of the chassis engage.
> **STE:** Make sure that the two connectors at the bottom of the chassis engage.

This adapts the spec pair directly: "base" → "bottom" when referring to a physical surface. Just as in the aerospace example, "base" is not permitted when it refers to a surface location. The STE version uses the approved alternative "bottom."

> **Non-STE:** The auxiliary function handles the error recovery.
> **STE:** The auxiliary function processes the error recovery.

This adapts the spec example where "backup" is not approved and its alternatives include "auxiliary (adj)." In the spec, "backup" can be a technical noun in computer science (category 19). In STE-Code, "handler" is not approved as a general verb, but "handler" as part of a code-domain technical noun is permitted, just as "backup" is permitted as a technical noun.
