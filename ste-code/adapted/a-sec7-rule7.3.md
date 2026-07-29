# Rule 7.3 — Give an Explanation to Show the Risk or Possible Result

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.3

## Original Rule

If it is possible, always tell your reader about the problems that can occur if the reader does not obey the safety instruction. If there is a clear and specified risk, the person who does the task will understand the risk and be more careful.

## STE-Code Adaptation

In code documentation, if it is possible, always tell the developer about the problems that can occur if the developer does not obey the safety instruction. If there is a clear and specified risk, the developer who uses the code will understand the risk and write safer integration code.

Give the explanation after the command or condition. The explanation must clearly state the risk or the possible result. Use precise technical terms for the risk (for example, "SQL injection attack," "buffer overflow," "race condition," "deadlock," "memory leak," or "unauthorized access"). Do not use vague or abstract terms such as "unexpected results" or "adverse effects" without describing what these results or effects are.

### Examples

In the non-STE example below, the safety instruction does not explain the risk. The developer does not know what "problems" can occur. The STE-Code example clearly states the risk.

> **Non-STE:** WARNING: DO NOT CALL THE DATABASECONNECTION.CLOSE METHOD DURING AN ACTIVE TRANSACTION. THIS CAN CAUSE PROBLEMS.

> **STE-Code:** WARNING: DO NOT CALL THE DATABASECONNECTION.CLOSE METHOD DURING AN ACTIVE TRANSACTION. IF YOU CLOSE THE CONNECTION DURING AN ACTIVE TRANSACTION, THE TRANSACTION ROLLS BACK AUTOMATICALLY. THIS CAN CAUSE DATA INCONSISTENCY AND DATA LOSS.

In the non-STE example below, the safety instruction uses an abstract term. The STE-Code example gives a specific explanation of the possible result.

> **Non-STE:** CAUTION: DO NOT SET THE CACHESERVICE.TIMEOUT VALUE TO ZERO. A ZERO TIMEOUT CAN CAUSE ADVERSE EFFECTS.

> **STE-Code:** CAUTION: DO NOT SET THE CACHESERVICE.TIMEOUT VALUE TO ZERO. A ZERO TIMEOUT VALUE DISABLES THE TIMEOUT MECHANISM. IF THE CACHE SERVER DOES NOT RESPOND, THE APPLICATION THREAD WAITS INDEFINITELY. THIS CAN CAUSE A DEADLOCK AND CAN MAKE THE APPLICATION STOP RESPONDING.

In the non-STE example below, the explanation is missing. The STE-Code example adds an explanation that tells the developer the specific risk and its result.

> **Non-STE:** WARNING: BEFORE YOU DEPLOY THE MIGRATION SCRIPT TO THE PRODUCTION DATABASE, RUN THE SCRIPT ON A STAGING ENVIRONMENT.

> **STE-Code:** WARNING: BEFORE YOU DEPLOY THE MIGRATION SCRIPT TO THE PRODUCTION DATABASE, RUN THE SCRIPT ON A STAGING ENVIRONMENT. THE MIGRATION SCRIPT CAN CHANGE THE DATABASE SCHEMA AND CAN DELETE DATA. IF THE SCRIPT HAS AN ERROR, THE PRODUCTION DATABASE CAN BECOME CORRUPT AND THE APPLICATION CAN STOP.
