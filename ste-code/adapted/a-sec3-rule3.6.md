# Rule 3.6 — Use the Active Voice

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.6

## Original Rule

Use the active voice. In descriptive writing, you can use the passive voice only if the agent is unknown.

Technical texts consist of procedural writing and descriptive writing. When you write in STE, always use the active voice. In descriptive writing, the passive voice is permitted only when the agent (the person or thing that does the action) is unknown.

What is active voice?

In the active voice, the subject of the sentence does the action of the sentence ("A" does "B"). Thus, the grammatical subject (A) is also the logical subject (agent).

What is passive voice?

In the passive voice, the subject of the sentence receives the action ("B" is done by "A"). Here, the grammatical subject is B, and the logical subject, or agent, is A.

General examples:

> **Active:** The manufacturer gives the safety procedures.
> **Passive:** The safety procedures are given by the manufacturer.

How do you know if a sentence is in the passive voice?

The best test for the passive voice is to think of the question "by whom or by what?" (the agent). If your text gives you an answer to this question, then the text is in the passive voice. When a sentence contains the preposition "by," it is a good indication that the sentence is in the passive voice. The object of the preposition "by" is then the agent and you can use the agent as the subject of a sentence in the active voice.

But a passive construction does not always contain an agent.

The dimensions are given in the table.

The main gear leg is held in its position.

A sentence in the active voice always has a grammatical subject (the agent), but in the passive sentence in the example below, the agent is unknown (and we do not know the cause of data corruption). In the active sentence, the agent ("transmission") is incorrect ("transmission" is not the cause of data corruption), and the meaning of the sentence is different. Thus, the active sentence becomes technically incorrect.

Example:

> **Passive:** During transmission, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During transmission, something corrupted the data. (Correct, you do not know the identity of "something," but you can use it as the agent.)
> **Active:** Transmission corrupted the data. (Incorrect, "transmission" is not the correct agent.)

In the example, if you use the word "something" ("a thing that is not determined or specified") as the agent, the active voice will be technically correct.

How do you change a sentence that is in the passive voice to the active voice?

To change a sentence from the passive voice to the active voice, you can use one of these four methods:

Method 1

When the sentence gives the agent (usually the object of the preposition "by"), put the agent at the start of the sentence. Then, use the agent as the subject. The subject must always be the noun that does the action in the sentence.

> **Non-STE:** The circuits are connected by a switching relay. (Passive)
> **STE:** A switching relay connects the circuits. (Active)

Method 2

Change an infinitive verb to an active verb.

> **STE:** The computer calculates the energy consumption from these values. (Active)

Method 3

In procedural writing, change the verb to the imperative ("command") form.

Method 4

When the agent (the person or thing that does the action) is not given in the sentence, you can use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your company, or organization, use "we."

Examples:

> **Non-STE:** On the ground, the valve can be opened with the override handle. (Passive)
> **STE:** On the ground, you can open the valve with the override handle. (Active)

When you find complex sentences in the passive voice that include auxiliary verbs, decide if you want to write a procedural sentence or a descriptive sentence.

> **STE:** This type of fuel does not contain additives. (Descriptive sentence)

## STE-Code Adaptation

Use the active voice in all code documentation. In descriptive writing, the passive voice is permitted only when the agent (the person, service, or component that does the action) is unknown.

In the active voice, the subject of the sentence does the action. This makes code documentation clearer because the reader immediately knows who or what performs the operation.

To test if a sentence is in the passive voice, ask "by whom or by what?" (the agent). If the sentence answers this question, it is passive. Convert it to active by using the agent as the subject.

To change a sentence from the passive voice to the active voice, use one of these four methods:

**Method 1:** When the preposition "by" identifies the agent, move the agent to the subject position:

> **Non-STE:** The API response is parsed by the middleware. (Passive)
> **STE:** The middleware parses the API response. (Active)
>
> *Adapted from spec pair: "The circuits are connected by a switching relay." / "A switching relay connects the circuits."*

**Method 2:** Change an infinitive verb to an active verb:

> **STE:** The profiler calculates the memory usage from these values. (Active)
>
> *Adapted from spec pair: "The computer calculates the energy consumption from these values."*

**Method 3:** In procedural writing, change the verb to the imperative ("command") form:

> **Non-STE:** The dependencies can be installed with the following command. (Passive)
> **STE:** Install the dependencies with this command: npm install (Active, imperative)
>
> *Adapted from original Method 3 principle — imperative ("command") form*

**Method 4:** When the agent is not given in the sentence, use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your organization, use "we."

> **Non-STE:** The configuration file can be edited with a text editor. (Passive)
> **STE:** You can edit the configuration file with a text editor. (Active)
>
> *Adapted from spec pair: "On the ground, the valve can be opened with the override handle." / "On the ground, you can open the valve with the override handle."*

When the agent is unknown and you cannot identify it:

> **Passive:** During the network request, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During the network request, something corrupted the data. (Correct, you do not know the identity of "something.")
> **Active:** The network request corrupted the data. (Incorrect, "network request" is not the correct agent.)
>
> *Adapted from spec pair: "During transmission, the data was corrupted." / "During transmission, something corrupted the data." / "Transmission corrupted the data."*

### Examples

> **Non-STE:** The database connection is established by the connection pool at startup.
> **STE:** The connection pool establishes the database connection at startup.
>
> *Adapted from spec pair: "The circuits are connected by a switching relay." / "A switching relay connects the circuits." (Method 1)*

> **Non-STE:** The test results can be viewed in the terminal output.
> **STE:** You can see the test results in the terminal output.
>
> *Adapted from spec pair: "On the ground, the valve can be opened with the override handle." / "On the ground, you can open the valve with the override handle." (Method 4)*
