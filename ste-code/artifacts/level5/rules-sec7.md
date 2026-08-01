<!-- a-sec7-rule7.1.md -->

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

> *Adapted from spec pair:* Non-STE: `CAUTION: EXTREME CLEANLINESS OF OXYGEN TUBES IS IMPERATIVE.`  |  STE: `WARNING: BEFORE YOU FILL THE LIQUID OXYGEN SYSTEM, PUT ON A FACE MASK AND PROTECTIVE CLOTHING. LIQUID OXYGEN CAN CAUSE IRRITATION OF THE RESPIRATORY TRACT AND EYE IRRITATION.` (ASD-STE100 Issue 9, Rule 7.1, page 99 — escalated from CAUTION to WARNING because the true risk is injury or death.)

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
function memoize(fn) {
  const cache = new Map();
  return function (...args) {
    const key = JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
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

```java
abstract class RequestValidator {
    /** Base security checks that apply to all request types. */
    void validate(Request request) {
        if (request.getUser() == null) {
            throw new SecurityException("Missing user context");
        }
        if (!request.isAuthenticated()) {
            throw new SecurityException("Request is not authenticated");
        }
    }
}

class PaymentRequestValidator extends RequestValidator {
    @Override
    void validate(Request request) {
        // WARNING: CALL super.validate() BEFORE YOU ADD CUSTOM LOGIC.
        super.validate();
        PaymentRequest payment = (PaymentRequest) request;
        if (payment.getAmount() <= 0) {
            throw new IllegalArgumentException("Amount must be greater than zero");
        }
    }
}
```

*The `PaymentRequestValidator.validate` method shows the correct override: it calls `super.validate()` first, so the base security checks (user context and authentication) still run. If a developer removes that call, an untrusted request can bypass the checks and reach the payment logic.*

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

---

<!-- a-sec7-rule7.2.md -->

# Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.2

> **Source:** [master.md#sec7-rule7.2](ste-code/grouped/)

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

Severity mapping: The command or condition in a safety instruction carries the severity from Rule 7.1. In release notes and changelogs, the same levels map as follows: WARNING to BREAKING, CAUTION to DEPRECATED, NOTE to NOTE.

### Examples

> *Adapted from spec pair:* Non-STE: `STORING API KEYS IN THE SOURCE CODE IS NOT RECOMMENDED.`  |  STE: `DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE ENVIRONMENT VARIABLES OR A SECRETS MANAGER TO STORE API KEYS. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.` (ASD-STE100 Issue 9, Rule 7.2, page 99–100 — the safety instruction starts with a clear command, not a description of the risk.)

> **Non-STE:** WARNING: STORING API KEYS IN THE SOURCE CODE IS NOT RECOMMENDED.

> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE ENVIRONMENT VARIABLES OR A SECRETS MANAGER TO STORE API KEYS. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.

> *Adapted from spec pair: "WARNING: DO NOT SWALLOW THE SOLVENT. ALWAYS MAKE SURE THAT YOU KNOW THE SAFETY PRECAUTIONS AND FIRST AID INSTRUCTIONS FOR SOLVENTS. SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH." — the safety instruction starts with a clear command ("DO NOT STORE") and explains the risk.*

Full runnable form — a Python module that reads credentials from the environment:

```python
import os

# WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE
# ENVIRONMENT VARIABLES OR A SECRETS MANAGER TO STORE API KEYS.
# API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND
# DATA BREACHES.
def get_api_client() -> "Client":
    api_key = os.environ.get("PAYMENT_API_KEY")
    if api_key is None:
        raise RuntimeError("PAYMENT_API_KEY is not set in the environment")
    return Client(api_key=api_key)
```

The non-STE version describes an attitude ("is not recommended"). The STE version starts with the command "DO NOT STORE", gives the required alternative, and names the consequence (data breaches).

> **Non-STE:** CAUTION: THE CODEBASE CONTAINS DEPRECATED FUNCTIONS.

> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS OR METHODS THAT HAVE KNOWN ISSUES. USE THE APPROVED REPLACEMENT FUNCTIONS SPECIFIED IN THE MIGRATION GUIDE. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.

> *Adapted from spec pair: "CAUTION: DO NOT USE BLEACH OR CLEANSERS THAT CONTAIN CHLORINE TO CLEAN THE UNIT. THESE CLEANING AGENTS CAN CAUSE CORROSION." — the safety instruction starts with a clear command ("DO NOT USE") and explains the risk.*

Full runnable form — a Python deprecation shim that warns and points to the replacement:

```python
import warnings

# CAUTION: DO NOT USE DEPRECATED FUNCTIONS OR METHODS THAT HAVE
# KNOWN ISSUES. USE THE APPROVED REPLACEMENT FUNCTIONS SPECIFIED
# IN THE MIGRATION GUIDE. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED
# BEHAVIOR AND INCORRECT RESULTS.
def legacy_send_email(address: str, body: str) -> None:
    warnings.warn(
        "legacy_send_email is deprecated; use send_message() instead",
        DeprecationWarning,
        stacklevel=2,
    )
    send_message(address, body)
```

The non-STE version only reports the presence of deprecated code. The STE version starts with the prohibition "DO NOT USE", names the replacement, and states the consequence (incorrect results).

> **Non-STE:** PERMANENT DATA LOSS CAN OCCUR.

> **STE:** IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.

> *Adapted from spec pair: "IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR." — the safety instruction starts with a clear condition ("IF YOU DO NOT SET...") before stating the risk.*

Full runnable form — a Go database client that requires a timeout:

```go
// WARNING: IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION
// CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.
func NewClient(dsn string) (*Client, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }
    // A zero value means "wait forever"; set a bound.
    db.SetConnMaxLifetime(0)
    db.SetMaxOpenConns(10)
    // Without a timeout the next call can block until the TCP
    // connection is silently dropped, and buffered writes are lost.
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    if err := db.PingContext(ctx); err != nil {
        return nil, err
    }
    return &Client{db: db}, nil
}
```

The non-STE version states only the consequence. The STE version starts with the condition "IF YOU DO NOT SET THE CONNECTION TIMEOUT" so the reader learns when the risk applies.

> **See also:** Rule 5.3 — Imperative (Command) Form for Instructions; Rule 5.4 — Descriptive Statement Before the Command; Rule 7.1 — Use an Applicable Word to Identify the Level of Risk

---

## Code-Domain Explanation

This rule defines the structure of every safety instruction in code documentation. A safety instruction has two parts: a signal word (WARNING or CAUTION, per Rule 7.1) and a body. The body must start with either a clear command or a clear condition. The reader must understand what action to take (or not take) within the first few words.

A safety instruction is complete only when it has all three of these parts:

1. **Signal word** — WARNING or CAUTION (Rule 7.1).
2. **Command or condition** — the first sentence after the colon. This tells the reader what to do, what not to do, or under what condition the risk applies.
3. **Consequence** — the explanation that shows the risk (Rule 7.3). This is what makes the command or condition "accurate": the reader understands why the instruction matters.

If you write the consequence but not the command, the instruction is not actionable. If you write the command but not the consequence, the reader does not know why the command matters. Both the command or condition and the consequence are required.

### Command-First Structure

A command-first safety instruction starts with an imperative verb. The most common command forms in code documentation are:

- **DO NOT [action]** — Prohibit a dangerous action. Example: "DO NOT COMMIT THE `.env` FILE."
- **ALWAYS [action]** — Require a mandatory action. Example: "ALWAYS SANITIZE THE INPUT BEFORE YOU PROCESS IT."
- **[imperative verb]** — Direct the reader to take a specific action (for example, "CHECK," "MAKE SURE," "BACK UP," "SANITIZE," "VALIDATE," "VERIFY").

The command must appear immediately after the signal word and colon. The reader must not read through background information before learning what to do. Use approved verbs: prefer "use," "check," "make," "get," "set," "send," "remove," "keep," "start," "stop," "show," "do" over "utilize," "leverage," "employ," "commence," "terminate," "initiate."

**Command-first WARNING — README file:**

> **Non-STE:** WARNING: It is important to consider that hardcoding database credentials in the configuration file can lead to serious security issues if the file is committed to version control.

> **STE:** WARNING: DO NOT HARDCODE DATABASE CREDENTIALS IN THE CONFIGURATION FILE. STORE CREDENTIALS IN A SECRETS MANAGER OR ENVIRONMENT VARIABLES. HARDCODED CREDENTIALS IN VERSION CONTROL CAN CAUSE UNAUTHORIZED DATABASE ACCESS.

> *Principles applied: P1, P9 — the command "DO NOT HARDCODE" starts the instruction. The reader knows the prohibition in the first three words.*

Full runnable form — a `.env.example` and a load step:

```bash
# .env.example  (copy to .env and fill in real values)
# WARNING: DO NOT HARDCODE DATABASE CREDENTIALS IN THE CONFIGURATION
# FILE. STORE CREDENTIALS IN A SECRETS MANAGER OR ENVIRONMENT VARIABLES.
# HARDCODED CREDENTIALS IN VERSION CONTROL CAN CAUSE UNAUTHORIZED
# DATABASE ACCESS.
DATABASE_URL=postgres://user:password@localhost:5432/app
```

```python
import os
# Reads DATABASE_URL from the environment, never from a committed file.
db = connect(os.environ["DATABASE_URL"])
```

**Command-first CAUTION — API documentation:**

> **Non-STE:** CAUTION: The `/search` endpoint returns results from a cache that is updated every 5 minutes, so recent changes may not be reflected immediately.

> **STE:** CAUTION: BEFORE YOU USE THE `/search` ENDPOINT, READ THE CACHE STALENESS NOTE. THE CACHE IS UPDATED EVERY 5 MINUTES. RECENT CHANGES ARE NOT VISIBLE UNTIL THE NEXT CACHE UPDATE. DO NOT USE THIS ENDPOINT FOR REAL-TIME DATA.

> *Principles applied: P1, P2 — the condition "BEFORE YOU USE" starts the instruction. The reader knows the prerequisite before the explanation.*

Full runnable form — an OpenAPI operation object:

```yaml
/search:
  get:
    summary: Search the catalog
    # CAUTION: BEFORE YOU USE THE `/search` ENDPOINT, READ THE CACHE
    # STALENESS NOTE. THE CACHE IS UPDATED EVERY 5 MINUTES. RECENT
    # CHANGES ARE NOT VISIBLE UNTIL THE NEXT CACHE UPDATE. DO NOT USE
    # THIS ENDPOINT FOR REAL-TIME DATA.
    description: >
      Results come from a cache that refreshes on a 5-minute interval.
      Do not poll this endpoint for live status; subscribe to the
      webhook stream instead.
    responses:
      '200':
        description: Cached search results
```

### Condition-First Structure

A condition-first safety instruction starts with a subordinate clause that describes the prerequisite the reader must know. The most common condition forms are:

- **IF [condition]...** — State the unsafe condition before the consequence. Example: "IF YOU DISABLE TLS, THE TRAFFIC IS IN CLEAR TEXT."
- **BEFORE YOU [action]...** — Require a pre-action check. Example: "BEFORE YOU RUN THE MIGRATION, BACK UP THE DATABASE."
- **WHEN [condition]...** — Describe a scenario that triggers the risk. Example: "WHEN THE QUEUE IS FULL, THE PUBLISH CALL BLOCKS."

The condition must come first. The consequence comes second. The reader must understand the context before learning the result. Use the active voice in the condition: "IF YOU DO NOT SET..." not "IF THE TIMEOUT IS NOT SET..."

**Condition-first WARNING — docstring:**

> **Non-STE:** WARNING: The database connection may not be initialized if you call this function before `connect()` has completed.

> **STE:** WARNING: IF YOU CALL THIS FUNCTION BEFORE `connect()` COMPLETES, THE DATABASE CONNECTION IS NOT INITIALIZED. THE FUNCTION RETURNS `null` AND YOUR APPLICATION CAN CRASH. CALL `connect()` AND WAIT FOR THE PROMISE BEFORE YOU USE THIS FUNCTION.

> *Principles applied: P1, P10 — the condition "IF YOU CALL THIS FUNCTION BEFORE" starts the instruction. The reader learns the prerequisite scenario first. The consequence follows.*

Full runnable form — a JavaScript class with an explicit precondition:

```javascript
class Repository {
  /**
   * WARNING: IF YOU CALL THIS FUNCTION BEFORE `connect()` COMPLETES,
   * THE DATABASE CONNECTION IS NOT INITIALIZED. THE FUNCTION RETURNS
   * `null` AND YOUR APPLICATION CAN CRASH. CALL `connect()` AND WAIT
   * FOR THE PROMISE BEFORE YOU USE THIS FUNCTION.
   *
   * @param {number} id
   * @returns {Promise<Row|null>}
   */
  async getById(id) {
    if (!this.db) return null; // connection not ready
    return this.db.query("SELECT * FROM rows WHERE id = $1", [id]);
  }

  async connect() {
    this.db = await createPool();
  }
}
```

**Condition-first CAUTION — commit message:**

> **Non-STE:** CAUTION: The CI pipeline will fail if the `NODE_ENV` variable is not set to `production` during the release build.

> **STE:** CAUTION: WHEN YOU RUN THE RELEASE BUILD, SET `NODE_ENV=production`. IF YOU DO NOT SET THIS VARIABLE, THE CI PIPELINE FAILS. THE DEPLOYMENT STOPS UNTIL THE VARIABLE IS SET.

> *Principles applied: P1, P12 — the condition "WHEN YOU RUN THE RELEASE BUILD" starts the instruction. The command follows. The consequence is explained.*

Full runnable form — a commit body that changelog tools can parse:

```text
CAUTION: Change the build to require NODE_ENV in the release job.

WHEN YOU RUN THE RELEASE BUILD, SET NODE_ENV=production. IF YOU DO
NOT SET THIS VARIABLE, THE CI PIPELINE FAILS. THE DEPLOYMENT STOPS
UNTIL THE VARIABLE IS SET.

- Add NODE_ENV=production to .github/workflows/release.yml
- Add a guard that fails fast when the variable is missing
```

### Documentation Type Differences

**README files:** Safety instructions in README files are read before the user sets up the project. Use command-first for prohibitions (for example, "DO NOT COMMIT"). Use condition-first for prerequisites (for example, "BEFORE YOU RUN THE BUILD").

**API documentation:** Safety instructions in API docs are read by external consumers. Use command-first for destructive operations. Use condition-first for preconditions that depend on application state.

**Docstrings:** Safety instructions in docstrings are read by developers who use the function. Use command-first for function contract violations. Use condition-first for argument preconditions that are not enforced by the type system.

**Commit messages:** Safety instructions in commit messages are read during code review and changelog generation. The command or condition must be the first sentence of the commit body after the signal word. Use command-first for behavioral changes. Use condition-first for conditional breakage.

**Error messages:** Safety instructions in error messages are read during incidents. Use command-first to tell the operator what to do. Use condition-first to explain the system state that caused the error.

**Error message with command-first:**

> **Non-STE:** WARNING: Rate limit exceeded, try again after the reset window.

> **STE:** WARNING: THE RATE LIMIT IS EXCEEDED. DO NOT SEND MORE REQUESTS UNTIL THE RESET WINDOW OPENS. SENDING MORE REQUESTS CAN CAUSE YOUR API KEY TO BE TEMPORARILY BLOCKED. CHECK THE `Retry-After` HEADER FOR THE RESET TIME.

> *Principles applied: P1, P9 — the command "DO NOT SEND MORE REQUESTS" tells the operator what to stop doing. The consequence of ignoring the command is stated.*

Full runnable form — a handler that returns an actionable error:

```python
from http import HTTPStatus

def handle_request(req):
    if rate_limiter.is_exceeded(req.api_key):
        # WARNING: THE RATE LIMIT IS EXCEEDED. DO NOT SEND MORE REQUESTS
        # UNTIL THE RESET WINDOW OPENS. SENDING MORE REQUESTS CAN CAUSE
        # YOUR API KEY TO BE TEMPORARILY BLOCKED. CHECK THE `Retry-After`
        # HEADER FOR THE RESET TIME.
        headers = {"Retry-After": str(rate_limiter.seconds_to_reset(req.api_key))}
        return HTTPStatus.TOO_MANY_REQUESTS, headers, b"rate limit exceeded"
    return process(req)
```

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation describes class invariants, method contracts, and inheritance rules. Use command-first for prohibitions on subclass overrides. Use condition-first when the state of the object affects the safety of a method call.

**Command-first WARNING for subclass override (Java):**

> **Non-STE:** WARNING: Subclasses of `Authenticator` need to ensure that the `authenticate` method always calls `super.authenticate()` first.

> **STE:** WARNING: DO NOT OVERRIDE THE `authenticate` METHOD WITHOUT CALLING `super.authenticate()` FIRST. IF YOU BYPASS THE BASE AUTHENTICATION, UNTRUSTED REQUESTS CAN ACCESS PROTECTED RESOURCES. ALWAYS PUT `super.authenticate()` AS THE FIRST LINE OF YOUR OVERRIDE.

> *Principles applied: P1, P7 — the command "DO NOT OVERRIDE..." starts the instruction. The prohibition is clear in the first sentence. The required action ("ALWAYS PUT...") follows.*

Full runnable form — a base class and a compliant subclass:

```java
abstract class Authenticator {
    // WARNING: DO NOT OVERRIDE THE `authenticate` METHOD WITHOUT
    // CALLING `super.authenticate()` FIRST. IF YOU BYPASS THE BASE
    // AUTHENTICATION, UNTRUSTED REQUESTS CAN ACCESS PROTECTED
    // RESOURCES. ALWAYS PUT `super.authenticate()` AS THE FIRST LINE
    // OF YOUR OVERRIDE.
    void authenticate(Request req) {
        if (!req.isSigned()) throw new SecurityException("missing signature");
    }
}

class TokenAuthenticator extends Authenticator {
    @Override
    void authenticate(Request req) {
        super.authenticate(); // required: keeps the base checks
        verifyToken(req.token());
    }
}
```

**Condition-first CAUTION for mutable state (Python):**

> **Non-STE:** CAUTION: The `logger` object is shared across modules, be careful about changing the log level at runtime.

> **STE:** CAUTION: BEFORE YOU CHANGE THE `logger.level` AT RUNTIME, CHECK THAT NO OTHER MODULE USES THE SAME LOGGER. IF ANOTHER MODULE EXPECTS A DIFFERENT LOG LEVEL, THE APPLICATION LOGS CAN BECOME INCOMPLETE. SET THE LOG LEVEL IN THE INITIALIZATION FUNCTION. DO NOT CHANGE IT DURING RUNTIME.

> *Principles applied: P1, P11 — the condition "BEFORE YOU CHANGE..." starts the instruction. The reader checks the precondition before acting.*

Full runnable form — a shared logger configured once at startup:

```python
import logging

logger = logging.getLogger("app")  # shared singleton

# CAUTION: BEFORE YOU CHANGE THE `logger.level` AT RUNTIME, CHECK THAT
# NO OTHER MODULE USES THE SAME LOGGER. IF ANOTHER MODULE EXPECTS A
# DIFFERENT LOG LEVEL, THE APPLICATION LOGS CAN BECOME INCOMPLETE.
# SET THE LOG LEVEL IN THE INITIALIZATION FUNCTION. DO NOT CHANGE IT
# DURING RUNTIME.
def configure_logging(level: int) -> None:
    logger.setLevel(level)  # called once, at startup only
```

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, effect types, and referential transparency. Use command-first when an unsafe function can break purity. Use condition-first when laziness or non-strict evaluation creates a hidden precondition.

**Command-first WARNING for unsafe code (Rust):**

> **Non-STE:** WARNING: `unsafe` blocks require the programmer to manually uphold invariants that the compiler does not check.

> **STE:** WARNING: DO NOT ADD AN `unsafe` BLOCK WITHOUT DOCUMENTING THE SAFETY INVARIANTS. AN `unsafe` BLOCK WITHOUT DOCUMENTED INVARIANTS CAN CAUSE UNDEFINED BEHAVIOR, MEMORY CORRUPTION, AND SECURITY VULNERABILITIES. WRITE A `// SAFETY:` COMMENT THAT LISTS EACH INVARIANT AND THE REASON IT HOLDS.

> *Principles applied: P1, P8 — the command "DO NOT ADD AN `unsafe` BLOCK WITHOUT..." starts the instruction. The required action ("WRITE A `// SAFETY:` COMMENT") follows.*

Full runnable form — a safe wrapper over an unsafe raw pointer read:

```rust
/// WARNING: DO NOT ADD AN `unsafe` BLOCK WITHOUT DOCUMENTING THE
/// SAFETY INVARIANTS. AN `unsafe` BLOCK WITHOUT DOCUMENTED
/// INVARIANTS CAN CAUSE UNDEFINED BEHAVIOR, MEMORY CORRUPTION, AND
/// SECURITY VULNERABILITIES. WRITE A `// SAFETY:` COMMENT THAT LISTS
/// EACH INVARIANT AND THE REASON IT HOLDS.
pub unsafe fn read_u32(ptr: *const u32) -> u32 {
    // SAFETY: `ptr` is non-null, 4-byte aligned, and points to
    // initialized memory for the lifetime of this call.
    ptr.read_unaligned()
}
```

**Condition-first CAUTION for lazy evaluation (Haskell):**

> **Non-STE:** CAUTION: Using `foldl` on infinite lists will not terminate.

> **STE:** CAUTION: IF YOU USE `foldl` ON AN INFINITE LIST, THE FUNCTION DOES NOT TERMINATE. THE PROGRAM HANGS INDEFINITELY. USE `foldr` FOR OPERATIONS THAT CAN SHORT-CIRCUIT ON LAZY LISTS. CHECK THAT YOUR LIST IS FINITE BEFORE YOU USE `foldl`.

> *Principles applied: P1, P3 — the condition "IF YOU USE `foldl` ON AN INFINITE LIST" starts the instruction. The consequence (hang) is explained.*

Full runnable form — a GHCi session that shows the difference:

```haskell
-- CAUTION: IF YOU USE `foldl` ON AN INFINITE LIST, THE FUNCTION DOES
-- NOT TERMINATE. THE PROGRAM HANGS INDEFINITELY. USE `foldr` FOR
-- OPERATIONS THAT CAN SHORT-CIRCUIT ON LAZY LISTS. CHECK THAT YOUR
-- LIST IS FINITE BEFORE YOU USE `foldl`.
import Data.List (foldl')

sumFinite :: Num a => [a] -> a
sumFinite = foldl' (+) 0   -- strict: safe on finite lists

-- This never returns; `foldl` builds a thunk chain:
-- sumInfinite = foldl (+) 0 [1..]
```

### Procedural (C, Go, Bash)

Procedural documentation describes memory management, buffer handling, and system calls. Use command-first for memory safety violations. Use condition-first when the program state determines whether a call is safe.

**Command-first WARNING for buffer handling (C):**

> **Non-STE:** WARNING: `gets` reads input without bounds checking and should never be used.

> **STE:** WARNING: DO NOT USE `gets()` IN ANY C PROGRAM. `gets()` READS INPUT WITHOUT BOUNDS CHECKING. A BUFFER OVERFLOW CAN CAUSE ARBITRARY CODE EXECUTION AND SYSTEM COMPROMISE. USE `fgets()` WITH A SIZE LIMIT.

> *Principles applied: P1, P8 — the command "DO NOT USE `gets()`" starts the instruction. The prohibition is absolute ("IN ANY C PROGRAM"). The consequence (arbitrary code execution) justifies the command.*

Full runnable form — a safe read replacement:

```c
/* WARNING: DO NOT USE `gets()` IN ANY C PROGRAM. `gets()` READS INPUT
 * WITHOUT BOUNDS CHECKING. A BUFFER OVERFLOW CAN CAUSE ARBITRARY CODE
 * EXECUTION AND SYSTEM COMPROMISE. USE `fgets()` WITH A SIZE LIMIT. */
char name[64];
if (fgets(name, sizeof(name), stdin) == NULL) {
    /* handle EOF or read error */
}
name[strcspn(name, "\n")] = '\0'; /* remove trailing newline */
```

**Condition-first CAUTION for file descriptors (Go):**

> **Non-STE:** CAUTION: Closing a file descriptor that has already been closed causes a panic.

> **STE:** CAUTION: BEFORE YOU CALL `file.Close()`, CHECK THAT THE FILE IS OPEN. IF YOU CLOSE A FILE THAT IS ALREADY CLOSED, THE PROGRAM PANICS. USE `defer file.Close()` IMMEDIATELY AFTER YOU OPEN THE FILE. THIS PATTERN PREVENTS DOUBLE-CLOSE ERRORS.

> *Principles applied: P1, P12 — the condition "BEFORE YOU CALL `file.Close()`" starts the instruction. The precondition check is stated first. The safe pattern follows.*

Full runnable form — the recommended `defer` pattern:

```go
// CAUTION: BEFORE YOU CALL `file.Close()`, CHECK THAT THE FILE IS
// OPEN. IF YOU CLOSE A FILE THAT IS ALREADY CLOSED, THE PROGRAM
// PANICS. USE `defer file.Close()` IMMEDIATELY AFTER YOU OPEN THE
// FILE. THIS PATTERN PREVENTS DOUBLE-CLOSE ERRORS.
f, err := os.Open("data.csv")
if err != nil {
    return err
}
defer f.Close() // single owner; no second Close() anywhere
```

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, resource specifications, and destructive operations. Use command-first for destructive state changes. Use condition-first when a configuration value depends on infrastructure state.

**Command-first WARNING for destructive SQL:**

> **Non-STE:** WARNING: This migration truncates the audit log table.

> **STE:** WARNING: DO NOT RUN THIS MIGRATION WITHOUT A FULL DATABASE BACKUP. THE MIGRATION TRUNCATES THE `audit_log` TABLE. ALL AUDIT RECORDS ARE DELETED PERMANENTLY. THE DATA CANNOT BE RECOVERED. RUN THE BACKUP COMMAND: `pg_dump audit_log > audit_log_backup.sql`. VERIFY THE BACKUP BEFORE YOU CONTINUE.

> *Principles applied: P1, P5 — the command "DO NOT RUN THIS MIGRATION WITHOUT A FULL DATABASE BACKUP" starts the instruction. The precondition command is stated first. The consequence clarifies why.*

Full runnable form — a migration file with a guard:

```sql
-- WARNING: DO NOT RUN THIS MIGRATION WITHOUT A FULL DATABASE BACKUP.
-- THE MIGRATION TRUNCATES THE `audit_log` TABLE. ALL AUDIT RECORDS ARE
-- DELETED PERMANENTLY. THE DATA CANNOT BE RECOVERED. RUN THE BACKUP
-- COMMAND: `pg_dump audit_log > audit_log_backup.sql`. VERIFY THE
-- BACKUP BEFORE YOU CONTINUE.
--
-- Safe pre-check: fail the migration if the table is unexpectedly large
-- and no backup marker exists.
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM backup_markers WHERE table_name = 'audit_log')
     AND (SELECT count(*) FROM audit_log) > 0
  THEN
    RAISE EXCEPTION 'audit_log backup missing; abort migration';
  END IF;
END $$;

TRUNCATE TABLE audit_log;
```

**Condition-first CAUTION for Kubernetes resource limits:**

> **Non-STE:** CAUTION: Setting resource limits too low causes OOMKilled errors.

> **STE:** CAUTION: IF YOU SET THE `memory.limits` VALUE TOO LOW, THE POD IS KILLED WITH AN OOMKILLED ERROR. THE APPLICATION RESTARTS. REQUESTS TO THE APPLICATION FAIL DURING THE RESTART. MONITOR THE ACTUAL MEMORY USAGE IN STAGING BEFORE YOU SET THE LIMIT IN PRODUCTION. USE A LIMIT THAT IS AT LEAST 50 PERCENT ABOVE THE AVERAGE USAGE.

> *Principles applied: P1, P11 — the condition "IF YOU SET THE `memory.limits` VALUE TOO LOW" starts the instruction. The cascade of consequences follows. The corrective action is specific.*

Full runnable form — a manifest with a measured limit:

```yaml
# CAUTION: IF YOU SET THE `memory.limits` VALUE TOO LOW, THE POD IS
# KILLED WITH AN OOMKILLED ERROR. THE APPLICATION RESTARTS. REQUESTS
# TO THE APPLICATION FAIL DURING THE RESTART. MONITOR THE ACTUAL
# MEMORY USAGE IN STAGING BEFORE YOU SET THE LIMIT IN PRODUCTION.
# USE A LIMIT THAT IS AT LEAST 50 PERCENT ABOVE THE AVERAGE USAGE.
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
        - name: web
          resources:
            requests:
              memory: "256Mi"
            limits:
              memory: "768Mi"   # avg usage 512Mi + 50% headroom
```

### Systems (Rust Ownership, C Memory)

Systems documentation describes ownership, unsafe blocks, and memory layout. Use command-first when an operation can cause undefined behavior. Use condition-first when the safety of an operation depends on a property that the compiler cannot verify.

**Command-first WARNING for pointer alignment (Rust):**

> **Non-STE:** WARNING: Reading from a misaligned pointer is undefined behavior on most platforms.

> **STE:** WARNING: DO NOT READ FROM A POINTER THAT IS NOT CORRECTLY ALIGNED. A MISALIGNED READ CAN CAUSE UNDEFINED BEHAVIOR. UNDEFINED BEHAVIOR CAN CORRUPT MEMORY, CAUSE SECURITY VULNERABILITIES, AND CRASH THE PROGRAM. USE `std::ptr::read_unaligned` FOR UNALIGNED MEMORY. CHECK THE ALIGNMENT WITH `std::mem::align_of` BEFORE YOU READ.

> *Principles applied: P1, P8 — the command "DO NOT READ FROM A POINTER THAT IS NOT CORRECTLY ALIGNED" starts the instruction. The safe alternative is given. The check instruction follows.*

Full runnable form — aligned and unaligned read paths:

```rust
use std::mem::align_of;
use std::ptr;

/// WARNING: DO NOT READ FROM A POINTER THAT IS NOT CORRECTLY ALIGNED.
/// A MISALIGNED READ CAN CAUSE UNDEFINED BEHAVIOR. UNDEFINED BEHAVIOR
/// CAN CORRUPT MEMORY, CAUSE SECURITY VULNERABILITIES, AND CRASH THE
/// PROGRAM. USE `std::ptr::read_unaligned` FOR UNALIGNED MEMORY. CHECK
/// THE ALIGNMENT WITH `std::mem::align_of` BEFORE YOU READ.
unsafe fn load_u64(buf: *const u8, aligned: bool) -> u64 {
    if aligned && (buf as usize) % align_of::<u64>() == 0 {
        ptr::read(buf as *const u64)          // safe when aligned
    } else {
        ptr::read_unaligned(buf as *const u64) // required when not aligned
    }
}
```

**Condition-first CAUTION for manual allocators:**

> **Non-STE:** CAUTION: Custom allocators must return memory with at least the requested alignment or the allocator API contract is violated.

> **STE:** CAUTION: WHEN YOU IMPLEMENT A CUSTOM ALLOCATOR, MAKE SURE THAT THE RETURNED POINTER SATISFIES THE REQUESTED ALIGNMENT. IF THE ALIGNMENT IS NOT SATISFIED, THE ALLOCATOR CONTRACT IS VIOLATED. CODE THAT USES THE ALLOCATOR CAN PRODUCE INCORRECT RESULTS OR CRASH. CALL `std::alloc::Layout::align()` TO GET THE REQUIRED ALIGNMENT.

> *Principles applied: P1, P12 — the condition "WHEN YOU IMPLEMENT A CUSTOM ALLOCATOR" starts the instruction. The precondition (alignment) is stated. The consequence of violation is explained.*

Full runnable form — an allocator that rounds up to the alignment:

```rust
use std::alloc::{Layout, alloc};

/// CAUTION: WHEN YOU IMPLEMENT A CUSTOM ALLOCATOR, MAKE SURE THAT THE
/// RETURNED POINTER SATISFIES THE REQUESTED ALIGNMENT. IF THE ALIGNMENT
/// IS NOT SATISFIED, THE ALLOCATOR CONTRACT IS VIOLATED. CODE THAT USES
/// THE ALLOCATOR CAN PRODUCE INCORRECT RESULTS OR CRASH. CALL
/// `std::alloc::Layout::align()` TO GET THE REQUIRED ALIGNMENT.
unsafe fn alloc_aligned(size: usize, align: usize) -> *mut u8 {
    let layout = Layout::from_size_align(size, align).unwrap();
    let ptr = alloc(layout);
    // `alloc` guarantees `ptr` is a multiple of `layout.align()`.
    assert!(ptr as usize % align == 0, "allocator contract violated");
    ptr
}
```

---

## Extended Examples

### Example 1 — Missing Command (Abstract Description Only)

> **Non-STE:** WARNING: API keys stored in plaintext configuration files are a major security risk.

> **STE:** WARNING: DO NOT STORE API KEYS IN PLAINTEXT CONFIGURATION FILES. STORE API KEYS IN ENVIRONMENT VARIABLES OR A SECRETS MANAGER. PLAINTEXT API KEYS IN VERSION CONTROL CAN CAUSE UNAUTHORIZED ACCESS AND DATA THEFT.

> *Principles applied: P1, P9 — the non-STE version describes the risk but gives no command. The STE version starts with "DO NOT STORE," gives an alternative, and explains the consequence. The reader learns the action in the first four words.*

Full runnable form — a test that fails on a committed secret:

```python
# WARNING: DO NOT STORE API KEYS IN PLAINTEXT CONFIGURATION FILES.
# STORE API KEYS IN ENVIRONMENT VARIABLES OR A SECRETS MANAGER.
# PLAINTEXT API KEYS IN VERSION CONTROL CAN CAUSE UNAUTHORIZED ACCESS
# AND DATA THEFT.
def test_no_secret_in_config(config_path):
    text = config_path.read_text()
    assert "sk_live_" not in text, "plaintext API key found in config"
```

### Example 2 — Missing Condition (Consequence Only)

> **Non-STE:** WARNING: THE DATABASE TRANSACTION CAN FAIL SILENTLY.

> **STE:** WARNING: IF YOU DO NOT CHECK THE RETURN VALUE OF `transaction.commit()`, THE TRANSACTION CAN FAIL SILENTLY. DATA THAT YOU THINK IS SAVED IS NOT SAVED. THIS SILENT DATA LOSS CAN CAUSE APPLICATION INCONSISTENCY. CHECK THE RETURN VALUE AND HANDLE THE `RollbackError` CASE.

> *Principles applied: P1, P4 — the non-STE version states only the risk. The STE version adds the condition ("IF YOU DO NOT CHECK...") before the consequence. The reader learns when the risk applies, not just that it exists.*

Full runnable form — a commit that checks the result:

```python
# WARNING: IF YOU DO NOT CHECK THE RETURN VALUE OF
# `transaction.commit()`, THE TRANSACTION CAN FAIL SILENTLY. DATA THAT
# YOU THINK IS SAVED IS NOT SAVED. THIS SILENT DATA LOSS CAN CAUSE
# APPLICATION INCONSISTENCY. CHECK THE RETURN VALUE AND HANDLE THE
# `RollbackError` CASE.
try:
    transaction.commit()
except RollbackError as exc:
    logger.error("commit failed: %s", exc)
    raise
```

### Example 3 — Command Buried in Background Information

> **Non-STE:** WARNING: Configuration drift between environments is a common cause of production incidents and represents a significant operational risk to the platform's availability, with the remedy being to always use the same configuration templates across all environments and verify them before each deployment.

> **STE:** WARNING: DO NOT USE DIFFERENT CONFIGURATION TEMPLATES FOR EACH ENVIRONMENT. USE THE SAME TEMPLATE FOR ALL ENVIRONMENTS. VERIFY THE CONFIGURATION BEFORE EACH DEPLOYMENT. CONFIGURATION DRIFT CAN CAUSE PRODUCTION INCIDENTS AND SERVICE UNAVAILABILITY.

> *Principles applied: P1, P9 — the non-STE version buries the command 30 words into the sentence. The STE version puts "DO NOT USE" at the start. The reader knows the prohibition immediately. The consequence follows.*

Full runnable form — a CI check that diffs configs:

```bash
# WARNING: DO NOT USE DIFFERENT CONFIGURATION TEMPLATES FOR EACH
# ENVIRONMENT. USE THE SAME TEMPLATE FOR ALL ENVIRONMENTS. VERIFY THE
# CONFIGURATION BEFORE EACH DEPLOYMENT. CONFIGURATION DRIFT CAN CAUSE
# PRODUCTION INCIDENTS AND SERVICE UNAVAILABILITY.
diff -q config/base.yaml config/staging.yaml || exit 1
diff -q config/base.yaml config/prod.yaml    || exit 1
```

### Example 4 — Wrong Condition Order (Consequence Before Condition)

> **Non-STE:** WARNING: PERMANENT DATA LOSS CAN OCCUR IF YOU DO NOT EXPORT THE DATA BEFORE YOU RUN THE CLEANUP SCRIPT.

> **STE:** WARNING: BEFORE YOU RUN THE CLEANUP SCRIPT, EXPORT THE DATA. IF YOU DO NOT EXPORT THE DATA, THE SCRIPT REMOVES THE DATA PERMANENTLY. THE DATA CANNOT BE RECOVERED. RUN `export-data --output backup.json` AND VERIFY THE FILE BEFORE YOU RUN THE CLEANUP SCRIPT.

> *Principles applied: P1, P3 — the non-STE version puts the consequence before the condition. The reader learns the risk before learning when it applies. The STE version puts the condition first ("BEFORE YOU RUN..."). The reader learns the context, then the risk.*

Full runnable form — a guarded cleanup script:

```bash
# WARNING: BEFORE YOU RUN THE CLEANUP SCRIPT, EXPORT THE DATA. IF YOU
# DO NOT EXPORT THE DATA, THE SCRIPT REMOVES THE DATA PERMANENTLY.
# THE DATA CANNOT BE RECOVERED. RUN `export-data --output backup.json`
# AND VERIFY THE FILE BEFORE YOU RUN THE CLEANUP SCRIPT.
export-data --output backup.json
test -s backup.json || { echo "backup empty; abort"; exit 1; }
./cleanup.sh
```

### Example 5 — Passive Voice Instead of Command

> **Non-STE:** CAUTION: The input data should be validated before it is processed by the pipeline.

> **STE:** CAUTION: VALIDATE THE INPUT DATA BEFORE THE PIPELINE PROCESSES IT. IF THE PIPELINE PROCESSES INVALID DATA, THE OUTPUT CAN BE INCORRECT. THE INCORRECT OUTPUT CAN PROPAGATE TO DOWNSTREAM SYSTEMS. USE THE `validateSchema` FUNCTION TO CHECK THE DATA STRUCTURE AND TYPES.

> *Principles applied: P1, P9 — the non-STE version uses passive voice ("should be validated"). The STE version uses an imperative command ("VALIDATE THE INPUT DATA"). The command is the first word after the colon. The consequence explains why validation matters.*

Full runnable form — a validation step in a pipeline:

```python
# CAUTION: VALIDATE THE INPUT DATA BEFORE THE PIPELINE PROCESSES IT.
# IF THE PIPELINE PROCESSES INVALID DATA, THE OUTPUT CAN BE INCORRECT.
# THE INCORRECT OUTPUT CAN PROPAGATE TO DOWNSTREAM SYSTEMS. USE THE
# `validateSchema` FUNCTION TO CHECK THE DATA STRUCTURE AND TYPES.
def run_pipeline(raw):
    validateSchema(raw)        # imperative: validate first
    return transform(raw)
```

### Example 6 — Multiple Commands Without Hierarchy

> **Non-STE:** WARNING: You need to sanitize inputs, escape SQL queries, validate return types, and check authentication tokens before processing the request, or data breaches can occur.

> **STE:** WARNING: BEFORE YOU PROCESS THE REQUEST, COMPLETE THESE CHECKS: (1) SANITIZE ALL INPUT DATA. (2) USE PARAMETERIZED SQL QUERIES. (3) VALIDATE THE RETURN TYPES. (4) VERIFY THE AUTHENTICATION TOKEN. IF YOU SKIP ANY CHECK, A SECURITY BREACH OR DATA LOSS CAN OCCUR.

> *Principles applied: P1, P4 — the non-STE version lists four commands in one run-on sentence. The STE version uses a numbered list with one command per item. The condition ("BEFORE YOU PROCESS") starts the instruction. Each command is imperative and self-contained.*

Full runnable form — a request handler that runs each check as a step:

```python
# WARNING: BEFORE YOU PROCESS THE REQUEST, COMPLETE THESE CHECKS:
# (1) SANITIZE ALL INPUT DATA. (2) USE PARAMETERIZED SQL QUERIES.
# (3) VALIDATE THE RETURN TYPES. (4) VERIFY THE AUTHENTICATION TOKEN.
# IF YOU SKIP ANY CHECK, A SECURITY BREACH OR DATA LOSS CAN OCCUR.
def process_request(req):
    data = sanitize(req.body)                       # (1)
    rows = db.query("SELECT * FROM u WHERE id=%s",  # (2) parameterized
                    (data["id"],))
    result = validate_return_type(rows)            # (3)
    verify_token(req.headers["Authorization"])      # (4)
    return result
```

---

## Edge Cases

### Edge Case 1 — When a Framework Method Name Conflicts with a Command Word

Some frameworks use method names that are the same as STE-Code command words (for example, `check`, `set`, `get`, `do`). When the command in the safety instruction is also a framework method name, use the method name in backticks only when referring to the method. Use the plain word as the command.

> **Non-STE:** WARNING: Check that you check the `check()` return value before proceeding.

> **STE:** WARNING: CHECK THE RETURN VALUE OF THE `check()` METHOD BEFORE YOU CONTINUE. IF `check()` RETURNS `false`, THE AUTHENTICATION IS NOT VALID. DO NOT PROCESS THE REQUEST. AN INVALID AUTHENTICATION CAN PERMIT UNAUTHORIZED ACCESS.

> *Principles applied: P1, P5 — the command word "CHECK" is plain uppercase. The method name `check()` is in backticks. The reader distinguishes the instruction from the method reference.*

Full runnable form — an auth guard that calls `check()`:

```python
# WARNING: CHECK THE RETURN VALUE OF THE `check()` METHOD BEFORE YOU
# CONTINUE. IF `check()` RETURNS `false`, THE AUTHENTICATION IS NOT
# VALID. DO NOT PROCESS THE REQUEST. AN INVALID AUTHENTICATION CAN
# PERMIT UNAUTHORIZED ACCESS.
def guard(req):
    if authenticator.check(req.token) is False:  # check() return value
        raise PermissionError("invalid authentication")
    return handle(req)
```

### Edge Case 2 — When the Condition Is Always True for a Subset of Users

Some conditions apply only to a specific deployment configuration, operating system, or library version. When the condition is not universal, use an "IF" clause that names the specific scenario. Do not write a command that is wrong for the other users.

> **Non-STE:** WARNING: DO NOT USE THE `fetch` API IN NODE.JS BEFORE VERSION 18.

> **STE:** WARNING: IF YOU USE NODE.JS BEFORE VERSION 18, DO NOT USE THE `fetch` API. THE `fetch` API IS NOT AVAILABLE IN NODE.JS BEFORE VERSION 18. YOUR APPLICATION CRASHES WITH A `ReferenceError`. USE `node-fetch` OR UPGRADE TO NODE.JS 18 OR LATER.

> *Principles applied: P1, P10 — the condition "IF YOU USE NODE.JS BEFORE VERSION 18" scopes the prohibition. Users on Node.js 18 or later know the command does not apply to them. The alternative is given.*

Full runnable form — a version-gated import:

```javascript
// WARNING: IF YOU USE NODE.JS BEFORE VERSION 18, DO NOT USE THE
// `fetch` API. THE `fetch` API IS NOT AVAILABLE IN NODE.JS BEFORE
// VERSION 18. YOUR APPLICATION CRASHES WITH A `ReferenceError`. USE
// `node-fetch` OR UPGRADE TO NODE.JS 18 OR LATER.
let fetchImpl;
if (process.versions.node.startsWith("18") ||
    Number(process.versions.node.split(".")[0]) >= 18) {
  fetchImpl = fetch;                 // global since Node 18
} else {
  fetchImpl = require("node-fetch"); // polyfill for older runtimes
}
```

### Edge Case 3 — When a Command and a Condition Are Both Required

Some safety instructions need both a command and a condition. When both are required, put the condition first (per the rule: "give this condition first"). The condition tells the reader when the command applies. The command tells the reader what to do.

> **Non-STE:** WARNING: Always run the database migration tool and make sure you are connected to the correct database before running the schema update.

> **STE:** WARNING: BEFORE YOU RUN THE SCHEMA UPDATE, CONNECT TO THE CORRECT DATABASE. RUN THE MIGRATION TOOL WITH THE `--check` FLAG. IF YOU RUN THE SCHEMA UPDATE ON THE WRONG DATABASE, THE SCHEMA IS CORRUPTED AND THE APPLICATION CANNOT START.

> *Principles applied: P1, P9 — the condition "BEFORE YOU RUN THE SCHEMA UPDATE" comes first. The command "CONNECT TO THE CORRECT DATABASE" follows. The reader knows the sequence: check the condition, then execute the command.*

Full runnable form — a migration runner with a pre-check:

```bash
# WARNING: BEFORE YOU RUN THE SCHEMA UPDATE, CONNECT TO THE CORRECT
# DATABASE. RUN THE MIGRATION TOOL WITH THE `--check` FLAG. IF YOU RUN
# THE SCHEMA UPDATE ON THE WRONG DATABASE, THE SCHEMA IS CORRUPTED AND
# THE APPLICATION CANNOT START.
export DATABASE_URL="postgres://app@staging:5432/app"
migrate --check        # fails fast if the connection is wrong
migrate up             # only reaches here on the correct database
```

### Edge Case 4 — When a Safety Instruction References Generated Code

Generated files (from tools such as `protoc`, `graphql-codegen`, or `terraform plan`) may contain auto-generated comments that look like safety instructions. These generated comments break the command-first or condition-first rule. For generated code:

- Do not modify the generated comments. The generator overwrites your changes.
- Add your own STE-Code WARNING or CAUTION above the generated block. Your instruction follows the command-first or condition-first rule.
- If the generated code has a safety concern that is not documented, open an issue with the generator project.

> **Generated comment (leave as-is):** // Note: This method is generated. Do not edit.

> **Your wrapper with command-first:** WARNING: DO NOT EDIT THE `generated/` DIRECTORY MANUALLY. THE GENERATOR OVERWRITES YOUR CHANGES ON THE NEXT BUILD. IF YOU CHANGE THE GENERATED CODE, YOUR CHANGES ARE LOST. EDIT THE `.proto` SOURCE FILE AND RUN THE GENERATOR AGAIN.

> *Principles applied: P1, P7 — the command "DO NOT EDIT" starts the instruction. The consequence (lost changes) follows. The correct workflow is explained.*

Full runnable form — a build step that regenerates from source:

```makefile
# WARNING: DO NOT EDIT THE `generated/` DIRECTORY MANUALLY. THE
# GENERATOR OVERWRITES YOUR CHANGES ON THE NEXT BUILD. IF YOU CHANGE
# THE GENERATED CODE, YOUR CHANGES ARE LOST. EDIT THE `.proto` SOURCE
# FILE AND RUN THE GENERATOR AGAIN.
generated/:
	protoc --python_out=generated/ api.proto   # regenerates from source
```

### Edge Case 5 — Internationalization of Command and Condition Words

When your documentation is translated, the command words (DO NOT, ALWAYS, CHECK, MAKE SURE) and condition words (IF, BEFORE, WHEN) must also be translated. Use the standard translation for these words. Maintain a glossary of translated command and condition words.

The command or condition must remain the first element after the translated signal word:

| Language | DO NOT | ALWAYS | IF | BEFORE YOU |
|----------|--------|--------|----|------------|
| English | DO NOT | ALWAYS | IF | BEFORE YOU |
| Spanish | NO | SIEMPRE | SI | ANTES DE |
| French | NE PAS | TOUJOURS | SI | AVANT DE |
| German | NICHT | IMMER | WENN | BEVOR SIE |
| Japanese | 禁止 | 必ず | 場合 | 前に |

The word order rules are the same in all languages. The command or condition comes first. The consequence comes after. Do not change the structure for any language.

Full runnable form — a localized warning (Spanish) in a docstring:

```python
# ADVERTENCIA: NO GUARDE CLAVES DE API EN EL CÓDIGO FUENTE. SIEMPRE
# USE VARIABLES DE ENTORNO O UN GESTOR DE SECRETOS. LAS CLAVES EN EL
# CÓDIGO FUENTE PUEDEN CAUSAR ACCESO NO AUTORIZADO Y FUGAS DE DATOS.
def get_client():
    return Client(os.environ["API_KEY"])
```

---

## Cross-References

- **Rule 1.4** — Use only approved verb forms and adjective forms. The command in a safety instruction must use an approved verb (for example, "check," "make sure," "use," "do not").
- **Rule 1.11** — One term per concept. Use the same command words across all safety instructions. Do not use "check" in one instruction and "verify" in another for the same action.
- **Rule 1.12** — Technical verbs (build, deploy, test, lint) are allowed. Use technical verbs in commands when they are the correct term (for example, "DO NOT DEPLOY," "ALWAYS SANITIZE").
- **Rule 4.1** — Write short and clear sentences. The command or condition must be a short sentence. The reader must understand it in one reading.
- **Rule 4.2** — Use the active voice. Commands are inherently active. Conditions must also use the active voice (for example, "IF YOU DO NOT SET..." not "IF THE TIMEOUT IS NOT SET...").
- **Rule 5.3** — Use the imperative (command) form for instructions. Every WARNING or CAUTION instruction uses the imperative mood for the command part.
- **Rule 5.4** — Write each step as a command. When a safety instruction has multiple actions, write each action as a separate command.
- **Rule 7.1** — Use an applicable word to identify the level of risk. The signal word (WARNING or CAUTION) comes before the command or condition. Choose the correct signal word before you write the command.
- **Rule 7.3** — Give an explanation to show the risk or possible result. The command or condition tells the reader what to do. The explanation tells the reader why. Both are required in a complete safety instruction.
- **Section 1 (Vocabulary)** — All words used in commands and conditions must come from the approved vocabulary unless they are technical code nouns.
- **Section 5 (Procedural Writing)** — Safety instructions are procedural sentences. Follow all procedural writing rules for the command and condition parts.

---

## Grammar Notes

### Imperative Mood in Commands

Commands in safety instructions use the imperative mood. The imperative mood addresses the reader directly and tells them what to do (or not do). The subject "you" is implied and not written.

The four imperative forms used in code documentation safety instructions:

1. **Positive imperative:** CHECK THE RETURN VALUE. MAKE SURE THAT THE FILE EXISTS. BACK UP THE DATABASE.
2. **Negative imperative (prohibition):** DO NOT COMMIT THE API KEY. DO NOT USE THIS FUNCTION. DO NOT SKIP THE VALIDATION STEP.
3. **Emphatic positive imperative:** ALWAYS SANITIZE THE INPUT. ALWAYS VERIFY THE SIGNATURE. ALWAYS USE PARAMETERIZED QUERIES.
4. **Sequence imperative:** BEFORE YOU [ACTION], [COMMAND].

Do not use modal verbs in commands. Modal verbs weaken the instruction:

> **Correct:** CHECK THE RETURN VALUE BEFORE YOU CONTINUE.
> **Incorrect:** You should check the return value before continuing.
> **Incorrect:** The return value must be checked before continuing.

### Condition Clause Grammar

Condition clauses use subordinating conjunctions (IF, BEFORE, WHEN, UNLESS). The condition clause is a dependent clause. It must be attached to an independent clause that contains the consequence or the command.

**Correct condition-first structure:** IF [condition], [consequence/command]. [Explanation].

**Incorrect (consequence first):** [Consequence] IF [condition]. [Explanation].

The condition clause uses the present tense, even when referring to a future action:

> **Correct:** IF YOU DO NOT SET THE TIMEOUT, THE APPLICATION HANGS.
> **Incorrect:** IF YOU WILL NOT SET THE TIMEOUT, THE APPLICATION WILL HANG.

### Sentence Length for Commands and Conditions

The command or condition sentence must not be more than 20 words. This limit makes sure the reader understands the instruction quickly. If the full safety instruction needs more words, use multiple sentences. The first sentence is the command or condition. The following sentences give the explanation and consequence.

> **Correct (19 words):** DO NOT USE THE `eval()` FUNCTION WITH DATA THAT COMES FROM AN UNTRUSTED SOURCE. EVAL() CAN EXECUTE ARBITRARY CODE.
>
> **Correct (split across sentences):** DO NOT USE THE `eval()` FUNCTION WITH UNTRUSTED DATA. EVAL() CAN EXECUTE ARBITRARY CODE. ARBITRARY CODE EXECUTION CAN CAUSE A COMPLETE SYSTEM COMPROMISE.

The condition sentence can also be split:

> **Correct (condition first, then consequence):** IF YOU DO NOT SANITIZE THE INPUT DATA, THE QUERY CAN FAIL. THE FAILURE CAN CAUSE DATA CORRUPTION. SANITIZE ALL INPUT WITH THE `cleanInput` FUNCTION.

### Punctuation After the Signal Word

The signal word is followed by a colon (:) and a single space. The command or condition sentence starts with an uppercase letter. Use a period (.) at the end of each sentence. Do not use semicolons to join the command and the consequence.

> **Correct:** WARNING: DO NOT STORE THE PRIVATE KEY IN THE REPOSITORY. THE PRIVATE KEY CAN BE ACCESSED BY UNAUTHORIZED USERS.
>
> **Incorrect:** WARNING: do not store the private key in the repository; the private key can be accessed by unauthorized users.

### Parallel Structure in Multi-Command Instructions

When a safety instruction contains multiple commands, use parallel grammatical structure. Each command must use the same verb form. Use a numbered list for clarity.

> **Correct:**
> WARNING: BEFORE YOU DEPLOY, COMPLETE THESE STEPS:
> (1) BACK UP THE DATABASE.
> (2) RUN THE MIGRATION SCRIPTS.
> (3) VERIFY THE APPLICATION HEALTH CHECK.
>
> **Incorrect:**
> WARNING: Before deploying you should back up the database, running migration scripts must be done, and the health check is verified.

### "Make Sure" as a Command Pattern

"Make sure" is a special command pattern in STE-Code. It is used when the reader must verify a condition before acting. "Make sure" is followed by a "that" clause that describes the condition to verify.

> **Correct:** MAKE SURE THAT THE DATABASE CONNECTION IS OPEN BEFORE YOU RUN THE QUERY.
> **Correct:** MAKE SURE THAT THE INPUT DATA IS SANITIZED BEFORE THE PIPELINE PROCESSES IT.

Do not use "make sure" when a direct imperative verb is clearer:

> **Better:** SANITIZE THE INPUT DATA BEFORE THE PIPELINE PROCESSES IT.
> **Acceptable:** MAKE SURE THAT THE INPUT DATA IS SANITIZED BEFORE THE PIPELINE PROCESSES IT.

Use "make sure" for verification of existing state. Use direct imperatives for actions the reader must perform.

---

<!-- a-sec7-rule7.3.md -->

# Rule 7.3 — Give an Explanation to Show the Risk or Possible Result

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 7.3

> **Source:** [master.md#sec7-rule7.3](ste-code/grouped/)

## Original Rule

**Rule 7.3** If it is possible, always tell your reader about the problems that can occur if the reader does not obey the safety instruction. If there is a clear and specified risk, the person who does the task will understand the risk and be more careful.

**Spec examples:**

(Refer to the underlined risk or possible result.)

> **WARNING:** DO NOT SWALLOW THE SOLVENT. ALWAYS MAKE SURE THAT YOU KNOW THE SAFETY PRECAUTIONS AND FIRST AID INSTRUCTIONS FOR SOLVENTS. SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH.

> **CAUTION:** DO NOT USE BLEACH OR CLEANSERS THAT CONTAIN CHLORINE TO CLEAN THE UNIT. THESE CLEANING AGENTS CAN CAUSE CORROSION.

> IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR.

## STE-Code Adaptation

**Rule 7.3** In code documentation, if it is possible, always tell your reader about the problems that can occur if the reader does not obey the safety instruction. If there is a clear and specified risk, the developer who uses the code will understand the risk and be more careful.

Severity mapping: The risk explanation must match the severity from Rule 7.1. For release-note and changelog severity, map the levels as follows: WARNING to BREAKING, CAUTION to DEPRECATED, NOTE to NOTE.

A risk explanation has three parts: (1) the violation or failure to obey the instruction, (2) the immediate consequence, and (3) the cascading or final harm. Write the chain in cause-first order: "If you do X, Y can happen." Do not stop at "Y must not happen" without naming what Y is. An instruction without a risk explanation is a prohibition the reader can dismiss. A risk explanation turns the prohibition into a reason.

### Examples

> *Adapted from spec pair:* Non-STE: `WARNING: DO NOT SWALLOW THE SOLVENT. ... SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH.`  |  STE: `WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.` (ASD-STE100 Issue 9, Rule 7.3, page 100 — the WARNING names the poison and the injury or death; the code-domain pair names the exposure and the breach.)

> **Non-STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.
>
> *Adapted from spec pattern: WARNING with risk explanation — "SOLVENTS ARE POISONOUS AND CAN CAUSE INJURY OR DEATH."*

A complete README section that uses this pair, with the risk explanation written in context:

```markdown
## Security Setup

WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.
API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.

Store the key in an environment variable named `PAYMENTS_API_KEY`.
Add the `.env` file to `.gitignore`. A committed key stays in the
repository history after you remove it, so rotate the key after a leak.
```

> **Non-STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS.
>
> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *Adapted from spec pattern: CAUTION with risk explanation — "THESE CLEANING AGENTS CAN CAUSE CORROSION."*

A JSDoc comment that uses this pair, with the specific deprecated function named:

```javascript
/**
 * CAUTION: DO NOT USE THE `formatDate` FUNCTION.
 * DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
 *
 * `formatDate` uses the host time zone. The output changes between
 * servers, so two users can see two different dates for the same event.
 * Use `formatDateUTC` instead.
 *
 * @deprecated since v3.2.0
 */
function formatDate(value) { /* ... */ }
```

> **Non-STE:** MAKE SURE THAT YOU SET THE CONNECTION TIMEOUT.
>
> **STE:** IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.
>
> *Adapted from spec pattern: consequence statement — "IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR."*

A configuration file and the docstring that explain the timeout risk:

```python
def connect(host: str, port: int, timeout: float | None = None) -> Socket:
    """Open a TCP connection to the server.

    IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN
    BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.

    Without a timeout, a connection that never answers keeps the calling
    thread blocked. Blocked threads fill the worker pool. When the pool
    is full, the application stops accepting new requests. Writes that
    wait for a blocked connection are not committed, so the data is lost.

    Parameters:
        timeout: Seconds to wait before the connect fails. The default is
            None, which means wait forever. Always pass a value.
    """
```

> **See also:** Rule 7.1 — Use an Applicable Word (for Example, "Warning" or "Caution") to Identify the Level of Risk; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition; Rule 7.4 — Use Imperative Mood for Instructions

---

## Code-Domain Explanation

Rule 7.3 addresses a fundamental gap in software documentation: instructions that tell the reader _what_ to avoid but not _why_ the avoidance matters. In aerospace, a mechanic who understands that a solvent is poisonous will handle it more carefully. In code, a developer who understands that an omitted timeout causes data loss will take the instruction seriously.

The rule applies differently across documentation types:

**README files.** README files give setup instructions and usage warnings. A README that says "do not use Node.js versions below 18" without explanation leaves new contributors vulnerable. The README must add: "Node.js versions below 18 do not include the `fetch` API. The application uses `fetch` for all network requests. If you use a version below 18, the requests will fail without an error message." The risk explanation connects the prohibition to a specific, observable failure.

```markdown
## Requirements

CAUTION: USE NODE.JS VERSION 18 OR HIGHER.
NODE.JS VERSIONS BELOW 18 DO NOT INCLUDE THE `fetch` API.
THE APPLICATION USES `fetch` FOR ALL NETWORK REQUESTS.
IF YOU USE A VERSION BELOW 18, THE REQUESTS WILL FAIL WITHOUT AN ERROR MESSAGE.

Run `node --version` before you run `npm install`.
```

**API documentation.** API docs describe function contracts. A docstring that says "do not pass null" is incomplete. It must also say: "If you pass null, the function throws a `NullPointerException` and the transaction is not committed. Uncommitted transactions can cause database lock contention." The reader now understands the cascading effect, not just the immediate error.

```java
/**
 * CAUTION: DO NOT PASS NULL FOR THE `orderId` PARAMETER.
 * A NULL `orderId` CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
 *
 * If you pass null, the method throws NullPointerException and the
 * transaction is not committed. An uncommitted transaction holds a row
 * lock. Locked rows can block other requests and cause database
 * contention for all users of the table.
 */
Order loadOrder(String orderId) { /* ... */ }
```

**Docstrings and inline comments.** Docstrings carry both usage notes and warnings. A docstring that says "this function is not thread-safe" without explanation is ignored. The docstring must add: "If two goroutines call this function at the same time, the internal map can become corrupt. Map corruption causes silent data loss because no error is returned." The risk explanation transforms an abstract property into a concrete hazard.

```go
// CAUTION: THE `Counter` TYPE IS NOT THREAD-SAFE.
// THE `Counter` TYPE CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
//
// If two goroutines call Add at the same time, the internal map can
// become corrupt. Map corruption causes silent data loss because no
// error is returned. Use CounterSafe, which uses a mutex, for concurrent
// code.
type Counter struct { values map[string]int }
```

**Commit messages.** Commit messages serve as historical records and review context. A commit that says "remove the `--force` flag from the deploy script" documents a change. The body must add: "If the `--force` flag is used, the deploy script overwrites the production database without confirmation. Overwriting the production database can cause permanent loss of user data." Future readers who consider reintroducing the flag will see the recorded risk.

```
WARNING: Remove the --force flag from the deploy script.

The --force flag made the deploy script overwrite the production
database without confirmation. A wrong branch name then destroyed
all user data. Overwriting the production database can cause
permanent loss of user data.

The script now fails if the target is the production database unless
you set DEPLOY_TO_PROD=true. Keep this guard. Do not add --force back.
```

**Error messages.** Error messages are the last line of defense. An error that says "configuration not found" tells the user a fact. A better error says: "The configuration file `config.toml` was not found. The application cannot start without this file. If the application starts without configuration, it uses unsafe default values that can expose sensitive data in logs." The risk explanation turns a missing-file notice into an actionable security warning.

```
WARNING: THE CONFIGURATION FILE config.toml WAS NOT FOUND.
THE APPLICATION CANNOT START WITHOUT THIS FILE.
IF THE APPLICATION STARTS WITHOUT CONFIGURATION, IT USES UNSAFE
DEFAULT VALUES THAT CAN EXPOSE SENSITIVE DATA IN LOGS.

Check that config.toml is in the working directory. Set the
CONFIG_PATH environment variable to the file location.
```

**Changelogs and release notes.** A changelog entry that says "BREAKING: removed the `legacy_auth` module" tells users about a deletion. It must also say: "If your code imports `legacy_auth`, the build will fail. You must replace all imports with the `auth_v2` module. A build failure can delay your deployment and cause service downtime." The risk explanation helps users plan their migration. A changelog without risk explanations is a list of facts. A changelog with risk explanations is a migration guide.

```markdown
## [4.0.0] - 2026-08-01

### BREAKING
- Removed the `legacy_auth` module.

  WARNING: IF YOUR CODE IMPORTS `legacy_auth`, THE BUILD WILL FAIL.
  YOU MUST REPLACE ALL IMPORTS WITH THE `auth_v2` MODULE.
  A BUILD FAILURE CAN DELAY YOUR DEPLOYMENT AND CAUSE SERVICE DOWNTIME.

  Run `grep -r legacy_auth src/` to find every import. The `auth_v2`
  module uses token scopes instead of the old role list. See the
  migration guide before you upgrade.
```

**The risk explanation must match the signal word level.** The original ASD-STE100 defines two severity levels: WARNING (risk of injury or death) and CAUTION (risk of equipment damage). In code documentation, WARNING maps to data loss, security breach, or system unavailability. CAUTION maps to incorrect results, degraded performance, or build failures. A risk explanation under a WARNING must describe a severe outcome. A risk explanation under a CAUTION must describe a moderate outcome. Do not use WARNING for a build failure. Do not use CAUTION for a data breach. Mismatched severity erodes trust in all safety instructions in the document.

## Paradigm-Specific Guidance

**Object-Oriented (Java, C++, C#, Python classes).** In OOP, risk explanations often involve state corruption and inheritance contracts. A warning about a mutable field must explain that subclasses can modify the field in unexpected ways. A caution about a non-final method must explain that overriding can violate the base class invariant.

> **Non-STE:** CAUTION: DO NOT OVERRIDE THE `initialize()` METHOD.
>
> **STE:** CAUTION: DO NOT OVERRIDE THE `initialize()` METHOD. IF YOU OVERRIDE `initialize()`, THE BASE CLASS CONNECTION POOL IS NOT SET. CONNECTIONS WITHOUT A POOL CAN CAUSE RESOURCE EXHAUSTION AND APPLICATION CRASHES.
>
> *Principles applied: P3 (get → is not set), P7 (initialize as verb, not noun). Risk connects override to pool state to crash.*

```python
class Database:
    def __init__(self):
        self._pool = self._build_pool()

    def initialize(self):
        """CAUTION: DO NOT OVERRIDE THE `initialize()` METHOD.
        IF YOU OVERRIDE `initialize()`, THE BASE CLASS CONNECTION POOL IS
        NOT SET. CONNECTIONS WITHOUT A POOL CAN CAUSE RESOURCE EXHAUSTION
        AND APPLICATION CRASHES.

        Subclasses that override initialize must call super().initialize()
        first, or the pool stays None and every query fails open."""
        self._ready = True
```

**Functional (Haskell, Elixir, Clojure, Rust).** In functional paradigms, risk explanations often involve purity violations and lazy evaluation surprises. A warning about an impure function must explain that referential transparency is broken. A caution about an unsafe IO operation must explain that laziness delays the side effect beyond the expected execution point.

> **Non-STE:** WARNING: `unsafePerformIO` IS DANGEROUS.
>
> **STE:** WARNING: DO NOT USE `unsafePerformIO` IN PRODUCTION CODE. `unsafePerformIO` REMOVES THE IO TYPE SAFETY GUARANTEE. WITHOUT THE IO GUARANTEE, SIDE EFFECTS CAN RUN AT UNEXPECTED TIMES. SIDE EFFECTS AT UNEXPECTED TIMES CAN CAUSE RACE CONDITIONS AND SILENT DATA CORRUPTION.
>
> *Principles applied: P10 (no slang: "dangerous" → specific risk), P4 (approved adjective forms). Risk traces from type-safety removal to corruption.*

```haskell
-- WARNING: DO NOT USE `unsafePerformIO` IN PRODUCTION CODE.
-- `unsafePerformIO` REMOVES THE IO TYPE SAFETY GUARANTEE.
-- WITHOUT THE IO GUARANTEE, SIDE EFFECTS CAN RUN AT UNEXPECTED TIMES.
-- SIDE EFFECTS AT UNEXPECTED TIMES CAN CAUSE RACE CONDITIONS AND
-- SILENT DATA CORRUPTION.
--
-- cacheLookup reads a file inside a pure function. Two calls with the
-- same key can return different values because the file changes between
-- them. Referential transparency is broken.
secret :: Key -> Value
secret k = unsafePerformIO (readSecretFromFile k)
```

**Procedural (C, Go, Bash).** In procedural code, risk explanations often involve resource lifetimes and error-code neglect. A warning about a `malloc` without `free` must explain the leak's cumulative effect. A caution about an ignored return code must explain the silent failure path.

> **Non-STE:** WARNING: YOU MUST FREE THE BUFFER.
>
> **STE:** WARNING: YOU MUST FREE THE BUFFER AFTER EACH `malloc` CALL. EACH UNFREED BUFFER STAYS IN MEMORY UNTIL THE PROCESS STOPS. IN A LONG-RUNNING PROCESS, UNFREED BUFFERS CAN USE ALL AVAILABLE MEMORY. MEMORY EXHAUSTION CAN CAUSE THE OPERATING SYSTEM TO STOP THE PROCESS.
>
> *Principles applied: P1 (use → after each call), P9 (short, clear nouns). Risk traces from unfreed buffer to OS termination.*

```c
/* WARNING: YOU MUST FREE THE BUFFER AFTER EACH `malloc` CALL.
   EACH UNFREED BUFFER STAYS IN MEMORY UNTIL THE PROCESS STOPS.
   IN A LONG-RUNNING PROCESS, UNFREED BUFFERS CAN USE ALL AVAILABLE
   MEMORY. MEMORY EXHAUSTION CAN CAUSE THE OPERATING SYSTEM TO STOP
   THE PROCESS. */
char *buf = malloc(1024);
if (buf == NULL) { return ERR_NOMEM; }
parse(buf);
free(buf);   /* without this line, the leak grows every call */
```

**Declarative (SQL, Terraform, Kubernetes YAML).** In declarative configurations, risk explanations often involve cascading side effects from a single declaration. A Terraform resource change can destroy and recreate infrastructure. A Kubernetes manifest misconfiguration can expose internal services.

> **Non-STE:** CAUTION: DO NOT CHANGE THE `family` FIELD.
>
> **STE:** CAUTION: DO NOT CHANGE THE `family` FIELD IN THE `aws_db_instance` RESOURCE. TERRAFORM INTERPRETS A CHANGE TO `family` AS A DESTROY-AND-RECREATE OPERATION. A DESTROY-AND-RECREATE OPERATION REMOVES THE CURRENT DATABASE AND ALL ITS DATA. THE REMOVED DATA CANNOT BE RECOVERED.
>
> *Principles applied: P3 (show → interprets), P11 (one term: destroy-and-recreate). Risk explains the interpreter behavior behind the field change.*

```hcl
resource "aws_db_instance" "main" {
  # CAUTION: DO NOT CHANGE THE `family` FIELD IN THIS RESOURCE.
  # TERRAFORM INTERPRETS A CHANGE TO `family` AS A DESTROY-AND-RECREATE
  # OPERATION. A DESTROY-AND-RECREATE OPERATION REMOVES THE CURRENT
  # DATABASE AND ALL ITS DATA. THE REMOVED DATA CANNOT BE RECOVERED.
  family = "postgres16"
}
```

**Systems (Rust ownership, C memory, kernel documentation).** Systems documentation carries the highest-risk instructions. A warning about undefined behavior in C must explain the practical consequence, not just cite the standard. A Rust `unsafe` block documentation must explain which safety invariant the caller must uphold and what happens if it is not.

> **Non-STE:** WARNING: THIS FUNCTION IS UNSAFE. THE CALLER MUST NOT ALIAS THE POINTER.
>
> **STE:** WARNING: THIS FUNCTION IS UNSAFE. THE CALLER MUST MAKE SURE THAT NO OTHER POINTER REFERS TO THE SAME MEMORY. IF TWO POINTERS REFER TO THE SAME MEMORY, THE COMPILER CAN REMOVE LOADS AND STORES THAT THE PROGRAM NEEDS. REMOVED LOADS AND STORES CAN CAUSE VALUES TO APPEAR FROM DIFFERENT EXECUTION TIMELINES, WHICH IS UNDEFINED BEHAVIOR.
>
> *Principles applied: P2 (alias → refer to, specified part of speech), P8 (standard technical nouns: undefined behavior). Risk connects aliasing to compiler optimization to undefined behavior.*

```rust
/// WARNING: THIS FUNCTION IS UNSAFE.
/// THE CALLER MUST MAKE SURE THAT NO OTHER POINTER REFERS TO THE SAME MEMORY.
/// IF TWO POINTERS REFER TO THE SAME MEMORY, THE COMPILER CAN REMOVE
/// LOADS AND STORES THAT THE PROGRAM NEEDS. REMOVED LOADS AND STORES CAN
/// CAUSE VALUES TO APPEAR FROM DIFFERENT EXECUTION TIMELINES, WHICH IS
/// UNDEFINED BEHAVIOR.
///
/// `write_volatile` writes through `ptr` with no aliasing check. Keep the
/// pointed-to memory exclusive to this call while it runs.
pub unsafe fn write_volatile(ptr: *mut u32, value: u32) { /* ... */ }
```

## Extended Examples

> **Non-STE:** WARNING: DO NOT USE `eval()`.
>
> **STE:** WARNING: DO NOT USE `eval()` WITH DATA FROM EXTERNAL SOURCES. `eval()` RUNS THE INPUT AS CODE WITH THE SAME PRIVILEGES AS THE APPLICATION. A MALICIOUS INPUT CAN RUN ARBITRARY COMMANDS ON THE HOST SYSTEM. ARBITRARY COMMANDS CAN CAUSE DATA THEFT, DATA DESTRUCTION, OR SYSTEM COMPROMISE.
>
> *Principles applied: P5 (technical code noun: `eval`), P3 (use → runs, approved meaning). Risk traces from eval to full system compromise.*

```javascript
// WARNING: DO NOT USE `eval()` WITH DATA FROM EXTERNAL SOURCES.
// `eval()` RUNS THE INPUT AS CODE WITH THE SAME PRIVILEGES AS THE APPLICATION.
// A MALICIOUS INPUT CAN RUN ARBITRARY COMMANDS ON THE HOST SYSTEM.
// ARBITRARY COMMANDS CAN CAUSE DATA THEFT, DATA DESTRUCTION, OR SYSTEM COMPROMISE.
function runFilter(userInput) {
  // Bad: eval(userInput)
  return JSON.parse(userInput); // Safe: parse only, no code execution
}
```

> **Non-STE:** CAUTION: PAGINATION IS MANDATORY.
>
> **STE:** CAUTION: YOU MUST USE PAGINATION FOR ALL LIST ENDPOINTS. WITHOUT PAGINATION, A SINGLE REQUEST CAN RETURN EVERY RECORD IN THE DATABASE. A LARGE RESULT SET CAN CAUSE MEMORY EXHAUSTION ON THE SERVER. MEMORY EXHAUSTION CAN CAUSE THE SERVER TO STOP AND ALL CONNECTED CLIENTS TO DISCONNECT.
>
> *Principles applied: P9 (short, clear: pagination), P1 (use → use). Risk traces from missing pagination to server crash.*

```python
@app.get("/users")
def list_users(page: int = 1, per_page: int = 50):
    """CAUTION: YOU MUST USE PAGINATION FOR ALL LIST ENDPOINTS.
    WITHOUT PAGINATION, A SINGLE REQUEST CAN RETURN EVERY RECORD IN THE
    DATABASE. A LARGE RESULT SET CAN CAUSE MEMORY EXHAUSTION ON THE SERVER.
    MEMORY EXHAUSTION CAN CAUSE THE SERVER TO STOP AND ALL CONNECTED
    CLIENTS TO DISCONNECT.

    Reject requests where per_page is above 100. Use keyset pagination on
    the `id` column for stable ordering."""
    return db.paginate(page, per_page)
```

> **Non-STE:** WARNING: CORS IS NOT CONFIGURED PROPERLY.
>
> **STE:** WARNING: THE CORS CONFIGURATION USES A WILDCARD ORIGIN (`*`). A WILDCARD ORIGIN LETS ANY WEBSITE SEND REQUESTS WITH THE USER'S CREDENTIALS. AN ATTACKER CAN MAKE AN AUTHENTICATED REQUEST FROM A MALICIOUS WEBSITE. AUTHENTICATED REQUESTS FROM A MALICIOUS ORIGIN CAN CAUSE DATA THEFT AND ACCOUNT TAKEOVER.
>
> *Principles applied: P5 (CORS, wildcard as technical nouns), P6 (non-approved word as technical noun). Risk traces from wildcard to account takeover.*

```javascript
// WARNING: THE CORS CONFIGURATION USES A WILDCARD ORIGIN (`*`).
// A WILDCARD ORIGIN LETS ANY WEBSITE SEND REQUESTS WITH THE USER'S
// CREDENTIALS. AN ATTACKER CAN MAKE AN AUTHENTICATED REQUEST FROM A
// MALICIOUS WEBSITE. AUTHENTICATED REQUESTS FROM A MALICIOUS ORIGIN CAN
// CAUSE DATA THEFT AND ACCOUNT TAKEOVER.
app.use(cors({
  origin: ["https://app.example.com"], // not "*"
  credentials: true,
}));
```

> **Non-STE:** WARNING: RACE CONDITION.
>
> **STE:** WARNING: TWO GOROUTINES CAN WRITE TO THE `counter` VARIABLE AT THE SAME TIME. CONCURRENT WRITES TO A GO VARIABLE WITHOUT A MUTEX CAUSE A DATA RACE. DATA RACES CAN MAKE THE COUNTER VALUE INCORRECT. AN INCORRECT COUNTER CAN CAUSE BILLING ERRORS AND FINANCIAL LOSS.
>
> *Principles applied: P7 (no technical noun as verb: "race" is a noun here), P3 (make → cause). Risk traces from data race to financial loss.*

```go
// WARNING: TWO GOROUTINES CAN WRITE TO THE `counter` VARIABLE AT THE SAME
// TIME. CONCURRENT WRITES TO A GO VARIABLE WITHOUT A MUTEX CAUSE A DATA
// RACE. DATA RACES CAN MAKE THE COUNTER VALUE INCORRECT. AN INCORRECT
// COUNTER CAN CAUSE BILLING ERRORS AND FINANCIAL LOSS.
var counter int
var mu sync.Mutex

func increment() {
    mu.Lock()
    defer mu.Unlock()
    counter++ // protected: no data race
}
```

> **Non-STE:** CAUTION: DO NOT SKIP MIGRATIONS.
>
> **STE:** CAUTION: DO NOT SKIP DATABASE MIGRATIONS. EACH PENDING MIGRATION CAN ADD, REMOVE, OR CHANGE COLUMNS. IF THE APPLICATION STARTS WITHOUT APPLYING ALL MIGRATIONS, THE APPLICATION SCHEMA DOES NOT MATCH THE DATABASE SCHEMA. SCHEMA MISMATCHES CAN CAUSE QUERY FAILURES, SILENT DATA LOSS, AND APPLICATION CRASHES.
>
> *Principles applied: P1 (skip → skip), P4 (approved adjective: pending). Risk traces from skipped migration to crashes.*

```sql
-- CAUTION: DO NOT SKIP DATABASE MIGRATIONS.
-- EACH PENDING MIGRATION CAN ADD, REMOVE, OR CHANGE COLUMNS.
-- IF THE APPLICATION STARTS WITHOUT APPLYING ALL MIGRATIONS, THE
-- APPLICATION SCHEMA DOES NOT MATCH THE DATABASE SCHEMA. SCHEMA
-- MISMATCHES CAN CAUSE QUERY FAILURES, SILENT DATA LOSS, AND CRASHES.
--
-- Run this before you start the application after a deploy:
--   alembic upgrade head
SELECT version_num FROM alembic_version;
```

> **Non-STE:** WARNING: HARDCODED SECRETS.
>
> **STE:** WARNING: THE CONFIGURATION FILE CONTAINS HARDCODED SECRETS. HARDCODED SECRETS BECOME PART OF THE SOURCE CODE HISTORY. ANY PERSON WITH ACCESS TO THE REPOSITORY CAN READ THE SECRETS. AN ATTACKER WITH REPOSITORY ACCESS CAN USE THE SECRETS TO ACCESS PRODUCTION SYSTEMS, DATABASES, AND THIRD-PARTY SERVICES.
>
> *Principles applied: P5 (secrets as technical noun), P3 (part of → become part of). Risk traces from hardcoded secrets to full infrastructure access.*

```yaml
# WARNING: THE CONFIGURATION FILE CONTAINS HARDCODED SECRETS.
# HARDCODED SECRETS BECOME PART OF THE SOURCE CODE HISTORY. ANY PERSON
# WITH ACCESS TO THE REPOSITORY CAN READ THE SECRETS. AN ATTACKER WITH
# REPOSITORY ACCESS CAN USE THE SECRETS TO ACCESS PRODUCTION SYSTEMS,
# DATABASES, AND THIRD-PARTY SERVICES.
#
# Replace the literal value with ${DATABASE_PASSWORD} and load it from
# the secret store. Then rotate the exposed password and remove the file
# from history with `git filter-repo`.
database:
  password: "s3cr3t-password"   # remove this line
```

## Edge Cases

**When a framework name is also an "unapproved" word.** Some framework names overlap with everyday English words that STE restricts. For example, the React framework `Suspense` is both a technical noun and an ordinary English word. A warning that says "DO NOT NEST SUSPENSE BOUNDARIES" could confuse readers who interpret Suspense as an emotion, not a component. The risk explanation must anchor the word in its technical meaning: "IF YOU NEST `Suspense` COMPONENTS, THE INNER SUSPENSE BOUNDARY CAN CAPTURE THE FALLBACK OF THE OUTER BOUNDARY. CAPTURED FALLBACKS CAN CAUSE INFINITE LOADING STATES AND UNRESPONSIVE PAGES." The code-formatted backticks and the repeated technical context disambiguate the term.

```jsx
// CAUTION: DO NOT NEST `Suspense` COMPONENTS.
// IF YOU NEST `Suspense` COMPONENTS, THE INNER SUSPENSE BOUNDARY CAN
// CAPTURE THE FALLBACK OF THE OUTER BOUNDARY. CAPTURED FALLBACKS CAN
// CAUSE INFINITE LOADING STATES AND UNRESPONSIVE PAGES.
function Page() {
  return (
    <Suspense fallback={<Spinner />}>
      <Suspense fallback={<Spinner />}>  {/* nested: captures fallback */}
        <Comments />
      </Suspense>
    </Suspense>
  );
}
```

**When a code keyword conflicts with the rule.** Keywords like `break`, `continue`, `return`, and `throw` carry control-flow meaning that risk explanations must address precisely. A warning that says "DO NOT USE `return` INSIDE A `finally` BLOCK" must explain the interaction: "IF YOU USE `return` IN A `finally` BLOCK, THE `return` REPLACES ANY EXCEPTION THAT WAS THROWN IN THE `try` BLOCK. THE REPLACED EXCEPTION IS LOST AND CANNOT BE CAUGHT BY CALLERS. SILENTLY LOST EXCEPTIONS CAN HIDE ERRORS THAT CAUSE INCORRECT PROGRAM BEHAVIOR." The risk explanation addresses the language-level semantic collision, not the word itself.

```java
// CAUTION: DO NOT USE `return` INSIDE A `finally` BLOCK.
// IF YOU USE `return` IN A `finally` BLOCK, THE `return` REPLACES ANY
// EXCEPTION THAT WAS THROWN IN THE `try` BLOCK. THE REPLACED EXCEPTION IS
// LOST AND CANNOT BE CAUGHT BY CALLERS. SILENTLY LOST EXCEPTIONS CAN HIDE
// ERRORS THAT CAUSE INCORRECT PROGRAM BEHAVIOR.
try {
  doWork();
} finally {
  cleanup();
  // return result;  // removes any exception from doWork()
}
```

**When the rule should be relaxed for generated code.** Generated code (protobuf stubs, OpenAPI clients, database ORM models) often contains instructions that violate Rule 7.3 because the generator produces terse, repetitive output. A generated file comment that says "DO NOT EDIT" without explanation is acceptable only if a companion document or the code generator's documentation explains the risk. If the generated code is the sole artifact the developer sees, the risk must still be explained: "DO NOT EDIT THIS FILE. THIS FILE IS REGENERATED EACH TIME YOU RUN `make generate`. IF YOU EDIT THE FILE, YOUR CHANGES ARE LOST THE NEXT TIME `make generate` RUNS. LOST CHANGES CAN CAUSE BUILD FAILURES AND REGRESSION BUGS."

```go
// Code generated by protoc-gen-go. DO NOT EDIT.
// DO NOT EDIT THIS FILE. THIS FILE IS REGENERATED EACH TIME YOU RUN
// `make generate`. IF YOU EDIT THE FILE, YOUR CHANGES ARE LOST THE NEXT
// TIME `make generate` RUNS. LOST CHANGES CAN CAUSE BUILD FAILURES AND
// REGRESSION BUGS.
package pb
```

**When the risk is probabilistic, not guaranteed.** Many software risks are not deterministic: a race condition may manifest only under load, a memory leak may exhaust resources only after days. Rule 7.3 still applies. Use "can" instead of "will" for probabilistic risks: "IF TWO THREADS WRITE TO THE MAP AT THE SAME TIME, A DATA RACE CAN OCCUR. THE DATA RACE CAN CAUSE INCORRECT MAP CONTENTS. INCORRECT MAP CONTENTS CAN CAUSE WRONG QUERY RESULTS AND SILENT DATA CORRUPTION." The word "can" communicates uncertainty without diminishing the severity.

```java
// CAUTION: THE CACHE IS NOT THREAD-SAFE.
// IF TWO THREADS WRITE TO THE MAP AT THE SAME TIME, A DATA RACE CAN OCCUR.
// THE DATA RACE CAN CAUSE INCORRECT MAP CONTENTS. INCORRECT MAP CONTENTS
// CAN CAUSE WRONG QUERY RESULTS AND SILENT DATA CORRUPTION.
// (A race may not happen on every run. Under load, it can.)
Map<String, Object> cache = new HashMap<>();
```

**When multiple risks share one instruction.** A single "DO NOT" instruction may prevent several different problems. List the risks in order of severity, from most severe to least severe: "DO NOT DISABLE TLS VERIFICATION. WITHOUT TLS VERIFICATION, A MAN-IN-THE-MIDDLE ATTACKER CAN DECRYPT AND CHANGE THE TRAFFIC. CHANGED TRAFFIC CAN CAUSE DATA THEFT, CREDENTIAL LEAKAGE, AND UNAUTHORIZED TRANSACTIONS." Each risk is a separate "can cause" clause that builds the cumulative case for the instruction.

```python
# WARNING: DO NOT DISABLE TLS VERIFICATION.
# WITHOUT TLS VERIFICATION, A MAN-IN-THE-MIDDLE ATTACKER CAN DECRYPT AND
# CHANGE THE TRAFFIC. CHANGED TRAFFIC CAN CAUSE DATA THEFT, CREDENTIAL
# LEAKAGE, AND UNAUTHORIZED TRANSACTIONS.
import urllib3
urllib3.disable_warnings()  # remove this line
```

**When the risk is a cascading chain with no single owner.** Distributed systems failures often involve emergent behavior where no single component is at fault. A warning about removing a circuit breaker must explain the cascading effect across services: "IF YOU REMOVE THE CIRCUIT BREAKER FROM THE PAYMENT SERVICE, A SLOWDOWN IN THE INVENTORY SERVICE CAN PROPAGATE TO THE PAYMENT SERVICE. THE PROPAGATED SLOWDOWN CAN CAUSE TIMEOUTS IN THE ORDER SERVICE. ORDER SERVICE TIMEOUTS CAN CAUSE CUSTOMERS TO PLACE DUPLICATE ORDERS. DUPLICATE ORDERS CAN CAUSE INCORRECT CHARGES AND FINANCIAL LOSS." The risk explanation traces the chain across three services without blaming any single component.

```yaml
# WARNING: DO NOT REMOVE THE CIRCUIT BREAKER FROM THE PAYMENT SERVICE.
# IF YOU REMOVE THE CIRCUIT BREAKER, A SLOWDOWN IN THE INVENTORY SERVICE
# CAN PROPAGATE TO THE PAYMENT SERVICE. THE PROPAGATED SLOWDOWN CAN CAUSE
# TIMEOUTS IN THE ORDER SERVICE. ORDER SERVICE TIMEOUTS CAN CAUSE
# CUSTOMERS TO PLACE DUPLICATE ORDERS. DUPLICATE ORDERS CAN CAUSE
# INCORRECT CHARGES AND FINANCIAL LOSS.
payment_service:
  circuit_breaker:
    enabled: true   # keep true
```

**When the risk affects a different team than the reader.** In large organizations, the person who reads the documentation is often not the person who suffers the consequence. An infrastructure engineer reading an application warning may not feel the urgency. The risk explanation must bridge the organizational gap: "DO NOT DEPLOY WITHOUT CONTACTING THE DATABASE TEAM FIRST. THE DATABASE TEAM MUST LOCK THE SCHEMA BEFORE DEPLOYMENT. IF YOU DEPLOY WITHOUT A SCHEMA LOCK, THE MIGRATION CAN CONFLICT WITH ANOTHER DEPLOYMENT. SCHEMA CONFLICTS CAN CAUSE DATA CORRUPTION THAT AFFECTS ALL TEAMS USING THE DATABASE." The phrase "affects all teams using the database" connects the reader's action to consequences beyond their immediate team.

```markdown
## Deploy Checklist

WARNING: DO NOT DEPLOY WITHOUT CONTACTING THE DATABASE TEAM FIRST.
THE DATABASE TEAM MUST LOCK THE SCHEMA BEFORE DEPLOYMENT.
IF YOU DEPLOY WITHOUT A SCHEMA LOCK, THE MIGRATION CAN CONFLICT WITH
ANOTHER DEPLOYMENT. SCHEMA CONFLICTS CAN CAUSE DATA CORRUPTION THAT
AFFECTS ALL TEAMS USING THE DATABASE.

Open the #db-deploys channel and request a lock before you run the
migration. Wait for the lock confirmation before you continue.
```

## Cross-References

- **Rule 1.1 (Use approved words):** The words in your risk explanation must come from the STE-Code dictionary. See the Canonical Synonym Table for substitutes (for example, replace non-approved verbs with their approved general-purpose equivalents such as use, set, check, make, get, remove, keep).
- **Rule 1.6 (Non-approved words only as technical nouns):** When a risk explanation must include a non-approved word (for example, `deadlock`, `thrashing`, `replay attack`), present it as a technical code noun and define it on first use.
- **Rule 1.10 (No slang, jargon, or regional terms):** A risk explanation that says "this will brick your deployment" fails Rule 1.10 and Rule 7.3 simultaneously. Replace "brick" with the specific consequence: "THIS WILL MAKE THE DEPLOYMENT PERMANENTLY UNAVAILABLE."
- **Rule 7.1 (Use clear, specific safety signal words):** The signal word (WARNING or CAUTION) sets the severity level. Rule 7.3 connects the signal word to the concrete consequence. A WARNING demands a risk of injury or data loss. A CAUTION demands a risk of incorrect results or system damage.
- **Rule 7.2 (Place safety instructions before the related step):** The instruction must come before the risky action. The risk explanation in Rule 7.3 comes immediately after the instruction, before the reader proceeds. The order is: signal word → instruction → risk explanation → action.
- **Rule 7.4 (Use imperative mood for instructions):** The instruction part of a Rule 7.3 warning must use imperative mood ("DO NOT USE"), not descriptive ("using this is not recommended"). The risk explanation part may use declarative mood to state the consequence.
- **Section 1 (Words):** All words in risk explanations follow the noun-verb-adjective rules of Section 1. A risk sentence like "This initiates a cascade failure" violates Rule 1.2 (initiate → start) and Rule 1.3 (cascade as unapproved modifier). The STE version: "This can start a sequence of failures."

> **See also:** Rule 7.1 — Use an Applicable Word (for Example, "Warning" or "Caution") to Identify the Level of Risk; Rule 7.2 — Start a Safety Instruction with a Clear and Accurate Command or Condition; Rule 7.4 — Use Imperative Mood for Instructions

## Grammar Notes

The original ASD-STE100 Rule 7.3 carries grammatical justification that adapts directly to code documentation.

**Causal connective "IF...THEN" structure.** The original spec uses "IF THEY FALL, PERMANENT DAMAGE TO THE PARTS CAN OCCUR." The "IF" clause states the violation (not obeying the instruction). The main clause states the consequence. This structure is mandatory for risk explanations in code documentation. Always state the violation first, then the consequence. Do not reverse the order: "PERMANENT DATA LOSS CAN OCCUR IF YOU DO NOT SET THE TIMEOUT" is grammatically correct but less effective because the reader processes the gravity before knowing the cause. The STE pattern puts cause before effect so the reader follows the logical chain.

**Modal verb "can" versus "will."** Use "can" for risks that are possible but not certain. Use "will" only for risks that are guaranteed. "A data race can cause incorrect results" (possible). "A build will fail if a required dependency is not declared" (guaranteed). Never use "may" — it introduces ambiguity about permission versus possibility, and STE restricts "may" to permission contexts only. Never use "might" — it is less direct than "can" and is listed as an unapproved word in the STE dictionary.

**Active voice in risk explanations.** The subject of a risk sentence must be the thing that causes harm, not an abstract noun. "Data loss can occur" identifies the concrete harm. "There can be a loss of data" is passive and indirect. The active form makes the risk tangible. For systemic risks where no single agent exists, use the system or component as the subject: "The database can reject inconsistent writes." "Inconsistent writes can be rejected" is passive and hides the agent.

**Article usage in risk statements.** Do not omit articles from risk explanations. "Buffer overflow can cause crash" is incorrect. Write: "A buffer overflow can cause a crash." The indefinite article "a" before "buffer overflow" establishes that any single overflow triggers the risk. The indefinite article before "crash" establishes the type of failure. Omitting articles makes the risk sound like a headline, not an explanation.

**Sentence length constraint.** Risk explanations can chain consequences, but each link in the chain must stay within the 20-word procedural limit. Break long causal chains into separate sentences: "WITHOUT A TIMEOUT, THE CONNECTION CAN HANG FOREVER. A HANGING CONNECTION CAN USE ALL AVAILABLE THREADS. EXHAUSTED THREADS CAN CAUSE THE SERVER TO REJECT NEW REQUESTS." Each sentence states one causal link. The cumulative effect is a multi-step risk chain that the reader can process incrementally.

**Avoid "ing" forms as main verbs in risk explanations.** Do not write: "Not setting the timeout causing the connection to hang." Write: "If you do not set the timeout, the connection can hang." The "-ing" form "causing" is a participle, not a main verb. The risk explanation requires a finite verb ("can hang") to form a complete clause that assigns the consequence to the violation.

**Avoid semicolons and nested clauses.** The causal relationship between violation and consequence must not depend on semicolons or deeply nested subordinate clauses. Write two simple sentences joined by the logical chain: "If you skip the migration, the schema does not match. A schema mismatch can cause query failures." Do not write: "If you skip the migration, which creates a schema mismatch that can cause query failures, the deployment will fail." The nested version buries the risk chain and exceeds the 2-level clause depth limit.

**Definite versus indefinite articles in multi-risk chains.** When a risk chain involves a series of consequences, use the indefinite article "a" for the first mention of each consequence and the definite article "the" for subsequent references to the same consequence: "An unhandled promise rejection can cause a memory leak. The memory leak can cause the process to use more memory over time." The shift from "a" to "the" signals to the reader that "the memory leak" refers back to the consequence just introduced. Do not use "this" as a determiner in risk chains ("This memory leak can cause...") — STE treats "this" without an explicit noun as potentially ambiguous. Always pair "this" with the noun it modifies: "This type of memory leak."

**Imperative versus declarative mood in compound warnings.** A complete Rule 7.3 instruction has two grammatical moods. The instruction is imperative: "DO NOT DISABLE TLS VERIFICATION." The risk explanation is declarative: "Without TLS verification, an attacker can decrypt the traffic." Do not mix moods within a single sentence. Do not write: "Do not disable TLS verification because an attacker can decrypt the traffic." The conjunction "because" weakens the imperative by making the instruction sound like a suggestion. Use a period and start a new sentence for the risk explanation. The pause between the command and the consequence gives the reader a moment to register the instruction before processing its justification.

## Practical Application

Apply Rule 7.3 during documentation review with this checklist:

1. Find every WARNING and CAUTION in the document.
2. For each, ask: "What happens if the reader ignores this?"
3. If the answer is not written after the instruction, add it.
4. Check that the risk explanation uses "can" (probabilistic) or "will" (guaranteed) correctly.
5. Verify the risk matches the signal word severity (WARNING = data loss/security, CAUTION = incorrect results/build failures).
6. Confirm the risk chain reads cause-first: "If you do X, Y can happen." Not effect-first: "Y can happen if you do X."
7. Break any risk explanation over 20 words into separate causal-link sentences.
8. Replace any "-ing" participles with finite verbs ("causing" → "can cause").
9. Replace "may" and "might" with "can" or "will."
10. Check that technical nouns in code formatting are defined on first use in the risk chain.

A document where every safety instruction carries a clear, specific risk explanation is a document developers trust. A document where instructions carry unexplained prohibitions is a document developers ignore. The difference is Rule 7.3.
