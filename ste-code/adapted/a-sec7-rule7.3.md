# Rule 7.3 — Give an Explanation to Show the Risk or Possible Result

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.3

## Original Rule

**Rule 7.3** If it is possible, always tell your reader about the problems that can occur if the reader does not obey the safety instruction. If there is a clear and specified risk, the person who does the task will understand the risk and be more careful.

**Spec examples:**

(Refer to the underlined risk or possible result.)

> **WARNING:** DO NOT SWALLOW THE SOLVENT. ALWAYS MAKE SURE THAT YOU KNOW THE SAFETY PRECAUTIONS AND FIRST AID INSTRUCTIONS FOR SOLVENTS. SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH.

> **CAUTION:** DO NOT USE BLEACH OR CLEANSERS THAT CONTAIN CHLORINE TO CLEAN THE UNIT. THESE CLEANING AGENTS CAN CAUSE CORROSION.

> IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR.

## STE-Code Adaptation

**Rule 7.3** In code documentation, if it is possible, always tell your reader about the problems that can occur if the reader does not obey the safety instruction. If there is a clear and specified risk, the developer who uses the code will understand the risk and be more careful.

### Examples

> **Non-STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.
>
> *Adapted from spec pattern: WARNING with risk explanation — "SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH."*

> **Non-STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS.
>
> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *Adapted from spec pattern: CAUTION with risk explanation — "THESE CLEANING AGENTS CAN CAUSE CORROSION."*

> **Non-STE:** MAKE SURE THAT YOU SET THE CONNECTION TIMEOUT.
>
> **STE:** IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.
>
> *Adapted from spec pattern: consequence statement — "IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR."*
