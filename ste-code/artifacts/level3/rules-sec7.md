# Level 3 — Section 7: Safety Instructions (Warnings and Cautions)

This slice covers STE-Code Rules 7.1, 7.2, and 7.3. It is the risk layer of the
standard: how to signal risk, how to open a safety instruction, and how to
explain what happens if the reader ignores it.

These rules apply to every form of code documentation: README files, API
reference docs, docstrings, inline comments, commit messages, error messages,
changelogs, release notes, and configuration files.

## How to use this slice

- Apply the rules in order 7.1 → 7.2 → 7.3. Each adds one required part of a
  complete safety instruction.
- 7.1 picks the signal word (WARNING or CAUTION) that matches the risk level.
- 7.2 opens the body with a clear command or a clear condition.
- 7.3 states the consequence, so the reader knows why the instruction matters.

A safety instruction is complete only when it has all three parts:

```
WARNING: [COMMAND OR CONDITION]. [CONSEQUENCE]. [RISK ESCALATION].
```

If the command is missing, the instruction is not actionable. If the consequence
is missing, the reader does not know why the command matters. Both are required.

## Rules at a glance

| Rule | One-line requirement | Hard limit |
|------|----------------------|------------|
| 7.1 Identify the level of risk | Use WARNING or CAUTION as the first word; match it to the real risk. | One signal word per instruction. |
| 7.2 Start with a command or condition | The first sentence after the colon is a command or a condition. | 20 words maximum for that sentence. |
| 7.3 Explain the risk | Name the concrete consequence in cause-first order. | No vague nouns ("problems," "issues"). |

## Risk level mapping

| Risk in the code domain | Signal word | Release-note severity |
|-------------------------|-------------|-----------------------|
| Security vulnerability, data loss, system corruption | WARNING | BREAKING |
| Unexpected behavior, performance degradation, incorrect results | CAUTION | DEPRECATED |
| Information only, no risk | NOTE | NOTE |

If two levels of risk apply together, use WARNING.

---

## Rule 7.1 — Use an Applicable Word to Identify the Level of Risk

> Adapted from ASD-STE100 Issue 9, Rule 7.1.

In code documentation, use a signal word (for example, WARNING or CAUTION) to
immediately show your reader the level of the related risk.

- If there is a risk of security vulnerabilities, data loss, or system
  corruption, use a WARNING.
- If there is a risk of unexpected behavior, performance degradation, or
  incorrect results, use a CAUTION.
- If the two levels of risk apply together, use a WARNING.

Do not let the signal word become routine noise. A document that marks every
note as a WARNING teaches the reader to ignore all of them.

### Escalation: choose the level from the real risk, not from the topic

An abstract caution must become a warning when the true risk is security or data
loss. This is the core move of the rule.

> **Non-STE:** CAUTION: ALWAYS VALIDATE INPUT DATA.
>
> **STE:** WARNING: BEFORE YOU PROCESS INPUT DATA, MAKE SURE THAT YOU SANITIZE AND VALIDATE THE DATA. UNSANITIZED INPUT CAN CAUSE SECURITY BREACHES AND DATA LOSS.

> **Non-STE:** CAUTION: THE CONFIGURATION FILE MAY CONTAIN OUTDATED SETTINGS.
>
> **STE:** CAUTION: BEFORE YOU DEPLOY THE APPLICATION, COMPARE THE CONFIGURATION FILE AGAINST THE REFERENCE CONFIGURATION. OUTDATED SETTINGS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.

The first pair escalates to WARNING because the true risk is a security breach.
The second stays a CAUTION because the risk is incorrect results only.

### By documentation type

| Type | Use WARNING for | Use CAUTION for |
|------|-----------------|-----------------|
| README | Security-critical setup steps | Configuration that can cause incorrect behavior |
| API docs | Sensitive data, authentication, destructive endpoints | Side effects, rate limits |
| Docstrings and comments | Misuse that corrupts data or breaks security | Performance pitfalls, non-obvious side effects |
| Commit messages | Security fixes, data-loss prevention | Behavior changes downstream consumers must know |
| Error messages | Detected security compromise or data corruption | Detected condition that gives incorrect results |

**README — WARNING:**

> **Non-STE:** Note: you should be careful with the API key and not commit it to version control.
>
> **STE:** WARNING: DO NOT COMMIT THE API KEY TO VERSION CONTROL. AN EXPOSED API KEY CAN CAUSE UNAUTHORIZED ACCESS AND DATA LOSS.

**README — CAUTION:**

> **Non-STE:** Make sure the port number does not conflict with other services or the app won't start.
>
> **STE:** CAUTION: BEFORE YOU START THE APPLICATION, CHECK THAT THE PORT NUMBER DOES NOT CONFLICT WITH OTHER SERVICES. A PORT CONFLICT CAN CAUSE THE APPLICATION TO FAIL.

**API docs — WARNING for a destructive endpoint:**

> **Non-STE:** DELETE /users/:id removes the user and all associated data, this cannot be undone.
>
> **STE:** WARNING: `DELETE /users/:id` REMOVES THE USER AND ALL RELATED DATA PERMANENTLY. THIS OPERATION CANNOT BE UNDONE. VERIFY THE USER ID BEFORE YOU SEND THE REQUEST.

**API docs — CAUTION for a rate limit:**

> **Non-STE:** This endpoint allows 100 requests per minute, exceeding this will return 429 errors.
>
> **STE:** CAUTION: THE ENDPOINT ALLOWS A MAXIMUM OF 100 REQUESTS PER MINUTE. IF YOU EXCEED THE LIMIT, THE ENDPOINT RETURNS A 429 ERROR. MONITOR THE `X-RateLimit-Remaining` HEADER.

**Docstring — WARNING (Python):**

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

**JSDoc — CAUTION (JavaScript):**

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
    if (cache.has(key)) return cache.get(key);
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  };
}
```

**Commit messages.** Use `WARNING:` as the type prefix for commits that fix
security vulnerabilities or prevent data loss. Use `CAUTION:` for commits that
change behavior downstream consumers depend on. Changelog tools can then group
commits by severity.

> **Non-STE:** fix: patch SQL injection in login form
>
> **STE:** WARNING: Prevent SQL injection in the login form. The previous code did not sanitize the `username` parameter. This vulnerability could permit unauthorized database access.

> **Non-STE:** change: update default timeout from 30s to 10s
>
> **STE:** CAUTION: Change the default timeout from 30 seconds to 10 seconds. Update all callers that rely on the previous default. The shorter timeout can cause connection failures in high-latency environments.

**Error messages.** Error messages are read during incidents. They must be
actionable.

> **Non-STE:** Error: invalid signature
>
> **STE:** WARNING: THE REQUEST SIGNATURE IS NOT VALID. THE REQUEST MAY HAVE BEEN TAMPERED WITH. REJECT THE REQUEST. CHECK YOUR SIGNING KEY AND ALGORITHM.

> **Non-STE:** The configuration value for max_connections must be less than database pool size.
>
> **STE:** CAUTION: THE `max_connections` VALUE IS GREATER THAN THE `pool_size` VALUE. THIS CONFIGURATION CAN CAUSE CONNECTION FAILURES. SET `max_connections` TO A VALUE THAT IS NOT MORE THAN `pool_size`.

### Paradigm notes for 7.1

| Paradigm | WARNING when | CAUTION when |
|----------|--------------|--------------|
| Object-oriented (Java, C++, C#, Python classes) | A subclass override can break a security invariant | A method mutates shared state |
| Functional (Haskell, Elixir, Clojure, Rust) | An unsafe escape hatch breaks referential transparency | A lazy operation can cause a space leak |
| Procedural (C, Go, Bash) | Buffer overflow, use-after-free, undefined behavior | Platform-specific behavior, resource limits |
| Declarative (SQL, Terraform, Kubernetes YAML) | Data destruction, public exposure of a resource | Configuration values with subtle effects |
| Systems (Rust ownership, C memory) | Undefined behavior, data races, memory corruption | Performance characteristics of unsafe optimizations |

**Object-oriented — WARNING (Java):**

> **Non-STE:** Subclasses should be careful to call super.validate() before performing custom validation.
>
> **STE:** WARNING: OVERRIDE THE `validate` METHOD WITH CARE. CALL `super.validate()` BEFORE YOU ADD CUSTOM VALIDATION LOGIC. IF YOU SKIP THE BASE VALIDATION, UNTRUSTED DATA CAN BYPASS SECURITY CHECKS.

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
        super.validate(request);
        PaymentRequest payment = (PaymentRequest) request;
        if (payment.getAmount() <= 0) {
            throw new IllegalArgumentException("Amount must be greater than zero");
        }
    }
}
```

**Object-oriented — CAUTION (C++ shared state):**

> **Non-STE:** Note that this method modifies the internal cache which may affect other threads.
>
> **STE:** CAUTION: THE `invalidateCache` METHOD MODIFIES THE INTERNAL CACHE. THIS CHANGE AFFECTS ALL THREADS THAT USE THE CACHE. USE A LOCK BEFORE YOU CALL THIS METHOD.

**Functional — WARNING and CAUTION (Haskell):**

> **Non-STE:** Use unsafePerformIO with caution as it breaks purity.
>
> **STE:** WARNING: `unsafePerformIO` BYPASSES THE IO TYPE SYSTEM. THIS FUNCTION HIDES SIDE EFFECTS IN PURE CODE. INCORRECT USE CAN CAUSE NONDETERMINISTIC BEHAVIOR AND DATA CORRUPTION. USE THIS FUNCTION ONLY WHEN NO SAFE ALTERNATIVE EXISTS.

> **Non-STE:** foldl is strict, but if you accumulate large thunks you might run out of memory.
>
> **STE:** CAUTION: `foldl` ACCUMULATES UNEVALUATED EXPRESSIONS (THUNKS). A LARGE ACCUMULATOR CAN CAUSE A SPACE LEAK AND MEMORY EXHAUSTION. USE `foldl'` FOR STRICT ACCUMULATION.

**Procedural — WARNING (C) and CAUTION (Go):**

> **Non-STE:** Make sure the destination buffer is at least as large as the source string when using strcpy.
>
> **STE:** WARNING: `strcpy` DOES NOT CHECK THE SIZE OF THE DESTINATION BUFFER. IF THE SOURCE STRING IS LARGER THAN THE DESTINATION BUFFER, THE FUNCTION WRITES PAST THE BUFFER BOUNDARY. THIS BUFFER OVERFLOW CAN CAUSE SECURITY VULNERABILITIES AND SYSTEM CRASHES. USE `strncpy` WITH A SIZE LIMIT.

> **Non-STE:** On Windows, filepath separator is backslash, be careful with cross-platform paths.
>
> **STE:** CAUTION: THE `filepath` PACKAGE USES THE OPERATING SYSTEM PATH SEPARATOR. USE `filepath.Join` OR `filepath.FromSlash` TO BUILD CROSS-PLATFORM PATHS. HARDCODED SEPARATORS CAUSE INCORRECT PATHS.

**Declarative — WARNING (SQL), CAUTION (Terraform), WARNING (Kubernetes):**

> **Non-STE:** Caution: this migration drops the users table.
>
> **STE:** WARNING: THIS MIGRATION DROPS THE `users` TABLE. ALL USER DATA IS DELETED PERMANENTLY. BACK UP THE DATABASE BEFORE YOU RUN THIS MIGRATION. VERIFY THAT YOU RUN THE MIGRATION AGAINST THE CORRECT DATABASE.

> **Non-STE:** Changing the subnet_id will cause the EC2 instance to be recreated, which may cause downtime.
>
> **STE:** CAUTION: IF YOU CHANGE THE `subnet_id` ARGUMENT, TERRAFORM DESTROYS THE EXISTING INSTANCE AND CREATES A NEW ONE. THIS RECREATION CAUSES DOWNTIME. THE INSTANCE PUBLIC IP ADDRESS CHANGES. PLAN THE CHANGE DURING A MAINTENANCE WINDOW.

> **Non-STE:** Be careful with LoadBalancer type services as they expose your app to the internet.
>
> **STE:** WARNING: A SERVICE OF TYPE `LoadBalancer` EXPOSES THE APPLICATION TO THE PUBLIC INTERNET. UNAUTHORIZED USERS CAN SEND REQUESTS TO THE APPLICATION. MAKE SURE THAT AUTHENTICATION AND NETWORK POLICIES ARE IN PLACE BEFORE YOU APPLY THIS CONFIGURATION.

**Systems — WARNING and CAUTION (Rust):**

> **Non-STE:** Dereferencing a raw pointer is unsafe and may cause undefined behavior if the pointer is invalid.
>
> **STE:** WARNING: DEREFERENCING A RAW POINTER CAN CAUSE UNDEFINED BEHAVIOR. UNDEFINED BEHAVIOR CAN CORRUPT MEMORY, CAUSE SECURITY VULNERABILITIES, AND CRASH THE PROGRAM. BEFORE YOU DEREFERENCE A RAW POINTER, CHECK THAT: (1) THE POINTER IS NOT NULL. (2) THE POINTER IS CORRECTLY ALIGNED. (3) THE POINTER POINTS TO VALID, INITIALIZED MEMORY.

> **Non-STE:** Using MaybeUninit can improve performance but be careful about initialization.
>
> **STE:** CAUTION: `MaybeUninit` SKIPS INITIALIZATION TO IMPROVE PERFORMANCE. IF YOU READ UNINITIALIZED MEMORY, THE PROGRAM BEHAVIOR IS UNDEFINED. MAKE SURE THAT YOU INITIALIZE THE VALUE BEFORE YOU READ IT. MEASURE THE PERFORMANCE GAIN BEFORE YOU USE THIS TYPE.

### Common signal-word failures

| Failure | Fix |
|---------|-----|
| CAUTION used for a security risk (exposed API key) | Escalate to WARNING; name unauthorized access, data theft, service abuse |
| WARNING with no consequence ("run this migration carefully") | Name the irrecoverable loss and give a pre-action check |
| Abstract caution ("be mindful of thread safety") | Name the class, the race, and the safe alternative |
| WARNING used for slowness | Downgrade to CAUTION; give the complexity, a threshold, and an alternative |
| No signal word at all | Add the signal word that matches the real risk |
| Two risks in one callout, marked CAUTION | If either risk is WARNING-level, use WARNING |

Worked corrections:

> **Non-STE:** CAUTION: Store the API key in an environment variable.
>
> **STE:** WARNING: STORE THE API KEY IN AN ENVIRONMENT VARIABLE. DO NOT HARDCODE THE API KEY IN THE SOURCE CODE. AN EXPOSED API KEY CAN CAUSE UNAUTHORIZED ACCESS, DATA THEFT, AND SERVICE ABUSE. ADD THE `.env` FILE TO `.gitignore`.

> **Non-STE:** WARNING: Run this migration carefully.
>
> **STE:** WARNING: BEFORE YOU RUN THIS MIGRATION, BACK UP THE `transactions` TABLE. THE MIGRATION REMOVES ALL RECORDS OLDER THAN 90 DAYS. THE DATA CANNOT BE RECOVERED AFTER THE MIGRATION COMPLETES. VERIFY THE DATE THRESHOLD AGAINST YOUR RETENTION POLICY.

> **Non-STE:** CAUTION: Be mindful of thread safety when using this library.
>
> **STE:** CAUTION: THE `Cache` CLASS IS NOT THREAD-SAFE. IF YOU SHARE A `Cache` INSTANCE ACROSS THREADS, RACE CONDITIONS CAN CAUSE INCORRECT CACHE ENTRIES AND APPLICATION CRASHES. USE `ConcurrentCache` FOR MULTI-THREADED APPLICATIONS. USE A MUTEX FOR MANUAL SYNCHRONIZATION.

> **Non-STE:** WARNING: This function is slow for large inputs.
>
> **STE:** CAUTION: THIS FUNCTION HAS O(N²) TIME COMPLEXITY. FOR INPUTS LARGER THAN 10,000 ITEMS, THE FUNCTION CAN TAKE SEVERAL MINUTES TO COMPLETE. USE `fastSort` FOR LARGE INPUTS. `fastSort` HAS O(N LOG N) TIME COMPLEXITY.

> **Non-STE:** The DEBUG_MODE environment variable controls verbose logging. Setting it to true in production will leak sensitive information.
>
> **STE:** WARNING: DO NOT SET `DEBUG_MODE=true` IN A PRODUCTION ENVIRONMENT. DEBUG MODE WRITES SENSITIVE DATA TO THE LOG OUTPUT. THIS DATA INCLUDES REQUEST BODIES, AUTHENTICATION TOKENS, AND DATABASE QUERIES. AN ATTACKER WITH LOG ACCESS CAN STEAL USER CREDENTIALS.

> **Non-STE:** CAUTION: The reset method clears the database and disables authentication, only use in development.
>
> **STE:** WARNING: THE `reset` METHOD CLEARS THE DATABASE AND DISABLES AUTHENTICATION. IF YOU CALL THIS METHOD IN A PRODUCTION ENVIRONMENT, ALL USER DATA IS DELETED AND ALL REQUESTS BYPASS AUTHENTICATION. THIS METHOD IS FOR DEVELOPMENT USE ONLY. CHECK THE `NODE_ENV` VARIABLE BEFORE YOU CALL THIS METHOD.

### Edge cases for 7.1

**The word "warning" is also a code identifier.** Some languages use it as a
name (`warnings` in Python, `#[allow(warnings)]` in Rust, `console.warn()` in
JavaScript). Put the identifier in backticks. Use plain uppercase for the signal
word.

> **Non-STE:** Warning: the warnings module suppresses warnings by default.
>
> **STE:** CAUTION: THE `warnings` MODULE SUPPRESSES WARNINGS BY DEFAULT. THE OUTPUT FROM `warn()` CALLS IS NOT SHOWN. CALL `warnings.simplefilter('always')` TO SHOW ALL WARNINGS.

**A third-party library uses a different convention.** Translate `DANGER`,
`CRITICAL`, or `IMPORTANT` into the STE-Code signal words. Do not replicate the
third-party convention.

> **Third-party:** DANGER: This operation is irreversible.
>
> **STE-Code:** WARNING: THIS OPERATION IS IRREVERSIBLE. THE DATA CANNOT BE RECOVERED AFTER THE OPERATION COMPLETES. BACK UP THE DATA BEFORE YOU START.

**Generated code inserts its own warnings.** Do not modify generated comments;
the generator overwrites them. Add your own signal word in the documentation
that wraps the generated code. If the generated warning misclassifies the risk,
open an issue with the generator project.

> **Generated (leave as-is):** `// CAUTION: This method is deprecated.`
>
> **Your wrapper:** WARNING: THE `legacy/client.go` FILE CONTAINS DEPRECATED METHODS. DEPRECATED METHODS MAY BE REMOVED IN A FUTURE VERSION. THE REMOVAL OF THESE METHODS CAN BREAK YOUR APPLICATION. MIGRATE TO THE `v2/client.go` API.

**A BREAKING change overlaps with a WARNING.** Use one signal word. Mention the
breaking nature in the body.

> **Non-STE:** BREAKING: WARNING: The encrypt function now requires a key parameter.
>
> **STE:** WARNING: THE `encrypt` FUNCTION NOW REQUIRES A `key` PARAMETER. THIS IS A BREAKING CHANGE. UPDATE ALL CALLERS TO PASS A KEY ARGUMENT. IF YOU DO NOT PASS A KEY, THE FUNCTION THROWS AN ERROR AND THE DATA IS NOT ENCRYPTED.

**Translation.** Translate the signal words with the standard term for each
language. Do not invent new signal words. Keep the format identical: uppercase
word, colon, single space.

| Language | WARNING | CAUTION |
|----------|---------|---------|
| English | WARNING | CAUTION |
| Spanish | ADVERTENCIA | PRECAUCIÓN |
| French | AVERTISSEMENT | ATTENTION |
| German | WARNUNG | VORSICHT |
| Japanese | 警告 | 注意 |

### Grammar notes for 7.1

- **Placement.** The signal word is the first word of the instruction. Do not
  indent it. Do not put text before it (`Important: WARNING: ...` is wrong).
- **Punctuation.** The signal word is followed by a colon and one space.
- **Case.** Write the signal word in uppercase. Uppercase is part of the signal,
  not emphasis. `Warning:` and `warning:` are both wrong.
- **Structure.** Command or condition → consequence → risk escalation, in that
  order, in one sentence or several.
- **Verb form.** Imperative mood. Use "do not" for prohibitions. Do not use
  "should," "must," or "needs to."
- **Visual distinction.** In rendered output the signal word must stand out:
  bold, color, or a border in Markdown/HTML; an admonition directive
  (`.. WARNING::`) in reStructuredText. Do not rely on uppercase alone.

**Risk vocabulary.** Name the risk with a specific noun. Do not write
"problems," "issues," or "trouble."

| WARNING-level risk nouns | CAUTION-level risk nouns |
|--------------------------|--------------------------|
| Security breach | Unexpected behavior |
| Data loss | Performance degradation |
| System corruption | Incorrect results |
| Unauthorized access | Connection failure |
| Credential theft | Memory exhaustion |
| Data leak | Application crash |
| Privilege escalation | Configuration drift |

### Checklist for 7.1

- [ ] The signal word matches the real risk level, not the topic.
- [ ] Security, data loss, and system corruption use WARNING.
- [ ] Unexpected behavior, performance, and incorrect results use CAUTION.
- [ ] Mixed levels with one WARNING-level risk use WARNING.
- [ ] The signal word is first, uppercase, followed by a colon and a space.
- [ ] Only one signal word per instruction.
- [ ] The risk noun is specific, not vague.
- [ ] Technical code nouns are in backticks.
- [ ] Third-party conventions are translated, not copied.
- [ ] The signal word is visually distinct in the rendered output.

**See also:** Rule 5.3 (imperative form), Rule 7.2 (command or condition first),
Rule 7.3 (risk explanation), Rules 1.1/1.6/1.10/1.11 (approved words, one term
per concept).

---
