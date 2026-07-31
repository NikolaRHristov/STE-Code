#!/usr/bin/env python3
"""Self-tests for the deterministic grouping engine + assembler.

Run:  python3 .agents/tools/grouping/test_grouping.py
No LLM, no network — pure logic checks. These are the "dry run" tuning harness:
every merge/slice invariant the grouping stage must guarantee is asserted here,
so the behavior can be tuned and regression-checked without touching the live
(refinement-in-progress) corpus.
"""
import importlib.util as ilu
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent


def _load(name, path):
    spec = ilu.spec_from_file_location(name, str(path))
    mod = ilu.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


engine = _load("group_engine", PROJECT / ".agents/tools/grouping/group_engine.py")
gb = _load("group_batch", PROJECT / ".agents/tools/grouping/group_batch.py")

_passed = 0
_failed = 0


def check(name, cond, detail=""):
    global _passed, _failed
    if cond:
        _passed += 1
        print(f"  ok   {name}")
    else:
        _failed += 1
        print(f"  FAIL {name}  {detail}")


def content_words(text):
    return gb.word_count(text)


# ── T1: dict tables across pages merge into ONE table, zero entry loss ───────
def t_dict_merge():
    print("T1 dict-table merge across pages")
    p1 = ("# Page 193 of 434\n\n"
          "| Word (POS) | Approved meaning / ALTERNATIVES | STE example | Non-STE example |\n"
          "|---|---|---|---|\n"
          "| CONTAIN (v) | To have in something | EACH SURVIVAL KIT CONTAINS THESE ITEMS: | |\n"
          "| CONTAINER (n) | Something that holds fluids | PUT THE CONTAINER BELOW THE DRAIN PLUG. | |\n")
    p2 = ("# Page 194 of 434\n\n"
          "| Word (POS) | Approved meaning / ALTERNATIVES | STE example | Non-STE example |\n"
          "|---|---|---|---|\n"
          "| CONTINUOUS (adj) | That continues | MAKE SURE THERE IS CONTINUOUS MOVEMENT. | |\n"
          "| COOL (adj) | Moderately cold | WHEN THE AREA IS COOL, POLISH THE SURFACE. | |\n")
    out = gb.merge_page_tables([p1, p2])
    hdrs = sum(1 for ln in out.splitlines() if gb._TABLE_HDR_RE.match(ln.strip()))
    seps = sum(1 for ln in out.splitlines() if gb._SEP_RE.match(ln.strip()))
    data = sum(1 for ln in out.splitlines()
               if ln.strip().startswith("|")
               and not gb._TABLE_HDR_RE.match(ln.strip())
               and not gb._SEP_RE.match(ln.strip()))
    check("single header", hdrs == 1, f"got {hdrs}")
    check("single separator", seps == 1, f"got {seps}")
    check("all 4 data rows", data == 4, f"got {data}")
    for w in ("CONTAIN", "CONTAINER", "CONTINUOUS", "COOL", "SURVIVAL", "POLISH"):
        check(f"entry word {w} preserved", w in out)
    check("page 194 provenance kept", "Page 194" in out)


# ── T2: RULES prose pages untouched (both markers + all blockquotes) ─────────
def t_rules_passthrough():
    print("T2 rules prose passthrough")
    r1 = ("# Page 45 of 434\n\n## Section 1 — Words\n\n### Rule 1.1\n\n"
          "> **STE:** Remove the used oil.\n> **Non-STE:** Remove the utilized oil.\n")
    r2 = ("# Page 46 of 434\n\n### Rule 1.2\n\n"
          "> **STE:** Do the test.\n> **Non-STE:** Accomplish the test.\n")
    out = gb.merge_page_tables([r1, r2])
    check("rule 1.1 kept", out.count("Rule 1.1") == 1)
    check("rule 1.2 kept", out.count("Rule 1.2") == 1)
    check("both STE kept", out.count("> **STE:**") == 2)
    check("both Non-STE kept", out.count("> **Non-STE:**") == 2)
    check("both page markers kept as headings",
          "# Page 45 of 434" in out and "# Page 46 of 434" in out)


# ── T3: picture-text passes through verbatim, even spanning a page ───────────
def t_picture_span():
    print("T3 picture-text passthrough (page-spanning)")
    p1 = ("# Page 41 of 434\n\n## Section 1\n\n"
          "<!-- Start of picture text -->\n"
          "Summary of the rules\n"
          "Rule 1.1 Use words that are approved.\n")
    p2 = ("# Page 42 of 434\n\n"
          "Rule 1.14 Use American English spelling.\n"
          "<!-- End of picture text -->\n\n"
          "### Which words can you use?\n\nSome prose here.\n")
    out = gb.merge_page_tables([p1, p2])
    check("picture start kept", "<!-- Start of picture text -->" in out)
    check("picture end kept", "<!-- End of picture text -->" in out)
    check("picture body line 1", "Summary of the rules" in out)
    check("picture body last", "Rule 1.14 Use American English spelling." in out)
    # The page-42 marker sits INSIDE the picture block → must NOT be demoted to a
    # heading that breaks the block; it should survive verbatim as picture body.
    check("interior page marker preserved verbatim inside picture",
          "# Page 42 of 434" in out)
    check("post-picture prose kept", "Which words can you use?" in out)


# ── T4: inline End-of-picture (content on same line) preserved ───────────────
def t_picture_inline_end():
    print("T4 picture inline-End content preserved")
    p = ("# Page 33 of 434\n\n"
         "<!-- Start of picture text -->\n"
         "yA SD<br><!-- End of picture text -->\n\n"
         "Real prose after.\n")
    out = gb.merge_page_tables([p])
    check("inline-end content kept", "yA SD" in out)
    check("prose after kept", "Real prose after." in out)


# ── T5: content-parity — merge never loses content words ─────────────────────
def t_parity():
    print("T5 content-word parity across merge")
    p1 = ("# Page 100 of 434\n\n"
          "| Word (POS) | meaning | STE | Non-STE |\n|---|---|---|---|\n"
          "| ALPHA (n) | first | USE ALPHA. | |\n")
    p2 = ("# Page 101 of 434\n\n"
          "| Word (POS) | meaning | STE | Non-STE |\n|---|---|---|---|\n"
          "| BETA (n) | second | USE BETA. | |\n")
    merged = gb.merge_page_tables([p1, p2])
    src = content_words(p1) + content_words(p2)
    out = content_words(merged)
    # Only the duplicated HEADER words ("Word POS meaning STE Non-STE") are
    # removed; every DATA word must remain. out <= src but all data words in.
    for w in ("ALPHA", "first", "BETA", "second"):
        check(f"data word {w} kept", w.upper() in merged.upper())
    check("parity: no data-row loss (out within header-diff of src)",
          out >= src - content_words("| Word (POS) | meaning | STE | Non-STE |"),
          f"src={src} out={out}")


# ── T6: plan integrity — full 434-page coverage, no dupes ────────────────────
def t_plan_coverage():
    print("T6 plan coverage integrity")
    man = engine.parse_manifest()
    plan = engine.build_plan(man)
    seen = {}
    for g in plan:
        for p in g.pages:
            seen[p] = seen.get(p, 0) + 1
    missing = [p for p in range(1, engine.TOTAL_PAGES + 1) if p not in seen]
    dupes = [p for p, c in seen.items() if c > 1]
    check("all 434 pages covered", not missing, f"missing={missing[:10]}")
    check("no duplicate pages", not dupes, f"dupes={dupes[:10]}")
    check("groups are contiguous page ranges",
          all(g.pages == list(range(g.pages[0], g.pages[-1] + 1)) for g in plan))
    # dict buckets balanced (no >40p, no orphan <5p except tiny tail sections)
    dict_groups = [g for g in plan if g.section == "DICT"]
    big = [g.gid for g in dict_groups if len(g.pages) > 40]
    check("no oversized dict bucket (>40p)", not big, f"big={big}")


# ── T7: format-agnostic slicing — resolves both sequential + page-ID markers ─
def t_slicer_formats():
    print("T7 format-agnostic page slicing")
    man = engine.parse_manifest()
    id2pos = engine.id_to_position(man)
    # sequential-number style
    check("seq token resolves", engine._token_to_position("45", id2pos) == 45)
    # spec page-ID style (1-2-2 is a real Part-1 rules page id)
    pid = "1-2-2"
    check(f"page-id {pid} resolves via manifest",
          engine._token_to_position(pid, id2pos) == id2pos.get(pid.upper()))
    # marker matchers
    check("h1 'of 434' marker", engine._match_page_marker("# Page 45 of 434") == "45")
    check("h2 seq marker", engine._match_page_marker("## Page 45") == "45")
    check("h2 page-id marker", engine._match_page_marker("## Page 1-2-2") == "1-2-2")
    check("bold legacy marker", engine._match_page_marker("**Page 2-1-C18**") == "2-1-C18")


def t_exact_parity():
    print("T8 exact content-token parity (multiset diff)")
    # Source: two dict pages with repeated header; merged drops the repeat.
    p1 = ("# Page 100 of 434\n\n"
          "| Word (POS) | meaning | STE | Non-STE |\n|---|---|---|---|\n"
          "| ALPHA (n) | first letter | USE ALPHA HERE. | |\n")
    p2 = ("# Page 101 of 434\n\n"
          "| Word (POS) | meaning | STE | Non-STE |\n|---|---|---|---|\n"
          "| BETA (n) | second letter | USE BETA THERE. | |\n")
    merged = gb.merge_page_tables([p1, p2])
    ok, missing, added = engine.parity_diff(p1 + "\n" + p2, merged)
    check("no content tokens missing after merge", ok, f"missing={dict(missing)}")
    check("dropped header words are NOT counted as loss",
          "meaning" not in missing and "ste" not in missing)
    # Now simulate a REAL loss: drop the BETA row entirely.
    broken = merged.replace("| BETA (n) | second letter | USE BETA THERE. | |", "")
    ok2, missing2, _ = engine.parity_diff(p1 + "\n" + p2, broken)
    check("real content loss is DETECTED", not ok2)
    check("missing tokens name the lost entry",
          "beta" in missing2 and "second" in missing2, f"missing={dict(missing2)}")


def main():
    for t in (t_dict_merge, t_rules_passthrough, t_picture_span,
              t_picture_inline_end, t_parity, t_plan_coverage, t_slicer_formats,
              t_exact_parity):
        t()
    print(f"\n{'='*50}\n{_passed} passed, {_failed} failed\n{'='*50}")
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
