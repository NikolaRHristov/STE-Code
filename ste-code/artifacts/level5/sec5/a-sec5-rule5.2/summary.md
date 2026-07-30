# Rule 5.2 — One Instruction Per Sentence

## Original Rule Summary

Rule 5.2 requires that each sentence contain only one instruction, unless two or more actions occur at the same time. When a sentence has too many instructions, the reader cannot easily follow or execute the steps. Write each instruction in its own sentence and clearly show the sequence of work steps, usually with numbers or letters. There is no limit on the number of work steps in a procedure.

## STE-Code Adaptation

Rule 5.2 in STE-Code requires one instruction per sentence in all procedural code documentation. When a sentence contains multiple instructions, the reader can miss or skip an action, which leads to errors in configuration, deployment, or debugging. Use numbered or bulleted lists to show the sequence of steps clearly, and write only one instruction per list item. You may write two instructions in one sentence with the conjunction "and" only when both actions occur at the same time and cannot be separated into distinct work steps. You may write more than one sentence in a single work step when a result or measurement occurs immediately after an action and separating them would break the logical flow.

## Example Pairs

> **Non-STE:** Open the configuration file in a text editor and locate the database section and change the connection string to point to the staging server and then save the file and close the editor.
>
> **STE:**
> 1. Open the configuration file in a text editor.
> 2. Locate the database section.
> 3. Change the connection string to point to the staging server.
> 4. Save the file.
> 5. Close the editor.

> **Non-STE:** Run the test suite with the coverage flag enabled and verify that the total line coverage is above 80 percent across all modules in the project.
>
> **STE:** Run the test suite with the coverage flag enabled. The total line coverage must be more than 80 percent across all project modules.

> **Non-STE:** Make sure the environment variable DATABASE_URL is set correctly and then execute the initialization script to create the required database tables and populate them with the seed data.
>
> **STE:** Make sure that the environment variable DATABASE_URL is set correctly. Then, execute the initialization script. The script creates the required database tables and populates them with the seed data.

## Principles Applied

**P5** — Write one instruction per procedural step. Each work step describes exactly one action and starts with an imperative verb. A sentence that contains multiple instructions must be split into separate numbered steps or separate sentences.

**P7** — Use the imperative mood for all procedural writing. Each instruction must start with the base form of the verb (open, locate, change, save, run, set, make sure). Do not use "you should," "you must," or "the user should."

**P4** — Write one topic per descriptive sentence. When a result or measurement follows an action, describe the action in one sentence and the result limit in a separate sentence. This keeps each sentence focused on a single topic.

**P13** — Do not use semicolons or conjunctions to join independent clauses that contain instructions. Split multi-instruction sentences into separate steps. Use "and" only for two actions that occur at the same time and cannot be separated.

**P8** — Use the approved active voice. "Change the connection string" and "execute the initialization script" are active instructions that tell the reader what to do.

**P1** — Use approved words from the controlled terminology. Short, single-instruction sentences are easier to write and read when every word is approved and unambiguous.
