# Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.12

## Original Rule

**Rule 1.12** You can use verbs that you can include in a technical verb category.

A technical verb is a verb term that refers to a specified concept or process and is applicable to a subject field.

The dictionary does not include technical verbs because there are too many, and each subject field uses different technical verbs for their texts.

You can find many of these technical verbs in your company glossary or terminology database.

STE gives you a list of categories, with examples, to help you:
- Select technical verbs to put in your company glossary or terminology database.
- Use technical verbs correctly.

Technical verbs must obey the same rules as other approved verbs in STE. Refer to section 3.

You can use technical verbs in procedural and descriptive texts if you can include them in one or more of these four categories.

[The original specification lists 4 main categories with subcategories: 1) Manufacturing processes (a-f subcategories); 2) Computer processes and applications (a-c subcategories); 3) Instructions and information for applicable subject fields (a-f subcategories); 4) Law and regulations.]

The technical verbs in their related categories are only examples. Rule 1.12 does not give a full list of all possible technical verbs.

If there is an approved verb in the dictionary that accurately gives the instruction or the information, use the approved verb. Do not use a technical verb if it is possible to write the same sentence with the words (verbs and other related words) that are approved in the dictionary.

Examples:

> **Non-STE:** If you detect broken wires, repair them.

("Detect" is not approved and cannot be a technical verb in this context.)

> **STE:** If you find broken wires, repair them.

But you can write:

("Detect" is the correct technical verb in this context.)

If you must use technical verbs, use only technical verbs that are correct in your context. Do not use technical verbs that are general or not clear.

Do not use a technical verb if it is not necessary. If it is possible, use a verb that is approved in the dictionary and an applicable technical noun.

"Clamp" is a technical noun, category 1, official parts information. Do not use "clamp" as a technical verb.

"Grease" is a technical noun, category 4, materials, consumables, and unwanted material. Do not use "grease" as a technical verb.

"Wire" is a technical noun, category 1, official parts information. Do not use "wire" as a technical verb.

The dictionary includes some words that, although not approved, can be technical verbs if you can put them in the specified categories.

> **STE:** Enter your password.

("Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes.)

## STE-Code Adaptation

**Rule 1.12** You can use verbs that you can include in a code-domain technical verb category.

A code-domain technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field.

The controlled terminology does not include all code-domain technical verbs because there are too many, and each project or subject field uses different technical verbs.

You can find many of these code-domain technical verbs in your project glossary or terminology database.

STE-Code gives you a list of categories, with examples, to help you:
- Select code-domain technical verbs to put in your project glossary or terminology database.
- Use code-domain technical verbs correctly.

Code-domain technical verbs must obey the same rules as other approved verbs in STE-Code. Refer to section 3.

You can use code-domain technical verbs in procedural and descriptive texts if you can include them in one or more of these four categories.

1. **Development processes**
   Terms that give instructions and information to:
   a) Write and modify code:
      compile, concatenate, import, inject, instantiate, lint, minify, optimize, polyfill, refactor, resolve, shim, stub, substitute, transpile
   b) Test and verify code:
      assert, benchmark, debug, instrument, mock, profile, spy, stub, unit-test
   c) Build and package:
      bundle, deploy, package, publish, release, tag, version
   d) Manage dependencies:
      hoist, install, link, lock, pin, update, upgrade

2. **Computer processes and applications**
   Terms that give instructions and information for:
   a) Input and output processes:
      click, copy, cut, digitize, enter, paste, press, print, scan, swipe, tap, type
   b) User interface and application operations:
      clear, close, delete, deselect, disable, drag, drag and drop, enable, encrypt, erase, filter, hide, highlight, invalidate, maximize, minimize, navigate, open, save, scroll, select, show, sort, store, submit, toggle, validate, zoom in, zoom out
   c) System operations:
      abort, authenticate, authorize, boot, cache, communicate, configure, debug, download, format, initialize, install, load, log, manage, mount, process, reboot, render, retry, serialize, synchronize, update, upgrade, upload

3. **Instructions and information for applicable subject fields**
   Terms that give instructions and information in these contexts:
   a) Algorithmic, mathematical, and data:
      aggregate, bisect, compute, concatenate, convert, count, encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, precompute, recalculate, reduce, transform, validate, verify
   b) Database and storage:
      backup, compact, flush, index, migrate, persist, query, replicate, restore, roll back, seed, shard, vacuum, write-ahead
   c) Network and communication:
      broadcast, connect, disconnect, establish, forward, handshake, intercept, listen, poll, proxy, reject, resolve, route, send, stream, timeout, tunnel, unsubscribe
   d) Security and authentication:
      authenticate, authorize, decrypt, encode, encrypt, hash, revoke, salt, sanitize, sign, validate, verify

4. **Legal and licensing terms**
   Terms that give instructions and information only for legal and regulatory texts. For example, licenses, terms of service, contributor agreements, and compliance documents.
   acknowledge, assign, comply with, conform to, disclose, enforce, explain, grant, inform, license, modify, notify, permit, regulate, sign, supersede, waive

The code-domain technical verbs in their related categories are only examples. Rule 1.12 does not give a full list of all possible code-domain technical verbs.

If there is an approved verb in the controlled terminology that accurately gives the instruction or the information, use the approved verb. Do not use a code-domain technical verb if it is possible to write the same sentence with the words (verbs and other related words) that are approved in the controlled terminology.

This adapts the spec principle: just as you must prefer the approved verb "find" over the technical verb "detect" when the context does not require the technical term, you must prefer approved verbs over code-domain technical verbs when the approved verb is sufficient.

If you must use code-domain technical verbs, use only code-domain technical verbs that are correct in your context. Do not use code-domain technical verbs that are general or not clear.

Do not use a code-domain technical verb if it is not necessary. If it is possible, use a verb that is approved in the controlled terminology and an applicable code-domain technical noun.

### Examples

> **Non-STE:** If you detect a null pointer exception, fix it.
>
> **STE:** If you find a null pointer exception, fix it.

> *Adapted from spec pair: "If you detect broken wires, repair them" → "If you find broken wires, repair them." In the spec, "detect" is not approved and cannot be a technical verb in the general maintenance context — the approved verb "find" must be used. The same principle applies in STE-Code: when describing a general debugging scenario, "detect" is not approved and "find" must be used.*

> **STE:** The intrusion detection system detects unauthorized access attempts.

> *Adapted from spec concept: "detect" becomes permissible as a technical verb in the correct context. In the spec, "detect" can be a technical verb in category 3 c), civil and military operations. In STE-Code, "detect" is a code-domain technical verb (category 3 c), network and communication) when used in a security context where it is the established technical term.*

> **STE:** Enter your API key in the configuration file.

> *Adapted from spec example: "Enter your password" — "Enter" is a technical verb, category 2 a), computer processes and applications, input and output processes. Just as "enter" is a technical verb in the spec, "enter" is a code-domain technical verb in category 2 a) in STE-Code. The word "enter" is not approved in the controlled terminology as a general verb, but it is permitted because it fits the code-domain technical verb category — exactly as the spec permits it.*

> **Non-STE:** Migrate the database schema to version 3.
>
> **STE:** Run the migration of the database schema to version 3.

> *Adapted from spec principle: prefer an approved verb with a technical noun over a technical verb when possible. In the spec, you must not use "clamp," "grease," or "wire" as technical verbs when you can use an approved verb with the technical noun. Similarly, "migrate" is a code-domain technical verb (category 3 b), database and storage), but the approved verb "run" with the code-domain technical noun "migration" is a valid alternative. The STE version uses the approved verb "run."*

---

## Code-Domain Explanation

This rule controls which verbs you can use in code documentation. Rule 1.12 applies differently to each documentation type because each type has a different audience and purpose.

### README Files

README files give a high-level description of a project. The audience includes both new users and experienced developers. README files must use approved verbs as the main verb of each sentence. Use code-domain technical verbs only when an approved verb cannot give the same meaning with the same precision.

> **Non-STE:** To bootstrap the project, execute `npm install` and then initiate the development server.
>
> **STE:** To start the project, run `npm install` and then start the development server.

> *Principles applied: P12 (canonical synonym table). "Bootstrap" and "initiate" are not approved; "start" is the approved verb. The instruction is a general project setup step, not a technical operation that needs a code-domain technical verb.*

> **Non-STE:** The build pipeline compiles TypeScript, minifies JavaScript, and deploys artifacts to the CDN.
>
> **STE:** The build pipeline compiles TypeScript, minifies JavaScript, and deploys artifacts to the CDN.

> *Principles applied: P12, Rule 1.12 categories 1 a) and 1 c). "Compile," "minify," and "deploy" are all code-domain technical verbs in their correct categories. The sentence describes specific build operations. No approved verb can replace them without losing precision.*

### API Reference Documentation

API documentation describes function signatures, parameters, return values, and side effects. API docs have the most tolerance for code-domain technical verbs because the verbs often match the method names in the code. The principle of one term per concept (Rule 1.11) is important here: if the method is named `serialize()`, the documentation must also use "serialize" to keep consistency.

> **Non-STE:** `serialize()` — This method performs serialization of the object into a byte stream.
>
> **STE:** `serialize()` — This method serializes the object to a byte stream.

> *Principles applied: P7, P13. The first version uses the technical noun "serialization" where the technical verb "serializes" is more direct and matches the method name. Do not use a technical verb as a noun or a technical noun as a verb.*

### Docstrings and Inline Comments

Docstrings must be short. Use approved verbs for general operations. Use code-domain technical verbs when the operation is specific to the code domain and an approved verb would make the text longer or less clear.

> **Non-STE:** // Utilize the cache to retrieve the user object, then verify its validity before returning.
>
> **STE:** // Get the user object from the cache, then check that it is valid before you return it.

> *Principles applied: P1 (approved words only). "Utilize," "retrieve," and "verify" are not approved. "Get," "check," and "return" are approved. The comment describes a general flow, not a specific technical operation.*

### Commit Messages

Commit messages must use the imperative mood. Use approved verbs as the main verb. Code-domain technical verbs can appear as the main verb when the commit describes a specific technical operation that only that verb can name.

> **Non-STE:** Implemented user authentication and authorization.
>
> **STE:** Add user authentication and authorization.

> *Principles applied: P4 (approved verb forms), imperative mood. "Add" is an approved verb. The past tense "Implemented" violates the imperative mood rule for commit messages.*

> **STE:** Refactor the token parser to use a recursive descent algorithm.

> *Principles applied: P12, Rule 1.12 category 1 a). "Refactor" is a code-domain technical verb. It names a specific code operation that "change" or "modify" does not capture with the same precision.*

### Error Messages

Error messages must be clear to all users, not only developers. Use approved verbs in error messages that end users see. Use code-domain technical verbs in error messages that only developers see, such as stack traces, debug logs, and internal error codes.

> **Non-STE:** (end-user error) The system failed to instantiate the configuration module due to deserialization failure.
>
> **STE:** (end-user error) Could not load the configuration file because its format is not correct.

> *Principles applied: P6, P10. "Instantiate" and "deserialization" are code-domain technical terms that an end user does not understand. Use approved verbs and plain language for end-user messages.*

> **STE:** (developer error log) Failed to deserialize config.yaml: unexpected token at line 42.

> *Principles applied: P12, Rule 1.12 category 2 c). "Deserialize" is a code-domain technical verb for a developer audience. The developer needs the precise technical term to debug the problem.*

---

## Paradigm-Specific Guidance

### Object-Oriented Programming (Java, C++, C#, Python classes)

Object-oriented documentation uses a specific set of code-domain technical verbs that describe class relationships and object lifecycles. These verbs are all in category 1 a) (write and modify code).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| instantiate | Make an instance of a class | "Instantiate the `UserService` class with the default constructor." |
| inherit | Get behavior from a parent class | "The `AdminController` inherits from `BaseController`." |
| override | Replace a parent method | "Override the `validate()` method to add custom checks." |
| extend | Add to a base class or interface | "Extend the `AbstractParser` to make a JSON parser." |
| implement | Give a body to an interface method | "Implement the `Serializable` interface." |
| encapsulate | Hide internal state | "Encapsulate the connection pool behind a getter method." |
| delegate | Forward a method call to another object | "Delegate the logging to the injected `Logger` instance." |
| inject | Supply a dependency from outside | "Inject the `Database` dependency through the constructor." |

NOTE: Do not use these verbs when an approved verb is sufficient. For example, do not say "The class encapsulates the data" when you can say "The class holds the data."

### Functional Programming (Haskell, Elixir, Clojure, Rust iterators)

Functional programming documentation uses verbs that describe transformations of immutable data. These verbs are in category 3 a) (algorithmic, mathematical, and data).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| compose | Combine functions into a pipeline | "Compose the `parse` and `validate` functions." |
| curry | Change a multi-argument function to a chain of single-argument functions | "Curry the `add` function for partial application." |
| map | Apply a function to each element | "Map the `toUpperCase` function over the list." |
| reduce | Combine elements with a binary operation | "Reduce the list with the `sum` function." |
| fold | Combine elements with an initial value | "Fold the collection from the left with a seed value of 0." |
| recurse | Call a function from within itself | "Recurse on the tail of the list." |
| memoize | Cache function results | "Memoize the `fibonacci` function to prevent recomputation." |
| lift | Move a function into a monadic context | "Lift the pure function into the `IO` monad." |

NOTE: "Map" and "reduce" are code-domain technical verbs in category 3 a). Do not confuse them with the approved verb "map" (to show a relationship) or "reduce" (to make smaller). The context must make the meaning clear.

### Procedural Programming (C, Go, Bash)

Procedural documentation uses verbs that describe memory management, control flow, and system-level operations. These verbs are in categories 2 c) and 3 a).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| allocate | Get a block of memory | "Allocate a buffer of 1024 bytes on the heap." |
| deallocate | Release a block of memory | "Deallocate the buffer before the function returns." |
| dereference | Get the value at a pointer address | "Dereference the pointer to get the struct value." |
| flush | Write buffered data to output | "Flush the output buffer after each write." |
| signal | Send a signal to a process | "Signal the worker process to stop." |

> **Non-STE:** You must free the memory that you malloced earlier in the function.
>
> **STE:** You must deallocate the memory that you allocated earlier in the function.

> *Principles applied: P11 (one term per concept). "Free" and "malloc" are C standard library function names. In documentation, use the code-domain technical verbs "allocate" and "deallocate" (category 2 c) for consistency across languages. The function names "malloc" and "free" are technical code nouns (Rule 1.5).*

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses verbs that describe the desired state of a system. The documentation describes what the configuration does, not how the system makes it happen.

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| provision | Make infrastructure available | "This resource provisions an AWS EC2 instance." |
| converge | Bring actual state to desired state | "The controller converges the cluster to the declared configuration." |
| reconcile | Compare actual state to desired state | "The operator reconciles the custom resource every 30 seconds." |
| apply | Put a configuration into effect | "Apply the Terraform plan to provision the resources." |
| destroy | Remove provisioned infrastructure | "Destroy the stack to remove all resources." |

> **Non-STE:** Terraform will make an S3 bucket for you when you execute `terraform apply`.
>
> **STE:** Terraform provisions an S3 bucket when you apply the configuration.

> *Principles applied: P12, Rule 1.12 category 3 a) and 2 c). "Provision" is a code-domain technical verb (category 3 a), algorithmic and data, or category 2 c), system operations). "Apply" is a code-domain technical verb (category 2 c). The approved verb "make" is not precise enough.*

### Systems Programming (Rust ownership, C memory, embedded)

Systems documentation uses verbs that describe ownership, borrowing, and lifetime management. These verbs are in category 2 c) and category 3 a).

| Code-Domain Technical Verb | Meaning | Example |
|---|---|---|
| borrow | Get a reference without taking ownership | "Borrow the vector immutably for the duration of the loop." |
| own | Hold exclusive control of a value | "The `String` struct owns its heap-allocated buffer." |
| drop | Run the destructor and release resources | "The value drops when it goes out of scope." |
| move | Transfer ownership to another binding | "Move the value into the closure." |
| pin | Prevent a value from moving in memory | "Pin the future to the heap before polling it." |
| acquire | Get exclusive access to a lock | "Acquire the mutex before you access the shared state." |
| release | Give up exclusive access to a lock | "Release the lock when the critical section is complete." |

> **Non-STE:** You need to clone the string to avoid a borrow checker violation.
>
> **STE:** You must clone the string to prevent a borrow conflict.

> *Principles applied: P10, P12. "Violation" is a legal term (category 4), not a systems programming term. "Conflict" or "error" is more correct for a compiler message.*

---

## Extended Examples

### Example Group A: General Verb vs. Code-Domain Technical Verb

> **Non-STE:** The script initiates a connection to the database and then commences the data migration process.
>
> **STE:** The script connects to the database and then migrates the data.

> *Principles applied: P12 (canonical synonym table + Rule 1.12). "Connect" and "migrate" are code-domain technical verbs (categories 3 c and 3 b). "Initiates" and "commences" are not approved and are not technical verbs in any category. The STE version uses the code-domain technical verbs directly, which is more concise and precise.*

### Example Group B: Technical Noun Used Incorrectly as a Verb

> **Non-STE:** You must docker the application before you ship it.
>
> **STE:** You must containerize the application before you ship it.

> *Principles applied: P7 (do not use technical nouns as verbs), P8 (use standard technical nouns). "Docker" is a brand name and a technical code noun (Rule 1.5). It is not a verb. "Containerize" is a code-domain technical verb (category 1 c), build and package). If "containerize" is not acceptable in your project glossary, use "package the application in a container" — the approved verb "package" with the technical noun "container."*

> **Non-STE:** Git the changes and then push them to the remote.
>
> **STE:** Commit the changes and then push them to the remote.

> *Principles applied: P7. "Git" is a tool name and a technical code noun. It is not a verb. "Commit" is a code-domain technical verb (category 2 b), user interface and application operations, when used in the version-control context).*

### Example Group C: When an Approved Verb Is Sufficient

> **Non-STE:** Execute the test suite to verify that the API endpoint returns the correct status code.
>
> **STE:** Run the test suite to check that the API endpoint returns the correct status code.

> *Principles applied: P1, P12 (canonical synonym table). "Execute" and "verify" are not approved. "Run" and "check" are approved. The operations are general testing steps. No code-domain technical verb category is needed. Use the approved verbs.*

### Example Group D: When Only the Code-Domain Technical Verb Works

> **Non-STE:** The function takes a string and turns it into a number, then does an operation on each item of the list.
>
> **STE:** The function parses a string to an integer, then maps the transformation over the list.

> *Principles applied: P12, Rule 1.12 categories 3 a) and 3 a). "Parse" and "map" are code-domain technical verbs. "Turns it into" and "does an operation on each item" are imprecise and wordy. The code-domain technical verbs are necessary for precision.*

### Example Group E: API Documentation — Method Name Consistency

> **Non-STE:** POST /api/users — This endpoint performs the creation of a new user record in the database.
>
> **STE:** POST /api/users — This endpoint makes a new user in the database.

> *Principles applied: P13 (do not use technical verbs as nouns), P1 (approved words). "Performs the creation" uses the technical noun "creation" instead of the approved verb "makes." Do not use the nominalized form of a verb when the verb form is available and approved.*

> **Non-STE:** `def serialize(self) -> bytes:` Returns the serialization of this object.
>
> **STE:** `def serialize(self) -> bytes:` Serializes this object and returns the result.

> *Principles applied: P13. The method is named "serialize" (a code-domain technical verb). The documentation must use the same verb form to keep one term per concept (Rule 1.11). Do not switch to the noun "serialization."*

### Example Group F: Commit Message — Imperative Mood with Technical Verbs

> **Non-STE:** Deployed the new authentication middleware and configured the rate limiter.
>
> **STE:** Deploy the new authentication middleware and set the rate limiter.

> *Principles applied: P4 (imperative mood for commit messages), P12 (canonical synonym table). "Deploy" is a code-domain technical verb (category 1 c). "Set" is an approved verb. "Configured" uses the wrong mood (past indicative instead of imperative) and "configure" is a code-domain technical verb that can be replaced by "set" in this context.*

---

## Edge Cases

### Edge Case 1: Framework or Tool Name That Is Also a General Verb

Some framework names are also common English verbs. For example, "Express" (the Node.js framework) is also a general verb meaning "to show" or "to state." "Go" (the programming language) is also a general verb. "C" (the language) sounds like "see."

RULE: When a framework or tool name is also a general verb, always use the framework name as a technical code noun (Rule 1.5). Add a qualifier if the context does not make the meaning clear.

> **Non-STE:** Express the route handler as a middleware function.
>
> **STE:** Write the route handler as an Express middleware function.

> *Principles applied: P6, Rule 1.5. "Express" as a verb meaning "to state" is not approved. As a proper noun, "Express" is a technical code noun. The STE version makes the meaning clear by adding the framework name as a qualifier.*

### Edge Case 2: Code Keyword That Conflicts with an Approved Verb

Some programming language keywords are the same as approved STE-Code verbs. For example, `return` (keyword) vs. "return" (approved verb meaning "to give back"). `import` (keyword) vs. "import" (code-domain technical verb, category 1 a). `class` (keyword) vs. "class" (technical code noun).

RULE: When a code keyword and an approved verb have the same spelling, use context to make the meaning clear. In inline code formatting, the keyword appears in monospace. In prose, the approved verb or technical verb appears in normal text.

> **Non-STE:** The function returns a promise that you must await to get the result.
>
> **STE:** The function returns a `Promise` that you must `await` to get the result.

> *Principles applied: P6, Rule 1.5. "Returns" is an approved verb. "Promise" and "await" are JavaScript keywords and technical code nouns. Use monospace formatting for keywords to distinguish them from approved verbs.*

> **Non-STE:** Import the module at the top of the file, then return the configured instance.
>
> **STE:** Import the module at the top of the file. Then return the set instance.

> *Principles applied: P12, Rule 1.12 category 1 a). "Import" is a code-domain technical verb. "Return" is an approved verb. "Configured" is a code-domain technical verb that can be replaced by the approved verb "set" in this context.*

### Edge Case 3: Generated Code and Automated Documentation

Generated code and auto-generated documentation do not always obey STE-Code rules. Generated code comes from tools (compilers, code generators, OpenAPI spec generators, protobuf compilers). You cannot control the word choices in generated output.

RULE: Rule 1.12 applies to documentation that a human writes. Generated code and auto-generated documentation are exempt, but you must write any surrounding explanation in STE-Code. When you refer to a generated symbol name, treat it as a technical code noun (Rule 1.5).

> **Non-STE:** The generated client library exposes a `serializeToJson()` method that leverages the native JSON encoder.
>
> **STE:** The generated client library has a `serializeToJson()` method that uses the native JSON encoder.

> *Principles applied: P1, P12. "Exposes" and "leverages" are not approved. "Has" and "uses" are approved. The method name `serializeToJson()` is a technical code noun — do not change it even though "serialize" is a code-domain technical verb. The method name is generated and fixed.*

### Edge Case 4: CLI Command Names as Verbs

Command-line interface (CLI) commands often use technical verbs as their names. For example, `git commit`, `docker build`, `kubectl apply`, `npm install`. When you document CLI commands, the command name is a technical code noun. The verb that describes the action can be an approved verb.

> **Non-STE:** Execute `docker build` to containerize the application, then execute `docker push` to upload the image.
>
> **STE:** Run `docker build` to containerize the application, then run `docker push` to upload the image.

> *Principles applied: P1, P12. "Execute" is not approved. "Run" is approved. The commands `docker build` and `docker push` are technical code nouns. "Containerize" and "upload" are code-domain technical verbs (categories 1 c and 2 c).*

### Edge Case 5: Multi-Word Technical Verbs

Some code-domain technical verbs have more than one word. For example, "roll back" (category 3 b), "drag and drop" (category 2 b), "zoom in" and "zoom out" (category 2 b), "write-ahead" (category 3 b). These multi-word verbs are permitted as single lexical units. Do not split them or substitute a different verb.

RULE: Keep the multi-word technical verb as one unit. Do not insert words between its parts. Use the full form every time you refer to the operation.

> **Non-STE:** You must roll the database migration back if the validation fails.
>
> **STE:** You must roll back the database migration if the check fails.

> *Principles applied: P11 (one term per concept), P1 (approved words). "Roll back" is a single code-domain technical verb (category 3 b). Do not split it with an object. "Validation" is a technical noun form; use the approved verb "check" instead. In English, phrasal verbs can be split ("roll it back"), but STE-Code does not permit splitting of multi-word technical verbs to prevent ambiguity.*

---

## Cross-References

This rule connects to several other STE-Code rules. Read these rules together to make sure that your documentation obeys all of them.

| Related Rule | Relationship to Rule 1.12 |
|---|---|
| **Rule 1.1** — Use approved words from the dictionary | You must try approved words before you use a code-domain technical verb. If an approved verb gives the same meaning, you must use the approved verb. |
| **Rule 1.2** — Use words only as their specified part of speech | A word that is approved as a noun cannot be a code-domain technical verb. Check the controlled terminology before you use a word as a verb. |
| **Rule 1.5** — Technical code nouns are allowed | Tool names, framework names, and CLI commands are technical code nouns (not verbs). Do not use them as code-domain technical verbs. |
| **Rule 1.7** — Do not use technical nouns as verbs | This is the inverse of Rule 1.12. Rule 1.7 prevents you from using "Docker" as a verb. Rule 1.12 permits "containerize" as a code-domain technical verb. |
| **Rule 1.11** — One term per concept | When you choose a code-domain technical verb, use it the same way everywhere. Do not use "serialize" in one file and "marshal" in another for the same concept. |
| **Rule 1.13** — Do not use technical verbs as nouns | If a word is a code-domain technical verb, do not use its nominalized form. Prefer "serialize" (verb) over "serialization" (noun) when the sentence calls for a verb. Use the approved verb with the technical noun when the sentence calls for a noun. |
| **Section 3** — Verb rules (tense, mood, voice) | Code-domain technical verbs must obey the same tense, mood, and voice rules as approved verbs. Use the imperative mood for procedures. Use the active voice. Do not use the "-ing" form as the main verb. |

---

## Grammar Notes

### Code-Domain Technical Verbs and the Imperative Mood

Procedural documentation (instructions, setup guides, API usage examples) must use the imperative mood. Code-domain technical verbs in the imperative mood follow the same rules as approved verbs.

> **STE:** Compile the source files before you run the tests.
> *"Compile" is a code-domain technical verb (category 1 a) in the imperative mood.*

> **STE:** Deploy the application to the staging environment.
> *"Deploy" is a code-domain technical verb (category 1 c) in the imperative mood.*

Do not use the "-ing" form of a code-domain technical verb as the main verb of a procedural sentence.

> **Non-STE:** Compiling the source files and then deploying to staging.
>
> **STE:** Compile the source files. Then deploy the application to staging.

> *Principles applied: P4 (approved verb forms). The "-ing" form is not an approved verb form for procedures. Use the imperative form.*

### Code-Domain Technical Verbs in Descriptive Texts

Descriptive documentation (architecture overviews, design documents, project descriptions) uses the indicative mood. Code-domain technical verbs in the indicative mood follow standard subject-verb agreement.

> **STE:** The build system compiles TypeScript, minifies JavaScript, and deploys static assets.
> *All three verbs ("compiles," "minifies," "deploys") are code-domain technical verbs in the third-person singular indicative form.*

> **STE:** The database engine indexes the new columns during the migration.
> *"Indexes" is a code-domain technical verb (category 3 b) in the indicative mood.*

### Prefer the Active Voice

Use the active voice for code-domain technical verbs. The passive voice is permitted in descriptive texts when the agent is not important, but the active voice is always clearer.

> **Non-STE:** The configuration file is parsed by the bootstrap module during initialization.
>
> **STE:** The bootstrap module parses the configuration file when it starts.

> *Principles applied: active voice, P12 (canonical synonym table). "Parses" is a code-domain technical verb (category 3 a). "Starts" is an approved verb. The passive construction "is parsed by" is wordier and less direct than the active "parses."*

### Code-Domain Technical Verbs and the Infinitive

When a code-domain technical verb follows another verb, use the full infinitive form ("to" + verb). Do not drop the "to."

> **Non-STE:** You need serialize the object before you send it.
>
> **STE:** You must serialize the object before you send it.

> *Principles applied: P4 (approved verb forms), grammar. "Need" is not approved; use "must." The full infinitive "to serialize" is required after some constructions, but "must" takes the bare infinitive ("must serialize"), which is correct.*

### Tense Restrictions for Code-Domain Technical Verbs

Code-domain technical verbs obey the same tense restrictions as approved verbs. Use only the tenses that STE-Code permits:

- Imperative (for procedures): "Compile the source files."
- Simple present (for descriptive texts): "The compiler optimizes the output."
- Simple past (for reporting completed actions): "The test suite found three failures."
- Simple future (for results and outcomes): "The deployment will complete in five minutes."

Do not use the present perfect, past perfect, or continuous tenses with code-domain technical verbs.

> **Non-STE:** The system has been indexing the database for ten minutes.
>
> **STE:** The system indexes the database. The index operation started ten minutes ago.

> *Principles applied: P4, tense restrictions. The present perfect continuous "has been indexing" is not permitted. Use the simple present with a time reference in a separate sentence.*
