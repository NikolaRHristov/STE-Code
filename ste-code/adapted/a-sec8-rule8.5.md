# Rule 8.5 — Parentheses and Word Count

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.5

> **Source:** [master.md#sec8-rule8.5](ste-code/grouped/)

## Original Rule

**Rule 8.5** When you put text in parentheses, it counts as one word in that sentence.

When you count words for sentence length, text in parentheses counts as one word of that sentence. But the words that you put between parentheses also make a new sentence. Thus, count them in that different sentence.

> **STE:** Make sure that the EMER pushbutton switch is released (the EMER legend is off).

(This sentence has 10 words, because the text in parentheses counts as one word. The sentence in parentheses has 5 words and counts as a different sentence.)

If there is an identifier in parentheses (a number, a letter, or an alphanumeric identifier), this identifier counts as one word in the sentence. Abbreviations in parentheses also count as one word.

> **STE:** Remove the safety pin (10). (5 words)
> **STE:** Installation of a Business Class (B/C) Seat (7 words)

| Example | Text |

|---------|------|

| | Hardware and Software Configuration Check of the In-Flight Entertainment (IFE) System (11 words) |

## STE-Code Adaptation

**Rule 8.5** In code documentation, when you put text in parentheses, it counts as one word in that sentence.

When you count words for sentence length, text in parentheses counts as one word of that sentence. But the words that you put between parentheses also make a new sentence. Thus, count them in that different sentence.

If there is an identifier in parentheses (a number, a letter, or an alphanumeric identifier), this identifier counts as one word in the sentence. Abbreviations in parentheses also count as one word.

### Examples

> **Non-STE:** Make sure that the DEBUG environment variable is set to false before you run the deployment script in the production cluster (the DEBUG flag must be explicitly disabled for all production workloads to prevent accidental log leakage).
>
> **STE:** Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off). (12 words)
>
> *Adapted from spec pair: "Make sure that the EMER pushbutton switch is released (the EMER legend is off)." — text in parentheses counts as one word in the main sentence but forms a separate sentence.*

(This sentence has 12 words, because the text in parentheses counts as one word. The sentence in parentheses has 5 words and counts as a different sentence.)

> **Non-STE:** Remove the health check flag number ten from the deployment configuration.
>
> **STE:** Remove the health check flag (10). (5 words)
>
> *Adapted from spec pair: "Remove the safety pin (10)." — identifier in parentheses counts as one word.*

> **Non-STE:** Installation and Configuration of a Continuous Integration and Continuous Deployment Pipeline for the Application
>
> **STE:** Configuration of a Continuous Integration/Continuous Deployment (CI/CD) Pipeline (7 words)
>
> *Adapted from spec pair: "Installation of a Business Class (B/C) Seat" — abbreviation in parentheses counts as one word.*

## Code-Domain Explanation

Rule 8.5 governs how parenthetical text affects word counting in all code documentation. The rule has two parts: (1) the parenthetical block counts as exactly one word in the enclosing sentence, and (2) the words inside the parentheses form their own separate sentence with their own word-count limit. This dual counting system lets the writer add clarifying asides without inflating the word count of the main sentence, while still enforcing brevity on the aside itself.

The most important practical effect of Rule 8.5 is that parentheses become a tool for managing sentence length. When a sentence approaches the 20-word procedural limit or the 25-word descriptive limit, moving qualifying information into parentheses reduces the main sentence's word count by the length of the moved text minus one. This is not a loophole — it is the intended mechanism. The parenthetical text remains subject to the same length limits as any other sentence. A parenthetical with 30 words violates the spirit of the rule even though the main sentence gains only one word.

A secondary effect is that parentheses create a hierarchy of attention. The main sentence carries the primary message. The parenthetical carries secondary or clarifying information. A reader who skips the parenthetical should still understand the main sentence. If the parenthetical contains mission-critical information, the information belongs in the main sentence, not in parentheses.

### README Files

README files use parentheses for version qualifications, platform notes, and dependency clarifications. A common violation: the writer puts long conditional instructions inside parentheses, creating a parenthetical sentence that far exceeds the 25-word descriptive limit. The parenthetical becomes a second paragraph hidden inside the first.

Example of a parenthetical violation in a README installation section:

````
Install the package with pip (if you are using a virtual environment
which we strongly recommend for all Python projects to avoid dependency
conflicts with system-level packages, make sure you activate it first
with the source venv/bin/activate command before running the install).
````

The parenthetical has 35 words — 10 over the descriptive limit. The fix splits the aside into its own sentence or moves it before the instruction:

````
We recommend that you use a virtual environment. Activate it with the
`source venv/bin/activate` command. Then install the package with pip.
````

### API Documentation

API documentation uses parentheses for HTTP status codes, content types, default values, and optionality markers. These parenthetical identifiers (200, 404, application/json, optional) count as one word each. They do not inflate the word count of endpoint descriptions.

A common violation: the writer uses parentheses to embed full conditional logic inside a parameter description. The parenthetical describes when the parameter is required, what it defaults to, and how it interacts with other parameters — all inside one pair of parentheses.

Example of a violation in an API parameter description:

````
The timeout parameter sets the request timeout in seconds (this
parameter is optional and defaults to 30 if not provided, but if
you set retries to a value greater than zero you should increase
the timeout accordingly to account for the cumulative wait time
across all retry attempts).
````

The parenthetical is 43 words. The fix moves the conditional guidance to a separate paragraph or a NOTE:

````
The timeout parameter sets the request timeout in seconds. The
default value is 30. This parameter is optional.

NOTE: If you set retries to a value larger than zero, increase the
timeout to account for the cumulative wait time.
````

### Docstrings and Inline Comments

Docstrings use parentheses for type annotations in some formats, default value indicators, and short clarifications about parameter behavior. Parentheses in docstrings are usually short — `(int, optional)`, `(default: 30)`, `(in seconds)` — and trivially comply with Rule 8.5.

The risk appears when a docstring uses parentheses to embed a full algorithmic explanation or a caution about side effects. The writer tries to keep the docstring concise by parenthesizing the complex part, but the parenthetical itself becomes a dense paragraph.

Example of a violation in a Python docstring:

````
def connect(timeout: int) -> Connection:
    """Open a connection to the database server.

    The timeout parameter controls how long the client waits for a
    response (this timeout applies to the initial TCP handshake only
    and does not cover query execution time, which is controlled by
    the separate query_timeout parameter on the Connection object
    returned by this function).
    """
````

The parenthetical is 32 words. The fix makes it a separate sentence or a separate paragraph:

````
def connect(timeout: int) -> Connection:
    """Open a connection to the database server.

    The timeout parameter controls how long the client waits for the
    initial TCP handshake. It does not cover query execution time.
    Use the query_timeout parameter on the returned Connection object
    to control query execution time.
    """
````

### Commit Messages

Commit messages use parentheses for issue tracker references, breaking change indicators, and scope qualifiers. These are almost always identifiers: `(#1234)`, `(breaking)`, `(auth)`. As identifiers, they count as one word each.

A common violation in longer commit message bodies: the writer uses parentheses to add retrospective commentary or justification for the change. This commentary belongs in the commit body as a separate paragraph, not in parentheses.

Example of a violation in a commit message body:

````
This commit removes the deprecated User.findByEmail method (this
method was deprecated in v2.1 and had a known bug where it returned
stale results from the cache when the underlying database record
had been updated by another process, which caused several production
incidents in the billing service).
````

The parenthetical has 41 words. The fix separates the justification:

````
This commit removes the deprecated User.findByEmail method.

This method was deprecated in v2.1. It had a known bug: it returned
stale cache results when another process updated the database record.
This bug caused production incidents in the billing service.
````

### Error Messages

Error messages use parentheses for error codes, suggested actions, and contextual data. These are usually short: `(Error code: EACCES)`, `(try: chmod 600)`, `(file: config.yaml)`. Each parenthetical is a separate sentence and must stay under the word-count limit.

A common violation: the error message puts the entire recovery procedure in parentheses, creating a procedural parenthetical that exceeds 20 words. Recovery instructions should be separate sentences, not parenthetical asides.

Example of a violation in a CLI error message:

````
Error: Cannot write to the configuration file (check that the file
exists and is not read-only, that the parent directory is writable,
and that your user account has the necessary file permissions — you
can use the ls -l command to inspect permissions and chmod to change
them if you have sufficient privileges).
````

The parenthetical is 46 words. The fix:

````
Error: Cannot write to the configuration file.

To fix this problem:
- Make sure that the file exists.
- Make sure that the file is not read-only.
- Make sure that the parent directory is writable.
- Make sure that your user account has the necessary permissions.

Use the `ls -l` command to inspect permissions. Use the `chmod`
command to change them.
````

## Paradigm-Specific Guidance

### Object-Oriented Paradigm (Java, C++, C#, Python classes)

In OOP documentation, parentheses appear most often around type names, class references, and design pattern qualifiers. These are identifier parentheses and count as one word each: `(User)`, `(abstract)`, `(Factory pattern)`.

A common OOP-specific violation: the writer uses parentheses to embed inheritance justifications or interface contract explanations inside class-level docstrings. The parenthetical describes why a class extends another class or implements an interface in a specific way. This design rationale belongs in a separate paragraph, not in a parenthetical aside.

Example of a violation in a Java class docstring:

````
The CachingUserRepository extends the BaseRepository class and
implements the UserRepository interface (the BaseRepository provides
generic CRUD operations with connection pooling, and UserRepository
adds user-specific query methods — we extend rather than compose
because the caching layer needs access to protected connection
management methods on BaseRepository).
````

The fix separates the design rationale:

````
The CachingUserRepository extends the BaseRepository class. It
implements the UserRepository interface.

The BaseRepository class provides generic CRUD operations with
connection pooling. The UserRepository interface adds user-specific
query methods. This class extends BaseRepository rather than
composing it. The caching layer needs access to protected
connection management methods.
````

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

In functional documentation, parentheses appear around type parameters, pattern match conditions, and guard clauses. These are often short and trivially compliant: `(Eq a)`, `(when x > 0)`, `(:else)`.

A functional-specific violation: the writer uses parentheses to embed a full explanation of a monadic transformation or a lazy evaluation behavior inside a function description. Functional paradigms favor composition and transformation chains — writers sometimes try to parenthesize the entire chain description.

Example of a violation in a Rust function docstring:

````
The transform function applies a series of operations to the input
stream (it first filters out all None values using filter_map, then
converts each remaining value through the provided mapper function,
and finally collects the results into a Vec — the entire chain is
lazy and does not allocate until collect is called at the end).
````

The fix moves the chain description to a separate paragraph:

````
The transform function applies a series of operations to the input
stream.

The function does these steps:
- Remove all None values with filter_map.
- Convert each remaining value with the mapper function.
- Collect the results into a Vec.

The chain is lazy. It does not allocate until collect is called.
````

### Procedural Paradigm (C, Go, Bash)

In procedural documentation, parentheses appear around exit codes, flag values, and short condition qualifiers: `(exit code 1)`, `(-v)`, `(if root)`. These are identifier parentheses and count as one word.

A procedural-specific violation: the writer uses parentheses to embed error-handling logic inside a step description. The parenthetical describes the full if-else branching for an error condition. Procedural documentation should use separate sentences or a NOTE block for error handling.

Example of a violation in a Go function docstring:

````
WriteConfig saves the application configuration to the specified
file path (if the file already exists, the function returns an
ErrExists error and the caller must check for this error and decide
whether to overwrite by calling WriteConfigForce or to abort — if
the parent directory does not exist, the function creates it with
0755 permissions before writing).
````

The fix separates the error conditions:

````
WriteConfig saves the application configuration to the specified
file path.

If the file exists, the function returns an ErrExists error. The
caller must check for this error. To overwrite the file, call
WriteConfigForce. To abort, return the error.

If the parent directory does not exist, the function creates it with
0755 permissions.
````

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

In declarative documentation, parentheses appear around allowed values, validation constraints, and version qualifiers: `(PostgreSQL 14+)`, `(required)`, `(default: true)`. These are short and usually compliant.

A declarative-specific violation: the writer uses parentheses to embed migration instructions or backward-compatibility notes inside a resource property description. Declarative configurations often evolve across versions, and the writer tries to capture the full evolution history in a parenthetical.

Example of a violation in a Terraform variable description:

````
The schema_version variable sets the database schema version (in
version 1.x of this module the default was "13" but in version 2.x
the default changed to "15" — if you are upgrading from 1.x you
must run the database migration script before changing this value
to avoid data loss, and you should also update the parameter group
family to match the new schema version).
````

The fix:

````
The schema_version variable sets the database schema version. The
default value is "15".

BREAKING: The default value changed from "13" in version 1.x to
"15" in version 2.x. Before you change this value during an upgrade,
run the database migration script. Also update the parameter group
family to match the new version.
````

### Systems Paradigm (Rust ownership docs, C memory docs)

In systems documentation, parentheses appear around safety preconditions, lifetime constraints, and UB (Undefined Behavior) qualifiers. These are safety-critical. A parenthetical that buries a safety precondition is a parenthetical that a developer might skip — and skipping a safety precondition in systems code can cause memory corruption.

The systems-specific rule is stricter than the general rule: do not put safety-critical information in parentheses. Put it in the main sentence or in its own `# Safety` section. Parentheses in systems documentation should contain only secondary clarifications, never preconditions.

Example of a violation in a Rust unsafe function docstring:

````
The set_ptr function writes a value to the memory location that
the pointer refers to (the caller must ensure that the pointer is
valid for writes, that it is properly aligned for type T, and that
no other thread holds a reference to the same memory location
during the write — violating any of these conditions causes
undefined behavior).
````

The parenthetical contains the safety contract. The safety contract should not be in parentheses. The fix:

````
The set_ptr function writes a value to the memory location that the
pointer refers to.

# Safety

The caller must obey these conditions:
- The pointer must be valid for writes.
- The pointer must be properly aligned for type T.
- No other thread must hold a reference to the same memory location
  during the write.

If any of these conditions is not obeyed, the behavior is undefined.
````

## Extended Examples

### Example 4 — README: Version-Dependent Instruction

> **Non-STE:** Run the database migration script to upgrade your schema (if you are currently running version 2.3.x or earlier you must first apply the intermediate migration for version 2.4 because the 2.5 migration depends on schema changes that were introduced in the 2.4 release cycle and cannot be applied directly to a pre-2.4 database without causing migration failures and potential data corruption).
>
> **STE:** Run the database migration script. If you use version 2.3.x or earlier, apply the version 2.4 migration first (the 2.5 migration needs schema changes from version 2.4). (12 words in the main sentence, 7 words in the parenthetical)
>
> *Principles applied: P3 (use words with approved meanings — "needs" instead of "depends on"), Rule 8.5 (the parenthetical counts as one word in the second sentence and forms a separate 7-word sentence). The original parenthetical was 57 words and buried a data-corruption warning. The fix splits the instruction into two sentences and uses a short parenthetical for the rationale.*

### Example 5 — API Documentation: Status Code Parentheses

> **Non-STE:** A successful deletion operation returns an HTTP 204 No Content response with an empty body and no further information about the deleted resource (if the resource was already deleted or never existed the endpoint returns 404 Not Found to maintain idempotency guarantees, and if the caller does not have delete permissions on the parent collection the endpoint returns 403 Forbidden).
>
> **STE:** A successful deletion returns an HTTP 204 status code (No Content). The response body is empty. If the resource was already deleted, the endpoint returns 404 (Not Found). If the caller does not have delete permissions, the endpoint returns 403 (Forbidden).
>
> *Principles applied: P1 (use "successful" instead of "returns successfully"), Rule 8.5 (each status code explanation in parentheses counts as one word in its sentence and forms a separate sentence). The original used one sentence with a 54-word parenthetical that described three different response scenarios. The fix separates each scenario into its own sentence with short parenthetical status code names.*

### Example 6 — Docstring: Default Value with Condition

> **Non-STE:** The cache_ttl parameter (which controls how many seconds cached entries remain valid before they are automatically evicted by the background cleanup worker that runs every 60 seconds by default) accepts any positive integer value greater than zero.
>
> **STE:** The cache_ttl parameter sets the cache time-to-live in seconds (default: 300). The value must be a positive integer. A background worker removes expired entries (the worker runs every 60 seconds).
>
> *Principles applied: Rule 8.5 (each parenthetical counts as one word and forms a separate sentence), P2 (the word "set" replaces "controls" — approved word from the STE-Code dictionary). The original had a 31-word parenthetical embedded in the middle of the parameter description. The fix uses three sentences with two short parentheticals (3 words and 4 words).*

### Example 7 — Commit Message: Issue Reference

> **Non-STE:** Fix the race condition in the connection pool that caused sporadic test failures in CI when multiple test workers tried to acquire connections simultaneously during high-load periods on shared CI runners (this issue was reported by the QA team in ticket PROJ-2847 and was initially thought to be a test environment problem but turned out to be a genuine concurrency bug in the pool implementation that only manifested under specific timing conditions).
>
> **STE:** Fix a race condition in the connection pool (PROJ-2847). The bug caused test failures when many workers acquired connections at the same time on shared CI runners.
>
> *Principles applied: Rule 8.5 (the issue reference "PROJ-2847" is an alphanumeric identifier in parentheses — counts as one word, forms a 1-word separate sentence), P5 (technical code nouns like "connection pool" and "CI runners" are allowed). The original had a 57-word parenthetical with investigative history. The fix moves the issue reference to a short parenthetical and separates the description.*

### Example 8 — Error Message: Error Code with Recovery Hint

> **Non-STE:** Failed to bind to port 8080 because the address is already in use by another process that was started previously and is still holding the socket open on that port number (you can identify the process using the lsof -i :8080 command and then stop it with kill followed by the process ID, or you can configure this application to use a different port by setting the PORT environment variable to an alternative value such as 3000 or 9090 before restarting).
>
> **STE:** Cannot bind to port 8080 (EADDRINUSE). The address is in use. To find the process, run `lsof -i :8080`. To use a different port, set the PORT environment variable (example: 3000). Then restart the application.
>
> *Principles applied: Rule 8.5 (the error code "EADDRINUSE" in parentheses counts as one word, the example value "3000" in parentheses counts as one word), P1 (use "cannot" instead of "failed to" — approved word). The original had a 71-word parenthetical containing both diagnostic and recovery instructions. The fix separates the error identification, diagnostic step, and recovery steps into distinct sentences with short parenthetical identifiers.*

### Example 9 — Configuration File Comment: Allowed Range

> **Non-STE:** The max_connections setting controls the upper limit of simultaneous database connections that the application will open (the valid range for this value is between 10 and 1000 inclusive because values below 10 can cause connection starvation under normal load and values above 1000 can exhaust the database server's connection limit which is typically configured to 1000 by default in most PostgreSQL installations unless the system administrator has adjusted the max_connections server parameter).
>
> **STE:** The max_connections setting controls the largest number of simultaneous database connections. The valid range is 10 to 1000 (inclusive). Values below 10 can cause connection starvation. Values above 1000 can exhaust the database server limit.
>
> *Principles applied: Rule 8.5 (the qualifier "(inclusive)" counts as one word), P2 (use "largest" instead of "upper limit" — approved adjective form). The original had a 55-word parenthetical that embedded the full range rationale. The fix breaks the rationale into separate sentences and uses a one-word parenthetical for the range qualifier.*

## Edge Cases

### Edge Case 1 — When a Function Call Name Looks Like a Parenthetical

Code documentation often includes function names followed by parentheses: `authenticate()`, `parse(input)`, `User.find(id)`. In prose documentation, these function-call notations use parentheses as part of the code token, not as STE-Code parenthetical boundaries. A code token inside backticks that contains parentheses (`authenticate()`) counts as one word total. The parentheses inside the token do not create a separate sentence.

Guidance: Backtick-delimited code tokens are atomic. A token like `setTimeout(callback, 1000)` is one word regardless of its internal parentheses. Only parentheses that appear outside backticks in the documentation prose trigger Rule 8.5 counting.

> **STE:** Call the `authenticate()` function. Then call `validate(token)`. (6 words)

> *The parentheses inside the backtick-delimited code tokens are part of the token, not Rule 8.5 parentheticals. The sentence has six prose words. The code tokens count as one word each.*

### Edge Case 2 — When Parentheses Contain a URL

Documentation sometimes places a URL in parentheses: `(https://example.com/docs)`. A URL is a single identifier for word-count purposes — it counts as one word. The URL does not need to obey the 20/25-word limit as a separate sentence because it is an identifier, not a prose sentence. This is consistent with the rule for alphanumeric identifiers in parentheses.

Guidance: Treat URLs in parentheses as identifiers. Count them as one word. Do not attempt to count the words inside the URL (slashes, dots, hyphens are not word boundaries). If the parenthetical contains both a URL and explanatory text, the explanatory text forms a sentence and must obey the word-count limit.

> **STE:** Read the deployment guide (https://example.com/deploy). (6 words)
> **STE:** Read the deployment guide (https://example.com/deploy — this guide has the full procedure). (6 words in the main sentence, 5 words in the parenthetical)

> *In the first example, the URL alone is an identifier parenthetical (1 word). In the second example, the parenthetical contains text after the URL (5 words) and forms a separate sentence.*

### Edge Case 3 — Nested Parentheses

Standard English permits nested parentheses in some contexts, but they are difficult to parse. In code documentation, nested parentheses create ambiguity about which closing parenthesis ends which parenthetical. The reader must mentally pair the delimiters.

Guidance: Do not use nested parentheses in STE-Code documentation. If you have a parenthetical that itself needs a parenthetical, restructure the content. Use an em-dash for the inner aside, or move one level of the aside to a separate sentence.

> **Non-STE:** The function returns a Result type (which can be either Ok (containing the parsed value) or Err (containing a ParseError)).
>
> **STE:** The function returns a Result type. The Result is either Ok (containing the parsed value) or Err (containing a ParseError).
>
> *Principles applied: Rule 8.5 (each single-level parenthetical counts as one word), P3 (use approved meanings). The original had nested parentheses — the inner parentheticals "(containing the parsed value)" and "(containing a ParseError)" were nested inside an outer parenthetical. The fix eliminates one level by making the outer parenthetical a separate sentence.*

### Edge Case 4 — When a Library or Framework Name Contains Parentheses

Some library names or API method names include parentheses as part of their canonical spelling. For example, a test framework might have a method literally called `expect()` with the parentheses as part of the API name. When you write documentation about this method, the parentheses are part of the technical noun, not Rule 8.5 punctuation.

Guidance: When a framework or tool name includes parentheses as part of its identifier, place the name in backticks. The backtick-delimited token is atomic and counts as one word. If you must write the name without backticks (in a heading, for example), treat the parentheses as part of the identifier and count the entire name as one word.

> **STE:** The `expect()` method checks a value against a condition. (8 words)

> *The `expect()` token is one word. The parentheses are part of the method signature, not a Rule 8.5 parenthetical.*

### Edge Case 5 — When Parentheses Appear in Generated Documentation

Auto-generated documentation (OpenAPI/Swagger, JSDoc, Sphinx autodoc, `--help` output) often inserts parentheses around type information, default values, and optionality markers automatically: `timeout (int, optional)`, `port (default: 8080)`. These generated parentheticals are usually short and automatically compliant.

Guidance: When you author the source annotations that feed the generator, follow Rule 8.5 for any parentheticals you write manually. When the generator inserts its own parentheticals (type hints, defaults), accept the generated output. If the generator produces parentheticals that consistently exceed 25 words, the generator likely has a configuration bug — file an issue with the generator project.

For CLI `--help` output: argument parsers often append parenthetical defaults automatically (`--port PORT (default: 8080)`). You control the help text you write in the source code. You do not control the auto-appended parenthetical. Focus your compliance effort on the help text you author.

## Cross-References

- **Rule 1.5 — Technical Code Nouns Are Allowed:** When a parenthetical contains a code noun (a class name, a function name, a framework identifier), that noun is a technical noun and is permitted. The parenthetical counting rule still applies: the code noun in parentheses counts as one word in the main sentence and as a one-word separate sentence. Example: `(UserRepository)` counts as one word.

- **Rule 1.6 — Non-Approved Words Only as Technical Code Nouns:** If a parenthetical contains a word that is not in the STE-Code dictionary, that word must be a technical code noun. Do not use parentheticals as a backdoor for non-approved descriptive words. The parenthetical's separate-sentence status does not exempt it from the approved-word rules.

- **Rule 3.1 — Use Simple Sentences:** A parenthetical counts as a separate sentence under Rule 8.5. That separate sentence must also obey Rule 3.1: one subject, one verb, one object. Do not put a complex multi-clause sentence inside parentheses. The parenthetical is a sentence, not a paragraph.

- **Rule 3.3 — Keep Paragraphs Short:** Parentheticals that grow beyond 15-20 words often indicate that the paragraph should be restructured. A long parenthetical is a sign that the paragraph has too many ideas. Split the parenthetical into its own sentence or paragraph. Rule 3.3 and Rule 8.5 work together: if the parenthetical is long enough to violate paragraph length norms, restructure.

- **Rule 4.1 — Keep Sentences Short:** The word-count limits (20 procedural, 25 descriptive) apply to the parenthetical sentence just as they apply to the main sentence. A parenthetical with 30 words violates Rule 4.1 for that separate sentence. Check the word count of every parenthetical against its sentence type.

- **Rule 8.1 — Do Not Use the Semicolon:** A semicolon inside a parenthetical is still a semicolon and is still forbidden. Do not use parentheses as a container for semicolon-joined clauses. If a parenthetical contains a semicolon, split it into two sentences. Consider whether the content even belongs in parentheses — semicolons in a parenthetical suggest the aside is too complex for its parenthetical form.

- **Rule 8.4 — Colon in a Vertical List:** A vertical list item can contain a parenthetical, and a parenthetical can contain a vertical list (rare, but possible). When these two structures combine, count words according to both rules: the parenthetical counts as one word in the list item, and the words inside the parenthetical form a separate sentence (which may itself be a vertical list with its own colon boundary).

- **STE-Code Dictionary — Section: Punctuation:** The dictionary defines parentheses as punctuation marks that create a subordinate sentence. The subordinate sentence has its own word-count limit and its own sentence-type classification (procedural or descriptive). Consult the dictionary for the full punctuation model and how parentheses interact with periods, commas, and dashes.

## Grammar Notes

### The Parenthetical as a Subordinate Sentence

In standard English grammar, a parenthetical is an aside — a phrase or clause that interrupts the main sentence to add qualifying, explanatory, or illustrative information. The parenthetical can be a fragment (a noun phrase, a prepositional phrase) or a complete clause. Standard grammar does not assign parentheticals their own sentence status.

In STE-Code, a parenthetical is always a separate sentence. This is a stricter rule than standard English. The grammatical justification: the parenthetical contains a complete thought that the writer considered important enough to include. That thought deserves the same structural discipline as any other sentence. If the thought is not important enough to be a sentence, it is not important enough to be a parenthetical — delete it.

This means that every parenthetical must have its own grammatical integrity. A fragmentary parenthetical like "(the DEBUG flag is off)" is acceptable because it is a complete clause (subject: "the DEBUG flag," verb: "is," complement: "off"). A truly fragmentary parenthetical like "(off)" is borderline — it is an identifier-style parenthetical, not a prose sentence, and should be used only for flags, states, or short qualifiers.

### Identifier Parentheticals Versus Explanatory Parentheticals

Rule 8.5 distinguishes two categories of parentheticals: identifier parentheticals and explanatory parentheticals.

Identifier parentheticals contain a number, a letter, an alphanumeric code, or an abbreviation. These count as one word and do not need to obey the sentence-length limits because they are not prose sentences. Examples: `(10)`, `(EACCES)`, `(CI/CD)`, `(v2.1)`. An identifier parenthetical can be a single word or token without a verb.

Explanatory parentheticals contain prose that explains, qualifies, or adds context to the main sentence. These count as one word in the main sentence but form a full separate sentence that must obey the word-count limits. Examples: `(the DEBUG flag is off)`, `(the worker runs every 60 seconds)`, `(this guide has the full procedure)`. An explanatory parenthetical must be a grammatically complete clause with a subject and verb.

The boundary between the two categories can blur. A parenthetical like `(optional)` is usually an identifier (a status label). A parenthetical like `(this parameter is optional)` is an explanatory parenthetical. When in doubt, treat the parenthetical as explanatory and apply the word-count limit. It is better to enforce the limit unnecessarily than to let a long explanatory parenthetical slip through as an identifier.

### Parentheses Versus Em-Dashes

Standard English offers three punctuation marks for asides: parentheses, em-dashes, and commas. Each has a different degree of separation from the main sentence. Commas provide the weakest separation — the aside blends into the flow of the sentence. Em-dashes provide a medium separation — the aside is set off but still feels connected. Parentheses provide the strongest separation — the aside is visually and grammatically cordoned off.

In STE-Code, parentheses are the approved punctuation for asides that need a separate sentence. Em-dashes are permitted for emphasis and for asides that must remain integrated in the main sentence's flow. Commas should not be used for asides longer than a few words — use parentheses or em-dashes instead.

The choice between parentheses and em-dashes depends on whether the aside forms a complete thought. If the aside is a complete clause that could stand as its own sentence, use parentheses (and count the words as a separate sentence). If the aside is a short qualifying phrase that cannot stand alone, use em-dashes (and count the words as part of the main sentence).

> **STE (em-dash):** The server — a Node.js application — listens on port 3000. (10 words, the em-dash aside counts as part of the main sentence)
> **STE (parentheses):** The server listens on port 3000 (the server is a Node.js application). (6 words in the main sentence, 5 words in the parenthetical)

> *In the first version, the aside is a noun phrase and integrates into the main sentence. In the second version, the aside is a complete clause and becomes its own parenthetical sentence.*

### Word Counting Mechanics for Parentheticals

The mechanics of word counting under Rule 8.5:

- **Main sentence:** Count every word outside the parentheses. The parenthetical block — regardless of its internal word count — contributes exactly one word to the main sentence's total. The opening parenthesis and closing parenthesis are not words and do not add to the count.

- **Parenthetical sentence:** Count every word between the opening parenthesis and the closing parenthesis. This forms a separate sentence. Apply the sentence-type limit (20 procedural, 25 descriptive) based on the content of the parenthetical, not the content of the enclosing sentence. A parenthetical inside a procedural sentence can be descriptive if its content describes rather than instructs.

- **Multiple parentheticals in one sentence:** Each parenthetical counts as one word in the main sentence. Each parenthetical forms its own separate sentence. There is no limit on the number of parentheticals in one sentence, but more than two parentheticals in one sentence suggest the sentence is overloaded. Restructure.

- **Parentheticals at the end of a sentence:** When a parenthetical appears at the end of a sentence, the closing parenthesis is followed by the end punctuation. The end punctuation belongs to the main sentence, not the parenthetical. Example: `(...).` — the period ends the main sentence. Do not put a period inside the closing parenthesis before the end punctuation: `(...).` is correct; `(....).` is incorrect.

A tool can verify Rule 8.5 compliance mechanically: (1) find all text between matching parentheses that are not inside backtick-delimited code tokens, (2) count the words in the text outside the parentheses for the main sentence limit, (3) count the words between the parentheses for the separate-sentence limit, (4) flag any sentence that exceeds its type-specific limit.

### Avoid Using Parentheses to Hide Important Information

A common misuse of parentheses: the writer puts a critical precondition, warning, or requirement in parentheses because it does not fit smoothly into the main sentence. The parentheses downgrade the visual priority of the information. A reader scanning the documentation sees the parenthetical as secondary and may skip it.

If the information is important enough to include, it is important enough to be a main sentence. Use parentheses for clarifications, examples, and secondary qualifications. Never use parentheses for safety conditions, required steps, or warnings that the reader must act on.

> **Non-STE:** Call the deallocate function to free the memory (the pointer must not be null and must have been previously allocated by the allocate function — calling deallocate on a null pointer or an unallocated pointer causes undefined behavior).
>
> **STE:** Call the deallocate function to free the memory. The pointer must not be null. The pointer must have been allocated by the allocate function. If you call deallocate on a null pointer or an unallocated pointer, the behavior is undefined.
>
> *Principles applied: Rule 8.5 (no parenthetical used for safety information), P3 (use approved meanings). The original buried undefined behavior warnings in a parenthetical. The fix promotes each precondition to its own sentence.*

### Historical Context and Domain Origins

The ASD-STE100 parentheses rule (Rule 8.5 in the original specification) was designed for technical manuals, where parenthetical text often contains part numbers, tool identifiers, measurement values, and safety condition clarifications. The dual counting system ensures that a reader can read the main procedural sentence (counting the parenthetical as one word) without the parenthetical inflating the sentence length, while the parenthetical's internal text remains constrained to prevent burying critical information.

In a technical manual, a parenthetical like `(set the parameter to 50-55 Nm)` is an explanatory parenthetical that forms a separate procedural sentence. The reader reads the main step, then reads the parenthetical for the specific parameter. The word-count limit on the parenthetical prevents the parameter from being buried in a sea of text.

In code documentation, the same principle applies with different nouns. Instead of measurement values, the parenthetical contains error codes, default values, version numbers, and rationale. The structural need is identical: the main sentence carries the action or description, and the parenthetical carries the qualifying detail. The rule is a reminder that parentheticals are not dumping grounds — they are structured asides with their own sentence discipline.

The original rule also emphasizes that parentheses should not be used to hide information the reader must see. The same applies to code documentation: do not use parentheses to hide deprecation warnings, breaking change notices, or safety-critical conditions. These deserve their own sentences, their own paragraphs, or their own labeled blocks (BREAKING, DEPRECATED, NOTE).
