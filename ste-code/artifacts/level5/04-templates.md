# Level 5 — Document Templates (code review / PR feedback)

Level 5 is the full STE-Code standard: every rule, the extension vocabulary, the
reference catalogue, and provenance. This sub-document is the **document
templates** slice — reusable, code-domain skeletons you can drop into an LLM
prompt when it generates or reviews code documentation: README pages, API
reference entries, docstrings, inline comments, commit messages, error messages,
configuration comments, and pull-request descriptions.

The templates below are distilled from the standard's rules on consistency
(Rule 9.4), safety instructions (Rule 7.2), sentence construction (Rule 9.1),
and the word / grammar rules that govern each genre. They are faithful to the
standard and use code-domain examples only. Use them as fill-in-the-blank
scaffolds; do not invent rules that are not in the standard.

## The three consistency templates (Rule 9.4)

Every genre below obeys the same three consistency rules. Pick one term, one
verb, and one sentence structure per action, and reuse it every time that
action appears.

- **Lexical consistency** — one term per concept. Do not alternate between
  "configuration file," "settings file," and "config" for the same file.
- **Syntactic consistency** — same structure for the same action. All setup
  steps, all configuration steps, and all verification steps share one template.
  The template signals the step type before the reader parses the content.
- **Semantic consistency** — same meaning for the same term across files,
  modules, and documentation types. If "build" means "compile and link" in the
  README, it must not mean "compile, link, and package" in the CI docs.

A reviewer comment that flags a synonym swap is a valid STE-Code finding.

---

## Template 1 — README / procedural doc page (Rules 5.3, 5.4, 8.1, 9.4)

Use imperative sentences for each step. Put a descriptive statement before the
command only when the reader needs context first (Rule 5.4). One sentence per
step. No semicolons (Rule 8.1).

```
## <Section title>

<Optional one-sentence context: why this step exists.>

1. <Imperative verb> <object> to <purpose clause>.
2. <Imperative verb> <object> to <purpose clause>.
3. <Imperative verb> <object>.
```

Worked example (STE):

```
## Configure the server

1. Open the configuration file in a text editor.
2. Change the port number in the configuration file.
3. Save the configuration file and close it.
4. Build the project with the build command.
```

Non-STE (three names for one file, three verbs for one action): "Open the
configuration file… Change the port in the settings file… Save the config…
Compile the project… Make the binary…" — each synonym forces the reader to
pause and ask "is this the same thing?"

## Template 2 — API reference entry (Rules 1.3, 9.1, 9.4)

Name each parameter exactly as it appears in the signature. Use the approved
word for the field's meaning (e.g. "permitted," not "acceptable"). Keep the
description to one short sentence.

```
### `VERB /path` — <Short resource name>

<One sentence: what the endpoint does.>

| Parameter   | Type    | Description                              |
|-------------|---------|------------------------------------------|
| `<name>`    | `<type>`| <One short sentence using the exact name.>|

**Responses**
- `200` — <one sentence>
- `4xx` — <one sentence>
```

Worked example (STE): the parameter `timeout_ms` is described as "A timeout
value of 5000 ms is permitted for this endpoint." (approved word "permitted").
The same field must be called `timeout_ms` in prose, schema, and code — never
"creation date" / "timestamp" / "created time" for one response field.

---

## Template 3 — Function docstring (Rules 1.9, 9.4)

The docstring uses the same term that appears in the signature. A parameter
named `max_retries` is "max_retries" in the body, never "maximum attempts" or
"retry limit." Use the shortest unambiguous term (Rule 1.9).

```
def <name>(<params>) -> <type>:
    """<One sentence: what the function does.>

    Args:
        <param>: <one short sentence, same name as signature>
    Returns:
        <one short sentence>
    """
```

Worked example (STE):

```python
def validate_email_address(value: str) -> bool:
    """Validate an email address against RFC 5322.

    Args:
        value: The string to validate.
    Returns:
        True if the string is a valid address.
    """
```

Do not write the 36-word paraphrase of the regex pattern — the signature and
the standard name the concept.

## Template 4 — Inline comment (Rules 1.9, 8.1, 9.4)

One short sentence. The code or the key name carries the context; the comment
only names the purpose in the shortest form. No semicolons.

```
# <Short phrase: the purpose of the next block>
```

Worked examples (STE):
- Config: `# Maximum number of parallel workers.` (the key `max_workers` and
  value `8` already state the rest — do not copy a 9-word phrase as the comment).
- Test: `# Checks that the fetch utility returns JSON from the API endpoint.`
  (the function name and `assert` line name the subject and expectation).

---

## Template 5 — Commit message (Rules 5.3, 7.1, 7.2, 9.4)

Imperative, one verb per category, consistent across the project. If the
convention is `Add`, do not mix in `Introduce`, `Insert`, or `Create`. If the
convention is `Fix`, do not mix in `Resolve`, `Correct`, or `Patch`.

```
<Type>: <Imperative summary in one sentence, <= 72 chars>

<Optional body: one sentence per point. For safety, start with the
command or condition (Rule 7.2).>
```

Worked examples (STE):
- `Add the configuration parser for the YAML settings file.`
- `Fix the connection leak in the worker pool.`
- Safety body: `WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. ALWAYS USE
  ENVIRONMENT VARIABLES OR A SECRETS MANAGER TO STORE API KEYS. API KEYS IN
  SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.`

If a commit needs many unapproved words, write a shorter message and put the
details in the pull-request description.

---

## Template 6 — Error message (Rules 7.1, 7.2, 9.4)

An error code must produce the same text every time (reliability property, Rule
9.4). Start with a signal word when the message carries risk. The reader
correlates the message with the code by the exact code name.

```
<Optional signal word: WARNING | CAUTION> <Clear command or condition, one sentence.>
```

Worked examples (STE):
- `E_CONNECT_FAIL: Cannot connect to the database. Check the connection string.`
- `WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.`

Do not let `E_CONNECT_FAIL` say "connection refused" in module A and "cannot
connect to server" in module B — the operator cannot search logs reliably.

## Template 7 — Configuration-file comment (Rules 1.9, 8.1, 9.4)

The key and value state the setting; the comment names only the purpose. One
sentence per option. No semicolons (split purpose and trade-off into two
sentences).

```
# <Purpose of this option, one short phrase.>
<key> = <value>
# <Optional trade-off, one sentence.>
```

Worked example (STE):

```
# Maximum number of parallel workers.
max_workers = 8
# A higher value uses more memory.
```

---

## Template 8 — Pull-request / review description (Rules 5.3, 5.4, 8.1, 9.4)

Write instructions as imperative sentences. Give context before a command only
when the reviewer needs it. One sentence per point; use numbered steps for
multi-step workflows so the reviewer can complete one before reading the next.

```
## Summary
<One or two sentences: what this change does.>

## Changes
1. <Imperative verb> <object>.
2. <Imperative verb> <object>.
3. <Imperative verb> <object>.

## Test plan
1. <Imperative verb> <object> to <purpose>.
2. <Imperative verb> <object>.

## Notes
<Optional context sentence before the action, if the reviewer needs it.>
```

Worked example (STE):

```
## Summary
Add the linter to the pre-commit hook.

## Changes
1. Create a new feature branch from the `main` branch.
2. Make your code changes on the feature branch.
3. Commit your changes with a descriptive message.
4. Push the branch to the remote repository.
5. Open a pull request against `main`.

## Test plan
1. Run the linter before you submit the pull request.
2. Squash your commits into a single change.
```

Non-STE (one 40-word sentence joined by "and"): "Create a new feature branch
from the main branch and make your code changes on that branch and then commit
your changes with a descriptive message and push the branch to the remote
repository and open a pull request against the main branch." — the reader
cannot complete one step before reading the next.

---

## Template 9 — Object-oriented inheritance docstring (Rule 9.4)

When you document a class hierarchy, use the same phrasing for overridden
methods. The base-class docstring sets the template; each subclass reuses it and
adds only the subclass-specific behavior.

```
class <Base>:
    """<Template sentence for the method.>"""

class <Sub>(<Base>):
    """<Same template sentence.> <Subclass-specific behavior.>"""
```

Worked example (STE):

```python
class Connection:
    """Establish a connection to the remote host."""

class TlsConnection(Connection):
    """Establish a connection to the remote host. Use TLS for transport."""
```

Non-STE: base says "Connects to server," subclass says "Opens a socket to the
backend," grandchild says "Initiates TCP handshake with data node" — three
templates for one operation.

---

## Sentence-construction fallback (Rule 9.1)

When a word is not approved and a word-for-word swap is not enough, restructure
the sentence — do not keep the unapproved word. Common approved swaps:

| Do not write        | Write             | Why |
|---------------------|-------------------|-----|
| execute the script  | run the script    | "run" is the approved verb |
| generate the artifact | make the artifact | "make" is approved |
| utilize / leverage  | use               | inflated verb |
| bootstrap / initiate | start            | "start" is approved |
| retrieve / fetch    | get               | "get" is approved |
| transmit            | send              | "send" is approved |
| validate / verify   | check             | "check" is approved |
| unable to           | cannot            | "cannot" is approved |
| acceptable          | permitted         | approved adjective |
| visible             | you can see       | verb replaces adjective |

If the part of speech differs or the meaning would change, write a new sentence
with a different structure that keeps the same technical meaning.

## Reviewer checklist (apply to any genre above)

1. One term per concept (lexical consistency).
2. One verb per action, reused everywhere (lexical + syntactic consistency).
3. Same sentence structure for the same step type (syntactic consistency).
4. Same meaning for the same term across files (semantic consistency).
5. One sentence per step; no semicolons (Rule 8.1).
6. Signature name == docstring name == prose name (Rule 9.4).
7. Safety / error text starts with a command or condition and is identical
   wherever the same code appears (Rules 7.2, 9.4).
8. Only approved words, code-domain technical nouns, or code-domain technical
   verbs (Section 1 gates).
