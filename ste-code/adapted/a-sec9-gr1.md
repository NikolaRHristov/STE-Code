# GR-1 — The Conjunction "That"

> **Source:** Adapted from ASD-STE100 Issue 9, GR-1

## Original Rule

The conjunction "that" (general recommendation, not an STE rule).

In English, you can use the conjunction "that" to connect new information (in a subordinate clause) to a main clause. You can use this conjunction after verbs. For example: "make sure," "show," and "recommend."

Native English speakers frequently do not use "that" when they speak, and this style also occurs in writing. But this conjunction helps the reader understand where the end of the main clause and the start of the subordinate clause is. Thus, use the conjunction "that" as much as possible to prevent ambiguity.

This conjunction also helps with translation because, in many other languages, it is not possible to omit the equivalent word.

## STE-Code Adaptation

In code documentation, use the conjunction "that" to connect new information in a subordinate clause to a main clause. Use it after verbs such as "make sure," "show," "recommend," "verify," and "confirm."

Native English speakers frequently omit "that" in speech and informal writing. But this conjunction helps the reader identify where the main clause ends and the subordinate clause begins. Use "that" as much as possible to prevent ambiguity, especially in complex sentences about software behavior, configuration requirements, or expected output.

This conjunction also helps with translation and with readers whose first language is not English.

### Examples

> **Non-STE:** Make sure the database connection is open before you run the query.
> **STE:** Make sure that the database connection is open before you run the query.
>
> *Adapted from spec pattern: "that" after "make sure" — the spec recommends using "that" after verbs such as "make sure," "show," and "recommend."*

> **Non-STE:** The API documentation recommends you set the timeout to 30 seconds.
> **STE:** The API documentation recommends that you set the timeout to 30 seconds.
>
> *Adapted from spec pattern: "that" after "recommend" — same verb class as the spec's "recommend."*

> **Non-STE:** The terminal output shows the build completed without errors.
> **STE:** The terminal output shows that the build completed without errors.
>
> *Adapted from spec pattern: "that" after "show" — same verb class as the spec's "show."*

> **Non-STE:** Verify the environment variable is set correctly.
> **STE:** Verify that the environment variable is set correctly.
>
> *Adapted from spec pattern: "that" after verification verbs — extends the spec's pattern to "verify" and similar verbs.*

> **Non-STE:** Confirm the user has write permissions to the target directory.
> **STE:** Confirm that the user has write permissions to the target directory.
>
> *Adapted from spec pattern: "that" after confirmation verbs — extends the spec's pattern to "confirm" and similar verbs.*
