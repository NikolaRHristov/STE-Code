# Rule 7.1 — Use an Applicable Word (for Example, "Warning" or "Caution") to Identify the Level of Risk

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.1

> **Source:** [master.md#sec7-rule7.1](ste-code/grouped/)

## Original Rule

**Rule 7.1** Use a word (for example, "warning" or "caution") or, when applicable, a symbol, to immediately show your reader the level of the related risk.

- If there is a risk of injury or death, use a "warning."
- If there is a risk of damage to machines, tools, or equipment, use a "caution."
- If there are the two levels of risk together, use a "warning."

In the non-STE example that follows, the safety instruction is a caution. But if you know about oxygen systems, you also know that oxygen mixed with other materials can cause explosions. Because there is a risk of injury or death here, you must identify this safety instruction as a warning.

Compare the wording in the two safety instructions. The non-STE safety instruction is an abstract sentence and only makes a general statement. The warning in STE gives clear and correct information about how to decrease the risk of explosion. The warning contains the words "explosion," "injury," and "death" to make the reader clearly understand how important this safety instruction is.

**Spec example:**

> **Non-STE:** CAUTION: EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE.
>
> **STE:** WARNING: BEFORE YOU FILL THE LIQUID OXYGEN SYSTEM, PUT ON A FACE MASK AND PROTECTIVE CLOTHING. LIQUID OXYGEN CAN CAUSE IRRITATION OF THE RESPIRATORY TRACT AND EYE IRRITATION.

## STE-Code Adaptation

**Rule 7.1** In code documentation, use a signal word (for example, "WARNING" or "CAUTION") to immediately show your reader the level of the related risk.

- If there is a risk of security vulnerabilities, data loss, or system corruption, use a "WARNING."
- If there is a risk of unexpected behavior, performance degradation, or incorrect results, use a "CAUTION."
- If there are the two levels of risk together, use a "WARNING."

Severity mapping: This rule teaches the WARNING and CAUTION safety signal words for code documentation. For release-note and changelog severity, map the same levels as follows: WARNING to BREAKING, CAUTION to DEPRECATED, NOTE to NOTE.

In the non-STE example that follows, the safety instruction is a caution. But if you know about data validation in software systems, you also know that unvalidated input can cause security breaches and data loss. Because there is a risk of security vulnerabilities and data loss here, you must identify this safety instruction as a warning.

Compare the wording in the two code-documentation safety instructions. The non-STE safety instruction is an abstract statement and only makes a general claim. The warning in STE-Code gives clear and correct information about how to decrease the risk of security breaches. The warning contains the words "security breach" and "data loss" to make the reader clearly understand how important this safety instruction is.

### Examples

> **Non-STE:** CAUTION: ALWAYS VALIDATE INPUT DATA.
>
> **STE:** WARNING: BEFORE YOU PROCESS INPUT DATA, MAKE SURE THAT YOU SANITIZE AND VALIDATE THE DATA. UNSANITIZED INPUT CAN CAUSE SECURITY BREACHES AND DATA LOSS.
>
> *Adapted from the spec pair shown in the Original Rule above: an abstract caution about cleanliness is escalated to a specific warning when the true risk level (injury or death) is higher. The code-domain pair below applies the same escalation. A vague caution about input becomes a warning that names the security breach and data loss risk.*

> **Non-STE:** CAUTION: THE CONFIGURATION FILE MAY CONTAIN OUTDATED SETTINGS.
>
> **STE:** CAUTION: BEFORE YOU DEPLOY THE APPLICATION, COMPARE THE CONFIGURATION FILE AGAINST THE REFERENCE CONFIGURATION. OUTDATED SETTINGS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *Code-domain CAUTION example — risk of unexpected behavior and incorrect results, not security or data loss.*

> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition

---

## Code-Domain Explanation

This rule applies to all code documentation types. Each type has a different level of exposure to security risks, data loss, and unexpected behavior. Use the correct signal word for the risk level. Do not let the signal word become routine noise.

### README Files

README files are the first document a user reads. Use WARNING for security-critical setup steps. Use CAUTION for configuration steps that can cause incorrect behavior. Place signal words at the top of the relevant section. Do not bury them in a paragraph.

**WARNING in a README setup section:**

> **Non-STE:** Note: you should be careful with the API key and not commit it to version control.
>
> **STE:** WARNING: DO NOT COMMIT THE API KEY TO VERSION CONTROL. AN EXPOSED API KEY CAN CAUSE UNAUTHORIZED ACCESS AND DATA LOSS.
>
> *Principles applied: P1, P2 — "warning" for security risk, imperative command, specific consequence*

**CAUTION in a README configuration section:**

> **Non-STE:** Make sure the port number does not conflict with other services or the app won't start.
>
> **STE:** CAUTION: BEFORE YOU START THE APPLICATION, CHECK THAT THE PORT NUMBER DOES NOT CONFLICT WITH OTHER SERVICES. A PORT CONFLICT CAN CAUSE THE APPLICATION TO FAIL.
>
> *Principles applied: P9, P11 — clear signal word, specific condition, specific consequence*

### API Documentation

API documentation describes functions that external callers use. Use WARNING for endpoints that handle sensitive data, authentication, or destructive operations. Use CAUTION for endpoints that have side effects or rate limits.

**WARNING for a destructive API endpoint:**

> **Non-STE:** DELETE /users/:id removes the user and all associated data, this cannot be undone.
>
> **STE:** WARNING: DELETE /users/:id REMOVES THE USER AND ALL RELATED DATA PERMANENTLY. THIS OPERATION CANNOT BE UNDONE. VERIFY THE USER ID BEFORE YOU SEND THE REQUEST.
>
> *Principles applied: P1, P5 — warning for irreversible data loss, technical noun preserved in backticks, specific pre-action instruction*

**CAUTION for a rate-limited endpoint:**

> **Non-STE:** This endpoint allows 100 requests per minute, exceeding this will return 429 errors.
>
> **STE:** CAUTION: THE ENDPOINT ALLOWS A MAXIMUM OF 100 REQUESTS PER MINUTE. IF YOU EXCEED THE LIMIT, THE ENDPOINT RETURNS A 429 ERROR. MONITOR THE `X-RateLimit-Remaining` HEADER.
>
> *Principles applied: P1, P12 — caution for incorrect results (429 errors), technical verb "monitor" is allowed*

### Docstrings and Inline Comments

Docstrings describe function contracts. Use WARNING in docstrings when a function can cause security vulnerabilities or data corruption if used incorrectly. Use CAUTION when a function has performance pitfalls or non-obvious side effects.

**WARNING in a Python docstring:**

```python
def execute_sql(query: str, params: tuple = ()) -> list:
    """Run a raw SQL query.

    WARNING: THIS FUNCTION EXECUTES THE QUERY DIRECTLY. SANITIZE ALL
    USER INPUT BEFORE YOU PASS IT TO THIS FUNCTION. UNSANITIZED INPUT
    CAN CAUSE SQL INJECTION ATTACKS AND DATA LOSS.

    Parameters:
        query: The raw SQL query string.
        params: The query parameters. The default is an empty tuple.

    Returns:
        A list of result rows.
    """
```

*Principles applied: P1, P7 — warning for security risk, "sanitize" used as a verb, specific consequence named*

**CAUTION in a JavaScript JSDoc comment:**

```javascript
/**
 * Caches the result of an expensive computation.
 *
 * CAUTION: THE CACHE USES MEMORY PROPORTIONAL TO THE NUMBER OF
 * UNIQUE ARGUMENTS. FOR UNBOUNDED INPUT SETS, USE A CACHE WITH
 * A SIZE LIMIT. AN UNLIMITED CACHE CAN CAUSE MEMORY EXHAUSTION.
 *
 * @param {Function} fn - The function to cache.
 * @returns {Function} A cached version of the function.
 */
function memoize(fn) { /* ... */ }
```

*Principles applied: P1, P13 — caution for performance degradation (memory exhaustion), "cache" used as noun not verb*

### Commit Messages

Commit messages can use WARNING or CAUTION as the commit type prefix. Use `WARNING:` for commits that fix security vulnerabilities or prevent data loss. Use `CAUTION:` for commits that change behavior in a way that downstream consumers must know about. This convention helps automated changelog tools group commits by severity.

> **Non-STE:** fix: patch SQL injection in login form
>
> **STE:** WARNING: Prevent SQL injection in the login form. The previous code did not sanitize the `username` parameter. This vulnerability could permit unauthorized database access.
>
> *Principles applied: P1, P14 — warning for security breach risk, American English spelling*

> **Non-STE:** change: update default timeout from 30s to 10s
>
> **STE:** CAUTION: Change the default timeout from 30 seconds to 10 seconds. Update all callers that rely on the previous default. The shorter timeout can cause connection failures in high-latency environments.
>
> *Principles applied: P1 — caution for unexpected behavior, specific instruction for callers*

### Error Messages

Error messages are read during incidents. Use WARNING in error messages when the system detects a condition that can lead to security compromise or data corruption. Use CAUTION when the system detects a condition that can lead to incorrect results. Error messages must be actionable.

**WARNING in an error message:**

> **Non-STE:** Error: invalid signature
>
> **STE:** WARNING: THE REQUEST SIGNATURE IS NOT VALID. THE REQUEST MAY HAVE BEEN TAMPERED WITH. REJECT THE REQUEST. CHECK YOUR SIGNING KEY AND ALGORITHM.
>
> *Principles applied: P1, P9 — warning for security risk, short clear sentences, actionable instruction*

**CAUTION in an error message:**

> **Non-STE:** The configuration value for max_connections must be less than database pool size.
>
> **STE:** CAUTION: THE `max_connections` VALUE IS GREATER THAN THE `pool_size` VALUE. THIS CONFIGURATION CAN CAUSE CONNECTION FAILURES. SET `max_connections` TO A VALUE THAT IS NOT MORE THAN `pool_size`.
>
> *Principles applied: P1, P11 — caution for incorrect results, one term per concept, actionable correction*

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation describes class contracts, inheritance hierarchies, and mutable state. Use WARNING when a subclass override can break a security invariant. Use CAUTION when a method mutates shared state.

**WARNING for a security-sensitive override (Java):**

> **Non-STE:** Subclasses should be careful to call super.validate() before performing custom validation.
>
> **STE:** WARNING: OVERRIDE THE `validate` METHOD WITH CARE. CALL `super.validate()` BEFORE YOU ADD CUSTOM VALIDATION LOGIC. IF YOU SKIP THE BASE VALIDATION, UNTRUSTED DATA CAN BYPASS SECURITY CHECKS.
>
> *Principles applied: P1, P7 — warning for security risk, "call" used as imperative verb, specific consequence*

**CAUTION for mutable shared state (C++):**

> **Non-STE:** Note that this method modifies the internal cache which may affect other threads.
>
> **STE:** CAUTION: THE `invalidateCache` METHOD MODIFIES THE INTERNAL CACHE. THIS CHANGE AFFECTS ALL THREADS THAT USE THE CACHE. USE A LOCK BEFORE YOU CALL THIS METHOD.
>
> *Principles applied: P1, P5 — caution for unexpected behavior in concurrent contexts, technical noun "thread" allowed, specific guard instruction*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, effect types, and immutable data. Use WARNING when an unsafe escape hatch breaks referential transparency. Use CAUTION when a lazy operation can cause space leaks.

**WARNING for unsafe escape hatches (Haskell):**

> **Non-STE:** Use unsafePerformIO with caution as it breaks purity.
>
> **STE:** WARNING: `unsafePerformIO` BYPASSES THE IO TYPE SYSTEM. THIS FUNCTION HIDES SIDE EFFECTS IN PURE CODE. INCORRECT USE CAN CAUSE NONDETERMINISTIC BEHAVIOR AND DATA CORRUPTION. USE THIS FUNCTION ONLY WHEN NO SAFE ALTERNATIVE EXISTS.
>
> *Principles applied: P1, P8 — warning for data corruption risk, standard technical noun preserved, clear prohibition*

**CAUTION for space leaks (Haskell):**

> **Non-STE:** foldl is strict, but if you accumulate large thunks you might run out of memory.
>
> **STE:** CAUTION: `foldl` ACCUMULATES UNEVALUATED EXPRESSIONS (THUNKS). A LARGE ACCUMULATOR CAN CAUSE A SPACE LEAK AND MEMORY EXHAUSTION. USE `foldl'` FOR STRICT ACCUMULATION.
>
> *Principles applied: P1, P9 — caution for performance degradation, alternative provided, short clear sentences*

### Procedural (C, Go, Bash)

Procedural documentation describes memory management, buffer handling, and system calls. Use WARNING for buffer overflows, use-after-free, and undefined behavior. Use CAUTION for platform-specific behavior or resource limits.

**WARNING for buffer overflow (C):**

> **Non-STE:** Make sure the destination buffer is at least as large as the source string when using strcpy.
>
> **STE:** WARNING: `strcpy` DOES NOT CHECK THE SIZE OF THE DESTINATION BUFFER. IF THE SOURCE STRING IS LARGER THAN THE DESTINATION BUFFER, THE FUNCTION WRITES PAST THE BUFFER BOUNDARY. THIS BUFFER OVERFLOW CAN CAUSE SECURITY VULNERABILITIES AND SYSTEM CRASHES. USE `strncpy` WITH A SIZE LIMIT.
>
> *Principles applied: P1, P8 — warning for security risk and system corruption, standard technical noun, alternative provided*

**CAUTION for platform-specific behavior (Go):**

> **Non-STE:** On Windows, filepath separator is backslash, be careful with cross-platform paths.
>
> **STE:** CAUTION: THE `filepath` PACKAGE USES THE OPERATING SYSTEM PATH SEPARATOR. ON WINDOWS, THE SEPARATOR IS `\\`. ON UNIX, THE SEPARATOR IS `/`. USE `filepath.Join` OR `filepath.FromSlash` TO BUILD CROSS-PLATFORM PATHS. HARDCODED SEPARATORS CAUSE INCORRECT PATHS.
>
> *Principles applied: P1, P11 — caution for incorrect results, one term per concept, specific code examples*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, resource specifications, and destructive operations. Use WARNING for operations that destroy data or expose resources publicly. Use CAUTION for configuration values that have subtle effects on behavior.

**WARNING for destructive SQL operations:**

> **Non-STE:** Caution: this migration drops the users table.
>
> **STE:** WARNING: THIS MIGRATION DROPS THE `users` TABLE. ALL USER DATA IS DELETED PERMANENTLY. BACK UP THE DATABASE BEFORE YOU RUN THIS MIGRATION. VERIFY THAT YOU RUN THE MIGRATION AGAINST THE CORRECT DATABASE.
>
> *Principles applied: P1, P5 — warning for irreversible data loss, technical noun in backticks, multiple pre-action checks*

**CAUTION for Terraform resource recreation:**

> **Non-STE:** Changing the subnet_id will cause the EC2 instance to be recreated, which may cause downtime.
>
> **STE:** CAUTION: IF YOU CHANGE THE `subnet_id` ARGUMENT, TERRAFORM DESTROYS THE EXISTING EC2 INSTANCE AND CREATES A NEW ONE. THIS RECREATION CAUSES DOWNTIME. THE INSTANCE PUBLIC IP ADDRESS CHANGES. PLAN THE CHANGE DURING A MAINTENANCE WINDOW.
>
> *Principles applied: P1, P12 — caution for unexpected behavior and downtime, "plan" used as approved verb, specific consequences listed*

**WARNING for public Kubernetes exposure:**

> **Non-STE:** Be careful with LoadBalancer type services as they expose your app to the internet.
>
> **STE:** WARNING: A SERVICE OF TYPE `LoadBalancer` EXPOSES THE APPLICATION TO THE PUBLIC INTERNET. UNAUTHORIZED USERS CAN SEND REQUESTS TO THE APPLICATION. MAKE SURE THAT AUTHENTICATION AND NETWORK POLICIES ARE IN PLACE BEFORE YOU APPLY THIS CONFIGURATION.
>
> *Principles applied: P1, P7 — warning for security risk, "apply" used as imperative verb, specific pre-condition check*

### Systems (Rust Ownership, C Memory)

Systems documentation describes ownership, unsafe blocks, and memory layout. Use WARNING for undefined behavior, data races, and memory corruption. Use CAUTION for performance characteristics of unsafe optimizations.

**WARNING for undefined behavior (Rust):**

> **Non-STE:** Dereferencing a raw pointer is unsafe and may cause undefined behavior if the pointer is invalid.
>
> **STE:** WARNING: DEREFERENCING A RAW POINTER CAN CAUSE UNDEFINED BEHAVIOR. UNDEFINED BEHAVIOR CAN CORRUPT MEMORY, CAUSE SECURITY VULNERABILITIES, AND CRASH THE PROGRAM. BEFORE YOU DEREFERENCE A RAW POINTER, CHECK THAT: (1) THE POINTER IS NOT NULL. (2) THE POINTER IS CORRECTLY ALIGNED. (3) THE POINTER POINTS TO VALID, INITIALIZED MEMORY.
>
> *Principles applied: P1, P4 — warning for system corruption and security, vertical list for preconditions, explicit checklist*

**CAUTION for unsafe optimization tradeoffs:**

> **Non-STE:** Using MaybeUninit can improve performance but be careful about initialization.
>
> **STE:** CAUTION: `MaybeUninit` SKIPS INITIALIZATION TO IMPROVE PERFORMANCE. IF YOU READ UNINITIALIZED MEMORY, THE PROGRAM BEHAVIOR IS UNDEFINED. MAKE SURE THAT YOU INITIALIZE THE VALUE BEFORE YOU READ IT. MEASURE THE PERFORMANCE GAIN BEFORE YOU USE THIS TYPE.
>
> *Principles applied: P1, P9 — caution for incorrect results (undefined behavior is also a WARNING-level risk, but the primary risk here is the subtlety of the contract), specific guard instruction*

---

## Extended Examples

### Example 1 — Misclassified Risk Level in API Key Documentation

> **Non-STE:** CAUTION: Store the API key in an environment variable.
>
> **STE:** WARNING: STORE THE API KEY IN AN ENVIRONMENT VARIABLE. DO NOT HARDCODE THE API KEY IN THE SOURCE CODE. AN EXPOSED API KEY CAN CAUSE UNAUTHORIZED ACCESS, DATA THEFT, AND SERVICE ABUSE. ADD THE `.env` FILE TO `.gitignore`.
>
> *Principles applied: P1 — the original used CAUTION for a security risk (exposed credentials). Escalated to WARNING. Specific consequences named. Actionable prevention steps.*

### Example 2 — Missing Consequence in Database Migration Documentation

> **Non-STE:** WARNING: Run this migration carefully.
>
> **STE:** WARNING: BEFORE YOU RUN THIS MIGRATION, BACK UP THE `transactions` TABLE. THE MIGRATION REMOVES ALL RECORDS OLDER THAN 90 DAYS. THE DATA CANNOT BE RECOVERED AFTER THE MIGRATION COMPLETES. VERIFY THE DATE THRESHOLD AGAINST YOUR RETENTION POLICY.
>
> *Principles applied: P1, P9 — the original warning has no specific consequence and no actionable instruction. The STE version names the consequence (irrecoverable data loss), gives a pre-action check, and links to a policy reference.*

### Example 3 — Abstract Caution in a Library README

> **Non-STE:** CAUTION: Be mindful of thread safety when using this library.
>
> **STE:** CAUTION: THE `Cache` CLASS IS NOT THREAD-SAFE. IF YOU SHARE A `Cache` INSTANCE ACROSS THREADS, RACE CONDITIONS CAN CAUSE INCORRECT CACHE ENTRIES AND APPLICATION CRASHES. USE `ConcurrentCache` FOR MULTI-THREADED APPLICATIONS. USE A MUTEX FOR MANUAL SYNCHRONIZATION.
>
> *Principles applied: P1, P8 — the original caution is abstract and does not give a specific risk or a fix. The STE version names the class, explains the risk, and gives two alternatives.*

### Example 4 — Wrong Signal Word for Performance Degradation

> **Non-STE:** WARNING: This function is slow for large inputs.
>
> **STE:** CAUTION: THIS FUNCTION HAS O(N²) TIME COMPLEXITY. FOR INPUTS LARGER THAN 10,000 ITEMS, THE FUNCTION CAN TAKE SEVERAL MINUTES TO COMPLETE. USE `fastSort` FOR LARGE INPUTS. `fastSort` HAS O(N LOG N) TIME COMPLEXITY.
>
> *Principles applied: P1, P9 — performance degradation is a CAUTION-level risk, not a WARNING. The original used WARNING incorrectly. The STE version downgrades to CAUTION, explains the complexity, gives a threshold, and provides an alternative.*

### Example 5 — Missing Signal Word in Environment Variable Documentation

> **Non-STE:** The DEBUG_MODE environment variable controls verbose logging. Setting it to true in production will leak sensitive information.
>
> **STE:** WARNING: DO NOT SET `DEBUG_MODE=true` IN A PRODUCTION ENVIRONMENT. DEBUG MODE WRITES SENSITIVE DATA TO THE LOG OUTPUT. THIS DATA INCLUDES REQUEST BODIES, AUTHENTICATION TOKENS, AND DATABASE QUERIES. AN ATTACKER WITH LOG ACCESS CAN STEAL USER CREDENTIALS.
>
> *Principles applied: P1 — the original has no signal word at all. The risk (data leak, credential theft) is a security vulnerability. A WARNING is required. The STE version adds the signal word, explains the data at risk, and names the attacker threat.*

### Example 6 — Mixed Risk Levels in a Single Callout

> **Non-STE:** CAUTION: The reset method clears the database and disables authentication, only use in development.
>
> **STE:** WARNING: THE `reset` METHOD CLEARS THE DATABASE AND DISABLES AUTHENTICATION. IF YOU CALL THIS METHOD IN A PRODUCTION ENVIRONMENT, ALL USER DATA IS DELETED AND ALL REQUESTS BYPASS AUTHENTICATION. THIS METHOD IS FOR DEVELOPMENT USE ONLY. CHECK THE `NODE_ENV` VARIABLE BEFORE YOU CALL THIS METHOD.
>
> *Principles applied: P1 — the original has two risks together: data loss (WARNING level) and disabled auth (WARNING level). When two WARNING-level risks exist together, use WARNING. The original used CAUTION incorrectly. The STE version escalates to WARNING, names both consequences, and adds an environment check.*

---

## Edge Cases

### Edge Case 1 — When a Framework or Language Feature Uses "Warning" as a Name

Some programming languages and frameworks use "Warning" as a type or module name (for example, Python's `warnings` module, Rust's `#[allow(warnings)]`, JavaScript's `console.warn()`). When the word "Warning" appears as a technical code noun, put it in backticks. When it appears as a risk signal word, use uppercase WARNING without backticks.

> **Non-STE:** Warning: the warnings module suppresses warnings by default.
>
> **STE:** CAUTION: THE `warnings` MODULE SUPPRESSES WARNINGS BY DEFAULT. THE OUTPUT FROM `warn()` CALLS IS NOT SHOWN. CALL `warnings.simplefilter('always')` TO SHOW ALL WARNINGS.
>
> *The risk is unexpected behavior (suppressed output), so CAUTION is the correct signal word. The `warnings` module name is in backticks. The signal word WARNING is not used here because that would conflict with the module name and cause confusion.*

### Edge Case 2 — When a Third-Party Library Uses a Different Risk Convention

Third-party libraries may use their own signal word conventions (for example, `DANGER`, `CRITICAL`, `IMPORTANT`, `NOTE`). When you document a third-party API in your project, translate their convention to STE-Code signal words. Do not replicate the third-party convention directly.

> **Third-party convention:** DANGER: This operation is irreversible.
>
> **STE-Code translation:** WARNING: THIS OPERATION IS IRREVERSIBLE. THE DATA CANNOT BE RECOVERED AFTER THE OPERATION COMPLETES. BACK UP THE DATA BEFORE YOU START.
>
> *The third party uses DANGER. STE-Code uses WARNING for irreversible data loss. Translate the signal word and add the specific consequence and pre-action instruction.*

### Edge Case 3 — Generated Code with Auto-Inserted Warnings

Generated code (from tools such as `protoc`, `graphql-codegen`, or OpenAPI generators) may insert WARNING or CAUTION comments automatically. These generated comments are not under your control. For generated code:

- Do not modify the generated comments. The generator may overwrite your changes.
- Add your own STE-Code WARNING or CAUTION in the documentation that wraps the generated code.
- If the generated warning misclassifies the risk level, open an issue with the generator project.

> **Generated (leave as-is):** // CAUTION: This method is deprecated.
>
> **Your wrapper documentation:** WARNING: THE `legacy/client.go` FILE CONTAINS DEPRECATED METHODS. DEPRECATED METHODS MAY BE REMOVED IN A FUTURE VERSION. THE REMOVAL OF THESE METHODS CAN BREAK YOUR APPLICATION. MIGRATE TO THE `v2/client.go` API.
>
> *The generated comment remains. Your documentation adds the correct signal word (WARNING, because removal of used methods is a BREAKING risk).*

### Edge Case 4 — When a BREAKING Change Overlaps with a WARNING

BREAKING changes and WARNING-level risks often occur together. When a breaking change also introduces a security risk or data loss risk, use WARNING and mention the breaking nature in the body. Do not use two signal words.

> **Non-STE:** BREAKING: WARNING: The encrypt function now requires a key parameter.
>
> **STE:** WARNING: THE `encrypt` FUNCTION NOW REQUIRES A `key` PARAMETER. THIS IS A BREAKING CHANGE. UPDATE ALL CALLERS TO PASS A KEY ARGUMENT. IF YOU DO NOT PASS A KEY, THE FUNCTION THROWS AN ERROR AND THE DATA IS NOT ENCRYPTED.
>
> *WARNING is used because unencrypted data is a security risk. The breaking nature is mentioned in the body, not as a competing signal word. The consequence of ignoring the warning is stated explicitly.*

### Edge Case 5 — Internationalization of Warning and Caution Strings

When your documentation is translated to other languages, the signal words WARNING and CAUTION must also be translated. Use the standard translation for these words in each target language. Do not invent new signal words per language. Maintain a glossary of translated signal words.

The signal word must remain visually distinct. Use the same formatting rules across all languages:

- Uppercase letters for the signal word.
- A colon (:) after the signal word.
- A space before the instruction text.

**STE-Code signal word glossary (example):**

| Language | WARNING | CAUTION |
|----------|---------|---------|
| English | WARNING | CAUTION |
| Spanish | ADVERTENCIA | PRECAUCIÓN |
| French | AVERTISSEMENT | ATTENTION |
| German | WARNUNG | VORSICHT |
| Japanese | 警告 | 注意 |

*For each new language, add the translation to the glossary. Use the same signal word consistently across all documentation in that language.*

---

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary. "Warning" and "caution" are approved signal words. Do not invent new signal words.
- **Rule 1.4** — Use only approved verb forms and adjective forms. A safety instruction must start with an approved verb (for example, "check," "make sure," "do not").
- **Rule 1.6** — Non-approved words are not permitted. Do not use non-approved words inside a WARNING or CAUTION instruction.
- **Rule 1.10** — No slang, jargon, or regional terms. Use standard signal words. Do not use slang signal words (for example, "heads up," "watch out").
- **Rule 1.11** — One term per concept. Use WARNING and CAUTION consistently across all documentation. Do not mix signal word conventions from different sources.
- **Rule 4.1** — Write short and clear sentences. Each WARNING or CAUTION instruction must be a short, clear imperative sentence.
- **Rule 4.2** — Use the active voice. Safety instructions must use the active voice to give clear commands.
- **Rule 5.3** — Use the imperative (command) form for instructions. A WARNING or CAUTION is a safety instruction. The body must use the imperative mood.
- **Rule 5.4** — Write each step as a command. Each action inside a WARNING or CAUTION is a step. Write each step as a command.
- **Rule 7.2** — Start a safety instruction with a clear and accurate command or condition. The sentence that follows the signal word must give a clear command or state a clear condition.
- **Rule 7.3** — Give a clear consequence in the safety instruction. The consequence must use the words that name the risk level (for example, "security breach," "data loss," "unexpected behavior").
- **Section 1 (Vocabulary)** — All words used in WARNING and CAUTION instructions must come from the approved vocabulary unless they are technical code nouns.
- **Section 5 (Procedural Writing)** — WARNING and CAUTION instructions are procedural. Follow all procedural writing rules.

---

## Grammar Notes

### Signal Word Placement

The signal word (WARNING or CAUTION) must be the first word of the safety instruction. Put the signal word at the start of the line. Do not indent the signal word. Do not put text before the signal word.

> **Correct placement:** WARNING: DO NOT SHARE THE PRIVATE KEY.
>
> **Incorrect placement:** Important: WARNING: DO NOT SHARE THE PRIVATE KEY.

The signal word is followed by a colon (:) and a single space. The instruction text starts after the space. The colon is part of the signal word format, not part of the instruction sentence.

### Uppercase Convention

Write the signal word in uppercase letters. This convention makes the signal word visually distinct from the body text. The uppercase is part of the signal, not emphasis. Do not write the signal word in lowercase or title case.

> **Correct:** WARNING: The operation is destructive.
> **Incorrect:** Warning: The operation is destructive.
> **Incorrect:** warning: The operation is destructive.

The instruction text after the signal word can use standard sentence case. The first word of the instruction is uppercase (as the start of a sentence). The rest of the instruction uses standard capitalization.

### Sentence Structure After the Signal Word

The sentence that follows the signal word must include three parts:

1. **A clear command or condition** — What the reader must do or must check.
2. **A clear consequence** — What happens if the reader ignores the instruction.
3. **A clear risk escalation** — How the consequence maps to the risk level (security, data loss, unexpected behavior).

These three parts can be in one sentence or across multiple sentences. The parts must appear in this order. The reader must understand the risk before acting.

> **Structure:** WARNING: [COMMAND/CONDITION]. [CONSEQUENCE]. [RISK ESCALATION].
>
> **Example:** WARNING: DO NOT COMMIT THE API KEY TO VERSION CONTROL. AN EXPOSED API KEY CAN CAUSE UNAUTHORIZED ACCESS AND DATA LOSS. ADD THE `.env` FILE TO `.gitignore`.

### Verb Form in WARNING and CAUTION Instructions

Use the imperative mood for the command part of the instruction. Use "do not" for prohibitions. Do not use "should," "must," or "needs to."

> **Correct (imperative):** CHECK THE INPUT DATA BEFORE YOU PROCESS IT.
> **Correct (prohibition):** DO NOT USE THIS FUNCTION IN PRODUCTION.
> **Incorrect:** You should check the input data before processing.
> **Incorrect:** The input data must be checked before processing.

For technical verbs that have specific meanings in the code domain (for example, "sanitize," "validate," "encrypt," "back up"), use them as verbs in the imperative mood. These are approved technical verbs under Rule 1.12.

### Risk Escalation Vocabulary

Use these approved nouns to describe the risk consequence in WARNING instructions:

- Security breach
- Data loss
- System corruption
- Unauthorized access
- Credential theft
- Data leak
- Privilege escalation

Use these approved nouns to describe the risk consequence in CAUTION instructions:

- Unexpected behavior
- Performance degradation
- Incorrect results
- Connection failure
- Memory exhaustion
- Application crash
- Configuration drift

Do not use vague nouns such as "problems," "issues," or "trouble." Name the specific risk.

### Visual Distinction

In rendered documentation (HTML, PDF, Markdown), the signal word must be visually distinct. Use bold formatting, color, or a border to make the signal word stand out. Do not rely only on the uppercase text. Some readers scan visually. The formatting must catch the eye before the text is read.

```
> **WARNING:** Do not expose the private key. An exposed key can cause unauthorized access.
```

*In Markdown, use a blockquote with bold formatting for the signal word. In HTML, use a `<div>` with a CSS class. In reStructuredText, use an admonition directive (`.. WARNING::`). Choose the format that your documentation generator supports.*

---

## Summary Checklist

Before you publish code documentation that contains WARNING or CAUTION instructions, check each safety instruction:

- [ ] The signal word (WARNING or CAUTION) is correct for the risk level.
- [ ] Security, data loss, or system corruption risks use WARNING.
- [ ] Unexpected behavior, performance, or incorrect result risks use CAUTION.
- [ ] Mixed risk levels with one WARNING-level risk use WARNING.
- [ ] The signal word is the first word of the instruction.
- [ ] The signal word is in uppercase.
- [ ] The signal word is followed by a colon and a space.
- [ ] The instruction gives a clear command or condition.
- [ ] The instruction gives a clear consequence.
- [ ] The consequence names the specific risk (not "problems" or "issues").
- [ ] The instruction uses the imperative mood (not "you should").
- [ ] The instruction is not abstract. It gives concrete actions.
- [ ] Technical code nouns are in backticks.
- [ ] No non-approved words are used in the instruction.
- [ ] No competing signal words from third-party conventions are mixed in.
- [ ] The signal word is visually distinct from body text.
