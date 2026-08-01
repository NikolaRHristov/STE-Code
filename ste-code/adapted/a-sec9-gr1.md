# GR-1 — The Conjunction "that"

> **Source:** Adapted from ASD-STE100 Issue 9, General Recommendation GR-1

> **Source:** [master.md#sec9-gr1](ste-code/grouped/)

> Source: master.md#sec9-gr1

## Original Rule

In English, you can use the conjunction "that" to connect new information (in a subordinate clause) to a main clause. You can use this conjunction after verbs. For example: "make sure," "show," and "recommend."

Native English speakers frequently do not use "that" when they speak, and this style also occurs in writing. But this conjunction helps the reader understand where the end of the main clause and the start of the subordinate clause is. Thus, use the conjunction "that" as much as possible to prevent ambiguity.

This conjunction also helps with translation because, in many other languages, it is not possible to omit the equivalent word.

### Examples

> **Do not write:** Make sure the valve is open.
>
> **WRITE:** Make sure that the valve is open.

> **Do not write:** The manufacturer recommends you prepare the mixture in an area with good airflow.
>
> **WRITE:** The manufacturer recommends that you prepare the mixture in an area with good airflow.

> **Do not write:** The gauge shows the reservoir is full.
>
> **WRITE:** The gauge shows that the reservoir is full.

## Adapted Rule

In code documentation, you can use the conjunction "that" to connect new information (in a subordinate clause) to a main clause. You can use this conjunction after verbs. For example: "make sure," "show," and "recommend."

Writers frequently omit "that" in informal code documentation, but the conjunction helps the reader understand where the main clause ends and the subordinate clause starts. Thus, use the conjunction "that" as much as possible to prevent ambiguity.

This conjunction also helps with translation because, in many other languages, it is not possible to omit the equivalent word. When you write documentation that a global team will read or that a tool will localize, keep "that" in place.

### Examples

> **Non-STE:** Make sure the test passes before you merge the branch.
>
> **STE:** Make sure that the test passes before you merge the branch.

(The "that" marks the boundary between the instruction "make sure" and the condition "the test passes." Without it, a reader can misread the scope of the instruction.)

> **Non-STE:** The style guide recommends you run the migration in a maintenance window.
>
> **STE:** The style guide recommends that you run the migration in a maintenance window.

("Recommend" is the main-clause verb. The subordinate clause "you run the migration in a maintenance window" follows "that" so the reader can see the full recommendation.)

> **Non-STE:** The log shows the queue is empty.
>
> **STE:** The log shows that the queue is empty.

("Show" is the main-clause verb. The "that" clause tells the reader exactly what the log reports. This prevents a misreading where "empty" appears to attach to "log.")

> **Non-STE:** The linter warns the build will fail if the file has no license header.
>
> **STE:** The linter warns that the build will fail if the file has no license header.

(Without "that," the reader can mistake "the build will fail" for a separate statement instead of the content of the warning.)

## Code-Domain Explanation

GR-1 is a low-cost clarity rule. In code documentation the verbs that most often take a "that" clause are:

- "make sure" (imperative, in procedures and checklists)
- "show," "indicate," "report" (in descriptions of logs, dashboards, and diagnostics)
- "recommend," "require," "specify" (in style guides, specs, and API contracts)

The rule is most valuable in three contexts:

1. **Procedures and checklists.** "Make sure that the test passes" is clearer than "Make sure the test passes" because the reader immediately sees the instruction and its condition as two parts.
2. **Descriptions of diagnostic output.** Logs, dashboards, and error pages report states. "The metric shows that the error rate increased" keeps the reported state inside a subordinate clause.
3. **Cross-language teams.** Teams that translate documentation benefit from the explicit "that" because many languages cannot drop the equivalent word.

Do not over-apply the rule. Short, direct sentences such as "Run the test" or "Open the file" need no "that." Use "that" only when a verb introduces a full subordinate clause.

## Edge Cases

### "That" as a pronoun versus "that" as a conjunction

The word "that" can be a conjunction ("make sure that the test passes") or a demonstrative pronoun ("use that function"). GR-1 applies only to the conjunction use. When "that" is a pronoun, Rule GR-3 and GR-4 apply instead.

### Compound objects after "make sure"

When the clause after "make sure" has its own subject, keep "that": "Make sure that the client retries the request." When the clause reuses the main subject, you may still keep "that" for clarity: "Make sure that the server closes the connection."

## Cross-References

- **Rule 9.2 (Use Each Approved Word Correctly):** Use "that" with its approved function as a conjunction. Do not use it as a pronoun when GR-4 (the pronoun "this") is the better fit.
- **Rule 5.1 (Short Sentences):** When a "make sure that" sentence becomes too long, split it: "Make sure that the build passes. Also make sure that the test coverage is above 80%."
- **Rule 4.1 (Sentence Structure):** A clear main clause followed by a "that" subordinate clause is the preferred structure for instructions that include a condition.
