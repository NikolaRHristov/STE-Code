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

### Code-Domain Explanation

Rule 7.3 addresses a fundamental gap in software documentation: instructions that tell the reader _what_ to avoid but not _why_ the avoidance matters. In aerospace, a mechanic who understands that a solvent is poisonous will handle it more carefully. In code, a developer who understands that an omitted timeout causes data loss will take the instruction seriously.

The rule applies differently across documentation types:

**README files.** README files give setup instructions and usage warnings. A README that says "do not use Node.js versions below 18" without explanation leaves new contributors vulnerable. The README must add: "Node.js versions below 18 do not include the `fetch` API. The application uses `fetch` for all network requests. If you use a version below 18, the requests will fail without an error message." The risk explanation connects the prohibition to a specific, observable failure.

**API documentation.** API docs describe function contracts. A docstring that says "do not pass null" is incomplete. It must also say: "If you pass null, the function throws a `NullPointerException` and the transaction is not committed. Uncommitted transactions can cause database lock contention." The reader now understands the cascading effect, not just the immediate error.

**Docstrings and inline comments.** Docstrings carry both usage notes and warnings. A docstring that says "this function is not thread-safe" without explanation is ignored. The docstring must add: "If two goroutines call this function at the same time, the internal map can become corrupt. Map corruption causes silent data loss because no error is returned." The risk explanation transforms an abstract property into a concrete hazard.

**Commit messages.** Commit messages serve as historical records and review context. A commit that says "remove the `--force` flag from the deploy script" documents a change. The body must add: "If the `--force` flag is used, the deploy script overwrites the production database without confirmation. Overwriting the production database can cause permanent loss of user data." Future readers who consider reintroducing the flag will see the recorded risk.

**Error messages.** Error messages are the last line of defense. An error that says "configuration not found" tells the user a fact. A better error says: "The configuration file `config.toml` was not found. The application cannot start without this file. If the application starts without configuration, it uses unsafe default values that can expose sensitive data in logs." The risk explanation turns a missing-file notice into an actionable security warning.

**Changelogs and release notes.** A changelog entry that says "BREAKING: removed the `legacy_auth` module" tells users about a deletion. It must also say: "If your code imports `legacy_auth`, the build will fail. You must replace all imports with the `auth_v2` module. A build failure can delay your deployment and cause service downtime." The risk explanation helps users plan their migration. A changelog without risk explanations is a list of facts. A changelog with risk explanations is a migration guide.

**The risk explanation must match the signal word level.** The original ASD-STE100 defines two severity levels: WARNING (risk of injury or death) and CAUTION (risk of equipment damage). In code documentation, WARNING maps to data loss, security breach, or system unavailability. CAUTION maps to incorrect results, degraded performance, or build failures. A risk explanation under a WARNING must describe a severe outcome. A risk explanation under a CAUTION must describe a moderate outcome. Do not use WARNING for a build failure. Do not use CAUTION for a data breach. Mismatched severity erodes trust in all safety instructions in the document.

### Paradigm-Specific Guidance

**Object-Oriented (Java, C++, C#, Python classes).** In OOP, risk explanations often involve state corruption and inheritance contracts. A warning about a mutable field must explain that subclasses can modify the field in unexpected ways. A caution about a non-final method must explain that overriding can violate the base class invariant.

> **Non-STE:** CAUTION: DO NOT OVERRIDE THE `initialize()` METHOD.
>
> **STE:** CAUTION: DO NOT OVERRIDE THE `initialize()` METHOD. IF YOU OVERRIDE `initialize()`, THE BASE CLASS CONNECTION POOL IS NOT SET. CONNECTIONS WITHOUT A POOL CAN CAUSE RESOURCE EXHAUSTION AND APPLICATION CRASHES.
>
> *Principles applied: P3 (get → is not set), P7 (initialize as verb, not noun). Risk connects override to pool state to crash.*

**Functional (Haskell, Elixir, Clojure, Rust).** In functional paradigms, risk explanations often involve purity violations and lazy evaluation surprises. A warning about an impure function must explain that referential transparency is broken. A caution about an unsafe IO operation must explain that laziness delays the side effect beyond the expected execution point.

> **Non-STE:** WARNING: `unsafePerformIO` IS DANGEROUS.
>
> **STE:** WARNING: DO NOT USE `unsafePerformIO` IN PRODUCTION CODE. `unsafePerformIO` REMOVES THE IO TYPE SAFETY GUARANTEE. WITHOUT THE IO GUARANTEE, SIDE EFFECTS CAN RUN AT UNEXPECTED TIMES. SIDE EFFECTS AT UNEXPECTED TIMES CAN CAUSE RACE CONDITIONS AND SILENT DATA CORRUPTION.
>
> *Principles applied: P10 (no slang: "dangerous" → specific risk), P4 (approved adjective forms). Risk traces from type-safety removal to corruption.*

**Procedural (C, Go, Bash).** In procedural code, risk explanations often involve resource lifetimes and error-code neglect. A warning about a `malloc` without `free` must explain the leak's cumulative effect. A caution about an ignored return code must explain the silent failure path.

> **Non-STE:** WARNING: YOU MUST FREE THE BUFFER.
>
> **STE:** WARNING: YOU MUST FREE THE BUFFER AFTER EACH `malloc` CALL. EACH UNFREED BUFFER STAYS IN MEMORY UNTIL THE PROCESS STOPS. IN A LONG-RUNNING PROCESS, UNFREED BUFFERS CAN USE ALL AVAILABLE MEMORY. MEMORY EXHAUSTION CAN CAUSE THE OPERATING SYSTEM TO STOP THE PROCESS.
>
> *Principles applied: P1 (use → after each call), P9 (short, clear nouns). Risk traces from unfreed buffer to OS termination.*

**Declarative (SQL, Terraform, Kubernetes YAML).** In declarative configurations, risk explanations often involve cascading side effects from a single declaration. A Terraform resource change can destroy and recreate infrastructure. A Kubernetes manifest misconfiguration can expose internal services.

> **Non-STE:** CAUTION: DO NOT CHANGE THE `family` FIELD.
>
> **STE:** CAUTION: DO NOT CHANGE THE `family` FIELD IN THE `aws_db_instance` RESOURCE. TERRAFORM INTERPRETS A CHANGE TO `family` AS A DESTROY-AND-RECREATE OPERATION. A DESTROY-AND-RECREATE OPERATION REMOVES THE CURRENT DATABASE AND ALL ITS DATA. THE REMOVED DATA CANNOT BE RECOVERED.
>
> *Principles applied: P3 (show → interprets), P11 (one term: destroy-and-recreate). Risk explains the interpreter behavior behind the field change.*

**Systems (Rust ownership, C memory, kernel documentation).** Systems documentation carries the highest-risk instructions. A warning about undefined behavior in C must explain the practical consequence, not just cite the standard. A Rust `unsafe` block documentation must explain which safety invariant the caller must uphold and what happens if it is not.

> **Non-STE:** WARNING: THIS FUNCTION IS UNSAFE. THE CALLER MUST NOT ALIAS THE POINTER.
>
> **STE:** WARNING: THIS FUNCTION IS UNSAFE. THE CALLER MUST MAKE SURE THAT NO OTHER POINTER REFERS TO THE SAME MEMORY. IF TWO POINTERS REFER TO THE SAME MEMORY, THE COMPILER CAN REMOVE LOADS AND STORES THAT THE PROGRAM NEEDS. REMOVED LOADS AND STORES CAN CAUSE VALUES TO APPEAR FROM DIFFERENT EXECUTION TIMELINES, WHICH IS UNDEFINED BEHAVIOR.
>
> *Principles applied: P2 (alias → refer to, specified part of speech), P8 (standard technical nouns: undefined behavior). Risk connects aliasing to compiler optimization to undefined behavior.*

### Extended Examples

> **Non-STE:** WARNING: DO NOT USE `eval()`.
>
> **STE:** WARNING: DO NOT USE `eval()` WITH DATA FROM EXTERNAL SOURCES. `eval()` RUNS THE INPUT AS CODE WITH THE SAME PRIVILEGES AS THE APPLICATION. A MALICIOUS INPUT CAN RUN ARBITRARY COMMANDS ON THE HOST SYSTEM. ARBITRARY COMMANDS CAN CAUSE DATA THEFT, DATA DESTRUCTION, OR SYSTEM COMPROMISE.
>
> *Principles applied: P5 (technical code noun: `eval`), P3 (use → runs, approved meaning). Risk traces from eval to full system compromise.*

> **Non-STE:** CAUTION: PAGINATION IS MANDATORY.
>
> **STE:** CAUTION: YOU MUST USE PAGINATION FOR ALL LIST ENDPOINTS. WITHOUT PAGINATION, A SINGLE REQUEST CAN RETURN EVERY RECORD IN THE DATABASE. A LARGE RESULT SET CAN CAUSE MEMORY EXHAUSTION ON THE SERVER. MEMORY EXHAUSTION CAN CAUSE THE SERVER TO STOP AND ALL CONNECTED CLIENTS TO DISCONNECT.
>
> *Principles applied: P9 (short, clear: pagination), P1 (use → use). Risk traces from missing pagination to server crash.*

> **Non-STE:** WARNING: CORS IS NOT CONFIGURED PROPERLY.
>
> **STE:** WARNING: THE CORS CONFIGURATION USES A WILDCARD ORIGIN (`*`). A WILDCARD ORIGIN LETS ANY WEBSITE SEND REQUESTS WITH THE USER'S CREDENTIALS. AN ATTACKER CAN MAKE AN AUTHENTICATED REQUEST FROM A MALICIOUS WEBSITE. AUTHENTICATED REQUESTS FROM A MALICIOUS ORIGIN CAN CAUSE DATA THEFT AND ACCOUNT TAKEOVER.
>
> *Principles applied: P5 (CORS, wildcard as technical nouns), P6 (non-approved word as technical noun). Risk traces from wildcard to account takeover.*

> **Non-STE:** WARNING: RACE CONDITION.
>
> **STE:** WARNING: TWO GOROUTINES CAN WRITE TO THE `counter` VARIABLE AT THE SAME TIME. CONCURRENT WRITES TO A GO VARIABLE WITHOUT A MUTEX CAUSE A DATA RACE. DATA RACES CAN MAKE THE COUNTER VALUE INCORRECT. AN INCORRECT COUNTER CAN CAUSE BILLING ERRORS AND FINANCIAL LOSS.
>
> *Principles applied: P7 (no technical noun as verb: "race" is a noun here), P3 (make → cause). Risk traces from data race to financial loss.*

> **Non-STE:** CAUTION: DO NOT SKIP MIGRATIONS.
>
> **STE:** CAUTION: DO NOT SKIP DATABASE MIGRATIONS. EACH PENDING MIGRATION CAN ADD, REMOVE, OR CHANGE COLUMNS. IF THE APPLICATION STARTS WITHOUT APPLYING ALL MIGRATIONS, THE APPLICATION SCHEMA DOES NOT MATCH THE DATABASE SCHEMA. SCHEMA MISMATCHES CAN CAUSE QUERY FAILURES, SILENT DATA LOSS, AND APPLICATION CRASHES.
>
> *Principles applied: P1 (skip → skip), P4 (approved adjective: pending). Risk traces from skipped migration to crashes.*

> **Non-STE:** WARNING: HARDCODED SECRETS.
>
> **STE:** WARNING: THE CONFIGURATION FILE CONTAINS HARDCODED SECRETS. HARDCODED SECRETS BECOME PART OF THE SOURCE CODE HISTORY. ANY PERSON WITH ACCESS TO THE REPOSITORY CAN READ THE SECRETS. AN ATTACKER WITH REPOSITORY ACCESS CAN USE THE SECRETS TO ACCESS PRODUCTION SYSTEMS, DATABASES, AND THIRD-PARTY SERVICES.
>
> *Principles applied: P5 (secrets as technical noun), P3 (part of → become part of). Risk traces from hardcoded secrets to full infrastructure access.*

### Edge Cases

**When a framework name is also an "unapproved" word.** Some framework names overlap with everyday English words that STE restricts. For example, the React framework `Suspense` is both a technical noun and an ordinary English word. A warning that says "DO NOT NEST SUSPENSE BOUNDARIES" could confuse readers who interpret Suspense as an emotion, not a component. The risk explanation must anchor the word in its technical meaning: "IF YOU NEST `Suspense` COMPONENTS, THE INNER SUSPENSE BOUNDARY CAN CAPTURE THE FALLBACK OF THE OUTER BOUNDARY. CAPTURED FALLBACKS CAN CAUSE INFINITE LOADING STATES AND UNRESPONSIVE PAGES." The code-formatted backticks and the repeated technical context disambiguate the term.

**When a code keyword conflicts with the rule.** Keywords like `break`, `continue`, `return`, and `throw` carry control-flow meaning that risk explanations must address precisely. A warning that says "DO NOT USE `return` INSIDE A `finally` BLOCK" must explain the interaction: "IF YOU USE `return` IN A `finally` BLOCK, THE `return` REPLACES ANY EXCEPTION THAT WAS THROWN IN THE `try` BLOCK. THE REPLACED EXCEPTION IS LOST AND CANNOT BE CAUGHT BY CALLERS. SILENTLY LOST EXCEPTIONS CAN HIDE ERRORS THAT CAUSE INCORRECT PROGRAM BEHAVIOR." The risk explanation addresses the language-level semantic collision, not the word itself.

**When the rule should be relaxed for generated code.** Generated code (protobuf stubs, OpenAPI clients, database ORM models) often contains instructions that violate Rule 7.3 because the generator produces terse, repetitive output. A generated file comment that says "DO NOT EDIT" without explanation is acceptable only if a companion document or the code generator's documentation explains the risk. If the generated code is the sole artifact the developer sees, the risk must still be explained: "DO NOT EDIT THIS FILE. THIS FILE IS REGENERATED EACH TIME YOU RUN `make generate`. IF YOU EDIT THE FILE, YOUR CHANGES ARE LOST THE NEXT TIME `make generate` RUNS. LOST CHANGES CAN CAUSE BUILD FAILURES AND REGRESSION BUGS."

**When the risk is probabilistic, not guaranteed.** Many software risks are not deterministic: a race condition may manifest only under load, a memory leak may exhaust resources only after days. Rule 7.3 still applies. Use "can" instead of "will" for probabilistic risks: "IF TWO THREADS WRITE TO THE MAP AT THE SAME TIME, A DATA RACE CAN OCCUR. THE DATA RACE CAN CAUSE INCORRECT MAP CONTENTS. INCORRECT MAP CONTENTS CAN CAUSE WRONG QUERY RESULTS AND SILENT DATA CORRUPTION." The word "can" communicates uncertainty without diminishing the severity.

**When multiple risks share one instruction.** A single "DO NOT" instruction may prevent several different problems. List the risks in order of severity, from most severe to least severe: "DO NOT DISABLE TLS VERIFICATION. WITHOUT TLS VERIFICATION, A MAN-IN-THE-MIDDLE ATTACKER CAN DECRYPT AND CHANGE THE TRAFFIC. CHANGED TRAFFIC CAN CAUSE DATA THEFT, CREDENTIAL LEAKAGE, AND UNAUTHORIZED TRANSACTIONS." Each risk is a separate "can cause" clause that builds the cumulative case for the instruction.

**When the risk is a cascading chain with no single owner.** Distributed systems failures often involve emergent behavior where no single component is at fault. A warning about removing a circuit breaker must explain the cascading effect across services: "IF YOU REMOVE THE CIRCUIT BREAKER FROM THE PAYMENT SERVICE, A SLOWDOWN IN THE INVENTORY SERVICE CAN PROPAGATE TO THE PAYMENT SERVICE. THE PROPAGATED SLOWDOWN CAN CAUSE TIMEOUTS IN THE ORDER SERVICE. ORDER SERVICE TIMEOUTS CAN CAUSE CUSTOMERS TO PLACE DUPLICATE ORDERS. DUPLICATE ORDERS CAN CAUSE INCORRECT CHARGES AND FINANCIAL LOSS." The risk explanation traces the chain across three services without blaming any single component.

**When the risk affects a different team than the reader.** In large organizations, the person who reads the documentation is often not the person who suffers the consequence. An infrastructure engineer reading an application warning may not feel the urgency. The risk explanation must bridge the organizational gap: "DO NOT DEPLOY WITHOUT CONTACTING THE DATABASE TEAM FIRST. THE DATABASE TEAM MUST LOCK THE SCHEMA BEFORE DEPLOYMENT. IF YOU DEPLOY WITHOUT A SCHEMA LOCK, THE MIGRATION CAN CONFLICT WITH ANOTHER DEPLOYMENT. SCHEMA CONFLICTS CAN CAUSE DATA CORRUPTION THAT AFFECTS ALL TEAMS USING THE DATABASE." The phrase "affects all teams using the database" connects the reader's action to consequences beyond their immediate team.

### Cross-References

- **Rule 1.1 (Use approved words):** The words in your risk explanation must come from the STE-Code dictionary. See the Canonical Synonym Table for substitutes: "retrieve" → "get", "terminate" → "stop", "utilize" → "use".
- **Rule 1.6 (Non-approved words only as technical nouns):** When a risk explanation must include a non-approved word (for example, `deadlock`, `thrashing`, `replay attack`), present it as a technical code noun and define it on first use.
- **Rule 1.10 (No slang, jargon, or regional terms):** A risk explanation that says "this will brick your deployment" fails Rule 1.10 and Rule 7.3 simultaneously. Replace "brick" with the specific consequence: "THIS WILL MAKE THE DEPLOYMENT PERMANENTLY UNAVAILABLE."
- **Rule 7.1 (Use clear, specific safety signal words):** The signal word (WARNING or CAUTION) sets the severity level. Rule 7.3 connects the signal word to the concrete consequence. A WARNING demands a risk of injury or data loss. A CAUTION demands a risk of incorrect results or system damage.
- **Rule 7.2 (Place safety instructions before the related step):** The instruction must come before the risky action. The risk explanation in Rule 7.3 comes immediately after the instruction, before the reader proceeds. The order is: signal word → instruction → risk explanation → action.
- **Rule 7.4 (Use imperative mood for instructions):** The instruction part of a Rule 7.3 warning must use imperative mood ("DO NOT USE"), not descriptive ("using this is not recommended"). The risk explanation part may use descriptive mood to state the consequence.
- **Section 1 (Words):** All words in risk explanations follow the noun-verb-adjective rules of Section 1. A risk sentence like "This initiates a cascade failure" violates Rule 1.2 (initiate → start) and Rule 1.3 (cascade as unapproved modifier). The STE version: "This can start a sequence of failures."

### Grammar Notes

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

### Practical Application

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
