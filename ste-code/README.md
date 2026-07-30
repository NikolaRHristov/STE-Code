# STE-Code Pipeline

The five-stage pipeline is complete. Nine agents orchestrated 109 parallel workers to extract, refine, merge, adapt, and package the standard.

```
┌──────────────────────────────────────────────────────────────────┐
│ STAGE 1: EXTRACTION                  Agent #1                    │
│   Input:  spec/issue-09-2025/page-dir/page-*.md (426 pages)              │
│   Output: ste-code/extracted/w*-p*.md (109 files)               │
│   Status: ✅ Complete                                           │
├──────────────────────────────────────────────────────────────────┤
│ STAGE 2: REFINEMENT                  Agent #2                    │
│   Input:  ste-code/extracted/w*-p*.md                           │
│   Output: ste-code/refined/r*-p*.md (109 files)                 │
│   Quality: 100.0/100 audit score                                 │
│   Status: ✅ Complete                                           │
├──────────────────────────────────────────────────────────────────┤
│ STAGE 3: MERGE                                                  │
│   Input:  ste-code/refined/r*-p*.md                             │
│   Output: ste-code/merged/master.md (23,737 lines, 780KB)       │
│   Status: ✅ Complete                                           │
├──────────────────────────────────────────────────────────────────┤
│ STAGE 4: ADAPTATION                                              │
│   Input:  ste-code/merged/master.md                             │
│   Output: ste-code/adapted/ (57 files: 51 rules + 4 GR +        │
│           dictionary + categories)                               │
│   Status: ✅ Complete                                           │
├──────────────────────────────────────────────────────────────────┤
│ STAGE 5: ARTIFACTS                                               │
│   Input:  ste-code/adapted/                                     │
│   Output: ste-code/artifacts/ (5 levels, 4 system prompts)      │
│   Status: ✅ Complete                                           │
├──────────────────────────────────────────────────────────────────┤
│ BENCHMARKING + LEVEL ASSEMBLY         Agents #7, #8              │
│   Benchmark: 59 tests, 14 categories                             │
│   Result: 96.6% STE-Code vs 11.9% plain assistant               │
│   Levels: 1-4 assembled, 5 from pipeline                         │
│   Quality: 2 sweep passes, 0 FIXME, 0 CRLF, 0 stale refs        │
│   Status: ✅ Complete                                           │
└──────────────────────────────────────────────────────────────────┘
```

## Directory Map

| Directory | Stage | Contents |
|-----------|-------|----------|
| `extracted/` | 1 — Raw | 109 files from spec pages (page-dir/page-*.md) |
| `refined/` | 2 — Formatted | 109 files, 100.0 audit score |
| `merged/` | 3 — Consolidated | master.md (deduplicated) |
| `adapted/` | 4 — Code-adapted | 57 adapted rule, dictionary, and category files |
| `artifacts/` | 5 — Final output | Level 1-5 system prompts, sweep report |
| `data/` | Reference | Structured JSON (vocabulary, synonyms) |
| `templates/` | Reference | Additional system prompt templates |

## Agents

| # | Agent | Status |
|---|-------|--------|
| 1 | Extractor | ✅ 109 workers complete |
| 2 | Refiner | ✅ 100.0 audit score |
| 3 | Auditor | ✅ Full pipeline verified |
| 4 | Continuator | ✅ Resumes partial work |
| 5 | SCE Populator | ✅ Dictionary and vocabulary generation |
| 6 | STE-Code Analysis | ✅ Paradigm-agnostic adaptation |
| 7 | Level Worker | ✅ Parameterized (levels 1-5) |
| 8 | Extension Worker | ✅ Code-domain gap fillers |
| 9 | Translation Orchestrator | 🔄 Scaffolding complete, population pending |

## Quality

- 0 FIXME markers across all adapted and artifact files
- 0 CRLF line endings
- 0 stale references (53 rules, 22 categories)
- All rule cross-references verified
- Two quality sweep passes over 65 files
- Agent-agnostic tooling with configurable backends

## Assembly Scripts

All scripts in `.agents/tools/` are agent-agnostic. Configure backends in `.agents/config/agents.yaml`.

| Script | Purpose |
|--------|---------|
| `assemble-level1.py` | Compress Level 2 to Level 1 |
| `assemble-level2.py` | Compress Level 3 to Level 2 |
| `assemble-level3.py` | Assemble Level 3 from 51 Level 5 summaries |
| `assemble-level4.py` | Assemble Level 4 from 51 Level 5 summaries |
| `sweep-quality.py` | Parallel quality audit (5-batch) |
| `fix-fixmes.py` | Generate missing STE corrections |
| `agent-runner.py` | Generic agent execution (Hermes, Claude, Codex) |
