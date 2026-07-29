# Category Mapping: STE → STE-Code

> CORRECTED: ASD-STE100 Issue 9 has exactly **19** technical noun categories,
> not 22. The previous version incorrectly claimed 22 categories.

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

## 4 Technical Code Verb Categories

| # | Category | Description | Example Verbs |
|---|----------|-------------|---------------|
| 1 | Development operations | Build, compile, test, version, deploy | `build`, `compile`, `test`, `lint`, `format`, `commit`, `push`, `deploy`, `rollback` |
| 2 | Data operations | I/O, serialization, persistence, transformation | `read`, `write`, `serialize`, `deserialize`, `parse`, `encode`, `decode`, `query`, `insert`, `migrate` |
| 3 | Application operations | Request handling, state, authentication, scheduling | `handle`, `route`, `authenticate`, `authorize`, `validate`, `schedule`, `dispatch`, `resolve` |
| 4 | Communication operations | Messaging, remote calls, streaming | `send`, `receive`, `publish`, `subscribe`, `stream`, `poll`, `broadcast`, `connect` |

## Verification Notes

- All category names verified against Issue 9 spec pages 47-52 (`page-0047.md` through `page-0052.md` in the extraction)
- All 19 categories confirmed present (no categories 20-22 in Issue 9 — those were from an earlier draft or confusion)
- STE-Code examples use concrete, recognizable software development terms
