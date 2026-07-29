---
id: example-readme-section
version: 1.0.0
document-type: readme
rules-demonstrated: [P1, P5, P7, P9, P11, P14]
---

# STE-Code Example — README Section

## Non-STE (Violations)

```markdown
## Getting Started

To get things going, you'll want to grab the dependencies and then kick off
the dev server. Make sure you've got Node.js installed (we recommend the LTS
version) before you do anything.
```

**Violations:**
- `get things going` → unapproved jargon (P10)
- `grab` → use `read` or `install` (P1)
- `kick off` → use `start` (P1 — synonym table)
- `we recommend` → ambiguous subject (P11)
- Sentences exceed 25 words (rule-5.1)

## STE-Code Compliant

```markdown
## Quick Start

**NOTE:** Install Node.js LTS before you run these steps.

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```
```

**Compliance:** 0 violations. Steps are imperative and sequential. No ambiguous pronouns. All verbs are approved (`install`, `run`, `start`). Sentences are under 20 words.
