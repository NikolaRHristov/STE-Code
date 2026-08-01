# Level 5 — Section 2: Technical Nouns (Rules 2.1–2.3)

Source: ASD-STE100 Issue 9, Section 2, adapted for code documentation.
Scope: how to write technical nouns — module names, class names, config keys,
endpoint paths, error types, test fixtures — in API docs, READMEs, commit
messages, runbooks, and code comments.

Section rule set:

| Rule | Title | One-line intent |
|---|---|---|
| 2.1 | Keep technical nouns short | Split noun chains with prepositions (`of`, `on`, `in`, `for`). |
| 2.2 | Write long technical nouns in full | More than three words: write in full on first use, then use a short form or approved abbreviation. |
| 2.3 | Use hyphens between words used as one unit | Hyphenate a related pair; never chain more than three words. |

Shared constraints for the whole section:

- A noun phrase is at most three words. A hyphenated unit counts as one word.
- Use approved verbs: `set`, `get`, `make`, `show`, `check`, `remove`, `send`,
  `start`, `stop`, `use`, `update`. Do not use `configure` for `set`,
  `retrieve` for `get`, `delete`/`purge` for `remove`, `display` for `show`.
- Use short, plain words. Not `utilize`, `leverage`, `employ` — use `use`.
  Not `commence`, `initiate`, `terminate` — use `start` and `stop`.
- Approved code-domain adjectives stay attached to the short noun they modify:
  `idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`,
  `stateless`, `backward-compatible`, `asynchronous`, `concurrent`,
  `deterministic`.

---

## Rule 2.1 — Keep Technical Nouns Short

> Source: ASD-STE100 Issue 9, Rule 2.1 · Group 005-rules-sec-2 · Alphabetical key 2

### Rule

To keep multi-word technical nouns short, use prepositions (`of`, `on`, `in`,
`for`) and explain the multi-word technical noun. When a phrase names a code
component with more than a few words, break the phrase into small nouns that
connect with prepositions. Do not write one long noun that stacks modifiers.

### Why it matters in code documentation

- A stacked noun such as `authentication_token_expiration_refresh_interval_setting`
  hides which part owns which. Short nouns with prepositions show the tree.
- Short technical nouns match how code is already structured: a config key, a
  class, or a JSON field is one short concept.
- Long merged nouns are hard to grep, hard to scan, and easy to parse wrongly.

### Procedure

1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at the ownership or containment points.
3. Connect the parts with `of`, `on`, `in`, or `for`.
4. If a part is itself a code component, name it with its short technical noun
   (its class, key, or file), not a merged word.
5. In instruction text, use the approved verbs.

### Examples

#### Configuration key — auth token refresh

> **Non-STE:** Authentication token expiration refresh interval setting
>
> **STE:** Setting of the refresh interval of the expiration of the authentication token

```yaml
# STE-Code: short keys, one concept per level
auth:
  token:
    expiration:
      refresh_interval_seconds: 300

# Non-STE: one long key hides the relationship (do not write this)
authentication_token_expiration_refresh_interval_setting: 300
```

```python
def get_refresh_interval(token):
    """Return the setting of the refresh interval of the expiration of the authentication token."""
    return token.expiration.refresh_interval_seconds
```

#### Deployment labels — middleware config

> **Non-STE:** Install the forward service request validator middleware config tags.
>
> **STE:** Install the config tags on the validator middleware of the request of the forward service.

```bash
kubectl label pods \
  -l app=forward-service \
  middleware=validator \
  config=enabled
```

#### Cleanup task — migration lock files

> **Non-STE:** Remove the database migration script output directory lock files.
>
> **STE:** Remove the lock files that lock the output directory of the migration script of the database.

Use the approved verb `remove`, not `delete` or `purge`.

```python
from pathlib import Path

def remove_migration_lock_files(db_name: str) -> int:
    """Remove the lock files that lock the output directory of the migration script of the database."""
    output_dir = Path("migrations") / db_name / "output"
    removed = 0
    for lock in output_dir.glob("*.lock"):
        lock.unlink()
        removed += 1
    return removed
```

```python
def test_remove_migration_lock_files(tmp_path):
    out = tmp_path / "app" / "output"
    out.mkdir(parents=True)
    (out / "write.lock").write_text("")
    count = remove_migration_lock_files("app")
    assert count == 1
    assert not any(out.glob("*.lock"))
```

#### Test setup — cache hook alignment

> **Non-STE:** Adjust to obtain cache invalidation hook alignment with the event emitter.
>
> **STE:** Adjust the cache invalidation hook until it aligns with the event emitter.

```python
import time

def align_cache_hook(hook, emitter, timeout: float = 5.0) -> bool:
    """Adjust the cache invalidation hook until it aligns with the event emitter."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if hook.target is emitter:
            return True
        hook.nudge()
    return False
```

#### API documentation — retry policy

> **Non-STE:** Payment gateway timeout retry exhaustion notification handler.
>
> **STE:** Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway.

```python
class PaymentGatewayTimeoutRetryExhaustionNotificationHandler:
    """Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway."""

    def handle(self, notice) -> None:
        log.error("retry of the timeout of the payment gateway is exhausted")
```

#### Commit message — schema change

> **Non-STE:** User account profile avatar image storage bucket policy update.
>
> **STE:** Update the policy of the storage bucket of the image of the avatar of the profile of the user account.

#### README section — rate limit

> **Non-STE:** The inbound request rate limit window reset schedule controls the burst.
>
> **STE:** The schedule of the reset of the window of the rate limit of the inbound request controls the burst.

#### Code comment — background job

> **Non-STE:** The background worker queue overflow alert suppression rule runs on the staging cluster.
>
> **STE:** The alert suppression rule on the overflow of the background worker queue runs on the staging cluster.

```python
def install_alert_rule(cluster: str) -> None:
    rule = AlertSuppressionRule(on=OverflowOf(WorkerQueue(background=True)))
    deploy(rule, cluster="staging")
```

### See also

- Rule 2.2 — write a long noun in full, then shorten it.
- Rule 2.3 — hyphenate a related pair, but do not chain more than three words.
- Rule 1.5 — what counts as a technical noun in code documentation.
- Rule 1.3 — use approved words with their approved meanings.

---

## Rule 2.2 — Write Long Technical Nouns in Full

> Source: ASD-STE100 Issue 9, Rule 2.2

### Rule

When a technical code noun has more than three words, write it in full. Then use
one of these methods to make it clear:

- Give a shorter form of the technical code noun.
- Use hyphens (`-`) between words that you use as one unit (see Rule 2.3).
- Use prepositions (`of`, `on`, `in`, `for`, `to`) to split the long noun into
  short parts (see Rule 2.1).

A long multi-word code noun can be one long technical noun or a combination of
shorter ones. Often you cannot divide it, because it is the approved term of
your company, framework, or subject field. In that case, write it as it is, in
its approved form.

### Method 1 — Shorter form of technical code nouns

If a long technical code noun comes from an official code document (an API
specification, a schema, an OpenAPI file, or an architecture diagram), write it
in full the first time it occurs. Explain it if possible, then use a shorter
form or an approved abbreviation in the rest of the document.

> **STE:** Before you do this procedure, initialize the user session cache
> invalidation lock handler (the handler that locks the cache of the user
> session, referred to in this procedure as the "invalidation lock handler").

The short form "invalidation lock handler" has three words and obeys Rule 2.1.

```python
def initialize_session_lock(user_id: str) -> None:
    """Initialize the user session cache invalidation lock handler.

    The invalidation lock handler locks the cache of the user session so that
    a background job cannot read stale data while a write is in flight.
    """
    handler = UserSessionCacheInvalidationLockHandler(user_id)
    handler.engage()   # from here, the "invalidation lock handler"
```

Abbreviations defined on first use work the same way:

> **STE:** The Main Form Validation Module (MFVM) is a TypeScript module that
> includes a Main Export Controller Unit (MECU) and a Data Bridge (DB). The
> MFVM operates in the form submission system. Its function is to validate and
> submit the form data from the Main Form Provider (MFP) to the data stores and
> the validation hooks. The Dynamic Config Unit (DECU) sends events to operate
> the MFVM.

```typescript
// Abbreviation defined on first use, then reused
interface FormPayload { fields: Record<string, unknown>; }

class MainFormValidationModule {       // MFVM
  constructor(
    private readonly exportController: MainExportControllerUnit,  // MECU
    private readonly bridge: DataBridge,                          // DB
    private readonly config: DynamicConfigUnit,                   // DECU
  ) {}

  submit(payload: FormPayload): void {
    this.config.onEvent("submit", () => this.exportController.run(payload));
  }
}
```

If an approved technical code noun has three words or fewer, you do not need an
abbreviation. Do not fill a procedure with letter codes.

| Do not write: | WRITE: |
|---|---|
| The primary parts of the controller are: - The DTA (8) - The PVA (15) - The BA (17) - The VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |
| A. Remove the DTA (8) from the VB (20). B. Remove the PVA (15) from its seat. C. Remove the BA (17) from the VB (20). | A. Remove the data transformer assembly (8) from the view body (20). B. Remove the pipeline validator assembly (15) from its seat. C. Remove the buffer assembly (17) from the view body (20). |

```yaml
# STE-Code: name each part in full; do not pack the parts into letter codes
controller:
  data_transformer_assembly:   # (8)  part of the view body
  pipeline_validator_assembly: # (15) sits on its seat
  buffer_assembly:             # (17) part of the view body

# Non-STE (do not write this):
#   parts: [DTA_8, PVA_15, BA_17, VB_20]
```

```python
def disassemble_controller(view_body, validator_seat):
    view_body.remove(data_transformer_assembly)         # (8)
    validator_seat.remove(pipeline_validator_assembly)  # (15)
    view_body.remove(buffer_assembly)                   # (17)
```

### Method 2 — Use prepositions to break up a long noun

When a long technical code noun is a chain of short nouns, make the main noun
the head of the sentence and attach the rest with `of`, `on`, `in`, `for`, or
`to`.

> **Non-STE:** Configure the user authentication token refresh failure retry policy before you deploy the service to production.
>
> **STE:** Set the retry policy for the failure of the refresh of the user authentication token before you deploy the service to production.

> **Non-STE:** Install the background worker queue overflow alert suppression rule on the staging cluster.
>
> **STE:** Install the alert suppression rule on the overflow of the background worker queue on the staging cluster.

> **Non-STE:** Remove the database connection pool exhaustion recovery timeout configuration parameter from the settings file.
>
> **STE:** Remove the configuration parameter that sets the recovery timeout for the exhaustion of the database connection pool from the settings file.

> **Non-STE:** Update the build script to obtain output directory naming consistency with the package convention.
>
> **STE:** Update the build script until the output directory naming is consistent with the package convention.

```python
def set_recovery_timeout(pool, seconds: float) -> None:
    """Set the configuration parameter that sets the recovery timeout
    for the exhaustion of the database connection pool."""
    pool.config["recovery_timeout_seconds"] = seconds
```

### Method 3 — Hyphenate words that you use as one unit

When two or more words act as a single modifier before a noun, hyphenate them:
`request-response`, `read-write`, `build-time`, `out-of-band`, `end-to-end`,
`run-time`. Do not hyphenate when the first word is an adverb ending in `-ly`
("a publicly documented API" stays open).

> **Non-STE:** Set the request response mapping handler to the new schema before the migration.
>
> **STE:** Set the request-response mapping handler to the new schema before the migration.

> **Non-STE:** Run the build time configuration check after you compile the module.
>
> **STE:** Run the build-time configuration check after you compile the module.

> **Non-STE:** Add an end to end test for the payment flow before you merge the change.
>
> **STE:** Add an end-to-end test for the payment flow before you merge the change.

> **Non-STE:** Use the out of band signal to stop the long running job.
>
> **STE:** Use the out-of-band signal to stop the long-running job.

```python
def handle_request_response(handler: "RequestResponseMappingHandler") -> None:
    """Set the request-response mapping handler to the new schema."""
    handler.apply(schema=SCHEMA_V2)

def run_build_time_check() -> None:
    """Run the build-time configuration check after you compile the module."""
    ...
```

Note: hyphenation groups words into one unit but does not make a long technical
noun short. If the hyphenated unit still has more than three words, write it in
full the first time, then use the shorter form.

### Expanded documentation pairs

> **Non-STE:** The USCIlh must run before the shutdown hook releases the cache. If the USCIlh fails, the stale session remains.
>
> **STE:** Initialize the user session cache invalidation lock handler (the handler that locks the cache of the user session; in this procedure, the "invalidation lock handler"). Run the invalidation lock handler before the shutdown hook releases the cache. If the invalidation lock handler fails, the stale session remains.

```python
class UserSessionCacheInvalidationLockHandler:
    def engage(self) -> None: ...
    def release(self) -> None: ...

def shutdown_hook(session_id: str) -> None:
    handler = UserSessionCacheInvalidationLockHandler(session_id)
    handler.engage()          # invalidation lock handler
    if not handler.release():
        raise StaleSessionError(session_id)
```

> **Non-STE:** The MFVM uses the MECU and the DB. The DECU sends events to the MFVM so that the MFVM can get data from the MFP.
>
> **STE:** The Main Form Validation Module (MFVM) is a TypeScript module that includes a Main Export Controller Unit (MECU) and a Data Bridge (DB). The Dynamic Config Unit (DECU) sends events to operate the MFVM, and the MFVM gets form data from the Main Form Provider (MFP).

```typescript
const mfvm = new MainFormValidationModule(     // MFVM
  mecu,  // Main Export Controller Unit
  db,    // Data Bridge
  decu,  // Dynamic Config Unit
);
decu.onEvent("submit", () => mfvm.submit(mfp.getData()));  // MFP = Main Form Provider
```

> **Non-STE:** Call the DTA to configure the MFVM before you run the build, then check the MFVM output for errors.
>
> **STE:** Use the data transformer adapter to set up the main form validation module before you run the build. Then check the output of the main form validation module for errors.

```bash
make configure MODULE=data-transformer-adapter   # data transformer adapter
make build MODULE=main-form-validation-module    # main form validation module
make test   MODULE=main-form-validation-module && echo "output checked for errors"
```

> **Non-STE:** Update the cross service request tracing correlation identifier generator after the schema change.
>
> **STE:** Update the correlation identifier generator for the tracing of the request across services after the schema change. (On first use, write "cross-service request tracing correlation identifier generator" in full, then use "correlation identifier generator.")

```python
def update_correlation_generator(schema: dict) -> None:
    """Update the cross-service request tracing correlation identifier generator.

    After the first use, this component is the correlation identifier generator.
    """
    CorrelationIdentifierGenerator.for_request_tracing().apply(schema)
```

> **Non-STE:** The CI pipeline docker image layer cache warming step now runs in parallel.
>
> **STE:** The cache warming step for the layer of the Docker image of the CI pipeline now runs in parallel. (On first use, write the full name, then use "cache warming step.")

```yaml
jobs:
  warm_cache:   # cache warming step for the layer of the Docker image of the CI pipeline
    runs-on: ubuntu-latest
    strategy:
      matrix:
        layer: [base, deps, build]
    steps:
      - run: ./scripts/warm-cache.sh "${{ matrix.layer }}"
```

> **Non-STE:** Document the legacy database migration rollback failure notification webhook endpoint in the runbook.
>
> **STE:** Document the webhook endpoint for the notification of the failure of the rollback of the legacy database migration in the runbook. (On first use, write the full name, then use "notification webhook endpoint.")

### Procedure

1. Find the long technical code noun (more than three words) in your sentence.
2. Write it in full the first time it occurs. If it comes from an official
   source (API spec, schema, architecture diagram), keep the approved form.
3. Give a shorter form or an approved abbreviation right after the full form,
   in parentheses.
4. In the rest of the document, use only the shorter form or the abbreviation.
5. If the noun is a chain of short nouns, split it with prepositions (Rule 2.1).
6. If two or more words act as one modifier, hyphenate them (Rule 2.3).
7. Do not fill a procedure with abbreviations. A short, clear noun is better
   than a string of letters.

### See also

- Rule 2.1 — keep technical nouns to three words or fewer.
- Rule 2.3 — hyphens between words used as one unit.
- Rule 1.5 — technical noun categories and your company glossary.
- Rule 1.3 — approved words: use, set, get, make, show, check, remove, send, start, stop.

---
