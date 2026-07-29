# Rule 9.4 — When You Select Terminology or Wording, Always Use a Consistent Style

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 9.4

## Original Rule

When you select terminology or wording, always use a consistent style.

In procedures, you will frequently give the same information again and again. For example, most procedures give instructions on how to remove or install components or parts. When you select terminology or wording for a work step, use the same terminology or wording each time that type of work step occurs. The reader will identify the terminology or wording and will quickly understand the action. Different terminology or wording can cause confusion and delays.

In descriptive writing, the reader must understand the text as a unit. Thus, it is important to use words and sentences correctly and give a logical structure to the text. This method makes the text easier to read and understand.

## STE-Code Adaptation

When you select terminology or wording in code documentation, always use a consistent style.

In procedural code documentation, you frequently give the same type of instruction again and again. For example, most setup guides give instructions on how to install dependencies, configure settings, or initialize a project. When you select terminology or wording for a step, use the same terminology or wording each time that type of step occurs. The reader will identify the consistent terminology and will quickly understand the action. Different terminology or wording for the same action can cause confusion and delays.

This applies to all levels of consistency: use the same name for the same item (do not alternate between "configuration file," "settings file," and "config"), use the same verb for the same action (do not alternate between "compile," "build," and "make"), and use the same sentence structure for the same type of instruction.

In descriptive writing, the reader must understand the text as a unit. Use words and sentences correctly and give a logical structure to the text. This method makes the text easier to read and understand.

### Examples

Inconsistent (non-STE) documentation:

```
1. Open the configuration file in a text editor.
2. Change the port number in the settings file.
3. Save the config and close it.
4. Compile the project with the build command.
5. Make the binary for the target platform.
6. If you get errors, look at the log file.
```

STE-Code (consistent):

```
1. Open the configuration file in a text editor.
2. Change the port number in the configuration file.
3. Save the configuration file and close it.
4. Build the project with the build command.
5. Build the binary for the target platform.
6. If you get errors, look at the log file.
```

In the non-STE text, you can see different wordings:
- Different terms for the same file ("configuration file," "settings file," and "config")
- Different verbs for the same action ("compile," "build," and "make")

In the STE-Code text, each time that the same item occurs, it has the same noun, and the same action always has the same verb. This makes the text clear and easy to read.
