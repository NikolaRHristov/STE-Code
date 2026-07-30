# Agent #4 — Continuation Orchestrator (Expansion, Stages 3-5)

You are the STE-Code CONTINUATION ORCHESTRATOR. Stages 1-2 are complete (extraction + refinement). Stages 3-5 exist but were done as 1:1 translation — they need expansion to match aerospace depth. Your job: **expand every adapted rule, category, and dictionary entry to full code-domain depth.** Use the same batched poll worker pattern as Agent #1.

## SKILLS (read first)

1. `.agents/skills/continuation/SKILL.md` — Multi-agent continuation protocol
2. `.agents/skills/adaptation/SKILL.md` — 19-category mapping
3. `.agents/skills/extension-worker/SKILL.md` — Code-domain gap filling
4. `.agents/references/category-mapping.md` — Category reference
5. `.agents/references/quality-checklist.md` — Quality gates

## CURRENT STATE (build on, do not delete)

```
STAGE 1 — EXTRACT    ✅ 109/109  (912K)
STAGE 2 — REFINE      ✅ 109/109  (1.0M)
STAGE 3 — MERGE       ✅ master.md exists (20,794 lines, deduplicated)
STAGE 4 — ADAPT       ✅ 57 files exist (9,400 lines)
STAGE 5 — ARTIFACTS   ✅ 6 files exist (~28K)
SCE v2.0.0            ✅ 4 strata, 175-entry code dictionary
```

**CRITICAL: Expand, do not delete.** Every existing file stays. Add new content that fills gaps.

## WHAT WENT WRONG (the compression problem)

The original adaptation did 1:1 translation — one aerospace example → one code example. Result: 434 aerospace pages compressed to 57 thin code files. The code domain needs MORE content than aerospace, not less — every language, framework, and paradigm adds terms.

## EXPANSION PROTOCOL — Stage 4 Extended

### Pass 1: Rule Examples (3-5 code examples per rule)
For each adapted rule in `ste-code/adapted/`, generate additional STE/non-STE code example pairs. Aerospace has 2-3 examples per rule. Code needs 3-5 because every language/paradigm uses rules differently.

```bash
# Launch 3 workers per batch (same as Agent #1)
hermes -z "$(cat prompt.txt)" -m deepseek-v4-pro --yolo
```

Output: `ste-code/adapted/expanded/a-secX-ruleY-examples.json`

**Dedup against:** `ste-code/adapted/a-sec1-rule1.1.md` through `a-sec9-gr4.md` (all existing code examples), `ste-code/merged/master.md` (all aerospace examples)

### Pass 2: Dictionary Depth (code-domain equivalents)
For every aerospace dictionary entry, generate a code-domain equivalent where applicable. "Engine" → "Server", "Ream" → "Refactor", "Flange" → "Interface".

Output: `ste-code/adapted/expanded/code-dictionary-mapping.json`

**Dedup against:** `ste-code/adapted/a-dictionary.md` (all aerospace entries), `SCE/data/vocabulary/code-dictionary.json` (all existing code entries)

### Pass 3: Category Concrete Examples (10+ per category)
The 19 categories have placeholder names. Fill each with 10-15 concrete code-domain terms, each with: term, definition, approved (bool), example usage.

Output: `ste-code/adapted/expanded/category-entries.json`

**Dedup against:** `SCE/core/categories/noun-categories.json` (existing examples), `SCE/core/categories/generated/nouns-batch-001.json` (190 terms)

### Pass 4: Anti-Pattern Expansion (15+ total)
The current 5 anti-patterns are structural (nesting, semicolons). Add 10+ code-specific anti-patterns: passive API docs, vague errors, synonym drift, jargon comments, hedging commits, noun-as-verb, verb-as-noun, omitted articles, contractions, multi-instruction sentences.

Output: `ste-code/adapted/expanded/anti-patterns.json`

**Dedup against:** `SCE/compute/generated/anti-patterns-batch-001.json` (10 entries), existing 5 anti-patterns in system prompt

### Pass 5: Paradigm Examples
Generate example pairs for each major paradigm:
- OOP: class docstrings, method signatures
- FP: pure function docs, type annotations
- Procedural: step-by-step operation docs
- Declarative: configuration schema docs
- Systems: memory/ownership docs
- Scripting: quick-reference comments

Output: `ste-code/adapted/expanded/paradigm-examples.json`

**Dedup against:** All existing code examples in `ste-code/adapted/`, `SCE/data/vocabulary/code-dictionary.json`, benchmark test cases

## EXPANSION PROTOCOL — Stage 5 Extended

After all Stage 4 passes complete, regenerate the 6 artifact files with expanded content:

| # | File | New Target |
|---|------|------------|
| 1 | `ste-code-distilled-system-prompt.txt` | ~3,000 tokens (include expanded synonym table) |
| 2 | `ste-code-self-reading-manual.txt` | ~12,000 tokens (include all code examples) |
| 3 | `ste-code-extraction-methodology.txt` | Unchanged |
| 4 | `ste-code-example-turn.txt` | ~1,000 tokens (include multi-paradigm example) |
| 5 | `ste-code-deployment-guide.txt` | Unchanged |
| 6 | `README.md` | ~1,000 tokens |

## WORKER PATTERN (proven — use this)

**Every worker must deduplicate before output.** Before writing any example, check:
1. Does it match an existing aerospace example in the original spec? → Skip
2. Does it match a previously generated code example in `expanded/`? → Skip
3. Does it use the same STE/non-STE pair already in the adapted files? → Skip

Each pass prompt must include a list of already-used examples so workers can avoid duplicates.

```bash
# Write prompt to file
cat > /tmp/worker-prompt.txt << 'EOF'
[full prompt with system rules + task + input content]
EOF

# Launch via oneshot wrapper (session_db=None, no tools, no file leaks)
# Launch via local tools launcher (auto-detects venv)
.agents/tools/launch-worker.sh prompt.txt deepseek-v4-pro > output-file.json 2>&1
```

- **Always** use the oneshot wrapper — NOT `hermes -z --yolo` via subprocess
- **Always** 3 workers per batch
- **Always** verify JSON output after each batch
- **Always** `git gcommit-hermes` after each batch
- Never delete existing files — only add new ones to `expanded/` subdirectories

## CROSS-AGENT COORDINATION

| Agent | Status | Overlap |
|-------|--------|---------|
| #8 Extension Worker | Complete (175-entry dictionary) | Use its output as input for Pass 2 |
| #9 Translation Orchestrator | In progress | No overlap — different directories |
| Maturity Audit | Nearly complete | No overlap |

## VERIFICATION (after each pass)

```bash
# Pass 1: Count examples per rule
ls ste-code/adapted/expanded/a-sec*-examples.json | wc -l

# Pass 2: Count dictionary mappings
python3 -c "import json; d=json.load(open('ste-code/adapted/expanded/code-dictionary-mapping.json')); print(len(d['entries']))"

# Pass 3: Count categories
python3 -c "import json; d=json.load(open('ste-code/adapted/expanded/category-entries.json')); print(len(d['categories']))"
```

## KEY FACTS (immutable)
- 19 technical noun categories (NOT 22)
- 53 writing rules + 4 GR rules
- Model: deepseek-v4-pro
- 434 pages in ASD-STE100 Issue 9, January 2025
- Expand, never compress — code domain is larger than aerospace
- Use oneshot wrapper pattern (proven reliable)
- Save state after every batch
