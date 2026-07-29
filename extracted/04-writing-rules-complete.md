# ASD-STE100 — Complete Rule-by-Rule Breakdown (Sections 2–9)

> Extracted and restructured from Perplexity conversation.
> Part 3 of the 5-part deep dive.
> Every rule, its formal constraint, and its code analogy.

---

## Section 2 — Noun Clusters (Rules 2.1–2.3)

A noun cluster is a sequence of nouns where each noun modifies the next — standard English allows unlimited stacking, which creates parse ambiguity. STE constrains this tightly.

### Rule 2.1 — Maximum three words in a noun cluster

A noun cluster must not contain more than three words.

- **Example**: "engine fuel pump" (3 words) is permitted; "engine fuel pump pressure indicator" (5 words) must be rewritten as "the pressure indicator of the engine fuel pump"
- **Code analogy**: **Nesting depth limit** — like restricting expression depth to 3 levels in an AST to prevent stack overflow in parsing

### Rule 2.2 — Use prepositions to break long clusters

When a cluster exceeds three words, writers must insert a preposition (usually "of") to clarify the relationship.

- **Code analogy**: **Explicit parenthesization** — instead of relying on operator precedence (`a * b * c * d * e`), you write `a * (b * (c * (d * e)))` to make the evaluation order unambiguous

### Rule 2.3 — No noun clusters as verbs

A noun cluster must not be used as a verb. For example, you cannot write "troubleshoot the system" if "troubleshoot" is not an approved verb — you must write "Do the troubleshooting of the system" or use an approved verb like "examine".

- **Code analogy**: **Type boundary enforcement** between nouns and verbs — no implicit casting

---

## Section 3 — Verbs (Rules 3.1–3.7)

Section 3 is the heart of STE's grammar engine — it restricts English's rich verb system to a minimal, deterministic subset.

### Rule 3.1 — Use approved verb forms only

Only verbs listed in the dictionary (or approved technical verbs) are permitted. Each verb has a fixed set of approved inflected forms — typically the base form, the -s form, the -ed form, and the past participle.

- **Code analogy**: **Fixed function signature** — you cannot call a verb with an unapproved conjugation

### Rule 3.2 — Use the imperative for instructions

Procedural steps must use the imperative form: "Remove the bolt" — not "You must remove the bolt" or "The bolt should be removed".

- **Code analogy**: **Function calls in imperative programming**: `remove(bolt)`. The subject is implicit, just as the calling context is implicit in a procedure call

### Rule 3.3 — Use only approved tenses

STE permits exactly four tenses:

| STE Tense | Usage | Code Analogy |
|-----------|-------|--------------|
| Simple present | General facts, descriptions | Constant declaration / type definition |
| Simple past | Completed actions | Executed statement / logged event |
| Past participle | Passive voice (descriptive only) | Returned value / state descriptor |
| Future (will/shall) | Future actions or requirements | Forward declaration / scheduled task |

Tenses like present continuous ("is removing"), present perfect ("has removed"), and all conditional forms ("would remove," "could remove") are **prohibited**. This eliminates the need for temporal logic in parsing — the time reference is always explicit and unambiguous.

### Rule 3.4 — Keep to one verb form per sentence

A sentence must not contain more than one verb form unless connected by an approved conjunction.

- "Remove the bolt and examine the flange" is acceptable (two imperatives joined by "and")
- "Remove the bolt that holds the cover that protects the seal" is not (chained relative clauses)

- **Code analogy**: **Limiting statements per basic block** — one operation, one statement

### Rule 3.5 — Restrict the -ing form

Gerunds and present participles are heavily restricted because they create syntactic ambiguity: "Removing the bolt is necessary" could parse as a gerund (nominalized action) or a participle (adjective modifying "bolt"). STE generally requires rewriting: "It is necessary to remove the bolt".

- **Code analogy**: Eliminates **ambiguous grammar productions** — the parser never encounters a token that could be a noun or a verb depending on context

### Rule 3.6 — Active voice mandatory in procedures

Procedural writing must use active voice: "Remove the bolt" — not "The bolt must be removed". Active voice makes the agent explicit, which is critical for safety — the reader must know *who* performs the action.

- **Code analogy**: **Explicit invocation** rather than implicit dispatch

### Rule 3.7 — Passive voice restricted to descriptive writing

Passive voice is permitted only in descriptive (non-procedural) text, and only when the agent is irrelevant or unknown.

- "The bolt is made of titanium" is acceptable (descriptive, agent = manufacturer, irrelevant)
- "The bolt is removed" in a procedure is not

- **Code analogy**: **Read-only accessors** in descriptive code vs. **explicit mutation calls** in procedural code

---

## Section 4 — Sentences (Rules 4.1–4.4)

### Rule 4.1 — Sentence length limits

Procedural sentences: maximum 20 words. Descriptive sentences: maximum 25 words.

- **Code analogy**: **Buffer size limit** — prevents sentences from becoming too complex to parse in a single cognitive or computational pass

### Rule 4.2 — No word omission

Words must not be omitted for brevity. Standard English permits "Clean and inspect the flange" (omitting the second "the"), but STE requires "Clean the flange and inspect the flange".

- **Code analogy**: **No-elision rule** — every token must be explicit, like requiring fully qualified names in code rather than relying on scope resolution

### Rule 4.3 — Vertical lists

Vertical (bulleted or numbered) lists must be formatted consistently, with each item being a complete sentence or a parallel fragment. The list must be introduced by a lead-in sentence ending with a colon.

- **Code analogy**: **Array initialization syntax** — each element follows the same type signature

### Rule 4.4 — Connecting words and phrases

Sentences must use approved connecting words (and, or, but, if, because, although, etc.) to show logical relationships. Lists of disconnected sentences are prohibited — the logical flow must be explicit.

- **Code analogy**: **Control-flow annotation** requirement — every transition between statements must be marked

---

## Section 5 — Procedural Writing (Rules 5.1–5.5)

Section 5 defines the **instruction grammar** — the closest STE gets to executable code.

### Rule 5.1 — One instruction per sentence

Each procedural sentence must contain exactly one instruction. "Remove the bolt and examine the flange" is technically two instructions and must be split into two numbered steps.

- **Code analogy**: **Single-responsibility principle** applied to text — one sentence, one action

### Rule 5.2 — Numbered steps

Procedural steps must be numbered sequentially.

- **Code analogy**: **Ordered execution sequence** — like line numbers in BASIC or sequential statements in a function body

### Rule 5.3 — Notes and cautions placement

Notes and cautions must appear **before** the step they relate to, not after.

- **Code analogy**: **Precondition assertion** pattern — you state the warning before the operation, like a `require` or `assert` statement at the top of a function

### Rule 5.4 — Conditional instructions

Conditional steps must use "If" at the beginning and clearly identify the condition and the resulting action. "If the temperature is more than 80 degrees Celsius, do the applicable steps in paragraph 3."

- **Code analogy**: **if-then block**:
```
if temperature > 80°C:
    execute(paragraph_3_steps)
```

### Rule 5.5 — Referencing other procedures

Cross-references to other procedures must use standardized language: "Do the steps given in [reference]".

- **Code analogy**: **Function call** pattern — `execute_procedure(reference)` — with a standardized calling convention

---

## Section 6 — Descriptive Writing (Rules 6.1–6.6)

### Rule 6.1 — Paragraph length

Descriptive paragraphs must not exceed 6 sentences.

- **Code analogy**: **Module size limit** — preventing a descriptive block from becoming too large to comprehend in one pass

### Rule 6.2 — One topic per paragraph

Each paragraph must address exactly one topic.

- **Code analogy**: **Single-responsibility principle** for descriptive text — analogous to one class per file or one function per purpose

### Rule 6.3 — Key phrases as signposts

Descriptive text must use key phrases (e.g., "General," "Description," "Function," "Location") to identify paragraph topics.

- **Code analogy**: **Section header / docstring** convention — each block is labeled with its semantic purpose

### Rule 6.4 — Logical flow with connecting words

Paragraphs must flow logically using approved connecting words.

- **Code analogy**: Like Rule 4.4, requires **explicit control-flow annotation**

### Rule 6.5 — Simple sentence structure

Descriptive sentences must use simple, direct structure — no embedded clauses beyond one level.

- **Code analogy**: Limits **AST depth** to prevent parser complexity

### Rule 6.6 — No procedural language in descriptive text

Descriptive sections must not contain imperative instructions.

- **Code analogy**: **Separation of concerns** — descriptions are read-only (declarative), procedures are executable (imperative)

---

## Section 7 — Safety Instructions (Rules 7.1–7.3)

### Rule 7.1 — Warnings and cautions format

Safety instructions must use a two-part structure: (1) a simple command identifying the hazard, then (2) an explanation of the consequence. "WARNING: DO NOT GET NEAR THE LEAK. THE FUEL IS FLAMMABLE."

- **Code analogy**: **Typed exception with a message**:
```
throw SafetyWarning(
    command="DO NOT GET NEAR THE LEAK",
    reason="THE FUEL IS FLAMMABLE"
)
```

### Rule 7.2 — Placement before the related step

Warnings and cautions must appear **before** the procedural step they protect — never after.

- **Code analogy**: **Precondition guard** — the safety check runs before the operation, like a `@precondition` annotation

### Rule 7.3 — Use approved safety vocabulary

Safety instructions must use approved words and must not be diluted with vague language. "Be careful" is unapproved; "WARNING: DO NOT TOUCH THE HOT SURFACE" is approved.

- **Code analogy**: **Typed safety vocabulary** — only specific, unambiguous tokens are permitted in safety-critical contexts

---

## Section 8 — Punctuation and Word Counts (Rules 8.1–8.7)

### Rule 8.1 — No semicolons

Semicolons are **prohibited** because they create compound sentences that are hard to parse.

- **Code analogy**: Prohibiting the comma operator in C — it forces each statement to stand alone

### Rule 8.2 — Word count per sentence

Enforces the limits from Rule 4.1 (20 words procedural, 25 descriptive).

- **Code analogy**: **Redundant check** — like a runtime assertion that validates the compile-time constraint

### Rule 8.3 — Period as the sentence terminator

Only the period may end a sentence — not exclamation marks or question marks in technical text.

- **Code analogy**: Standardized **statement terminator** to a single token

### Rule 8.4 — Colons only for lists

Colons are restricted to introducing vertical lists. They cannot join two independent clauses.

- **Code analogy**: **Type-specific operator** restriction — the colon token has one and only one valid production rule

### Rule 8.5 — Hyphens for compound words

Hyphens are permitted only in approved compound terms and must follow dictionary specifications. "left-hand" is approved; "left hand" (without hyphen) is not when used as a compound modifier.

- **Code analogy**: **Compound token rule** — certain multi-word tokens are treated as single lexical units

### Rule 8.6 — Abbreviations and acronyms

Abbreviations must be defined on first use, using the format: full term (abbreviation). "Federal Aviation Administration (FAA)" on first use, then "FAA" thereafter.

- **Code analogy**: **Variable declaration** pattern — `const FAA = "Federal Aviation Administration"` — define once, reference by symbol thereafter

### Rule 8.7 — No unnecessary punctuation

Parentheses, brackets, and quotation marks are restricted to specific approved uses. Parentheses are allowed only for abbreviations (Rule 8.6) and for optional information in descriptive text.

- **Code analogy**: Prevents **side-channel information embedding** — every piece of information must appear in the main syntactic flow

---

## Section 9 — Writing Practices (Rules 9.1–9.4 + General Rules GR1–GR4)

### Rule 9.1 — No word-for-word replacement without meaning check

You cannot simply swap an unapproved word for its approved alternative if the substitution changes the meaning. For example, "assemble" (unapproved) maps to "PUT TOGETHER" (approved), but "assemble a team" cannot become "put together a team" in a technical context — the meaning has shifted.

- **Code analogy**: **Semantic type checking** — a syntactically valid substitution may fail semantic validation
- This is the most important rule for preventing the **"Bag of Parts Fallacy"** — the idea that a dictionary alone makes text compliant

### Rule 9.2 — Use words correctly

Approved words must be used in their approved sense only. "Follow" means "to come after," not "to obey" — so "Follow the procedure" is wrong; "Do the procedure" is right.

- **Code analogy**: **Type safety enforcement** — a word has one and only one semantic type

### Rule 9.3 — Keep instructions in the correct order

Procedural steps must appear in the order they are to be performed.

- **Code analogy**: **Execution order invariant** — the text order must match the execution order, like requiring sequential statement ordering in a function body

### Rule 9.4 — Consistent style

The same word, format, and structure must be used consistently throughout a document.

- **Code analogy**: **Style guide / linter rule** — like enforcing consistent naming conventions across a codebase

---

## General Rules (GR1–GR4)

These are cross-cutting constraints that apply throughout the specification:

### GR1 — "That" usage

"That" is restricted to its demonstrative pronoun function ("that procedure") and as a relative pronoun in restrictive clauses. It must not be used as a conjunction meaning "so that" — "Adjust the valve that the pressure is correct" is wrong; "Adjust the valve to make sure that the pressure is correct" is right.

- **Code analogy**: **Overloaded token resolution** — "that" has a restricted type signature

### GR2 — "With" usage

"With" is restricted to meaning "together with" or "having". It must not mean "by means of" or "using" — "Tighten the bolt with a wrench" is wrong; "Use a wrench to tighten the bolt" is right.

- **Code analogy**: **Type restriction** on a polysemous word

### GR3 — Pronoun usage

Pronouns must refer clearly to their antecedent, and the antecedent must be unambiguous. "Remove the bolt and the nut. Discard it." — "it" is ambiguous (bolt or nut?).

- **Code analogy**: **Dangling reference** rule — like a linter flagging an ambiguous variable reference in code

### GR4 — "This" usage

"This" must always be followed by a noun — "this procedure," not "this" alone.

- **Code analogy**: Prevents the **ambiguous pointer** problem — "this" without a noun is like a void pointer with no type information

---

## Impact on Code: The Full Mapping Summary

Across all 53 rules, STE enforces constraints that map to well-known software engineering principles:

| STE Rule(s) | Code Principle | Effect |
|-------------|----------------|--------|
| 1.2, 1.3 | Type safety (one POS, one meaning) | Eliminates polymorphic ambiguity |
| 2.1–2.3 | Nesting depth limit | Prevents parser stack overflow |
| 3.1–3.5 | Fixed function signatures | Deterministic lexical resolution |
| 3.6–3.7 | Explicit invocation vs. accessor | Separates commands from queries (CQRS) |
| 4.1–4.2 | Buffer size + no elision | Bounded parse complexity |
| 5.1–5.5 | Single-responsibility + ordered execution | Procedural code mapping |
| 6.1–6.6 | Module size + separation of concerns | Declarative vs. imperative separation |
| 7.1–7.3 | Precondition guards + typed exceptions | Safety-critical runtime checks |
| 8.1–8.7 | Token restrictions + statement terminators | Deterministic tokenization |
| 9.1–9.4 | Semantic type checking + linter rules | Compile-time + runtime validation |
| GR1–GR4 | Overload resolution + dangling reference checks | Static analysis |

---

## References

- https://www.asd-ste100.org/
- https://www.youtube.com/watch?v=ffF-V7xQL68
