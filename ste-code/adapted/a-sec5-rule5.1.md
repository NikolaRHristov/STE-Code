# Rule 5.1 — Short Sentences (Maximum 20 Words)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.1

## Original Rule

Write short sentences. Use a maximum of 20 words in each sentence.

Procedures give instructions that tell you how to do a task. Long sentences in work steps are not easy to understand.

In STE, the maximum length of a sentence for procedures is 20 words.

Warnings, cautions, and other safety instructions must also obey this rule.

Examples in STE:

> **STE:** Install the three auxiliary screws (2) in the flange of the motor assembly (9). (This sentence has 14 words.)

> **CAUTION:** WHEN YOU REMOVE THE SHROUD (26), BE CAREFUL NOT TO CAUSE DAMAGE TO THE SURFACE OF THE FLANGE ASSEMBLY (22). (This sentence has 20 words.)

> **Non-STE:** Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover. (25 words)
>
> **STE:** Put preservation oil into the unit through the vent hole. (10 words) Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover. (16 words)

Note: Section 8 gives all the rules about word count.

Notes (rule 5.5) do not obey rule 5.1. Notes are important in procedures, but they contain information only. Thus, the maximum length of a sentence in a note is 25 words.

> **See also:** Rule 5.5 — Notes Give Information Only, Not Instructions

## STE-Code Adaptation

In code documentation, procedures include installation instructions, setup steps, deployment checklists, debugging workflows, and API usage guides. Long sentences in these procedures make them difficult to follow, especially when the reader is executing commands or writing code while reading.

Keep every sentence in code documentation procedures to a maximum of 20 words. Break long procedural sentences into shorter sentences, each focusing on one part of the task. Warnings and caution statements about security, data loss, or system stability must also obey the 20-word limit.

Notes in code documentation procedures have a maximum sentence length of 25 words. Notes give supplementary information only and are not required for the reader to complete the procedure.

This rule applies to sentences in procedural documentation text. Code snippets, command examples, and terminal output that appear inside code blocks are not subject to the word count rule. String literals and identifier names inside code examples are also excluded from the word count.

### Examples

> **Non-STE:** Run the database migration script from the project root directory and then restart the application server to apply all pending schema changes to the production environment. (27 words)
>
> **STE:** Run the database migration script from the project root directory. (9 words) Then, restart the application server to apply all pending schema changes. (13 words)
>
> *Adapted from spec pair: "Put preservation oil into the unit through the vent hole until the oil level is approximately 6 mm (0.24 inches) below the surface of the flange cover." (25 words) / "Put preservation oil into the unit through the vent hole." (10 words) "Continue until the oil level is approximately 6 mm (0.24 in) below the surface of the flange cover." (16 words)*

> **Non-STE:** The initialization process will automatically create the required directory structure and populate it with default configuration files before the application starts. (22 words)
>
> **STE:** The initialization process automatically creates the required directory structure. (8 words) Then, it populates the directory with default configuration files. (10 words)
>
> *Additional code-domain example — no direct spec pair*

> **Non-STE:** Set the environment variable HTTP_TIMEOUT to the value 30000 which represents the maximum number of milliseconds that the client will wait for a response from the upstream server. (30 words)
>
> **STE:** Set the environment variable HTTP_TIMEOUT to 30000. (8 words) This value is the maximum wait time in milliseconds for a response from the upstream server. (17 words)
>
> *Additional code-domain example — no direct spec pair*

> **CAUTION:** IF YOU DELETE THE CONFIGURATION DIRECTORY WITHOUT A BACKUP, YOU CANNOT RESTORE THE APPLICATION SETTINGS TO THEIR PREVIOUS STATE. (18 words)
>
> *Adapted from spec example: "WHEN YOU REMOVE THE SHROUD (26), BE CAREFUL NOT TO CAUSE DAMAGE TO THE SURFACE OF THE FLANGE ASSEMBLY (22)." (20 words)*

> **Non-STE (note):** For more detailed information about the supported authentication methods and their respective configuration parameters in this release, please refer to the official authentication module documentation page. (27 words)
> **STE (note):** For more information about the supported authentication methods, refer to the authentication module documentation. (15 words)
>
> *Adapted from original rule — notes have a maximum sentence length of 25 words; no direct spec pair*
