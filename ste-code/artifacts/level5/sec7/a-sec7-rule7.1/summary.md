# Rule 7.1 — Use an Applicable Word (WARNING or CAUTION) to Identify the Level of Risk

## Original Rule Summary

Rule 7.1 requires the use of a signal word (for example, "warning" or "caution") to immediately show the reader the level of risk. Use "warning" when there is a risk of injury or death. Use "caution" when there is a risk of damage to machines, tools, or equipment. When both levels of risk exist together, use "warning." An abstract caution must be escalated to a warning when the true risk involves injury or death.

## STE-Code Adaptation

Rule 7.1 in STE-Code requires the use of a signal word (WARNING or CAUTION) to immediately show the reader the level of risk in code documentation. Use WARNING when there is a risk of security vulnerabilities, data loss, or system corruption. Use CAUTION when there is a risk of unexpected behavior, performance degradation, or incorrect results. When both levels of risk exist together, use WARNING. The signal word must appear as the first word of the instruction in uppercase, followed by a colon and a space, followed by a clear command and a specific consequence.

## Example Pairs

> **Non-STE:** CAUTION: ALWAYS VALIDATE INPUT DATA.
>
> **STE:** WARNING: BEFORE YOU PROCESS INPUT DATA, MAKE SURE THAT YOU SANITIZE AND VALIDATE THE DATA. UNSANITIZED INPUT CAN CAUSE SECURITY BREACHES AND DATA LOSS.
>
> *(P1, P5, P7 applied — the original used CAUTION for a security risk; escalated to WARNING; specific consequence named: security breaches, data loss)*

> **Non-STE:** CAUTION: THE CONFIGURATION FILE MAY CONTAIN OUTDATED SETTINGS.
>
> **STE:** CAUTION: BEFORE YOU DEPLOY THE APPLICATION, COMPARE THE CONFIGURATION FILE AGAINST THE REFERENCE CONFIGURATION. OUTDATED SETTINGS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *(P1, P9, P11 applied — CAUTION is correct for unexpected behavior risk; abstract statement replaced with a concrete pre-action check and specific consequence)*

> **Non-STE:** The DEBUG_MODE environment variable controls verbose logging. Setting it to true in production will leak sensitive information.
>
> **STE:** WARNING: DO NOT SET `DEBUG_MODE=true` IN A PRODUCTION ENVIRONMENT. DEBUG MODE WRITES SENSITIVE DATA TO THE LOG OUTPUT. THIS DATA INCLUDES REQUEST BODIES, AUTHENTICATION TOKENS, AND DATABASE QUERIES. AN ATTACKER WITH LOG ACCESS CAN STEAL USER CREDENTIALS.
>
> *(P1, P5, P7 applied — the original has no signal word at all for a security risk; WARNING added; specific data-at-risk enumerated; attacker threat named)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. "WARNING" and "CAUTION" are the only approved signal words. Do not invent new signal words such as "DANGER," "CRITICAL," or "IMPORTANT." Translate third-party conventions to STE-Code signal words.

**P5** — Use code-domain technical nouns. Technical code nouns (`DEBUG_MODE`, `X-RateLimit-Remaining`, `users` table, `encrypt` function) are preserved in backticks within WARNING and CAUTION instructions. The signal word itself is not a technical noun — it is a procedural formatting convention.

**P7** — Do not use technical nouns as verbs. Inside a WARNING or CAUTION instruction, use approved verbs in the imperative mood. Technical verbs such as "sanitize," "validate," "encrypt," and "back up" are permitted as imperatives when they describe the required action.

**P9** — Prefer short, clear sentences. Each WARNING or CAUTION instruction must give a concrete command and a specific consequence. Do not write abstract statements such as "be careful" or "use with caution." Name the specific risk: "security breach," "data loss," "unexpected behavior," "incorrect results."

**P11** — One term per concept. Use WARNING and CAUTION consistently across all documentation types — README files, API documentation, docstrings, commit messages, error messages, and generated code wrappers. Do not mix signal word conventions from different sources.

**P14** — Use American English spelling. The signal words WARNING and CAUTION follow American English conventions. For internationalization, translate the signal words consistently using a maintained glossary.
