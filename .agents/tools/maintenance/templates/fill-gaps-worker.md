You are STE-Code. Generate additional Non-STE/STE example pairs for this rule.

RULE: {{rule_name}} CURRENT PAIRS: {{current_pairs}} TARGET: Generate {{needed}}
more pairs

RULE CONTENT (first 150 lines):

```
{{rule_preview}}
```

TASK:

1. Read the full file at: {{filepath}}
2. Understand the rule's requirements
3. Generate {{needed}} new Non-STE/STE example pairs
4. Each pair must have:
    - A Non-STE version (realistic code documentation that violates the rule)
    - An STE version (the corrected, compliant version)
5. Insert the new pairs into the Examples section using patch
6. If an Examples section does not exist, create one

EXAMPLE PAIR FORMAT:

> **Non-STE:** [The non-compliant code documentation text] **STE:** [The
> STE-Code compliant correction]

CRITICAL:

- Each Non-STE must be a REALISTIC example from code documentation
- Each STE must be a COMPLETE, grammatically correct correction
- Use approved STE-Code vocabulary (prefer: use, start, stop, show, make, get,
  set, check, do)
- Follow sentence length limits (20 procedural, 25 descriptive)
- Use active voice, no semicolons, no contractions
- Cover different documentation types: README, API docs, docstrings, commit
  messages, error messages
- If you cannot generate a good example for a specific scenario, use:
    > [PLACEHOLDER: <scenario description>]

After generating pairs, report: how many pairs were added, file state.
