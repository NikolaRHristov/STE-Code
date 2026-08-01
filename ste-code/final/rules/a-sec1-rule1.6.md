Wrote the enriched rule to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/adapted/a-sec1-rule1.6.md

What changed vs. the input:
- Every Non-STE/STE pair in the Examples section is now a full, runnable, self-contained documentation block (README markdown, JSDoc, Python docstring + inline comment, commit message, CI error line, Docker Compose YAML) — no "..." truncation.
- Added the required `> *Adapted from spec pair:*` traceability line directly under the Examples heading (base → bottom, the original ASD-STE100 pair).
- Expanded the Extended Examples (1–6) into fenced, complete code/documentation snippets instead of inline prose-only pairs.
- Kept the Original Rule block, STE-Code Adaptation, all paradigm sections, edge cases, cross-reference table, dictionary/category references, and grammar notes intact.
- Added the `> **See also:**` cross-reference list at the very end (Rules 1.1, 1.2, 1.5, 1.7, 1.8, 1.9, 1.11, 1.12).
- Borrowed plain code-domain vocabulary from the approved-verb list (uses/processes/makes/copies) and kept all examples strictly code-domain — no aerospace leakage.
