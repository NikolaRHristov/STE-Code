# Rule 3.5 — Use the "-ing" Form of a Verb Only as a Technical Noun or as a Modifier in a Technical Noun

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.5

## Original Rule

Use the "-ing" form of a verb only as a technical noun or as a modifier in a technical noun.

In English, words that have an "-ing" form can have different functions in a sentence (different parts of speech).

General examples:

Words that have an "-ing" form can be part of a verb to describe an action in the present.

Be careful while the door is opening.

They can also be adjectives.

An opening door can be dangerous.

They can be nouns or parts of noun phrases.

Opening a door can be dangerous.

They can make long groups of modifiers, noun phrases, and dependent clauses.

A mechanic opening a door without obeying the specified safety precautions can easily cause injury to persons standing near the door.

These different functions for words that have an "-ing" form can frequently cause ambiguity or long, complex sentences. Thus, words that have an "-ing" form are usually not permitted.

Examples:

> **Non-STE:** When you are doing this procedure, obey all the safety precautions.
> **STE:** When you do this procedure, obey all the safety precautions.

> **Non-STE:** [fragment] inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems.
> **STE:** Before you use dangerous materials, obey these precautions:
>
> 1. Read the manufacturer's instructions.
> 2. Make sure that there is sufficient airflow in the work area.
> 3. Put on a face mask and protective clothing.
> 4. Get the correct tools to open the containers for these materials.
>
> If you do not obey these precautions, injury to your skin and your lungs can occur.

Words that have an "-ing" form and are technical nouns or parts of technical nouns

You can use a word that has an "-ing" form as a technical noun (for example, in procedural titles or headings).

Examples:

Cleaning, Testing and Fault Isolation, Handling, Packaging, Shipping, Troubleshooting

You can also use the "-ing" form of a verb as a modifier in a technical noun. This modifier is an adjective that is related to the function of a system, component, part, tool, material, or equipment.

Examples:

Air-conditioning system, degreasing agent, grinding wheel, polishing disc, sanding machine, switching relay, welding torch

Approved words that have an "-ing" form

Only a small number of approved words in the dictionary have an "-ing" form. They are:

- Nouns (lighting, opening, routing, and servicing)
- Adjectives (mating, missing, and remaining)
- A pronoun (something)
- A preposition (during).

## STE-Code Adaptation

In code documentation, words with an "-ing" form cause ambiguity when they are used as part of a compound verb tense (present progressive, past progressive). STE-Code prohibits the "-ing" form in verb constructions.

The "-ing" form is permitted in only two contexts:

1. As a technical noun — used in section titles, headings, or the name of a code process:
   Building, Testing, Deploying, Logging, Parsing, Routing, Serializing

2. As a modifier in a technical noun — used to describe the function of a system, module, tool, or service:
   building system, testing framework, routing module, logging service, parsing library, scheduling middleware, rate-limiting gateway

Do not use the "-ing" form as part of a compound verb. Convert the sentence to a simple tense instead. If the "-ing" form appears in a long, complex sentence with multiple modifiers, break the sentence into a vertical list of clear instructions.

### Examples

> **Non-STE:** When you are running the build command, check the terminal for errors.
> **STE:** When you run the build command, check the terminal for errors.
>
> *Adapted from spec pair: "When you are doing this procedure, obey all the safety precautions." / "When you do this procedure, obey all the safety precautions."*

> **Non-STE:** Developers writing code without following the style guide can cause formatting conflicts and merge issues.
> **STE:** Obey the style guide when you write code. If you do not obey the style guide, formatting conflicts and merge issues can occur.
>
> *Adapted from spec pair: "[fragment] inappropriate tools without observing the manufacturer's instructions, are in danger of coming into contact with these materials and thus suffering from skin irritation and breathing problems." / "Before you use dangerous materials, obey these precautions: ... If you do not obey these precautions, injury to your skin and your lungs can occur."*

> **Non-STE:** The script is processing all the input files while logging the results to the console.
> **STE:** The script processes all the input files. Then it writes the results to the console.
>
> *Additional code-domain example — no direct spec pair*
