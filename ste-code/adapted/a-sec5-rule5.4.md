# Rule 5.4 — Descriptive Statement Before the Command

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.4

## Original Rule

When there is a condition that the reader must know about first, start the instruction with a descriptive statement. Then, divide that descriptive statement from the command with a comma.

If a special condition is necessary for a work step, the reader must know the condition first. Write the condition first in the sentence, and then use a comma to show the end of the condition, and the start of the instruction.

Examples:

| Do not write: | Before you remove the clamp, you must disconnect the hose. |
| --- | --- |
| WRITE: | Before you remove the clamp, disconnect the hose. |

WRITE: If the Constant Speed Drive (CSD) does not operate correctly, disconnect it from the gearbox.

The comma is important. Be careful when you use it because the position of the comma can change the meaning of your sentence.

| STE: | WARNING: IF YOU MUST CUT THE WIRE, ALWAYS USE A PROTECTIVE MASK. PIECES OF WIRES CAN CAUSE INJURY. |
| --- | --- |

If the Constant Speed Drive (CSD) does not operate, correctly disconnect it from the gearbox.

The two sentences in the examples are correct, but their meanings are different. In the first sentence, the comma after "correctly" shows that the adverb modifies the verb "operate." In the second sentence, the comma after "operate" shows that the adverb modifies the verb "disconnect."

## STE-Code Adaptation

In code documentation, many procedural steps have conditions that the reader must know before they act. Examples include checking that a service is running before stopping it, verifying that a file exists before editing it, or confirming that a previous step completed successfully before proceeding.

Write the condition as a descriptive statement at the start of the sentence, followed by a comma, and then the instruction in the imperative form. This structure ensures the reader evaluates the condition before executing the command.

The comma is critical for correct meaning. The position of the comma determines which part of the sentence an adverb or adverbial phrase modifies. Place the comma immediately after the condition clause, before the instruction.

### Examples

> **Non-STE:** Before you change the database schema you must shut down the application server and stop all background worker processes that are connected to the database.
> **STE:** Before you change the database schema, shut down the application server and stop all background worker processes that connect to the database.

(The comma separates the condition from the instruction. The reader evaluates the condition first.)

> **Non-STE:** You should disconnect the active client sessions first if the connection pool has reached its maximum capacity and new connections are being rejected by the server.
> **STE:** If the connection pool has reached its maximum capacity, disconnect the active client sessions.

(The condition comes first. The comma separates the descriptive "if" clause from the command "disconnect.")

| Do not write: | When the configuration file fails to load the application uses the default settings from the built-in configuration provider. |
| --- | --- |
| WRITE: | When the configuration file fails to load, the application uses the default settings from the built-in configuration provider. |

(The comma after "load" is necessary to show where the condition ends and the main clause begins.)

> **Non-STE:** Run the cleanup script to remove temporary build artifacts after the test suite completes successfully and all test results have been written to the output directory.
> **STE:** After the test suite completes successfully, run the cleanup script to remove temporary build artifacts.

(The condition "after the test suite completes successfully" comes first, separated by a comma from the instruction.)

Comma placement changes meaning:

> If the service does not start, automatically restart it with the recovery script.
> (The comma after "start" shows that "automatically" modifies the verb "restart." The restart happens automatically.)

> If the service does not start automatically, restart it with the recovery script.
> (The comma after "automatically" shows that "automatically" modifies the verb "start." The reader must restart the service manually if it does not start automatically.)

> **WARNING:** IF YOU MUST DELETE THE ENCRYPTION KEY, ALWAYS VERIFY THAT NO ACTIVE SESSIONS USE THE KEY. DELETING AN ACTIVE ENCRYPTION KEY CAN CAUSE PERMANENT DATA LOSS.

(The condition "IF YOU MUST DELETE THE ENCRYPTION KEY" comes first, followed by a comma and the safety instruction.)
