# Level 5 — Section 9: Sentence Construction & Word Usage (Rules 9.1–9.4)

This sub-document distills the four "writing-level" rules of STE-Code for use by an
LLM that generates or revises code documentation. It covers how to restructure
sentences when a word-for-word replacement fails (9.1), how to use each approved
word with its exact meaning and part of speech (9.2), why phrasal verbs are
prohibited (9.3), and why consistent terminology across a document or project is
mandatory (9.4).

These four rules sit at the top of the STE-Code writing stack. When a candidate
word is not in the controlled terminology, try a word-for-word replacement (9.2).
If no same-part-of-speech alternative keeps the meaning, restructure the sentence
(9.1). Never reach the meaning through a phrasal verb (9.3), and never vary the
term you picked (9.4).

All examples are code-domain. Code symbols (keywords, framework names, function
and variable names) are technical nouns and never change — only surrounding prose
is edited.

---

## Rule 9.1 — Restructure When a Word-for-Word Replacement Is Not Sufficient

**Core instruction.** Use a different sentence construction when you cannot replace
an unapproved word with an approved word of the same part of speech without
changing the meaning.

**When restructuring is required:**
1. You must change the grammatical structure to use the approved alternative.
2. A word-for-word replacement gives a meaningless or unclear result.
3. The approved alternative would change the meaning.
4. The word to replace is not in the controlled terminology at all.

**Procedure when a replacement fails:**
- Think about the *purpose* of the sentence, then select different words.
- Frequently you must: select different words, use a different verb form, write
  shorter sentences, remove unnecessary information, or get more detail from a
  developer.
- Keep code symbols unchanged (Rule 1.5). Only the prose around them changes.

**Code-domain examples (Non-STE → STE):**

| Non-STE | STE | Why |
|---|---|---|
| A timeout value of 5000 ms is **acceptable** for this endpoint. | A timeout value of 5000 ms is **permitted** for this endpoint. | "acceptable" not approved; "permitted" is same part of speech and keeps meaning → word-for-word replacement is enough, no restructure. |
| The stack trace in the console must be **visible** during the debugging session. | During the debugging session, **make sure that you can see** the stack trace in the console. | "visible" (adj) → "see" (verb); restructure around the agent "you." |
| **Loop** the function twice to remove null values from the array. | **Run** the function for two iterations to remove null values from the array. | "loop" not approved; "iteration" (noun) + "run" (verb) replace it; "twice" → "two" (technical). |
| Without this change, the behavior of the function can be **uncertain**. | Without this change, it is possible that the function will not behave as expected. | "uncertain" not in terminology; word-for-word fails → new sentence. |
| **Just** add a single log statement to the method. | **Only** add a single log statement to the method. | "just" → "only"; do NOT use "immediately" here (changes meaning). |

**Restructuring patterns (reuse these):**

- *Adjective → verb:* "X is visible/configurable/accessible" → "make sure that you
  can see/set/open X." Example: "The configuration panel is accessible only to
  administrators." → "Only administrators can open the configuration panel."
- *Noun → verb:* nominalizations ("retrieval", "validation", "execution") pair with
  light verbs ("perform", "carry out"). Drop the light verb: "perform the retrieval
  of X" → "get X." Example: "The service performs the validation of each request"
  → "The service checks each request."
- *Split long sentences* before a conjunction ("and", "or", "but"), a conditional
  ("if", "when"), or between cause/effect. After splitting, each sentence must
  stand alone.

**Per documentation type:**

- *README:* replace passive with active instructions; move complex detail to a
  separate doc; use bullets; drop marketing language.
  Non-STE: "This library leverages asynchronous I/O to facilitate high-throughput
  data processing." → STE: "This library uses async I/O. It can process large
  quantities of data quickly."
- *API docs:* keep parameter names unchanged (Rule 1.5); restructure the
  description around the approved word; use a different subject if the original
  subject depends on an unapproved word; split compound descriptions.
  Non-STE: "This endpoint facilitates the retrieval of user profiles." →
  STE: "This endpoint gets user profiles."
- *Docstrings/comments:* use the approved verb form even if longer; move complex
  detail out; never change a code symbol.
  Non-STE: `"""Computes the aggregate of the supplied metrics and persists them."""`
  → STE: `"""Gets the total of the metrics and saves them."""`
- *Commit messages:* imperative summary ("Add feature"); put detail in the PR.
  Non-STE: "Implemented utilization of the cached connection pool to expedite
  request handling." → STE: "Use the cached connection pool to make requests
  faster."
- *Error messages:* state what happened and what to do; keep stack traces/symbols
  unchanged.
  Non-STE: "The application encountered an unrecoverable exception while attempting
  to instantiate the connection pool." → STE: "The application cannot start the
  connection pool. Look at the log for more data."

**Paradigm-specific notes:**

- *OOP (Java/C#/C++/Python classes):* "provides an abstraction that facilitates"
  → restructure to the concrete purpose. Non-STE:
  "The `BaseRepository` class provides an abstraction that facilitates data access
  operations across multiple database backends." → STE: "The `BaseRepository`
  class lets you use the same data access methods with different databases."
- *Functional (Haskell/Elixir/Rust):* type signatures stay unchanged; "maps over"/
  "folds" are technical verbs only when naming an op — in general prose use
  "applies a function to each element."
- *Procedural (C/Go/Bash):* "deallocate" → "free" or "release"; "pipe command A to
  command B" → "send the output of command A to command B" unless "pipe" is a
  keyword in context.
- *Declarative (SQL/Terraform/K8s):* naturally passive/stative — split and use
  active: Non-STE: "This Deployment manifest orchestrates the rollout of three
  replicated Pods, ensuring high availability through automated rescheduling." →
  STE: "This Deployment makes three copies of the Pod. If a Pod stops, the system
  starts a new Pod automatically."
- *Systems (Rust ownership/C memory):* keywords (`move`, `borrow`) keep their
  technical meaning in code font; in prose, "borrow" → "get a reference to", "own"
  → "has".

**Edge cases:**

- *Framework name = English word* (Flask, Vite, Express, Tailwind): keep the name
  unchanged; never use it as a verb. "Flask your application" → "Use Flask with
  your application."
- *Keyword = approved word* (Rust `use`, `move`; `return`; `break`): code font =
  technical noun; prose = approved meaning. "You must move the value with the
  `move` keyword, then give it back from the function."
- *Generated code symbols* with unapproved words (e.g. `utilizeData()`): keep the
  symbol; describe it with approved words — "The `utilizeData()` function uses the
  data to make a report."
- *Quoted log/error text:* keep verbatim (it is data); explain it with approved
  prose.
- *Restructuring loses precision* (e.g. security audit): (1) split + clarifying
  note, (2) keep the term in code font with a glossary definition, or (3) for an
  internal expert audience keep it as a technical noun with an approved-word
  definition on first use.
- *Algorithm names* (QuickSort, Two-Phase Commit): technical nouns, keep unchanged;
  describe behavior with approved words.
