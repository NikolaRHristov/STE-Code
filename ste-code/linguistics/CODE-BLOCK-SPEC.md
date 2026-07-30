# Code Block Anatomy — Specification

> **Version:** FLAVOR-1.0.0
> **Workflow:** 18 (Code Block Anatomy)
> **Status:** Specification complete. Structural checker pending.

---

## The Five-Element Contract

Every code block in STE-Code documentation must satisfy five structural rules.
This is the most-copied, least-checked content in documentation.

### 1. Prompt Marker

| Context | Marker | Example |
|---------|--------|---------|
| Shell command | `$` | `$ npm install` |
| Language code | none | `const x = 1;` |
| REPL session | `>>>` | `>>> print("hello")` |
| SQL | none or `>` | `SELECT * FROM users;` |
| Dockerfile / config | none | `FROM node:18` |

**Rule:** One marker convention per document. Don't mix `$` and `>` in the same file.

### 2. Placeholder Form

Placeholders must use `<UPPER_SNAKE_CASE>` and be defined in surrounding prose.

```
# Correct
$ curl -H "Authorization: Bearer <API_TOKEN>" https://api.example.com/users
(The <API_TOKEN> is from the dashboard at Settings → API Keys.)

# Violation
$ curl -H "Authorization: Bearer abc123xyz" https://api.example.com/users
(abc123xyz looks real — a reader will paste it verbatim.)
```

**Rule:** Placeholders that look like real values (`abc123`, `mytoken`, `example-key`) are violations.

### 3. Output Elision

Truncated output uses `...` on its own line. Never invent plausible output.

```
# Correct
$ npm test
...
Tests: 42 passed, 0 failed

# Violation
$ npm test
Running test suite...
Test 1: PASS
Test 2: PASS
(Invented output — reader cannot distinguish from real.)
```

**Rule:** `...` must appear alone on a line. It must be the only content on that line except for a preceding prompt marker.

### 4. Expected Output Separation

If output is shown, it goes in a separate block introduced by `Output:`.

```
# Correct
$ curl https://api.example.com/health
Output:
{"status": "ok", "uptime": 12345}

# Violation
$ curl https://api.example.com/health
{"status": "ok", "uptime": 12345}
(Reader may copy-paste the output as the next command.)
```

**Rule:** Command and output must be in separate blocks. Copy-paste of entire block must not execute output as command.

### 5. Idempotency and Danger Marking

Destructive or irreversible commands carry an inline warning.

```
# Correct
$ rm -rf ./build  # WARNING: Deletes all build artifacts. Run `make build` to regenerate.
$ kubectl delete pod <POD_NAME>  # CAUTION: The pod is not recreated automatically.

# Violation
$ rm -rf ./build
(No warning — reader may not understand the command is destructive.)
```

**Rule:** Any command that deletes, overwrites, drops, or irreversibly modifies must carry `# WARNING:` or `# CAUTION:` on the same line, or be preceded by a Warning block.

---

## Copy-Paste Integrity Rule

The entire block, minus prompt markers and elisions, must be executable as-is after placeholder substitution.

```
Test: Can a reader copy-paste the entire block and run it?
If no → violation. Fix: add missing flags, clarify placeholders, separate output.
```

---

## Registration with the Linguistic Layer

Code blocks inherit the register of their enclosing section:
- Tutorial code blocks → `tutorial-step` register
- API reference code blocks → `api-description` register
- README code blocks → `readme-prose` register
- Error message code blocks → `error-message` register

Register affects sentence-length rules for prose surrounding the code block,
not the block content itself.

---

## Structural Checker (to implement)

```
For each code block in a document:
1. Identify language via fence marker (```python, ```bash, ```sql).
2. Classify block type: command, code, config, output, REPL.
3. Apply element checks per type.
4. Validate placeholder format and provenance.
5. Flag missing danger markers.
6. Test copy-paste integrity (structural only — execution is Workflow 18 tier 2).
```
