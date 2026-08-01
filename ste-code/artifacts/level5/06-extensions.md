# Level 5 — Extensions

Level 5 is the full STE-Code standard. This sub-document is the **extensions** slice:
the approved code-domain vocabulary that sits on top of the core rules in Sections 1–9.
It has two parts:

1. **Extension adjectives** — single approved words (such as `idempotent`, `immutable`,
   `atomic`) that you may attach to a short technical noun without breaking the word-count
   limits of Section 2.
2. **Domain extension vocabulary** — grouped lists of approved code-domain verbs, nouns,
   and signal words for common domains (build, testing, security, version control, and so
   on), each with the rules it must obey and the weak alternatives it replaces.

Use this file when you generate or review code documentation with an LLM and need a compact,
machine-readable list of the words STE-Code accepts beyond its core dictionary.

## How extensions relate to the rules

Extensions are not a new rule set. Each extension still obeys the core rules:

- **Rule 1.1** (approved words only) — every extension word is on an approved list.
- **Rule 2.1** (short technical nouns) — keep the noun short; the adjective attaches to it.
- **Rule 3.1 / 3.7** (prefer a verb) — domain verbs such as `build`, `test`, `deploy` replace
  noun phrases such as "perform a build of" or "do a deployment of".
- **Rule 7.1 / 7.2 / 7.3** (risk and safety words) — the signal-word group replaces vague
  warnings such as "heads up" or "be careful" with `WARNING`, `CAUTION`, `BREAKING`, `DEPRECATED`.

A hyphenated extension adjective counts as one word under Rule 2.1. Write
`the idempotent retry policy` (three words), not `idempotentretrypolicy`. Keep the hyphen
before the noun: `thread-safe`, `backward-compatible`, `read-only`, `stateless`.

---

## Part 1 — Extension adjectives

These adjectives are approved as single words. Each entry gives the definition and one
STE / Non-STE code-documentation pair so you can see the contrast. The Non-STE line shows
the weak alternative the extension replaces (usually `leverage` / `utilize` / `employ` plus a
nominalized verb).

### idempotent
- **meaning**: An operation that produces the same result when applied more than once, with no extra side effects after the first run.
- **STE**: Make the retry handler idempotent so a second call with the same input does not duplicate the record.
- **Non-STE**: Leverage an idempotent retry handler so a duplicate invocation will not create a redundant record.

### immutable
- **meaning**: A data structure or value that cannot be changed after it is created, which prevents accidental shared-state bugs.
- **STE**: Keep the request context immutable so concurrent threads cannot overwrite each other's values during a single operation.
- **Non-STE**: Utilize an immutable request context so concurrent threads will not overwrite shared values during processing.

### atomic
- **meaning**: An operation that completes fully or not at all, with no partial result visible to other processes.
- **STE**: Wrap the balance update in an atomic transaction so the debit and credit always succeed or fail together.
- **Non-STE**: Employ an atomic transaction to encapsulate the balance update so debit and credit always commit or roll back together.

### thread-safe
- **meaning**: Code that functions correctly when accessed by multiple threads at the same time without external locking.
- **STE**: Mark the singleton constructor thread-safe so two threads can call it on first use without creating two instances.
- **Non-STE**: Leverage a thread-safe singleton constructor so concurrent threads will not instantiate duplicate objects on first access.

### asynchronous
- **meaning**: A call or task that starts and returns before its work finishes, so the caller can do other work meanwhile.
- **STE**: Make the file upload asynchronous so the user interface stays responsive while the transfer runs in the background.
- **Non-STE**: Utilize an asynchronous upload mechanism so the user interface remains responsive while the transfer executes in the background.

### concurrent
- **meaning**: Tasks that make progress within the same time period, interleaved by the scheduler rather than strictly sequentially.
- **STE**: Run the test suites in concurrent processes so the full check finishes in a fraction of the single-threaded time.
- **Non-STE**: Employ concurrent processes to execute the test suites so the whole check terminates faster than a single-threaded run.

### deterministic
- **meaning**: A function whose output depends only on its inputs, with no hidden state or time-based variation between runs.
- **STE**: Keep the hash function deterministic so the same key always maps to the same bucket across restarts.
- **Non-STE**: Leverage a deterministic hash function so an identical key consistently maps to the same bucket after restarts.

### deprecated
- **meaning**: An API or feature that still works but that the maintainers plan to remove, so avoid new use of it.
- **STE**: Mark the old login endpoint deprecated and show a warning that points to the new token-based method.
- **Non-STE**: Flag the legacy login endpoint as deprecated and utilize a warning that redirects callers to the token-based method.

### nullable
- **meaning**: A field or variable that can hold a null value to indicate the absence of a meaningful value.
- **STE**: Make the middle-name field nullable so the profile save does not fail when the value is absent.
- **Non-STE**: Configure the middle-name field as nullable so the profile persistence will not fail when the value is missing.

### serializable
- **meaning**: An object that can be converted to a byte stream and rebuilt elsewhere without losing its data.
- **STE**: Make the session object serializable so the cache layer can store it and restore it on the next request.
- **Non-STE**: Utilize a serializable session object so the cache layer can persist and reconstitute it on the following request.

### stateless
- **meaning**: A service that keeps no client data between requests, which makes horizontal scaling simpler and safer.
- **STE**: Build the authentication proxy stateless so any node can answer a request without shared session memory.
- **Non-STE**: Employ a stateless authentication proxy so every node can service a request without shared session storage.

### backward-compatible
- **meaning**: A change that older clients can still use without modification because the old interface still works.
- **STE**: Keep the API response backward-compatible so existing mobile apps keep working after the schema update.
- **Non-STE**: Leverage a backward-compatible response format so legacy mobile clients remain functional after the schema update.

### read-only
- **meaning**: A resource or mode that permits inspection but forbids any write, update, or delete operation.
- **STE**: Open the database handle read-only during reports so the query tool cannot change production data by mistake.
- **Non-STE**: Utilize a read-only database handle for reports so the query tool cannot mutate production data accidentally.

### recursive
- **meaning**: A function that calls itself with a smaller part of the problem until it reaches a base case.
- **STE**: Write the directory walker recursive so it visits every nested folder without a manual loop stack.
- **Non-STE**: Employ a recursive directory walker so it traverses each nested folder without an explicit loop stack.

### monotonic
- **meaning**: A counter or clock that only increases and never goes backward, which makes ordering safe.
- **STE**: Use a monotonic sequence for the event id so replays never create a lower number than a prior record.
- **Non-STE**: Leverage a monotonic sequence for the event identifier so replays never yield a lower value than prior records.

### transitive
- **meaning**: A permission or relation that flows through a chain, so a grant to a group reaches its members.
- **STE**: Make the role grant transitive so a user in a child team inherits the parent team's read access automatically.
- **Non-STE**: Utilize a transitive role grant so a member of a child team inherits the parent team's read access automatically.

### volatile
- **meaning**: A memory value that another thread or device can change at any time, so the compiler must reload it.
- **STE**: Declare the status flag volatile so the loop reads the hardware register again instead of using a cached copy.
- **Non-STE**: Employ a volatile status flag so the loop reloads the hardware register rather than using a cached copy.

### hierarchical
- **meaning**: Data or permissions arranged in parent-child levels where a child inherits settings from its ancestor.
- **STE**: Store the configuration in a hierarchical map so a child setting overrides only the matching branch of the tree.
- **Non-STE**: Utilize a hierarchical configuration map so a child setting overrides solely the matching branch of the tree.

### normalized
- **meaning**: A database schema arranged to remove redundant data and reduce update anomalies across tables.
- **STE**: Keep the user table normalized so the address lives in one row and every order references it by id.
- **Non-STE**: Utilize a normalized user table so the address resides in one row and each order references it by identifier.

### incremental
- **meaning**: A build or update that processes only the changed parts instead of recomputing the whole result.
- **STE**: Run an incremental compile so the tool rebuilds only the modules whose source changed since the last run.
- **Non-STE**: Employ an incremental compile so the tool reconstructs only the modules whose source changed since the prior run.

---

## Part 2 — Domain extension vocabulary

Each domain below lists the approved code-domain words, the weak alternatives they replace,
the core rules that govern them, and one STE / Non-STE example. Use these as drop-in vocabulary
when documenting the matching domain.

### Build and Package
Operations for compiling, assembling, bundling, and distributing software artifacts.
- **Approved**: build, compile, bundle, package, deploy, publish, release, tag, version, transpile, minify, polyfill, ship
- **Replaces**: make a build of → build; perform compilation → compile; create a bundle → bundle; generate the artifact → build; assemble → build; construct → build; fabricate → build
- **Rules**: Rule 1.12, Rule 1.13, Rule 1.1, Rule 1.7
- **Example**: STE: Build the Docker image. Then deploy the container to the registry. | Non-STE: Perform a build of the Docker image and then do a deployment to the registry.

### Testing and Quality Assurance
Operations for verifying code correctness, measuring performance, and ensuring quality.
- **Approved**: test, assert, mock, stub, spy, benchmark, profile, instrument, debug, unit-test, lint, check
- **Replaces**: validate → check; verify → check; ensure → make sure; run validation → check; perform testing → test; execute tests → run tests; carry out verification → check
- **Rules**: Rule 1.12, Rule 1.1, Rule 1.5, Rule 4.1
- **Example**: STE: Run the test suite. Check that the coverage is above 80 percent. | Non-STE: Execute the test suite and verify that coverage exceeds 80%.

### Dependency Management
Operations for installing, updating, locking, and resolving software dependencies.
- **Approved**: install, update, upgrade, pin, lock, link, hoist, resolve, uninstall, add, remove
- **Replaces**: fetch dependencies → install; retrieve packages → install; pull down → install; bump → update; snag → install; grab → get
- **Rules**: Rule 1.12, Rule 1.1, Rule 1.10, Rule 1.11
- **Example**: STE: Install the dependencies with npm install. Pin the versions in the lock file. | Non-STE: Snag the deps and bump the versions.

### Version Control
Operations for tracking changes, branching, merging, and collaborating on source code.
- **Approved**: commit, branch, merge, rebase, tag, push, pull, clone, fork, checkout, revert, cherry-pick, stash, stage, reset
- **Replaces**: save changes → commit; upload → push; download → pull/clone; combine → merge; split off → branch
- **Rules**: Rule 1.12, Rule 1.7, Rule 1.13, Rule 1.1
- **Example**: STE: Commit the changes. Then push the branch to the remote repository. | Non-STE: Git the changes and then push them up. (Uses Git as a verb, Rule 1.7 violation)

### Security
Operations for authentication, authorization, encryption, and protecting systems from threats.
- **Approved**: authenticate, authorize, encrypt, decrypt, hash, salt, sanitize, validate, sign, revoke, audit, escape
- **Replaces**: secure → encrypt/protect; lock down → restrict; harden → make secure; obfuscate → hide
- **Rules**: Rule 1.12, Rule 7.1, Rule 1.5, Rule 1.1
- **Example**: STE: WARNING: Sanitize all user input before you process it. Unsanitized input can cause SQL injection attacks. | Non-STE: CAUTION: Always clean your inputs.

### Logging and Monitoring
Operations for recording events, measuring system health, and observing runtime behavior.
- **Approved**: log, monitor, trace, instrument, observe, alert, report, record
- **Replaces**: write to log → log; keep track of → monitor; watch → monitor; spy on → observe; output → write/log
- **Rules**: Rule 1.12, Rule 1.1, Rule 1.5, Rule 5.1
- **Example**: STE: Log the error details to the error file. Monitor the CPU usage. | Non-STE: Do a logging of the exception. Keep an eye on the CPU.

### API Design
Concepts for designing, documenting, and consuming application programming interfaces.
- **Approved**: endpoint, route, handler, middleware, controller, request, response, payload, header, status code, rate limit, query parameter, path parameter, body, schema
- **Replaces**: URL path → endpoint; API method → endpoint; args → parameters; params → parameters; data → payload/body; return value → response
- **Rules**: Rule 1.5, Rule 1.11, Rule 1.8, Rule 4.1
- **Example**: STE: The endpoint returns a JSON object. The object contains a user list and a pagination token. | Non-STE: The API method gives you back a JSON with the users and a next-page thing.

### Configuration Management
Operations for setting up, managing, and maintaining system and application configuration.
- **Approved**: configure, set, initialize, bootstrap, provision, override, default, environment variable, config file, dotenv, settings
- **Replaces**: tweak → set/change; dial in → configure; set up → configure/initialize; wire up → configure/connect; spin up → start/initialize
- **Rules**: Rule 1.12, Rule 1.1, Rule 1.10, Rule 5.4
- **Example**: STE: Set the DATABASE_URL environment variable in the .env file. | Non-STE: Tweak the DATABASE_URL knob in the dotenv thing.

### Object-Oriented Design
Concepts and operations specific to object-oriented programming paradigms.
- **Approved**: instantiate, inherit, override, extend, implement, encapsulate, delegate, inject, compose, abstract class, interface, constructor, method, property, polymorphism
- **Replaces**: make an instance → instantiate; new up → instantiate; subclass → extend/inherit; hide → encapsulate; pass → delegate
- **Rules**: Rule 1.12, Rule 1.5, Rule 1.7, Rule 1.13
- **Example**: STE: The UserRepository class extends BaseRepository. It implements the IAuditable interface. Inject the Database dependency through the constructor. | Non-STE: The repo subclasses the base and hides the data. Pass the DB in via the ctor.

### Functional Programming
Concepts and operations specific to functional programming paradigms.
- **Approved**: compose, curry, map, reduce, fold, filter, recurse, memoize, lift, pattern match, pure function, immutable, closure, higher-order function, monad, functor, applicative
- **Replaces**: chain → compose; loop over → map; combine → reduce/fold; cache results → memoize; call itself → recurse
- **Rules**: Rule 1.12, Rule 1.5, Rule 1.1, Rule 1.11
- **Example**: STE: Map the transformation over the list. Then fold the results with the sum function. | Non-STE: Loop over the array applying the transform and then add everything up.

### Systems Programming
Concepts and operations for memory management, ownership, lifetimes, and low-level system access.
- **Approved**: allocate, deallocate, borrow, own, drop, move, pin, acquire, release, dereference, lifetime, ownership, stack, heap, undefined behavior, dangling pointer, segmentation fault, mutex, atomic
- **Replaces**: free → deallocate; malloc → allocate; clean up → deallocate/drop; grab a lock → acquire; let go → release; shooting yourself in the foot → undefined behavior
- **Rules**: Rule 1.12, Rule 1.5, Rule 1.10, Rule 7.1
- **Example**: STE: Allocate a buffer on the heap. Deallocate the buffer before the function returns. The borrow checker prevents dangling pointers. | Non-STE: Malloc a chunk of memory and free it when you are done. Rust's thingy stops you from shooting yourself in the foot.

### Declarative Configuration
Concepts for describing desired system state through configuration files and infrastructure-as-code.
- **Approved**: provision, converge, reconcile, apply, destroy, declare, resource, provider, module, state, plan, namespace, pod, deployment, service
- **Replaces**: spin up → provision/start; tear down → destroy; make → provision; run → apply; set up → provision
- **Rules**: Rule 1.12, Rule 1.5, Rule 1.1, Rule 4.1
- **Example**: STE: The Terraform resource provisions an AWS EC2 instance. Apply the configuration to converge the infrastructure. | Non-STE: Terraform spins up an EC2 box when you run the apply command.

### Risk and Safety Documentation
Signal words and conventions for documenting security risks, breaking changes, and important notes in code.
- **Approved**: WARNING, CAUTION, BREAKING, DEPRECATED, NOTE, FIXME, TODO, HACK, XXX
- **Replaces**: DANGER → WARNING; IMPORTANT → NOTE/WARNING; BE CAREFUL → CAUTION; ATTENTION → NOTE; heads up → NOTE; watch out → CAUTION
- **Rules**: Rule 7.1, Rule 7.2, Rule 7.3, Rule 1.1
- **Example**: STE: WARNING: DO NOT COMMIT THE API KEY. AN EXPOSED KEY CAN CAUSE UNAUTHORIZED ACCESS. | Non-STE: heads up: don't check in the secret key or bad things happen.

### Commit Message Conventions
Standardized terms and formats for writing clear, consistent commit messages.
- **Approved**: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert, add, remove, update, change
- **Replaces**: implemented → feat/add; added → add/feat; fixed → fix; changed → update/change; removed → remove; bumped → update; patched → fix
- **Rules**: Rule 1.1, Rule 4.1, Rule 5.1, Rule 1.11
- **Example**: STE: feat: Add JWT authentication middleware for API routes. | Non-STE: Implemented JWT auth middleware for the API endpoints.

### Continuous Integration and Delivery
Operations and concepts for automated build, test, and deployment pipelines.
- **Approved**: pipeline, workflow, job, stage, runner, artifact, trigger, checkout, cache, matrix, environment, deploy, rollback, approval, gate
- **Replaces**: CI → pipeline/workflow; CD → deployment pipeline; build step → job/stage; CI runner → runner; kick off → trigger/start; fire → trigger
- **Rules**: Rule 1.5, Rule 1.12, Rule 1.8, Rule 5.2
- **Example**: STE: The pipeline has three stages: build, test, and deploy. Trigger the workflow on every push to the main branch. | Non-STE: The CI kicks off when you push to main and runs the build, test, and deploy stuff.

### Database Operations
Operations for querying, migrating, backing up, and managing database systems.
- **Approved**: query, migrate, seed, backup, restore, roll back, replicate, shard, index, vacuum, compact, flush, persist, transaction, schema
- **Replaces**: run a query → query; do a migration → migrate; populate the DB → seed; dump → backup; snapshot → backup; write to disk → persist/flush
- **Rules**: Rule 1.12, Rule 1.13, Rule 1.5, Rule 1.11
- **Example**: STE: Migrate the database schema to version 3. Seed the development database with test data. | Non-STE: Run the migration script to update the DB and populate it with fake data.

### User Interface Documentation
Terms for documenting UI components, interactions, and interface behavior.
- **Approved**: click, type, scroll, select, drag, drop, toggle, zoom in, zoom out, navigate, press, tap, swipe, hover, focus
- **Replaces**: hit → click/press; push → click/press; enter → type; choose → select; flip → toggle; go to → navigate
- **Rules**: Rule 1.12, Rule 1.5, Rule 1.1, Rule 5.2
- **Example**: STE: Click the Submit button. Type your password in the text field. | Non-STE: Hit the submit thing and enter your pwd in the box.
