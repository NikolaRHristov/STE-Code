# Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.2

## Original Rule

Start a safety instruction with a clear and accurate command or condition. Your reader must know how to prevent accidents and keep a high level of safety.

## STE-Code Adaptation

In code documentation, start a safety instruction with a clear and accurate command or condition. The developer must know how to prevent security vulnerabilities, data corruption, and system failures, and how to keep a high level of code safety.

When you start a safety instruction with a command, use an imperative verb (for example, "SANITIZE," "VALIDATE," "ENCRYPT," or "DO NOT USE"). The command tells the developer exactly what action to take or to avoid. When you start with a condition, give the condition first so the developer knows the state that must be true before the code can run safely.

### Examples

The non-STE example below uses an abstract and indirect safety instruction about a file system operation. The STE-Code example starts with a clear command that tells the developer exactly what to check.

> **Non-STE:** WARNING: THE FILEWRITER MODULE CAN OVERWRITE EXISTING FILES IF THE OVERWRITE FLAG IS NOT PROPERLY SET. USERS SHOULD VERIFY FILE PATHS BEFORE INVOCATION.

> **STE-Code:** WARNING: BEFORE YOU CALL THE FILEWRITER.CREATE METHOD, MAKE SURE THAT THE FILE PATH DOES NOT POINT TO AN EXISTING FILE. USE THE FILEEXISTS METHOD TO CHECK THE PATH. THE FILEWRITER MODULE OVERWRITES EXISTING FILES WITHOUT A CONFIRMATION PROMPT. THIS CAN CAUSE PERMANENT DATA LOSS.

The non-STE example below uses a general statement about a configuration parser. The STE-Code example starts with a command that gives the developer an exact action to take.

> **Non-STE:** CAUTION: THE CONFIGPARSER CLASS REQUIRES THAT THE CONFIGURATION FILE IS VALID JSON. MALFORMED INPUT CAN CAUSE APPLICATION FAILURES.

> **STE-Code:** CAUTION: DO NOT GIVE AN UNVALIDATED STRING TO THE CONFIGPARSER CLASS. FIRST VALIDATE THE INPUT STRING WITH THE JSONVALIDATOR.VALIDATE METHOD. MALFORMED JSON INPUT CAN CAUSE THE APPLICATION TO CRASH OR CAN CAUSE INCORRECT CONFIGURATION VALUES.

The non-STE example below describes an encryption library but buries the safety condition in the middle of the text. The STE-Code example gives the condition first so the developer knows the prerequisite before reading the command.

> **Non-STE:** WARNING: USE THE ENCRYPTDATA FUNCTION ONLY WHEN YOU HAVE INITIALIZED THE CRYPTOPROVIDER WITH A VALID KEY, OTHERWISE THE DATA WILL BE ENCRYPTED WITH A DEFAULT KEY THAT IS NOT SECURE.

> **STE-Code:** WARNING: THE CRYPTOPROVIDER MUST BE INITIALIZED WITH A VALID 256-BIT ENCRYPTION KEY. IF THE CRYPTOPROVIDER IS NOT INITIALIZED WITH A VALID KEY, THE ENCRYPTDATA FUNCTION USES A DEFAULT KEY. THE DEFAULT KEY IS NOT SECURE AND AN ATTACKER CAN DECRYPT THE DATA.
