# Level 5 — Code-Domain Technical Noun Categories (Rule 1.5)

> Slice 02 of STE-Code Level 5 (full standard: all rules + extensions + catalogue + provenance).
> Source: ASD-STE100 Issue 9, Rule 1.5 (master.md lines 1698-1878), adapted to the code-documentation domain.
> Companion rules: 1.1 (approved words), 1.6-1.11 (gate mechanics).

## When to use this slice

Use this reference when you must decide whether a word that is NOT in the STE-Code approved dictionary may still appear in code documentation — READMEs, API reference, docstrings, commit messages, ADRs, error messages, and test specs.

**Rule 1.5.** You can use a word that you can include in a code-domain technical noun category.

A code-domain technical noun is a noun term that refers to a specified software concept and is applicable to a given codebase, library, or system. The approved-term dictionary does not list project-specific technical nouns because each codebase, framework, and ecosystem uses different terminology. You can find them in your project glossary, API reference, or architecture decision records (ADRs).

STE-Code gives you the categories below, with examples, to help you:
- Select technical nouns to register in your project glossary.
- Use technical nouns correctly in documentation.

You may use a technical noun in procedural and descriptive code documentation if it fits one or more of the categories below.

**Non-STE vs STE.** "Use the thing to call the function that gets data from the database." → "Use the `fetchUser` method of the `UserRepository` to retrieve a `User` record from the `PostgreSQL` database." (`fetchUser`, `UserRepository`, `User`, `PostgreSQL` are technical nouns — categories 1, 6, 19.)

## How Rule 1.5 fits with the other rules

- **Rule 1.1** requires an approved dictionary word for all common vocabulary. Use an approved word whenever one exists.
- **Rule 1.5** is the complement: it permits a word outside the dictionary when it names a technical concept.
- **Rule 1.6** forbids any non-approved word unless it is a technical noun (classified in a category below) or part of one.
- Together, 1.1 + 1.5 + 1.6 form the gate: a word is allowed if it is approved (1.1) OR a classified code-domain technical noun (1.5); otherwise 1.6 forbids it.

**Glossary registration (required).** Before you use a code-domain technical noun, add it to the project glossary with: the noun term; the STE-Code category (or categories) it belongs to; the approved meaning in the project context; and an example sentence that uses it correctly.

---

## The 19 code-domain technical noun categories

### Category 1 — API and library components
Terms that refer to all API and library components. For example, technical nouns in API reference docs, SDK manifests, or interface definition files.
`endpoint, method, parameter, query parameter, path parameter, request body, response body, header, status code, module, class, interface, type alias, enum, constant, decorator, middleware, route handler, serializer, DTO, model, schema, callback, hook, plugin`

Non-STE: "Call the thing that makes users."
STE: "Call the `POST /api/v1/users` endpoint with a `CreateUserRequest` body to create a `User` resource."

### Category 2 — Applications, services, and subsystems
Terms that refer to all types of applications, services, and their subsystems, and the locations that are part of these units.
`web application, mobile app, desktop client, CLI tool, microservice, monolith, API gateway, load balancer, database server, message broker, cache layer, container, pod, cluster, frontend, backend, admin panel, user dashboard, authentication service, payment service, notification service, search engine, CDN, reverse proxy, serverless function, cron job, worker process`

Non-STE: "The thing that runs the website broke."
STE: "The `nginx` reverse proxy on the `web-01` frontend server stopped responding."

### Category 3 — Development tools and support equipment
Terms that refer to all types of development tools, SDKs, and their components, and locations that are part of these items.
`IDE, code editor, terminal emulator, compiler, interpreter, transpiler, bundler, linter, formatter, debugger, profiler, package manager, version control system, CI runner, test framework, assertion library, mocking library, static analyzer, API client, database client, container runtime, orchestration tool, IaC tool, monitoring dashboard, log aggregator, feature flag service, secrets manager`

Non-STE: "Run the check tool to find problems."
STE: "Run `ESLint` with the `@company/eslint-config` preset to find lint violations."

### Category 4 — Dependencies, packages, and technical debt
Terms that refer to dependencies, packages, and technical debt that can cause regressions or malfunctions.
`dependency, transitive dependency, package, library, framework, runtime, polyfill, shim, vendor bundle, dead code, deprecated API, legacy module, orphaned code, code smell, TODO comment, FIXME comment, zombie import, circular dependency, peer dependency, dev dependency, optional dependency, pinned version, lockfile, SBOM, supply chain artifact, third-party script, ad-hoc patch, monkey-patch, workaround code`

Non-STE: "There's a problem with one of the things we installed."
STE: "The `lodash@4.17.20` transitive dependency introduces a prototype pollution vulnerability (CVE-2020-8203)."

### Category 5 — Hosting, CI/CD, and deployment infrastructure
Terms that refer to the management, structure, and operations of hosting, CI/CD, and deployment infrastructure.
`cloud provider, region, availability zone, data center, Kubernetes cluster, namespace, Docker registry, artifact repository, build pipeline, deployment pipeline, staging environment, production environment, sandbox environment, on-premise server, virtual machine, bare-metal host, edge location, CDN endpoint, storage bucket, message queue, event bus, API gateway endpoint, load balancer target group, auto-scaling group, service mesh, ingress controller`

Non-STE: "Deploy to the cloud place."
STE: "Deploy the `orders-service` container image to the `us-east-1` `production` Kubernetes cluster in namespace `orders`."

### Category 6 — Systems, subsystems, and architectural components
Terms that refer to the structure, operation, composition, and system design of software.
`architecture, design pattern, layered architecture, hexagonal architecture, microservice, event-driven architecture, CQRS, event sourcing, pub/sub, message queue, event bus, database shard, read replica, write-ahead log, connection pool, circuit breaker, retry policy, rate limiter, cache layer, CDN edge, feature flag, A/B test variant, canary deployment, blue-green deployment, rolling update, service registry, configuration provider, secret store, reverse proxy, API gateway route, middleware chain, plugin system, dependency injection container, ORM, migration runner`

Non-STE: "The system uses a pattern to handle failures gracefully."
STE: "The `PaymentGateway` client uses a `CircuitBreaker` pattern — after 5 consecutive failures, it opens and returns cached fallback responses for 30 seconds."

### Category 7 — Mathematical, algorithmic, and scientific terms
Terms that refer to algorithms, data structures, computational concepts, and methodologies.
`algorithm, data structure, Big-O notation, time complexity, space complexity, hash table, binary tree, linked list, graph, trie, bloom filter, LRU cache, consistent hashing, recursion, memoization, dynamic programming, greedy algorithm, backtracking, binary search, quicksort, mergesort, topological sort, Dijkstra, BFS, DFS, A*, Paxos, Raft, two-phase commit, saga pattern, idempotency key, eventual consistency, CAP theorem, ACID, BASE, vector clock, Lamport timestamp, Merkle tree, consistent hashing ring, shard key, partition key, compound index, covering index, query plan, cardinality, selectivity, normalization, denormalization, OLTP, OLAP, ETL, stream processing, batch processing, map-reduce, actor model, CSP, semaphore, mutex, atomic operation, CAS`, `O(n log n)`, `f(x) = x² + 3x - 2`

Non-STE: "The search is fast because it uses a good algorithm."
STE: "The `SearchIndex` uses a `BloomFilter` (`O(k)` lookup) to skip negative lookups before falling back to a `B-Tree` index scan."

### Category 8 — Codebase navigation and project structure
Terms that refer to codebase navigation, project structure, and directory/import hierarchy.
`directory, subdirectory, file path, import path, package root, module root, workspace root, monorepo root, source directory, test directory, build output, entry point, barrel export, index file, re-export, absolute import, relative import, path alias, symlink, Git root, branch, tag, commit, HEAD, upstream, origin, fork, submodule, subtree, vendor directory, node_modules, virtual environment, GOPATH, classpath, namespace, package scope, module scope, public API surface, internal package, private module, exported symbol`

Non-STE: "The file is in the utils folder somewhere."
STE: "The `formatCurrency` helper is in `src/shared/utils/formatting.ts`, re-exported from the barrel file at `src/shared/utils/index.ts`."

### Category 9 — Numbers, units of measurement, and time
Terms that refer to metrics, benchmarks, timing data, and quantitative measurements.
`latency, throughput, response time, p50, p95, p99, p999, ops/sec, req/sec, RPM, RPS, QPS, TPS, bytes, KB, MB, GB, TB, KiB, MiB, ms, µs, ns, s, min, hr, CPU core, thread count, memory usage, heap size, stack size, GC pause, cold start time, warm start time, bootstrap time, build time, deploy time, MTTR, MTBF, uptime, downtime, error rate, success rate, availability (99.9%, 99.99%), RPO, RTO, SLO, SLI, SLA, concurrency, connection count, pool size, batch size, page size, offset, limit, TTL, timeout, interval, poll interval, retry delay, backoff multiplier, rate limit (tokens/sec), quota, sample rate, cardinality`

Non-STE: "The API is pretty fast most of the time."
STE: "The `GET /search` endpoint has a p95 latency of 120 ms and a p99 latency of 350 ms at 5000 RPM."

### Category 10 — Quoted text
Terms that refer to texts that you cannot change in code documentation. For example, quoted error messages, log output, API responses, UI string literals, and command-line output.
`error message, stack trace, log line, HTTP response body, JSON payload, XML response, environment variable value, CLI flag, command option, shell command output, status code text, exception message, assertion message, deprecation warning, compiler diagnostic, linter rule ID, test failure message, benchmark output, profiler report, API route pattern, SQL query string, GraphQL query, regex pattern, glob pattern, cron expression, semantic version string, git commit hash, UUID string, JWT token (example)`, `"Connection refused"`, `"404 Not Found"`, `"TypeError: Cannot read properties of undefined"`, `"--config=./prod.yaml"`, `"npm ERR! code ERESOLVE"`

Non-STE: "If you get an error about the database, restart it."
STE: "If the application logs `\"FATAL: sorry, too many clients already\"` from `PostgreSQL`, restart the `pgbouncer` connection pooler."
