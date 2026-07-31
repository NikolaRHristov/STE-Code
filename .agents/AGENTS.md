# STE-Code Agents — Benchmark & Pipeline

> **Project root:** `.agents/`  
> **Pipeline spec:** `ste-code/` (ASD-STE100 → STE-Code adaptation)  
> **Default agent:** Hermes (`poolside/laguna-s-2.1:free`)  
> **Framework:** Agent-agnostic (pre-configured for Hermes, supports Claude, Codex, custom)

## Agent Runner

All scripts use the **agent-agnostic runner** at `.agents/tools/lib/agent-runner.py`.
Configure backends in `.agents/config/agents.yaml`. Default: Hermes with `poolside/laguna-s-2.1:free`.

```bash
# Use default agent (Hermes)
python3 .agents/tools/refinement/assemble-level1.py

# Use a different agent
python3 .agents/tools/refinement/assemble-level1.py --agent claude

# List available agents
python3 .agents/tools/lib/agent-runner.py --list

# Shell launcher (agent-agnostic)
.agents/tools/shared/launch-worker.sh prompt.txt --agent hermes --model poolside/laguna-s-2.1:free out.txt
```

Adding a new agent: edit `.agents/config/agents.yaml` and add your backend.

## Quick Navigation

| Directory | Purpose |
|-----------|---------|
| [`MASTER.md`](MASTER.md) | Full launch protocol, terminology, pipeline stages |
| [`README.md`](README.md) | Project overview |
| [`config/`](config/) | Agent backend configuration (`agents.yaml`) |
| [`agent/`](agent/) | Agent role definitions (9 agents) |
| [`benchmark/`](benchmark/) | STE-Code benchmarking suite (59 tests, 14 categories) |
| [`prompts/`](prompts/) | Worker prompts (adapt, enrich, OSS, refine batches) |
| [`skills/`](skills/) | Agent skill definitions (extraction, refinement, adaptation, etc.) |
| [`references/`](references/) | Shared references (rails, quality checklist, worker grid) |
| [`uml/`](uml/) | Pipeline state machines, worker lifecycle diagrams |
| [`state/`](state/) | Progress tracking, migration plans |
| [`audit/`](audit/) | Execution auditor reports |
| `tools/quality/` | Quality checking (rails, tables, verification) |
| `tools/refinement/` | Level assembly (prompts, levels 1-4) |
| `tools/maintenance/` | Content fixes and gap filling |
| `tools/benchmark/` | Benchmark execution |
| `tools/runners/` | Pipeline phase runners |
| `tools/lib/` | Core infrastructure |
| `tools/shared/` | Shared utilities |
| [`feedback/`](feedback/) | Inter-agent communication |

## Pipeline Stages (5-stage)

```
Extraction → Refinement → Merge → Adaptation → Artifacts
(.extracted/)  (.refined/) (.merged/) (.adapted/) (.artifacts/)
```

## Agents

| # | Agent | Role |
|---|-------|------|
| 1 | Extractor | Reads spec pages, extracts raw text |
| 2 | Refiner | Reformats extracted text into clean markdown |
| 3 | Auditor | Verifies claims against disk evidence |
| 4 | Continuator | Resumes partial/incomplete work |
| 5 | SCE Populator | Generates STE-Code structured data (vocabulary, templates, schemas) |
| 6 | STE-Code Analysis | Paradigm-agnostic (OOP/FP/procedural/systems). Produces STE-Code compliant docs + self-audit |
| 7 | Level Worker | Parameterized worker. Receives level (1-5) + action (test/rewrite/benchmark), loads rules at that depth |
| 8 | Extension Worker | Generates code-domain gap fillers using batched poll workers. Dictionary entries, category examples, anti-patterns, domain extensions |
| 9 | Translation Orchestrator | Discovery-based locale scaffolding. Blank placeholders for all translatable content across 9 locales |

## Adaptation Levels

| Level | Content | Size | Use Case |
|-------|---------|------|----------|
| **1** | 14 core principles + synonym table | ~1.2K tokens | Interactive sessions, low-context scenarios |
| **2** | + Top dictionary excerpt + doc templates | ~4.5K tokens | Code review, PR feedback |
| **3** | + Section-specific grammar rules | ~8K tokens | Full document rewriting |
| **4** | + Complete dictionary excerpt + all 51 rules | ~45K tokens | Strict compliance checking |
| **5** | Full standard (all 51 rule summaries) | ~100K+ tokens | Specification-grade documentation |

## Assembly Scripts (all agent-agnostic)

| Script | Input | Output | Description |
|--------|-------|--------|-------------|
| `assemble-level1.py` | Level 2 | Level 1 (~1.2K) | Compress to essential principles |
| `assemble-level2.py` | Level 3 | Level 2 (~4.5K) | Compact compliance prompt |
| `assemble-level3.py` | 51× Level 5 | Level 3 (~8K) | Section grammar + vocabulary |
| `assemble-level4.py` | 51× Level 5 | Level 4 (~45K) | All rules + dictionary excerpt |
| `sweep-quality.py` | All artifacts | Sweep report | 5-batch parallel quality audit |
| `fix-fixmes.py` | Adapted files | Fixed files | Generate missing STE corrections |

All accept `--agent <name>` to use a different backend and `--dry-run` to preview.

## Benchmark Results (59 tests, 14 categories)

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| **Pass rate** | 96.6% (57/59) | 11.9% (7/59) | **+84.7%** |
| **Avg score** | 0.919 | 0.471 | **+0.448** |

Top 3 categories where STE-Code wins hardest: **comments** (+0.580), **error messages** (+0.560), **config files** (+0.520).

## Key Artifacts

- `ste-code/artifacts/level1/system-prompt.txt` — Level 1: 14 principles (~1.2K tokens)
- `ste-code/artifacts/level2/system-prompt.txt` — Level 2: 20 principles + dictionary (~4.5K tokens)
- `ste-code/artifacts/level3/system-prompt.txt` — Level 3: 9-section grammar (~8K tokens)
- `ste-code/artifacts/level4/system-prompt.txt` — Level 4: 51 rules + dictionary (~45K tokens)
- `ste-code/adapted/` — 57 files of ASD-STE100 rules adapted for code
- `.agents/benchmark/orchestrator.py` — Parallel benchmark runner (59 workers, CWD-isolated)
- `.agents/benchmark/orchestrator-control.py` — Control group runner (plain assistant, no STE-Code)

## Running

```bash
# Assemble level prompts (default: hermes)
python3 .agents/tools/refinement/assemble-level3.py
python3 .agents/tools/refinement/assemble-level2.py
python3 .agents/tools/refinement/assemble-level1.py

# Use a different agent
python3 .agents/tools/refinement/assemble-level1.py --agent claude

# Quality sweep (5 parallel batches)
python3 .agents/tools/quality/sweep-quality.py --batches 5

# STE-Code benchmark (59 tests, parallel)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, same tests)
python3 .agents/benchmark/orchestrator-control.py

# List available agent backends
python3 .agents/tools/lib/agent-runner.py --list
```

## Contributing

See [`.agents/GAPS.md`](GAPS.md) for the full domain coverage gap analysis.

### Quick Start
1. Pick a domain tag from GAPS.md (e.g., `[MOBILE]`, `[ML]`, `[SEC]`)
2. Find the target rule file in `ste-code/adapted/a-secN-ruleX.Y.md`
3. Add Non-STE/STE example pairs using canonical format:
   ```
   > [DOMAIN: mobile]  <!-- tracking placeholder -->
   > **Non-STE:** [realistic code documentation from the domain]
   > **STE:** [STE-Code compliant correction]
   ```
4. Submit a PR with the domain tag in the commit message.

### Domain Placeholders
Active placeholder tags in adapted files mark where domain content belongs:
- `[CONTRIBUTE]` — General contribution welcome
- `[MOBILE]`, `[ML]`, `[GAMEDEV]`, `[EMBEDDED]`, `[WEB3]` — Zero coverage domains
- `[SEC]`, `[A11Y]`, `[I18N]`, `[PERF]`, `[TEST]`, `[DOCS]` — High-priority gaps

### Batch Generation (Internal)
```bash
# Generate domain examples across rules
python3 .agents/tools/maintenance/fill-gaps.py --domain MOBILE --rule a-sec4-rule4.3
python3 .agents/tools/maintenance/fill-gaps.py --domain ML --all-rules --min-pairs 3
```

## Skills Inventory

| Skill | File | Description |
|-------|------|-------------|
| Extraction | `skills/extraction/SKILL.md` | 109 parallel workers, 4 pages each, 37 batches |
| Refinement | `skills/refinement/SKILL.md` | 9 formatting rules, section-aware v2 workers |
| Merging | `skills/merging/SKILL.md` | Concatenate, deduplicate, organize 109 files |
| Adaptation | `skills/adaptation/SKILL.md` | 53 rules → code domain, 19 categories |
| Artifacts | `skills/artifacts/SKILL.md` | 6 deployable files, quality gates |
| Auditing | `skills/auditing/SKILL.md` | 8-rail verification, fabrication detection |
| Validation | `skills/validation/SKILL.md` | Per-batch quality checks, spot-checks |
| Continuation | `skills/continuation/SKILL.md` | Multi-agent stages 3-5, any agent perspective |
| Benchmarking | `skills/benchmarking/SKILL.md` | 59 tests, 14 categories, control group |
| Level Worker | `skills/level-worker/SKILL.md` | 4 parallel workers at levels 1-4 using agent runner |
| Extension Worker | `skills/extension-worker/SKILL.md` | Batched poll workers generating code-domain gap fillers |
| Translations | `skills/translations/SKILL.md` | Multi-locale placeholder pipeline, 9 locales, ~540 files, batch-of-3 workers |
| State Report | `skills/state-report.md` | Standardized pipeline state format |
