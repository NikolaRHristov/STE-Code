# STE-Code Agents — Benchmark & Pipeline

> **Project root:** `.agents/`  
> **Pipeline spec:** `ste-code/` (ASD-STE100 → STE-Code adaptation)  
> **Model:** `deepseek-v4-pro`  
> **Framework:** Hermes Agent v0.19.0

## Quick Navigation

| Directory | Purpose |
|-----------|---------|
| [`MASTER.md`](MASTER.md) | Full launch protocol, terminology, pipeline stages |
| [`README.md`](README.md) | Project overview |
| [`agent/`](agent/) | Agent role definitions (7 agents) |
| [`benchmark/`](benchmark/) | STE-Code benchmarking suite (59 tests, 14 categories) |
| [`prompts/`](prompts/) | Worker prompts (adapt, enrich, OSS, refine batches) |
| [`skills/`](skills/) | Agent skill definitions (extraction, refinement, adaptation, etc.) |
| [`references/`](references/) | Shared references (rails, quality checklist, worker grid) |
| [`uml/`](uml/) | Pipeline state machines, worker lifecycle diagrams |
| [`state/`](state/) | Progress tracking, migration plans |
| [`audit/`](audit/) | Execution auditor reports |
| [`scripts/`](scripts/) | Utility scripts (verification, prompt generation) |
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
| 5 | SCE Populator | Generates STE-Code dictionary entries |
| 6 | STE-Code Analysis | Paradigm-agnostic (OOP/FP/procedural/systems). Produces STE-Code compliant docs + self-audit |
| 7 | Level Worker | Parameterized worker. Receives level (1-5) + action (test/rewrite/benchmark), loads rules at that depth |
| 8 | Extension Worker | Generates code-domain extensions (verbs, adjectives, noun categories, anti-patterns) |
| 9 | Translation Orchestrator | Multi-locale translation pipeline for STE-Code docs. Placeholders only for now — sub-worker polled |
| 8 | Extension Worker | Generates code-domain gap fillers using batched poll workers. Dictionary entries, category examples, anti-patterns, domain extensions |

## Adaptation Levels

| Level | Content | Size | Use Case |
|-------|---------|------|----------|
| **1** | 14 core principles + synonym table | ~500 tokens | Interactive sessions, current default |
| **2** | + Top dictionary excerpt | ~5K tokens | Code review, PR feedback |
| **3** | + Section-specific grammar rules | ~20K tokens | Full document rewriting |
| **4** | + Complete dictionary (5,943 lines) | ~50K tokens | Strict compliance checking |
| **5** | Full standard (all 57 adapted files) | ~100K+ tokens | Specification-grade documentation |

## Benchmark Results (59 tests, 14 categories)

| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| **Pass rate** | 96.6% (57/59) | 11.9% (7/59) | **+84.7%** |
| **Avg score** | 0.919 | 0.471 | **+0.448** |

Top 3 categories where STE-Code wins hardest: **comments** (+0.580), **error messages** (+0.560), **config files** (+0.520).

## Key Artifacts

- `ste-code/artifacts/ste-code-distilled-system-prompt.txt` — Level 1 system prompt (50 lines)
- `ste-code/adapted/` — 57 files of ASD-STE100 rules adapted for code (9,400 lines)
- `ste-code/adapted/a-dictionary.md` — Full approved word dictionary (5,943 lines)
- `.agents/benchmark/orchestrator.py` — Parallel benchmark runner (59 workers, CWD-isolated)
- `.agents/benchmark/orchestrator-control.py` — Control group runner (plain assistant, no STE-Code)

## Running

```bash
# STE-Code benchmark (59 tests, parallel)
python3 .agents/benchmark/orchestrator.py

# Control group (plain assistant, same tests)
python3 .agents/benchmark/orchestrator-control.py

# Launch Agent #7 at a specific level
hermes -z "level=3 action=rewrite target=ste-code/artifacts/ste-code-distilled-system-prompt.txt" -m deepseek-v4-pro

# Launch 4 level workers (rewrites all docs at levels 1-4)
python3 .agents/benchmark/launch-levels.py
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
| Level Worker | `skills/level-worker/SKILL.md` | 4 parallel workers at levels 1-4 using oneshot wrapper |
| Extension Worker | `skills/extension-worker/SKILL.md` | Batched poll workers generating code-domain gap fillers |
| State Report | `skills/state-report.md` | Standardized pipeline state format |
