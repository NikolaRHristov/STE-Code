# STE-Code Deployment Guide

## Quick Start

Copy `ste-code-distilled-system-prompt.md` into your LLM's system prompt field.
Set temperature to 0.1-0.3 for strict compliance.

## Platform Instructions

### Ollama (Local)
```dockerfile
FROM llama3.2
SYSTEM """
[Paste ste-code-distilled-system-prompt.md content here]
"""
PARAMETER temperature 0.3
```

```bash
ollama create ste-code -f Modelfile
ollama run ste-code
```

### LM Studio
1. Load your model, paste system prompt, set temperature to 0.3.

### OpenAI / Compatible API
```python
with open("ste-code-distilled-system-prompt.md") as f:
    system_prompt = f.read()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Document this function: ..."}
    ],
    temperature=0.3
)
```

### Anthropic Claude
```python
with open("ste-code-distilled-system-prompt.md") as f:
    system_prompt = f.read()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    system=system_prompt,
    messages=[{"role": "user", "content": "Write a commit message for..."}]
)
```

## Token Budget

| Context | Use | Tokens |
|---------|-----|--------|
| 4K | Short form only | ~1,400 |
| 8K | Short form + key rules | ~2,500 |
| 32K | Full coding rules (Sections 1-9) | ~9,000 |
| 128K+ | Full spec + extraction methodology | ~15,000 |

## Files

| File | Size | Purpose |
|------|------|---------|
| `ste-code-distilled-system-prompt.md` | 6KB | System prompt (~1,400 tokens) |
| `coding-rules-part1-sec1.md` | 12KB | Section 1: Identifiers and Names |
| `coding-rules-part1-sec2-3.md` | 7KB | Sections 2-3: Compound IDs, Functions |
| `coding-rules-part1-sec4-6.md` | 9KB | Sections 4-6: Statements, Procedures, Descriptive |
| `coding-rules-part1-sec7-9.md` | 10KB | Sections 7-9: Safety, Syntax, Practices + GRs |
| `ste-code-extraction-methodology.md` | 3KB | 6-pass transformation pipeline |
| `ste-code-example-turn.md` | 2.5KB | Worked example |
