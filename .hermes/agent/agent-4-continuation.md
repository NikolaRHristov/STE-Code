# Agent #4 — Continuation Orchestrator (Stages 3-5)

You are the STE-Code CONTINUATION ORCHESTRATOR. Agents #1 and #2 completed extraction and refinement. Your job: merge, adapt, and produce the final STE-Code artifacts.

## PREREQUISITES (must be complete before you start)

- Agent #1: 109 extracted files in `ste-code/extracted/` ✅
- Agent #2: 109 refined files in `ste-code/refined/` ✅
- Agent #3: Audit report confirming pipeline integrity

## YOUR JOB — Three Stages

### Stage 3: Merge

1. Concatenate all refined files: `cat ste-code/refined/r*-p*.md > ste-code/merged/master-raw.md`
2. Create structural index: map every rule, category, and dictionary section to its source
3. Write `ste-code/merged/master.md` — the authoritative index

### Stage 4: Adapt (GATE 3)

Produce 10 adaptation files in `ste-code/adapted/` converting ASD-STE100 rules to code domain:

1. `sec1-identifiers.md` — Rules 1.1-1.14 (Identifiers, 19 categories, 4 verb categories)
2. `sec2-compound-ids.md` — Rules 2.1-2.2 (Compound identifiers, max 3 components)
3. `sec3-functions.md` — Rules 3.1-3.7 (Functions, verb forms, active voice)
4. `sec4-statements.md` — Rules 4.1-4.5 (Statements, vertical lists, articles)
5. `sec5-procedural.md` — Rules 5.1-5.5 (Procedural docs, 20-word max, imperative)
6. `sec6-declarative.md` — Rules 6.1-6.6 (Descriptive docs, 25-word max, paragraphs)
7. `sec7-safety.md` — Rules 7.1-7.3 (BREAKING/DEPRECATED/NOTE)
8. `sec8-syntax.md` — Rules 8.1-8.7 (Punctuation, word count, hyphens)
9. `sec9-practices.md` — Rules 9.1-9.4 + GR-1 through GR-8 (Practices, recommendations)
10. `vocabulary.md` — Canonical synonym table, polysemy resolution, anti-patterns

**Adaptation rules:**
- PRESERVE: rule numbers, section organization, rule structure, pipeline
- REPLACE: every aerospace example → code-domain example
- SAFETY: WARNING → BREAKING, CAUTION → DEPRECATED
- 19 categories → code domain (languages, frameworks, tools, deps, etc.)

### Stage 5: Artifacts (GATE 4)

Produce 6 files in `ste-code/artifacts/`:

1. `ste-code-distilled-system-prompt.md` (~1,400 tokens) — drop-in system prompt for any LLM
2. `ste-code-self-reading-manual.md` (~7,000 tokens) — S0-S8 self-reading manual
3. `ste-code-extraction-methodology.md` — 6-pass pipeline protocol
4. `ste-code-example-turn.md` — worked transformation example
5. `ste-code-deployment-guide.md` — Ollama, OpenAI, Claude instructions
6. `README.md` — project overview

## SKILLS

Load for detailed protocol:
- `skill_view(name='ste-code-merge')` — Merge protocol
- `skill_view(name='ste-code-adaptation')` — Adaptation rules and category mapping
- `skill_view(name='ste-code-artifacts')` — Artifact specifications

## VERIFICATION

After completing all stages:
```bash
ls ste-code/adapted/*.md | wc -l    # must be 10
ls ste-code/artifacts/*.md | wc -l  # must be 6
grep -rl "TODO\|TBD" ste-code/adapted/ ste-code/artifacts/  # must be empty
python3 ste-code/check-rails.py     # all 4 checks must pass
```

## GIT

```bash
git add -A && git gcommit-hermes && git sync
```

## COMMUNICATION

Signal progress in `.hermes/feedback/exchange.md`. Write state report using `agent-state-report` skill when complete.

## START NOW

1. Verify `ste-code/refined/` has 109 files
2. Run `cat ste-code/refined/r*-p*.md > ste-code/merged/master-raw.md`
3. Create structural index in `ste-code/merged/master.md`
4. Begin Stage 4 — adapt all 53 rules
