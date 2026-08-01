# Level 5 — Section 1: Words (Rules 1.1–1.14)

STE-Code Section 1 governs **vocabulary** in code documentation. It is the gatekeeping tier of the standard. Every word in every sentence of documentation (READMEs, API docs, docstrings, commit messages, error messages, comments) must pass one of three gates:

1. **Approved word** — listed as APPROVED in the STE-Code controlled terminology (used with its specified part of speech and meaning).
2. **Code-domain technical noun** — a word not in the terminology (or listed UNAPPROVED) that fits one of the 19 technical-noun categories under Rule 1.5 (e.g. component names, type names, protocol names).
3. **Code-domain technical verb** — a word not in the terminology that names a specified domain operation or process (Rule 1.12), e.g. `serialize`, `map`, `allocate`.

A word that passes no gate must be replaced with an approved alternative or the sentence restructured.

This slice distills all 14 Section 1 rules (1.1–1.14) for LLM consumption. Each rule below gives: its wording, the code-domain adaptation, the key judgment calls, and minimal code-domain examples. When you must choose a word for code documentation, apply the rules in order: pick an approved word (1.1→1.4), else a technical noun (1.5→1.9), else a technical verb (1.12), and never slang/jargon (1.10), one-term-per-concept (1.11), American spelling (1.14).

---

## Rule 1.1 — Use Words That Are Approved, Technical Nouns, or Technical Verbs

**Rule (code-domain):** In code documentation, use words that are: approved in the project controlled terminology; code-domain technical nouns; or code-domain technical verbs. STE-Code has a controlled terminology (part 2) giving the most frequently used words in code documentation. Words outside it may be used only if they fit the technical-noun or technical-verb categories.

**Three-gate model:**
- Gate 1 (Approved word): default for general-purpose vocabulary. Must keep the specified part of speech (Rule 1.2) and approved meaning (Rule 1.3).
- Gate 2 (Code-domain technical noun): names a specific concept/component/tool/entity. Must NOT be used as a verb (Rule 1.7).
- Gate 3 (Code-domain technical verb): domain-specific action with no simple approved-word alternative. Must NOT be used as a noun (Rule 1.13).

**Per-artifact guidance:**
- **README:** procedural steps use approved imperative verbs (`run` not `execute`, `make` not `generate`, `set` not `configure`); descriptive prose uses approved adjectives/adverbs (`large` not `substantial`, `correct` not `valid` for data).
- **API docs:** surrounding prose uses approved verbs — `get` not `retrieve`/`fetch`, `send` not `transmit`, `remove` not `delete`/`purge`, `check` not `validate`/`verify`. Function/parameter/type names are technical nouns (Rule 1.5).
- **Docstrings/comments:** prefer shortest approved verb (`do` not `perform`, `check` not `ensure`); use `NOTE:`, `WARNING:`, `FIXME:` markers.
- **Commit messages:** approved imperatives only — `add`, `fix`, `remove`, `update`, `set`, `make`, `check`, `run`. Not `implement` (use `make`/`add`), not `optimize` (use `make faster`/`make smaller`).
- **Error messages:** `cannot` not `unable to`; `incorrect` not `invalid`/`malformed`. No jargon/slang unless a technical noun.

**Examples:**
```
Non-STE:  Execute the script to do the task.
STE:      Run the script to do the task.           # "run" approved verb

Non-STE:  Fetches a user record from the remote API.
STE:      Gets a user record from the remote API.   # "get" not "fetch"

Non-STE:  feat: implement JWT authentication middleware
STE:      feat: add JWT authentication middleware    # "add" not "implement"

Non-STE:  Error: Unable to establish connection.
STE:      Error: Cannot connect to the database.     # "cannot" not "unable to"
```

**Edge cases:**
- Framework name that is also an unapproved word (e.g. `Express`): proper-noun framework names are technical nouns; use the approved verb for the action (`Use Express routing…`).
- Keyword that conflicts with an unapproved word (e.g. `yield`): in code blocks it is quoted text; in prose mark it as a technical noun with backticks and describe with an approved verb (`The \`yield\` keyword gives control back…`).
- Generated docs: exempt when the generator cannot enforce STE-Code, but the source annotations (docstrings/JSDoc/OpenAPI descriptions) that feed it MUST comply.
- Technical verb used as a noun inside a compound (`build system`, `build pipeline`): the compound is a technical noun; standalone `build` as a noun violates Rule 1.13 (say `build procedure`).
- Non-English loanwords in technical terms (`naïve Bayes`, `rendezvous protocol`) are technical nouns; used generically, replace with approved English (`usual` not `de facto`).

**See also:** Rules 1.2, 1.3, 1.4 (approved-word constraints); 1.5, 1.6 (technical-noun exception); 1.7, 1.13 (no noun/verb crossing); 1.12 (technical verbs); 1.14 (American spelling). Dictionary: `a-dictionary.md`; Categories: `a-categories.md`.

---

## Rule 1.10 — Do Not Use Regional, Slang, or Jargon Words as Technical Nouns

**Rule (code-domain):** Do not use regional, slang, or jargon words as code-domain technical nouns. Only a small community understands such words, which causes confusion. When you select technical nouns, always use well-known words.

**What counts as prohibited:**
- **Regional terms:** vocabulary tied to a tech ecosystem (e.g. Ruby "gem"/"rake task" unknown to a Python dev). Use the standard term.
- **Slang (metaphor):** "spaghetti code," "brittle tests," "flaky behavior" → literal descriptions ("code with complex control flow," "tests that fail intermediately," "behavior that is not consistent").
- **Jargon:** fuzzy community-dependent terms ("grok," "cruft," "bikeshedding," "yak shaving," "dumpster fire," "nerfed"). The grammatical test: can it be found in a standard computing dictionary with the same definition? If not, it is jargon. Replace with approved words.
- **Abbreviation jargon:** "AFAICT," "IIRC," "IMHO," and principle initialisms ("DRY," "KISS," "YAGNI") — spell out on first use; better, state the principle directly ("remove duplicate code" not "apply DRY").
- **Temporal jargon:** "modern," "legacy," "cutting-edge" — no fixed meaning; replace with specific dates/characteristics ("written in 2018," "uses async/await syntax").
- **Community nicknames / slang verbs:** "POJO-ify," "bean-ize," "twiddle the bits," "massage the buffer," "yeet," "tweak the knobs," "hit the endpoint," "pwn the DOM" → use approved verbs (convert, change, write to, adjust, remove, set, send a request to).

**Permitted (NOT jargon):** widely-standard abbreviations (API, JSON, SQL, HTML); framework/library/proper-noun names (ESLint, Gradle, Express, Rails); precise technical terms whose meaning is agreed and defined ("undefined behavior," "data race," "monad," "use-after-free") — but spell out abbreviations like "UB"/"UAF" on first use.

**Per-artifact guidance:** README and error messages (global/non-expert audience) are most sensitive — never slang. Docstrings/commit messages form permanent history — write for a developer who joined yesterday. CLI help avoids regional idioms ("twiddle"/"tweak the knobs").

**Examples:**
```
Non-STE:  Remove all the cruft from the legacy module.
STE:      Remove all the unnecessary code from the legacy module.

Non-STE:  The upload went pear-shaped halfway through.
STE:      The upload failed at 50 percent. Check your network connection and try again.

Non-STE:  Yeet the deprecated config parser.
STE:      Remove the deprecated configuration parser.
```

**Review checklist:** (1) read aloud — would a foreign developer understand every word? (2) replace metaphors/idioms with literal text; (3) expand abbreviations on first use; (4) replace community nicknames with standard terms; (5) replace temporal words with dates/characteristics; (6) verify every noun/verb is approved (Rule 1.1) or a justified technical noun (Rule 1.5); (7) no slang verbs as technical actions ("hit," "nuke," "yeet," "tweak," "twiddle" are not approved).

**See also:** Rule 1.1 (approved words), 1.5 (technical nouns), 1.6 (non-approved only as nouns), 1.11 (consistency), 1.12 (technical verbs — not slang), 1.13 (no verb/noun crossing), 1.14 (American spelling).

---

## Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

**Rule (code-domain):** When you select a code-domain technical noun, do not use a different one elsewhere to refer to the same item. The source of truth is the code itself — the class, function, module, table, resource, environment variable, or config key as defined and used in the repository. Use the approved canonical noun consistently throughout.

**Why:** Switching names (e.g. "UserService," "AccountManager," "UserHandler" for one class) breaks the English article/pronoun reference chain — the reader assumes each new name is a new item and searches for it in vain.

**Per-artifact guidance:**
- **README:** one noun per component/service/endpoint; the entry file, main class, or public API name is the source of truth.
- **API docs:** use the URL path, field name, and schema name from the spec (e.g. `/api/login`) — not "the authentication route" or "the login endpoint" interchangeably.
- **Docstrings/comments:** use the entity's own name; no shorthand nicknames.
- **Commit messages:** refer to `src/auth/UserService.ts` consistently, not "the auth module" then "the login handler."
- **Error messages/logs:** use the canonical class/resource name ("PaymentProcessor" not "billing engine").

**Paradigm canonical nouns:** OO → class name; Functional → module-qualified function or type-alias name; Procedural → function/struct/file name (C: prefer typedef alias over tag); Declarative → resource/table name; Systems → language-spec term, defined once in a glossary.

**Examples:**
```
Non-STE:
 1. Initialize the UserService class to start the session manager.
 2. Call the authenticate method on the AccountManager to verify a user.
 3. The UserHandler returns a session token.
STE:
 1. Initialize the UserService class to start the session manager.
 2. Call the authenticate method on the UserService to verify a user.
 3. The UserService returns a session token.            # one noun for one class

Non-STE:  "user_accounts table" / "accounts relation" / "user table"
STE:      "user_accounts table" in all three sentences   # schema-defined name
```

**Edge cases:**
- Framework/library names that collide with approved words ("Make," "Act," "Before"): always use the framework's exact name (capitalized); disambiguate with case/qualifier ("Use the Make build tool to make the project").
- Code keywords in concept names ("async function"): use the full compound noun consistently; mark the bare keyword as code (`\`async\``) when it is syntax.
- Multiple legitimate names across contexts (Docker image `myapp:latest` vs CI `myapp-image`): pick one canonical name per document/section and declare the mapping once.
- Generated-code symbols: use the generated names as technical nouns; do not rename. Declare a shorter alias explicitly at first use if needed.
- Renames during refactoring: after the rename is committed, update all docs to the new name; use a DEPRECATED marker only for public APIs not yet deprecated.

**See also:** Rule 1.1 (the noun must itself be approved), 1.3 (use with approved meaning), 1.5/1.6 (technical-noun qualification), 1.8 (standard noun), 1.9 (prefer short noun), 1.10 (no jargon); Section 3: Rule 3.1 (approved verb forms), 3.6 (active voice).

---

## Rule 1.12 — You Can Use Verbs That You Can Include in a Technical Verb Category

**Rule (code-domain):** You can use verbs you can include in a code-domain technical verb category. A code-domain technical verb refers to a specified operation or process in software development. The controlled terminology does not list them all (there are too many and they vary by project); find them in your project glossary. They must obey the same tense/mood/voice rules as approved verbs (Section 3).

**Priority rule:** If an approved verb in the controlled terminology accurately gives the instruction, USE THE APPROVED VERB. Do not use a technical verb when an approved verb + technical noun works. Only use a technical verb when it is the correct, clear, necessary term for the context (e.g. "detect" is not approved generally → use "find"; but "detect" is the right technical verb in a security IDS context).

**The four categories (examples, not exhaustive):**
1. **Development processes** — a) write/modify: compile, import, inject, instantiate, lint, minify, refactor, resolve, stub, transpile, trace; b) test/verify: assert, benchmark, debug, fuzz, mock, profile, snapshot, spy, unit-test; c) build/package: bundle, deploy, package, publish, release, tag, version; d) deps: hoist, install, link, lock, pin, update, upgrade.
2. **Computer processes & applications** — a) I/O: click, copy, cut, enter, paste, press, print, scan, swipe, tap, type; b) UI/app: clear, close, delete, disable, enable, encrypt, filter, hide, highlight, open, save, scroll, select, show, sort, store, submit, toggle, validate, zoom; c) system: abort, authenticate, authorize, boot, cache, configure, deserialize, download, hydrate, initialize, load, log, mount, process, reboot, render, retry, serialize, spawn, synchronize, throttle, upload.
3. **Subject-field instructions** — a) algorithmic/data: aggregate, bisect, compute, concat, convert, count, decode, encode, escape, filter, hash, index, map, merge, normalize, parse, pipeline, reduce, tokenize, transform, verify; b) DB/storage: backup, compact, flush, migrate, persist, query, replicate, restore, roll back, seed, shard, upsert, vacuum; c) network: broadcast, connect, disconnect, establish, forward, handshake, listen, poll, proxy, route, send, stream, timeout, tunnel, unsubscribe, webhook; d) security: authenticate, authorize, decrypt, hash, revoke, salt, sanitize, sign, validate, verify.
4. **Legal & licensing** — acknowledge, assign, comply with, disclose, enforce, grant, license, modify, notify, permit, regulate, sign, supersede, waive (only for legal/regulatory text).

**Paradigm-specific technical verbs:** OO → instantiate, inherit, override, extend, implement, encapsulate, delegate, inject. FP → compose, curry, map, reduce, fold, recurse, memoize, lift. Procedural → allocate, deallocate, dereference, flush, signal. Declarative → provision, converge, reconcile, apply, destroy. Systems → borrow, own, drop, move, pin, acquire, release.

**Examples:**
```
Non-STE:  If you detect broken wires, repair them.        # "detect" not approved generally
STE:      If you find broken wires, repair them.

Non-STE:  The script initiates a connection and commences the migration.
STE:      The script connects to the database and then migrates the data.

Non-STE:  Git the changes and then push them.             # "Git" is a noun, not a verb
STE:      Commit the changes and then push them.

Non-STE:  The convert() function turns a string into a number, then does an
          operation on each item.
STE:      The convert() function parses a string to an integer, then maps the
          transformation over the list.                    # "parse"/"map" necessary for precision
```

**Edge cases:**
- Framework/tool name that is also a verb ("Express," "Go"): always use it as a technical noun (Rule 1.5); add a qualifier if unclear ("Write the handler as an Express middleware function").
- Code keyword same as approved verb (`return`, `import`): use monospace for the keyword, normal text for the verb.
- Generated code/docs: exempt; refer to generated symbol names as technical nouns. Human-written surrounding text must comply.
- CLI command names (`docker build`, `kubectl apply`): technical nouns; describe the action with "run" (approved) or the technical verb.
- Multi-word technical verbs ("roll back," "drag and drop," "zoom in," "write-ahead"): keep as one unit; do NOT split with an object ("roll back the migration" not "roll the migration back").

**Grammar:** technical verbs follow Section 3 — imperative mood for procedures (no "-ing" main verb: "Compile… Then deploy…"), active voice preferred, full infinitive after "to," and only simple present/past/future tenses (no present/past perfect continuous).

**See also:** Rule 1.1 (try approved verb first), 1.2 (part of speech), 1.5 (tool/framework names are nouns), 1.7 (inverse — no noun as verb), 1.11 (use the verb consistently), 1.13 (no technical verb as noun); Section 3 verb rules.

---

