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
