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
