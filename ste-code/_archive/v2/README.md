# STE-Code v2 — Multi-Strata Architecture

> **Version:** 2.0.0-alpha  
> **Source:** ASD-STE100 Issue 9, September 2025 (434 pages)  
> **Pipeline:** 5-stage agent extraction (v1 complete at `21bda7fa`)

The v2 architecture splits the STE-Code standard into four composable strata so that LLMs, developers, CI tools, and human readers can each load exactly what they need — nothing more.

---

## Directory Map

```
ste-code/v2/
├── core/           # Static: immutable rules + category definitions
│   ├── rules/      # One file per rule, YAML frontmatter + markdown body
│   └── categories/ # noun-categories.json, verb-categories.json
├── data/           # Variable: living vocabulary lists, synonym table
│   ├── vocabulary/ # approved-nouns.json, approved-verbs.json, etc.
│   ├── synonyms/   # synonym-table.json
│   └── exceptions/ # domain-extensions.json
├── compute/        # Computable: schemas, checklists, rails, scoring, prompts
│   ├── schemas/    # JSON Schema files for validation
│   ├── checklists/ # Boolean gate checks for CI and agents
│   ├── scoring/    # Compliance rubric, severity map
│   ├── agentic/    # Rails, gate conditions, worker contract
│   └── prompts/    # Parameterized prompt templates with {{variables}}
└── narratives/     # Readable: assembled docs for humans and LLMs
    ├── system-prompts/  # full, micro (2KB), agentic-only, user, developer
    ├── examples/        # example-readme, commit-message, api-doc, inline-comment
    └── self-reading/    # self-reading-manual
```

---

## Loading Strategy by Consumer

| Consumer | Load These Files |
|----------|------------------|
| LLM — full compliance check | `narratives/system-prompts/ste-code-full.md` + `data/synonyms/synonym-table.json` |
| LLM — small context window | `narratives/system-prompts/ste-code-micro.md` |
| LLM — pipeline agent (rails only) | `narratives/system-prompts/ste-code-agentic.md` + `compute/agentic/rails.json` |
| Developer extending the standard | `narratives/system-prompts/ste-code-developer.md` + `core/rules/` + `compute/schemas/` |
| Human user learning the standard | `narratives/system-prompts/ste-code-user.md` + `narratives/examples/` |
| CI linter / validator tool | `data/vocabulary/` + `compute/checklists/` + `compute/schemas/` |
| Agentic pipeline (GATE logic) | `compute/agentic/gate-conditions.json` + `compute/agentic/worker-contract.json` |

---

## Design Principles

1. **One truth per file** — each file has a single, clear responsibility
2. **Domain-tagged** — every vocabulary entry carries `domain` tags for selective loading
3. **Schema-validated** — every JSON file has a corresponding JSON Schema in `compute/schemas/`
4. **Frontmatter-indexed** — every rule file has YAML frontmatter for programmatic querying
5. **Composable prompts** — prompt templates use `{{variable}}` slots, never hardcoded values
6. **Strata never cross-contaminate** — `core/` never imports from `data/`, narratives are assembled not authored
7. **Agentic rails are isolated** — behavioral constraints in `compute/agentic/` are separate from content rules
