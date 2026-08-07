# Contributing to STE-Code 🤝

STE-Code adapts ASD-STE100 Issue 9 (January 2025) to code documentation. Every
rule, category, and vocabulary entry traces back to that standard. Contributions
must keep that trace intact.

---

## Before you start ▶️

Verify the checkout:

**`Terminal`**

```bash
make check
```

The gate prints `RESULT: all policies passed`. If it does not, fix that first.

| Target               | What it does                                                 |
| -------------------- | ------------------------------------------------------------ |
| `make check`         | The canonical gate: `lint`, `test`, `audit`, `jail`          |
| `make lint`          | Compile every benchmark module; check line length            |
| `make test`          | Run the adversarial benchmark self-test                      |
| `make audit`         | Prove emitted reports carry no operator identity             |
| `make jail`          | Prove the write-confinement plugins block folder escapes     |
| `make drift`         | Compare documented counts, badges, and versions against disk |
| `make release-test`  | Self-tests for the release tooling                           |
| `make release-check` | `lint`, tests, and `drift` for the release tooling           |

`make check` is the default target. `make drift` and the release targets are
deliberately separate from `check`.

---

## Development setup 🛠️

### Prerequisites ✅

| Requirement      | Needed for                                             |
| ---------------- | ------------------------------------------------------ |
| Python 3         | Every runner, every gate, and the deterministic stages |
| Git              | Version control and the release tooling                |
| An agent backend | The pipeline stages that call a model                  |

An LLM runtime is optional. You need one only to run a compliance check or a
model stage. Any of these work:

- **Ollama** with a code model (deepseek-coder, qwen-coder, codestral).
- **LM Studio** (GUI; macOS, Windows, Linux).
- **llama-cpp-python** for programmatic use.
- An **OpenAI** or **Anthropic** API key for cloud-based checks.

The default backend is Hermes. Configure the backends in
`.agents/config/agents.yaml` and list them with:

**`Terminal`**

```bash
python3 .agents/tools/lib/agent-runner.py --list
```

The model is read from the `STE_MODEL` environment variable. The default is
`tencent/hy3:free`.

### Clone 📥

**`Terminal`**

```bash
git clone https://github.com/NikolaRHristov/STE-Code.git
cd STE-Code
```

No package installation is required. The project is a set of markdown artifacts,
Python tools, and text system prompts. All standard content is under
`ste-code/`.

---

## Ways to contribute 💡

| Contribution       | What to supply                                                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| New synonym        | The unapproved term, the approved replacement, the domain, the reason it is ambiguous, and 3 real examples from public documentation |
| New category       | The category name, 5 example nouns, a counterexample, and why the existing 22 categories do not cover it                             |
| Rule improvement   | A before/after example pair, and a migration plan that keeps the output idempotent                                                   |
| Real-world example | The original text, your STE-Code rewrite, and a short metrics table                                                                  |
| Domain example     | A Non-STE / STE pair for a domain tag from `.agents/GAPS.md`                                                                         |
| Bug report         | The file, the line number, the expected behavior, and the actual behavior                                                            |

We do not accept speculative proposals. A new synonym needs a proven
counterexample from real documentation.

### New synonym 🔤

The controlled vocabulary is the core of STE-Code. Propose a synonym when you
find an unapproved term in real code documentation that has no approved
replacement.

1. Read the current synonym table in `ste-code/data/` and the dictionary in
   `ste-code/final/rules/a-dictionary.md`.
2. Open an issue with the term.
3. Include the **unapproved** term and where it appears (link a real repository
   or README), the **approved** replacement, the **domain** (for example DevOps,
   frontend, database, API design), the **reason** the term is ambiguous,
   metaphorical, or non-literal, and **3 real examples** of the term in code
   documentation.

### New category 🗂️

STE-Code carries 22 technical-noun categories, in
`ste-code/final/rules/a-categories.md`.

1. Read the 22 existing categories first.
2. Open an issue with the category name and at least 5 example nouns.
3. Give a counterexample: documentation that improves with this category.
4. State why the existing categories do not cover these terms. A new category
   must map to a distinct domain concept, for example "middleware components"
   against "frameworks".

### Rule improvement ✏️

The 54 rules and the 4 General Rules (GR1–GR4) were adapted from aerospace
English into the code domain. Propose a change when a rule produces awkward
output for a language or a framework.

1. Confirm the rule still matches the ASD-STE100 Issue 9 structure.
2. Supply a before/after example pair that shows the problem and the fix.
3. Supply a migration plan when the change alters existing output. Idempotency
   must hold: the same input must always produce the same output.

Rule changes need consensus: the maintainer, plus 2 community reviewers.

### Domain example format 🏷️

Add the pair to the matching rule file in `ste-code/adapted/`:

**`Markdown`**

```markdown
> [DOMAIN: mobile] **Non-STE:** [real code documentation from the domain]
> **STE:** [the STE-Code compliant correction]
```

Put the domain tag in the commit message.

### Bug report 🐞

Open an issue when you find a rule that references a missing page, a synonym
that contradicts an approved term, a truncated or malformed artifact file, or a
gate that produces inconsistent output. Name the file, the line number, the
expected behavior, and the actual behavior.

---

## Where the content lives 📍

| Path                         | Contents                                                                |
| ---------------------------- | ----------------------------------------------------------------------- |
| `ste-code/final/rules/`      | The 54 rules, one file per rule, plus the dictionary and the categories |
| `ste-code/adapted/`          | The code-domain adaptation, including the 4 General Rules               |
| `ste-code/final/extensions/` | Gap-fill entries: verbs, adjectives, nouns, anti-patterns, domains      |
| `ste-code/artifacts/`        | Generated. Do not hand-edit. Re-run the artifact stage instead          |
| `.agents/GAPS.md`            | The open domain-coverage gaps                                           |

Everything under `ste-code/artifacts/` is pipeline output. A hand edit there is
lost on the next run.

---

## Run the pipeline locally 🏃

The deterministic stages are safe on a clean checkout. The model stages cost
tokens and rewrite tracked content, so run them only when you intend to
regenerate that layer.

**`Terminal`**

```bash
python3 .agents/tools/runners/phase-c-run.py --dry-run # Merge, plan only
python3 .agents/tools/runners/phase-f-run.py --dry-run # Artifacts, plan only
bash .agents/tools/runners/launch-downstream.sh        # the whole chain
bash .agents/tools/runners/launch-downstream.sh --dry  # plan the chain only
```

`launch-downstream.sh` stops before the Merge stage when `ste-code/refined/`
holds fewer than 100 markdown files, because that means refinement is still
running.

See [docs/pipeline.md](docs/pipeline.md) for the stage table, the gates, and the
prerequisites.

### Stage gates 🚪

Run the gate for the layer you changed. Exit code `0` means it passes.

**`Terminal`**

```bash
python3 .agents/tools/grouping/verify-groups.py       # Merge
python3 .agents/tools/adaptation/verify-adaptation.py # Adaptation
python3 .agents/tools/extension/verify_extensions.py  # Extensions
python3 .agents/tools/artifacts/verify-artifacts.py   # Artifacts
```

---

## Testing 🧪

### Rails checker 🚆

The rails checker scans the pipeline output against 8 rails:

**`Terminal`**

```bash
python3 .agents/tools/quality/check-rails.py
```

| Rail | Name             | Checks                                                               |
| ---- | ---------------- | -------------------------------------------------------------------- |
| R1   | Stage isolation  | Each file is in the correct stage directory                          |
| R2   | Naming           | File names follow the `[w\|r]NNN-pAAAA-BBBB.md` pattern              |
| R3   | Completeness     | No page gaps; every page is accounted for                            |
| R4   | Fabrication      | No invented content, for example React, Docker, npm                  |
| R5   | Formatting       | Headings, blank lines, boilerplate, STE examples, page headers       |
| R6   | Factual accuracy | Documented counts match disk, for example 54 rules and 22 categories |
| R7   | Cross-references | Every internal reference resolves                                    |
| R8   | Metadata         | Required front matter and stamps are present                         |

A non-zero exit code means at least one rail failed. The checker names the file,
the rail, and the problem for every issue.

### Table integrity 📋

**`Terminal`**

```bash
python3 .agents/tools/quality/check-tables.py
```

### Quality sweep 🧹

A parallel audit across every markdown layer:

**`Terminal`**

```bash
python3 .agents/tools/quality/sweep-quality.py --batches 5
```

### Link checking 🔗

lychee scans `ste-code/final/` and `ste-code/artifacts/` for broken links:

**`Terminal`**

```bash
bash .agents/tools/linkcheck/run_linkcheck.sh
```

The configuration is `.agents/tools/linkcheck/lychee.toml`. It ignores the
intentional legacy `master.md#…` backlinks and reports real breakage: stale
internal paths and dead external URLs.

---

## Documentation 📝

All project documentation must follow STE-Code itself:

- Use the active voice. Write "Run the checker", not "The checker should be
  run".
- Use the imperative mood for instructions.
- One instruction per sentence.
- Keep sentences to 20 words or fewer.
- Use approved vocabulary. Replace "basically", "stuff", "make sure", and "be
  careful".
- Remove hedging: "should", "might", "could", "probably", "maybe".
- Use one word for one concept. Do not alternate between "function", "method",
  and "routine".
- Use no slang and no jargon. Replace "wanna", "cool", "magic incantation", and
  "a bunch of".
- Use descriptive headings. A heading states its content; it does not tease it.
- Prefer a table to three paragraphs.

Preview the documentation site:

**`Terminal`**

```bash
pip install mkdocs
mkdocs serve          # http://127.0.0.1:8000
mkdocs build --strict # fails on a broken link or a warning
```

`mkdocs.yml` is in the repository root. The pages are in `docs/`. Add a new page
to the `nav:` list in `mkdocs.yml`.

---

## Pull requests 🔀

### Branch names 🌿

| Prefix  | Purpose                                      |
| ------- | -------------------------------------------- |
| `feat/` | New synonyms, categories, rules, or features |
| `fix/`  | Bug fixes and pipeline corrections           |
| `docs/` | Documentation                                |

Examples: `feat/add-orchestrate-synonym`, `fix/r3-page-gap-145`,
`docs/level-table`.

### Commit messages 💬

Use [Conventional Commits](https://www.conventionalcommits.org/):

**`Commit`**

```text
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

Examples:

- `feat(synonyms): add orchestrate → control/manage to the synonym table`
- `fix(pipeline): correct the page gap in the R3 coverage check`
- `docs(levels): correct the level table token counts`

`CHANGELOG.md` is generated from these commits by
`.agents/tools/release/changelog.py`. Write the commit message carefully; do not
edit the changelog by hand.

### Checklist ✅

- [ ] `make check` passes.
- [ ] Rule and synonym changes trace to ASD-STE100 Issue 9.
- [ ] Idempotency holds: the same input produces the same output.
- [ ] The stage gate for the layer you changed passes.
- [ ] The rails checker passes.

### Review 👀

- At least 1 approval from a maintainer.
- Rule changes need 2 community reviewer approvals in addition.
- Resolve every review thread before the merge.

---

## Recognition 🏆

Every contribution type counts: code, documentation, synonym proposals, category
proposals, bug reports, and examples. Contributors are credited in the release
notes for the version that carries their change.

---

## Code of conduct 📜

This project uses the [Contributor Covenant](CODE_OF_CONDUCT.md). Be respectful,
be constructive, and assume good faith. Harassment, trolling, and dismissive
behavior are not tolerated.

---

## License ⚖️

MIT. By contributing, you agree to license your contribution under the same
terms. See [LICENSE](LICENSE).

---

## Questions ❓

Open a GitHub issue with the `question` label.
