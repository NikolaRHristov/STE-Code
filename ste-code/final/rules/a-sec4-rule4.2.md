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
