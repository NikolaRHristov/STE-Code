---
description: "Merge 109 worker extraction files into a single master state document with deduplication and section organization."
version: "2.0.0"
related:
  - ".agents/references/rails.md"
  - ".agents/references/worker-grid.md"
  - ".agents/references/section-types.md"
  - ".agents/skills/extraction/SKILL.md"
  - ".agents/skills/refinement/SKILL.md"
  - ".agents/skills/adaptation/SKILL.md"
  - ".agents/skills/validation/SKILL.md"
  - ".agents/skills/continuation/SKILL.md"
---

# Merge Protocol - Stage 3 (Full Protocol)

Concatenate, deduplicate, and organize 109 worker files into a single master document. Agent-agnostic.

## When to Use
- After GATE 1 passes: all 109 worker files exist and have content
- Before adaptation begins

## Prerequisites (Pre-Merge Checklist)

Confirm these conditions before you start the merge:

- [ ] All 109 worker files exist in `ste-code/extracted/` or `ste-code/refined/`
- [ ] File count matches: `ls ste-code/extracted/w*.md | wc -l` returns 109
- [ ] No zero-byte files: `find ste-code/extracted/ -name "w*.md" -size 0` returns empty
- [ ] No truncated workers: all files end with a complete sentence or table row
- [ ] Page coverage is complete: pages 1 through 434 are all assigned to a worker
- [ ] Stage isolation (RAIL 1): Stage 3 writes only to `ste-code/merged/`
- [ ] PROGRESS.md shows Stage 2 complete with all batches verified
- [ ] `ste-code/merged/` directory exists (create it with `mkdir -p` if missing)

If any prerequisite fails, stop the merge. Go back to the failing stage first.

## Step 1: Concatenate by Page Range

Workers output in order (w001 covers pages 1-4, w109 covers pages 433-434):

```bash
cat ste-code/extracted/w*.md > ste-code/merged/master-raw.md
```

NOTE: `cat` uses shell glob expansion. The shell sorts `w*.md` alphabetically. The naming convention `wNNN` with zero-padded numbers guarantees correct page order (w001, w002, ..., w109).

Check the raw concatenation size:

```bash
wc -c ste-code/merged/master-raw.md   # Expect >500KB
wc -l ste-code/merged/master-raw.md   # Expect >10,000 lines
```

If `master-raw.md` is smaller than 500KB, a worker file is missing or empty. Run:

```bash
# Find workers with suspiciously small output
for f in ste-code/extracted/w*.md; do
  size=$(wc -c < "$f")
  if [ "$size" -lt 3000 ]; then
    echo "SMALL: $f ($size bytes)"
  fi
done
```

## Step 2: Deduplicate

Workers on adjacent page ranges may capture the same content at boundaries. The spec often repeats a rule or dictionary entry across two pages. When both workers extract the same content, the merge produces duplicates.

### Deduplication Targets

- **Rule statements**: "Rule X.Y" with identical text → keep first occurrence
- **Example pairs**: Identical STE/non-STE pairs → keep first occurrence
- **Category listings**: Same category with same examples → keep from header page
- **Dictionary entries**: Same WORD (POS) with identical meaning → keep first

### Deduplication Algorithm (Exact Match)

Use this algorithm to find and remove duplicates. The algorithm uses normalized comparison to handle whitespace differences:

```
For each section type (rules, categories, dictionary entries):
  1. Extract all blocks of that section type from master-raw.md
  2. For each block, compute a normalized fingerprint:
     a. Collapse all whitespace sequences to a single space
     b. Convert to lowercase
     c. Strip leading and trailing whitespace
     d. Remove markdown formatting characters (#, *, >, |) from the comparison
     e. Keep only the first 200 characters as the fingerprint
  3. Group blocks by their fingerprint
  4. For each group with more than one block:
     a. Keep the block with the lowest page offset (first occurrence)
     b. Remove all later blocks from the group
  5. Write the deduplicated output to master.md
```

### Example: Correct vs Incorrect Deduplication

**CORRECT - one copy of each rule:**

```
#### Rule 1.1
Use approved words from the STE dictionary.

#### Rule 1.2
Use words only as their specified part of speech.
```

**INCORRECT - Rule 1.1 appears twice (duplicate from page boundary):**

```
#### Rule 1.1
Use approved words from the STE dictionary.

#### Rule 1.1
Use approved words from the STE dictionary.

#### Rule 1.2
Use words only as their specified part of speech.
```

### Example: Dictionary Entry Duplication

**CORRECT:**

```
#### ACCESS (n) - APPROVED
- **Meaning:** The right to go into or near
- **Forms:** access, accesses, accessed, accessing
- **STE:** Get access to the control panel.
- **Non-STE:** You can access the control panel.
```

**INCORRECT - duplicated with formatting variations:**

```
#### ACCESS (n) - APPROVED
- **Meaning:** The right to go into or near
...

#### ACCESS (n) - APPROVED
- **Meaning:** The right to go into or near
...
```

The second entry uses a hyphen instead of an em dash. The normalized fingerprint catches this.

### When to Use Fuzzy Matching

Use exact match (normalized fingerprint) for most cases. Use fuzzy matching only when:

- Two blocks differ by one or two punctuation characters
- Two blocks differ by a trailing space or newline
- Two blocks have the same structure but different Unicode dashes or quotes

Fuzzy threshold: 95% character similarity on the normalized text. If two blocks exceed this threshold and share the same heading identifier (rule number, category name, dictionary WORD), keep only the first.

WARNING: Do not set the threshold below 90%. Lower thresholds cause false matches between different rules with similar wording.

## Step 3: Organize by Section

Restructure into clean master.md:

```
# ASD-STE100 Issue 9 - Master Extraction

## Front Matter
- Title, copyright, disclaimer, highlights, TOC, index, introduction

## Part 1 - Writing Rules
### Section 1 - Words (Rules 1.1-1.14)
### Section 2 - Multi-word Nouns (Rules 2.1-2.3)
### Section 3 - Verbs (Rules 3.1-3.7)
### Section 4 - Sentences (Rules 4.1-4.4)
### Section 5 - Procedural Writing (Rules 5.1-5.5)
### Section 6 - Descriptive Writing (Rules 6.1-6.6)
### Section 7 - Safety Instructions (Rules 7.1-7.3)
### Section 8 - Punctuation (Rules 8.1-8.7)
### Section 9 - Writing Practices (Rules 9.1-9.4 + GR1-GR4)

### Technical Noun Categories (19 categories with descriptions)

## Part 2 - Dictionary
### A-Z entries with WORD (POS), APPROVED/UNAPPROVED, meaning, forms, examples

## Appendices
### Change History, Flowchart, Index, Change Form, Reference Documents
```

### Example: A Correctly Organized Rule Section

```
## Part 1 - Writing Rules

### Section 1 - Words

#### Rule 1.1
Use approved words from the STE dictionary.

Only words that appear in the dictionary are approved. Use approved words
when they are available. Technical names and technical verbs are the
only exceptions.

> **STE:** Use the approved words from the dictionary.
> **Non-STE:** Utilize the sanctioned terminology from the lexicon.

#### Rule 1.2
Use words only as their specified part of speech.

Each approved word has a specified part of speech (POS). Use the word
only as that POS. For example, use "test" only as a noun, not as a verb.

> **STE:** Do a test of the system.
> **Non-STE:** Test the system.

...
```

### Example: An Incorrectly Organized Section

```
## Section 1 - Words

Rule 1.2
Use words only as their specified part of speech.
...

#### Rule 1.1
Use approved words from the STE dictionary.
...

Rule 1.4 - Use only approved verb forms.
...
```

This is wrong because:
- Rules appear out of numerical order (1.2 before 1.1)
- Heading levels are inconsistent (Rule 1.2 has no `####` prefix)
- The section heading format does not match the standard (uses hyphen, not em dash)
- Rule 1.4 uses a different delimiter style (hyphen instead of newline)

Fix by reordering numerically and normalizing all heading formats.

## Step 4: Validate Completeness

```bash
grep -c "^#### Rule" master.md     # Must be 53
grep -c "^### Category" master.md  # Must be 19
grep -c "^#### " master.md         # Dictionary entries: ~875 approved + ~1400 unapproved
head -5 master.md                  # Verify starts at page 1
tail -5 master.md                  # Verify ends at page 434
```

### Extended Validation Commands

Run these additional checks after the basic counts:

```bash
# Check every rule number 1.1 through 9.4 appears exactly once
for section in 1 2 3 4 5 6 7 8 9; do
  case $section in
    1) max=14 ;; 2) max=3 ;; 3) max=7 ;; 4) max=4 ;;
    5) max=5 ;; 6) max=6 ;; 7) max=3 ;; 8) max=7 ;; 9) max=4 ;;
  esac
  for rule in $(seq 1 $max); do
    count=$(grep -c "^#### Rule ${section}\.${rule}$" master.md)
    if [ "$count" -ne 1 ]; then
      echo "MISSING/DUPLICATE: Rule ${section}.${rule} (found $count times)"
    fi
  done
done

# Check General Recommendations GR1-GR4
for gr in 1 2 3 4; do
  count=$(grep -c "^#### GR${gr}" master.md)
  if [ "$count" -ne 1 ]; then
    echo "MISSING/DUPLICATE: GR${gr} (found $count times)"
  fi
done

# Verify dictionary covers all letters A-Z
for letter in A B C D E F G H I J K L M N O P Q R S T U V W X Y Z; do
  if ! grep -q "^#### ${letter}" master.md; then
    echo "MISSING: No dictionary entries starting with $letter"
  fi
done

# Check no duplicate rule headers exist
grep "^#### Rule" master.md | sort | uniq -d

# Check no empty sections exist
grep -B1 "^$" master.md | grep "^### " | sort | uniq
```

### Integrity Check: Cross-Reference Consistency

Rules often reference other rules within the spec. Verify these cross-references:

```bash
# Extract all "see Rule X.Y" references and check they exist
grep -oP 'Rule \d+\.\d+' master.md | sort -u | while read ref; do
  if ! grep -q "^#### $ref$" master.md; then
    echo "DANGLING REFERENCE: $ref"
  fi
done
```

## Step 5: Spot-Check Fidelity

Pick 10 random page numbers. For each:
1. Read original spec page
2. Find corresponding content in master.md
3. Verify text matches EXACTLY - no paraphrasing, no omission

Flag any mismatched worker and re-extract those pages.

### Systematic Spot-Check Method

Use this script to generate and track spot-checks:

```bash
# Generate 10 random page numbers between 1 and 434
python3 -c "import random; random.seed(42); print('\n'.join(str(n) for n in sorted(random.sample(range(1, 435), 10))))" > ste-code/merged/spot-check-pages.txt

# For each page, find which worker covers it and verify
while read page; do
  worker=$(python3 -c "w = ($page - 1) // 4 + 1; print(f'w{w:03d}')")
  echo "Page $page → Worker $worker"
done < ste-code/merged/spot-check-pages.txt
```

### Spot-Check Criteria

For each spot-check page, confirm:

| Check | Expected |
|-------|----------|
| Page number in heading | `# Page N of 434` or equivalent |
| Rule numbers match | Rule numbers on page match spec |
| Example count matches | Same number of STE/non-STE pairs |
| No paraphrasing | Words, punctuation, and formatting match the spec |
| No missing content | No skipped paragraphs, tables, or examples |
| No fabricated content | No commentary, no modern software terms |

Record each result in `ste-code/merged/spot-check-results.md`:

```
| Page | Worker | Rules | Examples | Match | Notes |
|------|--------|-------|----------|-------|-------|
| 7    | w002   | 1.3-1.4 | 2/2    | PASS  |       |
| 89   | w023   | 3.5    | 1/1    | PASS  |       |
| 150  | w038   | 5.2    | 2/2    | PASS  |       |
...
```

## Step 6: Edge Case Handling

### Edge Case 1: Boundary Content Disagreement

Two adjacent workers may disagree on content that spans a page boundary.

**Example:**

Worker w050 (pages 197-200) extracts Rule 3.5 ending on page 200:
```
#### Rule 3.5
Use only the active voice in procedural writing.
```

Worker w051 (pages 201-204) also extracts what it identifies as Rule 3.5:
```
#### Rule 3.5
Use only the active voice in procedural writing. The active voice
makes instructions clearer for the reader.
```

**Resolution:**

1. Check the original spec PDF at the boundary page (page 200-201)
2. Determine which worker captured the complete rule
3. Keep the most complete version
4. If both are incomplete, merge them manually from the spec
5. Flag both workers for re-extraction if neither is correct

### Edge Case 2: Cross-Referenced Rules

Some rules appear in multiple sections of the spec. For example, Rule 1.1 (approved words) is referenced in Section 9 under writing practices.

**Detection:** A rule heading appears in more than one section.

**Resolution:**

1. Keep the primary occurrence in its numbered section (Section 1 for Rule 1.1)
2. If the cross-reference adds new content (not just a mention), keep it as a "See also" note
3. Format cross-references as:
   ```
   > **See also:** Rule 1.1 (Section 1 - Words)
   ```
4. Never duplicate the full rule text in multiple sections

### Edge Case 3: Dictionary Entry Formatting Divergence

Workers may format the same dictionary entry differently.

**Examples of divergence:**

```
# Worker A format:
#### ACCESS (n) - APPROVED
- **Meaning:** The right to go into or near

# Worker B format (same entry):
#### ACCESS (n) - APPROVED
**Meaning:** The right to go into or near
```

**Resolution:**

1. Normalize all dictionary entries to the refined format (see RAIL 5)
2. Use the deduplication algorithm from Step 2
3. Prefer the entry from the worker with the most complete page coverage
4. If format differences survive normalization, keep the entry that matches RAIL 5 exactly

### Edge Case 4: Non-Contiguous Page Ranges

An extraction failure may leave a gap. For example, worker w042 failed and pages 165-168 were not extracted.

**Detection:**

```bash
# Check for missing page ranges
python3 -c "
pages = set()
for w in range(1, 110):
    start = (w-1)*4 + 1
    end = min(start+3, 434)
    pages.update(range(start, end+1))
missing = sorted(set(range(1, 435)) - pages)
if missing:
    print(f'Missing pages: {missing}')
else:
    print('All 434 pages covered')
"
```

**Resolution:**

1. Identify the missing page range
2. Assign the gap to a new temporary worker
3. Re-extract using the standard worker command
4. Insert the recovered content into master-raw.md at the correct position
5. Re-run the merge from Step 2

### Edge Case 5: Overlapping Content Beyond Boundaries

Workers sometimes capture content well beyond their assigned 4 pages. Worker w010 (pages 37-40) might include content from page 41-42 due to section continuity.

**Detection:**

```bash
# Check if any worker file references pages outside its range
grep -oP 'page[ -]?\d+' ste-code/extracted/w*.md | sort -t: -k2 -n
```

**Resolution:**

1. Allow a 1-page overlap tolerance (workers may include the start of the next section for context)
2. If overlap exceeds 1 page, trim the excess from the later worker's output
3. If both workers have the same overlapping content, the deduplication algorithm handles it

### Edge Case 6: Empty or Truncated Worker Files

A worker may produce an empty file or a file that ends mid-sentence.

**Detection:**

```bash
# Find empty or suspiciously small files
find ste-code/extracted/ -name "w*.md" -size -3000c

# Find files that do not end with a sentence terminator
for f in ste-code/extracted/w*.md; do
  last_char=$(tail -c 1 "$f")
  if [[ "$last_char" != "." && "$last_char" != $'\n' ]]; then
    echo "TRUNCATED: $f (last char: '$last_char')"
  fi
done
```

**Resolution:**

1. If the file is empty: re-extract with the same page range
2. If the file is truncated: split the page range in half and re-extract with two workers
3. If the file has content but no clear end: check if content is complete by comparing with the spec

### Edge Case 7: Encoding or Character Issues

Workers may produce files with different encodings or Unicode normalization forms.

**Detection:**

```bash
# Check for mixed encodings
file -I ste-code/extracted/w*.md | grep -v "utf-8"

# Check for Unicode normalization differences (em dash vs hyphen, smart quotes vs straight quotes)
grep -Pn '[\x{2013}\x{2014}\x{2018}\x{2019}\x{201C}\x{201D}]' ste-code/extracted/w*.md
```

**Resolution:**

1. Convert all files to UTF-8 NFC normalization
2. Replace smart quotes with straight quotes (spec uses ASCII)
3. Normalize all dashes: use em dash (-) for definitions, hyphen (-) for compound words

## Failure Recovery

### Recovery Decision Table

| Validation Failure | Recovery Action |
|-------------------|-----------------|
| `master-raw.md` < 500KB | Check for missing worker files. Re-extract any zero-byte workers. If all 109 exist, check content quality (Step 1 diagnostic commands). |
| Rule count ≠ 53 | Run extended validation commands from Step 4. Identify missing/duplicate rules. For missing rules, find which worker covers that page range and re-extract. For duplicates, apply deduplication algorithm again with stricter thresholds. |
| Category count ≠ 19 | Check if categories appear in the expected section. Some workers may place categories in the dictionary section. Reorganize manually. |
| Dictionary entries missing for a letter | Check the worker that covers that letter's page range. Some letters (X, Z) have very few entries - confirm with spec. |
| Spot-check fails on 2+ pages | The worker for those pages likely has fabrication or truncation. Re-extract with split page ranges. |
| Duplicate rule headers found | Run deduplication again. If duplicates persist, they may be cross-references - see Edge Case 2. |
| File size increases but content is wrong | The deduplication algorithm may have merged different rules. Lower the fuzzy matching threshold or disable fuzzy matching. Re-run with exact match only. |
| Dangling cross-references found | Search master.md for the referenced rule. It may be mislabeled (wrong number) or missing. Find the correct rule and fix the reference. |

### Recovery Workflow

When a validation gate fails, follow this sequence:

```
1. Identify the specific failure (which count is wrong, which page fails spot-check)
2. Isolate the failing workers (which wNNN files contribute to the failure)
3. Check if the source files exist and have valid content
4. If source is bad → re-extract (split page ranges if needed)
5. If source is good → check deduplication parameters
6. If deduplication is correct → check section organization
7. If organization is correct → manual review of spec pages
8. Document the failure and resolution in ste-code/merged/recovery-log.md
```

### Recovery Log Format

Create `ste-code/merged/recovery-log.md` and record every recovery:

```
## Recovery #1 - 2025-07-29 14:30 UTC
- **Failure:** Rule count: 51 (expected 53)
- **Missing:** Rule 4.2, Rule 7.1
- **Workers:** w043 (pages 169-172), w073 (pages 289-292)
- **Action:** Re-extracted w043 and w073 with split page ranges
- **Result:** Rule count now 53. Spot-checks pass.
- **Duration:** 12 minutes
```

### Partial Rebuild

When only a few workers need re-extraction, you do not need to rebuild the entire master document. Use this procedure:

```bash
# 1. Re-extract the failing workers to a temp location
hermes -z "Read spec/issue-09-2025/page-169.md through page-172.md. Extract into ste-code/merged/_fix/w043-fix.md" -m poolside/laguna-s-2.1:free --yolo

# 2. Extract the affected section from master-raw.md
# Find the line numbers where the old worker content starts and ends
grep -n "Page 169" ste-code/merged/master-raw.md

# 3. Use a script to replace the old content with the new
python3 .agents/scripts/patch-master.py \
  --master ste-code/merged/master-raw.md \
  --replace w043 \
  --with ste-code/merged/_fix/w043-fix.md \
  --output ste-code/merged/master-raw-fixed.md

# 4. Re-run deduplication and organization on the patched raw file
# 5. Re-run validation (Step 4)
# 6. If validation passes, replace master-raw.md and master.md
```

## Merge Diagnostics Script

Save this diagnostic script as `.agents/scripts/merge-diagnostics.sh`. Run it after each merge attempt:

```bash
#!/bin/bash
# merge-diagnostics.sh - Comprehensive merge health check
MASTER="ste-code/merged/master.md"
RAW="ste-code/merged/master-raw.md"

echo "=== MERGE DIAGNOSTICS ==="
echo ""

echo "1. File sizes:"
echo "   master-raw.md: $(wc -c < "$RAW") bytes, $(wc -l < "$RAW") lines"
echo "   master.md:     $(wc -c < "$MASTER") bytes, $(wc -l < "$MASTER") lines"
echo ""

echo "2. Content completeness:"
echo "   Rules:     $(grep -c '^#### Rule' "$MASTER") / 53"
echo "   Categories: $(grep -c '^### Category' "$MASTER") / 19"
echo "   Dictionary: $(grep -c '^#### [A-Z]' "$MASTER") entries"
echo "   GR rules:  $(grep -c '^#### GR[1-4]' "$MASTER") / 4"
echo ""

echo "3. Structure integrity:"
echo "   Sections 1-9 present:"
for s in 1 2 3 4 5 6 7 8 9; do
  found=$(grep -c "^### Section $s " "$MASTER")
  [ "$found" -eq 1 ] && status="✓" || status="✗"
  echo "     Section $s: $status"
done
echo ""

echo "4. Duplicate check:"
dupes=$(grep "^#### Rule" "$MASTER" | sort | uniq -d)
if [ -z "$dupes" ]; then
  echo "   No duplicate rules ✓"
else
  echo "   DUPLICATES FOUND:"
  echo "$dupes"
fi
echo ""

echo "5. Cross-reference check:"
dangling=$(grep -oP 'Rule \d+\.\d+' "$MASTER" | sort -u | while read ref; do
  grep -q "^#### $ref$" "$MASTER" || echo "   DANGLING: $ref"
done)
if [ -z "$dangling" ]; then
  echo "   No dangling references ✓"
else
  echo "$dangling"
fi
echo ""

echo "6. Page coverage:"
first_page=$(head -20 "$MASTER" | grep -oP 'page[ -]?\d+' | head -1)
last_page=$(tail -20 "$MASTER" | grep -oP 'page[ -]?\d+' | tail -1)
echo "   First page reference: $first_page"
echo "   Last page reference:  $last_page"
echo ""

echo "=== END DIAGNOSTICS ==="
```

## Output

- `ste-code/merged/master-raw.md` - concatenated raw (temporary)
- `ste-code/merged/master.md` - deduplicated, organized (permanent)
- `ste-code/merged/spot-check-pages.txt` - random pages selected for spot-check
- `ste-code/merged/spot-check-results.md` - spot-check pass/fail log
- `ste-code/merged/recovery-log.md` - failure and recovery record

## Verification Gates

- [ ] master.md exists and >500KB
- [ ] 53 rules present and numbered correctly
- [ ] 4 General Recommendations (GR1-GR4) present
- [ ] 19 categories enumerated
- [ ] Dictionary entries cover A-Z
- [ ] 10 random spot-checks pass
- [ ] No duplicate rule headers
- [ ] No dangling cross-references
- [ ] All sections 1-9 have content (not empty)
- [ ] master-raw.md >500KB before deduplication
- [ ] Recovery log documents all failures (or states "no failures")
- [ ] Merge diagnostics script returns clean output
- [ ] PROGRESS.md updated with Stage 3 status

## Related Documents

| Document | Purpose |
|----------|---------|
| `.agents/references/rails.md` | 8 quality rails for all stages |
| `.agents/references/worker-grid.md` | Worker-to-page mapping (109 workers) |
| `.agents/references/section-types.md` | Section classification for organization |
| `.agents/skills/extraction/SKILL.md` | Stage 1 extraction protocol |
| `.agents/skills/refinement/SKILL.md` | Stage 2 refinement protocol |
| `.agents/skills/adaptation/SKILL.md` | Stage 4 adaptation protocol |
| `.agents/skills/validation/SKILL.md` | Per-batch quality validation |
| `.agents/skills/continuation/SKILL.md` | Multi-agent continuation from any stage |
