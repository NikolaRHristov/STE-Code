# Contributing to STE-Code

## Maturity Model

All instruction files are scored on a 7-level scale:

| Level | Name | Description |
|:-----:|------|------------|
| −2 | Placeholder | Empty or auto-generated stub |
| −1 | Skeleton | Headings only, no body text |
| 1 | Basic | Content exists but shallow — no examples |
| 2 | Functional | Usable but lacks edge cases, cross-refs |
| 3 | Comprehensive | Examples, cross-refs, specific enough to execute |
| 4 | Expert | Edge cases, failure recovery, rationale, known limitations |
| 5 | Production | Self-improving, measurable quality gates, version history |

## Extending the Dictionary

1. Find an unapproved term in `ste-code/adapted/a-dictionary.md`
2. Identify the approved alternative
3. Add a code-domain meaning and example pair
4. Update `SCE/data/vocabulary/approved-verbs.json` or `approved-adjectives.json`
5. Run expansion to generate code examples for the new entry
6. Commit: `feat(dictionary): Add code meaning for <term>`

## Adding Rules

1. Identify a documentation pattern not covered by the 53 existing rules
2. Write the rule following the adapted format: original STE text → code-domain rewrite → example pairs
3. Add to `ste-code/adapted/a-secN-ruleX.Y.md`
4. Update `SCE/core/rules/rule-X.Y.md` with YAML frontmatter
5. Update the benchmark test cases if the rule is testable
6. Commit: `feat(rules): Add rule X.Y — <description>`

## Building New Agents

1. Create `.agents/agent/agent-N-role.md` following the template:
   - Identity (who you are, what you do)
   - Skills (read these first, with paths)
   - Architecture (how you work)
   - Poll system (batch-of-3 pattern)
   - Worker template (the prompt each worker receives)
   - Verification (how to check output)
   - START NOW (concrete first steps)
2. Create `.agents/skills/<name>/SKILL.md` with YAML frontmatter
3. Add to `.agents/AGENTS.md` agent table + skills inventory
4. Test with a single worker before launching full batches
5. Commit: `feat(agent): Add Agent #N — <role>`

## Worker Protocol

All workers follow this pattern:

```bash
python3 .agents/tools/telemetry-worker.py <worker-id> <prompt-file> --output <output-file>
```

Rules:
- 3 workers per batch maximum
- `notify_on_complete=true` for background workers
- Verify output after every batch
- Commit after every batch: `git gcommit-hermes "phase:<letter> batch:<N>"`
- Failed workers → read `RECOVERY-NEEDED/<id>.md` → fix → re-launch

## Code Review

Pull requests must:
- Pass all 59 benchmark tests (96.6% minimum)
- Include STE/non-STE example pairs for any new rules
- Cross-reference every claim to a source in master.md
- Not decrease any agent's maturity score
