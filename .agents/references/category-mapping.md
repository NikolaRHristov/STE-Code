# Category Mapping: STE → STE-Code

> CORRECTED: ASD-STE100 Issue 9 has exactly **19** technical noun categories,
> not 22. The previous version incorrectly claimed 22 categories.

## Version History

| Date | Author | Change | Rationale |
|------|--------|--------|-----------|
| 2025-07-30 | Agent #6 (STE-Code Analysis) | Added decision guide, category grouping taxonomy, worker training anti-patterns, writing guidance, and edge case deep-dives | Maturity audit found missing operational guidance for workers beyond the conflict matrix. Added 6 new sections. |
| 2025-07-30 | Agent #3 (Auditor) | Corrected count from 22 to 19 | Audit verified Issue 9 pages 47-52 contain exactly 19 categories. Categories 20-22 did not exist in the specification. Source: extraction pages `page-0047.md` through `page-0052.md`. |
| 2025-07-29 | Agent #2 (Refiner) | Initial mapping with 22 categories (INCORRECT) | Original mapping used 22 categories from an earlier draft. Categories 20-22 were fabricated: "Security terms" (Category 20), "Build artifacts" (Category 21), and "Testing terminology" (Category 22). None exist in Issue 9. |
| 2025-07-28 | Agent #1 (Extractor) | Raw extraction of pages 47-52 | First pass extracted 22 headings. Header "## 20 Security Terms" on page-0052.md was a TOC entry, not a category definition — the extractor misread it as a category. |

NOTE: The 22-category version was an error. No Issue of ASD-STE100 has 22 technical noun categories. Always verify against the extraction artifacts at `ste-code/extracted/`.

## How to Use This Document

This document is the authoritative reference for mapping ASD-STE100 technical noun categories
to the code domain. Workers use it during adaptation, artifact generation, and quality audits.
Readers in three roles use this document:

| Role | Primary Sections | Goal |
|------|-----------------|------|
| Worker (mapping terms) | Category tables, Conflict Resolution Matrix, Edge Case Deep-Dives, Common Anti-Patterns | Assign every code-domain term to exactly one category |
| Auditor (verifying output) | Verification commands, Known Limitations, Worker Training Anti-Patterns | Catch misclassifications before they reach artifacts |
| Author (writing STE-Code docs) | Writing Guidance by Category, Category Grouping Taxonomy | Use approved vocabulary when describing each category |

## Category Grouping Taxonomy

The 19 categories fall into five logical groups. Use these groups to reason about
broad classification before assigning a specific category.

### Group A: Code Structure (Categories 1, 6, 15)
Language primitives, module organization, and specification files that define the codebase.
- Category 1: Language keywords and reserved words — the atoms of code
- Category 6: Modules, classes, components, and services — the molecules
- Category 15: Specification files, configs, and manifests — the blueprints

### Group B: Ecosystem and Tooling (Categories 2, 3, 4, 5)
External frameworks, tools, dependencies, and deployment surfaces.
- Category 2: Frameworks, runtimes, and platforms — what code runs on
- Category 3: Development tools and build systems — what builds and checks code
- Category 4: Dependencies, packages, and libraries — what code consumes
- Category 5: Deployment targets and environments — where code lands

### Group C: Data and Algorithms (Categories 7, 9, 19)
Computational concepts, formats, and I/O mechanisms.
- Category 7: Algorithmic and computational terms — how code processes data
- Category 9: Data sizes, time units, and numeric formats — how code measures
- Category 19: Network, protocol, API, and I/O terms — how code communicates

### Group D: Behavior and State (Categories 8, 14, 16, 18)
Navigation, runtime conditions, diagnostics, and failure modes.
- Category 8: Routing, pathing, and state management — how code navigates
- Category 14: Error states, diagnostics, and health checks — how code reports problems
- Category 16: Runtime conditions, states, and feature flags — how code behaves under load
- Category 18: Bug, defect, failure, and degradation taxonomy — how code breaks

### Group E: Human and Surface Concerns (Categories 10, 11, 12, 13, 17)
User-visible output, roles, interaction, preferences, and presentation.
- Category 10: String literals, error messages, and log output — what code says
- Category 11: Roles, teams, services, and actors — who uses code
- Category 12: UI/UX interaction and accessibility terms — how users touch code
- Category 13: Configuration and preference files — how users customize code
- Category 17: Terminal colors and syntax highlighting themes — how code looks

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
5. **Runtime condition over diagnostic term.** If a term describes a state the system can be in, Category 16 (Runtime conditions) takes priority over Category 14 (Diagnostics).
6. **Diagnostic over damage.** If a term describes detecting a problem (not the problem itself), Category 14 (Diagnostics) takes priority over Category 18 (Damage).

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
| 2 vs 3 | 2 (Frameworks) | `Next.js` → Category 2 | It is a framework that happens to include build tooling, not a standalone build tool. |
| 4 vs 2 | 4 (Dependencies) | `express` → Category 4 | It is consumed as a package, even though it is also a framework. The dependency relationship is primary. |
| 15 vs 13 | 15 (Documents) | `Makefile` → Category 15 | It is a specification of build rules, not a user preference file. |
| 13 vs 15 | 13 (Preferences) | `.env` → Category 13 | It is user-authored configuration, not a project specification document. |
| 9 vs 19 | 9 (Formats) | `200 OK` → Category 9 | It is a numeric-and-text format token. The protocol that carries it belongs in Category 19. |
| 10 vs 14 | 10 (Literals) | `Error: timeout` → Category 10 | It is a quoted string literal. Its diagnostic meaning is secondary to its form as text output. |
| 5 vs 11 | 5 (Deployment) | `Vercel` → Category 5 | It is an infrastructure target. The team that operates it is incidental. |
| 11 vs 5 | 11 (Actors) | `CI pipeline` → Category 11 | It acts on behalf of a team. The infrastructure is incidental. |

### Decision Guide for Category Assignment

When a term fits more than one category, answer these questions in order:

1. **Is it a word the language parser recognizes?** → Category 1
2. **Is it a quoted string literal or log message?** → Category 10
3. **Is it a number with a unit or format?** → Category 9
4. **Is it a path, URL, or route pattern?** → Category 8
5. **Is it a color or terminal attribute?** → Category 17
6. **Is it a network protocol or I/O mechanism?** → Category 19
7. **Is it an algorithm, data structure, or complexity class?** → Category 7
8. **Is it a deployment target or environment name?** → Category 5
9. **Is it a file that configures or specifies?** → Category 13 (user prefs) or 15 (project specs)
10. **Is it a named code component (class, module, service)?** → Category 6
11. **Is it a role, team, or organizational actor?** → Category 11
12. **Is it a UI element or accessibility term?** → Category 12
13. **Is it a runtime condition or feature flag?** → Category 16
14. **Is it a diagnostic term (describes detecting a problem)?** → Category 14
15. **Is it a damage term (describes the problem itself)?** → Category 18
16. **Is it a framework or runtime?** → Category 2
17. **Is it a development tool?** → Category 3
18. **Is it a dependency or library?** → Category 4

If none of the above apply, the term is probably not a technical code noun and should
use standard STE approved vocabulary instead.

## Edge Case Deep-Dives

These terms appear frequently in code documentation and cause persistent classification
errors. Each entry gives the correct category, the wrong categories workers choose,
and the reasoning.

### `Docker`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 5 (Deployment targets) | Category 2 (Frameworks), Category 3 (Tools) | Docker's primary role is providing a deployment surface (container runtime). It is not a framework your code imports, and it is not a build tool — it is where your code runs. The `Dockerfile` belongs in Category 15. |

### `Kubernetes`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 5 (Deployment targets) | Category 2 (Frameworks), Category 19 (Network) | Kubernetes orchestrates deployment. Its networking layer (`kube-proxy`, `CNI`) is Category 19, but the platform itself is Category 5. |

### `nginx`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 5 (Deployment targets) | Category 19 (Network), Category 3 (Tools) | nginx is a deployment surface (reverse proxy server). It handles network traffic, but its role is infrastructure hosting, not a protocol. |

### `GraphQL`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 19 (Network/I/O) | Category 2 (Frameworks), Category 7 (Algorithmic) | GraphQL is a query protocol and API specification. It is not a framework (Apollo and Relay are the frameworks) and it is not an algorithm. |

### `Redis`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 2 (Frameworks/Runtimes) | Category 19 (Network), Category 5 (Deployment) | Redis is a data structure server — a runtime your code connects to. It is not a protocol (RESP is the protocol, Category 19) and it is not a deployment target on its own. |

### `JWT` (JSON Web Token)

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 9 (Formats) | Category 19 (Network), Category 11 (Actors) | JWT is a token format with a defined structure (header.payload.signature). It is not a protocol and it is not an actor. |

### `OAuth`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 19 (Network/I/O) | Category 11 (Actors), Category 9 (Formats) | OAuth is an authorization protocol. It is not an actor (the OAuth provider is Category 11) and it is not a format (the token format is Category 9). |

### `Webpack`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 3 (Dev tools) | Category 2 (Frameworks), Category 4 (Dependencies) | webpack is a build tool. It processes source files but your application does not depend on it at runtime — it is a devDependency, which is a tool, not a library. |

### `CI/CD`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 11 (Actors) or Category 5 (Deployment) | Category 3 (Tools) | Context determines this. `CI pipeline` that acts on behalf of a team is Category 11. `CD` as a deployment target concept is Category 5. Never Category 3 — CI/CD is not a tool you run locally. |

### `YAML`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 9 (Formats) | Category 15 (Documents), Category 13 (Preferences) | YAML is a data serialization format. Files that use YAML (such as `docker-compose.yaml`) belong in Category 15, but the format itself is Category 9. |

### `console.log`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 10 (String literals) | Category 19 (I/O), Category 3 (Tools) | `console.log` as an expression that produces string output is Category 10. The console I/O mechanism is Category 19, but the literal output is what matters for documentation purposes. |

### `middleware`

| Correct | Wrong Choices | Reasoning |
|---------|---------------|-----------|
| Category 8 (Routing) | Category 19 (Network), Category 6 (Components) | Middleware intercepts request paths in a routing pipeline. It is a routing concept, not a network protocol and not a standalone component. |

## Known Limitations

- **AWS service names straddle three categories.** Terms such as `S3`, `Lambda`, and `EC2` fit Category 2 (Frameworks), Category 5 (Deployment targets), and Category 19 (Network protocols). Classify under Category 5 if primarily a deployment concern. Classify under Category 19 if primarily a network protocol. Document the rationale in the term entry.
- **`proxy` and `gateway` are assigned to Category 19.** Workers sometimes map these terms to Category 8 (Routing) because of URL path associations. Category 19 is correct because network I/O is their primary role.
- **`cache` appears in both Category 7 and Category 16.** Category 7 covers cache as a data structure (algorithmic). Category 16 covers cache as a runtime state (`warm cache`, `cold cache`). Choose based on context.
- **Only Category 4 has explicit unapproved annotations.** The `left-pad` and `is-odd` pattern mirrors the STE treatment of consumable materials that have approved alternatives. This pattern can extend to other categories. It has not been applied to Categories 2, 3, or 19 yet.
- **Category 4 (unwanted material) maps imperfectly to dependencies.** In STE, "unwanted material" refers to waste, debris, and contaminants. In STE-Code, this maps to unapproved or deprecated dependencies. The analogy is sound but the mapping is not one-to-one.
- **Categories 14 and 18 overlap on `race condition`.** Category 14 is correct when documenting how to detect a race condition. Category 18 is correct when documenting the damage a race condition causes. The same term can legitimately appear in both categories depending on the documentation context.
- **Category 8 and Category 19 conflict on networking terms in URL context.** `/api/users` is clearly Category 8 (a path). But `https://api.example.com/users` is a URL that straddles routing (the path) and networking (the protocol). Decompose: the protocol part (`https://`) → Category 19, the path part (`/users`) → Category 8.
- **Category 11 and Category 6 overlap on service names.** `UserService` is Category 6 (a code component). `auth service` is Category 11 (an organizational actor). The capitalization and naming convention often signal which is correct: PascalCase → Category 6, lowercase descriptive phrase → Category 11.

## Design Rationale: Unapproved Examples in Category 4

Category 4 includes `left-pad` and `is-odd` as unapproved examples. This mirrors the STE treatment of consumable materials that have approved alternatives. In the code domain:

- `left-pad` is a dependency that implements a built-in language feature. Use `String.prototype.padStart()` instead.
- `is-odd` is a dependency that replaces a one-line expression. Use `n % 2 !== 0` instead.

This pattern applies to any category where a term has a simpler, more standard alternative. Future work should add unapproved examples to:

- Category 2: frameworks with known lighter alternatives (for example, `moment.js` when `date-fns` is preferred)
- Category 3: tools replaced by built-in alternatives (for example, `gulp` when `npm scripts` or `Makefile` can replace it)
- Category 19: deprecated protocols (for example, `FTP` when `SFTP` or `HTTPS` is preferred)

### Criteria for Marking a Term as Unapproved

A term qualifies for the unapproved annotation when ALL of these conditions are true:

1. The term refers to a real technology in active or historical use.
2. A simpler, more standard alternative exists and is widely adopted.
3. The alternative does not add a new dependency or tool.
4. The documentation's audience benefits from knowing the alternative.

Do NOT mark a term as unapproved when:

- The term is deprecated but has no standard replacement.
- The alternative is subjective or contested in the community.
- The term is the standard in a specific ecosystem despite having alternatives elsewhere.

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
| Adapted dictionary | `ste-code/adapted/a-dictionary.md` | Full 5,943-line approved word dictionary. Use to verify non-technical nouns. |
| Worker grid | `.agents/references/worker-grid.md` | Worker role assignments, batch sizes, and category coverage expectations. |
| Pipeline state | `.agents/state/` | Current progress of category mapping across adaptation stages. |

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

# Count how many times each category appears in adapted output
for i in $(seq 1 19); do
  count=$(grep -c "Category $i" ste-code/adapted/*.md 2>/dev/null || echo 0)
  echo "Category $i: $count references"
done

# Find terms NOT yet assigned to any category
grep -r "TECHNICAL_NOUN" ste-code/adapted/ | grep -v "Category" | head -20
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
| `async` → Category 19 (I/O) | `async` → Category 1 (Keywords) | `async` is a language keyword in JavaScript, Python, Rust, and C#. It is not an I/O term. |
| `Promise` → Category 6 (Components) | `Promise` → Category 1 (Keywords) | `Promise` is a built-in language type in JavaScript. It is not a user-defined component. |
| `JSON` → Category 10 (Literals) | `JSON` → Category 9 (Formats) | JSON is a data interchange format, not a string literal. The string `'{"key":"value"}'` is Category 10. |

## Worker Training Anti-Patterns

These cognitive biases cause workers to misclassify terms. Train workers to recognize
and correct these patterns.

| Bias | Symptom | Correction |
|------|---------|------------|
| **Familiarity bias** | Worker assigns terms to the category they use most often. A backend developer puts everything in Category 19. A frontend developer puts everything in Category 12. | Use the Decision Guide. Do not trust instinct. |
| **Recency bias** | Worker assigns a term to the last category they read about. After reading Category 8, every term looks like a route. | Pause between categories. Check the full 19-category table before assigning. |
| **Compound-term flattening** | Worker treats `AWS Lambda` as one term and picks one category. | Decompose compound terms: `AWS` (Category 5) + `Lambda` (Category 19). Each part gets its own category. |
| **Framework-as-default** | Worker assigns any unfamiliar technology to Category 2 (Frameworks). | If you do not know what the term is, look it up before assigning. Guessing creates Category 2 bloat. |
| **Tool-vs-dependency confusion** | Worker cannot distinguish Category 3 (Tools) from Category 4 (Dependencies). | Rule: if the term is listed in `devDependencies` and never imported at runtime, it is Category 3. If it is in `dependencies` and imported, it is Category 4. |
| **Actors-vs-components confusion** | Worker assigns all named entities to Category 6 (Components). | Rule: if the entity has a login, permission, or human role, it is Category 11. If it is a code construct, it is Category 6. |
| **Error-as-damage bias** | Worker assigns all error terms to Category 18 (Damage). | Rule: an error message or status code is Category 10 or 9. An error state is Category 14. Only the harmful outcome itself is Category 18. |
| **Format blindness** | Worker overlooks Category 9 entirely. Numeric tokens, timeouts, and serialization formats go unclassified. | Category 9 is the catch-all for anything with a number, unit, or structured representation. Check it before falling back to "no category." |

## Writing Guidance by Category

When writing STE-Code documentation that mentions terms from each category,
use the approved vocabulary patterns below.

### Category 1: Language Keywords

Use: `the <keyword> keyword`, `the <keyword> statement`, `the <keyword> expression`.
Do NOT use: `the <keyword> function`, `the <keyword> command`.

Example: "The `if` statement controls conditional execution. The `return` keyword exits the function."

### Category 2: Frameworks and Runtimes

Use: `the <name> framework`, `the <name> runtime`, `the <name> platform`.
Do NOT use: `the <name> library`, `the <name> tool`.

Example: "The React framework renders components. The Node.js runtime executes JavaScript."

### Category 3: Development Tools

Use: `the <name> tool`, `the <name> build system`, `the <name> formatter`.
Do NOT use: `the <name> framework`, `the <name> service`.

Example: "The webpack tool bundles modules. The eslint tool checks code style."

### Category 4: Dependencies

Use: `the <name> package`, `the <name> library`, `the <name> dependency`.
Do NOT use: `the <name> framework`, `the <name> module` (unless it is a module).

Example: "The lodash library supplies utility functions. Install the express package."

### Category 5: Deployment Targets

Use: `the <name> environment`, `the <name> target`, `the <name> platform`.
Do NOT use: `the <name> server` (unless it is a server), `the <name> service`.

Example: "Deploy to the production environment. The Vercel platform hosts static sites."

### Category 6: Modules and Components

Use: `the <Name> module`, `the <Name> component`, `the <Name> service`.
Capitalize the component name. Use the article `the`.

Example: "The UserService module manages authentication. The PaymentGateway component processes transactions."

### Category 7: Algorithmic Terms

Use: `the <term> algorithm`, `the <term> structure`, `the <term> operation`.
Do NOT use: `the <term> function` (conflicts with Category 1), `the <term> method`.

Example: "The hash algorithm maps keys to values. The tree structure organizes data."

### Category 8: Routing and Paths

Use: `the <path> route`, `the <path> endpoint`, `the <name> middleware`.
Enclose paths in backticks. Use the article `the`.

Example: "The `/api/users` route returns user data. The middleware function intercepts requests."

### Category 9: Formats and Units

Use: the numeric value with its unit. Do not separate the number from the unit.
Write: `500ms`, `2GB`, `200 OK`. Do not write: `500 ms`, `2 GB`, `status 200`.

Example: "Set the timeout to `500ms`. The server returns `200 OK`."

### Category 10: String Literals

Use: quoted strings in backticks. Describe them as `the message`, `the string`, `the output`.
Do NOT use: `the error` (conflicts with Category 14), `the log` (ambiguous).

Example: "The message `'connection refused'` indicates a network failure."

### Category 11: Actors and Roles

Use: `the <role> role`, `the <name> provider`, `the <name> pipeline`.
Do NOT use: `the <role> user` (unless describing end users).

Example: "The admin role has full access. The OAuth provider authenticates requests."

### Category 12: UI and Accessibility

Use: `the <element> element`, `the <element> control`, `the <attribute> attribute`.
Follow accessibility naming conventions. Use lowercase for HTML elements.

Example: "The button element triggers the action. The `aria-label` attribute describes the control."

### Category 13: Configuration Files

Use: the filename in backticks. Describe them as `the <name> file`, `the configuration file`.
Do NOT use: `the config` as a standalone noun.

Example: "The `.env` file stores environment variables. Edit the `tsconfig.json` file."

### Category 14: Diagnostics

Use: `the <term> error`, `the <term> state`, `the <term> check`.
Do NOT use: `the <term> bug`, `the <term> failure` (those are Category 18).

Example: "The health check reports service status. The deadlock state blocks progress."

### Category 15: Specification Files

Use: the filename in backticks. Describe them as `the <name> manifest`, `the <name> specification`.
Do NOT use: `the config file` (that is Category 13).

Example: "The `package.json` manifest lists dependencies. The `Dockerfile` specification defines the image."

### Category 16: Runtime Conditions

Use: `the <condition> state`, `the <condition> condition`, `the <flag> flag`.
Use present tense. Use adjectives as states.

Example: "The degraded state reduces functionality. The feature flag controls the new behavior."

### Category 17: Colors and Themes

Use: the color name in lowercase. Describe terminal attributes with their effect.
Do NOT use: RGB values in documentation text.

Example: "The red color indicates an error. The bold attribute emphasizes the text."

### Category 18: Damage Terms

Use: `the <term> vulnerability`, `the <term> attack`, `the <term> failure`.
Describe the impact, not just the name.

Example: "The XSS vulnerability injects scripts. The SQL injection attack compromises the database."

### Category 19: Network and Protocols

Use: `the <name> protocol`, `the <name> API`, `the <name> connection`.
Version numbers attach directly to the protocol name.

Example: "The HTTP/2 protocol multiplexes streams. The TLS 1.3 connection encrypts traffic."

## Category Coverage Statistics

The benchmark suite tracks how often each category appears in test output.
Use these statistics to identify under-documented categories.

| Category | Benchmark Tests | Typical Doc Frequency | Risk if Missing |
|----------|----------------|----------------------|-----------------|
| 1 (Keywords) | 6 | High | Code examples lack language context |
| 2 (Frameworks) | 5 | Medium | Readers cannot identify the technology stack |
| 3 (Tools) | 4 | Medium | Build and lint instructions are incomplete |
| 4 (Dependencies) | 4 | Medium | Installation instructions are incomplete |
| 5 (Deployment) | 3 | Medium | Readers cannot deploy the software |
| 6 (Components) | 5 | High | Architecture is undocumented |
| 7 (Algorithms) | 3 | Low-Medium | Performance characteristics are unclear |
| 8 (Routing) | 4 | Medium | API structure is unclear |
| 9 (Formats) | 4 | High | Data contracts are undocumented |
| 10 (Literals) | 4 | High | Error messages are undocumented |
| 11 (Actors) | 3 | Low | Access control is unclear |
| 12 (UI/UX) | 3 | Medium | Accessibility is undocumented |
| 13 (Config) | 3 | Medium | Setup instructions are incomplete |
| 14 (Diagnostics) | 3 | Medium | Troubleshooting guide is incomplete |
| 15 (Specs) | 3 | High | Project structure is unclear |
| 16 (Conditions) | 2 | Low | Operational behavior is undocumented |
| 17 (Colors) | 1 | Low | Terminal output format is undocumented |
| 18 (Damage) | 2 | Low | Security posture is unclear |
| 19 (Network) | 4 | Medium | Integration points are undocumented |

Categories 16, 17, and 18 are the most frequently missing from documentation output.
Workers should actively search for opportunities to include terms from these categories.

## When a Term Fits No Category

Some code-domain terms do not fit any of the 19 categories. These terms are
not technical code nouns under STE-Code rules. Handle them as follows:

1. **Use the term as a standard STE approved word.** Check the adapted dictionary
   at `ste-code/adapted/a-dictionary.md`. If the word is approved, use it with its
   approved meaning. Do not enclose it in backticks.

2. **Replace the term with an approved synonym.** Consult the Canonical Synonym Table
   in the STE-Code system prompt. For example, replace `utilize` with `use`.

3. **Reclassify the term as a technical verb.** If the term describes an action
   (build, deploy, test, lint), assign it to one of the 4 verb categories instead
   of the 19 noun categories.

4. **Decompose the term into smaller parts.** A compound term such as
   `continuous integration pipeline` decomposes into `continuous integration`
   (concept — use standard STE words) and `pipeline` (Category 11, actor).

5. **Flag for dictionary extension.** If the term is genuinely a code-domain noun
   that fits none of the 19 categories, add it to the extension backlog. A future
   STE-Code issue may add new categories or expand existing ones.

## Quick Reference Card

Print this section for worker desks or include in prompt context.

```
STE-CODE CATEGORY ASSIGNMENT — 19 noun + 4 verb categories

QUESTION FLOW:
  Parser keyword? → Cat 1    String literal? → Cat 10
  Number+unit? → Cat 9       Path/URL? → Cat 8
  Color/terminal? → Cat 17   Protocol/I/O? → Cat 19
  Algorithm/structure? → Cat 7   Deploy target? → Cat 5
  Config/spec file? → Cat 13 (prefs) or 15 (specs)
  Code component? → Cat 6    Role/team? → Cat 11
  UI element? → Cat 12       Runtime state? → Cat 16
  Diagnostic? → Cat 14       Damage/failure? → Cat 18
  Framework/runtime? → Cat 2   Dev tool? → Cat 3
  Dependency/lib? → Cat 4

TOP CONFLICTS (priority wins):
  Deploy > Framework    (5 > 2)
  Protocol > Deploy     (19 > 5)
  Algorithmic > I/O     (7 > 19)
  Diagnostic > Damage   (14 > 18)
  Condition > Diagnostic (16 > 14)
  Docs > Prefs          (15 > 13)
  Literals > Diagnostic (10 > 14)

MOST COMMON ERRORS:
  queue → Cat 19 NOT 8    proxy → Cat 19 NOT 8
  middleware → Cat 8 NOT 19   router → Cat 8 NOT 19
  status code → Cat 9 NOT 14  config → Cat 13 NOT 15
  health check → Cat 14 NOT 18
  async → Cat 1 NOT 19    Promise → Cat 1 NOT 6
  JSON → Cat 9 NOT 10

VERIFICATION:
  grep -c "^### Category" ste-code/extracted/page-004*.md
  grep -c "^| [0-9]" .agents/references/category-mapping.md
```
