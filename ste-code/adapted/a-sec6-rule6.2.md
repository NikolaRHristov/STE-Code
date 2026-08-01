# Rule 6.2 — Use Key Words and Key Phrases to Give Your Text a Logical Structure

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec6-rule6.2](ste-code/grouped/), Rule 6.2

## Original Rule

Key words are words that occur in a text to connect different ideas, and key phrases are phrases that have the same function.

These key words and key phrases show how information in a text is related and give the text a logical structure.

You can also use connecting words and connecting phrases to help the reader understand the logical flow of ideas in the text. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your text. The same terminology will keep your text clear and correct.

## STE-Code Adaptation

In code documentation, use key words and key phrases to connect related ideas across sentences. Key words are terms that occur multiple times in a documentation block to link different concepts together. Key phrases are multi-word expressions that serve the same connecting function.

These key words and key phrases show how information in the documentation is related and give the documentation a logical structure.

You can also use connecting words and connecting phrases to help the developer understand the logical flow of ideas. Connecting words and connecting phrases have the function of traffic signs, which tell the reader if the information is new, different, or a result of previous information. Examples of approved connecting words are: "and," "but," "then," "thus," and examples of connecting phrases are "as a result," and "at the same time."

When you use key words and key phrases, make sure that you do not change them in your documentation. The same terminology will keep your documentation clear and correct.

### Examples

The example that follows is the STE text from the adapted example for rule 6.1. In the text, you can see how the underlined key words and key phrases connect sentences and their related ideas. This makes the documentation much easier to read and understand.

**Sentence 1 and Sentence 2:**

> Sentence 1: The authentication middleware validates each incoming request.
> Sentence 2: The middleware reads the bearer token from the `Authorization` header.

Sentence 2 uses the key word "middleware" again to add more information about sentence 1.

**Sentence 2 and Sentence 3:**

> Sentence 2: The middleware reads the bearer token from the `Authorization` header.
> Sentence 3: It sends the token to the `validateToken` function in the `security` module.

Sentence 3 uses the key word "token" again and adds new information about what the middleware does with it.

**Sentence 3 and Sentence 4:**

> Sentence 3: It sends the token to the `validateToken` function in the `security` module.
> Sentence 4: The `validateToken` function decodes the JWT payload.

Sentence 4 uses the key phrase "`validateToken` function" again and gives more details about its behavior.

**Sentence 4 and Sentence 5:**

> Sentence 4: The `validateToken` function decodes the JWT payload.
> Sentence 5: It uses the `HS256` algorithm from the `jwt-signer` library.

Sentence 5 uses the key word "uses" to connect to "decodes" in sentence 4, showing the method by which the function operates.

**Sentence 8 and Sentence 9:**

> Sentence 8: If the token is expired, the middleware returns a `401 Unauthorized` response.
> Sentence 9: The response body is a JSON object.

Sentence 9 uses the key word "response" again to add more detail about what the response contains.

**Sentence 11 and Sentence 12:**

> Sentence 11: The `errorCode` field is set to `TOKEN_EXPIRED`.
> Sentence 12: If the token is malformed, the middleware returns a `401 Unauthorized` response.

Sentences 11 and 12 use the key word "token" again. Sentence 12 then introduces the alternative condition "malformed" by contrasting with the previous condition "expired."

**Sentence 14 and Sentence 15:**

> Sentence 14: The middleware also logs each failure to the audit trail.
> Sentence 15: It calls the `AuditLogger.log` static method.

Sentence 15 uses the key phrase "audit" again (from "audit trail") to connect the logging mechanism with the specific method name.

There is also a logical connection between the three groups of sentences:

- Group 1 (Sentences 1 thru 7): token validation, `validateToken`, JWT, claims, `request.auth`
- Group 2 (Sentences 8 thru 13): error responses, `401 Unauthorized`, `errorCode`, `TOKEN_EXPIRED`, `TOKEN_MALFORMED`
- Group 3 (Sentences 14 thru 17): audit trail, `AuditLogger.log`, database, `audit_events`, asynchronous write

> *The analysis above applies Rule 6.2 to the STE text from Rule 6.1, demonstrating how key words and key phrases create a logical structure across sentences.*

> **See also:** Rule 6.1 — Give Information Gradually; Rule 6.3 — Write Short Sentences. Use a Maximum of 25 Words in Each Sentence; Rule 6.4 — Use Paragraphs to Show Related Information; Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic

## Code-Domain Explanation

This rule applies to all forms of code documentation. Key words and key phrases are the threads that bind a documentation block into a single coherent unit. When a developer reads your documentation, they follow these threads from sentence to sentence. Without them, each sentence becomes an isolated statement that the reader must manually connect.

### README Files

In README files, key words establish the project identity. Use the project name, the primary library name, and the core concept (such as "middleware," "pipeline," or "plugin") as key words that repeat across sections. The installation section, usage section, and configuration section all refer to the same project name. This repetition tells the reader they are still reading about the same system.

### API Documentation

In API documentation, key words are the function names, parameter names, and return type names. Each sentence in a function description must use the function name or a pronoun that refers to it. When you describe a parameter, use the parameter name as the key word. When you describe a return value, use "returns" as the key phrase. Consistent key words prevent the reader from losing track of which parameter or which function a sentence describes.

### Docstrings

In docstrings, the first sentence introduces the function or class name as the key word. Each subsequent sentence uses that name, the parameter names, or pronouns that refer back to the subject. A docstring for `def send_message(channel, payload)` must use "send," "message," "channel," and "payload" as key words. Do not switch to synonyms like "transmit," "data," or "queue" mid-description.

### Commit Messages

In commit messages, key words are the component name, the action verb, and the affected module. A commit message that starts with "Fix race condition in connection pool" must use "connection pool" as the key phrase in the body. Do not switch to "pool," "conn pool," or "connection manager" within the same commit message.

### Error Messages

In error messages, key words are the operation name and the resource name. An error message such as "Cannot read file: permission denied" introduces "file" as the key word. Any follow-up message or recovery instruction must use "file" again, not switch to "document" or "path."

### Key Word Consistency Across Documentation Types

The same key word must carry the same meaning across all documentation types within a project. If your README calls a component the "authentication middleware," your API docs, docstrings, and commit messages must also call it the "authentication middleware." Do not rename it to "auth middleware" in one place and "auth layer" in another. This cross-document consistency is part of Rule 1.11 (one term per concept).

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python Classes)

In object-oriented documentation, use class names, method names, and property names as key words. When you describe a class hierarchy, repeat the base class name as the key word across sentences that describe derived classes.

> **Non-STE:** The `DataExporter` class writes records. The superclass manages the connection lifecycle. Instances can be configured with different output strategies.
>
> **STE:** The `DataExporter` class writes records to an output stream. The `DataExporter` class extends `BaseExporter`. Each `DataExporter` instance uses an output strategy.
>
> *Principles applied: P11, P2 — consistent use of "DataExporter" as the key word instead of switching to "superclass" and "instances."*

When you document a method chain or builder pattern, repeat the return type as the key word to show how calls connect.

> **Non-STE:** `.filter()` removes unwanted entries. The result can be mapped to a new shape. Chaining `.collect()` finalizes it.
>
> **STE:** The `filter` method returns a new `Stream`. The `Stream` object supports the `map` method. Call the `collect` method on the `Stream` to get a `List`.
>
> *Principles applied: P2, P11 — "Stream" is the key word that connects the three sentences, showing the reader the chain flows through the same type.*

### Functional (Haskell, Elixir, Clojure, Rust)

In functional documentation, use type names, function names, and data constructors as key words. Purity and immutability mean that each sentence describes a transformation. The key word is the value that flows through the transformations.

> **Non-STE:** `parse_config` reads the file and returns a result. It gets mapped to extract the database URL. The connection is opened with that value.
>
> **STE:** The `parse_config` function returns a `Result` value. Map over the `Result` value to get the database URL. Use the database URL to open a connection.
>
> *Principles applied: P11, P2 — "Result" and "database URL" are the key words that show the data flow from parsing to connection.*

In Elixir pipe chains, the key word is the data structure that passes through each pipe step.

> **Non-STE:** The input is piped through validation, then transformed, then serialized to JSON.
>
> **STE:** The `changeset` goes through the `validate` function. The validated `changeset` goes through the `transform` function. The transformed `changeset` is serialized to JSON.
>
> *Principles applied: P6, P11 — "changeset" is the key word repeated at each stage so the reader follows the data.*

### Procedural (C, Go, Bash)

In procedural documentation, use variable names, struct field names, and error codes as key words. Procedural code often has sequential steps. Each step must refer to the same variable by the same name.

> **Non-STE:** Allocate a buffer for the request. Fill the memory with the payload bytes. Send the data over the socket.
>
> **STE:** Allocate a `buffer` for the `request`. Write the `payload` bytes into the `buffer`. Send the `buffer` over the `socket`.
>
> *Principles applied: P11, P1 — "buffer" is the key word that connects allocation, writing, and sending. Do not switch to "memory" or "data."*

### Declarative (SQL, Terraform, Kubernetes YAML)

In declarative documentation, use resource names, column names, and attribute names as key words. The reader must map documentation sentences to the exact identifiers in the declarative file.

> **Non-STE:** The resource creates a virtual machine. It references the subnet defined earlier. The instance gets a public IP attached.
>
> **STE:** The `aws_instance` resource creates a virtual machine. The `aws_instance` references the `aws_subnet`. Attach an `aws_eip` to the `aws_instance`.
>
> *Principles applied: P11, P5 — "aws_instance" is the technical noun and the key word. Do not switch to "resource," "VM," or "instance."*

### Systems (Rust Ownership, C Memory)

In systems documentation, use ownership terms, lifetime names, and pointer names as key words. Memory safety documentation relies on precise key word repetition because ambiguity causes bugs.

> **Non-STE:** The function borrows the buffer. The reference is valid for the scope. The caller retains ownership of the allocated memory.
>
> **STE:** The function borrows the `buffer`. The borrow of the `buffer` is valid for lifetime `'a`. The caller keeps ownership of the `buffer`.
>
> *Principles applied: P11, P2 — "buffer" is the key word. "Borrow" is used consistently as the connecting concept. Do not switch between "borrow," "reference," and "retain ownership" for the same relationship.*

## Extended Examples

### Example 1: Configuration Documentation

> **Non-STE:** `redis.host` sets the Redis server address. The default is `localhost` on the usual port. You can override this with an environment variable.
>
> **STE:** The `redis.host` option sets the Redis server hostname. The default hostname is `localhost`. Set the `REDIS_HOST` environment variable to override the default hostname.
>
> *Principles applied: P11 — "hostname" is the key word that connects the option, the default, and the override method. Do not switch from "address" to "host" to "this."*

### Example 2: Error Handling Flow

> **Non-STE:** The parser encounters invalid JSON. An exception gets raised with the position. The caller catches it and logs the incident.
>
> **STE:** The parser finds invalid JSON. The parser raises a `ParseError` exception. The caller catches the `ParseError`. The caller logs the `ParseError` to the error log.
>
> *Principles applied: P11, P1 — "parser" and "ParseError" are the key words. Each sentence repeats them so the reader follows the error path from detection to logging.*

### Example 3: Database Migration Script

> **Non-STE:** The migration adds a `last_login` column to the users table. It's populated with a default timestamp. The operation is not reversible.
>
> **STE:** The migration adds a `last_login` column to the `users` table. The `last_login` column gets the default value `NOW()`. The migration is not reversible.
>
> *Principles applied: P11, P2 — "last_login" and "migration" are the key words. Do not switch to "it," "the operation," or "populated."*

### Example 4: CLI Tool Description

> **Non-STE:** `ste-code lint` checks documentation files. It scans for rule violations and emits a report. The tool exits with a non-zero code on failure.
>
> **STE:** The `ste-code lint` command checks documentation files. The `lint` command scans for rule violations. The `lint` command writes a report. The `lint` command exits with code 1 on failure.
>
> *Principles applied: P11, P6 — "lint" is the key word and a technical code noun. Repeat "lint" or "lint command" in every sentence so the reader always knows the subject.*

### Example 5: Test Case Description

> **Non-STE:** The test verifies that `calculate_tax` returns zero for exempt items. It exercises the edge case where quantity is zero. The expected output is `0.00`.
>
> **STE:** The test checks that `calculate_tax` returns `0.00` for exempt items. The test uses a quantity of zero. The test checks that the result is `0.00`.
>
> *Principles applied: P11, P12 — "test" is the key word. "Checks" is an approved verb from the canonical synonym table. Do not switch between "verifies," "exercises," and "expected output."*

### Example 6: Deployment Pipeline Documentation

> **Non-STE:** The CI pipeline builds the Docker image. If the build succeeds, it pushes the artifact to the registry. The deploy step pulls the container and rolls it out.
>
> **STE:** The CI pipeline builds the Docker image. The CI pipeline pushes the image to the container registry. The deploy step pulls the image from the registry. The deploy step starts the container.
>
> *Principles applied: P11, P1 — "image" is the key word that connects build, push, and pull. Do not switch to "artifact," "container," and "it."*

## Edge Cases

### Edge Case 1: Framework Name Conflicts with an Unapproved Word

Some framework names use words that are not in the STE-Code approved dictionary. For example, a framework named "Leverage" or a library named "Commence." Rule 1.5 and Rule 1.6 permit technical code nouns even when they are not approved words. When the framework name is the key word, use it as-is. Do not replace it with an STE-approved synonym.

> **Non-STE:** The Leverage framework handles task orchestration. Leverage uses a DAG to define workflows. The DAG scheduler runs tasks in dependency order.
>
> **STE:** The `Leverage` framework handles task orchestration. The `Leverage` framework uses a DAG to define workflows. The DAG scheduler runs tasks in dependency order.
>
> *Principles applied: P5, P6 — "Leverage" is a technical code noun. It is the key word even though "leverage" is not an approved STE verb. Use code formatting to mark it as a technical name.*

### Edge Case 2: Code Keyword That Conflicts with the Rule

Some programming language keywords are very short and do not carry enough meaning to serve as key words. For example, the Go keyword `go` or the Rust keyword `mut`. In these cases, use a longer descriptive key phrase that includes the keyword.

> **Non-STE:** Use `go` to start a goroutine. The goroutine runs concurrently. It finishes when the function returns.
>
> **STE:** Use the `go` keyword to start a goroutine. The goroutine runs concurrently with the caller. The goroutine stops when the function returns.
>
> *Principles applied: P5, P11 — "goroutine" is the key word, not the bare keyword `go`. The keyword itself is a technical code noun but does not work alone as a key word.*

### Edge Case 3: Generated Code Documentation

Generated code (from protobuf compilers, OpenAPI generators, or ORMs) often produces documentation with inconsistent key words. When you write documentation that references generated code, use the generated type names as key words even if they are verbose. Do not abbreviate or rename them.

> **Non-STE:** The generated `UserServiceClientImpl` connects to the gRPC server. The client stub handles serialization. The RPC call returns a response.
>
> **STE:** The generated `UserServiceClientImpl` class connects to the gRPC server. The `UserServiceClientImpl` handles serialization automatically. Call a method on the `UserServiceClientImpl` to make an RPC.
>
> *Principles applied: P11, P5 — "UserServiceClientImpl" is the key word even though it is long. Do not shorten it to "client," "stub," or "it" in critical sentences.*

### Edge Case 4: Key Words in Multi-Language Repositories

When a repository contains code in multiple languages, the same concept may have different names in each language. For example, a "dictionary" in Python is a "HashMap" in Java and a "map" in Go. In cross-language documentation (such as the top-level README), choose one key word and use it consistently. Add a note that explains the language-specific names.

> **Non-STE:** The configuration is stored in a dict in Python and a HashMap in Java. Both structures map string keys to values.
>
> **STE:** The configuration is stored in a map (Python: `dict`, Java: `HashMap`, Go: `map`). The map uses string keys. Look up values in the map by key.
>
> *Principles applied: P11, P8 — "map" is the key word for the cross-language concept. The language-specific names are given once as a clarification, not repeated as key words.*

### Edge Case 5: Key Phrases That Span Multiple Words

When a key phrase is a multi-word technical term (such as "connection pool," "rate limiter," or "retry policy"), keep the full phrase as the key unit. Do not break it into separate words or abbreviate it mid-documentation.

> **Non-STE:** The connection pool limits concurrent database connections. The pool size is configurable. Idle connections are recycled after the timeout.
>
> **STE:** The connection pool limits concurrent database connections. The connection pool size is configurable. The connection pool recycles idle connections after the timeout.
>
> *Principles applied: P11, P9 — "connection pool" is the full key phrase. Do not shorten it to "pool" or break it into "pool" and "connections" in different sentences.*

## Cross-References

This rule is part of Section 6, which governs sentence structure and text organization. The rules in this section work together to create clear, scannable documentation:

- **Rule 6.1 — Give Information Gradually:** Key words from Rule 6.2 are the mechanism by which you introduce new information gradually. Each sentence adds to the reader's understanding of the key word, one detail at a time.
- **Rule 6.3 — Write Short Sentences:** Key words help you keep sentences short. When every sentence explicitly names its subject, you avoid long sentences that cram multiple ideas into one clause.
- **Rule 6.4 — Use Paragraphs to Show Related Information:** A paragraph is a group of sentences that share a key word. The key word is the topic of the paragraph. When the key word changes, start a new paragraph.
- **Rule 6.5 — Make Sure That Each Paragraph Has Only One Topic:** The "one topic" is the key word. If you use two different key words as subjects in the same paragraph, you have two topics.

The following rules from Section 1 (Vocabulary) support Rule 6.2:

- **Rule 1.11 — One Term per Concept:** Key words work only if you use the same term for the same concept. If you switch between synonyms, the key word chain breaks.
- **Rule 1.5 — Technical Code Nouns Are Allowed:** When your key word is a class name, function name, or library name, it is a technical code noun and is permitted even if it is not in the approved dictionary.
- **Rule 1.8 — Use Standard, Well-Known Technical Nouns:** Choose key words that are standard in the domain. An unusual or invented key word weakens the logical structure because the reader does not recognize it as a key term.
- **Rule 1.9 — Prefer Short, Clear Technical Nouns:** Long key words are harder to repeat. If your key word is `AbstractAsynchronousDatabaseConnectionManager`, consider whether the documentation can use a shorter approved term.

Cross-reference to the STE-Code dictionary for approved connecting words and connecting phrases. The dictionary lists all permitted transition words such as "and," "but," "then," "thus," "also," "however," "therefore," "as a result," "at the same time," and "for example."

## Grammar Notes

### Anaphora and Cohesion in Code Documentation

In linguistics, the repetition of key words across sentences is a form of lexical cohesion. Cohesion is the grammatical and lexical linking within a text that holds it together. Rule 6.2 applies the principle of lexical cohesion to code documentation. When you repeat a key word such as "middleware," "token," or "buffer" across consecutive sentences, you create a cohesive chain that the reader can follow.

There are three types of cohesive ties that Rule 6.2 uses:

1. **Repetition:** The same word appears again. Example: "The middleware validates the request. The middleware reads the token."
2. **Pronoun reference:** A pronoun (it, they, this) refers back to the key word. Example: "The middleware validates the request. It reads the token." Use pronouns sparingly. After two sentences, repeat the full key word to prevent ambiguity.
3. **Synonym or hypernym:** An approved related term refers to the key word. Example: "The function returns a `Result`. The value contains the parsed data." The STE-Code synonym table makes this safe by restricting which synonyms are permitted.

### Topic-Comment Structure

In English grammar, most sentences have a topic (what the sentence is about) and a comment (what is said about the topic). In code documentation, the key word is the topic. Each sentence in a documentation block should have the same topic (the same key word) in subject position.

> **Non-STE:** The parser reads the input stream. Invalid tokens are detected by the lexer. An error is returned to the caller.
>
> **STE (stable topic):** The parser reads the input stream. The parser detects invalid tokens. The parser returns an error to the caller.
>
> *Grammar note: In the Non-STE version, the topic shifts from "parser" to "invalid tokens" to "an error." The reader must reconstruct that all three sentences are about the parser. In the STE version, "parser" is the topic of every sentence.*

### Connecting Words as Grammatical Signals

Connecting words ("and," "but," "then," "thus," "however," "therefore," "also") are grammatical signals that tell the reader how the new sentence relates to the previous one. In STE-Code, these connecting words appear at or near the start of a sentence:

- **"And"** signals addition: the new sentence adds more information about the same key word.
- **"But"** signals contrast: the new sentence gives information that differs from the expectation set by the previous sentence.
- **"Then"** signals sequence: the new sentence describes the next step that involves the key word.
- **"Thus"** or **"Therefore"** signals consequence: the new sentence describes a result that follows from the previous sentence.

Use connecting words at the start of sentences, not buried in the middle. The reader must see the signal before reading the sentence content.

### Avoiding Dangling Key Words

A dangling key word is a term introduced once and never repeated. The reader sees the term, expects it to be important, and then never encounters it again. This breaks the logical structure.

> **Non-STE:** The build system compiles TypeScript and bundles static assets. The output goes to the `dist/` directory. Deployment uses a Docker container.
>
> **STE (resolved):** The build system compiles TypeScript and bundles static assets. The build system writes the output to the `dist/` directory. The deploy system copies the `dist/` directory into a Docker container.
>
> *Grammar note: In the Non-STE version, "static assets" and "output" appear once and disappear. The reader does not know if "output" refers to "static assets," "TypeScript," or both. In the STE version, "build system" and the `dist/` directory are the key words repeated across sentences.*
