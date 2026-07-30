# Category Mapping: STE → STE-Code

> CORRECTED: ASD-STE100 Issue 9 has exactly **19** technical noun categories,
> not 22. The previous version incorrectly claimed 22 categories.

## Version History

| Date | Author | Change | Rationale |
|------|--------|--------|-----------|
| 2025-07-30 | Agent #3 (Auditor) | Corrected count from 22 to 19 | Audit verified Issue 9 pages 47-52 contain exactly 19 categories. Categories 20-22 did not exist in the specification. Source: extraction pages `page-0047.md` through `page-0052.md`. |
| 2025-07-29 | Agent #2 (Refiner) | Initial mapping | Original mapping incorrectly used 22 categories from an earlier draft. |

NOTE: The 22-category version was an error. No Issue of ASD-STE100 has 22 technical noun categories. Always verify against the extraction artifacts at `ste-code/extracted/`.

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

## Category Conflict Resolution

Some terms fit more than one category. Use this priority chain to resolve conflicts:

1. **Most specific role wins.** Assign the term to the category that describes its primary code-domain function.
2. **Deployment concern over framework concern.** If a term is both a framework and a deployment target, Category 5 (Deployment targets) takes priority over Category 2 (Frameworks).
3. **Protocol concern over deployment concern.** If a term is both a deployment target and a network protocol, Category 19 (Network/I/O terms) takes priority over Category 5.
4. **Algorithmic concern over general IT.** If a term describes an algorithm or computational structure, Category 7 (Algorithmic terms) takes priority over Category 19.

### Conflict Resolution Matrix

| Conflicting Categories | Priority | Example | Why |
|------------------------|----------|---------|-----|
| 2 vs 5 | 5 (Deployment) | `Docker` → Category 5 | Deployment is its primary code-domain role. |
| 5 vs 19 | 19 (Network) | `AWS Lambda` → Category 19 | Its primary role is a network-accessible compute service. |
| 6 vs 11 | 6 (Modules/Services) | `AuthModule` → Category 6 | It is a code component before it is an actor. |
| 7 vs 19 | 7 (Algorithmic) | `hash` → Category 7 | It is a computational term before a data operation. |
| 8 vs 19 | 19 (Network) | `proxy` → Category 19 | `proxy` as network intermediary takes priority over routing. |
| 14 vs 18 | 14 (Diagnostics) | `race condition` → Category 14 | Diagnostics describe the state. Category 18 describes the damage. |
| 16 vs 14 | 16 (Conditions) | `degraded` → Category 16 | It is a runtime condition before a diagnostic term. |

## Known Limitations

- **AWS service names straddle three categories.** Terms such as `S3`, `Lambda`, and `EC2` fit Category 2 (Frameworks), Category 5 (Deployment targets), and Category 19 (Network protocols). Classify under Category 5 if primarily a deployment concern. Classify under Category 19 if primarily a network protocol. Document the rationale in the term entry.
- **`proxy` and `gateway` are assigned to Category 19.** Workers sometimes map these terms to Category 8 (Routing) because of URL path associations. Category 19 is correct because network I/O is their primary role.
- **`cache` appears in both Category 7 and Category 16.** Category 7 covers cache as a data structure (algorithmic). Category 16 covers cache as a runtime state (`warm cache`, `cold cache`). Choose based on context.
- **Only Category 4 has explicit unapproved annotations.** The `left-pad` and `is-odd` pattern mirrors the STE treatment of consumable materials that have approved alternatives. This pattern can extend to other categories. It has not been applied to Categories 2, 3, or 19 yet.
- **Category 4 (unwanted material) maps imperfectly to dependencies.** In STE, "unwanted material" refers to waste, debris, and contaminants. In STE-Code, this maps to unapproved or deprecated dependencies. The analogy is sound but the mapping is not one-to-one.

## Design Rationale: Unapproved Examples in Category 4

Category 4 includes `left-pad` and `is-odd` as unapproved examples. This mirrors the STE treatment of consumable materials that have approved alternatives. In the code domain:

- `left-pad` is a dependency that implements a built-in language feature. Use `String.prototype.padStart()` instead.
- `is-odd` is a dependency that replaces a one-line expression. Use `n % 2 !== 0` instead.

This pattern applies to any category where a term has a simpler, more standard alternative. Future work should add unapproved examples to:

- Category 2: frameworks with known lighter alternatives (for example, `moment.js` when `date-fns` is preferred)
- Category 3: tools replaced by built-in alternatives (for example, `gulp` when `npm scripts` or `Makefile` can replace it)
- Category 19: deprecated protocols (for example, `FTP` when `SFTP` or `HTTPS` is preferred)

## Cross-References

| Reference | File | Description |
|-----------|------|-------------|
| Adapted category rules | `ste-code/adapted/a-categories.md` | Full text of Rule 1.5 through Rule 1.9 adapted for the code domain. |
| Section type definitions | `.agents/references/section-types.md` | Extraction instructions for pages 47-52 (section type: CATEGORIES). |
| Worker prompt: categories | `.agents/prompts/adapt-categories.md` | Prompt that guides workers through the 19-category mapping during adaptation. |
| Quality checklist | `.agents/references/quality-checklist.md` | Rail 3 (Category Coverage) verifies all 19 categories appear in output. |
| Audit report | `.agents/audit/execution-report.md` | Audit that discovered the 22→19 correction. |
| Extraction source | `ste-code/extracted/page-0047.md` through `page-0052.md` | Raw extraction of spec pages containing the 19 category definitions. |
| Benchmark suite | `.agents/benchmark/` | 59 tests across 14 STE-Code categories, including category-mapping accuracy checks. |

## Verification

Use these commands to verify the category count and content:

```bash
# Count unique category definitions in extracted pages
grep -c "^### Category" ste-code/extracted/page-004*.md

# Verify all 19 categories appear in this mapping
grep -c "^| [0-9]" .agents/references/category-mapping.md

# Confirm no categories 20-22 exist in the extraction
grep -rn "Category 2[0-2]" ste-code/extracted/ || echo "None found — correct"

# List all category headers from the adapted rules
grep "^## Category" ste-code/adapted/a-categories.md
```

## Common Anti-Patterns

These errors occur frequently in worker output. Use this table to correct them.

| Incorrect Mapping | Correct Category | Rationale |
|-------------------|------------------|-----------|
| `queue` → Category 8 (Routing) | `queue` → Category 19 (Network/I/O) | `queue` is a data structure and I/O mechanism, not a path or route. |
| `proxy` → Category 8 (Routing) | `proxy` → Category 19 (Network/I/O) | `proxy` is a network intermediary. See the conflict resolution matrix. |
| `middleware` → Category 19 | `middleware` → Category 8 (Routing) | `middleware` intercepts request paths. It is a routing concern. |
| `CDN` → Category 6 (Services) | `CDN` → Category 11 (Actors) or Category 5 (Deployment) | `CDN` is a deployment infrastructure term, not a code component. |
| `router` → Category 19 | `router` → Category 8 (Routing) | `router` matches URL paths to handlers. It is a routing term. |
| `status code` → Category 14 (Diagnostics) | `status code` → Category 9 (Numbers/Formats) | HTTP status codes are numeric format tokens (`200 OK`, `404 Not Found`). |
| `config` → Category 15 (Documents) | `config` → Category 13 (Configuration files) | `config` is a preference/settings concept, not a specification document. |
| `health check` → Category 18 (Damage) | `health check` → Category 14 (Diagnostics) | Health checks diagnose state. Damage terms describe failure outcomes. |
