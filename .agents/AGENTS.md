# STE-Code Agents — Benchmark & Pipeline

> **Project root:** `.agents/`
> **Pipeline spec:** `ste-code/` (ASD-STE100 → STE-Code adaptation)
> **Default agent:** Hermes (configured in `.agents/config/agents.yaml`)
> **Framework:** Agent-agnostic (pre-configured for Hermes, supports Claude, Codex, custom)

## Agent Runner
All scripts use the **agent-agnostic runner** at `.agents/tools/lib/agent-runner.py`.
Configure backends in `.agents/config/agents.yaml`. The default model is
declared there and surfaced to every stage through `ste_config` (`CFG.model`) —
it is never hardcoded in a script.

```bash
# Use default agent (Hermes)
python3 .agents/tools/refinement/assemble-level1.py

# Use a different agent
python3 .agents/tools/refinement/assemble-level1.py --agent claude

# List available agents
python3 .agents/tools/lib/agent-runner.py --list
```

Adding a new agent: edit `.agents/config/agents.yaml` and add your backend.

## Configuration (one source of truth)
Tunables live in config, not in code:
- `.agents/config/defaults.yaml` — shared `agent:` and `runtime:` knobs.
- `.agents/tools/<unit>/config.yaml` — each stage's footprint; merged under
  defaults so the unit always wins.
- Stages read `ste_config.load(__file__)` for footprint + `ste_runtime.resolve`
  for pre-flight knobs (wrapper path, retry count, batch divisor, encoding).

## Quick Navigation
| Directory | Purpose |
|-----------|---------|
| `MASTER.md` | Full launch protocol, terminology, pipeline stages |
| `README.md` | Project overview |
| `config/` | Agent backend + shared defaults (`agents.yaml`, `defaults.yaml`) |
| `benchmark/` | STE-Code benchmarking suite (59 tests, 14 categories) |
| `prompts/`, `*/templates/` | Worker prompts (externalized) |
| `skills/` | Agent skill definitions |
| `references/` | Shared references (rails, worker grid) |
| `tools/` | Orchestration scripts (one unit per stage; each owns `config.yaml` + `README.md`) |
| `feedback/` | Inter-agent communication |

## Pipeline Stages
```
Extraction → Refinement → Merge → Adaptation → Artifacts
(.extracted/)  (.refined/) (.merged/) (.adapted/) (.artifacts/)
```
Run order for the consolidation pipeline: A → B → (B1) → C → D → E → F.

## Agents
| # | Agent | Role |
|---|-------|------|
| 1 | Extractor | Reads spec pages, extracts raw text |
| 2 | Refiner | Reformats extracted text into clean markdown |
| 3 | Auditor | Verifies claims against disk evidence |
| 4 | Continuator | Resumes partial/incomplete work |
| 5 | SCE Populator | Generates STE-Code structured data |
| 6 | STE-Code Analysis | Paradigm-agnostic; produces STE-Code compliant docs + self-audit |
| 7 | Level Worker | Parameterized worker (level 1-5 + action) |
| 8 | Extension Worker | Generates code-domain gap fillers |
| 9 | Translation Orchestrator | Discovery-based locale scaffolding |

## Adaptation Levels
| Level | Content | Size | Tokens |
|-------|---------|------|--------|
| -2 | 14 core principles only | 5 KB | ~1.2K |
| -1 | + synonym table | 26 KB | ~5.9K |
| 0 | + short dictionary excerpt | 17 KB | ~4.3K |
| 1 | + doc templates | 58 KB | ~14.5K |
| 2 | + section-specific grammar | 75 KB | ~18.5K |
| 3 | + complete dictionary + all 54 rules | 388 KB | ~95K |
| 4 | + extensions + reference catalogue | 462 KB | ~116K |
| 5 | Full standard + provenance | 539 KB | ~134K |

Measured with `python3 .agents/tools/maintenance/measure_artifacts.py`
(o200k_base tokenizer). Rule of thumb: ~0.24 tokens per byte of UTF-8 markdown.

## Assembly Scripts (all agent-agnostic)
| Script | Input | Output | Description |
|--------|-------|--------|-------------|
| `assemble-level1.py` | Level 2 | Level 1 (~14.5K) | Compress to essential principles |
| `assemble-level2.py` | Level 3 | Level 2 (~18.5K) | Compact compliance prompt |
| `assemble-level3.py` | 54× Level 5 | Level 3 (~95K) | Section grammar + vocabulary |
| `assemble-level4.py` | 54× Level 5 | Level 4 (~116K) | All rules + dictionary excerpt |
| `sweep-quality.py` | All artifacts | Sweep report | 5-batch parallel quality audit |
| `fix-fixmes.py` | Adapted files | Fixed files | Generate missing STE corrections |

All accept `--agent <name>` and `--dry-run`.

## Benchmark Results (59 tests, 14 categories)
| | STE-Code | Plain Assistant | Improvement |
|---|----------|-----------------|-------------|
| **Pass rate** | 96.6% (57/59) | 11.9% (7/59) | **+84.7%** |
| **Avg score** | 0.919 | 0.471 | **+0.448** |

Top categories where STE-Code wins hardest: **comments** (+0.580), **error
messages** (+0.560), **config files** (+0.520).

## Key Artifacts
- `ste-code/artifacts/level{1..5}/system-prompt.txt` — distilled levels.
- `ste-code/adapted/` — 60 files of ASD-STE100 rules adapted for code.
- `.agents/benchmark/orchestrator.py` — Parallel benchmark runner (59 workers).
- `.agents/benchmark/orchestrator-control.py` — Control group runner.

## Running
```bash
# Assemble level prompts (default: hermes)
python3 .agents/tools/refinement/assemble-level3.py
python3 .agents/tools/refinement/assemble-level2.py
python3 .agents/tools/refinement/assemble-level1.py

# Quality sweep (5 parallel batches)
python3 .agents/tools/quality/sweep-quality.py --batches 5

# STE-Code benchmark (59 tests, parallel)
python3 .agents/benchmark/orchestrator.py
```

## Contributing
See `GAPS.md` for the domain coverage gap analysis. Pick a domain tag, find the
target rule in `ste-code/adapted/a-secN-ruleX.Y.md`, add Non-STE/STE pairs in
the canonical format, submit a PR with the domain tag.

## Feedback & Lessons Learned
- `feedback/exchange.md` — Project-specific adaptations.
- `feedback/poll-vs-wait.md` — Use `process(action='poll')`, never blocking waits.
- `feedback/aphrodite-tool-testing.md` — On `<<<CCR:hash|type|size>>>` markers,
  call `aphrodite_retrieve(hash=...)` immediately; never re-read the file.

## See also
- `README.md` — structure + stage table.
- `tools/lib/README.md` — shared helper reference.
- `config/defaults.yaml` — shared agent + runtime defaults.
