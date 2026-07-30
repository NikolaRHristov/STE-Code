# Artifact Generation Protocol — Stage 5

Generate 6 final STE-Code artifact files from adapted content. Agent-agnostic.

## Prerequisites
- master.md exists and validated
- All 53 rules present, 19 categories enumerated
- Dictionary entries available
- Synonym and polysemy tables extracted

## 6 Artifacts

| # | File | Target | Purpose |
|---|------|--------|---------|
| 1 | `ste-code-distilled-system-prompt.txt` | ~1,200 tokens | LLM system prompt |
| 2 | `ste-code-self-reading-manual.txt` | ~7,000 tokens | S0-S8 self-reading manual |
| 3 | `ste-code-extraction-methodology.txt` | ~1,400 tokens | 6-pass pipeline protocol |
| 4 | `ste-code-example-turn.txt` | ~500 tokens | Worked example |
| 5 | `ste-code-deployment-guide.txt` | ~1,800 tokens | Ollama, LM Studio, Python |
| 6 | `README.md` | ~500 tokens | Project overview |

## Artifact 1 Quality Gates
- All 14 principles reference specific STE rules
- Synonym table uses actual canonical forms
- Anti-patterns are code-specific
- ~4,800 chars total

## Artifact 2 Quality Gates
- All 8 sections (S0-S8) present, S9 optional
- All 53 adapted rules have code-domain example pairs
- 19 categories listed with code examples
- S6 contains exactly 13 questions

## Anti-Fabrication
- Every adapted rule references master.md rule number
- Every synonym traces to master.md synonym table
- Every example adapts a real STE/non-STE pair
- 19 categories (NOT 22), deepseek-v4-pro (NOT deepseek-pro)

## Verification
```bash
for f in ste-code/artifacts/ste-code-*.txt; do
  chars=$(wc -c < "$f")
  echo "$(basename $f): $chars chars ~$((chars/4)) tokens"
done
```
Expected total: ~49,600 chars (~12,400 tokens)
