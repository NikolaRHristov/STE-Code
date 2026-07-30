# Phase 1 — Grounding Report


Date: 2026-07-30

# Batch 5 — Grounding Audit Report
## 11 files from sec8 and sec9

**Auditor:** STE-Code Grounding Auditor (batch 5/5)
**Date:** 2026-07-30
**Files audited:** a-sec8-rule8.4.md, a-sec8-rule8.5.md, a-sec8-rule8.6.md, a-sec9-gr1.md, a-sec9-gr2.md, a-sec9-gr3.md, a-sec9-gr4.md, a-sec9-rule9.1.md, a-sec9-rule9.2.md, a-sec9-rule9.3.md, a-sec9-rule9.4.md

---

## PART 1: SR CLAIMS (Semantic Role — Action Terms)

### CONFIRMED

| Claim | Rule File | Line | Notes |
|-------|-----------|------|-------|
| 'deploy' is an Action term | a-sec1-rule1.7.md | 269 | "deploy (code-domain technical verb, category 1 c)" |
| 'deploy' is an Action term | a-sec1-rule1.13.md | 259 | Dual-category: verb (cat 1c) and noun (cat 5) — explicitly listed |
| 'deploy' result form | a-sec1-rule1.13.md | 130 | "'deploy' can be both a code-domain technical verb...and a code-domain technical noun" |
| 'run' is an Action term | a-sec1-rule1.3.md | 59 | "run — Approved meaning: 'execute a program or command'" |
| 'commit' used as action verb | a-sec1-rule1.7.md | 245 | "'commit the changes'" in Extended Examples (STE translation) |
| 'commit' used as action verb | a-sec1-rule1.7.md | 449 | "'Commit the changes'" in preposition phrase repair table |
| 'test' used in procedural context | a-sec5-rule5.3.md | 215-219 | "'unit tests,'" "'Execute the unit tests,'" spec adaptation pairs |

### CONTRADICTION

| Claim | Rule Says | Layer Says |
|-------|-----------|------------|
| 'compile' result form = 'compilation' | Rule 1.13:276 states "'compile' is not a dual-category word → VIOLATION"; Rule 1.13:248 states "Compile does not fit any technical noun category naturally — it is only a technical verb" | Layer claims 'compilation' as result form of 'compile'. Rules explicitly prohibit nominalizing 'compile'. The word "compilation" does not appear as an approved noun form in the rules. |
| 'deploy' result form = 'deployment' | Rule 1.13:130, 259 — the noun form used is 'deploy' (not 'deployment'): "'the deploy' is correct" (line 248), "deploy | Category 5) Infrastructure, deployment, and platforms" | Layer claims result form is 'deployment' — rules consistently use 'deploy' as the noun form. 'Deployment' appears only as a category name, not as the preferred noun form. |

### NOVEL

| Claim | Description |
|-------|-------------|
| 'build' action term referenced in a-sec1-rule1.7.md | Rule 1.7 has ZERO mentions of 'build' anywhere in 513 lines. The claim's reference is to the wrong file. 'build' IS a dual-category term (verb/noun), but it is documented in a-sec1-rule1.13.md:258, NOT in a-sec1-rule1.7.md. |
| 'compile' action term referenced in a-sec1-rule1.9.md | Rule 1.9 has 'compile' only as 'compile-time' (adjective, lines 153, 157) and 'compiler' (lines 155, 230). It does NOT address 'compile' as an action term. The correct file is a-sec1-rule1.13.md (lines 116-117, 248, 276). |
| 'configure' action term referenced in a-sec1-rule1.9.md | Rule 1.9 mentions 'configuration' as a noun in shortening examples (lines 91, 139, 292) but does NOT address 'configure' as a verb. 'configure' as an imperative verb appears in a-sec5-rule5.3.md:48. The reference points to the wrong file. |
| 'validate' action term referenced in a-sec3-rule3.7.md | Rule 3.7 has ZERO mentions of 'validate' or 'validation.' The file is about "Use an Approved Verb to Describe an Action, Not a Noun or Other Parts of Speech." It does not explicitly name 'validate' anywhere. No counterpart found. |
| 'install' action term referenced in a-sec5-rule5.1.md | Rule 5.1 mentions 'installation' as a noun (lines 33, 76) but does not classify 'install' as an action term. 'install' as an imperative verb is listed in a-sec5-rule5.3.md:48. The reference is to a sentence-length rule that uses the word incidentally. |
| 'test' action term referenced in a-sec5-rule5.3.md | Rule 5.3 uses 'test' in compound nouns (unit tests, test suite) and code commands (`npm test`). It does NOT explicitly classify 'test' as an Action term. The rule's imperative verb list (line 48) does NOT include 'test.' 'test' is a dual-category term documented in a-sec1-rule1.13.md:260, not in rule 5.3. |
| 'migrate' action term referenced in a-sec5-rule5.4.md | Rule 5.4 uses 'migration' extensively (lines 46, 48, 190, 192, 194, 290, 462, 468) but 'migrate' as a standalone verb does not appear. The pattern is "run the migration script." The action 'migrate' is implied by the noun 'migration' but never explicitly categorized. |

---

## PART 2: SRR CLAIMS (Semantic Role Resolution — Domain Collisions)

All 10 SRR collision domain claims fall under **NOVEL**. None of the 11 adapted rule files in this batch (sec8 rules 8.4-8.6, sec9 GR-1 through GR-4, sec9 rules 9.1-9.4) explicitly address domain collision qualification for any of these terms.

### NOVEL

| Claim | Description |
|-------|-------------|
| 'deployment' has domain collisions: pipeline deployment, deployment resource, deployment artifact | None of the 11 files mention these qualifiers. 'deployment' appears in sec9-rule9.1:388, sec9-rule9.3:228/300/312 as a general noun, never with collision disambiguation. |
| 'build' has domain collisions: build process, build artifact, build pipeline | None of the 11 files contain these qualifiers. 'build' appears in sec8 files (8.3, 8.4, 8.6) and sec9 files as the verb or noun 'build' in examples, but never with collision-domain qualifiers like 'build process' or 'build artifact.' |
| 'config' has domain collisions: config file, configuration values, configuration system | 'configuration' appears throughout (sec8-rule8.4, sec9-rule9.1, sec9-rule9.2, sec9-gr3) primarily as "configuration file." The specific collision-qualifier subtypes are not addressed. |
| 'service' has domain collisions: service instance, service endpoint, system service | 'service' appears in sec9-rule9.1, sec9-rule9.3, sec9-gr3, sec9-gr4 in general usage. No collision-domain qualifiers are provided. |
| 'token' has domain collisions: auth token, syntax token, API token | 'token' appears in zero of the 11 files. No collision-domain qualifiers found. |
| 'cache' has domain collisions: cache store, cached data, cache command | 'cache' appears in sec9-gr4:64, sec9-rule9.1:346 general usage only. No collision-domain qualifiers. |
| 'log' has domain collisions: log entry, log file, logging system | 'log' appears in sec9 files (9.2, 9.3, 9.4) in general usage. The sec8 files contain no explicit 'log' collision qualifiers. |
| 'test' has domain collisions: test case, test suite, run tests | 'test' appears in sec9 files (9.2, 9.4) in general usage. No collision-qualifier subtypes. |
| 'request' has domain collisions: HTTP request, API request, work request | 'request' appears in sec9 files (9.2, 9.3, gr3, gr4) in general usage. No collision-qualifier subtypes. |
| 'model' has domain collisions: ML model, data model, domain model | 'model' appears zero times in any of the 11 files. |

---

## PART 3: WRONG REFERENCES

The following claim references point to non-existent or incorrect rule files:

| Claim | Claimed Reference | Actual Status |
|-------|-------------------|---------------|
| 'build' as Action term | a-sec1-rule1.7.md | **0 mentions of 'build' in rule 1.7** — correct file is a-sec1-rule1.13.md:258 |
| 'compile' as Action term | a-sec1-rule1.9.md | Rule 1.9 only has 'compile-time' (adj) — correct file is a-sec1-rule1.13.md:116-117, 248, 276 |
| 'configure' as Action term | a-sec1-rule1.9.md | Rule 1.9 only has 'configuration' (noun) — 'configure' as verb is in a-sec5-rule5.3.md:48 |
| 'validate' as Action term | a-sec3-rule3.7.md | **0 mentions of 'validate'** — no counterpart found in any referenced rule |
| 'run' as Action term | a-sec1-rule1.3.md | Initially returned 0 search hits via CCR, but manual read confirms 'run' IS defined at a-sec1-rule1.3.md:59 — reference is valid; the initial false-negative was a search tool artifact |
| 'test' as Action term | a-sec5-rule5.3.md | Rule 5.3 uses 'test' but only in compound nouns — correct classification as Action term is in a-sec1-rule1.13.md:260 |

---

## PART 4: COMPLETENESS CHECK

### Do all 10 semantic role terms have corresponding rule references?

| # | Term | Has Valid Rule Reference? | Correct File | Status |
|---|------|--------------------------|--------------|--------|
| 1 | deploy | YES | a-sec1-rule1.7.md:269, a-sec1-rule1.13.md:130,259 | Valid |
| 2 | build | NO — wrong ref | a-sec1-rule1.13.md:258 (actual) | Reference points to wrong file |
| 3 | compile | NO — wrong ref | a-sec1-rule1.13.md:116-117,248,276 (actual) | Reference points to wrong file |
| 4 | test | PARTIAL | a-sec5-rule5.3.md (weak), a-sec1-rule1.13.md:260 (correct) | Reference file doesn't classify the term |
| 5 | run | YES | a-sec1-rule1.3.md:51,59 | Valid |
| 6 | install | PARTIAL | a-sec5-rule5.1.md (weak), a-sec5-rule5.3.md:48 (correct) | Reference file only uses as noun |
| 7 | configure | NO — wrong ref | a-sec5-rule5.3.md:48 (actual) | Reference points to wrong file |
| 8 | validate | NO — no reference | NONE | No counterpart found in any rule |
| 9 | commit | PARTIAL | a-sec1-rule1.7.md:245,449 (verb in examples) | Used as verb but not classified explicitly |
| 10 | migrate | PARTIAL | a-sec5-rule5.4.md (noun 'migration' only) | 'migrate' verb not explicitly used |

**Result: 2/10 fully confirmed with correct references. 5/10 have partially valid references (term appears but not classified as Action term, or reference is to wrong file). 2/10 have no counterpart in referenced rules. 1/10 points to a file but the correct classification is elsewhere.**

### Do all 10 collision domains have examples in adapted rules?

**Result: 0/10.** None of the 11 adapted rule files explicitly address domain collision qualification. The collision domain claims represent net-new linguistic analysis that the adapted rules do not currently capture. All 10 fall under NOVEL.

### Are any rule references wrong?

**Result: 4 of 10 SR claim references are wrong** (pointing to the wrong file for the concept). See WRONG REFERENCES table above.

---

## SUMMARY

| Category | Count |
|----------|-------|
| CONFIRMED | 7 findings (across 5 SR terms) |
| CONTRADICTION | 2 findings (compile→compilation; deploy→deployment form mismatch) |
| NOVEL | 16 findings (6 SR references, 10 SRR collision domains) |
| Wrong References | 5 of 10 SR claims have incorrect or sub-optimal file references |
| SRR Coverage in 11 Files | 0/10 collision domains are addressed |

### Critical Issues

1. **'compile' is the only term with a hard contradiction.** Rule 1.13 explicitly states 'compile' is NOT a dual-category word and has no approved noun form. The linguistic layer claim of 'compilation' as a result form directly conflicts with this.

2. **'deploy' → 'deployment' is a soft mismatch.** Rules use 'deploy' as the noun form (e.g., "the deploy"). 'Deployment' appears only as a category name, not as the term's canonical noun form.

3. **5 of 10 SR references are wrong or sub-optimal.** The linguistic layer appears to have been generated without verifying the actual content of the referenced files. Key files like a-sec1-rule1.13.md (which is the central repository for dual-category classifications) were overlooked in favor of less relevant files.

4. **All 10 SRR collision domains have zero coverage in the 11 adapted files.** These are genuine linguistic-layer insights that the adapted rules do not yet address.


---
