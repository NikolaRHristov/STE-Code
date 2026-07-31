# STE-Code Agent Tools

Hierarchical organization of all agent orchestration scripts.

## Directory Structure

```
.agents/tools/
├── lib/          # Core infrastructure
│   ├── _import_runner.py      # Import helper (exec into agent-runner.py)
│   ├── agent-runner.py        # Generic agent runner (Hermes, Claude, Codex)
│   └── hermes-oneshot-wrapper.py  # Hermes oneshot wrapper (no TUI)
│
├── shared/       # Shared utilities
│   ├── launch-worker.sh       # Shell launcher for agents
│   ├── telemetry-worker.py    # Telemetry wrapper for hermes -z
│   └── telemetry-worker.sh    # Shell convenience wrapper
│
├── runners/      # Pipeline phase runners (self-exec into agent)
│   ├── phase-a-gen.py         # Pre-generate Phase A prompts
│   ├── phase-a-run.py         # Extraction phase runner
│   ├── phase-b-run.py         # Refinement phase runner
│   ├── phase-b1-run.py        # Continuation refinement runner
│   ├── phase-c-run.py         # Merge phase runner
│   ├── phase-d-run.py         # Adaptation phase runner
│   └── phase-f-run.py         # Artifact generation runner
│
├── extraction/   # Spec page extraction pipeline
│   └── extract_batch.py       # Batch orchestrator (109 workers)
│
├── refinement/   # Level assembly + content generation
│   ├── assemble-level1.py     # Compress to ~1.2K tokens
│   ├── assemble-level2.py     # Compress to ~5K tokens
│   ├── assemble-level3.py     # Assemble ~20K token grammar prompt
│   ├── assemble-level4.py     # Assemble ~50K token standard prompt
│   ├── assemble-level4-parallel.py  # Parallel version of level4
│   ├── populate-level5.py     # Generate Level 5 summaries
│   ├── regenerate-level5.py   # Regenerate Level 5 summaries
│   └── generate-max-prompt.py # Generate max-size system prompt
│
├── maintenance/  # Content fixes and gap filling
│   ├── fix-fixmes.py          # Fix FIXME placeholder markers
│   ├── fix-ste-gaps.py        # Fill STE-Code content gaps
│   ├── fix-ste-run.py         # Fix STE compliance issues
│   ├── fix-nested-fences.py   # Fix nested code fence issues
│   ├── fill-gaps.py           # Generate missing Non-STE/STE pairs
│   ├── standardize-markers.py # Standardize example pair markers
│   └── scan-fences.py         # Scan for nested fence issues
│
├── quality/      # Quality auditing and verification
│   ├── check-tables.py        # Table integrity checker
│   ├── dogfood-audit.py       # Audit our docs against STE-Code
│   ├── ground-phase1.py       # Phase 1 grounding auditor
│   └── sweep-quality.py       # Parallel quality sweep
│
├── benchmark/    # Benchmark execution
│   └── bench-run.py           # Lightweight benchmark runner
│
├── .env.example  # Environment variable template
└── README.md     # This file
```

## Common Patterns

### Import Pattern
All scripts that need the agent runner use:
```python
PROJECT = Path(__file__).resolve().parent.parent.parent.parent
exec(open(PROJECT / ".agents" / "tools" / "lib" / "_import_runner.py").read())
# Provides: run_agent, launch_agent, get_agent_command
```

### CLI Pattern
All scripts accept `--agent`, `--model`, and `--dry-run` flags:
```
python3 .agents/tools/<category>/<script>.py [--agent hermes|claude|codex] [--dry-run]
```

### Batch Processing
Scripts that process multiple items accept batch parameters:
```
python3 .agents/tools/extraction/extract_batch.py [start_batch] [num_batches]
```

### Environment Variables
Copy `.env.example` to `.env` to override defaults:
- `STE_MODEL` — model name (default: `poolside/laguna-s-2.1:free`)
- `STE_MAX_WORKERS` — total workers (default: 109)
- `STE_PAGES_PER_WORKER` — pages per worker (default: 4)
- `STE_WORKERS_PER_BATCH` — workers per batch (default: 3)
- `STE_TOTAL_PAGES` — total spec pages (default: 434)
