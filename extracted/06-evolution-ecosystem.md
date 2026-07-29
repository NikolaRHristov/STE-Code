# ASD-STE100 — Evolution, Ecosystem, and Consolidated 53-Rule Reference

> Extracted and restructured from Perplexity conversation.
> Part 5 (final analytical part) of the 5-part deep dive.

---

## The Issue-by-Issue Evolution (1986–2025)

The ASD-STE100 standard has evolved through nine major issues over nearly four decades, each reflecting changes in technology, user feedback, and terminological science.

| Issue | Year | Designation | Key Changes |
|-------|------|-------------|-------------|
| Pre-release (Issue 0) | 1985 | AECMA Document PSC-85-16598 | First draft; used "technical term" for nouns, numbers, and symbols alike |
| Issue 1 | 1986 | AECMA Simplified English Guide | "Technical term" renamed to "technical name"; manufacturing processes renamed to "technical verbs" in Revision 2 (2001) |
| Issue 2 | 1995 | AECMA Simplified English Guide | Refined rules and dictionary; still positioned as a "guide" |
| Issue 3 | 2001 | AECMA Simplified English | Expanded verb categories; began transition from guide to specification |
| Issue 4 | 2005 | ASD-STE100 Specification | Renamed after AECMA merged into ASD (2004); transitioned from "guide" to "international specification" |
| Issue 5 | 2006 | ASD-STE100 Specification | Minor revisions; dictionary expansion |
| Issue 6 | 2013 | ASD-STE100 Specification | Became **free of charge**; 18,981 cumulative copies distributed across Issues 6–8 |
| Issue 7 | January 2017 | ASD-STE100 Specification | Rule count reduced from **65 to 53** through consolidation; full revision of writing rules' wording and examples; section titles changed (Section 5 → "Procedural writing," Section 7 → "Safety instructions"); dictionary column label changed from "keyword" to "word" |
| Issue 8 | April 2021 | ASD-STE100 Specification | Added a **decision flowchart** for word approval; refined dictionary entries; expanded technical name categories |
| Issue 9 | January 15, 2025 | ASD-STE100 **Standard** | Transitioned from "specification" to **"international standard"** (subtitle: "Standard for Technical Documentation"); "technical name" renamed to **"technical noun"**; new subject field categories added (Law and regulations; Animals, plants, and other life forms); dictionary examples de-aerospaceified (legacy aerospace examples reduced from 15% to 3%); verb type definitions added (regular, irregular, irregular auxiliary, defective modal); FAIR principles adopted for terminology management; AI integration task team established |

The next issue, **Issue 10, is scheduled for 2028**.

---

## The Meta-Terminological Shift in Issue 9

The most significant conceptual change in Issue 9 was the **meta-terminological review** — a systematic harmonization of the standard's own vocabulary with international terminological standards (ISO 1087, ISO 5127, ISO 12620-1).

### "Technical name" → "technical noun"

The legacy designation "technical name" had been used since Issue 1 (1986) to describe domain-specific nouns permitted outside the core dictionary. However, ISO 1087:2019 defines a "term" as "a designation that represents a general concept by linguistic means" — and "name" can be misleading in technical contexts, implying a proper noun rather than a general concept. Issue 9 replaced it with "technical noun," aligning with the ISO definition while retaining the adjective "technical" (despite some STEMG members advocating for "noun-type term").

### Subject field reclassification

The 19 technical noun categories were restructured and expanded, with new categories like "Law and regulations" and "Animals, plants, and other life forms" added under Rule 1.5. A similar restructuring was applied to technical verb subject fields under Rule 1.12.

### Verb type formalization

Issue 9 introduced formal definitions of verb types in the dictionary introduction:

- **Regular verbs**: REMOVE → REMOVES, REMOVED, REMOVED
- **Irregular verbs**: GO → GOES, WENT, GONE
- **Irregular auxiliary verbs**: HAVE, BE
- **Defective modal verbs**: CAN, MAY, WILL, SHALL

This was a contentious debate within the STEMG, as it required balancing linguistic precision with usability for technical writers who lack formal linguistic training.

### FAIR principles

Issue 9 adopted the **FAIR guiding principles** (Findable, Accessible, Interoperable, Reusable) for terminology management, ensuring that dictionary entries and subject field categories are structured for machine-readable access and cross-industry reuse.

---

## The Broader Controlled-Language Ecosystem

STE is not the only controlled natural language (CNL). It exists within an ecosystem of controlled languages developed for different industries and purposes:

| Controlled Language | Origin | Industry | Key Difference from STE |
|---------------------|--------|----------|------------------------|
| **ASD-STE100** | AECMA/ASD, 1986 | Aerospace & defense (now cross-industry) | ~875 approved words, 53 rules, 19 technical noun categories; the most formally specified CNL |
| **Basic English** | Charles Ogden, 1930 | General communication | 850 words, minimal grammar rules; predecessor concept but lacks formal writing rules |
| **Caterpillar Fundamental English (CFE)** | Caterpillar Inc., 1970s | Heavy equipment | ~800 words; designed for service documentation; narrower scope than STE |
| **Eastman Kodak KISL** | Kodak, 1970s | Photography/consumer | Controlled English for consumer documentation; industry-specific |
| **Plain Language (PL)** | US Government, 2010 | Government/regulatory | Mandates clarity and readability but **does not restrict vocabulary** — no approved-word dictionary; governed by the Plain Writing Act of 2010 |
| **Attempto Controlled English (ACE)** | University of Zurich, 2002 | Knowledge representation/logic | Designed for machine reasoning; translates to first-order logic; more restrictive than STE but aimed at computation, not human readability |
| **General Motors Simplified English** | GM | Automotive | Domain-specific controlled English; narrower industry focus |
| **NATO Standardization Agreement (STANAG)** | NATO | Military | References STE for documentation; not an independent CNL |
| **Special English** | Voice of America, 1959 | Broadcasting | ~1,500 words; designed for radio broadcasts, not technical documentation; simpler grammar but no formal rules |

The key differentiator of STE is its **dual architecture** (rules + dictionary), its **formal change management process** (Change Forms submitted to STEMG), and its **international standard status** as of Issue 9. No other controlled language has achieved this level of formalization, governance, and cross-industry adoption.

---

## Adoption Beyond Aerospace

As of the end of Issue 8 distribution (December 2024), **64% of STE users come from outside the aerospace and defense industries**. The specification is now actively used in:

- **Automotive** — major manufacturers adopting STE for service documentation
- **Railway** — rolling stock maintenance manuals
- **Healthcare and medical devices** — regulatory documentation and IFUs (Instructions for Use)
- **Renewable energy** — wind turbine and solar documentation
- **Offshore logistics** — oil and gas platform documentation
- **Pharmaceuticals** — GMP-compliant procedural documentation
- **Academia** — information engineering, applied linguistics, computational linguistics

---

## Tools and Checkers

Several software tools support STE compliance, though none are endorsed or certified by ASD:

| Tool | Developer | Approach |
|------|-----------|----------|
| Boeing Simplified English Checker (BSEC) | Boeing | 350-rule English parser augmented with STE-specific checks |
| HyperSTE | Etteplan | Plugin for content management systems; checks rules and dictionary compliance |
| Congree | Congree Language Intelligence | Linguistic algorithm-based checker; supports Issue 7 rules |
| TechScribe Term Checker | TechScribe | Term-level checker for ASD-STE100 compliance |
| Acrolinx | Acrolinx | Style guide platform supporting Issues 6, 7, and 8 with configurable rule sets |

However, the ASD explicitly warns that **"software does not think in place of authors"** — checkers can flag non-STE terms and grammar violations but *cannot convert non-STE text into STE* and cannot validate semantic compliance (Rule 9.1). This is the "Bag of Parts Fallacy" — having the dictionary and a checker (the "parts") does not guarantee compliant text (the "whole").

---

## Consolidated 53-Rule Reference Table

### Sections 1–9 Rules

| Rule | Section | Formal Constraint | Code Analogy |
|------|---------|-------------------|--------------|
| 1.1 | Words | Three permitted word classes: approved dictionary, technical nouns, technical verbs | Typed token set |
| 1.2 | Words | One part of speech per word | Type safety |
| 1.3 | Words | One meaning per word | Single-valued function |
| 1.4 | Words | Approved inflectional forms only | Fixed function signature |
| 1.5 | Words | Technical nouns permitted if in a subject field category | Import statement (typed) |
| 1.6 | Words | Unapproved words redeemable as technical nouns in context | Exception mechanism |
| 1.7 | Words | Technical nouns must not be used as verbs | Type boundary enforcement |
| 1.8–1.9 | Words | Nomenclature consistency; no slang/jargon | Naming convention linter |
| 1.10 | Words | No regional terms, slang, or jargon | Locale restriction |
| 1.11 | Words | Approved nomenclature standards | Standards compliance |
| 1.12 | Words | Technical verbs permitted if in an approved category | Verb import (typed) |
| 1.13 | Words | Technical verbs must not be used as nouns | Type boundary enforcement |
| 1.14 | Words | American English spelling mandatory | Locale setting (en-US) |
| 2.1 | Noun Clusters | Max 3 words per cluster | Nesting depth limit |
| 2.2 | Noun Clusters | Use prepositions to break long clusters | Explicit parenthesization |
| 2.3 | Noun Clusters | No noun clusters as verbs | No implicit type casting |
| 3.1 | Verbs | Approved verb forms only | Fixed function signature |
| 3.2 | Verbs | Imperative form for instructions | Function call syntax |
| 3.3 | Verbs | Only 4 approved tenses | Reduced grammar productions |
| 3.4 | Verbs | One verb form per sentence (unless conjoined) | One statement per basic block |
| 3.5 | Verbs | -ing form heavily restricted | Ambiguous production removal |
| 3.6 | Verbs | Active voice mandatory in procedures | Explicit invocation |
| 3.7 | Verbs | Passive voice restricted to descriptive, agent-irrelevant | Read-only accessor |
| 4.1 | Sentences | Max 20 words (procedural), 25 (descriptive) | Buffer size limit |
| 4.2 | Sentences | No word omission | No elision / fully qualified names |
| 4.3 | Sentences | Vertical lists with consistent format | Array initialization syntax |
| 4.4 | Sentences | Connecting words mandatory | Control-flow annotation |
| 5.1 | Procedural | One instruction per sentence | Single-responsibility principle |
| 5.2 | Procedural | Numbered steps | Ordered execution sequence |
| 5.3 | Procedural | Notes/cautions before related step | Precondition assertion |
| 5.4 | Procedural | Conditional "If [condition], [action]" | if-then block |
| 5.5 | Procedural | Standardized cross-reference language | Function call convention |
| 6.1 | Descriptive | Max 6 sentences per paragraph | Module size limit |
| 6.2 | Descriptive | One topic per paragraph | Single-responsibility (declarative) |
| 6.3 | Descriptive | Key phrases as signposts | Section header / docstring |
| 6.4 | Descriptive | Logical flow with connecting words | Control-flow annotation |
| 6.5 | Descriptive | Simple sentence structure (one-level clauses) | AST depth limit |
| 6.6 | Descriptive | No imperative in descriptive text | Separation of concerns (CQRS) |
| 7.1 | Safety | Two-part format: command + consequence | Typed exception with message |
| 7.2 | Safety | Place before related step | Precondition guard (@precondition) |
| 7.3 | Safety | Approved safety vocabulary only | Typed safety vocabulary |
| 8.1 | Punctuation | No semicolons | Token exclusion (no comma operator) |
| 8.2 | Punctuation | Word count enforcement | Runtime assertion of compile-time limit |
| 8.3 | Punctuation | Period as sole sentence terminator | Standardized statement terminator |
| 8.4 | Punctuation | Colons only for introducing lists | Type-specific operator restriction |
| 8.5 | Punctuation | Hyphens for approved compounds only | Compound token rule |
| 8.6 | Punctuation | Abbreviations defined on first use | Variable declaration pattern |
| 8.7 | Punctuation | Parentheses/quotes restricted to approved uses | No side-channel information |
| 9.1 | Practices | No word-for-word replacement without meaning check | Semantic type checking |
| 9.2 | Practices | Words used in approved sense only | Type safety enforcement |
| 9.3 | Practices | Instructions in correct order | Execution order invariant |
| 9.4 | Practices | Consistent style throughout | Style guide / linter rule |

### General Rules (GR1–GR4)

| GR | Constraint | Code Analogy |
|----|------------|--------------|
| GR1 | "That" restricted to demonstrative/relative pronoun | Overloaded token resolution |
| GR2 | "With" restricted to "together with" / "having" | Type restriction on polysemous word |
| GR3 | Pronouns must have unambiguous antecedent | Dangling reference check |
| GR4 | "This" must be followed by a noun | No void pointers (typed reference) |

---

## The Future: AI Integration and Issue 10

The STEMG has established a dedicated **AI task team** (composed of STEMG and STEST participants) exploring how artificial intelligence can enhance STE implementation. Areas under investigation include:

- AI-driven compliance checking
- Real-time feedback for writers
- Automated adaptation of terminological updates

The team is collaborating with university research projects on innovative AI tools.

**Issue 10, scheduled for 2028**, will likely incorporate the results of this AI exploration, further extend FAIR principles across additional domains, and continue the trend of de-aerospaceifying the dictionary examples to serve STE's increasingly diverse user base.

The transition from specification to standard with Issue 9 — and the parallel adoption of FAIR principles, ISO terminological harmonization, and AI readiness — positions ASD-STE100 not just as a writing standard but as a **data quality infrastructure** for the era of machine-readable technical communication, NLP, and AI-driven information systems.

---

## References

- https://www.asd-ste100.org/
- https://www.asd-ste100.org/about.html
- https://en.wikipedia.org/wiki/Simplified_Technical_English
- https://qabiria.com/en/resources/blog/controlled-language
- https://support.markup.ai/hc/en-us/articles/10210995127698-STE-Simplified-Technical-English
- https://www.youtube.com/watch?v=ffF-V7xQL68
