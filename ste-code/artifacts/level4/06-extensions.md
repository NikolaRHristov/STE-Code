# Level 4 — Extensions & Reference Catalogue

This slice is the machine-readable extension catalogue that sits on top of the
core STE-Code rules (Levels 1–3). It lists the approved vocabulary, adjectives,
domain terms, component names, and a catalogue of documented anti-patterns that
violate the STE principles (P1–P9).

Use this file when you generate code documentation with an LLM: instruct the
model to (1) use only the approved verbs listed here, (2) prefer the approved
adjectives and domain terms, and (3) avoid every anti-pattern in the catalogue.
Each entry shows a short definition, an STE-conformant code example, and the
non-STE wording it replaces.

Scope of this slice:
- Approved verbs and their rejected synonyms
- Code-domain adjectives (approved modifiers)
- Domain terms (field-specific vocabulary)
- Approved component and data-structure nouns
- Verb usage examples (how the approved verbs apply in context)
- Anti-pattern catalogue (non-STE → STE rewrites)

## Approved verbs

Use the approved verb. Reject the listed synonyms — they are jargon or longer
words that add no technical precision.

| Verb | Replaces (rejected) | Definition | STE example |
|------|---------------------|------------|-------------|
| use | utilize, leverage, employ | Apply an existing function, library, or component without modifying it | Use the logger to record the request identifier before you return the response. |
| start | initiate, commence, bootstrap | Begin execution of a process, service, or background task | Start the worker process before the test suite connects to the message queue. |
| stop | terminate, halt, kill | End execution of a running process in a controlled manner | Stop the server before you change the configuration file and restart the service. |
| show | display, render, present | Make a value, status, or result visible to the user | Show the total request count on the dashboard after each successful batch completes. |
| make | create, generate, produce | Build or construct a new object, file, or data structure | Make a backup copy of the database before you run the migration script. |
| get | retrieve, fetch, obtain | Read or obtain a value, record, or resource from a store | Get the user profile from the cache before you render the account page. |
| set | configure, assign, establish | Assign a specific value to a variable, field, or option | Set the timeout to thirty seconds before you open the network connection. |
| check | verify, validate, ensure | Examine a condition to confirm it matches the expected result | Check that the response status is 200 before you parse the JSON body. |
| do | perform, execute, carry out | Run a defined operation as part of a larger flow | Do the cleanup step after the test finishes to remove the temporary files. |
| send | transmit, dispatch, forward | Transfer a message, request, or event to another component | Send the alert to the notification service when the job fails three times. |
| remove | delete, eliminate, purge | Take out a file, record, or component so it is no longer present | Remove the stale cache entry after the TTL expires to free memory. |
| keep | retain, preserve, maintain | Continue to hold a value or resource in its current state | Keep the connection open until all buffered messages have been written to disk. |
| add | append, insert, include | Put an extra element into a collection or configuration | Add the new middleware to the request pipeline before you deploy the service. |
| change | modify, alter, update | Make a controlled modification without replacing the whole item | Change the log level to debug before you reproduce the intermittent failure. |
| write | persist, save, store | Put data into a file, database, or output stream | Write the parsed metrics to the output file before the process exits. |
| read | load, parse, ingest | Obtain data from a file, stream, or input source | Read the configuration from the environment file at startup and apply the values. |
| connect | attach, link, associate | Establish a communication channel between two components | Connect the client to the database before the application starts to serve traffic. |
| close | shut, release, disconnect | End an open connection, file handle, or stream | Close the file handle after the last record is written to prevent data loss. |

Rejected synonyms (do NOT use): **utilize** and **leverage** are rejected spellings
of `use`. Both add length without meaning. Always rewrite to `use`.

## Code-domain adjectives

Preferred modifiers. Keep each adjective attached to the short noun it modifies
(write `the idempotent retry policy`, not `idempotentretrypolicy`).

| Adjective | Definition | STE example |
|-----------|------------|-------------|
| idempotent | An operation that produces the same result when applied more than once, with no extra side effects after the first run | Make the retry handler idempotent so a second call with the same input does not duplicate the record. |
| immutable | A data structure or value that cannot change after creation, preventing shared-state bugs | Keep the request context immutable so concurrent threads cannot overwrite each other's values during a single operation. |
| atomic | An operation that completes fully or not at all, with no partial result visible to other processes | Wrap the balance update in an atomic transaction so the debit and credit always succeed or fail together. |
| thread-safe | Code that works correctly when accessed by multiple threads at the same time without external locking | Mark the singleton constructor thread-safe so two threads can call it on first use without creating two instances. |
| asynchronous | A call or task that starts and returns before its work finishes, so the caller can do other work meanwhile | Make the file upload asynchronous so the user interface stays responsive while the transfer runs in the background. |
| concurrent | Tasks that make progress within the same time period, interleaved by the scheduler rather than strictly sequentially | Run the test suites in concurrent processes so the full check finishes in a fraction of the single-threaded time. |
| deterministic | A function whose output depends only on its inputs, with no hidden state or time-based variation | Keep the hash function deterministic so the same key always maps to the same bucket across restarts. |
| deprecated | An API or feature that still works but that maintainers plan to remove, so avoid new use | Mark the old login endpoint deprecated and show a warning that points to the new token-based method. |
| nullable | A field or variable that can hold a null value to indicate the absence of a meaningful value | Make the middle-name field nullable so the profile save does not fail when the value is absent. |
| serializable | An object that can be converted to a byte stream and rebuilt elsewhere without losing its data | Make the session object serializable so the cache layer can store it and restore it on the next request. |
| stateless | A service that keeps no client data between requests, making horizontal scaling simpler and safer | Build the authentication proxy stateless so any node can answer a request without shared session memory. |
| backward-compatible | A change that older clients can still use without modification because the old interface still works | Keep the API response backward-compatible so existing mobile apps keep working after the schema update. |
| read-only | A resource or mode that permits inspection but forbids any write, update, or delete | Open the database handle read-only during reports so the query tool cannot change production data by mistake. |
| recursive | A function that calls itself with a smaller part of the problem until it reaches a base case | Write the directory walker recursive so it visits every nested folder without a manual loop stack. |
| monotonic | A counter or clock that only increases and never goes backward, making ordering safe | Use a monotonic sequence for the event id so replays never create a lower number than a prior record. |
| transitive | A permission or relation that flows through a chain, so a grant to a group reaches its members | Make the role grant transitive so a user in a child team inherits the parent team's read access automatically. |
| volatile | A memory value that another thread or device can change at any time, so the compiler must reload it | Declare the status flag volatile so the loop reads the hardware register again instead of using a cached copy. |
| hierarchical | Data or permissions arranged in parent-child levels where a child inherits settings from its ancestor | Store the configuration in a hierarchical map so a child setting overrides only the matching branch of the tree. |
| normalized | A database schema arranged to remove redundant data and reduce update anomalies across tables | Keep the user table normalized so the address lives in one row and every order references it by id. |
| incremental | A build or update that processes only the changed parts instead of recomputing the whole result | Run an incremental compile so the tool rebuilds only the modules whose source changed since the last run. |

## Domain terms

Field-specific vocabulary. Use the term; the "replaces" column lists the vague or
informal wording it should displace.

| Term | Domain | Definition | Replaces |
|------|--------|------------|----------|
| orchestrator | containerization | A control plane that schedules, deploys, and manages containerized workloads across a cluster | scheduler, cluster manager, container manager |
| subnet | networking | A logical partition of an IP network that groups addresses so routers can forward traffic between isolated segments | network slice, IP range, address block |
| mock | testing | A test double that simulates a dependency and verifies the code under test calls it as expected | stub, fake, dummy object |
| telemetry | observability | Automated collection and transmission of metrics, traces, and logs to a central analysis backend | instrumentation data, system signals, monitoring output |
| pipeline | CI/CD | An automated sequence of build, test, and deploy stages that moves a change from commit to production | build chain, workflow, job stream |
| index | database | A secondary structure that maps column values to row locations so queries avoid full table scans | lookup table, secondary structure, access path |
| authentication | security | Verifying the identity of a user, service, or device before granting access to protected resources | auth, login check, identity confirmation |
| idempotency | distributed systems | A property of an operation that produces the same final result whether it runs once or multiple times with the same input | repeat safety, retry proof, safe re-execution |
| autoscaling | cloud | A mechanism that automatically increases or decreases running instances in response to measured load or schedule | elastic resize, self-adjust, dynamic capacity |
| hydration | frontend | The process where a browser attaches event handlers and interactive state to server-rendered HTML | client boot, attach behavior, re-render bind |
| rebase | version control | An operation that moves a branch's commits onto the tip of another branch so history stays linear | transplant, replay commits, restack |
| eviction | caching | The policy by which a cache removes entries when it reaches its size limit or entries exceed their TTL | purge rule, drop policy, clearance |
| broker | message queue | A middleware server that receives messages from producers and routes them to consumers while buffering during outages | message hub, relay, dispatcher |
| pagination | API design | A response strategy that splits a large collection into numbered or cursor-based pages for bounded, predictable fetches | paged results, chunking, windowing |
| latency | performance | The elapsed time between a system receiving a request and returning the first or last byte of the response | response delay, wait time, lag |
| rollout | deployment | The controlled procedure that releases a new version to production, often in stages, so failures affect only part of traffic | push, ship, go-live |
| structured log | logging | A log entry emitted as machine-readable key-value fields instead of free text so systems can parse and aggregate it | plain log, text log, raw print |
| race condition | concurrency | A defect where two or more concurrent operations access shared state without synchronization and the result depends on execution order | timing bug, collision, concurrent fault |
| cipher | encryption | An algorithm that transforms plaintext into ciphertext and back using a key so only key holders can read the data | crypto scheme, codec, scrambler |
| alert | monitoring | A notification fired when a metric crosses a defined threshold so an operator can investigate or a runbook can trigger remediation | warning, trigger, notification event |

## Approved component and data-structure nouns

Component and data-structure names to use in code documentation. Each replaces a
vaguer description.

| Noun | Definition | Replaces | STE example |
|------|------------|----------|-------------|
| AuthenticationService | A service that verifies user credentials and issues access tokens for protected API endpoints | login handler, auth component, credential service | Use the AuthenticationService to verify the user token before each protected request reaches the handler. |
| CacheManager | A component that controls cached-data lifecycle and removes entries when they exceed their TTL | cache store, memoization layer, buffer manager | Use the CacheManager to store the compiled template and reuse it on the next page load. |
| Logger | A component that records application events with a severity level to a configurable destination | log writer, event recorder, trace emitter | Use the Logger to record the request duration after the handler finishes the operation. |
| RateLimiter | A component that constrains requests a client can send in a fixed window to protect the service | throttle controller, request governor, flow regulator | Use the RateLimiter to stop a single client from sending more than one hundred requests per minute. |
| HttpClient | A component that sends HTTP requests to a remote server and returns the response with status code and body | request sender, web caller, rest client | Use the HttpClient to send the user data to the registration endpoint and read the response code. |
| Result<T, E> | A generic sum type that represents either a successful value of type T or an error of type E | either type, outcome wrapper, try result | Use a Result<T, E> to show the outcome of the parse operation without throwing an exception. |
| ConfigMap | A data structure that stores key-value application settings read at startup | settings object, configuration holder, option store | Use the ConfigMap to store the database address and read it when the service starts. |
| TreeNode | A data structure that holds a value and references to child nodes forming a hierarchical tree | node element, tree item, hierarchy unit | Use a TreeNode to store each directory and attach its children when you build the file tree. |
| Payload | The data carried by a network message or function call, separate from headers and routing metadata | data bundle, message body, request content | Use the Payload to send the order details and keep the headers small for faster transmission. |
| ConnectionPool | A data structure that keeps open database connections ready for reuse to reduce overhead | socket group, session store, connection cache | Use the ConnectionPool to get a database connection and return it after the query finishes. |
| BuildPipeline | A sequence of automated steps that compile, test, and package source into a deployable artifact on each commit | compile flow, build chain, assembly process | Use the BuildPipeline to run the unit tests and stop the release when a test fails. |
| MigrationScript | A script that applies a controlled schema change and records the version in a tracking table | schema update, database patch, version step | Use the MigrationScript to add the new column and check the schema version before you deploy. |
| DeployStep | A single automated action in a deployment plan that moves a build to a target environment and reports status | rollout action, release task, push operation | Use the DeployStep to start the service on the staging host and check the health endpoint. |
| IdleState | A condition in which a component performs no work and waits for an external signal to become active | inactive mode, standby condition, dormant status | Use the IdleState to show that the worker has finished its tasks and waits for new work. |
| ErrorState | A condition in which a component has a fault and cannot process requests until it recovers or resets | failure mode, fault condition, broken status | Use the ErrorState to show the user that the upload failed and how to retry the operation. |
| Middleware | A reusable component that sits between the request and the handler to modify, inspect, or block the request | request filter, interceptor piece, pipeline part | Use the Middleware to check the request header and stop unauthorized calls before they reach the handler. |
| Plugin | A separable component that adds optional behavior to a host application without changing its core source | add-on module, extension part, optional unit | Use the Plugin to add the export feature and keep the core application small and stable. |
| Timeout | A duration that specifies the maximum time a component waits for an operation before it aborts | wait limit, expiry period, deadline value | Use the Timeout to stop the request when the server does not answer within five seconds. |
| AvailabilityZone | An isolated location within a cloud region with independent power, cooling, and network for fault tolerance | data region, server location, host area | Use the AvailabilityZone to place the replica so the failure of one zone does not stop the service. |
| LoggingSystem | A subsystem that collects, formats, and routes log records from many components to files, metrics, or dashboards | trace framework, log facility, record subsystem | Use the LoggingSystem to record the startup event and send the warning to the operations dashboard. |

## Verb usage examples

Concrete applications of the approved verbs in context. Each shows the STE
wording next to the non-STE wording it replaces.

| Pattern | Approved verb | STE example | Non-STE (rejected) |
|---------|---------------|-------------|--------------------|
| use-service-client | use | Use the client object to send requests to the payment gateway. | Utilize the client object to leverage the payment gateway for request transmission. |
| start-worker-process | start | Start the worker process before you run the migration job. | Initiate the worker process and commence the migration job execution. |
| stop-background-scheduler | stop | Stop the background scheduler before you restart the host. | Terminate the background scheduler and halt the host restart sequence. |
| show-configuration-table | show | The command shows the current configuration values as a table. | The command displays and renders the current configuration values as a presentable table. |
| make-connection | make | The factory function makes a new connection from the supplied parameters. | The factory function creates and generates a new connection from the supplied parameters. |
| get-user-record | get | Get the user record from the cache with the supplied identifier. | Retrieve and fetch the user record from the cache with the obtained identifier. |
| set-timeout-value | set | Set the timeout value to 30 seconds before you open the connection. | Configure and assign the timeout value to 30 seconds before you establish the connection. |
| check-response-status | check | Check that the response status is 200 before you parse the body. | Verify and validate that the response status is 200 before you ensure body parsing. |
| do-build-step | do | Do the build step before you deploy the application to staging. | Perform and execute the build step before you deploy the application to staging. |
| send-queue-message | send | The producer sends a message to the queue when the job finishes. | The producer transmits and dispatches a message to the queue when the job finishes. |
| remove-session-token | remove | Remove the expired session token from the store after the user logs out. | Delete and purge the expired session token from the store after the user logs out. |
| keep-lock | keep | Keep the lock for the shortest time that the critical section needs. | Retain and preserve the lock for the shortest time that the critical section requires. |
| add-middleware | add | Add the new middleware to the pipeline before you start the server. | Create the new middleware and configure it into the pipeline before you initiate the server. |
| put-uploaded-file | put | Put the uploaded file in the temporary directory until the scan completes. | Store the uploaded file in the temporary directory and retain it until the scan completes. |
| open-socket | open | Open the socket and read the response until the server closes it. | Establish the socket and read the response until the server closes it. |
| close-file-handle | close | Close the file handle after the write operation finishes. | Terminate the file handle after the write operation finishes. |
| change-log-level | change | Change the log level to debug before you reproduce the failure. | Configure the log level to debug before you reproduce the failure. |
| give-result-object | give | The method gives a result object that contains the parsed response. | The method returns a result object and utilizes the parsed response internally. |
| go-settings-page | go | Go to the settings page and select the export option. | Proceed to the settings page and leverage the export option. |

## Anti-pattern catalogue

Documented non-STE patterns with their STE rewrites. `violates` lists the STE
principles broken (P1 = approved words, P2 = present tense, P3 = active voice,
P4 = short sentences, P5 = unambiguous reference, P8 = define terms). Each entry
shows non-STE (rejected) → STE (required).

| ID | Pattern | Severity | Non-STE | STE |
|----|---------|----------|---------|-----|
| AP-001 | Future tense in procedural instructions | error | The system will send a confirmation email after the registration process completes successfully. | The system sends a confirmation email after registration completes. |
| AP-002 | Undefined acronym in error message | blocking | Error: DAG execution failed at T2. | Error: The scheduled workflow (DAG) failed at step T2. Open the dashboard to see the step log. |
| AP-003 | Passive voice obscures the actor | blocking | The configuration file is read by the service at startup and is validated before the connection is established. | The service reads the configuration file at startup. The service validates the file before it establishes the connection. |
| AP-004 | Nominalization instead of a direct verb | error | Perform the installation of the package and execute the initialization of the database before you commence the server. | Install the package and initialize the database before you start the server. |
| AP-005 | Avoided synonym "utilize" for "use" | error | Utilize the cache layer to reduce database load during peak traffic periods. | Use the cache layer to reduce database load during peak traffic. |
| AP-006 | Overlong sentence with nested clauses | warning | When the user submits the form which contains invalid data the application will display an error message and it will also log the failure so that the team can investigate the root cause later. | When the user submits a form with invalid data, the application shows an error message. The application also logs the failure so the team can investigate. |
| AP-007 | Contraction in procedural documentation | error | Don't close the socket until the response isn't fully received. | Do not close the socket until the response is fully received. |
| AP-008 | Jargon without definition | error | The ingress controller reconciles the desired state with the cluster and emits events on drift. | The ingress controller matches the cluster state to the configuration that you specify. It reports an event when the states differ. |
| AP-009 | Semicolon joining two independent instructions | error | Open the settings file; then change the port value to 8080. | Open the settings file. Change the port value to 8080. |
| AP-010 | Avoided synonym "leverage" for "use" | error | Leverage the retry queue to handle transient failures without dropping requests. | Use the retry queue to handle transient failures without dropping requests. |
| AP-011 | Ambiguous pronoun reference | warning | The client calls the server and it returns the token, then it validates it before it stores it in memory. | The client calls the server. The server returns the token. The client validates the token and then stores it in memory. |
| AP-012 | Avoided synonym "commence" for "start" | error | Commence the build pipeline after the tests pass in the staging environment. | Start the build pipeline after the tests pass in the staging environment. |
| AP-013 | Avoided synonym "terminate" for "stop" | error | Terminate the background worker before you release the database connection to prevent locks. | Stop the background worker before you release the database connection to prevent locks. |
| AP-014 | Contradictory instructions in the same section | blocking | Always enable caching for the reports endpoint. Never enable caching for the reports endpoint because it returns user-specific data. | Enable caching for the reports endpoint only when the response is identical for all users. Do not enable caching when the response contains user-specific data. |
| AP-015 | Regional spelling inconsistency | error | Customise the serialise function to normalise the colour values before you initialise the widget. | Customize the serialize function to normalize the color values before you initialize the widget. |
| AP-016 | Slang and informal phrasing | error | Just spin up a quick instance and hack the config until the thing stops crashing. | Start an instance and edit the configuration until the application stops crashing. |
| AP-017 | Undefined technical term in README | error | The handler emits a webhook to the broker on each mutation event. | The handler sends an HTTP request to the message broker on each data change event. The broker distributes the request to subscribers. |
| AP-018 | Weak style — verbose phrasing | info | In order to be able to make use of the new logging feature it is necessary to carry out an update of the agent to the most recent version. | To use the new logging feature, update the agent to the latest version. |
| AP-019 | Synonym for an approved term | info | The module obtains the credentials and subsequently dispatches the request to the upstream service. | The module gets the credentials and then sends the request to the upstream service. |
| AP-020 | Avoided synonym "employ" with nominalization | error | Employ the prepared statement to effect the retrieval of rows from the table in a safe manner. | Use the prepared statement to get rows from the table safely. |

### Quick reference for LLM prompting

- Always use approved verbs (use, start, stop, show, make, get, set, check, do,
  send, remove, keep, add, change, write, read, connect, close). Never use
  utilize, leverage, employ, initiate, commence, terminate, perform, execute.
- Write in present tense for procedural steps; never future tense (AP-001).
- Use active voice and name the actor (AP-003).
- Keep one instruction per sentence; never join with semicolons (AP-009).
- Define every acronym and technical term on first use (AP-002, AP-008, AP-017).
- Avoid contractions in procedural documentation (AP-007).
- Pick one regional spelling and stay consistent (AP-015).
- Do not pile synonyms or nominalize verbs (AP-004, AP-018, AP-020).

<!-- APPEND -->
