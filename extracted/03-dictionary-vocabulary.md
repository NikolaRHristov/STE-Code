# ASD-STE100 — The Dictionary: Vocabulary, Categories, and Lexical Architecture

> Extracted and restructured from Perplexity conversation.
> Part 2 of the 5-part deep dive.

---

## How the Dictionary Is Organized

Part 2 of the specification is the **controlled lexicon** — a finite, enumerated word list that functions like the reserved-keyword table in a programming language. The dictionary has three tiers of vocabulary:

1. **Approved words** (written in UPPERCASE): ~875 core words that writers may use freely, each locked to exactly one part of speech and one approved meaning.
2. **Unapproved words** (written in lowercase): ~1,400 words that standard English permits but STE does not — each comes with a suggested approved alternative.
3. **Technical names and technical verbs**: domain-specific terms not in the core dictionary but permitted if they fall into one of the 19 technical-name categories or the approved technical-verb categories.

### Dictionary Entry Structure

Each dictionary entry is structured as a **lexical record** — mirroring a type definition in code:

| Field | Description | Example |
|-------|-------------|---------|
| Word | The term itself (uppercase = approved) | REMOVE |
| Part of speech | Exactly one grammatical function | (v) — verb |
| Approved meaning | A single, restricted definition | "to take away from a location" |
| Approved forms | Inflectional variants | REMOVES, REMOVED, REMOVED |
| Suggested alternatives | For unapproved words only | "discard" → REMOVE (v) |

The part-of-speech lock acts as a type constraint — each word is like a typed constant with a fixed signature.

---

## The 19 Technical Name Categories (Full Enumeration)

Technical names are the **extension mechanism** of the STE vocabulary — analogous to `import` statements that bring domain libraries into scope. A word qualifies as a technical name if and only if it can be placed in one of these 19 categories:

| # | Category | Representative Examples |
|---|----------|------------------------|
| 1 | Names in official parts information | bolt, cable, clip, conductor, engine, filter, hatch, indicator, light, pipe, screw, switch |
| 2 | Names of vehicles/machines and locations on them | aircraft, cabin, car, cockpit, fuselage, helicopter, ship, submarine, tank, truck, wing |
| 3 | Names of tools and support equipment | access ladder, blade, brush, clamp, cover, gauge, handle, jack, torque wrench |
| 4 | Names of materials, consumables, and unwanted material | acid, adhesive, copper, debris, detergent, fuel, grease, oil, paint, primer, sealant, tape, water |
| 5 | Names of facilities, infrastructure, and locations | airport, apron, base, building, dock, gate, hangar, port, shop |
| 6 | Names of systems, components, circuits, and functions | air conditioning, audio, exhaust, flight management, hardware, injection, inlet, pump, vent |
| 7 | Mathematical, scientific, and engineering terms | acceleration, capacitance, coefficient, density, diameter, force, gravity, pressure, torque, voltage |
| 8 | Navigation and geographic terms | altitude, axis, bank, heading, landing, north, pitch, roll, south, west |
| 9 | Numbers, units of measurement, and time | Ampere, degree, hour, kilogram, knot, meter, mile, minute, ohm, second, year |
| 10 | Quoted text (placards, labels, signs, markings) | EXIT sign, ON position, FAULT legend, NO STEP marking |
| 11 | Names of persons, groups, or organizations | air traffic control, captain, crew, EASA, FAA, manufacturer, operator |
| 12 | Parts of the body | blood, ear, eyes, hand, head, lung, mouth, skin |
| 13 | Common personal effects | clothing, food, footwear, jewelry, matches, perfume |
| 14 | Medical terms | allergy, asthma, blood poisoning, dermatitis, diabetes, dizziness, headache, nausea |
| 15 | Names of official documents and documentation parts | checklist, data module, engine logbook, figure, flow chart, paragraph, Service Bulletin |
| 16 | Environmental and operational conditions | atmosphere, cloud, day, ice, humidity, lightning, moisture, night, rain, snow, storm, wind |
| 17 | Colors | beige, cyan blue, dark brown, magenta, orange, red, white, yellow |
| 18 | Damage terms | buckle, chafing, corrosion, crack, deformation, dent, distortion, erosion, fracture, scratch |
| 19 | Information technology and telephony terms | backup, cursor, database, e-mail, file, firewall, HTML, icon, interface, network, XML |

### Context-Dependent Classification

The same word can fall into **different categories depending on context**. For example, "base" is unapproved as a general word for "a surface," but approved as a technical name in category 7 (mathematical term — "the base of the triangle") or category 5 (a facility — "access to the base"). This context-dependent classification is analogous to **overloaded type resolution** in programming languages.

---

## Technical Verbs — The Verb Extension Categories

Technical verbs follow a similar permission system. Rule 1.12 permits verbs that fall into specified categories — primarily **manufacturing processes, computer processes, and operational verbs**. Examples include:

- "ream" — a machining process
- "download" — an IT process
- "taxi" — an aircraft operation

Rule 1.13 prohibits using technical verbs as nouns — the same part-of-speech lock that applies to dictionary words.

---

## Keyword Coverage: What the Core Dictionary Contains

The ~875 approved words cover the **functional vocabulary** needed for technical writing:

| Part of Speech | Approximate Count | Role | Examples |
|----------------|-------------------|------|----------|
| Verbs (v) | ~300 | Actions | REMOVE, INSTALL, TEST, ADJUST, CONNECT, DISCONNECT |
| Nouns (n) | ~250 | Objects/concepts | TOOL, SYSTEM, PRESSURE, TEMPERATURE, PROCEDURE |
| Adjectives (adj) | ~150 | Descriptors | APPROVED, CORRECT, DIM, SLOW, DRY, FLAT |
| Adverbs (adv) | ~60 | Modifiers | ACCURATELY, SLOWLY, AGAIN, BEFORE, BELOW |
| Prepositions (prep) | ~40 | Relations | ABOVE, BELOW, BETWEEN, THROUGH, WITH |
| Conjunctions (conj) | ~15 | Connectors | AND, OR, IF, BECAUSE, ALTHOUGH, AS |
| Pronouns (pron) | ~10 | References | THIS, THAT, IT, WE, SAME |
| Articles | 3 | | A, AN, THE |

A key design principle is **synonym elimination**: where standard English offers multiple words for the same concept, STE selects exactly one. For instance, STE uses "start" instead of "begin," "commence," "initiate," or "originate". It uses "make sure" instead of "ensure," "ascertain," or "verify". This one-to-one mapping is what makes STE text highly machine-translatable — the translation engine faces minimal ambiguity.

---

## Relationships to Normal Language: A Formal Mapping

The relationship between STE and standard English can be modeled as a **language subset with constrained grammar**:

| Dimension | Standard English | STE Constraint | Formal-Language Analogy |
|-----------|-----------------|----------------|------------------------|
| Vocabulary size | ~170,000 words | ~875 approved + technical names | Restricted token set |
| Synonyms | Multiple per concept | Exactly one per concept | Canonical form enforced |
| Polysemy | Multiple meanings per word | Exactly one meaning per word | Single-valued function |
| Parts of speech | Flexible (word can be n, v, adj) | Locked to one per word | Type safety |
| Sentence length | Unlimited | ≤20 words (procedural), ≤25 (descriptive) | Expression depth limit |
| Verb tenses | 12+ tenses | 4: simple present, simple past, past participle, future | Reduced grammar productions |
| Voice | Active and passive freely | Active mandatory (procedural); passive restricted (descriptive) | Mode restriction |
| Noun clusters | Unlimited stacking | Maximum 3 words | Nesting depth limit |
| Semicolons | Common | Prohibited | Token exclusion |
| "-ing" forms | Common (gerunds, participles) | Heavily restricted | Production rule removal |

The overall effect is that STE defines a **proper subset of English** — every STE sentence is valid English, but most English sentences are not valid STE. This is analogous to how a strictly-typed programming language is a subset of a dynamically-typed one: more restrictive, but safer and more predictable.

---

## Impact on Code: From Controlled Language to Computable Text

### Deterministic Parsing

Because STE locks each word to one part of speech and one meaning, a parser can resolve lexical ambiguity without statistical methods. "Test" is always a noun, never a verb — so "Do the test" parses unambiguously. This contrasts with standard English where "test the system" requires POS-tagging.

### Reduced Translation Table Size

The one-to-one synonym mapping means a translation memory system needs far fewer entries. If "start" is the only word for "begin," the translation engine maps one source token to one target token — no disambiguation needed. Organizations report ~25% reduction in text volume, directly reducing translation costs.

### Structured Procedural Mapping

STE procedural writing (Section 5) maps closely to **imperative code constructs**: numbered steps become sequential statements, conditional instructions become `if-then` blocks, and the imperative verb form maps to function calls. "Remove the bolt from the flange" → `remove(bolt, flange)`.

### Safety-Critical Reliability

In aerospace and defense, ambiguous documentation can cause catastrophic failure. STE's single-meaning constraint eliminates the "replace" problem — where "replace" could mean "substitute" or "put back" — by locking each word to one definition. This is the linguistic equivalent of **defensive programming**: eliminating undefined behavior at the language level.

### AI Data Quality

STE provides the "clean data in" foundation for AI and information science — controlled vocabulary and grammar produce training data with minimal noise, improving NLP model accuracy downstream.

---

## References

- https://www.asd-ste100.org/
- https://www.youtube.com/watch?v=ffF-V7xQL68
- https://qabiria.com/en/resources/blog/controlled-language
