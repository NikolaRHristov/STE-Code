# Level 4 — Punctuation, Word Count & Document Formatting (STE-Code Section 8)

This slice of STE-Code covers the punctuation and word-count rules that apply
to all code documentation: README files, API reference docs, docstrings,
inline comments, commit messages, error messages, configuration comments, and
specification documents. It does NOT apply to source code (where semicolons
and parentheses are language syntax) or to code shown inside code blocks.

Rules in this slice:
- 8.1 — No semicolons
- 8.2 — Hyphens connect directly related words
- 8.3 — Permitted uses of parentheses
- 8.4 — Colon before a vertical list acts as a period
- 8.5 — Parenthetical text counts as one word (and forms its own sentence)
- 8.6 — Elements that count as one word for sentence length
- 8.7 — Hyphenated words count as one word

Use this document to check a draft of code documentation for punctuation and
length compliance. Each rule gives the constraint, the code-domain rationale,
canonical examples, edge cases, and cross-references. The "Reference Catalogue"
at the end lists every pattern an LLM should apply or recognise.

---

## Rule 8.1 — Use all standard English punctuation but NOT the semicolon (;)

**Constraint.** In code documentation you may use every standard English
punctuation mark except the semicolon (;). When two independent clauses would be
joined by a semicolon, write two sentences instead.

**Why.** The semicolon lets a writer pack two complete thoughts into one
sentence, which is hard to parse — especially for non-native English readers.
It also carries a different meaning in most programming languages (statement
terminator in C, C++, Java, JavaScript, Rust, Go), which creates cognitive
interference when the same symbol appears in prose. The fix is always the same:
split into two or more sentences, each with its own subject and verb.

**Where it applies.** README files, API docs, docstrings, inline comments,
commit messages, error messages, configuration comments, spec documents. It does
NOT apply to source code or to code inside code blocks.

**Code-domain examples.**

| Non-STE | STE |
|---------|-----|
| `Call the function to parse the response data; handle any errors that occur.` | `Call the function to parse the response data. Handle any errors that occur.` |
| The cache is invalid after a write operation; you must flush it before the next read. | The cache is invalid after a write operation. You must flush it before the next read. |

```python
def fetch_user(client, user_id):
    """Call the function to parse the response data. Handle any errors that occur.

    Parameters:
        client: The HTTP client.
        user_id: The identifier of the user.

    Returns:
        A user record.
    """
    response = client.get(f"/users/{user_id}")
    data = json.loads(response.text)
    if "error" in data:
        raise UserError(data["error"])
    return data
```

Per documentation type:
- **README:** split a feature from its rationale into two sentences.
- **API docs:** write the primary effect as one sentence, the secondary effect as a second.
- **Docstrings:** use a bullet list for multiple return conditions. Use separate sentences for multiple side effects.
- **Commit messages:** each body sentence states one fact. Split any semicolon you find.
- **Error messages:** "X is not valid. Do Y to fix this."
- **Config comments:** write the purpose as one sentence, the trade-off as a second.

**Edge cases.**
1. Semicolons inside code blocks/fences are language syntax — exempt. Inline backtick code (`const x = 5;`) is also exempt; the prose around it must obey the rule.
2. Auto-generated docs may splice semicolons. This is exempt for machine output. Write your source comments with periods only.
3. Semicolons inside quoted strings (error output, log text) are exempt. Keep the semicolon in the quote. Put the period outside.
4. A semicolon used as a super-comma in a list → replace the list with bullets or a table.
5. Chat and code-review threads are informal and exempt. Commit messages are NOT exempt (permanent history).
6. A semicolon inside a regex or data string is data, not prose — exempt inside the code span.

**Cross-references.** Rule 1.1 (approved words for connecting words), Rule 3.1 (simple sentences), Rule 4.1 (short sentences), Rule 4.4 (connecting words), Rule 8.2 (hyphens, not semicolons, connect words).

---

## Rule 8.2 — Use hyphens (-) to connect words that are directly related

**Constraint.** Use a hyphen to connect two or more words that function as one
concept — usually a compound adjective before a noun. The hyphen signals to the
reader that the words form a single unit and prevents ambiguity about what
modifies what.

**Five code-domain hyphenation categories.**
1. Compound adjectives before a noun: `high-priority task`, `read-only file`, `thread-safe method`, `event-driven architecture`, `type-safe interface`, `end-to-end test`, `server-side rendering`, `just-in-time compilation`, `fire-and-forget pattern`.
2. Two-word fractions/numbers: `seventy-two`, `three-fourths`, `one hundred and twenty-eight`.
3. Uppercase-or-number + noun (shape/config): `L-shaped bracket`, `64-bit register`, `8-byte alignment`, `128-bit value`, `3-prong connector`.
4. Verb whose first part is a noun: `dry-run`, `hot-reload`, `cold-start`, `hard-code`, `soft-delete`, `short-circuit`.
5. Prefix ending in a vowel + root starting with a vowel: `pre-initialized`, `re-entrant`, `de-allocated`, `anti-aliasing`, `re-indexed`.

**Code-domain examples.**

| Non-STE | STE |
|---------|-----|
| `// The high priority task must acquire the write lock` | `// The high-priority task must get the write lock` |
| `@param fd  A read only file descriptor` | `@param fd  A read-only file descriptor` |
| `Expected non negative integer` | `Expected non-negative integer` |

```go
// The thread-safe singleton uses lazy initialization to defer object creation
// until the first access.
class CacheManager { ... }
```

**Paradigm key compounds.**
- OOP: `read-only property`, `thread-safe collection`, `lazy-initialized singleton`, `reference-counted pointer`.
- Functional: `pure-function semantics`, `higher-order function`, `side-effect-free computation`, `persistent-data structure`, `tail-recursive call`.
- Procedural: `null-terminated string`, `zero-initialized struct`, `short-circuit evaluation`, `newline-delimited output`, `statically-linked binary`.
- Declarative: `left-joined table`, `fully-qualified column name`, `cluster-scoped resource`, `base64-encoded value`, `read-committed isolation`.
- Systems: `move-semantics transfer`, `borrow-checked reference`, `memory-mapped I/O`, `copy-on-write page`, `lock-free stack`, `undefined-behavior risk`.

**Edge cases.**
1. Keep hyphens in hyphenated tool names (`create-react-app`). Do not add a second hyphen when you use the name as a modifier.
2. Code keywords in prose: hyphenate as compound adjectives (`type-of operator`), but reproduce the keyword exactly in code spans (`typeof x`).
3. Generated/uncontrolled output: leave it as-is. Add a NOTE in the prose.
4. Established unhyphenated compounds in a codebase (`filename`, `namespace`) may stay if unambiguous and consistent.
5. URL path segments use kebab-case as proper nouns — keep them. Hyphenate prose adjectives normally.

**Grammar notes.**
- Hyphenate in attributive position (before the noun): `thread-safe collection`. Do NOT hyphenate in predicative position (after a linking verb): `the collection is thread safe`.
- Do NOT hyphenate when the first word is an `-ly` adverb: `a fully-qualified name` is wrong; use `a fully qualified name`.
- `self-` compounds always take a hyphen: `self-contained`, `self-signed`, `self-healing`.
- Do not insert hyphens into code identifiers (camelCase stays camelCase in backticks).

**Cross-references.** Rule 1.1 / 1.5 (technical nouns in compounds), Rule 1.9 (shorten long compounds), Rule 1.11 (use one form consistently), Rule 8.1 (punctuation pair), Rule 8.6 / 8.7 (hyphenated = one word).

---

## Rule 8.3 — Use of parentheses

**Constraint.** In code documentation, parentheses are permitted for these
uses (do NOT use square brackets `[ ]` for parentheticals; they are reserved for
optional syntax in code):

1. References to modules, diagrams, or text — `Call the request handler (Figure 3, Module A).`
2. Letters/numbers identifying items — `Disconnect the endpoints (2) and (12) from the load balancer (8).`
3. Work-step numbering in procedures — `(1) Install the dependency package (4).`
4. Abbreviations on first use — `A Command Line Interface (CLI) is ...`
5. Singular/plural at once — `Before you run the test(s), set the environment variable(s).`
6. Explanations of a word or clause — `Increase the timeout slowly (not more than 1000 ms each step).`
7. Alternatives — `Use the left (right) API key for the staging (production) environment.`

**Code-domain examples by type.**
- README: define abbreviations on first use. Reference related docs concisely.
- API docs: show units (`timeout: milliseconds (ms)`), status codes (`404 (Not Found)`), parameter constraints.
- Docstrings: show value ranges in parentheses (`timeout: milliseconds (1 to 30000)`); skip repetition already in the type signature.
- Commit messages: scope and issue refs — `feat(auth): add PKCE support (issue #482)`.
- Error messages: put diagnostic values at the END in parentheses — `Cannot find the configuration file (searched: /etc/myapp/config.yaml).`

**Edge cases.**
1. Framework/library names that are also common words — clarify in parentheses on first use: `Flask (the Python web framework)`.
2. Code keywords that are also punctuation (e.g. Rust `()`): keep the code literal; explain in a separate sentence, not nested.
3. Generated docs auto-insert parentheses — leave them. Apply the rule to human-written descriptions.
4. Never nest parentheses — split or restructure: `Set the cache TTL to 3600 (one hour). For production, set it to 86400 (one day).`
5. CLI `--help` text: use sparingly; prefer the alternative or explanation pattern.

**Grammar notes.** Parentheses are a secondary boundary. The period is primary.
Do NOT use em-dashes for asides (not permitted in STE). The abbreviation pattern
is always "Full Term (ABBR)" — after first use, use only the abbreviation. A
complete-sentence parenthetical should become its own sentence.

**Cross-references.** Rule 1.1 (abbreviation words), Rule 1.3 (approved meanings in explanations), Rule 1.9 (short technical nouns), Rule 5.1 (parenthetical word count), Rule 6.3 (one step per numbered line), Rule 8.2 (parentheses explain. Hyphens join).

---

## Rule 8.4 — Colon (:) in a vertical list acts as a period

**Constraint.** In a vertical list, the colon before the list has the effect of
a period. The introductory text before the colon must obey sentence length:
**20 words max for procedural text, 25 words max for descriptive text.** Each
list item after the colon is a new sentence with its OWN 20/25-word limit.

**Why.** This prevents burying enumerated content in a long clause-heavy
introduction. The introduction should state only what the list contains. The
items carry the detail.

**Code-domain examples.**

| Non-STE | STE |
|---------|-----|
| The config file, which is in the project root, supports these profiles that you can use for deployment: a development profile ..., a staging profile ..., and a production profile ... | The configuration file supports these environment profiles: - Development - Staging - Production. |

API docs, docstrings, commit messages, error messages, and config comments all
follow the same shape: short intro + vertical list. Each item is one thought.

**Edge cases.**
1. Code tokens in backticks inside the intro count as ONE word each (`com.example.service.UserRepository` = 1 word). Prefer ≤15 total words and ≤1 code token.
2. One level of nesting is allowed. The parent item is a short category heading.
3. A list item may contain a fenced code block — the prose part obeys the limit. The block contributes 0 words.
4. Long framework names: move them into the list items. Use a generic intro.
5. Generator-produced lists: obey the rule in your source comments. Accept rendered output.

**Cross-references.** Rule 1.1 (approved words in items), Rule 3.1 (one subject-verb-object per item), Rule 4.1 (length at two points: intro + items), Rule 6.3 (procedural lists), Rule 8.1 (colon replaces semicolon-joined enumerations).

---

## Rule 8.5 — Parentheses and word count

**Constraint.** When you put text in parentheses, it counts as **one word** in
the enclosing sentence. AND the words inside the parentheses form their OWN
separate sentence with its own 20/25-word limit. An identifier or abbreviation
in parentheses (a number, letter, alphanumeric code) also counts as one word.

**Two kinds of parentheticals.**
- **Identifier parentheticals** — `(10)`, `(EACCES)`, `(CI/CD)`, `(v2.1)`, `(PROJ-2847)`. Count as one word; no sentence-length limit (not prose).
- **Explanatory parentheticals** — `(the DEBUG flag is off)`, `(the worker runs every 60 seconds)`. Count as one word in the main sentence AND form a complete separate sentence (subject + verb) that must obey the limit.

**Critical rule.** Do NOT hide safety conditions, required steps, or warnings
in parentheses. If the reader must act on it, it deserves its own sentence or a
labeled block (`BREAKING`, `DEPRECATED`, `NOTE`). In systems docs, never put a
safety precondition in parentheses — use a `# Safety` section.

**Code-domain examples.**

| Non-STE | STE |
|---------|-----|
| Make sure DEBUG is false before you run the deploy in prod (the DEBUG flag must be explicitly disabled for all prod workloads to prevent log leakage). | Make sure that the DEBUG environment variable is set to false (the DEBUG flag is off). |
| Remove the health check flag number ten. | Remove the health check flag (10). |

**Edge cases.**
1. `function()` inside backticks is one atomic word — its parentheses are not Rule 8.5 parentheticals.
2. A URL in parentheses is an identifier (one word). If it has explanatory text after it, that text forms a sentence.
3. Never nest parentheses — restructure or use an em-dash for the inner aside.
4. Framework method names with parentheses (`expect()`): backtick them; one word.
5. Generated parentheticals (type hints, defaults): accept. Obey the rule in your own prose.

**Cross-references.** Rule 1.5 / 1.6 (technical nouns in parentheticals), Rule 3.1 (the parenthetical is a sentence), Rule 3.3 (long parentheticals signal a restructure), Rule 4.1 (limit applies to the parenthetical sentence too), Rule 8.1 (no semicolons inside parentheticals), Rule 8.4 (parentheticals inside list items).

---

## Rule 8.6 — Elements that count as one word

**Constraint.** When counting words for sentence length (20 procedural / 25
descriptive), count EACH of these as ONE word:

1. **Numbers** — `13`, `16`, `twenty-one`. (Do NOT count numbers that identify paragraphs or work steps — they are document numbering.)
2. **Numbers with units** — `10 ms`, `20 MB`, `10 μs`, `3000` + `seconds`.
3. **Abbreviations** — `CI/CD`, `VPN`, `JWT`, `OWASP`, `a.m.` (counts with its number).
4. **Alphanumeric identifiers** — `No. 1`, `E36L7`, `ERR_PG_TIMEOUT_0099`, `cache.miss.count`, `useUserProfile(userId)`.
5. **Quoted text** — anything in `"..."`, `` `...` ``, `<code>...</code>`, or UPPERCASE labels. Includes formulas (`C = (A - B) - 0.063 mm` = 1 word) and backtick-quoted paths/commands.
6. **Titles, headings, UI text, labels** — `Operations Runbook`, `Error Handling and Recovery`, dialog warnings (`"WARNING: This operation permanently deletes all user data."` = 1 word).
7. **Proper nouns** — individuals (`Linus Torvalds`), organizations (`Apache Software Foundation`), geopolitical entities (`United States of America`), and framework/library names (`React`, `AWS Lambda`, `Express`).

**Why this matters.** Correct application shrinks the apparent word count of a
sentence by 3–8 words on average (largest in API docs and READMEs), making it
easier to obey the 20/25 limits.

**Code-domain example.** "Set `http.client.retry.max.attempts` to 5. Set `http.client.retry.backoff.millis` to 1000." — each backtick path is 1 word, each number is 1 word.

**Edge cases.**
1. Framework names with "unapproved" words (`Express`, `Swift`, `React`) are proper nouns (1 word) — do not rewrite them; treat `React` as a noun, not a verb.
2. Code keywords quoted in docs (`class`, `return`) are quoted text (1 word); in your own prose use them as technical nouns/verbs per Rule 1.5/1.12.
3. Generated code/comments count as one word (category 6) when you cannot change them.
4. Quoted text inside quoted text — the outer fence defines the boundary; everything inside is 1 word.
5. Semantic version strings (`1.2.3-alpha.1+build.456`), commit hashes (`a1b2c3d`), image digests (`sha256:abc...`) are alphanumeric identifiers (1 word each). "Version 1.2.3" = 2 words.
6. Numbers that identify document parts (rule numbers in cross-refs, step numbers, issue IDs used as refs) are exempt structural numbering.

**Cross-references.** Rule 1.1 (proper nouns/identifiers exempt from approved-word rule), Rule 1.5 / 1.6 (framework names are technical nouns = proper nouns), Rule 1.14 (keep non-American spelling in proper nouns), Rule 8.7 (hyphenated = one word, a separate case).

---

## Rule 8.7 — Hyphenated words count as one word

**Constraint.** A hyphenated word group counts as ONE word for sentence length,
whether it is a compound adjective before a noun or a long hyphenated technical
noun. The hyphen joins the words into a single unit, so count the unit, not the
individual words inside it.

**Case 1 — Compound adjectives (before a noun, hyphenate):** `read-only file descriptor`, `thread-safe singleton`, `event-driven architecture`, `client-side rendering pipeline`, `end-to-end test suite`, `backward-compatible API`. After a linking verb, write them as separate words and count each: `the singleton is thread safe` = 5 words.

**Case 2 — Long hyphenated technical nouns:** `cutoff-switch power connection` (3 words: `cutoff-switch`/`power`/`connection`), `build-time environment variable` (3: `build-time`/`environment`/`variable`), `client-side rendering pipeline`, `sign-in error message`, `look-up table index`. Only the hyphenated group is one word; the following words are separate.

**Worked count.** "The build-time environment variable must point to the staging cluster." = 10 words (`build-time` is 1). "The thread-safe singleton must cache the read-only file descriptor." = 9 words (both hyphenated terms are 1 each).

**Interaction with other rules.**
- Rule 8.2 (when to hyphenate) + Rule 8.7 (how to count) work together.
- Rule 8.6 covers numbers/units/abbreviations/identifiers; a hyphenated word is a SEPARATE case — do not double-count it as an identifier.
- A hyphen in a spelled-out numeral (`twenty-one`) or range (`pages 10-15`) is covered by Rule 8.6, not 8.7.

**Approved code-domain hyphenated terms (each = one word before a noun).**
`read-only`, `write-only`, `thread-safe`, `event-driven`, `client-side`, `server-side`, `end-to-end`, `backward-compatible`, `low-latency`, `build-time`, `run-time`, `sign-in`, `check-out`, `request-response`.

When such a term follows the noun or a linking verb, write it as separate words and count each word.

**Cross-references.** Rule 8.2 (use hyphens), Rule 8.6 (other one-word elements), Rule 4.1 / 4.2 (sentence-length limits that hyphenation helps you meet).

---

## Reference Catalogue — apply/recognise these patterns in code documentation

**Punctuation allowed:** period (.), question mark (?), exclamation mark (!), comma, colon (:), hyphen (-), parentheses ( ) for the seven listed uses.
**Punctuation banned:** semicolon (;). Em-dashes for asides are not permitted; use parentheses (own sentence) or split into sentences. Square brackets are for code syntax only.

**Sentence-length limits (the master constraint):** 20 words procedural, 25 words descriptive. Count via Rule 8.6 (identifiers/numbers/abbreviations/quoted text/proper nouns = 1 word) and Rule 8.7 (hyphenated groups = 1 word).

**Quick checklist for an LLM reviewing/revising code documentation:**
1. No semicolons in any prose. Split into sentences.
2. Semicolons inside code blocks/fences/backticks — leave them (language syntax).
3. Compound adjectives before a noun get a hyphen; the same words after a verb do not. Never hyphenate `-ly` adverb + adjective. `self-` always hyphenated.
4. Parentheses only for: refs, item IDs, step numbers, abbreviations, singular/plural, explanations, alternatives. Never nest. Never hide safety/required info in them.
5. A parenthetical = 1 word in the sentence AND its own sentence with its own 20/25 limit (identifiers excepted).
6. Vertical list: intro ≤ 20/25 words; each item ≤ 20/25 words. Use a colon, then bullets.
7. Count identifiers, numbers+units, abbreviations, backtick code, proper nouns, and hyphenated groups as ONE word each.

**Cross-slice links.** These punctuation/length rules interact most with:
Rule 1.1 (approved words), Rule 3.1 (simple sentences), Rule 4.1 (short sentences),
Rule 4.4 (connecting words after a semicolon split), Rule 6.3 (procedural lists).
Apply them together — a document can pass general sentence rules yet still fail
Rule 8.1/8.4/8.5 on punctuation and list structure.
