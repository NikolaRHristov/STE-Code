# STE-Code — Part 1: Coding Rules

> Adapted from ASD-STE100 Issue 9 (January 2025). Preserves exact rule structure,
> replaces all aerospace examples with code-domain equivalents.

---

## Section 1 — Identifiers and Names

### Summary of the rules

**Which identifiers can you use?**

**Rule 1.1** Use identifiers that are:
- Approved in the STE-Code vocabulary
- Technical Code Nouns
- Technical Code Verbs

**Part of speech**
**Rule 1.2** Use approved vocabulary words only as their specified part of speech.

**Approved meaning**
**Rule 1.3** Use approved words only with their approved meanings.

**Forms of verbs and adjectives**
**Rule 1.4** Use only the approved forms of verbs and adjectives.

**Technical Code Nouns**
**Rule 1.5** You can use words that you can include in a Technical Code Noun category.
**Rule 1.6** Use a word not approved in the vocabulary only when it is a Technical Code Noun or part of one.
**Rule 1.7** Do not use Technical Code Nouns as verbs.
**Rule 1.8** Use Technical Code Nouns approved in your organization, ecosystem, or subject field.
**Rule 1.9** When you must select a Technical Code Noun, use one that is short and easy to understand.
**Rule 1.10** Do not use regional, slang, or jargon words as Technical Code Nouns.
**Rule 1.11** Do not use different Technical Code Nouns for the same item.

**Technical Code Verbs**
**Rule 1.12** You can use verbs that you can include in a Technical Code Verb category.
**Rule 1.13** Do not use Technical Code Verbs as nouns.

**Spelling**
**Rule 1.14** Use American English spelling unless other official directives tell you differently.

---

### Rule 1.1 — Use identifiers that are: approved in the vocabulary, Technical Code Nouns, or Technical Code Verbs.

STE-Code has a controlled vocabulary that provides the words most frequently used in
software documentation. You can also use words not in the vocabulary if you can include
them in the specified categories of Technical Code Nouns and Technical Code Verbs.

A **Technical Code Noun** is a noun term that refers to a specified concept in software
development. A **Technical Code Verb** is a verb term that refers to a specified operation
or process in software development.

*Examples:*
- The word `validate` is an approved verb in the vocabulary.
- The word `UserService` is a Technical Code Noun.
- The word `serialize` is a Technical Code Verb.

> **Non-STE-Code:** The function does the validation of the input and returns the data.
> **STE-Code:** The `validate` function validates the input and returns the data.

---

### Rule 1.2 — Use approved words only as their specified part of speech.

`validate` is approved as a verb. Do not use it as a noun.

> **Non-STE-Code:** Run the validate on the payload.
> **STE-Code:** Validate the payload.

`async` is a Technical Code Noun (category 1: Language keywords). Do not use it as a verb.

> **Non-STE-Code:** Async the database query.
> **STE-Code:** Make the database query asynchronous.

---

### Rule 1.3 — Use approved words only with their approved meanings.

The approved meaning of `resolve` is "determine the final value of a deferred computation."
You cannot use `resolve` to mean "fix a bug."

> **Non-STE-Code:** Resolve the null pointer exception in the payment module.
> **STE-Code:** Fix the null pointer exception in the payment module.

The approved meaning of `execute` is "run a program or command."

> **Non-STE-Code:** Execute the business strategy for Q4.
> **STE-Code:** Implement the business strategy for Q4.

---

### Rule 1.4 — Use only the approved forms of verbs and adjectives.

| Verb | Infinitive | Present | Past | Past Participle |
|------|-----------|---------|------|-----------------|
| DEPLOY | deploy | deploys | deployed | deployed |
| SERIALIZE | serialize | serializes | serialized | serialized |
| VALIDATE | validate | validates | validated | validated |
| RENDER | render | renders | rendered | rendered |
| PARSE | parse | parses | parsed | parsed |
| QUERY | query | queries | queried | queried |

Adjectives use their base form. Comparatives and superlatives with `more`/`most` are
permitted since `more` and `most` are approved words.

| Adjective | Base | Comparative | Superlative |
|-----------|------|-------------|-------------|
| FAST | fast | faster | fastest |
| EFFICIENT | efficient | more efficient | most efficient |

---

### Rule 1.5 — Technical Code Noun Categories (19 categories)

1. **Language keywords and reserved words** — `if`, `else`, `return`, `class`, `async`, `await`, `import`, `export`, `const`, `let`, `var`, `function`, `interface`, `type`, `enum`, `namespace`, `extends`, `implements`, `try`, `catch`, `throw`, `finally`, `yield`, `static`, `public`, `private`, `protected`, `readonly`

2. **Frameworks, runtimes, and platforms** — `React`, `Vue`, `Angular`, `Node.js`, `Deno`, `Docker`, `Kubernetes`, `PostgreSQL`, `Redis`, `MongoDB`, `GraphQL`, `REST`, `gRPC`, `Linux`, `macOS`, `Windows`

3. **Development tools and build systems** — `webpack`, `esbuild`, `vite`, `prettier`, `eslint`, `git`, `npm`, `yarn`, `pnpm`, `cargo`, `pip`, `maven`, `gradle`, `cmake`, `make`

4. **Dependencies, packages, and libraries** — `lodash`, `express`, `axios`, `react-dom`, `pytest`, `serde`, `tokio`, `django`, `flask`, `spring-boot`, `hibernate`

5. **Deployment targets and environments** — `staging`, `production`, `development`, `AWS`, `GCP`, `Azure`, `Vercel`, `Netlify`, `Cloudflare`, `localhost`, `CI/CD pipeline`

6. **Modules, classes, components, and services** — `UserService`, `AuthModule`, `PaymentGateway`, `EventBus`, `Logger`, `CacheManager`, `DatabasePool`, `HttpClient`, `MessageQueue`

7. **Algorithmic and computational terms** — `hash`, `sort`, `bfs`, `dfs`, `binary search`, `O(n)`, `O(log n)`, `tree`, `graph`, `cache`, `LRU`, `FIFO`, `stack`, `queue`, `heap`

8. **Routing, pathing, and state management** — `/api/users`, `/auth/login`, `useNavigate`, `Router`, `middleware`, `redirect`, `redux`, `mobx`, `zustand`, `recoil`

9. **Data sizes, time units, and numeric formats** — `500ms`, `2GB`, `64MB`, `200 OK`, `404 Not Found`, `500 Internal Server`, `64-bit`, `32-bit`, `UTC`, `epoch`, `ISO 8601`, `hex`, `base64`

10. **String literals, error messages, and log output** — `"connection refused"`, `Error: timeout exceeded`, `[ERROR] failed to parse`, `console.log("debug:", value)`

11. **Roles, teams, services, and actors** — `admin`, `moderator`, `viewer`, `editor`, `OAuth provider`, `identity provider`, `CDN`, `load balancer`, `reverse proxy`

12. **UI/UX interaction and accessibility terms** — `button`, `modal`, `dropdown`, `tooltip`, `aria-label`, `focus`, `viewport`, `breakpoint`, `responsive`, `dark mode`, `light mode`

13. **Configuration and preference terms** — `.env`, `.gitignore`, `tsconfig.json`, `settings.py`, `preferences`, `profile`, `theme`, `workspace`

14. **Error states, diagnostics, and health checks** — `NullPointerException`, `StackOverflowError`, `SegmentationFault`, `race condition`, `deadlock`, `memory leak`, `OOM`, `latency spike`, `health check`, `heartbeat`

15. **Specification files, configs, manifests, and schemas** — `package.json`, `Dockerfile`, `docker-compose.yml`, `openapi.yaml`, `Makefile`, `Cargo.toml`, `pyproject.toml`, `README.md`, `CHANGELOG.md`

16. **Runtime conditions, states, and flags** — `cold start`, `warm cache`, `idle`, `under load`, `degraded`, `healthy`, `unhealthy`, `draining`, `feature flag`, `kill switch`

17. **Terminal colors and syntax highlighting** — `red`, `green`, `yellow`, `blue`, `cyan`, `magenta`, `white`, `bold`, `dim`, `italic`, `underline`, `256-color`, `true color`

18. **Bug, defect, failure, and degradation taxonomy** — `crash`, `memory leak`, `race condition`, `deadlock`, `XSS`, `SQL injection`, `CSRF`, `buffer overflow`, `integer overflow`, `data corruption`, `packet loss`, `timeout`, `throttling`

19. **Network, protocol, API, and I/O terms** — `HTTP/1.1`, `HTTP/2`, `HTTP/3`, `WebSocket`, `gRPC`, `TLS 1.3`, `DNS`, `TCP`, `UDP`, `IP`, `SSL`, `OAuth 2.0`, `JWT`, `CORS`, `HSTS`

---

### Rule 1.6 — Technical Code Noun exceptions

A word not approved in the vocabulary can be used if it fits a Technical Code Noun category.

> **Non-STE-Code:** The base function handles all requests.
> **STE-Code:** The primary function handles all requests. *(base → primary)*

But `base` is a Technical Code Noun in `base64` (category 9: Data sizes and numeric formats).

> **STE-Code:** Encode the binary data as base64.

---

### Rule 1.7 — Do not use Technical Code Nouns as verbs

`cache` is a Technical Code Noun (category 6). Do not use it as a verb.

> **Non-STE-Code:** Cache the API response for 60 seconds.
> **STE-Code:** Store the API response in the cache for 60 seconds.

`docker` is a Technical Code Noun (category 2). Do not use it as a verb.

> **Non-STE-Code:** Docker the application for production.
> **STE-Code:** Build a Docker image of the application for production.

---

### Rule 1.8 — Use approved organizational Technical Code Nouns

If your team calls it `PaymentProcessor`, do not call it `PaymentHandler` or `PaymentService`.

> **Non-STE-Code:** The PaymentHandler validates the card and the PaymentService charges it.
> **STE-Code:** The PaymentProcessor validates the card. Then the PaymentProcessor charges the card.

---

### Rule 1.9 — Short, understandable Technical Code Nouns (max 3 words)

> **Non-STE-Code:** `AbstractUserAuthenticationCredentialValidationServiceFactory`
> **STE-Code:** `AuthCredentialFactory` or `CredentialValidator`

---

### Rule 1.10 — No regional, slang, or jargon

> **Non-STE-Code:** The foo service calls the bar baz endpoint.
> **STE-Code:** The notification service calls the webhook endpoint.

> **Non-STE-Code:** Just yeet the old migration and spin up a fresh one.
> **STE-Code:** Remove the old migration. Create a new migration.

---

### Rule 1.11 — Consistent Technical Code Nouns

> **Non-STE-Code:**
> 1. Initialize the UserManager with the config.
> 2. Call the UserService to fetch the profile.
> 3. Update the UserHandler with the new data.
>
> **STE-Code:**
> 1. Initialize the UserService with the configuration.
> 2. Call the UserService to get the profile.
> 3. Update the UserService with the new data.

---

### Rule 1.12 — Technical Code Verb Categories (4 categories)

**1. Development Operations**
a) Build and compilation: `compile`, `link`, `transpile`, `bundle`, `minify`, `optimize`, `tree-shake`
b) Testing: `test`, `assert`, `mock`, `stub`, `spy`, `verify`, `measure coverage`
c) Version control: `commit`, `push`, `pull`, `merge`, `rebase`, `branch`, `tag`, `cherry-pick`, `stash`
d) Deployment: `deploy`, `release`, `rollback`, `scale`, `provision`, `configure`, `orchestrate`

**2. Data Operations**
a) Input/Output: `read`, `write`, `parse`, `emit`, `stream`, `buffer`, `flush`, `seek`
b) Serialization: `serialize`, `deserialize`, `marshal`, `unmarshal`, `encode`, `decode`
c) Persistence: `persist`, `save`, `load`, `query`, `index`, `migrate`, `seed`, `vacuum`
d) Transformation: `map`, `filter`, `reduce`, `transform`, `convert`, `normalize`, `denormalize`

**3. Application Operations**
a) Request handling: `route`, `dispatch`, `handle`, `serve`, `respond`, `redirect`, `forward`
b) State management: `initialize`, `mount`, `unmount`, `hydrate`, `reconcile`, `invalidate`, `subscribe`
c) Authentication: `authenticate`, `authorize`, `sign`, `verify`, `encrypt`, `decrypt`, `hash`
d) Scheduling: `schedule`, `enqueue`, `dequeue`, `retry`, `cancel`, `timeout`, `delay`

**4. Communication Operations**
a) Messaging: `publish`, `subscribe`, `broadcast`, `emit`, `receive`, `acknowledge`, `nack`
b) Remote calls: `request`, `fetch`, `invoke`, `call`, `rpc`, `poll`, `watch`

---

### Rule 1.13 — Do not use Technical Code Verbs as nouns

`deploy` is a Technical Code Verb. Do not use it as a noun.

> **Non-STE-Code:** The deploy failed because of a configuration error.
> **STE-Code:** The deployment failed because of a configuration error.

---

### Rule 1.14 — American English spelling

> **Non-STE-Code:** `colour_scheme`, `initialise`, `authorise`, `behaviour`
> **STE-Code:** `color_scheme`, `initialize`, `authorize`, `behavior`
