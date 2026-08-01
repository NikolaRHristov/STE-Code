# Rule 8.4 — Colon in a Vertical List

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.4

> **Source:** [master.md#sec8-rule8.4](ste-code/grouped/)

## Original Rule

**Rule 8.4** In a vertical list, a colon (:) has the same effect on word count as a period and shows the end of a sentence.

In a vertical list, a colon (:) divides the first part of the sentence from the subsequent items in the vertical list. This colon has the effect of a period (full stop). Thus:

- In procedural sentences, you can use a maximum of 20 words before the colon.
- In descriptive sentences, you can use a maximum of 25 words before the colon.

Each item in a vertical list that comes after the colon counts as a new sentence. Thus, the limit for each item in a vertical list is:

- 20 words for procedural sentences
- 25 words for descriptive sentences.

> **STE:** To extinguish a possible fire, portable fire extinguishers are installed in these areas: (13 words)
>
> - The cockpit (2 words)
> - The cabin (2 words)
> - The cabin sub-compartment (3 words)
> - The crew rest compartment. (4 words)

## STE-Code Adaptation

**Rule 8.4** In code documentation, a colon (:) in a vertical list has the same effect on word count as a period and shows the end of a sentence.

In a vertical list, a colon (:) divides the first part of the sentence from the subsequent items in the vertical list. This colon has the effect of a period (full stop). Thus:

- In procedural sentences, you can use a maximum of 20 words before the colon.
- In descriptive sentences, you can use a maximum of 25 words before the colon.

Each item in a vertical list that comes after the colon counts as a new sentence. Thus, the limit for each item in a vertical list is:

- 20 words for procedural sentences
- 25 words for descriptive sentences.

### Examples

> *Adapted from spec pair:* Non-STE: `To extinguish a possible fire, portable fire extinguishers are installed in these areas:` followed by a vertical list of locations with word counts | STE: `To handle possible error conditions, the error handler catches these exception types:` followed by a vertical list (ASD-STE100 Issue 9, Rule 8.4, page 105 — the colon before a vertical list acts as a period and each list item is a new sentence with its own word-count limit).

> **Non-STE:** To handle all possible error conditions, the following exception types must be caught and processed by the error handler: database connection timeouts which occur when the primary node is unreachable, authentication failures caused by expired or invalid tokens, and validation errors due to malformed request payloads.
>
> **STE:** To handle possible error conditions, the error handler catches these exception types:
>
> - Database connection timeout (3 words)
> - Authentication failure (2 words)
> - Validation error. (2 words)
>
> *Adapted from spec pair: "To extinguish a possible fire, portable fire extinguishers are installed in these areas:" followed by a vertical list of locations with word counts.*

The non-STE sentence buries three distinct catch cases in one 31-word introduction. Written as a handler, the same content is hard to scan:

```python
# Non-STE: one long comment, no clear list of cases.
# To handle all possible error conditions, the following exception types
# must be caught and processed by the error handler: database connection
# timeouts which occur when the primary node is unreachable, authentication
# failures caused by expired or invalid tokens, and validation errors due
# to malformed request payloads.
try:
    result = call_external_service(request)
except Exception as exc:        # catches everything in one branch
    logger.error("unhandled error: %s", exc)
    raise
```

The STE version names each case as a separate, scannable item and maps it to its own `except` branch:

```python
# STE: the comment lists each exception type on its own line.
# To handle possible error conditions, the error handler catches
# these exception types:
#   - Database connection timeout
#   - Authentication failure
#   - Validation error
try:
    result = call_external_service(request)
except DatabaseTimeout as exc:    # Database connection timeout
    retry_with_backoff(exc)
except AuthenticationFailure as exc:  # Authentication failure
    redirect_to_login(exc)
except ValidationError as exc:    # Validation error
    return error_response(exc)
```

> **Non-STE:** The configuration file, which is located in the project root, supports these environment profiles that you can use for deployment: a development profile for local testing and debugging, a staging profile for pre-production integration verification, and a production profile for the live customer-facing environment.
>
> **STE:** The configuration file supports these environment profiles:
>
> - Development (1 word)
> - Staging (1 word)
> - Production. (1 word)
>
> *Adapted from spec pair: vertical list with colon introducing enumerated items, each counted as a separate sentence.*

The non-STE comment hides the three profile names behind a 31-word introduction:

```yaml
# Non-STE: the profile names are buried in the lead-in sentence.
# The configuration file, which is located in the project root, supports
# these environment profiles that you can use for deployment: a development
# profile for local testing and debugging, a staging profile for
# pre-production integration verification, and a production profile for
# the live customer-facing environment.
profiles:
  development: { url: "http://localhost:8080" }
  staging:     { url: "https://staging.example.com" }
  production:  { url: "https://example.com" }
```

The STE comment states the category in 7 words and lets the list carry the names:

```yaml
# STE: short introduction, then a vertical list.
# The configuration file supports these environment profiles:
#   - Development
#   - Staging
#   - Production
profiles:
  development: { url: "http://localhost:8080" }
  staging:     { url: "https://staging.example.com" }
  production:  { url: "https://example.com" }
```

## Code-Domain Explanation

Rule 8.4 sets word-count limits for vertical lists in all code documentation. The colon (:) before a vertical list acts as a period. The introductory text before the colon must obey the sentence-length rules: a maximum of 20 words for procedural text and 25 words for descriptive text. Each list item after the colon is a new sentence with its own length limit.

This rule prevents the most common vertical list abuse: a long, clause-heavy introduction that tries to include qualifiers, conditions, and justifications before the colon. The introduction should state only what the list contains. The list items should deliver the full content. The colon is the boundary between the "setup" and the "payload." A reader processes the introduction, understands the category, and then reads each list item as a standalone sentence.

When the introductory text before the colon exceeds the word limit, the writer has three options: (1) move the extra words into the list items themselves, (2) split the introduction into two sentences — one sentence before the list (without a colon) and a second sentence that introduces the list, or (3) remove unnecessary qualifiers from the introduction. The third option is usually correct. Writers tend to over-explain the list's contents in the introduction instead of trusting the list items to speak for themselves.

Word count in list items follows standard STE-Code rules. Articles (a, an, the) count as words. Code tokens inside backticks count as one word each regardless of their length. Parenthetical word counts in examples serve as training aids and are not required in production documentation.

### README Files

README files use vertical lists for installation steps, prerequisites, feature lists, supported platforms, and contribution guidelines. A common violation: the introductory sentence embeds version numbers, compatibility notes, and caveats before the colon. The reader must parse a 30-plus-word introduction before reaching the list items.

The fix: move qualifiers into the list items or into a separate sentence before the introduction. The introduction to a vertical list should state only the category of items that follow.

Example of a colon-in-list violation in a README installation section:

````
To install this package, which requires Python 3.10 or later and a
working C compiler for the native extensions on Linux and macOS
systems only, you need these dependencies: libssl-dev, pkg-config,
and cmake version 3.20 or later.
````

The introduction has 32 words before the colon. The dependency names and version requirements are buried in a single long sentence:

````
This package needs Python 3.10 or later. It also needs a C compiler
for native extensions on Linux and macOS systems. Install these
dependencies:

- libssl-dev
- pkg-config
- cmake (version 3.20 or later).
````

### API Documentation

API documentation uses vertical lists for endpoint parameters, request body fields, response fields, error codes, and authentication methods. The introductory sentence should name the endpoint or resource and state what the list enumerates. It should not describe each parameter's type, default value, and validation rules — those details belong in the list items.

A common violation: the introduction tries to summarize every nuance of the parameter list. Example:

````
POST /users accepts the following JSON body fields, all of which are
required except for middle_name which is optional and defaults to
null:
````

The introduction embeds type and optionality information for one field. The fix keeps the introduction generic:

````
A POST request to /users accepts these JSON body fields:

- username (string, required)
- email (string, required)
- middle_name (string, optional — the default value is null)
- role (string, required).
````

### Docstrings and Inline Comments

Docstrings use vertical lists for parameter descriptions (Args:), return value descriptions (Returns:), raised exceptions (Raises:), and usage examples. Many docstring formats (Google style, NumPy style, Sphinx reStructuredText) already enforce a colon-before-list structure. Rule 8.4 aligns with these formats but adds the explicit word-count constraint for the introductory text.

In practice, docstring introductions are usually short — "Args:", "Returns:", "Raises:" — and trivially comply with Rule 8.4. The risk appears in custom section headers where the writer crafts a longer introduction. Example of a violation:

````
The following edge cases are handled by this function and must be
considered by any caller that passes untrusted input to the parser:
````

The fix shortens the introduction and puts the nuance in the list:

````
This function handles these edge cases:

- Empty input strings
- Input with only whitespace characters
- Input longer than the maximum buffer size
- Input with non-UTF-8 byte sequences.
````

### Commit Messages

Commit messages use vertical lists in the body to enumerate related changes, breaking changes, or migration steps. A common violation: the subject line or the first body sentence becomes a long introduction that summarizes all the changes. The subject line is not an introduction to a vertical list — it is a standalone sentence that summarizes the commit. The body's introductory sentence (if any) must be short.

Example of a violation in a commit message body:

````
This commit refactors the authentication middleware to support
multiple token providers including JWT, OAuth2, and SAML, and makes
these related changes:
````

The introduction has 17 words — within the limit — but it also duplicates information that belongs in the list items. The fix:

````
This commit makes these changes to the authentication middleware:

- Add support for JWT tokens
- Add support for OAuth2 tokens
- Add support for SAML tokens
- Remove the deprecated Basic Auth provider.
````

### Error Messages

Error messages sometimes use vertical lists to enumerate possible causes or recovery steps. This is common in CLI tools and server applications that produce multi-line error output. The colon introduction must be short ("The command failed for one of these reasons:"). Each reason or step is a separate sentence. Do not chain multiple reasons into one long list item.

The word-count limit for procedural list items (20 words) applies to each recovery step. If a step needs more than 20 words, it is too complex — split it into two steps or simplify the instruction.

Example of a violation in a CLI error message:

````
The database migration failed due to one of the following possible
causes which you should investigate in order: the database server is
not reachable on the configured host and port, the migration user
does not have the ALTER TABLE privilege, or the migration scripts
directory contains SQL files with syntax errors.
````

The introduction and the single list item both violate the limits. The fix:

````
The database migration failed for one of these reasons:

- The database server is not reachable. Check the host and port.
- The migration user does not have the ALTER TABLE privilege.
- A SQL file in the migrations directory has a syntax error.
````

Underlying code that emits the message:

```python
# STE: the message uses a short introduction and one item per cause.
def run_migration(db, migrations_dir):
    causes = []
    if not db.reachable():
        causes.append("The database server is not reachable. Check the host and port.")
    if not db.user_has_privilege("ALTER TABLE"):
        causes.append("The migration user does not have the ALTER TABLE privilege.")
    bad = find_sql_syntax_error(migrations_dir)
    if bad is not None:
        causes.append(f"A SQL file in the {migrations_dir} directory has a syntax error.")
    if causes:
        raise MigrationError("The database migration failed for one of these reasons:")
```

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

In OOP documentation, vertical lists appear in class overviews (list of public methods), interface specifications (list of implementing classes), constructor documentation (list of parameters), and exception specifications (list of thrown exceptions). The introductory text should name the class and state the list category. Avoid embedding type constraints, access modifiers, or inheritance details in the introduction.

Pattern: Write the class or method name in the introduction. State the list category with a generic phrase ("accepts these parameters," "throws these exceptions," "implements these interfaces"). Put the type, default value, and constraint information in each list item. Never use the introduction to describe the first parameter in detail and then append the remaining parameters as an afterthought.

Example of a colon-in-list violation in a Java class docstring:

````
The ConnectionPool constructor accepts the following arguments
including the database URL which must be a valid JDBC connection
string with the host, port, and database name:
````

The introduction embeds detail about one argument. The fix:

````
The ConnectionPool constructor accepts these arguments:

- url — A valid JDBC connection string (host, port, and database name)
- maxConnections — The largest number of concurrent connections
- timeout — The connection timeout value in milliseconds.
````

Full docstring context:

```java
/**
 * The ConnectionPool constructor accepts these arguments:
 *   - url — A valid JDBC connection string (host, port, and database name)
 *   - maxConnections — The largest number of concurrent connections
 *   - timeout — The connection timeout value in milliseconds.
 */
public ConnectionPool(String url, int maxConnections, int timeout) { ... }
```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

In functional documentation, vertical lists appear in ADT (algebraic data type) documentation (list of variants), function composition descriptions (list of transformation steps), and pattern matching documentation (list of match arms). Each list item often describes a separate case, variant, or transformation. The introduction should state the type or function name and the cases it handles.

Pattern: Use the introduction to name the type or function. Use list items to describe each case independently. Do not use the introduction to describe the "happy path" and relegate error cases to an unindented continuation after the colon.

Example of a violation in a Rust enum docstring:

````
The ParseResult enum represents the possible outcomes of parsing a
configuration file which can succeed with the parsed Config struct,
fail due to an I/O error when the file cannot be read, or fail due to
invalid syntax when the file contains malformed TOML:
````

The introduction is 38 words — far over the 25-word descriptive limit. The fix:

````
The ParseResult enum represents the result of parsing a configuration
file. The enum has these variants:

- Ok(Config) — The file was parsed successfully.
- Err(ParseError::Io) — The file could not be read.
- Err(ParseError::Syntax) — The file contains incorrect TOML syntax.
````

Full doc context:

```rust
/// The ParseResult enum represents the result of parsing a configuration
/// file. The enum has these variants:
///   - Ok(Config) — The file was parsed successfully.
///   - Err(ParseError::Io) — The file could not be read.
///   - Err(ParseError::Syntax) — The file contains incorrect TOML syntax.
enum ParseResult {
    Ok(Config),
    Err(ParseError),
}
```

### Procedural Paradigm (C, Go, Bash)

In procedural documentation, vertical lists are central to step-by-step procedures. Each step is a list item. The introduction states the goal of the procedure. A common violation: the introduction tries to summarize all the steps before the colon, effectively duplicating the list.

Pattern: Write a short goal statement before the colon ("To configure the server, do these steps:"). Write each step as an imperative list item. Do not use the introduction to describe the first step in detail and then list the remaining steps. Every step gets equal treatment as a list item.

Example of a violation in a Go setup guide:

````
To compile the project from source, first make sure you have Go 1.21
or later installed and your GOPATH is set correctly, then run these
commands:
````

The introduction includes a prerequisite check that should be a separate step or a separate sentence. The fix:

````
Make sure that Go 1.21 or later is installed. Make sure that the
GOPATH environment variable is set correctly. Then do these steps:

- Clone the repository.
- Run the `go mod download` command.
- Run the `go build` command.
````

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

In declarative documentation, vertical lists appear in resource property specifications (list of allowed values), constraint descriptions (list of validation rules), and configuration option documentation (list of valid settings). The introduction names the resource or option. Each list item gives one value, one rule, or one setting.

Pattern: The introduction states the resource name and the list category ("The `instance_type` variable accepts these values:"). Each list item is one value with an optional short description. Do not use the introduction to explain why certain values are excluded — put that in a NOTE after the list.

Example of a violation in a Terraform variable description:

````
The instance_type variable, which controls the EC2 instance size for
the application tier and must be compatible with the selected AMI,
accepts these values:
````

The introduction embeds AMI compatibility constraints. The fix:

````
The instance_type variable sets the EC2 instance size. The variable
accepts these values:

- t3.micro
- t3.small
- t3.medium.

NOTE: The value must be compatible with the selected AMI.
````

### Systems Paradigm (Rust ownership docs, C memory docs)

In systems documentation, vertical lists appear in safety requirement specifications (list of preconditions), UB (Undefined Behavior) catalogs (list of triggering conditions), and ownership/borrowing rule documentation. The introduction states what the list enumerates. Each list item is a standalone safety condition. The word-count limit for list items ensures that safety-critical conditions are not buried in long sentences.

Systems documentation is the most safety-sensitive domain for Rule 8.4 compliance. A precondition buried in a long introduction is a precondition that a developer might miss during a code review. Each precondition must be a separate, numbered or bulleted list item. Each consequence must be explicit.

Example of a violation in a Rust unsafe function doc:

````
The caller must ensure that all of the following safety conditions
are met before calling this function including pointer validity,
alignment, and lifetime constraints:
````

This introduction is within the 25-word limit but it does not list the conditions — it only gestures at them. The fix enumerates each condition:

````
The caller must obey these safety conditions:

- The pointer must not be null.
- The pointer must be aligned to a 4-byte boundary.
- The data that the pointer refers to must be valid for the lifetime
  parameter `'a`.
- No other thread must write to the data during the call.
````

## Extended Examples

### Example 3 — README: Supported Platform List

> **Non-STE:** This library has been tested and verified to work correctly on the following operating system platforms and their respective versions including both 64-bit and ARM architectures where applicable: Ubuntu 22.04 LTS and 24.04 LTS, macOS 14 Sonoma and 15 Sequoia, and Windows 11 with MSVC 2022 or later.
>
> **STE:** This library operates on these platforms:
>
> - Ubuntu 22.04 LTS and 24.04 LTS (x86_64 and ARM64)
> - macOS 14 Sonoma and 15 Sequoia (x86_64 and ARM64)
> - Windows 11 with MSVC 2022 or later (x86_64).
>
> *Principles applied: P1, P2 (short introduction, 7 words before colon). The original introduction was 37 words with embedded architecture and version details. The fix moves architecture information into each list item as a parenthetical. Each list item stands as a complete descriptive sentence.*

Repository CI workflow that pins the same matrix — note the list stays short:

```yaml
# STE: the comment lists the supported platforms; the matrix mirrors it.
# This library operates on these platforms:
#   - Ubuntu 22.04 LTS and 24.04 LTS (x86_64 and ARM64)
#   - macOS 14 Sonoma and 15 Sequoia (x86_64 and ARM64)
#   - Windows 11 with MSVC 2022 or later (x86_64)
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-22.04, ubuntu-24.04, macos-14, macos-15, windows-2022]
```

### Example 4 — API Documentation: Response Fields

> **Non-STE:** A successful request to the GET /users/{id} endpoint returns a JSON response body that contains the following fields which describe the user account and its current state in the system: an id field with the unique user identifier as a UUID string, a username field with the display name chosen by the user during registration, an email field containing the verified email address, a created_at field with the ISO 8601 timestamp of account creation, and a status field that can be either active, suspended, or pending_verification.
>
> **STE:** A GET request to /users/{id} returns a JSON response with these fields:
>
> - `id` — The unique user identifier (UUID string)
> - `username` — The display name
> - `email` — The verified email address
> - `created_at` — The account creation timestamp (ISO 8601)
> - `status` — The account status (`active`, `suspended`, or `pending_verification`).
>
> *Principles applied: P1, P2 (introduction under 25 words, list items under 25 words each). The original had a 60-plus-word introduction with field descriptions embedded inline. The fix uses a short introduction and a dash-separated field description format. Code tokens in backticks count as one word each.*

OpenAPI schema that documents the same fields — each field is its own entry, mirroring the list:

```yaml
# STE: A GET request to /users/{id} returns a JSON response with these fields:
#   - id — The unique user identifier (UUID string)
#   - username — The display name
#   - email — The verified email address
#   - created_at — The account creation timestamp (ISO 8601)
#   - status — The account status (active, suspended, or pending_verification)
components:
  schemas:
    User:
      type: object
      properties:
        id:         { type: string, format: uuid }
        username:   { type: string }
        email:      { type: string, format: email }
        created_at: { type: string, format: date-time }
        status:     { type: string, enum: [active, suspended, pending_verification] }
```

### Example 5 — Docstring: Raised Exceptions

> **Non-STE:** This method can potentially raise the following exception types under various error conditions that the caller should be prepared to handle with appropriate try-catch blocks: a ValueError when the input string cannot be parsed into a valid integer representation, a TypeError when the provided argument is not a string type as expected by the parser, and an OverflowError when the parsed integer value exceeds the maximum allowed size for the platform's native integer type.
>
> **STE:** This method can raise these exceptions:
>
> - ValueError — The input string is not a valid integer.
> - TypeError — The argument is not a string.
> - OverflowError — The parsed value is too large for the platform.
>
> *Principles applied: P2 (descriptive sentence, 6 words before colon). The original introduction contained 29 words with redundant "try-catch" guidance. The fix puts the exception name and condition in each list item. The caller's responsibility to handle exceptions is implied by the method contract and does not need to be repeated.*

Python function where the docstring matches the `raise` statements:

```python
def parse_int(text):
    """Convert a string to an integer.

    This method can raise these exceptions:
      - ValueError — The input string is not a valid integer.
      - TypeError — The argument is not a string.
      - OverflowError — The parsed value is too large for the platform.
    """
    if not isinstance(text, str):
        raise TypeError("The argument is not a string.")
    try:
        value = int(text)
    except ValueError as exc:
        raise ValueError("The input string is not a valid integer.") from exc
    return value
```

### Example 6 — Commit Message: Breaking Changes

> **Non-STE:** This release introduces several breaking changes that affect the public API surface and require updates to existing integration code in downstream projects that consume this library: the authenticate function now returns a Promise instead of accepting a callback as its final parameter, the User type no longer includes the deprecated avatarUrl field which has been moved to the Profile type, and the minimum supported Node.js version has been increased from 16 to 18.
>
> **STE:** This release introduces these breaking changes:
>
> - The `authenticate` function returns a Promise. It no longer accepts a callback.
> - The `User` type does not include the `avatarUrl` field. Use the `Profile` type instead.
> - The minimum Node.js version is now 18 (was 16).
>
> *Principles applied: P2 (descriptive sentence, 7 words before colon). The original introduction was 48 words and described the nature of the changes instead of letting the list items speak. Each list item is now a descriptive or imperative sentence under 25 words.*

```text
Subject:  Bump to v3.0.0 with auth and type breaking changes

This release introduces these breaking changes:
- The `authenticate` function returns a Promise. It no longer accepts a callback.
- The `User` type does not include the `avatarUrl` field. Use the `Profile` type instead.
- The minimum Node.js version is now 18 (was 16).
```

### Example 7 — Error Message: Validation Errors

> **Non-STE:** The configuration file failed validation because of the following problems that must be fixed before the application can start and accept any incoming requests: the server.port value of "0" is not within the allowed range of 1024 to 65535 for privileged and non-privileged ports respectively, the database.url field is empty but is marked as required in the configuration schema, and the logging.level field contains "verbose" which is not one of the recognized log level values.
>
> **STE:** The configuration file has these problems:
>
> - The server.port value "0" is not in the range 1024 to 65535.
> - The database.url field is empty. This field is required.
> - The logging.level value "verbose" is not a valid log level.
>
> *Principles applied: P1 (short introduction, 6 words before colon), P2 (list items as new sentences). The original introduction was 42 words. Each list item now obeys the 25-word descriptive limit. The recovery instruction is implicit in the error format and does not need a separate "must be fixed" preamble.*

Validation routine that builds the message from the same list:

```python
# STE: the error uses a short introduction and one item per problem.
errors = []
if not (1024 <= cfg.server.port <= 65535):
    errors.append(f'The server.port value "{cfg.server.port}" is not in the range 1024 to 65535.')
if not cfg.database.url:
    errors.append("The database.url field is empty. This field is required.")
if cfg.logging.level not in {"debug", "info", "warn", "error"}:
    errors.append(f'The logging.level value "{cfg.logging.level}" is not a valid log level.')
if errors:
    raise ConfigError("The configuration file has these problems:")
```

### Example 8 — Configuration File Comment: Option Values

> **Non-STE:** The retry_strategy option in this configuration block controls how the client handles transient network failures and supports the following strategies with different trade-offs between consistency guarantees and tail latency characteristics that you should evaluate based on your workload profile: a fixed strategy that retries with a constant delay between attempts, an exponential strategy that doubles the delay after each failed retry, and a jittered strategy that adds random variation to the delay to avoid thundering herd problems during widespread outages.
>
> **STE:** The retry_strategy option accepts these values:
>
> - fixed — Retry with a constant delay between attempts.
> - exponential — Double the delay after each failed retry.
> - jittered — Add random variation to the delay.
>
> *Principles applied: P1, P2 (short introduction, 5 words before colon). The original introduction was 57 words with trade-off analysis embedded. The fix moves the strategy descriptions to the list items. The trade-off analysis belongs in a separate paragraph below the list, not in the introduction.*

Config file where the comment documents the option as a list:

```toml
# STE: the retry_strategy option accepts these values:
#   - fixed — Retry with a constant delay between attempts.
#   - exponential — Double the delay after each failed retry.
#   - jittered — Add random variation to the delay.
# The trade-off analysis belongs in a separate paragraph below the list,
# not in the introduction.
retry_strategy = "exponential"
```

## Edge Cases

### Edge Case 1 — When the Introductory Text Contains Inline Code

Code tokens inside backticks in the introductory text count as one word each, regardless of their character length. This means `docker-compose` counts as one word, and `com.example.service.UserRepository` also counts as one word. A long code token does not inflate the word count of the introduction.

However, this can create a false sense of compliance. An introduction that is technically 25 words but contains 12 code tokens is hard to read. Use the word-count limit as a ceiling, not a target. Prefer introductions with one or zero code tokens and fewer than 15 total words.

> **STE:** The `UserRepository` interface declares these methods: (6 words)
>
> - `findById(id: UserId): Option<User>`
> - `save(user: User): Result<(), Error>`
> - `delete(id: UserId): Result<(), Error>`.

> *The introduction uses one code token and six total words. Each list item is a function signature that counts as one "word" in STE-Code counting rules because it is a single code token.*

### Edge Case 2 — Nested Vertical Lists

A vertical list item can itself contain a nested vertical list. In this case, the parent list item is a sentence with its own word-count limit (20 procedural, 25 descriptive). The nested list has its own introductory text and its own colon, each subject to the same limits.

Guidance: Limit nesting to one level. A list item that introduces a nested list should be short — it serves only as a category heading. The nested list items carry the detail. If you find yourself writing a three-level nested list, restructure the content with subheadings.

> **STE:** The build system supports these output formats:
>
> - JavaScript bundles:
>   - ES module format
>   - CommonJS format
>   - UMD format.
> - CSS bundles:
>   - Standard CSS
>   - CSS modules.

> *The parent list items ("JavaScript bundles:" and "CSS bundles:") are short category headings. Each has its own colon and its own nested list. The structure stays at two levels.*

### Edge Case 3 — Code Blocks Inside List Items

A list item can contain a fenced code block. In this case, the list item's prose text must obey the word-count limit. The code block itself is exempt from word counting — it is code, not documentation prose. The code block does not contribute to the list item's word count.

Guidance: Use a short introductory sentence in the list item ("The command has this format:"), then place the code block. Do not put a long explanation before the code block inside a single list item. If the explanation is long, split it: one list item for the explanation, another for the code block.

> **STE:** The configuration file uses this format:
>
> - The `[server]` section sets the host and port:
>
>   ```
>   [server]
>   host = "0.0.0.0"
>   port = 8080
>   ```
>
> - The `[database]` section sets the connection parameters:
>
>   ```
>   [database]
>   url = "postgres://localhost:5432/app"
>   pool_size = 10
>   ```

> *Each list item has a short prose introduction followed by a code block. The prose introductions are 8 and 7 words respectively — well under the limit. The code blocks contribute zero words to the count.*

### Edge Case 4 — When a Framework or Tool Name Pushes the Introduction Over the Limit

Some framework names, API endpoint paths, or tool names are long by nature. For example, `KubernetesHorizontalPodAutoscaler` is a single code token but a visually heavy one. When the introduction must include several such names, the word count can appear within limits while the visual density is high.

Guidance: If the introduction feels visually heavy even when technically compliant, rewrite it. Move the long names into the list items. Use a generic introduction and let each list item introduce its own subject.

> **Non-STE:** The KubernetesHorizontalPodAutoscaler, PrometheusServiceMonitor, and IstioVirtualService custom resources support these configuration annotations: (10 words, but visually dense)
>
> **STE:** These custom resources support configuration annotations:
>
> - KubernetesHorizontalPodAutoscaler
> - PrometheusServiceMonitor
> - IstioVirtualService.
>
> *Principles applied: P1, P9 (prefer short, clear technical nouns in the introduction). The fix moves the long resource names into the list items. The introduction is now 6 common words with no code tokens. The reader processes the introduction quickly and encounters the domain-specific names in a scannable list.*

### Edge Case 5 — Generated Documentation with Automatic Colon-List Structures

Auto-generated API documentation (OpenAPI/Swagger UI, JSDoc HTML output, Sphinx autodoc, `--help` CLI output) often produces vertical lists with colons automatically. The generator controls the introduction text and the list formatting. The writer cannot always control the word count of the generated introduction.

Guidance: When you write the source comments or annotations that feed the generator, obey Rule 8.4. When the generator renders the output, accept its default formatting. If the generator produces introductions that consistently violate word-count limits, file an issue with the generator project. For hand-written documentation (README files, standalone API docs, commit messages), Rule 8.4 applies in full.

> **NOTE:** CLI `--help` output generated by argument parsers (clap for Rust, argparse for Python, cobra for Go) is often auto-formatted. The help text for each flag or argument becomes a list item. You control the help text you write in the source code. You do not control the generated list introduction ("Options:", "Commands:", "Arguments:"). Focus your compliance effort on the help text you author, not on the generator's boilerplate.

## Cross-References

- **Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs:** The words in your list introductions and list items must come from the STE-Code approved dictionary. Use the canonical synonyms (get, set, check, use) in list items. Do not use non-approved words just because a list item gives you a fresh sentence boundary.
- **Rule 1.3 — Use Approved Words Only with Their Approved Meanings:** When a list item describes a function's return value, make sure the verb "return" carries its approved meaning. Do not use "return" to mean "send back to the caller" in one list item and "produce as output" in another. Consistency across list items is mandatory.
- **Rule 3.1 — Use only the verb forms that are given in the dictionary:** Each list item after a colon is a new sentence. It must obey Rule 3.1: one subject, one verb, one object. Do not nest clauses inside a list item. If a list item feels complex, split it into two list items.
- **Rule 3.3 — Use the past participle form as an adjective:** Vertical lists are a way to obey Rule 3.3 organically. A dense paragraph with a buried enumeration can be restructured as a short introduction plus a vertical list. The combined structure satisfies both Rule 3.3 and Rule 8.4.
- **Rule 4.1 — One Topic Per Sentence, No Abstract Text:** Rule 8.4 enforces Rule 4.1 at two points: the introduction before the colon (20/25 words) and each list item (20/25 words). A document that passes Rule 4.1 on all prose sentences can still fail Rule 8.4 on its vertical list introductions. Check both.
- **Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.:** Procedural vertical lists are the standard format for step-by-step instructions. Rule 6.3 governs when to use a list for procedures. Rule 8.4 governs the word counts within those lists. Together, they define the structure and the length of procedural documentation.
- **Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;):** The semicolon ban in Rule 8.1 means writers cannot use semicolons to join list items into a single sentence. They must use a vertical list with a colon instead. The colon in Rule 8.4 is the approved replacement for semicolon-joined enumerations.
- **STE-Code Dictionary — Section: Punctuation:** The dictionary defines the colon (:) as a sentence-boundary punctuation mark in the context of vertical lists. It also defines the period (.), question mark (?), and exclamation mark (!) as the other sentence terminators. Consult the dictionary for the full set of approved sentence boundaries.

## Grammar Notes

### The Colon as a Sentence Boundary

In standard English grammar, the colon can serve several functions: it introduces a list, it introduces an explanation, it introduces a quotation, or it separates independent clauses where the second clause explains the first. Not all of these functions create a sentence boundary.

In STE-Code, the colon before a vertical list is always a sentence boundary. The text before the colon is a complete sentence that ends at the colon. The text after the colon consists of separate sentences, one per list item. This grammatical rule simplifies mechanical compliance checking: a tool can split text on the colon, count words in the introduction, and then count words in each list item independently.

This is a stricter rule than standard English grammar, which permits a colon to appear mid-sentence in constructions like "The algorithm needs three inputs: X, Y, and Z." In STE-Code, this construction becomes:

> The algorithm needs these inputs:
>
> - X
> - Y
> - Z.

The colon always ends the introductory sentence. The enumerated items are always vertical, never inline.

### Vertical List Items as Independent Clauses

In standard English, vertical list items can be fragments (noun phrases, verb phrases, prepositional phrases) or complete sentences. STE-Code inherits this flexibility but adds the word-count rule: whether a list item is a fragment or a complete sentence, it must not exceed the word limit.

This creates an interesting tension. A fragment like "Database connection timeout" is 3 words and trivially compliant. But a fragment does not always give enough information. A complete sentence like "The database connection timed out because the primary node was unreachable" is 11 words — compliant but borderline. The writer must balance completeness against conciseness.

Guidance: When a list item needs more than 15 words to be complete, it probably contains two ideas. Split it into two list items. A vertical list of 8 short items is easier to read than a list of 4 long items. The visual structure of the list makes fragmentation acceptable — the reader uses the list introduction to establish the context, so each item can be terse.

### Word Counting Mechanics

The mechanics of word counting in vertical list contexts:

- **Introduction:** Count all words from the first word of the introductory sentence through the word before the colon. The colon itself is not a word. Parenthetical word counts in examples are for training and are not required in production text.
- **List items:** Count all words in each list item. If a list item contains a period at the end, the period is not a word. If a list item contains inline code in backticks, each backtick-delimited token counts as one word.
- **Nested lists:** Count the words in the parent list item up to its colon. Then count the words in each nested list item. The parent list item's word count does not include the nested list items.

A tool can verify Rule 8.4 compliance mechanically: (1) find all colons followed by a newline and a list marker, (2) count words in the text before each such colon, (3) count words in each list item, (4) flag any sentence that exceeds its type-specific limit.

### Parallel Structure in List Items

Rule 8.4 does not explicitly require parallel structure across list items, but parallel structure is a natural consequence of the rule. When each list item is a new sentence with its own subject and verb, and the introduction establishes the shared context, the items tend toward parallel structure organically.

If the first list item starts with a noun phrase ("Database connection timeout"), all items should start with noun phrases. If the first item is an imperative verb ("Check the database connection"), all items should be imperative verbs. Mixing structures within one vertical list violates Rule 6.3 (consistency in procedural lists) and makes the list harder to scan.

### The Colon Versus the Em-Dash in List Introductions

Some writers use an em-dash (—) instead of a colon to introduce a vertical list. In standard English, this is a stylistic choice. In STE-Code, only the colon is approved for vertical list introductions. The em-dash is reserved for parenthetical asides and emphasis — it does not function as a sentence boundary in the STE-Code punctuation model.

If you encounter a vertical list introduced by an em-dash, replace the em-dash with a colon. Count the words in the introduction as usual. The replacement is mechanical and does not require rewriting the introduction.

### Historical Context and Domain Origins

The ASD-STE100 vertical list rule (Rule 8.4 in the original specification) was designed for technical manuals, where a vertical list of components, tools, or steps is the primary documentation format. The colon divides the procedural context ("To remove the pump, disconnect these hoses:") from the actionable items. The word-count limit prevents the context from overwhelming the items.

In code documentation, the same principle applies with different nouns. Instead of "hoses" and "pumps," the list enumerates parameters, return values, exceptions, dependencies, or steps. The structural need is identical: a short context-setter followed by a scannable list of items. The rule has been tested in high-stakes operational environments where misreading a list item causes real harm. In software, the stakes are lower but the readability benefit is the same.

## See Also

> **See also:** Rule 1.1 — Use Words That Are Approved in the Dictionary, Technical Nouns, or Technical Verbs

> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings

> **See also:** Rule 3.1 — Use only the verb forms that are given in the dictionary.

> **See also:** Rule 3.3 — Use the past participle form as an adjective.

> **See also:** Rule 4.1 — One Topic Per Sentence, No Abstract Text

> **See also:** Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence.

> **See also:** Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

