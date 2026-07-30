# Agent State Report — STE-Code Pair Count Comparison

## Role
- **Role**: Benchmarking Orchestrator / Agent #4
- **Last action**: Counted all example pairs and vocabulary entries across original ASD-STE100 and STE-Code adaptation

## Pipeline Status

| Stage | Directory | Files | Status |
|-------|-----------|-------|--------|
| 1 — Extract | extracted/ | 109 | ✅ |
| 2 — Refine | refined/ | 109 | ✅ |
| 3 — Merge | merged/ | 2 (20,794 lines) | ✅ |
| 4 — Adapt | adapted/ | 57 | ✅ Expanding |
| 5 — Artifacts | artifacts/ | 6 | ✅ |

## Pair Count Comparison

| Dimension | Aerospace (Original) | STE-Code (Ours) | Coverage |
|-----------|:---:|:---:|:---:|
| **STE/non-STE example pairs** | 4,945 (in master.md) | 1,212 (in adapted dictionary) | 24.5% |
| **Dictionary entries** | 2,206 | 175 (code-dictionary.json) | 7.9% |
| **Synonym pairs** | ~900 (word-level) | 30 (condensed) | 3.3% |
| **Anti-patterns** | Embedded in rules | 15 (5 structural + 10 code) | N/A |
| **Noun categories** | ~10 (aerospace) | 19 (with 289 examples) | 190% |
| **Approved verbs** | ~875 (in dictionary) | 65 (35 core + 15 gen + 15 dict) | 7.4% |
| **Approved adjectives** | ~1,400 (in dictionary) | 30 (20 core + 10 gen) | 2.1% |

## Expanded Breakdown (SCE)

| Component | Count | File |
|-----------|:---:|------|
| Canonical synonym pairs | 30 | `SCE/core/categories/synonym-table.json` |
| Code dictionary verbs | 50 | `SCE/data/vocabulary/code-dictionary.json` |
| Code dictionary adjectives | 20 | `SCE/data/vocabulary/code-dictionary.json` |
| Code dictionary concepts | 20 | `SCE/data/vocabulary/code-dictionary.json` |
| Noun category examples | 289 | `SCE/data/vocabulary/code-dictionary.json` |
| Generated verbs | 15 | `SCE/data/vocabulary/generated/verbs-batch-001.json` |
| Generated adjectives | 10 | `SCE/data/vocabulary/generated/adjectives-batch-001.json` |
| Generated anti-patterns | 10 | `SCE/compute/generated/anti-patterns-batch-001.json` |
| Generated category terms | 190 | `SCE/core/categories/generated/nouns-batch-001.json` |
| Adapted rule files | 55 | `ste-code/adapted/` |
| **Total unique entries** | **~700** | |

## Gap Analysis

| Area | Gap | Expansion Target |
|------|-----|-----------------|
| Example pairs | 4,945 → 1,212 | Need 3,733 more code examples (Pass 1) |
| Dictionary entries | 2,206 → 175 | Need ~2,000 code-domain equivalents (Pass 2) |
| Verb entries | 875 → 65 | Need ~800 more approved verbs |
| Adjective entries | 1,400 → 30 | Need ~1,300 more approved adjectives |
| Anti-patterns | N/A → 15 | Need 30+ more code-specific anti-patterns |

## Next Actions (prioritized)
1. Launch Agent #4 Pass 1: Generate 3,733 code example pairs
2. Launch Agent #4 Pass 2: Map 2,000 aerospace→code dictionary entries
3. Launch Agent #4 Pass 3: Expand category examples
4. Launch Agent #4 Pass 4: Expand anti-patterns
5. Launch Agent #4 Pass 5: Paradigm examples
6. Regenerate Stage 5 artifacts with expanded content
