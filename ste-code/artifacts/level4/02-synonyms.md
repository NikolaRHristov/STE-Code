# Level 4 — Synonyms and Approved Words: Technical Noun Categories

Source rule: STE-Code Rule 1.5 (adapted from ASD-STE100 Issue 9, Rule 1.5).

## Rule 1.5 (code-domain)

You can use a term that fits one or more technical noun categories.

A technical noun in code documentation is a noun term that names a specified
software concept and applies to a given codebase, library, or system.

The approved-word dictionary does not list project-specific technical nouns:
every codebase, framework, and ecosystem uses different terminology. Take those
terms from your project glossary, API reference, or architecture decision
records (ADRs), and keep them there.

Use technical nouns in procedural and descriptive code documentation only when
they fit at least one category below.

## How an LLM should apply this

1. Before writing a noun, ask: is it in the approved dictionary?
2. If not, ask: does it fit a technical noun category?
3. If yes — use the exact project name (`UserRepository`, `POST /api/v1/users`,
   `lodash@4.17.20`), not a vague placeholder.
4. If no — rewrite with an approved word. Do not invent terminology.

Vague nouns are never technical nouns. Replace them.

| Do not write | Write |
|---|---|
| thing, stuff, item (unspecified) | the named class, endpoint, file, or field |
| the data, the info | the `UserResponse` DTO, the `id` field |
| the tool, the system | `ESLint`, the `orders-service` microservice |

### Example pair

| Non-STE | STE |
|---|---|
| Use the thing to call the function that gets data from the database. | Use the `fetchUser` method of the `UserRepository` to retrieve a `User` record from the `PostgreSQL` database. |
| *("thing", "gets data" — no technical nouns; ambiguous)* | *(`fetchUser`, `UserRepository`, `User`, `PostgreSQL` — classified technical nouns: categories 1, 6, 19)* |

## The 19 technical noun categories (code domain)

A term is approved as a technical noun if it belongs to at least one category.
Categories are numbered as in the standard; the code-domain scope and the
approved example vocabulary follow each heading.

### Category 1 — API and library components

Scope: everything named in API reference documentation, SDK manifests, or
interface definition files.

*endpoint, method, parameter, query parameter, path parameter, request body, response body, header, status code, module, class, interface, type alias, enum, constant, decorator, middleware, route handler, serializer, DTO, model, schema, callback, hook, plugin*

| Non-STE | STE |
|---|---|
| Call the thing that makes users. | Call the `POST /api/v1/users` endpoint with a `CreateUserRequest` body to create a `User` resource. |
| The thing you get back has the ID and name. | The `UserResponse` DTO contains the `id` (UUID) and `displayName` (string) fields. |
| Pass the options object to configure the behavior. | Pass a `RetryPolicy` enum value to the `maxRetries` parameter of the `fetchWithRetry` function. |

### Category 2 — Applications, services, and their subsystems

Scope: deployable units and the locations that are part of them.

*web application, mobile app, desktop client, CLI tool, microservice, monolith, API gateway, load balancer, database server, message broker, cache layer, container, pod, cluster, frontend, backend, admin panel, user dashboard, authentication service, payment service, notification service, search engine, CDN, reverse proxy, serverless function, cron job, worker process*

| Non-STE | STE |
|---|---|
| The thing that runs the website broke. | The `nginx` reverse proxy on the `web-01` frontend server stopped responding. |
| Log into the admin area. | Log into the `AdminPanel` at `https://admin.example.com`. |
| The background job processor handles emails. | The `EmailWorker` process in the `worker` pod handles outbound email delivery. |

### Category 3 — Development tools, SDKs, and their components

*IDE, code editor, terminal emulator, compiler, interpreter, transpiler, bundler, linter, formatter, debugger, profiler, package manager, version control system, CI runner, test framework, assertion library, mocking library, static analyzer, API client, database client, container runtime, orchestration tool, IaC tool, monitoring dashboard, log aggregator, feature flag service, secrets manager*

| Non-STE | STE |
|---|---|
| Run the check tool to find problems. | Run `ESLint` with the `@company/eslint-config` preset to find lint violations. |
| Use the test thing to verify the code. | Use the `Jest` test framework with `@testing-library/react` to verify component behavior. |
| The build tool makes the final files. | The `Webpack` bundler, configured via `webpack.config.js`, produces the production bundle in `dist/`. |

### Category 4 — Dependencies, packages, and technical debt

Scope: consumed material that can cause regressions or malfunctions.

*dependency, transitive dependency, package, library, framework, runtime, polyfill, shim, vendor bundle, dead code, deprecated API, legacy module, orphaned code, code smell, TODO comment, FIXME comment, zombie import, circular dependency, peer dependency, dev dependency, optional dependency, pinned version, lockfile, SBOM, supply chain artifact, third-party script, ad-hoc patch, monkey-patch, workaround code*

| Non-STE | STE |
|---|---|
| Watch out for old stuff that nobody uses anymore. | Remove the deprecated `UserService.legacyCreate()` method — it is dead code with zero callers as of v3.2. |
| There's a problem with one of the things we installed. | The `lodash@4.17.20` transitive dependency introduces a prototype pollution vulnerability (CVE-2020-8203). |
| Don't use the thing from the old library. | Replace the deprecated `moment` package with the `date-fns` library in the `OrderTimeline` component. |

### Category 5 — Hosting, CI/CD, and deployment infrastructure

*cloud provider, region, availability zone, data center, Kubernetes cluster, namespace, Docker registry, artifact repository, build pipeline, deployment pipeline, staging environment, production environment, sandbox environment, on-premise server, virtual machine, bare-metal host, edge location, CDN endpoint, storage bucket, message queue, event bus, API gateway endpoint, load balancer target group, auto-scaling group, service mesh, ingress controller*

| Non-STE | STE |
|---|---|
| Deploy to the cloud place. | Deploy the `orders-service` container image to the `us-east-1` `production` Kubernetes cluster in namespace `orders`. |
| The pipeline builds and ships the code. | The `deploy-prod` GitHub Actions workflow builds the Docker image, pushes it to `ECR`, and applies the `kustomize` overlay for `production`. |

### Category 6 — Systems, architecture, and their configurations

Scope: the structure, operation, composition, and system design of software.

*architecture, design pattern, layered architecture, hexagonal architecture, microservice, event-driven architecture, CQRS, event sourcing, pub/sub, message queue, event bus, database shard, read replica, write-ahead log, connection pool, circuit breaker, retry policy, rate limiter, cache layer, CDN edge, feature flag, A/B test variant, canary deployment, blue-green deployment, rolling update, service registry, configuration provider, secret store, reverse proxy, API gateway route, middleware chain, plugin system, dependency injection container, ORM, migration runner*

| Non-STE | STE |
|---|---|
| The system uses a pattern to handle failures gracefully. | The `PaymentGateway` client uses a `CircuitBreaker` pattern — after 5 consecutive failures, it opens and returns cached fallback responses for 30 seconds. |
| The config changes depending on where it's running. | The `FeatureFlags` service resolves the `enable_new_checkout` flag from `LaunchDarkly` based on the `X-Environment` header (`staging` or `production`). |

### Category 7 — Algorithms, data structures, and formulas

*algorithm, data structure, Big-O notation, time complexity, space complexity, hash table, binary tree, linked list, graph, trie, bloom filter, LRU cache, consistent hashing, recursion, memoization, dynamic programming, greedy algorithm, backtracking, binary search, quicksort, mergesort, topological sort, Dijkstra, BFS, DFS, A\*, Paxos, Raft, two-phase commit, saga pattern, idempotency key, eventual consistency, CAP theorem, ACID, BASE, vector clock, Lamport timestamp, Merkle tree, shard key, partition key, compound index, covering index, query plan, cardinality, selectivity, normalization, denormalization, OLTP, OLAP, ETL, stream processing, batch processing, map-reduce, actor model, CSP, semaphore, mutex, atomic operation, CAS,* `O(n log n)`, `f(x) = x² + 3x - 2`

| Non-STE | STE |
|---|---|
| The search is fast because it uses a good algorithm. | The `SearchIndex` uses a `BloomFilter` (`O(k)` lookup, where `k` is the number of hash functions) to skip negative lookups before falling back to a `B-Tree` index scan. |
| The function remembers results so it doesn't recompute. | `computeShippingCost(addressHash)` is memoized with an `LRU Cache` (capacity 1024, `O(1)` eviction) to avoid redundant API calls. |

### Category 8 — Codebase navigation and project structure

*directory, subdirectory, file path, import path, package root, module root, workspace root, monorepo root, source directory, test directory, build output, entry point, barrel export, index file, re-export, absolute import, relative import, path alias, symlink, Git root, branch, tag, commit, HEAD, upstream, origin, fork, submodule, subtree, vendor directory, node_modules, virtual environment, GOPATH, classpath, namespace, package scope, module scope, public API surface, internal package, private module, exported symbol*

| Non-STE | STE |
|---|---|
| The file is in the utils folder somewhere. | The `formatCurrency` helper is in `src/shared/utils/formatting.ts`, re-exported from the barrel file at `src/shared/utils/index.ts`. |
| Go to the branch where the fix was made. | Check out the `hotfix/payment-timeout` branch from `origin` (forked from `main` at commit `a3f8b2c`). |

### Category 9 — Numbers, units of measurement, and time

*latency, throughput, response time, p50, p95, p99, p999, ops/sec, req/sec, RPM, RPS, QPS, TPS, bytes, KB, MB, GB, TB, KiB, MiB, ms, µs, ns, s, min, hr, CPU core, thread count, memory usage, heap size, stack size, GC pause, cold start time, warm start time, bootstrap time, build time, deploy time, MTTR, MTBF, uptime, downtime, error rate, success rate, availability (99.9%, 99.99%), RPO, RTO, SLO, SLI, SLA, concurrency, connection count, pool size, batch size, page size, offset, limit, TTL, timeout, interval, poll interval, retry delay, backoff multiplier, rate limit (tokens/sec), quota, sample rate, cardinality*

| Non-STE | STE |
|---|---|
| The API is pretty fast most of the time. | The `GET /search` endpoint has a p95 latency of 120 ms and a p99 latency of 350 ms at 5000 RPM. |
| Give it time to try again if it fails. | Configure the `RetryPolicy` with a `baseDelay` of 200 ms, a `maxDelay` of 5 s, and an exponential backoff multiplier of 2.0 (max 3 retries). |

### Category 10 — Quoted text

Scope: text you cannot change — error messages, log output, API responses, UI
string literals, command-line output.

*error message, stack trace, log line, HTTP response body, JSON payload, XML response, environment variable value, CLI flag, command option, shell command output, status code text, exception message, assertion message, deprecation warning, compiler diagnostic, linter rule ID, test failure message, benchmark output, profiler report, API route pattern, SQL query string, GraphQL query, regex pattern, glob pattern, cron expression, semantic version string, git commit hash, UUID string, JWT token (example),* `"Connection refused"`, `"404 Not Found"`, `"TypeError: Cannot read properties of undefined"`, `"--config=./prod.yaml"`, `"npm ERR! code ERESOLVE"`

| Non-STE | STE |
|---|---|
| If you get an error about the database, restart it. | If the application logs `"FATAL: sorry, too many clients already"` from `PostgreSQL`, restart the `pgbouncer` connection pooler. |
| Run the command with the flag that skips tests. | Run `./gradlew build -x test` (the `-x` flag excludes the `test` Gradle task from the build lifecycle). |

Quoted text is reproduced verbatim, even when it breaks other STE-Code rules.

### Category 11 — Roles, teams, and organizations

*maintainer, author, contributor, reviewer, approver, code owner, release manager, on-call engineer, SRE, DevOps engineer, security champion, triage team, core team, steering committee, technical lead, staff engineer, principal engineer, intern, vendor, client, stakeholder, end user, GitHub organization, npm organization, Docker Hub organization, CNCF, Apache Software Foundation, Linux Foundation, Mozilla, Google, Microsoft, OpenAPI Initiative, ECMA, ISO, W3C, IETF, OWASP,* `CODEOWNERS` file, `@backend-team`, `@security-reviewers`

### Category 12 — User interface elements and accessibility

*button, text input, checkbox, radio button, dropdown, select menu, toggle, slider, modal, dialog, tooltip, popover, toast, snackbar, banner, tab, accordion, breadcrumb, pagination, carousel, card, table, data grid, form, form field, label, placeholder, icon, avatar, badge, spinner, progress bar, skeleton loader, navbar, sidebar, footer, header, search bar, filter panel, drawer, split pane, context menu, keyboard shortcut, hotkey, focus trap, skip link, screen reader label, ARIA role, ARIA attribute, landmark region, heading hierarchy*

### Category 13 — User data, preferences, and session state

*user profile, display name, avatar URL, email address, phone number, billing address, shipping address, payment method, credit card, subscription plan, usage quota, rate limit bucket, API key, access token, refresh token, ID token, session cookie, CSRF token, user preference, theme setting, language locale, timezone, notification setting, opt-in flag, consent record, bookmark, watchlist, shopping cart, wishlist, search history, recently viewed, draft content, clipboard data, localStorage key, IndexedDB store, browser fingerprint, device ID, push notification token*

### Category 14 — Health, diagnostics, and observability

*health check, liveness probe, readiness probe, startup probe, heartbeat, ping, metric, trace, span, log level, structured log, correlation ID, trace ID, span ID, alert, incident, SLO, SLI, error budget, burn rate, on-call rotation, escalation policy, runbook, playbook, postmortem, root cause analysis (RCA), mean time to recovery (MTTR), mean time to detection (MTTD), anomaly detection, threshold breach, saturation, latency tail, error spike, traffic drop, resource exhaustion, memory pressure, disk pressure, CPU throttling, GC thrashing, connection storm, thundering herd, cascading failure, split-brain, partition, degraded state, brownout, blackout*

### Category 15 — Documents, standards, and their structural parts

*README, CHANGELOG, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, ARCHITECTURE, ADR (Architecture Decision Record), RFC (Request for Comments), API reference, OpenAPI spec, GraphQL schema, AsyncAPI spec, style guide, coding standard, linting rules, PR template, issue template, discussion template, release notes, migration guide, upgrade guide, getting started guide, quickstart, tutorial, how-to guide, explanation, reference, concept document, FAQ, glossary, onboarding guide, runbook, playbook, incident report, postmortem, design doc, technical spec, product requirements document (PRD), test plan, test case, acceptance criteria, Definition of Done, Definition of Ready, service level agreement (SLA), terms of service (TOS), privacy policy, cookie policy, data processing agreement (DPA), semantic versioning (SemVer), conventional commits, Git commit message format, doc comment, TSDoc, JSDoc, godoc, docstring, annotation, attribute, decorator doc, heading, subheading, section, subsection, paragraph, code block, table, list, admonition (note, warning, tip, danger, caution, important), hyperlink, cross-reference, footnote, bibliography, index, glossary entry, TOC (table of contents)*

### Category 16 — Environmental and operational conditions

Scope: runtime environments, execution contexts, and operating parameters that
affect software behavior.

*production, staging, development, testing, CI, localhost, operating system, OS version, kernel version, distribution, CPU architecture (x86_64, arm64), Node.js version, Python version, Java version, Go version, browser, browser version, rendering engine, screen resolution, viewport size, device type, network condition (offline, slow 3G, 4G, WiFi), Docker image, container runtime, Kubernetes version, cloud region, availability zone, environment variable, build flag, feature flag state, A/B test bucket, configuration profile, Spring profile, Rails environment, NODE_ENV, DEBUG mode, verbose logging, trace level, read-only mode, maintenance mode, degraded mode, dark mode, high contrast mode, reduced motion, forced colors, RTL locale, daylight saving time transition, leap second, timezone offset*

### Category 17 — Colors and theme tokens

*primary, secondary, accent, success, warning, error, info, neutral, background, surface, text, border, divider, shadow, overlay, red, green, blue, yellow, orange, purple, pink, teal, cyan, gray, black, white, transparent, hex code* (`#FF5733`, `#1A1A2E`)*, RGB* (`rgb(255, 87, 51)`)*, RGBA* (`rgba(26, 26, 46, 0.8)`)*, HSL* (`hsl(12, 100%, 60%)`)*, CSS custom property* (`--color-primary-500`, `--color-text-on-primary`)*, design token, color ramp, color scale (50-900), light mode, dark mode, high contrast mode, color blindness safe palette, WCAG contrast ratio, semantic color, brand color*

Colors in design systems are technical nouns. Do not use comparative forms
("darker", "lightest") — reference the specific design token or color ramp step.

### Category 18 — Damage terms: bugs, errors, and failure modes

*crash, segfault, null pointer exception, type error, reference error, syntax error, range error, stack overflow, buffer overflow, memory leak, resource leak, dangling pointer, use-after-free, double free, race condition, deadlock, livelock, starvation, priority inversion, ABA problem, torn read, torn write, dirty read, non-repeatable read, phantom read, lost update, write skew, serialization anomaly, split-brain, network partition, timeout, connection reset, DNS failure, TLS handshake failure, certificate expiry, HTTP 500, HTTP 502, HTTP 503, HTTP 504, rate limit exceeded, quota exceeded, out of memory (OOM), disk full, inode exhaustion, file descriptor exhaustion, thread pool exhaustion, connection pool exhaustion, GC thrashing, cache stampede, cache penetration, cache avalanche, hot partition, data corruption, bit rot, checksum failure, hash collision, infinite loop, infinite recursion, integer overflow, integer underflow, floating point precision error, off-by-one error, SQL injection, XSS, CSRF, prototype pollution, deserialization vulnerability, dependency confusion, supply chain attack, CVE, CWE, zero-day*

### Category 19 — Computer science, information and communication technology

*API, REST, GraphQL, gRPC, WebSocket, SSE, HTTP/2, HTTP/3, TCP, UDP, TLS, mTLS, OAuth 2.0, OIDC, SAML, JWT, API key, CORS, CSP, HSTS, DNS, CDN, IP, IPv4, IPv6, CIDR, VPN, VPC, subnet, firewall rule, WAF, DDoS, load balancing, reverse proxy, forward proxy, caching, compression, serialization (JSON, Protobuf, MessagePack, Avro), encoding (Base64, URL encoding, UTF-8, ASCII), hashing (SHA-256, bcrypt, Argon2), encryption (AES-256-GCM, RSA, ECDSA), Unicode, emoji, regex, glob pattern, SQL, NoSQL, ORM, migration, seed data, transaction, ACID, BASE, sharding, replication, partitioning, indexing, normalization, denormalization, message queue, pub/sub, event sourcing, CQRS, saga, distributed transaction, consensus, leader election, service discovery, circuit breaker, bulkhead, retry, backoff, idempotency, rate limiting, throttling, API versioning, semantic versioning, feature flag, canary release, blue-green deployment, rolling update, immutable infrastructure, infrastructure as code, configuration as code, GitOps, observability, telemetry, tracing, metrics, logging, profiling, APM, RUM, continuous integration, continuous delivery, continuous deployment, DevOps, DevSecOps, Git, Docker, Kubernetes, Helm, Terraform, Ansible*

## Extension categories (STE-Code additions)

The nineteen categories above map the source standard. STE-Code adds three
further categories for terminology that code documentation needs and that has
no aerospace counterpart. Use them the same way: a term is approved if it fits.

### Category 20 — Operations, release management, and lifecycle

*deployment, release, rollout, rollback, hotfix, patch, minor release, major release, breaking change, deprecation, end-of-life (EOL), sunset, migration, upgrade path, backward compatibility, forward compatibility, downtime, maintenance window, zero-downtime deployment, graceful shutdown, drain, scale up, scale down, scale out, scale in, autoscaling, horizontal scaling, vertical scaling, incident, outage, service disruption, failover, disaster recovery, backup, restore, point-in-time recovery, snapshot, retention policy, runbook execution, playbook, on-call handoff, escalation, war room, status page, SLA breach, SLO violation, error budget policy, change freeze, code freeze, release train, sprint, iteration, milestone, roadmap, epic, user story, bug ticket, triage, priority (P0, P1, P2, P3), severity (SEV0, SEV1, SEV2, SEV3), service level objective, operational level agreement (OLA), underpinning contract (UC), vendor management, procurement, onboarding, offboarding, access revocation, audit log, compliance check, penetration test, vulnerability scan, security patch, responsible disclosure, coordinated vulnerability disclosure (CVD)*

### Category 21 — Licenses, compliance, and legal terms

*license, open-source license, proprietary license, MIT License, Apache 2.0 License, GPLv3, LGPL, BSD, AGPL, MPL, Unlicense, Creative Commons, EULA, terms of service (TOS), privacy policy, cookie policy, data processing agreement (DPA), service level agreement (SLA), contributor license agreement (CLA), Developer Certificate of Origin (DCO), copyright, trademark, patent, intellectual property, attribution, copyleft, permissive license, compliance, regulatory compliance, GDPR, CCPA, HIPAA, SOC 2, ISO 27001, PCI DSS, FedRAMP, FISMA, export control, EAR, ITAR, sanctions list, embargo, data residency, data sovereignty, data retention policy, right to erasure, right to access, data subject request (DSR), personal data, PII (Personally Identifiable Information), PHI (Protected Health Information), sensitive data, data classification, data handling policy, acceptable use policy, code of conduct, vendor risk assessment, security questionnaire (CAIQ, SIG), audit report, attestation, SOC report, penetration test report, vulnerability disclosure policy, bug bounty program terms, responsible disclosure policy, indemnification, limitation of liability, warranty disclaimer, governing law, jurisdiction, severability, force majeure, assignment, termination, survival clause, third-party notice, open-source attribution, NOTICE file, SBOM (Software Bill of Materials)*

### Category 22 — Test fixtures, mock data, and placeholders

Scope: sample entities used in code examples, test cases, and documentation
demonstrations.

*test fixture, mock object, stub, spy, fake, dummy, test double, seed data, sample data, example record, placeholder, synthetic data, faker data, lorem ipsum,* `"John Doe"`, `"Jane Smith"`, `"Acme Corp"`, `"example.com"`, `"test@example.com"`, `"user_12345"`, `"order_abc"`, `"00000000-0000-0000-0000-000000000000"`, `"foo"`, `"bar"`, `"baz"`, `"qux"`, `"quux"`, `"spam"`, `"eggs"`, `"ham"`, `"hello world"`, `"TODO"`, `"FIXME"`, `"HACK"`, `"XXX"`, `"WIP"`, `"tmp"`, `"scratch"`, `"sandbox"`, `"playground"`, `"hello-world-app"`, `"my-first-repo"`, `"boilerplate"`, `"starter-kit"`, `"todo-mvc"`, `"FakeUser"`, `"MockOrderRepository"`, `"StubPaymentGateway"`, `"InMemoryDatabase"`, `"NullLogger"`, `TestUserFactory.create()`, `Fixtures.defaultUser()`, `faker.internet.email()`

## Reference catalogue: where project technical nouns come from

Do not invent terms. Take unlisted technical nouns from a source of record and
record them in the project glossary before use:

| Source | Supplies |
|---|---|
| Project glossary / terminology database | Approved project-specific nouns |
| API reference, OpenAPI/GraphQL schema | Endpoint, type, field, and parameter names |
| Architecture Decision Records (ADRs) | Architecture and component names |
| `CODEOWNERS`, org charts | Role and team names |
| Package manifest and lockfile | Exact dependency names and versions |
| Standards bodies (ISO, W3C, IETF, OWASP, ECMA) | Protocol, format, and security terms |

Rules for glossary entries:

1. One term, one meaning. Do not use two terms for the same concept.
2. Record the category number the term belongs to.
3. Spell and capitalize the term exactly as the source of record does
   (`PostgreSQL`, `Node.js`, `Kubernetes`).
4. If a term fits no category, it is not a technical noun — rewrite the sentence
   with approved words.
