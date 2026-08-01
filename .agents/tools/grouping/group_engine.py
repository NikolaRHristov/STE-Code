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


def _build_group_map(plan):
    """page -> (gid, key, start_letter, prev_gid).

    For DICT groups, `start_letter` is the first alpha of the bucket key
    (e.g. 'e' for group key 'e-f'); used to split straddler files at the
    alphabetical boundary. Non-DICT groups have start_letter=None.
    """
    gmap = {}
    prev = None
    for g in plan:
        start_letter = None
        if g.section == "DICT" and g.key:
            m = re.match(r"^([A-Za-z])", g.key)
            start_letter = m.group(1).upper() if m else None
        for p in g.pages:
            gmap[p] = (g.gid, g.key, start_letter, prev)
        prev = g.gid
    return gmap


_GROUP_MAP_CACHE: Dict[str, Dict[int, tuple]] = {}


def _group_map() -> Dict[int, tuple]:
    """Cached page->group map (one source of truth with build_plan)."""
    if "m" not in _GROUP_MAP_CACHE:
        man = parse_manifest()
        _GROUP_MAP_CACHE["m"] = _build_group_map(build_plan(man))
    return _GROUP_MAP_CACHE["m"]


_ENTRY_HEAD_RE = re.compile(r"^#{2,4}\s+([A-Za-z])", re.I)   # ### Word
_ENTRY_ROW_RE = re.compile(r"^\|\s*([A-Za-z])", re.I)        # | Word (POS)


def _entry_first_letter(line: str):
    """If `line` begins a dictionary entry, return its first alpha letter (upper);
    else None. Used to locate the alphabetical split point inside a merged
    straddler file."""
    s = line.strip()
    m = _ENTRY_HEAD_RE.match(s) or _ENTRY_ROW_RE.match(s)
    return m.group(1).upper() if m else None


def _maybe_split_straddler(ps: int, pe: int, txt: str, gmap: Dict[int, tuple]):
    """If segment [ps,pe] spans a group boundary, split it deterministically.

    Only DICT straddlers need a real split: the boundary is the dictionary
    letter change, found by scanning the merged body for the first entry whose
    first letter >= the NEXT group's start letter. Returns a list of
    (start_page, end_page, text) covering [ps,pe] exactly once.
    """
    g0 = gmap.get(ps)
    g1 = gmap.get(pe)
    if not g0 or not g1 or g0[0] == g1[0]:
        return [(ps, pe, txt)]
    # boundary page b = first page in (ps,pe] owned by a different group
    b = None
    for p in range(ps + 1, pe + 1):
        if gmap.get(p, (None,))[0] != g0[0]:
            b = p
            break
    if b is None:
        return [(ps, pe, txt)]
    split_letter = gmap.get(b, (None, None, None, None))[2]
    if not split_letter:
        # Non-dict straddler without a letter cue: keep whole in first group
        # (rare; verify-groups will surface any coverage gap).
        return [(ps, pe, txt)]
    lines = txt.splitlines()
    cut = len(lines)
    for k, ln in enumerate(lines):
        L = _entry_first_letter(ln)
        if L is not None and L >= split_letter:
            cut = k
            break
    part1 = "\n".join(lines[:cut]).rstrip() + "\n"
    part2 = "\n".join(lines[cut:]).rstrip() + "\n"
    return [(ps, b - 1, part1), (b, pe, part2)]


def file_segments(rf: "RefinedFile", id2pos: Dict[str, int]) -> List[Tuple[int, int, str]]:
    """Return ordered (start_page, end_page, text) segments that tile `rf` once.

    Tolerates the four real-world drift conditions the refiner produces:
      A_dupes        — spurious nav cross-references (e.g. `**Page TOC-2**`)
                       resolved to a position OUTSIDE the file's range are
                       ignored; consecutive equal positions are de-duped.
      B_missing_lead — content before the first real marker belongs to rf.start
                       (and trailing content after the last marker to rf.end).
      C_merged       — a file with only its first-page marker (rest merged) is
                       one segment spanning all its pages.
      STRADDLER      — a merged segment that crosses a group boundary is split
                       at the dictionary letter change (deterministic, no LLM).

    Returns [] only for a genuinely broken file (segments don't cover the full
    declared range) — the caller treats that as "not ready".
    """
    text = rf.path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    # Real page boundaries ONLY: a marker whose resolved position is inside
    # this file's own page range. This drops spurious nav cross-references
    # (TOC/SRI page-IDs pointing outside the range).
    marks: List[Tuple[int, int]] = []
    for i, ln in enumerate(lines):
        tok = _match_page_marker(ln)
        if tok is None:
            continue
        pos = _token_to_position(tok, id2pos)
        if pos is None or pos < rf.start or pos > rf.end:
            continue
        marks.append((i, pos))
    # de-dupe consecutive equal positions (keep first)
    dm: List[Tuple[int, int]] = []
    for i, p in marks:
        if not dm or p != dm[-1][1]:
            dm.append((i, p))

    expected = list(rf.pages)

    # CLEAN: markers resolve exactly to the declared range, in order.
    if [p for _, p in dm] == expected:
        segs = []
        for j, (li, pos) in enumerate(dm):
            end = dm[j + 1][0] if j + 1 < len(dm) else len(lines)
            segs.append((pos, pos, "\n".join(lines[li:end]).rstrip() + "\n"))
        return segs

    gmap = _group_map()
    segs: List[Tuple[int, int, str]] = []
    if not dm:
        # Fully merged: the entire file is one segment.
        segs.append((rf.start, rf.end, text.rstrip() + "\n"))
    else:
        first_pos = dm[0][1]
        last_pos = dm[-1][1]
        last_line = dm[-1][0]
        # leading content (missing leading marker) -> rf.start..first_pos-1
        if first_pos > rf.start:
            segs.append((rf.start, first_pos - 1,
                         "\n".join(lines[:dm[0][0]]).rstrip() + "\n"))
        for j, (li, pos) in enumerate(dm):
            end = dm[j + 1][0] if j + 1 < len(dm) else len(lines)
            segs.append((pos, pos, "\n".join(lines[li:end]).rstrip() + "\n"))
        # trailing content (missing trailing marker) -> last_pos+1..rf.end
        if last_pos < rf.end:
            segs.append((last_pos + 1, rf.end,
                         "\n".join(lines[last_line:]).rstrip() + "\n"))

    # Split any segment that straddles a group boundary (STRADDLER).
    out: List[Tuple[int, int, str]] = []
    for (ps, pe, txt) in segs:
        out.extend(_maybe_split_straddler(ps, pe, txt, gmap))

    # Validate exact coverage of the declared range.
    cover: List[int] = []
    for ps, pe, _ in out:
        cover.extend(range(ps, pe + 1))
    if sorted(cover) != expected:
        return []
    return out


def slice_pages(rf: "RefinedFile", id2pos: Optional[Dict[str, int]] = None) -> Dict[int, str]:
    """Split a refined file into {sequential_page: body_text} using whatever
    page-marker style the file uses (see _PAGE_MARKERS).

    Tolerates marker drift (A_dupes / B_missing_lead / C_merged / STRADDLER) so
    grouping no longer refuses a complete-but-imperfectly-marked corpus. Returns
    {} only when a file is genuinely broken (its segments cannot cover the
    declared page range) — the caller MUST treat that as "not ready".

    Multi-page segments (merged/straddler) assign their full text to the FIRST
    page of the segment and "" to the others, so that concatenating
    slice[p] over a group's pages yields each segment exactly once (no
    duplication) — which keeps the content-parity gate honest.
    """
    if id2pos is None:
        id2pos = id_to_position(parse_manifest())
    segs = file_segments(rf, id2pos)
    if not segs:
        return {}
    out: Dict[int, str] = {}
    for (ps, pe, txt) in segs:
        out[ps] = txt
        for p in range(ps + 1, pe + 1):
            out[p] = ""
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
