# Rule 7.1 — Use an Applicable Word (for Example, "Warning" or "Caution") to Identify the Level of Risk

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.1

## Original Rule

Use a word (for example, "warning" or "caution") or, when applicable, a symbol, to immediately show your reader the level of the related risk.

- If there is a risk of injury or death, use a "warning."
- If there is a risk of damage to machines, tools, or equipment, use a "caution."
- If there are the two levels of risk together, use a "warning."

## STE-Code Adaptation

In code documentation, use an applicable word (for example, "WARNING" or "CAUTION") or, when applicable, a symbol, to immediately show the developer the level of the related risk.

- If there is a risk of a security breach, data loss, system crash, or severe functional failure, use a "WARNING."
- If there is a risk of unexpected behavior, performance degradation, incorrect output, or API misuse, use a "CAUTION."
- If there are the two levels of risk together, use a "WARNING."

When a safety instruction relates to code that handles sensitive data (for example, user credentials, payment data, or personal information), always use "WARNING" because a failure can cause data loss or a security breach, which is equivalent to injury in the physical domain. In code documentation, the WARNING label tells the developer that incorrect use of the code can cause critical system failure, data corruption, or a security vulnerability. The CAUTION label tells the developer that incorrect use can cause non-critical defects, degraded performance, or wasted resources.

### Examples

The non-STE example below describes a database query function that concatenates user input directly into SQL. The safety instruction is a caution. But if you know about SQL injection, you also know that unsanitized user input can cause data breaches and data loss. Because there is a risk of data loss or a security breach here, you must identify this safety instruction as a warning.

> **Non-STE:** CAUTION: THE QUERYBUILDER FUNCTION REQUIRES CAREFUL HANDLING OF ITS INPUT PARAMETERS.

> **STE-Code:** WARNING: BEFORE YOU CALL THE QUERYBUILDER FUNCTION, ALWAYS SANITIZE ALL USER INPUT WITH THE PREPAREDSTATEMENT CLASS. UNSANITIZED INPUT CAN CAUSE AN SQL INJECTION ATTACK, DATA CORRUPTION, AND DATA LOSS.

In the non-STE example, the safety instruction is an abstract sentence and only makes a general statement. The warning in STE-Code gives clear and correct information about how to decrease the risk of an SQL injection attack. The warning contains the words "SQL injection attack," "data corruption," and "data loss" to make the developer clearly understand how important this safety instruction is.
