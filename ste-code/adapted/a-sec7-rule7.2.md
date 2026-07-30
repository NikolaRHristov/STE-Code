# Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.2

## Original Rule

**Rule 7.2** Start a safety instruction with a clear and accurate command or condition. Your reader must know how to prevent accidents and keep a high level of safety.

If your reader must know about a condition before the start of a procedure or work step, give this condition first.

**Spec examples:**

(Refer to the underlined command.)

> **WARNING:** DO NOT SWALLOW THE SOLVENT. ALWAYS MAKE SURE THAT YOU KNOW THE SAFETY PRECAUTIONS AND FIRST AID INSTRUCTIONS FOR SOLVENTS. SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH.

> **CAUTION:** DO NOT USE BLEACH OR CLEANSERS THAT CONTAIN CHLORINE TO CLEAN THE UNIT. THESE CLEANING AGENTS CAN CAUSE CORROSION.

(Refer to the underlined condition.)

> IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR.

## STE-Code Adaptation

**Rule 7.2** In code documentation, start a safety instruction with a clear and accurate command or condition. Your reader must know how to prevent security vulnerabilities, data loss, and system failures.

If your reader must know about a condition before they use a function, method, or API, give this condition first.

### Examples

> **Non-STE:** WARNING: STORING API KEYS IN THE SOURCE CODE IS NOT RECOMMENDED.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE ENVIRONMENT VARIABLES OR A SECRETS MANAGER TO STORE API KEYS. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.
>
> *Adapted from spec pair: "WARNING: DO NOT SWALLOW THE SOLVENT. ALWAYS MAKE SURE THAT YOU KNOW THE SAFETY PRECAUTIONS AND FIRST AID INSTRUCTIONS FOR SOLVENTS. SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH." — the safety instruction starts with a clear command ("DO NOT STORE") and explains the risk.*

> **Non-STE:** CAUTION: THE CODEBASE CONTAINS DEPRECATED FUNCTIONS.
>
> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS OR METHODS THAT HAVE KNOWN ISSUES. USE THE APPROVED REPLACEMENT FUNCTIONS SPECIFIED IN THE MIGRATION GUIDE. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *Adapted from spec pair: "CAUTION: DO NOT USE BLEACH OR CLEANSERS THAT CONTAIN CHLORINE TO CLEAN THE UNIT. THESE CLEANING AGENTS CAN CAUSE CORROSION." — the safety instruction starts with a clear command ("DO NOT USE") and explains the risk.*

> **Non-STE:** PERMANENT DATA LOSS CAN OCCUR.
>
> **STE:** IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.
>
> *Adapted from spec pair: "IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR." — the safety instruction starts with a clear condition ("IF YOU DO NOT SET...") before stating the risk.*

> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions; Rule 5.4 — Descriptive Statement Before the Command; Rule 7.1 — Use an Applicable Word to Identify the Level of Risk
