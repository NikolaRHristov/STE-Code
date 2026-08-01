# Rule 1.7 — Do Not Use Words That Are Technical Nouns as Verbs

> **Source:** Adapted from ASD-STE100 Issue 9
> **Source:** [master.md#sec1-rule1.7](ste-code/grouped/), Rule 1.7

## Original Rule

**Rule 1.7** Do not use words that are technical nouns as verbs.

Use a technical noun only as a noun or as an adjective that is part of a different technical noun. Do not use the same word as a verb.

Examples:

> *Adapted from spec pair:* Non-STE: Oil the steel surfaces.  |  STE: Apply oil to the steel surfaces.

"Oil" is a technical noun, category 4, materials, consumables, and unwanted material. Do not use "oil" as a verb. Use a different sentence construction that lets you use "oil" as a technical noun.

> **Non-STE:** Oil the steel surfaces.
>
> **STE:** Apply oil to the steel surfaces.

"Snow" is a technical noun, category 16, environmental and operational conditions. Do not use "snow" as a verb. Use a different sentence construction that lets you use "snow" as a technical noun.

> **Non-STE:** Snow the walkway before the shift starts.
>
> **STE:** Remove snow from the walkway before the shift starts.

In some contexts, the same word can be a technical noun and a technical verb. This condition occurs when you can put this word in a technical noun category (rule 1.5) and in a technical verb category (rule 1.12).

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

"Drill" is a technical noun, category 3, tools and support equipment, their parts, and locations on them.

> **STE:** Drill a hole at the intersection of the two lines.

("Drill" is a technical verb, rule 1.12, category 1 a), manufacturing processes, remove material.)

## STE-Code Adaptation

**Rule 1.7** Do not use words that are code-domain technical nouns as verbs.

Use a code-domain technical noun only as a noun or as an adjective that is part of a different code-domain technical noun. Do not use the same word as a verb. Use a different sentence construction that lets you use the word as a code-domain technical noun.

"Database" is a code-domain technical noun, category 18, database and storage terminology. This adapts the spec example where "oil" is a technical noun (category 4, materials). Do not use "database" as a verb. Use a different sentence construction that lets you use "database" as a code-domain technical noun.

> **Non-STE:** Database the user records before the migration.
>
> ```python
> def migrate_users(records):
>     # "database" used as a verb — part of speech violated
>     database(records)
> ```
>
> **STE:** Store the user records in the database before the migration.
>
> ```python
> def migrate_users(records, db):
>     # "store" is the approved verb; "database" stays a noun
>     db.store(records)
> ```

This adapts the spec pair: "Oil the steel surfaces" becomes "Apply oil to the steel surfaces." Just as you cannot use "oil" as a verb in STE, you cannot use "database" as a verb in STE-Code. The STE version uses the approved verb "store" (analogous to "apply") and keeps "database" as a code-domain technical noun.

"Cache" is a code-domain technical noun, category 16, computer science, information and communication technology. This adapts the spec example where "snow" is a technical noun (category 16, environmental and operational conditions). Both "snow" and "cache" are technical nouns in their respective domains that must not be used as verbs.

> **Non-STE:** Cache the API responses to improve performance.
>
> ```javascript
> // Non-STE: "cache" forced into a verb role
> function handleRequest(req, res) {
>   const data = fetchData();
>   cache(data); // unclear: store? read? invalidate?
>   res.send(data);
> }
> ```
>
> **STE:** Store the API responses in the cache to improve performance.
>
> ```javascript
> // STE: "store" is the approved verb; "cache" stays a noun
> function handleRequest(req, res) {
>   const data = fetchData();
>   cache.store(data); // clear action on a clear entity
>   res.send(data);
> }
> ```

NOTE: "Cache" is also a code-domain technical verb (Rule 1.12, category 2 c), system operations. When "cache" is cataloged in your project glossary as both a noun and a verb, you may use it as a verb in its approved verb sense. If your project glossary only lists "cache" as a code-domain technical noun, you must obey Rule 1.7 and use a different sentence construction.

In some contexts, the same word can be a code-domain technical noun and a code-domain technical verb. This condition occurs when you can put this word in a code-domain technical noun category (rule 1.5) and in a code-domain technical verb category (rule 1.12). This adapts the spec example where "drill" can be both a technical noun (a tool) and a technical verb (a manufacturing process).

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

"Log" is a code-domain technical noun, category 18, database and storage terminology. Use "log" only as a noun in this context.

> **STE:** Write a log entry for each failed request.
>
> ```python
> for request in failed_requests:
>     write_log_entry(request.id, request.error)
> ```

"Log" is also a code-domain technical verb, rule 1.12, category 2 c), computer processes and applications, system operations. Use "log" as a verb in this context.

> **STE:** Log each failed request.
>
> ```python
> for request in failed_requests:
>     logger.log(request.id, request.error)
> ```

This distinction is central to Rule 1.7: when a word is a code-domain technical noun in your glossary, do not use it as a verb. When the same word is a code-domain technical verb in your glossary, you may use it as a verb. The key is consistency: decide which part of speech the word has in your project glossary and obey that decision.

---

## Code-Domain Explanation

This rule prevents the conversion of code-domain technical nouns into verbs. The rule applies differently to each documentation type because the risk of noun verbing changes with audience and purpose.

### README Files

README files describe a project at a high level. The audience includes new users who may not know that a tool name is not a verb. README files must keep all code-domain technical nouns as nouns. Use an approved verb or a code-domain technical verb to describe the action.

> **Non-STE:** To Docker the application, first Git the repository and then npm the dependencies.
>
> ```markdown
> ## Quick start
> 1. Docker the application with `docker compose up`.
> 2. Git the repository to get the latest code.
> 3. npm the dependencies before you run the tests.
> ```
>
> **STE:** To containerize the application, first clone the repository and then install the dependencies.
>
> ```markdown
> ## Quick start
> 1. Containerize the application with `docker compose up`.
> 2. Clone the repository to get the latest code.
> 3. Install the dependencies with `npm install` before you run the tests.
> ```

> *Principles applied: P7 (do not use technical nouns as verbs), P8 (standard technical nouns). "Docker," "Git," and "npm" are tool names and code-domain technical nouns. Do not use them as verbs. Use "containerize" (a code-domain technical verb, category 1 c), "clone" (a code-domain technical verb, category 2 c), and "install" (a code-domain technical verb, category 2 c).*

### API Reference Documentation

API documentation describes function signatures, parameters, and return values. The function name is a technical code noun. Do not use it as a verb in the description unless the name itself is a verb.

> **Non-STE:** `getUser(id)` — Users the database to retrieve a user.
>
> ```python
> def getUser(id):
>     """Users the database to retrieve a user."""
>     return db.query(id)
> ```
>
> **STE:** `getUser(id)` — Gets a user from the database.
>
> ```python
> def getUser(id):
>     """Gets a user from the database.
>
>     Args:
>         id: The unique identifier of the user.
>     Returns:
>         The user record, or None if not found.
>     """
>     return db.get_user(id)
> ```

> *Principles applied: P7, P1. "Users" is a noun (plural of "user") forced into a verb role. "Retrieve" is not approved. Use the approved verb "get" — which matches the function name `getUser`.*

### Docstrings and Inline Comments

Docstrings must be short and direct. Code-domain technical nouns that appear in comments must stay as nouns. If a comment describes an action, use an approved verb.

> **Non-STE:** # Buffer the output before you socket it to the client.
>
> ```python
> def send_response(output, client):
>     # Buffer the output before you socket it to the client.
>     buffered = buffer(output)
>     socket(client, buffered)
> ```
>
> **STE:** # Write the output to a buffer before you send it through the socket to the client.
>
> ```python
> def send_response(output, client):
>     # Write the output to a buffer before you send it
>     # through the socket to the client.
>     buffered = buffer_writer.write(output)
>     socket_connection.send(client, buffered)
> ```

> *Principles applied: P7, P1. "Buffer" is a code-domain technical noun (category 4, data structures). "Socket" is a code-domain technical noun (category 19, network and protocol terminology). Do not use them as verbs. Use "write" and "send" (approved verbs).*

### Commit Messages

Commit messages use the imperative mood. Code-domain technical nouns must not become verbs in commit messages. If a commit describes an action on a technical noun, use an approved verb to describe the action.

> **Non-STE:** Interface the payment module with the order system.
>
> ```text
> commit subject: Interface the payment module with the order system
> ```
>
> **STE:** Add an interface between the payment module and the order system.
>
> ```text
> commit subject: Add an interface between the payment module and the order system
> ```

> *Principles applied: P7, P13. "Interface" is a code-domain technical noun (category 6, systems and architectural components). Do not use it as a verb. Use the approved verb "add" with the code-domain technical noun "interface." The phrase "between X and Y" follows STE pattern for two entities.*

> **Non-STE:** Middleware the authentication layer.
>
> ```text
> commit subject: Middleware the authentication layer
> ```
>
> **STE:** Add authentication middleware.
>
> ```text
> commit subject: Add authentication middleware
> ```

> *Principles applied: P7, P9. "Middleware" is a code-domain technical noun (category 1, code components). Do not force it into a verb. Use the approved verb "add."*

### Error Messages

Error messages must be clear to all users. End-user error messages must use only approved verbs. Developer-facing error messages may use code-domain technical verbs but must not use code-domain technical nouns as verbs.

> **Non-STE:** (end-user error) Failed to JSON the configuration file.
>
> ```text
> Error: Failed to JSON the configuration file.
> ```
>
> **STE:** (end-user error) Could not parse the configuration file. The JSON format is not correct.
>
> ```text
> Error: Could not parse the configuration file.
> The JSON format is not correct. Check line 42.
> ```

> *Principles applied: P7, P1, P6. "JSON" is a code-domain technical noun (category 4, data structures). Do not use it as a verb. Use "parse" (a code-domain technical verb, category 3 a). For end-user messages, also replace "parse" with a plain-language explanation when possible.*

> **STE:** (developer error) Failed to parse config.json: invalid JSON at line 42.
>
> ```text
> ERROR  config.load: failed to parse config.json:
> invalid JSON at line 42, column 7
> ```

> *Principles applied: P12, P6. "Parse" is a code-domain technical verb for a developer audience. "JSON" stays as a technical code noun, correctly used as an adjective modifying "format" (implied).*

---

## Paradigm-Specific Guidance

### Object-Oriented Programming (Java, C++, C#, Python classes)

Object-oriented documentation has many nouns that developers habitually use as verbs. The most frequent violations of Rule 1.7 in OOP documentation involve class names, design pattern names, and architectural concepts.

| Code-Domain Technical Noun | Incorrect Verb Use | Correct Construction |
|---|---|---|
| interface | "Interface the module with..." | "Add an interface between the module and..." |
| class | "Class the user data model." | "Make a class for the user data model." |
| subclass | "Subclass the base controller." | "Make a subclass of the base controller." |
| singleton | "Singleton the logger." | "Make the logger a singleton." |
| factory | "Factory the parser objects." | "Use a factory to make parser objects." |
| observer | "Observer the state changes." | "Add an observer for the state changes." |
| dependency | "Dependency the service into the controller." | "Inject the service as a dependency into the controller." |

> **Non-STE:** You must abstract the connection pool behind an interface and then factory the pool instances.
>
> ```java
> // Non-STE: "abstract" and "factory" used as verbs
> ConnectionPool pool = abstract(behind(Interface.class));
> List<Pool> instances = factory(pool);
> ```
>
> **STE:** You must make an abstraction of the connection pool behind an interface. Then use a factory to make the pool instances.
>
> ```java
> // STE: nouns stay nouns; approved verbs carry the action
> ConnectionPool pool = makeAbstraction(behind(Interface.class));
> List<Pool> instances = poolFactory.make(pool);
> ```

> *Principles applied: P7, P1. "Abstract" is not approved as a verb in the controlled terminology. "Interface" and "factory" are code-domain technical nouns (category 6 and category 1). Do not use them as verbs. Use "make" (approved verb) with the technical nouns "abstraction" and "factory."*

### Functional Programming (Haskell, Elixir, Clojure, Rust iterators)

Functional programming documentation uses nouns that name mathematical concepts, type classes, and data structures. These nouns must not become verbs.

| Code-Domain Technical Noun | Incorrect Verb Use | Correct Construction |
|---|---|---|
| monad | "Monad the computation." | "Wrap the computation in a monad." |
| functor | "Functor the list." | "Map the function over the functor." |
| combinator | "Combinator the parsers." | "Combine the parsers with a combinator." |
| closure | "Closure the variable." | "Capture the variable in a closure." |
| thunk | "Thunk the expression." | "Wrap the expression in a thunk." |
| lambda | "Lambda the function." | "Write the function as a lambda." |

> **Non-STE:** To monad the optional value, you must functor the inner computation first.
>
> ```haskell
> -- Non-STE: "monad" and "functor" used as verbs
> result = monad optionalValue (functor innerComputation)
> ```
>
> **STE:** To wrap the optional value in a monad, you must map the inner computation over the functor first.
>
> ```haskell
> -- STE: nouns stay nouns; "wrap" and "map" carry the action
> result = wrapInMonad optionalValue (mapOverFunctor innerComputation)
> ```

> *Principles applied: P7, P12. "Monad" and "functor" are code-domain technical nouns (category 7, algorithmic terms). Do not use them as verbs. Use "wrap" (approved verb) with "monad" and "map" (code-domain technical verb, category 3 a) with "functor."*

### Procedural Programming (C, Go, Bash)

Procedural documentation uses nouns that name memory structures, system resources, and data formats. These nouns are frequently misused as verbs in low-level documentation.

| Code-Domain Technical Noun | Incorrect Verb Use | Correct Construction |
|---|---|---|
| buffer | "Buffer the output." | "Write the output to a buffer." |
| pointer | "Pointer the struct." | "Get a pointer to the struct." |
| malloc | "Malloc a block of memory." | "Allocate a block of memory with `malloc`." |
| struct | "Struct the data fields." | "Put the data fields in a struct." |
| heap | "Heap the large objects." | "Allocate the large objects on the heap." |
| stack | "Stack the local variables." | "Put the local variables on the stack." |

> **Non-STE:** Malloc a buffer, then pointer it to the struct you heaped earlier.
>
> ```c
> /* Non-STE: "malloc", "pointer", "heap" used as verbs */
> char *buf = malloc(1024);
> pointer(buf, &req);
> heap(req);
> ```
>
> **STE:** Allocate a buffer with `malloc`. Then set a pointer to the struct that you allocated on the heap.
>
> ```c
> /* STE: "allocate", "set" are approved verbs; nouns stay nouns */
> char *buf = malloc(1024);
> char **ptr = &buf;
> request_t *req = heap_alloc(sizeof(request_t));
> ```

> *Principles applied: P7, P12. "Malloc" is a standard library function and a technical code noun (Rule 1.5). "Buffer," "pointer," and "heap" are code-domain technical nouns (categories 4, 4, and 13). Do not use any of them as verbs. Use "allocate" (code-domain technical verb, category 2 c), "set" (approved verb), and "put" / "allocate" for the remaining constructions.*

### Declarative Programming (SQL, Terraform, Kubernetes YAML)

Declarative documentation uses nouns that name resources, schemas, and configuration objects. The declarative paradigm describes what exists, not what to do, so noun verbing is especially confusing because it implies an imperative action.

| Code-Domain Technical Noun | Incorrect Verb Use | Correct Construction |
|---|---|---|
| table | "Table the user records." | "Store the user records in a table." |
| schema | "Schema the database." | "Apply a schema to the database." |
| index | "Index the column." | "Make an index on the column." |
| YAML | "YAML the configuration." | "Write the configuration in YAML." |
| pod | "Pod the container." | "Put the container in a pod." |
| secret | "Secret the API key." | "Store the API key as a secret." |

> **Non-STE:** First, schema the database. Then table the data and index the primary key column.
>
> ```sql
> -- Non-STE: "schema", "table", "index" used as verbs
> SCHEMA users_db;
> TABLE user_records;
> INDEX id_column;
> ```
>
> **STE:** First, apply a schema to the database. Then store the data in a table and make an index on the primary key column.
>
> ```sql
> -- STE: approved verbs; nouns stay nouns
> CREATE SCHEMA users_db;
> CREATE TABLE user_records (...);
> CREATE INDEX id_idx ON user_records (id_column);
> ```

> *Principles applied: P7, P1. "Schema," "table," and "index" are code-domain technical nouns (category 18, database and storage terminology). Do not use them as verbs. Use "apply," "store," and "make" (approved verbs) with the technical nouns.*

### Systems Programming (Rust ownership, C memory, embedded)

Systems documentation uses nouns that describe memory regions, hardware components, and ownership concepts. These nouns have precise technical meanings that are lost when they are forced into verb roles.

| Code-Domain Technical Noun | Incorrect Verb Use | Correct Construction |
|---|---|---|
| mutex | "Mutex the shared state." | "Lock the mutex before you access the shared state." |
| semaphore | "Smaphore the resource." | "Use a semaphore to control access to the resource." |
| register | "Register the hardware address." | "Write to the register at the hardware address." |
| interrupt | "Interrupt the CPU." | "Send an interrupt to the CPU." |
| DMA | "DMA the buffer to the device." | "Transfer the buffer to the device with DMA." |
| MMU | "MMU the virtual address." | "Map the virtual address through the MMU." |

> **Non-STE:** Mutex the critical section, then DMA the buffer, and finally interrupt the processor.
>
> ```rust
> // Non-STE: "mutex", "DMA", "interrupt" used as verbs
> mutex(critical_section);
> dma(buffer, device);
> interrupt(processor);
> ```
>
> **STE:** Lock the mutex for the critical section. Then transfer the buffer with DMA. Then send an interrupt to the processor.
>
> ```rust
> // STE: approved / code-domain verbs; nouns stay nouns
> mutex.lock();
> dma_transfer(buffer, device);
> send_interrupt(processor);
> ```

> *Principles applied: P7, P12. "Mutex," "DMA," and "interrupt" are code-domain technical nouns (categories 16 and 19). Do not use them as verbs. Use "lock" (code-domain technical verb in systems context, category 2 c), "transfer" (code-domain technical verb, category 3 c), and "send" (approved verb) with the technical nouns.*

---

## Extended Examples

### Example Group A: Tool Name Used as a Verb

> **Non-STE:** You must Docker the application, then Git the changes, and finally Webpack the bundle.
>
> ```bash
> # Non-STE: tool names forced into verb roles
> docker the application
> git the changes
> webpack the bundle
> ```
>
> **STE:** You must containerize the application, then commit the changes, and then bundle the code with Webpack.
>
> ```bash
> # STE: approved verbs; tool names stay nouns
> docker build -t app:1.0 .
> git commit -m "Update application"
> npx webpack --mode production
> ```

> *Principles applied: P7 (do not use technical nouns as verbs), P8 (standard technical nouns), P12 (technical verbs are allowed). "Docker" and "Git" are tool names and code-domain technical nouns. Do not use them as verbs. "Containerize" is a code-domain technical verb (category 1 c). "Commit" is a code-domain technical verb (category 2 b). "Bundle" is a code-domain technical verb (category 1 c). "Webpack" stays as a technical code noun (Rule 1.5) — it names the tool that does the bundling.*

### Example Group B: Data Structure Name Used as a Verb

> **Non-STE:** Queue the jobs, stack the frames, and hash the passwords.
>
> ```python
> # Non-STE: data-structure nouns used as verbs
> queue(jobs)
> stack(frames)
> hash(passwords)
> ```
>
> **STE:** Put the jobs in a queue, push the frames onto the stack, and hash the passwords.
>
> ```python
> # STE: "put" and "push" are approved verbs; "queue" and "stack" stay nouns
> job_queue.put(jobs)
> frame_stack.push(frames)
> hash_passwords(passwords)  # "hash" is a code-domain technical verb
> ```

> *Principles applied: P7, P12. "Queue" and "stack" are code-domain technical nouns (category 4, data structures). "Hash" is a code-domain technical verb (category 3 a) — it is permitted as a verb because it fits a technical verb category. The first two nouns must not be verbed. Use approved verbs "put" and "push" with the technical nouns "queue" and "stack."*

### Example Group C: Brand or Product Name Used as a Verb

> **Non-STE:** You can Google the error message and then Slack the results to your team.
>
> ```text
> Non-STE: "Google the error, then Slack it to the team."
> ```
>
> **STE:** You can search for the error message with Google and then send the results to your team with Slack.
>
> ```text
> STE: "Search for the error with Google, then send the results
> to the team with Slack."
> ```

> *Principles applied: P7, P8, P10. "Google" and "Slack" are brand names and technical code nouns (Rule 1.5). Do not use brand names as verbs. Use "search" (approved verb in the controlled terminology) and "send" (approved verb) with the brand names as nouns.*

> **Non-STE:** Kubernetes the microservices and then Terraform the infrastructure.
>
> ```bash
> # Non-STE: platform names forced into verbs
> kubernetes the microservices
> terraform the infrastructure
> ```
>
> **STE:** Deploy the microservices with Kubernetes and then provision the infrastructure with Terraform.
>
> ```bash
> # STE: approved verbs; platform names stay nouns
> kubectl apply -f microservices.yaml
> terraform apply -var-file=infra.tfvars
> ```

> *Principles applied: P7, P12. "Kubernetes" and "Terraform" are platform names and technical code nouns. Do not use them as verbs. Use "deploy" (code-domain technical verb, category 1 c) and "provision" (code-domain technical verb, category 3 a) with the platform names as nouns.*

### Example Group D: Protocol or Format Name Used as a Verb

> **Non-STE:** JSON the response and then HTTP it to the client.
>
> ```python
> # Non-STE: format and protocol names used as verbs
> body = json(response)
> http(body, client)
> ```
>
> **STE:** Encode the response as JSON and then send it to the client through HTTP.
>
> ```python
> # STE: approved / code-domain verbs; names stay nouns
> body = json_encode(response)
> send_over_http(body, client)
> ```

> *Principles applied: P7, P1. "JSON" and "HTTP" are code-domain technical nouns (category 4, data structures, and category 19, network terminology). Do not use them as verbs. Use "encode" (code-domain technical verb, category 3 a) and "send" (approved verb) with the protocol names as nouns.*

> **Non-STE:** The service must REST the resources and GraphQL the queries.
>
> ```text
> Non-STE: "The service will REST the resources and GraphQL the queries."
> ```
>
> **STE:** The service must expose the resources through a REST API and process the queries through GraphQL.
>
> ```text
> STE: "The service exposes the resources through a REST API and
> processes the queries through GraphQL."
> ```

> *Principles applied: P7, P8. "REST" and "GraphQL" are architectural style names and technical code nouns (category 6 and category 16). Do not use them as verbs. Use "expose" (code-domain technical verb, category 2 b, when describing API surface) and "process" (code-domain technical verb, category 2 c) with the style names as nouns.*

### Example Group E: Architecture Concept Used as a Verb

> **Non-STE:** You must microservice the monolith and then API the new services.
>
> ```text
> Non-STE: "Microservice the monolith, then API the new services."
> ```
>
> **STE:** You must break the monolith into microservices and then add an API for each new service.
>
> ```text
> STE: "Break the monolith into microservices, then add an API
> for each new service."
> ```

> *Principles applied: P7, P1. "Microservice" and "API" are code-domain technical nouns (category 6, systems and architectural components). Do not use them as verbs. Use "break" (approved verb) and "add" (approved verb) with the technical nouns. "Monolith" is also a code-domain technical noun — do not use it as a verb or object of a noun-verb construct.*

> **Non-STE:** We will serverless the compute layer and then container the remaining services.
>
> ```bash
> # Non-STE: architecture nouns forced into verbs
> serverless the compute_layer
> container the services
> ```
>
> **STE:** We will move the compute layer to a serverless architecture and then package the remaining services in containers.
>
> ```bash
> # STE: approved verbs; nouns stay nouns
> deploy compute_layer --target serverless
> docker package services
> ```

> *Principles applied: P7, P9. "Serverless" is an adjective used as a code-domain technical noun (category 6). "Container" is a code-domain technical noun (category 5, infrastructure). Do not force either into a verb role. Use "move" (approved verb) and "package" (code-domain technical verb, category 1 c) with the technical nouns.*

### Example Group F: The Same Word as Noun and Verb — Choose the Correct Form

> **Non-STE:** Log the error and write the log to the log file.
>
> ```python
> # Non-STE: "log" used three ways in one line
> log(error)
> write(log, log_file)
> ```
>
> **STE:** Log the error and write the entry to the log file.
>
> ```python
> # STE: verb "log", noun "entry", noun "log file" kept distinct
> logger.log(error)
> write_log_entry(error, log_file)
> ```

> *Principles applied: P11 (one term per concept), P7. "Log" is both a code-domain technical noun and a code-domain technical verb (Rule 1.12, category 2 c). When you use "log" as a verb, you log data. When you refer to the result, it is a "log entry" or "log file" — not simply "the log" unless the context is clear. Use "entry" to keep the noun and verb distinct.*

> **Non-STE:** The script will script the deployment process.
>
> ```bash
> # Non-STE: "script" (noun) used as a verb
> ./script the deployment
> ```
>
> **STE:** The script will automate the deployment process.
>
> ```bash
> # STE: "automate" is the code-domain technical verb
> ./run_deploy.sh   # automates the deployment process
> ```

> *Principles applied: P7, P1. "Script" is a code-domain technical noun (category 1, code components). Do not use it as a verb. Use "automate" (code-domain technical verb, category 2 c) or an approved verb like "run" with the noun "script": "Run the script to automate the deployment process."*

---

## Edge Cases

### Edge Case 1: Words That Are Both Code-Domain Technical Nouns and Verbs

Some words are cataloged in both a noun category (Rule 1.5) and a verb category (Rule 1.12). These words are the exception to Rule 1.7: you may use them as verbs only in their approved verb sense. The spec example "drill" (noun = tool, verb = manufacturing process) is the exact model.

| Word | Code-Domain Technical Noun (Rule 1.5) | Code-Domain Technical Verb (Rule 1.12) |
|---|---|---|
| cache | Category 16: computer science ("The cache stores responses.") | Category 2 c: system operations ("Cache the responses.") |
| log | Category 18: database and storage ("Write a log entry.") | Category 2 c: system operations ("Log the error.") |
| queue | Category 4: data structures ("Add the job to the queue.") | Category 3 a: algorithmic and data ("Queue the job for processing.") |
| filter | Category 4: data structures or Category 16 ("Apply a filter.") | Category 2 b: UI operations ("Filter the results.") |
| sort | Category 7: algorithmic terms ("Use a merge sort.") | Category 2 b: UI operations ("Sort the list by name.") |
| map | Category 4: data structures ("Use a hash map.") | Category 3 a: algorithmic and data ("Map the function over the list.") |

RULE: Decide which part of speech the word has in your project glossary. If you catalog the word as a noun only, obey Rule 1.7. If you catalog it as both a noun and a verb, use the verb form only when the context matches the verb category description. Do not mix noun and verb uses in the same paragraph without clear context signals.

> **Non-STE:** Filter the results with a filter and then sort the filtered list with a sort.
>
> ```python
> # Non-STE: "filter"/"sort" used as both verb and noun in one sentence
> out = filter(results, with_a=filter)
> out2 = sort(out, with_a=sort)
> ```
>
> **STE:** Filter the results and then sort the list.
>
> ```python
> # STE: verb form implies the noun; no double noun use
> out = filter(results)
> out2 = sort(out, by="name")
> ```

> *Principles applied: P11, P7. When "filter" and "sort" are code-domain technical verbs, do not also use them as nouns in the same sentence. The verb form implies the noun. Use the verb alone for brevity. If you must name the filter or sort mechanism, use a more specific term: "Apply a Bloom filter" or "Use a merge sort algorithm."*

### Edge Case 2: Framework Names That Are Also English Words

Some framework and library names are also common English words with verb senses. For example: "Express" (Node.js framework), "Go" (language), "C" (language), "R" (language), "Boost" (C++ library), "Spring" (Java framework), "React" (JavaScript library — also a verb meaning "to respond"), "Vue" (JavaScript framework — sounds like "view," a verb).

RULE: Framework names are always code-domain technical nouns. Do not use them as verbs, and do not let their English verb meaning interfere with the documentation. Add a qualifier if the context does not make the meaning clear.

> **Non-STE:** Express the middleware and then React to the state changes.
>
> ```javascript
> // Non-STE: framework names used with English verb senses
> express(middleware);
> react(stateChanges);
> ```
>
> **STE:** Write the middleware with Express and then respond to the state changes with React.
>
> ```javascript
> // STE: framework names stay nouns; approved verbs carry meaning
> const app = express();
> app.use(middleware);
> componentDidUpdate() { respondTo(stateChanges); }
> ```

> *Principles applied: P7, P10. "Express" and "React" are framework names and technical code nouns. Do not use their English verb meanings. Use "write" (approved verb) and "respond" (approved verb) with the framework names as nouns.*

> **Non-STE:** Spring the application context and then Go to handle the request.
>
> ```java
> // Non-STE: framework / language names used as verbs
> spring(context);
> go(handleRequest);
> ```
>
> **STE:** Initialize the application context with Spring and then use Go to handle the request.
>
> ```java
> // STE: nouns stay nouns; approved verbs carry the action
> ApplicationContext ctx = Spring.initialize(context);
> router.HandleFunc("/req", goHandler)
> ```

> *Principles applied: P7, P10. "Spring" is a framework name and a technical code noun. "Go" is a language name and a technical code noun. Do not use either as a verb. Use "initialize" (code-domain technical verb, category 2 c) and "use" (approved verb) with the nouns.*

### Edge Case 3: Code Keywords That Look Like Nouns Used as Verbs

Some programming language keywords have the same spelling as nouns but function as keywords. For example: `class` (Java/C++ keyword), `new` (Java/C++ operator), `import` (Python/JavaScript keyword), `return` (ubiquitous keyword), `yield` (Python/C# keyword — also a verb), `async` (JavaScript/Python keyword — not a noun, but sounds like one to non-programmers).

RULE: Keywords are technical code nouns (Rule 1.5) when you refer to them as language features. When they appear in inline code formatting, they are quoted text. Do not use them as verbs in prose.

> **Non-STE:** You must `class` the data model and then `import` the dependencies.
>
> ```python
> # Non-STE: keywords used as verbs in prose and code
> class(data_model)
> import(dependencies)
> ```
>
> **STE:** You must make a `class` for the data model and then add the `import` statements for the dependencies.
>
> ```python
> # STE: keywords quoted as nouns; approved verbs carry action
> class DataModel:
>     pass
> import dependencies
> ```

> *Principles applied: P7, P6. The keywords `class` and `import` are technical code nouns. Do not use them as verbs in prose. Use "make" and "add" (approved verbs) with the keywords as nouns.*

> **Non-STE:** `return` the result and `yield` the intermediate values.
>
> ```python
> # Non-STE: keywords used as verbs
> return(result)
> yield(values)
> ```
>
> **STE:** Use `return` to give back the result and `yield` to supply the intermediate values.
>
> ```python
> # STE: keywords quoted as nouns; approved verbs carry action
> def gen():
>     return result
>     yield from intermediate_values
> ```

> *Principles applied: P7, P6. `return` and `yield` are keywords and technical code nouns. Do not use them as verbs even though they name actions. Use approved verbs "give back" and "supply" (or "send") with the keywords as quoted code nouns. NOTE: "return" is also an approved verb in the controlled terminology. When you mean the general action, use the approved verb "return" — but when you refer to the keyword, format it as inline code: `` `return` ``.*

### Edge Case 4: Generated Code and Auto-Generated Documentation

Generated code and auto-generated documentation do not always obey Rule 1.7. Code generators, protocol buffer compilers, OpenAPI spec generators, and ORM tools produce output that may convert nouns to verbs in symbol names (for example, a generated method named `toJson()` or `asMap()`).

RULE: Rule 1.7 applies to documentation that a human writes. Generated symbol names are exempt, but you must write any surrounding explanation in STE-Code. When you refer to a generated symbol name, treat it as a technical code noun (Rule 1.5). Do not change the generated name even if it violates Rule 1.7.

> **Non-STE:** The generated `UserBuilder` class can `User` the data and `Json` the output.
>
> ```java
> // Non-STE: nouns "User"/"Json" used as verbs in human-written prose
> UserBuilder b = new UserBuilder();
> b.User(data);
> b.Json(output);
> ```
>
> **STE:** The generated `UserBuilder` class makes a `User` object and encodes the output as JSON.
>
> ```java
> // STE: refer to generated symbols as nouns; use approved verbs
> UserBuilder b = new UserBuilder();
> User u = b.build(data);        // generated: makes a User object
> String out = b.toJson(output); // generated: encodes output as JSON
> ```

> *Principles applied: P7, P6. The method names `toJson()` or the class name `UserBuilder` are generated and fixed. Do not use "User" and "Json" as verbs in the prose. Use "makes" (approved verb) and "encodes" (code-domain technical verb, category 3 a) with the technical nouns.*

### Edge Case 5: Multi-Word Technical Nouns Used as Verbs

Some code-domain technical nouns have more than one word. For example, "load balancer" (category 6), "rate limiter" (category 6), "connection pool" (category 18), "feature flag" (category 16), "circuit breaker" (category 6). Developers often drop part of the noun to make a verb: "load balance," "rate limit," "connection pool" (used as a verb), "feature flag" (used as a verb).

RULE: Keep the multi-word technical noun as a noun phrase. Do not drop part of it to make a verb, and do not use the full phrase as a verb. Use an approved verb or a code-domain technical verb to describe the action.

> **Non-STE:** Load balance the requests, then rate limit the clients, and feature flag the new endpoint.
>
> ```python
> # Non-STE: multi-word nouns truncated or used as verbs
> load_balance(requests)
> rate_limit(clients)
> feature_flag(endpoint)
> ```
>
> **STE:** Distribute the requests with a load balancer. Then set a rate limit for the clients. Then put the new endpoint behind a feature flag.
>
> ```python
> # STE: full noun phrases; approved verbs carry the action
> balancer.distribute(requests)
> limiter.set_rate(clients)
> flags.enable(endpoint)
> ```

> *Principles applied: P7, P11. "Load balancer," "rate limit," and "feature flag" are multi-word code-domain technical nouns. Do not drop "balancer" to make "load balance" a verb. Do not use "rate limit" as a verb. Do not use "feature flag" as a verb. Use "distribute" and "set" (approved verbs) and "put" (approved verb) with the full technical noun phrases.*

> **Non-STE:** Circuit break the failing service and connection pool the database connections.
>
> ```python
> # Non-STE: "circuit break" / "connection pool" used as verbs
> circuit_break(service)
> connection_pool(db_connections)
> ```
>
> **STE:** Apply a circuit breaker to the failing service and use a connection pool for the database connections.
>
> ```python
> # STE: full noun phrases; approved verbs carry the action
> breaker.apply(service)
> pool = connection_pool.for_(db_connections)
> ```

> *Principles applied: P7, P1. "Circuit breaker" and "connection pool" are code-domain technical nouns. Do not use them as verbs. Use "apply" (approved verb) and "use" (approved verb) with the full technical noun phrases.*

---

## Cross-References

This rule connects to several other STE-Code rules. Read these rules together to make sure that your documentation obeys all of them.

| Related Rule | Relationship to Rule 1.7 |
|---|---|
| **Rule 1.1** — Use approved words from the dictionary | When a code-domain technical noun cannot be used as a verb, you must replace it with an approved verb from the controlled terminology. Check the dictionary for the correct approved verb. |
| **Rule 1.2** — Use words only as their specified part of speech | This rule is the direct application of Rule 1.2 to technical nouns. If a word is cataloged as a noun in your glossary, Rule 1.2 already forbids using it as a verb. Rule 1.7 extends this principle to all code-domain nouns. |
| **Rule 1.5** — Technical code nouns are allowed | This rule tells you which words are code-domain technical nouns. Rule 1.7 tells you that once a word is in a noun category, you must not use it as a verb. The two rules work together. |
| **Rule 1.12** — Technical verbs are allowed | This is the partner rule to Rule 1.7. Rule 1.12 tells you which words can be code-domain technical verbs. When a word appears in both a noun category (Rule 1.5) and a verb category (Rule 1.12), Rule 1.7 does not apply in the verb context. |
| **Rule 1.8** — Use standard, well-known technical nouns | When you must replace a noun-verb with a different construction, choose a standard technical noun. Do not invent a new noun to replace the verbed noun. |
| **Rule 1.13** — Do not use technical verbs as nouns | This is the inverse rule. Just as Rule 1.7 prevents nouns from becoming verbs, Rule 1.13 prevents verbs from becoming nouns. Together they keep the part-of-speech boundary clear between the two technical word categories. |
| **Rule 1.11** — One term per concept | When you choose an approved verb to replace a noun-verb, use the same approved verb everywhere for the same concept. Do not use "store" in one file and "put" in another for the same action. |
| **Section 3** — Verb rules (tense, mood, voice) | When you replace a noun-verb with an approved verb, the replacement verb must obey all verb rules in Section 3. Use the correct tense, mood, and voice. |

---

## Grammar Notes

### Noun Verbing and the Loss of Precision

When a code-domain technical noun becomes a verb, it lose its precise technical meaning. A "database" is a specific type of storage system with ACID properties, schemas, and query languages. The verb "to database" carries none of that meaning. It is not clear if it means "store," "index," "query," "back up," or "replicate."

The central grammatical justification for Rule 1.7 is that nouns and verbs have different semantic roles. A noun identifies an entity. A verb describes an action, process, or state. When you force a noun into a verb role, you obscure both the entity and the action. The reader must guess which property of the noun you intended to activate as a verb.

> **Non-STE:** The service must database the user data and then cache the results.
>
> ```python
> # Non-STE: "database" and "cache" used as verbs — meaning unclear
> service.database(user_data)
> service.cache(results)
> ```
>
> **STE:** The service must store the user data in the database and then put the results in the cache.
>
> ```python
> # STE: approved verbs name the action; nouns name the entity
> service.store(user_data, in_database=True)
> service.put(results, in_cache=True)
> ```

> *Principles applied: P7, P1. The non-STE version forces "database" and "cache" into verb roles. The reader must guess: does "database" mean store, index, or query? Does "cache" mean store temporarily, retrieve from cache, or invalidate? The STE version removes the guesswork by using approved verbs ("store," "put") that name the specific action, with the technical nouns ("database," "cache") that name the specific entities.*

### The Preposition Phrase Replacement Pattern

The most common repair for a noun-verb is to use an approved verb followed by the technical noun inside a prepositional phrase. This pattern keeps the noun as a noun and adds a precise verb.

| Noun-Verb Construction | STE Repair Pattern | Approved Verb | Preposition |
|---|---|---|---|
| "Cache the data" | "Put the data in the cache" | put | in |
| "Queue the job" | "Add the job to the queue" | add | to |
| "Buffer the output" | "Write the output to a buffer" | write | to |
| "Socket the connection" | "Send the connection through a socket" | send | through |
| "Database the records" | "Store the records in the database" | store | in |
| "Docker the app" | "Package the app in a container" | package | in |
| "Git the changes" | "Commit the changes" (or "Save the changes with Git") | commit / save | (none) / with |
| "JSON the response" | "Encode the response as JSON" | encode | as |

The choice of preposition depends on the relationship between the action and the entity. Use "in" for containment, "to" for destination, "through" for medium, "as" for format or role, and "with" for instrument.

### Noun Verbing in Compound Technical Nouns

When a code-domain technical noun is part of a compound noun phrase (for example, "database migration," "cache invalidation," "buffer overflow"), the noun stays as an adjective modifying another noun. This use is permitted and is not a violation of Rule 1.7. The rule only applies when the noun is the main verb of a clause.

> **STE:** Run the database migration script. (correct — "database" is an adjective modifying "migration script")
> **Non-STE:** Database the migration script. (incorrect — "database" is the main verb)
>
> **STE:** The cache invalidation policy triggers on write. (correct — "cache" is an adjective modifying "invalidation policy")
> **Non-STE:** Cache the invalidation policy. (incorrect — "cache" is the main verb and the meaning is different)

### Affect on Sentence Length

Obeying Rule 1.7 often makes sentences longer. The noun-verb construction is usually shorter (one word) than the approved-verb-plus-prepositional-phrase construction (three to five words). This increase in length is acceptable because the gain in clarity is larger than the loss of brevity.

> **Non-STE:** Cache the response. (3 words)
>
> **STE:** Put the response in the cache. (7 words)

The STE version is four words longer, but it removes all ambiguity. The reader knows exactly which action (put) applies to which entity (cache). The non-STE version is shorter but ambiguous: does "cache" mean store in cache, retrieve from cache, or invalidate the cache?

When sentence length becomes a problem (for example, in docstrings where space is limited), choose the shortest approved verb that gives the correct meaning. "Store the response in the cache" (6 words) is shorter than "Put the response in the cache" and is equally clear.

### The "Log" Exception and the Dual-Category Pattern

The spec gives "drill" as the example of a word that is both a technical noun and a technical verb. In STE-Code, "log" is the most frequent dual-category word. The grammar of "log" as a verb is simple: it takes a direct object (the data to record) and may take a prepositional phrase (the destination).

> **STE:** Log the error to the system log file.
> *"Log" is a code-domain technical verb (category 2 c). "Log file" is a code-domain technical noun (category 18). The sentence uses both correctly.*

The risk is that writers will use "log" as both a noun and a verb in ways that confuse the reader.

> **Non-STE:** Log the log to the log.
>
> ```python
> # Non-STE: "log" used three ways in one line
> log(log, log_file)
> ```
>
> **STE:** Write the log entry to the log file.
>
> ```python
> # STE: verb "log", noun "entry", noun "log file" kept distinct
> logger.log(entry)
> write_log_entry(entry, log_file)
> ```

> *Principles applied: P11, P7. When "log" appears three times with different meanings (verb, noun=entry, noun=file), the sentence is unclear. Use distinct terms: "log entry" for the data, "log file" for the destination, and "log" as the verb.*

### Imperative Mood and Noun Verbing

When a noun-verb appears in an instruction, it forces the noun into the imperative mood — a grammatical form that nouns do not have in English. This creates an ungrammatical construction.

> **Non-STE:** Docker the application. (imperative mood forced onto a noun)
>
> **STE:** Containerize the application. (imperative mood applied to a verb — correct)

The STE version uses "containerize," which is a code-domain technical verb that can correctly take the imperative mood. The non-STE version forces "Docker" into a slot that only verbs can occupy.

---

## Summary Checklist

Use this checklist to check that your documentation obeys Rule 1.7:

1. Find each sentence that has a code-domain technical noun as the main verb.
2. Check your project glossary: is the word cataloged as a noun only, or as both a noun and a verb?
3. If the word is a noun only, use an approved verb with the noun in a prepositional phrase.
4. If the word is both a noun and a verb, make sure you used the verb form correctly.
5. Check that you did not use a tool name, brand name, or protocol name as a verb.
6. Check that you did not drop part of a multi-word technical noun to make a verb.
7. Read the sentence again and make sure the action is clear and the entity is clear.

---

> **See also:** Rule 1.1 — Use Approved Words from the Dictionary
> **See also:** Rule 1.2 — Use Words Only as Their Specified Part of Speech
> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category
> **See also:** Rule 1.8 — Use Standard, Well-Known Technical Nouns
> **See also:** Rule 1.11 — One Term per Concept
> **See also:** Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category
> **See also:** Rule 1.13 — Do Not Use Technical Verbs as Nouns
