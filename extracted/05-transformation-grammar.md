# ASD-STE100 — The Transformation Grammar: Converting Standard English to STE

> Extracted and restructured from Perplexity conversation.
> Part 4 of the 5-part deep dive.
> Polysemy resolution, synonym elimination, transformation pipeline, and impact on MT/NLP/Code.

---

## The Core Transformation Pipeline

Converting standard English into STE is not a word-for-word substitution — it is a **multi-pass transformation pipeline** that operates at the lexical, syntactic, and semantic levels. The specification itself includes a decision flowchart (added in Issue 8) that walks writers through the process of determining whether a word is approved, unapproved with an alternative, or qualifies as a technical name.

### Pass 1 — Lexical lookup

Each word in the source text is checked against the STE dictionary.

- If the word is an approved word (uppercase entry), it passes.
- If it is an unapproved word (lowercase entry), the dictionary provides an approved alternative.
- If the word is not in the dictionary at all, proceed to Pass 2.

### Pass 2 — Technical name/verb classification

If a word is not in the dictionary, check whether it qualifies as a technical name (one of 19 categories) or a technical verb (manufacturing, IT, or operational process). If yes, the word is permitted. If no, the writer must find an approved alternative or rephrase.

### Pass 3 — Part-of-speech lock check

Even if a word is approved, verify it is used in its approved part of speech. "Test" is an approved noun but not an approved verb — "Test the system" fails this check and must be rewritten as "Do a test of the system".

### Pass 4 — Meaning validation (Rule 9.1)

Even if the word passes lexical and POS checks, verify that the approved meaning matches the intended sense. "Follow the procedure" uses "follow" in the sense of "obey," which is not its approved meaning ("come after") — so it must be rewritten as "Do the procedure". This is the semantic type-checking pass that prevents the "Bag of Parts Fallacy".

### Pass 5 — Grammar rule application

Apply all 53 writing rules: rewrite passive voice to active (Rule 3.6), break noun clusters over 3 words (Rule 2.1), split compound sentences (Rule 4.1), remove semicolons (Rule 8.1), enforce imperative form (Rule 3.2), and so on.

### Pass 6 — Consistency check (Rule 9.4)

Verify that the same term is used consistently throughout the document — no synonym variation.

---

## Polysemy Resolution: One Word, One Meaning

In standard English, polysemy — a single word carrying multiple meanings — is pervasive and is the primary source of ambiguity in technical text. STE resolves this by **locking each approved word to exactly one meaning**.

| Word | Standard English Meanings | STE Approved Meaning | Rejected Meanings (Must Use Instead) |
|------|--------------------------|---------------------|--------------------------------------|
| FOLLOW | (1) come after, (2) obey, (3) track | Come after | Obey → OBEY; track → TRACK |
| TEST | (1) noun: examination, (2) verb: to examine | Noun only | Verb sense → DO A TEST |
| REPLACE | (1) put back, (2) substitute | Put back | Substitute → use a different word |
| BASE | (1) foundation, (2) bottom surface, (3) math term, (4) facility | Unapproved as general word | Foundation → BOTTOM; math/facility → technical name |
| SET | (1) to adjust, (2) a group, (3) to harden, (4) to put | To put (verb) | Adjust → ADJUST; group → GROUP; harden → CURE |
| RIGHT | (1) correct, (2) direction, (3) entitlement | Correct (adjective) | Direction → STARBOARD; entitlement → APPROVED TECHNICAL NAME |
| LIGHT | (1) not heavy, (2) illumination, (3) to ignite | Not heavy (adjective) | Illumination → APPROVED TECHNICAL NAME; ignite → not approved |
| FAIR | (1) just, (2) weather condition, (3) exhibition | Unapproved | Just → CORRECT; weather → weather technical name |
| MATCH | (1) to pair, (2) a contest, (3) a small fire-starter | To pair (verb) | Contest/igniter → technical names |
| SOUND | (1) noise, (2) healthy, (3) to measure depth | Unapproved as adjective | Noise → APPROVED NOUN; healthy → CORRECT; measure → MEASURE |

This resolution has a profound effect on **automated processing**: a parser or NLP system processing STE text never needs word-sense disambiguation (WSD) because each word has exactly one sense. In standard English, WSD is one of the hardest problems in NLP — STE eliminates it entirely at the source.

---

## Synonym Elimination: Canonical Forms

Standard English offers multiple words for the same concept, which creates inconsistency in technical documentation and reduces translation memory match rates. STE selects exactly one **canonical form** per concept.

| Concept | Standard English Synonyms | STE Canonical Form |
|---------|--------------------------|-------------------|
| Begin an action | start, begin, commence, initiate, originate | START |
| End an action | stop, end, finish, terminate, conclude, halt | STOP |
| Remove from location | remove, take out, extract, withdraw, detach | REMOVE |
| Make certain | ensure, verify, ascertain, confirm, make sure | MAKE SURE |
| Display/show | show, display, indicate, reveal, present | SHOW |
| Examine | examine, inspect, check, review, look at | EXAMINE |
| Connect | connect, attach, join, link, couple | CONNECT |
| Close | close, shut, seal, secure | CLOSE |
| Open | open, unseal, unfasten, release | OPEN |
| Put in place | install, fit, mount, place, position | INSTALL |
| Observe | observe, monitor, watch, view | MONITOR (approved); observe → not approved |
| Fasten | tighten, fasten, secure, lock | TIGHTEN |
| Discard | discard, dispose of, throw away, jettison | DISCARD |
| Stop/cease | stop, cease, discontinue, suspend | STOP |
| Correct/accurate | correct, accurate, right, exact, precise | CORRECT |

The translation impact is direct: because there is exactly one source word per concept, a translation memory system stores one translation per source token. In uncontrolled English, the same instruction might be written five different ways across a manual, generating five different translation memory entries — or worse, five different translations. STE collapses these to one.

---

## Transformation Examples: Non-STE → STE

### Example 1 — Polysemy + passive voice + compound sentence

**Non-STE**: "The bolts should be replaced and the flange needs to be examined prior to reassembly."

- **Pass 1 (lexical)**: "replaced" → REMOVE (but "replace" means "put back," not "substitute" — meaning check fails in Pass 4)
- **Pass 4 (meaning)**: Intended meaning is "substitute/remove old" — use REMOVE
- **Pass 5 (grammar)**: Passive → active (Rule 3.6); compound sentence → split (Rule 4.1)

**STE**: "Remove the bolts. Examine the flange. Then, install the new bolts."

### Example 2 — Noun cluster + gerund + word omission

**Non-STE**: "Removing the engine fuel pump pressure indicator is necessary before commencing the repair procedure."

- **Pass 1 (lexical)**: "commencing" → START
- **Pass 5 (grammar)**: Gerund "removing" → rewrite (Rule 3.5); noun cluster "engine fuel pump pressure indicator" (5 words) → break with preposition (Rule 2.1)

**STE**: "It is necessary to remove the pressure indicator of the engine fuel pump before you start the repair procedure."

### Example 3 — Semicolon + -ing form + vague safety language

**Non-STE**: "Be careful when working near the exhaust; temperatures can be extremely high."

- **Pass 1 (lexical)**: "be careful" → not approved; "working" → not approved as gerund
- **Pass 5 (grammar)**: Semicolon prohibited (Rule 8.1); -ing form restricted (Rule 3.5); vague safety language → specific warning (Rule 7.1)

**STE**: "WARNING: DO NOT TOUCH THE EXHAUST. THE TEMPERATURE IS HIGH."

---

## Impact on Machine Translation

Controlled languages like STE were designed with machine translation (MT) in mind. The effects are measurable:

**Higher translation memory (TM) match rates.** Because STE eliminates synonyms, the same concept is always written the same way. This means TM systems achieve near-100% fuzzy match rates for repeated instructions, versus 30–60% in uncontrolled English.

**Reduced post-editing effort.** STE's unambiguous grammar means MT engines produce fewer errors. Texts written in controlled language require significantly less post-editing than uncontrolled text, because the source has fewer ambiguities for the MT engine to resolve.

**Smaller translation table.** With ~875 approved words plus domain-specific technical names, the total translatable vocabulary is bounded. A standard English technical manual might use 5,000–10,000 distinct words; STE uses ~875 + a controlled set of technical terms. This reduces the translation lexicon by 80–90%.

**Support for S1000D.** STE is a requirement of the S1000D specification, which uses XML-based data modules for technical documentation. STE-compliant text fits naturally into S1000D's structured XML containers because its grammar is predictable and parseable.

---

## Impact on NLP Pipelines

For natural language processing, STE text is dramatically easier to process than standard English:

| NLP Task | Standard English Challenge | STE Advantage |
|----------|---------------------------|---------------|
| Tokenization | Contractions, abbreviations, compound words | Standardized — no contractions, defined abbreviations (Rule 8.6) |
| POS tagging | Ambiguous (word can be n/v/adj) | Deterministic — one POS per word (Rule 1.2) |
| Word-sense disambiguation | Multiple meanings per word | Eliminated — one meaning per word (Rule 1.3) |
| Parsing | Complex clause structures, embedded clauses | Bounded — sentence length limits, one verb per sentence (Rules 4.1, 3.4) |
| Coreference resolution | Ambiguous pronoun references | Restricted — pronouns must have clear antecedents (GR3) |
| Named entity recognition | Mixed entity types | Categorized — 19 technical-name categories provide entity classes |
| Dependency parsing | Long-range dependencies, passive constructions | Simplified — active voice, short sentences, explicit connectors |

---

## Impact on Code Generation

The structural parallels between STE procedural writing and imperative code make STE a strong candidate for **automated code generation from technical documentation**.

### Procedural STE → imperative code

**STE**: "1. Remove the bolt (2) from the flange. 2. Examine the flange for damage. 3. If the flange is damaged, replace the flange."

Maps to:
```
remove(bolt_2, flange)
damage = examine(flange, check_type="damage")
if damage:
    remove(flange)
    install(new_flange)
```

### Conditional STE → branching logic

**STE**: "If the temperature is more than 80 degrees Celsius, do the steps in paragraph 3."

Maps to:
```
if temperature > 80:
    execute_procedure(paragraph_3)
```

### Safety instructions → assertions/exceptions

**STE**: "WARNING: DO NOT GET NEAR THE LEAK. THE FUEL IS FLAMMABLE."

Maps to:
```
@precondition(not near(leak), reason="fuel is flammable")
```

### Descriptive STE → data models

**STE**: "Function: The pressure indicator shows the pressure of the fuel in the tank."

Maps to:
```
class PressureIndicator:
    """Function: shows the pressure of the fuel in the tank."""
    fuel_tank: FuelTank
    
    def show_pressure(self) -> Pressure:
        return self.fuel_tank.pressure
```

### Cross-references → function calls

Rule 5.5's "Do the steps given in [reference]" maps to procedure invocation, making STE documentation a **call graph** where procedures reference other procedures by standardized identifiers.

---

## The Clean Data Principle

The overarching impact of STE on automated processing can be summarized as the **"clean data in" principle**. Every downstream system — whether MT, NLP, AI training, or code generation — depends on the quality of its input data. STE's controlled vocabulary, restricted grammar, and single-meaning constraint produce input data with minimal noise, maximal consistency, and zero lexical ambiguity. This is why STE is increasingly seen not just as a writing standard but as a **data quality foundation** for information science and AI initiatives.

---

## References

- https://www.asd-ste100.org/
- https://www.youtube.com/watch?v=ffF-V7xQL68
- https://qabiria.com/en/resources/blog/controlled-language
- https://www.researchgate.net/publication/300657298_Polysemy_and_synonymy
- https://www.sciencedirect.com/science/article/pii/S2589004224021035
