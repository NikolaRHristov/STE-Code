# ARTIFACT SYNTHESIS WORKER (Phase F)

You are packaging the FINAL STE-Code standard into shippable LEVELS for
people who use LLMs to generate code documentation. You have the FULL standard
available on disk (and may research .agents/vendor/ for vocabulary). Produce
LEVEL {{level_label}} of STE-Code.

Level {{level_label}} should contain: {{desc}}

Guidelines:
- Be faithful to the full standard; do not invent rules.
- Use code-domain examples only (no aerospace leakage).
- Level -2 = ultra-minimal; level -1 = core principles; level 0 = baseline;
  higher levels progressively add dictionary, grammar, extensions, and full rules.
- Keep your output coherent with the overall STE-Code voice (plain, code-domain).

# RESEARCH FREEDOM (read, do not guess)
You have file-read and file-write tools. Spend MANY tool calls:
- Read `ste-code/final/README.md` for the standard's structure and intent.
- The full standard was SPLIT into ordered chunks so nothing is lost. Read the
  chunks listed in the MANIFEST below, IN ORDER, to absorb the whole standard:
{{bundle}}
- FIRST read the DETERMINISTIC BASE sub-document for THIS file and DISTILL it
  (do not merely copy it — reshape it for LLM consumption):
  {{base_path}}
  This base file is `{{subdoc}}` — the structural boilerplate for this slice of
  the tier. Your job is to turn it into a clean, LLM-optimized sub-document (in
  the spirit of llms.txt / llms-full.txt) that is faithful to the STE-Code spec
  but shaped for an LLM to load and follow.
- For low tiers (-2/-1/0) you may read selectively (core principles live in the
  early rules); for high tiers (3/4/5) you MUST read ALL chunks to assemble the
  complete dictionary + every rule + extensions.
- Research `.agents/vendor/` (Microsoft Style Guide, SCOWL, Vale
  Microsoft/Google/write-good, dwyl/OpenSTE glossaries, software-terms.dic) to
  ground vocabulary in approved, controlled words. Do not invent words.

# HOW TO WRITE THE FILE (critical)
You are a session with file-read and file-write tools. Do NOT print the file to
the chat. Instead:
- READ the standard chunks above and research .agents/vendor/ as needed.
- WRITE the finished level file directly to disk at:
  ste-code/artifacts/level{{level_label}}.md   (use a minus sign for negative tiers:
  level-2.md for -2, level-1.md for -1)
  using your file-write tool (overwrite any existing content there).
- The file MUST be self-contained, parseable markdown for that level, and begin
  with the level heading.
- WRITE IN MULTIPLE write_file CALLS, never one giant call. Build the file
  section by section (e.g. write the heading + principles first, then append
  each rule group, then the dictionary/extensions) using append-mode writes or
  successive writes to the same path. This avoids accidentally omitting content
  for brevity under a single huge output. Never truncate or summarize to fit
  one response.
- After writing and re-reading to confirm completeness, END the session.
- Do NOT write any narration, tool logs, or "Rewrote…"/"What changed vs…" into the
  file or the chat. Do not create helper scripts.

# OUTPUT: write ste-code/artifacts/level{{level_label}}.md now (in several write_file calls).
