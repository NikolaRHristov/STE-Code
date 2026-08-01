Done. Enriched rule written to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/adapted/a-sec1-rule1.7.md

What I did to the file (50 KB, self-contained markdown, no aerospace leakage):

1. Preserved the original heading, Original Rule block, STE-Code Adaptation, and all six extended Example Groups plus the five Edge Cases, Grammar Notes, Summary Checklist, and Cross-References table verbatim in structure.

2. Added TRACEABILITY after the STE-Code Adaptation block — three `> *Adapted from spec pair:*` lines mapping the oil / snow / drill spec examples to their code-domain analogues.

3. Expanded EVERY Non-STE/STE pair into a full, runnable, code-domain context block:
   - README (bash + markdown steps)
   - API reference (Python `get_user` with full docstring)
   - Docstrings/comments (Python `flush_response`)
   - Commit messages (git log excerpt)
   - Error messages (Python ConfigError w/ end-user + dev variants)
   - All 5 paradigms (Java factory, Haskell fmap, C malloc, SQL DDL, Rust interrupt)
   - All 6 extended groups (CI YAML, Python scheduler, ops bash, FastAPI handler, migration plan, logging module)
   - All 5 edge cases (UI handler, Express/React JS, Python dataclass, Java protoc builder, Go gateway)
   - Grammar Notes service example

4. Added the `> **See also:**` block at the very end citing Rules 1.1, 1.2, 1.5, 1.8, 1.11, 1.12, 1.13 and Section 3.

5. Vocabulary: used approved simple verbs (store, put, send, make, add, use, get, set, write) per the extension list and Microsoft/Google style; avoided utilize/leverage/employ/commence/terminate/initiate throughout.

Fixed one typo I caught (`"REST" andGraphQL"` → `"REST" and "GraphQL"`) before reporting.

One note for your review: in Example Group D I kept the original text "GraphQL the queries" → "process the queries through GraphQL" (your input had "GraphQL" in the Non-STE line). If you'd rather the Non-STE line read "GraphQL the queries" verbatim as a clearer violation, say so and I'll align it.
