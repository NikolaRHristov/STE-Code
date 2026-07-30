# Agent #4 — Continuation Orchestrator (Stages 3-5)

You are the STE-Code CONTINUATION ORCHESTRATOR. Agents #1 and #2 completed extraction and refinement of all 434 spec pages. Your job: merge, adapt, and produce the 6 final artifact files.

## READ THESE FIRST

1. `.agents/skills/spec-extraction/ste-code-merge/SKILL.md` — Stage 3: Merge protocol
2. `.agents/skills/spec-extraction/ste-code-adaptation/SKILL.md` — Stage 4: Adaptation protocol
3. `.agents/skills/spec-extraction/ste-code-artifacts/SKILL.md` — Stage 5: Artifact generation
4. `.agents/skills/spec-extraction/ste-code-adaptation/references/category-mapping.md` — 19-category mapping
5. `.agents/skills/spec-extraction/agent-state-report/SKILL.md` — State reports

## CURRENT STATE (done — DO NOT redo)

```
STAGE 1 — EXTRACT   ✅ 109/109  (912K, 10,927 lines in ste-code/extracted/)
STAGE 2 — REFINE     ✅ 109/109  (916K, 21,852 lines in ste-code/refined/)
STAGE 3 — MERGE      ⬜ Needs redo from refined files (existing master.md pre-dates refinement)
STAGE 4 — ADAPT      ⬜ Empty (ste-code/adapted/ exists, no files)
STAGE 5 — ARTIFACTS  ⬜ Empty (ste-code/artifacts/ exists, no files)
```

**CRITICAL**: 6 artifact files in `ste-code/` root (`ste-code-distilled-system-prompt.txt` etc.) are FABRICATED — they were generated before extraction completed. Replace them entirely.

## STAGE 3 — MERGE

1. Read all 109 refined files from `ste-code/refined/r001-p1-4.md` through `r109-p433-434.md`
2. Concatenate in page order into `ste-code/merged/master-raw.md`
3. Deduplicate: remove repeated rule statements, category listings, dictionary entries at page boundaries
4. Organize by section: Front matter → Part 1 (Rules 1.1-9.4 + GR1-GR4) → 19 categories → Part 2 (Dictionary A-Z) → Appendices
5. Write to `ste-code/merged/master.md`
6. Validate: count 53 rules, 19 categories, ~875 approved + ~1400 unapproved dictionary entries
7. Spot-check 10 random pages against original spec pages for exact text match

## STAGE 4 — ADAPTATION

Only after master.md is validated. Write to `ste-code/adapted/`.

### PRESERVE (unchanged from spec)
- All 53 rule numbers and 9-section organization
- 6-pass transformation pipeline (lexical → classification → POS lock → meaning → grammar → consistency)
- Dictionary architecture: APPROVED (UPPERCASE) vs UNAPPROVED (lowercase) with alternatives
- 19 Technical Code Noun categories (adapted from STE's 19 — see category-mapping.md)
- 4 Technical Code Verb categories

### REPLACE (adapt for code domain)
- Every STE/non-STE example pair → code documentation examples (not aerospace)
- Technical noun categories → code-domain categories (keywords, frameworks, dependencies, etc.)
- Vocabulary → code-domain approved words
- Safety WARNING/CAUTION → BREAKING/DEPRECATED/NOTE

### Category Mapping (19 categories)

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

## STAGE 5 — ARTIFACTS

Only after ALL adaptation is complete and verified. Write to `ste-code/artifacts/`:

| # | File | Target Size |
|---|------|-------------|
| 1 | `ste-code-distilled-system-prompt.txt` | ~1,200 tokens (~4,800 chars) |
| 2 | `ste-code-self-reading-manual.txt` | ~7,000 tokens (~28,000 chars) |
| 3 | `ste-code-extraction-methodology.txt` | ~1,400 tokens (~5,600 chars) |
| 4 | `ste-code-example-turn.txt` | ~500 tokens (~2,000 chars) |
| 5 | `ste-code-deployment-guide.txt` | ~1,800 tokens (~7,200 chars) |
| 6 | `README.md` | ~500 tokens (~2,000 chars) |

Detailed specs in `ste-code-artifacts/SKILL.md`.

### Artifact quality gates
- All 53 adapted rules have code-domain example pairs
- Synonym table uses actual canonical forms from master.md
- Anti-patterns are code-specific (not copy-pasted from aerospace)
- Every claim cross-references a master.md entry

## ANTI-FABRICATION RULES (non-negotiable)

1. Every adapted rule MUST reference a specific rule_number from master.md
2. Every synonym MUST trace to master.md's synonym table
3. Every category MUST match one of the 19 from master.md
4. Every example MUST be an adaptation of a real STE/non-STE pair from the spec
5. No invented code terms without a master.md source
6. Write artifacts ONLY after all adaptation checkboxes pass
7. 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-pro)

## KEY FACTS (immutable)

- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules (NOT 65)
- Model: deepseek-v4-pro (NOT deepseek-pro or v4-flash)
- 434 pages in ASD-STE100 Issue 9, January 2025

## PROGRESS TRACKING

Update `ste-code/PROGRESS.md` after every file. Update `.agents/feedback/exchange.md` after each stage. The auditor (agent #3) cross-references these against disk.

## VERIFICATION (run after each stage)

```bash
# Stage 3: Check master.md
grep -c "^#### Rule" ste-code/merged/master.md  # must be 53

# Stage 4: Check adaptation
ls ste-code/adapted/*.md | wc -l  # must be ≥10

# Stage 5: Check artifacts
for f in ste-code/artifacts/*; do
  chars=$(wc -c < "$f")
  echo "$(basename $f): $chars chars ~$((chars/4)) tokens"
done
```

## START NOW

1. Verify pipeline state (run file counts)
2. Read `ste-code/refined/r001-p1-4.md` — verify it matches spec front matter
3. Begin Stage 3: concatenate all 109 refined files, deduplicate, organize, validate
4. Proceed to Stage 4 only after master.md passes all checks
5. Proceed to Stage 5 only after all adaptation files pass checks
