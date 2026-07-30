  ┊ 🔎 find      *Agent*1*  0.2s
  ┊ 🔎 grep      *extraction*orchestrat*  0.2s [Search failed: rg: regex parse error:
    (?:...]
  ┊ 🔎 find      extraction*orchestrat*  0.2s
  ┊ 🔎 find      Agent #1  0.2s
  ┊ 🔎 grep      EXTRACTION ORCHESTRATOR  0.1s
  ┊ 🔎 find      w*-p*-*.md  0.1s
  ┊ 🔎 find      ste-code  0.1s
  ┊ 📖 read      w061-p241-244.md  0.1s
  ┊ 📖 read      w060-p237-240.md  0.1s
  ┊ 📖 read      w001-p1-4.md  0.1s
  ┊ 📖 read      w050-p197-200.md  0.2s
Done. Added three new sections to `.agents/agent/agent-1-extractor.md` (lines 49-154):

**SAMPLE OUTPUT — w001-p1-4.md** (title + highlights pages) — Shows the front-matter format: page marker headings (`# Page N of 434`), the ASD-STE100 standard header, copyright notices, a Highlights changes table, and rule section excerpts.

**SAMPLE OUTPUT — w061-p241-244.md** (dictionary table pages) — Shows the dictionary table format with the two-column structure (`Word (POS) | Meaning & Examples`), UNNAPROVED tags on unapproved words, STE EXAMPLE vs Non-STE example columns, and page separators.

**WHAT TO CHECK IN EVERY OUTPUT FILE** — A 7-point checklist covering page marker headings, standard headers, table structure, UNNAPROVED tags, page separators (`---`), content preservation rules, and expected file size ranges (5-9 KB for dictionary pages, 4-7 KB for rules pages).

All samples are drawn from real extracted files in `ste-code/extracted/`, so they accurately reflect what workers produce.
