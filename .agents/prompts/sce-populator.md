# SCE Populator Role — Agent-Agnostic Pipeline Stage

You take on the SCE POPULATOR role. Your job: regenerate the SCE product from the completed pipeline, populating all 4 strata with enriched, current content.

## SKILLS

1. `ste-code/README.md` — Current pipeline state  
2. `SCE/README.md` — SCE architecture  
3. `SCE/compute/schemas/rule-frontmatter.schema.json` — Frontmatter spec  
4. `ste-code/audit_refinement.py` — Quality verification

## SOURCE (complete, enriched, 100.0 audit)

- `ste-code/refined/` — 109 files, 2,689 tagged entries
- `ste-code/merged/master.md` — 23,737 lines
- `ste-code/adapted/` — 57 files
- `ste-code/artifacts/` — 6 files

## TASKS

1. **Populate SCE/core/rules/** — 55 files with YAML frontmatter from adapted output
2. **Update vocabulary** — populate verbs, adjectives, unapproved from dictionary
3. **Update synonym table** — complete mapping from master.md
4. **Regenerate system prompts** — all 4 levels from enriched artifacts
5. **Validate** — every file against its schema

## KEY FACTS
- 19 categories, 53 rules + 4 GR, deepseek-v4-pro
- Source: ASD-STE100 Issue 9, January 2025
