# Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition

## Original Rule Summary

Rule 7.2 governs the opening structure of safety instructions in Simplified Technical English. Every safety instruction must begin with either a clear command (an imperative verb such as "DO NOT," "ALWAYS," or "MAKE SURE") or a clear condition (a subordinate clause such as "IF...," "BEFORE YOU...," or "WHEN..."). The reader must understand what action to take or what prerequisite condition exists within the first few words of the instruction body. The command or condition appears immediately after the signal word (WARNING or CAUTION) and colon, without background information or explanatory text before it.

## STE-Code Adaptation

Rule 7.2 in STE-Code applies the same command-first and condition-first structures to safety instructions in code documentation. Every WARNING or CAUTION in docstrings, README files, API references, and configuration files must start with either a command ("DO NOT STORE," "ALWAYS SANITIZE," "CHECK") or a condition ("IF YOU CALL...," "BEFORE YOU DEPLOY...," "WHEN THE CONNECTION FAILS..."). The reader must know the prohibition, requirement, or prerequisite context within the first few words. Explanatory text and background information follow the command or condition, never precede it.

## Example Pairs

> **Non-STE:** WARNING: It is important to consider that hardcoding database credentials in the configuration file can lead to serious security issues if the file is committed to version control.
>
> **STE:** WARNING: DO NOT HARDCODE DATABASE CREDENTIALS IN THE CONFIGURATION FILE. STORE CREDENTIALS IN A SECRETS MANAGER OR ENVIRONMENT VARIABLES. HARDCODED CREDENTIALS IN VERSION CONTROL CAN CAUSE UNAUTHORIZED DATABASE ACCESS.
>
> *(P1, P9 applied — the command "DO NOT HARDCODE" starts the instruction; the reader knows the prohibition in the first three words)*

> **Non-STE:** CAUTION: The `/search` endpoint returns results from a cache that is updated every 5 minutes, so recent changes may not be reflected immediately.
>
> **STE:** CAUTION: BEFORE YOU USE THE `/search` ENDPOINT, READ THE CACHE STALENESS NOTE. THE CACHE IS UPDATED EVERY 5 MINUTES. RECENT CHANGES ARE NOT VISIBLE UNTIL THE NEXT CACHE UPDATE. DO NOT USE THIS ENDPOINT FOR REAL-TIME DATA.
>
> *(P1, P2 applied — the condition "BEFORE YOU USE" starts the instruction; the reader knows the prerequisite before the explanation)*

> **Non-STE:** WARNING: The database connection may not be initialized if you call this function before `connect()` has completed.
>
> **STE:** WARNING: IF YOU CALL THIS FUNCTION BEFORE `connect()` COMPLETES, THE DATABASE CONNECTION IS NOT INITIALIZED. THE FUNCTION RETURNS `null` AND THE APPLICATION CAN FAIL WITHOUT AN ERROR MESSAGE.
>
> *(P1, P9 applied — the condition "IF YOU CALL" starts the instruction; the consequence follows the condition)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. "Consider" is not approved for safety instructions when a direct command is needed. "Hardcode" → "store" (negative command form). "Reflected" → "visible." "May not be initialized" → "is not initialized."

**P2** — Use simple verb tenses. "Is updated" instead of "gets updated." "Completes" instead of "has completed." The simple present conveys the condition clearly without tense complexity.

**P9** — Prefer short, clear technical nouns and commands. The command or condition must appear in the first few words: "DO NOT HARDCODE" (three words), "BEFORE YOU USE" (three words), "IF YOU CALL" (three words). The reader identifies the required action or context immediately.
