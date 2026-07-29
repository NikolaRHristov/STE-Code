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

The same word can go into different categories of code-domain technical nouns. This condition occurs when you use the word with different meanings in different contexts.

If a word is not in the controlled terminology, you can use it if it is part of a code-domain technical noun. A word that is part of an established code-domain technical noun must not be replaced with its approved alternative, because doing so would change the established name that your project, industry, or subject field uses.

### Examples

> **Non-STE:** The handler processes each incoming event.
> **STE:** The function processes each incoming event.

"Handler" is not approved in the controlled terminology, and its approved alternative is "function (n)." In the non-STE example, "handler" refers to a generic processing function — it is not a code-domain technical noun. The STE version correctly uses the approved word "function."

> **STE:** The event handler processes each incoming event.

"Event handler" is a code-domain technical noun (category 1, code components, modules, and libraries). You can use "handler" as part of this two-word code-domain technical noun, because "event handler" is the established term in the project, industry, or subject field. It is incorrect to replace "handler" with "function" here, because "event function" is not the term that is approved.

> **Non-STE:** The main branch of the repository has the latest code.
> **STE:** The primary branch of the repository has the latest code.

"Main" is not approved in the controlled terminology, and its alternative is "primary (adj)." In the non-STE example, "main" is used as a general adjective. The STE version correctly uses the approved word "primary."

> **STE:** Merge the feature branch into the main branch.

"Main branch" is a code-domain technical noun (category 5, infrastructure, deployment, and platforms). In Git-based workflows, "main branch" is the established term. It is incorrect to replace "main" with "primary" here, because "primary branch" is not the technical noun that is approved in your project, industry, or subject field.
