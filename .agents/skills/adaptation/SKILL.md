# Adaptation Protocol - Stage 4

> **MANDATORY**: Read `.agents/skills/OPERATING_PRINCIPLES.md` before any work.
> Session isolation + STRICT_RULES (R1-R6) from `lib/pipeline_core.py` apply to THIS skill.
> One session = one operation = one read + one write. No re-editing own output.

Transform STE rules into STE-Code (coding domain). Agent-agnostic.

## Input: `ste-code/grouped/*.md` (all grouped group files; the orchestrator
concatenates them and slices each rule section by its canonical title)
## Output: `ste-code/adapted/` (rule-by-rule STE→STE-Code)

## Orchestration & prompts
- **`.agents/tools/adaptation/adapt_batch.py`** launches one LLM worker per rule
  section (1-9 + GR), embeds THIS skill as the authoritative protocol, and commits
  each section only after its deterministic gate passes (verify-adaptation.py).
- Worker prompts are externalized to **`.agents/tools/adaptation/templates/`**
  (edit those `.md` files to change wording — not the `.py`). The embedded skill
  text below is the single source of truth for behavior.
- Refuses to launch until `ste-code/grouped/` exists and is non-trivial.
- Checkpoint + `--resume` + per-section git commit (crash-safe, like refine_batch.py).

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

### Pass 1 - Lexical (word-level)
Replace aerospace-domain words with code-domain approved words. Map dictionary entries to their STE-Code equivalents. Example: "adjust" (aerospace) stays as-is or becomes "modify" depending on code context, but the approved/non-approved status transfers directly.

### Pass 2 - Classification (category mapping)
Replace each STE technical noun category with its corresponding STE-Code category. All 19 STE categories map 1:1 to the 19 STE-Code categories in the table above. Example: Category 1 (Official parts information → Language keywords and reserved words).

### Pass 3 - POS Lock (part-of-speech verification)
Verify that every adapted word keeps the same part of speech as its STE source. If STE says "TEST (n)" is an approved noun but not an approved verb, STE-Code must preserve that restriction. The POS lock prevents accidental usage drift.

### Pass 4 - Meaning (semantic alignment)
Verify that each adapted word keeps its approved meaning from the STE dictionary. Some words carry over directly (e.g., "follow" meaning "come after" applies in both domains). Others need domain-specific clarification (e.g., "return" means "send a value back from a function" in code context).

### Pass 5 - Grammar (form and tense rules)
Apply STE grammar rules (Rules 3.1-3.7) to the adapted text. Verify that only approved verb forms appear: infinitive, imperative, simple present, simple past, simple future, and past participle as adjective. Remove all progressive, perfect, and compound tenses.

### Pass 6 - Consistency (synonym and terminology lock)
Apply the canonical synonym table. Verify that each adapted rule uses exactly one term per concept. Cross-check against master.md's synonym table and the STE-Code synonym table. Flag any drift.

## Adaptation Examples

Below are real before/after examples showing how STE rules with their original example pairs become STE-Code rules with code-domain example pairs.

### Example 1: Rule 1.1 - Approved Words

**Original STE rule (from master.md):**
The word "use" is an approved verb in the dictionary. The word "engine" is a technical noun. The word "ream" is a technical verb.

**STE-Code adaptation (from a-sec1-rule1.1.md):**
The word "run" is an approved verb in the controlled terminology. The word "UserAuthenticator" is a code-domain technical noun. The word "serialize" is a code-domain technical verb.

**Before/after pair:**

> *Original spec example:*
> The word "use" is an approved verb in the dictionary. The word "engine" is a technical noun. The word "ream" is a technical verb.

> *STE-Code adaptation:*
> The word "run" is an approved verb in the controlled terminology - just as "use" is the approved general-purpose verb in STE, "run" is the approved general-purpose verb for executing programs in STE-Code. The word "UserAuthenticator" is a code-domain technical noun - just as "engine" belongs to the aerospace subject field, "UserAuthenticator" belongs to the software subject field. The word "serialize" is a code-domain technical verb - just as "ream" describes a manufacturing process, "serialize" describes a data transformation process.

### Example 2: Rule 1.3 - Approved Meanings

**Original STE rule (from master.md):**
The approved meaning of the verb "follow" is "come after, go after." You cannot use "follow" with other meanings. Use "obey" for compliance.

**STE-Code adaptation (from a-sec1-rule1.3.md):**

**Before/after pair:**

> **Non-STE:** Follow the configuration steps to set up the server.
> **STE:** Obey the configuration instructions to set up the server.
>
> *Adaptation note: "follow" (approved meaning: "come after, go after") is misused to mean "act in accordance with." In the spec, you must use "obey" when you mean "comply with instructions." The same distinction applies in STE-Code.*

> **Non-STE:** The function will return you to the login screen.
> **STE:** The function will go back to the login screen.
>
> *Adaptation note: The approved meaning of "return" in STE-Code is "to send a value back from a function to its caller." Using "return" to mean "go back" is not an approved meaning. Use "go back" instead.*

### Example 3: Rule 3.2 - Verb Forms and Tenses

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

### Example 4: Rule 7.1 - WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

**Original STE rule (from master.md):**
WARNING comes before instructions that can cause injury or death. CAUTION comes before instructions that can cause equipment damage.

**STE-Code adaptation (from a-sec7-rule7.1.md):**

**Before/after pairs:**

> **Original:** WARNING: DO NOT TOUCH THE HOT EXHAUST. IT CAN BURN YOU.
> **STE-Code:** BREAKING: This change deletes all user data in the `users` table. Make a backup before you run the migration.

> **Original:** CAUTION: MAKE SURE THAT THE LOCKWIRE IS TIGHT. A LOOSE LOCKWIRE CAN CAUSE DAMAGE TO THE ENGINE.
> **STE-Code:** DEPRECATED: The `legacyAuth()` method will be removed in v4.0. Use `oidcLogin()` instead.

> **Original:** NOTE: This procedure is for the left engine only.
> **STE-Code:** NOTE: This endpoint accepts only `application/json` content type. XML payloads will get a `415 Unsupported Media Type` response.

### Example 5: Rule 3.7 - Technical Verbs as Nouns (Anti-Pattern)

**Original STE rule (from master.md):**
Do not use technical verbs as nouns. Use an approved noun instead.

**STE-Code adaptation:**

**Before/after pairs:**

> **Non-STE:** Run a deploy to staging before the production push.
> **STE:** Run a deployment to staging before you push to production.
>
> *"deploy" is a technical verb (category 1). Use "deployment" as the noun form.*

> **Non-STE:** The build failed because of a missing dependency.
> **STE:** The build process failed because a dependency is missing.
>
> *"build" used as a noun is acceptable in this context because it refers to the build artifact, not the verb action. But prefer "build process" for clarity when the distinction matters.*

> **Non-STE:** We need a quick test on that endpoint.
> **STE:** We must test that endpoint quickly.
>
> *"test" is a technical verb (category 1). Use it as a verb, not as a noun.*

## Execution Instructions

### Launch by Section (recommended)

Launch one worker per section. Each worker reads the merged master.md and adapts all rules in one section:

```bash
# Section 1 - Words (Rules 1.1-1.14)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec1.txt)" -m poolside/laguna-s-2.1:free

# Section 2 - Multi-word Nouns (Rules 2.1-2.3)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec2.txt)" -m poolside/laguna-s-2.1:free

# Section 3 - Verbs (Rules 3.1-3.7)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec3.txt)" -m poolside/laguna-s-2.1:free

# Section 4 - Sentences (Rules 4.1-4.5)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec4.txt)" -m poolside/laguna-s-2.1:free

# Section 5 - Procedural Writing (Rules 5.1-5.5)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec5.txt)" -m poolside/laguna-s-2.1:free

# Section 6 - Descriptive Writing (Rules 6.1-6.6)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec6.txt)" -m poolside/laguna-s-2.1:free

# Section 7 - Safety Instructions (Rules 7.1-7.3)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec7.txt)" -m poolside/laguna-s-2.1:free

# Section 8 - Punctuation (Rules 8.1-8.7)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec8.txt)" -m poolside/laguna-s-2.1:free

# Section 9 - Writing Practices (Rules 9.1-9.4 + GR1-GR4)
hermes -z "$(cat .agents/prompts/adapt/adapt-sec9.txt)" -m poolside/laguna-s-2.1:free
```

### Launch All at Once

Use the combined prompt that adapts all 9 sections plus categories and synonyms:

```bash
hermes -z "$(cat .agents/prompts/adapt/adapt-all-prompt.txt)" -m poolside/laguna-s-2.1:free
```

### Naming Convention

| Pattern | Usage |
|---------|-------|
| `a-secN-ruleX.Y.md` | Per-rule adaptation (e.g., `a-sec1-rule1.1.md`) |
| `a-categories.md` | 19 categories mapped to code domain |
| `a-dictionary.md` | Full approved word dictionary adapted for code |

### Prerequisites

- `ste-code/grouped/master.md` must exist and pass all merge verification gates
- All 53 rules must be present and numbered correctly
- All 19 categories must be enumerated
- Dictionary entries must cover A-Z

## Quality Checks and Verification Gates

After adaptation, verify each output file against these gates. Fix any failures before proceeding to Stage 5 (Artifacts).

### Gate 1 - Structural Completeness

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
ls ste-code/adapted/a-sec9-rule*.md | wc -l  #  4 rules (plus GR1-GR4)

# Verify supporting files exist
test -f ste-code/adapted/a-categories.md && echo "PASS" || echo "FAIL: missing categories"
test -f ste-code/adapted/a-dictionary.md && echo "PASS" || echo "FAIL: missing dictionary"
```

### Gate 2 - Source Traceability

Every adapted rule file must contain a source reference:

```bash
# Count files with source reference (must equal total rule count)
grep -l "Adapted from ASD-STE100 Issue 9" ste-code/adapted/a-sec*-rule*.md | wc -l
```

### Gate 3 - Example Pair Completeness

Every adapted rule that has STE/non-STE pairs in the original must have at least one code-domain pair:

```bash
# Count files that contain both Non-STE and STE example markers
grep -l "Non-STE:" ste-code/adapted/a-sec*-rule*.md | wc -l
```

### Gate 4 - Adaptation Fidelity (Spot Check)

Pick 5 random adapted rules. For each:
1. Read the original rule text in `ste-code/grouped/master.md`
2. Read the adapted rule in `ste-code/adapted/a-secN-ruleX.Y.md`
3. Verify that the adaptation:
   - Preserves the rule number and core instruction
   - Replaces aerospace examples with valid code-domain examples
   - Does not invent terms without a master.md source
   - Uses only approved STE-Code vocabulary
4. Flag any rule that fails for re-adaptation

### Gate 5 - Verb Category Coverage

```bash
# Verify all 4 verb categories appear in adapted verb rules
grep -l "development operations\|Development operations" ste-code/adapted/a-sec3-*.md | wc -l
```

### Gate 6 - Synonym Consistency

```bash
# Verify no non-approved synonyms leak through (check top offenders)
grep -rn "utilize\|leverage\|employ" ste-code/adapted/ | grep -v "## Original Rule" | wc -l
# Result must be 0 - non-approved synonyms must not appear outside original rule text
```

### Gate 7 - Part of Speech Lock

Every approved word in adapted output must keep the same part of speech as the STE source dictionary. Cross-check 10 random dictionary entries from `a-dictionary.md` against the corresponding entries in `master.md`.

### Gate 8 - Backlink Integrity

Every adapted rule must link back to the exact section of the original. Verify that each `a-secN-ruleX.Y.md` file contains a machine-readable anchor:

```bash
# Every adapted rule must contain an anchor like [Source: master.md#secN-ruleX.Y]
grep -c "Source: master.md#" ste-code/adapted/a-sec*-rule*.md | grep ":0"
# Any file with ":0" failed - it is missing the source anchor
```

### Gate 9 - Aerospace Artifact Sweep

Verify that no aerospace-domain artifacts survive into adapted output:

```bash
# Known aerospace terms that must NOT appear outside original rule blocks
grep -rn "aircraft\|engine\|landing gear\|fuselage\|cockpit\|APU\|ECS\|ATA chapter" \
  ste-code/adapted/ | grep -v "## Original Rule" | wc -l
# Result must be 0 - aerospace terms are domain leakage
```

## Troubleshooting

### Symptom: Adapted rule uses the same example as the original

**Cause:** The worker did not replace the STE/non-STE example pair with a code-domain pair. This happens when the prompt does not provide enough code-domain context or when the rule text itself is abstract enough that the worker sees no clear substitution.

**Fix:** Re-launch the section worker with a prompt that includes 3 candidate code-domain scenarios for the affected rule. The worker picks the best-fit scenario and adapts the example.

### Symptom: Adapted dictionary entry has wrong part of speech

**Cause:** The POS lock in Pass 3 was skipped or misapplied. An STE noun was adapted to a STE-Code verb (or vice versa).

**Fix:** Diff the original dictionary entry against the adapted entry. Restore the original part of speech tag. If the code domain genuinely needs a different POS, document the exception in a `pos-exceptions.md` file and get sign-off before committing.

### Symptom: Synonym drift across sections

**Cause:** Two different section workers chose different STE-Code synonyms for the same STE term. For example, Section 1 adapts "show" as "show" while Section 8 adapts it as "display."

**Fix:** Run Gate 6 (Synonym Consistency) first. Then grep across all adapted files for the conflicting term. Normalize to one term. Update the synonym table in `a-dictionary.md` to record the final choice.

### Symptom: Missing rule file (53 expected, fewer found)

**Cause:** A section worker failed silently. The merged file was missing that section's content, or the worker crashed mid-adaptation.

**Fix:** Identify the gap by comparing expected vs actual file counts per section. Re-launch only the missing section. Do not re-run sections that passed Gate 1.

### Symptom: Category mismatch (STE category maps to wrong STE-Code category)

**Cause:** The category mapping table was not followed. The worker guessed a mapping instead of using the canonical 1:1 table.

**Fix:** Cross-check the adapted rule's category tag against the Category Mapping table above. If the tag is wrong, rewrite the rule from the merged source with the correct mapping enforced.

## Edge Cases

### Edge Case 1: STE term has no direct code-domain equivalent

Some STE terms are physical-world concepts with no software analog (e.g., "grease," "lockwire," "torque"). Do not force a code-domain mapping.

**Rule:** If an STE term appears only in examples and has no plausible code-domain equivalent, keep the original example structure but annotate it as a "structural carryover" with a note explaining why no substitution was made. The term itself stays in the original rule block and is not adapted.

### Edge Case 2: Code-domain term is both a noun and a verb

Some code terms like "build," "test," "deploy" are approved as technical verbs (categories 1-4) but also appear as nouns in standard usage (e.g., "the build failed"). STE-Code Rule 1.13 forbids using technical verbs as nouns.

**Rule:** When a technical verb must be used as a noun, use an approved nominalization: "build process," "test suite," "deployment pipeline." If no clean nominalization exists, document the exception and propose adding the noun form to the approved dictionary.

### Edge Case 3: Multi-word code noun contains a non-approved word

A technical code noun like "feature flag" or "cold start" may contain a word that is not in the approved dictionary (e.g., "flag" as a noun, "cold" as an adjective). Rule 1.5 permits technical code nouns as a whole even when their constituents are non-approved.

**Rule:** Do not disassemble a technical code noun to check its parts. Treat the multi-word unit as a single approved term. This applies to all 19 categories.

### Edge Case 4: Adapted example is too domain-specific

An example that references `React` or `PostgreSQL` may not generalize to all code domains. The adaptation should be representative, not prescriptive.

**Rule:** When possible, use framework-agnostic examples that apply across languages and runtimes. Prefer universal concepts (function, module, endpoint, query) over framework-specific concepts (useEffect, ActiveRecord, middleware chain). When a framework-specific term is unavoidable, annotate with "For example, in React:" or equivalent.

### Edge Case 5: BREAKING/DEPRECATED mapping ambiguity

Not every WARNING maps to BREAKING, and not every CAUTION maps to DEPRECATED. The severity mapping depends on context.

**Rule:**

| STE Signal | Code-Domain Signal | When to Use |
|------------|-------------------|-------------|
| WARNING (injury/death) | BREAKING | Irreversible data loss, auth bypass, security vulnerability |
| CAUTION (equipment damage) | DEPRECATED | API removal, config format change, behavior change with migration path |
| NOTE (important info) | NOTE | Constraints, preconditions, non-obvious behavior |

## Non-Negotiable

- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair
- No invented code terms without a master.md source
- All 53 rules must pass all 9 verification gates before Stage 5 begins
- Any adaptation that cannot find a code-domain equivalent must be flagged, not forced
- All adapted output must use American English spelling (Rule 1.14)
- No progressive, perfect, or compound verb tenses in adapted rule text
- No contractions in adapted rule text

Full mapping: `.agents/references/category-mapping.md`
