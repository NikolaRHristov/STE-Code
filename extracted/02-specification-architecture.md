# ASD-STE100 — The 53 Writing Rules: Complete Specification Architecture

> Extracted and restructured from Perplexity conversation.
> Part 1 of the 5-part deep dive.

---

## Architecture Overview

The ASD-STE100 standard (current Issue 9, January 2025) is organized as a **two-part controlled-language system**: a rule-based grammar engine (Part 1) and a constrained lexical database (Part 2). It is a formal grammar for English — analogous to how a programming language defines syntax rules and a reserved-word table.

Part 1 contains **53 rules across 9 sections**, reduced from 65 rules in Issue 6 through consolidation. Each rule has a short imperative statement, explanatory prose, and STE/non-STE example pairs — functioning like assertions in a formal specification.

---

## The "UML" of STE: A Formal Relationship Model

While the specification does not contain actual UML diagrams, its architecture can be modeled using UML-like relationships to normal English:

| STE Concept | Normal English Equivalent | UML Relationship |
|-------------|---------------------------|------------------|
| Approved word (dictionary) | A standard English word | **Specialization** — a subset of English vocabulary |
| Technical noun | Any domain noun | **Extension** — extends vocabulary via category membership |
| Technical verb | Any domain verb | **Extension** — extends verb set via category membership |
| Writing rule | A grammar/style guideline | **Constraint** — UML invariant on text production |
| Approved meaning | The full semantic range of a word | **Restriction** — narrows the semantic field to one sense |
| Unapproved word + alternative | Synonym in standard English | **Substitution** — one-to-one replacement mapping |
| Part-of-speech lock | A word's grammatical flexibility | **Cardinality** — exactly 1 part of speech per word |

The key insight is that STE treats English as a **formal language with a restricted grammar and a finite lexicon**, much like a programming language. The writing rules act as syntax constraints, the dictionary acts as a token table, and the technical-noun/technical-verb categories act as extension points — analogous to `import` statements that bring in domain-specific libraries.

---

## Section 1 — Words (Rules 1.1–1.14)

This section defines the **lexical policy**: what vocabulary is permitted and how.

**Rule 1.1** — Three permissible word classes: approved dictionary words, technical nouns (formerly "technical names"), and technical verbs.

**Rule 1.2** — One-to-one part-of-speech mapping: each approved word is locked to a single grammatical function.

**Rule 1.3** — Each word locked to a single meaning.

**Rule 1.4** — Verb/adjective inflection restricted to approved forms only.

**Rules 1.5–1.11** — Govern **technical nouns**: domain-specific terms not in the core dictionary but permitted if they fall into one of 19 categories. Rule 1.6 creates an **exception mechanism** — an unapproved word can be "redeemed" if it qualifies as a technical noun in context. Rule 1.7 prevents using technical nouns as verbs. Rules 1.8–1.11 enforce nomenclature consistency and prohibit slang/jargon.

**Rules 1.12–1.13** — Define **technical verbs** using a similar category-based permission system.

**Rule 1.14** — Mandates American English spelling.

---

## Section 2 — Noun Clusters (Rules 2.1–2.3)

Noun clusters (e.g., "engine fuel pump pressure indicator") are restricted to a **maximum of three words**; longer clusters must be broken using prepositions. This prevents the "noun-stacking" ambiguity that plagues uncontrolled technical English — analogous to limiting expression nesting depth in code.

---

## Section 3 — Verbs (Rules 3.1–3.7)

Section 3 enforces **active voice** in procedural writing (Rule 3.6), permits passive voice only in descriptive writing and only when the agent is irrelevant, mandates the **imperative form** for instructions (Rule 3.2), and restricts approved verb tenses to simple present, simple past, past participle, and future. The "-ing" form is heavily restricted (Rule 3.5) because gerunds and participles create syntactic ambiguity.

---

## Section 4 — Sentences (Rules 4.1–4.4)

- **Rule 4.1** — Procedural sentences max **20 words**, descriptive max **25 words**.
- **Rule 4.2** — No word omission (no ellipsis-based shorthand).
- **Rule 4.3** — Vertical lists with consistent formatting.
- **Rule 4.4** — Connecting words and phrases mandatory for coherence.

---

## Section 5 — Procedural Writing (Rules 5.1–5.5)

This section defines the **step-by-step instruction grammar**: one instruction per sentence, imperative voice, numbered steps, and how notes and cautions integrate into procedures. It is the most "code-like" section, as procedural STE text maps closely to imperative programming constructs.

---

## Section 6 — Descriptive Writing (Rules 6.1–6.6)

Governs explanatory/informational text: paragraph length limits, one topic per paragraph, use of key phrases as signposts, and logical flow through connecting words. This section maps to the "narrative" or "documentation comment" layer of a formal system.

---

## Section 7 — Safety Instructions (Rules 7.1–7.3)

Safety instructions (warnings and cautions) must use **simple command form followed by explanation**. This section is critical for human-factors safety in aerospace and defense — a safety instruction that is ambiguous can cost lives.

---

## Section 8 — Punctuation and Word Counts (Rules 8.1–8.7)

This section regulates punctuation marks:

- **Rule 8.1** — Semicolons are prohibited
- **Rule 8.4** — Colons restricted to introducing lists
- Dashes are limited
- Hyphens regulated for compound terms
- Word-count limits enforced per sentence type
- Abbreviations, acronyms, and initialisms governed (Rules 8.5–8.6)

---

## Section 9 — Writing Practices (Rules 9.1–9.4)

Covers **meta-practices**:

- **Rule 9.1** — No word-for-word replacement without meaning check (prevents "Bag of Parts Fallacy")
- **Rule 9.2** — Use words in approved sense only
- **Rule 9.3** — Instructions in correct order (execution order invariant)
- **Rule 9.4** — Consistent style throughout

Plus four **General Rules** (GR1–GR4) governing "that," "with," pronouns, and "this."

---

## The Nine Sections Summary Table

| Section | Topic | What It Covers |
|---------|-------|----------------|
| 1 | Words | Which words are approved, parts of speech, approved meanings, verb/adjective forms, 19 categories of technical nouns, technical verbs, American English spelling |
| 2 | Noun clusters | Keeping noun clusters short (max 3 words), using prepositions to break them up |
| 3 | Verbs | Active vs. passive voice, imperative form for instructions, approved verb tenses |
| 4 | Sentences | Sentence length limits, one topic per sentence, vertical lists |
| 5 | Procedural writing | How to write step-by-step instructions |
| 6 | Descriptive writing | Paragraph length, topic focus, descriptive structure |
| 7 | Safety instructions | Warnings, cautions, and how to format them |
| 8 | Punctuation and word counts | Semicolons, colons, dashes, hyphens, word count limits |
| 9 | Writing practices | Word-for-word replacement, correct usage, consistent style |

---

## References

- https://www.asd-ste100.org/
- https://www.asd-ste100.org/about.html
