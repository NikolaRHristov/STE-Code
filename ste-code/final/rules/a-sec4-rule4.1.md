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
