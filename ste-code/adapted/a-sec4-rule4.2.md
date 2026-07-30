# Rule 4.2 — Do Not Omit Words or Use Contractions to Make Your Sentences Shorter

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.2

## Original Rule

Each sentence must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). If you do that, your sentence will be shorter, but it will not be easier to read. Write all the words in full.

Do not omit nouns to make short sentences. It will not be easy for the reader to understand the meaning of the sentence.

Do not omit verbs because the reader will not understand the action.

Do not omit the subject because the reader will not understand the action.

Do not omit articles to make the sentence shorter because omitted articles can cause ambiguity.

Do not omit parts of words to make contractions because contractions will not be easy to understand.

## STE-Code Adaptation

Each sentence in code documentation must have all its parts. When you write sentences, do not omit words or use contractions (for example, "don't," "isn't," "aren't"). Write all words in full. A shorter sentence is not necessarily easier to read.

Do not omit nouns. If you omit a noun, the reader will not know which code element the sentence refers to.

Do not omit verbs. If you omit a verb, the reader will not understand the action that the code performs.

Do not omit the subject. If you omit the subject, the reader will not understand which function, class, or module performs the action.

Do not omit articles (the, a, an). If you omit an article, the sentence can become ambiguous about which code element is specified.

Do not use contractions. Write "do not" instead of "don't," "is not" instead of "isn't," and "are not" instead of "aren't."

### Examples

**Do not omit the subject:**

> **Non-STE:** Can be a maximum length of 256 characters.
>
> **STE:** The input string can have a maximum length of 256 characters.
>
> *Adapted from original rule principle — "Do not omit the subject because the reader will not understand the action"; no direct spec pair*

**Do not omit the verb:**

> **Non-STE:** The return value a boolean that indicates success.
>
> **STE:** The return value is a boolean that indicates success.
>
> *Adapted from original rule principle — "Do not omit verbs because the reader will not understand the action"; no direct spec pair*

**Do not omit the noun:**

> **Non-STE:** The function returns the parsed.
>
> **STE:** The function returns the parsed configuration object.
>
> *Adapted from original rule principle — "Do not omit nouns to make short sentences"; no direct spec pair*

**Do not use contractions:**

> **Non-STE:** The method doesn't throw an exception when the input is null.
>
> **STE:** The method does not throw an exception when the input is null.
>
> *Adapted from original rule principle — "Do not omit parts of words to make contractions because contractions will not be easy to understand"; no direct spec pair*

**Do not omit articles:**

> **Non-STE:** `validate` function checks input parameter.
>
> **STE:** The `validate` function checks the input parameter.
>
> *Adapted from original rule principle — "Do not omit articles to make the sentence shorter because omitted articles can cause ambiguity"; no direct spec pair*

---

## Code-Domain Explanation

This rule applies across all code documentation types. The types of omitted words change with the documentation format. The consequences of omission also change with the audience and the reading context.

### README Files

README files often use a casual tone to sound friendly. Writers use contractions and omit articles. This style causes ambiguity. Write each sentence in full. Do not use contractions. Do not omit articles. Include the subject in every sentence.

**Omitted subject (headlinese):**

> **Non-STE:** Can be started with `npm start`.
>
> **STE:** You can start the application with `npm start`.
>
> *Principle applied: Do not omit the subject. The reader must know who or what performs the action.*

**Contractions in setup instructions:**

> **Non-STE:** You'll need to install Docker before you can run the container.
>
> **STE:** You must install Docker before you run the container.
>
> *Principles applied: P1 (approved words), no contractions. "You'll" becomes "You must".*

**Omitted articles in configuration steps:**

> **Non-STE:** Copy `.env.example` to `.env` and set database URL.
>
> **STE:** Copy the `.env.example` file to a `.env` file. Set the database URL in the `.env` file.
>
> *Principle applied: Do not omit articles. The articles "the" and "a" specify which file is the source and which file is new.*

### API Documentation

API reference documentation is dense with technical nouns. Writers often omit subjects and articles to save space. This practice is called "headlinese." It makes the text hard to parse for non-native readers. Write each endpoint description as a full sentence.

**Omitted subject in endpoint description:**

> **Non-STE:** Returns a list of users with their role assignments.
>
> **STE:** The GET /users endpoint returns a list of users. Each user object includes the role assignments.
>
> *Principle applied: Do not omit the subject. "Returns" has no subject. Add "The GET /users endpoint" as the subject.*

**Omitted articles in parameter descriptions:**

> **Non-STE:** `limit` — Maximum number of results to return.
>
> **STE:** The `limit` parameter sets the maximum number of results. The endpoint returns no more than this number.
>
> *Principle applied: Do not omit articles. The parameter description is a full sentence, not a fragment.*

**Contractions in error response docs:**

> **Non-STE:** The server doesn't accept requests with an expired token.
>
> **STE:** The server does not accept requests that have an expired token.
>
> *Principle applied: Do not use contractions. "doesn't" becomes "does not".*

### Docstrings and Inline Comments

Docstrings are part of the source code. Writers often omit verbs and articles in parameter descriptions. This makes the docstring shorter but less clear. Each parameter description must be a full sentence. Each return value description must be a full sentence.

**Omitted verb in parameter description:**

> **Non-STE:**
> ```python
> def connect(host: str, port: int):
>     """Connect to a server.
>
>     Args:
>         host: The server address.
>         port: The server port.
>     """
> ```
> **STE:**
> ```python
> def connect(host: str, port: int):
>     """Connect to a server.
>
>     Args:
>         host: The server address to connect to.
>         port: The port number on the server.
>     """
> ```
>
> *Principle applied: Do not omit verbs. The parameter description must express the relationship between the parameter and the function.*

**Omitted subject in return description:**

> **Non-STE:**
> ```python
>     Returns:
>         A new Connection object.
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```python
>     Returns:
>         The method returns a new Connection object.
> ```
>
> *Principle applied: Do not omit the subject. The return description includes the subject.*

### Commit Messages

Commit messages have strict length limits. The summary line allows a maximum of 72 characters. This limit causes writers to omit articles and subjects. For commit messages, apply this rule to the body text. The summary line can use a relaxed form (see Edge Cases).

**Omitted articles in commit body:**

> **Non-STE:**
> ```
> Fix timeout in database connection pool
>
> Connection pool didn't have timeout set. Added default 30s timeout.
> Connections now close after timeout expires.
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```
> Fix timeout in database connection pool
>
> The connection pool did not have a timeout value. Add a default timeout of 30 seconds. Connections now close after the timeout expires.
> ```
>
> *Principles applied: Do not use contractions ("didn't" → "did not"). Do not omit articles. Write full sentences in the body.*

### Error Messages

Error messages appear in logs, consoles, and user interfaces. Writers often omit articles and verbs to save space. An incomplete error message is hard to understand. Write error messages as full sentences. Include the subject, verb, and articles.

**Omitted verb and article:**

> **Non-STE:** File not found.
>
> **STE:** The file is not found.
>
> *Principle applied: Do not omit the verb "is". Do not omit the article "The".*

**Contractions in error messages:**

> **Non-STE:** Can't connect to the database server.
>
> **STE:** Cannot connect to the database server.
>
> *Principle applied: Do not use contractions. "Can't" becomes "Cannot". Note that "Cannot" is one word and is approved in STE-Code.*

**Omitted subject in error messages:**

> **Non-STE:** Invalid configuration value.
>
> **STE:** The configuration file contains an invalid value.
>
> *Principle applied: Do not omit the subject. "Invalid configuration value" has no subject. Add the subject that identifies where the problem is.*

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

Object-oriented documentation uses class and method descriptions. Method return descriptions often omit the subject. Constructor documentation often omits the verb. Write each description as a full sentence. Use the class name or "the method" as the subject. Use "the constructor" as the subject for constructor documentation.

**Method return description:**

> **Non-STE:**
> ```java
> /**
>  * @return A sorted copy of the list.
>  */
> public List<T> sort() { ... }
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```java
> /**
>  * @return The method returns a sorted copy of the list.
>  */
> public List<T> sort() { ... }
> ```
>
> *Principle applied: Do not omit the subject. Add "The method" before "returns".*

**Constructor omission of subject and verb:**

> **Non-STE:** Creates a new HttpClient with the default timeout.
>
> **STE:** The constructor creates a new HttpClient. The client uses the default timeout value.
>
> *Principles applied: Do not omit the subject. Do not combine multiple facts into one sentence.*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional code documentation describes type signatures and pure functions. Pattern-match documentation often omits verbs. Type variable descriptions often omit subjects. Write each pattern match arm as a full sentence. Write each type variable with a full description.

**Omitted verb in pattern match documentation:**

> **Non-STE:**
> ```haskell
> -- | Parse a configuration string.
> -- Left err  — Parse failure with error message.
> -- Right cfg — Successful parse.
> parseConfig :: String -> Either String Config
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```haskell
> -- | Parse a configuration string.
> -- Left err means that the parse failed. The err value is an error message.
> -- Right cfg means that the parse was successful. The cfg value is the parsed configuration.
> parseConfig :: String -> Either String Config
> ```
>
> *Principle applied: Do not omit verbs. Each pattern match arm uses a full sentence with a verb.*

**Omitted articles in type documentation:**

> **Non-STE:** `map` applies function to each element in list.
>
> **STE:** The `map` function applies a transformation function to each element in the list.
>
> *Principle applied: Do not omit articles. Add "a" before "transformation function" and "the" before "list".*

### Procedural (C, Go, Bash)

Procedural code documentation often uses headlinese. Function synopses in C header files omit articles. Go doc comments often omit subjects. Write each function description as a full sentence. Use "The function" as the subject.

**Headlinese in C header:**

> **Non-STE:**
> ```c
> /* parse_config: reads config file, returns Config struct */
> Config parse_config(const char *path);
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```c
> /* The parse_config function reads a configuration file. The function returns a Config struct. */
> Config parse_config(const char *path);
> ```
>
> *Principles applied: Do not omit articles. Do not omit subjects. Write full sentences.*

**Omitted subject in Go doc comment:**

> **Non-STE:**
> ```go
> // NewServer creates a new HTTP server with the provided handler.
> func NewServer(h http.Handler) *Server { ... }
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```go
> // The NewServer function creates a new HTTP server. The server uses the provided handler.
> func NewServer(h http.Handler) *Server { ... }
> ```
>
> *Principle applied: Do not omit the subject. Add "The NewServer function" as the subject.*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation describes resources and configurations. Comment lines in YAML and HCL often omit verbs and articles. This practice is common but causes ambiguity. Write each comment as a full sentence. Include the subject, verb, and articles.

**Omitted verb and article in Terraform:**

> **Non-STE:**
> ```hcl
> resource "aws_instance" "web" {
>   ami           = "ami-0c55b159cbfafe1f0"  # Amazon Linux 2 AMI
>   instance_type = "t3.micro"               # small instance for dev
> }
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```hcl
> resource "aws_instance" "web" {
>   ami           = "ami-0c55b159cbfafe1f0"  # This is the Amazon Linux 2 AMI.
>   instance_type = "t3.micro"               # The t3.micro instance type is sufficient for development.
> }
> ```
>
> *Principle applied: Do not omit verbs and subjects. Each comment is a full sentence.*

**Omitted article in SQL schema comment:**

> **Non-STE:**
> ```sql
> CREATE TABLE orders (
>   id SERIAL PRIMARY KEY,  -- unique order identifier
>   status VARCHAR(20)      -- order status
> );
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```sql
> CREATE TABLE orders (
>   id SERIAL PRIMARY KEY,  -- The id column is a unique order identifier.
>   status VARCHAR(20)      -- The status column stores the order status.
> );
> ```
>
> *Principle applied: Do not omit articles. Do not omit verbs. Each comment is a full sentence.*

### Systems (Rust Ownership, C Memory)

Systems documentation describes ownership, lifetimes, and memory behavior. Incomplete sentences in safety documentation cause real bugs. A reader who misunderstands an ownership rule writes unsafe code. Write all safety documentation in full sentences. Never omit the subject, verb, or articles.

**Omitted subject in safety documentation:**

> **Non-STE:**
> ```rust
> /// Returns a raw pointer to the internal buffer.
> /// # Safety
> /// Must not outlive the parent struct.
> pub unsafe fn as_ptr(&self) -> *const u8 { ... }
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```rust
> /// The method returns a raw pointer to the internal buffer.
> /// # Safety
> /// The caller must make sure that the pointer does not outlive the parent struct.
> pub unsafe fn as_ptr(&self) -> *const u8 { ... }
> ```
>
> *Principle applied: Do not omit the subject. "Must not outlive" has no subject. Add "The caller" as the subject.*

**Contractions in unsafe code documentation:**

> **Non-STE:** This function isn't safe to call from multiple threads.
>
> **STE:** This function is not safe to call from multiple threads.
>
> *Principle applied: Do not use contractions. "isn't" becomes "is not". Safety documentation must use full forms to prevent misreading.*

---

## Extended Examples

### Example 1 — Omitted Subject Across a Function Description

> **Non-STE:** Validates the input against the schema. Returns a Result object. Throws ValidationError on failure.
>
> **STE:** The function validates the input against the schema. The function returns a Result object. The function throws a ValidationError on failure.
>
> *Principle applied: Do not omit the subject. Each sentence starts with "The function". The reader always knows which entity performs the action.*

### Example 2 — Contractions in a Configuration Guide

> **Non-STE:** You'll need to set three environment variables before you can run the app. The server won't start if any of them aren't set. It's best to use a `.env` file.
>
> **STE:** You must set three environment variables before you run the application. The server will not start if one of the variables is not set. The best method is to use a `.env` file.
>
> *Principles applied: Do not use contractions. "You'll" → "You must". "won't" → "will not". "aren't" → "is not" (singular for "one"). "It's" → "The best method is".*

### Example 3 — Omitted Articles in Error Messages

> **Non-STE:**
> - Invalid token.
> - Request timed out.
> - Rate limit exceeded.
> - Permission denied.
> **STE:** [FIXME: generate STE correction for: ...]
> - The access token is not valid.
> - The request timed out.
> - The rate limit is exceeded.
> - The permission is denied.
>
> *Principle applied: Do not omit articles and verbs. Each error message is a full sentence. The reader knows what element failed and what the failure state is.*

### Example 4 — Omitted Noun (Implied Object)

> **Non-STE:** The `serialize` method converts the object to a JSON string and returns the serialized.
>
> **STE:** The `serialize` method converts the object to a JSON string. The method returns the serialized object.
>
> *Principle applied: Do not omit nouns. "the serialized" is an adjective without a noun. Add "object" to complete the noun phrase.*

### Example 5 — Multiple Omissions in a Bug Report Description

> **Non-STE:** Clicking save button doesn't persist data. Page refreshes and form's empty. Happens on Chrome 120.
>
> **STE:** When you click the Save button, the data is not saved. The page refreshes. The form is then empty. This problem occurs on Chrome version 120.
>
> *Principles applied: Do not omit articles ("save button" → "the Save button"). Do not use contractions ("doesn't" → "is not", "form's" → "the form is"). Do not omit the subject ("Happens" → "This problem occurs").*

### Example 6 — Omitted Verb in Status Update Documentation

> **Non-STE:**
> ```
> Migration status: pending.
> Connection pool: ready.
> Cache: warm.
> ```
> **STE:** [FIXME: generate STE correction for: ...]
> ```
> The migration status is pending.
> The connection pool is ready.
> The cache is warm.
> ```
>
> *Principle applied: Do not omit verbs. Each status line includes the verb "is". The sentence has a subject and a predicate.*

---

## Edge Cases

### Edge Case 1 — Commit Message Summary Line (Space Constraint)

The commit message summary line has a practical limit of 72 characters. This limit makes it difficult to include all articles and write a full sentence. The summary line may use a relaxed form. The body text must follow the rule strictly.

> **Acceptable summary (relaxed):** Fix race condition in connection pool shutdown
> **Body (must follow the rule):** The connection pool had a race condition during shutdown. A worker thread could access a closed connection. Add a mutex lock to the shutdown procedure.
>
> *The summary line omits articles for space. This is a known edge case. The body compensates with full sentences.*

### Edge Case 2 — CLI Help Text (Terminal Width Constraint)

CLI help text displays in terminal windows with a maximum of 80 characters per line. This width limit causes writers to omit articles and subjects. Write the long-form documentation in full sentences (man pages, online docs). The CLI help text may use a relaxed form.

> **Acceptable CLI help (relaxed):**
> ```
> --timeout SECONDS   Set connection timeout (default: 30)
> --retries N         Maximum retry attempts (default: 3)
> ```
> **Long-form documentation (must follow the rule):**
> The `--timeout` option sets the connection timeout in seconds. The default value is 30.
> The `--retries` option sets the maximum number of retry attempts. The default value is 3.
>
> *The CLI help text uses fragments for space. The full documentation uses complete sentences.*

### Edge Case 3 — When a Code Token Is Also a Contraction

Some code tokens look like contractions. For example, a Python variable named `don't_save` or a Rust lifetime parameter `'static`. These tokens are technical code nouns and are allowed (Rule 1.5). Format them as inline code. Do not confuse them with English contractions.

> **Acceptable:** The `don't_save` flag prevents the function from writing to the database. The default value of the flag is `false`.
>
> *The token `don't_save` is a code identifier. It is not an English contraction. The surrounding text uses no contractions.*

### Edge Case 4 — Inline Comments with Code on the Same Line

An inline comment sits on the same line as a code statement. The line length limit creates pressure to omit words. Write the comment as a full sentence when possible. If the line is too long, move the comment to the line above the code.

> **Non-STE (cramped):**
> ```python
> timeout = value if value > 0 else 30  # fallback to default
> ```
> **STE (comment moved above):**
> ```python
> # Use the default timeout value of 30 if the parameter is not positive.
> timeout = value if value > 0 else 30
> ```
>
> *Moving the comment above the code gives more space for a full sentence.*

### Edge Case 5 — The "'s" Possessive Form

The "'s" suffix in English marks both contractions ("it's" = "it is") and possessives ("the function's return value"). Possessive "'s" is not a contraction. It is allowed in STE-Code. Make sure that the context makes the possessive meaning clear.

> **Acceptable (possessive):** The function's return value is a boolean.
> **Not acceptable (contraction):** The function's called from the event loop.
> **Correction:** The function is called from the event loop.
>
> *The possessive "'s" is allowed. The contraction "'s" for "is" is not allowed. Check each instance to make sure it is possessive.*

---

## Grammar Notes

### Why Contractions Are Harder to Parse

A contraction combines two words by removing letters and inserting an apostrophe. The apostrophe replaces the removed letters. For example, "do not" becomes "don't" (the letter "o" is removed). This process creates words that are not in the dictionary. A non-native reader must parse the contraction into its original words. This step adds cognitive load.

Contractions also have regional variants. For example, "ain't" is common in some English dialects but not in others. A reader from a different region may not know the contraction. The full form ("is not", "are not", "am not") is universal.

In code documentation, contractions create ambiguity with code syntax. Many programming languages use the apostrophe for character literals (C, Rust), string quoting (Python, JavaScript), or atom literals (Elixir, Erlang). A reader may briefly confuse a contraction with a code token.

### The Function of Articles in English

Articles (a, an, the) mark noun phrases. The definite article "the" points to a specific instance. The indefinite article "a" or "an" points to any instance. When you omit an article, the reader does not know if the noun is specific or general.

Consider these two sentences:

> The function returns an error.
> The function returns the error.

The first sentence means that the function returns some error object. The second sentence means that the function returns a specific error that was mentioned before. Without an article ("Function returns error"), the meaning is not clear.

In code documentation, omitted articles cause two common problems:

1. The reader does not know if a parameter is a specific instance or a general type.
2. The reader does not know if a return value is a new object or a reference to an existing object.

### Subject-Verb Agreement After Full Forms

When you replace a contraction with its full form, check the subject-verb agreement. The verb form may need to change.

> **Contraction:** The list doesn't contain the element.
> **Full form:** The list does not contain the element. (Subject is "list", verb is "does")

> **Contraction:** The values don't match the expected results.
> **Full form:** The values do not match the expected results. (Subject is "values", verb is "do")

The verb "do" changes form based on the subject: "does" for third-person singular, "do" for all other persons and numbers. When you expand a contraction, make sure the verb agrees with the subject.

### Negative Contractions and Double Negatives

Negative contractions (don't, doesn't, won't, can't, isn't, aren't, wasn't, weren't, haven't, hasn't, hadn't) are common in casual writing. When you expand these contractions, the word "not" appears after the auxiliary verb. The resulting sentence is longer but clearer.

Some sentences with expanded negatives can become awkward because of word order. In these cases, restructure the sentence.

> **Contraction:** The function doesn't ever return null.
> **Awkward full form:** The function does not ever return null.
> **Restructured:** The function never returns null.

The word "never" is a single-word negative and is allowed in STE-Code. Use "never" instead of "does not ever" when it improves clarity.

### Contractions in Quoted Code Output

When you quote code output, error messages, or log entries, preserve the original text. Do not expand contractions inside quoted blocks. The quote is a record of what the system produced. The surrounding text must still follow the rule.

> **Acceptable:** The command prints the message "Can't open file" to the console. This message means that the file path is not correct.
>
> *The quoted message "Can't open file" contains a contraction. This is acceptable because it is a direct quote. The surrounding explanation uses "is not correct" instead of a contraction.*

---

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary. Contractions are not approved words. Write the full forms.
- **Rule 1.2** — Use words only as their specified part of speech. Contractions combine two words into one and blur the part-of-speech boundary.
- **Rule 1.4** — Use only approved verb forms and adjective forms. Contractions create non-standard verb forms (for example, "don't" as a negative auxiliary).
- **Rule 1.10** — No slang, jargon, or regional terms. Many contractions are regional. Their meanings change across English dialects.
- **Rule 1.11** — One term per concept. Omitted words create inconsistency because different writers omit different words for the same concept.
- **Rule 1.14** — Use American English spelling. Contractions such as "shan't" are British. Use the full form to avoid regional variation.
- **Rule 4.1** — Write short and clear sentences. Omission and contraction are the wrong way to make sentences shorter. Use the methods in Rule 4.1 instead.
- **Rule 4.3** — Use the active voice. Omitted subjects often appear in passive constructions. Identify the subject and use the active voice.
- **Section 5 (Procedural Writing)** — Imperative sentences in procedures have an implied subject ("you"). The implied subject is acceptable in procedural writing. Do not omit other sentence parts.

---

## Summary Checklist

Before you publish code documentation, check each sentence:

- [ ] The sentence has a subject. The reader can identify who or what performs the action.
- [ ] The sentence has a verb. The reader can identify the action.
- [ ] The sentence has all necessary nouns. No noun is implied or omitted.
- [ ] The sentence includes articles (a, an, the) where needed.
- [ ] The sentence has no contractions. "don't" is "do not". "isn't" is "is not".
- [ ] The "'s" suffix is possessive only. It is not used as a contraction for "is" or "has".
- [ ] Each parameter description in a docstring is a full sentence.
- [ ] Each return value description in a docstring is a full sentence.
- [ ] Each error message is a full sentence with subject, verb, and articles.
- [ ] Commit message body text uses full sentences. The summary line may use a relaxed form.
