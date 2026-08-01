Done. The enriched final rule is written to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/final/rules/a-sec1-rule1.3.md

Verification (real tool output):
- 655 lines, self-contained markdown.
- 28 `Non-STE:` and 55 `STE:` occurrences (every Non-STE has its STE pair + principle annotations).
- 9 `See also:` cross-references (Rules 1.1, 1.2, 1.4, 1.5, 1.7, 1.8, 1.11, 1.12, 1.13).
- 1 `Adapted from spec pair:` traceability line under the Examples heading.

What I enriched per the task spec:

1. Complete runnable examples — Examples 1–8 each now show a concrete code-domain situation (full Python controller/docstring/test, Go CLI error path, git-style refactor diff, config.ini, SQL migration) with NO "..." truncation. Examples 1–6 from the source are preserved and expanded; I added Example 7 (test suite) and Example 8 (SQL migration warning) to cover two documentation types only lightly touched before.

2. Cross-references — added `> **See also:**` lines for all nine related Section 1 rules cited in the body.

3. Traceability — added the `Adapted from spec pair:` line immediately after the Examples heading, derived from the rule's own Original Rule block (the follow/obey distinction) and the follow-vs-obey STE-Code example.

4. Borrowed vocabulary — used plain approved verbs throughout (execute/operate/give/remove/connect/examine/verify), aligning with the Microsoft/Google style guides and the STE-Code extension verb list; avoided utilize/leverage/employ/commence/terminate/initiate.

5. No aerospace leakage — every example and term is code-domain (functions, APIs, configs, tests, errors, Rust ownership, SQL, Terraform). The only aerospace reference kept is the historical note about "follow"/"obey," which the spec explicitly preserves as the ASD-STE100 precedent, and the probe example which is explicitly framed as the code-domain conflict.

I also added Edge Case 6 (approved adjective forced into verb slot — "idempotents"/"atomices") to deepen the part-of-speech/meaning intersection guidance, with a code-domain STE rewrite.
