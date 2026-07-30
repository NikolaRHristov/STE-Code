# Translation Discovery Grid — Dynamic

> **Status:** Discovery-based — this document tracks what's been found, not what should exist.
> **Last full scan:** Not yet performed
> **Locales:** zh-CN, ja, ko, es, fr, de, pt-BR, ru, ar (9 total)

## How Discovery Works

Workers explore source directories and **reason** about translatability. This grid is populated as discoveries happen — it's a running log, not a prescription. After each batch, discovered files get recorded here.

## Discovery Targets

| # | Target | Status | Last Scan |
|---|--------|--------|-----------|
| 1 | `ste-code/artifacts/` | ⬜ Pending | — |
| 2 | `ste-code/adapted/` | ⬜ Pending | — |
| 3 | `SCE/narratives/system-prompts/` | ⬜ Pending | — |
| 4 | `SCE/narratives/examples/` | ⬜ Pending | — |
| 5 | `SCE/core/rules/` | ⬜ Pending | — |
| 6 | `ste-code/v2/narratives/system-prompts/` | ⬜ Pending | — |
| 7 | `ste-code/v2/narratives/examples/` | ⬜ Pending | — |
| 8 | `ste-code/v2/core/rules/` | ⬜ Pending | — |
| 9 | `SCE/compute/prompts/` | ⬜ Pending | — |
| 10 | `ste-code/v2/compute/prompts/` | ⬜ Pending | — |

## Expected File Counts (from current disk state)

### ste-code/artifacts/ — 6 files expected
```
ste-code-distilled-system-prompt.txt
ste-code-self-reading-manual.txt
ste-code-extraction-methodology.txt
ste-code-example-turn.txt
ste-code-deployment-guide.txt
README.md
```

### ste-code/adapted/ — 57 files expected
```
a-dictionary.md
a-categories.md
a-sec1-rule1.1.md through a-sec1-rule1.14.md (14 files)
a-sec2-rule2.1.md through a-sec2-rule2.2.md (2 files)
a-sec3-rule3.1.md through a-sec3-rule3.7.md (7 files)
a-sec4-rule4.1.md through a-sec4-rule4.5.md (5 files)
a-sec5-rule5.1.md through a-sec5-rule5.5.md (5 files)
a-sec6-rule6.1.md through a-sec6-rule6.5.md (5 files)
a-sec7-rule7.1.md through a-sec7-rule7.3.md (3 files)
a-sec8-rule8.1.md through a-sec8-rule8.6.md (6 files)
a-sec9-rule9.1.md through a-sec9-rule9.4.md (4 files)
a-sec9-gr1.md through a-sec9-gr4.md (4 files)
```

### SCE/narratives/system-prompts/ — 4 files expected
```
ste-code-micro.md
ste-code-full.md
ste-code-agentic.md
ste-code-developer.md
```

### SCE/narratives/examples/ — 2 files expected
```
example-readme-section.md
example-commit-message.md
```

### SCE/core/rules/ — growing (1+ files expected)
Currently: `README.md`. More rules added as enrichment progresses.

### ste-code/v2/narratives/system-prompts/ — 4 files expected
```
ste-code-user.md
ste-code-micro.md
ste-code-developer.md
ste-code-agentic.md
```

### ste-code/v2/narratives/examples/ — 2 files expected
```
example-readme.md
example-commit-message.md
```

### ste-code/v2/core/rules/ — growing (3+ files expected)
Currently: `README.md`, `rule-1.1.md`, `rule-1.11.md`, `rule-1.12.md`

### SCE/compute/prompts/ — 2 files expected
```
rule-adaptation.prompt.md
compliance-check.prompt.md
```

### ste-code/v2/compute/prompts/ — 4 files expected
```
vocabulary-review.prompt.md
rule-adaptation.prompt.md
compliance-check.prompt.md
agentic-worker.prompt.md
```

## What Gets Skipped (no placeholders)

| File Pattern | Reason |
|-------------|--------|
| `*.schema.json` | JSON schema, structural |
| `*.py` | Python scripts, not translatable |
| `*worker-contract.json` | Agent configuration, structural |
| `*rails.json` | Agent configuration, structural |
| `*gate-conditions.json` | Agent configuration, structural |
| `*violation-severity-map.json` | Scoring config |
| `*compliance-rubric.json` | Scoring config |
| `*generated/*.json` (nouns-batch, verbs-batch, adjectives-batch, anti-patterns-batch) | Generated data — translate definitions only |
| `*verb-categories.json` | Category definitions (translate if prose, skip if structural IDs) |
| `*noun-categories.json` | Category definitions (translate if prose, skip if structural IDs) |

## Placeholder Directory Layout

```
translations/
├── catalog.md
├── zh-CN/
│   ├── ste-code/artifacts/*
│   ├── ste-code/adapted/*
│   ├── SCE/narratives/system-prompts/*
│   ├── SCE/narratives/examples/*
│   ├── SCE/core/rules/*
│   ├── SCE/compute/prompts/*
│   ├── ste-code-v2/narratives/system-prompts/*
│   ├── ste-code-v2/narratives/examples/*
│   ├── ste-code-v2/core/rules/*
│   └── ste-code-v2/compute/prompts/*
├── ja/ (same)
├── ko/ (same)
├── es/ (same)
├── fr/ (same)
├── de/ (same)
├── pt-BR/ (same)
├── ru/ (same)
└── ar/ (same)
```

Note: Paths use the source directory name as-is (e.g., `ste-code/`, `SCE/`, `ste-code-v2/`), not flattened.

## Batch Worker Assignments

Per discovery target, 3 workers × 3 locales each:

| Worker | Locales |
|--------|---------|
| W1 | zh-CN, ja, ko |
| W2 | es, fr, de |
| W3 | pt-BR, ru, ar |

All 3 workers explore the same source directory. Each creates placeholders for its 3 assigned locales.

## Re-Discovery Protocol

After any enrichment session:

1. Re-launch discovery on affected target(s)
2. Workers skip files that already have placeholders (check `test -f translations/<locale>/<path>` before creating)
3. Net-new files get fresh placeholders
4. Update this grid's status and last-scan timestamp
5. Update catalog.md with additions
