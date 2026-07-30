# Rule 8.1 — Use All Standard English Punctuation Marks but Not the Semicolon (;)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 8.1

---

## 1. Rule Title and Number

**Rule 8.1** — Use All Standard English Punctuation Marks but Not the Semicolon (;)

---

## 2. Original Rule Summary

The semicolon (;) is not permitted in STE because it enables writers to construct very long sentences that combine multiple independent clauses. It is also a punctuation mark that is not easy to use correctly, even for experienced writers. When you encounter a sentence that uses a semicolon, the required fix is always the same: split it into two or more separate sentences, each with its own subject and verb. This ensures every sentence delivers one complete thought before the reader moves to the next.

---

## 3. STE-Code Adaptation for Code Documentation

In code documentation, the semicolon creates a unique additional hazard: it has a different meaning in many programming languages (statement terminator in C, Java, JavaScript, Rust, and Go), which causes cognitive interference when the same symbol appears in documentation prose. Developers who write semicolons thousands of times per day in code can unconsciously carry them into documentation. The STE-Code rule is absolute — split every semicolon-joined sentence into two or more independent sentences. Each sentence must stand alone so that automated tooling can reliably count words per sentence, and so that a developer debugging at 3:00 AM can read one complete thought at a time without parsing internal clause boundaries.

---

## 4. Example Pairs

> **Non-STE:** The server supports WebSocket connections; these use a persistent channel instead of the standard request-response cycle.
>
> **STE:** The server supports WebSocket connections. These connections use a persistent channel instead of the standard request-response cycle.

> **Non-STE:** POST /sessions creates a new session and returns a token; the token must be included in the Authorization header of subsequent requests.
>
> **STE:** A POST request to /sessions makes a new session and returns a token. You must include the token in the Authorization header of all later requests.

> **Non-STE:** Returns the user record if found; raises UserNotFoundError otherwise.
>
> **STE:** The function returns the user record when the user ID matches a database entry. The function raises a UserNotFoundError when the user ID does not match any entry.

---

## 5. Principles Applied

- **P1 — Split semicolon into two sentences:** Every semicolon that joins two independent clauses must be replaced by a period. Each clause becomes its own sentence with a subject and verb. This is the primary fix pattern for Rule 8.1 and applies to all six example pairs above.

- **Rule 3.1 — Use simple sentences:** After splitting a semicolon sentence, verify that each resulting sentence is a simple subject-verb-object clause. If a split sentence is still complex, simplify it further. The docstring example above shows this: the original had two return conditions in one sentence; the STE version uses two simple sentences with repeated subjects for clarity.

- **Rule 4.1 — Keep sentences short:** Semicolons let writers evade the 20-word (procedural) and 25-word (descriptive) sentence length limits. Removing semicolons and splitting sentences makes length compliance mechanically verifiable. Each STE sentence in the examples above stays within the length limits.

- **Rule 4.4 — Use connecting words and phrases:** After splitting a semicolon sentence, use an approved connecting word (and, but, thus, then) to show the logical relationship between the two new sentences when the relationship needs to be explicit. The README example uses the demonstrative adjective "these" to connect the second sentence back to the first.

- **Rule 6.1 — Use imperative mood for instructions:** When one of the split sentences is a recovery action or instruction, write it in the imperative mood. The API documentation example uses "You must include" to give a clear instruction in the second sentence.

- **Rule 3.3 — Use lists for complex items:** When a semicolon is used as a super-comma to separate list items that themselves contain commas, restructure the content as a bullet list or table instead. This eliminates the semicolon entirely and makes the nesting visually explicit.

- **Rule 1.1 — Use approved words:** The connecting words added after splitting a semicolon sentence (and, but, thus, then) must come from the STE-Code approved dictionary. Do not invent new connecting words.

- **Rule 1.3 — Use words only with their approved meanings:** Each connecting word must carry its approved meaning. Do not use "thus" to mean "and" or "but" to mean "then."

- **Rule 8.2 — Use hyphens for word connections:** Hyphens connect words; semicolons connect clauses. Do not confuse these two punctuation marks. If you are connecting words, use a hyphen. If you are connecting clauses, split into two sentences.

---

*Generated from STE-Code adapted rule file: a-sec8-rule8.1.md*
