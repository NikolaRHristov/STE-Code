# STE-Code Flavor: Linguistic Layer v1.0.0

> **Flavor version:** FLAVOR-1.1.0
> **Base standard:** STANDARD-1.1.0 (54 rules, 22 categories, 8 levels)
> **Relationship:** Additive — extends STANDARD without modifying it
> **Status:** Specification complete; grounding, enrichment, and verification pending (see workflows)

---

## What This Is

The Linguistic Layer is a **closed-table, mechanical** extension to STE-Code STANDARD-1.0.0.
It adds 12 checking layers that operate on linguistic phenomena the current rule set
addresses implicitly but doesn't name explicitly. Every layer is:

- **A table** (closed set, no LLM judgment required at check time)
- **A repair** (mechanical fix per violation — no "rewrite this sentence" guidance)
- **A benchmark hook** (testable via the existing `.agents/benchmark/` harness)
- **An evidence path** (corpus or git history justifies each entry)

## Architecture

```
STANDARD-1.0.0                    FLAVOR-1.0.0
──────────────                    ────────────
ste-code/adapted/                 ste-code/linguistics/
  a-sec*-rule*.md (54 rules)        semantics.json        ← semantic roles + collisions
  a-dictionary.md (560 entries)     DECISION-TREE.md      ← rule application order
  a-categories.md (22 categories)   SPECIFICATION.md      ← full layer specification
                                    registers.json        ← register profiles
ste-code/artifacts/                 ste_code_lint.py      ← reference checker
  level1-5/system-prompt.txt        GENERATION-CONTRACT.md ← LLM generation rules
                                    WORKFLOWS.md          ← 17 implementation workflows
.agents/
  config/agents.yaml              (unchanged — both use same agent runner)
  benchmark/                      (extended — linguistic benchmark hooks)
```

## Layer Stack

| # | Layer | File | What It Checks |
|---|-------|------|----------------|
| 1 | Epistemic Marking | `semantics.json#epistemic` | Facts vs measured claims vs expectations |
| 2 | Actor Model | `semantics.json#actors` | Who acts in each sentence |
| 3 | Single Referent Rule | `semantics.json#single_referent` | Ambiguous cross-sentence references |
| 4 | Semantic Roles | `semantics.json#semantic_roles` | Word class legality (Action/Result/Entity) |
| 5 | Verb Frames | `semantics.json#verb_frames` | Argument completeness |
| 6 | Negation Control | `SPECIFICATION.md#negation` | Double negation, scope of negation |
| 7 | Scope Bracketing | `SPECIFICATION.md#scope` | Modifier attachment ambiguity |
| 8 | Discourse/Anaphora | `SPECIFICATION.md#discourse` | Cross-sentence pronoun resolution |
| 9 | Quantifier Table | `semantics.json#quantifiers` | Vague quantifiers → precise alternatives |
| 10 | Register Profiles | `registers.json` | Sentence length, articles by text type |
| 11 | Lifecycle States | `semantics.json#lifecycle` | Term deprecation/graduation tracking |
| 12 | Definition Discipline | `SPECIFICATION.md#definitions` | Term provenance and glossary hygiene |

## Quick Start

```bash
# Run the reference linter on a document
python3 ste-code/linguistics/ste_code_lint.py sample-doc.md

# Run with semantic layer enabled
python3 ste-code/linguistics/ste_code_lint.py sample-doc.md --flavor FLAVOR-1.0.0

# Ground the linguistic layer against adapted rules (Workflow 1)
# See ste-code/linguistics/WORKFLOWS.md
```

## Relationship to STANDARD

- **FLAVOR extends STANDARD.** No rule is removed or weakened.
- **FLAVOR is optional.** Documents can conform to STANDARD-1.0.0 without FLAVOR.
- **FLAVOR is additive.** Every FLAVOR layer adds precision, never removes coverage.
- **FLAVOR is testable.** Every layer has benchmark hooks in `.agents/benchmark/`.

## Version Policy

| Version | Base | Changes |
|---------|------|---------|
| STANDARD-1.0.0 | — | 54 rules, 22 categories, 8 level prompts |
| FLAVOR-1.0.0 | STANDARD-1.0.0 | 12 linguistic checking layers + 18 workflows |

Future versions: MINIMAL-PAIRS-1.0.0 (corpus), DIACHRONIC-1.0.0 (temporal), GENERATIVE-1.0.0 (LLM contract).

## Precedence Stack

When multiple layers flag the same sentence, resolve in this order:

```
truth/identifiers
  > safety (Warning/Prohibition)
    > reference (SRR + discourse)
      > negation
        > intent/form
          > semantic roles/domains
            > verb frames
              > quantifiers
                > structure (scope)
                  > register fit
                    > consistency
                      > brevity
```

## Master Roadmap

See [`docs/roadmap/ROADMAP.md`](../../docs/roadmap/ROADMAP.md) for the 6-phase implementation plan:

| Phase | Name | Deliverable |
|:-----:|------|-------------|
| 0 | State Reconciliation | STATE-RECONCILIATION.md |
| 1 | Grounding | GROUNDING-REPORT.md |
| 2 | Self-Conformance | SELF-CONFORMANCE.md + coverage metric |
| 3 | Complete Specification | discourse.json + registers.json + specs |
| 4 | Benchmark Integration | BENCHMARK-RESULTS.md |
| 5 | Harden Checker | 5 linter fixes |
| 6 | Living Standard Loop | Continuous graduation + lifecycle |

## Exit Criteria

- [ ] Phase 0 reconciliation committed
- [ ] Grounding report: 0 unresolved contradictions
- [ ] Coverage metric published; tracked per version
- [ ] All 3 spec stores complete
- [ ] Benchmark A/B/C run; minimal-pairs category live
- [ ] Linter hardened through all 5 fixes
- [ ] Graduation + lifecycle loop operational
