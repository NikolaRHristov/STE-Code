# STE-Code — Part 1: Sections 7–9 + General Recommendations

---

## Section 7 — Error Handling and Safety Patterns

### Summary of the rules

**Rule 7.1** Use an applicable word (BREAKING, DEPRECATED, or NOTE) to identify the level of impact.
**Rule 7.2** Start a safety instruction with a clear and accurate command or condition.
**Rule 7.3** Give an explanation to show the risk or possible result.

### Definitions

- **BREAKING:** The reader must know that an API change will break existing consumers.
  Equivalent to WARNING in ASD-STE100 (risk of injury or death).
- **DEPRECATED:** The reader must know that a feature will be removed in a future version.
  Equivalent to CAUTION in ASD-STE100 (risk of damage to objects).
- **NOTE:** Informative context that does not indicate risk.

---

### Rule 7.1 — Identify the level of impact

> **STE-Code:**
> ```
> ## BREAKING: `authenticate()` now requires a `tenantId` parameter
>
> The `authenticate()` method signature changed. You must supply a
> `tenantId` parameter. Existing call sites that do not supply this
> parameter will fail at compile time.
> ```

> **STE-Code:**
> ```
> ## DEPRECATED: `UserService.findByEmail()` is deprecated
>
> Use `UserRepository.search({ email })` instead.
> `findByEmail()` will be removed in version 4.0.0.
> ```

> **STE-Code:**
> ```
> ## NOTE: The default database connection pool size is 10 connections.
> ```

---

### Rule 7.2 — Clear command or condition

> **STE-Code:**
> ```
> ## BREAKING: Update your import paths
>
> The package name changed from `@company/old-auth` to `@company/auth`.
> Update all import statements. If you do not update the imports, your
> application will not compile.
> ```

> **STE-Code:**
> ```
> ## DEPRECATED: Do not use the `/v1/users` endpoint
>
> Use the `/v2/users` endpoint instead. The `/v1/users` endpoint will
> return a 410 Gone status after 2026-01-01.
> ```

---

### Rule 7.3 — Explain the risk or result

> **STE-Code:**
> ```
> ## BREAKING: The default port changed from 8080 to 3000
>
> Update your configuration. If you do not update the port, your
> application will not connect to the service.
> ```

> **STE-Code:**
> ```
> ## BREAKING: `createUser()` now returns a `Result<User, Error>` instead of `User`
>
> Handle the error case in all call sites. If you do not handle the error,
> uncaught exceptions can cause your application to crash.
> ```

---

## Section 8 — Syntax and Formatting

### Summary of the rules

**Rule 8.1** Use all standard English punctuation. Do not use the semicolon (;) in documentation text.
**Rule 8.2** Use hyphens (-) to connect words that are directly related.
**Rule 8.3** Use parentheses for references, identifiers, abbreviations, alternatives, and explanations.
**Rule 8.4** In a vertical list, a colon (:) has the same effect on word count as a period.
**Rule 8.5** Text in parentheses counts as one word.
**Rule 8.6** Count numbers, abbreviations, and quoted text as one word each.
**Rule 8.7** Hyphenated words count as one word.

---

### Rule 8.1 — No semicolon

> **Non-STE-Code:** `// The function returns a Result; it may contain an error.`
> **STE-Code:** `// The function returns a Result. The result can contain an error.`

---

### Rule 8.2 — Hyphens for related words

> **STE-Code:**
> - `request-response cycle`
> - `client-server architecture`
> - `read-only permission`
> - `well-known endpoint`
> - `high-availability cluster`
> - `run-on initialization`

---

### Rule 8.3 — Parentheses usage

Parentheses can be used for:
1. References: `(see auth.go:42)`
2. Identifiers: `UserService.create(user: User) -> Result`
3. Abbreviations: `JSON Web Token (JWT)`
4. Alternatives: `The cache (or "the store")`
5. Explanations: `The timeout (in milliseconds)`

---

### Rules 8.4–8.7 — Word count

**Rule 8.4:** A colon before a vertical list ends the sentence for word-count purposes.
**Rule 8.5:** Parenthetical text counts as one word.
**Rule 8.6:** Count as one word:
- Numbers: `404`, `2024`
- Numbers with units: `500ms`, `2GB`, `64MB`
- Abbreviations: `API`, `JSON`, `JWT`, `HTTPS`
- Alphanumeric identifiers: `UserService`, `auth-middleware`
- Quoted text: `"connection refused"`
- Titles and headings: `## Installation Guide`
- Proper nouns: `GitHub`, `Docker`, `Kubernetes`

**Rule 8.7:** Hyphenated words: `request-response`, `client-server`, `read-only` = one word each.

---

## Section 9 — Coding Practices

### Summary of the rules

**Rule 9.1** Use a different sentence construction when a word-for-word replacement is not sufficient.
**Rule 9.2** Use each approved word correctly.
**Rule 9.3** Do not make phrasal verbs.
**Rule 9.4** Use a consistent style.

---

### Rule 9.1 — Different sentence constructions

When word-for-word replacement fails, restructure the entire sentence.

**Case 1: The alternative changes the meaning.**
> **Non-STE-Code:** `// Just call the init function once.`
> **STE-Code:** `// Call the init function one time only.`
> NOT: `// Immediately call the init function once.` (changes meaning)

**Case 2: The word is not in the vocabulary.**
> **Non-STE-Code:** `// The incidence of null pointer errors is high.`
> **STE-Code:** `// Null pointer errors occur frequently.`

**Case 3: Restructuring for clarity.**
> **Non-STE-Code (1 sentence, 28 words):**
> ```
> // If cracks are detected during inspection, the operator must
> // perform the repair within a certain number of flight hours
> // depending on crack length, refer to following table.
> ```
>
> **STE-Code (4 sentences, short):**
> ```
> // Examine the component for cracks.
> // If you find cracks, use the table to identify the repair interval.
> // The repair interval depends on the crack length.
> // Do the repair within the specified flight hours.
> ```

---

### Rule 9.2 — Use approved words correctly

Restricted meanings in STE-Code:

| Word | Approved Meaning | Not Approved Meaning |
|------|-----------------|---------------------|
| resolve | Determine final value of deferred computation | Fix a bug |
| execute | Run a program or command | Carry out a business plan |
| render | Produce visual output from template | Make or cause to be |
| deploy | Transfer software to a runtime environment | Position military forces |
| mount | Attach a filesystem or component | Climb onto |
| stream | Transfer data continuously | A small river |

> **Non-STE-Code:** `// Render a decision about the architecture.`
> **STE-Code:** `// Make a decision about the architecture.`

---

### Rule 9.3 — No phrasal verbs

> **Non-STE-Code → STE-Code:**
> - `set up the database` → `configure the database`
> - `tear down the test` → `remove the test fixtures`
> - `spin up a server` → `start a server`
> - `fire off a request` → `send a request`
> - `write out the log` → `write the log`
> - `look up the value` → `find the value`
> - `turn off the feature` → `disable the feature`
> - `back up the data` → `create a backup of the data`

Approved exceptions: `log in`, `log out` (restricted to authentication contexts).

---

### Rule 9.4 — Consistent style

> **Non-STE-Code (inconsistent):**
> ```
> 1. Initialize the user service with the database config.
> 2. Create the user record in the DB.
> 3. Set up the user profile in the identity store.
> 4. Return the newly made user object.
> ```
>
> **STE-Code (consistent):**
> ```
> 1. Initialize the UserService with the database configuration.
> 2. Create the user record in the database.
> 3. Create the user profile in the identity store.
> 4. Return the new User object.
> ```

---

## General Recommendations

### GR-1 — The conjunction "that"

Use "that" after verbs like `make sure`, `verify`, `confirm`, `ensure` to remove ambiguity.

> **Do not write:** `// Make sure the connection is open.`
> **Write:** `// Make sure that the connection is open.`

### GR-2 — The preposition "with"

"With" has three approved meanings: association, means, and accompaniment. Avoid ambiguity.

> **Do not write:** `// Deploy the application with Docker.` (ambiguous — using Docker? alongside Docker?)
> **Write:** `// Use Docker to deploy the application.`

### GR-3 — How to use pronouns

If a pronoun can refer to multiple nouns, replace it with the specific noun.

> **Do not write:** `// If the cache is full and the queue is empty, it will block.`
> **Write:** `// If the cache is full and the queue is empty, the cache will block.`

### GR-4 — The pronoun "this"

Always follow "this" with the noun it refers to.

> **Do not write:** `// If the token is expired, this causes an error.`
> **Write:** `// If the token is expired, this expiration causes an error.`

### GR-5 — False friends

Words that look similar but have different meanings in code contexts:

| Word | Code Meaning | Non-Code Meaning |
|------|-------------|-----------------|
| class | Object-oriented programming construct | Category or quality |
| interface | Type definition or contract | Boundary between systems |
| argument | Function parameter | Disagreement |
| package | Software distribution unit | Wrapped item |
| library | Collection of reusable code | Building with books |

### GR-6 — Latin abbreviations

Do not use `e.g.`, `i.e.`, `etc.` Use English words:

- `e.g.` → `for example`
- `i.e.` → `that is`
- `etc.` → `and so on` or omit

### GR-7 — Inclusive language

Use gender-neutral terms. Do not use `guys`, `he/she`, `man-hours`.
Use `they`, `team members`, `person-hours`.

### GR-8 — Possessive form

Avoid the Saxon genitive (`'s`) for inanimate objects in formal documentation.

> **Non-STE-Code:** `// The function's return value is a Promise.`
> **STE-Code:** `// The return value of the function is a Promise.`
