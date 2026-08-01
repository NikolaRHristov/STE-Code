# Rule 2.1 — Keep Technical Nouns Short

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.1
> **Spec reference:** [master.md#sec2-rule2.1](ste-code/grouped/) (pages 60–63 of 434)
> **Domain:** Code documentation — API docs, commit messages, README sections, code comments
> **Alphabetical key:** 2 · **Group:** 005-rules-sec-2

## Original Rule

To keep multi-word nouns short, you can use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word nouns.

> The four pairs below are the ASD-STE100 source examples. They show the pattern in the aerospace domain. The STE-Code examples later in this file re-express the same pattern for code documentation. Keep them only as the traceable source; do not copy the aerospace terms into STE-Code guidance.

#### Examples (ASD-STE100 source)

> **Non-STE:** _Runway light connection resistance calibration._ (5 words)
>
> **STE:** Calibration of the resistance of the runway light connection. (1 word, 1 word, and 3 words)
>
> **Non-STE:** _Install the forward turbine overheat thermocouple terminal tags._ (6 words)
>
> **STE:** Install the terminal tags on the forward overheat thermocouple of the turbine. (2 words and 3 words)
>
> **Non-STE:** _Remove the engine transmission housing attachment bolts._ (5 words)
>
> **STE:** Remove the bolts that attach the transmission housing to the engine. (1 word, 1 word, 2 words, and 1 word)
>
> **Non-STE:** _Adjust to obtain door operating rod alignment with the attachment point._ (4 words)
>
> **STE:** Adjust the door operating rod until it aligns with the attachment point. (3 words and 1 word)

## Adapted Rule

To keep multi-word technical nouns short, use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word technical nouns. Write each multi-word technical noun as a short noun that uses prepositions to make the meaning clear. A technical noun that the code domain uses (for example, a module name, a class name, a configuration key, an endpoint path, an error type, or a test fixture) must stay short so that the reader can parse it without effort.

When a phrase names a code component with more than a few words, break the phrase into small nouns that connect with prepositions. Do not write one long noun that stacks modifiers. Explain the relationship between the parts with "of," "on," "in," or "for."

Why this matters in code documentation:

- A reader scans docs fast. A stacked noun such as `authentication_token_expiration_refresh_interval_setting` hides which part owns which. A short noun with prepositions shows the tree: the setting belongs to the interval, the interval belongs to the expiration, the expiration belongs to the token.
- Short technical nouns match how code is already structured. A config key, a class, or a JSON field is one short concept. Prepositions in the sentence show how those short concepts relate.
- Follow the Microsoft and Google style guides: use short, plain words. Do not use `utilize`, `leverage`, or `employ` when `use` is enough. Do not use `commence`, `initiate`, or `terminate` when `start` and `stop` are enough. Keep the verb simple and the noun short.
- Approved code-domain adjectives stay attached to the short noun they modify: `idempotent`, `immutable`, `thread-safe`, `atomic`, `nullable`, `deprecated`, `stateless`, `backward-compatible`, `asynchronous`, `concurrent`, `deterministic`. Write `the idempotent retry policy`, not `idempotentretrypolicy`.

How to apply the rule:

1. Find a noun that stacks two or more modifiers (a "noun chain").
2. Split the chain at the ownership or containment points.
3. Connect the parts with `of`, `on`, `in`, or `for`.
4. If a part is itself a code component, name it with its short technical noun (its class, key, or file), not a merged word.
5. In instruction text, use the approved verbs: `set`, `get`, `make`, `show`, `check`, `remove`, `send`, `start`, `stop`, `use`, `update`. Do not use `configure` for `set`, `retrieve` for `get`, `delete`/`purge` for `remove`, or `display` for `show`.

### Examples in STE-Code

> *Adapted from spec pair:* Non-STE: Runway light connection resistance calibration. | STE: Calibration of the resistance of the runway light connection.

The pairs below re-express the ASD-STE100 pattern for code documentation. Each pair shows a full, runnable situation: a long stacked noun (Non-STE) and the same idea written as short nouns with prepositions (STE), followed by the code, config, API doc, test, or commit message that the documentation describes.

#### 1. Configuration key — auth token refresh

> **Non-STE:** Authentication token expiration refresh interval setting
>
> **STE:** Setting of the refresh interval of the expiration of the authentication token

A doc that names the config as one long chain forces the reader to decode the ownership tree. Write the key as short nested nouns and state the relationship with `of`.

```yaml
# STE-Code: short keys, one concept per level
auth:
  token:
    expiration:
      refresh_interval_seconds: 300   # setting of the refresh interval of the expiration of the authentication token

# Non-STE: one long key hides the relationship (do not write this)
authentication_token_expiration_refresh_interval_setting: 300
```

```python
# STE-Code doc comment
def get_refresh_interval(token):
    """Return the setting of the refresh interval of the expiration of the authentication token."""
    return token.expiration.refresh_interval_seconds
```

#### 2. Deployment labels — middleware config

> **Non-STE:** Install the forward service request validator middleware config tags.
>
> **STE:** Install the config tags on the validator middleware of the request of the forward service.

A setup guide that stacks the component path into one noun makes the target unclear. Name the target with prepositions so the reader knows what the tag goes on.

```bash
# STE-Code: the tag goes on the validator middleware of the request of the forward service
kubectl label pods \
  -l app=forward-service \
  middleware=validator \
  config=enabled
```

```yaml
# Non-STE: one long noun, unclear where the tag applies (do not write this)
install_forward_service_request_validator_middleware_config_tags: true
```

#### 3. Cleanup task — migration lock files

> **Non-STE:** Remove the database migration script output directory lock files.
>
> **STE:** Remove the lock files that lock the output directory of the migration script of the database.

A runbook step that names the file as a chain is hard to search and hard to parse. State the ownership with `of` and use the approved verb `remove` (not `delete` or `purge` in instruction text).

```python
# STE-Code: remove the lock files that lock the output directory
#            of the migration script of the database
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
# Test that checks the cleanup (use `check`, not `verify`)
def test_remove_migration_lock_files(tmp_path):
    out = tmp_path / "app" / "output"
    out.mkdir(parents=True)
    (out / "write.lock").write_text("")
    count = remove_migration_lock_files("app")
    assert count == 1
    assert not any(out.glob("*.lock"))
```

#### 4. Test setup — cache hook alignment

> **Non-STE:** Adjust to obtain cache invalidation hook alignment with the event emitter.
>
> **STE:** Adjust the cache invalidation hook until it aligns with the event emitter.

A test helper that stacks the alignment target is vague. Name the hook, then state what it aligns with.

```python
# STE-Code: adjust the cache invalidation hook until it aligns with the event emitter
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

#### 5. API documentation — retry policy

> **Non-STE:** Payment gateway timeout retry exhaustion notification handler.
>
> **STE:** Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway.

An API doc, error type, or log line that stacks five nouns is hard to grep and hard to read. Split it so each level is a short noun.

```python
# STE-Code: handler of the notification of the exhaustion of the retry
#            of the timeout of the payment gateway
class PaymentGatewayTimeoutRetryExhaustionNotificationHandler:
    """Handler of the notification of the exhaustion of the retry of the timeout of the payment gateway."""

    def handle(self, notice) -> None:
        log.error("retry of the timeout of the payment gateway is exhausted")
```

```text
# Non-STE log line (do not write this)
paymentgatewaytimeoutretryexhaustionnotificationhandler: retry failed
```

#### 6. Commit message — schema change

> **Non-STE:** User account profile avatar image storage bucket policy update.
>
> **STE:** Update of the policy of the storage bucket of the image of the avatar of the profile of the user account.

A commit title that stacks the path is unclear about what changed. Use the approved verb `update` (or `make`/`set`) and show ownership with `of`.

```text
# STE-Code commit title
Update the policy of the storage bucket of the image of the avatar of the profile of the user account

# Non-STE commit title (do not write this)
useraccountprofileavatarimagestoragebucketpolicyupdate
```

#### 7. README section — rate limit

> **Non-STE:** The inbound request rate limit window reset schedule controls the burst.
>
> **STE:** The schedule of the reset of the window of the rate limit of the inbound request controls the burst.

A README sentence that stacks the noun hides what the schedule actually resets. Name the short nouns and connect them with `of`.

```markdown
# STE-Code README

The schedule of the reset of the window of the rate limit of the inbound
request controls the burst. Set the window to 60 seconds.
```

```yaml
# Non-STE: one long key, unclear what resets (do not write this)
inbound_request_rate_limit_window_reset_schedule: "*/1 * * * *"
```

#### 8. Code comment — background job

> **Non-STE:** The background worker queue overflow alert suppression rule runs on the staging cluster.
>
> **STE:** The alert suppression rule on the overflow of the background worker queue runs on the staging cluster.

A code comment that stacks the subject makes the reader re-read. Put the head noun first, then attach the rest with `on` and `of`.

```python
# STE-Code comment: the alert suppression rule on the overflow
# of the background worker queue runs on the staging cluster
def install_alert_rule(cluster: str) -> None:
    rule = AlertSuppressionRule(on=OverflowOf(WorkerQueue(background=True)))
    deploy(rule, cluster="staging")
```

## See also

> **See also:** Rule 1.5 — You Can Use Words That You Can Include in a Code-Domain Technical Noun Category (what counts as a technical noun in code documentation)
> **See also:** Rule 1.3 — Use Approved Words Only with Their Approved Meanings (keep verbs and nouns plain: use, set, get, remove, check, update, show)
> **See also:** Rule 2.2 — Write Long Technical Nouns in Full (when a noun must stay long, write it in full then use a short form)
> **See also:** Rule 2.3 — Use Hyphens Between Words Used as One Unit (hyphenate a related pair, but do not chain more than three words)
