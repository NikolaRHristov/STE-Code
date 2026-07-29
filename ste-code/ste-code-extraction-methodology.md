# STE-Code Extraction Methodology
# Turn-by-turn protocol for processing code documents

## Document Classification

Identify the document type before processing:
- **PROCEDURAL:** commit messages, setup guides, runbooks, code review instructions → 20-word max (Rule 5.1)
- **DESCRIPTIVE:** README files, API documentation, architecture descriptions → 25-word max (Rule 6.3)
- **SAFETY:** changelogs, migration guides, deprecation notices → 20-word max (Rule 5.1)
- **MIXED:** documents containing multiple types

## 6-Pass Transformation Pipeline

### Pass 1 — Lexical Lookup
Tokenize the input on whitespace and punctuation boundaries. For each word:
- **APPROVED:** word is in the STE-Code dictionary as approved.
- **UNAPPROVED:** word is in the dictionary as not approved.
- **TECHNICAL_NOUN:** word fits a Technical Code Noun category (Rule 1.5, 19 categories).
- **TECHNICAL_VERB:** word fits a Technical Code Verb category (Rule 1.12, 4 categories).
- **UNKNOWN:** word needs classification.

### Pass 2 — Classification
For each UNKNOWN word:
1. Can it fit in a Technical Code Noun category? → Mark TECHNICAL_NOUN.
2. Can it fit in a Technical Code Verb category? → Mark TECHNICAL_VERB.
3. Is it a function name, class name, or module name? → Mark TECHNICAL_NOUN (category 6).
4. Otherwise: mark for replacement.

### Pass 3 — Part-of-Speech Lock
- Each APPROVED word must match its dictionary POS.
- Each TECHNICAL_NOUN must be used as a noun (Rule 1.7).
- Each TECHNICAL_VERB must be used as a verb (Rule 1.13).

### Pass 4 — Meaning Validation
- Verify each approved word's context matches its approved meaning.
- Check the polysemy resolution table for ambiguous words.
- Replace words with incorrect meanings.

### Pass 5 — Grammar Enforcement
- Verify verb forms: only approved tenses (infinitive, imperative, simple present/past/future, past participle as adjective — Rules 3.1-3.2).
- Verify voice: active required unless agent unknown (Rule 3.6).
- Enforce sentence length limits based on document type.
- Verify compound identifiers ≤ 3 components (Rule 2.1).

### Pass 6 — Consistency Check
- Scan for inconsistent Technical Code Noun usage (Rule 1.11).
- Scan for undefined abbreviations.
- Scan for jargon/slang (Rule 1.10).
- Scan for phrasal verbs (Rule 9.3).
- Scan for Latin abbreviations (GR-6).
- Verify inclusive language (GR-7).

## Output Format

```
## DOCUMENT TYPE: [PROCEDURAL / DESCRIPTIVE / SAFETY / MIXED]

## COMPLIANCE STATUS: [COMPLIANT / NON-COMPLIANT]

## TRANSFORMATION LOG:
- Pass 1 (Lexical): [X words: Y APPROVED, Z UNAPPROVED, ...]
- Pass 2 (Classification): [X words reclassified]
- Pass 3 (POS Lock): [X violations corrected]
- Pass 4 (Meaning): [X polysemy resolutions applied]
- Pass 5 (Grammar): [X violations corrected]
- Pass 6 (Consistency): [X issues resolved]

## STE-CODE OUTPUT:
[The compliant text]

## OPTIMIZATIONS:
- [Optional improvements beyond minimum compliance]
```

## Edge Cases

**Quoted text:** Code literals, error messages, and display text. Do not transform.
Count as one word (Rule 8.6).

**Code blocks:** Treat as quoted text. Do not transform.

**Mixed language:** Flag non-English text. STE-Code applies only to English.

**Ambiguous classification:** Prefer Technical Code Noun (more restrictive).
