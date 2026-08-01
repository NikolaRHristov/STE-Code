# Level 3 — Core Principles (Words: Rules 1.1–1.14)

Section 1 of STE-Code governs **words**: which words you may use, in which part
of speech, with which meaning, and in which form. Every other section of the
standard assumes these fourteen rules already hold.

Three gates decide whether a word is allowed in code documentation:

1. The word is **approved in the controlled terminology** (STE-Code part 2), or
2. The word is a **code-domain technical noun** (Rule 1.5 categories), or
3. The word is a **code-domain technical verb** (Rule 1.12 categories).

A word that passes no gate must be replaced, or the sentence must be
restructured so that approved words can carry the meaning.

Definitions used throughout:

- **Controlled terminology** — the STE-Code approved word list. Each entry gives
  one part of speech and one approved meaning, plus the approved verb and
  adjective forms.
- **Code-domain technical noun** — a noun term for a specified concept in
  software development, applicable to a subject field (Rule 1.5, 19 categories).
- **Code-domain technical verb** — a verb term for a specified operation or
  process in software development (Rule 1.12, 4 categories).

Rule index:

| Rule | Statement |
|------|-----------|
| 1.1 | Use words that are approved in the controlled terminology, code-domain technical nouns, or code-domain technical verbs. |
| 1.2 | Use approved words only as the specified part of speech. |
| 1.3 | Use approved words only with their approved meanings. |
| 1.4 | Use only the approved forms of verbs and adjectives. |
| 1.5 | You can use words that you can include in a code-domain technical noun category. |
| 1.6 | Use a word that is not approved only when it is a code-domain technical noun or part of one. |
| 1.7 | Do not use words that are code-domain technical nouns as verbs. |
| 1.8 | Use code-domain technical nouns that are approved in your project, company, industry, or subject field. |
| 1.9 | When you must select a code-domain technical noun, use one which is short and easy to understand. |
| 1.10 | Do not use regional, slang, or jargon words as code-domain technical nouns. |
| 1.11 | Do not use different code-domain technical nouns for the same item. |
| 1.12 | You can use verbs that you can include in a code-domain technical verb category. |
| 1.13 | Do not use code-domain technical verbs as nouns. |
| 1.14 | Use American English spelling unless other official directives tell you differently. |

---

## Rule 1.1 — Use approved words, code-domain technical nouns, or code-domain technical verbs

In code documentation, use words that are:

- approved in the project controlled terminology,
- code-domain technical nouns, or
- code-domain technical verbs.

The controlled terminology gives the words most frequently used in code
documentation. It also lists words that are **not** approved, with approved
alternatives. Your project glossary or terminology database holds the technical
nouns and technical verbs of your subject field; always check it first.

Worked vocabulary swaps:

| Do not write | Write | Why |
|---|---|---|
| execute the script | run the script | "run" is the approved verb for executing programs |
| generate the artifact | make the artifact | "make" is approved; "generate" is not |
| utilize / leverage the cache | use the cache | inflated verb |
| bootstrap / initiate the service | start the service | "start" is approved |
| configure the runtime | set the runtime behavior | "set" is approved |
| retrieve / fetch the record | get the record | "get" is approved |
| transmit the payload | send the data | "send" is approved |
| validate / verify the input | check the input | "check" is approved |
| unable to connect | cannot connect | "cannot" is approved |
| invalid / malformed data | incorrect data, data that is not correct | "correct" is the approved adjective |

Technical terms stay: `UserAuthenticator` is a code-domain technical noun,
`serialize` is a code-domain technical verb, and both are permitted although
neither is in the controlled terminology.

Examples by documentation type:

> **Non-STE (README):** To begin utilizing the build toolchain, you must first
> generate the distributable artifact, then execute the compiled binary to
> bootstrap the local development service.
>
> **STE:** Use the build tool to make the binary. Run the binary to start the
> local service.

> **Non-STE (JSDoc):** Fetches a user record. The duration in milliseconds the
> client shall await a response prior to terminating the connection attempt.
>
> **STE:** Gets a user record. The time in milliseconds that the client waits
> for a response before it stops the connection.

> **Non-STE (docstring):** Performs validation on the input data to ensure it
> conforms to the expected schema.
>
> **STE:** Checks the input data against the schema. Gives `True` when the data
> is correct and `False` when the data is not correct.

> **Non-STE (commit):** feat: implement JWT authentication middleware
>
> **STE:** feat: add JWT authentication middleware

> **Non-STE (CLI error):** Unable to establish connection to the database.
> Please verify your credentials and retry.
>
> **STE:** Cannot connect to the database. Check your credentials and try again.

Paradigm notes:

- **Object-oriented** — prose uses approved verbs (make, get, set, call, send,
  keep). Class, method, and pattern names stay as technical nouns.
- **Functional** — `map`, `fold`, `reduce`, `filter`, `compose`, and `curry` are
  code-domain technical verbs, permitted under Rule 1.12. "Pure function" is a
  compound code-domain technical noun.
- **Procedural** — each step starts with an approved imperative verb.
  "Allocate" is not approved: write "make a buffer". "Free" and "dereference"
  are code-domain technical verbs.
- **Declarative** — SQL keywords and resource kind names are technical terms.
  "Provision" is not approved (use "make" or "set up"); "orchestrate" is not
  approved (use "control" or "manage").
- **Systems** — "own", "borrow", and "move" are Rust technical verbs.
  "Dangling pointer" and "undefined behavior" are compound technical nouns
  (category 15).

---

## Rule 1.2 — Use approved words only as the specified part of speech

Each entry in the controlled terminology carries one label: verb (v), noun (n),
adjective (adj), adverb (adv), preposition (prep), conjunction (conj), pronoun
(pron), or article (art). Use the word only in that grammatical role.

- "Query" is an approved **noun**, not a verb. Write "Send a query to the
  database", not "Query the database".
- "Static" is an approved **adjective**, not a verb. Write "Make the variable
  static", not "Static the variable".
- Some words carry more than one label. "Call" is an approved verb and an
  approved noun; the position in the sentence shows the function.

If the word you want is not in the controlled terminology:

1. Find the word in a standard English dictionary.
2. Find the best synonym that is approved in the STE-Code controlled terminology.
3. Use that approved word, or write a different sentence construction.

When you replace a word, make sure that the meaning does not change. If it
changes, select a different word or restructure the sentence.

| Violating form (do not use) | Part-of-speech error | Approved replacement |
|---|---|---|
| Query the database / Cache the result / Queue the job / Log the error / Index the record | technical noun used as verb | Send a query / Keep the result in the cache / Put the job in the queue / Write the error in the log / Use the index to find the record |
| Docker the app / Git the change / Kubectl the pod / Terraform the VPC | tool name used as verb | Use Docker / Save with Git / Use `kubectl` / Use Terraform |
| Secure the endpoint / Empty the buffer / Silent the log | adjective used as verb | Make the endpoint secure / Make the buffer empty / Make the log silent |
| Static the variable / Ready the worker / Live the connection | adjective used as verb | Make the variable static / Make the worker ready / Make the connection live |
| Utilize / Leverage / Employ the service | inflated verb | Use the service |
| Commence the build / Initiate the transfer / Terminate the process | inflated verb | Start the build / Start the transfer / Stop the process |
| Orchestrate the services / Facilitate the sync | unapproved verb | Control the services / Help the sync |

Examples:

> **Non-STE:** Docker the app and deploy to production. If it fails, rollback.
>
> **STE:** Use Docker to make a container for the application. Deploy the
> container to production. If the deployment fails, roll back to the previous
> version.

> **Non-STE:** Creates a user. Caches the profile. Errors on duplicate email.
>
> **STE:** Makes a new user record. Keeps the profile in the cache. Gives an
> error on a duplicate email address.

> **Non-STE:** # init the pool, then cache the results, finally error if null
>
> **STE:** # Start the connection pool. Keep the results in the cache. Give an
> error when the value is null.

> **Non-STE:** Error: Connection timeout. The server timed out after 30s.
>
> **STE:** Error: Connection did not complete. The server did not answer within
> the 30-second timeout.

Paradigm notes: "Factory the object" and "Singleton the instance" are OOP
violations (use "Make the object with a factory", "Get the singleton
instance"). "Malloc a buffer" and "Goroutine the task" are procedural
violations (use "Make a buffer with `malloc`", "Run the task in a goroutine").
"Terraform the VPC" is a declarative violation (use "Use Terraform to make the
VPC"). In Rust, mark keywords with backticks: "The function uses `unsafe` for
the pointer access."

---

## Rule 1.3 — Use approved words only with their approved meanings

Each approved word has one specified meaning, which is often narrower than the
standard English meaning. Do not use an approved word with any other meaning.

- The approved meaning of the verb **follow** is "come after, go after". Use it
  only for sequence: "Do the steps that follow."
- The approved meaning of the verb **obey** is "to do that which the procedures
  or instructions tell you". Use it for compliance: "Obey the instructions."

Four-step check for every approved word you write:

1. **Identify the part of speech** as you used it in the sentence.
2. **Look up the approved meaning** for that part of speech in the controlled
   terminology.
3. **Ask: does my sentence use exactly that meaning?** If not, the word fails —
   even when the word is approved and the sentence reads well.
4. **Replace or restructure** so the approved word carries its approved meaning.

Worked check:

> **Sentence:** The background worker runs every night.
> **Step 1:** "runs" is a verb.
> **Step 2:** Approved meaning of "run" = "execute a program or command".
> **Step 3:** The writer means "operates on a schedule". The meaning does not match.
> **Step 4:** Rewrite: "The background worker operates every night."

Examples:

> **Non-STE:** Follow the configuration steps to set up the server. After you
> follow the steps, the service starts and listens on port 8080.
>
> **STE:** Obey the configuration instructions to set up the server. After you
> do the steps that follow, the service starts and listens on port 8080.

---

## Rule 1.4 — Use only the approved forms of verbs and adjectives

The controlled terminology gives each approved verb with its approved forms, and
each approved adjective in the base form with the comparative and superlative
forms where applicable.

Verb entry:

COMPILE (v), COMPILES, COMPILED, COMPILED

| Infinitive / imperative | Simple present | Simple past | Past participle (as adjective) |
|---|---|---|---|
| (To) Compile / Compile | Compile(s) | Compiled | Compiled |

Forms that are not listed are not permitted: "compilating" and "compilates" are
both incorrect.

Adjective entry:

FAST (adj) (FASTER, FASTEST) — base form *fast*, comparative *faster*,
superlative *fastest*. Adjectives that make their comparative and superlative
with "more" and "most" have no extra forms in the terminology, because "more"
and "most" are approved words.

Do not use the "-ing" form as a main verb in procedural writing unless the
controlled terminology lists it.

Examples:

> **Non-STE:** The compiler is compilating the source files every time you save
> the document.
>
> **STE:** The compiler compiles the source files each time you save the
> document.

> **Non-STE:** This algorithm is more fast than the previous one.
>
> **STE:** This algorithm is faster than the previous one.

> **Non-STE:** After installing the dependencies, you can start compiling the
> project by running the build script.
>
> **STE:** After you install the dependencies, compile the project with the
> build script.

---

## Rule 1.5 — Code-domain technical noun categories

A code-domain technical noun is a noun term for a specified concept in software
development, applicable to a subject field. The controlled terminology cannot
list them all, because each project uses different ones; keep yours in the
project glossary or terminology database.

You may use a code-domain technical noun in procedural and descriptive writing
when you can put it in one or more of these **nineteen** categories. The words
shown are examples only, not a complete list.

| # | Category | Example terms |
|---|---|---|
| 1 | Code components, modules, and libraries | class, controller, helper, hook, middleware, mixin, module, package, plugin, provider, repository, service, utility |
| 2 | Computing devices and their components | CPU, disk, GPU, keyboard, laptop, memory, monitor, mouse, printer, screen, server, smartphone, tablet, terminal |
| 3 | Development tools, environments, and support equipment | CLI, compiler, debugger, Docker, editor, IDE, Git, Jest, linter, loader, Prettier, terminal, test runner, TypeScript, webpack |
| 4 | Data structures, types, and formats | array, boolean, buffer, CSV, enum, hash map, integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML |
| 5 | Infrastructure, deployment, and platforms | AWS, CI/CD, container, deployment, Heroku, Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel |
| 6 | Systems, subsystems, and architectural components | API gateway, authentication layer, caching layer, client, database layer, message broker, microservice, proxy, rate limiter, REST API, routing layer, server, WebSocket |
| 7 | Mathematical, algorithmic, and scientific terms | Big O notation, binary search, coefficient, complexity, exponent, hash function, iteration, logarithm, matrix, recursion, regex, sorting algorithm, time complexity, traversal |
| 8 | Interface elements and navigation | button, checkbox, dialog, dropdown, footer, header, menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field, toggle, tooltip |
| 9 | Numbers, units of measurement, and time | byte, gigabyte (GB), hertz (Hz), hour (h), kilobyte (KB), megabyte (MB), millisecond (ms), minute, nanosecond (ns), second (s), terabyte (TB) |
| 10 | Quoted text (text you cannot change: error messages, code snippets, UI labels, log output) | `Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused` |
| 11 | Professional roles, teams, and organizations | administrator, backend developer, contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner, QA engineer, reviewer, scrum master, user |
| 12 | Official documents, API references, and standards | API reference, changelog, code of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification, note, paragraph, README, release notes, RFC, section, table, warning |
| 13 | Runtime environments and operational conditions | development, environment variable, garbage collection, heap, hot reload, live reload, memory leak, production, sandbox, stack trace, staging, test, thread, timeout, virtual machine |
| 14 | Colors | black, blue, cyan, gray, green, magenta, orange, red, white, yellow |
| 15 | Defects, errors, and fault terminology | assertion failure, bug, crash, deadlock, defect, exception, hang, infinite loop, memory leak, null pointer, race condition, regression, stack overflow, timeout, type error |
| 16 | Computer science, information, and communication technology | AI, algorithm, authentication, authorization, blockchain, containerization, cryptography, database, encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural network, protocol, query, sandbox, schema, token, virtualization |
| 17 | Legal and licensing terms | Apache 2.0, BSD license, compliance, copyright, GPL, license, MIT license, open source, proprietary, terms of service, third-party, trademark, warranty |
| 18 | Database and storage terminology | connection pool, cursor, foreign key, index, migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite, stored procedure, table, transaction, view |
| 19 | Network and protocol terminology | DNS, endpoint, HTTP, HTTPS, IP address, localhost, middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL, VPN, WebSocket |

Note on category 14: colors are adjectives, but STE-Code identifies them as
code-domain technical nouns. Comparative and superlative forms of colors (for
example "blacker", "the reddest") are not permitted.

---

## Rule 1.6 — Unapproved words are permitted only inside technical nouns

A word that the controlled terminology marks as not approved fails when you use
it as a general noun or adjective, and passes when it is part of a recognized
code-domain technical noun.

**"Handler"** — not approved; the alternative is "function (n)".

> **Non-STE:** The handler processes each incoming event.
>
> **STE:** The function processes each incoming event.
>
> **STE:** The event handler processes each incoming event.
> ("Event handler" is a code-domain technical noun, category 1.)

**"Main"** — not approved as a general adjective; the alternative is
"primary (adj)".

> **Non-STE:** The main configuration has the latest values.
>
> **STE:** The primary configuration has the latest values.
>
> **STE:** Merge the feature branch into the main branch.
> ("Main branch" is a code-domain technical noun, category 5. Do not write
> "primary branch" — that is not the approved technical noun.)

**"Base"** — not approved for a surface location; the alternative is
"bottom (n)". "Base" stays inside the technical nouns "base case" (category 7)
and "base class" (category 1).

> **Non-STE:** Copy the files to the base of the build folder.
>
> **STE:** Copy the files to the bottom of the build folder.

---

## Rule 1.7 — Do not use code-domain technical nouns as verbs

Use a code-domain technical noun only as a noun, or as an adjective inside a
different technical noun. Restructure the sentence with an approved verb.

> **Non-STE:** Database the user records before the migration.
>
> **STE:** Store the user records in the database before the migration.

> **Non-STE:** Cache the API responses to improve performance.
>
> **STE:** Store the API responses in the cache to improve performance.

A word can be a technical noun **and** a technical verb when it fits a category
in Rule 1.5 and a category in Rule 1.12. Your project glossary decides:

> **STE (noun):** Write a log entry for each failed request.
>
> **STE (verb):** Log each failed request.

If your glossary lists the word only as a technical noun, obey Rule 1.7 and use
a different sentence construction.

> **See also:** Rule 1.5, Rule 1.12, Rule 1.13.

---

## Rule 1.8 — Use the technical nouns approved in your project or field

If your project, company, industry, or subject field already has an approved
name for a class, module, function, method, variable, component, or process,
use that name. These names live in your project glossary, API documentation,
coding standards, or company documentation.

Do not invent your own names for items that already have established names.
The source of truth is the repository.

> **STE:** The dashboard page has a `UserTable` component and a `FilterPanel`
> component.

> **Non-STE:** The account controller manages login and user profile operations.
>
> **STE:** The `AccountController` manages authentication and user profile
> operations.

---

## Rule 1.9 — Select short, easy technical nouns

When no approved technical noun exists in your project, company, industry, or
subject field, select one that is short (not more than three words) and easy to
understand. Do not write a long descriptive phrase when a shorter term is
enough. When the context identifies the item — a code snippet, a line number, a
diagram, an API reference — use the shortest unambiguous term. Add one or two
adjectives only when clarification is necessary.

```javascript
// client.js — line 42
async function fetchUtility(url) {
  const response = await fetch(url);
  return response.json();
}
```

> **Non-STE:** Call the asynchronous JavaScript XML HTTP request wrapper utility
> function (line 42) to get the serialized JSON payload from the remote
> application programming interface endpoint.
>
> **STE:** Call the `fetchUtility` function (line 42) to get the JSON data from
> the API endpoint.

---

## Rule 1.10 — No regional, slang, or jargon words as technical nouns

Some technical words are used only inside confined communities or single
technology ecosystems. They are not easy to understand for readers from a
different background or stack. Code documentation is read by junior developers,
developers from other language communities, and non-native English speakers: a
word that one subculture finds clear can be opaque to every other reader.
Always select well-known words.

| Do not write | Write |
|---|---|
| Remove all the cruft from the legacy module. | Remove all the unnecessary code from the legacy module. |
| The function monkeys with the input data before validation. | The function changes the input data before validation. |
| Bikeshedding delayed the API design by two weeks. | Unnecessary discussion about small details delayed the API design by two weeks. |
| I spent the morning yak shaving before I could write the test. | I spent the morning completing unrelated prerequisite tasks before I could write the test. |
| Replace the foo and bar placeholders with real values. | Replace the example and placeholder values with real values. |

---

## Rule 1.11 — One technical noun per item

Do not use a different code-domain technical noun in another part of your
documentation for the same item. Changing the name of one item between sections
forces the reader to decide whether you mean the same item or a different one.
The source of truth for the name is the code: the class, function, module,
table, resource, environment variable, or configuration key as it is defined in
the repository.

> **Non-STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the AccountManager to verify a user.
> 3. The UserHandler returns a session token that you send in later requests.
>
> **STE:**
> 1. Initialize the UserService class to start the session manager.
> 2. Call the authenticate method on the UserService to verify a user.
> 3. The UserService returns a session token that you send in later requests.

> **Non-STE:** "/api/login path", "authentication route", "login endpoint" —
> three names for one endpoint.
>
> **STE:** Use "/api/login endpoint" in every sentence, because the OpenAPI file
> defines the path as `/api/login`.
