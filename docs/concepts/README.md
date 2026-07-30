# STE-Code Concepts

STE-Code applies Simplified Technical English principles to code documentation.
Every concept maps to a specific writing rule in the adapted standard.

## 14 Core Principles

| P# | Principle | Rule | Applies To |
|----|-----------|------|------------|
| P1 | Use approved words from the STE-Code dictionary | 1.1 | Docstrings, comments, README, errors, commits |
| P2 | Use words only as their specified part of speech | 1.2 | All documentation text |
| P3 | Use words only with their approved meanings | 1.3 | All documentation text |
| P4 | Active voice; imperative mood for instructions | 1.4 | Procedural docs, API descriptions |
| P5 | Technical code nouns (keywords, frameworks, tools) allowed as-is | 1.5 | Code references in docs |
| P6 | Non-approved words only when technical code nouns | 1.6 | API names, library names |
| P7 | Do not use technical nouns as verbs | 1.7 | Documentation references |
| P8 | Use standard, well-known technical nouns | 1.8 | Documentation references |
| P9 | Prefer short, clear technical nouns | 1.9 | Documentation references |
| P10 | No slang, jargon, or vague terms | 1.10 | All documentation |
| P11 | One term per concept — no synonym drift | 1.11 | API docs, variable descriptions |
| P12 | Technical verbs (build, deploy, test) are allowed | 1.12 | Procedural docs |
| P13 | Do not use technical verbs as nouns | 1.13 | All documentation |
| P14 | American English spelling | 1.14 | All documentation |

## Canonical Synonym Table

| Prefer | Avoid |
|--------|-------|
| use | utilize, leverage, employ |
| start | initiate, commence, bootstrap |
| stop | terminate, halt, kill |
| show | display, render, present |
| make | create, generate, produce |
| get | retrieve, fetch, obtain |
| set | configure, assign, establish |
| check | verify, validate, ensure |
| do | perform, execute, carry out |
| send | transmit, dispatch, forward |
| remove | delete, eliminate, purge |
| keep | retain, preserve, maintain |

## Anti-Patterns

| Rule | Violation | Fix |
|------|-----------|-----|
| 20 words max per procedural sentence | "The function iterates through the array and applies the transformation to each element before returning the result." | "The function transforms each array element. It returns the result." |
| One instruction per step | "Install the package and configure the settings." | "1. Install the package.\n2. Configure the settings." |
| No nested clauses >2 deep | "The module, which handles authentication, uses OAuth, which requires a provider, which must be configured." | "The authentication module uses OAuth. Configure the OAuth provider." |
| No semicolons in prose | "Set the variable; then call the function." | "Set the variable. Then, call the function." |
| No contractions | "The function doesn't return a value." | "The function does not return a value." |
| No "-ing" forms as main verbs in procedures | "Clicking the button submits the form." | "Click the button. The form submits." |

## Signal Words

| Word | Use |
|------|-----|
| `BREAKING:` | Before destructive API changes |
| `DEPRECATED:` | Before removed features |
| `NOTE:` | Important non-safety information |

## Paradigm Adaptation

STE-Code works with any programming paradigm:

| Paradigm | Documentation Style | Languages |
|----------|-------------------|-----------|
| OOP | Class/method docstrings, interface contracts | Python, Java, C++, C# |
| FP | Pure function signatures, type annotations, immutability notes | Haskell, Elixir, Clojure |
| Procedural | Step-by-step operation docs, side-effect warnings | C, Go, Bash |
| Declarative | Configuration schema docs, rule descriptions | SQL, Terraform, YAML |
| Systems | Memory/ownership docs, safety invariants | Rust, C, Zig |
| Scripting | Quick-reference comments, pipeline docs | Python scripts, Shell, Lua |
