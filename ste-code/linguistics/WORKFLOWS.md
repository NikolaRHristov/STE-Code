# Linguistic Layer — Implementation Workflows

> **Status:** Specification complete. All workflows pending local execution.
> **Prerequisite:** Workflow 1 (Grounding) must complete before any other workflow.

---

## Workflow 1 — Grounding (MANDATORY FIRST)

**Goal:** Verify every claim in the linguistic layer against actual repository content.

```
Read ste-code/linguistics/semantics.json, DECISION-TREE.md, SPECIFICATION.md.

Then read, in order:
1. ste-code/artifacts/level*/system-prompt.txt (levels 1-4)
2. All files in ste-code/adapted/a-sec*-rule*.md (51 files)
3. ste-code/data/synonym-table.json
4. .agents/benchmark/benchmark_lib.py

Produce GROUNDING-REPORT.md with three sections:
A. CONFIRMED — items in the linguistic layer that already exist in adapted rules.
B. CONTRADICTION — items where the layer disagrees with an adapted rule.
C. NOVEL — items with no counterpart (expected: pragmatic intents, SRR collisions, scope bracketing, semantic domains).
```

**Output:** `ste-code/linguistics/GROUNDING-REPORT.md`

---

## Workflow 2 — Collision Table Enrichment

**Goal:** Grow the `domain_collisions` table from corpus evidence.

```
Scan ste-code/adapted/*.md for noun phrases matching "the <noun>" where <noun>
appears in two or more distinct rule contexts.

For each candidate: could a new reader mistake which entity this refers to?
If yes → add to domain_collisions with context-derived qualifier members.

Also mine .agents/benchmark/test-cases/*.json — sloppy-* and ste-base-*
inputs are deliberately ambiguous.

Output: semantics.json (expanded domain_collisions) + COLLISION-SOURCES.md
```

---

## Workflow 3 — Cross-Wire Semantic Roles into Adapted Rules

**Goal:** Bidirectional traceability between rules and semantic roles.

```
For each term in semantics.json → semantic_roles → term_table:
  Search ste-code/adapted/ for rule files that mention the term.
  Add non-destructive appendix block to each matching rule file:

  ---
  > Semantic layer: `deploy` — Action-only. Result form: `deployment`.
  > See ste-code/linguistics/semantics.json#semantic_roles.term_table.deploy

Conversely, add "rule_refs" array to each term in semantics.json.

Never edit normative text. Appendices only.
```

---

## Workflow 4 — Adversarial Benchmark Verification

**Goal:** Test the linguistic layer with existing benchmark infrastructure.

```
Run A: level2/system-prompt.txt as-is (baseline)
Run B: level2/system-prompt.txt + GENERATION-CONTRACT.md appended
Run C: level2/system-prompt.txt + contract + semantics.json inlined

Compare with rescore.py. Success criterion: B > A on P7/P13 tests,
no regression on P9 (brevity).
```

---

## Workflow 5 — Improve the Layer Itself

1. **Per-section referent tracking.** Implement heading-delimited section scoping.
2. **Compound-form exemptions.** Node.js contains node; deployment contains deploy. Add morphological pass.
3. **Counterexample hunting.** Run linter over repo's own docs. Every false positive → spec bug.
4. **Intent detection.** LLM-classify sentence intent; flag intent/form mismatches.

---

## Workflow 6 — Verb Frame Extraction

Scan adapted rules for verb usage patterns. Build verb frame table:
- Required complements (objects, prepositions)
- Forbidden frames (e.g., Action-terms as subjects of passive)
- Restructuring templates per frame violation

---

## Workflow 7 — Negation Scope Analysis

Rules for negation in code documentation:
- `not` before the verb, not after
- `no` for existence (`no file exists` not `a file does not exist`)
- Double negation → positive restatement
- Exception: `not only... but also` banned (scope ambiguity)

---

## Workflow 8 — Anaphora Resolution Rules

Cross-sentence pronoun resolution:
- `it`, `they`, `this`, `these`, `that`, `those`
- Each must resolve to antecedent in the SAME sentence
- Cross-sentence → replace pronoun with explicit noun
- `This function validates input. It returns a boolean.` → `This function validates input. The function returns a boolean.`

---

## Workflow 9 — Modifier Attachment Rules

Ambiguous modifier attachment patterns:
- `with <NP>` after verbs → ambiguous instrument or accompaniment
- `using <NP>` → preferred for instruments
- Series modifiers: `big red ball` vs `big, red ball`

Restructuring template per pattern.

---

## Workflow 10 — Definition Discipline

Rules for introducing and maintaining terminology:
- First use: bold + definition
- Subsequent use: consistent term
- No circular definitions
- No synonym chaining in definitions
- Glossary cross-reference format

---

## Workflow 11 — Corpus Conformance Scan

Run register classifier against repo docs:
- README.md → readme-prose check
- CONTRIBUTING.md → readme-prose check
- API docs → api-description check
- Error messages in code → error-message check

Report violations per register.

---

## Workflow 12 — Evidential & Epistemic Marking

Implement the epistemic classes from semantics.json#epistemic:
- Modal audit: scan for will/may/might/should
- Bare performance adjective detection
- Measured claim expiration check

---

## Workflow 13 — Imperative Address Model

Implement the Actor Registry:
- Classify every imperative by implied actor
- Count actor shifts per document section
- Flag >2 unmarked shifts per section

---

## Workflow 14 — Contrastive Minimal Pairs

Build pairs.jsonl corpus:
- Mine existing examples from adapted rules → seed
- Generate new pairs isolating one linguistic dimension
- Store as {dim, bad, good, rule_ref, source}
- Feed into benchmark as "minimal-pairs" test category

---

## Workflow 15 — Diachronic Layer

Backfill lifecycle states:
- Scan git history for term transitions
- Tag terms as current/deprecated/obsolete/emerging
- Add version tags to semantics.json entries

---

## Workflow 16 — Register Stratification

Implement register profiles from registers.json:
- Document/section register detection
- Register-specific rule application
- Register mixing detection

---

## Workflow 17 — Generative Constraints

A/B test generation with linguistic contract:
- Run A: base prompt
- Run B: base + contract
- Run C: base + contract + semantics.json

Score with rescore.py AND minimal-pairs benchmark.
