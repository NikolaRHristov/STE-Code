# STE-Code — Level -1 (Core)

> Tier: -1 of STE-Code. Scope: the 14 core word-choice principles (Section 1 of
> the full standard) plus the approved-word / synonym table.
> Not included at this tier: the full dictionary, the grammar and style rules
> (Sections 2-9), and the extension sets. Use level 0 and higher for those.
> Domain: code documentation — README files, docstrings, API reference,
> comments, commit messages, changelogs, and error messages.

## How to use this file

Load this file as the working word-choice contract for generated code
documentation. Level -2 states the principles; this level adds the approved
word list, so you can both judge a word and replace it.

Three gates control every word you write:

1. The word is approved in the project controlled terminology, or
2. The word is a code-domain technical noun (Rule 1.5), or
3. The word is a code-domain technical verb (Rule 1.12).

If a word passes no gate, replace it. The synonym table below gives the
replacement for the words that most often fail.

## Core principles (14)

### Rule 1.1 — Use approved words, code-domain technical nouns, or code-domain technical verbs

Use only words that pass one of the three gates. The controlled terminology
gives the words most used in code documentation, and gives an approved
alternative for each word that is not approved.

> Non-STE: Execute the script to do the task.
>
> STE: Run the script to do the task.

### Rule 1.2 — Use approved words only as the specified part of speech

Each approved word has one or more specified parts of speech. Do not use a word
in a part of speech that is not approved for it.

> Non-STE: Query the database for the user record.
>
> STE: Send a query to the database for the user record.

"Query" is an approved noun, but it is not an approved verb.

### Rule 1.3 — Use approved words only with their approved meanings

An approved word can have a more restricted meaning in the controlled
terminology than in standard English. Use only the approved meaning.

The approved meaning of "follow" is "come after, go after". The approved meaning
of "obey" is "to do that which the procedures or instructions tell you". Write
"Obey the safety instructions", not "Follow the safety instructions".

### Rule 1.4 — Use only the approved forms of verbs and adjectives

The controlled terminology gives each approved verb with its approved forms, and
each approved adjective with its comparative and superlative forms.

> COMPILE (v), COMPILES, COMPILED, COMPILED
>
> FAST (adj) (FASTER, FASTEST)

Do not write "compilates" or "compilating". These forms are not approved.

### Rule 1.5 — You can use words that are in a code-domain technical noun category

A code-domain technical noun refers to a specified concept in software
development. The controlled terminology cannot list them all, because each
codebase uses different ones. You can use a noun if you can put it in one of the
nineteen code-domain technical noun categories, for example: code components,
modules, and libraries; computing devices and hardware; development tools;
data structures and formats; infrastructure and platforms; architectural
components; algorithmic and mathematical terms; interface elements; units, time,
and measurement; quoted text such as error strings and labels; and database and
storage terms.

Examples: `module`, `container`, `hash map`, `middleware`, `load balancer`.

### Rule 1.6 — Use a word that is not approved only when it is a code-domain technical noun, or part of one

A word that is not approved on its own can be correct inside a compound
code-domain technical noun.

> Non-STE: The handler processes each incoming event.
>
> STE: The function processes each incoming event.

But you can write:

> STE: The event handler processes each incoming event.

"Event handler" is a code-domain technical noun in category 1, code components,
modules, and libraries.

### Rule 1.7 — Do not use code-domain technical nouns as verbs

Use a code-domain technical noun as a noun, or as an adjective inside a
different code-domain technical noun. Do not use it as a verb. Change the
sentence construction and use an approved verb.

> Non-STE: Database the user records before the migration.
>
> STE: Store the user records in the database before the migration.

### Rule 1.8 — Use code-domain technical nouns that are approved in your project, company, industry, or subject field

If the class, module, function, table, resource, or configuration key already
has a name in the codebase or in the domain, use that name. Do not invent a new
name for an item that has an approved name.

> STE: The dashboard page has a `UserTable` component and a `FilterPanel` component.

### Rule 1.9 — When you must select a code-domain technical noun, use one which is short and easy to understand

Select a term of not more than three words. Do not use a long descriptive
phrase when the context (a code snippet, a line number, an API reference)
identifies the item. Add one or two adjectives only if the reader needs them.

> Non-STE: Call the asynchronous JavaScript XML HTTP request wrapper utility function (line 42).
>
> STE: Call the `fetchUtility` function (line 42).

### Rule 1.10 — Do not use regional, slang, or jargon words as code-domain technical nouns

Some words are known only in one region, one subculture, or one technology
stack. Readers of code documentation have different backgrounds, and many are
not native English speakers. Use well-known words.

> Non-STE: Remove all the cruft from the legacy module.
>
> STE: Remove all the unnecessary code from the legacy module.

### Rule 1.11 — Do not use different code-domain technical nouns for the same item

Use one name for one item in all parts of the documentation. The source of
truth is the code: the class, function, module, table, resource, environment
variable, or configuration key as it is defined in the repository.

> Non-STE: Initialize the `UserService` class. Call the authenticate method on
> the `AccountManager`. The `UserHandler` returns a session token.
>
> STE: Initialize the `UserService` class. Call the authenticate method on the
> `UserService`. The `UserService` returns a session token.

### Rule 1.12 — You can use verbs that are in a code-domain technical verb category

A code-domain technical verb refers to a specified operation or process in
software development. You can use a verb if you can put it in one of the four
code-domain technical verb categories: development processes (write, modify,
test, and verify code); computer processes and applications; instructions and
information for applicable subject fields; and law and regulations.

Examples: `compile`, `transpile`, `lint`, `refactor`, `serialize`, `debug`,
`profile`, `deploy`.

If an approved verb gives the same instruction or information, use the approved
verb. Do not use a code-domain technical verb when it is not necessary.
Code-domain technical verbs obey the same rules as all other approved verbs.

### Rule 1.13 — Do not use code-domain technical verbs as nouns

Use a code-domain technical verb only as a verb. If you need a noun, use an
approved noun or a code-domain technical noun with the equivalent meaning.

> Non-STE: Do a deploy of the service to staging.
>
> STE: Deploy the service to staging.

Some words can be a code-domain technical verb and a code-domain technical
noun. This condition occurs only when the word is in a verb category (Rule
1.12) and also in a noun category (Rule 1.5).

### Rule 1.14 — Use American English spelling unless other official directives tell you differently

Use the spelling given in the controlled terminology. Use a different spelling
only if a project specification, style guide, contract, or other official
directive is applicable.

> Non-STE: The log file shows the colour of each output line.
>
> STE: The log file shows the color of each output line.

Do not change the spelling of quoted text, for example an error message, a code
comment, or a user interface label. Keep quoted text as it is.

## Synonym table — approved words and the words they replace

Use the approved word in the left column. Replace every word in the right
column. The table is the short form of the controlled terminology at this tier;
higher levels give the full dictionary with parts of speech, approved meanings,
and approved forms.

### Approved verbs (Rules 1.1, 1.2, 1.4, 1.13)

| Approved verb | Do not write | Approved meaning in code documentation |
| --- | --- | --- |
| use | utilize, leverage, employ | Apply an existing function, library, or component without a change to its implementation. |
| start | initiate, commence, bootstrap | Begin the execution of a process, service, or background task. |
| stop | terminate, halt, kill | End the execution of a running process or service in a controlled manner. |
| show | display, render, present | Make a value, status, or result visible in the interface or in a log. |
| make | create, generate, produce | Build a new object, file, or data structure as the result of an operation. |
| get | retrieve, fetch, obtain | Read a value, record, or resource from a store, API, or cache. |
| set | configure, assign, establish | Give a value to a field, option, or configuration key. |
| check | verify, validate, ensure | Examine a value or state against a condition. |
| do | perform, execute, carry out | Complete an operation or a task. |
| send | transmit, dispatch, forward | Move a message, request, or record to a destination. |
| remove | delete, eliminate, purge | Take an item out of a store, list, or file. |
| keep | retain, preserve, maintain | Hold an item or value in its current state. |
| add | append, insert, include | Put a new item into a list, file, or record. |
| change | modify, alter, update | Make a value or item different. |
| write | persist, save, store | Put data into a file, database, or stream. |
| read | load, parse, ingest | Take data from a file, database, or stream. |
| connect | attach, link, associate | Make a connection between two components or endpoints. |
| close | shut, release, disconnect | End a connection, file handle, or session. |

### Approved nouns for common components (Rules 1.5, 1.8, 1.9, 1.11)

Use the project name of the item. When the project has no name, use the
approved code-domain technical noun in the left column, and use it in all
documents for the same item.

| Approved noun | Do not write |
| --- | --- |
| `AuthenticationService` | login handler, auth component, credential service |
| `CacheManager` | cache store, memoization layer, buffer manager |
| `Logger` | log writer, event recorder, trace emitter |
| `RateLimiter` | throttle controller, request governor, flow regulator |
| `HttpClient` | request sender, web caller, rest client |
| `Result<T, E>` | either type, outcome wrapper, try result |
| `ConfigMap` | settings object, configuration holder, option store |
| `TreeNode` | node element, tree item, hierarchy unit |
| `Payload` | data bundle, message body, request content |
| `ConnectionPool` | socket group, session store, connection cache |
| `BuildPipeline` | compile flow, build chain, assembly process |
| `MigrationScript` | schema update, database patch, version step |
| `DeployStep` | rollout action, release task, push operation |
| `IdleState` | inactive mode, standby condition, dormant status |
| `ErrorState` | failure mode, fault condition, broken status |
| middleware | request filter, interceptor piece, pipeline part |
| plugin | add-on module, extension part, optional unit |
| timeout | wait limit, expiry period, deadline value |
| availability zone | data region, server location, host area |
| logging system | trace framework, log facility, record subsystem |

### Approved adjectives (Rules 1.2, 1.3, 1.4)

Use these adjectives only with the approved meaning. They are technical
adjectives of the code domain, and they have no comparative or superlative form.

| Approved adjective | Approved meaning |
| --- | --- |
| idempotent | Produces the same result when applied more than once, with no extra effect after the first run. |
| immutable | Cannot be changed after it is created. |
| atomic | Completes fully or not at all, with no partial result visible to other processes. |
| thread-safe | Functions correctly when more than one thread uses it at the same time. |
| asynchronous | Starts and returns before its work is complete, so the caller can do other work. |
| concurrent | Makes progress in the same time period as other tasks. |
| deterministic | Gives an output that depends only on its inputs. |
| deprecated | Still functions, but the maintainers plan to remove it. Do not use it in new code. |
| nullable | Can hold a null value to show that there is no value. |
| serializable | Can be changed to a byte stream and built again without loss of data. |
| stateless | Keeps no client data between requests. |
| backward-compatible | Older clients can use it without a change. |
| read-only | Permits inspection, but does not permit a write, update, or delete operation. |
| recursive | Calls itself with a smaller part of the problem until it gets to a base case. |
| monotonic | Only increases, and never decreases. |
| transitive | Flows through a chain, so a grant to a group gets to its members. |
| volatile | Another thread or device can change it at any time. |
| hierarchical | Arranged in parent-child levels, where a child inherits the settings of its parent. |
| normalized | Arranged to remove redundant data across tables. |
| incremental | Processes only the parts that changed. |

## Worked replacements

These examples show the principles and the synonym table together.

> Non-STE: Utilize the cache layer to reduce database load during peak traffic periods.
>
> STE: Use the cache layer to reduce database load during peak traffic.

> Non-STE: Perform the installation of the package and execute the initialization of the database before you commence the server.
>
> STE: Install the package and initialize the database before you start the server.

> Non-STE: The configuration file is read by the service at startup and is validated before the connection is established.
>
> STE: The service reads the configuration file at startup. The service checks the file before it connects to the database.

> Non-STE: Terminate the server prior to modifying the configuration file.
>
> STE: Stop the server before you change the configuration file.

## Summary checklist

Before you publish code documentation, check each word:

- Is the word approved, a code-domain technical noun, or a code-domain
  technical verb? (1.1)
- Is it in an approved part of speech? (1.2)
- Does it carry its approved meaning? (1.3)
- Is the verb form or adjective form approved? (1.4)
- Is each new noun in a noun category (1.5), short (1.9), well-known (1.10),
  approved in the project (1.8), and used consistently (1.11)?
- Is each new verb in a verb category (1.12), and used only as a verb? (1.13)
- Is each noun used only as a noun? (1.7)
- Is unapproved wording used only inside a compound technical noun? (1.6)
- Is the spelling American English, and is quoted text unchanged? (1.14)
- Is every word in the right column of the synonym table replaced?
