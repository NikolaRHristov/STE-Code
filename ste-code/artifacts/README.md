# STE-Code — Simplified Technical English for Code Documentation

> **Source:** Adapted from ASD-STE100 Issue 9, January 2025
> **Stage:** 5 — Artifacts
> **Model:** deepseek-v4-pro

## What Is STE-Code?

STE-Code adapts the ASD-STE100 Simplified Technical English standard from aerospace into the code documentation domain. It provides 53 writing rules, 19 technical noun categories, 4 technical verb categories, and a controlled vocabulary for producing clear, unambiguous code documentation. Every README, API doc, comment block, commit message, and error message can be made clearer with STE-Code.

---

## Files

| # | File | Size | Purpose |
|---|------|------|---------|
| 1 | `ste-code-distilled-system-prompt.txt` | ~10.8 KB | System prompt constraining any LLM to STE-Code output |
| 2 | `ste-code-self-reading-manual.txt` | ~25.6 KB | 8-section self-reading manual (S0-S8) |
| 3 | `ste-code-extraction-methodology.txt` | ~5.8 KB | 6-pass extraction pipeline with turn-by-turn protocol |
| 4 | `ste-code-example-turn.txt` | ~3.0 KB | Worked example: non-STE-Code → STE-Code with changes table |
| 5 | `ste-code-deployment-guide.txt` | ~4.6 KB | Deployment: Ollama, LM Studio, Python, batch processing |
| 6 | `README.md` | This file | Overview and quick start |

**Total:** ~6 files, ~50 KB, ~12,400 tokens

---

## Quick Start (3 Steps)

### 1. Choose a Deployment Option

```bash
# Option A: Ollama (simplest)
ollama create ste-code -f Modelfile
ollama run ste-code
```

See `ste-code-deployment-guide.txt` for LM Studio, Python, and batch options.

### 2. Run a Compliance Check

Feed any code document to the STE-Code model:

```
Input: "This function does a bunch of stuff and should be called with the user object."
Output: "Call this function with the user object."
```

### 3. Review the Output

Every output includes:
- **COMPLIANCE STATUS** — Violations found and fixed
- **CORRECTED TEXT** — Document in STE-Code compliant form
- **CHANGES TABLE** — Every correction with principle reference
- **UML DIAGRAMS** — Mermaid class and flowchart diagrams

---

## Architecture Summary

### Preserved (from ASD-STE100)
- 53 writing rules (same numbers: 1.1–9.4)
- 4 General Rules (GR1–GR4)
- 6-pass transformation pipeline (lexical → classification → POS lock → meaning → grammar → consistency)
- Dictionary architecture (APPROVED/UNAPPROVED with alternatives)
- 19 technical noun categories (adapted from STE's 19)
- 4 technical verb categories

### Replaced (adapted for code domain)
- Aerospace examples → Code documentation examples
- WARNING → BREAKING, CAUTION → DEPRECATED
- Aircraft parts/materials → Frameworks/dependencies/tools
- Maintenance procedures → Development workflows
- Safety instructions → Version migration guides

---

## Design Principles

1. **Zero Fabrication** — Every rule, category, and synonym traces to the original ASD-STE100 Issue 9 spec.
2. **Code Domain First** — Examples use real frameworks, languages, and tools (not abstract placeholders).
3. **LLM-Deployable** — The system prompt is ~1,200 tokens, fitting any model with ≥4K context.
4. **Self-Contained** — The self-reading manual (S0-S8) enables recursive, page-by-page processing.
5. **Idempotent** — The same input always produces the same compliance output.

---

## Pipeline

```
ASD-STE100 Issue 9 (434 pages)
  → Stage 1: Extract (109 workers)
  → Stage 2: Refine (109 workers, 9 formatting rules)
  → Stage 3: Merge (master.md, 21K lines)
  → Stage 4: Adapt (53 rules + 19 categories → code domain)
  → Stage 5: Artifacts (6 files, ~12,400 tokens)
```

---

## References

- **ASD-STE100 Issue 9** (January 2025) — ASD, Brussels, Belgium — www.asd-europe.org
- **Model:** deepseek-v4-pro
- **19 technical noun categories** (NOT 22)
- **53 writing rules + 4 GR rules** (NOT 65)
- **434 pages** in the Issue 9 specification
