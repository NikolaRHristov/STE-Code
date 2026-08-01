┊ 🔎 grep      ^# Rule 1\.(1|2|3|5|7|12|13)  0.1s
  ┊ 🔎 find      a-sec1-rule1.4.md  0.2s
Both matches are legitimate traceability references to the ASD-STE100 source (the spec pair note and the historical note), not aerospace-domain leakage in examples. The file is complete and clean.

Enrichment complete. Wrote the final rule to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/final/rules/a-sec1-rule1.4.md

What I did, per the task spec:

1. Preserved the required blocks — heading, Original Rule block, STE-Code Adaptation, and the Examples structure all kept verbatim from the input.

2. Expanded examples into full, runnable code-documentation scenarios — added a "Full Code-Domain Examples" block after the traceability note with 9 complete Non-STE/STE pairs as fenced code blocks: README build section, API reference (getUser), Python docstring (deduplicate), commit message, config-file YAML comment, Python error-message string, Rust module doc, Terraform module doc, and a test-spec docstring. Each shows concrete functions/APIs/config/tests/errors and applies P4 verb-form fixes.

3. Traceability note — added directly after the Examples heading:
   > *Adapted from spec pair:* Non-STE: ... REMOVE (v) ... SLOW (adj) ... | STE: COMPILE (v) ... FAST (adj) ...
   derived from the Original Rule block.

4. Borrowed only approved plain vocabulary — used "make/gives/checks/controls/sets/removes/runs" etc. per the extension verb list; avoided utilize/leverage/employ/commence/terminate/initiate throughout. "return" replaced with "give" (approved alternative), "perform/execute" with "do", "create/generate" with "make".

5. No aerospace leakage — the only two "aerospace" string hits are the intentional spec-source traceability note and the historical note naming ASD-STE100 (both required for provenance, not example content). All examples are code-domain.

6. Cross-references — added the `> **See also:** Rule X.Y — <title>` block at the end for Rules 1.1, 1.2, 1.3, 1.5, 1.7, 1.12, 1.13, with exact titles verified against the adapted/ files.

Stats: 705 lines, 32 Non-STE / 32 STE example pairs (balanced), self-contained and parseable as one markdown document.
