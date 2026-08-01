#!/usr/bin/env python3
"""group_engine.py — pure, deterministic grouping logic for STE-Code Phase C.

WHY THIS IS PURE PYTHON (not an LLM worker)
-------------------------------------------
Grouping is a *deterministic* re-organization: concatenate 109 refined page
files into ~20 semantically coherent chunks, split by section + dictionary
letter. There is no judgement call an LLM adds — only risk it removes.

The old phase-c-run.py handed the ENTIRE 109-file -> ~20-group concatenation
(~600 KB of output) to a single free-tier `tencent/hy3:free` agent. Per the
Refinement agent's hard-won lessons (.agents/feedback/exchange.md):

  Lesson #3  "Explosion/inflation is the enemy of free-tier workers."
             tencent/hy3:free truncates when asked to produce >> source length.
             Grouping ASKS for ~600 KB of output in one shot — a guaranteed
             mid-stream truncation, i.e. silent content loss (a Rule 1 breach)
             across the whole corpus.
  Lesson #4  "Verify against DISK, not self-reports." The worker would claim
             success; half the groups would be truncated.

So grouping must be deterministic Python. The LLM is removed from the copy path
entirely; content cannot be lost because bytes are only *moved*, never *re-typed*.

THE SECTION ORACLE (churn-proof)
--------------------------------
Section membership is read from the MANIFEST page-IDs, NOT from:
  - section-types.md  -> its page ranges are STALE (it claims DICT ends p360 /
    APPENDIX 361-434, but the MANIFEST proves the dictionary runs A..Y through
    page 426). Trusting it would misfile ~66 dictionary pages as "appendix".
  - the refined files' internal page markers -> during refinement these churn.
    Worse, the Refinement agent is EVOLVING the marker format as it self-
    improves: some finished files use `# Page 12 of 434` (sequential), others
    use `## Page 1-2-2` (the spec page-ID). The slicer below tolerates BOTH and
    resolves either to a sequential position via the MANIFEST, so grouping does
    not break when the refiner changes its output style.

MANIFEST page-IDs (`FRONT-MATTER`, `HI-3`, `1-1-2`, `2-0-6`, `2-1-C18`, ...)
are stable ground truth: the spec's own pagination.

This module has NO side effects and NO LLM calls. It is imported by
group_batch.py (assembler) and verify-groups.py (checker) so all three agree
on the plan — satisfying Refinement Lesson #1 ("prompt, skill, and gate must
agree"): here there is ONE source of truth for the plan, shared by every tool.
"""
from __future__ import annotations

import collections
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
REFINED_DIR = PROJECT / "ste-code" / "refined"
MANIFEST_PATH = PROJECT / "spec" / "issue-09-2025" / "page-dir" / "MANIFEST.md"

TOTAL_PAGES = 434

# Refined filename: r<worker>-p<start>-<end>.md
REFINED_RE = re.compile(r"^r(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$")

# ── Page-marker detection: tolerate every style the refiner has emitted ──────
# The Refinement agent's output format is a moving target. We accept:
#   `# Page 34 of 434`   `# Page 34`   `## Page 34`   (sequential number)
#   `## Page 1-2-2`      `# Page 2-1-C18`             (spec page-ID)
#   `**Page 1-2-2**`     `**Page HI-3**`             (bold, legacy extraction)
# Each match is resolved to a *sequential position* (1..434). A marker line is
# ANY line matching one of these — captured group 1 is the page token.
_PAGE_MARKERS = [
    re.compile(r"^#{1,4}\s+Page\s+(\d{1,4})\s+of\s+\d{2,4}\s*$", re.I),
    re.compile(r"^#{1,4}\s+Page\s+(\d{1,4})\s*$", re.I),
    re.compile(r"^#{1,4}\s+Page\s+([A-Za-z0-9][A-Za-z0-9\-]*)\s*$", re.I),
    re.compile(r"^\*\*\s*Page\s+([A-Za-z0-9][A-Za-z0-9\-]*)\s*\*\*\s*$", re.I),
]


# ───────────────────────────────────────────────────────────────────────────
# MANIFEST parsing → the section oracle
# ───────────────────────────────────────────────────────────────────────────
def parse_manifest() -> Dict[int, str]:
    """position (1..426) → page_id (e.g. 'FRONT-MATTER', 'HI-3', '2-1-C18')."""
    mapping: Dict[int, str] = {}
    if not MANIFEST_PATH.exists():
        return mapping
    for line in MANIFEST_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("| ") and "page-" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5 and parts[1].isdigit():
                mapping[int(parts[1])] = parts[2]
    return mapping


def id_to_position(manifest: Dict[int, str]) -> Dict[str, int]:
    """Reverse map: page_id (upper-cased) → position. Case-insensitive lookups."""
    return {pid.upper(): pos for pos, pid in manifest.items()}


def classify_page(page: int, page_id: Optional[str]) -> Tuple[str, Optional[str]]:
    """Return (section, key) for a page.

    section ∈ {FRONT, NAV, INTRO, RULES, DICT_INTRO, DICT, APPENDIX}
    key: for RULES = chapter number (str '1'..'9'); for DICT = letter 'A'..'Z';
         else None.

    Classification is by MANIFEST page-ID prefix (churn-proof). Pages past the
    MANIFEST (427-434) fall through to APPENDIX by page number.
    """
    if page_id is None:
        return "APPENDIX", None

    if page_id == "FRONT-MATTER":
        return "FRONT", None
    if page_id.startswith("HI-"):
        return "FRONT", None  # Highlights-of-changes rides with front matter.
    if page_id.startswith("TOC"):
        return "NAV", None
    if page_id.startswith("SRI"):
        return "NAV", None
    if re.fullmatch(r"[ivxlcdm]+", page_id):  # roman-numeral front pages
        return "NAV", None

    # Part 1 = the writing rules. `1-0-*` is the intro to Part 1; `1-N-*` is
    # rule section N (N=1..9). Categories are interleaved inside these sections
    # in Issue 9 (see section-types.md rationale) — we keep them with their rule
    # section rather than artificially splitting.
    m = re.match(r"^1-(\d+)-", page_id)
    if m:
        chap = m.group(1)
        if chap == "0":
            return "INTRO", None
        return "RULES", chap

    # Part 2 = the dictionary. `2-0-*` is the dictionary preface/how-to-use;
    # `2-1-<Letter>*` are the alphabetical entries.
    if page_id.startswith("2-0-"):
        return "DICT_INTRO", None
    md = re.match(r"^2-1-([A-Z])", page_id)
    if md:
        return "DICT", md.group(1)
    if page_id.startswith("2-1-"):
        return "DICT", None  # dict page whose letter didn't parse — still DICT

    return "APPENDIX", None  # unknown prefix → appendix (never dropped)


# ───────────────────────────────────────────────────────────────────────────
# Refined-file index
# ───────────────────────────────────────────────────────────────────────────
@dataclass
class RefinedFile:
    path: Path
    worker: int
    start: int
    end: int

    @property
    def pages(self) -> range:
        return range(self.start, self.end + 1)


def index_refined() -> Dict[int, "RefinedFile"]:
    """page number → RefinedFile that contains it (by filename range)."""
    idx: Dict[int, RefinedFile] = {}
    if not REFINED_DIR.exists():
        return idx
    for f in sorted(REFINED_DIR.glob("*.md")):
        m = REFINED_RE.match(f.name)
        if not m:
            continue
        rf = RefinedFile(f, int(m.group("worker")), int(m.group("start")), int(m.group("end")))
        for p in rf.pages:
            idx[p] = rf
    return idx


# ───────────────────────────────────────────────────────────────────────────
# Group plan
# ───────────────────────────────────────────────────────────────────────────
@dataclass
class Group:
    gid: str            # e.g. "005-dict-A-C"
    label: str          # human-readable
    section: str        # FRONT / RULES / DICT / ...
    pages: List[int] = field(default_factory=list)
    key: Optional[str] = None  # rule chapter or letter-range

    @property
    def filename(self) -> str:
        return f"group-{self.gid}.md"


# DICT letter bucketing knobs. Deterministic Python has no output limit, but the
# group is later CONSUMED by a free-tier model (adaptation) — Lesson #3 applies
# to the consumer. We keep each dict group digestible and balanced. A single
# oversized letter (e.g. 'S' ≈ 32 pages) becomes its own bucket; tiny tail
# letters merge with neighbours instead of orphaning. Tunable; validated via
# --dry-run.
DICT_BUCKET_TARGET_PAGES = 26
DICT_BUCKET_MAX_PAGES = 36


def _bucket_dict_letters(order: List[str], letter_pages: Dict[str, List[int]]):
    """Balanced greedy: walk letters in page order, keep whole letters together,
    flush a bucket before it would exceed MAX, and after it reaches TARGET. A
    letter bigger than MAX on its own becomes its own bucket. Returns a list of
    (letter_list, page_list)."""
    buckets: List[Tuple[List[str], List[int]]] = []
    cur_letters: List[str] = []
    cur_pages: List[int] = []

    def flush():
        nonlocal cur_letters, cur_pages
        if cur_letters:
            buckets.append((cur_letters, cur_pages))
            cur_letters, cur_pages = [], []

    for L in order:
        lp = letter_pages[L]
        # Flush first if adding this letter would overshoot MAX (unless empty).
        if cur_pages and len(cur_pages) + len(lp) > DICT_BUCKET_MAX_PAGES:
            flush()
        cur_letters.append(L)
        cur_pages.extend(lp)
        if len(cur_pages) >= DICT_BUCKET_TARGET_PAGES:
            flush()
    flush()

    # Merge a tiny trailing bucket (< half target) back into the previous one,
    # so we never orphan a 2-page 'Y' as its own group.
    if len(buckets) >= 2 and len(buckets[-1][1]) < DICT_BUCKET_TARGET_PAGES // 2:
        last_letters, last_pages = buckets.pop()
        buckets[-1][0].extend(last_letters)
        buckets[-1][1].extend(last_pages)
    return buckets


def build_plan(manifest: Dict[int, str]) -> List[Group]:
    """Deterministically assign all 434 pages to ordered groups.

    Every page 1..434 lands in exactly one group. Section boundaries come from
    the oracle; DICT is split into alphabetical buckets that never split a
    letter (letters change on page boundaries, and we group whole pages, so a
    dictionary entry — which lives within a page's table — is never split).
    """
    sect: Dict[int, Tuple[str, Optional[str]]] = {}
    for p in range(1, TOTAL_PAGES + 1):
        sect[p] = classify_page(p, manifest.get(p))

    groups: List[Group] = []
    n = 0

    def add(label, section, pages, key=None):
        nonlocal n
        n += 1
        slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")
        groups.append(Group(gid=f"{n:03d}-{slug}", label=label, section=section,
                            pages=list(pages), key=key))

    def pages_of(section):
        return [p for p in range(1, TOTAL_PAGES + 1) if sect[p][0] == section]

    # 1. FRONT (cover, copyright, trademark + highlights-of-changes).
    if pages_of("FRONT"):
        add("front-matter", "FRONT", pages_of("FRONT"))
    # 2. NAV (table of contents, SRI, roman-numeral front pages).
    if pages_of("NAV"):
        add("toc-and-nav", "NAV", pages_of("NAV"))
    # 3. INTRO (Part 1 chapter 0 — how to use the writing rules).
    if pages_of("INTRO"):
        add("introduction", "INTRO", pages_of("INTRO"))
    # 4. RULES — one group per rule chapter (Sec 1..9), in order.
    chapters = sorted({sect[p][1] for p in range(1, TOTAL_PAGES + 1)
                       if sect[p][0] == "RULES" and sect[p][1] is not None},
                      key=lambda c: int(c))
    for chap in chapters:
        pages = [p for p in range(1, TOTAL_PAGES + 1)
                 if sect[p][0] == "RULES" and sect[p][1] == chap]
        add(f"rules-sec-{chap}", "RULES", pages, key=chap)
    # 5. DICT_INTRO (dictionary preface / how-to-use).
    if pages_of("DICT_INTRO"):
        add("dictionary-intro", "DICT_INTRO", pages_of("DICT_INTRO"))
    # 6. DICT — balanced alphabetical buckets.
    dict_pages = pages_of("DICT")
    if dict_pages:
        letter_pages: Dict[str, List[int]] = {}
        order: List[str] = []
        for p in dict_pages:
            L = sect[p][1] or "?"
            if L not in letter_pages:
                letter_pages[L] = []
                order.append(L)
            letter_pages[L].append(p)
        for letters, pages in _bucket_dict_letters(order, letter_pages):
            lo, hi = letters[0], letters[-1]
            rng = lo if lo == hi else f"{lo}-{hi}"
            add(f"dict-{rng}", "DICT", sorted(pages), key=rng)
    # 7. APPENDIX — everything left (change history, flowchart, forms, index).
    if pages_of("APPENDIX"):
        add("appendix", "APPENDIX", pages_of("APPENDIX"))

    return groups


# ───────────────────────────────────────────────────────────────────────────
# Page-accurate content slicing (format-agnostic; used by the real assembler)
# ───────────────────────────────────────────────────────────────────────────
def _match_page_marker(line: str) -> Optional[str]:
    """If `line` is a page marker in any accepted style, return its page token
    (either a sequential number string or a spec page-ID). Else None."""
    s = line.strip()
    for pat in _PAGE_MARKERS:
        m = pat.match(s)
        if m:
            return m.group(1)
    return None


def _token_to_position(token: str, id2pos: Dict[str, int]) -> Optional[int]:
    """Resolve a page-marker token to a sequential position (1..434).

    A pure integer token IS the sequential position. A spec page-ID token is
    looked up in the MANIFEST reverse map. Returns None if unresolvable.
    """
    if token.isdigit():
        v = int(token)
        return v if 1 <= v <= TOTAL_PAGES else None
    return id2pos.get(token.upper())


def slice_pages(rf: "RefinedFile", id2pos: Optional[Dict[str, int]] = None) -> Dict[int, str]:
    """Split a refined file into {sequential_page: body_text} using whatever
    page-marker style the file uses (see _PAGE_MARKERS).

    Returns {} if the file's markers do not cleanly resolve to exactly the
    file's declared page range — the caller MUST treat that as "not ready" (do
    not guess). During refinement churn many files have partial/absent markers;
    grouping should WAIT for a clean corpus rather than slice blind.

    The file's leading metadata block (title + `> **Source:**` / `> **Pages:**`)
    that precedes the first page marker is dropped: it is per-file boilerplate,
    re-emitted once per group by the assembler.
    """
    if id2pos is None:
        id2pos = id_to_position(parse_manifest())
    text = rf.path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    marks: List[Tuple[int, int]] = []  # (line_index, sequential_position)
    for i, ln in enumerate(lines):
        tok = _match_page_marker(ln)
        if tok is None:
            continue
        pos = _token_to_position(tok, id2pos)
        if pos is None:
            continue
        marks.append((i, pos))

    expected = list(rf.pages)
    got = [pos for _, pos in marks]
    # Must be exactly the declared range, in order, no dupes/gaps.
    if got != expected:
        return {}
    out: Dict[int, str] = {}
    for j, (li, pos) in enumerate(marks):
        end = marks[j + 1][0] if j + 1 < len(marks) else len(lines)
        out[pos] = "\n".join(lines[li:end]).rstrip() + "\n"
    return out


def corpus_ready(idx: Dict[int, "RefinedFile"],
                 id2pos: Optional[Dict[str, int]] = None) -> Tuple[bool, List[str]]:
    """Is the refined corpus complete + sliceable (all 434 pages present, every
    file's markers resolving to its full page range)? Returns (ready, problems).

    Used by the assembler to REFUSE to run on a mid-refinement corpus, and by
    --dry-run to report readiness without failing. This is a *structural*
    readiness check (are the bytes here and addressable), NOT a quality verdict
    on the refinement — per the user's instruction we do not re-verify the
    refiner's work, we only confirm we can slice it losslessly.
    """
    if id2pos is None:
        id2pos = id_to_position(parse_manifest())
    problems: List[str] = []
    missing = [p for p in range(1, TOTAL_PAGES + 1) if p not in idx]
    if missing:
        problems.append(f"{len(missing)} pages have no refined file: {missing[:12]}...")
    seen_files: Dict[str, RefinedFile] = {}
    for p in range(1, TOTAL_PAGES + 1):
        rf = idx.get(p)
        if rf and rf.path.name not in seen_files:
            seen_files[rf.path.name] = rf
    unsliceable = []
    for name, rf in sorted(seen_files.items()):
        if not slice_pages(rf, id2pos):
            unsliceable.append(name)
    if unsliceable:
        problems.append(f"{len(unsliceable)} refined files whose page markers "
                        f"don't cleanly resolve to their range (refinement in "
                        f"progress / format drift): {unsliceable[:8]}...")
    return (not problems), problems


# ───────────────────────────────────────────────────────────────────────────
# Content-token parity — the strongest zero-loss gate
# ───────────────────────────────────────────────────────────────────────────
# Grouping only MOVES bytes; it never re-types them. The one place it legitimately
# *drops* text is repeated dictionary-table headers/separators and per-page
# boilerplate (page stamps, source blocks) — never real content. So the correct
# gate is NOT a word-count ratio (Refinement Lesson #2: never count formatting as
# content — dropped repeated headers make a naive ratio wrongly fail). Instead we
# compare the MULTISET of content tokens between the source pages and the merged
# output after removing ONLY structural boilerplate from both sides. If they
# match exactly, no content word was lost or duplicated. If a real entry vanished
# mid-merge (the truncation failure mode grouping must never have), the multisets
# differ and we can name the exact missing tokens.

_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_DICT_HDR_LINE_RE = re.compile(r"^\|\s*Word\s*\(?POS\)?", re.I)
_SEP_LINE_RE = re.compile(r"^\|[\s:\-\|]+\|?\s*$")
_PAGE_LINE_RE = re.compile(r"^(?:#{1,4}\s+Page\s+.+|\*\*\s*Page\s+.+\*\*)\s*$", re.I)
_BOILERPLATE_RE = re.compile(
    r"(?i)(ASD[-\s]?STE100(\s+Simplified\s+Technical\s+English)?"
    r"|Simplified\s+Technical\s+English"
    r"|Issue\s+9(\s*[-,]?\s*(2025-01-15|January\s+2025))?"
    r"|Part\s+\d+\s*[-–]\s*Dictionary"
    r"|Page\s+[A-Z0-9]+-[A-Z0-9\-]+"
    r"|Page\s+\d+(\s*[–-]\s*\d+)?\s+of\s+434"
    r"|Highlights)"
)


def content_tokens(text: str) -> "collections.Counter[str]":
    """Multiset of CONTENT tokens after stripping structural boilerplate.

    Removes (from a COPY, never the real output): dict-table header + separator
    lines, page-marker lines, HTML comments, markup tags, and repeated page-stamp
    boilerplate. What's left is real content: dictionary entry words, meanings,
    STE/Non-STE example words, rule prose, picture-text words. Tokens are
    lower-cased alphanumeric runs of length >= 2 (same shape the refinement gate
    uses), so punctuation/whitespace/case never cause false diffs.
    """
    kept: List[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if _PAGE_LINE_RE.match(s):
            continue
        if _DICT_HDR_LINE_RE.match(s):
            continue
        if _SEP_LINE_RE.match(s):
            continue
        kept.append(line)
    blob = "\n".join(kept)
    blob = _HTML_COMMENT_RE.sub(" ", blob)
    blob = _TAG_RE.sub(" ", blob)
    blob = _BOILERPLATE_RE.sub(" ", blob)
    return collections.Counter(re.findall(r"[a-z0-9]{2,}", blob.lower()))


def parity_diff(src_text: str, out_text: str):
    """Compare content-token multisets. Returns (ok, missing, added) where
    `missing` = tokens in source but not in output (CONTENT LOSS — fatal), and
    `added` = tokens in output but not in source (unexpected injection). Both are
    Counters of the net difference. ok = no missing tokens (loss is the only
    fatal direction; harmless additions like a group title are tolerated but
    reported)."""
    src = content_tokens(src_text)
    out = content_tokens(out_text)
    missing = src - out       # Counter subtraction keeps only positive counts
    added = out - src
    return (sum(missing.values()) == 0), missing, added


if __name__ == "__main__":
    man = parse_manifest()
    idx = index_refined()
    plan = build_plan(man)
    print(f"MANIFEST positions: {len(man)}")
    print(f"Refined pages indexed: {len(idx)}/{TOTAL_PAGES}")
    print(f"Groups planned: {len(plan)}")
    total = sum(len(g.pages) for g in plan)
    print(f"Pages covered by plan: {total}")
