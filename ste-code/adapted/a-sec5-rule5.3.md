# Rule 5.3 — Imperative (Command) Form for Instructions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 5.3

## Original Rule

Write instructions in the imperative (command) form.

An instruction tells the reader to do something. Write the verb in the imperative (command) form.

Examples in STE:

Set the switch to ON.
Remove the four bolts.
Increase the pressure to 60 psi.
Inflate the tires.
Install the new O-ring.

The imperative form gives the reader a clear instruction. If you use other types of sentence structure, you can cause ambiguity. Thus, the reader will not know:

- If it is important to do a work step.
- If a different person did the work step.
- If a different person must do the work step in the future.

Examples:

> **Non-STE:** The test can be continued.
>
> **STE:** Continue the test.

> **Non-STE:** Oil and grease are to be removed with a degreasing agent.
>
> **STE:** Remove oil and grease with a degreasing agent.

Do not use the verb "must" before the imperative form, unless the instruction is very important for safety (for example, in a safety instruction) or when you give an important condition.

Example:

| Do not write: | Before you remove the clamp, you must disconnect the hose. |
| --- | --- |
| WRITE: | Before you remove the clamp, disconnect the hose. |
| STE: | WARNING: IF YOU MUST CUT THE WIRE, ALWAYS USE A PROTECTIVE MASK. PIECES OF WIRES CAN CAUSE INJURY. |

## STE-Code Adaptation

In code documentation, instructions that tell the reader to execute a command, edit a file, change a setting, or run a script must use the imperative (command) form. The imperative form gives a direct and unambiguous instruction. Passive constructions, modal verbs, and indirect phrasing create ambiguity about whether the reader needs to act, whether the action has already been completed, or whether someone else will perform it.

Start each procedural instruction with an imperative verb. Common imperative verbs in code documentation include: "run," "set," "open," "save," "install," "configure," "restart," "execute," "copy," "delete," "create," "add," "enter," "select," "click," "type," and "verify."

Do not use passive voice, gerunds, or modal verbs (such as "can," "could," "should," "may," or "might") for instructions. Do not use "must" before the imperative form in a standard instruction. Reserve "must" for security warnings, data loss cautions, and conditions that are critical for safety.

### Examples

Imperative form in code documentation procedures:

Set the environment variable to the production value.
Run the database migration command.
Install the required dependencies.
Save the configuration file.
Restart the application server.

> **Non-STE:** The unit tests can be executed with the command `npm test`.
>
> **STE:** Execute the unit tests with the command `npm test`.
>
> *Adapted from spec pair: "The test can be continued." → "Continue the test."*

> **Non-STE:** The old log files are to be removed before the new deployment.
>
> **STE:** Remove the old log files before the new deployment.
>
> *Adapted from spec pair: "Oil and grease are to be removed with a degreasing agent." → "Remove oil and grease with a degreasing agent."*

> **Non-STE:** The configuration file should be validated against the schema before the application is started.
>
> **STE:** Validate the configuration file against the schema before you start the application.
>
> *Adapted from spec: modal verb guidance — replace "should," "can," "could," "may," "might" with the direct imperative form.*

> **Non-STE:** The SSL certificate must be renewed and then the web server must be restarted to apply the changes.
>
> **STE:** Renew the SSL certificate. Then, restart the web server to apply the changes.
>
> *Adapted from spec: "must" guidance — do not use "must" before the imperative form in standard instructions.*

(No "must" is necessary because certificate renewal is a standard procedure, not a safety-critical instruction.)

> **Non-STE:** It is recommended that you create a backup of the database before running the migration script.
>
> **STE:** Create a backup of the database before you run the migration script.
>
> *Adapted from spec: indirect phrasing guidance — replace "it is recommended that" with the direct imperative form.*

(Do not use "it is recommended that." Give the instruction directly.)

| Do not write: | Before you delete the branch, you must push all local commits to the remote repository. |
| --- | --- |
| WRITE: | Before you delete the branch, push all local commits to the remote repository. |

> *Adapted from spec pair: "Before you remove the clamp, you must disconnect the hose." → "Before you remove the clamp, disconnect the hose."*

> **WARNING:** IF YOU MUST STORE CREDENTIALS IN THE CONFIGURATION FILE, ALWAYS USE AN ENCRYPTED SECRETS MANAGER. PLAIN-TEXT CREDENTIALS CAN CAUSE SECURITY BREACHES.
>
> *Adapted from spec: "WARNING: IF YOU MUST CUT THE WIRE, ALWAYS USE A PROTECTIVE MASK. PIECES OF WIRES CAN CAUSE INJURY."*

("Must" is correct here because the instruction is critical for security. The warning format signals the importance to the reader.)

> **See also:** Rule 5.4 — Descriptive Statement Before the Command; Rule 7.1 — Use an Applicable Word to Identify the Level of Risk; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition
