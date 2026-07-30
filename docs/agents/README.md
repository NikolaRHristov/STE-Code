# Agent Catalog

9 specialized orchestrators power the STE-Code pipeline. Each is defined in
`.agents/agent/agent-N-role.md` and uses the same batch-of-3 worker pattern.

| # | Agent | Role | File |
|---|-------|------|------|
| 1 | Extractor | Reads spec pages, extracts raw text via 109 workers | `agent-1-extractor.md` |
| 2 | Refiner | Reformats extracted text into clean markdown (9 rules) | `agent-2-refiner.md` |
| 3 | Auditor | Verifies claims against disk evidence (8 rails) | `agent-3-auditor.md` |
| 4 | Continuator | 5-pass expansion, merge→adapt→artifacts | `agent-4-continuation.md` |
| 5 | SCE Populator | Rules, vocabulary, synonyms, system prompts → SCE/ | `agent-5-sce-populator.md` |
| 6 | STE-Code Analysis | Paradigm-agnostic documentation + self-audit | `agent-6-phi-sce.md` |
| 7 | Level Worker | Parameterized: level 1-5, test/rewrite/benchmark | `agent-7-level-worker.md` |
| 8 | Extension Worker | Code-domain gap fillers (verbs, categories, anti-patterns) | `agent-8-extension-worker.md` |
| 9 | Translation | 9-locale discovery + blank placeholders | `agent-9-translations.md` |

## Launch Pattern

All agents follow the same launch pattern:

```bash
# Read the agent definition, execute it
hermes -z "$(cat .agents/agent/agent-N-role.md)" -m deepseek-v4-pro

# Or for parameterized agents:
hermes -z "level=3 action=rewrite target=ste-code/artifacts/ste-code-distilled-system-prompt.txt" -m deepseek-v4-pro
```

## Skills

Each agent loads skills from `.agents/skills/`:

| Skill | File | Used By |
|-------|------|---------|
| Extraction | `skills/extraction/SKILL.md` | Agent #1 |
| Refinement | `skills/refinement/SKILL.md` | Agent #2 |
| Merging | `skills/merging/SKILL.md` | Agent #4 |
| Adaptation | `skills/adaptation/SKILL.md` | Agent #4 |
| Artifacts | `skills/artifacts/SKILL.md` | Agent #4 |
| Auditing | `skills/auditing/SKILL.md` | Agent #3 |
| Validation | `skills/validation/SKILL.md` | Agent #1, #2 |
| Continuation | `skills/continuation/SKILL.md` | Agent #4 |
| Benchmarking | `skills/benchmarking/SKILL.md` | Agent #7 |
| Level Worker | `skills/level-worker/SKILL.md` | Agent #7 |
| Extension Worker | `skills/extension-worker/SKILL.md` | Agent #8 |
| Translations | `skills/translations/SKILL.md` | Agent #9 |
| State Report | `skills/state-report.md` | All agents |

## Communication

Agents communicate through `.agents/feedback/exchange.md` (turn-based).
State is tracked in `.agents/state/`. Audit reports are immutable in `.agents/audit/`.
