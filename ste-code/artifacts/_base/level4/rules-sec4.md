<!-- a-sec4-rule4.1.md -->

# Rule 4.1 — One Topic Per Sentence, No Abstract Text

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.1
> **Source:** [master.md#sec4-rule4.1](ste-code/grouped/)
> Source: master.md#sec4-rule4.1

## Original Rule

In a descriptive text, make sure that each sentence has only one topic (subject or idea) and does not contain the imperative form. Then, in the sentences that follow, gradually give information about that topic.

### Example:

> **Non-STE:** The side stay assembly has two folding toggles hinged together and attached with hinges between the main gear strut and the side stay bracket. (This sentence contains more than one topic. To make this information clearer, you can write a new sentence for each topic.)

> **STE:** The side stay assembly has two folding toggles. The folding toggles are attached together with hinges. These folding toggles are also attached with hinges between the main gear strut and the side stay bracket. (The new text has three sentences, and each sentence has its topic. Refer to the underlined text for the specified subjects in each sentence.)

For the two types of writing, always make sure that your text is not abstract. Make sure that it clearly shows how to do a task or how a system operates. Be accurate. Do not give information that is not accurate or can have different meanings.

### Examples:

> **Non-STE:** Do not write: No leaks are permitted. (This sentence does not tell the reader about the action.)

> **STE:** WRITE: Make sure that there are no leaks. (This sentence directly tells the reader about the action.)

> **Non-STE:** Do not write: Different temperatures will change the cure time. (This is an abstract sentence because it contains no information about how the cure time changes.)

> **STE:** WRITE: When the temperature increases, the cure time will decrease. (This sentence tells the reader the correct information about how the cure time changes. To make your writing more accurate, give the specified temperatures and the related cure times.)

> **STE:** WRITE: The cure time is 2 hours at a temperature of 20 °C.

## STE-Code Adaptation

In a descriptive text (a class, module, or type description), make sure that each sentence has only one topic and does not contain the imperative form. Then, in the sentences that follow, gradually give information about that topic.

In a procedural text (an API method or function description), give one instruction per sentence in the imperative form.

For the two types of writing, always make sure that your text is not abstract. Make sure that it clearly shows how to use a function or how a module operates. Be accurate. Do not give information that is not accurate or can have different meanings.

### Code-Domain Examples

> *Adapted from spec pair:* Non-STE: The side stay assembly has two folding toggles hinged together and attached with hinges between the main gear strut and the side stay bracket.  |  STE: The side stay assembly has two folding toggles. The folding toggles are attached together with hinges. These folding toggles are also attached with hinges between the main gear strut and the side stay bracket.

**Descriptive writing (one topic per sentence):**

> **Non-STE:** The `HttpClient` class has two internal buffers connected together and linked with callbacks between the request handler and the response dispatcher.

> **STE:** The `HttpClient` class has two internal buffers. The internal buffers are connected together with callbacks. These callbacks link the request handler to the response dispatcher.

**Descriptive writing applied to a docstring (Java):**

```java
/**
 * Non-STE:
 * The ConnectionPool manages a set of reusable TCP connections that are
 * created lazily and validated on checkout and also reset before they are
 * returned to the pool so that the caller always gets a clean socket.
 */

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

**Avoid abstract statements (the "leaks" pair, recast for code):**

> *Adapted from spec pair:* Non-STE: No leaks are permitted.  |  STE: Make sure that there are no leaks.

> **Non-STE:** No null values are permitted.

> **STE:** Make sure that the function does not return a null value.

**Avoid abstract statements in a docstring (Python):**

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

**Show how the behavior changes instead of stating it abstractly (the "temperature" pair, recast for code):**

> *Adapted from spec pair:* Non-STE: Different temperatures will change the cure time.  |  STE: When the temperature increases, the cure time will decrease.  |  STE: The cure time is 2 hours at a temperature of 20 °C.

> **Non-STE:** Different payload sizes will change the parse time.

> **STE:** When the payload size increases, the parse time will increase.

> **STE:** The parse time is 2 milliseconds for a payload of 1 KB.

**Show measurable behavior in an API doc (Go):**

```go
// Non-STE:
// ParseMessage decodes the wire format. Larger inputs take longer.

// STE:
// ParseMessage decodes a message from the given byte slice.
// The function parses 1 KB of input in 2 milliseconds.
// When the input size doubles, the parse time increases by 1.8 milliseconds.
// The function returns ErrTooLarge if the input is larger than 4 MB.
func ParseMessage(buf []byte) (*Message, error)
```

**Procedural writing (one instruction per sentence, imperative):**

```python
# Non-STE:
# To send a request you'd probably want to build the client, set the timeout,
# and then call send() and check the response.

# STE:
# 1. Build the HttpClient with the default configuration.
# 2. Set the timeout to 30 seconds.
# 3. Call the send method with the request object.
# 4. Check the response status code.
# 5. Read the response body into a string.
def send_request(req: Request) -> str:
    ...
```

**Procedural writing for a CLI tool (Bash):**

```bash
# Non-STE:
# you can just run the deploy script after you export the token and pick the env

# STE:
# 1. Export the API token to the TOKEN variable.
# 2. Select the staging environment with the --env flag.
# 3. Run the deploy script.
# 4. Check the build log for the success message.
```

**Descriptive writing for a declarative resource (Terraform):**

```hcl
# Non-STE:
# resource "aws_s3_bucket" "logs" { bucket = "app-logs" # stores our logs, versioned, encrypted }

# STE:
# The aws_s3_bucket resource creates a storage bucket for application logs.
# The bucket name is "app-logs".
# The bucket keeps a version of each object that you overwrite.
# The bucket encrypts each object with the AES256 algorithm.
resource "aws_s3_bucket" "logs" {
  bucket = "app-logs"
}
```

### Paradigm-Specific Guidance

- **Object-Oriented (Java, C++, C#, Python):** Class documentation uses descriptive writing. Keep the class summary to one short sentence with one topic. Break method descriptions into numbered imperative steps.
- **Functional (Haskell, Elixir, Clojure, Rust):** Type signatures use descriptive writing. State one property per sentence. Effectful functions use procedural steps.
- **Procedural (C, Go, Bash):** Function documentation is a sequence of steps. Each step is one imperative sentence with one instruction.
- **Declarative (SQL, Terraform, Kubernetes YAML):** Resource documentation uses descriptive writing. Describe what the configuration does, one fact per sentence.
- **Systems (Rust ownership, C memory):** Describe invariants and ownership rules in descriptive sentences. Use imperative steps only for unsafe operations.

### Edge Cases

- **Generated documentation:** Generated output (from JSDoc, Sphinx, `go doc`) may combine sentences. Apply Rule 4.1 to the source docstrings and comments. Prefer to fix the source text, not the generated output.
- **Single-sentence module summary:** The first line of a module docstring may convey the purpose in one sentence. Expand the details in the body with one topic per sentence.
- **Safety callouts (BREAKING, DEPRECATED, NOTE):** Keep the callout to one short sentence. Put additional detail in the paragraph that follows.
- **Error messages:** Write the error text as one topic. State what failed and, when useful, tell the reader how to fix it in a second sentence. Do not write a vague abstract error such as "Invalid input occurred."
- **Commit messages:** Keep the subject line to one topic. Put each related change in its own bullet in the body. Do not combine two unrelated changes in one sentence.
- **README sections:** Write each paragraph around one idea. Use one sentence per listed feature. Do not pack several features into a single long sentence.

### Grammar Notes

- **Sentence length:** Use a maximum of 20 words for procedural sentences and 25 words for descriptive sentences. Code spans, inline code, and URLs do not count toward the word limit.
- **Imperative mood:** In procedural writing, start each step with an imperative verb (call, set, pass, check, start, send, remove, add, make, use, run, build, test, deploy). Do not use "you should" or "the user must." Microsoft and Google style guides make the same point: use the imperative mood for required actions and reserve "we recommend" for optional ones.
- **Clause nesting:** Do not nest clauses deeper than two levels. Break nested clauses into separate sentences.
- **Voice:** Prefer the active voice for both descriptive and procedural sentences. The subject of the sentence must perform the action. The active voice keeps each sentence to one clear topic.
- **Abstract text:** Do not write a sentence that states a property without showing the action or the measured result. Replace "performance may vary" with a sentence that gives the measured value and the condition.

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 1.3** — Use words only with their approved meanings.
- **Rule 4.2** — Do not omit words or use contractions.
- **Section 5 (Procedural Writing)** — Detailed guidance for step-by-step instructions.
- **Section 6 (Descriptive Writing)** — Detailed guidance for descriptions and explanations.

> **See also:** Rule 1.1 — Use approved words from the STE-Code dictionary.
> **See also:** Rule 1.3 — Use words only with their approved meanings.
> **See also:** Rule 4.2 — Do not omit words or use contractions.
> **See also:** Section 5 (Procedural Writing) — Detailed guidance for step-by-step instructions.
> **See also:** Section 6 (Descriptive Writing) — Detailed guidance for descriptions and explanations.

## Summary Checklist

Before you publish code documentation, check each sentence:

- [ ] The sentence has a maximum of 20 words (procedural) or 25 words (descriptive).
- [ ] The sentence has only one topic or one instruction.
- [ ] Procedural sentences use the imperative mood.
- [ ] Descriptive sentences do not use the imperative mood.
- [ ] The text is not abstract and shows how to use the code.
- [ ] Each descriptive sentence states one fact in the active voice.
- [ ] Each measurable claim gives the value and the condition.

---

<!-- a-sec4-rule4.2.md -->

# Rule 4.2 — Do Not Omit Words or Use Contractions

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.2
> **Source:** [master.md#sec4-rule4.2](ste-code/grouped/)
> Source: master.md#sec4-rule4.2

## Original Rule

Each sentence must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). If you do that, your sentence will be shorter, but it will not be easier to read. Write all the words in full.

Do not omit nouns to make short sentences. It will not be easy for the reader to understand the meaning of the sentence.

Do not omit verbs because the reader will not understand the action.

Do not omit the subject because the reader will not understand the action.

Do not omit articles to make the sentence shorter because omitted articles can cause ambiguity.

Do not omit parts of words to make contractions because contractions will not be easy to understand.

### Examples:

> **Non-STE:** Can be a maximum of five inches long.
>
> **STE:** Cracks can have a maximum length of five inches.

> **Non-STE:** Rotary switch to INPUT.
>
> **STE:** Set the rotary switch to INPUT.

> **Non-STE:** If installed, remove the shims.
>
> **STE:** If shims are installed, remove them.

> **Non-STE:** WARNING: MAKE SURE THAT THE POTABLE WATER SYSTEM IS NOT PRESSURIZED. IF NOT, THIS CAN CAUSE INJURY TO PERSONS.
>
> **STE:** WARNING: MAKE SURE THAT THE POTABLE WATER SYSTEM IS NOT PRESSURIZED. A PRESSURIZED SYSTEM CAN CAUSE INJURY TO PERSONS.

> **Non-STE:** Remove the bolt and stop.
>
> **STE:** Remove the bolt and the stop.

> **Non-STE:** If your hands are wet, don't touch the USB power adapter.
>
> **STE:** If your hands are wet, do not touch the USB power adapter.

## STE-Code Adaptation

Each sentence in code documentation must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). Write all words in full. A shorter sentence is not necessarily easier to read.

Do not omit nouns. If you omit a noun, the reader will not know which code element the sentence refers to.

Do not omit verbs. If you omit a verb, the reader will not understand the action that the code performs.

Do not omit the subject. If you omit the subject, the reader will not understand which function, class, or module performs the action.

Do not omit articles (the, a, an). If you omit an article, the sentence can become ambiguous about which code element is specified.

Do not use contractions. Write "do not" instead of "don't," "is not" instead of "isn't," and "are not" instead of "aren't."

### Code-Domain Examples

> *Adapted from spec pair:* Non-STE: Can be a maximum of five inches long.  |  STE: Cracks can have a maximum length of five inches.

**Do not omit the subject:**

> **Non-STE:** Can be a maximum length of 256 characters.
>
> **STE:** The input string can have a maximum length of 256 characters.

Full context — a Python docstring for a validation helper:

```python
def validate_username(name: str) -> bool:
    """Check whether the user name is valid.

    The user name can have a maximum length of 256 characters.
    The user name must contain only letters, digits, and underscores.
    """
    return len(name) <= 256 and name.isidentifier()
```

The subject `The user name` is present in every sentence, so the reader always knows which value the rule applies to.

**Do not omit the verb:**

> **Non-STE:** The return value a boolean that indicates success.
>
> **STE:** The return value is a boolean that indicates success.

Full context — a Java method comment:

```java
/**
 * Attempts to lock the resource for exclusive access.
 *
 * The return value is a boolean that indicates success.
 * The method returns true when the lock is acquired.
 * The method returns false when the lock is already held.
 */
public boolean tryLock() { ... }
```

Without the verb `is`, the first sentence reads as a fragment and the reader cannot tell whether it describes the return value or an instruction.

**Do not omit the noun:**

> **Non-STE:** The function returns the parsed.
>
> **STE:** The function returns the parsed configuration object.

Full context — a Go function:

```go
// LoadConfig reads the settings file and returns the parsed configuration object.
// The function returns the parsed configuration object.
// The function returns an error when the file is missing or malformed.
func LoadConfig(path string) (*Config, error) { ... }
```

Omitting the noun leaves `the parsed`, which refers to nothing the reader can identify.

**Do not omit articles:**

> **Non-STE:** `validate` function checks input parameter.
>
> **STE:** The `validate` function checks the input parameter.

Full context — a TypeScript signature with a descriptive comment:

```typescript
/**
 * The `validate` function checks the input parameter.
 * The `validate` function returns a boolean that reports the result.
 * A missing input parameter causes the function to return false.
 */
function validate(input: Request): boolean { ... }
```

The article `The` before `validate` and `the` before `input parameter` mark the specific element and the specific argument. Without them, the sentence could mean any `validate` function or any parameter.

**Do not use contractions:**

> **Non-STE:** The method doesn't throw an exception when the input is null.
>
> **STE:** The method does not throw an exception when the input is null.

Full context — a C# XML documentation comment:

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

Write `does not`, `is not`, `are not`, `cannot`, and `will not` in full. Do not use the apostrophe forms `doesn't`, `isn't`, `aren't`, `can't`, or `won't`.

**Do not omit the subject in a safety statement:**

> **Non-STE:** BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. IF NOT, THIS CAN CAUSE DATA LOSS.
>
> **STE:** BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP. A MISSING BACKUP CAN CAUSE DATA LOSS.

Full context — a Rust migration note in a changelog:

```markdown
## BREAKING CHANGES

BREAKING: MAKE SURE THAT THE DATABASE IS BACKED UP.
A MISSING BACKUP CAN CAUSE DATA LOSS.
The migration deletes the `sessions` table.
The migration runs automatically when you start version 3.0.
```

The second sentence gives the subject `A MISSING BACKUP` so the reader understands the exact cause of the data loss.

**Do not omit the noun that the verb acts on (parallel structure):**

> **Non-STE:** Remove the bolt and stop.
>
> **STE:** Remove the bolt and the stop.

Full context — a procedural step in a Bash script comment:

```bash
# To disassemble the unit, remove the bolt and the stop.
# The bolt holds the cover in place.
# The stop limits the travel of the actuator.
```

Without the second `the stop`, the reader may read `stop` as the verb "stop" rather than the noun "the stop" (a physical part). Repeating the article and noun keeps the meaning clear.

**Do not omit the verb in a conditional step:**

> **Non-STE:** If installed, remove the shims.
>
> **STE:** If shims are installed, remove them.

Full context — a Python setup instruction:

```python
# If shims are installed, remove them before you run the calibration.
# The calibration step reads the raw sensor values.
# The shims change the offset of the sensor.
```

The subject `shims` and the verb `are` make the condition explicit, so the reader knows when to act.

**Do not use a contraction in a warning:**

> **Non-STE:** If your hands are wet, don't touch the USB power adapter.
>
> **STE:** If your hands are wet, do not touch the USB power adapter.

Full context — a hardware interface warning in a README:

```markdown
> **WARNING**
> If your hands are wet, do not touch the USB power adapter.
> The adapter supplies current that can cause injury.
> Keep the adapter away from water while it is connected.
```

Write the warning in full words so that automated checkers and non-native readers parse it without ambiguity.

### Paradigm-Specific Guidance

- **Object-Oriented (Java, C#, C++, Python):** Method return descriptions often omit the subject. Write "The method returns…" Constructor documentation often omits the verb. Write "The constructor creates…" Getter and setter comments often omit the article. Write "The getter returns the value of the field."
- **Functional (Haskell, Elixir, Clojure, F#):** Pattern-match documentation often omits verbs. Write each arm as a full sentence with a verb. Type variable descriptions often omit subjects. Add a subject such as "The type variable represents…" Monad-law notes often omit articles. Write "The first law states that…"
- **Procedural (C, Go, Bash, Rust):** Function synopses in headers often omit articles and subjects. Write "The function reads a configuration file." Make-file and shell comments often omit the verb. Write "The script removes the build directory."
- **Declarative (SQL, Terraform, Kubernetes YAML, Ansible):** Comments and resource descriptions often omit verbs and articles. Write each comment as a full sentence with a subject and a verb. For a SQL view, write "The view returns the active users." For a Terraform block, write "The resource creates a storage bucket."
- **Systems (Rust unsafe code, C memory management):** Safety documentation with omitted subjects causes real bugs. Always write the subject, verb, and articles in full. For an unsafe block, write "The caller must ensure that the pointer is valid." Omitting the subject hides the party that owns the obligation.

### Edge Cases

- **Commit message summary line:** The 72-character limit makes full sentences hard. The summary line may use a relaxed form. The body must follow the rule strictly. Write the body as "The patch removes the unused import. The change does not alter the behavior of the function."
- **CLI help text:** Terminal width limits cause omitted articles and subjects. The long-form documentation must use full sentences. The CLI help text may use a relaxed form such as `rm FILE` or `get NAME`. The manual page must write "The command removes the file."
- **When a code token is also a contraction:** A token such as `won't` (a test name), `can't` (a variable), or `it's` (a key in a map) is a technical code noun. Keep it in backticks. Do not expand it. Write "The test `won't` checks the failure path." Do not write "The test `will not` checks the failure path," because that changes the identifier.
- **Error messages and log lines:** Short error strings may omit articles to save space on the wire. The documentation that explains the error must use full sentences. Write "The error means that the connection is closed."
- **Tables and lists:** A table cell may hold a short phrase. The surrounding prose and the column header must supply the subject and verb. Write the header "The function returns the status code" rather than "Returns status."

### Grammar Notes

- Write "do not," "is not," "are not," "cannot," "will not," "does not," "did not" in full. Do not use apostrophe contractions.
- Every sentence needs a subject, a verb, and the required articles (the, a, an).
- When you connect two nouns with "and," repeat the article if the two items are different physical or logical things. Write "Remove the bolt and the stop," not "Remove the bolt and stop."
- Prefer plain verbs from the STE-Code dictionary. Use "check" instead of "verify," "make" instead of "create," "get" instead of "retrieve," "set" instead of "configure," and "remove" instead of "delete" when the simpler word fits the meaning.

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 1.3** — Use words only with their approved meanings.
- **Rule 4.1** — Write one topic per sentence; do not write abstract text.
- **Rule 4.3** — Write the specified information in the specified order.
- **Rule 4.4** — Write procedural sentences in the imperative mood.
- **Rule 4.5** — Use an article or a demonstrative adjective before a noun.
- **Section 5 (Procedural Writing)** — Sentence structure for instructions.
- **Section 6 (Descriptive Writing)** — Sentence structure for descriptions.

> **See also:** Rule 4.1 — One topic per sentence, no abstract text
> **See also:** Rule 4.4 — Write procedural sentences in the imperative mood
> **See also:** Rule 4.5 — Use an article or a demonstrative adjective before a noun

## Summary Checklist

Before you publish code documentation, check each sentence:

- [ ] Every sentence has a subject, a verb, and the required articles.
- [ ] No words are omitted to make the sentence shorter.
- [ ] No contractions are used (write "do not," "is not," "are not," "cannot," "will not" in full).
- [ ] The reader knows which element performs the action.
- [ ] Parallel nouns joined by "and" each keep their article.
- [ ] Code tokens that look like contractions stay in backticks and are not expanded.

---

<!-- a-sec4-rule4.3.md -->

# Rule 4.3 — Use a Vertical List for Complex Text

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.3
> **Source:** [master.md#sec4-rule4.3](ste-code/grouped/)
> Source: master.md#sec4-rule4.3

## Original Rule

When your sentence is long and you must include many different items (for example, a list of components, parts, or documents) or actions, you can put them in a vertical list. Vertical lists make long and complex texts much easier to read and understand.

#### When you make a vertical list:

- Put a colon (:) at the end of the first sentence, before the first item in the vertical list.
- Identify each item in the vertical list with a number, letter, punctuation mark, or symbol. For example, you can use:
  - A dash (-)
  - A bullet point (•)
  - A letter (a, b, c…)
  - A number (1, 2, 3…).
- Start each item in the vertical list with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of each item in the vertical list.
- Put a period at the end of an item in the vertical list if it is a full sentence.
- Do not put a period at the end of an item in the vertical list if it is not a full sentence.
- Do not put a comma or a semicolon at the end of an item in the vertical list.
- Put a period at the end of the last item in the vertical list.

You can use vertical lists in procedural and descriptive writings, but you cannot mix the two types of writing in the same vertical list.

In safety instructions, include negative commands (DO NOT) where necessary for each item in the vertical list. This method will make the safety instruction more direct and easier to understand.

Always make sure that each item in the vertical list connects clearly and correctly to the first part of the vertical list (the text that is before the colon).

Always make sure that the layout of your vertical list is easy to read. In the example that follows, there is a second vertical list included in the primary vertical list. Use the same level for all items in the vertical list.

An item in a vertical list can contain a verb and not be a full sentence. Then, you do not use a period at the end of that item.

### Examples (from source):

> **Non-STE:** The wheel assembly comprises the tire, the tube, the spokes, the spoke fittings, the valve, and the hub.
>
> **STE:** The wheel assembly has these parts:
> - The tire
> - The tube
> - The spokes
> - The spoke fittings
> - The valve
> - The hub.

> **Non-STE:** The report must include each of the following: a completed REC-1 form, a three-view drawing of the unit, a photograph of the unit, a copy of the source data.
>
> **STE:** The report must include:
> - A completed REC-1 form
> - A three-view drawing of the unit
> - A photograph of the unit
> - A copy of the source data.

## STE-Code Adaptation

When a sentence in code documentation is long and must include many different items (for example, a list of parameters, return fields, error codes, configuration options, environment variables, dependencies, or test cases) or actions, put them in a vertical list. Vertical lists make complex documentation much easier to read and understand.

When you make a vertical list:

- Put a colon (:) at the end of the introductory sentence, before the first item.
- Identify each item with a number, letter, dash, or bullet.
- Start each item with an uppercase letter.
- Where applicable, use an article before the noun that is the subject of each item.
- Put a period at the end of an item if it is a full sentence (an imperative step such as "Set the timeout value" is a full sentence).
- Do not put a period at the end of an item if it is not a full sentence (for example, a noun phrase such as "The `timeout` parameter that controls the delay").
- Do not put a comma or a semicolon at the end of an item.
- Put a period at the end of the last item.

You can use vertical lists in procedural and descriptive documentation, but you cannot mix imperative instructions and descriptive statements in the same vertical list.

In safety instructions, include negative commands (DO NOT) where necessary for each item in the vertical list. This method makes the safety instruction more direct and easier to understand.

Always make sure that each item connects clearly and correctly to the introductory text (the text before the colon). Read "Introductory text [item]" as one sentence to test the connection.

Do not nest a second vertical list inside the primary vertical list. Use the same level for all items. If a sub-item needs its own list, start a new introductory sentence after the parent item, or describe the sub-fields with a table or a separate vertical list under a new heading.

An item can contain a verb and not be a full sentence. Then, do not use a period at the end of that item.

## Examples

> *Adapted from spec pair:* Non-STE: The wheel assembly comprises the tire, the tube, the spokes, the spoke fittings, the valve, and the hub.  |  STE: The wheel assembly has these parts: The tire, The tube, The spokes, The spoke fittings, The valve, The hub.
>
> *Adapted from spec pair:* Non-STE: The report must include each of the following: a completed REC-1 form, a three-view drawing of the unit, a photograph of the unit, a copy of the source data.  |  STE: The report must include: A completed REC-1 form, A three-view drawing of the unit, A photograph of the unit, A copy of the source data.

### Descriptive list of constructor parameters

> **Non-STE:** The `UserService` constructor accepts the database URL, the cache backend, and the maximum retry count.

> **STE:** The `UserService` constructor accepts these parameters:
> - The `database_url` for the PostgreSQL connection string.
> - The `cache_backend` for session storage.
> - The `max_retries` for transient failure handling.

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

### Procedural steps (one type only, no mixed items)

> **Non-STE:** To deploy the application: set the `DATABASE_URL` variable, the server binds to port 8080 after startup, run the migration command.

> **STE:** To deploy the application, do these steps:
> - Set the `DATABASE_URL` environment variable.
> - Run the `apply-migrations` command.
> - Start the server on port 8080.

````markdown
## Deploy the application

To deploy the application, do these steps:

- Set the `DATABASE_URL` environment variable.
- Run the `apply-migrations` command.
- Start the server on port 8080.

The server binds to port 8080 after startup.
````

### Error code reference for an HTTP API

> **Non-STE:** The API returns 400 for validation issues, 401 when the token is expired, 403 if permissions are not sufficient, and 404 when the resource is missing.

> **STE:** The API returns these error codes:
> - `400 Bad Request` for a failed input validation.
> - `401 Unauthorized` for an expired or missing token.
> - `403 Forbidden` for insufficient permissions.
> - `404 Not Found` for a missing resource.

```http
GET /api/v1/orders/8f2c HTTP/1.1
Authorization: Bearer <token>

HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "unauthorized",
  "message": "The token is expired. Get a new token and send the request again."
}
```

The API returns these error codes:
- `400 Bad Request` for a failed input validation.
- `401 Unauthorized` for an expired or missing token.
- `403 Forbidden` for insufficient permissions.
- `404 Not Found` for a missing resource.

### Safety instruction with a negative command on each item

> **Non-STE:** CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL, DO NOT CHANGE THE SECRET KEY. DO NOT DISABLE THE AUDIT LOG.

> **STE:** CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:
> - DO NOT CHANGE THE SECRET KEY.
> - DO NOT DISABLE THE AUDIT LOG.

```text
CAUTION: WHEN YOU ACCESS THE CONFIGURATION THROUGH THE ADMIN PANEL:

- DO NOT CHANGE THE SECRET KEY.
- DO NOT DISABLE THE AUDIT LOG.
```

### Declarative configuration options (YAML)

> **Non-STE:** The service reads a YAML file with the server port, the log level, the database pool size, and the feature flags.

> **STE:** The `config.yaml` file has these top-level fields:
> - The `server.port` that sets the listen port.
> - The `log.level` that sets the log verbosity.
> - The `database.pool_size` that sets the maximum open connections.
> - The `features` that lists the enabled feature flags.

```yaml
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

### Data-transfer-object fields

> **Non-STE:** The `CreateUserRequest` DTO has the email, the display name, and the role.

> **STE:** The `CreateUserRequest` object has these fields:
> - The `email` that gives the user login.
> - The `display_name` that gives the name that shows in the UI.
> - The `role` that gives the access level.

```json
{
  "email": "ada@example.com",
  "display_name": "Ada Lovelace",
  "role": "editor"
}
```

### Function return codes (procedural, Go)

> **Non-STE:** The `openFile` function returns 0 on success, -1 if the path is missing, and -2 if the user lacks permission.

> **STE:** The `openFile` function returns these codes:
> - `0` for a successful open.
> - `-1` for a missing path.
> - `-2` for insufficient permission.

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

### Test cases for a unit test

> **Non-STE:** The `parse_interval` function must accept "10s" and return 10 seconds, accept "0" and return an error, and accept "abc" and return an error.

> **STE:** The `parse_interval` function passes these test cases:
> - Accept `"10s"` and return 10 seconds.
> - Accept `"0"` and return an error.
> - Accept `"abc"` and return an error.

```python
def test_parse_interval():
    # The parse_interval function passes these test cases:
    # - Accept "10s" and return 10 seconds.
    # - Accept "0" and return an error.
    # - Accept "abc" and return an error.
    assert parse_interval("10s") == 10
    with pytest.raises(ValueError):
        parse_interval("0")
    with pytest.raises(ValueError):
        parse_interval("abc")
```

### Dependencies in a package manifest

> **Non-STE:** This project needs express for routing, pg for the database, and redis for caching.

> **STE:** The project uses these dependencies:
> - `express` for HTTP routing.
> - `pg` for the PostgreSQL database.
> - `redis` for cache storage.

```json
{
  "dependencies": {
    "express": "^4.19.2",
    "pg": "^8.11.3",
    "redis": "^4.6.10"
  }
}
```

The project uses these dependencies:
- `express` for HTTP routing.
- `pg` for the PostgreSQL database.
- `redis` for cache storage.

### Environment variables

> **Non-STE:** The worker reads LOG_LEVEL, QUEUE_URL, and MAX_WORKERS from the environment.

> **STE:** The worker reads these environment variables:
> - The `LOG_LEVEL` that sets the log verbosity.
> - The `QUEUE_URL` that sets the message queue address.
> - The `MAX_WORKERS` that sets the maximum concurrent tasks.

```bash
# The worker reads these environment variables:
# - The LOG_LEVEL that sets the log verbosity.
# - The QUEUE_URL that sets the message queue address.
# - The MAX_WORKERS that sets the maximum concurrent tasks.
export LOG_LEVEL=info
export QUEUE_URL=amqp://broker:5672/tasks
export MAX_WORKERS=8
```

## Paradigm-Specific Guidance

- **Object-Oriented:** Use a vertical list for constructor parameters, public methods, data-transfer-object fields, and exceptions that a method can send.
- **Functional:** Use a vertical list to document each variant of a sum type or each pattern-match arm.
- **Procedural (C, Go, Bash):** Use a vertical list for function return codes. Each item gives one code and its meaning.
- **Declarative (SQL, Terraform, YAML):** Use a vertical list for top-level fields. Use a separate list for the sub-fields of a complex field.
- **Systems (Rust, C memory):** Use a vertical list for ownership or lifecycle rules. Each item gives one constraint.

## Edge Cases

- **Nested fields:** Do not put a second vertical list inside the primary list. Describe the sub-fields with a new introductory sentence after the parent item, or with a table.
- **Generated documentation:** Generated API docs (JSDoc, Sphinx, rustdoc) may use tables. That is acceptable. Apply Rule 4.3 to prose that a human writes.
- **Very short lists:** A list of two or three very short items may stay inline. Use a vertical list when each item has more than five words or the inline sentence exceeds 25 words.
- **Code blocks in items:** Put the code block after the item text, indented under the item. The item still starts with an uppercase letter.
- **Mixed code and prose:** When an item needs a code sample, keep the item sentence first (starting with an uppercase letter), then add the code block. Do not start the item with a code fence.

## Grammar Notes

- Each item must complete the introductory sentence grammatically. Test by reading "Introductory text [item]" as one sentence.
- Use "the" or "a/an" consistently across all items. Put the article before the backticks when the item starts with a code identifier.
- A full sentence has a subject and a finite verb. An item with only a verb phrase (for example, "Set the timeout value") is a full imperative sentence and gets a period. An item such as "The `timeout` parameter that controls the delay" is a relative clause and gets no period until the last item.

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 1.6** — Non-approved words are permitted only as technical code nouns.
- **Rule 4.1** — Use short sentences. A vertical list helps you obey the length limit.
- **Rule 4.2** — Use one sentence per instruction in procedures.
- **Rule 5.1** — Use the active voice in procedural steps.

> **See also:** Rule 1.1 — Use approved words from the STE-Code dictionary.
> **See also:** Rule 1.6 — Non-approved words are permitted only as technical code nouns.
> **See also:** Rule 4.1 — Use short sentences.
> **See also:** Rule 4.2 — Use one sentence per instruction in procedures.
> **See also:** Rule 5.1 — Use the active voice in procedural steps.

## Summary Checklist

- [ ] The introductory sentence ends with a colon.
- [ ] Each item starts with an uppercase letter.
- [ ] Each item connects to the introductory text.
- [ ] No period on non-sentence items; period on the last item.
- [ ] No mixed procedural and descriptive items in one list.
- [ ] No nested vertical lists.
- [ ] Each code sample (if any) comes after its item sentence.

---

<!-- a-sec4-rule4.4.md -->

# Rule 4.4 — Use Connecting Words and Connecting Phrases

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.4
> **Source:** [master.md#sec4-rule4.4](ste-code/grouped/)
> **Domain:** code documentation (API docs, commit messages, README sections, code comments)

## Original Rule

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows.

In a descriptive text, connecting words and connecting phrases give your writing a logical structure and give information that is easy to understand.

Some of the connecting words that are approved in the dictionary are "and," "but," "then," and "thus."

"As a result" and "at the same time" are examples of connecting phrases that you can use.

You can also use demonstrative adjectives as connecting words to connect ideas in related sentences.

In procedures, you can use these connecting words when an explanation is necessary after a work step. Connecting words can also be necessary in safety instructions to connect related sentences or make the text clear.

### Examples (from source):

> **STE:** The localizer course aligns with the centerline of the runway. And the glideslope path is at a constant angle to the threshold of the runway.
>
> **STE:** These safety precautions are the minimum necessary for work in the pit lane. But the local regulations can give other necessary safety precautions.
>
> **STE:** If the pressure increases, it changes the electrical currents in the transmitter. Thus, the power unit supplies currents to the indicator on the related panel.
>
> **STE:** When the hydraulic pressure is released, the sequence valve moves to the open position. As a result, the actuators are connected to the hydraulic return.

## STE-Code Adaptation

Connecting words and connecting phrases connect a topic in one sentence with an idea in a sentence that follows. In code documentation, they give your writing a logical structure and make technical information easy to understand.

Use approved connecting words such as "and," "but," "then," and "thus."

Use connecting phrases such as "as a result" and "at the same time."

You can also use demonstrative adjectives (this, these) as connecting words to connect ideas in related sentences. They refer back to a topic introduced in the previous sentence.

In procedural documentation (function and method descriptions), use connecting words when an explanation is necessary after a work step. In safety instructions, use connecting words to connect related sentences and make the text clear.

### Code-Domain Examples

> *Adapted from spec pair:* Non-STE: "The localizer course aligns with the centerline of the runway. The glideslope path is at a constant angle to the threshold of the runway." (two related facts joined only by context)  |  STE: "The localizer course aligns with the centerline of the runway. And the glideslope path is at a constant angle to the threshold of the runway."

**Using "and" to connect two related descriptions:**

The two sentences stay independent. Each sentence has one topic. The connecting word makes the link explicit.

> **Non-STE:** `parseInput` validates the request payload and `formatOutput` serializes the response, and they're both called in the handler.
>
> **STE:** The `parseInput` function validates the request payload. And the `formatOutput` function serializes the response data.

**Using "but" to show an exception or alternative:**

Use "but" when the second sentence corrects, limits, or extends the first.

> **Non-STE:** These error-handling rules are the minimum necessary for the API layer, although the local project conventions may specify additional ones.
>
> **STE:** These error-handling rules are the minimum necessary for the API layer. But the local project conventions can give other necessary error-handling rules.

**Using "thus" to show a logical consequence:**

Use "thus" when the second sentence is a direct result of the first.

> **Non-STE:** If the validation step fails, the middleware sets an error code on the response object, so the downstream handler gets it and skips processing.
>
> **STE:** If the validation step fails, the middleware sets an error code on the response object. Thus, the downstream handler receives the error code and skips the processing step.

**Using "as a result" to show cause and effect:**

Use "as a result" for a clear physical or state change caused by the first sentence.

> **Non-STE:** When the cache eviction policy runs, expired entries are removed, which frees up capacity for new entries.
>
> **STE:** When the cache eviction policy runs, expired entries are removed from the cache. As a result, the cache has free capacity for new entries.

**Using "then" to show a time sequence in a procedure:**

Use "then" for an ordered work step, not for logical consequence.

> **Non-STE:** Open the database connection, after that run the migration script, and finally start the API server.
>
> **STE:** Open the database connection. Then run the migration script. And then start the API server.

**Using demonstrative adjectives as connecting words in procedures:**

The demonstrative adjective must point back to a topic that the previous sentence already named.

> **Non-STE:** Tag the deprecated methods with the `@deprecated` annotation; it helps developers migrate to the new API.
>
> **STE:** Tag the deprecated methods with the `@deprecated` annotation. This annotation will help developers during the migration to the new API.

**Connecting words in a safety instruction:**

Safety instructions use the imperative form. The connecting word still links the precaution to its reason.

> **Non-STE:** Always validate user input in this module because it prevents injection attacks.
>
> **STE:** BREAKING: ALWAYS VALIDATE USER INPUT IN THIS MODULE. THIS PRECAUTION WILL PREVENT INJECTION ATTACKS.

**Non-STE versus STE (missing connection):**

When you omit the connecting word, the reader must guess the link. STE makes the link explicit.

> **Non-STE:** POST /users creates a new user account and returns a 201 status. The response body contains the created user object with an auto-generated ID. The ID can be used in later requests to reference this user.
>
> **STE:** A POST request to `/users` makes a new user account. As a result, the API returns a 201 status code. And the response body contains the created user object with an auto-generated ID. You can use this ID in later requests to refer to the user.

**Using "as a result" in a configuration description:**

> **Non-STE:** When you set `max_connections` to 64, the pool reuses sockets and latency drops under load.
>
> **STE:** Set the `max_connections` value to 64 in the config file. As a result, the connection pool reuses idle sockets. And the average request latency decreases under load.

**Using "thus" in a test description:**

> **Non-STE:** The test seeds a row, calls the delete endpoint, and the row is gone from the database afterward.
>
> **STE:** The test seeds one row in the database. Thus, the delete endpoint removes that row. And the database has zero rows after the call.

**Using "at the same time" to show concurrency:**

> **Non-STE:** The worker fetches the page and parses it concurrently using asyncio tasks.
>
> **STE:** The worker fetches the page from the remote server. At the same time, the parser reads the response stream. And both tasks finish before the timeout.

**Using "but" in an error-message description:**

> **Non-STE:** The `read_file` function returns the contents; however, it raises `PermissionError` when the path is not readable.
>
> **STE:** The `read_file` function returns the contents of the file. But it raises a `PermissionError` when the path is not readable.

### Paradigm-Specific Guidance

- **Object-Oriented:** Describe the class invariants in one sentence. Use "thus" to connect them to the behavioral guarantees of the public API. Use "this" to refer back to a private field. Use "and" to group related methods.
- **Functional:** Describe the input type in one sentence. Use "and" to connect the happy path to the error path. Use "thus" to connect a transformation step to the shape of the output.
- **Procedural (C, Go, Bash):** Describe the allocation step in one sentence. Use "then" to introduce initialization. Use "as a result" to connect processing to the final state.
- **Declarative (SQL, Terraform, YAML):** Describe the resource spec in one sentence. Use "thus" to connect the spec to the reconciliation outcome. Use "this" to refer back to a named resource.
- **Systems (Rust, C memory):** Describe the ownership rule in one sentence. Use "thus" to connect the rule to the compiler guarantee. Use "but" to introduce an unsafe escape hatch.

### Edge Cases

- **Connecting word that is also a framework name:** Some frameworks use names that overlap with connecting words (for example, the `Then` assertion library, the Rust `and_then` combinator). When the word is a code token in backticks, treat it as a technical noun. The sentence-initial connecting word is not in backticks.
- **"Then" ambiguity:** "Then" can mean time sequence ("do A, then do B") or logical consequence ("if A, then B"). When ambiguous, use "after" for time or "thus" for logic.
- **Generated code comments:** This rule applies to documentation you write, not to auto-generated comments. Do not edit generated comments to add connecting words.
- **Connecting across three or more sentences:** Limit connecting-word chains to two or three sentences. If more are needed, restructure into a list or a table.
- **Connecting word at the start of a section:** Do not use a connecting word at the very start of a new section to link it to the previous section. The heading provides the structural connection. Restate the topic so the section stands alone.

### Grammar Notes

- Starting a sentence with "and" or "but" is permitted and encouraged. It creates short, independent sentences with an explicit logical link.
- "Thus" and "as a result" sit at the start of the second sentence. Do not use a semicolon before "thus."
- "This" and "these" are demonstrative adjectives when they modify a noun ("this function," "these parameters"). Prefer the adjective form with an explicit noun to remove ambiguity.
- When you connect two sentences with "and," keep the two sentences parallel in structure.

## Cross-References

- **Rule 1.1** — The connecting words and phrases must come from the approved dictionary.
- **Rule 1.3** — Use each connecting word only with its approved meaning.
- **Rule 1.11** — Use one term per concept. Use "thus" or "as a result" consistently, not both, for the same link.
- **Rule 3.1** — Connecting words join simple sentences. Simplify a complex sentence before you connect it.
- **Rule 4.1** — Each sentence before and after the connecting word must obey the length limit.

> **See also:** Rule 1.1 — Approved Words Come from the Dictionary
> **See also:** Rule 1.3 — Use Approved Words with the Approved Meaning
> **See also:** Rule 1.11 — Use One Term per Concept
> **See also:** Rule 3.1 — Write One Topic per Sentence
> **See also:** Rule 4.1 — Write Sentences That Are Not Too Long

## Summary Checklist

- [ ] Each connecting word links a sentence to the one that follows.
- [ ] Only approved connecting words and phrases are used.
- [ ] Demonstrative adjectives refer back to a clearly introduced topic.
- [ ] No mixed procedural and descriptive modes inside one connected pair.
- [ ] Connecting-word chains do not exceed three sentences.

---

<!-- a-sec4-rule4.5.md -->

# Rule 4.5 — Use an Article or a Demonstrative Adjective Before a Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.5
> **Source:** [master.md#sec4-rule4.5](ste-code/grouped/)
> **Domain:** code documentation (API docs, commit messages, README sections, code comments)

## Original Rule

Articles and demonstrative adjectives show the position of nouns and multi-word nouns in the sentence. Use articles and demonstrative adjectives correctly and do not omit them to make the text shorter.

It is not always correct English to put an article before a noun. Do not use articles in general statements or concepts.

In short sentences, it can be clearer to use articles before all nouns.

But sentences that contain a long series of items are clearer when you use the article only before the first noun in the series.

When you use the article in a series of items, always make sure that adjectives do not cause ambiguity.

A definite article is incorrect before a noun when an alphanumeric identifier comes after it. This is because the alphanumeric identifier shows that it is a proper noun.

### Examples (from source):

> **Non-STE:** Turn shaft assembly.
>
> **STE:** Turn the shaft assembly.
>
> **Non-STE:** Data module tells you how to operate unit.
>
> **STE:** This data module tells you how to operate the unit.
>
> **STE:** Install the nuts (2) and the bolts (3).
>
> **STE:** Discard the O-rings (3), gaskets (4), seals (7), and washers (9).
>
> **STE:** Install the new O-rings (15), spacers (14), nut (13), and safety pin (12).
>
> **Incorrect:** Tag the circuit breaker 36L7
>
> **Correct:** Tag circuit breaker 36L7.

## STE-Code Adaptation

Articles ("the," "a," "an") and demonstrative adjectives ("this," "these") show the position of nouns and multi-word nouns in code documentation. Use them correctly. Do not remove them to make the text shorter.

Do not use an article in a general statement or before an abstract concept ("performance," "scalability," "error handling," "concurrency," "backward compatibility").

In short sentences, use an article before each noun. This makes the text clear for readers and for machine translation.

In a sentence that contains a long series of items, use the article only before the first noun in the series. This keeps the text short and clear.

When you use an article in a series of items, make sure that an adjective does not cause ambiguity. If an adjective applies only to the first item, repeat the article before each item.

Do not use a definite article before a noun when a code identifier comes after it. The identifier is a proper noun. A function name, a class name, a variable name, a file name, an environment variable, an error code, and a version tag are all proper nouns in code documentation.

Use a demonstrative adjective ("this," "these") to connect a noun to the topic of the sentence before it. Always keep the noun after the demonstrative adjective. Do not write "this" or "these" alone.

### Code-Domain Examples

> *Adapted from spec pair:* Non-STE: "Turn shaft assembly." | STE: "Turn the shaft assembly." — In the code domain, this becomes: Non-STE: "Call callback function." | STE: "Call the callback function."

**Article before a noun in a short instruction:**

Each noun in a short imperative sentence takes an article. Do not remove the article to shorten the step.

> **Non-STE:** Call callback function. Pass response object to handler and set retry flag.
>
> **STE:** Call the callback function. Pass the response object to the handler. Then set the retry flag.

**Article in an API reference sentence:**

> **Non-STE:** Method reads configuration file and returns settings object.
>
> **STE:** The `load` method reads the configuration file and returns the settings object.

**No article in a general statement:**

An abstract concept takes no article. A specific, identifiable item takes "the."

> **Non-STE:** The error handling is important for the production applications. A function throws the error when the input is not valid.
>
> **STE:** Error handling is important for production applications. The function throws an error when the input is not valid.

> **Non-STE:** The backward compatibility is a requirement for the public API.
>
> **STE:** Backward compatibility is a requirement for the public API. The `v2` endpoints keep the response shape of the `v1` endpoints.

**Article only before the first noun in a long series:**

When the same article applies to all items, write it one time before the first item.

> **Non-STE:** Delete temporary files, log files, cache entries, and lock files before you start the build.
>
> **STE:** Delete the temporary files, log files, cache entries, and lock files before you start the build.

> **Non-STE:** Close database connection, file handle, socket, and worker pool in the shutdown hook.
>
> **STE:** Close the database connection, file handle, socket, and worker pool in the shutdown hook.

**Article before each noun when an adjective applies to only one item:**

Repeat the article when a shared article would make the adjective ambiguous.

> **Non-STE:** Register the new event listeners, timers, subscriptions, and cleanup callbacks.
>
> **STE:** Register the new event listeners, the timers, the subscriptions, and the cleanup callbacks. (Only the event listeners are new.)

> **Non-STE:** The release includes the deprecated helper functions, adapters, and CLI flags.
>
> **STE:** The release includes the deprecated helper functions, the adapters, and the CLI flags. (Only the helper functions are deprecated.)

**No article before a noun with a code identifier:**

The identifier makes the noun phrase a proper noun. Remove the definite article, or move it to the common noun that follows the identifier.

> **Non-STE:** Call the function `validateInput` before you send the request.
>
> **STE:** Call function `validateInput` before you send the request.
>
> **STE (alternative):** Call the `validateInput` function before you send the request.

> **Non-STE:** Configure the module `AuthService` in the container.
>
> **STE:** Configure module `AuthService` in the container.

> **Non-STE:** Set the variable `LOG_LEVEL` to `debug`.
>
> **STE:** Set variable `LOG_LEVEL` to `debug`.

> **Non-STE:** The error `ERR_TIMEOUT_1042` shows in the console log.
>
> **STE:** Error `ERR_TIMEOUT_1042` shows in the console log.

> **Non-STE:** Install the version 3.2.1 of the package.
>
> **STE:** Install version 3.2.1 of the package.

**Demonstrative adjective for sentence linking:**

> **Non-STE:** The function returns a configuration object. Configuration object has three fields: host, port, and timeout.
>
> **STE:** The function returns a configuration object. This object has three fields: `host`, `port`, and `timeout`.

> **Non-STE:** The middleware writes two headers to the response. They are used by the cache layer.
>
> **STE:** The middleware writes two headers to the response. These headers control the behavior of the cache layer.

**Article use in a commit message and a release note:**

> **Non-STE:** Fix race condition in scheduler; worker pool now waits for queue drain.
>
> **STE:** Fix the race condition in the scheduler. The worker pool now waits for the queue to become empty.

> **Non-STE:** Adds retry logic to the `HttpClient` and removes the deprecated method `sendSync`.
>
> **STE:** Adds retry logic to the `HttpClient` class. Removes deprecated method `sendSync`.

**Article use in an error message and a test description:**

> **Non-STE:** Input not valid: field must be string.
>
> **STE:** The input is not valid. The `name` field must be a string.

> **Non-STE:** Test verifies handler returns 404 when record missing.
>
> **STE:** The test checks that the handler returns the status code 404 when the record is not in the database.

### Paradigm-Specific Guidance

- **Object-Oriented (Java, C#, Python, TypeScript):** Use an article to separate a class (the type) from an instance (the value). "The `ConnectionPool` class manages a pool of database connections. Each instance keeps a list of open connections." Use no article directly before a bare identifier: "Call `connect`."
- **Functional (Haskell, Elixir, F#, Scala):** Use an article to separate a type constructor from a value. "The `Ok(value)` pattern shows a successful result. A `Result` value is either `Ok` or `Err`." Write concepts such as "immutability" and "referential transparency" with no article.
- **Procedural (C, Go, Bash):** Use an article to separate a pointer from the value at the address. "The function receives a pointer to a buffer. The buffer must hold at least 512 bytes."
- **Declarative (SQL, Terraform, YAML, Kubernetes):** Use an article to separate a resource type from a resource instance. "A `Deployment` resource manages a set of pods. The `web` deployment runs three replicas." Write no article before a named resource: "Apply manifest `web-deployment.yaml`."
- **Systems (Rust, C memory, embedded):** Use an article to make ownership and lifetime relationships clear. "The pointer must point to an initialized region of memory. A borrow of the value must not outlive the owner."

### Edge Cases

- **Identifier as a proper noun compared with a concept:** `ConnectionPool` alone is a proper noun and takes no article. "The `ConnectionPool` class" takes "the" because "class" is the noun. "Call `initialize`" takes no article. "The `initialize` function" takes "the" because "function" is the noun.
- **"a" compared with "an":** Use "an" before a vowel sound (an SQL query, an HTML element, an XML parser, an ID, an API key). Use "a" before a consonant sound (a URL, a Unix system, a UUID, a JSON payload, a `User` record). Choose the form that matches the usual pronunciation of the term.
- **Headings, titles, and table cells:** A heading, a table cell, and a UI label can omit the article. The first sentence below the heading must obey the full rule.
- **Product and framework names that start with "The":** Treat a name such as `TheMovieDB` as a proper noun. The leading "The" is part of the identifier and is not an article.
- **Plural types used as a general statement:** "Iterators are lazy in this library" is a general statement and takes no article. "The iterator stops at the end of the sequence" refers to one identifiable item and takes "the."
- **Code samples and command lines:** Do not add an article inside a code block, a command, or a log line. This rule applies to the prose only.
- **Acronyms that expand to a different sound:** Choose the article for the spoken form of the acronym, not for the expanded words. Write "an API" (spoken "ay-pee-eye"), not "a API."
- **Uncountable technical nouns:** "memory," "throughput," "latency," and "state" take no indefinite article. Write "The function allocates memory," not "The function allocates a memory."

### Grammar Notes

- **Definite compared with indefinite:** "A" refers to any instance of a type. "The" refers to one specific, identifiable item. No article refers to the type or the concept as a whole.
- **First mention compared with later mention:** Use "a" for the first mention ("The method throws a `ValidationError`"). Use "the" for each later mention ("The `ValidationError` contains a message field").
- **Proper noun exception:** A code identifier is a proper noun. Do not put a definite article directly before it. "Call `connect`" is correct. "Call the `connect`" is not correct.
- **Demonstrative adjectives keep their noun:** Write "this object" or "these headers." Do not write "this" or "these" alone as a pronoun, because the reference becomes ambiguous.
- **Multi-word nouns:** Put the article before the full multi-word noun, not inside it. Write "the retry policy object," not "retry the policy object."
- **Possessive forms replace the article:** "its return value" and "the return value of the method" are both correct. Do not write "the its return value."

## Cross-References

- **Rule 1.1** — Each noun and each adjective in the sentence must come from the approved dictionary.
- **Rule 1.5** — A technical noun from an approved category still takes an article in prose.
- **Rule 1.11** — Use one term per concept, so the definite article always refers to the same item.
- **Rule 3.1** — Write one topic per sentence, so that "the" and "this" have one clear referent.
- **Rule 4.1** — Keep sentences short. Do not remove an article to satisfy the length limit.
- **Rule 4.4** — A demonstrative adjective can also work as a connecting word between sentences.

> **See also:** Rule 1.1 — Approved Words Come from the Dictionary
> **See also:** Rule 1.5 — Use Technical Nouns from an Approved Category
> **See also:** Rule 1.11 — Use One Term per Concept
> **See also:** Rule 3.1 — Write One Topic per Sentence
> **See also:** Rule 4.1 — Write Sentences That Are Not Too Long
> **See also:** Rule 4.4 — Use Connecting Words and Connecting Phrases

## Summary Checklist

- [ ] Articles and demonstrative adjectives are used correctly and are not removed to shorten the text.
- [ ] No article appears before a general statement or an abstract concept.
- [ ] Short sentences use an article before each noun.
- [ ] A long series uses the article only before the first noun, unless an adjective applies to one item only.
- [ ] No definite article appears directly before a code identifier used as a proper noun.
- [ ] "a" and "an" match the spoken sound of the term that follows.
- [ ] Each demonstrative adjective is followed by a noun and refers to one clear topic.
