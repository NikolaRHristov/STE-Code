# GR-4 — The Pronoun "this"

> **Source:** Adapted from ASD-STE100 Issue 9, General Recommendation GR-4

> **Source:** [master.md#sec9-gr4](ste-code/grouped/)

> Source: master.md#sec9-gr4

## Original Rule

When you use the pronoun "this" in a sentence, make sure that the reader knows the item the pronoun refers to. If "this" can refer to more than one item, give the applicable context again.

### Examples

> **Do not write:** Make sure that the cover is not locked (this can cause damage to the probe).
>
> (Which is the cause of damage to the probe? The cover in the locked condition? Or the cover in the unlocked condition?)

> **WRITE:** Make sure that the cover is not locked. If the cover is locked, this can cause damage to the probe.
>
> Or: If the cover is locked, damage to the probe can occur.

> **Do not write:** Do not use crocus cloth on aluminum parts. If you do this, you can cause corrosion on aluminum parts. Crocus cloth contains ferrous oxide.
>
> **WRITE:** Do not use crocus cloth on aluminum parts. Crocus cloth contains ferrous oxide, which can cause corrosion on aluminum parts.

## Adapted Rule

When you use the pronoun "this" in a sentence, make sure that the reader knows the item the pronoun refers to. If "this" can refer to more than one item, give the applicable context again.

### Examples

> **Non-STE:** Make sure that the cache is not locked (this can cause a stale read).
>
> (Which is the cause of the stale read? The cache in the locked condition? Or the cache in the unlocked condition?)

> **STE:** Make sure that the cache is not locked. If the cache is locked, this can cause a stale read.
>
> Or: If the cache is locked, a stale read can occur.

(The first STE version repeats "the cache is locked" so "this" has one clear referent. The second removes "this" entirely and states the consequence directly.)

> **Non-STE:** Do not use `console.log` in production code. If you do this, you can cause a performance problem. `console.log` writes to the standard output synchronously.
>
> **STE:** Do not use `console.log` in production code. `console.log` writes to the standard output synchronously, which can cause a performance problem.

(The "this" version is ambiguous because "this" could refer to "use `console.log`" or to "production code." The STE version binds the cause to `console.log` with "which.")

> **Non-STE:** Close the file handle before you exit the process (this prevents a descriptor leak).
>
> **STE:** Close the file handle before you exit the process. If you do not close the file handle, a descriptor leak can occur.

("This" after a parenthetical is a frequent ambiguity source. Restate the condition and the consequence without the pronoun.)

## Code-Domain Explanation

GR-4 is a focused form of GR-3. The pronoun "this" most often appears at the start of a clause or inside parentheses, where it can float between two nearby nouns. In code documentation the two nouns are frequently a component and an action, and the reader cannot tell which one "this" modifies.

Three fixes, in order of preference:

1. **Restate the referent.** "Make sure that the cache is not locked. If the cache is locked, this can cause a stale read." The repetition removes all doubt.
2. **State the consequence directly.** "If the cache is locked, a stale read can occur." No pronoun, no ambiguity.
3. **Bind with "which."** "The `console.log` call writes synchronously, which can cause a performance problem." The "which" clause attaches to the nearest complete idea.

Avoid the pattern "Do X. If you do this, Y" when "this" could mean X or the surrounding context. Name the cause.

## Edge Cases

### "This" as a determiner versus a pronoun

"This" can be a determiner ("use this function") or a pronoun ("this causes a leak"). GR-4 applies to the pronoun use. As a determiner, "this" is clear when it directly precedes the noun it modifies ("use this function," not "use this"). When "this" stands alone as a pronoun, apply the rule above.

### "This" at the start of a sentence after a list

When a sentence starts with "This" after a list of items, the referent is usually the whole list, not one item. State the list result instead: "These three steps prepare the environment" is clearer than "This prepares the environment" when the reader must know that all three steps matter.

## Cross-References

- **GR-3 (How to Use Pronouns):** The general rule for pronoun clarity. GR-4 is the "this" special case.
- **Rule 9.2 (Use Each Approved Word Correctly):** Use "this" only as the approved pronoun. Do not use it where a noun is required for clarity.
- **Rule 4.1 (Sentence Structure):** Keep the referent and "this" in the same or adjacent sentence so the link stays clear.
