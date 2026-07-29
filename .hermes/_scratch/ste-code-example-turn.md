# STE-Code Worked Example
# Single-turn extraction: transforming a non-STE code comment

## INPUT (Non-STE-Code)

```
// This function does the validation of the incoming request body and
// if it's all good, it'll hit the payment gateway and then update the
// order status in the DB. Should work for most cases but might break
// if the token's expired or something like that.
```

## TRANSFORMATION LOG

### Pass 1 — Lexical Lookup
Tokenized 52 words. Classification:
- APPROVED: the, of, and, if, it, all, then, in, for, but, or, like, that (13)
- UNAPPROVED: does, stuff, validation, hit, update, should, work, most, cases, might, break, something (12)
- TECHNICAL_NOUN: request body, payment gateway, order status, DB, token (5)
- TECHNICAL_VERB: (none)
- UNKNOWN: this, function, incoming, it'll, status, expired, what (7)

### Pass 2 — Classification
- "function" → TECHNICAL_NOUN (category 6)
- "incoming" → modifier for "request body"
- "it'll" → contraction → split into "it" + "will" (APPROVED)
- "status" → TECHNICAL_NOUN (category 6)
- "expired" → TECHNICAL_NOUN (category 14: Error states — past participle as adjective)
- "what" → remove (filler word)

### Pass 3 — POS Lock
- "validation" used as noun where verb is preferred → "validate" (Rule 3.7)
- "update" is a verb → OK
- "break" → UNAPPROVED, needs replacement

### Pass 4 — Meaning Validation
- "does" → replace with appropriate verb
- "hit" → replace with "call" (canonical synonym table)
- "should" → remove (descriptive, not normative)
- "might break" → "can fail" or "can return an error"

### Pass 5 — Grammar Enforcement
- Sentence exceeds 25-word descriptive limit → split into multiple sentences
- "it'll" → "it will" (no contractions, Rule 4.2)
- "token's" → "the token is" (no contractions, avoid possessive for inanimate, GR-8)

### Pass 6 — Consistency Check
- "DB" → undefined abbreviation → "database (DB)" on first use

## STE-CODE OUTPUT

```
// This function validates the incoming request body.
// If the validation succeeds, the function calls the payment gateway.
// Then the function updates the order status in the database.
// The function returns an error if the token is expired.
```

## COMPLIANCE STATUS: COMPLIANT

Word counts: 8 + 9 + 9 + 10 = all under 25 words ✓
Active voice ✓ (except "the token is expired" — passive justified, agent unknown ✓)
No phrasal verbs ✓
No contractions ✓
Articles before nouns ✓
