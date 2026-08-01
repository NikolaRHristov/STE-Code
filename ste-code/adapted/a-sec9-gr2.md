# GR-2 — The Preposition "with"

> **Source:** Adapted from ASD-STE100 Issue 9, General Recommendation GR-2

> **Source:** [master.md#sec9-gr2](ste-code/grouped/)

> Source: master.md#sec9-gr2

## Original Rule

In STE, the preposition "with" has three approved meanings. It is a function word that shows "association or relationship," "help or sharing," or "a means or instrument." In some sentences, this word can cause ambiguity. For example, the sentence: "Install the panel with the green fasteners" can have different meanings:

- Install the panel that has green fasteners.
- Install the panel together with the green fasteners.
- Use the green fasteners to install the panel.

Usually, the context of the sentence will give the reader sufficient information to know which meaning is correct.

But when you use the word "with," read your sentence again. Make sure that your sentence does not cause ambiguity, that there are no errors, and that the meaning of the sentence does not change.

### Examples

> **Do not write:** Lift the aircraft at the maximum takeoff weight with passengers.
>
> **WRITE:** Lift the aircraft at the maximum takeoff weight (passenger weight included).

> **Do not write:** Make sure that the lever does not touch the stop (1) with hydraulic pressure supplied.
>
> **WRITE:** When you supply hydraulic pressure, make sure that the lever does not touch the stop (1).

> **Do not write:** Use tool TS9867 to seal the opening.
>
> **WRITE:** Seal the opening with tool TS9867.

## Adapted Rule

In code documentation, the preposition "with" has three approved meanings. It is a function word that shows "association or relationship," "help or sharing," or "a means or instrument." In some sentences, this word can cause ambiguity. For example, the sentence: "Run the service with the new config flags" can have different meanings:

- Run the service that has the new config flags (the flags are part of its state).
- Run the service together with the new config flags (start both at the same time).
- Use the new config flags to run the service (the flags are the means).

Usually, the context of the sentence will give the reader sufficient information to know which meaning is correct.

But when you use the word "with," read your sentence again. Make sure that your sentence does not cause ambiguity, that there are no errors, and that the meaning of the sentence does not change.

When you want to use a different sentence construction to replace the word "with", make sure that you show the primary action verb in the work step.

### Examples

> **Non-STE:** Deploy the application at the maximum memory limit with debug logging enabled.
>
> **STE:** Deploy the application at the maximum memory limit (debug logging enabled).

(The context tells you that you will not ask the debug logging to help you deploy the application. Because the sentence can have two different meanings, one interpretation makes it a joke. State the enabled state in parentheses.)

> **Non-STE:** Make sure that the container does not restart with the health check enabled.
>
> **STE:** When you enable the health check, make sure that the container does not restart.

(Write the condition first. The "with" version is ambiguous: does the health check cause the restart, or must you check during a restart that already happens for another reason?)

> **Non-STE:** Use script migrate.py to seed the database.
>
> **STE:** Seed the database with script migrate.py.

(This sentence is clear because it gives the script name. In code documentation you must give the primary action verb, which is "seed," and not "use.")

> **Non-STE:** Build the image with the cache disabled to force a clean layer pull.
>
> **STE:** Build the image. Set the cache to disabled to force a clean layer pull.

(When "with" hides a second action, split the sentence so the primary verb "build" and the configuration verb "set" are both explicit.)

## Code-Domain Explanation

GR-2 warns against ambiguity that the word "with" introduces when it can mean "has," "together with," or "by means of." In code documentation these three readings appear most often in:

1. **Deployment and run commands.** "Start the worker with the staging profile" can mean the worker carries the staging profile, or you use the staging profile to start it. Prefer "Start the worker. Use the staging profile." or "Use the staging profile to start the worker."
2. **Build and test configuration.** "Run the tests with coverage on" is clearer as "Run the tests. Turn coverage on." when two actions are involved.
3. **Tool and script invocation.** When a tool is the instrument, keep the primary action verb and attach the tool with "with": "Seed the database with script migrate.py." Do not lead with "Use script migrate.py to seed."

The rule does not forbid "with." It forbids ambiguous "with." When the context removes the ambiguity, "with" is acceptable. When in doubt, restructure and make the primary action verb explicit.

## Edge Cases

### "With" as a relationship word in data descriptions

"The user with the admin role" means the user who has the admin role. This is the "association or relationship" meaning and is usually clear. Keep it unless the sentence also has a second "with" that could conflict.

### Multi-tool instructions

When more than one instrument is involved, "with" stacks badly: "Process the file with parser A with validator B." Restructure: "Process the file with parser A. Then validate the result with validator B."

## Cross-References

- **Rule 9.1 (Use a Different Sentence Construction):** When "with" makes a sentence ambiguous, restructure it instead of replacing the word directly.
- **Rule 9.4 (Consistent Style):** Pick one construction for "run with X" versus "use X to run" and apply it every time the same situation occurs.
- **Rule 5.1 (Short Sentences):** Splitting an ambiguous "with" sentence into two short sentences frequently removes the ambiguity.
