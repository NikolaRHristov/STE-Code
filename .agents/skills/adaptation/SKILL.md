# Adaptation Protocol — Stage 4

Transform STE rules into STE-Code (coding domain). Agent-agnostic.

## Input: `ste-code/merged/master.md`
## Output: `ste-code/adapted/` (rule-by-rule STE→STE-Code)

## PRESERVE (unchanged)
- All 53 rule numbers and 9-section organization
- 6-pass transformation pipeline (lexical → classification → POS lock → meaning → grammar → consistency)
- Dictionary architecture: APPROVED (UPPERCASE) vs UNAPPROVED (lowercase)
- 19 Technical Code Noun categories
- 4 Technical Code Verb categories

## REPLACE (adapt for code domain)
- Every STE/non-STE example pair → code documentation examples
- Technical noun categories → code-domain categories
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

## Category Mapping (19 categories)

| # | STE-Code Category | Examples |
|---|-------------------|----------|
| 1 | Language keywords | `if`, `else`, `return`, `class`, `async`, `await` |
| 2 | Frameworks and runtimes | `React`, `Node.js`, `Docker`, `PostgreSQL` |
| 3 | Dev tools and build systems | `webpack`, `eslint`, `git`, `npm`, `cargo` |
| 4 | Dependencies and packages | `lodash`, `express`, `serde`, `tokio` |
| 5 | Deployment targets | `staging`, `production`, `AWS`, `Vercel` |
| 6 | Modules, classes, services | `UserService`, `AuthModule`, `PaymentGateway` |
| 7 | Algorithmic terms | `hash`, `sort`, `O(n)`, `cache`, `memoize` |
| 8 | Routing and state management | `Router`, `middleware`, `redirect`, `proxy` |
| 9 | Data sizes and time units | `500ms`, `2GB`, `200 OK`, `timeout`, `TTL` |
| 10 | String literals and log output | `"connection refused"`, `Error: timeout` |
| 11 | Roles, teams, services | `admin`, `moderator`, `OAuth provider` |
| 12 | UI/UX and accessibility | `button`, `modal`, `aria-label`, `focus` |
| 13 | Configuration and preferences | `.env`, `.gitignore`, `tsconfig.json` |
| 14 | Error states and diagnostics | `NullPointerException`, `500`, `race condition` |
| 15 | Spec files and configs | `package.json`, `Dockerfile`, `openapi.yaml` |
| 16 | Runtime conditions | `cold start`, `degraded`, `feature flag on` |
| 17 | Terminal colors and themes | `red`, `cyan`, `256-color`, `truecolor` |
| 18 | Bug and defect taxonomy | `crash`, `memory leak`, `XSS`, `SQL injection` |
| 19 | Network and protocol terms | `HTTP/2`, `WebSocket`, `gRPC`, `TLS 1.3` |

## 4 Technical Code Verb Categories

These are the four approved categories for technical verbs in STE-Code. A technical verb is a verb term that refers to a specified operation or process in software development and is applicable to a subject field.

| # | Category | Description | Example Verbs |
|---|----------|-------------|---------------|
| 1 | Development operations | Build, test, version, and deploy software | `build`, `compile`, `test`, `lint`, `format`, `commit`, `push`, `deploy`, `rollback` |
| 2 | Data operations | I/O, serialization, persistence, and transformation | `read`, `write`, `serialize`, `deserialize`, `parse`, `encode`, `decode`, `query`, `insert`, `migrate` |
| 3 | Application operations | Request handling, state, authentication, and scheduling | `handle`, `route`, `authenticate`, `authorize`, `validate`, `schedule`, `dispatch`, `resolve` |
| 4 | Communication operations | Messaging, remote calls, and streaming | `send`, `receive`, `publish`, `subscribe`, `stream`, `poll`, `broadcast`, `connect` |

## 6-Pass Transformation Pipeline

Each rule goes through six sequential passes when adapting from STE to STE-Code. Each pass transforms one aspect of the rule while preserving all others.

### Pass 1 — Lexical (word-level)
Replace aerospace-domain words with code-domain approved words. Map dictionary entries to their STE-Code equivalents. Example: "adjust" (aerospace) stays as-is or becomes "modify" depending on code context, but the approved/non-approved status transfers directly.

### Pass 2 — Classification (category mapping)
Replace each STE technical noun category with its corresponding STE-Code category. All 19 STE categories map 1:1 to the 19 STE-Code categories in the table above. Example: Category 1 (Official parts information → Language keywords and reserved words).

### Pass 3 — POS Lock (part-of-speech verification)
Verify that every adapted word keeps the same part of speech as its STE source. If STE says "TEST (n)" is an approved noun but not an approved verb, STE-Code must preserve that restriction. The POS lock prevents accidental usage drift.

### Pass 4 — Meaning (semantic alignment)
Verify that each adapted word keeps its approved meaning from the STE dictionary. Some words carry over directly (e.g., "follow" meaning "come after" applies in both domains). Others need domain-specific clarification (e.g., "return" means "send a value back from a function" in code context).

### Pass 5 — Grammar (form and tense rules)
Apply STE grammar rules (Rules 3.1–3.7) to the adapted text. Verify that only approved verb forms appear: infinitive, imperative, simple present, simple past, simple future, and past participle as adjective. Remove all progressive, perfect, and compound tenses.

### Pass 6 — Consistency (synonym and terminology lock)
Apply the canonical synonym table. Verify that each adapted rule uses exactly one term per concept. Cross-check against master.md's synonym table and the STE-Code synonym table. Flag any drift.

## Adaptation Examples

Below are real before/after examples showing how STE rules with their original example pairs become STE-Code rules with code-domain example pairs.

### Example 1: Rule 1.1 — Approved Words

**Original STE rule (from master.md):**
The word "use" is an approved verb in the dictionary. The word "engine" is a technical noun. The word "ream" is a technical verb.

**STE-Code adaptation (from a-sec1-rule1.1.md):**
The word "run" is an approved verb in the controlled terminology. The word "UserAuthenticator" is a code-domain technical noun. The word "serialize" is a code-domain technical verb.

**Before/after pair:**

> *Original spec example:*
> The word "use" is an approved verb in the dictionary. The word "engine" is a technical noun. The word "ream" is a technical verb.

> *STE-Code adaptation:*
> The word "run" is an approved verb in the controlled terminology — just as "use" is the approved general-purpose verb in STE, "run" is the approved general-purpose verb for executing programs in STE-Code. The word "UserAuthenticator" is a code-domain technical noun — just as "engine" belongs to the aerospace subject field, "UserAuthenticator" belongs to the software subject field. The word "serialize" is a code-domain technical verb — just as "ream" describes a manufacturing process, "serialize" describes a data transformation process.

### Example 2: Rule 1.3 — Approved Meanings

**Original STE rule (from master.md):**
The approved meaning of the verb "follow" is "come after, go after." You cannot use "follow" with other meanings. Use "obey" for compliance.

**STE-Code adaptation (from a-sec1-rule1.3.md):**

**Before/after pair:**

> **Non-STE:** Follow the configuration steps to set up the server.
> **STE:** Obey the configuration instructions to set up the server.

> *Adaptation note: "follow" (approved meaning: "come after, go after") is misused to mean "act in accordance with." In the spec, you must use "obey" when you mean "comply with instructions." The same distinction applies in STE-Code.*

> **Non-STE:** The function will return you to the login screen.
> **STE:** The function will go back to the login screen.

> *Adaptation note: The approved meaning of "return" in STE-Code is "to send a value back from a function to its caller." Using "return" to mean "go back" is not an approved meaning. Use "go back" instead.*

### Example 3: Rule 3.2 — Verb Forms and Tenses

**Original STE rule (from master.md):**
Use only these forms: infinitive, imperative, simple present, simple past, simple future, past participle as adjective. Do not use present perfect (have/has adjusted), past perfect (had adjusted), or progressive forms (is/was adjusting).

**STE-Code adaptation (from a-sec3-rule3.2.md):**

**Before/after pairs:**

> **Non-STE:** The linter has found three errors in the source file.
> **STE:** The linter found three errors in the source file.
>
> *Adapted from spec: present perfect "have/has adjusted" is prohibited.*

> **Non-STE:** The server was processing the request when the timeout occurred.
> **STE:** The server processed the request. Then the timeout occurred.
>
> *Adapted from spec: past progressive "was adjusting" is prohibited. Break into separate sentences.*

> **Non-STE:** The framework had already initialized the connection pool before the query started.
> **STE:** The framework initialized the connection pool. Then the query started.
>
> *Adapted from spec: past perfect "had adjusted" is prohibited. Use simple past tense and sequence with "Then."*

## Execution Instructions

### Launch by Section (recommended)

Launch one worker per section. Each worker reads the merged master.md and adapts all rules in one section:

```bash
# Section 1 — Words (Rules 1.1–1.14)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec1.txt)" -m deepseek-v4-pro

# Section 2 — Multi-word Nouns (Rules 2.1–2.3)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec2.txt)" -m deepseek-v4-pro

# Section 3 — Verbs (Rules 3.1–3.7)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec3.txt)" -m deepseek-v4-pro

# Section 4 — Sentences (Rules 4.1–4.5)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec4.txt)" -m deepseek-v4-pro

# Section 5 — Procedural Writing (Rules 5.1–5.5)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec5.txt)" -m deepseek-v4-pro

# Section 6 — Descriptive Writing (Rules 6.1–6.6)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec6.txt)" -m deepseek-v4-pro

# Section 7 — Safety Instructions (Rules 7.1–7.3)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec7.txt)" -m deepseek-v4-pro

# Section 8 — Punctuation (Rules 8.1–8.7)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec8.txt)" -m deepseek-v4-pro

# Section 9 — Writing Practices (Rules 9.1–9.4 + GR1–GR4)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec9.txt)" -m deepseek-v4-pro
```

### Launch All at Once

Use the combined prompt that adapts all 9 sections plus categories and synonyms:

```bash
hermes -z "$(cat .agents/prompts/adapt/adapt-all-prompt.txt)" -m deepseek-v4-pro
```

### Naming Convention

| Pattern | Usage |
|---------|-------|
| `a-secN-ruleX.Y.md` | Per-rule adaptation (e.g., `a-sec1-rule1.1.md`) |
| `a-categories.md` | 19 categories mapped to code domain |
| `a-dictionary.md` | Full approved word dictionary adapted for code |

### Prerequisites

- `ste-code/merged/master.md` must exist and pass all merge verification gates
- All 53 rules must be present and numbered correctly
- All 19 categories must be enumerated
- Dictionary entries must cover A–Z

## Quality Checks and Verification Gates

After adaptation, verify each output file against these gates. Fix any failures before proceeding to Stage 5 (Artifacts).

### Gate 1 — Structural Completeness

```bash
# Count adapted rule files (must be 53)
ls ste-code/adapted/a-sec*-rule*.md | wc -l

# Verify every section has its rules adapted
ls ste-code/adapted/a-sec1-rule*.md | wc -l  # 14 rules
ls ste-code/adapted/a-sec2-rule*.md | wc -l  #  3 rules
ls ste-code/adapted/a-sec3-rule*.md | wc -l  #  7 rules
ls ste-code/adapted/a-sec4-rule*.md | wc -l  #  5 rules
ls ste-code/adapted/a-sec5-rule*.md | wc -l  #  5 rules
ls ste-code/adapted/a-sec6-rule*.md | wc -l  #  6 rules
ls ste-code/adapted/a-sec7-rule*.md | wc -l  #  3 rules
ls ste-code/adapted/a-sec8-rule*.md | wc -l  #  7 rules
ls ste-code/adapted/a-sec9-rule*.md | wc -l  #  4 rules (plus GR1–GR4)

# Verify supporting files exist
test -f ste-code/adapted/a-categories.md && echo "PASS" || echo "FAIL: missing categories"
test -f ste-code/adapted/a-dictionary.md && echo "PASS" || echo "FAIL: missing dictionary"
```

### Gate 2 — Source Traceability

Every adapted rule file must contain a source reference:

```bash
# Count files with source reference (must equal total rule count)
grep -l "Adapted from ASD-STE100 Issue 9" ste-code/adapted/a-sec*-rule*.md | wc -l
```

### Gate 3 — Example Pair Completeness

Every adapted rule that has STE/non-STE pairs in the original must have at least one code-domain pair:

```bash
# Count files that contain both Non-STE and STE example markers
grep -l "Non-STE:" ste-code/adapted/a-sec*-rule*.md | wc -l
```

### Gate 4 — Adaptation Fidelity (Spot Check)

Pick 5 random adapted rules. For each:
1. Read the original rule text in `ste-code/merged/master.md`
2. Read the adapted rule in `ste-code/adapted/a-secN-ruleX.Y.md`
3. Verify that the adaptation:
   - Preserves the rule number and core instruction
   - Replaces aerospace examples with valid code-domain examples
   - Does not invent terms without a master.md source
   - Uses only approved STE-Code vocabulary
4. Flag any rule that fails for re-adaptation

### Gate 5 — Verb Category Coverage

```bash
# Verify all 4 verb categories appear in adapted verb rules
grep -l "development operations\|Development operations" ste-code/adapted/a-sec3-*.md | wc -l
```

### Gate 6 — Synonym Consistency

```bash
# Verify no non-approved synonyms leak through (check top offenders)
grep -rn "utilize\|leverage\|employ" ste-code/adapted/ | grep -v "## Original Rule" | wc -l
# Result must be 0 — non-approved synonyms must not appear outside original rule text
```

### Gate 7 — Part of Speech Lock

Every approved word in adapted output must keep the same part of speech as the STE source dictionary. Cross-check 10 random dictionary entries from `a-dictionary.md` against the corresponding entries in `master.md`.

## Non-Negotiable
- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair
- No invented code terms without a master.md source

Full mapping: `.agents/references/category-mapping.md`
