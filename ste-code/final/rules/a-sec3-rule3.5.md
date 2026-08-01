# Rule 3.5 — Use the "-ing" form of a verb only as a technical noun or as a modifier in a technical noun.

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.5

> Source: master.md#sec3-rule3.5

## Original Rule

In English, words that have an "-ing" form can have different functions in a sentence (different parts of speech).

Words that have an "-ing" form can be part of a verb to describe an action in the present.

> **STE:** Be careful while the door is opening.

They can also be adjectives.

> **STE:** An opening door can be dangerous.

They can be nouns or parts of noun phrases.

> **STE:** Opening a door can be dangerous.

They can make long groups of modifiers, noun phrases, and dependent clauses.

> **STE:** A mechanic opening a door without obeying the specified safety precautions can easily cause injury to persons standing near the door.

These different functions for words that have an "-ing" form can frequently cause ambiguity or long, complex sentences. Thus, words that have an "-ing" form are usually not permitted.

> **Non-STE:** When you are doing this procedure, obey all the safety precautions.
>
> **STE:** When you do this procedure, obey all the safety precautions.
>
> **Non-STE:** Mechanics wearing insufficient protective clothing and opening containers containing hazardous materials in areas where there is a lack of ventilation, using inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems.
>
> **STE:** Before you use dangerous materials, obey these precautions: (1) Read the manufacturer's instructions. (2) Make sure that there is sufficient airflow in the work area. (3) Put on a face mask and protective clothing. (4) Get the correct tools to open the containers for these materials. If you do not obey these precautions, injury to your skin and your lungs can occur.

Words that have an "-ing" form and are technical nouns or parts of technical nouns:

You can use a word that has an "-ing" form as a technical noun (for example, in procedural titles or headings).

> **STE:** Cleaning, Testing and Fault Isolation, Handling, Package, Shipping, Troubleshooting

You can also use the "-ing" form of a verb as a modifier in a technical noun. This modifier is an adjective that is related to the function of a system, component, part, tool, material, or equipment.

> **STE:** Air-conditioning system, degreasing agent, grinding wheel, polishing disc, sanding machine, switching relay, welding torch

Approved words that have an "-ing" form:

Only a small number of approved words in the dictionary have an "-ing" form. They are:

- Nouns (lighting, opening, routing, and servicing)
- Adjectives (mating, missing, and remaining)
- A pronoun (something)
- A preposition (during).

## STE-Code Adaptation

In code documentation, words that have an "-ing" form can have different functions in a sentence. They can be part of a verb that describes an action in the present, an adjective, a noun, or a long group of modifiers. These different functions can cause ambiguity or long, complex sentences. Thus, words that have an "-ing" form are usually not permitted as verbs.

Use a word that has an "-ing" form only as a technical noun (for example, in procedural titles or headings) or as a modifier in a technical noun.

Approved words that have an "-ing" form in STE-Code:

- Nouns (logging, monitoring, routing, and servicing)
- Adjectives (matching, missing, and remaining)
- A pronoun (something)
- A preposition (during).

### Two patterns to avoid

1. **The present progressive (is/are/was/were + -ing).**
   Do not write "the test is running," "the service was starting," or "the workers are processing the queue." Use an approved tense instead: the simple present ("the test runs"), the simple past ("the service started"), or the simple future ("the worker will process the queue"). See Rule 3.2.

2. **The stacked "-ing" modifier group.**
   Do not write "a function reading the file, writing the log, and sending the email without checking the return value, using an old certificate without reading the security policy, is in danger of dropping data and thus corrupting the backup." Break the long chain into a list of short, active sentences with one action each. See Rule 3.6.

### How to rewrite an "-ing" construction

- **"is/are + -ing" → simple present or command.**
  "Be careful while the process is starting" becomes "Be careful while the process starts." "Errors are occurring when you run the script" becomes "Errors occur when you run the script."
- **"-ing" used as a noun subject → name the actor and use a verb.**
  "Running the script causes errors" becomes "The script causes errors when you run it." Or "When you run the script, errors can occur."
- **"-ing" clause stacked as a modifier → a numbered list of short steps.**
  Move each action into its own sentence or bullet, and use the approved verbs (run, open, read, check, get, set, send, start, stop, remove). See Rule 1.3.

### When the "-ing" form is correct (not a verb)

Use the "-ing" form only in these two cases, and only with an approved "-ing" word:

- **As a technical noun in a title or heading.**
  "Logging," "Monitoring," "Testing and Fault Isolation," "Handling," "Package," "Shipping," "Troubleshooting." These are section names, not sentences.
- **As a modifier inside a technical noun (an adjective that names a function).**
  "logging service," "monitoring agent," "routing table," "switching relay," "caching layer," "matching record," "missing key," "remaining retry." The "-ing" word attaches to a component or service and tells what that component does.

The approved "-ing" adjectives (matching, missing, remaining) and the approved "-ing" nouns (logging, monitoring, routing, servicing) are the only "-ing" words you may use. Do not add new ones. If you need another word, use a non-"-ing" approved term instead (for example, write "the service that logs requests" rather than inventing "loggingness").

### Why this rule helps code writing

A reader of a README, a runbook, a code comment, or a test name wants a direct statement with one clear actor and one clear action. Present-progressive and stacked "-ing" phrases hide the actor, blur the tense, and make the sentence long. The simple tenses and short sentences are easier to scan, to translate, and to grep. A heading such as "Logging" or a component name such as "routing table" reads fast and maps to a real code object.

## Examples

> *Adapted from spec pair:* Non-STE: When you are doing this procedure, obey all the safety precautions.  |  STE: When you do this procedure, obey all the safety precautions.

> **Non-STE:** When you are running this script, obey all the safety checks.
>
> **STE:** When you run this script, obey all the safety checks.
>
> *Adapted from spec pair: present progressive "are running" is not approved. Use the simple present tense. See Rule 3.2.*

```bash
# Non-STE: "When you are running this script, obey all the safety checks."
# STE: when you run this script, obey all the safety checks.
./run-tests.sh          # when you run this script, obey all the safety checks
#   (1) the test database is clean
#   (2) the API keys are in the environment
#   (3) the network is offline so no request leaves the host
```

```python
# STE-Code doc comment — simple present, not present progressive
def run_tests() -> None:
    """When you run this script, obey all the safety checks:
    clean the test database, set the API keys, and go offline."""
    reset_test_db()
    load_api_keys()
    assert network.is_offline(), "go offline before you run the script"
```

> **Non-STE:** A script opening a socket without checking the firewall rules and sending data to an unknown host, using an unverified certificate without reading the security policy, is in danger of causing a breach and thus exposing private keys and credentials.
>
> **STE:** Before you open a socket, obey these precautions: (1) Read the security policy. (2) Make sure that the firewall rules allow the connection. (3) Verify the host certificate. (4) Get the correct credentials to send data to the host. If you do not obey these precautions, a breach of private keys and credentials can occur.
>
> *Adapted from spec pair: the long "-ing" construction becomes a vertical list of short, clear sentences. See Rule 3.6.*

```python
# Non-STE: a script opening a socket without checking the firewall rules
#          and sending data to an unknown host, using an unverified
#          certificate without reading the security policy, is in danger
#          of causing a breach ...
# STE: before you open a socket, obey these precautions.

def open_socket(host: str, port: int, cert: Cert, creds: Credentials) -> Socket:
    """Before you open a socket, obey these precautions.

    1. Read the security policy.
    2. Make sure that the firewall rules allow the connection.
    3. Verify the host certificate.
    4. Get the correct credentials to send data to the host.

    If you do not obey these precautions, a breach of private keys and
    credentials can occur.
    """
    policy = read_security_policy()          # 1. read the security policy
    if not firewall.allows(host, port):      # 2. check the firewall rules
        raise BlockedConnection(host, port)
    if not cert.verify(host):                 # 3. verify the host certificate
        raise UntrustedCertificate(host)
    creds = get_credentials(host)             # 4. get the correct credentials
    return Socket.connect(host, port, creds)
```

> **STE:** Logging, Testing and Fault Isolation, Handling, Package, Shipping, Troubleshooting
>
> *Adapted from spec pair: approved "-ing" technical nouns used as procedural titles or headings.*

```markdown
# Service Runbook

## Logging
Describe how the service writes logs and where to find them.

## Testing and Fault Isolation
Run the test suite and find the fault when a test fails.

## Handling
Handle the common error types that the API returns.

## Package
Build the package before you ship it.

## Shipping
Ship the package to the registry.

## Troubleshooting
Use this section when the service does not start.
```

```python
# STE-Code: "-ing" words as section names in a docstring, not as verbs
class ReportService:
    """ReportService

    Logging:
        The service writes one log line per request.
    Monitoring:
        The monitoring agent reads the log and raises an alert on error.
    """
```

> **STE:** Logging service, monitoring agent, routing table, switching relay, caching layer
>
> *Adapted from spec pair: the "-ing" form used as a modifier in a technical noun (related to the function of a component or service).*

```python
# STE-Code: "-ing" modifier inside a technical noun — names what the
# component does. These are approved "-ing" words only.
class LoggingService:     # logging service
    """The logging service writes one log line per request."""

class MonitoringAgent:    # monitoring agent
    """The monitoring agent reads the log and raises an alert on error."""

ROUTING_TABLE: dict = {}  # routing table

class SwitchingRelay:     # switching relay
    """The switching relay moves traffic from port A to port B."""

class CachingLayer:       # caching layer
    """The caching layer stores the response so the next read is fast."""
```

```python
# STE-Code: approved "-ing" adjectives attached to a short technical noun
def find_match(records: list[Record], key: str) -> Record | None:
    """Return the matching record, or None if no matching record exists."""
    for record in records:
        if record.key == key:
            return record
    return None

def get_remaining_retries(attempt: int, limit: int) -> int:
    """Return the remaining retries after this attempt."""
    return limit - attempt

def read_config(path: str) -> dict:
    """Stop if the config file is missing; show the missing key."""
    if not file_exists(path):
        raise MissingFile(path)   # "missing" is an approved "-ing" adjective
```

> **Non-STE:** Be careful while the process is starting.
>
> **STE:** Be careful while the process starts.
>
> *Adapted from spec pair: "Be careful while the door is opening." The progressive form "is starting" is not approved. See Rule 3.2.*

```bash
# Non-STE: "Be careful while the process is starting."
# STE: be careful while the process starts.
./start-api.sh
# be careful while the process starts: do not send requests for 5 seconds
sleep 5
curl -f http://localhost:8080/health || echo "api not ready"
```

```go
// Non-STE: "Be careful while the process is starting."
// STE: be careful while the process starts.
func main() {
    srv := NewAPI()      // be careful while the process starts
    go srv.Listen()      // the listener starts in the background
    time.Sleep(5 * time.Second)
    if !srv.Healthy() {  // do not send requests until the process starts
        log.Fatal("api did not start")
    }
}
```

> **Non-STE:** Errors are occurring when the worker is processing the queue, causing the job to fail and dropping the messages that remain.
>
> **STE:** Errors occur when the worker processes the queue. The job fails and the remaining messages drop.
>
> *Adapted from spec principle: replace the present progressive ("are occurring", "is processing") with the simple present, and split the stacked "-ing" chain ("causing ... dropping") into short sentences. "remaining" is an approved "-ing" adjective. See Rule 3.2 and Rule 3.6.*

```python
# Non-STE: errors are occurring when the worker is processing the queue,
#          causing the job to fail and dropping the messages that remain.
# STE: errors occur when the worker processes the queue. The job fails and
#      the remaining messages drop.

def process_queue(worker: Worker, queue: Queue) -> int:
    """Errors occur when the worker processes the queue.

    The job fails and the remaining messages drop. Check the log to find
    the error.
    """
    handled = 0
    remaining = queue.size()     # "remaining" is an approved "-ing" adjective
    while not queue.empty():
        try:
            worker.handle(queue.pop())
            handled += 1
        except WorkerError as err:
            log.error("job failed: %s", err)   # the job fails
            remaining = queue.size()            # the remaining messages drop
            break
    return handled
```

> **Non-STE:** Configuring the routing table before the service starts prevents the requests from going to the wrong host.
>
> **STE:** Configure the routing table before the service starts. Then the requests go to the correct host.
>
> *Adapted from spec principle: a leading "-ing" clause ("Configuring ...") used as a noun subject is not approved; turn it into a command and a separate result sentence. "routing table" is an approved "-ing" technical noun. See Rule 3.6.*

```yaml
# STE-Code: configure the routing table before the service starts
services:
  api:
    depends_on:
      - routing-table        # configure the routing table first
    command: ./start-api.sh  # then the service starts
```

```bash
# Non-STE: "Configuring the routing table before the service starts ..."
# STE: configure the routing table before the service starts.
./configure-routing.sh   # configure the routing table before the service starts
./start-api.sh           # then the requests go to the correct host
```

> **See also:** Rule 3.2 — Use only these verb forms and tenses of verbs
> **See also:** Rule 3.3 — Use the past participle form as an adjective
> **See also:** Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions
> **See also:** Rule 3.6 — Use the Active Voice
> **See also:** Rule 1.1 — Use words that are approved in the dictionary
> **See also:** Rule 1.3 — Use Approved Words (keep verbs plain: run, open, read, check, get, set, send, start, stop, remove)
> **See also:** Rule 1.5 — Technical Noun Categories (what counts as a technical noun in code documentation)
> **See also:** The STE-Code dictionary (a-dictionary.md) — approved "-ing" words: LOGGING, MONITORING, ROUTING, SERVICING (nouns); MATCHING, MISSING, REMAINING (adjectives)
