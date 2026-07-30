# GR-2 — The Preposition "With"

> **Source:** Adapted from ASD-STE100 Issue 9, GR-2

## Original Rule

The preposition "with" (general recommendation, not an STE rule).

In STE, the preposition "with" has three approved meanings. It is a function word that shows "association or relationship," "help or sharing," or "a means or instrument." In some sentences, this word can cause ambiguity. For example, the sentence: "Install the panel with the green fasteners" can have different meanings:

- Install the panel that has green fasteners.
- Install the panel together with the green fasteners.
- Use the green fasteners to install the panel.

Usually, the context of the sentence will give the reader sufficient information to know which meaning is correct. But when you use the word "with," read your sentence again. Make sure that your sentence does not cause ambiguity, that there are no errors, and that the meaning of the sentence does not change.

When you want to use a different sentence construction to replace the word "with," make sure that you show the primary action verb in the work step.

## STE-Code Adaptation

In code documentation, the preposition "with" has three approved meanings: "association or relationship," "help or sharing," and "a means or instrument." In some sentences, "with" can cause ambiguity. For example, the sentence "Build the project with the debug flag" can have different meanings:

- Build the project that has the debug flag set.
- Build the project together with the debug flag.
- Use the debug flag to build the project.

Usually, the context gives sufficient information to know which meaning is correct. But when you use "with," read your sentence again. Make sure that it does not cause ambiguity, that there are no errors, and that the meaning does not change.

When you want to use a different sentence construction to replace "with," make sure that you show the primary action verb in the step. Start with the condition or the primary action to make the sentence clearer.

### Examples

> **Non-STE:** Compile the project at the maximum optimization level with debug symbols.
>
> **STE:** Compile the project at the maximum optimization level (debug symbols included).
>
> *Adapted from spec pair: "Install the panel with the green fasteners" — ambiguous "with" replaced by a clarifying construction using parentheses.*
>
> (The context tells you that you will not ask the debug symbols to help you compile the project. But because the sentence can have two different meanings, one interpretation makes it ambiguous. Use parentheses to clarify that debug symbols are included, not that they are the means.)

> **Non-STE:** Make sure that the function does not modify the global state with the write flag enabled.
>
> **STE:** When you enable the write flag, make sure that the function does not modify the global state.
>
> *Adapted from spec pattern: ambiguous "with" resolved by restructuring the sentence to place the condition first — as recommended in the spec: "make sure that you show the primary action verb in the work step."*
>
> (Write the condition first to remove the ambiguity about what "with" refers to.)

> **Non-STE:** Use the linter to check the source code for style violations.
>
> **STE:** Check the source code for style violations with the linter.
>
> *Adapted from spec pattern: "with" in the approved meaning of "a means or instrument" — the spec recommends showing the primary action verb ("check") rather than "use."*
>
> (This sentence is clear because it identifies the tool. In the controlled terminology, give the primary action verb which is "check" and not "use." The word "with" here has the approved meaning "a means or instrument.")
