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

## Examples

> **Non-STE:** When you are running this script, obey all the safety checks.
>
> **STE:** When you run this script, obey all the safety checks.
>
> *Adapted from spec pair: present progressive "are running" is not approved. Use the simple present tense.*

> **Non-STE:** A script opening a socket without checking the firewall rules and sending data to an unknown host, using an unverified certificate without reading the security policy, is in danger of causing a breach and thus exposing private keys and credentials.
>
> **STE:** Before you open a socket, obey these precautions: (1) Read the security policy. (2) Make sure that the firewall rules allow the connection. (3) Verify the host certificate. (4) Get the correct credentials to send data to the host. If you do not obey these precautions, a breach of private keys and credentials can occur.
>
> *Adapted from spec pair: the long "-ing" construction becomes a vertical list of short, clear sentences.*

> **STE:** Logging, Testing and Fault Isolation, Handling, Package, Shipping, Troubleshooting
>
> *Adapted from spec pair: approved "-ing" technical nouns used as procedural titles or headings.*

> **STE:** Logging service, monitoring agent, routing table, switching relay, caching layer
>
> *Adapted from spec pair: the "-ing" form used as a modifier in a technical noun (related to the function of a component or service).*

> **Non-STE:** Be careful while the process is starting.
>
> **STE:** Be careful while the process starts.
>
> *Adapted from spec pair: "Be careful while the door is opening." The progressive form "is starting" is not approved.*
