# Level 3 — STE-Code Section 4: Sentence Structure (Rules 4.1–4.5)

This slice covers the five Section 4 rules that govern sentence-level structure in
code documentation: one topic per sentence, no omitted words or contractions,
vertical lists, connecting words, and articles / demonstrative adjectives.

Apply these rules to docstrings, API references, README sections, commit messages,
and code comments. This is the Level 3 (high-fidelity) form: every rule is complete
with code-domain examples, paradigm guidance, edge cases, grammar notes, and a
checklist. Use the checklist at the end of each rule as a quick pass before you
publish documentation.

Each rule below gives: the requirement, code-domain examples, paradigm-specific
guidance, edge cases, grammar notes, and a summary checklist.

---

## Rule 4.1 — One Topic Per Sentence, No Abstract Text

**Requirement**
- Descriptive text (a class, module, or type description): each sentence has one
  topic and does not use the imperative mood. Add detail in the sentences that follow.
- Procedural text (an API method or function description): one instruction per
  sentence in the imperative mood.
- Never write abstract sentences. Show how to use a function or how a module
  operates. State the action or the measured result — not a vague property.

**Code examples — descriptive (one topic per sentence)**
- Non-STE: `The HttpClient class has two internal buffers connected together and linked with callbacks between the request handler and the response dispatcher.`
- STE: `The HttpClient class has two internal buffers. The internal buffers are connected together with callbacks. These callbacks link the request handler to the response dispatcher.`

**Code example — descriptive docstring (Java)**
```java
/**
 * STE:
 * The ConnectionPool manages a set of reusable TCP connections.
 * The connections are created lazily when the pool starts.
 * Each connection is validated when the caller checks it out.
 * Each connection is reset before the caller returns it to the pool.
 * The caller always receives a clean socket from the pool.
 */
public class ConnectionPool { /* ... */ }
```

**Code examples — avoid abstract statements**
- Non-STE: `No null values are permitted.` → STE: `Make sure that the function does not return a null value.`
- Non-STE: `Different payload sizes will change the parse time.` → STE: `When the payload size increases, the parse time will increase.` / `The parse time is 2 milliseconds for a payload of 1 KB.`

**Code example — avoid abstract statements (Python docstring)**
```python
# Non-STE:
def read_config(path: str) -> dict:
    """Loads the configuration. Returns None on error."""
    ...

# STE:
def read_config(path: str) -> dict:
    """Load the configuration from the file at the given path.
    Return an empty dictionary if the file does not exist.
    Do not return null. Raise ConfigError if the file is not valid."""
    ...
```

**Code example — procedural (one instruction per sentence, imperative)**
```python
# STE:
# 1. Build the HttpClient with the default configuration.
# 2. Set the timeout to 30 seconds.
# 3. Call the send method with the request object.
# 4. Check the response status code.
# 5. Read the response body into a string.
def send_request(req: Request) -> str:
    ...
```

**Code example — procedural (Bash CLI)**
```bash
# STE:
# 1. Export the API token to the TOKEN variable.
# 2. Select the staging environment with the --env flag.
# 3. Run the deploy script.
# 4. Check the build log for the success message.
```

**Code example — declarative resource (Terraform)**
```hcl
# STE:
# The aws_s3_bucket resource creates a storage bucket for application logs.
# The bucket name is "app-logs".
# The bucket keeps a version of each object that you overwrite.
# The bucket encrypts each object with the AES256 algorithm.
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs"
}
```

**Paradigm guidance**
- Object-Oriented (Java, C++, C#, Python): class docs are descriptive (one short sentence, one topic); method descriptions are numbered imperative steps.
- Functional (Haskell, Elixir, Clojure, Rust): type signatures descriptive (one property per sentence); effectful functions use procedural steps.
- Procedural (C, Go, Bash): function docs are a sequence of steps; each step is one imperative sentence with one instruction.
- Declarative (SQL, Terraform, Kubernetes YAML): resource docs descriptive; describe what the configuration does, one fact per sentence.
- Systems (Rust ownership, C memory): describe invariants and ownership rules in descriptive sentences; use imperative steps only for unsafe operations.

**Edge cases**
- Generated documentation (JSDoc, Sphinx, `go doc`): apply Rule 4.1 to the source docstrings and comments; fix the source text, not the generated output.
- Single-sentence module summary: the first line conveys the purpose; expand the body with one topic per sentence.
- Safety callouts (BREAKING, DEPRECATED, NOTE): keep the callout to one short sentence; put detail in the paragraph that follows.
- Error messages: one topic; state what failed and, when useful, tell the reader how to fix it in a second sentence. Do not write a vague abstract error such as "Invalid input occurred."
- Commit messages: subject line one topic; each related change its own bullet in the body.
- README sections: one idea per paragraph; one sentence per listed feature.

**Grammar notes**
- Sentence length: max 20 words for procedural, 25 words for descriptive. Code spans, inline code, and URLs do not count.
- Imperative mood: start each procedural step with an imperative verb (call, set, pass, check, start, send, remove, add, make, use, run, build, test, deploy). Avoid "you should" / "the user must."
- Clause nesting: do not nest clauses deeper than two levels; break nested clauses into separate sentences.
- Voice: prefer active for both descriptive and procedural sentences; the subject performs the action.
- Abstract text: replace "performance may vary" with a sentence giving the measured value and the condition.

**Checklist**
- [ ] Max 20 words (procedural) / 25 words (descriptive).
- [ ] One topic or one instruction per sentence.
- [ ] Procedural sentences use the imperative mood.
- [ ] Descriptive sentences do not use the imperative mood.
- [ ] Text is not abstract; shows how to use the code.
- [ ] Each descriptive sentence states one fact in the active voice.
- [ ] Each measurable claim gives the value and the condition.

---

## Rule 4.2 — Do Not Omit Words or Use Contractions

**Requirement**
- Every sentence must have all its parts. Do not omit words or use contractions to
  make a sentence shorter; a shorter sentence is not necessarily easier to read.
- Do not omit nouns (the reader will not know which code element the sentence refers to).
- Do not omit verbs (the reader will not understand the action performed).
- Do not omit the subject (the reader will not know which function, class, or module acts).
- Do not omit articles (the, a, an); omitted articles cause ambiguity.
- Do not use contractions. Write "do not" not "don't", "is not" not "isn't",
  "are not" not "aren't", "cannot" not "can't", "will not" not "won't".

**Code examples**
- Subject: Non-STE: `Can be a maximum length of 256 characters.` → STE: `The input string can have a maximum length of 256 characters.`
- Verb: Non-STE: `The return value a boolean that indicates success.` → STE: `The return value is a boolean that indicates success.`
- Noun: Non-STE: `The function returns the parsed.` → STE: `The function returns the parsed configuration object.`
- Article: Non-STE: `` `validate` function checks input parameter. `` → STE: `The \`validate\` function checks the input parameter.`
- Contraction: Non-STE: `The method doesn't throw an exception when the input is null.` → STE: `The method does not throw an exception when the input is null.`
- Noun the verb acts on (parallel): Non-STE: `Remove the bolt and stop.` → STE: `Remove the bolt and the stop.`
- Conditional verb: Non-STE: `If installed, remove the shims.` → STE: `If shims are installed, remove them.`
- Safety subject: Non-STE: `BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. IF NOT, THIS CAN CAUSE DATA LOSS.` → STE: `BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. A MISSING BACKUP CAN CAUSE DATA LOSS.`

**Code example — do not omit the subject (Python docstring)**
```python
def validate_username(name: str) -> bool:
    """Check whether the user name is valid.

    The user name can have a maximum length of 256 characters.
    The user name must contain only letters, digits, and underscores.
    """
    return len(name) <= 256 and name.isidentifier()
```

**Code example — do not use a contraction (C# XML doc)**
```csharp
/// <summary>
/// Reads the next record from the stream.
/// </summary>
/// <remarks>
/// The method does not throw an exception when the input is null.
/// The method returns null when the end of the stream is reached.
/// </remarks>
public Record? ReadNext(Stream? input) { ... }
```

**Code example — contraction in a warning (README)**
```markdown
> **WARNING**
> If your hands are wet, do not touch the USB power adapter.
> The adapter supplies current that can cause injury.
> Keep the adapter away from water while it is connected.
```

**Paradigm guidance**
- Object-Oriented: method return descriptions often omit the subject — write "The method returns…"; constructor docs often omit the verb — write "The constructor creates…"; getter/setter comments often omit the article — write "The getter returns the value of the field."
- Functional (Haskell, Elixir, Clojure, F#): pattern-match docs often omit verbs — write each arm as a full sentence with a verb; type-variable descriptions often omit subjects — add "The type variable represents…"; monad-law notes often omit articles — write "The first law states that…"
- Procedural (C, Go, Bash, Rust): function synopses in headers often omit articles and subjects — write "The function reads a configuration file."; makefile/shell comments often omit the verb — write "The script removes the build directory."
- Declarative (SQL, Terraform, Kubernetes YAML, Ansible): comments and resource descriptions often omit verbs and articles — write each as a full sentence with subject and verb. For a SQL view: "The view returns the active users." For a Terraform block: "The resource creates a storage bucket."
- Systems (Rust unsafe, C memory): safety docs with omitted subjects cause real bugs. Always write subject, verb, and articles in full — e.g. "The caller must ensure that the pointer is valid."

**Edge cases**
- Commit message summary line: the 72-char limit makes full sentences hard; the summary may use a relaxed form, but the body must follow the rule strictly.
- CLI help text: terminal width causes omitted articles/subjects; long-form docs must use full sentences. CLI help may relax to `rm FILE`; the manual page must write "The command removes the file."
- Code token that is also a contraction: a token such as `won't` (test name), `can't` (variable), `it's` (map key) is a technical noun — keep it in backticks, do not expand. Write "The test `won't` checks the failure path," not "The test `will not` checks the failure path."
- Error messages and log lines: short error strings may omit articles; the docs that explain the error must use full sentences ("The error means that the connection is closed.").
- Tables and lists: a cell may hold a short phrase; the surrounding prose and the column header must supply the subject and verb. Write the header "The function returns the status code," not "Returns status."

**Grammar notes**
- Write "do not," "is not," "are not," "cannot," "will not," "does not," "did not" in full. No apostrophe contractions.
- Every sentence needs a subject, a verb, and the required articles (the, a, an).
- When you connect two nouns with "and," repeat the article if the two items are different physical or logical things: "Remove the bolt and the stop," not "Remove the bolt and stop."
- Prefer plain dictionary verbs: "check" not "verify," "make" not "create," "get" not "retrieve," "set" not "configure," "remove" not "delete" when the simpler word fits.

**Checklist**
- [ ] Every sentence has a subject, a verb, and the required articles.
- [ ] No words are omitted to make the sentence shorter.
- [ ] No contractions are used (write "do not," "is not," "are not," "cannot," "will not" in full).
- [ ] The reader knows which element performs the action.
- [ ] Parallel nouns joined by "and" each keep their article.
- [ ] Code tokens that look like contractions stay in backticks and are not expanded.

---

## Rule 4.3 — Use a Vertical List for Complex Text

**Requirement**
- When a sentence is long and lists many items (parameters, return fields, error
  codes, configuration options, environment variables, dependencies, test cases) or
  actions, put them in a vertical list.
- Put a colon (`:`) at the end of the introductory sentence, before the first item.
- Identify each item with a number, letter, dash, or bullet.
- Start each item with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of each item.
- Put a period at the end of an item if it is a full sentence (e.g. an imperative
  step like "Set the timeout value"). Do not put a period at the end of a non-sentence
  item (e.g. "The `timeout` parameter that controls the delay").
- Do not put a comma or semicolon at the end of an item.
- Put a period at the end of the last item.
- Use vertical lists in procedural and descriptive docs, but do not mix imperative
  instructions and descriptive statements in the same list.
- In safety instructions, include negative commands (DO NOT) where necessary for each item.
- Each item must connect clearly to the introductory text. Test by reading
  "Introductory text [item]" as one sentence.
- Do not nest a second vertical list inside the primary list. Use the same level for
  all items. If a sub-item needs its own list, start a new introductory sentence after
  the parent item, or use a table or a separate list under a new heading.
- An item can contain a verb and not be a full sentence; then it takes no period.

**Code examples**
- Non-STE: `The UserService constructor accepts the database URL, the cache backend, and the maximum retry count.`
- STE:
```
The `UserService` constructor accepts these parameters:
- The `database_url` for the PostgreSQL connection string.
- The `cache_backend` for session storage.
- The `max_retries` for transient failure handling.
```

**Code example — constructor parameters (Python docstring)**
```python
class UserService:
    """Manage application users and their sessions.

    The UserService constructor accepts these parameters:
    - The database_url for the PostgreSQL connection string.
    - The cache_backend for session storage.
    - The max_retries for transient failure handling.
    """

    def __init__(self, database_url, cache_backend, max_retries=3):
        self.database_url = database_url
        self.cache_backend = cache_backend
        self.max_retries = max_retries
```

**Code example — procedural steps (one type only)**
```
## Deploy the application

To deploy the application, do these steps:
- Set the `DATABASE_URL` environment variable.
- Run the `apply-migrations` command.
- Start the server on port 8080.

The server binds to port 8080 after startup.
```

**Code example — error codes (HTTP API)**
- Non-STE: `The API returns 400 for validation issues, 401 when the token is expired, 403 if permissions are not sufficient, and 404 when the resource is missing.`
- STE:
```
The API returns these error codes:
- `400 Bad Request` for a failed input validation.
- `401 Unauthorized` for an expired or missing token.
- `403 Forbidden` for insufficient permissions.
- `404 Not Found` for a missing resource.
```

**Code example — safety instruction (negative command per item)**
```
CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:
- DO NOT CHANGE THE SECRET KEY.
- DO NOT DISABLE THE AUDIT LOG.
```

**Code example — declarative config fields (YAML)**
```
# The config.yaml file has these top-level fields:
# - The server.port that sets the listen port.
# - The log.level that sets the log verbosity.
# - The database.pool_size that sets the maximum open connections.
# - The features that lists the enabled feature flags.
server:
  port: 8080
log:
  level: info
database:
  pool_size: 20
features:
  - new_checkout
  - dark_mode
```

**Code example — function return codes (Go)**
```go
// The openFile function returns these codes:
// - 0 for a successful open.
// - -1 for a missing path.
// - -2 for insufficient permission.
func openFile(path string) (int, error) {
    if _, err := os.Stat(path); errors.Is(err, os.ErrNotExist) {
        return -1, fmt.Errorf("the path %q is missing", path)
    }
    f, err := os.Open(path)
    if err != nil {
        return -2, fmt.Errorf("the user lacks permission for %q", path)
    }
    defer f.Close()
    return 0, nil
}
```

**Other list types covered by this rule**
- Data-transfer-object fields (object has these fields: `email`, `display_name`, `role`)
- Test cases (the function passes these test cases: accept `"10s"` and return 10 seconds; …)
- Dependencies in a package manifest (`express` for HTTP routing; `pg` for PostgreSQL; `redis` for cache)
- Environment variables (the worker reads these: `LOG_LEVEL`, `QUEUE_URL`, `MAX_WORKERS`)

**Paradigm guidance**
- Object-Oriented: use a vertical list for constructor parameters, public methods, DTO fields, and exceptions a method can send.
- Functional: use a vertical list to document each variant of a sum type or each pattern-match arm.
- Procedural (C, Go, Bash): use a vertical list for function return codes; one item per code and meaning.
- Declarative (SQL, Terraform, YAML): use a vertical list for top-level fields; a separate list for sub-fields of a complex field.
- Systems (Rust, C memory): use a vertical list for ownership or lifecycle rules; one item per constraint.

**Edge cases**
- Nested fields: do not put a second vertical list inside the primary list; describe sub-fields with a new introductory sentence after the parent item, or with a table.
- Generated documentation (JSDoc, Sphinx, rustdoc) may use tables — acceptable; apply Rule 4.3 to prose a human writes.
- Very short lists: a list of two or three items under ~5 words each may stay inline; use a vertical list when each item has more than five words or the inline sentence exceeds 25 words.
- Code blocks in items: put the code block after the item text, indented under the item; the item still starts with an uppercase letter.
- Mixed code and prose: keep the item sentence first (starting uppercase), then add the code block; do not start the item with a code fence.

**Grammar notes**
- Each item must complete the introductory sentence grammatically.
- Use "the" or "a/an" consistently across all items; put the article before the backticks when the item starts with a code identifier.
- A full sentence has a subject and a finite verb. An item with only a verb phrase (e.g. "Set the timeout value") is a full imperative sentence and gets a period. An item such as "The `timeout` parameter that controls the delay" is a relative clause and gets no period until the last item.

**Checklist**
- [ ] The introductory sentence ends with a colon.
- [ ] Each item starts with an uppercase letter.
- [ ] Each item connects to the introductory text.
- [ ] No period on non-sentence items; period on the last item.
- [ ] No mixed procedural and descriptive items in one list.
- [ ] No nested vertical lists.
- [ ] Each code sample (if any) comes after its item sentence.

---

## Rule 4.4 — Use Connecting Words and Connecting Phrases

**Requirement**
- Connecting words and phrases connect a topic in one sentence with an idea in the
  sentence that follows.
- In code documentation they give the writing a logical structure and make technical
  information easy to understand.
- Approved connecting words: "and," "but," "then," "thus."
- Approved connecting phrases: "as a result," "at the same time."
- Demonstrative adjectives (this, these) also connect ideas in related sentences; they
  refer back to a topic named in the previous sentence.
- In procedural docs, use connecting words when an explanation is necessary after a work
  step. In safety instructions, use them to connect related sentences and make the text clear.
- Starting a sentence with "and" or "but" is permitted and encouraged — it creates short,
  independent sentences with an explicit logical link.

**Code examples**
- "and" (two related descriptions):
  - Non-STE: `` `parseInput` validates the request payload and `formatOutput` serializes the response, and they're both called in the handler. ``
  - STE: `The \`parseInput\` function validates the request payload. And the \`formatOutput\` function serializes the response data.`
- "but" (exception or alternative):
  - Non-STE: `These error-handling rules are the minimum necessary for the API layer, although the local project conventions may specify additional ones.`
  - STE: `These error-handling rules are the minimum necessary for the API layer. But the local project conventions can give other necessary error-handling rules.`
- "thus" (logical consequence):
  - Non-STE: `If the validation step fails, the middleware sets an error code on the response object, so the downstream handler gets it and skips processing.`
  - STE: `If the validation step fails, the middleware sets an error code on the response object. Thus, the downstream handler receives the error code and skips the processing step.`
- "as a result" (cause and effect):
  - Non-STE: `When the cache eviction policy runs, expired entries are removed, which frees up capacity for new entries.`
  - STE: `When the cache eviction policy runs, expired entries are removed from the cache. As a result, the cache has free capacity for new entries.`
- "then" (time sequence in a procedure):
  - Non-STE: `Open the database connection, after that run the migration script, and finally start the API server.`
  - STE: `Open the database connection. Then run the migration script. And then start the API server.`
- Demonstrative adjective "this" in procedures:
  - Non-STE: `Tag the deprecated methods with the @deprecated annotation; it helps developers migrate to the new API.`
  - STE: `Tag the deprecated methods with the @deprecated annotation. This annotation will help developers during the migration to the new API.`
- Safety instruction:
  - Non-STE: `Always validate user input in this module because it prevents injection attacks.`
  - STE: `BREAKING: ALWAYS VALIDATE USER INPUT IN THIS MODULE. THIS PRECAUTION WILL PREVENT INJECTION ATTACKS.`
- Missing connection (STE makes the link explicit):
  - Non-STE: `POST /users creates a new user account and returns a 201 status. The response body contains the created user object with an auto-generated ID. The ID can be used in later requests to reference this user.`
  - STE: `A POST request to /users makes a new user account. As a result, the API returns a 201 status code. And the response body contains the created user object with an auto-generated ID. You can use this ID in later requests to refer to the user.`
- "at the same time" (concurrency):
  - Non-STE: `The worker fetches the page and parses it concurrently using asyncio tasks.`
  - STE: `The worker fetches the page from the remote server. At the same time, the parser reads the response stream. And both tasks finish before the timeout.`
- "but" in an error-message description:
  - Non-STE: `The read_file function returns the contents; however, it raises PermissionError when the path is not readable.`
  - STE: `The read_file function returns the contents of the file. But it raises a PermissionError when the path is not readable.`

**Paradigm guidance**
- Object-Oriented: describe class invariants in one sentence; use "thus" to connect them to public-API behavioral guarantees; use "this" to refer to a private field; use "and" to group related methods.
- Functional: describe the input type in one sentence; use "and" to connect happy path to error path; use "thus" to connect a transformation step to the output shape.
- Procedural (C, Go, Bash): describe the allocation step in one sentence; use "then" to introduce initialization; use "as a result" to connect processing to the final state.
- Declarative (SQL, Terraform, YAML): describe the resource spec in one sentence; use "thus" to connect the spec to the reconciliation outcome; use "this" to refer to a named resource.
- Systems (Rust, C memory): describe the ownership rule in one sentence; use "thus" to connect the rule to the compiler guarantee; use "but" to introduce an unsafe escape hatch.

**Edge cases**
- Connecting word that is also a framework name: e.g. the `Then` assertion library, the Rust `and_then` combinator. When the word is a code token in backticks, treat it as a technical noun; the sentence-initial connecting word is not in backticks.
- "Then" ambiguity: use "after" for time or "thus" for logic when ambiguous (do A, then do B = time; if A, then B = logic).
- Generated code comments: this rule applies to documentation you write, not auto-generated comments. Do not edit generated comments to add connecting words.
- Connecting across three or more sentences: limit connecting-word chains to two or three sentences; if more are needed, restructure into a list or a table.
- Connecting word at the start of a section: do not use a connecting word at the very start of a new section to link it to the previous section; the heading provides the connection. Restate the topic so the section stands alone.

**Grammar notes**
- Start a sentence with "and" or "but" to create short, independent sentences with an explicit logical link.
- "Thus" and "as a result" sit at the start of the second sentence; do not use a semicolon before "thus."
- "This" and "these" are demonstrative adjectives when they modify a noun ("this function," "these parameters"); prefer the adjective form with an explicit noun to remove ambiguity.
- When you connect two sentences with "and," keep the two sentences parallel in structure.

**Checklist**
- [ ] Each connecting word links a sentence to the one that follows.
- [ ] Only approved connecting words and phrases are used.
- [ ] Demonstrative adjectives refer back to a clearly introduced topic.
- [ ] No mixed procedural and descriptive modes inside one connected pair.
- [ ] Connecting-word chains do not exceed three sentences.

---

## Rule 4.5 — Use an Article or a Demonstrative Adjective Before a Noun

**Requirement**
- Articles ("the," "a," "an") and demonstrative adjectives ("this," "these") show the
  position of nouns in the sentence. Use them correctly; do not remove them to shorten text.
- Do not use an article in a general statement or before an abstract concept
  ("performance," "scalability," "error handling," "concurrency," "backward compatibility").
- In short sentences, use an article before each noun.
- In a long series of items, use the article only before the first noun in the series.
- When an adjective applies to only one item in a series, repeat the article before each
  item to avoid ambiguity.
- Do not use a definite article before a noun when a code identifier follows it — the
  identifier makes the noun phrase a proper noun (function, class, variable, file,
  environment variable, error code, version tag).
- Use a demonstrative adjective ("this," "these") to connect a noun to the topic of the
  previous sentence; always keep the noun after it — do not write "this" or "these" alone.

**Code examples**
- Article in a short instruction:
  - Non-STE: `Call callback function. Pass response object to handler and set retry flag.`
  - STE: `Call the callback function. Pass the response object to the handler. Then set the retry flag.`
- API reference sentence:
  - Non-STE: `Method reads configuration file and returns settings object.`
  - STE: `The \`load\` method reads the configuration file and returns the settings object.`
- No article in a general statement:
  - Non-STE: `The error handling is important for the production applications. A function throws the error when the input is not valid.`
  - STE: `Error handling is important for production applications. The function throws an error when the input is not valid.`
- Article only before the first noun in a long series:
  - Non-STE: `Delete temporary files, log files, cache entries, and lock files before you start the build.`
  - STE: `Delete the temporary files, log files, cache entries, and lock files before you start the build.`
- Article before each noun when an adjective applies to only one item:
  - Non-STE: `Register the new event listeners, timers, subscriptions, and cleanup callbacks.`
  - STE: `Register the new event listeners, the timers, the subscriptions, and the cleanup callbacks.` (Only the event listeners are new.)
- No article before a noun with a code identifier:
  - Non-STE: `Call the function \`validateInput\` before you send the request.` → STE: `Call function \`validateInput\` before you send the request.` (or `Call the \`validateInput\` function …`)
  - Non-STE: `Set the variable \`LOG_LEVEL\` to \`debug\`.` → STE: `Set variable \`LOG_LEVEL\` to \`debug\`.`
  - Non-STE: `Install the version 3.2.1 of the package.` → STE: `Install version 3.2.1 of the package.`
- Demonstrative adjective for sentence linking:
  - Non-STE: `The function returns a configuration object. Configuration object has three fields: host, port, and timeout.`
  - STE: `The function returns a configuration object. This object has three fields: \`host\`, \`port\`, and \`timeout\`.`
- Article in a commit message / release note:
  - Non-STE: `Fix race condition in scheduler; worker pool now waits for queue drain.`
  - STE: `Fix the race condition in the scheduler. The worker pool now waits for the queue to become empty.`
- Article in an error message / test description:
  - Non-STE: `Input not valid: field must be string.` → STE: `The input is not valid. The \`name\` field must be a string.`
  - Non-STE: `Test verifies handler returns 404 when record missing.` → STE: `The test checks that the handler returns the status code 404 when the record is not in the database.`

**Paradigm guidance**
- Object-Oriented (Java, C#, Python, TypeScript): use an article to separate a class (the type) from an instance (the value): "The `ConnectionPool` class manages a pool of database connections. Each instance keeps a list of open connections." No article directly before a bare identifier: "Call `connect`."
- Functional (Haskell, Elixir, F#, Scala): use an article to separate a type constructor from a value: "The `Ok(value)` pattern shows a successful result. A `Result` value is either `Ok` or `Err`." Write concepts ("immutability," "referential transparency") with no article.
- Procedural (C, Go, Bash): use an article to separate a pointer from the value at the address: "The function receives a pointer to a buffer. The buffer must hold at least 512 bytes."
- Declarative (SQL, Terraform, YAML, Kubernetes): use an article to separate a resource type from a resource instance: "A `Deployment` resource manages a set of pods. The `web` deployment runs three replicas." No article before a named resource: "Apply manifest `web-deployment.yaml`."
- Systems (Rust, C memory, embedded): use an article to make ownership and lifetime relationships clear: "The pointer must point to an initialized region of memory. A borrow of the value must not outlive the owner."

**Edge cases**
- Identifier as a proper noun compared with a concept: `ConnectionPool` alone is a proper noun (no article); "The `ConnectionPool` class" takes "the" because "class" is the noun. "Call `initialize`" takes no article; "The `initialize` function" takes "the" because "function" is the noun.
- "a" compared with "an": use "an" before a vowel sound (an SQL query, an HTML element, an XML parser, an ID, an API key); use "a" before a consonant sound (a URL, a Unix system, a UUID, a JSON payload, a `User` record). Match the usual pronunciation.
- Headings, titles, and table cells: may omit the article; the first sentence below the heading must obey the full rule.
- Product / framework names that start with "The" (e.g. `TheMovieDB`): treat as a proper noun; the leading "The" is part of the identifier, not an article.
- Plural types used as a general statement: "Iterators are lazy in this library" is general (no article); "The iterator stops at the end of the sequence" refers to one identifiable item (uses "the").
- Code samples and command lines: do not add an article inside a code block, command, or log line; this rule applies to prose only.
- Acronyms that expand to a different sound: choose the article for the spoken form (write "an API", not "a API").
- Uncountable technical nouns: "memory," "throughput," "latency," "state" take no indefinite article ("The function allocates memory", not "The function allocates a memory").

**Grammar notes**
- "A" refers to any instance of a type; "the" refers to one specific, identifiable item; no article refers to the type or concept as a whole.
- First mention uses "a" ("The method throws a `ValidationError`"); later mentions use "the" ("The `ValidationError` contains a message field").
- Proper-noun exception: a code identifier is a proper noun — do not put a definite article directly before it ("Call `connect`" correct; "Call the `connect`" not correct).
- Demonstrative adjectives keep their noun: write "this object" or "these headers"; do not write "this" or "these" alone as a pronoun.
- Multi-word nouns: put the article before the full multi-word noun ("the retry policy object", not "retry the policy object").
- Possessive forms replace the article ("its return value" and "the return value of the method" are both correct; do not write "the its return value").

**Checklist**
- [ ] Articles and demonstrative adjectives are used correctly and not removed to shorten text.
- [ ] No article appears before a general statement or an abstract concept.
- [ ] Short sentences use an article before each noun.
- [ ] A long series uses the article only before the first noun, unless an adjective applies to one item only.
- [ ] No definite article appears directly before a code identifier used as a proper noun.
- [ ] "a" and "an" match the spoken sound of the term that follows.
- [ ] Each demonstrative adjective is followed by a noun and refers to one clear topic.
