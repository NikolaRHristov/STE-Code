# Linguistic Layer — Decision Tree

> **Version:** FLAVOR-1.0.0
> **Purpose:** Ordered rule application for linguistic checking.
> **Principle:** Mechanical check → mechanical repair. No LLM judgment at check time.

---

## Step 0 — Classify Intent (before any rule)

| Intent | Signal | Example |
|--------|--------|---------|
| Imperative | Verb-first, no subject | `Set the token.` |
| Warning | WARNING/CAUTION prefix | `WARNING: Do not use in production.` |
| Prohibition | DO NOT / NEVER / prohibited | `Do not call this function from a signal handler.` |
| Note | Informational, no command | `The default timeout is 30 seconds.` |
| Assumption | Conditional framing | `When you set the DEBUG flag, ...` |

Intent determines which rules apply. Imperative sentences skip referent checks (no subject to resolve). Notes skip actor checks.

---

## Step 1 — Semantic Role Check (SR)

**Table:** `semantics.json#semantic_roles`

For every verb: is it an Action term? If yes:
- In noun position → violation. Replace with Result form.
- In imperative position → permitted.
- `The deploy takes five minutes` → `The deployment takes five minutes.`

For every noun: is it an Action term used as noun? If yes:
- Check if Result form exists. If yes, replace.
- If no Result form (rare), restructure sentence.

**Repair:** Replace Action-as-noun with Result form from `semantic_roles.term_table`.

---

## Step 2 — Single Referent Rule (SRR)

**Table:** `semantics.json#single_referent_rule`

For every noun phrase: does the head noun appear in `domain_collisions`?
- If yes: is it qualified on first use in this section? If not → violation.
- If no: check if it appears unqualified in multiple contexts within one document.

For every pronoun (it, they, this, these, that):
- Does the antecedent appear in the same sentence? If not → violation.
- `The server retries the request. It uses exponential backoff.` → `The server retries the request. The server uses exponential backoff.`

**Repair:** Add qualifier from `domain_collisions` or replace pronoun with antecedent.

---

## Step 3 — Scope Bracketing (SB)

Condition-first: `When X, do Y.` not `Do Y when X.`

Modifier attachment:
- `The function validates input from the user with the token.` → ambiguous
- `The function uses the token to validate input from the user.` → clear

Time/condition position: Conditions and temporal clauses precede the main clause.
- `After the build completes, the deployment starts.` ✓
- `The deployment starts after the build completes.` → violation (for procedural)

---

## Step 4 — Epistemic Marking (EPI)

**Table:** `semantics.json#epistemic`

Scan for: performance adjectives (`fast`, `slow`, `scalable`, `reliable`), reliability claims, scale claims.

If bare (unqualified by measurement or expectation marker) → violation.
`The API is fast` → `The API responds with p99 latency of 87 ms (load test, 2026-07).`

Modal check: `will`, `should`, `may` (system), `might` → violation.
`The server will retry` → `The server retries.`

---

## Step 5 — Quantifier Precision (QUANT)

**Table:** `semantics.json#quantifiers`

Replace vague quantifiers with precise alternatives:
- `many requests` → `1000 or more requests`
- `often fails` → `fails in 5% of requests`
- `approximately 100 ms` → `about 100 ms` (acceptable; bounded vagueness)

---

## Step 6 — Negation Control (NEG)

One negation per clause maximum.

Prohibited: `not uncommon`, `not without`, `never not`, double negatives.
`It is not uncommon for the server to fail` → `The server fails in 2% of requests.`

Prefer antonyms: `not available` → `unavailable`, `not correct` → `incorrect`.

---

## Step 7 — Register Check (REG)

**Table:** `registers.json`

For each document section: verify sentence length, article usage, and intent mix against the declared register.

| Register | Max words | Articles | Intents |
|----------|:---------:|:--------:|---------|
| error-message | 12 | droppable | Note/Warning only |
| commit-subject | 72 chars | droppable | Imperative only |
| readme-prose | 25 | required | full |
| api-description | 20 | required | Note + Assumption |
| inline-comment | 15 | droppable | Note (+ reason clause) |
| cli-help | 10 | droppable | Note only |

---

## Step 8 — Precedence Order

When two rules conflict on the same sentence, apply in this order:

1. SR (Semantic Role) — fixes word class; everything else depends on correct word class
2. SRR (Single Referent) — resolves ambiguity; later checks need unambiguous referents
3. SB (Scope Bracketing) — fixes structure; epistemic checks need correct structure
4. EPI (Epistemic) — checks claims; needs correct subjects and structure
5. QUANT (Quantifiers) — precision; applied last in lexical checks
6. NEG (Negation) — safety; applied after meaning is established
7. REG (Register) — context; applied last because it may override earlier rules

If an earlier fix makes a later violation impossible, mark as `RESOLVED-BY-PRECEDENCE` rather than `FIXED` or `VIOLATION`.
