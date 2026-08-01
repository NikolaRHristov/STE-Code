# Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.11](ste-code/grouped/), Rule 1.11

## Original Rule

**Rule 1.11** Do not use different technical nouns for the same item.

When you select a technical noun, do not use a different technical noun in other parts of your text to refer to the same item.

Example:

> **Non-STE:**
> 1. Make sure that the servo control unit is in the open position.
> 2. Do the operational test of the actuator.
> 3. Disconnect the control unit from the test rig.

> **STE:**
> 1. Make sure that the actuator is in the open position.
> 2. Do the operational test of the actuator.
> 3. Disconnect the actuator from the test rig.

In the non-STE example, "servo control unit," "actuator," and "control unit" refer to the same item. Use the technical noun that is approved in your company, industry, or subject field. If, as in the example, the technical noun is "actuator," then always use this technical noun in your text.

## STE-Code Adaptation

**Rule 1.11** Do not use different code-domain technical nouns for the same item.

When you select a code-domain technical noun, do not use a different code-domain technical noun in other parts of your documentation to refer to the same item. Use the code-domain technical noun that is approved in your project, company, industry, or subject field consistently throughout your text.

Changing the name of the same item in different sections of the documentation causes confusion. The reader must determine whether you refer to the same item or to a different item. Always use the same code-domain technical noun for the same item.

### Examples

> **Non-STE:**
> 1. Initialize the UserService class.
> 2. Call the authenticate method on the AccountManager.
> 3. The UserHandler returns a session token.

> **STE:**
> 1. Initialize the UserService class.
> 2. Call the authenticate method on the UserService.
> 3. The UserService returns a session token.

> *Adapted from spec pair: "servo control unit," "actuator," and "control unit" → "actuator" (consistent technical noun). In the spec, three different names refer to the same component, and the reader cannot tell if they are the same or different items. The same problem occurs in code documentation when a class is referred to by three different names. In the non-STE example, "UserService," "AccountManager," and "UserHandler" refer to the same class. The STE version uses the approved code-domain technical noun "UserService" in all three sentences, just as the spec example uses "actuator" consistently.*

> **Non-STE:**
> 1. Send a request to the /api/login path.
> 2. The authentication route returns a JSON Web Token.
> 3. Include the token from the login endpoint in subsequent requests.

> **STE:**
> 1. Send a request to the /api/login endpoint.
> 2. The /api/login endpoint returns a JSON Web Token.
> 3. Include the token from the /api/login endpoint in subsequent requests.

> *Adapted from spec pair: "servo control unit," "actuator," and "control unit" → "actuator" (consistent technical noun). In the spec, three names refer to one item. In the non-STE example, "/api/login path," "authentication route," and "login endpoint" are three names for the same API endpoint. The STE version uses the single approved code-domain technical noun "/api/login endpoint" consistently, just as the spec example uses "actuator" consistently.*

---

## Code-Domain Explanation

Rule 1.11 is one of the most frequently violated rules in software documentation. Code projects accumulate names from many sources: class names in source code, route patterns in HTTP APIs, file paths on disk, configuration keys, database table names, and colloquial names that developers use in conversation. When documentation mixes these names, the reader cannot know whether each name refers to the same item or to different items.

This rule applies to five primary code documentation types:

### README Files

README files introduce the project to new developers. If the README calls the same component by three different names, the reader will think the project has three separate components. A README must use exactly one code-domain technical noun for each component, service, module, or endpoint that it describes. The project's entry file, the main class name, or the documented public API name is the source of truth for this noun.

### API Documentation

API documentation (OpenAPI, JSDoc, Sphinx, Javadoc) describes endpoints, parameters, and response objects. Each endpoint has one URL path. Each parameter has one field name. Each response object has one schema name. The API documentation must use the URL path, the field name, and the schema name consistently. Do not substitute a colloquial name for the actual path. Do not describe the same parameter as "user ID" in one sentence and "account identifier" in the next sentence.

### Docstrings and Inline Comments

Docstrings describe a single function, method, class, or module. The name of the entity is given by the code itself. The docstring must use that name consistently. Do not refer to the function by a shorthand nickname in the docstring body. Do not describe the same argument by different names in different parts of the docstring. Inline comments must use the same name that the surrounding code uses.

### Commit Messages

Commit messages are short and refer to components by their file paths, class names, or function names. A commit message about `src/auth/UserService.ts` must use "UserService" or "src/auth/UserService.ts" consistently. Do not call it "the auth module" in the subject line and "the login handler" in the body. A reviewer who reads the commit later must know exactly which component changed.

### Error Messages and Log Output

Error messages and log output are read during debugging. If the error message uses a different name than the code, the developer must manually map the error message to the source. Always use the canonical code-domain technical noun in error messages. The log line `ERROR [PaymentProcessor] transaction failed` must use "PaymentProcessor" if that is the class name, not "billing engine" or "payment handler."

---

## Paradigm-Specific Guidance

### Object-Oriented (Java, C++, C#, Python)

In object-oriented documentation, the canonical technical noun is the class name. The class name is defined once in the source code. All documentation that refers to that class must use the exact class name.

**Rule:** Choose the class name as the code-domain technical noun. Use it in all method descriptions, architecture diagrams, sequence diagrams, and README sections.

**Common violations in OO documentation:**
- Calling the class `PaymentProcessor` in one section and "the payment module" in another
- Using a shortened nickname like "PP" or "the processor" in inline comments
- Describing an interface by its implementation class name

**Guidance for interfaces and abstract classes:**
When a component implements an interface, choose one canonical noun. If the documentation is about the interface contract, use the interface name. If the documentation is about the specific implementation, use the implementation class name. Document this choice at the start of the section.

### Functional (Haskell, Elixir, Clojure, Rust)

In functional documentation, the canonical technical noun is the module name or the top-level function name. Functional code often uses type aliases and generic type parameters. The documentation must settle on one name per concept.

**Rule:** Choose the module-qualified function name (for example, `Auth.authenticate`) or the type alias name as the code-domain technical noun. Use it consistently.

**Common violations in functional documentation:**
- Calling a function `validate_input` in the module doc and `check_params` in the function docstring
- Using different type alias names for the same data structure in different documentation sections
- Describing a data type by its structural shape instead of its named alias (for example, calling `UserRecord` a "map of string to user field" in one place and "the user dictionary" in another)

**Guidance for type aliases:**
When a type alias (`type User = { name: String, age: Int }`) names a concept, use the alias name. Do not describe the same concept by its structural expansion.

### Procedural (C, Go, Bash)

In procedural documentation, the canonical technical noun is the function name, the struct name, or the file path. Procedural code often has fewer naming layers than OO code, making the rule simpler but also easier to violate through informal nicknames.

**Rule:** Choose the function name or the struct name as given in the source header file or the module file. Use it in all documentation.

**Common violations in procedural documentation:**
- Calling a function `parse_config_file` in the header comment and "the config parser" in the README
- Using the file path as a name in one section and the exported function name in another
- Describing a C struct by its typedef alias in one file and its tag name in another

**Guidance for C structs with multiple names:**
A C struct can have a tag name (`struct user_record`), a typedef alias (`user_record_t`), and a variable instance name. Choose the typedef alias as the canonical noun. Use it in all documentation. Do not switch between the tag name and the typedef alias.

### Declarative (SQL, Terraform, Kubernetes YAML)

In declarative documentation, the canonical technical noun is the resource name or the table name. Declarative configuration files define resources by name. Documentation about those resources must use the defined name.

**Rule:** Choose the resource name from the configuration file or the table name from the schema as the code-domain technical noun. Use it in all documentation.

**Common violations in declarative documentation:**
- Calling a Terraform resource `aws_instance.web_server` in one section and "the EC2 instance" or "the web VM" in another
- Referring to a SQL table as `users` in the schema comment and "the user table," "the accounts table," or "the user_relation" in query documentation
- Describing a Kubernetes Deployment by its metadata name, its label selector, and its Pod template interchangeably

**Guidance for generated resource names:**
Some declarative tools generate resource names dynamically (for example, Terraform `count.index` or Helm release names). When the name is not static, choose the most specific static part of the name as the canonical noun. Document this choice.

### Systems (Rust Ownership Docs, C Memory Docs)

In systems documentation (ownership, lifetimes, memory layout), the canonical technical noun is the concept name as defined by the language specification or the standard library documentation. Systems concepts are abstract and do not have a single source file to point to. The documentation must define the term once and use it consistently.

**Rule:** Choose the name from the language specification or the standard library documentation. Define it in a glossary section. Use it in all documentation.

**Common violations in systems documentation:**
- Calling the same concept "the borrow checker" in one section and "the ownership system" in another
- Describing a memory region as "the heap allocation," "the arena," and "the buffer pool" interchangeably
- Using "lifetime parameter," "lifetime annotation," and "borrow annotation" for the same Rust syntax element

**Guidance for abstract concepts:**
When the concept does not map to a single code identifier, create a glossary entry in the project documentation. Use the glossary entry as the canonical code-domain technical noun. Cross-reference the glossary in each documentation section.

---

## Extended Examples

### Example 1: Database Table

> **Non-STE:**
> 1. The user_accounts table stores authentication data.
> 2. Query the accounts relation to find active sessions.
> 3. The user table has a foreign key to the roles table.

> **STE:**
> 1. The user_accounts table stores authentication data.
> 2. Query the user_accounts table to find active sessions.
> 3. The user_accounts table has a foreign key to the roles table.

> *Principle applied: P11 (One term per concept). Three names — "user_accounts table," "accounts relation," and "user table" — refer to the same database table. The reader cannot know whether "user table" is a shortened name for "user_accounts" or a different table. The STE version uses the schema-defined name "user_accounts" in all three sentences. If the canonical noun includes the "table" qualifier, use it consistently or drop it consistently — do not mix.*

### Example 2: Configuration Key

> **Non-STE:**
> 1. Set the database_connection_timeout value in your config.
> 2. The DB timeout parameter controls how long the driver waits.
> 3. Increase the connection deadline if you see timeout errors.

> **STE:**
> 1. Set the database_connection_timeout value in your configuration file.
> 2. The database_connection_timeout parameter controls how long the driver waits.
> 3. Increase the database_connection_timeout value if you see timeout errors.

> *Principle applied: P11 (One term per concept) and P1 (Use approved words from the dictionary). Four names — "database_connection_timeout," "DB timeout," "connection deadline," and "database_connection_timeout" — refer to the same configuration key. The first and fourth sentences use the correct name, but the middle sentences drift into informal synonyms. The STE version uses the configuration file key name in all three sentences. "DB" is an unapproved abbreviation (Rule 1.5); "deadline" has a different approved meaning than "timeout."*

### Example 3: CLI Command

> **Non-STE:**
> 1. Run the project-builder tool to compile your source files.
> 2. The build system outputs artifacts to the dist/ directory.
> 3. Use the compiler's --watch flag for development.

> **STE:**
> 1. Run the project-builder tool to compile your source files.
> 2. The project-builder tool outputs artifacts to the dist/ directory.
> 3. Use the project-builder tool's --watch flag for development.

> *Principle applied: P11 (One term per concept). Three names — "project-builder tool," "build system," and "compiler" — refer to the same CLI tool. The reader may think the project has three separate tools. The STE version uses the binary name "project-builder" in all three sentences. If the tool has other legitimate subsystem names (for example, a separate compiler), those must be introduced explicitly as distinct items.*

### Example 4: Error Type

> **Non-STE:**
> 1. The function throws a ValidationFailure when the input is invalid.
> 2. Catch the InputError to show a user-friendly message.
> 3. The validation exception includes a list of field errors.

> **STE:**
> 1. The function throws a ValidationError when the input is invalid.
> 2. Catch the ValidationError to show a user-friendly message.
> 3. The ValidationError includes a list of field errors.

> *Principle applied: P11 (One term per concept) and P8 (Use standard, well-known technical nouns). Three names — "ValidationFailure," "InputError," and "validation exception" — refer to the same error type. The reader cannot know whether "InputError" is a parent class of "ValidationFailure" or the same class. The STE version uses the class name "ValidationError" in all three sentences. If the class name is "ValidationError" in the source code, the documentation must match.*

### Example 5: Environment Variable

> **Non-STE:**
> 1. Set the API_KEY environment variable before starting the server.
> 2. The service reads its auth token from the environment.
> 3. If the secret key is not set, the process exits with code 1.

> **STE:**
> 1. Set the API_KEY environment variable before you start the server.
> 2. The service reads the API_KEY environment variable at startup.
> 3. If the API_KEY environment variable is not set, the process exits with code 1.

> *Principle applied: P11 (One term per concept) and P4 (Use only approved verb and adjective forms). Three names — "API_KEY environment variable," "auth token," and "secret key" — refer to the same environment variable. The reader cannot know whether "auth token" is the same concept as "API_KEY" or a separate configuration value. The STE version uses the exact environment variable name "API_KEY" in all three sentences. The approved verb "start" replaces "starting" (Rule 1.4, no -ing forms as main verbs).*

### Example 6: Git Branch

> **Non-STE:**
> 1. Create a feature branch from the mainline.
> 2. Push your topic branch to the remote repository.
> 3. Merge the development line back into master.

> **STE:**
> 1. Create a feature branch from the main branch.
> 2. Push your feature branch to the remote repository.
> 3. Merge the feature branch back into the main branch.

> *Principle applied: P11 (One term per concept) and P14 (Use American English spelling). The names "mainline," "master," and "main branch" refer to the same branch. "Topic branch," "development line," and "feature branch" refer to the same branch. The STE version uses the Git convention names "main branch" and "feature branch" in all three sentences. Some projects use "master" as the canonical branch name — if so, use "master branch" consistently. The project's Git configuration determines the canonical noun.*

---

## Edge Cases

### Edge Case 1: Framework Names That Are Also Unapproved Words

Some software frameworks and libraries have names that are also words in the STE-Code controlled terminology. For example, a framework named "Act" (conflicts with the approved verb "act"), a library named "Before" (conflicts with the approved preposition "before"), or a tool named "Make" (conflicts with the approved verb "make").

**Resolution:** Framework and library names are code-domain technical nouns under Rule 1.5. They are exempt from the dictionary restriction. Use the framework name as the code-domain technical noun, exactly as it appears in the framework's own documentation. Do not rename the framework to avoid the conflict. Capitalize the framework name when the framework's own documentation does so.

**Guidance:** When both the approved word and the framework name appear in the same sentence, use capitalization and context to disambiguate. For example: "Use the Make build tool to make the project." The capital "Make" signals the technical noun; the lowercase "make" signals the approved verb. If capitalization alone is insufficient, add a qualifier: "Use the Make tool to make the project."

### Edge Case 2: Code Keywords That Conflict with the Canonical Noun

A code keyword (for example, `class`, `type`, `def`, `fn`, `let`, `async`, `await`) can sometimes be part of the concept name that the documentation needs to describe. The documentation must distinguish between the keyword as syntax and the concept name.

**Resolution:** Use a code-formatted span (backticks in Markdown, `<code>` in HTML) for the keyword when it appears as syntax. Use the prose form without code formatting for the concept name. For example: "The `async` keyword marks a function as asynchronous. An async function returns a Promise."

**Guidance:** When the concept name includes the keyword (for example, "async function" is the canonical name in JavaScript documentation), use the same compound noun consistently. Do not shorten it to "async" in some sentences and "async function" in others. The full compound noun is the code-domain technical noun.

### Edge Case 3: Multiple Canonical Names for the Same Item in Different Contexts

Some items have multiple legitimate names in different contexts. A Docker container image might be named `myapp:latest` in the Dockerfile, `myapp-image` in the CI pipeline configuration, and "the application container" in the architecture documentation. All three names refer to the same item but serve different audiences.

**Resolution:** Choose one canonical name per documentation document or per section. If you must use different names in different documents, declare the mapping at the start of each document. For example, a section header: "Container Image (myapp:latest)". After this declaration, use "myapp:latest" consistently in that section.

**Guidance:** This edge case is common in multi-repository projects and microservice architectures. The name that the build system uses may differ from the name that the deployment system uses, and both may differ from the name that the monitoring system uses. Do not force one name across all documentation. Force one name within each document or section, and document the cross-reference.

### Edge Case 4: Generated Code and Auto-Generated Documentation

Generated code (from protobuf, OpenAPI codegen, GraphQL codegen, ORM tools) produces class names, method names, and type names automatically. These names may not follow the project's naming conventions. The generated names may also change when the generator version changes.

**Resolution:** Use the generated names as code-domain technical nouns when documenting the generated code itself. Do not rename generated symbols. When documenting the hand-written code that uses the generated code, use the hand-written names as the canonical nouns and mention the generated names only in cross-references.

**Guidance:** If the generated name is long or awkward, you may define a shorter alias in the documentation, provided that you declare the alias explicitly at first use. For example: "The generated class `com.example.api.v1.UserServiceGrpc.UserServiceImplBase` (referred to as `UserServiceImplBase` in this document) provides the base implementation." After this declaration, use the alias consistently.

### Edge Case 5: Renaming During Refactoring

During a refactoring, a component changes its name. Documentation written before the refactoring uses the old name. Documentation written after the refactoring uses the new name. During the transition period, both names exist.

**Resolution:** After a rename is complete and committed, update all documentation to use the new name. Do not keep the old name in documentation with a "formerly known as" note, unless the old name is part of a public API that has not yet been deprecated. Use the DEPRECATED marker (per the STE-Code output format conventions) when the old name still appears in public-facing documentation.

**Guidance:** A git log or changelog records the rename history. Documentation does not need to preserve the old name for historical purposes. If the rename affects a public API, add a deprecation notice that maps the old name to the new name, and remove the old name from all other documentation.

---

## Cross-References

### Related Rules in Section 1

- **Rule 1.1** (Use words that are approved in the dictionary, technical nouns, or technical verbs): Rule 1.11 assumes that the chosen code-domain technical noun is itself approved under Rule 1.1. A consistent noun that violates the dictionary is still a violation.

- **Rule 1.3** (Use approved words only with their approved meanings): The canonical code-domain technical noun must be used with its approved meaning. Do not use the canonical noun to mean something else, even if you use it consistently.

- **Rule 1.5** (Technical code nouns are allowed): Rule 1.11 applies to code-domain technical nouns. Rule 1.5 defines what qualifies as a code-domain technical noun. Together, these rules say: code-domain technical nouns are allowed, and once you choose one, use it consistently.

- **Rule 1.6** (Non-approved words only when they are technical code nouns): If the code-domain technical noun is not in the controlled terminology, it is only permitted if it qualifies as a code-domain technical noun under Rule 1.6. Rule 1.11 does not override the dictionary restriction.

- **Rule 1.8** (Use standard, well-known technical nouns): The canonical noun chosen under Rule 1.11 should be the standard, well-known name for the item. Rule 1.8 helps select the correct canonical noun. Rule 1.11 enforces consistency once the noun is chosen.

- **Rule 1.9** (Prefer short, clear technical nouns): When choosing the canonical noun under Rule 1.11, prefer the shorter, clearer option among legitimate alternatives. Rule 1.9 guides the selection. Rule 1.11 governs the usage.

- **Rule 1.10** (No slang, jargon, or regional terms): The canonical noun must not be slang or jargon. Rule 1.10 disqualifies inappropriate candidates. Rule 1.11 applies to the noun that survives the Rule 1.10 filter.

### Related Rules in Section 3 (Verbs)

- **Rule 3.1** (Use only the approved verb forms): When the canonical noun is used as the subject or object of a sentence, the verb must obey Rule 3.1. A consistent noun with an unapproved verb form is still a violation.

- **Rule 3.6** (Use the active voice): A sentence that uses the canonical noun consistently but in passive voice violates Rule 3.6 if active voice is possible. Rule 1.11 governs noun choice; Rule 3.6 governs sentence structure.

### STE-Code Dictionary

- **Entry: TECHNICAL NOUN (TN):** The dictionary defines the category "technical noun" and gives examples. Rule 1.11 applies to all terms that qualify as code-domain technical nouns under this category. Refer to the dictionary entry for the full definition and scope.

- **Entry: NAME (n):** The approved noun "name" is the general term for identifiers. When you cannot use the specific code-domain technical noun (for example, when describing the naming process itself), use "name." Do not use "identifier," "label," "tag," or "handle" as synonyms for "name" — these are reserved for their specific approved meanings.

---

## Grammar Notes

### Definite Article Consistency

When a code-domain technical noun is used with the definite article "the," the article signals that the noun is specific and known to the reader. If you switch to a different noun for the same item, the reader expects "the" to introduce a different, also-known item. The reader then searches for the new item and finds nothing. This is a grammatical cause of the confusion that Rule 1.11 prevents.

In English, the first mention of an item can use the indefinite article "a" or "an":
> "A UserService handles authentication."

Subsequent mentions use the definite article "the":
> "The UserService returns a session token."

If the second sentence says "The AccountManager returns a session token," the reader interprets "the AccountManager" as a previously introduced item. The reader searches the preceding text for the first mention of "an AccountManager" and does not find it. This breaks the discourse coherence.

**Rule 1.11 is a semantic rule, but it has a direct grammatical consequence:** the article system of English depends on consistent noun choice to maintain reference chains. When you change the noun, you break the reference chain that the articles establish.

### Anaphora and Pronoun Reference

Pronouns (it, they, them, its, their) refer back to the most recent noun phrase that matches in number and gender. If the documentation alternates between "UserService" (singular) and "authentication modules" (plural), a pronoun like "it" becomes ambiguous. The reader does not know whether "it" refers to the service or to the modules.

**Example of pronoun ambiguity caused by noun inconsistency:**

> **Non-STE:**
> The UserService processes login requests. The authentication modules validate credentials. It returns a token on success.

The pronoun "it" could refer to "UserService" (singular) or the nearest plural "authentication modules" (treated as a singular system). The reader must guess. The STE version eliminates this ambiguity by using one noun consistently:

> **STE:**
> The UserService processes login requests. The UserService validates credentials. The UserService returns a token on success.

### Compound Nouns and Head Nouns

A compound noun is a sequence of nouns that together name one concept (for example, "user authentication service"). The last noun in the sequence is the head noun. The head noun carries the core meaning. The preceding nouns modify the head noun.

When documentation alternates between the full compound noun and a shortened form that changes the head noun, the reader may think the shortened form refers to a different concept.

**Example of head-noun drift:**

> **Non-STE:**
> 1. The user authentication service handles login.
> 2. The authentication system validates tokens.
> 3. The user service manages profiles.

Three different head nouns — "service," "system," and "service" — appear. The reader cannot know whether the second and third sentences describe the same component or different components. The STE version uses one compound noun with one head noun:

> **STE:**
> 1. The user authentication service handles login.
> 2. The user authentication service validates tokens.
> 3. The user authentication service manages profiles.

If the project genuinely has three separate components (an authentication service, an authentication system, and a user service), the documentation must introduce each one explicitly and explain their relationships. Rule 1.11 does not prevent projects from having multiple components. It prevents one component from having multiple names.

### Parallel Structure in Lists

Lists of steps, features, or components rely on parallel grammatical structure for readability. When each item in a list names a different component, each item must use the same grammatical form (for example, all capitalized class names, or all lowercase noun phrases). If one item uses a different naming pattern, the reader cannot tell whether the difference is meaningful or accidental.

**Example of broken parallelism:**

> **Non-STE:**
> The project has these components:
> - UserService (handles authentication)
> - The payment module (processes transactions)
> - notification_system (sends emails)

Three different naming conventions — PascalCase, sentence case with article, and snake_case — appear in one list. The STE version normalizes the naming:

> **STE:**
> The project has these components:
> - UserService (handles authentication)
> - PaymentService (processes transactions)
> - NotificationService (sends emails)

The normalization enforces Rule 1.11 at the list level. Each item uses the code-domain technical noun that matches the source code naming convention for the project.
