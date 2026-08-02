# ARTIFACT SYNTHESIS WORKER (Phase F — per-sub-document distillation)

You are distilling ONE sub-document of the FINAL STE-Code standard into an
LLM-optimized form, for people who use LLMs to generate code documentation.

You are producing: `{{subdoc}}` — a slice of STE-Code level {{level_label}}.
Level {{level_label}} should contain: {{desc}}
This is sub-document #{{batch_no}} in the distillation sequence.

Guidelines:
- Be faithful to the standard; do not invent rules.
- Use code-domain examples only (no aerospace leakage).
- Keep your output coherent with the overall STE-Code voice (plain, code-domain).
- The DETERMINISTIC BASE sub-document already contains this slice's full content.
  Your job is to DISTILL it — reshape it for LLM consumption (in the spirit of
  llms.txt / llms-full.txt) — not to copy it verbatim, and not to go hunting
  across the whole standard.

# RESEARCH FREEDOM (read, do not guess)
You have file-read and file-write tools. Spend MANY tool calls:
- FIRST read the DETERMINISTIC BASE sub-document for this slice and DISTILL it:
  {{base_path}}
  This file is `{{subdoc}}` — the structural boilerplate for this part of the
  tier. Turn it into a clean, LLM-optimized sub-document.
- If you need a rule or term that is NOT in the base file, you MAY read the
  corresponding source under `ste-code/final/rules/` or research
  `.agents/vendor/` (Microsoft Style Guide, SCOWL, Vale Microsoft/Google/
  write-good, dwyl/OpenSTE glossaries, software-terms.dic). Do NOT invent words.
- For low tiers (-2/-1/0) the base file is all you need. For high tiers (3/4/5)
  the base already bundles the full dictionary + every rule + extensions; read
  it in full before writing.

# HOW TO WRITE THE FILE (critical)
You are a session with file-read and file-write tools (write_file, patch, and
any other file-editing tool available to you). Do NOT print the file to the
chat. Instead:
- READ the base sub-document (and any extra sources you need).
- WRITE the finished sub-document directly to disk at:
  ste-code/artifacts/level{{level_label}}/{{subdoc}}
  using your file-write tool (overwrite any existing content there). You may use
  write_file for a full rewrite, or patch / successive writes to build/append
  section by section — whichever you prefer.
- The file MUST be self-contained, parseable markdown for this slice, and begin
  with a Markdown heading for the content (e.g. `# Level {{level_label}} — <topic>`).
- WRITE IN MULTIPLE calls, never one giant call. Build the file section by
  section (e.g. write the heading + intro first, then append each rule group,
  then the dictionary/extensions) using append-mode writes, patch edits, or
  successive writes to the same path. This avoids accidentally omitting content
  for brevity under a single huge output. Never truncate or summarize to fit
  one response.
- After writing and re-reading to confirm completeness, COMMIT your work
  TURN-BASED (per sub-document, not on a timer). Stage only the file you just
  wrote and commit it with the batch number, e.g.:
    git add ste-code/artifacts/level{{level_label}}/{{subdoc}}
    git commit -m "Phase F synthesize: batch {{batch_no}} — level{{level_label}}/{{subdoc}}"
  Stage the single file by path. Never run `git add -A`, `git add .` or a
  commit-all helper: another session may be writing elsewhere in the repo and a
  repo-wide sweep would capture its unrelated work.
  Do NOT push. If a git lock prevents the commit, skip it and move on — the file
  is already written to disk.
- Do NOT write any narration, tool logs, or "Rewrote…"/"What changed vs…" into
  the file or the chat. Do not create helper scripts.

# OUTPUT: write ste-code/artifacts/level{{level_label}}/{{subdoc}} now (in several write_file calls).
