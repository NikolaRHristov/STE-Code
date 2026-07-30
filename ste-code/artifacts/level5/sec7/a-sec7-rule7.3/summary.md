# Rule 7.3 — Give an Explanation to Show the Risk or Possible Result

## Original Rule Summary

Rule 7.3 requires that every safety instruction include an explanation of the problems that can occur if the reader does not obey it. When there is a clear and specified risk, the person who does the task understands the risk and is more careful. The spec provides three patterns: a WARNING that explains the poison risk of solvents, a CAUTION that explains the corrosion risk of chlorine-based cleansers, and a consequence statement that explains the permanent damage from dropping parts. Each pattern connects the prohibition to a concrete, observable outcome.

## STE-Code Adaptation

Rule 7.3 applies the same risk-explanation requirement to all code documentation safety instructions. Every WARNING or CAUTION in README files, API documentation, docstrings, commit messages, error messages, and changelogs must include a specific, concrete explanation of what goes wrong when the instruction is ignored. A WARNING without a risk explanation is a prohibition without justification; a CAUTION without a consequence is a suggestion the reader has no reason to follow. The risk explanation must match the signal word severity — WARNING maps to data loss, security breach, or system unavailability, while CAUTION maps to incorrect results, degraded performance, or build failures.

## Example Pairs

> **Non-STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE.
>
> **STE:** WARNING: DO NOT STORE API KEYS IN THE SOURCE CODE. API KEYS IN SOURCE CODE CAN CAUSE UNAUTHORIZED ACCESS AND DATA BREACHES.
>
> *(P1 applied: "store," "access," "data" are approved words. P3 applied: "cause" carries its specific meaning of direct causation. P10 applied: the risk is stated concretely — "unauthorized access and data breaches" — not a vague term like "security issues.")*

> **Non-STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS.
>
> **STE:** CAUTION: DO NOT USE DEPRECATED FUNCTIONS. DEPRECATED FUNCTIONS CAN CAUSE UNEXPECTED BEHAVIOR AND INCORRECT RESULTS.
>
> *(P1 applied: "use," "cause," "unexpected," "incorrect" are approved words. P3 applied: "behavior" and "results" carry specific meanings — the reader knows exactly what degrades. P7 applied: "deprecated" is a technical adjective, not used as a verb.)*

> **Non-STE:** MAKE SURE THAT YOU SET THE CONNECTION TIMEOUT.
>
> **STE:** IF YOU DO NOT SET THE CONNECTION TIMEOUT, THE APPLICATION CAN BECOME UNAVAILABLE AND PERMANENT DATA LOSS CAN OCCUR.
>
> *(P1 applied: "set," "connection," "application," "data" are approved words. P3 applied: "unavailable" is specific — the application stops serving — not "bad things happen." P10 applied: "permanent data loss" states the concrete worst-case outcome, not slang like "your data is toast." P7 applied: "timeout" is a technical noun, not used as a verb.)*

## Principles Applied

**P1** — Use approved words from the controlled terminology. Every word in a risk explanation must come from the STE-Code dictionary. Words like "cause," "occur," "access," "behavior," "loss," and "unavailable" are approved and carry their dictionary meanings. Unapproved words in risk explanations weaken the authority of the safety instruction and can confuse the reader about the nature of the risk.

**P3** — Use words with their specific, approved meanings. A risk explanation must not rely on vague terms like "dangerous," "bad," "wrong," or "problematic." Instead, state the exact consequence: "unauthorized access," "incorrect results," "data loss," "system unavailability." The reader must understand what specifically will occur, not just that something undesirable will occur. Vague risk explanations train readers to ignore all safety instructions.

**P7** — Do not use technical nouns as verbs (Rule 1.7). Risk explanations frequently involve technical nouns like "timeout," "deadlock," "race," and "cache." These must remain nouns. Write "A timeout can occur" not "The connection can timeout." When a risk chain involves a technical action, pair the technical noun with an approved verb: "A data race can cause incorrect results" not "Concurrent writes can race."

**P10** — Do not use slang, jargon, or regional terms (Rule 1.10). Risk explanations must use standard, universally understood terms. A risk explanation that says "This will brick your deployment" fails Rule 7.3 because "brick" is slang. The STE version must state the specific consequence: "This will make the deployment permanently unavailable." Similarly, "blows up," "nukes," "tanks," "eats," and other informal verbs for failure must be replaced with approved words that state the exact outcome.
