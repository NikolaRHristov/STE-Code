# .agents — Agent-Agnostic Pipeline Skills

Role-based, self-contained skills for the STE-Code pipeline. Any agent can read any prompt or skill and act in that role.

## Structure

```
.agents/
├── AGENTS.md                     ← Full project documentation
├── README.md                     ← This file
├── agent/                        ← Agent definitions (7 agents)
│   ├── agent-1-extractor.md
│   ├── agent-2-refiner.md
│   ├── agent-3-auditor.md
│   ├── agent-4-continuation.md
│   ├── agent-5-sce-populator.md
│   ├── agent-6-phi-sce.md        ← Paradigm-agnostic analysis agent
│   └── agent-7-level-worker.md   ← Parameterized level worker
├── benchmark/                    ← STE-Code benchmark suite
│   ├── SKILL.md                  ← Benchmark orchestrator prompt
│   ├── schema.json               ← JSON schema for tests/results
│   ├── orchestrator.py           ← STE-Code parallel runner
│   ├── orchestrator-control.py   ← Control group runner
│   ├── run-benchmark.sh          ← Shell runner (legacy)
│   ├── rescore.py                ← Re-scoring utility
│   ├── test-cases/               ← 14 category files, 59 tests
│   ├── results/                  ← STE-Code benchmark results
│   ├── results-control/          ← Control group results
│   └── examples/                 ← Generated code examples
├── prompts/                      ← Role-based agent prompts
│   ├── extractor.md
│   ├── refiner.md
│   ├── auditor.md
│   ├── continuator.md
│   ├── sce-populator.md
│   ├── adapt/                    ← Adaptation phase prompts
│   ├── enrich/                   ← Enrichment phase prompts
│   ├── refine/                   ← Refinement batch prompts
│   └── oss/                      ← Open-source doc prompts
├── skills/                       ← Capability skills
│   ├── extraction/SKILL.md
│   ├── refinement/SKILL.md
│   ├── auditing/SKILL.md
│   ├── merging/SKILL.md
│   ├── adaptation/SKILL.md
│   ├── artifacts/SKILL.md
│   ├── benchmarking/SKILL.md
│   ├── validation/SKILL.md
│   ├── continuation/
│   └── spec-extraction/          ← Full extraction pipeline skills
├── references/                   ← Shared reference data
│   ├── worker-grid.md
│   ├── section-types.md
│   ├── quality-checklist.md
│   ├── rails.md
│   ├── category-mapping.md
│   └── STE-CODE-IMPLEMENTATION.md
├── uml/                          ← Pipeline diagrams
├── state/                        ← Progress tracking
├── audit/                        ← Auditor reports
├── scripts/                      ← Utility scripts
└── feedback/                     ← Inter-agent communication
```

## Quick Reference

| Task | Command |
|------|---------|
| Run STE-Code benchmark | `python3 .agents/benchmark/orchestrator.py` |
| Run control group | `python3 .agents/benchmark/orchestrator-control.py` |
| Re-score existing outputs | `python3 .agents/benchmark/rescore.py` |
| Launch Agent #7 at Level 3 | `hermes -z "level=3 action=rewrite target=..."` |

## Adaptation Levels

| Level | Content | Tokens |
|-------|---------|--------|
| 1 | 14 principles + synonym table | ~500 |
| 2 | + Top dictionary excerpt | ~5K |
| 3 | + Section-specific grammar | ~20K |
| 4 | + Full dictionary | ~50K |
| 5 | Full standard | ~100K+ |

## Benchmark Results

**STE-Code: 96.6% pass rate (57/59)** vs Plain Assistant: 11.9% (7/59). +84.7% improvement.
