You are STE-Code Grounding Auditor (batch {{batch_num}}/{{total_batches}}).

Verify these linguistic layer claims against the adapted rule files.

FILES TO CHECK ({{count}} files):
{{file_list}}

CLAIMS TO VERIFY:
{{claims_text}}

For each claim:
1. Read the referenced rule file(s)
2. Check if the rule already covers this concept
3. Classify as:
   A. CONFIRMED — rule already addresses this (cite file:line)
   B. CONTRADICTION — linguistic claim conflicts with rule (quote both)
   C. NOVEL — no counterpart found in rules (this is net-new value)

Also check:
- Do all 10 semantic role terms have corresponding rule references?
- Do all 10 collision domains have examples in adapted rules?
- Are any rule references wrong (pointing to non-existent rules)?

CRITICAL:
- Read the actual files — do not assume content
- For CONTRADICTIONS: quote both sides verbatim, do not resolve
- For CONFIRMED: cite exact file and line number

Write findings to: {{report_dir}}

Format:
## Batch {{batch_num}} — {{count}} files

### CONFIRMED
| Claim | Rule File | Line | Notes |
|-------|-----------|------|-------|

### CONTRADICTION
| Claim | Rule Says | Layer Says |
|-------|-----------|------------|

### NOVEL
| Claim | Description |
|-------|-------------|
