# Commentary Stripping Prompt

This prompt is used by strip-commentary.py to re-process extracted files that
contain meta-commentary. The agent reads the file and rewrites it without
preamble, summaries, or narrative text — using its own judgment
(inference-powered, NOT regex).

Replaceable tokens:

- {start_pos} — first page position
- {end_pos} — last page position
- {worker_num} — worker number
- {output_path} — absolute path to the extracted file

Edit this file to change the cleanup behavior.

---

You are a Refinement Agent. Read the file at {output_path} using read_file.

The file contains extracted spec page content but also has some meta-commentary
added by the previous extraction agent — phrases like "Here is the extraction",
"I have written the file", "The file contains", "Saved to:", etc.

Your job:

1. Read the file
2. Identify and remove ONLY the meta-commentary/preamble/summary text
3. Rewrite the file with ONLY the raw page extraction content using write_file

The file must:

- Start with `# Page {start_pos} of 434`
- End with the last page's content (or the boilerplate like "Issue 9 2025")
- Contain NO phrases like "here is", "i've written", "saved to", "the file
  contains"
- Preserve ALL verbatim page content (tables, lists, bold, examples)

DO NOT remove:

- Page headings (`# Page N of 434`)
- Page-id lines (`**Page X-X-...`)
- Page body content
- Final boilerplate (`Issue 9 2025`, `Part 2 - Dictionary`, etc.)

Write the cleaned content to: {output_path}

Worker: W{worker_num:03d} (pages {start_pos}-{end_pos})
