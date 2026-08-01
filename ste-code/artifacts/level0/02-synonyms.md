# Level 0 — Technical Noun Categories (Rule 1.5)

This is the Rule 1.5 slice of STE-Code Level 0: the **code-domain technical noun
categories**. It is the "approved-word / synonym table" for Level 0 — the short,
deterministic list of domain-specific terms you may use outside the approved-word
dictionary.

Everything below is faithful to the STE-Code standard. No categories or terms are
invented. Examples stay inside the code domain (no aerospace or other subject-field
leakage).

Rule 1.5 is the **gateway for all domain-specific vocabulary**. The approved-word
dictionary (Rule 1.1) cannot list every project's nouns, so STE-Code permits a word
outside the dictionary *only* when it names a precise concept in one of the nineteen
categories below. Use an approved word whenever one exists; use a code-domain
technical noun only when no approved word names the concept.

---

## How the gate works

A word is allowed in STE-Code documentation if it is **one** of:

1. **An approved word** — listed in the controlled terminology (Rule 1.1).
2. **A code-domain technical noun** — a word that fits at least one of the
   nineteen categories below and is registered in your project glossary (Rule 1.5).
3. **A code-domain technical verb** — a verb in the technical-verb category
   (Rule 1.12).

Any word that is none of these is **forbidden** by Rule 1.6. There is no fourth
category.

> Non-STE: The developer used the thing to get data from the storage layer and put it on the screen.
> STE: The frontend developer used the API client to get data from the database and show it on the UI.
> (`frontend developer` = category 11, `API client` = category 16, `database` = category 18, `UI` = category 8 — each names a precise concept.)

---

## The 19 Code-Domain Technical Noun Categories

The terms listed under each category are **examples only** — Rule 1.5 does not give
a full list. A word belongs in a category if it names a precise software concept.
Register every project-specific noun in your glossary before using it.

### 1. Code components, modules, and libraries
Software parts, packages, and reusable units of code.
`class`, `controller`, `helper`, `hook`, `middleware`, `mixin`, `module`, `package`, `plugin`, `provider`, `repository`, `service`, `utility`

### 2. Computing devices and their components
Hardware, devices, and physical computing resources.
`CPU`, `disk`, `GPU`, `keyboard`, `laptop`, `memory`, `monitor`, `mouse`, `printer`, `screen`, `server`, `smartphone`, `tablet`, `terminal`

### 3. Development tools, environments, and support equipment
Development tools, IDEs, build systems, and testing frameworks.
`CLI`, `compiler`, `debugger`, `Docker`, `editor`, `IDE`, `Git`, `Jest`, `linter`, `loader`, `Prettier`, `terminal`, `test runner`, `TypeScript`, `webpack`

### 4. Data structures, types, and formats
Data representation, storage structures, and file formats.
`array`, `boolean`, `buffer`, `CSV`, `enum`, `hash map`, `integer`, `JSON`, `linked list`, `object`, `queue`, `stack`, `string`, `struct`, `tree`, `tuple`, `XML`, `YAML`

### 5. Infrastructure, deployment, and platforms
Hosting, deployment, containerization, and runtime platforms.
`AWS`, `CI/CD`, `container`, `deployment`, `Heroku`, `Kubernetes`, `load balancer`, `Node.js`, `pipeline`, `pod`, `production`, `staging`, `Vercel`

---

### 6. Systems, subsystems, and architectural components
System design, architecture patterns, and their parts.
`API gateway`, `authentication layer`, `caching layer`, `client`, `database layer`, `message broker`, `microservice`, `proxy`, `rate limiter`, `REST API`, `routing layer`, `server`, `WebSocket`

### 7. Mathematical, algorithmic, and scientific terms
Algorithms, computational concepts, and mathematical formulas.
`Big O notation`, `binary search`, `coefficient`, `complexity`, `exponent`, `hash function`, `iteration`, `logarithm`, `matrix`, `recursion`, `regex`, `sorting algorithm`, `time complexity`, `traversal`

### 8. Interface elements and navigation
UI components, navigation controls, and layout elements.
`button`, `checkbox`, `dialog`, `dropdown`, `footer`, `header`, `menu`, `modal`, `navigation bar`, `radio button`, `scrollbar`, `sidebar`, `tab`, `text field`, `toggle`, `tooltip`

### 9. Numbers, units of measurement, and time
Quantitative data, measurements, and time-related information.
`byte`, `gigabyte (GB)`, `hertz (Hz)`, `hour (h)`, `kilobyte (KB)`, `megabyte (MB)`, `millisecond (ms)`, `minute`, `nanosecond (ns)`, `second (s)`, `terabyte (TB)`

### 10. Quoted text
Texts you cannot change in code documentation — error messages, code snippets, UI labels, log output.
`Cannot read properties of undefined`, `ENOENT: no such file or directory`, `Submit` button, `404 Not Found`, `connection refused`

---

### 11. Professional roles, teams, and organizations
Roles, individuals, organizations, and teams related to software development.
`administrator`, `backend developer`, `contributor`, `DevOps engineer`, `frontend developer`, `Google`, `maintainer`, `Microsoft`, `product owner`, `QA engineer`, `reviewer`, `scrum master`, `user`

### 12. Official documents, API references, and standards
Documentation types, standards, specifications, and their structural parts.
`API reference`, `changelog`, `code of conduct`, `contributing guide`, `diagram`, `figure`, `Getting Started guide`, `HTTP specification`, `note`, `paragraph`, `README`, `release notes`, `RFC`, `section`, `table`, `warning`

### 13. Runtime environments and operational conditions
Execution contexts, environment variables, and operating parameters.
`development`, `environment variable`, `garbage collection`, `heap`, `hot reload`, `live reload`, `memory leak`, `production`, `sandbox`, `stack trace`, `staging`, `test`, `thread`, `timeout`, `virtual machine`

### 14. Colors
Colors that identify color-related properties in code (CSS, terminal output, syntax highlighting).
`black`, `blue`, `cyan`, `gray`, `green`, `magenta`, `orange`, `red`, `white`, `yellow`
Colors are adjectives, but STE-Code identifies them as code-domain technical nouns. Comparative and superlative forms (for example, `blacker`, `the reddest`) are not permitted.

### 15. Defects, errors, and fault terminology
Types of software defects, errors, and malfunctions.
`assertion failure`, `bug`, `crash`, `deadlock`, `defect`, `exception`, `hang`, `infinite loop`, `memory leak`, `null pointer`, `race condition`, `regression`, `stack overflow`, `timeout`, `type error`

---

### 16. Computer science, information, and communication technology
Concepts, technologies, and architectures in computing and communication.
`AI`, `algorithm`, `authentication`, `authorization`, `blockchain`, `containerization`, `cryptography`, `database`, `encoding`, `encryption`, `firewall`, `hashing`, `internet`, `machine learning`, `metadata`, `neural network`, `protocol`, `query`, `sandbox`, `schema`, `token`, `virtualization`

### 17. Legal and licensing terms
Software licenses, legal documents, and compliance terminology.
`Apache 2.0`, `BSD license`, `compliance`, `copyright`, `GPL`, `license`, `MIT license`, `open source`, `proprietary`, `terms of service`, `third-party`, `trademark`, `warranty`

### 18. Database and storage terminology
Database concepts, storage systems, and data persistence.
`connection pool`, `cursor`, `foreign key`, `index`, `migration`, `NoSQL`, `ORM`, `PostgreSQL`, `primary key`, `query`, `Redis`, `relation`, `row`, `schema`, `seed`, `SQL`, `SQLite`, `stored procedure`, `table`, `transaction`, `view`

### 19. Network and protocol terminology
Networking concepts, protocols, and communication.
`DNS`, `endpoint`, `HTTP`, `HTTPS`, `IP address`, `localhost`, `middleware`, `packet`, `port`, `request`, `response`, `route`, `socket`, `SSH`, `TCP`, `TLS`, `UDP`, `URL`, `VPN`, `WebSocket`

---

## Using the categories (gateway rules)

- **Use an approved word whenever one exists.** A technical noun is the *exception*,
  not the default. Reach for `use`, not a jargon synonym, when an approved word fits.
- **Register every technical noun in your project glossary** before you use it. The
  glossary entry must give the term, its category or categories, its approved meaning
  in context, and an example sentence.
- **Use each noun only with its registered meaning** (Rule 1.3) and only as a noun or
  noun modifier (Rule 1.2). Do not turn a technical noun into a verb (Rule 1.7).
- **Prefer short, standard terms** (Rules 1.8, 1.9). Do not invent a new term when a
  standard one exists, and do not use regional or slang words as technical nouns
  (Rule 1.10).
- **One concept, one term** (Rule 1.11). If the README says `auth middleware`, the API
  reference and docstrings must say `auth middleware` — not `auth layer`.

The terms in each category are examples only. Rule 1.5 does not give a full list of
all possible code-domain technical nouns. When a term is a literal identifier, API
name, or exact string from code (a class name, function name, environment variable, or
error message), show it in backticks — for example, `UserRepository`, `NODE_ENV`,
`"404 Not Found"`.

These nineteen categories, together with the fourteen core principles and the
dictionary excerpt, complete the Level 0 slice. They are the deterministic base from
which higher tiers build.
