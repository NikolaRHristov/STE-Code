# STE-Code Domain Coverage Gaps

> **Generated:** 2026-07-30 **Purpose:** Track missing code domains for future
> contribution and batch generation. **Status:** These are intentional gaps —
> placeholders mark where domain-specific content belongs.

---

## Coverage Snapshot

| Axis                      |                                     Covered                                     |                                     Missing                                      |
| ------------------------- | :-----------------------------------------------------------------------------: | :------------------------------------------------------------------------------: |
| **Languages in examples** | 13 (Rust, Python, Go, Java, C++, JS/TS, SQL, Bash, YAML, JSON, HTML, CSS, Ruby) |     Swift, Kotlin, Dart, C#, PHP, Scala, Elixir, Haskell, Zig, Lua, R, Julia     |
| **Paradigms**             |                                       5/5                                       |                                        —                                         |
| **Doc types**             |  9 (README, docstring, API, commits, errors, config, comments, CLI, changelog)  | Tutorials, Getting Started, Architecture Decision Records, Runbooks, Postmortems |
| **Domains**               |                                       15+                                       |                                    See below                                     |

---

## Critical Gaps — Domains With Zero Coverage

### Mobile Development

- **Languages:** Swift, Kotlin, Dart, Objective-C
- **Frameworks:** SwiftUI, UIKit, Jetpack Compose, Flutter, React Native
- **Concepts:** App lifecycle, push notifications, deep linking, store review
  guidelines
- **Placeholder prefix:** `[MOBILE: ...]`

### Data Science & Machine Learning

- **Languages:** Python (pandas, NumPy, scikit-learn, PyTorch, TensorFlow, JAX),
  R
- **Concepts:** Model training, inference, feature engineering, MLOps,
  experiment tracking
- **Placeholder prefix:** `[ML: ...]`

### Game Development

- **Languages:** C#, C++ (Unreal), GDScript, Lua
- **Engines:** Unity, Unreal Engine, Godot
- **Concepts:** Game loop, physics engine, shaders, asset pipeline, ECS patterns
- **Placeholder prefix:** `[GAMEDEV: ...]`

### Embedded Systems & IoT

- **Languages:** C, C++, Rust (embedded), MicroPython, Arduino
- **Concepts:** RTOS, firmware, bootloader, memory-mapped I/O, interrupts,
  watchdog timer
- **Placeholder prefix:** `[EMBEDDED: ...]`

### Blockchain & Web3

- **Languages:** Solidity, Vyper, Move, Rust (Solana)
- **Concepts:** Smart contracts, consensus, gas optimization, wallet
  integration, DeFi protocols
- **Placeholder prefix:** `[WEB3: ...]`

---

## High-Priority Gaps — Underrepresented But Important

### Security Engineering

- **Current:** ~5 mentions (mostly in Category 18 — Damage Terms)
- **Missing:** OWASP Top 10 examples, threat modeling, SAST/DAST, CVE
  remediation patterns
- **Placeholder prefix:** `[SEC: ...]`

### Accessibility (a11y)

- **Current:** ~8 mentions (Category 12 — UI elements)
- **Missing:** WCAG 2.1/2.2 conformance examples, screen reader testing, ARIA
  live regions
- **Placeholder prefix:** `[A11Y: ...]`

### Internationalization (i18n) & Localization (L10n)

- **Current:** ~2 mentions
- **Missing:** RTL layout examples, Unicode normalization, ICU message format,
  locale data
- **Placeholder prefix:** `[I18N: ...]`

### Performance Engineering

- **Current:** ~3 mentions
- **Missing:** Profiling (flame graphs), SIMD, cache-line optimization,
  lock-free data structures
- **Placeholder prefix:** `[PERF: ...]`

### Testing Methodologies

- **Current:** ~15 mentions (mostly mock/stub in Category 22)
- **Missing:** Property-based testing, contract testing, fuzzing, mutation
  testing, TDD/BDD patterns
- **Placeholder prefix:** `[TEST: ...]`

### Documentation Process

- **Current:** ~2 mentions
- **Missing:** Doc review workflows, style guide enforcement, doc versioning,
  translation pipelines
- **Placeholder prefix:** `[DOCS: ...]`

---

## Documentation Type Gaps

| Type                              | Files With Examples | Priority |
| --------------------------------- | :-----------------: | :------: |
| README                            |         50          |    —     |
| API documentation                 |         51          |    —     |
| Docstrings                        |         50          |    —     |
| Commit messages                   |         50          |    —     |
| Error messages                    |         50          |    —     |
| Config files                      |         54          |    —     |
| Code comments                     |         50          |    —     |
| CLI help text                     |         36          |    —     |
| **Changelog/Release notes**       |       **16**        |   High   |
| **Tutorials**                     |        **2**        |   High   |
| **Getting Started guides**        |        **5**        |   High   |
| **Architecture Decision Records** |        **0**        |  Medium  |
| **Runbooks/Playbooks**            |        **0**        |  Medium  |
| **Postmortems/Incident reports**  |        **0**        |  Medium  |
| **Style guides**                  |        **0**        |   Low    |
| **FAQ/Glossary**                  |        **0**        |   Low    |

---

## How to Contribute

1. Pick a gap from this file.
2. Find the relevant adapted rule file(s) in `ste-code/adapted/`.
3. Add Non-STE/STE example pairs using the canonical format:

    ```
    > **Non-STE:** [realistic code doc from the domain that violates the rule]
    > **STE:** [STE-Code compliant correction]
    ```

4. Use the placeholder prefix in a comment line above the pair for tracking:

    ```
    > [DOMAIN: domain-name]
    ```

5. Submit a PR with the domain tag in the commit message.

## Batch Generation (Internal)

To generate domain content in batch:

```bash
# Generate domain-specific examples for one rule file
python3 .agents/tools/maintenance/fill-gaps.py --domain MOBILE --rule a-sec4-rule4.3

# Batch generate across all rules for one domain
python3 .agents/tools/maintenance/fill-gaps.py --domain ML --all-rules --min-pairs 3
```

## Tracking

- [ ] MOBILE: Swift/Kotlin examples (target: 5+ rules)
- [ ] ML: pandas/PyTorch/TensorFlow examples (target: 8+ rules)
- [ ] GAMEDEV: Unity/Unreal examples (target: 3+ rules)
- [ ] EMBEDDED: C/RTOS examples (target: 5+ rules)
- [ ] WEB3: Solidity/smart contract examples (target: 3+ rules)
- [ ] SEC: OWASP/threat modeling examples (target: 5+ rules)
- [ ] A11Y: WCAG conformance examples (target: 5+ rules)
- [ ] I18N: RTL/Unicode examples (target: 3+ rules)
- [ ] PERF: Profiling/SIMD examples (target: 5+ rules)
- [ ] TEST: Property-based/fuzz testing examples (target: 5+ rules)
- [ ] DOCS: Review workflow/governance examples (target: 3+ rules)
- [ ] TUTORIAL: Tutorial-style doc type examples (target: 5+ rules)
- [ ] CHANGELOG: Release note examples (target: 3+ rules)
- [ ] ADR: Architecture decision record examples (target: 3+ rules)
- [ ] RUNBOOK: Operational runbook examples (target: 3+ rules)
