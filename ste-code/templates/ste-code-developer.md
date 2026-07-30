---
id: ste-code-developer
version: 3.0.0
tokens: ~2000
use-when: extending the standard, adding domain support, building tooling
source: Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe, Brussels. © ASD, 2025. STE is EU Trade Mark 017966390. Independent adaptation not endorsed by ASD. asd-ste100.org
---

# STE-Code Developer Guide v3.0

This guide is for developers who extend STE-Code — adding new domains, vocabulary, rules, or building tooling.

---

## STANDARD ARCHITECTURE

STE-Code is organized into 9 sections with 51 rules, adapted from ASD-STE100 Issue 9.

| Section | Title | Rules | Purpose |
|---------|-------|-------|---------|
| 1 | Words | 1.1–1.14 | Vocabulary control, technical nouns, technical verbs |
| 2 | Noun Phrases | 2.1–2.2 | Multi-word noun limits, shorter forms |
| 3 | Verbs | 3.1–3.7 | Verb forms, active voice, tenses |
| 4 | Sentences | 4.1–4.5 | Sentence clarity, structure |
| 5 | Procedures | 5.1–5.5 | Imperative instructions, word limits |
| 6 | Descriptive Writing | 6.1–6.5 | Explanatory text rules |
| 7 | Warnings, Cautions, Notes | 7.1–7.3 | Safety markers and risk levels |
| 8 | Punctuation | 8.1–8.6 | Punctuation rules, word count |
| 9 | Writing Practice | 9.1–9.4 | Restructuring, phrasal verbs, style |

### Key Architecture Decisions

**Three-Gate Vocabulary Model (Rule 1.1):** Every word must pass through Gate 1 (approved word), Gate 2 (code-domain technical noun, 19 categories), or Gate 3 (code-domain technical verb, 4 categories). If a word cannot pass any gate, replace it or restructure the sentence.

**Technical Noun Categories (Rule 1.5, 19 categories):** Code components, devices, tools, data types, infrastructure, systems, algorithms, UI elements, units, quoted text, roles, documents, runtime, colors, defects, CS terms, legal, databases, networks.

**Technical Verb Categories (Rule 1.12, 4 categories):** Manufacturing processes, computer processes, subject-field instructions, law/regulations.

**Authority Hierarchy for Technical Nouns (Rule 1.8):** source code > language specification > framework docs > project glossary > industry standard > company docs.

**Safety Markers (Rule 7.1):** WARNING for security/data-loss risks. CAUTION for unexpected-behavior/performance risks.

---

## FILE ORGANIZATION

```
ste-code/
├── adapted/           # 51 deepened rule files (a-secN-ruleN.M.md)
├── templates/         # System prompt templates
│   ├── ste-code-micro.md      # ~500 tokens, minimal
│   ├── ste-code-full.md       # ~4,000 tokens, all 51 rules
│   ├── ste-code-agentic.md    # ~2,500 tokens, agent behavior
│   └── ste-code-developer.md  # ~2,000 tokens, extension guide
├── a-dictionary.md    # Controlled terminology
└── a-categories.md    # 22 category definitions
```

---

## ADDING A NEW DOMAIN

To adapt STE-Code to a new domain (e.g., aerospace, medical, legal):

1. **Map technical noun categories.** Create domain-specific subcategories under the 19 existing Rule 1.5 categories. Each subcategory must have a clear name, description, and example terms.

2. **Map technical verb categories.** Create domain-specific subcategories under the 4 existing Rule 1.12 categories. Define which operations are unique to the domain.

3. **Add approved terms.** Extend the controlled terminology with domain-approved words. Each entry requires: word, part of speech, approved meaning, approved forms (for verbs/adjectives), and domain tag.

4. **Add synonym mappings.** Extend the synonym table with domain-specific prefer/avoid pairs. Each mapping must specify which domain it applies to.

5. **Adapt safety markers.** If the domain has different risk levels than code documentation, adjust the WARNING/CAUTION criteria from Rule 7.1.

6. **Generate domain template.** Create `ste-code-{domain}.md` by combining the core rules with domain-specific extensions.

---

## ADDING A NEW RULE

Rules follow the deepened format established in `ste-code/adapted/`:

1. **Create rule file:** `a-sec{section}-rule{section}.{number}.md`

2. **Required sections:**
   - `# Rule X.Y — Title`
   - `> Source: Adapted from ASD-STE100 Issue 9, Rule X.Y`
   - `## Original Rule` — the verbatim ASD-STE100 rule text
   - `## STE-Code Adaptation` — the adapted rule for code documentation
   - `## Code-Domain Explanation` — how the rule applies to READMEs, API docs, docstrings, commit messages, error messages
   - `## Paradigm-Specific Guidance` — guidance for OOP, functional, procedural, declarative, systems paradigms
   - `## Extended Examples` — 5-6 non-STE/STE example pairs with principle citations
   - `## Edge Cases` — 4-6 tricky boundary scenarios with resolution guidance
   - `## Cross-References` — table of related rules with relationship descriptions
   - `## Grammar Notes` — detailed grammatical analysis and application guidance

3. **Example pairs must include:**
   - The non-STE version (Before)
   - The STE version (After)
   - Which principle was applied (P1-P14 or specific rule number)
   - An explanation of the fix

4. **Update the rule index.** Add the new rule to the section's rule list in this document and in the full template.

---

## ADDING A NEW VOCABULARY TERM

1. **Determine the gate.** Is the term an approved word (Gate 1), a technical noun (Gate 2), or a technical verb (Gate 3)?

2. **For Gate 1 (approved word):** Add to the controlled terminology. Specify: word, part of speech, approved meaning, approved forms, usage example.

3. **For Gate 2 (technical noun):** Assign to one or more of the 19 categories from Rule 1.5. Add to the project glossary with: term, category, approved meaning, example sentence.

4. **For Gate 3 (technical verb):** Assign to one or more of the 4 categories from Rule 1.12. Add to the project glossary with: term, category, approved meaning, example of correct use as a verb.

5. **Add synonym mapping.** If the new term replaces existing non-approved terms, add entries to the synonym table with prefer/avoid pairs.

6. **Cross-reference rules.** Check that the new term does not violate Rule 1.2 (part of speech), Rule 1.3 (approved meaning), Rule 1.7 (noun as verb), Rule 1.10 (slang/jargon), Rule 1.11 (one term per concept), or Rule 1.13 (verb as noun).

---

## BUILDING A COMPLIANCE CHECKER

A compliance checker must validate text against each applicable rule:

**Vocabulary checks (Section 1):**
- Every word passes the three-gate model (Rule 1.1)
- Approved words used as correct part of speech (Rule 1.2)
- No technical nouns used as verbs (Rule 1.7)
- No technical verbs used as nouns (Rule 1.13)
- One term per concept throughout (Rule 1.11)
- No slang, jargon, or regional terms (Rule 1.10)
- American English spelling (Rule 1.14)

**Structure checks (Sections 2-6):**
- Multi-word nouns ≤ 3 words (Rule 2.1)
- Procedural sentences ≤ 20 words (Rule 5.1)
- Descriptive sentences ≤ 25 words (Rule 6.1)
- Imperative mood in procedures (Rule 5.2)
- One instruction per step (Rule 5.4)
- Active voice in descriptive text (Rule 6.3)
- No -ing forms as main verbs in procedures (Rule 3.7)

**Safety checks (Section 7):**
- WARNING before security/data-loss risks (Rule 7.1)
- CAUTION before unexpected-behavior risks (Rule 7.1)
- Notes are supplementary only (Rule 5.5)

**Punctuation checks (Section 8):**
- No semicolons in prose (Rule 8.1)
- Quoted text preserved verbatim (Rule 8.6)

**Writing practice checks (Section 9):**
- Restructured when word-for-word fails (Rule 9.1)
- No phrasal verbs (Rule 9.3)
- Consistent style throughout (Rule 9.4)

---

## ADDING A NEW PROMPT TEMPLATE

1. Create the template in `ste-code/templates/` with the naming convention `ste-code-{purpose}.md`.

2. Include YAML frontmatter with: `id`, `version`, `tokens` (estimated token count), `use-when` (when to load this template), and `source` (ASD-STE100 attribution).

3. Reference specific rule numbers for all behavioral constraints. Never state a rule without its number: "Keep procedural sentences ≤ 20 words (Rule 5.1)" not "Keep sentences short."

4. Use examples drawn from the deepened rule files where possible. Cite the rule file: `(see Rule 1.1, a-sec1-rule1.1.md)`.

5. Target the specified token budget. Templates are loaded into context windows. Exceeding the budget degrades agent performance.

---

## VALIDATION CHECKLIST

Before finalizing any STE-Code extension:

- [ ] All rule numbers referenced are correct
- [ ] All synonym mappings have both prefer and avoid columns
- [ ] All technical noun categories referenced exist in Rule 1.5 (19 categories)
- [ ] All technical verb categories referenced exist in Rule 1.12 (4 categories)
- [ ] Safety markers (WARNING/CAUTION/NOTE) match Rule 7.1 criteria
- [ ] Sentence length limits match Rule 5.1 (20 words procedural) and Rule 6.1 (25 words descriptive)
- [ ] No semicolons used in prose (Rule 8.1)
- [ ] No contractions used
- [ ] American English spelling used throughout (Rule 1.14)
- [ ] ASD-STE100 attribution included in frontmatter
