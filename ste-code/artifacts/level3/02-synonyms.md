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

<!-- MORE -->

