# Rule 1.6 — Use a Word That Is Not Approved in the Dictionary, Only When It Is a Code-Domain Technical Noun or Part of a Code-Domain Technical Noun

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.6](ste-code/grouped/), Rule 1.6

## Original Rule

**Rule 1.6** Use a word that is not approved in the dictionary, only when it is a technical noun or part of a technical noun.

The dictionary includes some words that you cannot use because they are not approved. But if you can put these words in an applicable category of technical nouns, you can use them as technical nouns in some contexts.

Examples:

The word "base" is not approved in the dictionary and its alternative is "bottom (n)."

> **Non-STE:** Make sure that the two spigots at the base of the unit engage.

("Base" is not permitted when it is related to a surface.)

> **STE:** Make sure that the two spigots at the bottom of the unit engage.

But you can use "base" as a technical noun.

("Base" is a technical noun, category 7, mathematical, scientific, engineering terms, and formulas.)

The same word "base" can go into different categories of technical nouns. This condition occurs when you use the word "base" with different meanings in different contexts.

("Base" is a technical noun, category 5, facilities, infrastructure, and logistic procedures.)

"Backup" is not approved in the dictionary and its alternatives are "emergency (n)" and "auxiliary (adj)." But you can use "backup" as a technical noun.

("Backup" is a technical noun, category 19, computer science, information and communication technology.)

"Backup" is a one-word technical noun. But you can also write "backup file," a two-word technical noun.

("Backup file" is a technical noun, category 19, computer science, information and communication technology.)

"Main" is a word that is not approved, and its alternative is "primary (adj)."

("Main part" is not a technical noun, and it is correct to replace "main" with "primary.")

But you can use "main" as part of a technical noun.

("Main landing gear" is a technical noun. It is incorrect to replace "main" with "primary" here, because "primary landing gear" is not the technical noun that is approved in your company, industry, or subject field.)

If a word is not in the dictionary, you can use it if it is part of a technical noun. In the example that follows, "angular" and "position" are approved but "relative" is not in the dictionary.

(You can use "relative" as part of a technical noun, category 7, mathematical, scientific, engineering terms, and formulas.)

## STE-Code Adaptation

**Rule 1.6** Use a word that is not approved in the controlled terminology, only when it is a code-domain technical noun or part of a code-domain technical noun.

The controlled terminology includes some words that you cannot use because they are not approved. But if you can put these words in an applicable category of code-domain technical nouns, you can use them as code-domain technical nouns in some contexts.

"Handler" is not approved in the controlled terminology and its alternative is "function (n)." A writer must use "function" instead of "handler" when referring to a general processing function.

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.

But you can use "handler" as part of a code-domain technical noun.

> **STE:** The event handler processes each incoming event.
>
> *Adapted from spec pair: "base" can be used as a technical noun in categories 7 and 5. Just as "base" transitions from unapproved word to technical noun when part of a recognized compound term, "handler" transitions from unapproved word to code-domain technical noun when part of "event handler."*

("Event handler" is a code-domain technical noun, category 1, code components, modules, and libraries.)

"Main" is not approved in the controlled terminology and its alternative is "primary (adj)." When "main" is used as a general adjective, it must be replaced with "primary."

> **Non-STE:** The main configuration has the latest values.
>
> **STE:** The primary configuration has the latest values.

But you can use "main" as part of a code-domain technical noun.

> **STE:** Merge the feature branch into the main branch.
>
> *Adapted from spec pair: "Main landing gear" is a technical noun and it is incorrect to replace "main" with "primary." Just as "primary landing gear" is not the approved technical name, "primary branch" is not the approved code-domain technical noun. The official Git term "main branch" must be used.*

("Main branch" is a code-domain technical noun, category 5, infrastructure, deployment, and platforms. It is incorrect to replace "main" with "primary" here, because "primary branch" is not the technical noun that is approved in your project, industry, or subject field.)

"Base" is not approved in the controlled terminology and its alternative is "bottom (n)" for a surface location. When "base" refers to a physical surface, replace it with "bottom."

> **Non-STE:** Make sure that the two connectors at the base of the chassis engage.
>
> **STE:** Make sure that the two connectors at the bottom of the chassis engage.

But "base" is permitted as part of code-domain technical nouns such as "base case" (category 7) and "base class" (category 1).

## Examples

> *Adapted from spec pair:* Non-STE: Make sure that the two spigots at the base of the unit engage.  |  STE: Make sure that the two spigots at the bottom of the unit engage.

### Core Spec Adaptations

The two source examples (handler and main) show the full gate: an unapproved word fails when it is a general noun or adjective, and passes when it is embedded in a recognized code-domain technical noun.

> **Non-STE:** A Python module that uses "handler" as a general noun for any processing unit, and "main" as a general adjective for the primary configuration:

```python
# config_loader.py
def handler(name):
    """The handler loads the config file and returns the data."""
    with open(name) as fh:
        return fh.read()

# start the main worker that uses the handler
if __name__ == "__main__":
    data = handler("app.conf")
    print(data)
```

> **STE:** Replace "handler" with the approved noun "function" when it is a general processing unit. Keep "main" only where it names the entry-point function `main()`; use "primary" for the general adjective. The compound "event handler" may stay because it is a code-domain technical noun (category 1):

```python
# config_loader.py
def load_config(name):
    """The function loads the config file and returns the data."""
    with open(name) as fh:
        return fh.read()

# start the primary worker that uses the function
if __name__ == "__main__":
    data = load_config("app.conf")
    print(data)
```

> **Non-STE:** A Git instruction that treats "main branch" as if it needed replacement, and "base" as a surface word:

```
Check out the primary branch, then copy the files to the base of the build folder.
```

> **STE:** "Main branch" is a recognized Git technical noun (category 5) and stays. "Base" as a surface location becomes "bottom":

```
Check out the main branch, then copy the files to the bottom of the build folder.
```

### README Files

README files mix descriptive prose with tool, library, and package names. The tool names are technical nouns; the prose must use approved words.

> **Non-STE:** A README section that uses unapproved words in the descriptive prose and as verbs:

```markdown
# Acme API

The base setup leverages Express for the main API and MongoDB for the database backend.
The handler backs up the data every night.
```

> **STE:** Replace "base" (general adjective) with "primary", "leverages" with "uses", "handler" with "function", and "backs up" with "makes an auxiliary copy". The package names "Express", "MongoDB", and "database backend" are code-domain technical nouns (categories 3 and 18) and stay:

```markdown
# Acme API

The primary setup uses Express for the main API and MongoDB for the database backend.
The function makes an auxiliary copy of the data each night.
```

> **Non-STE:** A README that refers to a project by a name that contains an unapproved word, then breaks the compound apart:

```
Install react-router. The router in react-router is not approved, so replace it with a controller.
```

> **STE:** "React Router" is a package name — a code-domain technical noun (category 3). Keep the compound whole; do not split the unapproved word out:

```markdown
## Routing
Install `react-router`. The `react-router` package manages client-side routes.
```

### API Documentation

Endpoint paths, HTTP method names, header names, and field names are code-domain technical nouns. The prose that describes them must use approved words.

> **Non-STE:** An OpenAPI description that uses "backup" as a verb and a vague adjective:

```yaml
/post:
  summary: Backups the database and returns a backup ID.
  responses:
    '200':
      description: The backup was made. The handler processed the request.
```

> **STE:** The path `/api/v1/backup` and the field "backup ID" are technical nouns (category 18) and stay. The verb "Backups" becomes "Makes an auxiliary copy"; "handler" becomes "event handler":

```yaml
/api/v1/backup:
  summary: Makes an auxiliary copy of the database. Returns a backup ID.
  responses:
    '200':
      description: The auxiliary copy was made. The event handler processed the request.
```

> **Non-STE:** An endpoint note that uses an unapproved phrasal verb built from a technical noun:

```
POST /api/v1/backup — Authenticates the user and backups the records.
```

> **STE:** "Authenticates" is approved in the controlled terminology for this context; "backups" becomes "makes an auxiliary copy":

```
POST /api/v1/backup — Checks the user and makes an auxiliary copy of the records.
```

### Docstrings and Inline Comments

Docstrings and comments must use approved words; only quoted code names are exempt.

> **Non-STE:** A Python docstring and a comment that use unapproved verbs and a general "base":

```python
def serve(req):
    """Handles the request and returns a response."""
    # base case: handler returns null when req is empty
    if not req:
        return None
    return build(req)
```

> **STE:** "Handles" becomes "processes"; "base case" is a code-domain technical noun (category 7) and stays; "handler" becomes "event handler":

```python
def serve(req):
    """Processes the request and returns a response."""
    # base case: the event handler returns null when req is empty
    if not req:
        return None
    return build(req)
```

> **Non-STE:** A Go comment that uses "handler" as a standalone general word:

```go
// processEdgeCase runs when the base URL is null and the handler times out.
func processEdgeCase() {
    // ...
}
```

> **STE:** "Base URL" is a compound technical noun and stays; "handler" becomes "event handler"; "times out" becomes "runs longer than the timeout":

```go
// processEdgeCase runs when the base URL is null and the event handler runs longer than the timeout.
func processEdgeCase() {
    // ...
}
```

### Commit Messages

Conventional commit prefixes are code-domain technical nouns; the description must follow Rule 1.6.

> **Non-STE:** A commit message that uses "backup" as a verb, "main" as a general adjective, and "handler" alone:

```
feat: add handler for the backup endpoint and the main config loader
```

> **STE:** "Handler" becomes "event handler" (technical noun); "backup" as a standalone adjective becomes "auxiliary"; "main config loader" becomes "primary config loader" because "main" is a general adjective here:

```
feat: add an event handler for the auxiliary-copy endpoint and the primary config loader
```

> **Non-STE:** A commit that treats "backup" and "main" as if they were always unapproved, even inside a named component:

```
fix: run the main backup script before the primary migration
```

> **STE:** "Backup script" is a recognized compound technical noun (category 18) and stays. "Main" as a general adjective becomes "primary":

```
fix: run the backup script before the primary migration
```

> **Non-STE:** A commit where a project glossary defines "main config" as a named file, but the writer still replaces it:

```
chore: update the primary config loader settings
```

> **STE:** Because the project glossary names the file "main config", the compound is a technical noun (category 1) and "main" is permitted:

```
chore: update the main config loader settings
```

### Error Messages

Error messages shown in logs and terminals must use approved words; error codes and type names are technical nouns.

> **Non-STE:** A CI log line that uses two standalone unapproved words:

```
Error: base config file not found. The backup handler will exit.
```

> **STE:** "Base" becomes "primary"; "backup handler" becomes "event handler for auxiliary copies"; "config file" and "event handler" are technical nouns (category 1, 18):

```
Error: primary config file not found. The event handler for auxiliary copies will stop.
```

> **Non-STE:** A runtime error that uses a phrasal verb from a technical noun:

```
Build failed: the main config loader timed out. The backup handler did not start.
```

> **STE:** "Timed out" becomes "ran longer than the timeout" (timeout is a technical noun, category 13, but the phrasal verb is unapproved); "main" becomes "primary"; "backup handler" becomes "auxiliary-copy handler":

```
Build failed: the primary config loader ran longer than the timeout. The auxiliary-copy handler did not start.
```

### Object-Oriented Paradigm (Java, C++, C#, Python Classes)

Class names, interface names, and design-pattern names are code-domain technical nouns (category 1).

> **Non-STE:** A Java class whose docstring uses unapproved verbs and a general "base":

```java
/**
 * The BaseService class handlers requests and backups data.
 * It factories new instances via the MainFactory.
 */
class BaseService { }
```

> **STE:** `BaseService` and `MainFactory` are class names (technical nouns) and stay. "Handlers" becomes "processes"; "backups" becomes "makes auxiliary copies"; "factories" becomes "makes":

```java
/**
 * The BaseService class processes requests and makes auxiliary copies of data.
 * It makes new instances with the MainFactory class.
 */
class BaseService { }
```

> **Non-STE:** A docstring that turns a technical noun into a verb (Rule 1.7 violation):

```python
class Cache:
    """This class singletons the connection for all callers."""
```

> **STE:** "Singleton" is a design-pattern technical noun (category 7); do not use it as a verb. State the pattern with approved words:

```python
class Cache:
    """This class uses the Singleton pattern for the connection used by all callers."""
```

### Functional Paradigm (Haskell, Elixir, Clojure, Rust)

Type names and monad names are technical nouns. "Base case" and "base functor" are permitted compound technical nouns (category 7).

> **Non-STE:** A Haskell comment that uses unapproved verbs and a non-standard "base monad":

```haskell
-- The ReaderT transformer wraps the base monad. It handlers the environment and backups the state.
runApp :: ReaderT Env IO ()
runApp = undefined
```

> **STE:** "Base monad" is permitted only if the library's own docs use it; otherwise use "underlying monad". "Handlers" becomes "supplies"; "backups" becomes "makes an auxiliary copy"; `ReaderT` is a type name (technical noun) and stays:

```haskell
-- The ReaderT transformer wraps the underlying monad. It supplies the environment to each function and makes an auxiliary copy of the state.
runApp :: ReaderT Env IO ()
runApp = undefined
```

> **Non-STE:** A docstring that uses "base case" correctly but verbs wrongly:

```python
def fib(n):
    """Base case returns 1. Recursive case handlers the sum."""
```

> **STE:** "Base case" is a code-domain technical noun (category 7) and stays. "Handlers" becomes "processes":

```python
def fib(n):
    """The base case returns 1. The recursive case processes the sum."""
```

### Procedural Paradigm (C, Go, Bash)

Function names, struct names, and command names are technical nouns. `main()` and the Go `main` package are permitted; "main" as a general adjective is not.

> **Non-STE:** A C comment that uses "handler" and "backup" as standalone general words:

```c
/* The main function calls the backup routine and then the handler for each file. */
void main(void) { }
```

> **STE:** `main` is the entry-point function name (technical noun) and stays. "Backup routine" and "file handler" are code-domain technical nouns (category 1, 18) and stay. Make "handler" explicit as "file handler":

```c
/* The main function calls the backup routine and then the file handler for each file. */
void main(void) { }
```

> **Non-STE:** A Go doc that uses "main" as a general adjective for a goroutine:

```go
// startMain starts the main goroutine that reads from the queue.
func startMain() { }
```

> **STE:** Unless the project convention treats "main goroutine" as a technical noun, "main" becomes "primary":

```go
// startPrimary starts the primary goroutine that reads from the queue.
func startPrimary() { }
```

### Declarative Paradigm (SQL, Terraform, Kubernetes YAML)

Resource names, table names, column names, and property names are technical nouns.

> **Non-STE:** A SQL comment and a Kubernetes manifest comment with unapproved words:

```sql
-- the backup_logs table backups the records each night
SELECT * FROM backup_logs;
```

```yaml
# This ConfigMap holds the base settings. The handler deployment backups the data.
```

> **STE:** `backup_logs` is a table name (technical noun, category 18) and stays; "backups" becomes "keeps auxiliary copies". "ConfigMap" is a resource name (technical noun, category 5) and stays; "base" becomes "primary"; "handler Deployment" stays as a named resource:

```sql
-- the backup_logs table keeps auxiliary copies of the records each night
SELECT * FROM backup_logs;
```

```yaml
# This ConfigMap holds the primary settings. The handler Deployment makes auxiliary copies of the data.
```

### Systems Paradigm (Rust Ownership, C Memory Management)

Dense vocabularies where "unsafe", "raw pointer", and "dangling pointer" are technical nouns.

> **Non-STE:** A Rust comment that uses "unsafe" as a descriptive adjective and "base" as a general word:

```rust
// the main function uses an unsafe block to access the raw pointer.
// the handler drops the base allocation.
fn main() {
    let p = std::ptr::null_mut::<i32>();
    drop(p);
}
```

> **STE:** `main` is the function name (technical noun) and stays. `unsafe` block and `raw pointer` are technical nouns (category 6) and stay. "Handler" becomes "drop handler"; "base allocation" becomes "primary allocation" because "base" is a general adjective there:

```rust
// the main function uses an unsafe block to access the raw pointer.
// the drop handler frees the primary allocation.
fn main() {
    let p = std::ptr::null_mut::<i32>();
    drop(p);
}
```

> **Non-STE:** A comment that uses "unsafe" as a vague descriptive adjective:

```
This approach is unsafe because the buffer is shared.
```

> **STE:** "Unsafe" is not an approved adjective; use the approved adjective with negation. The `unsafe` Rust keyword is a separate technical noun and is backtick-quoted when referring to the construct:

```
This approach is not safe because the buffer is shared.
```

## Decision Procedure — The Technical Noun Gate

Rule 1.6 acts as a gate. An unapproved word may stay in code documentation only when it clears all three tests below. If it fails any test, replace it with the approved alternative from the controlled terminology or restructure the sentence.

### Test 1 — Is the word unapproved?

Approved words never enter this gate. They pass through Rule 1.1 and Rule 1.2 instead. Only unapproved words are tested here.

- "function" is approved — not tested by Rule 1.6.
- "handler" is unapproved — enters the gate.

### Test 2 — Is it a technical noun, or part of a compound technical noun?

The unapproved word must either be a standalone technical noun that fits one of the 19 categories (Rule 1.5), or embedded inside a compound technical noun that fits a category.

- "handler" alone — not a recognized technical noun — fails Test 2.
- "event handler" — recognized design-pattern term, category 1 — passes Test 2.
- "main" alone — not a recognized technical noun — fails Test 2.
- "main branch" — recognized Git term, category 5 — passes Test 2.

### Test 3 — Is it used as a noun in the sentence?

Even a word that passes Test 2 must function as a noun. If it is a verb, adjective, or adverb, it fails Test 3. This is enforced by Rule 1.7.

- "The event handler processes the request." — "event handler" is a noun — passes.
- "This class handlers the request." — "handlers" is a verb — fails Test 3 even though "handler" is a known technical noun. Replace with "processes" or "The request handler processes the request."

### Worked trace

> **Non-STE:** The main config loader backups the data through the handler pipeline.

> **STE:** The primary config loader makes an auxiliary copy of the data through the processing pipeline.

| Word / phrase | Test 1 (unapproved?) | Test 2 (technical noun?) | Test 3 (used as noun?) | Result |
|---|---|---|---|---|
| main config loader | yes | "main" is a general adjective, not part of a recognized compound here | — | replace "main" → "primary" |
| backups | yes | "backup" as a verb is not a technical noun | used as verb | replace with "makes an auxiliary copy" |
| handler pipeline | yes | "handler" + "pipeline" is not a recognized compound | used as noun, but fails Test 2 | replace with "processing pipeline" |

### Compound technical noun checklist

A compound counts as a code-domain technical noun only when all three are true:

1. The words combine to name one concept that the domain recognizes.
2. The compound fits one of the 19 categories.
3. Replacing the unapproved word with its approved alternative changes the recognized name and causes confusion.

If you can swap the unapproved word for its approved alternative and the term still names the same concept, it is NOT a technical noun — make the replacement. If the swap produces a name no one in the domain would recognize, the compound IS a technical noun and the unapproved word is permitted inside it.

### Category overlap — the same word in different categories

The same unapproved word can pass through the gate in different categories when its meaning changes:

- "base" passes as part of "base case" (category 7, algorithmic), "base class" (category 1, code components), and "base URL" (category 8, directory hierarchy). It fails when used as a general adjective for a surface ("the base of the file") where "bottom" applies.
- "cache" passes as a standalone technical noun in category 6 (cache layer), category 16 (cache invalidation), and category 18 (query cache).

In each case the word names a specific concept within a category. It is not a general adjective or verb.

### Distinguishing a technical noun from a descriptive adjective

The hardest judgment in Rule 1.6 is telling a permitted technical noun from a descriptive adjective that must be replaced.

1a. "Check out the main branch before you merge." — "main branch" is a Git convention, a technical noun. Permitted.
1b. "The main configuration has the latest values." — "main" is a descriptive adjective. Replace with "primary".

2a. "The base case returns the single-element array." — "base case" is an algorithmic term. Permitted.
2b. "The base configuration is loaded first." — "base" is a descriptive adjective. Replace with "primary".

3a. "The event handler processes each request." — "event handler" is a design-pattern term. Permitted.
3b. "The handler processes each request." — "handler" alone is not a recognized technical noun. Replace with "function".

Criterion: does the compound appear in the official documentation of the framework, language, or standard? If yes, it is a technical noun. If no, it is descriptive prose and the unapproved words must be replaced.

### Edge Cases

**Edge Case 1 — Framework name that is also an unapproved word.** When a word is the proper name of a tool, it is a technical noun (category 3); when used with its general meaning, it is unapproved.

> **Non-STE:** A setup script that confuses the library name with the general verb:

```bash
# use pandas to data-frame the csv, then express the results as json
python etl.py
```

> **STE:** `pandas` is a library name (technical noun) and stays; "data-frame" as a verb becomes "load ... into a data frame"; "express" as a general verb becomes "use Express" (the framework name, technical noun). Capitalize tool names as published:

```bash
# use pandas to load the csv into a data frame, then use Express to send the results as json
python etl.py
```

**Edge Case 2 — Code keyword that is also an unapproved general word.** Inside backticks a keyword is quoted text (category 10) and exempt; in prose its role decides.

> **Non-STE:** Prose that uses "class" as a general noun and "main" as a general adjective:

```
The class of objects that return a value must not block the main thread.
```

> **STE:** "Class" as a general noun becomes "category"; `return` as a keyword is backtick-quoted (technical noun); "main" as a general adjective becomes "primary":

```
The category of objects that `return` a value must not block the primary thread.
```

**Edge Case 3 — A compound that looks like a technical noun but is not recognized.** A compound qualifies only if a project glossary, framework docs, an industry standard (RFC, W3C), or one of the 19 categories confirms it.

> **Non-STE:** Three invented compounds with unapproved words and no recognized status:

```
The handler pipeline integrates with the backup orchestrator via the main dispatcher.
```

> **STE:** None of the three compounds is recognized, so restructure with approved words: "processing pipeline", "auxiliary-copy service", "primary dispatcher":

```
The processing pipeline integrates with the auxiliary-copy service through the primary dispatcher.
```

**Edge Case 4 — Auto-generated documentation.** Apply Rule 1.6 to the source (docstrings, comments, annotations), not the generated output.

> **Non-STE source:** A C# XML doc that uses unapproved verbs:

```csharp
/// <summary>Handlers the backup operation for the main controller.</summary>
public void Run() { }
```

> **STE source:** Fix at the source; the generated docs inherit compliance:

```csharp
/// <summary>Processes the auxiliary-copy operation for the primary controller.</summary>
public void Run() { }
```

**Edge Case 5 — Open-source project names and brand names.** The project name is always a technical noun (category 3 or 11); descriptive phrases that echo it are still reviewed.

> **Non-STE:** A README that uses a project name as a technical noun but also uses the same word generally:

```
Use Homebrew to install the base packages. Then webpack the main bundle.
```

> **STE:** `Homebrew` is a project name (technical noun) and stays; "base" becomes "primary"; `webpack` as a verb becomes "use `webpack` to make"; "main" becomes "primary":

```
Use Homebrew to install the primary packages. Then use `webpack` to make the primary bundle.
```

## Dictionary and Category Reference

**Controlled-terminology entries referenced by this rule** (see `a-dictionary.md` for the full list):

- **BASE (n) — UNAPPROVED.** Approved alternatives: BOTTOM (n) for a surface or stack position, ROOT (n) for a positional or filesystem root. Permitted as part of compound code-domain technical nouns: "base case" (category 7), "base class" (category 1), "base URL" (category 8).
- **MAIN (adj) — UNAPPROVED.** Approved alternative: PRIMARY (adj). Permitted as part of "main branch" (category 5) and "main function" / `main()` (category 1, the entry-point function).
- **HANDLER (n) — UNAPPROVED.** Approved alternative: FUNCTION (n). Permitted as part of compound technical nouns such as "event handler" and "request handler" (category 1).
- **BACKUP (n, v) — UNAPPROVED.** Approved alternatives: AUXILIARY (adj) for the adjective sense, and the construction "makes an auxiliary copy" for the verb sense. Permitted as part of "backup file", "backup_logs" (category 18), and resource names such as `/api/v1/backup` (category 19).
- **BOTTOM (n), BOTTOM (adj) — APPROVED.** The approved alternative for "base" when it refers to a physical surface or stack position.
- **FUNCTION (n) — APPROVED.** The approved alternative for a standalone unapproved "handler".
- **PRIMARY (adj) — APPROVED.** The approved alternative for "main" used as a general adjective.
- **AUXILIARY (adj) — APPROVED.** One approved alternative for "backup".
- **ROOT (n) — (TN).** Code-domain technical noun for the top-level directory in a filesystem. Permitted (category 5 or 13). Approved alternative for "base" in positional contexts.

**Categories most often used by Rule 1.6** (see `a-categories.md`):

- Category 1 — Code components, modules, and libraries (event handler, base class, main function)
- Category 3 — Development tools, environments, and support equipment (Express, pandas, webpack)
- Category 5 — Infrastructure, deployment, and platforms (main branch, ConfigMap)
- Category 7 — Mathematical, algorithmic, and scientific terms (base case, base functor)
- Category 8 — Codebase navigation and directory hierarchy (base URL, Git root)
- Category 18 — Database and storage terminology (backup_logs, backup file, config file)
- Category 19 — Computer science, information, and communication technology (backup as a resource name, API)

> **See also:** Rule 1.1 — Use Approved Words from the Dictionary, Technical Nouns, or Technical Verbs
> **See also:** Rule 1.2 — Use Approved Words Only as the Specified Part of Speech
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.7 — Do Not Use Technical Nouns as Verbs
> **See also:** Rule 1.8 — Use Standard, Well-Known Technical Nouns
> **See also:** Rule 1.9 — Prefer Short, Clear Technical Nouns
> **See also:** Rule 1.11 — One Term Per Concept — Be Consistent
> **See also:** Rule 1.12 — Technical Verbs Are Allowed
