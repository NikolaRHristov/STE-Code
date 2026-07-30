# Rule 7.1 — Use an Applicable Word (for Example, "Warning" or "Caution") to Identify the Level of Risk

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.1

## Original Rule

**Rule 7.1** Use a word (for example, "warning" or "caution") or, when applicable, a symbol, to immediately show your reader the level of the related risk.

- If there is a risk of injury or death, use a "warning."
- If there is a risk of damage to machines, tools, or equipment, use a "caution."
- If there are the two levels of risk together, use a "warning."

In the non-STE example that follows, the safety instruction is a caution. But if you know about oxygen systems, you also know that oxygen mixed with other materials can cause explosions. Because there is a risk of injury or death here, you must identify this safety instruction as a warning.

Compare the wording in the two safety instructions. The non-STE safety instruction is an abstract sentence and only makes a general statement. The warning in STE gives clear and correct information about how to decrease the risk of explosion. The warning contains the words "explosion," "injury," and "death" to make the reader clearly understand how important this safety instruction is.

**Spec example:**

> **Non-STE:** CAUTION: EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE.
> **STE:** WARNING: BEFORE YOU FILL THE LIQUID OXYGEN SYSTEM, PUT ON A FACE MASK AND PROTECTIVE CLOTHING. LIQUID OXYGEN CAN CAUSE IRRITATION OF THE RESPIRATORY TRACT AND EYE IRRITATION.

## STE-Code Adaptation

**Rule 7.1** In code documentation, use a signal word (for example, "WARNING" or "CAUTION") to immediately show your reader the level of the related risk.

- If there is a risk of security vulnerabilities, data loss, or system corruption, use a "WARNING."
- If there is a risk of unexpected behavior, performance degradation, or incorrect results, use a "CAUTION."
- If there are the two levels of risk together, use a "WARNING."

In the non-STE example that follows, the safety instruction is a caution. But if you know about data validation in software systems, you also know that unvalidated input can cause security breaches and data loss. Because there is a risk of security vulnerabilities and data loss here, you must identify this safety instruction as a warning.

Compare the wording in the two code-documentation safety instructions. The non-STE safety instruction is an abstract statement and only makes a general claim. The warning in STE-Code gives clear and correct information about how to decrease the risk of security breaches. The warning contains the words "security breach" and "data loss" to make the reader clearly understand how important this safety instruction is.

### Examples

> **Non-STE:** CAUTION: ALWAYS VALIDATE INPUT DATA.
> **STE:** WARNING: BEFORE YOU PROCESS INPUT DATA, MAKE SURE THAT YOU SANITIZE AND VALIDATE THE DATA. UNSANITIZED INPUT CAN CAUSE SECURITY BREACHES AND DATA LOSS.
>
> *Adapted from spec pair: "CAUTION: EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE." → "WARNING: BEFORE YOU FILL THE LIQUID OXYGEN SYSTEM, PUT ON A FACE MASK AND PROTECTIVE CLOTHING. LIQUID OXYGEN CAN CAUSE IRRITATION OF THE RESPIRATORY TRACT AND EYE IRRITATION." — an abstract caution is escalated to a specific warning when the true risk level is higher.*

> **Non-STE:** CAUTION: THE CONFIGURATION FILE MAY CONTAIN OUTDATED SETTINGS.
> **STE:** CAUTION: BEFORE YOU DEPLOY THE APPLICATION, COMPARE THE CONFIGURATION FILE AGAINST THE REFERENCE CONFIGURATION. OUTDATED SETTINGS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *Code-domain CAUTION example — risk of unexpected behavior and incorrect results, not security or data loss.*

> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition
