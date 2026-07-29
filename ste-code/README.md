# STE-Code Pipeline

Semantically separated stages. Each stage's output feeds the next.

```
┌─────────────────────────────────────────────────────────────┐
│ STAGE 1: EXTRACTION                  Session 2 (orchestrator) │
│   Input:  spec/issue-09-2025/page-*.md (434 pages)           │
│   Output: ste-code/extracted/w*-p*.md (109 files)             │
│   Status: 🟢 Running — 12/109 workers done                    │
├─────────────────────────────────────────────────────────────┤
│ STAGE 2: REFINEMENT                  Session 3 (orchestrator) │
│   Input:  ste-code/extracted/w*-p*.md                         │
│   Output: ste-code/refined/r*-p*.md (109 files)               │
│   Status: 🟢 Running — 14/109 workers done                    │
├─────────────────────────────────────────────────────────────┤
│ STAGE 3: MERGE                      (after stages 1+2 done)   │
│   Input:  ste-code/refined/r*-p*.md (or extracted if no refine)│
│   Output: ste-code/merged/master.md                           │
│   Status: ⬜ Pending                                           │
├─────────────────────────────────────────────────────────────┤
│ STAGE 4: ADAPTATION                 (after merge complete)     │
│   Input:  ste-code/merged/master.md                           │
│   Output: ste-code/adapted/ (rule-by-rule STE→STE-Code)       │
│   Status: ⬜ Pending                                           │
├─────────────────────────────────────────────────────────────┤
│ STAGE 5: ARTIFACTS                  (after adaptation done)    │
│   Input:  ste-code/adapted/                                   │
│   Output: ste-code/artifacts/ (6 final .txt files)            │
│   Status: ⬜ Pending                                           │
├─────────────────────────────────────────────────────────────┤
│ CROSS-CUTTING: AUDIT                Hidden agent              │
│   Watches: All stages                                         │
│   Output: ste-code/audit/audit-*.md                           │
│   Status: ⬜ Ready to launch                                   │
└─────────────────────────────────────────────────────────────┘
```

## Directory Map

| Directory | Stage | Contents |
|-----------|-------|----------|
| `extracted/` | 1 — Raw extraction | 109 files, one per 4-page batch |
| `refined/` | 2 — Formatted | 109 files, cleaned markdown |
| `prompts-refine/` | 2 — Worker prompts | 109 prompt files for refinement workers |
| `merged/` | 3 — Consolidated | master.md (deduplicated, organized) |
| `adapted/` | 4 — Code-adapted | Rule-by-rule STE→STE-Code transformations |
| `artifacts/` | 5 — Final output | 6 .txt files (system prompt, manual, etc.) |
| `audit/` | Cross-cutting | Immutable audit reports |
