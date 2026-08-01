# ARTIFACT SYNTHESIS WORKER (Phase F)

You are packaging the FINAL STE-Code standard into shippable LEVELS for
people who use LLMs to generate code documentation. You have the FULL standard
below (and may research .agents/vendor/ for vocabulary). Produce LEVEL {{level_label}}
of STE-Code.

Level {{level_label}} should contain: {{desc}}

Guidelines:
- Be faithful to the full standard; do not invent rules.
- Use code-domain examples only (no aerospace leakage).
- Level -2 = ultra-minimal; level -1 = core principles; level 0 = baseline;
  higher levels progressively add dictionary, grammar, extensions, and full rules.
- Keep your output coherent with the overall STE-Code voice (plain, code-domain).

# HOW TO WRITE THE FILE (critical)
You are a session with file-read and file-write tools. Do NOT print the file to
the chat. Instead:
- READ the standard context below and research .agents/vendor/ as needed.
- WRITE the finished level file directly to disk at:
  ste-code/artifacts/level{{level_label}}.md   (use a minus sign for negative tiers:
  level-2.md for -2, level-1.md for -1)
  using your file-write tool (overwrite any existing content there).
- The file MUST be self-contained, parseable markdown for that level.
- After writing and re-reading to confirm correctness, END the session.
- Do NOT write any narration, tool logs, or "Rewrote…"/"What changed vs…" into the
  file or the chat. Do not create helper scripts.

# FULL STE-Code STANDARD (read all of it)
{{bundle}}
