# Installing STE-Code

## Prerequisites

- Python 3.11+
- Git
- Hermes Agent (for pipeline orchestration)
- `deepseek-v4-pro` API access (or any OpenAI-compatible endpoint)

## Setup

```bash
# Clone the repository
git clone git@github.com:NikolaRHristov/STE-Code.git
cd STE-Code

# Verify pipeline state
ls ste-code/extracted/ ste-code/refined/ ste-code/adapted/ ste-code/artifacts/

# Set reasoning to high (recommended)
# Edit ~/.hermes/config.yaml:
#   reasoning_effort: high
```

## Quick Start

```bash
# Use STE-Code as a system prompt in any LLM session
cat ste-code/artifacts/ste-code-distilled-system-prompt.txt

# Run an agent
hermes -z "$(cat .agents/agent/agent-6-phi-sce.md)" -m deepseek-v4-pro

# Run the benchmark
python3 .agents/benchmark/orchestrator.py

# Launch expansion workers
python3 .agents/tools/telemetry-worker.py b1-005 \
  .agents/prompts/expansion-pass1/pass1-batch-005.txt \
  --output ste-code/adapted/expanded/pass1-batch-005.json
```

## Directory Layout

```
STE-Code/
├── docs/                    ← You are here
├── ste-code/
│   ├── extracted/           ← Stage 1: 109 raw extraction files
│   ├── refined/             ← Stage 2: 109 formatted files
│   ├── merged/              ← Stage 3: master.md (20,794 lines)
│   ├── adapted/             ← Stage 4: 57 code-domain adapted rules
│   ├── artifacts/           ← Stage 5: 6 deployable files
│   └── v2/                  ← v2 pipeline (partial)
├── SCE/                     ← Product directory (rules, vocab, schemas)
├── .agents/                 ← Agent definitions, skills, prompts, tools
│   ├── agent/               ← 9 agent role definitions
│   ├── skills/              ← 13 skill definitions
│   ├── prompts/             ← Generated worker prompts
│   ├── tools/               ← telemetry-worker.py, launch scripts
│   ├── audit/               ← Maturity audit reports
│   ├── state/               ← Progress tracking, handoffs, plans
│   └── telemetry/           ← Per-worker telemetry records
├── translations/            ← 9-locale placeholder structure
└── spec/                    ← Source ASD-STE100 spec pages
```

## Configuration

| File | Purpose |
|------|---------|
| `~/.hermes/config.yaml` | Hermes agent config: model, reasoning, timeouts |
| `.agents/state/FINAL-PASS-TRACKER.md` | Worker progress tracker |
| `.agents/state/HANDOFF-*.md` | Session handoff documents |
| `.agents/feedback/exchange.md` | Inter-agent communication |
