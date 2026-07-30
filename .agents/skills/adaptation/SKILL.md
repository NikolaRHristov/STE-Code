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

## Non-Negotiable
- Every adapted rule MUST reference its original rule number from master.md
- Every synonym MUST trace to master.md's synonym table
- Every category MUST match one of the 19 from master.md
- Every example MUST be an adaptation of a real STE/non-STE pair
- No invented code terms without a master.md source

Full mapping: `.agents/references/category-mapping.md`
