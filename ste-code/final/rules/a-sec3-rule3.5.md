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

### Why the progressive verb form is not approved

Rule 3.2 lists the only permitted verb forms and tenses: the infinitive, the imperative, the simple present, the simple past, the simple future, and the past participle as an adjective. The present progressive (for example, "is running", "are deploying", "was processing") is not on that list. Because the "-ing" form appears inside the progressive tense, you must not use it to describe an action. Replace the progressive with the simple present or simple past, and break a long continuous clause into short separate sentences.

The "-ing" form also tends to hide complex verb constructions with auxiliary verbs, which Rule 3.4 forbids. A clause such as "the service is starting and then it is logging the request" stacks two progressive auxiliaries and is not approved; write "The service starts. Then it logs the request" instead.

### Approved "-ing" technical nouns (section and document titles)

Use the "-ing" form as a section heading or document title when it names a process, service, or procedure. These are technical nouns, not verbs:

- Logging
- Monitoring
- Testing and Fault Isolation
- Handling
- Packaging
- Shipping
- Troubleshooting
- Building
- Deployment

### Approved "-ing" modifiers (technical-noun adjectives)

Use the "-ing" form as an adjective that names the function of a component, service, tool, or layer. These modifiers stay inside the technical noun they describe:

- logging service
- monitoring agent
- routing table
- switching relay
- caching layer
- building pipeline
- binding configuration
- streaming endpoint
- rendering engine

Do not pull the "-ing" word out of the technical noun and use it as a verb. "The caching layer stores the result" is approved; "The layer is caching the result" is not.

## Examples

> *Adapted from spec pair:* Non-STE: "When you are doing this procedure, obey all the safety precautions."  |  STE: "When you do this procedure, obey all the safety precautions."

> **Non-STE:** When you are running this script, obey all the safety checks.
>
> **STE:** When you run this script, obey all the safety checks.
>
> *Adapted from spec pair: the present progressive "are running" is not approved. Use the simple present tense.*

> **Non-STE:** While the deployment is starting, you must watch the logs and you must not stop the process because stopping it during startup can corrupt the state file.
>
> **STE:** The deployment starts. While it starts, watch the logs. Do not stop the deployment. If you stop the deployment during startup, the state file can become corrupt.
>
> *Adapted from spec pair: the present progressive "is starting" is not approved; the "-ing" verb "stopping" in a dependent clause is not approved. Use the simple present and short separate sentences.*

> **Non-STE:** A script opening a socket without checking the firewall rules and sending data to an unknown host, using an unverified certificate without reading the security policy, is in danger of causing a breach and thus exposing private keys and credentials.
>
> **STE:** Before you open a socket, obey these precautions: (1) Read the security policy. (2) Make sure that the firewall rules allow the connection. (3) Verify the host certificate. (4) Get the correct credentials to send data to the host. If you do not obey these precautions, a breach of private keys and credentials can occur.
>
> *Adapted from spec pair: the long "-ing" construction becomes a vertical list of short, clear sentences.*

> **Non-STE:** The background worker is processing the queue and it is writing the results to the cache while the main thread is waiting for the response, causing the request to time out and the user to see an error.
>
> **STE:** The background worker processes the queue. It writes the results to the cache. The main thread waits for the response. If the main thread waits too long, the request times out and the user sees an error.
>
> *Adapted from spec pair: three progressive verbs ("is processing", "is writing", "is waiting") and a trailing "-ing" cause clause are not approved. Use the simple present and separate the steps into short sentences.*

> **Non-STE:** Developers committing code without running the test suite and pushing directly to the main branch, ignoring the review policy, risk breaking the build and therefore blocking the release for all team members.
>
> **STE:** Before you commit code, obey these precautions: (1) Run the test suite. (2) Make sure that the tests pass. (3) Open a review before you merge to the main branch. If you do not obey these precautions, you can break the build and block the release for all team members.
>
> *Adapted from spec pair: the long "-ing" subject ("Developers committing... and pushing... ignoring...") becomes a vertical list of short, clear steps.*

> **Non-STE:** Be careful while the process is starting.
>
> **STE:** Be careful while the process starts.
>
> *Adapted from spec pair: "Be careful while the door is opening." The progressive form "is starting" is not approved.*

> **Non-STE:** The function is returning the value while the cache is loading the entry, which makes the result incorrect during the first request.
>
> **STE:** The function returns the value. The cache loads the entry. During the first request, the result is incorrect.
>
> *Adapted from spec pair: the progressive verbs "is returning" and "is loading" and the "-ing" cause clause "which makes" are not approved. Use the simple present and short separate sentences.*

> **STE:** Logging, Testing and Fault Isolation, Handling, Package, Shipping, Troubleshooting
>
> *Adapted from spec pair: approved "-ing" technical nouns used as procedural titles or headings.*

> **STE:** Logging service, monitoring agent, routing table, switching relay, caching layer
>
> *Adapted from spec pair: the "-ing" form used as a modifier in a technical noun (related to the function of a component or service).*

> **Non-STE:** The matching algorithm is comparing the remaining items during the iteration and it is removing the missing records from the list.
>
> **STE:** The matching algorithm compares the remaining items during the iteration. It removes the missing records from the list.
>
> *Adapted from spec pair: the approved adjectives "matching", "remaining", and "missing" are permitted inside technical nouns, but the progressive verbs "is comparing" and "is removing" are not. Use the simple present.*

> **Non-STE:** Something going wrong during the migration can make the database stay in a broken state.
>
> **STE:** If something goes wrong during the migration, the database can stay in a broken state.
>
> *Adapted from spec pair: the pronoun "something" is an approved "-ing" word but the gerund "going" used as a verb is not approved. Use the simple present "goes".*

> **See also:** Rule 3.2 — Use only these verb forms and tenses of verbs. (The present progressive tense is not approved, which is why the "-ing" verb form is excluded.)
>
> **See also:** Rule 3.4 — Do not use auxiliary verbs to make complex verb constructions. (Progressive "-ing" forms usually hide auxiliary-verb constructions that Rule 3.4 forbids.)
>
> **See also:** Rule 1.5 — You can use words that you can include in a technical noun category. (The "-ing" modifier and technical noun uses in this rule depend on the technical-noun categories.)
