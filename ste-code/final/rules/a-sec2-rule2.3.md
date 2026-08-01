┊ 📖 read      a-sec2-rule2.3.md  0.1s
  ┊ 📖 read      a-sec2-rule2.3.md  0.1s
  ┊ 📖 read      a-sec2-rule2.1.md  0.1s
  ┊ 📖 read      a-sec2-rule2.2.md  0.1s
Done. The enriched final rule is written to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/final/rules/a-sec2-rule2.3.md

What changed vs. the adapted version:

- Preserved the heading, Original Rule block, Adapted Rule prose, and Examples structure (no aerospace terms leak into the STE-Code guidance; source pairs are kept only as traceable text).
- Expanded every Non-STE/STE pair into full, runnable, code-domain situations: API handler doc comment, YAML rate-limit config + log line, feature-flag trigger function, input-output stream class, short-noun removal function, build-time check script, end-to-end test, and out-of-band/long-running job signal. Each keeps the `> **Non-STE:**` / `> **STE:**` block format with realistic code/config/test/error prose.
- Added a Traceability line right after the Examples heading: `*Adapted from spec pair:* Non-STE: Move the main-gear-door-retraction-winch handle. | STE: Move the main-gear-door retraction-winch handle.`
- Added `## See also` cross-references to Rule 2.1, Rule 2.2, Rule 1.5, and Rule 1.3.
- Borrowed and applied controlled vocabulary: plain approved verbs (use, set, get, remove, check, stop), code-domain adjectives (fail-safe, long-running, build-time), and hyphenated compound modifiers (request-response, read-write, end-to-end, out-of-band) consistent with the Microsoft/Google style guides and the STE-Code dictionary.
- Added reviewer-facing notes on the `-ly` adverb exception, the hyphen-vs-underscore distinction (prose hyphen vs. identifier underscore/camelCase/kebab-case), and the "hyphen groups but does not shorten" link back to Rule 2.2.

The file is self-contained and parses as one markdown document.
