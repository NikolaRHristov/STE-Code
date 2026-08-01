# Contributing to STE-Code

Thank you for your interest in contributing to STE-Code — Simplified Technical English adapted for code documentation. This project traces its rules, categories, and vocabulary to ASD-STE100 Issue 9 (January 2025), and every contribution helps make code documentation clearer, more precise, and more machine-readable.

---

## Ways to Contribute

### Suggest New Synonyms for the Synonym Table

The controlled vocabulary is the heart of STE-Code. If you find an unapproved term in real-world code documentation that lacks an approved replacement, propose it.

1. Locate the master synonym table in [`ste-code/artifacts/ste-code-self-reading-manual.txt`](./ste-code/artifacts/ste-code-self-reading-manual.txt) (Section S4).
2. Open a GitHub issue using the **Synonym Proposal** template.
3. Include:
   - **UNAPPROVED** term and where it appears in documentation (link to a real repo or README).
   - **RECOMMENDED APPROVED** replacement(s).
   - **DOMAIN** (e.g. DevOps, frontend, database, API design).
   - **JUSTIFICATION** — why the term is ambiguous, metaphorical, or non-literal.
   - At least **3 real-world examples** of the term in code documentation.

New synonyms must have a proven unapproved counterexample from actual documentation. We do not accept speculative proposals.

### Propose New Code-Domain Categories

STE-Code inherits 19 technical noun categories from ASD-STE100. If you believe a new category is warranted:

1. Review the 19 existing categories in Section S3 of the self-reading manual.
2. Open a **Category Proposal** issue with:
   - **Category name** and at least **5 example nouns**.
   - **Counterexample** — documentation that would improve with this category.
   - **Justification** — why existing categories do not cover these terms.
3. New categories must map to a distinct domain concept not already represented (e.g. "Middleware Components" vs. "Frameworks").

### Improve Adaptation Rules

The 53 writing rules and 4 General Rules (GR1–GR4) were adapted from aerospace English into the code domain. If a rule produces awkward output for a specific language or framework:

1. Confirm the rule aligns with ASD-STE100 Issue 9 structure.
2. Provide a **before/after example pair** showing the problem and the proposed fix.
3. Include a **migration plan** if the change alters existing compliance output — idempotency must be preserved (the same input must always produce the same output).

Rule changes require consensus: the maintainer plus at least 2 community reviewers.

### Submit Real-World Code Documentation Examples

The project's example corpus strengthens every rule and synonym. Submit:

- A link to a public repository with documentation that would benefit from STE-Code.
- The **original text** and your **STE-Code compliant rewrite**.
- A short table of metrics (word count, ambiguous terms removed, hedging eliminated).

Accepted examples are added to [`ste-code/artifacts/ste-code-example-turn.txt`](./ste-code/artifacts/ste-code-example-turn.txt) with attribution.

### Report Bugs in the Pipeline

The 5-stage pipeline (Extract → Refine → Merge → Adapt → Artifacts) processes 434 pages of the ASD-STE100 Issue 9 specification. If you find:

- A rule that references a missing page.
- A synonym that contradicts an approved term.
- An artifact file that is truncated or malformed.
- A compliance check that produces inconsistent output.

Open a **Bug Report** issue. Include the specific file, line number (if known), expected behavior, and actual behavior.

### Improve Deployment Guides

The deployment guide covers ChatGPT, Claude, Gemini, local models (Ollama, LM Studio, llama.cpp), and CI/CD integration. If you:

- Use STE-Code with a platform not yet documented (e.g. vLLM, Groq, Together AI, AWS Bedrock).
- Discover a simpler setup flow for an existing platform.
- Find a broken command or outdated dependency.

Submit a PR against [`ste-code/artifacts/ste-code-deployment-guide.txt`](./ste-code/artifacts/ste-code-deployment-guide.txt).

---

## Development Setup

### Prerequisites

- Python 3.9+
- Git
- An LLM runtime (optional — only needed for running compliance checks):
  - **Ollama** with a compatible model (deepseek-coder, qwen-coder, codestral).
  - **LM Studio** (GUI, macOS/Windows/Linux).
  - **llama-cpp-python** for programmatic use.
  - **OpenAI API key** or **Anthropic API key** for cloud-based checks.

### Clone and Install

```bash
git clone https://github.com/NikolaRHristov/STE-Code.git
cd ste-code
```

No package installation is required. The project is a collection of markdown artifacts, a Python rails checker, and text-based system prompts. All source material lives under `ste-code/`.

### Run the Pipeline

The pipeline is already executed and the artifacts are committed. To verify:

```bash
# Verify all 8 rails pass
python3 ste-code/check-rails.py

# Expected output: ✅ All files pass rails compliance.
```

To run a compliance check against your own documentation:

```bash
# Ollama (simplest)
ollama create ste-code -f Modelfile && ollama run ste-code

# Batch processing
cat ste-code/artifacts/ste-code-distilled-system-prompt.txt > /tmp/ste-code-context.txt
echo -e "\n---\n" >> /tmp/ste-code-context.txt
cat my-readme.md >> /tmp/ste-code-context.txt
hermes -z "$(cat /tmp/ste-code-context.txt)" -m tencent/hy3:free --yolo
```

Full deployment instructions are in [`ste-code/artifacts/ste-code-deployment-guide.txt`](./ste-code/artifacts/ste-code-deployment-guide.txt).

---

## Pull Request Process

### Branch Naming

Use one of the following prefixes:

| Prefix   | Purpose                                     |
|----------|---------------------------------------------|
| `feat/`  | New synonyms, categories, rules, or features |
| `fix/`   | Bug fixes, pipeline corrections              |
| `docs/`  | Documentation, deployment guide updates      |

Examples: `feat/add-orchestrate-synonym`, `fix/r3-page-gap-145`, `docs/vllm-deployment`.

### PR Template

All pull requests must use the template at [GitHub Issues](https://github.com/NikolaRHristov/STE-Code/issues). The template requires:

- A summary of the change.
- Reference to the related issue.
- A checklist confirming:
  - The change is traceable to ASD-STE100 Issue 9 (for rule/synonym changes).
  - Idempotency is preserved.
  - The 8-rail checker passes (`python3 ste-code/check-rails.py`).

### Review Requirements

- At least **1 approval** from a maintainer or trusted reviewer.
- Rule changes require **2 community reviewer approvals** in addition to the maintainer.
- All review threads must be resolved before merge.

### Rails Compliance

All 8 rails must pass before merge:

| Rail | Name              | Description                                              |
|------|-------------------|----------------------------------------------------------|
| R1   | Stage Isolation   | Files must be in the correct stage directory             |
| R2   | Naming            | Files must follow `[w|r]NNN-pPPPP-PPPP.md` pattern       |
| R3   | Page Coverage     | All 434 pages must be accounted for, no gaps             |
| R4   | Fabrication       | No AI-fabricated content (e.g. React, Docker, npm)       |
| R5   | Formatting        | Headings, blank lines, boilerplate, STE examples, headers |
| R6   | Facts             | No incorrect claims (e.g. "22 categories" — must be 19)  |

Run the checker locally:

```bash
python3 ste-code/check-rails.py
```

A failing rail blocks the merge. Fix the issue and re-run until all rails pass.

---

## Style Guide

### STE-Code Compliance for Documentation

All project documentation — including this CONTRIBUTING.md, README.md, and all artifact files — must itself be STE-Code compliant. This means:

- **Use the active voice.** Write "Run the checker" not "The checker should be run."
- **Use approved vocabulary.** Consult the synonym table in the self-reading manual (Section S4). Replace unapproved terms like "basically," "stuff," "make sure," and "be careful" with their approved equivalents.
- **Write short sentences.** Target 20 words or fewer per sentence. Break long sentences at natural clause boundaries.
- **Use imperative mood for instructions.** Write "Open the file" not "You should open the file."
- **One instruction per sentence.** Write "Install the package. Run the tests." not "Install the package and then run the tests."
- **Avoid hedging.** Remove "should," "might," "could," "probably," and "maybe" from procedural text.
- **Use consistent terminology.** Refer to the same concept with the same word throughout. Do not alternate between "function," "method," and "routine" for the same thing.
- **No slang or jargon.** Replace "wanna," "cool," "magic incantation," "bunch of," and similar informal language.
- **Use descriptive headings.** Section titles must describe their content, not tease it.

### Conventional Commits

All commit messages must follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

Examples:
- `feat(synonyms): add orchestrate → control/manage to synonym table`
- `fix(pipeline): correct page gap in R3 coverage check`
- `docs(deploy): add vLLM deployment instructions`

---

## Testing

### Running the Rails Checker

The 8-rail compliance checker validates pipeline integrity across all stage directories:

```bash
python3 ste-code/check-rails.py
```

Expected output:

```
Files checked: 218
Clean: 218
Issues: 0

✅ All files pass rails compliance.
```

A non-zero exit code indicates at least one rail failure. The checker reports the specific file, rail, and description for each issue.

### Verifying Artifacts

All 6 artifacts in `ste-code/artifacts/` must be consistent:

1. **System prompt** (`ste-code-distilled-system-prompt.txt`): ~1,200 tokens. Must contain all 14 principles.
2. **Self-reading manual** (`ste-code-self-reading-manual.txt`): Must contain all 51 adapted rules (9 sections), 17 domain extensions, and the synonym table.
3. **Extraction methodology** (`ste-code-extraction-methodology.txt`): Must describe the 6-pass pipeline with turn-by-turn protocol.
4. **Example turn** (`ste-code-example-turn.txt`): Must include a before/after pair with a changes table and metrics.
5. **Deployment guide** (`ste-code-deployment-guide.txt`): Must cover at least 7 deployment options.
6. **README** (`README.md`): Must include quick start, examples, comparison metrics, and the roadmap.

To verify artifact consistency against the pipeline output:

```bash
# Check that the system prompt references match the self-reading manual
grep -c "Principle" ste-code/artifacts/ste-code-distilled-system-prompt.txt
grep -c "Rule " ste-code/artifacts/ste-code-self-reading-manual.txt

# Verify no fabrication signals in any artifact
grep -r "fabricate\|hallucinat\|guess" ste-code/artifacts/ && echo "FABRICATION DETECTED" || echo "Clean"
```

---

## Issue Templates

Issue templates are available in `.github/ISSUE_TEMPLATE/`. Choose the template that matches your contribution:

- **Synonym Proposal** — suggest a new unapproved → approved pair.
- **Category Proposal** — propose a new technical noun category.
- **Rule Change** — suggest an improvement to an existing adaptation rule.
- **Bug Report** — report a pipeline, artifact, or checker defect.
- **Documentation Example** — submit a real-world before/after documentation pair.

If your contribution does not fit a template, open a blank issue with a descriptive title.

---

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you agree to uphold its standards. In short: be respectful, be constructive, and assume good faith. Harassment, trolling, and dismissive behavior are not tolerated.

---

## Recognition

### Contributors

STE-Code follows the [all-contributors](https://allcontributors.org/) specification. Every contribution type is recognized — code, documentation, synonym proposals, category proposals, bug reports, deployment guides, and examples.

To add yourself, mention `@all-contributors` in a PR or issue comment:

```
@all-contributors please add @username for code, doc, ideas, bug
```

Supported contribution types: `code`, `doc`, `ideas`, `bug`, `example`, `review`, `question`, `talk`, `tutorial`.

### Current Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This list is auto-generated. Do not edit it manually.

---

## License

STE-Code is licensed under the MIT License. By contributing, you agree that your contributions will be licensed under the same terms. See [`LICENSE`](./LICENSE) for the full text.

---

## Questions?

Open a GitHub issue with the `question` label, or start a Discussion. We respond to all contributor inquiries.
