# Rule 1.5 — You Can Use Words That You Can Include in a Technical Noun Category

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.5

## Original Rule

**Rule 1.5** You can use words that you can include in a technical noun category.

A technical noun is a noun term that refers to a specified concept and is applicable to a subject field.

The dictionary does not include technical nouns because there are too many, and each subject field uses different technical nouns for their texts.

You can find many of these technical nouns in your company glossary or terminology database.

STE gives you a list of categories, with examples, to help you:
- Select technical nouns to put in your company glossary or terminology database.
- Use technical nouns correctly.

You can use technical nouns in procedural and descriptive writing if you can include them in one or more of these twenty-two categories.

[Original spec lists 22 categories — see master.md lines 2540-2627]

## STE-Code Adaptation

**Rule 1.5** You can use words that you can include in a code-domain technical noun category.

A code-domain technical noun is a noun term that refers to a specified concept in software development and is applicable to a subject field.

The controlled terminology does not include all code-domain technical nouns because there are too many, and each project or subject field uses different technical nouns.

You can find many of these code-domain technical nouns in your project glossary or terminology database.

STE-Code gives you a list of categories, with examples, to help you:
- Select code-domain technical nouns to put in your project glossary or terminology database.
- Use code-domain technical nouns correctly.

You can use code-domain technical nouns in procedural and descriptive writing if you can include them in one or more of these nineteen categories.

1. **Code components, modules, and libraries**
   Terms that refer to software parts, packages, and reusable units of code.
   class, controller, helper, hook, middleware, mixin, module, package, plugin, provider, repository, service, utility

2. **Computing devices and their components**
   Terms that refer to hardware, devices, and physical computing resources.
   CPU, disk, GPU, keyboard, laptop, memory, monitor, mouse, printer, screen, server, smartphone, tablet, terminal

3. **Development tools, environments, and support equipment**
   Terms that refer to software development tools, IDEs, build systems, and testing frameworks.
   CLI, compiler, debugger, Docker, editor, IDE, Git, Jest, linter, loader, Prettier, terminal, test runner, TypeScript, webpack

4. **Data structures, types, and formats**
   Terms that refer to data representation, storage structures, and file formats.
   array, boolean, buffer, CSV, enum, hash map, integer, JSON, linked list, object, queue, stack, string, struct, tree, tuple, XML, YAML

5. **Infrastructure, deployment, and platforms**
   Terms that refer to hosting, deployment, containerization, and runtime platforms.
   AWS, CI/CD, container, deployment, Heroku, Kubernetes, load balancer, Node.js, pipeline, pod, production, staging, Vercel

6. **Systems, subsystems, and architectural components**
   Terms that refer to system design, architecture patterns, and their parts.
   API gateway, authentication layer, caching layer, client, database layer, message broker, microservice, proxy, rate limiter, REST API, routing layer, server, WebSocket

7. **Mathematical, algorithmic, and scientific terms**
   Terms that refer to algorithms, computational concepts, and mathematical formulas.
   Big O notation, binary search, coefficient, complexity, exponent, hash function, iteration, logarithm, matrix, recursion, regex, sorting algorithm, time complexity, traversal

8. **Interface elements and navigation**
   Terms that refer to UI components, navigation controls, and layout elements.
   button, checkbox, dialog, dropdown, footer, header, menu, modal, navigation bar, radio button, scrollbar, sidebar, tab, text field, toggle, tooltip

9. **Numbers, units of measurement, and time**
   Terms that refer to quantitative data, measurements, and time-related information.
   byte, gigabyte (GB), hertz (Hz), hour (h), kilobyte (KB), megabyte (MB), millisecond (ms), minute, nanosecond (ns), second (s), terabyte (TB)

10. **Quoted text**
    Terms that refer to texts that you cannot change in code documentation. For example, error messages, code snippets, UI labels, and log output.
    `Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused`

11. **Professional roles, teams, and organizations**
    Terms that refer to roles, individuals, organizations, and teams related to software development.
    administrator, backend developer, contributor, DevOps engineer, frontend developer, Google, maintainer, Microsoft, product owner, QA engineer, reviewer, scrum master, user

12. **Official documents, API references, and standards**
    Terms that refer to documentation types, standards, specifications, and their structural parts.
    API reference, changelog, code of conduct, contributing guide, diagram, figure, Getting Started guide, HTTP specification, note, paragraph, README, release notes, RFC, section, table, warning

13. **Runtime environments and operational conditions**
    Terms that refer to execution contexts, environment variables, and operating parameters.
    development, environment variable, garbage collection, heap, hot reload, live reload, memory leak, production, sandbox, stack trace, staging, test, thread, timeout, virtual machine

14. **Colors**
    Terms that refer to colors that identify color-related properties in code (for example, CSS, terminal output, syntax highlighting).
    black, blue, cyan, gray, green, magenta, orange, red, white, yellow
    Colors are adjectives, but STE-Code identifies them as code-domain technical nouns. Comparative and superlative forms of colors (for example, blacker, the reddest) are not permitted in STE-Code.

15. **Defects, errors, and fault terminology**
    Terms that refer to types of software defects, errors, and malfunctions.
    assertion failure, bug, crash, deadlock, defect, exception, hang, infinite loop, memory leak, null pointer, race condition, regression, stack overflow, timeout, type error

16. **Computer science, information, and communication technology**
    Terms that refer to concepts, technologies, and architectures in computing and communication.
    AI, algorithm, authentication, authorization, blockchain, containerization, cryptography, database, encoding, encryption, firewall, hashing, internet, machine learning, metadata, neural network, protocol, query, sandbox, schema, token, virtualization

17. **Legal and licensing terms**
    Terms that refer to software licenses, legal documents, and compliance terminology.
    Apache 2.0, BSD license, compliance, copyright, GPL, license, MIT license, open source, proprietary, terms of service, third-party, trademark, warranty

18. **Database and storage terminology**
    Terms that refer to database concepts, storage systems, and data persistence.
    connection pool, cursor, foreign key, index, migration, NoSQL, ORM, PostgreSQL, primary key, query, Redis, relation, row, schema, seed, SQL, SQLite, stored procedure, table, transaction, view

19. **Network and protocol terminology**
    Terms that refer to networking concepts, protocols, and communication.
    DNS, endpoint, HTTP, HTTPS, IP address, localhost, middleware, packet, port, request, response, route, socket, SSH, TCP, TLS, UDP, URL, VPN, WebSocket

The code-domain technical nouns in their related categories are only examples. Rule 1.5 does not give a full list of all possible code-domain technical nouns.

### Examples

> **Non-STE:** The developer used the thing to get data from the storage layer and put it on the screen.
> **STE:** The frontend developer used the API client to get data from the database and show it on the UI.

"Frontend developer" is a code-domain technical noun (category 11, professional roles). "API client" and "database" are code-domain technical nouns (category 16, computer science). "UI" is a code-domain technical noun (category 8, interface elements).
