# STE-Code — Simplified Technical English for Code

STE-Code adapts the ASD-STE100 Issue 9 specification (Simplified Technical English, January 2025) for software documentation. It provides 53 writing rules, 19 code-domain noun categories, and a controlled vocabulary to make code documentation clear, consistent, and unambiguous.

## Files

| File | Size | Purpose |
|------|------|---------|
| ste-code-distilled-system-prompt.txt | ~1,200 tokens | LLM system prompt |
| ste-code-self-reading-manual.txt | ~7,000 tokens | Full 8-section manual |
| ste-code-extraction-methodology.txt | ~1,400 tokens | 6-pass pipeline |
| ste-code-example-turn.txt | ~500 tokens | Worked example |
| ste-code-deployment-guide.txt | ~1,800 tokens | Ollama/LM Studio/Python setup |
| README.md | ~500 tokens | This file |

## Quick Start

1. **Read the manual**: Start with `ste-code-self-reading-manual.txt` S0-S3
2. **Load the prompt**: Use `ste-code-distilled-system-prompt.txt` as your LLM system prompt
3. **Process documents**: Follow the deployment guide for your platform

## Architecture

**Preserved from ASD-STE100 Issue 9:**
- 53 writing rules across 9 sections
- 6-pass transformation pipeline
- Dictionary architecture (APPROVED/UNAPPROVED)
- Safety instruction format (WARNING/CAUTION → BREAKING/DEPRECATED)

**Adapted for code domain:**
- 19 Technical Code Noun categories (keywords, frameworks, tools, protocols)
- Code-domain example pairs (replacing aerospace examples)
- Code-specific anti-patterns
- Modern deployment options (Ollama, LM Studio, Python)

## References
- ASD-STE100 Issue 9, January 2025 — original specification
- 434 pages extracted, enriched, merged, and adapted
