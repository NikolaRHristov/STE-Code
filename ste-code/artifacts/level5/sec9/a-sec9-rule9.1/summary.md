# Rule 9.1 — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 9.1

---

## 1. Rule Title and Number

**Rule 9.1** — Use a Different Sentence Construction to Write a Sentence When a Word-for-Word Replacement Is Not Sufficient

---

## 2. Original Rule Summary

Rule 9.1 is the fallback rule for the entire STE-Code system. It applies when a word-for-word replacement using the dictionary fails — because the approved alternative has a different part of speech, because the replacement would change the meaning, because the replacement gives a meaningless result, or because the word is not in the dictionary at all. When any of these conditions is true, you must write a completely new sentence that uses only approved words while preserving the same technical meaning. This frequently requires you to change the grammatical structure, select different verbs, split long sentences, remove unnecessary information, or consult a developer for more context.

---

## 3. STE-Code Adaptation for Code Documentation

In code documentation, Rule 9.1 is the most powerful and most frequently used rule in the system. It applies when you cannot do a one-to-one word swap because the dictionary alternative has the wrong part of speech (for example, replacing an adjective with a verb requires a new sentence structure), because the replacement would alter the technical meaning (for example, "just" → "immediately" changes a limiting instruction into a timing instruction), or because a chain of unapproved words makes individual replacements impossible (for example, "leverages a virtual DOM diffing algorithm to minimize expensive DOM manipulations" cannot be fixed one word at a time). When restructuring, you must preserve code symbols, framework names, and algorithm names as technical nouns (Rule 1.5), use only simple verb tenses (Rule 3.1), keep sentences short (Rule 5.1), and prefer active voice (Rule 6.1). After restructuring, verify each approved word in the new sentence against Rule 9.2 and Rule 9.3 to ensure correct usage and no phrasal verbs.

---

## 4. Example Pairs

> **Non-STE:** The stack trace in the console must be visible during the debugging session.
>
> **STE:** During the debugging session, make sure that you can see the stack trace in the console.

*(P1, P6 applied — "visible" is an unapproved adjective; the approved alternative "see" is a verb with a different part of speech, so a word-for-word replacement is impossible; the sentence is restructured around the verb "see" with an active imperative construction)*

> **Non-STE:** This configuration option governs whether the linter enforces the rule set in a strict or permissive fashion.
>
> **STE:** This configuration option sets how the linter applies the rules. You can set it to strict or permitted.

*(P1, P2, P7, P11 applied — "governs," "enforces," and "fashion" are all unapproved; no single word-for-word replacement works; the sentence is restructured around the approved verb "sets" and split into two short sentences; "permissive" has no direct approved alternative, so it is restructured to use the approved adjective "permitted")*

> **Non-STE:** The middleware intercepts incoming requests and modifies the headers prior to forwarding them to the downstream service.
>
> **STE:** The middleware gets each request. It changes the headers. Then it sends the request to the next service.

*(P1, P2, P6, P10, P11 applied — "intercepts," "modifies," "prior to forwarding," and "downstream service" are all unapproved or jargon; individual word-for-word replacements produce a meaningless result; the sentence is split into three short sentences; each sentence uses one approved verb; "downstream service" (jargon, P10) becomes "next service")*

---

## 5. Principles Applied

- **P1 — Use approved words:** Rule 9.1 is the fallback for Rule 1.1. When a word-for-word replacement fails, you must construct a new sentence that uses only approved words from the STE-Code dictionary. Every word in the restructured sentence must pass the dictionary check. The three example pairs above demonstrate replacing "visible," "governs," "enforces," "fashion," "intercepts," "modifies," "prior to," "forwarding," and "downstream" — none of which can be swapped one-for-one with an approved alternative of the same part of speech.

- **P2 — Use each approved word with its approved meaning:** After restructuring with Rule 9.1, verify that each approved word in the new sentence carries only its dictionary-approved meaning (Rule 9.2). For example, in the configuration option example above, "sets" must mean "puts into a specified state" — not "a collection of items." In the middleware example, "gets" must mean "receives" — not "obtains by effort."

- **P5 — Technical code nouns are preserved:** When restructuring a sentence, all code symbols, framework names, library names, parameter names, and algorithm names are technical nouns (Rule 1.5) and must remain unchanged. Only the prose around them is restructured. In all three example pairs, technical terms like "stack trace," "console," "debugging session," "linter," "rules," "middleware," "headers," and "request" are kept because they are either approved terms or domain-specific technical nouns.

- **P6 — Use active voice:** When restructuring a sentence with Rule 9.1, prefer the active voice (Rule 6.1). The first example pair demonstrates this pattern: the passive construction "must be visible" becomes the active "make sure that you can see." The third example pair uses three active sentences ("gets," "changes," "sends") instead of one passive-laden sentence.

- **P7 — Do not use technical nouns as verbs:** When restructuring, ensure that code-domain technical nouns are not pressed into service as verbs (Rule 1.7). None of the three example pairs use technical nouns as verbs. The restructured sentences use approved general verbs ("see," "sets," "gets," "changes," "sends") alongside preserved technical nouns.

- **P10 — Replace jargon with plain language:** When restructuring a sentence that uses domain-specific jargon, replace the jargon with an approved plain-language equivalent or define the term on first use. The third example pair replaces "downstream service" (jargon) with "next service." The second example pair replaces "permissive fashion" with the plain approved adjective "permitted."

- **P11 — One term per concept; use short sentences:** Rule 9.1 frequently requires splitting a long compound sentence into multiple short sentences. The second example pair splits one sentence into two. The third example pair splits one sentence into three. After splitting, ensure each sentence stays within the 20-word (procedural) or 25-word (descriptive) limit (Rule 5.1). Also ensure consistency: if you restructure one description of a concept, use the same construction for all descriptions of that concept in the document (Rule 9.4).

- **P13 — Prefer the simple present, simple past, or imperative:** When you restructure a sentence with Rule 9.1, use only the simple verb tenses (Rule 3.1). Do not introduce continuous tenses ("is running"), perfect tenses ("has run"), or complex modals ("might have been running"). All three example pairs use simple present tense and imperative mood exclusively.

- **P14 — Use American English spelling:** All approved words in the restructured sentence must use American English spelling. The words "behavior," "authorization," and "capitalize" follow American conventions. For internationalized documentation, translate the restructured sentences using a maintained glossary that maps approved STE-Code terms to target-language equivalents.

---

## 6. Cross-References

Rule 9.1 interacts with nearly every other rule in the STE-Code system because restructuring a sentence touches vocabulary, grammar, style, and punctuation simultaneously:

- **Rule 1.1 (Use Approved Words):** Always try a word-for-word replacement first. Only use Rule 9.1 when the replacement fails.
- **Rule 1.5 (Technical Code Nouns):** Code symbols, framework names, and algorithm names are exempt from replacement during restructuring.
- **Rule 1.7 (Do Not Use Technical Nouns as Verbs):** When a technical noun is used as a verb, Rule 9.1 provides the method for restructuring around an approved verb.
- **Rule 1.12 (Technical Verbs):** Approved technical verbs ("build," "deploy," "test," "lint") are not replaced. Rule 9.1 applies only to non-technical descriptive prose.
- **Rule 3.1 (Simple Verb Tenses):** Restructured sentences must use only simple present, simple past, or imperative.
- **Rule 5.1 (Short Sentences):** Restructured sentences must not exceed 20 words (procedural) or 25 words (descriptive).
- **Rule 6.1 (Active Voice):** Prefer active voice when restructuring.
- **Rule 9.2 (Use Each Approved Word Correctly):** After restructuring, verify each approved word against its dictionary definition.
- **Rule 9.3 (Do Not Make Phrasal Verbs):** Do not introduce phrasal verbs during restructuring (for example, do not replace "start" with "kick off").
- **Rule 9.4 (Consistent Style):** Use the same restructured construction for the same concept throughout a document.

---

*Generated from STE-Code adapted rule file: a-sec9-rule9.1.md*
