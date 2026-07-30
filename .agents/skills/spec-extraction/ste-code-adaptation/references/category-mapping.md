# Category Mapping: STE → STE-Code

> CORRECTED: ASD-STE100 Issue 9 has exactly **19** technical noun categories,
> not 22. The previous version incorrectly claimed 22 categories.

## Usage Protocol

When you adapt an STE technical noun from the source spec:

1. Identify the original STE category name from your source text.
2. Find the matching row in the **19 Technical Code Noun Categories** table below.
3. Select a replacement term from the **STE-Code Category** column that fits your context.
4. If the term you need is not in the table, use the **Decision Table for Disambiguation** to classify it.
5. Add new terms to the **Exhaustive Example Expansion** section under the correct category.
6. Record the addition in the **Version History**.

Do not invent a category. Every code-domain term must map to one of the 19 categories. If a term does not fit any category, see **Edge Cases and Multi-Category Terms**.

---

## 19 Technical Code Noun Categories

| # | Original STE Category (Issue 9) | STE-Code Category | Representative Examples |
|---|----------------------|-------------------|--------------------------|
| 1 | Names in official parts information | Language keywords and reserved words | `if`, `else`, `return`, `class`, `async`, `await`, `import`, `export`, `const`, `let`, `var`, `function`, `interface`, `type`, `enum` |
| 2 | Names of vehicles/machines and locations on them | Frameworks, runtimes, and platforms | `React`, `Node.js`, `Docker`, `Kubernetes`, `PostgreSQL`, `Redis`, `Deno`, `Bun`, `V8`, `JVM`, `.NET`, `LLVM` |
| 3 | Names of tools and support equipment | Development tools and build systems | `webpack`, `esbuild`, `vite`, `prettier`, `eslint`, `git`, `npm`, `cargo`, `make`, `cmake`, `bazel` |
| 4 | Names of materials, consumables, and unwanted material | Dependencies, packages, and libraries | `lodash`, `express`, `axios`, `pytest`, `serde`, `tokio`, `left-pad`, `is-odd` (unapproved — use alternatives) |
| 5 | Names of facilities, infrastructure, and locations | Deployment targets and environments | `staging`, `production`, `AWS`, `Vercel`, `Cloudflare`, `localhost`, `CI`, `CD`, `edge`, `region` |
| 6 | Names of systems, components, circuits, and functions | Modules, classes, components, and services | `UserService`, `AuthModule`, `PaymentGateway`, `EventBus`, `DatabasePool`, `CacheLayer` |
| 7 | Mathematical, scientific, and engineering terms | Algorithmic and computational terms | `hash`, `sort`, `bfs`, `dfs`, `O(n)`, `O(log n)`, `tree`, `graph`, `cache`, `memoize`, `idempotent` |
| 8 | Navigation and geographic terms | Routing, pathing, and state management | `/api/users`, `/dashboard`, `useNavigate`, `Router`, `middleware`, `redirect`, `rewrite`, `proxy` |
| 9 | Numbers, units of measurement, and time | Data sizes, time units, and numeric formats | `500ms`, `2GB`, `200 OK`, `404 Not Found`, `64-bit`, `UTC`, `epoch`, `timeout`, `TTL` |
| 10 | Quoted text (placards, labels, signs, markings) | String literals, error messages, and log output | `"connection refused"`, `Error: timeout`, `console.log(...)`, `panic!("...")` |
| 11 | Names of persons, groups, or organizations | Roles, teams, services, and actors | `admin`, `moderator`, `viewer`, `OAuth provider`, `CI pipeline`, `CDN`, `auth service` |
| 12 | Parts of the body | UI/UX interaction and accessibility terms | `button`, `modal`, `aria-label`, `focus`, `viewport`, `breakpoint`, `screen reader`, `keyboard nav` |
| 13 | Common personal effects | Configuration and preference files | `.env`, `.gitignore`, `tsconfig.json`, `settings.json`, `profile`, `rc file`, `dotfile` |
| 14 | Medical terms | Error states, diagnostics, and health checks | `NullPointerException`, `500 Internal Server Error`, `race condition`, `deadlock`, `livelock`, `OOM`, `stack overflow` |
| 15 | Names of official documents and documentation parts | Specification files, configs, and manifests | `package.json`, `Dockerfile`, `openapi.yaml`, `Makefile`, `README.md`, `CHANGELOG.md`, `Cargo.toml` |
| 16 | Environmental and operational conditions | Runtime conditions, states, and feature flags | `cold start`, `warm cache`, `idle`, `under load`, `degraded`, `throttled`, `feature flag on`, `dark mode` |
| 17 | Colors | Terminal colors and syntax highlighting themes | `red`, `green`, `cyan`, `magenta`, `bold`, `dim`, `256-color`, `truecolor`, `ANSI escape` |
| 18 | Damage terms | Bug, defect, failure, and degradation taxonomy | `crash`, `memory leak`, `race condition`, `XSS`, `SQL injection`, `DoS`, `data corruption`, `bit rot` |
| 19 | Information technology and telephony terms | Network, protocol, API, and I/O terms | `HTTP/2`, `WebSocket`, `gRPC`, `TLS 1.3`, `DNS`, `TCP`, `UDP`, `REST`, `GraphQL`, `protobuf` |

---

## Decision Table for Disambiguation

Use this table when a term could fit more than one category. Start at the top and stop at the first match. The first matching rule wins.

| # | If the term is... | Classify as... | Rationale |
|---|-------------------|----------------|-----------|
| D1 | A specific package name on a registry (npm, PyPI, crates.io, Maven) | **Cat 4** — Dependencies, packages, and libraries | Registries are the "supply chain." This mirrors STE's "consumables and materials." |
| D2 | A specific tool you invoke from the command line (`eslint`, `prettier`, `git`, `docker`) | **Cat 3** — Development tools and build systems | Tools are "equipment." You use them but do not import them as libraries. |
| D3 | A specific runtime, platform, or engine that hosts code (`Node.js`, `JVM`, `V8`, `.NET`, `Bun`) | **Cat 2** — Frameworks, runtimes, and platforms | Runtimes are "vehicles/machines" that carry code. They are not tools you invoke directly. |
| D4 | A specific library you import into your code (`express`, `lodash`, `serde`, `tokio`) | **Cat 4** — Dependencies, packages, and libraries | Imported libraries are "consumables" — they become part of your project. |
| D5 | A generic algorithmic concept or data structure (`hash`, `sort`, `bfs`, `tree`, `graph`) | **Cat 7** — Algorithmic and computational terms | Generic concepts are "mathematical/engineering terms." They are not specific to any library. |
| D6 | A specific named module, class, component, or service in a codebase (`UserService`, `AuthModule`, `PaymentGateway`) | **Cat 6** — Modules, classes, components, and services | Named entities in code are "systems/components/functions." They have a specific role in an architecture. |
| D7 | A URL path, route pattern, or redirect rule (`/api/users`, `/dashboard`, `middleware`) | **Cat 8** — Routing, pathing, and state management | Paths and routes are "navigation/geographic" terms. They describe where things go. |
| D8 | A specific filename that configures a tool (`.env`, `package.json`, `Dockerfile`, `tsconfig.json`) | **Cat 15** — Specification files, configs, and manifests | Config files are "official documents." They declare how things work. |
| D9 | A specific filename for user preferences (`.gitignore`, `settings.json`, `.editorconfig`) | **Cat 13** — Configuration and preference files | Preference files are "personal effects." They store user choices. |
| D10 | An error condition, failure state, or diagnostic signal (`NullPointerException`, `race condition`, `deadlock`, `OOM`) | **Cat 14** — Error states, diagnostics, and health checks | Errors and failures are "medical terms" — they describe unhealthy states. |
| D11 | A security vulnerability or attack vector (`XSS`, `SQL injection`, `DoS`, `CSRF`) | **Cat 18** — Bug, defect, failure, and degradation taxonomy | Attack vectors are "damage terms." They describe things that break systems. |
| D12 | A network protocol, API paradigm, or I/O standard (`HTTP/2`, `WebSocket`, `gRPC`, `REST`, `GraphQL`) | **Cat 19** — Network, protocol, API, and I/O terms | Protocols and APIs are "IT/telephony terms." They describe how systems talk. |
| D13 | A UI element, interaction pattern, or accessibility feature (`button`, `modal`, `aria-label`, `viewport`, `focus`) | **Cat 12** — UI/UX interaction and accessibility terms | UI elements are "parts of the body." They are the visible, tangible parts users interact with. |
| D14 | A state, condition, or flag that changes behavior at runtime (`cold start`, `idle`, `dark mode`, `feature flag on`) | **Cat 16** — Runtime conditions, states, and feature flags | States and conditions are "environmental/operational" terms. They describe the current context. |
| D15 | A string value, error message text, or log output line (`"connection refused"`, `console.log(...)`, `panic!("...")`) | **Cat 10** — String literals, error messages, and log output | Quoted text is "placards/labels/markings." It is the literal text produced by the system. |

### Boundary Cases: Worked Examples

These examples show how the decision table resolves common ambiguous terms.

| Term | Could be... | Decision Rule | Final Category | Why |
|------|-------------|---------------|----------------|-----|
| `cache` | Cat 7 (algorithmic concept) or Cat 16 (warm cache state) | Context-dependent. If used as a data structure concept → D5. If used as a runtime state → D14. | Cat 7 if generic; Cat 16 if state | Check if the term describes a structure or a condition. |
| `React` | Cat 2 (runtime) or Cat 4 (library) | D3: It is a runtime that hosts code. | Cat 2 | React is a platform. You do not `npm install react` and call it "just a dependency." |
| `proxy` | Cat 8 (routing) or Cat 19 (network) | D12: It is a network intermediary concept in most uses. | Cat 19 | When describing how traffic flows, proxy is an IT term. When used as a routing pattern, classify under Cat 8. |
| `.gitignore` | Cat 13 (preference) or Cat 15 (config) | D9: It stores user preferences about tracked files. | Cat 13 | `.gitignore` is a personal choice file, not a project specification. |
| `Dockerfile` | Cat 3 (tool) or Cat 15 (config) | D8: It is an "official document" that specifies a build. | Cat 15 | A Dockerfile is a declarative specification, not a tool invocation. |
| `race condition` | Cat 14 (error state) or Cat 18 (damage) | D10: It is a diagnostic signal of an unhealthy state. | Cat 14 | A race condition is detected as a health problem. The damage from it (Cat 18) is the downstream effect. |
| `Redis` | Cat 2 (platform) or Cat 5 (deployment target) | D3: It is a runtime platform that hosts data. | Cat 2 | Redis is a platform. Running it on `AWS` makes `AWS` Cat 5, but Redis remains Cat 2. |

---

## Edge Cases and Multi-Category Terms

### When a Term Fits No Category

A new code-domain term may have no clear STE analogue. Use this protocol:

1. **Check the decision table** (D1–D15). Is there a match you missed?
2. **Find the closest STE category by function.** Ask: "What does this term DO in the system?"
   - If it stores configuration → likely Cat 13 or Cat 15
   - If it moves data → likely Cat 8 or Cat 19
   - If it describes a problem → likely Cat 14 or Cat 18
   - If it is a specific named thing → likely Cat 1, Cat 2, Cat 4, or Cat 6
3. **If no category fits:** Document the term in the **Unclassified Terms** section below. Do not force a classification. Mark it as `⚠️ UNCLASSIFIED` and move on. An extension worker will handle it in a later phase.
4. **Do not invent a 20th category.** The 19-category architecture comes from ASD-STE100 Issue 9. Deviating from 19 categories breaks the adaptation contract.

### When a Term Fits Multiple Categories

Some terms legitimately span categories. Use these priority rules:

1. **Specific over generic:** A specific library name (`lodash`) is Cat 4, even if `lodash` provides algorithmic utilities. The specificity of a package name overrides the generic function it performs.
2. **Function over form:** A file named `.eslintrc.js` could be Cat 13 (preference file) or Cat 15 (config manifest). Choose based on function: if it configures a tool's behavior → Cat 15. If it stores user preferences → Cat 13.
3. **Primary role over secondary role:** `Docker` could be Cat 2 (platform), Cat 3 (tool), or Cat 5 (deployment target). Its primary role in most documentation is as a platform (Cat 2). Classify by the most common usage in your context.
4. **Origin over effect:** A `race condition` is Cat 14 (the condition itself) even though it causes Cat 18 damage (the crash). Classify by what the term IS, not what it causes.

### Unclassified Terms

Terms that have no clear STE analogue. Extension workers assign these to categories in a later phase.

| Term | Candidate Categories | Reason Unclassified | Date |
|------|---------------------|---------------------|------|
| *(none yet)* | — | — | — |

---

## Exhaustive Example Expansion

Each category includes all known terms from the Issue 9 source pages and code-domain equivalents. New terms discovered during adaptation are added here.

### Cat 1 — Language Keywords and Reserved Words

**STE source:** Names in official parts information (part numbers, specification references, catalog entries)

**Expanded examples:**

JavaScript/TypeScript: `if`, `else`, `return`, `class`, `async`, `await`, `import`, `export`, `const`, `let`, `var`, `function`, `interface`, `type`, `enum`, `extends`, `implements`, `new`, `this`, `super`, `throw`, `try`, `catch`, `finally`, `switch`, `case`, `default`, `break`, `continue`, `for`, `while`, `do`, `in`, `of`, `typeof`, `instanceof`, `void`, `delete`, `yield`, `static`, `get`, `set`, `namespace`, `module`, `declare`, `abstract`, `readonly`, `private`, `protected`, `public`, `as`, `is`, `keyof`, `infer`, `never`, `unknown`, `any`

Python: `def`, `class`, `return`, `if`, `elif`, `else`, `for`, `while`, `break`, `continue`, `pass`, `raise`, `try`, `except`, `finally`, `with`, `as`, `import`, `from`, `lambda`, `yield`, `async`, `await`, `global`, `nonlocal`, `assert`, `del`, `not`, `and`, `or`, `is`, `in`, `True`, `False`, `None`

Rust: `fn`, `let`, `mut`, `const`, `static`, `struct`, `enum`, `impl`, `trait`, `mod`, `use`, `pub`, `crate`, `self`, `super`, `match`, `if`, `else`, `loop`, `while`, `for`, `in`, `break`, `continue`, `return`, `move`, `ref`, `async`, `await`, `dyn`, `where`, `unsafe`, `extern`, `type`

Go: `func`, `var`, `const`, `type`, `struct`, `interface`, `map`, `chan`, `go`, `defer`, `select`, `case`, `default`, `if`, `else`, `for`, `range`, `break`, `continue`, `return`, `package`, `import`, `fallthrough`, `goto`

### Cat 2 — Frameworks, Runtimes, and Platforms

**STE source:** Names of vehicles/machines and locations on them (aircraft models, engine types, structural locations)

**Expanded examples:**

Frontend frameworks: `React`, `Vue`, `Svelte`, `Angular`, `SolidJS`, `Preact`, `Next.js`, `Nuxt`, `Remix`, `Astro`, `Qwik`, `Lit`, `htmx`, `Alpine.js`

Backend runtimes: `Node.js`, `Deno`, `Bun`, `Python`, `Ruby`, `Go`, `Rust`, `Java`, `C#`, `PHP`

Mobile platforms: `React Native`, `Flutter`, `SwiftUI`, `Jetpack Compose`, `Expo`, `Capacitor`

Database engines: `PostgreSQL`, `MySQL`, `SQLite`, `MongoDB`, `Redis`, `Elasticsearch`, `Cassandra`, `Neo4j`, `ClickHouse`, `DuckDB`

Container and orchestration: `Docker`, `Kubernetes`, `Podman`, `Helm`, `Nomad`, `Rancher`

Compilation targets: `V8`, `JVM`, `.NET`, `LLVM`, `WebAssembly`, `GraalVM`, `BEAM`, `CPython`

### Cat 3 — Development Tools and Build Systems

**STE source:** Names of tools and support equipment (wrenches, test equipment, calibration devices)

**Expanded examples:**

Bundlers: `webpack`, `esbuild`, `vite`, `rollup`, `parcel`, `turbopack`, `rspack`, `swc`

Linters and formatters: `prettier`, `eslint`, `biome`, `oxlint`, `ruff`, `clippy`, `gofmt`, `black`, `isort`, `mypy`, `pyright`

Version control: `git`, `mercurial`, `svn`, `fossil`

Package managers: `npm`, `yarn`, `pnpm`, `cargo`, `pip`, `poetry`, `uv`, `gem`, `bundler`, `composer`, `go mod`

Build systems: `make`, `cmake`, `bazel`, `gradle`, `maven`, `ninja`, `meson`, `scons`, `buck2`

CI/CD runners: `GitHub Actions`, `GitLab CI`, `Jenkins`, `CircleCI`, `Drone`, `ArgoCD`, `Tekton`

### Cat 4 — Dependencies, Packages, and Libraries

**STE source:** Names of materials, consumables, and unwanted material (lubricants, sealants, waste products)

**Expanded examples:**

JavaScript/TypeScript libraries: `lodash`, `express`, `axios`, `react`, `react-dom`, `zod`, `prisma`, `drizzle`, `next`, `nuxt`, `tailwindcss`, `jest`, `vitest`, `playwright`, `storybook`, `zod`, `yup`, `joi`, `moment`, `dayjs`, `date-fns`, `rxjs`, `immer`, `zustand`, `jotai`

Python libraries: `pytest`, `django`, `flask`, `fastapi`, `sqlalchemy`, `pydantic`, `numpy`, `pandas`, `scikit-learn`, `tensorflow`, `pytorch`, `celery`, `httpx`, `requests`, `beautifulsoup4`, `pydantic`, `typer`, `rich`, `click`

Rust crates: `serde`, `tokio`, `axum`, `actix-web`, `diesel`, `sqlx`, `clap`, `anyhow`, `thiserror`, `reqwest`, `tracing`, `rayon`, `crossbeam`

Unapproved / deprecated: `left-pad`, `is-odd`, `is-even`, `is-number`, `request` (deprecated), `crypto` (unmaintained)

### Cat 5 — Deployment Targets and Environments

**STE source:** Names of facilities, infrastructure, and locations (hangars, runways, maintenance bays, test facilities)

**Expanded examples:**

Environment names: `staging`, `production`, `development`, `testing`, `sandbox`, `canary`, `preview`, `ephemeral`

Cloud providers: `AWS`, `GCP`, `Azure`, `Vercel`, `Netlify`, `Cloudflare`, `Heroku`, `Railway`, `Fly.io`, `Render`, `DigitalOcean`, `Linode`, `Supabase`, `PlanetScale`

Local: `localhost`, `127.0.0.1`, `::1`

CI/CD stages: `CI`, `CD`, `build`, `test`, `deploy`, `release`, `promote`

Edge: `edge`, `region`, `zone`, `CDN edge`, `POP`, `origin`

### Cat 6 — Modules, Classes, Components, and Services

**STE source:** Names of systems, components, circuits, and functions (hydraulic system, electrical bus, navigation computer)

**Expanded examples:**

Backend services: `UserService`, `AuthModule`, `PaymentGateway`, `EventBus`, `DatabasePool`, `CacheLayer`, `MessageQueue`, `RateLimiter`, `SchedulerService`, `NotificationDispatcher`, `FileStorageService`, `SearchIndexService`, `AnalyticsPipeline`

Frontend components: `UserProfile`, `Dashboard`, `Navbar`, `Sidebar`, `DataTable`, `SearchBar`, `Pagination`, `Modal`, `Toast`, `FormField`, `FileUploader`, `ChartWidget`, `NotificationBell`

Classes and modules: `User`, `Order`, `Product`, `Cart`, `Session`, `Token`, `Config`, `Logger`, `Validator`, `Transformer`, `Serializer`, `Repository`, `Controller`, `Middleware`

Design patterns: `Singleton`, `Factory`, `Observer`, `Strategy`, `Decorator`, `Adapter`, `Facade`, `Proxy`, `Command`, `Builder`

### Cat 7 — Algorithmic and Computational Terms

**STE source:** Mathematical, scientific, and engineering terms (torque, voltage, frequency, drag coefficient)

**Expanded examples:**

Algorithms: `hash`, `sort`, `bfs`, `dfs`, `binary search`, `merge sort`, `quick sort`, `dijkstra`, `a-star`, `dynamic programming`, `greedy`, `backtracking`, `divide and conquer`

Complexity: `O(1)`, `O(n)`, `O(log n)`, `O(n log n)`, `O(n²)`, `O(2ⁿ)`, `O(n!)`

Data structures: `array`, `list`, `tree`, `graph`, `hash table`, `stack`, `queue`, `heap`, `trie`, `bloom filter`, `linked list`, `doubly linked list`, `binary tree`, `red-black tree`, `B-tree`, `skip list`

Techniques: `memoize`, `cache`, `lazy evaluation`, `tail recursion`, `currying`, `partial application`, `thunk`, `trampoline`, `continuation`, `monad`, `functor`, `applicative`

Properties: `idempotent`, `pure`, `deterministic`, `side-effect`, `referentially transparent`, `immutable`, `stateless`, `thread-safe`, `lock-free`, `wait-free`, `eventually consistent`

### Cat 8 — Routing, Pathing, and State Management

**STE source:** Navigation and geographic terms (latitude, longitude, heading, waypoint, route segment)

**Expanded examples:**

URL paths: `/api/users`, `/api/users/:id`, `/dashboard`, `/login`, `/logout`, `/settings`, `/search`, `/products/:slug`, `/checkout`, `/webhook`

React Router: `useNavigate`, `Router`, `Route`, `Link`, `NavLink`, `Outlet`, `useParams`, `useSearchParams`, `useLocation`, `Navigate`, `redirect`

Middleware: `middleware`, `guard`, `interceptor`, `pipeline`, `handler chain`, `before`, `after`, `onRequest`, `onResponse`

Routing concepts: `rewrite`, `proxy`, `reverse proxy`, `load balancer`, `CDN`, `edge function`, `serverless function`, `API gateway`

State management: `Redux`, `MobX`, `Zustand`, `Jotai`, `Recoil`, `Valtio`, `Pinia`, `Vuex`, `XState`, `useReducer`, `useState`, `useContext`, `store`, `action`, `reducer`, `selector`, `dispatch`, `subscribe`, `atom`, `signal`

### Cat 9 — Data Sizes, Time Units, and Numeric Formats

**STE source:** Numbers, units of measurement, and time (inches, pounds, seconds, gallons, degrees Celsius)

**Expanded examples:**

Time units: `500ms`, `30s`, `5m`, `2h`, `1d`, `60fps`, `144Hz`, `1kHz`, `3GHz`

Data sizes: `1B`, `1KB`, `1MB`, `1GB`, `1TB`, `1PB`, `8-bit`, `16-bit`, `32-bit`, `64-bit`, `128-bit`

HTTP status codes: `200 OK`, `201 Created`, `204 No Content`, `301 Moved Permanently`, `302 Found`, `304 Not Modified`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `405 Method Not Allowed`, `409 Conflict`, `429 Too Many Requests`, `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`

Date/time formats: `UTC`, `epoch`, `ISO 8601`, `Unix timestamp`, `RFC 3339`

Duration and limits: `timeout`, `TTL`, `rate limit`, `quota`, `budget`, `threshold`, `deadline`, `expiry`, `retry after`, `backoff`

### Cat 10 — String Literals, Error Messages, and Log Output

**STE source:** Quoted text — placards, labels, signs, markings (warning labels, instruction placards, cockpit markings)

**Expanded examples:**

Error messages: `"connection refused"`, `"permission denied"`, `"not found"`, `"invalid input"`, `"timeout exceeded"`, `"out of memory"`, `"disk full"`, `"rate limit exceeded"`, `"unauthorized"`, `"forbidden"`

Log output: `console.log("server started on port 3000")`, `console.error("failed to connect")`, `console.warn("deprecated API")`, `panic!("unreachable code")`, `throw new Error("invalid state")`, `logger.info("request completed")`, `logger.debug("query took 42ms")`

String literals: `"Hello, World!"`, `"success"`, `"failure"`, `"pending"`, `"active"`, `"inactive"`, `"enabled"`, `"disabled"`, `""` (empty string), `null`, `undefined`

Template strings: `` `User ${name} not found` ``, `` `Page ${current} of ${total}` ``, `` `${status}: ${message}` ``

### Cat 11 — Roles, Teams, Services, and Actors

**STE source:** Names of persons, groups, or organizations (pilot, engineer, maintenance crew, regulatory authority)

**Expanded examples:**

User roles: `admin`, `moderator`, `viewer`, `editor`, `owner`, `member`, `guest`, `superadmin`, `auditor`, `reviewer`, `contributor`, `maintainer`

External actors: `OAuth provider`, `CI pipeline`, `CDN`, `auth service`, `payment processor`, `email service`, `SMS gateway`, `push notification service`, `search provider`, `analytics service`, `monitoring service`

Team names: `platform team`, `frontend team`, `backend team`, `devops team`, `security team`, `QA team`, `SRE team`, `data team`, `design team`

Automated actors: `bot`, `crawler`, `webhook`, `scheduler`, `cron job`, `daemon`, `worker`, `agent`, `service account`

### Cat 12 — UI/UX Interaction and Accessibility Terms

**STE source:** Parts of the body (hands, eyes, ears — parts users use to interact)

**Expanded examples:**

UI elements: `button`, `modal`, `dialog`, `tooltip`, `dropdown`, `combobox`, `tab`, `accordion`, `carousel`, `breadcrumb`, `pagination`, `stepper`, `slider`, `toggle`, `switch`, `checkbox`, `radio`, `select`, `textarea`, `input`, `search`, `filter`, `sort`, `datagrid`, `card`, `panel`, `drawer`, `sheet`, `popover`, `menu`, `context menu`, `command palette`

Layout: `viewport`, `breakpoint`, `container`, `grid`, `flex`, `stack`, `spacer`, `divider`, `separator`, `gap`, `margin`, `padding`, `border`, `shadow`, `z-index`

Accessibility: `aria-label`, `aria-describedby`, `aria-hidden`, `aria-expanded`, `aria-selected`, `aria-current`, `role`, `tabindex`, `alt text`, `focus`, `focus trap`, `focus ring`, `screen reader`, `keyboard nav`, `skip link`, `landmark`, `live region`, `announcement`

Interaction: `hover`, `click`, `tap`, `swipe`, `drag`, `drop`, `pinch`, `zoom`, `scroll`, `resize`, `focus`, `blur`, `keydown`, `keyup`, `submit`, `reset`

### Cat 13 — Configuration and Preference Files

**STE source:** Common personal effects (clothing, tools, personal items carried by personnel)

**Expanded examples:**

Dotfiles: `.env`, `.env.local`, `.env.production`, `.gitignore`, `.gitattributes`, `.editorconfig`, `.prettierrc`, `.eslintrc`, `.eslintignore`, `.npmrc`, `.yarnrc`, `.browserslistrc`, `.nvmrc`, `.node-version`, `.ruby-version`, `.python-version`, `.tool-versions`, `.bashrc`, `.zshrc`, `.profile`, `.bash_profile`, `.zprofile`, `.vimrc`, `.tmux.conf`, `.gitconfig`

IDE/editor settings: `.vscode/settings.json`, `.vscode/extensions.json`, `.idea/`, `settings.json`, `keybindings.json`, `snippets/`

Preference files: `tsconfig.json` (user-level), `jsconfig.json`, `preferences.json`, `rc file`, `dotfile`, `config.yaml`, `config.toml`, `config.ini`, `config.cfg`

### Cat 14 — Error States, Diagnostics, and Health Checks

**STE source:** Medical terms (symptoms, diagnoses, conditions, treatments)

**Expanded examples:**

Exceptions and errors: `NullPointerException`, `TypeError`, `ReferenceError`, `SyntaxError`, `RangeError`, `URIError`, `EvalError`, `InternalError`, `StackOverflowError`, `OutOfMemoryError`, `IOException`, `SQLException`, `TimeoutError`, `ConnectionError`, `AuthenticationError`, `AuthorizationError`, `ValidationError`, `SerializationError`, `DeserializationError`, `ParseError`, `RuntimeError`, `Panic`

HTTP error states: `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`, `504 Gateway Timeout`, `429 Too Many Requests`, `409 Conflict`

Concurrency problems: `race condition`, `deadlock`, `livelock`, `starvation`, `priority inversion`, `ABA problem`, `thundering herd`

Resource exhaustion: `OOM` (out of memory), `stack overflow`, `heap exhaustion`, `file descriptor exhaustion`, `connection pool exhaustion`, `thread pool exhaustion`, `CPU throttling`, `disk full`, `quota exceeded`

Health checks: `liveness probe`, `readiness probe`, `startup probe`, `health check endpoint`, `/healthz`, `/readyz`, `/livez`, `heartbeat`, `watchdog`, `circuit breaker open`, `circuit breaker half-open`

Degraded states: `degraded`, `partial outage`, `brownout`, `throttled`, `rate limited`, `backpressure`, `shed load`

### Cat 15 — Specification Files, Configs, and Manifests

**STE source:** Names of official documents and documentation parts (maintenance manuals, service bulletins, airworthiness directives)

**Expanded examples:**

Package manifests: `package.json`, `Cargo.toml`, `pyproject.toml`, `Pipfile`, `requirements.txt`, `Gemfile`, `go.mod`, `composer.json`, `pubspec.yaml`, `build.gradle`, `pom.xml`, `CMakeLists.txt`

Container and infra: `Dockerfile`, `docker-compose.yml`, `compose.yaml`, `Containerfile`, `Vagrantfile`, `Procfile`, `heroku.yml`

Infrastructure as code: `terraform.tf`, `pulumi.yaml`, `cdk.json`, `cloudformation.yaml`, `ansible.cfg`, `playbook.yml`, `inventory.ini`

API specs: `openapi.yaml`, `swagger.json`, `graphql.schema`, `protobuf.proto`, `thrift.idl`, `avro.avsc`, `grpc.proto`

Documentation: `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `LICENSE`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `ARCHITECTURE.md`, `API.md`, `DEVELOPMENT.md`, `DEPLOYMENT.md`

CI/CD configs: `.github/workflows/ci.yml`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`, `bitbucket-pipelines.yml`, `netlify.toml`, `vercel.json`, `fly.toml`, `render.yaml`

### Cat 16 — Runtime Conditions, States, and Feature Flags

**STE source:** Environmental and operational conditions (temperature, altitude, humidity, pressure, load factor)

**Expanded examples:**

Application lifecycle: `cold start`, `warm start`, `hot reload`, `live reload`, `HMR`, `fast refresh`, `graceful shutdown`, `drain`, `prestop`, `poststart`

Cache states: `warm cache`, `cold cache`, `cache hit`, `cache miss`, `cache eviction`, `cache invalidation`, `cache stampede`, `stale-while-revalidate`

Load states: `idle`, `under load`, `peak load`, `spike`, `burst`, `saturated`, `overloaded`, `throttled`, `degraded`, `backpressure`

Feature flags: `feature flag on`, `feature flag off`, `dark mode`, `beta feature`, `canary release`, `A/B test`, `percentage rollout`, `kill switch`, `circuit breaker`, `feature gate`, `launchdarkly flag`

Process states: `running`, `sleeping`, `stopped`, `zombie`, `orphan`, `defunct`, `waiting`, `blocked`, `suspended`, `paused`, `resumed`, `terminated`, `killed`

Connection states: `connected`, `disconnected`, `reconnecting`, `draining`, `closing`, `closed`, `half-open`, `established`, `listening`, `time_wait`, `close_wait`

### Cat 17 — Terminal Colors and Syntax Highlighting Themes

**STE source:** Colors (red, green, blue, yellow — used in markings and indicators)

**Expanded examples:**

ANSI colors: `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `black`, `bright red`, `bright green`, `bright yellow`, `bright blue`, `bright magenta`, `bright cyan`, `bright white`, `gray`, `dark gray`, `default`

Text attributes: `bold`, `dim`, `italic`, `underline`, `blink`, `reverse`, `hidden`, `strikethrough`, `reset`, `normal`

Color modes: `256-color`, `truecolor`, `24-bit color`, `8-bit color`, `16-color`, `no-color`, `NO_COLOR`, `FORCE_COLOR`

ANSI escapes: `\x1b[31m`, `\x1b[0m`, `\x1b[1m`, `\x1b[4m`, `ESC[`, `CSI`, `SGR`, `tput`

Syntax themes: `Monokai`, `Dracula`, `Nord`, `Solarized`, `One Dark`, `Gruvbox`, `Catppuccin`, `Tokyo Night`, `Rose Pine`

### Cat 18 — Bug, Defect, Failure, and Degradation Taxonomy

**STE source:** Damage terms (crack, corrosion, dent, wear, fatigue, fracture)

**Expanded examples:**

Failure types: `crash`, `hang`, `freeze`, `panic`, `segfault`, `abort`, `SIGSEGV`, `SIGABRT`, `SIGKILL`, `SIGTERM`, `undefined behavior`, `UB`, `double free`, `use after free`, `null pointer dereference`

Resource problems: `memory leak`, `handle leak`, `file descriptor leak`, `connection leak`, `goroutine leak`, `event listener leak`, `subscription leak`, `retained object`, `circular reference`

Security vulnerabilities: `XSS`, `SQL injection`, `command injection`, `path traversal`, `CSRF`, `SSRF`, `DoS`, `DDoS`, `buffer overflow`, `integer overflow`, `prototype pollution`, `open redirect`, `insecure deserialization`, `timing attack`, `side channel`, `privilege escalation`, `information disclosure`, `MITM`, `replay attack`

Data problems: `data corruption`, `bit rot`, `data loss`, `split brain`, `write skew`, `phantom read`, `dirty read`, `lost update`, `stale read`, `inconsistent state`, `partial write`, `torn write`

Degradation: `bit rot`, `code rot`, `software rot`, `entropy`, `drift`, `configuration drift`, `schema drift`, `API drift`

Anti-patterns: `god object`, `spaghetti code`, `lasagna code`, `ravioli code`, `dead code`, `zombie code`, `cargo cult`, `magic number`, `magic string`, `hardcoded`, `gold plating`, `premature optimization`, `yak shaving`, `bike shedding`

### Cat 19 — Network, Protocol, API, and I/O Terms

**STE source:** Information technology and telephony terms (radio frequency, bandwidth, signal, antenna)

**Expanded examples:**

Protocols: `HTTP/1.1`, `HTTP/2`, `HTTP/3`, `HTTPS`, `WebSocket`, `SSE`, `gRPC`, `TCP`, `UDP`, `QUIC`, `TLS 1.3`, `SSL`, `DNS`, `DHCP`, `SMTP`, `IMAP`, `POP3`, `FTP`, `SFTP`, `SSH`, `NTP`, `SNMP`, `MQTT`, `AMQP`, `STOMP`, `WebRTC`, `RTMP`, `HLS`, `DASH`

API paradigms: `REST`, `GraphQL`, `SOAP`, `gRPC`, `JSON-RPC`, `XML-RPC`, `tRPC`, `OpenAPI`, `Swagger`, `AsyncAPI`

Data formats: `JSON`, `YAML`, `TOML`, `XML`, `CSV`, `protobuf`, `MsgPack`, `BSON`, `Avro`, `Thrift`, `Cap'n Proto`, `FlatBuffers`, `CBOR`, `MessagePack`

I/O concepts: `stdin`, `stdout`, `stderr`, `pipe`, `socket`, `file descriptor`, `buffer`, `stream`, `chunk`, `flush`, `drain`, `backpressure`, `async I/O`, `non-blocking I/O`, `epoll`, `kqueue`, `io_uring`, `mmap`, `sendfile`, `zero-copy`

Architecture: `client`, `server`, `peer`, `proxy`, `reverse proxy`, `load balancer`, `API gateway`, `service mesh`, `sidecar`, `ambassador`, `ingress`, `egress`, `NAT`, `firewall`, `VPN`, `DMZ`

---

## 4 Technical Code Verb Categories

| # | Category | Description | Example Verbs |
|---|----------|-------------|---------------|
| 1 | Development operations | Build, compile, test, version, deploy | `build`, `compile`, `test`, `lint`, `format`, `commit`, `push`, `deploy`, `rollback` |
| 2 | Data operations | I/O, serialization, persistence, transformation | `read`, `write`, `serialize`, `deserialize`, `parse`, `encode`, `decode`, `query`, `insert`, `migrate` |
| 3 | Application operations | Request handling, state, authentication, scheduling | `handle`, `route`, `authenticate`, `authorize`, `validate`, `schedule`, `dispatch`, `resolve` |
| 4 | Communication operations | Messaging, remote calls, streaming | `send`, `receive`, `publish`, `subscribe`, `stream`, `poll`, `broadcast`, `connect` |

---

## Version History

| Date | Version | Change | Rationale |
|------|---------|--------|-----------|
| 2025-07-30 | 1.3.0 | Added Decision Table for Disambiguation (D1–D15), Boundary Cases table, Usage Protocol, Edge Cases section, Exhaustive Example Expansion for all 19 categories, Cross-References section | Maturity audit identified gaps in disambiguation guidance, usage instructions, and example coverage. The decision table resolves ambiguous term classification with priority rules. The exhaustive expansion covers all known terms from Issue 9 source pages plus code-domain equivalents. |
| 2025-07-15 | 1.2.0 | Added Unclassified Terms table. | Edge case protocol needed for new code-domain terms with no STE analogue. Extension workers handle these in a later phase. |
| 2025-07-01 | 1.1.0 | Expanded verb categories table with fuller descriptions. | Verb categories lacked enough description for agents to classify borderline operation terms. |
| 2025-06-20 | 1.0.1 | Added Correction note: 22 → 19 categories. | Previous version claimed 22 categories based on an earlier draft. Audit of Issue 9 spec pages 47–52 confirmed exactly 19 categories. All dependent files updated to reflect this correction. |
| 2025-06-15 | 1.0.0 | Initial release. 19 noun categories + 4 verb categories with representative examples. | First adaptation of ASD-STE100 Issue 9 category architecture to the code domain. |

---

## Cross-References to Dependent Skills

These skills consume this category mapping file. When the mapping changes, check these files for consistency.

| Skill | File | Lines | How It Uses This Mapping |
|-------|------|-------|--------------------------|
| STE-Code Adaptation | `.agents/skills/spec-extraction/ste-code-adaptation/SKILL.md` | 55, 61 | References `category-mapping.md` as the authority for the 19-category adaptation. Rule 55: "Technical noun categories → code-domain categories (see references/category-mapping.md)." Rule 61: "See `references/category-mapping.md` for the full 19-category adaptation." |
| STE-Code Continuation | `.agents/skills/spec-extraction/ste-code-continuation/SKILL.md` | 337, 403, 618 | Line 337: Agent command referencing "Map per references/category-mapping.md." Line 403: Verification checkpoint "19 categories mapped per category-mapping.md." Line 618: Final validation "Category mapping: 19/19 per category-mapping.md." |
| Continued Orchestrator | `.agents/skills/spec-extraction/ste-code-continue/continuation.md` | 34, 48, 123, 131, 184 | Line 34: Lists category-mapping.md as prerequisite reading. Line 48: "19 technical noun categories — remapped per category-mapping.md." Line 123: Template field "Category mapping: references/category-mapping.md." Line 131: Template field "Category name adapted for code domain per category-mapping.md." Line 184: Recovery rule "Verify against category-mapping.md. If master.md is wrong, use the mapping file as the source of truth." |
| Agent State Report | `.agents/skills/spec-extraction/agent-state-report/SKILL.md` | — | Uses category mapping indirectly through the adaptation phase reporting. Category count consistency depends on this file. |
| Extension Worker | `.agents/skills/spec-extraction/extension-worker/SKILL.md` | — | Extension workers consult category-mapping.md to classify newly discovered code-domain terms and fill gaps where Issue 9 provides no analogue. |
| Benchmark Orchestrator | `.agents/benchmark/orchestrator.py` | — | Benchmark tests validate that adapted documentation uses the correct 19 categories. Category count mismatch triggers a test failure. |

---

## Verification Notes

- All category names verified against Issue 9 spec pages 47-52 (`page-0047.md` through `page-0052.md` in the extraction)
- All 19 categories confirmed present (no categories 20-22 in Issue 9 — those were from an earlier draft or confusion)
- STE-Code examples use concrete, recognizable software development terms
- The Decision Table (D1–D15) covers all known ambiguous classification cases. If you find a new ambiguous case, add it to the Boundary Cases table and the Version History.
- The Exhaustive Example Expansion is a living section. Add new terms as they are encountered during adaptation. Do not remove terms — the expansion must only grow.
- The Unclassified Terms table must remain empty during Stage 4 (adaptation). Terms that cannot be classified during adaptation are a signal that the decision table needs an update. If a term truly has no analogue, defer it to Stage 6 (extension workers).
- Cross-references to dependent skills must be updated when line numbers change due to edits in those files. Run a `search_files` for `category-mapping` across `.agents/skills/` before declaring this file correct.
