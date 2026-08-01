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
