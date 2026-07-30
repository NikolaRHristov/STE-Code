# Rule 8.3 — Use of Parentheses

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.3

## Original Rule

**Rule 8.3** You can use parentheses:

- To make references to illustrations or text
- To include letters or numbers that identify items on an illustration or in a text
- To identify the work steps in a procedure
- To include abbreviations
- To give the singular and plural forms of a noun at the same time
- To explain words or a part of a sentence
- To include an alternative.

In STE, you can use parentheses as follows:

1. To make references to illustrations or text

   > **STE:** Remove the valve (10, Figure 1).
   > **STE:** Install the cover (refer to paragraphs 2 thru 5).

2. To include letters or numbers that identify items on an illustration or in a text

   > **STE:** Disconnect the hoses (2) and (12) from the suction ejector (8).
   > **STE:** Remove the nuts (74), the washers (76), the bolts (68), the seals (70), and the bonding straps (72).

3. To identify the work steps in a procedure

   > **STE:** (1) Install the locking cap (4) on the body (8).
   > **STE:** (2) Safety the locking cap (4) with the cotter pin (5).
   > **STE:** (3) Install a new retaining ring (6).

4. To include abbreviations

   > **STE:** A Liquid Crystal Display (LCD) is a flat-panel display that uses the light-modulating properties of liquid crystals.

5. To give the singular and plural forms of a noun at the same time

   | Example | Text |

   |---------|------|

   | A | Before you do the test(s), install the component(s). |

   | B | Do the applicable test(s). |

6. To explain words or a part of a sentence

   > **STE:** Increase the pressure slowly (not more than 10 psi each minute).
   > **STE:** Make sure that the BLEED pushbutton switch is released (the ON legend is off).

7. To include an alternative

   > **STE:** Open the left (right) access panel L42 (R42).

## STE-Code Adaptation

**Rule 8.3** In code documentation, you can use parentheses:

- To make references to code modules, diagrams, or text
- To include letters or numbers that identify items in a diagram or in a text
- To identify the work steps in a procedure
- To include abbreviations
- To give the singular and plural forms of a noun at the same time
- To explain words or a part of a sentence
- To include an alternative.

1. To make references to code modules, diagrams, or text

   > **STE:** Call the handler (Figure 3, Module A).
   > **STE:** Deploy the service (refer to sections 2 thru 5).

2. To include letters or numbers that identify items in a diagram or in a text

   > **STE:** Disconnect the endpoints (2) and (12) from the load balancer (8).
   > **STE:** Remove the configuration keys (74), the environment variables (76), the secrets (68), the tokens (70), and the certificates (72).

3. To identify the work steps in a procedure

   > **STE:** (1) Install the dependency package (4) in the project directory (8).
   > **STE:** (2) Pin the dependency package (4) with the lock file (5).
   > **STE:** (3) Add a new test case (6).

4. To include abbreviations

   > **STE:** A Command Line Interface (CLI) is a text-based interface that uses typed commands to interact with the operating system.

5. To give the singular and plural forms of a noun at the same time

   > **STE:** Before you run the test(s), set the environment variable(s).

6. To explain words or a part of a sentence

   > **STE:** Increase the timeout slowly (not more than 1000 ms each step).
   > **STE:** Make sure that the DEBUG flag is released (the ON indicator is off).

7. To include an alternative

   > **STE:** Use the left (right) API key for the staging (production) environment.

### Examples

> **Non-STE:** A Representational State Transfer Application Programming Interface, or REST API, is an architectural style for designing networked applications relying on stateless, client-server communication.
>
> **STE:** A Representational State Transfer Application Programming Interface (REST API) is an architectural style for designing networked applications that uses stateless, client-server communication.
>
> *Adapted from spec pattern: abbreviation in parentheses — "A Liquid Crystal Display (LCD) is a flat-panel display..."*

> **Non-STE:** Run the migration on all database shard servers, the primary and all replica instances, before you deploy.
>
> **STE:** Run the migration on all database shard(s) before you deploy.
>
> *Adapted from spec pattern: singular/plural in parentheses — "Before you do the test(s), install the component(s)."*

## Code-Domain Explanation

Rule 8.3 governs how parentheses appear across all code documentation types. Each documentation type uses parentheses differently because each type has a unique audience and purpose.

### README Files

README files introduce a project to new users. Use parentheses to define abbreviations on first use. The abbreviation must follow immediately after the full term, enclosed in parentheses. This pattern helps the reader scan the document quickly.

> **Non-STE:** This project provides a CLI, or command-line interface, for managing your deployment pipeline.
>
> **STE:** This project provides a Command Line Interface (CLI) for managing your deployment pipeline.
>
> *Principles applied: P11, P3 — one term per concept, use words with approved meanings*

Use parentheses to reference related documentation files or sections. Keep the reference concise. Do not use parentheses to inject commentary or asides that distract from the main instruction.

> **Non-STE:** Follow the setup guide (which you can find in the docs/ folder, specifically in the getting-started subdirectory) before you run the server.
>
> **STE:** Follow the setup guide (refer to docs/getting-started.md) before you run the server.
>
> *Principles applied: P9, P1 — prefer short technical nouns, use approved words*

### API Documentation

API documentation describes endpoints, parameters, and return types. Use parentheses to explain parameter constraints or to show the unit of measurement for numeric values. Do not use parentheses to nest multiple levels of conditional logic.

> **Non-STE:** The timeout parameter accepts an integer representing milliseconds (though you can also use seconds if you set the unit flag to "s", which is available starting in version 2.1).
>
> **STE:** The timeout parameter accepts an integer in milliseconds (ms). To use seconds, set the unit flag to "s" (available in version 2.1 and later).
>
> *Principles applied: P9, P6 — prefer short nouns, non-approved words only as technical nouns*

Use parentheses around HTTP status codes or error codes to keep the main sentence flow uninterrupted.

> **Non-STE:** If the request fails you will get back a 404 which means the resource was not found on the server.
>
> **STE:** If the request fails, the server returns a 404 (Not Found) status.
>
> *Principles applied: P2, P3 — use words only as their specified part of speech, use approved meanings*

### Docstrings and Inline Comments

Docstrings describe a function, method, or class at its point of definition. Use parentheses to show parameter types, return types, or valid value ranges. In statically typed languages, do not repeat the type in parentheses when the type signature already states it. Use parentheses only for clarifying constraints the type system cannot express.

> **Non-STE:** // timeout - an int, must be between 1 and 30000, represents milliseconds
>
> **STE:** // timeout: milliseconds (1 to 30000)
>
> *Principles applied: P9, P4 — prefer short nouns, use approved adjective forms*

> **Non-STE:** """Calculate the factorial of n. n must be a non-negative integer."""
>
> **STE:** """Calculate the factorial of n (a non-negative integer)."""
>
> *Principles applied: P6, P9 — non-approved words only as technical nouns, prefer short nouns*

### Commit Messages

Commit messages benefit from the alternative-use pattern of parentheses. Use parentheses to indicate the scope of a change or to reference an issue tracker identifier. The scope word must be short and standard.

> **Non-STE:** feat(authentication module, the whole OAuth2 flow including token refresh): add PKCE support
>
> **STE:** feat(auth): add PKCE support (issue #482)
>
> *Principles applied: P9, P11 — prefer short nouns, one term per concept*

> **Non-STE:** fix: resolve problem where the dropdown menu sometimes displayed behind the modal dialog
>
> **STE:** fix(ui): correct z-index conflict between dropdown and modal (regression from v2.3)
>
> *Principles applied: P6, P1 — technical nouns allowed, use approved words*

### Error Messages

Error messages must be unambiguous. Use parentheses to include diagnostic values (file paths, line numbers, actual versus expected values) without breaking the sentence structure. Put the diagnostic data at the end of the message in parentheses.

> **Non-STE:** Couldn't find the config file you specified; looked in /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, and ./config.yaml but none existed or were readable.
>
> **STE:** Cannot find the configuration file (searched: /etc/myapp/config.yaml, ~/.config/myapp/config.yaml, ./config.yaml).
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech*

> **Non-STE:** The value for --workers must be between 1 and 64 inclusive but you supplied 0 which is out of range.
>
> **STE:** Invalid value for --workers: 0 (valid range: 1 to 64).
>
> *Principles applied: P9, P3 — prefer short nouns, use approved meanings*

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python)

Object-oriented documentation uses parentheses to show method parameters, constructor arguments, and type parameters (generics). In narrative documentation, use parentheses to note the class hierarchy or to identify which interface a method implements. Do not use parentheses to nest multiple inheritance chains.

> **Non-STE:** The process method, which belongs to the DataPipeline class (that extends BasePipeline, which itself implements the Pipeline interface from the core package), orchestrates the ETL workflow.
>
> **STE:** The `process` method (inherited from `BasePipeline`, which implements `core.Pipeline`) orchestrates the ETL workflow.
>
> *Principles applied: P9, P6 — prefer short nouns, technical nouns allowed*

Use parentheses to show default parameter values in documentation tables. This mirrors how IDEs display method signatures.

> **Non-STE:** | timeout | int | how long to wait before giving up, defaults to 5000 |
>
> **STE:** | timeout | int | milliseconds to wait before failure (default: 5000) |
>
> *Principles applied: P1, P4 — use approved words, use approved adjective forms*

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure transformations, type signatures, and algebraic data types. Use parentheses to group type parameters or to show the shape of a curried function. In narrative text, use parentheses to explain the difference between a function's pure and effectful variants.

> **Non-STE:** map is a higher-order function that takes a transformation function and applies it to every element inside a functor, producing a new functor with the transformed elements.
>
> **STE:** `map` applies a function to each element of a functor (a container type that supports mapping). It returns a new functor with the transformed values.
>
> *Principles applied: P6, P7 — technical nouns allowed, do not use technical nouns as verbs*

> **Non-STE:** The state monad threads an immutable state value through a sequence of computations, and StateT is the monad transformer version that lets you stack it on top of another monad.
>
> **STE:** The `State` monad passes an immutable state value through a chain of computations. Use `StateT` (the transformer variant) to combine it with another monad.
>
> *Principles applied: P9, P11 — prefer short nouns, one term per concept*

### Procedural Documentation (C, Go, Bash)

Procedural documentation focuses on sequential steps, error codes, and resource lifecycle. Use parentheses to show return codes or exit statuses. Use parentheses to note ownership or allocation responsibility (who must free or close a resource).

> **Non-STE:** The function returns 0 if everything went fine, -1 if there was an I/O error, -2 if the input was malformed, and -3 if the operation timed out.
>
> **STE:** The function returns: 0 (success), -1 (I/O error), -2 (malformed input), -3 (timeout).
>
> *Principles applied: P9, P2 — prefer short nouns, use words only as their specified part of speech*

> **Non-STE:** The caller is responsible for deallocating the buffer that this function allocates, and failure to do so will cause a memory leak.
>
> **STE:** The caller must free the returned buffer (allocated by this function). Failure to free the buffer causes a memory leak.
>
> *Principles applied: P1, P12 — use approved words, technical verbs allowed*

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, schema, and resource definitions. Use parentheses to show valid enumeration values. Use parentheses to note the unit of a numeric field. Do not use parentheses to embed conditional logic that belongs in a separate note or warning.

> **Non-STE:** The `provider` field must be set to one of the following: "aws", "gcp", or "azure" (case-sensitive, do not use uppercase).
>
> **STE:** Set the `provider` field to one of: "aws", "gcp", "azure" (lowercase only).
>
> *Principles applied: P1, P3 — use approved words, use approved meanings*

> **Non-STE:** The `replicas` field controls how many copies of the pod the deployment maintains, and you can set it to any integer from 1 (the minimum for production) to 100.
>
> **STE:** Set `replicas` to the number of pod copies (range: 1 to 100, production minimum: 1).
>
> *Principles applied: P9, P2 — prefer short nouns, use words only as their specified part of speech*

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation explains ownership, lifetimes, and memory safety. Use parentheses to mark the ownership transfer point or to note the lifetime relationship. Use parentheses to annotate unsafe blocks with the safety invariant they uphold.

> **Non-STE:** When you pass a value to this function, ownership moves into the function and the caller can no longer access that value unless the function returns it back.
>
> **STE:** This function takes ownership of the value (the caller cannot use it after the call). To keep access, pass a reference instead.
>
> *Principles applied: P6, P7 — technical nouns allowed, do not use technical nouns as verbs*

> **Non-STE:** // SAFETY: the pointer must be non-null, properly aligned for the type T, and point to a valid initialized instance of T.
>
> **STE:** // SAFETY: the pointer must be non-null, aligned for type T, and point to a valid initialized T (invariant enforced by caller).
>
> *Principles applied: P9, P1 — prefer short nouns, use approved words*

## Extended Examples

### Example 1: Abbreviation on First Use

> **Non-STE:** Set up CI/CD, meaning continuous integration and continuous delivery, for your project by adding a pipeline configuration file to the repository root.
>
> **STE:** Set up Continuous Integration and Continuous Delivery (CI/CD) for your project. Add a pipeline configuration file to the repository root.
>
> *Principles applied: P1, P4 — use approved words, use approved adjective forms. The abbreviation follows immediately after the full term in parentheses, as the original STE spec requires. The original sentence was split into two shorter procedural sentences per STE length limits.*

### Example 2: Step Numbering in Procedures

> **Non-STE:** To initialize the database, first run the schema migration, then seed the reference data, and finally create the admin user account.
>
> **STE:** To initialize the database:
> (1) Run the schema migration.
> (2) Seed the reference data.
> (3) Create the admin user account.
>
> *Principles applied: P2, P9 — use words only as their specified part of speech, prefer short nouns. The numbered steps in parentheses follow the original STE pattern for procedure identification. Each step is one instruction.*

### Example 3: Alternative Configuration Values

> **Non-STE:** Set the log level to either debug if you are troubleshooting or info if you are running in production mode.
>
> **STE:** Set the log level to debug (troubleshooting) or info (production).
>
> *Principles applied: P3, P9 — use approved meanings, prefer short nouns. The alternative-value pattern from the original STE spec ("left (right)") is adapted here for configuration options. Each option's purpose is explained concisely in parentheses.*

### Example 4: Explaining a Code Statement

> **Non-STE:** The retry loop will attempt the request up to five times, waiting one second between each attempt, and if all five fail it will propagate the last error to the caller.
>
> **STE:** The retry loop attempts the request (maximum 5 attempts, 1-second delay between attempts). If all attempts fail, it propagates the last error to the caller.
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech. The parenthetical explanation clarifies the loop parameters without interrupting the sentence flow. "Maximum" replaces the informal "up to."*

### Example 5: Singular/Plural in Configuration Instructions

> **Non-STE:** Before starting the service, make sure all necessary environment variable or variables have been set in the .env file or through the shell.
>
> **STE:** Before you start the service, set the necessary environment variable(s) in the .env file.
>
> *Principles applied: P1, P11 — use approved words, one term per concept. The "(s)" pattern from the original STE spec eliminates the awkward "variable or variables" construction. The instruction is direct and uses one term consistently.*

### Example 6: Reference to External Documentation

> **Non-STE:** For detailed information about the authentication protocol, check out the OAuth 2.0 specification which is documented in RFC 6749 and available online.
>
> **STE:** For detailed information about the authentication protocol, refer to RFC 6749 (OAuth 2.0 Authorization Framework).
>
> *Principles applied: P1, P3 — use approved words, use approved meanings. The parenthetical title of the referenced document helps the reader confirm they have the correct standard. "Refer to" replaces the informal "check out."*

## Edge Cases

### Edge Case 1: Framework Names That Are Also Unapproved Words

When a framework or library name is identical to a common English word that STE restricts, parentheses clarify meaning. For example, the Python web framework "Flask" is also a common noun. Use parentheses to distinguish the technical noun from the common word.

> **Non-STE:** Use Flask to serve the application. Flask is a microframework that does not require particular tools or libraries.
>
> **STE:** Use Flask (the Python web framework) to serve the application. Flask does not require particular tools or libraries.
>
> *Principles applied: P6, P8 — non-approved words only as technical nouns, use standard technical nouns. The parenthetical clarification eliminates ambiguity between the framework name and the common English word.*

Similarly, when a framework uses an STE-approved word in an unapproved sense (for example, "React" does not mean "to respond"), add a brief parenthetical on first use.

> **Non-STE:** This project uses React to build the user interface. React components are reusable pieces of UI.
>
> **STE:** This project uses React (a JavaScript UI library) to build the user interface. React components are reusable pieces of UI.
>
> *Principles applied: P6, P8 — non-approved words only as technical nouns, use standard technical nouns.*

### Edge Case 2: Code Keywords That Conflict with the Rule

Some programming language keywords are also punctuation characters. For example, Rust uses parentheses for tuple types and unit types. In documentation, do not add extra parentheses around these keywords — the code syntax itself is unambiguous. Reserve narrative parentheses for explanations.

> **Non-STE:** The function returns `()` (pronounced "unit"), which is Rust's equivalent of void (meaning no meaningful value).
>
> **STE:** The function returns `()` (the unit type, equivalent to void in other languages).
>
> *Principles applied: P6, P9 — technical nouns allowed, prefer short nouns. The parenthetical explanation is kept because "unit type" is a domain concept that some readers may not know. The nested parenthetical "(meaning no meaningful value)" was removed to avoid clutter.*

When documentation describes generic type parameters in angle brackets (for example, `<T>`), do not place the angle brackets inside parentheses. Keep the code literal distinct from the narrative explanation.

> **Non-STE:** The `Option` type (which is generic over `<T>`) represents an optional value that may or may not be present.
>
> **STE:** The `Option<T>` type represents an optional value. The type parameter `T` can be any type.
>
> *Principles applied: P9, P7 — prefer short nouns, do not use technical nouns as verbs. The code literal `Option<T>` is self-documenting. The explanation is separated into its own sentence instead of being nested in parentheses.*

### Edge Case 3: Parentheses in Generated Code or Auto-Generated Docs

Generated API reference docs (for example, from JSDoc, Sphinx, or rustdoc) often include parentheses around types and return values automatically. Do not remove these — they are not part of the narrative text. Apply Rule 8.3 only to the portions of documentation that a human writes, such as description fields and summary paragraphs.

> **Auto-generated (acceptable as-is):** `getUser(id: number): Promise<User>`
>
> **STE description field:** Get a user by their identifier (returns a Promise that resolves to a User object).
>
> *Principles applied: P6, P11 — technical nouns allowed, one term per concept. The auto-generated signature is left untouched. The human-written description follows STE rules, using parentheses to explain the return type.*

> **Auto-generated (acceptable as-is):** `fn connect(addr: SocketAddr) -> Result<TcpStream, Error>`
>
> **STE description field:** Connect to the address. Returns a Result (Ok with a TcpStream on success, Err with an Error on failure).
>
> *Principles applied: P6, P1 — technical nouns allowed, use approved words. Parentheses explain the two Result variants concisely.*

### Edge Case 4: Nested Parentheses

Never nest parentheses. The original STE standard does not permit nesting because it reduces readability. If a sentence requires nested parenthetical information, restructure the sentence or split it.

> **Non-STE:** Set the cache TTL to 3600 (one hour (or 86400 for one day in production)).
>
> **STE:** Set the cache TTL to 3600 (one hour). For production, set the cache TTL to 86400 (one day).
>
> *Principles applied: P1, P9 — use approved words, prefer short nouns. The nested parentheses are eliminated by splitting into two sentences. Each parenthetical stands alone.*

> **Non-STE:** The middleware pipeline processes requests through authentication (via JWT (JSON Web Token)), authorization, and rate limiting.
>
> **STE:** The middleware pipeline processes requests through authentication (via JWT), authorization, and rate limiting. JWT is an abbreviation for JSON Web Token.
>
> *Principles applied: P1, P11 — use approved words, one term per concept. The abbreviation is defined in a separate sentence. Nested parentheses are eliminated.*

### Edge Case 5: Parentheses in Command-Line Help Text

Command-line help text appears in terminal output with limited formatting. Use parentheses sparingly. Prefer the alternative-use pattern (for example, `--verbose (--quiet)`) or the explanation pattern (for example, `--timeout MILLISECONDS (default: 5000)`). Do not use parentheses for long descriptions that belong in a man page.

> **Non-STE:** --config PATH    Path to config file (can be JSON, YAML, or TOML)
>
> **STE:** --config PATH    Path to the configuration file (JSON, YAML, or TOML)
>
> *Principles applied: P1, P9 — use approved words, prefer short nouns. The parenthetical lists valid formats concisely.*

## Cross-References

This rule interacts with several other STE-Code rules:

- **Rule 1.1 (Approved Words):** Parentheses introduce abbreviations. The word inside parentheses must be the approved abbreviation form. See the STE-Code Dictionary for the canonical abbreviation list.

- **Rule 1.3 (Approved Meanings):** When parentheses explain a word, the explanation must use words with their approved meanings. Do not use parentheses to sneak in an unapproved meaning.

- **Rule 1.9 (Short Technical Nouns):** Parenthetical explanations must use short, standard technical nouns. Long explanatory phrases defeat the purpose of concise parenthetical notation.

- **Rule 5.1 (Sentence Length):** Parenthetical content counts toward the sentence word limit (20 procedural, 25 descriptive). If a parenthetical pushes a sentence over the limit, split the sentence.

- **Rule 6.3 (Procedural Steps):** When parentheses identify work steps, each step number must have its own line. Do not list multiple steps inside one set of parentheses.

- **Bracket usage:** Parentheses are the only permitted brackets in STE. Do not use square brackets `[ ]` for parenthetical information. Square brackets are reserved for optional parameters in code syntax.

- **Comma usage with parentheses:** Do not use a comma before an opening parenthesis unless the parenthetical is an alternative at the end of a list (for example, "the staging server (node 3), and the production server (node 1)").

- **Rule 8.2 (Hyphens):** Do not confuse parentheses with hyphens when listing compound adjectives. Parentheses explain. Hyphens join words into a single modifier.

## Grammar Notes

### Syntactic Function of Parentheses in STE

In the original ASD-STE100, parentheses serve as a secondary syntactic boundary. The primary boundary is the period (full stop). Commas separate items within a clause. Parentheses enclose supplementary information that relates to but does not interrupt the main clause structure.

In code documentation, parentheses serve the same role but must also coexist with code syntax that uses parentheses for function calls, type parameters, and grouping expressions. The writer must distinguish narrative parentheses from code parentheses.

### Parentheses vs. Commas vs. Dashes

Original STE permits parentheses but does not permit em dashes or en dashes for parenthetical asides. The comma is the only other permitted punctuation for supplementary information. Use commas for brief, non-essential clauses. Use parentheses when the supplementary information is a discrete unit (an abbreviation, a reference, a range, or an alternative value).

> **Non-STE:** The API gateway -- which sits between clients and microservices -- routes requests to the correct backend.
>
> **STE:** The API gateway (which sits between clients and microservices) routes requests to the correct backend.
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech. Dashes are not permitted in STE. Parentheses handle the non-restrictive clause.*

### Punctuation Inside and Outside Parentheses

In STE, the punctuation of the main sentence is not affected by the parenthetical content. A period that ends a sentence goes outside the closing parenthesis. A period that ends only the parenthetical content (when the parenthetical is a complete sentence) goes inside. However, complete-sentence parentheticals are discouraged in STE because they can be written as separate sentences.

> **Non-STE:** Deploy to the staging environment first. (The production deployment follows after approval.)
>
> **STE:** Deploy to the staging environment first. Deploy to the production environment after approval.
>
> *Principles applied: P1, P9 — use approved words, prefer short nouns. The parenthetical complete sentence is converted to a standalone imperative sentence. This improves readability and follows STE conventions.*

When the parenthetical ends the sentence and is not a complete sentence, the period goes outside:

> **STE:** Set the log level to debug (recommended for development).
>
> *Principles applied: P1, P2 — use approved words, use words only as their specified part of speech.*

### Abbreviation Placement

The original STE rule requires that the abbreviation appear in parentheses immediately after the first use of the full term. Do not place the full term in parentheses after the abbreviation. The pattern is always: "Full Term (ABBR)." After the first definition, use only the abbreviation.

> **Non-STE:** Use the CLI (Command Line Interface) to deploy. The Command Line Interface provides quick access.
>
> **STE:** Use the Command Line Interface (CLI) to deploy. The CLI gives quick access.
>
> *Principles applied: P4, P11 — use approved adjective forms, one term per concept. The abbreviation follows the full term, not vice versa. After definition, only the abbreviation is used.*
