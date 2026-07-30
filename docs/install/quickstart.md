# Quick Start

5-minute guide to using STE-Code.

## 1. Use as a System Prompt

```bash
cat ste-code/artifacts/ste-code-distilled-system-prompt.txt
```

Paste this into your LLM's system prompt field. Your documentation will follow
STE-Code rules automatically.

## 2. Run an Agent

```bash
# Documentation agent with self-audit
hermes -z "$(cat .agents/agent/agent-6-phi-sce.md)" -m deepseek-v4-pro

# Level 3 rewrite of a document
hermes -z "level=3 action=rewrite target=README.md" -m deepseek-v4-pro

# Translation orchestrator
hermes -z "$(cat .agents/agent/agent-9-translations.md)" -m deepseek-v4-pro
```

## 3. Run the Benchmark

```bash
python3 .agents/benchmark/orchestrator.py
```

Compares STE-Code against plain assistant baseline across 59 tests.

## 4. Launch Expansion Workers

```bash
python3 .agents/tools/telemetry-worker.py b1-005 \
  .agents/prompts/expansion-pass1/pass1-batch-005.txt \
  --output ste-code/adapted/expanded/pass1-batch-005.json
```

Generates code-domain examples for adapted rules.

## 5. Check Pipeline State

```bash
ls ste-code/extracted/ | wc -l   # 109 files
ls ste-code/refined/ | wc -l     # 109 files
ls ste-code/adapted/ | wc -l     # 57 files
ls ste-code/artifacts/ | wc -l   # 6 files
```
