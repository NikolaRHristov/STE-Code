# Reference

## Rules

53 writing rules + 4 grammar rules adapted from ASD-STE100 for code documentation.

| Section | Rules | Topic |
|---------|-------|-------|
| Section 1 | 1.1–1.14 | Words — vocabulary, parts of speech, technical nouns, consistency |
| Section 2 | 2.1–2.2 | Sentence structure — length, clarity |
| Section 3 | 3.1–3.7 | Verbs — forms, tenses, voice |
| Section 4 | 4.1–4.5 | Adjectives and adverbs — approved forms |
| Section 5 | 5.1–5.5 | Technical nouns — keywords, frameworks, tools |
| Section 6 | 6.1–6.5 | Non-approved words — when to allow exceptions |
| Section 7 | 7.1–7.3 | Noun clusters — maximum depth, clarity |
| Section 8 | 8.1–8.6 | Procedural writing — instructions, steps, warnings |
| Section 9 | 9.1–9.4 | Grammar rules — articles, prepositions, conjunctions |
| GR | GR1–GR4 | General grammar — punctuation, capitalization, abbreviations |

Each adapted rule file at `ste-code/adapted/a-secN-ruleX.Y.md` contains:
- Original STE rule text
- Code-domain rewrite
- STE/non-STE example pairs replaced with code documentation examples
- Cross-reference to the source rule in `master.md`

## Dictionary

The approved word dictionary at `ste-code/adapted/a-dictionary.md` (5,943 lines)
contains:

| Type | Count | Format |
|------|:-----:|--------|
| Approved verbs | ~350 | `WORD (v) — APPROVED` with meanings, forms, examples |
| Approved adjectives | ~125 | `WORD (adj) — APPROVED` with meanings, examples |
| Approved nouns | ~200 | `WORD (n) — APPROVED` with meanings |
| Approved other | ~200 | Prepositions, adverbs, conjunctions |
| Unapproved | ~1,400 | `word (pos) — UNAPPROVED` with approved alternatives |

Vocabulary JSON extracts are at `SCE/data/vocabulary/`:
- `approved-verbs.json` — All approved verbs with code-domain meanings
- `approved-adjectives.json` — All approved adjectives
- `domain-extensions.json` — Domain-specific approved terms

## Synonyms

The canonical synonym table at `SCE/core/categories/synonym-table.json` maps every
unapproved term to exactly one approved alternative. No circular references.
12 primary pairs + 18 extended pairs = 30 canonical pairs.

## Categories

19 code-domain noun categories adapted from STE's technical noun categories:

| # | Category | Examples |
|---|----------|----------|
| 1 | Language keywords | `if`, `return`, `class`, `async`, `await` |
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

## Schemas

JSON schemas for pipeline output validation at `SCE/compute/schemas/` and `ste-code/v2/compute/schemas/`:

| Schema | Validates |
|--------|----------|
| `rule-frontmatter.schema.json` | YAML frontmatter in rule files (`id`, `section`, `principle`, `severity`) |
| `vocabulary-entry.schema.json` | Dictionary entry format (`term`, `type`, `approved`, `meaning`, `examples`) |
| `synonym-table.schema.json` | Synonym pair format (`approved`, `avoid`) |
| `worker-contract.json` | Worker behavioral contract (`batch-size`, `must-do`, `must-not-do`) |

## Rails

8 behavioral guardrails for all pipeline agents at `.agents/references/rails.json`:

| Rail | Rule | Severity |
|------|------|----------|
| R1 | Stage Isolation — never cross-contaminate stage directories | Critical |
| R2 | Naming Convention — `wNNN-pPPPP-PPPP.md` / `rNNN-pPPPP-PPPP.md` | Critical |
| R3 | Completion Integrity — never claim completion without disk proof | Critical |
| R4 | Content Fidelity — zero fabrication, every word from spec | Critical |
| R5 | Formatting Standards — 9 refinement rules applied | Critical |
| R6 | Factual Correctness — 19 categories, deepseek-v4-pro | Blocking |
| R7 | Progress Tracking — PROGRESS.md matches disk | Blocking |
| R8 | Error Recovery — fixes documented, stale files purged | Blocking |
