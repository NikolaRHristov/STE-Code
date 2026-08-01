# Level 3 — Synonyms and Approved Words

This slice defines how to choose words in STE-Code when the approved-words
dictionary does not contain the term you need. It covers the **technical-noun
category system** (Rule 1.5) and the rules that govern unapproved-word use and
synonym selection (Rules 1.6–1.11).

Core idea: the dictionary lists approved everyday words. When you need a
word not in the dictionary, you may still use it if it qualifies as a
**technical noun** — a noun term for a specified software concept that fits one
of 19 categories. This lets project-specific terminology (class names, protocol
names, metrics, error strings) appear in documentation without breaking
controlled-language rules.

## Rule 1.5 — Technical noun categories (framework)

You can use a term in code documentation if you can include it in a technical
noun category.

- A **technical noun** is a noun term that refers to a specified software
  concept and is applicable to a given codebase, library, or system.
- The approved-words dictionary does not list project-specific technical nouns
  because each codebase, framework, and ecosystem uses different terminology.
- Find these terms in your project glossary, API reference, or architecture
  decision records (ADRs).
- Use technical nouns in procedural and descriptive documentation — API
  references, commit messages, READMEs, code comments, technical specs — when
  they fit one or more of the 19 categories below.

Non-STE vs STE:

| Non-STE | STE |
|---------|-----|
| Use the thing to call the function that gets data from the database. | Use the `fetchUser` method of the `UserRepository` to retrieve a `User` record from the `PostgreSQL` database. |
| ("thing", "gets data" — no technical nouns; ambiguous) | (`fetchUser`, `UserRepository`, `User`, `PostgreSQL` — all classified technical nouns) |

## The 19 technical noun categories

Each category below lists **code-domain** terms that count as technical nouns.
A term fits if it refers to a specified software concept of that kind. The lists
are examples, not a closed vocabulary — add project-specific terms via your
glossary.

### 1. API and library components
Terms for API and library components: endpoint, method, parameter, query
parameter, path parameter, request body, response body, header, status code,
module, class, interface, type alias, enum, constant, decorator, middleware,
route handler, serializer, DTO, model, schema, callback, hook, plugin.
- STE: Call the `POST /api/v1/users` endpoint with a `CreateUserRequest` body
  to create a `User` resource.

### 2. Applications, services, and subsystems
Web application, mobile app, desktop client, CLI tool, microservice, monolith,
API gateway, load balancer, database server, message broker, cache layer,
container, pod, cluster, frontend, backend, admin panel, user dashboard,
authentication service, payment service, notification service, search engine,
CDN, reverse proxy, serverless function, cron job, worker process.
- STE: The `nginx` reverse proxy on the `web-01` frontend server stopped
  responding.

### 3. Development tools and SDKs
IDE, code editor, terminal emulator, compiler, interpreter, transpiler, bundler,
linter, formatter, debugger, profiler, package manager, version control system,
CI runner, test framework, assertion library, mocking library, static analyzer,
API client, database client, container runtime, orchestration tool, IaC tool,
monitoring dashboard, log aggregator, feature flag service, secrets manager.
- STE: Run `ESLint` with the `@company/eslint-config` preset to find lint
  violations.

### 4. Dependencies, packages, technical debt
Dependency, transitive dependency, package, library, framework, runtime,
polyfill, shim, vendor bundle, dead code, deprecated API, legacy module,
orphaned code, code smell, TODO comment, FIXME comment, zombie import, circular
dependency, peer dependency, dev dependency, optional dependency, pinned
version, lockfile, SBOM, supply chain artifact, third-party script, ad-hoc
patch, monkey-patch, workaround code.
- STE: Remove the deprecated `UserService.legacyCreate()` method — dead code
  with zero callers as of v3.2.

### 5. Hosting, CI/CD, deployment infrastructure
Cloud provider, region, availability zone, data center, Kubernetes cluster,
namespace, Docker registry, artifact repository, build pipeline, deployment
pipeline, staging environment, production environment, sandbox environment,
on-premise server, virtual machine, bare-metal host, edge location, CDN
endpoint, storage bucket, message queue, event bus, API gateway endpoint, load
balancer target group, auto-scaling group, service mesh, ingress controller.
- STE: Deploy the `orders-service` container image to the `us-east-1`
  `production` Kubernetes cluster in namespace `orders`.

### 6. Software system design and architecture
Architecture, design pattern, layered architecture, hexagonal architecture,
microservice, event-driven architecture, CQRS, event sourcing, pub/sub, message
queue, event bus, database shard, read replica, write-ahead log, connection
pool, circuit breaker, retry policy, rate limiter, cache layer, CDN edge,
feature flag, A/B test variant, canary deployment, blue-green deployment,
rolling update, service registry, configuration provider, secret store, reverse
proxy, API gateway route, middleware chain, plugin system, dependency injection
container, ORM, migration runner.
- STE: The `PaymentGateway` client uses a `CircuitBreaker` pattern — after 5
  consecutive failures it opens and returns cached fallback responses for 30 s.

### 7. Algorithms, data structures, computational concepts
Algorithm, data structure, Big-O notation, time complexity, space complexity,
hash table, binary tree, linked list, graph, trie, bloom filter, LRU cache,
consistent hashing, recursion, memoization, dynamic programming, greedy
algorithm, backtracking, binary search, quicksort, mergesort, topological sort,
Dijkstra, BFS, DFS, A*, Paxos, Raft, two-phase commit, saga pattern, idempotency
key, eventual consistency, CAP theorem, ACID, BASE, vector clock, Lamport
timestamp, Merkle tree, shard key, partition key, compound index, covering
index, query plan, cardinality, selectivity, normalization, denormalization,
OLTP, OLAP, ETL, stream processing, batch processing, map-reduce, actor model,
CSP, semaphore, mutex, atomic operation, CAS.
- STE: `computeShippingCost(addressHash)` is memoized with an `LRU Cache`
  (capacity 1024, `O(1)` eviction) to avoid redundant API calls.

### 8. Codebase navigation and project structure
Directory, subdirectory, file path, import path, package root, module root,
workspace root, monorepo root, source directory, test directory, build output,
entry point, barrel export, index file, re-export, absolute import, relative
import, path alias, symlink, Git root, branch, tag, commit, HEAD, upstream,
origin, fork, submodule, subtree, vendor directory, node_modules, virtual
environment, GOPATH, classpath, namespace, package scope, module scope, public
API surface, internal package, private module, exported symbol.
- STE: The `formatCurrency` helper is in `src/shared/utils/formatting.ts`,
  re-exported from the barrel file at `src/shared/utils/index.ts`.

### 9. Metrics, timing, quantitative measurements
Latency, throughput, response time, p50, p95, p99, p999, ops/sec, req/sec, RPM,
RPS, QPS, TPS, bytes, KB, MB, GB, TB, KiB, MiB, ms, µs, ns, s, min, hr, CPU
core, thread count, memory usage, heap size, stack size, GC pause, cold start
time, warm start time, bootstrap time, build time, deploy time, MTTR, MTBF,
uptime, downtime, error rate, success rate, availability (99.9%, 99.99%), RPO,
RTO, SLO, SLI, SLA, concurrency, connection count, pool size, batch size, page
size, offset, limit, TTL, timeout, interval, poll interval, retry delay, backoff
multiplier, rate limit (tokens/sec), quota, sample rate, cardinality.
- STE: The `GET /search` endpoint has a p95 latency of 120 ms and a p99 latency
  of 350 ms at 5000 RPM.

### 10. Quoted text (cannot change)
Quoted error messages, log output, API responses, UI string literals, CLI
output: error message, stack trace, log line, HTTP response body, JSON payload,
XML response, environment variable value, CLI flag, command option, shell
command output, status code text, exception message, assertion message,
deprecation warning, compiler diagnostic, linter rule ID, test failure message,
benchmark output, profiler report, API route pattern, SQL query string, GraphQL
query, regex pattern, glob pattern, cron expression, semantic version string,
git commit hash, UUID string, JWT token (example), `"Connection refused"`,
`"404 Not Found"`, `"TypeError: Cannot read properties of undefined"`,
`"--config=./prod.yaml"`, `"npm ERR! code ERESOLVE"`.
- STE: If the application logs `"FATAL: sorry, too many clients already"` from
  `PostgreSQL`, restart the `pgbouncer` connection pooler.

### 11. Project roles, teams, organizations, entities
Maintainer, author, contributor, reviewer, approver, code owner, release
manager, on-call engineer, SRE, DevOps engineer, security champion, triage team,
core team, steering committee, technical lead, staff engineer, principal
engineer, intern, vendor, client, stakeholder, end user, GitHub organization,
npm organization, Docker Hub organization, CNCF, Apache Software Foundation,
Linux Foundation, Mozilla, Google, Microsoft, OpenAPI Initiative, ECMA, ISO,
W3C, IETF, OWASP, `CODEOWNERS` file, `@backend-team`, `@security-reviewers`.
- STE: Request a review from `@frontend-core` (code owners for `src/components/`
  per `.github/CODEOWNERS`).

### 12. UI elements, interaction points, accessibility
Button, text input, checkbox, radio button, dropdown, select menu, toggle,
slider, modal, dialog, tooltip, popover, toast, snackbar, banner, tab, accordion,
breadcrumb, pagination, carousel, card, table, data grid, form, form field,
label, placeholder, icon, avatar, badge, spinner, progress bar, skeleton loader,
navbar, sidebar, footer, header, search bar, filter panel, drawer, split pane,
context menu, keyboard shortcut, hotkey, focus trap, skip link, screen reader
label, ARIA role, ARIA attribute, landmark region, heading hierarchy.
- STE: Click the `hamburger` icon in the `Navbar` to open the `Sidebar` drawer
  (ARIA role `navigation`, label "Main menu").

### 13. User data, preferences, session state
User profile, display name, avatar URL, email address, phone number, billing
address, shipping address, payment method, credit card, subscription plan, usage
quota, rate limit bucket, API key, access token, refresh token, ID token,
session cookie, CSRF token, user preference, theme setting, language locale,
timezone, notification setting, opt-in flag, consent record, bookmark,
watchlist, shopping cart, wishlist, search history, recently viewed, draft
content, clipboard data, localStorage key, IndexedDB store, browser fingerprint,
device ID, push notification token.
- STE: Persist the user's `uiPreferences` (theme `"dark"`, locale `"en-GB"`,
  timezone `"Europe/London"`) to `localStorage` under key `user_prefs_v2`.

### 14. System health, diagnostics, observability, failure modes
Health check, liveness probe, readiness probe, startup probe, heartbeat, ping,
metric, trace, span, log level, structured log, correlation ID, trace ID, span
ID, alert, incident, SLO, SLI, error budget, burn rate, on-call rotation,
escalation policy, runbook, playbook, postmortem, root cause analysis (RCA),
mean time to recovery (MTTR), mean time to detection (MTTD), anomaly detection,
threshold breach, saturation, latency tail, error spike, traffic drop, resource
exhaustion, memory pressure, disk pressure, CPU throttling, GC thrashing,
connection storm, thundering herd, cascading failure, split-brain, partition,
degraded state, brownout, blackout.
- STE: The `payments-service` `readinessProbe` is failing — `/healthz` returns
  HTTP 503; the service is `degraded` and removed from the load balancer target
  group.

### 15. Documents, standards, specifications, their parts
README, CHANGELOG, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, GOVERNANCE,
ARCHITECTURE, ADR (Architecture Decision Record), RFC (Request for Comments),
API reference, OpenAPI spec, GraphQL schema, AsyncAPI spec, style guide, coding
standard, linting rules, PR template, issue template, discussion template,
release notes, migration guide, upgrade guide, getting started guide, quickstart,
tutorial, how-to guide, explanation, reference, concept document, FAQ, glossary,
onboarding guide, runbook, playbook, incident report, postmortem, design doc,
technical spec, product requirements document (PRD), test plan, test case,
acceptance criteria, Definition of Done, Definition of Ready, service level
agreement (SLA), terms of service (TOS), privacy policy, cookie policy, data
processing agreement (DPA), semantic versioning (SemVer), conventional commits,
Git commit message format, doc comment, TSDoc, JSDoc, godoc, docstring,
annotation, attribute, decorator doc, heading, subheading, section, subsection,
paragraph, code block, table, list, admonition (note, warning, tip, danger,
caution, important), hyperlink, cross-reference, footnote, bibliography, index,
glossary entry, TOC (table of contents).
- STE: Record the decision in an ADR
  (`docs/adr/0014-use-event-sourcing-for-orders.md`) with Context, Decision,
  Consequences, Alternatives Considered sections.

### 16. Runtime environments, execution contexts, operating parameters
Production, staging, development, testing, CI, localhost, operating system, OS
version, kernel version, distribution, CPU architecture (x86_64, arm64), Node.js
version, Python version, Java version, Go version, browser, browser version,
rendering engine, screen resolution, viewport size, device type, network
condition (offline, slow 3G, 4G, WiFi), Docker image, container runtime,
Kubernetes version, cloud region, availability zone, environment variable, build
flag, feature flag state, A/B test bucket, configuration profile, Spring
profile, Rails environment, NODE_ENV, DEBUG mode, verbose logging, trace level,
read-only mode, maintenance mode, degraded mode, dark mode, high contrast mode,
reduced motion, forced colors, RTL locale, daylight saving time transition, leap
second, timezone offset.
- STE: The `TextRenderer` crash only reproduces on `macOS 14.5` (arm64) with
  `Node.js 20.11.0` — the `canvas` native addon fails to load the prebuilt
  binary.

### 17. Colors and theme tokens
Primary, secondary, accent, success, warning, error, info, neutral, background,
surface, text, border, divider, shadow, overlay, red, green, blue, yellow,
orange, purple, pink, teal, cyan, gray, black, white, transparent, hex code
(`#FF5733`, `#1A1A2E`), RGB (`rgb(255, 87, 51)`), RGBA (`rgba(26, 26, 46, 0.8)`),
HSL (`hsl(12, 100%, 60%)`), CSS custom property (`--color-primary-500`,
`--color-text-on-primary`), design token, color ramp, color scale (50-900), light
mode, dark mode, high contrast mode, color blindness safe palette, WCAG contrast
ratio, semantic color, Brand Color.
- Colors in design systems are technical nouns. Do NOT use comparative forms
  ("darker", "lightest") — reference the specific design token or ramp step.
- STE: Set the page background to `--color-surface-page` (resolves to `#FFFFFF`
  in light mode, `#121212` in dark mode), WCAG AA contrast ≥ 4.5:1.

### 18. Bugs, errors, exceptions, failure modes
Crash, segfault, null pointer exception, undefined is not a function, type error,
reference error, syntax error, range error, stack overflow, buffer overflow,
memory leak, resource leak, dangling pointer, use-after-free, double free, race
condition, deadlock, livelock, starvation, priority inversion, ABA problem, torn
read, torn write, dirty read, non-repeatable read, phantom read, lost update,
write skew, serialization anomaly, split-brain, network partition, timeout,
connection reset, DNS failure, TLS handshake failure, certificate expiry,
HTTP 500, HTTP 502, HTTP 503, HTTP 504, rate limit exceeded, quota exceeded, out
of memory (OOM), disk full, inode exhaustion, file descriptor exhaustion, thread
pool exhaustion, connection pool exhaustion, GC thrashing, cache stampede, cache
penetration, cache avalanche, hot partition, data corruption, bit rot, checksum
failure, hash collision, infinite loop, infinite recursion, integer overflow,
integer underflow, floating point precision error, off-by-one error, SQL
injection, XSS, CSRF, prototype pollution, deserialization vulnerability,
dependency confusion, supply chain attack, CVE, CWE, zero-day.
- STE: `OrderProcessor` has a race condition: threads A and B both check
  `inventory[sku].quantity > 0` before either decrements — oversell. Fix:
  `SELECT ... FOR UPDATE` row lock.

### 19. Computer science and ICT
API, REST, GraphQL, gRPC, WebSocket, SSE, HTTP/2, HTTP/3, TCP, UDP, TLS, mTLS,
OAuth 2.0, OIDC, SAML, JWT, API key, CORS, CSP, HSTS, DNS, CDN, IP, IPv4, IPv6,
CIDR, VPN, VPC, subnet, firewall rule, WAF, DDoS, load balancing, reverse proxy,
forward proxy, caching, compression, serialization (JSON, Protobuf, MessagePack,
Avro), encoding (Base64, URL encoding), hashing (SHA-256, bcrypt, Argon2),
encryption (AES-256-GCM, RSA, ECDSA), encoding (UTF-8, ASCII), Unicode, emoji,
regex, glob pattern, SQL, NoSQL, ORM, migration, seed data, transaction, ACID,
BASE, sharding, replication, partitioning, indexing, normalization,
denormalization, message queue, pub/sub, event sourcing, CQRS, saga, distributed
transaction, consensus, leader election, service discovery, circuit breaker,
bulkhead, retry, backoff, idempotency, rate limiting, throttling, API versioning,
semantic versioning, feature flag, canary release, blue-green deployment, rolling
update, immutable infrastructure, infrastructure as code, configuration as code,
GitOps, observability, telemetry, tracing, metrics, logging, profiling, APM, RUM,
continuous integration, continuous delivery, continuous deployment, DevOps,
DevSecOps, Git, Docker, Kubernetes, Helm, Terraform, Ansible.
- STE: `Orders API` uses OAuth 2.0 Authorization Code flow (PKCE); clients get a
  JWT from `POST /oauth/token` and pass it in the `Authorization: Bearer <token>` header.

### 20. DevOps, release management, lifecycle support
Deployment, release, rollout, rollback, hotfix, patch, minor release, major
release, breaking change, deprecation, end-of-life (EOL), sunset, migration,
upgrade path, backward compatibility, forward compatibility, downtime,
maintenance window, zero-downtime deployment, graceful shutdown, drain, scale up,
scale down, scale out, scale in, autoscaling, horizontal scaling, vertical
scaling, incident, outage, service disruption, failover, disaster recovery,
backup, restore, point-in-time recovery, snapshot, retention policy, runbook
execution, playbook, on-call handoff, escalation, war room, status page, SLA
breach, SLO violation, error budget policy, change freeze, code freeze, release
train, sprint, iteration, milestone, roadmap, epic, user story, bug ticket,
triage, priority (P0, P1, P2, P3), severity (SEV0, SEV1, SEV2, SEV3), SL1-SL4,
service level objective, operational level agreement (OLA), underpinning
contract (UC), vendor management, procurement, onboarding, offboarding, access
revocation, audit log, compliance check, penetration test, vulnerability scan,
security patch, responsible disclosure, coordinated vulnerability disclosure
(CVD).
- STE: Initiate a hotfix: cherry-pick `fix/payment-null-pointer` onto
  `release/v3.2`, trigger `deploy-hotfix`, canary at 10% for 30 min before full
  rollout.

### 21. Licenses, compliance, regulatory and legal texts
License, open-source license, proprietary license, MIT License, Apache 2.0
License, GPLv3, LGPL, BSD, AGPL, MPL, Unlicense, Creative Commons, EULA, terms of
service (TOS), privacy policy, cookie policy, data processing agreement (DPA),
service level agreement (SLA), contributor license agreement (CLA), Developer
Certificate of Origin (DCO), copyright, trademark, patent, intellectual property,
attribution, copyleft, permissive license, compliance, regulatory compliance,
GDPR, CCPA, HIPAA, SOC 2, ISO 27001, PCI DSS, FedRAMP, FISMA, export control, EAR,
ITAR, sanctions list, embargo, data residency, data sovereignty, data retention
policy, right to erasure, right to access, data subject request (DSR), personal
data, PII, PHI, sensitive data, data classification, data handling policy,
acceptable use policy, code of conduct, vendor risk assessment, security
questionnaire (CAIQ, SIG), audit report, attestation, SOC report, penetration
test report, vulnerability disclosure policy, bug bounty program terms,
responsible disclosure policy, indemnification, limitation of liability, warranty
disclaimer, governing law, jurisdiction, severability, force majeure, assignment,
termination, survival clause, third-party notice, open-source attribution,
NOTICE file, SBOM.
- STE: The `request@2.88.2` package has a missing license field — replace with
  `node-fetch@3.3.2` (MIT). Validate with `npx license-checker --onlyAllow
  "MIT;Apache-2.0;ISC;BSD-2-Clause;BSD-3-Clause"`.

### 22. Test fixtures, mock data, sample datasets, placeholders
Test fixture, mock object, stub, spy, fake, dummy, test double, seed data, sample
data, example record, placeholder, synthetic data, faker data, lorem ipsum,
"John Doe", "Jane Smith", "Acme Corp", "example.com", "test@example.com",
"user_12345", "order_abc", "00000000-0000-0000-0000-000000000000", "foo", "bar",
"baz", "qux", "quux", "spam", "eggs", "ham", "hello world", "TODO", "FIXME",
"HACK", "XXX", "WIP", "tmp", "scratch", "sandbox", "playground", "hello-world-app",
"my-first-repo", "boilerplate", "starter-kit", "todo-mvc", "hello-kubernetes",
"nginx-hello", "FakeUser", "MockOrderRepository", "StubPaymentGateway",
"InMemoryDatabase", "NullLogger", "noop", `TestUserFactory.create()`,
`Fixtures.defaultUser()`, `faker.internet.email()`.
- STE: The `OrderService` test uses `Fixtures.defaultOrder()` and a
  `MockPaymentGateway` stub that returns `PaymentResult.SUCCESS` without real
  HTTP calls.

## Related rules — unapproved words, synonyms, technical-noun use

### Rule 1.6 — Use an unapproved word only as a technical noun
Use a word that is not approved in the standard documentation vocabulary only
when it is a technical noun (classified in one of the 19 categories) or part of a
technical noun.

| Non-STE | STE |
|---------|-----|
| The `base` class holds shared logic for all the page objects. | The `BasePage` class (technical noun, Category 1: API and library components) holds shared logic for all `PageObject` subclasses. |
| ("base" is ambiguous — common word or class name?) | (`BasePage` is a classified technical noun — intentional, project-specific identifier.) |

### Rule 1.7 — Do not verb technical nouns
Do not use words that are technical nouns as verbs in code documentation.

| Non-STE | STE |
|---------|-----|
| `docker` the container and `curl` the endpoint to verify it. | Build the `Docker` image (Category 5: Hosting, CI/CD) and send a request to the endpoint using `curl` (Category 3: Development tools). |

### Rule 1.8 — Use approved technical nouns
Use technical nouns that are approved in your project glossary, organization
style guide, or ecosystem conventions.

| Non-STE | STE |
|---------|-----|
| The `data fetcher thing` in the `store layer` gets records from the `DB`. | The `Repository` pattern implementation (`UserRepository`) in the `data` layer fetches `User` entities from `PostgreSQL` via `TypeORM`. |

### Rule 1.9 — Keep technical nouns short
When you must select a technical noun for code documentation, use one which is
short (not more than three words) and easy to understand.

| Non-STE | STE |
|---------|-----|
| Call the `asynchronous JavaScript Object Notation web token-based user authentication and authorization pre-validation middleware handler`. | Call the `JWT auth middleware`. |

### Rule 1.10 — No slang, regional, or jargon technical nouns
Do not use team-internal slang, regional programming jargon, or company-specific
nicknames as technical nouns in public-facing documentation.

| Non-STE | STE |
|---------|-----|
| The `magic button` on the `admin doodad page` sends a `zap` to the `thingamajig service`. | The `"Sync All"` button on the `Admin Dashboard` sends a `POST` request to the `DataSyncService`. |

### Rule 1.11 — One technical noun per entity
Do not use different technical nouns for the same software entity across your
documentation.

| Non-STE | STE |
|---------|-----|
| Step 1: Call the `UserFetcher` service. Step 2: Configure the `AccountRetriever` module. Step 3: Restart the `ProfileLoader` microservice. | Step 1: Call the `UserService`. Step 2: Configure the `UserService`. Step 3: Restart the `UserService` microservice. |

## Closing notes

- The terms listed in each category are **examples only**. Rule 1.5 does not
  give a full list of all possible technical nouns for code documentation.
- Listed terms use backtick formatting (`LikeThis`) only when the term is a
  literal identifier, API name, or exact string value from code — for example,
  class names, function names, environment variable names, and error message
  strings.
- Add project-specific technical nouns to your project glossary or terminology
  database; they then qualify as approved technical nouns under these categories.

## Quick reference for LLM code-doc generation

1. If the word is in the approved-words dictionary, use it as written.
2. If the word is not in the dictionary, check whether it fits a technical-noun
   category (1–22). If yes, you may use it — preferably verbatim as an
   identifier (`ClassName`) when it is a literal code name.
3. Never verb a technical noun (Rule 1.7); never use slang nicknames for
   public docs (Rule 1.10); never invent multiple names for one entity
   (Rule 1.11).
4. Keep added technical nouns short (≤ 3 words) and consistent with the project
   glossary (Rules 1.9, 1.8, 1.11).



