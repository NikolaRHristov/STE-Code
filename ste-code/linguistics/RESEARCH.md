# Research Foundation — Linguistic Layer

> **Version:** FLAVOR-1.0.0
> **Status:** Literature review complete. Empirical validation pending (Workflows 1, 11, 19).

---

## Key Sources

### Kuhn's CNL Classification (2014) — PENS Framework

**Citation:** Kuhn, T. "A Survey and Classification of Controlled Natural Languages." *Computational Linguistics*, 40(1):121–170, 2014. 636 citations.

**Framework:** Every CNL rule can be classified on four dimensions:
- **P** (Precision) — How sharply the rule constrains ambiguity
- **E** (Expressiveness) — How much natural language the rule permits
- **N** (Naturalness) — How close the output is to unconstrained English
- **S** (Simplicity) — How easy the rule is to learn and apply

**STE-Code assessment:** High on N and S, medium on P, E unmeasured.
**Historical lesson:** Caterpillar Fundamental English died in 1982 because *"the basic guidelines were not enforceable."* Every layer in FLAVOR-1.0.0 exists to make rules machine-checkable.

### Rimay CNL Study (2021) — Coverage Methodology

**Citation:** Rimay. "A Controlled Natural Language for Requirements." *PubMed*, 34776756, 2021.

**Method:** Built a CNL for requirements and measured that it could express 88% of 460 real-world statements.
**STE-Code application:** Run the linguistic layer over the repo's documentation corpus. Count expressible vs. violating sentences. Publish `coverage: X%` per standard version (Workflow 19).

### Attempto Controlled English (1995) — Use–Mention

**Citation:** Fuchs, N.E., Schwertel, U., Schwitter, R. "Attempto Controlled English — Not Just Another Logic Specification Language." *ILPS*, 1995.

**Finding:** The use–mention distinction (quoting vs. using a term) is solved with explicit quoting conventions. Directly applicable to STE-Code's code-block handling (Workflow 18).

### Carroll's Minimalism (1998) — Task-Oriented Documentation

**Citation:** Carroll, J.M. "Minimalism Beyond the Nurnberg Funnel." *ACM*, 1998.

**Finding:** Users don't read manuals cover-to-cover; they dip in at the moment of action.
**STE-Code application:** Register stratification (Workflow 16) matches text type to task context. Error messages, commit subjects, and CLI help are *action-moment* texts — they need different rules than README prose.

### Asciidoctest — Executable Documentation

**Citation:** `asciidoctest` (PyPI). Verifiable, stateful, interactive documentation.

**Finding:** Documentation that embeds executable code blocks can be automatically verified.
**STE-Code application:** Code Block Anatomy rules (Workflow 18) are the structural prerequisite for executable verification.

---

## PENS Classification of STE-Code Rules

Every adapted rule can be scored on Kuhn's PENS dimensions. Low-P rules (unenforceable mechanically) are priority candidates for table-ification in the linguistic layer.

| Rule | P | E | N | S | Priority |
|------|:-:|:-:|:-:|:-:|:--------:|
| 1.1 (vocabulary gate) | High | Med | High | High | — |
| 1.2 (part of speech) | High | Med | Med | Med | Table (SR) |
| 1.3 (single meaning) | Med | Med | Med | Med | Table (SRR) |
| 1.7 (noun as verb) | High | Med | High | High | Table (SR) |
| 1.9 (short nouns) | Low | Med | High | High | **Priority** |
| 1.11 (one term per concept) | Low | Med | Med | Med | **Priority** |
| 1.13 (verb as noun) | High | Med | High | High | Table (SR) |
| 3.6 (active voice) | Med | Low | Med | Med | Checker |
| 3.7 (verb not noun) | High | Med | Med | High | Table (SR) |
| 4.1 (sentence length) | High | Low | Med | High | REG check |
| 4.4 (demonstratives) | Med | Med | Med | Med | SRR check |
| 6.1 (one topic) | Low | Med | Med | Low | **Priority** |
| 7.1 (warning signals) | High | Med | High | High | — |
| 8.1 (no semicolons) | High | Med | High | High | — |

**Priority rules** (low-P, unenforceable): 1.9, 1.11, 6.1. These need the strongest table-ification.
**Table-ready rules** (high-P, mechanical): 1.2, 1.7, 1.13, 3.7 → already in `semantics.json#semantic_roles`.

---

## Research Frontiers (Workflows 19+)

### Workflow 19 — Coverage Metric

Apply Rimay's 88% method: run the full linguistic layer over the entire documentation corpus. Report `coverage: X%` per FLAVOR version. Track improvement across iterations.

### Workflow 20 — Translation Readiness

CNL research shows controlled text cuts post-editing time ~20%. Every layer (especially SRR and scope bracketing) compounds this. Measure translatability score per document.

### Workflow 21 — PENS Profiling

Classify all 51 STE-Code rules on Kuhn's PENS dimensions. Publish `PENS-profile.json`. Rules scoring low-P (unenforceable) get priority for table-ification.

### Workflow 22 — Historical Validation

Run the linguistic layer against Caterpillar Fundamental English documentation (if obtainable). Confirm that the enforceability gap that killed CFE is closed by FLAVOR's table-driven approach.
