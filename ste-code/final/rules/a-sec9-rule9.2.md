# Rule 9.2 — Use Each Approved Word Correctly

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec9-rule9.2](ste-code/grouped/), Rule 9.2
> **Domain:** Code documentation (API docs, README files, docstrings, commit messages, error messages, generated code)

## Original Rule

Use each approved word correctly.

Some STE-approved words have meanings that are applicable only in some contexts (restricted meaning). Before you use a word, read its definition in the approved meaning column of the dictionary. Words frequently have many different meanings in standard English. In STE, approved words usually only have one approved meaning. Other meanings that the word can have in standard English are not approved.

Always make sure that the word that you select has the correct meaning in the applicable context.

Also, make sure that you use approved words as their approved part of speech. In English, words usually do not have different forms that immediately show their function in a sentence. Thus, readers can frequently think differently about the same word. To make sentences clearer, an approved word can usually only have one function (part of speech). In STE, use each approved word as the approved part of speech.

There are a small number of words that are approved as more than one part of speech and have more than one meaning. These words are important and frequently occur in technical English.

## STE-Code Adaptation

> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient; Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs

Use each approved word correctly in code documentation.

Some words in the controlled terminology have restricted meanings that apply only in specific contexts. Before you use a word, read its definition in the approved meaning column of the controlled terminology. Words frequently have many different meanings in standard English. In the controlled terminology, approved words usually have only one approved meaning. Other meanings that the word can have in standard English are not approved.

Always make sure that the word that you select has the correct meaning in the applicable code documentation context.

Also, make sure that you use approved words as their approved part of speech. In English, words do not usually have different forms that immediately show their function. Thus, use each approved word as the approved part of speech only.

A small number of words are approved as more than one part of speech and have more than one meaning. These words are important and occur frequently in software development documentation.

### Examples

> *Adapted from spec pair:* Non-STE: "Wear protective clothing."  |  STE: "Use (or put on) protective clothing." — in ASD-STE100 the word "wear" is approved only with the meaning "to become damaged by friction," not "to have on one's body." This restriction carries over: a word may be approved for one meaning only.
> *Adapted from spec pair:* Non-STE: "When the pressure goes down, lift the cover."  |  STE: "When the pressure decreases, lift the cover." — a verb combined with a preposition can imply physical movement; use the single approved verb for the numeric or state change.
> *Adapted from spec pair:* Non-STE: "Flush the pipes with a disinfectant solution." / "Make sure that the surface is flush with the mating surface."  |  STE: same wording — "flush" is approved as both a verb ("to remove remaining data from a buffer") and an adjective ("where one surface fully touches a different surface"). It is the primary example of a word approved as more than one part of speech.

> **Non-STE:** Execute the initialization script before you start the server.
>
> **STE:** Run the initialization script before you start the server.

(The word "execute" is not approved in STE-Code. In standard English it can mean "to carry out a death sentence" or "to run a program," but STE-Code gives only one approved word for "to run a program": "run." Use "run" for this context.)

Realistic code-documentation context — a Python test fixture docstring:

```python
# Non-STE docstring
def start_integration_server():
    """Execute the initialization script before you start the server."""
    subprocess.run(["./init.sh"], check=True)
    subprocess.run(["./server", "--port", "8080"], check=True)


# STE docstring
def start_integration_server():
    """Run the initialization script before you start the server."""
    subprocess.run(["./init.sh"], check=True)
    subprocess.run(["./server", "--port", "8080"], check=True)
```

> **Non-STE:** When the error count goes down, restart the service.
>
> **STE:** When the error count decreases, restart the service.

(The verb "goes" together with the preposition "down" makes a phrase that refers to physical movement. "Decrease" is better because it refers to the error count, a number, not to a physical indicator that monitors the count.)

Realistic code-documentation context — a runbook note in Markdown:

```markdown
## Recovery

Non-STE: When the error count goes down for 5 minutes, restart the service to clear the circuit breaker.

STE: When the error count decreases for 5 minutes, restart the service to clear the circuit breaker.
```

> **Non-STE:** Log the exception details to the output stream.
>
> **STE:** Write the exception details to the log.

(The word "log" is approved as a noun, but not as a verb. Use the approved noun "log" with the approved verb "write.")

Realistic code-documentation context — a Python exception handler docstring:

```python
# Non-STE
def handle_error(exc: Exception) -> None:
    """Log the exception details to the output stream."""
    logger.error("error: %s", exc)


# STE
def handle_error(exc: Exception) -> None:
    """Write the exception details to the log."""
    logger.error("error: %s", exc)
```

> **Non-STE:** The config help shows all available command-line options.
>
> **STE:** The configuration help text shows all available command-line options.

(The word "help" is approved as a verb, but not as a noun. Use the approved noun phrase "help text" or "help information.")

Realistic code-documentation context — a README section that describes the `--help` flag:

```markdown
## Get help

Non-STE: The config help shows all available command-line options.

STE: The configuration help text shows all available command-line options,
including `--port` and `--verbose`.
```

> **Non-STE:** The recursive call damaged the call stack.
>
> **STE:** The recursive call caused damage to the call stack.

(The word "damage" is approved as a noun, but not as a verb. Use "cause damage" or "do damage" instead of the verb form.)

Realistic code-documentation context — an inline comment in a C crash report:

```c
/* Non-STE: The recursive call damaged the call stack and corrupted the return addresses. */

/* STE: The recursive call caused damage to the call stack and corrupted the return addresses. */
```

> **STE:** Flush the output buffer before you close the file handle.

("Flush" is a verb here with the approved meaning "to remove remaining data from a buffer.")

Realistic code-documentation context — a file writer docstring:

```python
def close_writer(self) -> None:
    """Flush the output buffer before you close the file handle."""
    self.buffer.flush()
    self.handle.close()
```

> **STE:** Make sure that the connector is flush with the port.

("Flush" is an adjective here with the approved meaning "where one surface fully touches a different surface." The word "flush" is approved as both a verb and an adjective because the different positions and contexts make it easy to see their function.)

Realistic code-documentation context — a hardware setup doc:

```markdown
## Install the cable

Push the connector in until it stops. Make sure that the connector is flush
with the port before you tighten the screw.
```

## Code-Domain Explanation

Rule 9.2 is the quality-control rule of the STE-Code system. It makes sure that every approved word in your documentation is used with its correct meaning and its correct part of speech. This is more difficult in code documentation than in general technical English because code documentation mixes natural language with code symbols, and many words have specialized meanings in software engineering that they do not have in other technical fields.

In the original ASD-STE100, most approved words have exactly one approved meaning and one approved part of speech. This is intentional. When a word can mean only one thing, the reader never needs to guess which meaning you intend. The same principle applies to code documentation: each approved word in your prose must have one clear meaning. When a word could mean two different things in a software context, you must choose a different word or add context that removes the ambiguity.

### README Files

README files introduce a project to new developers. They must be clear on first reading. Rule 9.2 applies to README files in these ways:

- Every verb in a README must be an approved verb used in its approved meaning. Do not use "leverage" when you mean "use." Do not use "facilitate" when you mean "help" or "let you."

  ```markdown
  Non-STE: You can leverage the cache layer to facilitate faster lookups.
  STE:     You can use the cache layer to help you do faster lookups.
  ```

- Every noun that describes a concept must be an approved noun. Do not use "functionality" when you mean "feature." Do not use "capability" when you mean "can."

  ```markdown
  Non-STE: This release adds logging functionality for the export capability.
  STE:     This release adds a logging feature. You can now export logs.
  ```

- The word "build" is approved as both a noun and a verb. In a README, "build the project" (verb, imperative) and "the build output" (noun, the result) are both correct. But "the build" used to mean "the build process" is less clear. Prefer "the build process" or "when you build the project."

  ```markdown
  Non-STE: Run the tests after the build.
  STE:     Run the tests after you build the project.   # or: ... after the build process.
  ```

- The word "run" is approved as a verb. Do not use it as a noun ("do a run of the tests" must be "run the tests"). The exception is when "run" is part of a technical noun phrase like "test run" or "dry run," which are technical nouns (Rule 1.5).

  ```markdown
  Non-STE: Do a run of the test suite before you merge.
  STE:     Run the test suite before you merge.   # or: Do a test run before you merge.
  ```

### API Documentation

API documentation must be precise because developers use it as a reference while writing code. Rule 9.2 applies strictly:

- The word "get" is approved as a verb meaning "to obtain." In HTTP API documentation, "GET" (uppercase, the HTTP method) is a technical noun (Rule 1.5). Do not confuse the two. Write: "Send a GET request to this endpoint to get the user data."

  ```http
  # Non-STE: Make a GET to /users to retrieve the user data.
  # STE:     Send a GET request to /users to get the user data.
  GET /users HTTP/1.1
  Host: api.example.com
  ```

- The word "set" is approved as a verb meaning "to put into a specified state" and as a noun meaning "a group of related items." In API documentation, use "set the timeout value" (verb) and "a set of endpoints" (noun). Do not use "set" to mean "configured" as an adjective ("the set timeout value" is ambiguous; use "the timeout value that you set").

  ```markdown
  Non-STE: The set timeout value applies to all requests.
  STE:     The timeout value that you set applies to all requests.
  ```

- The word "check" is approved as a verb meaning "to make sure that something is correct." Do not use it as a noun ("do a check" must be "check"). The exception is when "check" is part of a technical noun like "type check" or "health check" (Rule 1.5).

  ```markdown
  Non-STE: Do a check before you deploy.
  STE:     Check before you deploy.   # or: Do a health check before you deploy.
  ```

- The word "return" is approved as a verb meaning "to go back" or "to give back." In API documentation, "the function returns a value" is correct. "The return value" is also correct because "return" modifies "value" (it is a noun adjunct, not a standalone noun). But "the return of the function" is not approved because "return" is used as a standalone noun.

  ```typescript
  // Non-STE: The return of the function is a User object.
  // STE:     The function returns a User object.   # or: The return value is a User object.
  function getUser(id: string): User { /* ... */ }
  ```

### Docstrings and Inline Comments

Docstrings and inline comments are short and appear next to the code they describe. Rule 9.2 applies with these considerations:

- The word "do" is approved as a verb meaning "to perform an action." In docstrings, use "do" as a main verb only when the action is general: "Do the setup before you call this function." For specific actions, use the specific verb: "Run the database migration before you call this function."

  ```python
  # Non-STE: Do a database migration before you call this function.
  # STE:     Run the database migration before you call this function.
  ```

- The word "make" is approved as a verb meaning "to create." Do not use it as a light verb in phrases like "make a call" (use "call") or "make an update" (use "update"). The exception is when the object of "make" is a thing that you create: "make a copy of the file" is correct because the copy is a new thing. "Make a request" is less good; prefer "send a request."

  ```python
  # Non-STE: Make a call to the upstream service.
  # STE:     Call the upstream service.

  # Non-STE: Make a request to the API.
  # STE:     Send a request to the API.

  # STE (acceptable): Make a copy of the config file before you change it.
  ```

- The word "use" is approved as a verb. Do not confuse it with "using" as a preposition meaning "by means of." In C# and some other languages, `using` is a keyword for resource management. In docstrings, the keyword `using` in code font is a technical noun (Rule 1.5). In prose, "use" is the approved verb. Do not write "Using this method, you can..." Write "Use this method to..." or "You can use this method to..."

  ```csharp
  /// Non-STE: Using this method, you can open the file and read it.
  /// STE:     Use this method to open the file and read it.
  public void OpenAndRead(string path) { /* ... */ }
  ```

### Commit Messages

Commit messages have a strict format. Rule 9.2 applies to the summary line and the body:

- The summary line must use the imperative mood with an approved verb: "Add feature," "Remove deprecated method," "Set default timeout." Do not use unapproved verbs in the summary: "Implement feature" must be "Add feature" (unless "implement" is a technical verb for your project, Rule 1.12). "Introduce breaking change" must be "Add breaking change" or restructured.

  ```text
  Non-STE: Implement retry logic for the uploader
  STE:     Add retry logic to the uploader

  Non-STE: Introduce breaking change to the config schema
  STE:     Add breaking change to the config schema
  ```

- The word "fix" is approved as a verb. "Fix the memory leak" is correct. But "fix" as a noun ("a fix for the bug") is not approved. Use "correction" or restructure: "correct the bug."

  ```text
  Non-STE: Add a fix for the null-pointer bug
  STE:     Correct the null-pointer bug

  STE (acceptable): Fix the null-pointer bug
  ```

- The word "update" is approved as a verb meaning "to make something more current." Do not use it as a noun ("an update to the config" must be "an update of the config" or restructure to "update the config").

  ```text
  Non-STE: Ship an update to the config
  STE:     Update the config
  ```

### Error Messages

Error messages must tell the user what is wrong and what to do. Rule 9.2 applies with special strictness because error messages are read under stress:

- Use "cannot" (the approved negative form of "can"). Do not use "unable to" or "failed to" when "cannot" is sufficient. Write "Cannot open the config file" instead of "Failed to open the config file" or "Unable to open the config file."

  ```text
  Non-STE: Failed to open the config file
  STE:     Cannot open the config file

  Non-STE: Unable to connect to the database
  STE:     Cannot connect to the database
  ```

- The word "must" is approved to express a requirement. In error messages, use "must" only when the user must do something to continue: "You must set the API key before you can use this feature." Do not use "must" to describe a system state: "The file must exist" is less clear than "The file does not exist."

  ```text
  Non-STE: The config file must exist.
  STE:     The config file does not exist.

  STE (acceptable): You must set the API key before you can use this feature.
  ```

- The word "if" is approved as a conjunction for conditions. In error messages, use "if" to give the user a conditional action: "If the problem continues, look at the log for more data."

  ```text
  STE: If the problem continues, look at the log for more data.
  ```

### Generated Code and Automated Output

When you document generated code, the generated symbols (function names, variable names, class names) are technical nouns (Rule 1.5) and are not subject to Rule 9.2. However, your prose that describes the generated code must follow Rule 9.2. If a generated symbol uses a word that is unapproved in its meaning or part of speech, keep the symbol unchanged but describe its function with approved words.

```python
# Generated by an OpenAPI client generator (kept unchanged):
def utilize_config(self) -> None:
    """Configure the client from the loaded spec."""
    self._apply_settings()

# Your documentation of the generated symbol:
# The `utilize_config()` function uses the configuration to set
# the application state. (The word "utilize" appears only inside the
# symbol name in code font; your prose uses the approved verb "uses".)
```

## Paradigm-Specific Guidance

### Object-Oriented Documentation (Java, C++, C#, Python Classes)

Object-oriented documentation uses class hierarchies, interfaces, and design patterns as its organizing structure. Rule 9.2 applies to these patterns as follows:

- The word "extend" is a keyword in Java, C++, and many other languages. In code font, `extend` is a technical noun (Rule 1.5). In prose, "extend" is an unapproved verb. Do not write "This class extends the base class." Write "This class is a child of the base class" or "This class inherits from the base class" (where "inherits" is a technical verb, Rule 1.12). If the sentence refers to the keyword, use code font: "Put `extends BaseClass` in the class declaration."

  ```java
  // Non-STE docstring: This class extends the base class to add retry logic.
  // STE docstring:     This class is a child of the base class. It adds retry logic.
  public class RetryClient extends BaseClient { /* ... */ }
  ```

- The word "implement" is a keyword in Java and C#. In code font, `implements` is a technical noun. In prose, "implement" is an unapproved verb in the context of interfaces. Write "This class uses the `Serializable` interface" instead of "This class implements `Serializable`." When you describe the act of writing code for a method, use "write" or "add": "Write the `save` method" instead of "Implement the `save` method."

  ```java
  // Non-STE docstring: This class implements the `Serializable` interface.
  // STE docstring:     This class uses the `Serializable` interface.
  public class User implements Serializable { /* ... */ }
  ```

- The word "override" is a keyword in Java, C#, and C++. In code font, `@Override` or `override` is a technical noun. In prose, do not use "override" as a verb. Write "This method replaces the parent method" instead of "This method overrides the parent method." When you refer to the keyword, use code font: "Put `@Override` before the method."

  ```java
  // Non-STE docstring: This method overrides the parent method.
  // STE docstring:     This method replaces the parent method.
  @Override
  public String toString() { /* ... */ }
  ```

- The word "abstract" is a keyword in Java and C#. In code font, `abstract` is a technical noun. In prose, "abstract" as an adjective is not approved (it does not appear in the STE-Code dictionary with this meaning). Write "This class is a base class. You cannot make an instance of it" instead of "This is an abstract class." When you refer to the keyword, use code font.

  ```java
  // Non-STE docstring: This is an abstract class for all handlers.
  // STE docstring:     This is a base class for all handlers. You cannot make an instance of it.
  public abstract class Handler { /* ... */ }
  ```

> **Non-STE:** The `PaymentProcessor` abstract class implements the `TransactionHandler` interface and provides a default implementation for the `validate` method, which subclasses can override.
>
> **STE:** The `PaymentProcessor` base class uses the `TransactionHandler` interface. It gives a default `validate` method. Child classes can replace this method.

*Principles applied: P1, P2, P5, P7. "Abstract" in prose is not approved; "base class" is clearer. "Implements" as a verb is replaced with "uses." "Provides a default implementation" is restructured to "gives a default method." "Override" is replaced with "replace." The long sentence is split into three shorter sentences.*

Realistic code-documentation context — a Java class header comment:

```java
/**
 * Non-STE: The PaymentProcessor abstract class implements the
 * TransactionHandler interface and provides a default implementation for
 * the validate method, which subclasses can override.
 *
 * STE: The PaymentProcessor base class uses the TransactionHandler
 * interface. It gives a default validate method. Child classes can
 * replace this method.
 */
public abstract class PaymentProcessor implements TransactionHandler {
    public void validate(Transaction t) { /* default behaviour */ }
}
```

### Functional Documentation (Haskell, Elixir, Clojure, Rust)

Functional documentation describes pure functions, type transformations, and immutable data. Rule 9.2 applies to the unique vocabulary of functional programming:

- The word "map" is approved as a noun meaning "a visual representation of an area." In functional programming, `map` is a function name (technical noun, Rule 1.5) and a general operation. In prose, do not use "map" as a verb meaning "to apply a function to each element." Write "apply the function to each element of the list" instead of "map the function over the list." When you refer to the `map` function itself, use code font: "Use `map` to apply a function to each element."

  ```haskell
  -- Non-STE docstring: Maps the parser function over the input list.
  -- STE docstring:     Applies the parser function to each element of the input list.
  parseAll :: [String] -> [Value]
  parseAll = map parse
  ```

- The word "reduce" is not approved as a verb in STE-Code. In functional programming, `reduce` (or `fold`) is a function name (technical noun, Rule 1.5). In prose, write "combine the elements of the list into a single value" instead of "reduce the list." When you refer to the function, use code font: "Use `reduce` to combine all elements."

  ```clojure
  ;; Non-STE docstring: Reduces the list to a single sum.
  ;; STE docstring:     Combines the elements of the list into a single sum.
  (defn total [xs] (reduce + 0 xs))
  ```

- The word "filter" is approved as a noun meaning "a device that removes unwanted parts." In functional programming, `filter` is a function name (technical noun, Rule 1.5). In prose, do not use "filter" as a verb. Write "remove elements that do not match the condition" instead of "filter the list." When you refer to the function, use code font: "Use `filter` to remove unwanted elements."

  ```elixir
  # Non-STE docstring: Filters the list to keep only active users.
  # STE docstring:     Removes elements that do not match the condition (keep only active users).
  def active_users(users), do: Enum.filter(users, & &1.active)
  ```

- The word "apply" is not approved in STE-Code (use "use" or "put on"). In functional programming, `apply` (or `ap`) is a function name associated with applicative functors. Keep the function name in code font as a technical noun. In prose, write "use the function on the value" instead of "apply the function to the value."

  ```haskell
  -- Non-STE docstring: Applies the function to the value inside the functor.
  -- STE docstring:     Uses the function on the value inside the functor.
  runReader :: Reader r a -> r -> a
  ```

> **Non-STE:** The `sequence` function maps an `Effect`-producing function over a list of elements, then collects all the effects into a single `Effect` that produces a list.
>
> **STE:** The `sequence` function applies an `Effect`-producing function to each element of a list. Then it collects all the effects into one `Effect` that gives a list.

*Principles applied: P1, P2, P5. "Maps" as a verb is replaced with "applies to each element." "Collects" is an unapproved verb; kept here because it is the name of the operation in the type signature context — but in a stricter application, "puts together" would be used. The sentence is split.*

Realistic code-documentation context — a Haskell module comment:

```haskell
-- Non-STE: The sequence function maps an Effect-producing function over a
-- list of elements, then collects all the effects into a single Effect
-- that produces a list.
--
-- STE: The sequence function applies an Effect-producing function to each
-- element of a list. Then it collects all the effects into one Effect that
-- gives a list.
sequence :: [Effect a] -> Effect [a]
```

### Procedural Documentation (C, Go, Bash)

Procedural documentation describes step-by-step operations, memory management, and system interaction. Rule 9.2 applies to these patterns:

- The word "free" is approved as a verb meaning "to release" and as an adjective meaning "not restricted." In C documentation, `free()` is a function name (technical noun, Rule 1.5). In prose, use "free" as a verb: "free the memory" is correct. "The memory is free" (adjective) is also correct. Do not confuse the two: "free the pointer" is ambiguous; write "free the memory that the pointer points to."

  ```c
  /* Non-STE: Free the pointer when you finish. */
  /* STE:     Free the memory that the pointer points to when you finish. */
  free(ptr);
  ```

- The word "open" is approved as a verb meaning "to make accessible." In C and Go, `open()` is a function name. In prose, "open the file" is correct. Do not use "open" as an adjective in the sense of "available": "the port is open" could mean "the port is not closed" (physical) or "the port is available for connections." Prefer "the port is available" for the second meaning.

  ```go
  // Non-STE: Open the file, then read the port. The port is open for connections.
  // STE:     Open the file, then read the port. The port is available for connections.
  f, _ := os.Open("data.txt")
  ```

- The word "close" is approved as a verb and as an adjective meaning "near." In C and Go, `close()` is a function name. In prose, "close the file" (verb) is correct. Do not use "close" as an adjective meaning "near" in a technical context where it could be confused with the verb: "close the connection" is clear; "the close port" is ambiguous. Use "the nearest port" for proximity.

  ```c
  /* Non-STE: Close the file and use the close port for the next socket. */
  /* STE:     Close the file and use the nearest port for the next socket. */
  fclose(fp);
  ```

- The word "read" is approved as a verb. In C and Go, `read()` is a function name. In prose, "read the data from the buffer" is correct. Do not use "read" as a noun: "the read operation" is acceptable as a noun adjunct, but "do a read" must be "read the data."

  ```go
  // Non-STE: Do a read from the buffer to get the header.
  // STE:     Read the data from the buffer to get the header.
  n, _ := buf.Read(header)
  ```

> **Non-STE:** After you allocate memory on the heap with `malloc`, you must deallocate it with `free` when the program no longer needs it. Failing to free allocated memory causes memory leaks.
>
> **STE:** After you get memory from the heap with `malloc`, you must free the memory with `free` when the program does not need it. If you do not free the memory, the program uses more memory over time.

*Principles applied: P1, P2, P11. "Allocate" is replaced with "get" (the memory comes from the heap). "Deallocate" is not approved; "free" is the approved verb. "Failing to" becomes "If you do not." "Memory leaks" is jargon (P10); restructured to "uses more memory over time."*

Realistic code-documentation context — a C function comment:

```c
/* Non-STE: After you allocate memory on the heap with malloc, you must
 * deallocate it with free when the program no longer needs it. Failing to
 * free allocated memory causes memory leaks.
 *
 * STE: After you get memory from the heap with malloc, you must free the
 * memory with free when the program does not need it. If you do not free the
 * memory, the program uses more memory over time.
 */
void process(void) {
    char *buf = malloc(1024);
    /* ... use buf ... */
    free(buf);
}
```

### Declarative Documentation (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes desired state, not procedures. Rule 9.2 applies to the stative vocabulary of declarative systems:

- The word "create" is not approved in STE-Code (use "make"). In SQL, `CREATE` is a keyword (technical noun, Rule 1.5). In prose, do not use "create" as a verb. Write "make a table" instead of "create a table." When you refer to the SQL keyword, use code font: "Use `CREATE TABLE` to make a new table."

  ```sql
  -- Non-STE prose: Create a table for the users.
  -- STE prose:     Make a table for the users.
  -- keyword in code font:
  CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
  ```

- The word "select" is not approved in STE-Code (use "choose" or "get" depending on context). In SQL, `SELECT` is a keyword (technical noun, Rule 1.5). In prose, write "get rows from the table" instead of "select rows from the table." When you refer to the SQL keyword, use code font: "The `SELECT` statement gets data from a table."

  ```sql
  -- Non-STE prose: Select rows from the table where active is true.
  -- STE prose:     Get rows from the table where active is true.
  SELECT * FROM users WHERE active = TRUE;
  ```

- The word "drop" is approved as a verb meaning "to let fall." In SQL, `DROP` is a keyword (technical noun, Rule 1.5). In prose, write "remove the table" instead of "drop the table" unless you are directly quoting the SQL statement. When you refer to the SQL keyword, use code font.

  ```sql
  -- Non-STE prose: Drop the table if it exists.
  -- STE prose:     Remove the table if it exists.
  DROP TABLE IF EXISTS users;
  ```

- The word "apply" is not approved. In Terraform, `terraform apply` is a command (technical noun, Rule 1.5). In prose, write "use `terraform apply` to make the changes" instead of "apply the configuration."

  ```hcl
  # Non-STE prose: Apply the configuration to make the bucket.
  # STE prose:     Use `terraform apply` to make the bucket.
  resource "aws_s3_bucket" "logs" { bucket = "app-logs" }
  ```

> **Non-STE:** The `Deployment` resource creates and manages a set of replicated Pods. It ensures that the specified number of Pods are running at all times.
>
> **STE:** The `Deployment` resource makes and controls a set of Pod copies. It makes sure that the set number of Pods runs at all times.

*Principles applied: P1, P2, P11. "Creates" replaced with "makes." "Manages" is unapproved; replaced with "controls." "Replicated" is unapproved; replaced with "copies." "Ensures" is unapproved; replaced with "makes sure." "Specified" is unapproved; replaced with "set." "Running" (adjective) is restructured to "runs" (verb).*

Realistic code-documentation context — a Kubernetes manifest comment:

```yaml
# Non-STE: The Deployment resource creates and manages a set of replicated
# Pods. It ensures that the specified number of Pods are running at all times.
#
# STE: The Deployment resource makes and controls a set of Pod copies.
# It makes sure that the set number of Pods runs at all times.
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
spec:
  replicas: 3
```

### Systems Documentation (Rust Ownership, C Memory)

Systems documentation has the strictest requirements for word precision because it describes memory safety, ownership, and lifetimes. Rule 9.2 applies with special attention to words that have both a standard English meaning and a systems-programming meaning:

- The word "move" is approved as a verb meaning "to change position." In Rust, `move` is a keyword for ownership transfer (technical noun, Rule 1.5). In prose, when you describe Rust ownership, "move" as a verb is acceptable as a technical verb (Rule 1.12) because it names a specific Rust operation. But make sure the context makes the Rust meaning clear: "When you move a value, the first variable can no longer use it."

  ```rust
  // Non-STE docstring: Transfers ownership of the buffer to the worker.
  // STE docstring:     Moves the buffer to the worker. The first variable
  //                   can no longer use the buffer.
  let buf = String::from("data");
  let worker = buf; // move
  ```

- The word "borrow" is not approved as a verb in STE-Code. In Rust, `borrow` (via `&`) is an ownership concept. In prose, do not use "borrow" as a verb. Write "get a reference to the value" instead of "borrow the value." The Rust concept of borrowing is a technical noun: "the borrow checker" is correct because "borrow" modifies "checker."

  ```rust
  // Non-STE docstring: Borrow the value to read it without a copy.
  // STE docstring:     Get a reference to the value to read it without a copy.
  let r: &String = &buf;
  ```

- The word "drop" is approved as a verb meaning "to let fall." In Rust, `drop` is a trait and a function (technical noun, Rule 1.5). In prose, when describing the Rust concept, use "drop" as a technical verb (Rule 1.12): "The value drops when it goes out of scope." This is acceptable because "drop" in Rust has a specific, well-defined meaning.

  ```rust
  // STE docstring: The value drops when it goes out of scope.
  fn scoped() {
      let v = String::from("x");
  } // v drops here
  ```

- The word "own" is not approved as a verb in STE-Code. In Rust, ownership is a core concept. In prose, do not use "own" as a verb. Write "the variable has the value" or "the value is in the variable" instead of "the variable owns the value." The noun "ownership" is a technical noun (Rule 1.5): "Rust's ownership system" is correct.

  ```rust
  // Non-STE docstring: The variable owns the value and frees it on drop.
  // STE docstring:     The variable has the value and frees it on drop.
  let s = String::from("hi");
  ```

> **Non-STE:** When a variable goes out of scope, Rust automatically drops the value, freeing the memory it owned. You do not need to manually deallocate memory.
>
> **STE:** When a variable goes out of scope, Rust automatically drops the value and frees the memory. You do not need to free memory manually.

*Principles applied: P1, P2, P5. "Owned" as a verb is replaced with restructured sentence. "Automatically" is an approved adverb. "Manually" is an approved adverb. "Deallocate" is not approved; "free" is used instead. The sentence is split and simplified.*

Realistic code-documentation context — a Rust function comment:

```rust
/// Non-STE: When a variable goes out of scope, Rust automatically drops the
/// value, freeing the memory it owned. You do not need to manually deallocate
/// memory.
///
/// STE: When a variable goes out of scope, Rust automatically drops the value
/// and frees the memory. You do not need to free memory manually.
fn run() {
    let data = load();
} // data drops and the memory is free
```

## Extended Examples

> **Non-STE:** The initialization function bootstraps the dependency injection container and registers all service implementations.
>
> **STE:** The initialization function starts the dependency injection container and adds all service implementations.

*Principles applied: P1, P11. "Bootstraps" is not approved; replaced with "starts" from the Synonym Table. "Registers" is not approved as a verb in this sense; "adds" is clearer. "Container" and "dependency injection" are technical nouns (Rule 1.5) and kept unchanged.*

Realistic code-documentation context — a Go startup function comment:

```go
// Non-STE: The initialization function bootstraps the dependency injection
// container and registers all service implementations.
//
// STE: The initialization function starts the dependency injection container
// and adds all service implementations.
func Initialize(services *Container) {
    services.Add(NewAuth())
    services.Add(NewBilling())
}
```

> **Non-STE:** If the validation check fails, the form will display an error message beneath the input field.
>
> **STE:** If the validation check does not pass, the form shows an error message below the input field.

*Principles applied: P1, P2. "Fails" as a verb is approved only in the sense of "to become weaker" or "to not do something." Here, "does not pass" is clearer. "Display" is in the Synonym Table (prefer "show"). "Beneath" is not approved; "below" is the approved alternative.*

Realistic code-documentation context — a JavaScript form handler docstring:

```javascript
/**
 * Non-STE: If the validation check fails, the form will display an error
 * message beneath the input field.
 *
 * STE: If the validation check does not pass, the form shows an error
 * message below the input field.
 */
function onSubmit(values) {
  if (!validate(values)) showError("Invalid input");
}
```

> **Non-STE:** The caching layer intercepts database queries and serves cached results when possible, dramatically reducing latency.
>
> **STE:** The caching layer gets database queries. When possible, it gives cached results. This decreases latency.

*Principles applied: P1, P2, P10. "Intercepts" is not approved; "gets" is the approved alternative. "Serves" as a verb meaning "to provide" is not approved; "gives" is the approved alternative. "Dramatically" is a marketing word (P10); removed. The long sentence is split into three sentences.*

Realistic code-documentation context — a Python cache docstring:

```python
class Cache:
    """Non-STE: The caching layer intercepts database queries and serves
    cached results when possible, dramatically reducing latency.

    STE: The caching layer gets database queries. When possible, it gives
    cached results. This decreases latency."""

    def get(self, key):
        return self._store.get(key)
```

> **Non-STE:** You can leverage the `--parallel` flag to execute multiple test suites concurrently, which significantly accelerates the overall test duration.
>
> **STE:** You can use the `--parallel` flag to run multiple test suites at the same time. This decreases the total test duration.

*Principles applied: P1, P11. "Leverage" is in the Synonym Table (prefer "use"). "Execute" is not approved; replaced with "run." "Concurrently" is not in the controlled terminology; "at the same time" is clearer. "Significantly" and "accelerates" are marketing words; "decreases" is the approved verb. "Overall" is replaced with "total." The sentence is split.*

Realistic code-documentation context — a pytest configuration note:

```ini
# Non-STE: You can leverage the --parallel flag to execute multiple test
# suites concurrently, which significantly accelerates the overall test duration.
#
# STE: You can use the --parallel flag to run multiple test suites at the
# same time. This decreases the total test duration.
[pytest]
addopts = --parallel
```

> **Non-STE:** Upon completion of the build pipeline, the artifacts are persisted to the configured storage backend.
>
> **STE:** When the build pipeline is complete, the system keeps the artifacts in the configured storage.

*Principles applied: P1, P2, P7, P11. "Upon" is not approved as a preposition; "When" is the approved alternative. "Completion" is not approved as a noun (the verb "complete" is approved). "Persisted" as a verb is not approved; "keeps" is the approved alternative. "Backend" is jargon (P10); removed because "storage" communicates the meaning. "Are persisted" (passive) becomes active "the system keeps."*

Realistic code-documentation context — a CI workflow comment:

```yaml
# Non-STE: Upon completion of the build pipeline, the artifacts are
# persisted to the configured storage backend.
#
# STE: When the build pipeline is complete, the system keeps the artifacts
# in the configured storage.
jobs:
  build:
    steps:
      - run: make build
      - run: cp dist/* storage/
```

> **Non-STE:** This configuration option dictates the verbosity level of the logging output, ranging from "error" to "trace."
>
> **STE:** This configuration option sets the log detail level. You can set it from "error" to "trace."

*Principles applied: P1, P2, P11. "Dictates" is not approved; "sets" is the approved alternative. "Verbosity" is not approved; "detail" is the approved alternative. "Ranging from" is replaced with "You can set it from." The sentence is split for clarity.*

Realistic code-documentation context — a config schema comment:

```json
{
  "// Non-STE": "This configuration option dictates the verbosity level of the logging output, ranging from 'error' to 'trace'.",
  "// STE": "This configuration option sets the log detail level. You can set it from 'error' to 'trace'.",
  "log_level": "info"
}
```

## Edge Cases

### Words Approved as Multiple Parts of Speech

A small number of words in the STE-Code dictionary are approved as more than one part of speech, each with a different approved meaning. These words need special attention because the same spelling appears in different grammatical roles. The original ASD-STE100 gives "flush" as the primary example: approved as a verb ("to remove remaining data from a buffer") and as an adjective ("where one surface fully touches a different surface"). In code documentation, the following words are approved as more than one part of speech:

- **"build"** — Verb: "to construct software from source code" (technical verb, Rule 1.12). Noun: "the result of a build process" or "a specific version." In a sentence, the position of "build" tells the reader its function: "Build the project" (verb, imperative) vs. "The build completed successfully" (noun, subject). When "build" is used as a noun, make sure the context makes its meaning clear. Do not write "the build" when you mean "the build output" or "the build process." Be specific.

  ```text
  Verb:    Build the project before you run the tests.
  Noun:    The build completed successfully and the artifact is in dist/.
  Avoid:   The build failed.                 # does it mean the process or the artifact?
  Prefer:  The build process failed.          # or: The build output is missing.
  ```

- **"run"** — Verb: "to start and operate software." Noun: approved only in the compound noun "test run" or "dry run" (technical noun, Rule 1.5). Do not use "run" as a standalone noun: "the run failed" must be "the test run failed" or "the program did not run correctly."

  ```text
  Verb:    Run the migration before you deploy.
  Noun:    Do a test run before you deploy.
  Avoid:   The run failed.
  Prefer:  The test run failed.               # or: The program did not run correctly.
  ```

- **"set"** — Verb: "to put into a specified state." Noun: "a group of related items." In documentation, "set the timeout" (verb) and "a set of configuration options" (noun) are both correct. The context must make the function clear. When ambiguity is possible, add a determiner or a modifier: "the set of options" (noun) vs. "you can set the options" (verb).

  ```text
  Verb:    Set the timeout to 30 seconds.
  Noun:    A set of configuration options is available.
  Ambiguous: The set timeout applies.          # "set" looks like an adjective here.
  Prefer:    The timeout value that you set applies.
  ```

- **"check"** — Verb: "to make sure that something is correct." Noun: approved only in compound technical nouns like "type check," "health check," or "lint check." Do not use "check" as a standalone noun: "do a check" must be "check" (verb) or "do a type check" (compound technical noun).

  ```text
  Verb:    Check the input before you save it.
  Noun:    Do a health check before you deploy.
  Avoid:   Do a check before you deploy.
  Prefer:  Check before you deploy.            # or: Do a health check before you deploy.
  ```

### When a Framework or Tool Name Is Also an Unapproved Word

Some framework and tool names are ordinary English words that are not approved in STE-Code. For example, "Express" (the Node.js web framework), "Flask" (the Python web framework), "Fresh" (the Deno web framework), and "FastAPI" (contains "fast," which appears in the Synonym Table only with the note that it is approved as an adjective). These names are technical nouns (Rule 1.5) and must stay unchanged in your documentation. The rule is:

1. Always put the framework name in code font or with its official capitalization so the reader knows it is a proper noun.
2. Never use the framework name as a verb (Rule 1.7). Do not write "Express your API" or "Flask your application."
3. When the framework name appears next to prose that uses the same word with a different meaning, the code font and prose font make the distinction clear: "Use `Express` to express your API routes" would be unacceptable because "express" appears both as a name and as a verb meaning "to state." Restructure: "Use the `Express` framework to write your API routes."

Realistic code-documentation context — a README for a Node.js service:

```markdown
## Routes

Non-STE: Express your API routes with the Express router.
STE:     Use the `Express` framework to write your API routes.
```

### When a Code Keyword Conflicts With an Approved Word

Some programming language keywords are spelled the same as approved STE-Code words but have a different meaning. For example:

- Rust `use` — keyword for importing names. STE-Code "use" — verb meaning "to put into service." When you document Rust code, use code font for the keyword: "Put `use std::io` at the top of the file. Then you can use the `io` module." The code font tells the reader that the first "use" is a keyword and the second "use" is prose.

  ```rust
  // Put `use std::io` at the top of the file.
  // Then you can use the `io` module to read from the console.
  use std::io;
  fn main() {
      let mut input = String::new();
      io::stdin().read_line(&mut input).unwrap();
  }
  ```

- Rust `move` — keyword for ownership transfer. STE-Code "move" — verb meaning "to change position" or technical verb for the Rust operation. When you describe Rust ownership, "move" as a technical verb (Rule 1.12) is acceptable: "When you move a value, the first variable can no longer use it." But when you describe non-Rust movement, "move" has its standard STE-Code meaning.

  ```rust
  // When you move a value, the first variable can no longer use it.
  let a = String::from("x");
  let b = a; // move
  // a can no longer use the value.
  ```

- `return` — keyword in most languages. STE-Code "return" — verb meaning "to go back" or "to give back." In documentation, "return" in prose is correct: "The function returns a string." When you refer to the keyword, use code font: "Put `return` at the end of the function."

  ```python
  # The function returns a string.
  # Put `return` at the end of the function to give back the result.
  def name() -> str:
      return "app"
  ```

- `break` — keyword for loop exit. STE-Code "break" — verb meaning "to separate into pieces." In documentation, use "break" in prose only when you mean physical separation: "Do not break the API contract" is ambiguous. Write "Do not change the API contract" unless you mean "Do not separate the API contract into parts."

  ```text
  Non-STE: Do not break the API contract.
  STE:     Do not change the API contract.
  ```

### When the Rule Should Allow Flexibility for Generated Code

Generated code (code produced by a compiler, a code generator, or an AI tool) frequently uses symbol names that contain unapproved words or use words in unapproved parts of speech. Your documentation of generated code must handle this:

1. The generated symbols themselves are technical nouns (Rule 1.5). Keep them unchanged.
2. When you describe what a generated symbol does, you can use approved words that do not match the symbol name. For example, if a generator produces `utilizeConfig()`, your description says: "The `utilizeConfig()` function uses the configuration to set the application state." The word "utilize" appears only in code font as part of the symbol name.
3. If the generated code is part of a public API that developers will call directly, consider adding a wrapper with an approved name. Document the wrapper using approved words and note that it calls the generated function.
4. If you are the author of the code generator, apply STE-Code rules to the generator's output templates so that generated symbol names use approved words from the start.

Realistic code-documentation context — an OpenAPI-generated client and an approved wrapper:

```python
# Generated (kept unchanged):
def utilizeConfig(self) -> None:
    """Generated client method."""
    ...

# Approved wrapper (document with approved words):
def use_config(self) -> None:
    """Use the configuration to set the application state.
    This function calls the generated `utilizeConfig()` function."""
    self.utilizeConfig()
```

### Quoted Error Messages and Log Output

When you quote an error message or log output from a system that does not follow STE-Code, the quoted text is data, not documentation. Keep it exactly as it appears. Your surrounding prose must follow Rule 9.2:

- Put the quoted text in quotation marks or a code block.
- Use approved words to explain what the quoted text means.
- If the quoted text uses a word in an unapproved meaning, explain the meaning with approved words.
- Do not edit the quoted text to make it follow STE-Code. The quote must be accurate.

Realistic code-documentation context — a troubleshooting section:

```markdown
## Troubleshooting

The database log shows: "FATAL: could not allocate memory for shared buffer."
This error means that the database cannot get memory for the shared buffer.
Increase the memory limit or restart the service.
```

## Grammar Notes

### The One-Meaning-Per-Word Principle

The original ASD-STE100 is built on the principle that each approved word should have exactly one approved meaning. This principle comes from aerospace documentation, where a misunderstood word can cause a fatal error. In code documentation, a misunderstood word can cause a bug, a security vulnerability, or a system failure. The same principle applies: each approved word must have one clear meaning in your documentation.

When a word has two meanings that are both common in software engineering, the STE-Code dictionary assigns only one approved meaning. The other meaning must be expressed with a different word or a phrase. This is intentional. It removes ambiguity. For example:

- "Log" is approved as a noun (the record of events). It is not approved as a verb. If you want to describe the action of adding to a log, use "write to the log."
- "Help" is approved as a verb (to assist). It is not approved as a noun. If you want to refer to help documentation, use "help text" or "help information."
- "Damage" is approved as a noun (harm or injury). It is not approved as a verb. If you want to describe causing damage, use "cause damage" or "do damage."

### Parts of Speech in the Code-Documentation Mix

In standard English, a word's part of speech is shown by its position in the sentence and by inflectional endings (-s, -ed, -ing). In code documentation, a word's part of speech is further complicated because code documentation mixes natural language with code symbols. A word in your documentation can be:

1. A natural language word whose part of speech follows English grammar rules and STE-Code restrictions.
2. A code keyword in code font (technical noun, Rule 1.5), which has no English part of speech.
3. A framework, library, or tool name (technical noun, Rule 1.5), which is a proper noun.
4. A parameter, variable, or function name (technical noun, Rule 1.5), which is a proper noun.

When you apply Rule 9.2, first identify which category the word belongs to. If the word is in category 1, check the STE-Code dictionary for its approved part of speech and approved meaning. If the word is in categories 2, 3, or 4, the part-of-speech restriction does not apply because the word is not English prose — it is a technical identifier.

### The Noun-Verb Boundary in Code Documentation

The boundary between noun and verb is the most frequent source of Rule 9.2 violations in code documentation. Many words that are used as both nouns and verbs in general software English have only one approved part of speech in STE-Code. The pattern is:

- If a word is approved only as a verb, you must restructure sentences that use it as a noun. For example, "run" is approved as a verb and as part of compound nouns like "test run." You cannot write "do a run" — write "run the program" or "do a test run."
- If a word is approved only as a noun, you must restructure sentences that use it as a verb. For example, "log" is approved as a noun. You cannot write "log the error" — write "write the error to the log."
- If a word is approved as both, you must make the function clear from context. Add determiners for nouns ("the build," "a set"), and use imperative or inflected forms for verbs ("build the project," "sets the value").

The original ASD-STE100 notes that "in English, words usually do not have different forms that immediately show their function in a sentence." This is exactly why Rule 9.2 is necessary. In standard English, "log" could be a noun or a verb, and the reader must guess from context. In STE-Code, the dictionary removes the guess by assigning one approved part of speech.

### The Adjective-Verb Distinction

Some approved words can function as adjectives when they modify a noun, even if the dictionary lists them only as verbs or nouns. This is because English allows nouns and verbs to function as noun adjuncts (a noun that modifies another noun) or participles (a verb form that functions as an adjective). The original ASD-STE100 permits this when the meaning is clear:

- "The build process" uses "build" (noun) as a noun adjunct modifying "process." This is allowed because "build" is approved as a noun and its meaning does not change.
- "The configured storage" uses "configured" (past participle of the verb "configure") as an adjective. This is allowed because "configure" is approved as a technical verb (Rule 1.12) and the past participle keeps the same meaning.
- "The running service" uses the -ing form of "run" as an adjective. The original ASD-STE100 Rule 1.4 gives guidance on when -ing forms are permitted as adjectives. In general, prefer the simple form: "the service that runs" is clearer than "the running service."

When you use an approved word in a noun-adjunct or participle role, make sure that its approved meaning does not change. If the meaning shifts (for example, "the running total" where "running" means "continuously updated," which is a different meaning from "run" as a verb), use a different construction or a different approved word.

### Using the Dictionary as the Source of Truth

Rule 9.2 cannot be applied without the STE-Code dictionary. The dictionary is the authoritative reference for which words are approved, which part of speech they are approved for, and which meaning they are approved with. Before you write any documentation, you must be familiar with the dictionary entries for the words you plan to use. When you are not sure about a word, look it up.

The dictionary also gives approved alternatives for unapproved words. When you find an unapproved word in your draft, first check if the dictionary gives an approved alternative with the same part of speech. If it does, do a word-for-word replacement. If it does not, apply Rule 9.1 to restructure the sentence. After restructuring, apply Rule 9.2 again to make sure that every word in the new sentence is used correctly.

## Cross-References

This rule is the central quality-control rule in the STE-Code system. It interacts with most other rules. The most important cross-references are:

- **Rule 1.1 (Use Approved Words):** Rule 9.2 is the rule that tells you how to use the approved words from Rule 1.1. Rule 1.1 says which words you can use. Rule 9.2 says how you must use them.
- **Rule 1.2 (Use Words Only as Their Specified Part of Speech):** This rule is a direct statement of the part-of-speech constraint. Rule 9.2 gives the detailed justification and the procedure for applying the constraint. Together, they make sure that each word appears only in its approved grammatical role.
- **Rule 1.3 (Use Words Only With Their Approved Meanings):** This rule is a direct statement of the meaning constraint. Rule 9.2 gives the detailed justification and examples. Together, they make sure that each word communicates exactly one concept.
- **Rule 1.4 (Use Only Approved Verb Forms and Adjective Forms):** When you use an approved word in a verb form or adjective form that is not in the dictionary, Rule 1.4 applies. Rule 9.2 tells you to check the dictionary for the approved part of speech. Rule 1.4 tells you which inflections are permitted.
- **Rule 1.5 (Technical Code Nouns Are Allowed):** Technical code nouns (keywords, framework names, library names, function names) are not subject to the part-of-speech and meaning restrictions of Rule 9.2. When you apply Rule 9.2, first identify technical nouns and exclude them from the check.
- **Rule 1.7 (Do Not Use Technical Nouns as Verbs):** When a technical noun is used as a verb (for example, "to docker the application"), Rule 1.7 applies. Rule 9.2 reinforces this by requiring that each word be used as its approved part of speech. If a word is approved as a noun, it cannot be used as a verb even if it is a technical term.
- **Rule 1.12 (Technical Verbs Are Allowed):** Technical verbs like "build," "deploy," "test," "lint," "compile," and "debug" are approved as verbs even if they are not in the general STE-Code dictionary. Rule 9.2 applies to technical verbs: you must use them with their correct technical meaning and not confuse them with their general-English meanings.
- **Rule 9.1 (Use a Different Sentence Construction):** When a word-for-word replacement is not sufficient because the approved alternative has a different part of speech or changes the meaning, you must use Rule 9.1 to restructure the sentence. After restructuring, apply Rule 9.2 to the new sentence.
- **Rule 9.3 (Do Not Make Phrasal Verbs):** When you use approved verbs, do not combine them with prepositions to make phrasal verbs that have unapproved meanings. Rule 9.2 tells you to use approved words with their approved meanings. Rule 9.3 prevents you from creating new meanings by combining approved words.
- **Rule 9.4 (Consistent Style):** After you apply Rule 9.2 to individual words, apply Rule 9.4 to make sure that you use the same approved words for the same concepts throughout the document and across the project.
- **The STE-Code Dictionary (A-Z):** The dictionary is the source of truth for Rule 9.2. You cannot apply this rule without consulting the dictionary. Every word you write must be checked against the dictionary's approved meaning column and approved part of speech.

> **See also:** Rule 1.1 — Use Approved Words
> **See also:** Rule 1.2 — Use Words Only as Their Specified Part of Speech
> **See also:** Rule 1.3 — Use Words Only With Their Approved Meanings
> **See also:** Rule 1.4 — Use Only Approved Verb Forms and Adjective Forms
> **See also:** Rule 1.5 — Technical Code Nouns Are Allowed
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
> **See also:** Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient
> **See also:** Rule 9.3 — When You Use Two Words Together, Do Not Make Phrasal Verbs
> **See also:** Rule 9.4 — Consistent Style

