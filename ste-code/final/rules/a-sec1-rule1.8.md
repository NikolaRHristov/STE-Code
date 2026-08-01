Wrote the enriched final rule to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/final/rules/a-sec1-rule1.8.md

What I changed vs. the adapted source:

1. Traceability block added right after the Examples heading:
   > Adapted from spec pair: Non-STE: (ASD-STE100 gives only the compliant example — no Non-STE version shown) | STE: The front panel of the phone has a touchscreen and a home button.
   Derived from the Original Rule block — the source spec for 1.8 only supplies the compliant example, so I marked the Non-STE side honestly rather than inventing one.

2. Every Non-STE/STE pair now has a full, runnable code block appended (no "..." abbreviation). Each shows a concrete code-domain situation: an exported TSX page, a Java @RestController, an OpenAPI reference + HTTP/JSON, a Python observer docstring, a Java SQLException handler, a Java Singleton/MVC class, Haskell Option/composition, a C malloc/struct/pointer program, Terraform aws_instance + an invalid-HCL counter-example, Rust move/borrow, a PaymentProcessor class, a TS Observer, an HTTPS YAML server block, a React useEffect hook, a Go binarySearch, a .env + SQLAlchemy DATABASE_URL setup, and the edge-case runnable variants (DataStore docstring, EventHandler callback, Django view, migration note, pip install python-dotenv).

3. Cross-references appended as See also lines for Rules 1.1, 1.2, 1.3, 1.5, 1.6, 1.7, 1.9, 1.10, 1.11, 1.12, 1.14 — matching the table already in the file.

4. Vocabulary check: kept plain approved verbs (use/check/show/set/make/get/send) and Microsoft/Google-style nouns; no utilize/leverage/employ/commence/terminate/initiate. No aerospace leakage — all terms are code-domain (class names, APIs, protocols, standard library functions, framework features, package managers).

The file is self-contained and parses as one markdown document. Same structure preserved: heading, Original Rule, STE-Code Adaptation, Examples, Code-Domain Explanation, Paradigm-Specific Guidance, Extended Examples, Edge Cases, Cross-References, Grammar Notes, Summary Checklist, Distinction table.
