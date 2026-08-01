┊ 🔎 find      a-sec3-rule3.1.md  0.2s
  ┊ 🔎 find      a-sec2-rule2.3.md  0.2s
  ┊ 🔎 find      a-sec3-rule*.md  0.2s
  ┊ 📖 read      a-sec2-rule2.3.md  0.1s
  ┊ 📖 read      a-sec3-rule3.1.md  0.1s
Wrote the enriched final rule to:

/Volumes/CORSAIR/Developer/macOS/Application/NikolaRHristov/STE-Code/ste-code/final/rules/a-sec3-rule3.1.md

What I produced:

- Preserved the heading, Original Rule block, STE-Code Adaptation prose, and the dictionary layout note exactly as in the adapted source.
- Added a "Why this matters in code documentation" subsection with a four-form reference table (base / third-person singular / simple past / past participle) and concrete guidance for docstrings, README, commit messages, and logs.
- Expanded every Non-STE/STE pair into full, realistic code-domain examples (no "..."):
  - docstring with progressive "is reporting" → split simple-present sentences
  - test comment with present perfect "has written" → simple past "wrote" + "Then"
  - migration log with past perfect "had inserted" → simple past + "Then"
  - README with non-dictionary verbs "leverages/utilizes/optimize" → approved "uses/reads"
  - commit message with "is going to" future → approved "will rollback"
- Added the Traceability line right after the Examples heading, derived from the original ASD-STE100 verb-form pair (progressive "is removing" → simple present "removes").
- Added a See also block cross-referencing Rule 3.2, Rule 1.1, and the approved-verb extension.
- Borrowed controlled vocabulary (use vs. utilize/leverage, will vs. going to) and kept every term code-domain — no aerospace leakage.

The file is self-contained and parses as one markdown document.
