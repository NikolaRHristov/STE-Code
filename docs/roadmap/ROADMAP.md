# STE-Code Linguistic Layer — Master Integration Roadmap

> **Version:** FLAVOR-1.0.0
> **Status:** Plan complete. Phase 0 (state reconciliation) is the blocker — nothing proceeds until it completes.
> **Rule:** Additive only — nothing deleted, no rule text modified. Appendices, new files, and new directories only.

---

## Phase 0 — Reconcile State (blocker)

```
1. Verify repo state on Current:
   - Confirm merged PRs and current branch state.
   - List ste-code/ tree: adapted/ (57 files), artifacts/ (5 levels),
     data/, refined/, enriched-code/.
   - Diff local agent's parse of remote work against this plan's file map.

2. Confirm input artifacts exist:
   - semantics.json, DECISION-TREE.md, SPECIFICATION.md,
     ste_code_lint.py, sample-doc.md
   - README credits block (research references)
   - CODE-BLOCK-SPEC.md, RESEARCH.md, registers.json
   - GENERATION-CONTRACT.md, WORKFLOWS.md, FLAVOR.md

3. Create target structure:
   ste-code/linguistics/          # the layer itself
     semantics.json
     discourse.json               # to be created (Phase 3)
     registers.json
     DECISION-TREE.md
     SPECIFICATION.md
     DISCOURSE-SPEC.md            # to be written (Phase 3)
     REFERENCES.md                # full credits + research links
   tests/linguistics/             # corpus + fixtures
   docs/roadmap/                  # reports produced by this plan
```

**Deliverable:** `docs/roadmap/STATE-RECONCILIATION.md`

---

## Phase 1 — Grounding (Workflow 1, mandatory)

Verify every claim in the linguistic layer against actual repo content.

```
Read: linguistics/* + all level prompts + all 58 adapted rule files
      + data/synonym-table.json + benchmark_lib.py

Produce docs/roadmap/GROUNDING-REPORT.md:
  A. CONFIRMED — layer items already present in adapted rules (cite file:line)
  B. CONTRADICTION — layer vs. rule conflicts; quote both sides; DO NOT resolve
  C. NOVEL — net-new value (intents, SRR, scope, domains, discourse, registers,
     epistemic, lifecycle)
```

**Exit criterion:** Zero unresolved section-B items before Phase 4.

---

## Phase 2 — Self-Conformance & Coverage (Workflow 11 + coverage metric)

```
1. Lint: adapted/*.md, all level prompts, all SKILL.md, all READMEs.
2. Classify findings: doc bug → fix; false positive → spec bug;
   mention-context → use–mention exemption rule.
3. Coverage: percentage of corpus sentences expressible without violation.
   Publish as "coverage: X% @ semantics v1.0" — tracked per version.
4. Classify text by register: error strings, commit subjects, prose,
   API descriptions, comments, CLI help.
```

**Deliverables:** `docs/roadmap/SELF-CONFORMANCE.md`, coverage figure, use–mention rule.

---

## Phase 3 — Complete the Specification (Workflows 6–10, 12–13, 15–18)

### discourse.json
- Anaphora table (this/it/they/former-latter/ellipsis)
- Quantifier table (vague → required precision form)
- Verb frames (seed 10 → corpus-complete inventory)
- Negation rules + antonym table
- Definition discipline (first-use, inventory, graduation)

### semantics.json extensions
- Epistemic rules: Specified / Measured(+date) / Expected classes; modal bans
- Actor model: 4 actors, one-per-sentence, labeled handoff pattern
- Lifecycle: per-entry states + changelog (current / deprecated:DATE / obsolete:DATE / emerging)

### registers.json
- 6 register profiles calibrated against Phase 2 register census

### SPECIFICATION.md + CODE-BLOCK-SPEC.md
- 5-element code-block contract, copy-paste integrity rule

**Method note:** Corpus-mining uses POS-based noun-phrase candidate extraction + C-value/TF-IDF filtering. Requirements-glossary line (GlossEx; Sharma et al. semantic filter) applies for definition inventory. Acrolinx lifecycle (extract → validate → manage → check) is the reference pipeline.

---

## Phase 4 — Benchmark Integration (Workflows 4, 14, 17)

```
1. Minimal-pairs corpus (pairs.jsonl):
   - {dim, bad, good, rule_ref, source}; one dimension per pair
   - ≥3 pairs per semantics table; ≥1 per adapted rule
   - Add "minimal-pairs" test category to benchmark.

2. Generation contract A/B/C:
   - Run A: level2 prompt (baseline)
   - Run B: + generation contract
   - Run C: + contract + semantics.json inlined
   - Score with rescore.py + minimal-pairs discrimination.
   - Tag all runs with semantics version.

3. Report: docs/roadmap/BENCHMARK-RESULTS.md
```

---

## Phase 5 — Harden the Checker (Workflow 5.x)

1. Per-section referent tracking — heading-delimited scoping, qualification reset.
2. Compound-form exemptions — `Node.js` ⊃ `node`, `deployment` ⊃ `deploy`; data-driven.
3. Mention-context exemption — quoted/italic terms in normative text exempt.
4. Register-aware rule gating — violation only within the register profile.
5. LLM-augmented intent detection — probabilistic, with per-finding confidence logged.

---

## Phase 6 — Living Standard Loop (continuous)

```
1. Term graduation: doc-local term in ≥3 documents → propose (emerging → current).
2. Lifecycle backfill: scan git history for term transitions.
3. conform_to front-matter on all docs; linter warns on version drift.
4. Quarterly: re-run Phase 2 coverage; coverage must not regress.
```

---

## Final File Map

```
ste-code/linguistics/
  semantics.json        roles, domains, collisions, intents, epistemic, actors, lifecycle
  discourse.json        anaphora, quantifiers, verb frames, negation, definitions
  registers.json        6 register profiles
  DECISION-TREE.md      author procedure (steps 0–8)
  SPECIFICATION.md      SRR + scope + code-block anatomy
  DISCOURSE-SPEC.md     W6–W10 formal spec
  REFERENCES.md         full credits + research links
tests/linguistics/
  pairs.jsonl           minimal-pairs corpus
  sample-doc.md         linter fixture
docs/roadmap/
  STATE-RECONCILIATION.md
  GROUNDING-REPORT.md
  SELF-CONFORMANCE.md
  BENCHMARK-RESULTS.md
```

## Precedence Stack (normative, final)

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

## Exit Criteria

- [ ] Phase 0 reconciliation committed
- [ ] Grounding report: 0 unresolved contradictions
- [ ] Coverage metric published; tracked per version
- [ ] All 3 spec stores complete; every rule class has table + repair + hook + evidence
- [ ] Benchmark A/B/C run; minimal-pairs category live; results versioned
- [ ] Linter hardened through all 5 fixes; false-positive log near-empty
- [ ] Graduation + lifecycle loop operational; first quarterly coverage re-run scheduled
