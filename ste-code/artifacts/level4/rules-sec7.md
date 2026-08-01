# Level 4 — Section 7: Safety Instructions (Rules 7.1–7.3)

This slice distills **Section 7 (Safety Instructions)** of the STE-Code controlled
standard for people who use LLMs to generate code documentation. Sections 1–6 control
words, sentences, and paragraphs. Section 7 controls the one construct that must never
be misread: the safety instruction.

A safety instruction is any callout that tells a reader an action can harm the system,
the data, or the users. In code documentation it appears in README files, API
reference docs, docstrings, inline comments, commit messages, error messages,
changelogs, release notes, and configuration files.

## The three rules at a glance

| Rule | Requirement | Failure signal |
|---|---|---|
| 7.1 | Use a signal word (`WARNING` / `CAUTION`) that matches the level of risk. | `CAUTION` on a credential leak; `WARNING` on a slow function. |
| 7.2 | Start the body with a clear command or a clear condition. | The callout opens with background prose or with the consequence. |
| 7.3 | Give the risk or possible result. | `DO NOT USE eval().` with no explanation of what happens. |

A complete safety instruction has three parts, always in this order:

```
<SIGNAL WORD>: <COMMAND or CONDITION>. <CONSEQUENCE>. <RISK ESCALATION>.
```

Remove the signal word and the reader cannot triage. Remove the command and the
instruction is not actionable. Remove the consequence and the reader dismisses it.

## Severity model

| Signal word | Use for | Changelog / release-note level |
|---|---|---|
| `WARNING` | Security vulnerability, data loss, system corruption, service unavailability. | `BREAKING` |
| `CAUTION` | Unexpected behavior, performance degradation, incorrect results, build failure. | `DEPRECATED` |
| `NOTE` | Information with no risk. | `NOTE` |

When two levels of risk occur together, use `WARNING`. Use one signal word only — never
`BREAKING: WARNING:`. Mention the breaking nature in the body instead.

---

## Rule 7.1 — Use a signal word that identifies the level of risk

**Rule.** In code documentation, use a signal word (for example, `WARNING` or `CAUTION`)
to immediately show your reader the level of the related risk.

- Risk of security vulnerabilities, data loss, or system corruption → `WARNING`.
- Risk of unexpected behavior, performance degradation, or incorrect results → `CAUTION`.
- Two levels of risk together → `WARNING`.

The signal word is a classification, not emphasis. Do not let it become routine noise:
a document where every callout is a `WARNING` has no signal at all.

### Escalation: the core pattern

> **Non-STE:** CAUTION: ALWAYS VALIDATE INPUT DATA.
>
> **STE:** WARNING: BEFORE YOU PROCESS INPUT DATA, MAKE SURE THAT YOU SANITIZE AND
> VALIDATE THE DATA. UNSANITIZED INPUT CAN CAUSE SECURITY BREACHES AND DATA LOSS.

The original names an abstract obligation and classifies it as `CAUTION`. The true risk
is a security breach and data loss, so the correct signal word is `WARNING`. The STE
version escalates the signal word, gives a command, and names the risk.

The mirror case is over-classification:

> **Non-STE:** WARNING: This function is slow for large inputs.
>
> **STE:** CAUTION: THIS FUNCTION HAS O(N²) TIME COMPLEXITY. FOR INPUTS LARGER THAN
> 10,000 ITEMS, THE FUNCTION CAN TAKE SEVERAL MINUTES TO COMPLETE. USE `fastSort` FOR
> LARGE INPUTS. `fastSort` HAS O(N LOG N) TIME COMPLEXITY.

Performance degradation is a `CAUTION`-level risk. Downgrade, give a threshold, and
give an alternative.

### By documentation type

| Type | Use `WARNING` for | Use `CAUTION` for |
|---|---|---|
| README | Security-critical setup steps. | Configuration that can cause incorrect behavior. |
| API docs | Sensitive data, authentication, destructive endpoints. | Side effects, rate limits. |
| Docstrings / comments | Functions that can cause vulnerabilities or corruption. | Performance pitfalls, non-obvious side effects. |
| Commit messages | Security fixes, data-loss prevention. | Behavior changes downstream consumers must know. |
| Error messages | Detected compromise or corruption conditions. | Detected conditions that give incorrect results. |

Place the signal word at the top of the relevant section. Do not bury it in a paragraph.

**README — `WARNING` (security) and `CAUTION` (configuration):**

> **STE:** WARNING: DO NOT COMMIT THE API KEY TO VERSION CONTROL. AN EXPOSED API KEY
> CAN CAUSE UNAUTHORIZED ACCESS AND DATA LOSS.

> **STE:** CAUTION: BEFORE YOU START THE APPLICATION, CHECK THAT THE PORT NUMBER DOES
> NOT CONFLICT WITH OTHER SERVICES. A PORT CONFLICT CAN CAUSE THE APPLICATION TO FAIL.

**API documentation — destructive endpoint and rate limit:**

> **STE:** WARNING: `DELETE /users/:id` REMOVES THE USER AND ALL RELATED DATA
> PERMANENTLY. THIS OPERATION CANNOT BE UNDONE. VERIFY THE USER ID BEFORE YOU SEND THE
> REQUEST.

> **STE:** CAUTION: THE ENDPOINT ALLOWS A MAXIMUM OF 100 REQUESTS PER MINUTE. IF YOU
> EXCEED THE LIMIT, THE ENDPOINT RETURNS A 429 ERROR. MONITOR THE
> `X-RateLimit-Remaining` HEADER.

**Docstring — `WARNING` for a security-sensitive contract:**

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

**JSDoc — `CAUTION` for a performance contract:**

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
```

**Commit messages** may use the signal word as the type prefix, which lets changelog
tools group commits by severity:

> **STE:** WARNING: Prevent SQL injection in the login form. The previous code did not
> sanitize the `username` parameter. This vulnerability could permit unauthorized
> database access.

> **STE:** CAUTION: Change the default timeout from 30 seconds to 10 seconds. Update
> all callers that rely on the previous default. The shorter timeout can cause
> connection failures in high-latency environments.

**Error messages** are read during incidents, so they must be actionable:

> **STE:** WARNING: THE REQUEST SIGNATURE IS NOT VALID. THE REQUEST MAY HAVE BEEN
> TAMPERED WITH. REJECT THE REQUEST. CHECK YOUR SIGNING KEY AND ALGORITHM.

> **STE:** CAUTION: THE `max_connections` VALUE IS GREATER THAN THE `pool_size` VALUE.
> THIS CONFIGURATION CAN CAUSE CONNECTION FAILURES. SET `max_connections` TO A VALUE
> THAT IS NOT MORE THAN `pool_size`.

### By paradigm

| Paradigm | `WARNING` triggers | `CAUTION` triggers |
|---|---|---|
| Object-oriented | A subclass override that breaks a security invariant. | A method that mutates shared state. |
| Functional | An unsafe escape hatch that breaks referential transparency. | A lazy operation that can cause a space leak. |
| Procedural | Buffer overflow, use-after-free, undefined behavior. | Platform-specific behavior, resource limits. |
| Declarative | Data destruction, public exposure of a resource. | Values with subtle effects on behavior. |
| Systems | Undefined behavior, data races, memory corruption. | Performance tradeoffs of unsafe optimizations. |

**Object-oriented — override that must preserve a security invariant (Java):**

> **STE:** WARNING: OVERRIDE THE `validate` METHOD WITH CARE. CALL `super.validate()`
> BEFORE YOU ADD CUSTOM VALIDATION LOGIC. IF YOU SKIP THE BASE VALIDATION, UNTRUSTED
> DATA CAN BYPASS SECURITY CHECKS.

```java
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

**Object-oriented — mutable shared state (C++):**

> **STE:** CAUTION: THE `invalidateCache` METHOD MODIFIES THE INTERNAL CACHE. THIS
> CHANGE AFFECTS ALL THREADS THAT USE THE CACHE. USE A LOCK BEFORE YOU CALL THIS METHOD.

**Functional — escape hatch and space leak (Haskell):**

> **STE:** WARNING: `unsafePerformIO` BYPASSES THE IO TYPE SYSTEM. THIS FUNCTION HIDES
> SIDE EFFECTS IN PURE CODE. INCORRECT USE CAN CAUSE NONDETERMINISTIC BEHAVIOR AND DATA
> CORRUPTION. USE THIS FUNCTION ONLY WHEN NO SAFE ALTERNATIVE EXISTS.

> **STE:** CAUTION: `foldl` ACCUMULATES UNEVALUATED EXPRESSIONS (THUNKS). A LARGE
> ACCUMULATOR CAN CAUSE A SPACE LEAK AND MEMORY EXHAUSTION. USE `foldl'` FOR STRICT
> ACCUMULATION.

**Procedural — buffer overflow (C) and platform behavior (Go):**

> **STE:** WARNING: `strcpy` DOES NOT CHECK THE SIZE OF THE DESTINATION BUFFER. IF THE
> SOURCE STRING IS LARGER THAN THE DESTINATION BUFFER, THE FUNCTION WRITES PAST THE
> BUFFER BOUNDARY. THIS BUFFER OVERFLOW CAN CAUSE SECURITY VULNERABILITIES AND SYSTEM
> CRASHES. USE `strncpy` WITH A SIZE LIMIT.

> **STE:** CAUTION: THE `filepath` PACKAGE USES THE OPERATING SYSTEM PATH SEPARATOR.
> USE `filepath.Join` OR `filepath.FromSlash` TO BUILD CROSS-PLATFORM PATHS. HARDCODED
> SEPARATORS CAUSE INCORRECT PATHS.

**Declarative — destructive SQL, Terraform recreation, public exposure:**

> **STE:** WARNING: THIS MIGRATION DROPS THE `users` TABLE. ALL USER DATA IS DELETED
> PERMANENTLY. BACK UP THE DATABASE BEFORE YOU RUN THIS MIGRATION. VERIFY THAT YOU RUN
> THE MIGRATION AGAINST THE CORRECT DATABASE.

> **STE:** CAUTION: IF YOU CHANGE THE `subnet_id` ARGUMENT, TERRAFORM DESTROYS THE
> EXISTING EC2 INSTANCE AND CREATES A NEW ONE. THIS RECREATION CAUSES DOWNTIME. THE
> INSTANCE PUBLIC IP ADDRESS CHANGES. PLAN THE CHANGE DURING A MAINTENANCE WINDOW.

> **STE:** WARNING: A SERVICE OF TYPE `LoadBalancer` EXPOSES THE APPLICATION TO THE
> PUBLIC INTERNET. UNAUTHORIZED USERS CAN SEND REQUESTS TO THE APPLICATION. MAKE SURE
> THAT AUTHENTICATION AND NETWORK POLICIES ARE IN PLACE BEFORE YOU APPLY THIS
> CONFIGURATION.

**Systems — undefined behavior (Rust) and an unsafe optimization:**

> **STE:** WARNING: DEREFERENCING A RAW POINTER CAN CAUSE UNDEFINED BEHAVIOR. UNDEFINED
> BEHAVIOR CAN CORRUPT MEMORY, CAUSE SECURITY VULNERABILITIES, AND CRASH THE PROGRAM.
> BEFORE YOU DEREFERENCE A RAW POINTER, CHECK THAT: (1) THE POINTER IS NOT NULL.
> (2) THE POINTER IS CORRECTLY ALIGNED. (3) THE POINTER POINTS TO VALID, INITIALIZED
> MEMORY.

> **STE:** CAUTION: `MaybeUninit` SKIPS INITIALIZATION TO IMPROVE PERFORMANCE. IF YOU
> READ UNINITIALIZED MEMORY, THE PROGRAM BEHAVIOR IS UNDEFINED. MAKE SURE THAT YOU
> INITIALIZE THE VALUE BEFORE YOU READ IT. MEASURE THE PERFORMANCE GAIN BEFORE YOU USE
> THIS TYPE.

### Six classification failures

**1 — Under-classified security risk.**

> **Non-STE:** CAUTION: Store the API key in an environment variable.
>
> **STE:** WARNING: STORE THE API KEY IN AN ENVIRONMENT VARIABLE. DO NOT HARDCODE THE
> API KEY IN THE SOURCE CODE. AN EXPOSED API KEY CAN CAUSE UNAUTHORIZED ACCESS, DATA
> THEFT, AND SERVICE ABUSE. ADD THE `.env` FILE TO `.gitignore`.

**2 — Correct signal word, missing consequence.**

> **Non-STE:** WARNING: Run this migration carefully.
>
> **STE:** WARNING: BEFORE YOU RUN THIS MIGRATION, BACK UP THE `transactions` TABLE.
> THE MIGRATION REMOVES ALL RECORDS OLDER THAN 90 DAYS. THE DATA CANNOT BE RECOVERED
> AFTER THE MIGRATION COMPLETES. VERIFY THE DATE THRESHOLD AGAINST YOUR RETENTION
> POLICY.

**3 — Abstract caution.**

> **Non-STE:** CAUTION: Be mindful of thread safety when using this library.
>
> **STE:** CAUTION: THE `Cache` CLASS IS NOT THREAD-SAFE. IF YOU SHARE A `Cache`
> INSTANCE ACROSS THREADS, RACE CONDITIONS CAN CAUSE INCORRECT CACHE ENTRIES AND
> APPLICATION CRASHES. USE `ConcurrentCache` FOR MULTI-THREADED APPLICATIONS. USE A
> MUTEX FOR MANUAL SYNCHRONIZATION.

**4 — Over-classified performance risk.** See the O(N²) example above. Performance is a
`CAUTION`, so downgrade the signal word, give a threshold, and give an alternative.

**5 — No signal word at all.**

> **Non-STE:** The DEBUG_MODE environment variable controls verbose logging. Setting it
> to true in production will leak sensitive information.
>
> **STE:** WARNING: DO NOT SET `DEBUG_MODE=true` IN A PRODUCTION ENVIRONMENT. DEBUG
> MODE WRITES SENSITIVE DATA TO THE LOG OUTPUT. THIS DATA INCLUDES REQUEST BODIES,
> AUTHENTICATION TOKENS, AND DATABASE QUERIES. AN ATTACKER WITH LOG ACCESS CAN STEAL
> USER CREDENTIALS.

**6 — Mixed levels in one callout.**

> **Non-STE:** CAUTION: The reset method clears the database and disables
> authentication, only use in development.
>
> **STE:** WARNING: THE `reset` METHOD CLEARS THE DATABASE AND DISABLES
> AUTHENTICATION. IF YOU CALL THIS METHOD IN A PRODUCTION ENVIRONMENT, ALL USER DATA IS
> DELETED AND ALL REQUESTS BYPASS AUTHENTICATION. THIS METHOD IS FOR DEVELOPMENT USE
> ONLY. CHECK THE `NODE_ENV` VARIABLE BEFORE YOU CALL THIS METHOD.

### Edge cases

**A framework uses "warning" as a name.** Python's `warnings`, Rust's
`#[allow(warnings)]`, and `console.warn()` are technical code nouns. Put them in
backticks; reserve bare uppercase `WARNING` for the signal word.

> **STE:** CAUTION: THE `warnings` MODULE SUPPRESSES WARNINGS BY DEFAULT. THE OUTPUT
> FROM `warn()` CALLS IS NOT SHOWN. CALL `warnings.simplefilter('always')` TO SHOW ALL
> WARNINGS.

**A third-party library uses a different convention.** Translate `DANGER`, `CRITICAL`,
or `IMPORTANT` into the STE-Code signal word for the actual risk level. Do not
replicate the foreign convention.

**Generated code carries auto-inserted callouts.** Do not edit generated comments — the
generator overwrites them. Add your own signal word in the documentation that wraps the
generated code. If the generator misclassifies a risk, open an issue with that project.

**A breaking change overlaps with a warning.** Use `WARNING` and state the breaking
nature in the body: `WARNING: THE `encrypt` FUNCTION NOW REQUIRES A `key` PARAMETER.
THIS IS A BREAKING CHANGE. UPDATE ALL CALLERS TO PASS A KEY ARGUMENT.`

**Translated documentation.** Translate the signal word with the standard term for each
language and keep the format (uppercase, colon, single space). Maintain a glossary.

| Language | WARNING | CAUTION |
|---|---|---|
| English | WARNING | CAUTION |
| Spanish | ADVERTENCIA | PRECAUCIÓN |
| French | AVERTISSEMENT | ATTENTION |
| German | WARNUNG | VORSICHT |
| Japanese | 警告 | 注意 |

### Grammar notes for Rule 7.1

- **Placement.** The signal word is the first word of the instruction, at the start of
  the line, with nothing before it. `Important: WARNING: …` is wrong.
- **Punctuation.** Signal word, colon, one space, then the instruction.
- **Case.** Uppercase the signal word. Uppercase is part of the signal, not emphasis.
  `Warning:` and `warning:` are both wrong.
- **Structure.** Command or condition → consequence → risk escalation, in that order.
- **Verb form.** Imperative only. Use `DO NOT` for prohibitions. Do not use "should",
  "must", or "needs to". Technical verbs (`sanitize`, `validate`, `encrypt`, `back up`)
  are approved under Rule 1.12 and are used in the imperative.
- **Visual distinction.** In rendered output the signal word must stand out on its own:
  a bold blockquote in Markdown, a `<div>` with a CSS class in HTML, an admonition
  directive (`.. WARNING::`) in reStructuredText. Do not rely on uppercase alone.

**Risk vocabulary.** Name the specific risk. Never write "problems", "issues", or
"trouble".

| `WARNING` consequences | `CAUTION` consequences |
|---|---|
| Security breach | Unexpected behavior |
| Data loss | Performance degradation |
| System corruption | Incorrect results |
| Unauthorized access | Connection failure |
| Credential theft | Memory exhaustion |
| Data leak | Application crash |
| Privilege escalation | Configuration drift |

---

## Rule 7.2 — Start a safety instruction with a clear command or condition

**Rule.** In code documentation, start a safety instruction with a clear and accurate
command or condition. Your reader must know how to prevent security vulnerabilities,
data loss, and system failures. If your reader must know about a condition before they
use a function, method, or API, give this condition first.

The signal word tells the reader *how bad*. The first sentence of the body must tell
the reader *what to do*, within the first few words. The reader must not read through
background information before learning the action.

### Command-first structure

A command-first instruction starts with an imperative verb. The three common forms:

| Form | Pattern | Example |
|---|---|---|
| Prohibition | `DO NOT <action>` | `DO NOT COMMIT THE .env FILE.` |
| Mandatory action | `ALWAYS <action>` | `ALWAYS SANITIZE THE INPUT BEFORE YOU PROCESS IT.` |
| Direct action | `<imperative verb>` | `CHECK`, `MAKE SURE`, `BACK UP`, `SANITIZE`, `VALIDATE`, `VERIFY` |

Use approved verbs — `use`, `check`, `make`, `get`, `set`, `send`, `remove`, `keep`,
`start`, `stop`, `show`, `do` — not `utilize`, `leverage`, `employ`, `commence`,
`terminate`, or `initiate`.

> **Non-STE:** WARNING: STORING API KEYS IN THE SOURCE CODE IS NOT RECOMMENDED.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE ENVIRONMENT
> VARIABLES OR A SECRETS MANAGER TO STORE API KEYS. API KEYS IN SOURCE CODE CAN CAUSE
> UNAUTHORIZED ACCESS AND DATA BREACHES.

The non-STE version describes an attitude ("is not recommended"). The STE version opens
with the command `DO NOT STORE`, gives the required alternative, and names the
consequence.

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

> **Non-STE:** CAUTION: THE CODEBASE CONTAINS DEPRECATED FUNCTIONS.
>
> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS OR METHODS THAT HAVE KNOWN ISSUES.
> USE THE APPROVED REPLACEMENT FUNCTIONS SPECIFIED IN THE MIGRATION GUIDE. DEPRECATED
> FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.

The non-STE version only reports the presence of deprecated code. The STE version opens
with the prohibition, names the replacement, and states the consequence.

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

### Condition-first structure

Use a condition first when the risk applies only under a specific state, version, or
configuration. The condition scopes the instruction so readers outside that scope know
it does not apply to them.

> **Non-STE:** PERMANENT DATA LOSS CAN OCCUR.
>
> **STE:** IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN BECOME
> UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.

The non-STE version states only the consequence. The STE version opens with the
condition so the reader learns *when* the risk applies.

```go
// WARNING: IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION
// CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.
func NewClient(dsn string) (*Client, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }
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

When both a command and a condition are required, **put the condition first**. The
condition tells the reader when the command applies; the command tells them what to do.

### Six structural failures

**1 — Missing command (description only).**

> **Non-STE:** Storing API keys in plaintext configuration files is a security risk.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN PLAINTEXT CONFIGURATION FILES. STORE API
> KEYS IN ENVIRONMENT VARIABLES OR A SECRETS MANAGER. PLAINTEXT API KEYS IN VERSION
> CONTROL CAN CAUSE UNAUTHORIZED ACCESS AND DATA THEFT.

**2 — Missing condition (consequence only).**

> **Non-STE:** Transactions can fail silently.
>
> **STE:** WARNING: IF YOU DO NOT CHECK THE RETURN VALUE OF `transaction.commit()`, THE
> TRANSACTION CAN FAIL SILENTLY. DATA THAT YOU THINK IS SAVED IS NOT SAVED. THIS SILENT
> DATA LOSS CAN CAUSE APPLICATION INCONSISTENCY. CHECK THE RETURN VALUE AND HANDLE THE
> `RollbackError` CASE.

**3 — Command buried in background information.**

> **Non-STE:** Because environments drift over time and templates diverge, you should
> probably not keep separate configuration templates per environment.
>
> **STE:** WARNING: DO NOT USE DIFFERENT CONFIGURATION TEMPLATES FOR EACH ENVIRONMENT.
> USE THE SAME TEMPLATE FOR ALL ENVIRONMENTS. VERIFY THE CONFIGURATION BEFORE EACH
> DEPLOYMENT. CONFIGURATION DRIFT CAN CAUSE PRODUCTION INCIDENTS AND SERVICE
> UNAVAILABILITY.

**4 — Wrong order (consequence before condition).**

> **Non-STE:** Data is removed permanently if you run the cleanup script without an
> export.
>
> **STE:** WARNING: BEFORE YOU RUN THE CLEANUP SCRIPT, EXPORT THE DATA. IF YOU DO NOT
> EXPORT THE DATA, THE SCRIPT REMOVES THE DATA PERMANENTLY. THE DATA CANNOT BE
> RECOVERED. RUN `export-data --output backup.json` AND VERIFY THE FILE BEFORE YOU RUN
> THE CLEANUP SCRIPT.

**5 — Passive voice instead of a command.**

> **Non-STE:** Input data should be validated before it is processed by the pipeline.
>
> **STE:** CAUTION: VALIDATE THE INPUT DATA BEFORE THE PIPELINE PROCESSES IT. IF THE
> PIPELINE PROCESSES INVALID DATA, THE OUTPUT CAN BE INCORRECT. THE INCORRECT OUTPUT
> CAN PROPAGATE TO DOWNSTREAM SYSTEMS. USE THE `validateSchema` FUNCTION TO CHECK THE
> DATA STRUCTURE AND TYPES.

**6 — Multiple commands without hierarchy.**

> **STE:** WARNING: BEFORE YOU PROCESS THE REQUEST, COMPLETE THESE CHECKS:
> (1) SANITIZE ALL INPUT DATA. (2) USE PARAMETERIZED SQL QUERIES. (3) VALIDATE THE
> RETURN TYPES. (4) VERIFY THE AUTHENTICATION TOKEN. IF YOU SKIP ANY CHECK, A SECURITY
> BREACH OR DATA LOSS CAN OCCUR.

### Edge cases

**A framework method name is also a command word.** Use the plain uppercase word as the
command and backticks for the method reference.

> **STE:** WARNING: CHECK THE RETURN VALUE OF THE `check()` METHOD BEFORE YOU CONTINUE.
> IF `check()` RETURNS `false`, THE AUTHENTICATION IS NOT VALID. DO NOT PROCESS THE
> REQUEST. AN INVALID AUTHENTICATION CAN PERMIT UNAUTHORIZED ACCESS.

**The condition is true only for a subset of users.** Scope it with `IF` instead of
writing a command that is wrong for everyone else.

> **STE:** WARNING: IF YOU USE NODE.JS BEFORE VERSION 18, DO NOT USE THE `fetch` API.
> THE `fetch` API IS NOT AVAILABLE IN NODE.JS BEFORE VERSION 18. YOUR APPLICATION
> CRASHES WITH A `ReferenceError`. USE `node-fetch` OR UPGRADE TO NODE.JS 18 OR LATER.

**Both a command and a condition are required.** Condition first, then command.

```bash
# WARNING: BEFORE YOU RUN THE SCHEMA UPDATE, CONNECT TO THE CORRECT
# DATABASE. RUN THE MIGRATION TOOL WITH THE `--check` FLAG. IF YOU RUN
# THE SCHEMA UPDATE ON THE WRONG DATABASE, THE SCHEMA IS CORRUPTED AND
# THE APPLICATION CANNOT START.
export DATABASE_URL="postgres://app@staging:5432/app"
migrate --check        # fails fast if the connection is wrong
migrate up             # only reaches here on the correct database
```

**The instruction references generated code.** Leave the generated comment alone and add
your own command-first instruction above the generated block.

> **STE:** WARNING: DO NOT EDIT THE `generated/` DIRECTORY MANUALLY. THE GENERATOR
> OVERWRITES YOUR CHANGES ON THE NEXT BUILD. IF YOU CHANGE THE GENERATED CODE, YOUR
> CHANGES ARE LOST. EDIT THE `.proto` SOURCE FILE AND RUN THE GENERATOR AGAIN.

**Translation.** Command words (`DO NOT`, `ALWAYS`, `CHECK`, `MAKE SURE`) and condition
words (`IF`, `BEFORE`, `WHEN`) are translated too, and they stay first after the
translated signal word. The word order rules do not change per language.

| Language | DO NOT | ALWAYS | IF | BEFORE YOU |
|---|---|---|---|---|
| English | DO NOT | ALWAYS | IF | BEFORE YOU |
| Spanish | NO | SIEMPRE | SI | ANTES DE |
| French | NE PAS | TOUJOURS | SI | AVANT DE |
| German | NICHT | IMMER | WENN | BEVOR SIE |
| Japanese | 禁止 | 必ず | 場合 | 前に |

### Grammar notes for Rule 7.2

- **Four imperative forms.** Positive (`CHECK THE RETURN VALUE.`), negative
  (`DO NOT COMMIT THE API KEY.`), emphatic (`ALWAYS SANITIZE THE INPUT.`), and
  sequence (`BEFORE YOU <action>, <command>.`).
- **No modal verbs.** "You should check…" and "The value must be checked…" both weaken
  the instruction. Write `CHECK THE RETURN VALUE BEFORE YOU CONTINUE.`
- **Condition clauses** use `IF`, `BEFORE`, `WHEN`, `UNLESS` and stay in the present
  tense: `IF YOU DO NOT SET THE TIMEOUT, THE APPLICATION HANGS.` — not "IF YOU WILL NOT
  SET…".
- **Length.** The command or condition sentence is 20 words or fewer. Split longer
  instructions into a command sentence plus explanation sentences.
- **Punctuation.** Colon and one space after the signal word; a period at the end of
  each sentence; no semicolons joining command and consequence.
- **Parallel structure.** Multiple commands use the same verb form and a numbered list.
- **"Make sure"** is for verifying existing state (`MAKE SURE THAT THE DATABASE
  CONNECTION IS OPEN BEFORE YOU RUN THE QUERY.`). For an action the reader performs, a
  direct imperative is better (`SANITIZE THE INPUT DATA…`).
