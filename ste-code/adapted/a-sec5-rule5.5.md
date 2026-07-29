# Rule 5.5 — Notes Give Information Only, Not Instructions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.5

## Original Rule

Write notes only to give information, not instructions.

Notes only give information to help the reader during a procedure. They contain descriptive text and obey the rules for descriptive writing.

Notes must not give instructions, requirements, or limits.

Examples in STE:

| NOTE: | The gyroscope will become stable after approximately 15 seconds. |
| --- | --- |

A note can have one or more sentences. Each sentence in a note can have a maximum of 25 words.

Examples in STE:

the CROSS FEED port is more than 5 cc/minute.

(One sentence, 22 words.)

results.

(Two sentences, 6 words and 8 words.)

Do not use the imperative form in a note. If you use the imperative form, the note becomes an instruction for a work step.

Example:

correctly.

(This text is not a note because it contains the imperative form.)

> **STE:** (6) Make sure that the avionics ventilation system continues to operate correctly.

(This is work step number 6 in the applicable procedure.)

If you include instructions in a note, it is possible that the reader will not see the information. If the information given in a note is important to prevent damage or injury, you must give such information in a safety instruction.

Examples:

| Non-STE: | NOTE: When you connect the lines, do not bend them too much. If you bend the lines too much, you can cause damage to them. (This text is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | CAUTION: WHEN YOU CONNECT THE LINES, DO NOT BEND THEM TOO MUCH. IF YOU BEND THE LINES TOO MUCH, YOU CAN CAUSE DAMAGE TO THEM. |

airflow to the compartment and therefore there is a risk of suffocation.

(Although the non-STE text does not contain the imperative form, it is not a note. It is a safety instruction.)

> **STE:** WARNING: BEFORE YOU CLOSE THE HATCH, MAKE SURE THAT NO PERSONS ARE IN THE CREW REST COMPARTMENT. WHEN THE HATCH IS CLOSED, THERE IS NO AIRFLOW TO THE COMPARTMENT AND THERE IS A RISK OF SUFFOCATION.

Do not use a note to give limits, tolerances, or results of a work step. This information must come directly after the related action in the work step.

## How to use notes correctly

When you write a procedure, and this procedure contains notes, do this test:

- Carefully read the procedure without the notes.
- Make sure that the reader can do the procedure correctly without the notes.

A satisfactory result of this test tells you that you used the notes correctly.

If important information is missing from the procedure and this information is in a note:

- Remove the information from the note.
- Write the missing information in a work step.
- Include this new work step where applicable in the procedure.
- Do the test again until you are fully sure that the reader can do the procedure without the notes.

In STE, you use notes in procedures. You can write notes in descriptions only if the notes are necessary for illustrations or tables that are parts of such descriptions.

## STE-Code Adaptation

In code documentation, notes provide supplementary information that helps the reader understand context, behavior, or background details about a procedure. Notes must contain descriptive information only. Notes must not contain instructions for the reader to execute, commands to run, or step-by-step actions.

Notes must not give requirements, limits, tolerances, or expected results of a work step. This information belongs directly in the work step itself, after the related action, so the reader sees it while executing the step. Notes must not contain imperative verbs. If you need to give an instruction, write it as a numbered work step.

If a note contains information that is critical for preventing data loss, security issues, or system damage, move that information into a WARNING or CAUTION safety instruction. A note is never a substitute for a safety instruction.

Each sentence in a note can have a maximum of 25 words. A note can contain one or more sentences.

To verify correct note usage, read the procedure without the notes. If the reader cannot complete the procedure correctly, move the missing information from the notes into work steps and repeat the test.

### Examples

> **STE:** NOTE: The API rate limiter allows a maximum of 1000 requests per minute per client IP address on the free tier.

(One sentence, 20 words. This note gives context about the API behavior without instructing the reader to do anything.)

> **STE:** NOTE: The configuration cache refreshes automatically every 60 seconds. Manual changes to the configuration file will not take effect until the next cache refresh cycle.

(Two sentences, 8 words and 19 words. Descriptive information only, no instructions.)

> **Non-STE:** NOTE: When you update the dependencies, run the command `npm audit fix` to resolve known vulnerabilities. If you skip this step, your application may have security issues.
> **STE:** (5) Run the command `npm audit fix` to resolve known vulnerabilities.

(Do not put instructions in a note. The instruction to run a command is a work step.)

> **Non-STE:** NOTE: The response time must be less than 200 milliseconds under normal load conditions. If the response time is higher, investigate the database query performance.
> **STE:** The response time must be less than 200 milliseconds under normal load conditions.

(Do not put limits or requirements in a note. The limit belongs directly in the work step.)

| Non-STE: | NOTE: Before you deploy to production, make sure that all environment variables are set correctly. If you deploy with missing variables, the application will not start and the deployment will fail. (This text is not a note. It is a safety instruction.) |
| --- | --- |
| STE: | CAUTION: BEFORE YOU DEPLOY TO PRODUCTION, MAKE SURE THAT ALL ENVIRONMENT VARIABLES ARE SET CORRECTLY. IF YOU DEPLOY WITH MISSING VARIABLES, THE APPLICATION WILL NOT START. |

> **Non-STE:** NOTE: Do not run the migration script on the production database without first creating a full backup. Running the migration without a backup can cause irreversible data loss.
> **STE:** WARNING: DO NOT RUN THE MIGRATION SCRIPT ON THE PRODUCTION DATABASE WITHOUT A FULL BACKUP. RUNNING THE MIGRATION WITHOUT A BACKUP CAN CAUSE IRREVERSIBLE DATA LOSS.

(Critical safety information belongs in a WARNING, not a note.)
