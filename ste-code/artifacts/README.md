# STE-Code Artifacts

Ready-to-use files for the STE-Code specification. STE-Code adapts ASD-STE100 Issue 9 (January 2025) for software documentation. It gives you 51 writing rules, 19 code-domain noun categories, and a controlled vocabulary.

> Adapted from ASD-STE100 Issue 9 (January 2025), published by the AeroSpace and Defence Industries Association of Europe (ASD), Brussels, Belgium. (C) ASD, 2025 -- All rights reserved. STE is a European Union Trade Mark (No. 017966390). STE-Code is an independent adaptation not endorsed by ASD. For the authoritative standard, visit asd-ste100.org.

## File Index (6 files, ~13,100 total tokens)

| # | File | Tokens | Adaptation Level | Purpose |
|---|------|--------|-----------------|---------|
| 1 | ste-code-distilled-system-prompt.txt | ~1,200 | Level 1 | Concise LLM system prompt (14 principles, synonym table, anti-patterns) |
| 2 | ste-code-self-reading-manual.txt | ~7,000 | Level 5 | Full reference manual (all 51 rules, 4 GR rules, top 50 dictionary entries, full synonym table, compliance checklist, 19 categories) |
| 3 | ste-code-extraction-methodology.txt | ~2,000 | Meta | 5-stage pipeline documentation (extract, refine, merge, adapt, artifacts), quality assurance, benchmark results |
| 4 | ste-code-example-turn.txt | ~500 | Level 2 | Worked before/after example with violation report and metrics |
| 5 | ste-code-deployment-guide.txt | ~1,800 | Level 4 | Integration instructions for Ollama, LM Studio, Python/llama.cpp |
| 6 | README.md | ~400 | Level 1 | This file -- artifact index and quick start |

## Adaptation Levels

Each level adds more STE-Code rules for stricter compliance:

- **Level 1** (~1,200 tokens): 14 core principles, synonym table, output format, anti-patterns. Best for tight token budgets.
- **Level 2** (~2,000 tokens): Level 1 plus rule summaries for Sections 1 through 5 (words, noun phrases, verbs, sentences, procedures).
- **Level 3** (~3,000 tokens): Level 2 plus full all-section rule summaries and GR grammar recommendations.
- **Level 4** (~4,500 tokens): Level 3 plus dictionary excerpt, full synonym table, and compliance checklist.
- **Level 5** (~7,000 tokens): Complete specification: all 51 rules, 19 categories, dictionary, checklist, and appendix.

## Quick Start

1. **Learn the rules.** Read `ste-code-self-reading-manual.txt` sections 1 through 4.
2. **Load the prompt.** Copy `ste-code-distilled-system-prompt.txt` into your LLM system prompt field.
3. **See an example.** Open `ste-code-example-turn.txt` for a worked before/after transformation.
4. **Deploy.** Follow `ste-code-deployment-guide.txt` for your platform.

## Integration Guide

### OpenAI (ChatGPT, GPT-4, GPT-4o)
Use the distilled system prompt from file 1 or the full manual from file 2. Paste the text into the system message of your chat completion API call. Set `temperature` to 0.3.

### Anthropic (Claude)
Paste the distilled system prompt into the `system` parameter. For long documents, use the full manual in the first user message as context. Set `temperature` to 0.3.

### Google (Gemini)
Use the `systemInstruction` field with the distilled prompt. For the full manual, split it across multiple turns.

### Ollama
Follow the Modelfile instructions in `ste-code-deployment-guide.txt`. Run `ollama create ste-code -f Modelfile`.

### LM Studio
Paste the distilled system prompt into the system prompt field. Save the configuration as a preset named "STE-Code."

### llama.cpp / llama-cpp-python
Use the Python example in `ste-code-deployment-guide.txt`. Load the system prompt from file and pass it to `create_chat_completion`.

### Hugging Face (Text Generation Inference)
Add the distilled system prompt to the `parameters.system_prompt` field in your inference request.

## File Dependencies

```
ste-code-distilled-system-prompt.txt  (standalone, Level 1)
ste-code-example-turn.txt             (uses Level 2 rules)
ste-code-extraction-methodology.txt   (standalone, meta-documentation)
ste-code-deployment-guide.txt         (references files 1 and 2)
ste-code-self-reading-manual.txt      (standalone, Level 5)
README.md                             (this file)
```

## Version

Generated: 2026-07-30. Source: 51 deepened rule files, 4 GR files, categories, dictionary, synonym table, and structured data files from ste-code/data/.
