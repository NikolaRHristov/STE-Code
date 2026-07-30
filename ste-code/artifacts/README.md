# STE-Code Artifacts

Ready-to-use system prompts for STE-Code. STE-Code adapts ASD-STE100 Issue 9 (January 2025) for software documentation. It gives you 51 writing rules, 19 code-domain noun categories, and a controlled vocabulary.

> Adapted from ASD-STE100 Issue 9 (January 2025), ASD Europe. (c) ASD, 2025.
> STE is EU Trade Mark 017966390. Independent adaptation.

## System Prompts (4 levels + full specification)

| Level | File | Tokens | Purpose |
|:-----:|------|:------:|---------|
| **1** | [`level1/system-prompt.txt`](level1/system-prompt.txt) | ~1.2K | 14 principles, synonym table, anti-patterns |
| **2** | [`level2/system-prompt.txt`](level2/system-prompt.txt) | ~4.5K | 20 principles, dictionary excerpt, doc templates |
| **3** | [`level3/system-prompt.txt`](level3/system-prompt.txt) | ~8K | 9-section grammar, vocabulary, synonym table |
| **4** | [`level4/system-prompt.txt`](level4/system-prompt.txt) | ~45K | All 51 rules, dictionary excerpt, full synonym table |
| **5** | [`level5/`](level5/) | ~100K | 51 rule summaries (full specification) |

## Supporting Artifacts

| File | Purpose |
|------|---------|
| `ste-code-distilled-system-prompt.txt` | Legacy Level 1 prompt (14 principles) |
| `ste-code-self-reading-manual.txt` | Full reference manual |
| `ste-code-extraction-methodology.txt` | Pipeline documentation |
| `ste-code-example-turn.txt` | Worked before-and-after example |
| `ste-code-deployment-guide.txt` | Integration instructions |
| `ste-code-level5-max.txt` | Maximum-size system prompt |
| `sweep-report.md` | Quality sweep report (65 files, 2 passes) |

## Quick Start

1. Choose a level. Use Level 1 for tight token budgets. Use Level 4 for strict compliance.
2. Copy the system prompt into the system prompt field of your LLM.
3. Send your documentation. The model rewrites it in STE-Code.

## Level Details

**Level 1** (~1.2K tokens): 14 core principles, 15 synonym pairs, output rules, 8 anti-patterns. Best for interactive sessions.

**Level 2** (~4.5K tokens): 20 principles with rule references, 25 synonym pairs, 25 approved verbs, output rules, document structure, documentation templates. Best for code review.

**Level 3** (~8K tokens): Full grammar breakdown across 9 sections with example pairs, 30 approved verbs, 20 synonym pairs, output rules, word-count rules. Best for full document rewriting.

**Level 4** (~45K tokens): All 51 rules with example pairs, dictionary excerpt, full synonym table, output rules. Best for strict compliance checking.

**Level 5** (~100K tokens): 51 individual rule summaries organized by section. Best for specification-grade reference.

## Assembly

All levels are assembled by agent-agnostic scripts in `.agents/tools/`. See `.agents/AGENTS.md` for documentation.

```bash
python3 .agents/tools/assemble-level3.py   # L5 → L3
python3 .agents/tools/assemble-level2.py   # L3 → L2
python3 .agents/tools/assemble-level1.py   # L2 → L1
```
