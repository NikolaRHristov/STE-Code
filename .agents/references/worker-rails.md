# Worker Rails — Injected Into Every Worker Prompt

> These rails are appended to every worker prompt. Workers self-validate
> before writing output. Copy this block into every prompt template.

---

## WORKER RAILS (validate before writing output)

### BEFORE YOU WRITE THE OUTPUT FILE, CHECK:

□ **RAIL W1 — Page Header**: Does my output start with `# Page N of M`?

□ **RAIL W2 — No Glued Headings**: After every `###` or `####` heading, is there a blank line before content?

□ **RAIL W3 — No Fabrication**: Does my output contain ONLY text from the spec pages? No commentary ("This page shows..."), no modern terms ("React", "Docker"), no summaries.

□ **RAIL W4 — Boilerplate Control**: Is "ASD-STE100 Simplified Technical English" appearing only where it belongs, not repeated on every line?

□ **RAIL W5 — STE/Non-STE Format**: Are ALL example pairs formatted as:
```
> **STE:** [example text]
> **Non-STE:** [example text]
```

□ **RAIL W6 — Tables Clean**: Do all tables have header row + separator row? No merged columns from PDF interleaving?

□ **RAIL W7 — Blank Line After Tables**: Is there a blank line after every table before the next content?

□ **RAIL W8 — No Triple Blanks**: Are there zero instances of three or more consecutive blank lines?

□ **RAIL W9 — Content Complete**: Did I include EVERY word, number, and example from the source pages? Nothing omitted?

□ **RAIL W10 — Naming Correct**: Does my output filename match the pattern `[w|r]NNN-pPPPP-PPPP.md`?

### AFTER WRITING, VERIFY:
```bash
# Check line count
wc -l <OUTPUT_FILE>
# Must be > 30 lines for 4-page extraction

# Check for glued headings
grep -c $'### [^\n]\n[^ \n#]' <OUTPUT_FILE>
# Must be 0

# Check page header
head -1 <OUTPUT_FILE>
# Must match: # Page NNN of 434
```
