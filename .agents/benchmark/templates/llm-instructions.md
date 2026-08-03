You are reading the evidence dossier of an adversarial benchmark harness with
five participants:

RED generates adversarial inputs and records which ones escaped BLUE relocates
each escaped payload and measures resistance PURPLE stitches RED x BLUE into an
interplay matrix WHITE learns from escapes, proposes remedies, validates them
BLACK attacks the CONCLUSION the other four produce, and rules on it

The design thesis is adversarial self-refutation: WHITE hands BLACK an attack
brief describing the weakest links in the other colours' reasoning, so BLACK can
disprove results that only looked correct. Claims that survive that process are
the ones worth keeping.

Write a report for an engineer who did not run this. Requirements:

1. Lead with what is MEASURED versus SIMULATED. Never present a simulated number
   as a measurement. If the pipeline ran offline, say so first.
2. Explain what the benchmark set out to test, what it actually established, and
   what it failed to establish.
3. Use markdown tables for anything comparative.
4. Address the self-refutation loop explicitly: did BLACK genuinely challenge
   the claims, or did it confirm them by construction? Did the learning curve
   converge?
5. Ground every claim in a number from the dossier. Do not invent figures.
6. End with concrete next actions, ordered by what unblocks the most.

> **Provenance is the first duty.** If the pipeline ran offline, say so before
> any adversarial figure, and never present a simulated number as a measurement.

Dossier follows.

OUTPUT CONTRACT: reply with the report itself as markdown, and nothing else. Do
not create, write or modify any file. Do not run any command. Do not preface the
report with a summary of what you did. The report text IS the deliverable.
