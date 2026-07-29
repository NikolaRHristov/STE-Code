# Rule 3.6 — Use the Active Voice

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 3.6

## Original Rule

Use the active voice. In descriptive writing, you can use the passive voice only if the agent is unknown.

Technical texts consist of procedural writing and descriptive writing. When you write in STE, always use the active voice. In descriptive writing, the passive voice is permitted only when the agent (the person or thing that does the action) is unknown.

In the active voice, the subject of the sentence does the action of the sentence ("A" does "B"). Thus, the grammatical subject (A) is also the logical subject (agent).

In the passive voice, the subject of the sentence receives the action ("B" is done by "A"). Here, the grammatical subject is B, and the logical subject, or agent, is A.

General examples:

> **Active:** The manufacturer gives the safety procedures.
> **Passive:** The safety procedures are given by the manufacturer.

The best test for the passive voice is to think of the question "by whom or by what?" (the agent). If your text gives you an answer to this question, then the text is in the passive voice.

But a passive construction does not always contain an agent:

> The dimensions are given in the table.
> The main gear leg is held in its position.

When the agent is unknown (and we do not know the cause of data corruption):

> **Passive:** During transmission, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During transmission, something corrupted the data. (Correct, you do not know the identity of "something," but you can use it as the agent.)
> **Active:** Transmission corrupted the data. (Incorrect, "transmission" is not the correct agent.)

To change a sentence from the passive voice to the active voice, you can use one of these four methods:

Method 1: When the sentence gives the agent (usually the object of the preposition "by"), put the agent at the start of the sentence. Then, use the agent as the subject.

> **Non-STE:** The circuits are connected by a switching relay. (Passive)
> **STE:** A switching relay connects the circuits. (Active)

Method 2: Change an infinitive verb to an active verb.

Method 3: In procedural writing, change the verb to the imperative ("command") form.

Method 4: When the agent is not given in the sentence, you can use the pronouns "you" or "we" as subjects in the active form. If the agent is the reader, use "you." If the agent is your company, or organization, use "we."

> **Non-STE:** On the ground, the valve can be opened with the override handle. (Passive)
> **STE:** On the ground, you can open the valve with the override handle. (Active)

## STE-Code Adaptation

Use the active voice in all code documentation. In descriptive writing, the passive voice is permitted only when the agent (the person, service, or component that does the action) is unknown.

In the active voice, the subject of the sentence does the action. This makes code documentation clearer because the reader immediately knows who or what performs the operation.

To test if a sentence is in the passive voice, ask "by whom or by what?" If the sentence answers this question, it is passive. Convert it to active by using the agent as the subject.

Method 1: When the preposition "by" identifies the agent, move the agent to the subject position:

> **Non-STE:** The API response is parsed by the middleware. (Passive)
> **STE:** The middleware parses the API response. (Active)

Method 2: In procedural writing, use the imperative form directly:

> **Non-STE:** The dependencies can be installed with the following command. (Passive)
> **STE:** Install the dependencies with this command: `npm install` (Active, imperative)

Method 3: When the agent is not given, use "you" (for the reader) or "we" (for your organization):

> **Non-STE:** The configuration file can be edited with a text editor. (Passive)
> **STE:** You can edit the configuration file with a text editor. (Active)

Method 4: When the agent is unknown and you cannot identify it, the passive voice is permitted in descriptive writing:

> **Passive:** During the network request, the data was corrupted. (Correct, the agent is unknown.)
> **Active:** During the network request, something corrupted the data. (Correct, you do not know the identity of "something.")
> **Active:** The network request corrupted the data. (Incorrect, "network request" is not the correct agent.)

### Examples

> **Non-STE:** The database connection is established by the connection pool at startup.
> **STE:** The connection pool establishes the database connection at startup.

> **Non-STE:** The test results can be viewed in the terminal output.
> **STE:** You can see the test results in the terminal output.
