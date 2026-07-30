# Rule 1.14 — Use American English Spelling Unless Other Official Directives Tell You Differently

## Original Rule Summary

Rule 1.14 requires American English spelling as the default in all technical documentation. The STE dictionary specifies American English spelling for every approved word. Use a different spelling only when other technical publication specifications, style guides, contracts, or official directives require it. When quoted text contains British English spelling — for example, text displayed on a computer screen — you must not change the spelling of the quoted text.

## STE-Code Adaptation

Rule 1.14 applies directly to all code documentation: use American English spelling in README files, API documentation, docstrings, inline comments, and all other documentation forms. Use a different spelling only when project specifications, style guides, contracts, or other official directives require it. British English spellings can cause confusion in technical contexts — for example, "meter" is a measuring device while "metre" is a unit of length. When quoted text contains British English spelling — for example, an error message, a terminal output, or a user interface string — you must not change the spelling of the quoted text. Refer to Rule 8.6 for correct handling of quoted text.

## Example Pairs

> **Non-STE:** The log file shows the colour of each output line.
>
> **STE:** The log file shows the color of each output line.
>
> *(P14 applied: "colour" → "color". The spec explicitly lists "color" as the American English spelling. "Colour" is British English and is not permitted in code documentation.)*

> **Non-STE:** Initialise the variable before you use it in the loop.
>
> **STE:** Initialize the variable before you use it in the loop.
>
> *(P14 applied: "initialise" → "initialize". The -ise suffix is British English; the -ize suffix is American English. The spec establishes American English as the default, and "initialize" follows this pattern.)*

> **Non-STE:** The terminal shows the message `Color profile not recognized`.
>
> **STE:** The terminal shows the message `Colour profile not recognised`.
>
> *(P14, P1 applied: the quoted terminal output must not be changed. The British spellings "Colour" and "recognised" are preserved because they appear in quoted text from the terminal. Changing them to American English would misrepresent the actual output and violate Rule 8.6 for quoted text.)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. The STE dictionary specifies the approved spelling for each word. When a British and American spelling both exist, only the American spelling is approved.

**P14** — Use American English spelling. This is the primary principle for Rule 1.14. All words in code documentation — in README files, API documentation, docstrings, inline comments, headings, bullet points, and link text — must use American English spelling. The -ise/-ize suffix pair ("initialise" → "initialize"), the -yse/-yze pair ("analyse" → "analyze"), and the -our/-or pair ("colour" → "color") are the most common violations. Quoted text that contains British English spelling must not be changed — Rule 8.6 governs the correct handling of quoted text.
