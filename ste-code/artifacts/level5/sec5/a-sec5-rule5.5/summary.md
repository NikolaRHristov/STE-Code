# Rule 5.5 — Notes Give Information Only, Not Instructions

## Original Rule Summary

Rule 5.5 requires that notes give information only, not instructions, requirements, or limits. Notes contain descriptive text that helps the reader during a procedure and follow the rules for descriptive writing. A note must not use the imperative form; if it does, it becomes a work step. Information that is important to prevent damage or injury belongs in a safety instruction, not in a note. Each sentence in a note can have a maximum of 25 words.

## STE-Code Adaptation

In code documentation, notes provide supplementary descriptive information that helps the reader understand context, behavior, or background details. Notes must not contain instructions for the reader to execute, commands to run, or step-by-step actions. Notes must not give requirements, limits, tolerances, or expected results of a work step — this information belongs directly in the work step body. If a note contains information critical for preventing data loss, security issues, or system damage, move it into a WARNING or CAUTION safety instruction. To verify correct note usage, read the procedure without the notes; if the reader cannot complete the procedure correctly, move the missing information from notes into work steps.

## Example Pairs

> **Non-STE:** NOTE: When you update the dependencies, run the command `npm audit fix` to resolve known vulnerabilities. If you skip this step, your application may have security issues.
>
> **STE:** (5) Run the command `npm audit fix` to resolve known vulnerabilities.

> **Non-STE:** NOTE: Before you deploy to production, make sure that all environment variables are set correctly. If you deploy with missing variables, the application will not start and the deployment will fail.
>
> **STE:** CAUTION: BEFORE YOU DEPLOY TO PRODUCTION, MAKE SURE THAT ALL ENVIRONMENT VARIABLES ARE SET CORRECTLY. IF YOU DEPLOY WITH MISSING VARIABLES, THE APPLICATION WILL NOT START.

> **Non-STE:** NOTE: The response time must be less than 200 milliseconds under normal load conditions. If the response time is higher than 200 milliseconds, investigate the database query performance.
>
> **STE:** The response time must be less than 200 milliseconds under normal load conditions.

## Principles Applied

**P1** — Use approved words from the controlled terminology. Notes follow the same vocabulary constraints as all other descriptive writing in STE-Code.

**P4** — Write one topic per descriptive sentence. Notes contain descriptive statements only. Each sentence in a note must describe one fact about the system, the code, or the environment.

**P5** — Write one instruction per procedural step. If a note contains instructions, extract them into separate numbered work steps. Each instruction becomes its own step with a clear action.

**P7** — Use the imperative mood for all procedural writing. Notes must use descriptive mood only, never imperative mood. If a sentence in a note uses imperative form, it is not a note — it is a work step or a safety instruction.
