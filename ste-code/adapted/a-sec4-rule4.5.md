# Rule 4.5 — When Applicable, Use an Article (the, a, an) or a Demonstrative Adjective (this, these) Before a Noun or a Multi-Word Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 4.5

## Original Rule

Articles and demonstrative adjectives show the position of nouns and multi-word nouns in the sentence. Use articles and demonstrative adjectives correctly and do not omit them to make the text shorter.

It is not always correct English to put an article before a noun. Do not use articles in general statements or concepts.

In short sentences, it can be clearer to use articles before all nouns.

But sentences that contain a long series of items are clearer when you use the article only before the first noun in the series.

When you use the article in a series of items, always make sure that adjectives do not cause ambiguity.

A definite article is incorrect before a noun when an alphanumeric identifier comes after it. This is because the alphanumeric identifier shows that it is a proper noun.

## STE-Code Adaptation

Articles (the, a, an) and demonstrative adjectives (this, these) show the position of nouns and multi-word nouns in code documentation. Use them correctly and do not omit them to make the text shorter.

Do not use articles in general statements or when referring to abstract concepts in code (for example, "performance," "scalability," "error handling").

In short sentences, use articles before all nouns to make the text clear.

In sentences that contain a long series of items, use the article only before the first noun in the series. This keeps the text clear without unnecessary repetition.

When you use an article in a series of items, always make sure that adjectives do not cause ambiguity. If an adjective applies only to the first noun, the reader must know this from the article placement.

Do not use a definite article before a noun when a code identifier (function name, class name, variable name) comes after it. The identifier is a proper noun and does not need an article.

### Examples

**Using an article before a noun in a short instruction:**

> **Non-STE:** Call callback function.
>
> **STE:** Call the callback function.
>
> *Adapted from original rule principle — in short sentences, use articles before all nouns; no direct spec pair*

**Omitting articles in general statements:**

> **STE:** You can use equivalent alternatives for these middleware functions.
>
> *(No articles before "performance" or "scalability." The context does not give a specified metric.)*
>
> *Adapted from original rule principle — do not use articles in general statements or concepts; no direct spec pair*

**Using the article only before the first noun in a long series:**

> **STE:** Install the new configuration file, the log directory, the environment variables, and the startup script.
>
> *Adapted from original rule principle — use the article only before the first noun in a series; no direct spec pair*

**Using articles before each noun when an adjective applies to only one item:**

> **STE:** Install the new configuration file, the log directory, the environment variables, and the startup script.
>
> *(The article "the new" applies only to the configuration file. The remaining items are not described as new.)*
>
> *Adapted from original rule principle — make sure that adjectives do not cause ambiguity; no direct spec pair*

**No article before a noun with a code identifier:**

> **Non-STE:** Call the function `validateInput`.
>
> **STE:** Call function `validateInput`.
>
> *Adapted from original rule principle — a definite article is incorrect before a noun when an alphanumeric identifier comes after it; no direct spec pair*

> **Non-STE:** Configure the module `AuthService`.
>
> **STE:** Configure module `AuthService`.
>
> *Adapted from original rule principle — a definite article is incorrect before a noun when an alphanumeric identifier comes after it; no direct spec pair*

---

## Code-Domain Explanation

Article use changes with the documentation format. Each type has a different reader expectation for article presence. Missing articles in one format may be acceptable (CLI help) but harmful in another (safety documentation).

### README Files

README files mix general descriptions with specific instructions. Use no article for general concepts. Use articles for specific, named items.

> **Non-STE:** Project uses Redis for caching and PostgreSQL for persistence. Configuration is done through environment variables.
>
> **STE:** The project uses a Redis instance for caching and a PostgreSQL database for persistence. Set the configuration values through environment variables.
>
> *Principles applied: No article on "Redis" (proper noun). Article on "instance," "database," "configuration values" (specific items).*

**Setup instructions (specific items with articles):**

> **Non-STE:** Run `npm install` to get dependencies. Copy `.env.example` to `.env` and fill in values.
>
> **STE:** Run `npm install` to install the dependencies. Copy the `.env.example` file to a `.env` file. Set the required values in the `.env` file.
>
> *Principles applied: "the" before specific dependencies and file. "a" before the new `.env` file (not yet existing).*

### API Documentation

API endpoint descriptions need articles to distinguish the endpoint (general) from a specific response (instance). Parameter descriptions must use articles to mark type vs instance.

> **Non-STE:** GET /users returns paginated list of user objects. `limit` parameter controls page size. Response includes metadata with total count.
>
> **STE:** The GET /users endpoint returns a paginated list of user objects. The `limit` parameter controls the page size. The response includes a metadata object with the total count.
>
> *Principles applied: "a" for list (one of many possible). "the" for `limit` parameter, page size, total count (specific to this endpoint). "a" for metadata object (instance).*

**Error response description:**

> **Non-STE:** Returns error object with message and code fields when request fails validation.
>
> **STE:** The endpoint returns an error object when the request fails validation. The error object has a `message` field and a `code` field.
>
> *Principles applied: "an" before error object (instance). "the" for endpoint and request (specific). No article before `message` and `code` field identifiers.*

### Docstrings and Inline Comments

Docstrings combine the two rules: no article before a noun followed by a code identifier, but use articles for plain nouns in descriptions.

> **Non-STE:**
> ```python
> def find(id: int) -> User:
>     """Find user by ID and return User object or None if not found."""
> ```
>
> **STE:** [FIXME: generate STE correction for: ...]
> ```python
> def find(id: int) -> User:
>     """Find a user by the given ID.
>
>     Returns:
>         A User object if the user is found.
>         None if no user has the given ID.
>     """
> ```
>
> *Principles applied: "a" before User object (instance). "the" before given ID (specific). No article before "None" (code identifier).*

**Parameter with code identifier:**

> **Non-STE:** `host: The server address.` (acceptable short form)
> **STE:** `host: The host address of the server.` (full sentence with article)
>
> *Principles applied: Parameter descriptions benefit from articles even in short forms. "The host address" is a specific parameter.*

### Commit Messages

The commit summary line often omits articles due to the 72-character limit. The body must use full article rules.

> **Non-STE:**
> ```
> Fix null pointer in cache lookup
>
> Cache.get returned null when key expired during concurrent access.
> Added null check before dereference.
> ```
>
> **STE:**
> ```
> Fix null pointer in cache lookup
>
> The Cache.get method returned a null value when a key expired during a concurrent access. Add a null check before the dereference operation.
> ```
>
> *Principles applied: Summary line may drop articles. Body uses "the" for specific method and operation, "a" for null value and concurrent access (instances).*

### Error Messages

Error messages must use articles to specify which entity caused the error. A missing article makes the error message ambiguous.

> **Non-STE:** Connection refused. Invalid configuration value. Timeout exceeded.
>
> **STE:** The connection to the server is refused. The configuration file has an invalid value. The request timeout is exceeded.
>
> *Principles applied: "the" before server, configuration file, request timeout (specific entities). Articles tell the user which resource failed.*

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

Class documentation uses articles to distinguish between a class (type) and an instance. Method documentation uses articles to distinguish between the method (general) and a call (specific).

**Class description:**

> **Non-STE:** `ConnectionPool` manages pool of database connections. Pool supports configurable minimum and maximum size.
>
> **STE:** The `ConnectionPool` class manages a pool of database connections. The pool supports a configurable minimum size and a configurable maximum size.
>
> *Principles applied: "The" before `ConnectionPool` (specific class name, treated as common noun in sentence context). "a" before pool (instance). Note: "The `ConnectionPool` class" uses "the" because "class" is the noun, not `ConnectionPool`.*

**Method description with return value:**

> **Non-STE:** `getConnection()` acquires connection from pool and returns Connection object.
>
> **STE:** The `getConnection` method acquires a connection from the pool. The method returns a `Connection` object.
>
> *Principles applied: "The" before method name. "a" before connection (one of many in pool). No article before `Connection` — it is a code identifier following the noun "object."*

**Property description:**

> **Non-STE:** `isConnected` — boolean indicating whether connection is active.
>
> **STE:** The `isConnected` property is a boolean value. The value is `true` when the connection is active.
>
> *Principles applied: "The" before property and connection. "a" before boolean value.*

### Functional (Haskell, Elixir, Clojure, Rust)

Functional documentation uses articles to distinguish between a type constructor and a value, and between a general function and a specific application.

**Type alias documentation:**

> **Non-STE:** `type UserId = Int` — unique identifier for user.
>
> **STE:** The `UserId` type is an alias for `Int`. The type represents a unique identifier for a user.
>
> *Principles applied: "The" before `UserId` type. "an" before alias (vowel sound). "a" before unique identifier and user.*

**Pattern match documentation:**

> **Non-STE:** `Ok(value)` — successful result containing parsed value. `Err(error)` — failure with error description.
>
> **STE:** The `Ok(value)` pattern represents a successful result. The variant contains the parsed value. The `Err(error)` pattern represents a failure. The variant contains an error description.
>
> *Principles applied: "The" before pattern names. "a" before result and failure (instances). "the" before parsed value (specific to the variant). "an" before error description.*

**Higher-order function documentation:**

> **Non-STE:** `map` applies function to each element of list and returns new list.
>
> **STE:** The `map` function applies a given function to each element of a list. The function returns a new list with the transformed elements.
>
> *Principles applied: "The" before `map` function. "a" before given function and list (general). "the" before transformed elements (specific to this operation).*

### Procedural (C, Go, Bash)

Procedural documentation uses articles to distinguish between a pointer (address) and the pointed-to value, and between a buffer (memory region) and its content.

**Function with pointer parameter:**

> **Non-STE:** `write_to_buffer` takes pointer to buffer and writes data from source array.
>
> **STE:** The `write_to_buffer` function receives a pointer to a buffer. The function writes the data from a source array into the buffer.
>
> *Principles applied: "a" before pointer and buffer (instances). "the" before data (specific data being written). "a" before source array (one of possibly many). "the" before buffer (the same buffer from the first sentence).*

**Struct field documentation:**

> **Non-STE:** `fd` — file descriptor for socket. `addr` — sockaddr_in with remote address.
>
> **STE:** The `fd` field stores a file descriptor for the socket. The `addr` field stores a `sockaddr_in` struct with the remote address.
>
> *Principles applied: "The" before field names. "a" before file descriptor. "the" before socket (specific to this struct). No article before `sockaddr_in` (code identifier after "struct"). "the" before remote address.*

**Error return documentation:**

> **Non-STE:** Returns 0 on success, -1 on failure with errno set.
>
> **STE:** The function returns a 0 value on success. The function returns a -1 value on failure. On failure, the `errno` variable contains an error code.
>
> *Principles applied: "a" before 0 value and -1 value (instances of return values). "the" before `errno` variable. "an" before error code.*

### Declarative (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses articles to distinguish between a resource type and a resource instance, and between a table (the concept) and a row.

**Terraform variable documentation:**

> **Non-STE:** `instance_type` — EC2 instance type for virtual machine. Must be valid type in selected region.
>
> **STE:** The `instance_type` variable sets the EC2 instance type for the virtual machine. The value must be a valid type in the selected region.
>
> *Principles applied: "The" before variable name. "the" before virtual machine (specific to this configuration). "a" before valid type.*

**SQL table documentation:**

> **Non-STE:** `users` table stores account information. `email` column has unique constraint.
>
> **STE:** The `users` table stores account information for each user. The `email` column has a unique constraint.
>
> *Principles applied: "The" before table and column names (specific database objects). "a" before unique constraint.*

**Kubernetes resource documentation:**

> **Non-STE:** `Deployment` manages set of pods running containerized application. Supports rolling updates and rollbacks.
>
> **STE:** A `Deployment` resource manages a set of pods. The pods run a containerized application. The resource supports rolling updates. The resource supports rollbacks.
>
> *Principles applied: "A" before `Deployment` (one instance of the resource type). "a" before set and application. "The" in subsequent references (the same resource and pods). No article before "rolling updates" and "rollbacks" (general concepts).*

### Systems (Rust Ownership, C Memory)

Systems documentation uses articles to make ownership and lifetime relationships unambiguous. A missing article can cause a reader to misunderstand which pointer owns which memory.

**Ownership transfer documentation:**

> **Non-STE:** `into_raw` consumes Box and returns raw pointer. Caller is responsible for freeing memory.
>
> **STE:** The `into_raw` function consumes a `Box` value. The function returns a raw pointer to the allocated memory. The caller is responsible for freeing the memory.
>
> *Principles applied: "The" before function. "a" before `Box` value and raw pointer (instances). "the" before allocated memory and memory (specific, same memory). "The" before caller.*

**Safety requirement documentation:**

> **Non-STE:** Pointer must be valid and point to initialized memory of correct type.
>
> **STE:** The pointer must be valid. The pointer must point to an initialized region of memory. The memory must be of the correct type.
>
> *Principles applied: Articles make each requirement a full, unambiguous sentence. "The" before pointer and memory (specific instances). "an" before initialized region. "the" before correct type.*

**Lifetime documentation:**

> **Non-STE:** Reference must not outlive data it points to. Returned reference has same lifetime as input.
>
> **STE:** The reference must not outlive the data that it points to. The returned reference has the same lifetime as the input reference.
>
> *Principles applied: "The" before reference, data, returned reference, input reference — all specific to the documented function.*

---

## Extended Examples

### Example 1 — Missing Article in API Parameter Description

> **Non-STE:** `timeout` — number of seconds to wait for response before connection fails.
>
> **STE:** The `timeout` parameter sets the number of seconds to wait for a response. The connection fails after the timeout period.
>
> *Principles applied: P1 (approved words), Rule 4.5 — "The" introduces the specific parameter. "a" before response (any response). "the" before timeout period (the same timeout).*

### Example 2 — Article Before Acronym (a vs an)

> **Non-STE:** A HTTP request is sent to a API endpoint. The response contains a URL to a HTML page.
>
> **STE:** An HTTP request is sent to an API endpoint. The response contains a URL to an HTML page.
>
> *Principles applied: Rule 4.5 — Use "an" before acronyms that start with a vowel sound. "HTTP" starts with a vowel sound ("aitch"). "API" starts with a vowel sound ("ay"). "URL" starts with a consonant sound ("yoo"). "HTML" starts with a vowel sound ("aitch").*

### Example 3 — Demonstrative Adjective for Sentence Linking

> **Non-STE:** The function returns a configuration object. Configuration object has three fields: host, port, and timeout.
>
> **STE:** The function returns a configuration object. This object has three fields: host, port, and timeout.
>
> *Principles applied: Rule 4.5 — Use the demonstrative adjective "this" to refer to the object from the previous sentence. This linking prevents repetition and makes the relationship clear. "This object" = "the configuration object just mentioned."*

> **Non-STE:** The `validate` and `sanitize` functions run before each request. Functions check the input for invalid characters.
>
> **STE:** The `validate` and `sanitize` functions run before each request. These functions check the input for invalid characters.
>
> *Principles applied: Rule 4.5 — Use "these" for a plural referent already introduced. "These functions" links back clearly to the two functions named in the previous sentence.*

### Example 4 — General Statement vs Specific Instance

> **Non-STE:** The error handling is important for the production applications. The function throws the error when the input is an invalid.
>
> **STE:** Error handling is important for production applications. The function throws an error when the input is not valid.
>
> *Principles applied: Rule 4.5 — No article before "error handling" (general concept). No article before "production applications" (general class). "an" before error (one instance). "the" before function and input (specific to this context).*

### Example 5 — Series with Mixed Specificity

> **Non-STE:** The deployment needs the configuration file, a log directory for the output, and environment variables for the runtime.
>
> **STE:** The deployment needs a configuration file, a log directory, and the environment variables.
>
> *Principles applied: Rule 4.5 — In a short series, use articles before each noun. "a" before configuration file and log directory (not yet created). "the" before environment variables (already defined in the project). The simplified version removes unnecessary prepositional phrases.*

### Example 6 — Article Before Noun With Version Number

> **Non-STE:** The project uses the Node.js 20 and the PostgreSQL 16. The migration requires the Python 3.12.
>
> **STE:** The project uses Node.js 20 and PostgreSQL 16. The migration requires Python 3.12.
>
> *Principles applied: Rule 4.5 — No definite article before a proper noun with a version number. "Node.js 20" is a proper noun (product name with version). The version number makes it a proper noun identifier. But "the Node.js runtime" would use an article because "runtime" is a common noun.*

---

## Edge Cases

### Edge Case 1 — Article Before Code Identifiers in Prose

When a code identifier is used as the subject of a sentence, it acts as a proper noun. But when the sentence refers to the concept or role of the identifier, an article may be needed. This distinction depends on the sentence structure.

> **No article (identifier as proper noun):** `ConnectionPool` manages database connections.
>
> **Article (identifier as concept):** The `ConnectionPool` class manages database connections.
>
> *The word "class" after the identifier turns the identifier into an adjective describing the common noun. The article belongs to "class," not to `ConnectionPool`.*

> **No article (identifier as proper noun):** Call `initialize` before `connect`.
>
> **Article (identifier in descriptive context):** The `initialize` function must run before the `connect` function.
>
> *When "function" follows the identifier, the article is required. Without "function," the identifier is a proper noun and takes no article.*

### Edge Case 2 — Article "a" vs "an" Before Code Terms

The choice between "a" and "an" depends on the initial sound of the word, not the initial letter. Code terms with leading acronyms or symbols create edge cases.

> **"an" before vowel sound:** an SQL query (pronounced "ess-que-ell"), an HTML element, an XML parser, an npm package (pronounced "en-pee-em")
>
> **"a" before consonant sound:** a URL (pronounced "yoo-are-ell"), a USB device, a Unix system, a one-time token
>
> *When the pronunciation is ambiguous, choose the form that matches the most common pronunciation in the target community.*

### Edge Case 3 — Article Use in Headings and Titles

Documentation headings often omit articles for brevity. This practice is acceptable in section titles but not in body text.

> **Acceptable heading:** Installation Guide
> **Body text:** The installation guide describes how to set up the project.

> **Acceptable heading:** Error Codes
> **Body text:** The error codes table lists each error that the API can return.

> *Headings may omit articles. The first sentence below a heading must use the full article rule. This pattern helps skimming while keeping body text unambiguous.*

### Edge Case 4 — Framework Names That Include "The"

Some frameworks and tools use "The" as part of their official name. In these cases, treat the full name (including "The") as a proper noun.

> **Acceptable:** The `TheMovieDB` client wraps the REST API.
>
> *The leading "The" is part of the proper noun identifier. The sentence structure works because the article does not belong to the identifier when it is used with a common noun ("client").*

> **Better alternative:** The `TheMovieDB` API client wraps the REST endpoints.
>
> *Adding a common noun ("API client") after the identifier gives the sentence a natural article target while keeping the proper noun intact.*

### Edge Case 5 — Articles in CLI Help Text vs Long-Form Documentation

CLI help text displayed in an 80-character terminal may drop articles. The long-form manual page or online documentation must use the full article rules.

> **Acceptable CLI help:**
> ```
> --host ADDRESS     Server hostname or IP address
> --port NUMBER      Server port (default: 5432)
> ```
>
> **Long-form documentation:**
> The `--host` option sets the server hostname or an IP address. The `--port` option sets the server port. The default value is 5432.
>
> *CLI help text is a constrained format. The long-form documentation must use articles as specified in this rule. Never use the CLI form in README files or API documentation.*

---

## Grammar Notes

### Definite vs Indefinite Articles in Code Contexts

The definite article "the" refers to a specific, identifiable item. The indefinite article "a" or "an" refers to any item of a type. In code documentation, this distinction has important consequences.

> **"a" (any instance):** The function returns a `Connection` object. *(The caller receives one of many possible Connection objects.)*
>
> **"the" (specific instance):** The function returns the `Connection` object from the pool. *(The caller receives a specific Connection that was mentioned before.)*
>
> **No article (general type):** `Connection` objects are not thread-safe. *(Statement about the type as a whole.)*

**Common pattern in error documentation:**

> First mention (indefinite): The method throws a `ValidationError` when the input is empty.
> Second mention (definite): The `ValidationError` contains a message that describes the invalid field.
>
> *This pattern follows the linguistic rule: indefinite for first introduction, definite for subsequent references.*

### Demonstrative Adjectives for Cohesion

Demonstrative adjectives ("this," "these") link sentences by referring to previously introduced nouns. Use them instead of repeating a long noun phrase.

> **Without demonstrative:** The `authenticate` method validates a user token. The `authenticate` method returns a session object. The session object has an expiry time.
>
> **With demonstrative:** The `authenticate` method validates a user token. This method returns a session object. This object has an expiry time.
>
> *"This method" refers to the `authenticate` method. "This object" refers to the session object. The demonstrative adjectives reduce repetition and make the relationship between sentences clear.*

**Use "these" for plural referents:**

> The library exports three functions: `parse`, `validate`, and `format`. These functions process the configuration data.
>
> *"These functions" refers to the set of three functions. Using "these" is more concise than repeating all three names.*

### The Proper Noun Exception for Code Identifiers

A code identifier (function name, class name, variable name, module name) is a proper noun. Do not place a definite article directly before a proper noun.

> **Incorrect:** Call the `connect`.
> **Correct:** Call `connect`.
> **Correct:** Call the `connect` function.
>
> *In the correct version with "function," the article belongs to "function," not to `connect`. The code identifier acts as an adjective describing the noun "function."*

**This rule applies to all identifier types:**

> **No article (proper noun):** `UserRepository` extends `BaseRepository`.
> **Article (common noun follows):** The `UserRepository` class extends the `BaseRepository` class.
> **No article (proper noun):** Set `DEBUG_MODE` to `true`.
> **Article (common noun follows):** Set the `DEBUG_MODE` environment variable to the `true` value.

### Articles with Uncountable Nouns

Uncountable nouns in code documentation refer to abstract concepts: performance, scalability, security, reliability, memory, throughput, latency. Use no article when referring to the concept in a general sense.

> **General (no article):** Performance is critical for real-time applications.
> **Specific (article):** The performance of the `parse` function decreased in version 2.0.
>
> *The first sentence talks about performance as a concept. The second sentence talks about the specific performance of a specific function.*

**Common uncountable nouns in code:**

> **General:** Security requires careful input validation.
> **Specific:** The security of the authentication module depends on the key length.
>
> **General:** Memory usage increases with the input size.
> **Specific:** The memory that the `cache` object allocates is freed on shutdown.

### Article in Sentences with Code Identifiers in Series

When a sentence lists multiple code identifiers, apply the same rule: no article before identifiers used as proper nouns. But use articles for the common nouns that follow.

> **Incorrect:** Import the `Router`, the `Middleware`, and the `Logger` from the framework.
>
> **Correct:** Import `Router`, `Middleware`, and `Logger` from the framework.
>
> **Correct:** Import the `Router` class, the `Middleware` class, and the `Logger` class from the framework.
>
> *The first correct version treats identifiers as proper nouns. The second correct version uses articles before "class" (the common noun). Both are acceptable. Choose one style and be consistent (Rule 1.11).*

---

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary. Approved words have defined articles and grammatical roles.
- **Rule 1.5** — Technical code nouns are allowed. Code identifiers are proper nouns and take no direct article.
- **Rule 1.6** — Non-approved words are allowed when they are technical code nouns. The article rules still apply to surrounding text.
- **Rule 1.7** — Do not use technical nouns as verbs. Using a code identifier as a verb often leads to missing articles.
- **Rule 1.11** — One term per concept. Be consistent with article use for the same concept across all documentation.
- **Rule 1.14** — Use American English spelling. Article conventions are the same in American and British English, but noun phrases may differ (for example, "a hospital" vs "an hospital" in some British dialects).
- **Rule 4.1** — Write short and clear sentences. Articles help keep sentences clear by marking the boundaries of noun phrases.
- **Rule 4.2** — Do not omit words or use contractions. Omitted articles are a common form of word omission.
- **Rule 4.3** — Use a vertical list for complex texts. Each list item must connect grammatically to the introductory text, including article agreement.
- **Rule 4.4** — Do not use noun clusters of more than three nouns. Articles help break up long noun clusters by marking the start of each noun phrase.
- **Section 5 (Procedural Writing)** — Imperative sentences often place the article after the verb. The article must still be present.
- **Section 6 (Descriptive Writing)** — Descriptive sentences use articles to track which entities are new (a/an) and which were introduced earlier (the).

---

## Summary Checklist

Before you publish code documentation, check each sentence:

- [ ] Each noun has an article (a, an, the) or a demonstrative adjective (this, these) unless it is a general concept, a code identifier, or an abstract/uncountable noun.
- [ ] The definite article "the" is used only for specific, identifiable items.
- [ ] The indefinite article "a" or "an" is used for first mentions and general instances.
- [ ] No definite article directly precedes a code identifier (function name, class name, variable name).
- [ ] The article "an" is used before words that start with a vowel sound (an HTTP request, an SQL query).
- [ ] Demonstrative adjectives ("this," "these") link sentences to previously introduced nouns.
- [ ] In a series of items, the article placement does not cause adjective ambiguity.
- [ ] Headings may drop articles, but body text must include them.
- [ ] General statements about abstract concepts (performance, security, scalability) use no article.
- [ ] CLI help text may relax this rule. All other documentation must follow it.
