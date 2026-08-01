---

## Rule 4.5 — Use an Article or a Demonstrative Adjective Before a Noun

**Source:** Adapted from ASD-STE100 Issue 9, Rule 4.5.

### Requirement

Articles (**the**, **a**, **an**) and demonstrative adjectives (**this**, **these**) show
the position of nouns and multi-word nouns in the sentence. Use them correctly; do not
omit them to make the text shorter.

- Do not use an article in a general statement or before an abstract concept
  (performance, scalability, error handling, concurrency, backward compatibility).
- In short sentences, use an article before each noun.
- In a long series of items, use the article only before the first noun. Repeat it
  before each item when an adjective applies to only one item (to avoid ambiguity).
- Do not use a definite article before a noun when a code identifier follows it —
  the identifier is a proper noun (function, class, variable, file, environment
  variable, error code, version tag).
- Use a demonstrative adjective (**this**, **these**) to connect a noun to the topic
  of the previous sentence. Always keep the noun after it; do not write "this"/"these" alone.

### Code-domain examples

Article before a noun in a short instruction:

> **Non-STE:** Call callback function. Pass response object to handler and set retry flag.
> **STE:** Call the callback function. Pass the response object to the handler. Then set the retry flag.

API reference sentence:

> **Non-STE:** Method reads configuration file and returns settings object.
> **STE:** The `load` method reads the configuration file and returns the settings object.

No article in a general statement; "the" for a specific item:

> **Non-STE:** The error handling is important for the production applications. A function throws the error when the input is not valid.
> **STE:** Error handling is important for production applications. The function throws an error when input is not valid.

Article only before the first noun in a long series:

> **STE:** Delete the temporary files, log files, cache entries, and lock files before you start the build.

Article before each noun when an adjective applies to only one item:

> **STE:** Register the new event listeners, the timers, the subscriptions, and the cleanup callbacks. (Only the event listeners are new.)

No article before a noun with a code identifier (proper noun):

> **Non-STE:** Call the function `validateInput` before you send the request.
> **STE:** Call function `validateInput` before you send the request.  — or —  Call the `validateInput` function before you send the request.
> **STE:** Configure module `AuthService` in the container.  /  Set variable `LOG_LEVEL` to `debug`.  /  Error `ERR_TIMEOUT_1042` shows in the console log.  /  Install version 3.2.1 of the package.

Demonstrative adjective for sentence linking:

> **Non-STE:** The function returns a configuration object. Configuration object has three fields: host, port, and timeout.
> **STE:** The function returns a configuration object. This object has three fields: `host`, `port`, and `timeout`.

Article use in commit messages and release notes:

> **STE:** Fix the race condition in the scheduler. The worker pool now waits for the queue to become empty.
> **STE:** Adds retry logic to the `HttpClient` class. Removes deprecated method `sendSync`.

Article use in an error message and a test description:

> **STE:** The input is not valid. The `name` field must be a string.
> **STE:** The test checks that the handler returns the status code 404 when the record is not in the database.

### Paradigm-specific guidance

- **Object-Oriented:** use an article to separate a class (type) from an instance (value) — "The `ConnectionPool` class manages a pool of database connections. Each instance keeps a list of open connections." No article directly before a bare identifier: "Call `connect`."
- **Functional:** separate a type constructor from a value — "The `Ok(value)` pattern shows a successful result. A `Result` value is either `Ok` or `Err`." Write concepts (immutability, referential transparency) with no article.
- **Procedural (C, Go, Bash):** separate a pointer from the value at the address — "The function receives a pointer to a buffer. The buffer must hold at least 512 bytes."
- **Declarative (SQL, Terraform, YAML, Kubernetes):** separate a resource type from an instance — "A `Deployment` resource manages a set of pods. The `web` deployment runs three replicas." No article before a named resource: "Apply manifest `web-deployment.yaml`."
- **Systems (Rust, C memory, embedded):** make ownership/lifetime clear — "The pointer must point to an initialized region of memory. A borrow of the value must not outlive the owner."

### Edge cases

- **Identifier vs concept:** `ConnectionPool` alone is a proper noun (no article). "The `ConnectionPool` class" takes "the" (noun is "class"). "Call `initialize`" no article; "The `initialize` function" takes "the".
- **"a" vs "an":** use "an" before a vowel sound (an SQL query, an HTML element, an XML parser, an ID, an API key); "a" before a consonant sound (a URL, a Unix system, a UUID, a JSON payload, a `User` record). Match the usual pronunciation.
- **Headings, titles, table cells, UI labels:** may omit the article; the first sentence below the heading must obey the rule.
- **Product/framework names starting with "The":** `TheMovieDB` is a proper noun; the leading "The" is part of the identifier, not an article.
- **Plural types as a general statement:** "Iterators are lazy in this library" takes no article; "The iterator stops at the end of the sequence" takes "the".
- **Code samples and command lines:** do not add an article inside a code block, command, or log line; the rule applies to prose only.
- **Acronyms:** choose the article for the spoken form — "an API" (ay-pee-eye), not "a API".
- **Uncountable technical nouns:** memory, throughput, latency, state take no indefinite article — "The function allocates memory", not "a memory".

### Grammar notes

- "A" = any instance of a type; "the" = one specific identifiable item; no article = the type or concept as a whole.
- First mention uses "a" ("The method throws a `ValidationError`"); later mentions use "the" ("The `ValidationError` contains a message field").
- Proper-noun exception: a code identifier is a proper noun — no definite article directly before it ("Call `connect`", not "Call the `connect`").
- Demonstrative adjectives keep their noun: "this object", "these headers" — never "this"/"these" alone.
- Multi-word nouns: put the article before the full noun ("the retry policy object"), not inside it.
- Possessive forms replace the article: "its return value" and "the return value of the method" are both correct; not "the its return value".

### Summary checklist

- [ ] Articles and demonstrative adjectives are used correctly and not removed to shorten the text.
- [ ] No article appears before a general statement or an abstract concept.
- [ ] Short sentences use an article before each noun.
- [ ] A long series uses the article only before the first noun, unless an adjective applies to one item only.
- [ ] No definite article appears directly before a code identifier used as a proper noun.
- [ ] "a" and "an" match the spoken sound of the term that follows.
- [ ] Each demonstrative adjective is followed by a noun and refers to one clear topic.

---

## Cross-References

- **Rule 1.1** — Use approved words from the STE-Code dictionary.
- **Rule 1.3** — Use words only with their approved meanings.
- **Rule 1.5** — Technical nouns from an approved category still take an article in prose.
- **Rule 1.6** — Non-approved words are permitted only as technical code nouns.
- **Rule 1.11** — Use one term per concept.
- **Rule 3.1** — Write one topic per sentence (simplify before you connect).
- **Rule 4.1** — One topic per sentence, no abstract text.
- **Rule 4.2** — Do not omit words or use contractions.
- **Rule 4.3** — Vertical lists for complex text.
- **Rule 4.4** — Connecting words and phrases.
- **Rule 4.5** — Articles / demonstrative adjectives before a noun.
- **Rule 5.1** — Active voice in procedural steps.
- **Section 5 (Procedural Writing)** — sentence structure for step-by-step instructions.
- **Section 6 (Descriptive Writing)** — sentence structure for descriptions and explanations.
