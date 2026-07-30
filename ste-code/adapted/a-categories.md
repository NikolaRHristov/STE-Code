# STE-Code Adaptation - Technical Noun Categories

> **Source:** ASD-STE100 Issue 9, Rule 1.5, Pages 49-52 (lines 1698-1878 of master.md)
> **Adaptation:** Aerospace → Code Documentation Domain
> **Categories:** 22 (not 19 - Issue 9 added categories 21 and 22)
> **Generated:** 2026-07-30

---

## Rule 1.5 - Framework

### Original (master.md line 1698-1709)

**Rule 1.5** You can use words that you can include in a technical noun category.

A technical noun is a noun term that refers to a specified concept and is applicable to a subject field.
The dictionary does not include technical nouns because there are too many, and each subject field uses different technical nouns for their texts.
You can find many of these technical nouns in your company glossary or terminology database.
STE gives you a list of categories, with examples, to help you:
- Select technical nouns to put in your company glossary or terminology database.
- Use technical nouns correctly.
You can use technical nouns in procedural and descriptive writing if you can include them in one or more of these twenty-two categories.

### Adapted (Code Documentation Domain)

**Rule 1.5** You can use terms that you can include in a technical noun category for code documentation.

A technical noun in code documentation is a noun term that refers to a specified software concept and is applicable to a given codebase, library, or system.
The standard library of approved terms does not include project-specific technical nouns because each codebase, framework, and ecosystem uses different terminology.
You can find many of these technical nouns in your project glossary, API reference, or architecture decision records (ADRs).
This adaptation gives you a list of categories, with examples, to help you:
- Select technical nouns to put in your project glossary or terminology database.
- Use technical nouns correctly in API documentation, commit messages, README files, code comments, and technical specifications.
You can use technical nouns in procedural and descriptive code documentation if you can include them in one or more of these twenty-two categories.

### STE / Non-STE Example Pair

| Non-STE | STE |
|---------|-----|
| Use the thing to call the function that gets data from the database. | Use the `fetchUser` method of the `UserRepository` to retrieve a `User` record from the `PostgreSQL` database. |
| *("thing", "gets data" - no technical nouns; ambiguous)* | *(`fetchUser`, `UserRepository`, `User`, `PostgreSQL` - all classified technical nouns, categories 1, 6, 19)* |

---

## Category 1 - Official Parts Information

### Original (master.md line 1710-1714)
Terms that refer to all design items. For example, technical nouns included in illustrated parts catalogs or engineering drawings.
*bolt, cable, clip, conductor, contact, engine, ferry tank, filter, hatch, hazard lights, indicator, light, logo, oil seal, prelubricated seal, pipe, propeller, retractor link, screw, switch, transceiver*

### Adapted (Code Documentation)
Terms that refer to all API and library components. For example, technical nouns included in API reference documentation, SDK manifests, or interface definition files.
*endpoint, method, parameter, query parameter, path parameter, request body, response body, header, status code, module, class, interface, type alias, enum, constant, decorator, middleware, route handler, serializer, DTO, model, schema, callback, hook, plugin*

### STE / Non-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Call the thing that makes users. | Call the `POST /api/v1/users` endpoint with a `CreateUserRequest` body to create a `User` resource. |
| The thing you get back has the ID and name. | The `UserResponse` DTO contains the `id` (UUID) and `displayName` (string) fields. |
| Pass the options object to configure the behavior. | Pass a `RetryPolicy` enum value to the `maxRetries` parameter of the `fetchWithRetry` function. |

---

## Category 2 - Vehicles or Machines, and Locations on Them

### Original (master.md line 1715-1720)
Terms that refer to all types of vehicles and machines, and the locations that are part of these units.
*aircraft, aircraft carrier, airframe, airplane, bicycle, cabin, car, cargo compartment, cargo hold, cockpit, deck, engine room, fuselage, helicopter, galley, lifeboat, overhead panel, ship, submarine, tank, train, truck, wing, wing root*

### Adapted (Code Documentation)
Terms that refer to all types of applications, services, and their subsystems, and the locations that are part of these units.
*web application, mobile app, desktop client, CLI tool, microservice, monolith, API gateway, load balancer, database server, message broker, cache layer, container, pod, cluster, frontend, backend, admin panel, user dashboard, authentication service, payment service, notification service, search engine, CDN, reverse proxy, serverless function, cron job, worker process*

### STE / Non-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The thing that runs the website broke. | The `nginx` reverse proxy on the `web-01` frontend server stopped responding. |
| Log into the admin area. | Log into the `AdminPanel` at `https://admin.example.com`. |
| The background job processor handles emails. | The `EmailWorker` process in the `worker` pod handles outbound email delivery. |

---

## Category 3 - Tools and Support Equipment, Their Parts, and Locations on Them

### Original (master.md line 1727-1732)
Terms that refer to all types of tools, support equipment, their parts, and locations that are part of these items.
*access ladder, blade, brush, cap, chock, clamp, cover, display, drill, file, gauge (gage), graduated beaker, handle, jack, label, rigging pin, roller, rope, rung, shaft, stand, tag, test rig, torque wrench, trestle*

### Adapted (Code Documentation)
Terms that refer to all types of development tools, SDKs, and their components, and locations that are part of these items.
*IDE, code editor, terminal emulator, compiler, interpreter, transpiler, bundler, linter, formatter, debugger, profiler, package manager, version control system, CI runner, test framework, assertion library, mocking library, static analyzer, API client, database client, container runtime, orchestration tool, IaC tool, monitoring dashboard, log aggregator, feature flag service, secrets manager*

### STE / Non-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Run the check tool to find problems. | Run `ESLint` with the `@company/eslint-config` preset to find lint violations. |
| Use the test thing to verify the code. | Use the `Jest` test framework with `@testing-library/react` to verify component behavior. |
| The build tool makes the final files. | The `Webpack` bundler, configured via `webpack.config.js`, produces the production bundle in `dist/`. |

---

## Category 4 - Materials, Consumables, and Unwanted Material

### Original (master.md line 1733-1739)
Terms that refer to materials, consumable items, and other substances that can cause contamination or malfunctions.
*acid, adhesive, aluminum alloy, ammunition, compound, copper, debris, detergent, dirt, disinfectant, dust, foam, foreign object, fuel, grease, hazardous substances, hazardous waste, metal, metallic coating, oil, paint, penetrant spray, plastic, primer, sealant, sealing, soap, stainless steel, tape, waste, water, wire*

### Adapted (Code Documentation)
Terms that refer to dependencies, packages, and technical debt that can cause regressions or malfunctions.
*dependency, transitive dependency, package, library, framework, runtime, polyfill, shim, vendor bundle, dead code, deprecated API, legacy module, orphaned code, code smell, TODO comment, FIXME comment, zombie import, circular dependency, peer dependency, dev dependency, optional dependency, pinned version, lockfile, SBOM, supply chain artifact, third-party script, ad-hoc patch, monkey-patch, workaround code*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Watch out for old stuff that nobody uses anymore. | Remove the deprecated `UserService.legacyCreate()` method - it is dead code with zero callers as of v3.2. |
| There's a problem with one of the things we installed. | The `lodash@4.17.20` transitive dependency introduces a prototype pollution vulnerability (CVE-2020-8203). |
| Don't use the thing from the old library. | Replace the deprecated `moment` package with the `date-fns` library in the `OrderTimeline` component. |

---

## Category 5 - Facilities, Infrastructure, and Logistic Procedures

### Original (master.md line 1740-1745)
Terms that refer to the management, structure, and operations of physical facilities, infrastructure systems, and logistic procedures. For example, areas for utility systems, transportation networks, storage, distribution processes, and operational logistic workflows.
*airport, apron, base, building, camp, dock, engine shop floor, flight simulator, gate, handling, hangar, packaging, packing, port, service bay, shipping, shop, store, storage, transport*

### Adapted (Code Documentation)
Terms that refer to the management, structure, and operations of hosting, CI/CD, and deployment infrastructure. For example, areas for cloud providers, container registries, deployment pipelines, and operational workflows.
*cloud provider, region, availability zone, data center, Kubernetes cluster, namespace, Docker registry, artifact repository, build pipeline, deployment pipeline, staging environment, production environment, sandbox environment, on-premise server, virtual machine, bare-metal host, edge location, CDN endpoint, storage bucket, message queue, event bus, API gateway endpoint, load balancer target group, auto-scaling group, service mesh, ingress controller*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Deploy to the cloud place. | Deploy the `orders-service` container image to the `us-east-1` `production` Kubernetes cluster in namespace `orders`. |
| The pipeline builds and ships the code. | The `deploy-prod` GitHub Actions workflow builds the Docker image, pushes it to `ECR`, and applies the `kustomize` overlay for `production`. |
| Store the files somewhere safe. | Upload build artifacts to the `releases` S3 bucket (`s3://company-releases/production/`). |

---

## Category 6 - Systems, Components and Circuits, Their Functions, Configurations, and Parts

### Original (master.md line 1746-1750)
Terms that refer to the structure, operation, composition, and system design.
*air conditioning, amplifying circuit, armament, audio, aural warning system, collapsed position, exhaust, flight management, hardware, inhibiting signal, injection, inlet, input frequency, latch, pedal, power unit, pump, reverse mode, reverse position, standby mode, upright position, vent*

### Adapted (Code Documentation)
Terms that refer to the structure, operation, composition, and system design of software.
*architecture, design pattern, layered architecture, hexagonal architecture, microservice, event-driven architecture, CQRS, event sourcing, pub/sub, message queue, event bus, database shard, read replica, write-ahead log, connection pool, circuit breaker, retry policy, rate limiter, cache layer, CDN edge, feature flag, A/B test variant, canary deployment, blue-green deployment, rolling update, service registry, configuration provider, secret store, reverse proxy, API gateway route, middleware chain, plugin system, dependency injection container, ORM, migration runner*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The system uses a pattern to handle failures gracefully. | The `PaymentGateway` client uses a `CircuitBreaker` pattern - after 5 consecutive failures, it opens and returns cached fallback responses for 30 seconds. |
| Data flows through a bunch of steps before it gets saved. | A `CreateOrder` command flows through the `OrderAggregate` (CQRS write model), which emits an `OrderPlaced` event to the `EventBus`, triggering the `OrderProjection` to update the read model in the `orders_read` PostgreSQL shard. |
| The config changes depending on where it's running. | The `FeatureFlags` service resolves the `enable_new_checkout` flag from `LaunchDarkly` based on the `X-Environment` header (`staging` vs `production`). |

---

## Category 7 - Mathematical, Scientific, Engineering Terms, and Formulas

### Original (master.md line 1751-1763)
Terms that refer to concepts, design, calculations, or methodologies.
*acceleration, allowance, astronomy, atom, average, biochemistry, biology, biome, burr, capacitance, carbon, category, cavitation, center, circle, coefficient, combination, configuration, conversion, count, critical temperature, curve, cycle, defect, degree, deceleration, density, diameter, displacement, duty cycle, elapsed time, electricity, energy, exponent, ferry flight, flutter, force, fumes, genetics, geology, geophysics, graph, gravity, hardness, heat treatment, idle speed, ignition, inhibition, instrumentation, interference, issue, light, line replaceable unit, load, loss, measurement, modification, momentum, motoring, overhaul, oversized hole, oxygen, performance, phase, polarity, power, pressure, process, radius, rating, ratio, reduction, relative angular position, resistance, scan, shutdown, signal, specific gravity, stall, standard, steam, stiffness, strength, suction, temperature, tension, thread, tightness, torque, toxic property, vapor, voltage, water vapor, "C = (A - B) - 0.063 mm"*

### Adapted (Code Documentation)
Terms that refer to algorithms, data structures, computational concepts, and methodologies.
*algorithm, data structure, Big-O notation, time complexity, space complexity, hash table, binary tree, linked list, graph, trie, bloom filter, LRU cache, consistent hashing, recursion, memoization, dynamic programming, greedy algorithm, backtracking, binary search, quicksort, mergesort, topological sort, Dijkstra, BFS, DFS, A*, Paxos, Raft, two-phase commit, saga pattern, idempotency key, eventual consistency, CAP theorem, ACID, BASE, vector clock, Lamport timestamp, Merkle tree, consistent hashing ring, shard key, partition key, compound index, covering index, query plan, cardinality, selectivity, normalization, denormalization, OLTP, OLAP, ETL, stream processing, batch processing, map-reduce, actor model, CSP, semaphore, mutex, atomic operation, CAS*, `O(n log n)`, `f(x) = x² + 3x - 2`

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The search is fast because it uses a good algorithm. | The `SearchIndex` uses a `BloomFilter` (`O(k)` lookup, where `k` is the number of hash functions) to skip negative lookups before falling back to a `B-Tree` index scan. |
| The function remembers results so it doesn't recompute. | `computeShippingCost(addressHash)` is memoized with an `LRU Cache` (capacity 1024, `O(1)` eviction) to avoid redundant API calls. |
| The database query got slow because of how the data is laid out. | The `orders` table has low cardinality on the `status` column - the query planner defaults to a sequential scan. A composite index on `(customer_id, status, created_at DESC)` reduces the query from `O(n)` to `O(log n)`. |

---

## Category 8 - Navigation and Geographic Terms

### Original (master.md line 1764-1769)
Terms that refer to positions, directions, or locations related to mapping, routing, or spatial orientation.
*air, altitude, attitude, axis, bank, clearance, climb, coordinates, critical approach, datum, delay, deviation, drag, east, France, glideslope, gradient, heading, landing, leeway, Lima, north, pitch, roll, skid, south, west*

### Adapted (Code Documentation)
Terms that refer to codebase navigation, project structure, and directory/import hierarchy.
*directory, subdirectory, file path, import path, package root, module root, workspace root, monorepo root, source directory, test directory, build output, entry point, barrel export, index file, re-export, absolute import, relative import, path alias, symlink, Git root, branch, tag, commit, HEAD, upstream, origin, fork, submodule, subtree, vendor directory, node_modules, virtual environment, GOPATH, GOPATH, classpath, namespace, package scope, module scope, public API surface, internal package, private module, exported symbol*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The file is in the utils folder somewhere. | The `formatCurrency` helper is in `src/shared/utils/formatting.ts`, re-exported from the barrel file at `src/shared/utils/index.ts`. |
| Import the thing from the parent directory. | Import `UserService` using the path alias `@services/UserService` (resolves to `src/services/UserService.ts` via `tsconfig.json` `paths`). |
| Go to the branch where the fix was made. | Check out the `hotfix/payment-timeout` branch from `origin` (forked from `main` at commit `a3f8b2c`). |

---

## Category 9 - Numbers, Units of Measurement and Time (and Their Symbols)

### Original (master.md line 1776-1780)
Terms that refer to quantitative data, measurements, or time-related information.
*92, 303, ampere (A), degree (°), first (1st), half (½), hour (h), kilogram (kg), knot, liter (L or l), meter (m), mile, minute ('), month, ohm (Ω), one, one-quarter (¼), second ("), second (s), second (2nd), square inch (sq.in.), spring, third (3rd), three, year, winter, zero*

### Adapted (Code Documentation)
Terms that refer to metrics, benchmarks, timing data, and quantitative measurements.
*latency, throughput, response time, p50, p95, p99, p999, ops/sec, req/sec, RPM, RPS, QPS, TPS, bytes, KB, MB, GB, TB, KiB, MiB, ms, µs, ns, s, min, hr, CPU core, thread count, memory usage, heap size, stack size, GC pause, cold start time, warm start time, bootstrap time, build time, deploy time, MTTR, MTBF, uptime, downtime, error rate, success rate, availability (99.9%, 99.99%), RPO, RTO, SLO, SLI, SLA, concurrency, connection count, pool size, batch size, page size, offset, limit, TTL, timeout, interval, poll interval, retry delay, backoff multiplier, rate limit (tokens/sec), quota, sample rate, cardinality*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The API is pretty fast most of the time. | The `GET /search` endpoint has a p95 latency of 120 ms and a p99 latency of 350 ms at 5000 RPM (requests per minute). |
| Give it time to try again if it fails. | Configure the `RetryPolicy` with a `baseDelay` of 200 ms, a `maxDelay` of 5 s, and an exponential backoff multiplier of 2.0 (max 3 retries). |
| The database can handle a lot of connections. | The `pgbouncer` connection pool is configured with a `pool_size` of 25 per `PostgreSQL` read replica - sustained at 800 TPS with <1% error rate. |

---

## Category 10 - Quoted Text

### Original (master.md line 1781-1786)
Terms that refer to texts that you cannot change in technical writing. For example, texts on placards, labels, signs, markings, and display units.
*abort button, EXIT sign, INOP system, OXYGEN pushbutton switch, ON position, NEXT button, FAULT legend, NO STEP marking, FASTEN SAFETY BELT sign, WEAR PROTECTIVE CLOTHING sign*

### Adapted (Code Documentation)
Terms that refer to texts that you cannot change in code documentation. For example, quoted error messages, log output, API responses, UI string literals, and command-line output.
*error message, stack trace, log line, HTTP response body, JSON payload, XML response, environment variable value, CLI flag, command option, shell command output, status code text, exception message, assertion message, deprecation warning, compiler diagnostic, linter rule ID, test failure message, benchmark output, profiler report, API route pattern, SQL query string, GraphQL query, regex pattern, glob pattern, cron expression, semantic version string, git commit hash, UUID string, JWT token (example), `"Connection refused"`, `"404 Not Found"`, `"TypeError: Cannot read properties of undefined"`, `"--config=./prod.yaml"`, `"npm ERR! code ERESOLVE"`*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| If you get an error about the database, restart it. | If the application logs `"FATAL: sorry, too many clients already"` from `PostgreSQL`, restart the `pgbouncer` connection pooler. |
| The output shows something went wrong. | The `curl` command returns `{"error": "invalid_grant", "error_description": "Refresh token has expired"}` with HTTP status `400`. |
| Run the command with the flag that skips tests. | Run `./gradlew build -x test` (the `-x` flag excludes the `test` Gradle task from the build lifecycle). |

---

## Category 11 - Professional Roles, Individuals, Groups, Organizations, and Geopolitical Entities

### Original (master.md line 1787-1793)
Terms that refer to professional functions, names of persons, organizations, companies, teams, sovereign states, or entities related to processes, responsibilities, or decision-making.
*air traffic control, British Broadcasting Corporation (BBC), captain, commander, copilot, crew, crew chief, European Aviation Safety Agency (EASA), Federal Aviation Administration (FAA), John Kirkman, manufacturer, operator, Transport Canada Civil Aviation (TCCA), United States of America (USA)*

### Adapted (Code Documentation)
Terms that refer to project roles, contributors, teams, organizations, and entities related to processes, responsibilities, or decision-making.
*maintainer, author, contributor, reviewer, approver, code owner, release manager, on-call engineer, SRE, DevOps engineer, security champion, triage team, core team, steering committee, technical lead, staff engineer, principal engineer, intern, vendor, client, stakeholder, end user, GitHub organization, npm organization, Docker Hub organization, CNCF, Apache Software Foundation, Linux Foundation, Mozilla, Google, Microsoft, OpenAPI Initiative, ECMA, ISO, W3C, IETF, OWASP, `CODEOWNERS` file, `@backend-team`, `@security-reviewers`*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Ask the person in charge to look at the PR. | Request a review from `@frontend-core` (the code owners for `src/components/`, per `.github/CODEOWNERS`). |
| The people who take care of the servers fixed it. | The SRE team (`@sre-oncall` in Slack channel `#incidents`) resolved the production outage - see postmortem `INC-2024-042`. |
| Follow the rules from the standards group. | Follow the `OpenAPI 3.1.0` specification (maintained by the OpenAPI Initiative under the Linux Foundation) for REST API documentation. |

---

## Category 12 - Parts of the Body

### Original (master.md line 1794-1798)
Terms that refer to anatomical features or functions related to medical, biological, or ergonomic contexts.
*blood, digestive system, ear, eyes, hair, hand, head, lung, mouth, respiratory tract, skin, stomach*

### Adapted (Code Documentation)
Terms that refer to user interface elements, interaction points, and accessibility features of software.
*button, text input, checkbox, radio button, dropdown, select menu, toggle, slider, modal, dialog, tooltip, popover, toast, snackbar, banner, tab, accordion, breadcrumb, pagination, carousel, card, table, data grid, form, form field, label, placeholder, icon, avatar, badge, spinner, progress bar, skeleton loader, navbar, sidebar, footer, header, search bar, filter panel, drawer, split pane, context menu, keyboard shortcut, hotkey, focus trap, skip link, screen reader label, ARIA role, ARIA attribute, landmark region, heading hierarchy*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Click the thing that opens the side menu. | Click the `hamburger` icon in the `Navbar` component to open the `Sidebar` drawer (ARIA role `navigation`, label "Main menu"). |
| The popup shows an error if the field is empty. | The `Toast` component (variant `error`, duration 5000 ms) displays "Email is required" when the `EmailInput` form field loses focus with an empty value. |
| Use the keyboard thing to close the window. | Press `Escape` to close the `Modal` dialog - the `useFocusTrap` hook returns focus to the trigger `Button` that opened it. |

---

## Category 13 - Common Personal Effects, Food, and Beverages

### Original (master.md line 1799-1802)
Terms that refer to everyday personal items and types of food and beverage.
*beans, bread, cigarette lighter, clothing, coffee, flour, footwear, high-heeled shoes, jewelry, lipstick, matches, milk, mineral water, nail scissors, perfume, pizza, shampoo, wine*

### Adapted (Code Documentation)
Terms that refer to user data, preferences, session state, and personalization artifacts.
*user profile, display name, avatar URL, email address, phone number, billing address, shipping address, payment method, credit card, subscription plan, usage quota, rate limit bucket, API key, access token, refresh token, ID token, session cookie, CSRF token, user preference, theme setting, language locale, timezone, notification setting, opt-in flag, consent record, bookmark, watchlist, shopping cart, wishlist, search history, recently viewed, draft content, clipboard data, localStorage key, IndexedDB store, browser fingerprint, device ID, push notification token*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Save the user's stuff so it's there next time. | Persist the user's `uiPreferences` (theme: `"dark"`, locale: `"en-GB"`, timezone: `"Europe/London"`) to `localStorage` under key `user_prefs_v2`. |
| The thing that keeps them logged in expires after a while. | The `refreshToken` (stored in an `httpOnly` cookie with `SameSite=Strict`) expires after 7 days of inactivity - the `AuthProvider` silently renews it via `POST /auth/refresh`. |
| Don't let them use more than they're allowed. | The `rateLimiter` middleware enforces the `APIKey` quota: 1000 requests per hour for the `"free"` subscription plan, 10000 for `"pro"`. |

---

## Category 14 - Medical Terms

### Original (master.md line 1803-1807)
Terms that refer to medical conditions, procedures, or anatomical structures.
*allergy, aspirin, asthma, blood poisoning, breathing, circulation, dermatitis, diabetes, dizziness, female, hallucination, headache, heart rate, irritation, male, medication, nausea, pneumonia, pregnancy, pulse, skin irritation, virus*

### Adapted (Code Documentation)
Terms that refer to system health, diagnostics, observability, and failure modes.
*health check, liveness probe, readiness probe, startup probe, heartbeat, ping, metric, trace, span, log level, structured log, correlation ID, trace ID, span ID, alert, incident, SLO, SLI, error budget, burn rate, on-call rotation, escalation policy, runbook, playbook, postmortem, root cause analysis (RCA), mean time to recovery (MTTR), mean time to detection (MTTD), anomaly detection, threshold breach, saturation, latency tail, error spike, traffic drop, resource exhaustion, memory pressure, disk pressure, CPU throttling, GC thrashing, connection storm, thundering herd, cascading failure, split-brain, partition, degraded state, brownout, blackout*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The service is kind of broken right now. | The `payments-service` `readinessProbe` is failing - `/healthz` returns HTTP 503. The service is in a `degraded` state and has been removed from the load balancer target group. |
| Set up monitoring so you know when things go wrong. | Configure a `Prometheus` alert: `histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 2` triggers a `PagerDuty` incident with severity `SEV2` if the p99 latency exceeds 2 seconds for 5 minutes. |
| The database is slow because too many things are asking for the same data. | The `thundering herd` problem on `GET /products/featured` caused 2000 concurrent cache misses - the `singleflight` pattern coalesces duplicate requests into one database query. |

---

## Category 15 - Official Documents, Parts of Documentation, Standards, and Guidelines

### Original (master.md line 1808-1820)
Terms that refer to different types of official documents and their structural parts. For example, manuals, technical records, standards, specifications, and regulations requirements.
*Acceptance Test, Activation/Deactivation, Allowable Damage, attention, caution, chapter, Checklist, Class, Cleaning, Compass Correction Card, danger, data module, Description and Operation, diagram, engine logbook, Federal Aviation Regulations, Fault Isolation, figure, flowchart, font, Functional Test, Ice and Rain Protection, Inspection/Check, issue, language policy, letter, maintenance planning, maintenance practice, maintenance records, Normal Braking, note, notice, packaging, page, paragraph, parentheses, post-flight report, post-mod, pre-mod, prerequisite, preservation, reference, Removal/Installation, Required Conditions, Repair Scheme, recommendation, revision, section, Service Bulletin, Standard Practices Manual, storage, Structural Repair Manual, table, test procedure, training material, Transportation, valid welding certificate, warning*

### Adapted (Code Documentation)
Terms that refer to different types of documentation, standards, specifications, and their structural parts in software projects.
*README, CHANGELOG, CONTRIBUTING, LICENSE, CODE_OF_CONDUCT, SECURITY, GOVERNANCE, ARCHITECTURE, ADR (Architecture Decision Record), RFC (Request for Comments), API reference, OpenAPI spec, GraphQL schema, AsyncAPI spec, style guide, coding standard, linting rules, PR template, issue template, discussion template, release notes, migration guide, upgrade guide, getting started guide, quickstart, tutorial, how-to guide, explanation, reference, concept document, FAQ, glossary, onboarding guide, runbook, playbook, incident report, postmortem, design doc, technical spec, product requirements document (PRD), test plan, test case, acceptance criteria, Definition of Done, Definition of Ready, service level agreement (SLA), terms of service (TOS), privacy policy, cookie policy, data processing agreement (DPA), semantic versioning (SemVer), conventional commits, Git commit message format, doc comment, TSDoc, JSDoc, godoc, docstring, annotation, attribute, decorator doc, heading, subheading, section, subsection, paragraph, code block, table, list, admonition (note, warning, tip, danger, caution, important), hyperlink, cross-reference, footnote, bibliography, index, glossary entry, TOC (table of contents)*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| There's a doc that explains how to set things up. | Follow the `GETTING_STARTED.md` guide in the repository root - it covers prerequisites (Node.js ≥ 18, PostgreSQL 15), environment setup, and the `npm run dev` bootstrap command. |
| Write down why you made that architectural choice. | Record this decision in an ADR (`docs/adr/0014-use-event-sourcing-for-orders.md`). The `ADR` template includes Context, Decision, Consequences, and Alternatives Considered sections. |
| Put a warning in the docs about the dangerous API. | Add a `:::caution` admonition in the `Orders API` reference: "The `DELETE /api/v1/orders/{id}` endpoint is irreversible. Use `POST /api/v1/orders/{id}/cancel` to soft-cancel an order instead." |

---

## Category 16 - Environmental and Operational Conditions

### Original (master.md line 1827-1831)
Terms that refer to external factors and operating parameters that are related to systems or processes.
*atmosphere, cloud, day, daylight, ice, hail, humidity, lightning, moisture, night, rain, relative humidity, sand, snow, storm, turbulence, volcanic ash, wind*

### Adapted (Code Documentation)
Terms that refer to runtime environments, execution contexts, and operating parameters that affect software behavior.
*production, staging, development, testing, CI, localhost, operating system, OS version, kernel version, distribution, CPU architecture (x86_64, arm64), Node.js version, Python version, Java version, Go version, browser, browser version, rendering engine, screen resolution, viewport size, device type, network condition (offline, slow 3G, 4G, WiFi), Docker image, container runtime, Kubernetes version, cloud region, availability zone, environment variable, build flag, feature flag state, A/B test bucket, configuration profile, Spring profile, Rails environment, NODE_ENV, DEBUG mode, verbose logging, trace level, read-only mode, maintenance mode, degraded mode, dark mode, high contrast mode, reduced motion, forced colors, RTL locale, daylight saving time transition, leap second, timezone offset*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The bug only happens on some computers. | The `TextRenderer` crash only reproduces on `macOS 14.5` (arm64) with `Node.js 20.11.0` - the `canvas` native addon fails to load the prebuilt binary for `darwin-arm64`. |
| It works differently on the live site. | In `production` (`NODE_ENV=production`), the `React` error boundary renders a generic fallback UI. In `development`, it displays the full component stack trace via `react-error-overlay`. |
| Change the settings when you're testing the new version. | Set the `ENABLE_NEW_CHECKOUT=true` feature flag and `X-AB-Bucket=variant-b` header to test the redesigned checkout flow in the `staging` environment. |

---

## Category 17 - Colors

### Original (master.md line 1832-1838)
Terms that refer to colors that identify color-related properties, or show color attributes in different contexts.
*beige, black, cyan blue, dark brown, gray, green, magenta, light green, orange, red, white, yellow*
Colors are adjectives, but STE identifies them as technical nouns. Comparative and superlative forms of colors (for example, blacker, the reddest) are not permitted in STE.

### Adapted (Code Documentation)
Terms that refer to colors and theme tokens used to identify color-related properties in UI documentation and design system specs.
*primary, secondary, accent, success, warning, error, info, neutral, background, surface, text, border, divider, shadow, overlay, red, green, blue, yellow, orange, purple, pink, teal, cyan, gray, black, white, transparent, hex code (`#FF5733`, `#1A1A2E`), RGB (`rgb(255, 87, 51)`), RGBA (`rgba(26, 26, 46, 0.8)`), HSL (`hsl(12, 100%, 60%)`), CSS custom property (`--color-primary-500`, `--color-text-on-primary`), design token, color ramp, color scale (50-900), light mode, dark mode, high contrast mode, color blindness safe palette, WCAG contrast ratio, semantic color, Brand Color*
Colors in design systems are treated as technical nouns in documentation. Comparative forms ("darker", "lightest") are not used - instead, reference the specific design token or color ramp step.

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Make the error text reddish. | Set the `Alert` component's `variant` prop to `"error"` - this applies the `--color-semantic-error` design token (`#DC2626`). |
| Use a darker version of the main color. | Use the `--color-primary-700` design token (one step darker on the primary color ramp) instead of `--color-primary-500` for the hover state. |
| The background should be kind of white. | Set the page background to `--color-surface-page` (resolves to `#FFFFFF` in light mode, `#121212` in dark mode), ensuring a WCAG AA contrast ratio of ≥4.5:1 against body text. |

---

## Category 18 - Damage Terms

### Original (master.md line 1839-1843)
Terms that refer to types of defects or degradation and give information about malfunctions.
*buckle, chafing, corrosion, crack, crack propagation, deformation, dent, discoloration, distortion, erosion, fracture, fraying, galling, kink, nick, score, scratch, stain, spurious fault message*

### Adapted (Code Documentation)
Terms that refer to bugs, errors, exceptions, and failure modes in software.
*crash, segfault, null pointer exception, undefined is not a function, type error, reference error, syntax error, range error, stack overflow, buffer overflow, memory leak, resource leak, dangling pointer, use-after-free, double free, race condition, deadlock, livelock, starvation, priority inversion, ABA problem, torn read, torn write, dirty read, non-repeatable read, phantom read, lost update, write skew, serialization anomaly, split-brain, network partition, timeout, connection reset, DNS failure, TLS handshake failure, certificate expiry, HTTP 500, HTTP 502, HTTP 503, HTTP 504, rate limit exceeded, quota exceeded, out of memory (OOM), disk full, inode exhaustion, file descriptor exhaustion, thread pool exhaustion, connection pool exhaustion, GC thrashing, cache stampede, cache penetration, cache avalanche, hot partition, data corruption, bit rot, checksum failure, hash collision, infinite loop, infinite recursion, integer overflow, integer underflow, floating point precision error, off-by-one error, SQL injection, XSS, CSRF, prototype pollution, deserialization vulnerability, dependency confusion, supply chain attack, CVE, CWE, zero-day*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The program crashes when two things happen at the same time. | The `OrderProcessor` has a race condition: threads A and B both check `inventory[sku].quantity > 0` before either thread decrements it, causing an oversell. Fix: use `SELECT ... FOR UPDATE` to acquire a row-level lock. |
| The database query sometimes gets weird data. | Under `READ COMMITTED` isolation, the `TransferService` is vulnerable to a lost update: transaction T1 reads balance $100, T2 reads balance $100, T2 writes $80, T1 writes $70 - the $20 debit from T2 is lost. |
| There's a security hole in the old version. | The `lodash@4.17.20` transitive dependency is affected by CVE-2020-8203 (prototype pollution via `_.zipObjectDeep`). Upgrade to `lodash@4.17.21` or use `Object.create(null)` to create prototype-less objects in affected paths. |

---

## Category 19 - Computer Science, Information and Communication Technology

### Original (master.md line 1844-1852)
Terms that refer to technological concepts, systems, or components in this subject field.
*add-in, add-on, AI, arrow, artificial intelligence, authentication, backup, backup file, bookmark, chatbot, content, cursor, cybersecurity, database, deep learning, dialog check box, digitalization, digitization, e-mail, embedding, field, file, firewall, hallucination, HTML, icon, interface, internet, laptop, large language model, local operation, machine learning, memory, menu, metadata, mouse, network, operating system, phone, plug-in, pre-loaded software, preset value, prompt engineering, remote operation, screen, search engine, smartphone, status bar, store, tablet, token, toolbar, touchscreen, tweet, tuning, update, voice mail, XML*

### Adapted (Code Documentation)
Terms that refer to computer science, information and communication technology concepts used specifically in documentation about software systems.
*API, REST, GraphQL, gRPC, WebSocket, SSE, HTTP/2, HTTP/3, TCP, UDP, TLS, mTLS, OAuth 2.0, OIDC, SAML, JWT, API key, CORS, CSP, HSTS, DNS, CDN, IP, IPv4, IPv6, CIDR, VPN, VPC, subnet, firewall rule, WAF, DDoS, load balancing, reverse proxy, forward proxy, caching, compression, serialization (JSON, Protobuf, MessagePack, Avro), encoding (Base64, URL encoding), hashing (SHA-256, bcrypt, Argon2), encryption (AES-256-GCM, RSA, ECDSA), encoding (UTF-8, ASCII), Unicode, emoji, regex, glob pattern, SQL, NoSQL, ORM, migration, seed data, transaction, ACID, BASE, sharding, replication, partitioning, indexing, normalization, denormalization, message queue, pub/sub, event sourcing, CQRS, saga, distributed transaction, consensus, leader election, service discovery, circuit breaker, bulkhead, retry, backoff, idempotency, rate limiting, throttling, API versioning, semantic versioning, feature flag, canary release, blue-green deployment, rolling update, immutable infrastructure, infrastructure as code, configuration as code, GitOps, observability, telemetry, tracing, metrics, logging, profiling, APM, RUM, continuous integration, continuous delivery, continuous deployment, DevOps, DevSecOps, Git, Docker, Kubernetes, Helm, Terraform, Ansible*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The API uses token-based auth. | The `Orders API` uses OAuth 2.0 with the Authorization Code flow (PKCE). Clients obtain a JWT access token from `POST /oauth/token` and pass it in the `Authorization: Bearer <token>` header. |
| Data syncs between services using a queue. | The `OrderPlaced` event is published to the `RabbitMQ` topic exchange `orders.events`. Downstream services (`InventoryService`, `NotificationService`) consume from durable queues with manual acknowledgment and dead-letter routing for failed messages. |
| Deploy gradually so you don't break everything. | Use a canary release: deploy the new `checkout-service:v2.3.0` to 5% of pods. Monitor p95 latency and error rate for 15 minutes. If SLOs hold, roll out to 100%. If the error budget burn rate exceeds 1x, trigger an automatic rollback to `v2.2.1`. |

---

## Category 20 - Civil and Military Operations

### Original (master.md line 1853-1860)
Terms that refer to concepts and activities, service delivery, product management, and customer and life-cycle support in civil and military operations.
*armed forces, assault, bomb, bullet, checkpoint, combat plan, contractor, customer, customer support, customer service, deployment, echelon, ejection seat, end item, end user, evacuation, formation, ground zero, gun, Integrated Product Support (IPS), know-how, lifecycle, machine gun, maintenance concept, mission, obsolescence, operator, Original Equipment Manufacturer (OEM), patrol*

### Adapted (Code Documentation)
Terms that refer to DevOps operations, release management, deployment strategies, service delivery, product management, and lifecycle support in software.
*deployment, release, rollout, rollback, hotfix, patch, minor release, major release, breaking change, deprecation, end-of-life (EOL), sunset, migration, upgrade path, backward compatibility, forward compatibility, downtime, maintenance window, zero-downtime deployment, graceful shutdown, drain, scale up, scale down, scale out, scale in, autoscaling, horizontal scaling, vertical scaling, incident, outage, service disruption, failover, disaster recovery, backup, restore, point-in-time recovery, snapshot, retention policy, runbook execution, playbook, on-call handoff, escalation, war room, status page, SLA breach, SLO violation, error budget policy, change freeze, code freeze, release train, sprint, iteration, milestone, roadmap, epic, user story, bug ticket, triage, priority (P0, P1, P2, P3), severity (SEV0, SEV1, SEV2, SEV3), SL1-SL4, service level objective, operational level agreement (OLA), underpinning contract (UC), vendor management, procurement, onboarding, offboarding, access revocation, audit log, compliance check, penetration test, vulnerability scan, security patch, responsible disclosure, coordinated vulnerability disclosure (CVD)*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| We need to put the fix out ASAP. | Initiate a hotfix deployment: cherry-pick commit `fix/payment-null-pointer` onto `release/v3.2`, trigger the `deploy-hotfix` pipeline, and set the `PAYMENT_SERVICE` canary to 10% for 30 minutes before full rollout. |
| The update will require the site to be down for a bit. | The database migration from `PostgreSQL 14` to `PostgreSQL 16` requires a maintenance window (2024-08-15 02:00-04:00 UTC). During this window, the read replicas will serve stale data and write operations will return HTTP 503. |
| Figure out who broke it and how to prevent it next time. | File a blameless postmortem for INC-2024-042 (template: `docs/postmortems/INC-2024-042.md`). Identify the contributing factor (missing `NullPointerException` guard in `PaymentValidator`), the detection gap (no alert on `NullPointerException` count spike), and assign action items to `@payments-team`. |

---

## Category 21 - Law and Regulations

### Original (master.md line 1861-1867)
Terms that refer to legal and regulatory texts. For example, contracts, warranty texts, certificates, standards and specifications, and legal papers.
*action, ambiguity, appeal, arbitration, bankruptcy, communication, competence, compliance, concession, contract, court, damages, explanation, explanatory text, impeachment, jury, law, judgement, jurisdiction, purpose, recommendation, scope, serious incident, serious offense, signature, statute, term, trade, waiver, wording*

### Adapted (Code Documentation)
Terms that refer to licenses, compliance frameworks, regulatory requirements, and legal texts in software documentation.
*license, open-source license, proprietary license, MIT License, Apache 2.0 License, GPLv3, LGPL, BSD, AGPL, MPL, Unlicense, Creative Commons, EULA, terms of service (TOS), privacy policy, cookie policy, data processing agreement (DPA), service level agreement (SLA), contributor license agreement (CLA), Developer Certificate of Origin (DCO), copyright, trademark, patent, intellectual property, attribution, copyleft, permissive license, compliance, regulatory compliance, GDPR, CCPA, HIPAA, SOC 2, ISO 27001, PCI DSS, FedRAMP, FISMA, export control, EAR, ITAR, sanctions list, embargo, data residency, data sovereignty, data retention policy, right to erasure, right to access, data subject request (DSR), personal data, PII (Personally Identifiable Information), PHI (Protected Health Information), sensitive data, data classification, data handling policy, acceptable use policy, code of conduct, vendor risk assessment, security questionnaire (CAIQ, SIG), audit report, attestation, SOC report, penetration test report, vulnerability disclosure policy, bug bounty program terms, responsible disclosure policy, indemnification, limitation of liability, warranty disclaimer, governing law, jurisdiction, severability, force majeure, assignment, termination, survival clause, third-party notice, open-source attribution, NOTICE file, SBOM (Software Bill of Materials)*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| Make sure we're allowed to use that library. | The `request@2.88.2` package is deprecated and its license field in `package.json` is missing - it cannot be included in our Apache 2.0 project. Replace with `node-fetch@3.3.2` (MIT License, compatible). Validate via `npx license-checker --production --onlyAllow "MIT;Apache-2.0;ISC;BSD-2-Clause;BSD-3-Clause"`. |
| We need to handle European user data carefully. | Under GDPR Article 17 (Right to Erasure), implement the `DELETE /api/v1/users/{id}/personal-data` endpoint. The handler must cascade-delete all PII from `users`, `orders`, `sessions`, and `audit_log` tables, and issue a 30-day retention hold before permanent deletion from backups per our `DataRetentionPolicy` v2.1. |
| Put a disclaimer in the README about not being responsible. | Add to `LICENSE` (MIT): `THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.` This is the standard MIT warranty disclaimer. |

---

## Category 22 - Animals, Plants, and Other Life Forms

### Original (master.md line 1868-1871)
Terms that refer to biological entities in technical and environmental contexts.
*bacteria, bird, cassowary, cat, conifer, cow, dog, emu, fern, ferret, fungi, horse, insect, leopard, monkey, moss, mouse, pocket gopher, rose, termite, wombat*

### Adapted (Code Documentation)
Terms that refer to test fixtures, mock data, sample datasets, and placeholder entities used in code examples, test cases, and documentation demonstrations.
*test fixture, mock object, stub, spy, fake, dummy, test double, seed data, sample data, example record, placeholder, synthetic data, faker data, lorem ipsum, "John Doe", "Jane Smith", "Acme Corp", "example.com", "test@example.com", "user_12345", "order_abc", "00000000-0000-0000-0000-000000000000", "foo", "bar", "baz", "qux", "quux", "spam", "eggs", "ham", "hello world", "TODO", "FIXME", "HACK", "XXX", "WIP", "tmp", "scratch", "sandbox", "playground", "hello-world-app", "my-first-repo", "boilerplate", "starter-kit", "todo-mvc", "hello-kubernetes", "nginx-hello", "FakeUser", "MockOrderRepository", "StubPaymentGateway", "InMemoryDatabase", "NullLogger", "noop*, `TestUserFactory.create()`, `Fixtures.defaultUser()`, `faker.internet.email()`*

### STE / NON-STE Example Pairs

| Non-STE | STE |
|---------|-----|
| The test uses made-up data to check if it works. | The `OrderService` unit test uses `Fixtures.defaultOrder()` (returns an `Order` with `id="order_test_001"`, `userId="user_abc"`, `total=99.99`) and a `MockPaymentGateway` stub that returns `PaymentResult.SUCCESS` without making real HTTP calls. |
| The README example shows a user named Bob. | The `GET /api/v1/users/{id}` example in the API reference uses `id=00000000-0000-0000-0000-000000000000` (the nil UUID) and shows a sample response with `displayName: "Jane Smith"` and `email: "jane.smith@example.com"` - all example.com email addresses are reserved for documentation per RFC 6761. |
| The seed script populates the dev database with dummy stuff. | The `prisma/seed.ts` script creates 50 `User` records via `Faker` (`faker.internet.email()`, `faker.person.fullName()`), 200 `Product` records, and 500 `Order` records with randomized `status` fields to provide a realistic `development` dataset for manual QA. |

---

## Closing Notes (adapted from master.md line 1879-1882)

**Original:**
The technical nouns in their related categories are only examples. Rule 1.5 does not give a full list of all possible technical nouns. The listed words in each category have uppercase letters only when it is necessary. For example, official identifications, titles, and abbreviations.

**Adapted:**
The technical nouns in their related categories are only examples. Rule 1.5 does not give a full list of all possible technical nouns for code documentation. The listed terms in each category use backtick formatting (`LikeThis`) only when the term is a literal identifier, API name, or exact string value from code. For example, class names, function names, environment variable names, and error message strings.

---

## Related Rules (adapted)

### Rule 1.6 - adapted (from master.md line 1883)

**Original:** Use a word that is not approved in the dictionary, only when it is a technical noun or part of a technical noun.

**Adapted:** Use a word that is not approved in the standard documentation vocabulary, only when it is a technical noun (classified in one of the 22 categories above) or part of a technical noun.

| Non-STE | STE |
|---------|-----|
| The `base` class holds shared logic for all the page objects. | The `BasePage` class (technical noun, Category 1: API and library components) holds shared logic for all `PageObject` subclasses. |
| ("base" here is ambiguous - is it a common English word or a class name? Without classification, the reader cannot tell.) | (`BasePage` is a classified technical noun - the reader knows it is an intentional, project-specific identifier.) |

### Rule 1.7 - adapted (from master.md line 1981)

**Original:** Do not use words that are technical nouns as verbs.

**Adapted:** Do not use words that are technical nouns as verbs in code documentation.

| Non-STE | STE |
|---------|-----|
| `docker` the container and `curl` the endpoint to verify it. | Build the `Docker` image (technical noun, Category 5: Hosting, CI/CD infrastructure) and send a request to the endpoint using `curl` (technical noun, Category 3: Development tools). |
| (Using "docker" and "curl" as verbs is jargon that assumes domain knowledge.) | (Keeping them as technical nouns with explicit action verbs - "build", "send a request using" - makes the instruction self-documenting.) |

### Rule 1.8 - adapted (from master.md line 2018)

**Original:** Use technical nouns that are approved in your company, industry, or subject field.

**Adapted:** Use technical nouns that are approved in your project glossary, organization style guide, or ecosystem conventions.

| Non-STE | STE |
|---------|-----|
| The `data fetcher thing` in the `store layer` gets records from the `DB`. | The `Repository` pattern implementation (`UserRepository`) in the `data` layer fetches `User` entities from `PostgreSQL` via `TypeORM`. |
| ("data fetcher thing", "store layer", "DB" - none are approved technical nouns) | (`Repository`, `UserRepository`, `data layer`, `User`, `PostgreSQL`, `TypeORM` - all are approved technical nouns matching the project glossary.) |

### Rule 1.9 - adapted (from master.md line 2034)

**Original:** When you must select a technical noun, use one which is short and easy to understand.

**Adapted:** When you must select a technical noun for code documentation, use one which is short (not more than three words) and easy to understand.

| Non-STE | STE |
|---------|-----|
| Call the `asynchronous JavaScript Object Notation web token-based user authentication and authorization pre-validation middleware handler`. | Call the `JWT auth middleware`. |
| (Overly long - the reader must parse 14 words before understanding the concept.) | (3 words - `JWT`, `auth`, `middleware` - each is a known technical noun in the project glossary.) |

### Rule 1.10 - adapted (from master.md line 2048)

**Original:** Do not use regional, slang, or jargon words as technical nouns.

**Adapted:** Do not use team-internal slang, regional programming jargon, or company-specific nicknames as technical nouns in public-facing documentation.

| Non-STE | STE |
|---------|-----|
| The `magic button` on the `admin doodad page` sends a `zap` to the `thingamajig service`. | The `"Sync All"` button on the `Admin Dashboard` sends a `POST` request to the `DataSyncService`. |
| ("magic button", "doodad", "zap", "thingamajig" - team slang not understood by external readers) | (`"Sync All"` button, `Admin Dashboard`, `POST`, `DataSyncService` - all are clear, well-known technical nouns.) |

### Rule 1.11 - adapted (from master.md line 2093)

**Original:** Do not use different technical nouns for the same item.

**Adapted:** Do not use different technical nouns for the same software entity across your documentation.

| Non-STE | STE |
|---------|-----|
| Step 1: Call the `UserFetcher` service. Step 2: Configure the `AccountRetriever` module. Step 3: Restart the `ProfileLoader` microservice. | Step 1: Call the `UserService`. Step 2: Configure the `UserService`. Step 3: Restart the `UserService` microservice. |
| (`UserFetcher`, `AccountRetriever`, `ProfileLoader` all refer to the same `UserService` - the reader cannot tell they are the same entity.) | (`UserService` is used consistently throughout - the reader immediately recognizes each reference.) |

---

*Adaptation complete. All 22 categories from ASD-STE100 Issue 9, Rule 1.5 (master.md lines 1698-1878) have been adapted from aerospace to code documentation domain. Related rules 1.6 through 1.11 (master.md lines 1883-2108) are included with adapted STE/non-STE code example pairs.*
