# Rule 1.8 — Use Technical Nouns That Are Approved in Your Company, Industry, or Subject Field

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.8

## Original Rule

**Rule 1.8** Use technical nouns that are approved in your company, industry, or subject field.

If your company, industry, or subject field, has an approved technical noun for a system, component, part, or process, use that technical noun. Usually, such technical nouns are included in official parts information and in company documentation.

Example:

> **STE:** The front panel of the phone has a touchscreen and a home button.

("Touchscreen" and "home button" are technical nouns that are approved in your company, industry, or subject field.)

## STE-Code Adaptation

**Rule 1.8** Use code-domain technical nouns that are approved in your project, company, industry, or subject field.

If your project, company, industry, or subject field has an approved code-domain technical noun for a class, module, function, method, variable, component, or process, use that code-domain technical noun. Usually, such code-domain technical nouns are included in your project glossary, API documentation, coding standards, or company documentation.

Do not invent your own names for items that already have established names in your codebase or domain. Consistency with the approved terminology helps all readers understand the documentation.

### Examples

> **STE:** The dashboard page has a UserTable component and a FilterPanel component.

This adapts the spec example: "The front panel of the phone has a touchscreen and a home button." Just as "touchscreen" and "home button" are technical nouns approved in the industry, "UserTable" and "FilterPanel" are code-domain technical nouns approved in the project. The reader recognizes these exact names from the codebase.

> **Non-STE:** The account controller manages login and user profile operations.
> **STE:** The AccountController manages authentication and user profile operations.

This adapts the spec principle that you must use the approved term. "AccountController" is the code-domain technical noun that is approved in the project (the actual class name in the codebase). The non-STE version uses "account controller," which is not the approved name. Just as you would not replace "touchscreen" with "finger screen" in the spec example, you must not replace "AccountController" with an invented name.

---

## Code-Domain Explanation

Rule 1.8 requires that you use the standard, approved technical noun for each concept in your documentation. This rule is not about whether a word is a technical noun (Rule 1.5 covers that). This rule is about which technical noun to choose when more than one name exists for the same concept. The rule applies differently to each documentation type because the degree of available authority changes.

### README Files

README files introduce a project to new users. The project glossary, API docs, and codebase define the approved technical nouns. Use those exact names. Do not substitute descriptive phrases for the approved class names, module names, or component names.

> **Non-STE:** The data display widget shows user information in a table format.
> **STE:** The UserTable component shows user information.

> *Principles applied: P8 (use standard, well-known technical nouns), P11 (one term per concept). "UserTable" is the approved code-domain technical noun from the codebase. "Data display widget" is an invented description that no reader can map to the code. The STE version uses the exact class name so readers can find it in the source code.*

### API Reference Documentation

API documentation describes endpoints, parameters, return types, and error codes. The API spec and the source code define the approved names. Use the names from the spec — never substitute your own variant even if it seems clearer.

> **Non-STE:** The user retrieval endpoint sends back a user data object.
> **STE:** The `GET /users/:id` endpoint returns a `User` object.

> *Principles applied: P8, P11, P5 (technical code nouns are allowed). `GET /users/:id` and `User` are the approved technical nouns from the API spec and the type system. "User retrieval endpoint" and "user data object" are invented phrases that do not match the spec. Readers who search for "user retrieval" will not find the endpoint. Use the exact names.*

### Docstrings and Inline Comments

Docstrings explain what a function, class, or module does. Use the approved names from the codebase and the project glossary. When a standard industry term exists (for example, "observer pattern"), use it rather than a homegrown description.

> **Non-STE:** This class listens to changes on the data holder and runs callback functions when the data changes.
> **STE:** This class implements the observer pattern. It watches a `Subject` and notifies registered `Observer` instances.

> *Principles applied: P8, P11. "Observer pattern," "Subject," and "Observer" are approved technical nouns from the design pattern literature and the codebase. "Listens to changes" and "data holder" are non-standard descriptions. Use the industry-approved name so readers recognize the design pattern immediately.*

### Commit Messages

Commit messages record changes to the codebase. Use the approved names for files, classes, functions, and components exactly as they appear in the source tree. A commit message that invents names for code elements is not traceable.

> **Non-STE:** Refactor the auth helper to use the new token validator.
> **STE:** Refactor `AuthService` to use `JwtValidator`.

> *Principles applied: P8, P11, P5. `AuthService` and `JwtValidator` are the approved file and class names from the project. "Auth helper" and "token validator" are imprecise descriptions. A developer reading the commit log must be able to map the message to the actual code change. Exact names make that possible.*

### Error Messages

Error messages report failures to users and developers. Use the approved component names, not generic descriptions. When a system component fails, the error message must name the component that failed.

> **Non-STE:** Error: The storage system could not process the request.
> **STE:** Error: `PostgreSQLConnectionPool` could not execute the query. The pool is exhausted.

> *Principles applied: P8, P11. `PostgreSQLConnectionPool` is the approved component name from the configuration and source code. "Storage system" could mean the database, the cache, the file system, or the object store. The STE version gives the exact component name so the operations team knows which system failed and which configuration to check.*

---

## Paradigm-Specific Guidance

### Object-Oriented Programming (Java, C++, C#, Python classes)

OOP documentation has many names for the same concept: class names, interface names, design pattern names, and architectural terms. Rule 1.8 requires that you use the name from the most authoritative source. For class and interface names, the source code is the authority. For design patterns, the published pattern literature is the authority.

| Concept | Non-Standard Name (avoid) | Approved Technical Noun (use) | Authority |
|---|---|---|---|
| A class that manages user data | user manager, user handler, user service | `UserRepository` | Source code (class name) |
| A method that saves an entity | save method, persist operation, store function | `save()` | Source code (method name) |
| The Factory pattern | maker pattern, creator class, object builder | Factory pattern | Design pattern literature |
| Dependency injection | wiring, hookup, service plumbing | Dependency injection | Industry terminology |
| Model-View-Controller | display pattern, screen architecture | MVC (Model-View-Controller) | Architectural pattern literature |
| An interface for data access | data layer, DB interface, storage contract | `IRepository<T>` | Source code (interface name) |

> **Non-STE:** The user maker class is a singleton. The display part uses a watcher to update the screen when the data part changes.
> **STE:** The `UserFactory` class is a Singleton. The `View` uses an `Observer` to update the UI when the `Model` changes.

> *Principles applied: P8, P11. "UserFactory" is the approved class name (source code). "Singleton," "View," "Observer," and "Model" are approved technical nouns from design pattern literature and MVC terminology. "User maker," "display part," "watcher," and "data part" are invented names. The STE version uses the standard terms that every OOP developer recognizes.*

### Functional Programming (Haskell, Elixir, Clojure, Rust iterators)

Functional programming documentation uses mathematical and type-theoretic names. These names are exact and have precise definitions. Do not replace them with informal descriptions even if the description seems clearer.

| Concept | Non-Standard Name (avoid) | Approved Technical Noun (use) | Authority |
|---|---|---|---|
| A type that wraps an optional value | nullable wrapper, maybe container | `Option` / `Maybe` | Language standard library |
| A computation with effects | effectful wrapper, IO box | `IO` monad | Language standard library |
| Function composition | chaining, piping, sequencing | Function composition | Mathematical terminology |
| Pattern matching | destructuring, case analysis, switch on types | Pattern matching | Language specification |
| Immutable data | unchangeable data, frozen data | Immutable data | Functional programming literature |
| Higher-order function | function parameter, callback function | Higher-order function | Mathematical terminology |

> **Non-STE:** The maybe-type holds an optional value. You can chain functions on it without checking for empty values.
> **STE:** The `Option` monad holds an optional value. You can compose functions on it without checking for `None`.

> *Principles applied: P8, P11, P5. `Option` and `None` are the approved type and variant names from the language standard library. "Monad" is the approved technical noun from category theory and functional programming. "Maybe-type," "chain functions," and "empty values" are informal descriptions. Use the exact names from the language, the library, and the mathematical foundation.*

### Procedural Programming (C, Go, Bash)

Procedural documentation uses names for memory structures, system calls, and standard library functions. These names are defined by the language specification and the POSIX standard. Use the exact names from the authoritative source.

| Concept | Non-Standard Name (avoid) | Approved Technical Noun (use) | Authority |
|---|---|---|---|
| Dynamic memory allocation | heap allocation, memory request, RAM grab | `malloc` | C standard library |
| A data structure grouping | record, compound type, data bundle | `struct` | Language specification |
| A reference to memory | address variable, memory reference, location tracker | `pointer` | Language specification |
| A concurrent execution unit | light thread, green process, concurrent function | `goroutine` (Go) | Language specification |
| Standard output stream | console, terminal, screen output | `stdout` | POSIX standard |
| Environment variables | config vars, system settings, shell vars | Environment variables | POSIX standard |

> **Non-STE:** The C program uses heap allocation to get memory for the data record. It then uses a memory address to pass the record to the processing function.
> **STE:** The C program uses `malloc` to allocate memory for the `struct`. It then uses a `pointer` to pass the `struct` to the processing function.

> *Principles applied: P8, P11, P5. `malloc`, `struct`, and `pointer` are approved technical nouns from the C language specification. "Heap allocation," "data record," and "memory address" are descriptions — they are not wrong, but they are not the standard names. Use the standard names that appear in the source code and in the language documentation.*

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses resource type names, keyword names, and configuration block names. These names are defined by the spec, the provider documentation, or the API reference. Use the exact names — do not paraphrase them.

| Concept | Non-Standard Name (avoid) | Approved Technical Noun (use) | Authority |
|---|---|---|---|
| A Terraform virtual machine resource | VM block, compute instance, server resource | `aws_instance` | Terraform provider docs |
| A Kubernetes pod spec | container group, deployment unit, pod config | `Pod` / `PodSpec` | Kubernetes API reference |
| An SQL SELECT query | data fetch, retrieval query, read statement | `SELECT` statement | SQL standard |
| A database transaction | atomic block, all-or-nothing unit, DB transaction | `TRANSACTION` | SQL standard |
| A Terraform output value | export block, return value, output config | `output` | Terraform language docs |
| A Kubernetes namespace | isolation zone, project space, resource group | `Namespace` | Kubernetes API reference |

> **Non-STE:** The Terraform config declares a compute instance in the AWS cloud. It then exports the IP number.
> **STE:** The Terraform configuration declares an `aws_instance` resource. It then exports the `public_ip` with an `output` block.

> *Principles applied: P8, P11, P5. `aws_instance`, `public_ip`, and `output` are approved technical nouns from the Terraform provider documentation and the HCL language specification. "Compute instance," "AWS cloud," "IP number," and "exports" are descriptions that do not match the actual resource type names or attribute names. Users who copy "compute instance" into a Terraform file will get a syntax error. Use the exact resource type name.*

### Systems Programming (Rust ownership, C memory, embedded)

Systems documentation uses names for memory regions, hardware components, and ownership concepts. These names have precise meanings defined by the language specification, the hardware reference manual, or the operating system standard.

| Concept | Non-Standard Name (avoid) | Approved Technical Noun (use) | Authority |
|---|---|---|---|
| Rust ownership transfer | move operation, ownership handoff, transfer | `move` semantics | Rust language reference |
| Rust borrowing | reference pass, temporary access, pointer loan | `borrow` | Rust language reference |
| A memory region for dynamic allocation | dynamic memory, free store, malloc area | `heap` | Operating system / language spec |
| A memory region for automatic allocation | automatic memory, call stack, function memory | `stack` | Operating system / language spec |
| A mutual exclusion lock | thread lock, access guard, concurrency lock | `Mutex` | Language standard library |
| An interrupt service routine | interrupt function, handler code, ISR function | `ISR` (Interrupt Service Routine) | Hardware reference manual |

> **Non-STE:** Rust moves ownership when you give a value to another variable. You can also lend a reference without giving ownership.
> **STE:** Rust applies `move` semantics when you assign a value to another binding. You can also `borrow` a reference without transferring ownership.

> *Principles applied: P8, P11, P5. `move` and `borrow` are the approved technical nouns from the Rust language reference. "Give a value" and "lend a reference" are English paraphrases that do not match the language specification. Readers who learn Rust from the official documentation expect the terms "move" and "borrow." Use these terms so your documentation matches the language reference.*

---

## Extended Examples

### Example Group A: Class Name vs. Descriptive Phrase

> **Non-STE:** The payment processing handler checks the card information and talks to the bank system to complete the transaction.
> **STE:** The `PaymentProcessor` validates the `CardDetails` and sends a request to the `BankGateway` to complete the `Transaction`.

> *Principles applied: P8 (use standard, well-known technical nouns), P11 (one term per concept), P5 (technical code nouns). `PaymentProcessor`, `CardDetails`, `BankGateway`, and `Transaction` are the approved class names from the source code. "Payment processing handler," "card information," "bank system," and "the transaction" are descriptions. The STE version uses the exact class names so every reader can find these classes in the codebase.*

### Example Group B: Pattern Name vs. Homemade Description

> **Non-STE:** The class uses a setup where one object notifies many waiting objects when its state changes.
> **STE:** The class implements the Observer pattern. The `Subject` notifies all registered `Observer` instances when its state changes.

> *Principles applied: P8, P11, P9 (prefer short, clear technical nouns). "Observer pattern" is the industry-approved name from the Gang of Four design patterns. "Subject" and "Observer" are the approved role names from the pattern. "A setup where one object notifies many waiting objects" is a long description that no reader will recognize as the Observer pattern. The STE version uses the standard name so readers immediately understand the design.*

### Example Group C: Protocol Name vs. Generic Description

> **Non-STE:** The service uses secure web communication to send data between the client and the server.
> **STE:** The service uses HTTPS to send data between the client and the server.

> *Principles applied: P8, P9. "HTTPS" is the approved technical noun from the IETF standards. "Secure web communication" is a description that could refer to HTTPS, TLS, SSH, or a VPN. The STE version uses the exact protocol name so readers know which standard applies and can refer to the RFC.*

### Example Group D: Framework Feature Name vs. Informal Description

> **Non-STE:** React's function that manages state and side effects runs after the component draws on the screen.
> **STE:** React's `useEffect` hook runs after the component renders.

> *Principles applied: P8, P11, P5. `useEffect` is the approved API name from the React documentation. "Hook" is the approved category name for this type of function. "Render" is the approved term for the drawing phase. "Function that manages state and side effects" and "draws on the screen" are informal descriptions. Use the exact API names and React terminology.*

### Example Group E: Algorithm Name vs. Plain-Language Description

> **Non-STE:** The search function splits the sorted list in half again and again until it finds the target value or runs out of items.
> **STE:** The `binarySearch` function applies the binary search algorithm to the sorted array. It returns the index of the target value or `-1` if the value is not present.

> *Principles applied: P8, P11, P9. "Binary search algorithm" is the approved technical noun from computer science literature. "Splits the sorted list in half again and again" is a description of how binary search works, but it does not name the algorithm. A reader who knows binary search will recognize the name immediately. A reader who does not can look up "binary search" in any algorithms textbook. A description cannot be searched for as easily as a standard name.*

### Example Group F: Configuration Key vs. Generic Description

> **Non-STE:** Set the database location setting to point to your local database server address.
> **STE:** Set the `DATABASE_URL` environment variable to your local PostgreSQL connection string.

> *Principles applied: P8, P11, P5. `DATABASE_URL` is the approved configuration key name from the project's `.env.example` file. "Database location setting" is a description that does not tell the user which key to set. The STE version uses the exact key name so the user can copy it directly into their configuration file. "PostgreSQL" is the approved database name (not "database server"). "Connection string" is the approved technical noun for the value format.*

---

## Edge Cases

### Edge Case 1: When the Codebase Uses a Non-Standard Name for a Standard Concept

Sometimes a codebase names a class, module, or function with a term that is not the industry standard. For example, a codebase might call a repository class `DataStore` instead of `Repository`, or a factory class `Maker` instead of `Factory`. Which name does Rule 1.8 require?

RULE: The codebase name is the primary authority for code elements. If the class is named `DataStore`, use `DataStore` in documentation that refers to that specific class. However, you may also mention the industry-standard name to help readers understand the concept.

> **STE:** The `DataStore` class (a Repository pattern implementation) manages all database access.

> *Principles applied: P8, P11. `DataStore` is the approved name from the source code. "Repository pattern" is the industry-approved name. Use both: the codebase name for traceability and the industry name for comprehension. Do not replace the codebase name with the industry name — that breaks the link between the documentation and the code.*

### Edge Case 2: When Two Industry Standards Compete for the Same Concept

Some concepts have two accepted names from different communities. For example, "callback" vs. "handler" vs. "listener" (all refer to a function that responds to an event). "Hash map" vs. "dictionary" vs. "associative array" (all refer to a key-value data structure). "Argument" vs. "parameter" (both refer to inputs to a function, with a narrow technical distinction that most documentation ignores).

RULE: Choose one name and use it consistently (Rule 1.11). Register your choice in the project glossary. Prefer the name that matches your language ecosystem: Java projects use "map," Python projects use "dictionary," JavaScript projects use "object" or "Map."

> **Non-STE:** The callback handler receives the event and passes it to the listener function.
> **STE:** The `EventHandler` callback receives the event and passes it to the registered listener.

> *Principles applied: P11, P8. The non-STE version uses "callback," "handler," and "listener" interchangeably. The STE version assigns each term a distinct meaning: `EventHandler` is a class, "callback" is the function type, and "listener" is the registered consumer. Register these distinctions in the project glossary.*

### Edge Case 3: When the Approved Name Is an Acronym or Initialism

Many standard technical nouns are acronyms or initialisms: API, JSON, SQL, HTML, CSS, HTTP, JWT, ORM, MVC. Rule 1.8 requires that you use the approved acronym. However, you must also define the acronym at its first use in each document unless the audience is known to understand it.

> **STE:** The application programming interface (API) returns JavaScript Object Notation (JSON). The JSON Web Token (JWT) in the response header identifies the user.

> *Principles applied: P8, P11. Define each acronym at first use. After the definition, use only the acronym. Do not alternate between the full form and the acronym — that suggests two different concepts (violates P11).*

> **Non-STE:** The application programming interface returns JSON. The API also sends a JWT (JSON Web Token).
> **STE:** The API returns JSON. The API also sends a JWT.

> *Principles applied: P11. After the first definition, use only the acronym. "Application programming interface" and "API" refer to the same concept — using both suggests a distinction that does not exist.*

### Edge Case 4: When a Framework Renames a Standard Concept

Frameworks sometimes rename standard concepts with project-specific vocabulary. React calls its UI building blocks "components." Vue calls them "components." Angular calls them "components." All three use the same term — no conflict. But Django calls them "views" and "templates." Ruby on Rails calls them "views" and "partials." Phoenix calls them "views" and "templates."

RULE: In documentation for a specific framework, use the framework's approved name. In general documentation (not framework-specific), use the most widely recognized name and mention the framework variant if necessary.

> **Non-STE:** (Django documentation) The component renders the HTML and the controller handles the request.
> **STE:** (Django documentation) The view renders the HTML and the view handles the request.

> *Principles applied: P8, P11. Django uses "view" for both the rendering function and the request handler. Using "component" and "controller" (terms from other frameworks) in Django documentation confuses Django developers. Use the framework's own terminology.*

> **STE:** (General documentation) The framework's controller (called a "view" in Django and a "handler" in Phoenix) processes the request.

> *Principles applied: P8, P11. General documentation uses the most common term ("controller") and acknowledges the framework-specific variants in parentheses. This helps readers from different ecosystems understand the concept.*

### Edge Case 5: When the Approved Name Changes During a Migration or Refactor

During migrations and refactors, the codebase may have two names for the same concept: the old name (still in some files) and the new name (in the refactored files). Documentation must choose which name to use.

RULE: Use the target name (the name after the migration is complete). If you must mention the old name (for example, in a migration guide), use it only in quoted text (Rule 1.5, category 10) and always with a note that it is deprecated.

> **STE:** The `UserService` class (formerly `UserManager`) handles user authentication. DEPRECATED: `UserManager` is the old name. Use `UserService` in new code.

> *Principles applied: P8, P11. `UserService` is the approved target name. `UserManager` is the deprecated name, shown only for migration context. After the migration is complete, remove all references to `UserManager` from the documentation.*

### Edge Case 6: Package Managers and Ecosystem-Specific Name Variants

The same package may have different names in different package registries. For example, `lodash` (npm) vs. `lodash` (RubyGems — a different library), `python-dotenv` (PyPI) vs. `dotenv` (npm), `org.apache.commons:commons-lang3` (Maven) vs. `apache-commons-lang` (system package).

RULE: In documentation for a specific ecosystem, use the name from that ecosystem's registry. Include the registry-qualified name (for example, `pip install python-dotenv`) in installation instructions. In general documentation, use the most common name and note ecosystem variants.

> **Non-STE:** Install the dotenv package to load environment variables.
> **STE:** Install the `python-dotenv` package with `pip` to load environment variables.

> *Principles applied: P8, P11. "Dotenv package" is ambiguous — it could be the npm package, the PyPI package, or the Ruby gem. The STE version gives the exact PyPI package name (`python-dotenv`) and the exact tool (`pip`). This instruction can be copied directly into a terminal.*

---

## Cross-References

This rule connects to several other STE-Code rules. Read these rules together to make sure that your documentation obeys all of them.

| Related Rule | Relationship to Rule 1.8 |
|---|---|
| **Rule 1.1** — Use approved words from the dictionary | Rule 1.1 controls common vocabulary. Rule 1.8 controls which technical noun to choose among competing candidates. When a common word and a technical noun both name the same concept, use the technical noun from the approved source. |
| **Rule 1.2** — Use words only as their specified part of speech | The approved technical noun is a noun. Do not use it as a verb or an adjective that lacks a head noun. See also Rule 1.7 for the full restriction on noun verbing. |
| **Rule 1.3** — Use words only with their approved meanings | The approved technical noun has the meaning registered in your project glossary or the industry standard. Do not assign it a different meaning even if the word seems clearer with that meaning. |
| **Rule 1.5** — Technical code nouns are allowed | Rule 1.5 defines which words can be code-domain technical nouns. Rule 1.8 tells you to choose the standard, well-known code-domain technical noun when more than one candidate exists. |
| **Rule 1.6** — Non-approved words only when they are technical code nouns | When a concept has both an approved code-domain technical noun and a common English description, Rule 1.8 requires the technical noun. Rule 1.6 reinforces this by forbidding the common description if it is not an approved word. |
| **Rule 1.7** — Do not use technical nouns as verbs | The approved technical noun that you choose under Rule 1.8 must stay as a noun. Rule 1.7 forbids using it as a verb regardless of which name you chose. |
| **Rule 1.9** — Prefer short, clear technical nouns | When two approved technical nouns both name the same concept, Rule 1.9 breaks the tie: choose the shorter one. Rule 1.8 provides the set of approved candidates. Rule 1.9 ranks them. |
| **Rule 1.10** — No slang, jargon, or regional terms | Slang and jargon are often invented names for standard concepts. Rule 1.10 forbids them. Rule 1.8 tells you to replace them with the standard, approved technical noun. The two rules work together: Rule 1.10 removes the non-standard name; Rule 1.8 supplies the standard replacement. |
| **Rule 1.11** — One term per concept | Rule 1.11 requires consistency: one concept, one name. Rule 1.8 provides the decision process for choosing that one name. When you choose an approved technical noun under Rule 1.8, Rule 1.11 guarantees that you use it everywhere. |
| **Rule 1.12** — Technical verbs are allowed | Some concepts have both a technical noun and a technical verb form (for example, "cache" is both a noun and a verb). Rule 1.8 applies to the noun form. Rule 1.12 applies to the verb form. When you use the verb form, choose the approved technical verb — but when you name the concept in documentation, use the approved technical noun. |
| **Rule 1.14** — Use American English spelling | When the industry-standard technical noun has different spellings in different English variants (for example, "color" vs. "colour" in CSS property names), use the spelling from the specification. CSS uses "color" (American English). HTML uses "colour" in some deprecated attributes. Follow the specification, not Rule 1.14, for spec-defined names. For all other technical nouns, use American English spelling. |

---

## Grammar Notes

### The Authority Hierarchy for Technical Noun Selection

When more than one name exists for the same concept, choose the name from the most authoritative source. The authority hierarchy is:

1. **The source code** (class names, function names, file names, variable names, type names)
2. **The language specification** (keyword names, standard library names, built-in type names)
3. **The framework or library documentation** (API names, component names, hook names, configuration key names)
4. **The project glossary** (project-specific terms registered under Rule 1.5)
5. **The industry standard** (design pattern names, protocol names, algorithm names, architecture names)
6. **The company documentation** (internal system names, service names, team names)

When a conflict exists (for example, the source code calls it `DataStore` but the industry standard calls it `Repository`), use the higher-ranked source for code elements and the industry standard for conceptual explanations. Never mix names from different levels for the same concept in the same document.

> **STE:** The `DataStore` class provides the repository layer. It implements the Repository pattern from domain-driven design.

> *Explanation: `DataStore` (source code, level 1) is the code element name. "Repository pattern" (industry standard, level 5) is the conceptual name. The sentence uses both correctly by distinguishing them: one names the class, the other names the pattern.*

### Approved Technical Nouns as Modifiers

When you use the approved technical noun as a modifier (an adjective before another noun), the compound noun phrase inherits the approval status of the head noun. The modifier must be the approved technical noun — do not substitute a description as the modifier.

> **STE:** The `UserRepository` interface defines the database operations. (correct — `UserRepository` is the approved name, used as a modifier of "interface")
> **Non-STE:** The user storage interface defines the database operations. (incorrect — "user storage" is not the approved name)

> **STE:** The Observer pattern implementation uses a list of Observer instances. (correct — "Observer" is the approved pattern role name)
> **Non-STE:** The watcher pattern implementation uses a list of watcher objects. (incorrect — "watcher" is not the approved pattern name)

### Capitalization of Approved Technical Nouns

Follow the capitalization conventions of the source. Class names use PascalCase in most languages. Function names use camelCase in JavaScript and Java, snake_case in Python and Rust. Configuration keys use UPPER_SNAKE_CASE. Do not change the capitalization to match the surrounding sentence — the approved technical noun keeps its original form.

> **STE:** The `userService` instance calls the `findById` method. (correct — `userService` and `findById` keep their source code capitalization)
> **Non-STE:** The `UserService` instance calls the `FindById` method. (incorrect — changed capitalization; these are not the names in the source code)

### Approved Technical Nouns and the Definite Article

When you refer to an approved technical noun that is a unique entity (a specific class, a specific configuration key, a specific protocol), use the definite article "the." When you refer to the concept in general, omit the article.

> **STE:** The `UserController` handles the request. (specific class — use "the")
> **STE:** `UserController` is a common pattern in Spring Boot applications. (concept in general — no article)
> **Non-STE:** `UserController` handles the request. (missing article — `UserController` is a specific class in this context)

### Approved Names in Code Blocks vs. Prose

When the approved technical noun appears in a code block, it is part of the quoted text (Rule 1.5, category 10). When it appears in prose, it is a code-domain technical noun. In both cases, use the exact approved name. The formatting changes, but the name does not.

> **STE:**
> ```
> const user = await UserService.findById(id);
> ```
> The `UserService.findById` method returns a `User` object.

> *Explanation: `UserService`, `findById`, and `User` appear in both the code block and the prose. The formatting changes (code block vs. inline code), but the names are identical. A reader who sees `UserService.findById` in the prose can find it in the code block and in the source code.*

---

## Summary Checklist

Use this checklist to check that your documentation obeys Rule 1.8:

1. Identify each concept that has a name in more than one place (codebase, glossary, industry standard).
2. Find the most authoritative source for each concept (source code > language spec > framework docs > glossary > industry standard > company docs).
3. Use the exact name from the most authoritative source. Do not paraphrase, abbreviate, or describe it.
4. If the codebase name differs from the industry name, mention both with clear context (codebase name for traceability, industry name for comprehension).
5. Define each acronym at its first use. Use only the acronym after the definition.
6. Keep the capitalization and spelling of the approved name exactly as it appears in the source.
7. Check that you did not use a description where an approved technical noun exists.
8. If the approved name changes during a refactor, use the new name. Mark the old name as DEPRECATED.
9. Make sure the same concept uses the same approved name throughout the document and across all project documentation.

---

## Distinction from Related Rules

Rule 1.8 is often confused with other rules because they all deal with word choice. Use this table to distinguish them:

| Situation | Which Rule Applies | Example |
|---|---|---|
| A word is not in the STE-Code dictionary, but it names a code concept | Rule 1.5 | "middleware" is a code-domain technical noun |
| A word is not in the dictionary and is not a code concept | Rule 1.6 | "utilize" is forbidden — use "use" |
| A code-domain technical noun is used as a verb | Rule 1.7 | "Cache the data" → "Put the data in the cache" |
| Two names exist for the same code concept — which to use? | **Rule 1.8** | "AccountController" vs. "account controller" |
| Two approved names exist — which is better? | Rule 1.9 | "UserRepository" vs. "UserDatabaseAccessObject" |
| An informal term names a standard concept | Rule 1.10 | "kicks off" → "starts" |
| The same concept has two different names in the same document | Rule 1.11 | Use "UserService" everywhere, not mixed with "UserManager" |

Rule 1.8 answers one question: "I know this is a technical noun — but which name should I use?" The answer is always: use the name from the most authoritative source.
