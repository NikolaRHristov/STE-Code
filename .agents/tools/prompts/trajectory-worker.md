# TRAJECTORY — Parametrized Standard Distillation Worker

You are running a TRAJECTORY experiment for STE-Code. Your job is NOT to reformat
or summarize the source rule. It is to **distill and completely re-express** the
canonical STE-Code rule into a NEW document shaped entirely by the MISSION
PARAMETERS below — so that, upon receipt, a different consumer (an LLM coding
tool, an autonomous agent, a human-assembled doc block, etc.) receives the same
underlying standard through a paradigm and vocabulary tuned to *their* context.

The parameters are the "mission" the information is sent under. They change the
information on receipt: the same rule, delivered under parameter-set A vs B, is a
*different* document — different paradigm, different examples, different
emphasis, different edge-case focus, different hints. That is the point of
trajectory: encode *how the knowledge is received* into the run.

---

# SOURCE RULE (read it, then TRANSFORM it)
File: {{src_name}}

{{src_text}}

---

# MISSION PARAMETERS (this variant)
{{param_block}}

# WHAT "DISTILL" MEANS HERE
Do NOT copy the source with light edits. Re-derive the rule's *intent* and
re-express it from scratch for the target defined by the parameters:
- If `target_consumer` is an LLM coding tool or agent, frame the rule as
  machine-actionable guidance: concrete DO / DON'T, copy-paste-able patterns,
  function/comment shapes it should emit, and explicit "when you receive a
  request that trips this rule, do X" instructions.
- If `target_consumer` is a human doc block, keep it readable but tune density
  and examples to `format` (e.g. "example-led with library HINTS",
  "DO/DON'T checklist + copy-paste patterns", "full sections + decision
  procedures").
- If `use_case` names a library/framework/ecosystem, re-cast EVERY example in
  that library's idioms, APIs, error types, and naming — include library-specific
  HINTS (common pitfalls, gotchas, migration notes) the generic rule omits.
- If `paradigm_emphasis` is set, lead with and organize around that paradigm
  (e.g. functional, OO, async, systems, declarative); show the rule through that
  lens first.
- `example_density` controls how many Non-STE/STE pairs to generate.
- `vocab_strictness` controls whether to enforce only Microsoft/Google/STE-Code
  approved words.
- `edge_case_focus` (e.g. "edge-cases to X", "edge-cases to Y") means you MUST
  add a dedicated section enumerating concrete edge cases for X (and/or Y),
  with a Non-STE/STE pair and the reasoning for each.
- `register` sets the voice (strict spec / friendly tutorial / terse reference).

# RESEARCH FREEDOM (use it — this is a long session)
You have file-read and file-write tools and the whole repo. Spend MANY tool
calls. You MAY and SHOULD:
- Read `{{src_name}}` and any related `ste-code/final/rules/*.md` to understand
  cross-rule relationships.
- Read `.agents/vendor/` corpora (Microsoft Style Guide, SCOWL, Vale
  Microsoft/Google/write-good, dwyl/OpenSTE glossaries, software-terms.dic) to
  borrow APPROVED, controlled vocabulary and realistic examples. Verify a word is
  approved before using it — do not guess.
- Read `.agents/vendor/FINAL_PHASE_CONTEXT_INSTRUCTIONS.md` for which corpora to
  consult.
- Make SMALL, surgical, MULTI-TURN edits: research, draft a section, write,
  re-read to confirm, refine, repeat. Depth and correctness beat speed.

# OUTPUT REQUIREMENTS
- Write the variant to: `{{out_path}}` (create the directory if needed).
- Begin with `# Rule {{self_num}} — {{title}}` and be valid, self-contained markdown.
- Preserve the rule's identity (it is still the same ASD-STE100-derived rule),
  but expressed in the target paradigm/voice — NOT a verbatim copy.
- Include a `## Mission parameters` block at the top listing the exact
  parameters used (so the variant is self-describing and reproducible).
- Include `> **Non-STE:**` / `> **STE:**` example pairs in the target idiom.
- If `edge_case_focus` is set, include `## Edge cases` with the required entries.
- End with `## Sources consulted` listing every vendor/reference file you read
  (relative paths under `.agents/vendor/`), for traceability.
- NO aerospace leakage: every example and term must be code-domain.

# WHEN DONE
- Re-read the written file; confirm it is complete, correct, and shaped by the
  mission parameters (not a copy of the source).
- Your ONLY artifact is that one written file. Do not print it to chat, no
  narration or tool logs.

Output ONLY the rewritten markdown. No code fences, no commentary before/after.
Start immediately with the rule heading.
