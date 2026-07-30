# GR-4 — The Pronoun "This"

> **Source:** Adapted from ASD-STE100 Issue 9, GR-4

## Original Rule

The pronoun "this" (general recommendation, not an STE rule).

When you use the pronoun "this" in a sentence, make sure that the reader knows the item the pronoun refers to. If "this" can refer to more than one item, give the applicable context again.

## STE-Code Adaptation

> **See also:** GR-1 — The Conjunction "That"; GR-2 — The Preposition "With"; GR-3 — How to Use Pronouns

In code documentation, when you use the pronoun "this" in a sentence, make sure that the reader knows exactly which item, condition, or result the pronoun refers to. If "this" can refer to more than one item in the preceding text, repeat the applicable context to remove the ambiguity.

In software documentation, "this" frequently refers to a condition, an error state, a configuration, or a result described in the previous sentence. If the reader cannot immediately identify the referent, the instruction or explanation becomes unclear and can lead to incorrect implementation.

### Examples

> **Non-STE:** Make sure that the connection is not closed. If it is, this can cause failure of the request.
>
> (Does "this" refer to the connection in the closed condition or to the connection in the not-closed condition?)

> **STE:** Make sure that the connection is not closed. If the connection is closed, this can cause failure of the request.

(The context is repeated so that the reader knows "this" refers to the closed condition.)
*Adapted from spec pair: "Make sure that the cover is not locked. If it is, this can cause damage to the probe." / "Make sure that the cover is not locked. If the cover is locked, this can cause damage to the probe."*

Or:

> **STE:** If the connection is closed, failure of the request can occur.

*Adapted from spec alternative: "If the cover is locked, damage to the probe can occur."*

> **Non-STE:** Check that the environment variable is set. If it is not, this can prevent the build from completing.
>
> (Does "this" refer to the variable being not set, or to the act of checking?)

> **STE:** Check that the environment variable is set. If the environment variable is not set, this condition can prevent the build from completing.

*Adapted from spec pattern: repeat the applicable context to disambiguate "this."*

> **Non-STE:** Verify that the function returns a non-null value. If it does not, this can cause a runtime error in the caller.
>
> **STE:** Verify that the function returns a non-null value. If the function returns a null value, this null value can cause a runtime error in the caller.

*Adapted from spec pattern: replace the pronoun with the explicit referent to remove ambiguity.*
