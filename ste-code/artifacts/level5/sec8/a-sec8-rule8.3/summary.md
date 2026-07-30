# Rule 8.3 — Use of Parentheses (Level 5 Summary)

## Original Rule Summary

Rule 8.3 governs the permitted uses of parentheses in STE technical writing. You can use parentheses to make references to illustrations or text, to include letters or numbers that identify items in a diagram or text, to identify work steps in a procedure, to include abbreviations, to give singular and plural forms of a noun at the same time, to explain words or part of a sentence, or to include an alternative. Parentheses must not be nested, and the main sentence punctuation is not affected by the parenthetical content. The original standard does not permit em dashes or en dashes — only parentheses and commas handle supplementary information.

## STE-Code Adaptation for Code Documentation

Rule 8.3 adapts naturally to code documentation by replacing illustration references with references to code modules, diagrams, or related documentation files. Abbreviations introduced on first use in parentheses help readers scan README files, API docs, and docstrings quickly. Parenthetical explanations clarify parameter constraints, return types, and valid value ranges without interrupting the main sentence flow or repeating information already present in type signatures. The alternative-use pattern supports configuration instructions (e.g., `debug (troubleshooting) or info (production)`), and the step-numbering pattern structures procedural documentation commands.

## Example Pairs

### Example 1: Abbreviation on First Use

> **Non-STE:** The application uses a DOM, or document object model, to represent the page structure, and an API, which stands for application programming interface, to fetch data from the server.
>
> **STE:** The application uses a Document Object Model (DOM) to represent the page structure and an Application Programming Interface (API) to fetch data from the server.

### Example 2: Explaining a Sentence Part

> **Non-STE:** Rate limit the endpoint to 100 requests per minute, which means you can send one request roughly every 600 milliseconds assuming uniform distribution.
>
> **STE:** Rate limit the endpoint to 100 requests per minute (approximately one request every 600 ms).

### Example 3: Singular/Plural Form

> **Non-STE:** Before you compile the project, confirm that all the dependency or dependencies have been installed in the correct version or versions specified by the lock file.
>
> **STE:** Before you compile the project, confirm that all dependency(ies) are installed in the correct version(s) specified by the lock file.

## Principles Applied

- **P1 — Use approved words:** All words in parenthetical content must come from the approved STE dictionary.
- **P2 — Use words only as their specified part of speech:** Parenthetical explanations must respect the approved part of speech for each word.
- **P3 — Use words with approved meanings:** When parentheses explain a term, the explanation must use the term in its approved meaning only.
- **P4 — Use approved adjective forms:** Abbreviation introductions and parameter descriptions must use approved adjective forms where applicable.
- **P6 — Technical nouns allowed:** Framework names, library names, and API identifiers may appear in parentheses as technical nouns.
- **P7 — Do not use technical nouns as verbs:** Parenthetical explanations must not convert a technical noun into a verb.
- **P8 — Use standard technical nouns:** When clarifying an ambiguous technical name in parentheses, use the standard community-accepted term.
- **P9 — Prefer short nouns:** Parenthetical content must be concise; long explanatory phrases belong in separate sentences.
- **P11 — One term per concept:** After defining an abbreviation in parentheses, use only that abbreviation consistently throughout the document.
- **P12 — Technical verbs allowed:** Command names and action verbs in parenthetical procedural steps are permitted as technical verbs.
