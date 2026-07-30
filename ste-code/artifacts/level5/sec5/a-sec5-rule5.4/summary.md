# Rule 5.4 — Descriptive Statement Before the Command

## Original Rule Summary

Rule 5.4 requires that when a condition exists that the reader must know before acting, the writer places a descriptive statement before the command and separates the two with a comma. The condition comes first so the reader evaluates it before executing the instruction. The comma is the syntactic boundary that shows where the condition ends and the command begins. The position of the comma is critical because it determines which part of the sentence an adverb or adverbial phrase modifies, and an incorrectly placed comma can change the meaning of the entire sentence.

## STE-Code Adaptation

Rule 5.4 in STE-Code applies the condition-before-command structure to all procedural code documentation. When an instruction depends on a prerequisite — such as verifying that a service is running, confirming that a file exists, or checking that a previous step completed successfully — the condition must appear as a descriptive statement at the start of the sentence, followed by a comma, then the instruction in the imperative form. This structure ensures the reader evaluates the condition before executing the command, which prevents errors caused by acting on incomplete or invalid state. Do not bury the condition in a dependent clause after the instruction, and do not combine multiple unrelated conditions into a single sentence.

## Example Pairs

> **Non-STE:** Run the database migration script after you set the `DATABASE_URL` environment variable to your production database connection string and confirmed that the database server is accepting connections.
>
> **STE:** After you set the `DATABASE_URL` environment variable, run the database migration script.

> **Non-STE:** First you need to have Node.js version 18 or higher installed then run `npm install` and after all dependencies finish downloading if there are no errors you can run `npm run build` to compile the TypeScript source files.
>
> **STE:** Make sure that Node.js version 18 or higher is installed. Run `npm install`. After the dependencies install without errors, run `npm run build`.

> **Non-STE:** You can call the `/users` endpoint to retrieve a list of users but only after you have obtained a valid OAuth2 access token from the `/auth/token` endpoint and included it in the Authorization header of your request.
>
> **STE:** After you get a valid OAuth2 access token from the `/auth/token` endpoint, call the `/users` endpoint. Include the token in the `Authorization` header.

## Principles Applied

**P13** — Use clear, direct, unambiguous language. The condition-before-command structure removes ambiguity about execution order. When the condition appears after the command, the reader may start the action without processing the prerequisite. Placing the condition first with a comma forces the reader to evaluate the condition before they read the instruction. The comma is the syntactic marker that signals the boundary between prerequisite and action.

**P4** — Write one topic per descriptive sentence. A condition clause describes one prerequisite, and the command that follows describes one action. Do not combine several conditions in one sentence with multiple conjunctions. When a procedure has multiple prerequisites, write each condition-command pair as a separate step or separate sentence. This keeps each sentence focused on a single topic and makes the work steps individually verifiable.

**P5** — Write one instruction per procedural step. The comma that separates the condition from the command also enforces the one-instruction-per-step rule. The structure "Condition, command" naturally limits each sentence to one action because a second action would require a second condition-command pair. This prevents multi-instruction sentences that confuse the reader about which action depends on which condition.

**P1** — Use approved words from the controlled terminology. Short condition-command sentences are easier to write and read when every word is approved and unambiguous. The comma boundary between condition and command makes the sentence structure predictable, which simplifies translation and localization of code documentation.

**P8** — Use the approved active voice. The command portion of the sentence must use the imperative mood ("run," "set," "call," "include"). The condition portion uses declarative language to describe the prerequisite. The comma keeps the two modes distinct: descriptive for the condition, imperative for the command.
