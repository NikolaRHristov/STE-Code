# Rule 3.7 — Use an approved verb to describe an action, not a noun or other parts of speech.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.7
> **Source file:** master.md#sec3-rule3.7

## Original Rule

There can be different solutions to give the same information in STE. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

> **Non-STE:** Do not write: The ohmmeter gives an indication of 450 ohms.
> **STE:** WRITE: The ohmmeter shows 450 ohms.
> **Non-STE:** Do not write: Before the removal of the unit, make sure that the power supply is OFF.
> **STE:** WRITE: Before you remove the unit, make sure that the power supply is OFF.

In the examples, all sentences are in STE, but those with direct verbs describe the action more clearly.

If a word is not approved as a verb in the dictionary, do not use it as a verb. Use a different sentence construction to give the same information.

> **Non-STE:** Check the laptop battery.
> **STE:** Do a check of the laptop battery.

## STE-Code Adaptation

There can be different solutions to give the same information in STE-Code. If there is an approved verb that describes an action, use the approved verb. Verbs describe actions more clearly than nouns or other parts of speech.

The four approved Technical Code Verb categories give you the verbs that you can use to describe an action:

1. **Development operations** — build, compile, test, lint, format, commit, push, deploy, rollback
2. **Data operations** — read, write, serialize, deserialize, Parse, Encode, Decode, Query, Insert, Migrate
3. **Application operations** — handle, route, authenticate, authorize, validate, schedule, Dispatch, resolve
4. **Communication actions** — send, receive, publish, subscribe, stream, poll, broadcast, connect

If a word is not approved as a verb in the STE-Code dictionary, do not use it as a verb. Use a different sentence construction (usually the noun form of the word) to give the same information.

### Why verbs, not nouns, in code documentation

A noun names a thing; a verb names the work. When you write `validate the token`, the reader knows to run the check. When you write `validation of the token`, the reader must stop and ask: do I run it, log it, or skip it? Prefer the verb. Prefer the plain, approved verb — `use`, `start`, `stop`, `show`, `make`, `get`, `set`, `check`, `do`, `send`, `remove`, `keep` — over wordy substitutes such as *utilize*, *leverage*, *employ*, *commence*, *terminate*, or *initiate* when a simpler verb already does the job.

## Examples

> *Adapted from spec pair:* Non-STE: "The ohmmeter gives an indication of 450 ohms." | STE: "The ohmmeter shows 450 ohms."

---

### Example 1 — Profiler reports latency (development operations)

**Non-STE:**

```
# benchmark_report.py
def report_latency():
    # The profiler gives an indication of 200ms latency.
    return "profiler indicates 200ms"
```

> **Non-STE:** The profiler gives an indication of 200ms latency.

**STE:**

```
# benchmark_report.py
def report_latency():
    # The profiler shows 200ms latency.
    return "profiler shows 200ms"
```

> **STE:** The profiler shows 200ms latency.

*Adapted from spec pair: "The ohmmeter gives an indication of 450 ohms." / "The ohmmeter shows 450 ohms." The approved verb "show" describes the action more clearly than the noun phrase "gives an indication of."*

---

### Example 2 — Service initialization (application actions)

**Non-STE:**

```
# deploy.sh
# Before the initialization of the service, make sure that the config is valid.
cp config.default.yaml config.yaml
```

> **Non-STE:** Before the initialization of the service, make sure that the config is valid.

**STE:**

```
# deploy.sh
# Before you initialize the service, make sure that the config is valid.
./init-service.sh
```

> **STE:** Before you initialize the service, make sure that the config is valid.

*Adapted from spec pair: "Before the removal of the unit, make sure that the power supply is OFF." / "Before you remove the unit, make sure that the power supply is OFF." Use the approved verb "initialize" instead of the noun "initialization."*

---

### Example 3 — Caching a response (data + communication actions)

**Non-STE:**

```
// cache_client.go
func Get(r *http.Request) string {
    // Cache the response.
    return upstream(r)
}
```

> **Non-STE:** Cache the response.

**STE:**

```
// cache_client.go
func Get(r *http.Request) string {
    // Do a cache of the response.
    return cache.Do(upstream(r))
}
```

> **STE:** Do a cache of the response.

*Adapted from spec pair: "Check the laptop battery." / "Do a check of the laptop battery." "Cache" is an approved technical noun (category 1.5) but not an approved verb. Use the noun form "Do a cache" instead of the verb "Cache."*

---

### Example 4 — HTTP status from a function (communication actions)

**Non-STE:**

```
# handler.py
def status() -> str:
    # Do not write: The function gives a result of Put 500 OK.
    return "result 500"
```

> **Non-STE:** The function gives a result of 500 OK.

**STE:**

```
# handler.py
def status() -> str:
    # The function returns 500 OK.
    return "500 OK"
```

> **STE:** The function returns 500 OK.

*Adapted from spec principle: the approved verb "return" describes the action more clearly than the noun phrase "gives a result of."*

---

### Example 5 — Validate input (application actions)

**Non-STE:**

```
// validate.go
// The parser does a verification of the payload.
func Verify(p []byte) error { /* ... */ }
```

> **Non-STE:** The parser does a verification of the payload.

**STE:**

```
// validate.go
// You validate the payload before you store it.
func Validate(p []byte) error { /* ... */ }
```

> **STE:** You validate the payload before you store it.

---

### Example 6 — Read and write config (data actions)

**Non-STE:**

```
# config_io.py
# A read of the config, then a write of the config.
def load(): ...
def store(): ...
```

> **Non-STE:** A read of the config, then a write of the config.

**STE:**

```
# config_io.py
# Read the config, then write the config.
def read(): ...
def write(): ...
```

> **STE:** Read the config, then write the config.

---

### Example 7 — Send and receive messages (communication actions)

**Non-STE:**

```
// bus.go
// A transmission of the event, then a reception of the event.
func Transmit(e Event) { ... }
func Receive(e Event) { ... }
```

> **Non-STE:** A transmission of the event, then a reception of the event.

**STE:**

```
// bus.go
// Send the event, then receive the event.
func Send(e Event) { ... }
func Receive(e Event) { ... }
```

> **STE:** Send the event, then receive the event.

---

> **See also:**
> - Rule 3.2 — Use only these verb forms and tenses of verbs (infinitive, imperative, simple present, simple past, simple future, past participle).
> - Rule 1.5 — Technical noun categories: the noun-form fallback when a word is not an approved verb.
> - Extension approved verbs — use, start, stop, show, make, get, set, check, do, send, remove, keep.
> - Rule 3.3 — related verb and tense guidance in the STE-Code dictionary.
