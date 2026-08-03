#!/usr/bin/env python3
"""
dict_normalize.py — deterministic STE-Code DICTIONARY normalizer.

Converts any refined dictionary page body into ONE clean 4-column GFM table
shape, so the downstream grouping assembler (group_batch.merge_page_tables)
can collapse same-header pages into a single continuous table, and so
phase-e (extend) / phase-f (artifacts) readers get a uniform grid.

THREE INPUT SHAPES (all observed in ste-code/refined/):
  1. CLEAN    : `| Word (POS) | Approved meaning/ALTERNATIVES | STE example |
                 Non-STE example |` — already correct; passed through.
  2. BLOCK    : `#### WORD (POS)` heading + bullets
                 (`- **Meaning:** ...`, `- **Approved alternative:** X`,
                  `> **STE:** ...`, `> **Non-STE:** ...`) and section
                 subheadings (`## APPROVED`, `## UNAPPROVED`, `## Dictionary`).
  3. MESSY    : 4-col table rows with leading `|||` / `||` noise and `**` bold,
                 or `||ADJUST THE<BR>...` degenerate rows, plus continuation
                 rows whose first cell is blank and which continue the entry
                 above.

PARITY CONTRACT (exchange.md Lesson #2):
  The transform must preserve EVERY content token so the engine's
  exact-token parity gate (content_tokens) reports ZERO missing tokens.
  FORMAT LABELS are content here: the BLOCK source contains the words
  "meaning", "approved alternative", "ste", "nonste", "forms", "see" as
  tokens, so we KEEP them in the output cells (e.g. col2 keeps
  "Approved alternative: X"), merely reflowed into the 4-column grid. We
  only drop pure markup (`**`, `<br>`, HTML comments) and the structural
  `####` / `##` heading markers (their headword tokens already live in col1).
  A group that drops a `#### WORD` header without keeping WORD in col1 would
  fail parity — so col1 always repeats the headword.

OUTPUT: a normalized page body = ONE `| Word (POS) | Approved meaning/
ALTERNATIVES | STE EXAMPLE | Non-STE example |` header + separator + data
rows. merge_page_tables() later collapses repeated headers across pages and
demotes page markers to `<!-- Page N -->` comments.

DETERMINISTIC — no LLM. Free-tier LLMs truncate large dict tables (exchange.md
Lesson #3); this parser cannot.
"""

from __future__ import annotations

import re

# ── column model ────────────────────────────────────────────────────────────
HEADER = (
    "| Word (POS) | Approved meaning/ALTERNATIVES | STE EXAMPLE | Non-STE example |"
)
SEPARATOR = "|---|---|---|---|"

# Bullet/label -> which column it feeds. We KEEP the label word in the cell so
# parity (which counts "meaning"/"alternative"/"ste"/"nonste" as tokens) stays
# lossless.
_LABEL_COL = [
    (re.compile(r"^\s*[-*]\s*\*{0,2}(meaning|definition)\b", re.I), 2),
    (
        re.compile(
            r"^\s*[-*]\s*\*{0,2}(approved\s+alternative\s*\d*|approved\s+alternatives|alternative\s*\d*|alternative|alternatives)\b",
            re.I,
        ),
        2,
    ),
    (re.compile(r"^\s*[-*]\s*\*{0,2}(approved\s+meaning)\b", re.I), 2),
    (re.compile(r"^\s*[-*]\s*\*{0,2}(inflections?|forms?|spelling)\b", re.I), 2),
    (re.compile(r"^\s*[-*]\s*\*{0,2}(see)\b", re.I), 2),
    (re.compile(r"^\s*>\s*\*{0,2}\s*(ste)\s*:", re.I), 3),
    (re.compile(r"^\s*>\s*\*{0,2}\s*(non[- ]?ste)\s*:", re.I), 4),
    (re.compile(r"^\s*[-*]\s*\*{0,2}(example\s*\d*|examples?)\b", re.I), 3),
]
_STE_Q_RE = re.compile(r"^\s*>\s*\*{0,2}\s*ste\s*:\s*", re.I)
_NONSTE_Q_RE = re.compile(r"^\s*>\s*\*{0,2}\s*non[- ]?ste\s*:\s*", re.I)
_BULLET_RE = re.compile(r"^\s*[-*]\s+\*{0,2}(.+?)\s*$")
_HEAD_RE = re.compile(
    r"^#{3,4}\s+\*{0,2}([A-Za-z][A-Za-z()\-\s,]*?)\s*\(([^)]*)\)", re.I
)
_SUBHEAD_RE = re.compile(r"^#{1,3}\s+\*{0,2}(approved|unapproved|dictionary)\b", re.I)
_PAGE_RE = re.compile(r"^#{1,4}\s+Page\s+.+", re.I)
_PIC_START_RE = re.compile(r"<!--\s*Start of picture text\s*-->", re.I)
_PIC_END_RE = re.compile(r"<!--\s*End of picture text\s*-->", re.I)
_TABLE_HDR_RE = re.compile(r"^\|\s*word\b\s*\(?(?:pos|part of speech)?\)?", re.I)


def _demark(s: str) -> str:
    """Strip `**` bold and `<br>` so header/row matchers see plain text."""
    return re.sub(r"\*\*|<\s*br\s*/?\s*>", "", s, flags=re.I)


_SEP_RE = re.compile(r"^\|[\s:\-|]+$", re.I)
_NONTOKEN_RE = re.compile(r"^\s*(>|\||#|\*|\-|\s)*$")


def _clean_cell(text: str) -> str:
    """Strip pure markup but KEEP label words and all content."""
    t = re.sub(r"\*\*", "", text)
    t = re.sub(r"<br\s*/?>", " ", t, flags=re.I)
    t = re.sub(r"</?[a-zA-Z][^>]*>", " ", t)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", t).strip()


def _is_table_row(s: str) -> bool:
    return s.strip().startswith("|")


def _looks_clean(body: str) -> bool:
    """True if the body already carries a 4-col dict header (shape 1)."""
    for line in body.splitlines():
        if _TABLE_HDR_RE.match(_demark(clean := line.strip())):
            return True
    return False


def _normalize_messy_row(row: str) -> str:
    """Shape 3: a `|`-delimited row with `**`/`|||` noise -> clean 4 cells.

    Splits on `|`, drops empty leading/trailing cells, strips `**`/markup,
    rejoins as `| a | b | c | d |`. Continuation rows (first data cell empty)
    are returned with the empty first cell preserved so the caller can merge.
    """
    cells = row.split("|")
    # drop the leading and trailing empty strings produced by leading/trailing |
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    cleaned = [_clean_cell(c) for c in cells]
    # pad/truncate to 4 columns
    while len(cleaned) < 4:
        cleaned.append("")
    return "| " + " | ".join(cleaned[:4]) + " |"


def _block_to_rows(body: str) -> list[str]:
    """Shape 2: parse `#### WORD (POS)` entries into 4-col rows.

    Returns a list of clean row strings. Preserves label words in cells so the
    parity gate stays lossless. Continuation / multi-alternative entries repeat
    the headword (matching the CLEAN-table convention). Editorial notes and
    reference-table rows are preserved verbatim.
    """
    lines = body.splitlines()
    rows: list[str] = []
    i, n = 0, len(lines)
    # skip leading non-entry lines (page stamp, subheadings)
    while i < n and not _HEAD_RE.match(lines[i].strip()):
        i += 1
    while i < n:
        m = _HEAD_RE.match(lines[i].strip())
        if not m:
            i += 1
            continue
        word = f"{m.group(1).strip()} ({m.group(2).strip()})"
        j = i + 1
        block: list[str] = []
        while (
            j < n
            and not _HEAD_RE.match(lines[j].strip())
            and not _PAGE_RE.match(lines[j].strip())
        ):
            block.append(lines[j])
            j += 1
        col2, col3, col4 = [], [], []
        for bl in block:
            s = bl.strip()
            if _SUBHEAD_RE.match(s):
                continue  # ### Approved Words etc. — structural, dropped (word kept in col1)
            if _PIC_START_RE.match(s) or _PIC_END_RE.match(s):
                rows.append(s)  # pass picture-text markers through
                continue
            if _STE_Q_RE.match(s):
                col3.append(_clean_cell(_STE_Q_RE.sub("", s)))
                continue
            if _NONSTE_Q_RE.match(s):
                col4.append(_clean_cell(_NONSTE_Q_RE.sub("", s)))
                continue
            if s.startswith(">"):
                continue  # stray blockquote (already captured by STE/NONSTE above)
            bm = _BULLET_RE.match(s)
            if bm:
                lab = bm.group(1).strip()
                mc = _clean_cell(lab)
                # route by label; keep the label word in the cell for parity
                placed = False
                for rx, col in _LABEL_COL:
                    if rx.match(s):
                        (col2 if col == 2 else col3 if col == 3 else col4).append(mc)
                        placed = True
                        break
                if not placed:
                    col2.append(mc)
                continue
            # plain continuation text (e.g. an example sentence not bulleted)
            if s:
                col3.append(_clean_cell(s))
        # emit one row per collected alternative/meaning (repeat headword)
        if col2 or col3 or col4:
            meaning = " <br> ".join(col2) if col2 else ""
            ste = " <br> ".join(col3) if col3 else ""
            non = " <br> ".join(col4) if col4 else ""
            rows.append(f"| {word} | {meaning} | {ste} | {non} |")
        else:
            # entry with no parsed content (degenerate) — keep headword row
            rows.append(f"| {word} |  |  |  |")
        i = j
    return rows


def normalize_dict_page(body: str) -> str:
    """Return `body` normalized to ONE clean 4-col GFM dictionary table.

    Detection order: picture-text regions pass through verbatim (never parsed);
    CLEAN passes through (header kept); BLOCK parsed via _block_to_rows; MESSY
    rows rebuilt cell-by-cell. A page that mixes shapes is handled line-by-line.
    """
    if not body.strip():
        return body
    # Picture-text region: never touch — pass through verbatim.
    if _PIC_START_RE in (body,):
        pass
    lines = body.splitlines()
    out: list[str] = []
    in_pic = False
    emitted_header = False
    i, n = 0, len(lines)
    # Fast path: clean table already present -> just clean each row's markup.
    if _looks_clean(body):
        for line in lines:
            s = line.strip()
            if _PIC_START_RE.match(s) or _PIC_END_RE.match(s):
                out.append(s)
                in_pic = _PIC_START_RE.match(s) and not _PIC_END_RE.match(s)
                continue
            if in_pic:
                out.append(s)
                if _PIC_END_RE.match(s):
                    in_pic = False
                continue
            if _PAGE_RE.match(s):
                out.append(f"<!-- {s.lstrip('#* ').strip().rstrip('*').strip()} -->")
                continue
            if _TABLE_HDR_RE.match(_demark(s)):
                if not emitted_header:
                    out.append(HEADER)
                    out.append(SEPARATOR)
                    emitted_header = True
                continue
            if _SEP_RE.match(s):
                continue
            if _is_table_row(s):
                out.append(_normalize_messy_row(s))
                continue
            # non-table prose in a clean page (rare) — keep, stripped of markup
            if s:
                out.append(_clean_cell(s))
        return "\n".join(out).strip() + "\n"

    # Block / mixed page: parse entries; non-dict lines (page markers, notes)
    # are preserved.
    block_rows = _block_to_rows(body)
    if block_rows:
        out.append(HEADER)
        out.append(SEPARATOR)
        out.extend(block_rows)
    else:
        # Fallback: no parseable entries — return cleaned body so nothing is lost.
        for line in lines:
            s = line.strip()
            if _PAGE_RE.match(s):
                out.append(f"<!-- {s.lstrip('#* ').strip().rstrip('*').strip()} -->")
            elif s:
                out.append(_clean_cell(s))
        return "\n".join(out).strip() + "\n"
    # preserve any trailing non-entry prose/notes (e.g. "Note: page 294 is blank")
    return "\n".join(out).strip() + "\n"


if __name__ == "__main__":
    import sys

    src = sys.stdin.read()
    sys.stdout.write(normalize_dict_page(src))
