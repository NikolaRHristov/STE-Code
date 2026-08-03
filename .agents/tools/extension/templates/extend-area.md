# STE-Code Extension Worker — gap area: {{area}}

You generate code-domain STE-Code entries to fill a documented gap between
ASD-STE100 (aerospace) and the code-documentation domain.

## Output format — MARKDOWN ONLY

Write ONE markdown file to this exact path: `{{out_path}}`

Each entry is a level-3 heading block. Use this structure per entry:

```markdown
### <term or id>

- **type**: <verb|adjective|noun|verb-example|anti-pattern|domain>
- **category-id**: <1-19, for noun/verb entries>
- **approved**: <true|false>
- **replaces**: <comma list of avoided synonyms, or empty>
- **definition**: <10+ words describing the term in a code-documentation context>
- **code_example_ste**: <one STE-Code compliant sentence>
- **code_example_non_ste**: <the same instruction using an avoided synonym>
- **source**: <batch id, e.g. generated-batch-001>
```

For anti-pattern entries use: `id`, `pattern`, `non_ste`, `ste`, `violates`
(P1-P14), `severity` (blocking|error|warning|info), `context`.
For domain entries use: `domain`, `term`, `definition`, `replaces`, `source`.

Generate up to **{{count}}** entries.

## Rules

- NO JSON. NO markdown code fences around the whole file. Output is plain markdown.
- Every entry must include all fields for its type (see above).
- `definition` must be 10+ words.
- `code_example_non_ste` must contain a real avoided synonym
  (utilize, leverage, employ, commence, terminate, …); `code_example_ste` must
  differ substantively, not just by punctuation/word order.
- No placeholder text (TODO, TBD, FIXME, ???, <placeholder>). Do not invent terms;
  skip a term if unknown rather than fabricate it.
- Use only code-domain vocabulary. No aerospace examples.

Output ONLY the markdown file.
