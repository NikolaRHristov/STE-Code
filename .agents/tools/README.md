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
├── runners/      # Pipeline phase runners (stages A-F)
│   ├── phase-a-gen.py         # Pre-generate Phase A prompts
│   ├── phase-a-run.py         # A: extraction runner
│   ├── phase-b-run.py         # B: refinement runner
│   ├── phase-b1-run.py        # B1: continuation / redo refinement runner
│   ├── phase-c-run.py         # C: grouping runner (deterministic)
│   ├── phase-d-run.py         # D: adaptation runner
│   ├── phase-e-run.py         # E: extension (gap-fill) runner
│   ├── phase-f-run.py         # F: artifact assembly runner (deterministic)
│   ├── launch-downstream.sh   # Runs C -> D -> E -> F
│   └── templates/             # Externalized worker prompts
│
├── extraction/   # Spec page extraction pipeline
│   └── extract_batch.py       # Batch orchestrator (109 workers)
│
├── grouping/     # Stage C — deterministic grouping (no LLM)
│   ├── group_engine.py        # Plan + parity primitives (single source of truth)
│   ├── group_batch.py         # Assembler: refined/ -> grouped/ (24 groups)
│   ├── dict_normalize.py      # Dictionary page -> one 4-column table
│   └── verify-groups.py       # Post-assembly gate (coverage, parity, marks)
│
├── adaptation/   # Stage D — STE -> STE-Code adaptation
│   ├── adapt_batch.py         # Orchestrator: one worker per rule section
│   └── verify-adaptation.py   # Gate: aerospace leakage, synonyms, coverage
│
├── extension/    # Stage E — gap-fill extensions (markdown first)
│   ├── extend_batch.py        # Orchestrator: six gap areas
│   ├── md_to_json.py          # Deterministic markdown -> JSON derivation
│   └── verify_extensions.py   # Gate: six deterministic checks
│
├── artifacts/    # Stage F — final assembly (no LLM)
│   ├── artifact_batch.py      # adapted/ -> ste-code-rules.md + system prompt
│   └── verify-artifacts.py    # Gate: rule coverage, no drops or duplicates
│
├── continuation/ # Redo queue for incomplete refined pages (B1)
│   ├── continue_batch.py      # Re-processes a queue with checkpoint + commit
│   └── verify_continuation.py # Finds incomplete pages, writes the queue
│
├── refinement/   # Level assembly + content generation
│   ├── assemble-level1.py     # Compress to ~1.2K tokens
│   ├── assemble-level2.py     # Compress to ~5K tokens
│   ├── assemble-level3.py     # Assemble ~20K token grammar prompt
│   ├── assemble-level4.py     # Assemble ~50K token standard prompt
│   ├── assemble-level4-parallel.py  # Parallel version of level4
│   ├── populate-level5.py     # Generate Level 5 summaries
│   ├── regenerate-level5.py   # Regenerate Level 5 summaries
│   ├── generate-max-prompt.py # Generate max-size system prompt
│   ├── generate_expansion_prompts.py # Generate expansion worker prompts
│   └── generate_refinement_prompts.py # Generate refinement worker prompts
│
├── maintenance/  # Content fixes and gap filling
│   ├── fix-fixmes.py          # Fix FIXME placeholder markers
│   ├── fix-ste-gaps.py        # Fill STE-Code content gaps
│   ├── fix-ste-run.py         # Fix STE compliance issues
│   ├── fix-nested-fences.py   # Fix nested code fence issues
│   ├── fill-gaps.py           # Generate missing Non-STE/STE pairs
│   ├── standardize-markers.py # Standardize example pair markers
│   ├── scan-fences.py         # Scan for nested fence issues
│   └── generate_maturity_fix_prompts.py # Generate maturity fix prompts
│
├── quality/      # Quality auditing and verification
│   ├── check-tables.py        # Table integrity checker
│   ├── check-rails.py         # 8-rail quality compliance checker
│   ├── dogfood-audit.py       # Audit our docs against STE-Code
│   ├── ground-phase1.py       # Phase 1 grounding auditor
│   ├── sweep-quality.py       # Parallel quality sweep
│   ├── verify-batch.sh        # Batch verification script
│   ├── _check_md.py           # Markdown format checker (basic)
│   ├── _check_md2.py          # Markdown format checker (heading check)
│   └── _check_md3.py          # Markdown format checker (tables)
│
├── benchmark/    # Benchmark execution
│   └── bench-run.py           # Lightweight benchmark runner
│
├── .env.example  # Environment variable template
└── README.md     # This file
```

> **Note:** Scripts previously in `.agents/scripts/` have been moved into the
> appropriate subdirectories above. The `scripts/` directory has been retired.

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
- `STE_MODEL` — model name (default: `tencent/hy3:free`)
- `STE_MAX_WORKERS` — total workers (default: 109)
- `STE_PAGES_PER_WORKER` — pages per worker (default: 4)
- `STE_WORKERS_PER_BATCH` — workers per batch (default: 3)
- `STE_TOTAL_PAGES` — total spec pages (default: 434)
