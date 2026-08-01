# Level -1 — Synonym / Approved-Word Table

Minimal vocabulary layer of STE-Code. One meaning, one word. If a word appears in
the **Not approved** column, replace it with the word in the **Approved** column.

Scope rule (Rule 1.1 / Rule 1.5): a word is allowed if it is
1. approved in the controlled terminology (tables below), or
2. a code-domain technical noun (Rule 1.5 categories), or
3. a code-domain technical verb.

Nothing else. Do not invent synonyms.

---

## 1. Approved verbs

Use the approved verb in imperative steps and in descriptive prose. The
"Not approved" words are rejected for that meaning.

| Approved | Not approved | Meaning |
|---|---|---|
| use | utilize, leverage, employ | Apply an existing function, library, or component without changing its internals. |
| start | initiate, commence, bootstrap | Begin execution of a process, service, or background task. |
| stop | terminate, halt, kill | End execution of a running process or service in a controlled way. |
| show | display, render, present | Make a value, status, or result visible in the interface or in a log. |
| make | create, generate, produce | Build a new object, file, or data structure as the result of an operation. |
| get | retrieve, fetch, obtain | Read a value, record, or resource from a store, API, or cache. |
| set | configure, assign, establish | Assign a value to a variable, field, or configuration option. |
| check | verify, validate, ensure | Examine a condition or value to confirm it matches the expected result. |
| do | perform, execute, carry out | Run a defined operation or unit of work. |
| send | transmit, dispatch, forward | Transfer a message, request, or event over a channel. |
| remove | delete, eliminate, purge | Take out a file, record, or component so it is no longer present. |
| keep | retain, preserve, maintain | Hold a value, file, or resource in its current state. |
| add | append, insert, include | Put an extra element or field into a collection or configuration. |
| change | modify, alter, update | Make a controlled modification without replacing the whole item. |
| write | persist, save, store | Put data into a file, database, or output stream for later use. |
| read | load, parse, ingest | Obtain data from a file, stream, or input source. |
| connect | attach, link, associate | Establish a channel between two components, services, or endpoints. |
| close | shut, release, disconnect | End an open connection, file handle, or stream. |

### Verb examples

| Write this | Do not write this |
|---|---|
| Use the logger to record the request identifier before you return the response. | Leverage the logger to capture the request identifier prior to returning the response. |
| Start the worker process before the test suite connects to the message queue. | Commence the worker process prior to the test suite establishing a connection. |
| Stop the server before you change the configuration file. | Terminate the server prior to modifying the configuration file. |
| Make a backup copy of the database before you run the migration script. | Generate a backup copy of the database before you run the migration script. |
| Check that the response status is 200 before you parse the JSON body. | Validate that the response status is 200 prior to parsing the JSON body. |
| Set the timeout to thirty seconds before you open the network connection. | Configure the timeout to thirty seconds before establishing the network connection. |
| Use the built-in sort function to order the list before you print it. | Utilize the built-in sort function to order the list before printing it. |

---

## 2. Approved technical nouns

These are code-domain technical nouns (Rule 1.5). Use the approved name; do not
substitute a loose paraphrase.

| Approved noun | Not approved |
|---|---|
| AuthenticationService | login handler, auth component, credential service |
| CacheManager | cache store, memoization layer, buffer manager |
| Logger | log writer, event recorder, trace emitter |
| RateLimiter | throttle controller, request governor, flow regulator |
| HttpClient | request sender, web caller, rest client |
| Result<T, E> | either type, outcome wrapper, try result |
| ConfigMap | settings object, configuration holder, option store |
| TreeNode | node element, tree item, hierarchy unit |
| Payload | data bundle, message body, request content |
| ConnectionPool | socket group, session store, connection cache |
| BuildPipeline | compile flow, build chain, assembly process |
| MigrationScript | schema update, database patch, version step |
| DeployStep | rollout action, release task, push operation |
| IdleState | inactive mode, standby condition, dormant status |
| ErrorState | failure mode, fault condition, broken status |
| Middleware | request filter, interceptor piece, pipeline part |
| Plugin | add-on module, extension part, optional unit |
| Timeout | wait limit, expiry period, deadline value |
| AvailabilityZone | data region, server location, host area |
| LoggingSystem | trace framework, log facility, record subsystem |

---

## 3. Approved domain terms

One approved term for each subject field. The rejected column lists common
near-synonyms that must not be used for that concept.

| Approved term | Subject field | Not approved |
|---|---|---|
| orchestrator | containerization | scheduler, cluster manager, container manager |
| subnet | networking | network slice, IP range, address block |
| mock | testing | stub, fake, dummy object |
| telemetry | observability | instrumentation data, system signals, monitoring output |
| pipeline | CI/CD | build chain, workflow, job stream |
| index | database | lookup table, secondary structure, access path |
| authentication | security | auth, login check, identity confirmation |
| idempotency | distributed systems | repeat safety, retry proof, safe re-execution |
| autoscaling | cloud | elastic resize, self-adjust, dynamic capacity |
| hydration | frontend | client boot, attach behavior, re-render bind |
| rebase | version control | transplant, replay commits, restack |
| eviction | caching | purge rule, drop policy, clearance |
| broker | message queue | message hub, relay, dispatcher |
| pagination | API design | paged results, chunking, windowing |
| latency | performance | response delay, wait time, lag |
| rollout | deployment | push, ship, go-live |
| structured log | logging | plain log, text log, raw print |
| race condition | concurrency | timing bug, collision, concurrent fault |
| cipher | encryption | crypto scheme, codec, scrambler |
| alert | monitoring | warning, trigger, notification event |

---

## 4. Approved adjectives

Each adjective has one technical meaning. Use it only in that meaning.

| Adjective | Meaning |
|---|---|
| idempotent | The operation gives the same result when applied more than once, with no extra side effects. |
| immutable | The value cannot be changed after it is created. |
| atomic | The operation completes fully or not at all; no partial state is visible. |
| thread-safe | The code stays correct when more than one thread calls it at the same time. |
| asynchronous | The operation returns before the work completes; the result arrives later. |
| concurrent | More than one task makes progress in overlapping time. |
| deterministic | The same input always gives the same output. |
| deprecated | The item still works but must not be used in new code; it will be removed. |
| nullable | The value is permitted to be null or absent. |
| serializable | The value can be converted to a byte or text form and read back. |
| stateless | The component keeps no data between calls. |
| backward-compatible | Existing callers continue to work after the change. |
| read-only | The value can be read but not written. |
| recursive | The function or structure refers to itself. |
| monotonic | The value only increases, or only decreases, over time. |
| transitive | If A relates to B and B relates to C, then A relates to C. |
| volatile | The value can change outside the current thread of control. |
| hierarchical | The items are arranged as a tree of parents and children. |
| normalized | The data is stored in one canonical form, with no duplication. |
| incremental | The work is done in small steps that add to the previous result. |

Adjective examples:

> **Do not write:** Leverage an idempotent retry handler so a duplicate invocation will not create a redundant record.
>
> **Write:** Make the retry handler idempotent so a second call with the same input does not duplicate the record.

> **Do not write:** Utilize an immutable request context so concurrent threads will not overwrite shared values during processing.
>
> **Write:** Keep the request context immutable so concurrent threads cannot overwrite each other's values during one operation.

---

## 5. Technical-noun categories (Rule 1.5)

A word that is not in the tables above is still allowed if it belongs to one of
these nineteen code-domain technical noun categories.

1. **Code components, modules, and libraries** — class, controller, helper, hook, middleware, mixin, module, package, plugin, provider, repository, service, utility
2. **Computing devices and their components** — CPU, disk, GPU, keyboard, laptop, memory, monitor, mouse, printer, screen, server, smartphone, tablet, terminal
3. **Development tools and environments** — CLI, compiler, debugger, Docker, editor, IDE, Git, Jest, linter, loader, Prettier, terminal, test runner, TypeScript, webpack
4. **Data structures, types, and formats** — array, boolean, buffer, CSV, enum, hash map, integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML
5. **Infrastructure, deployment, and platforms** — AWS, CI/CD, container, deployment, Heroku, Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel
6. **Systems and architectural components** — API gateway, authentication layer, caching layer, client, database layer, message broker, microservice, proxy, rate limiter, REST API, routing layer, server, WebSocket
7. **Mathematical and algorithmic terms** — Big O notation, binary search, coefficient, complexity, exponent, hash function, iteration, logarithm, matrix, recursion, regex, sorting algorithm, time complexity, traversal
8. **Interface elements and navigation** — button, checkbox, dialog, dropdown, footer, header, menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field, toggle, tooltip
9. **Numbers, units of measurement, and time** — byte, gigabyte (GB), hertz (Hz), hour (h), kilobyte (KB), megabyte (MB), millisecond (ms), minute, nanosecond (ns), second (s), terabyte (TB)
10. **Quoted text** — `Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused`
11. **Professional roles, teams, and organizations** — administrator, backend developer, contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner, QA engineer, reviewer, scrum master, user
12. **Documents, API references, and standards** — API reference, changelog, code of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification, note, paragraph, README, release notes, RFC, section, table, warning
13. **Runtime environments and operational conditions** — development, environment variable, garbage collection, heap, hot reload, live reload, memory leak, production, sandbox, stack trace, staging, test, thread, timeout, virtual machine
14. **Colors** — black, blue, cyan, gray, green, magenta, orange, red, white, yellow. Colors are adjectives, but STE-Code treats them as technical nouns. Do not use comparative or superlative forms (blacker, the reddest).
15. **Defects, errors, and faults** — assertion failure, bug, crash, deadlock, defect, exception, hang, infinite loop, memory leak, null pointer, race condition, regression, stack overflow, timeout, type error
16. **Computer science, information, and communication technology** — AI, algorithm, authentication, authorization, blockchain, containerization, cryptography, database, encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural network, protocol, query, sandbox, schema, token, virtualization
17. **Legal and licensing terms** — Apache 2.0, BSD license, compliance, copyright, GPL, license, MIT license, open source, proprietary, terms of service, third-party, trademark, warranty
18. **Database and storage terminology** — connection pool, cursor, foreign key, index, migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite, stored procedure, table, transaction, view
19. **Network and protocol terminology** — DNS, endpoint, HTTP, HTTPS, IP address, localhost, middleware, packet, port, request, response, route, socket

Record project-specific technical nouns in the project glossary or terminology
database before you use them in documentation.
