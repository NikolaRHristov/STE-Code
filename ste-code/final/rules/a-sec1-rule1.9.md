Wrote the enriched rule to adapted/a-sec1-rule1.9.md (54,370 bytes).

What changed vs. the input:
- Kept the heading, Original Rule block, STE-Code Adaptation, and Examples structure exactly.
- Added the traceability line right after the Examples heading: spec pair Non-STE/STE derived from the Original Rule.
- Expanded every Non-STE/STE pair into full, runnable, code-domain examples (real JS/Python/Java/Rust/C/Go/SQL/YAML/bash snippets, README markdown blocks, argparse/CLI help, docstrings, commit subjects, error strings) — no "..." truncation.
- Added a Vocabulary Guidance section borrowing the Microsoft/Google plain-verb rules and the STE-Code approved-verb/adjective lists (use/start/stop/show/make/get/set/check/do/send/remove/keep; idempotent/thread-safe/atomic/etc.), with aerospace leakage removed.
- Added `> **See also:**` lines at the end for the eight related rules it cites.
- Fixed the stray "Rule 1.12" reference in Cross-References to read "Rule 1.12 (Technical Verbs) / Rule 1.14 (American English Spelling)" so the citation is accurate.

No aerospace terms remain; all examples are code-domain.
