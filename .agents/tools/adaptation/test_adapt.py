#!/usr/bin/env python3
"""Self-tests for the Phase D/E adaptation + Phase F artifact tooling.

Pure logic checks — no LLM, no network. These are the "dry run" evidence that
the orchestration, prompt templates, section slicing, deterministic gates, and
artifact assembly are correct before any worker is launched.

Run:  python3 .agents/tools/adaptation/test_adapt.py
"""
import sys
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "adaptation"))
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "artifacts"))

from templater import Templater

_passed = 0
_failed = 0


def check(name, cond, detail=""):
    global _passed, _failed
    if cond:
        _passed += 1
        print(f"  ok   {name}")
    else:
        _failed += 1
        print(f"  FAIL {name} — {detail}")


AD = __import__("adapt_batch")
AR = __import__("artifact_batch")

TPL_AD = Templater(PROJECT / ".agents" / "tools" / "adaptation" / "adapt_batch.py")
TPL_AR = Templater(PROJECT / ".agents" / "tools" / "artifacts" / "artifact_batch.py")


def t_prompt_render():
    print("T1 adaptation section prompt renders (strict, no leftover {{}})")
    title = AD.SECTIONS[1][0]
    src = "# 1. Words\nRule 1.1 ...\nRule 1.14 ..."
    out = TPL_AD.render("adapt-sec", section_num=1, section_title=title,
                        rule_count=14, rule_ids="1.1, 1.2", source_text=src)
    check("renders without error", "adapt" in out.lower() or "Adaptation" in out)
    check("no leftover {{", "{{" not in out)
    check("embeds section title", title in out)
    check("embeds source text", "Rule 1.1" in out)
    # strict: missing var raises
    try:
        TPL_AD.render("adapt-sec", section_num=1)
        check("strict missing-var raises", False, "no raise")
    except KeyError:
        check("strict missing-var raises", True)


def t_section_slicing():
    print("T2 section source slicing from grouped text")
    grouped = (
        "# 1. Words\nRULES ONE\n"
        "# 2. Multi-word Nouns\nRULES TWO\n"
        "# 3. Verbs\nRULES THREE\n"
    )
    s1 = AD.extract_section_source(1, grouped)
    s2 = AD.extract_section_source(2, grouped)
    s3 = AD.extract_section_source(3, grouped)
    check("sec1 sliced", "RULES ONE" in s1 and "RULES TWO" not in s1, repr(s1[:30]))
    check("sec2 sliced", "RULES TWO" in s2 and "RULES THREE" not in s2)
    check("sec3 sliced", "RULES THREE" in s3)
    # last section goes to end
    check("sec3 reaches end", grouped.rstrip().endswith(s3.strip()))


def t_gate_logic():
    print("T3 section gate rejects aerospace leakage / missing / synonym")
    import tempfile
    d = Path(tempfile.mkdtemp())
    # Monkeypatch expected counts so the gate accepts this synthetic 3-file section.
    AD.SECTIONS[1] = ("Words", 3)
    # Good file (realistic size, code-domain, source + example pair)
    good = d / "a-sec1-rule1.1.md"
    good.write_text(
        "# Rule 1.1 — Use Words That Are Approved in the Dictionary\n\n"
        "> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.1\n\n"
        "## Original Rule\n\nThe word \"use\" is an approved verb in the dictionary.\n\n"
        "## Adapted Rule\n\nThe word \"run\" is an approved verb in the controlled terminology.\n\n"
        "> **Non-STE:** Utilize the build tool to generate the artifact.\n"
        "> **STE:** Use the build tool to make the artifact.\n"
    )
    # Bad: aerospace leak outside Original Rule
    bad = d / "a-sec1-rule1.2.md"
    bad.write_text("# Rule 1.2\n> **Source:** Adapted from ASD-STE100 Issue 9, Rule 1.2\n"
                   "The aircraft must land safely.\n## Original Rule\nfoo\n")
    # Missing example pair
    nomore = d / "a-sec1-rule1.3.md"
    nomore.write_text("# Rule 1.3\n> **Source:** x\n## Original Rule\nfoo\n> **Non-STE:** a\n")
    AD.ADAPTED_DIR = d
    ok, why = AD._section_passed_gate(1, "Words")
    check("gate fails on bad section", not ok, why)
    # fix bad+nomore, keep good
    bad.write_text(good.read_text())
    nomore.write_text(good.read_text())
    ok2, why2 = AD._section_passed_gate(1, "Words")
    check("gate passes when clean", ok2, why2)
    AD.SECTIONS[1] = ("Words", 14)  # restore


def t_artifact_assembly(tmp_path=None):
    print("T4 artifact assembly collects + orders adapted rules")
    import tempfile
    ad = Path(tempfile.mkdtemp())
    (ad / "a-sec1-rule1.1.md").write_text("# Rule 1.1\nbody one")
    (ad / "a-sec3-rule3.1.md").write_text("# Rule 3.1\nbody three")
    (ad / "a-sec1-rule1.2.md").write_text("# Rule 1.2\nbody two")
    (ad / "a-categories.md").write_text("CATS")
    (ad / "a-dictionary.md").write_text("DIC")
    AR.ADAPTED_DIR = ad
    files = AR._ordered_rule_files()
    names = [f.name for f in files]
    check("orders by section then rule", names == ["a-sec1-rule1.1.md", "a-sec1-rule1.2.md", "a-sec3-rule3.1.md"],
          str(names))
    text = AR._collect_rule_text(files)
    check("collects all bodies", "body one" in text and "body two" in text and "body three" in text)
    # render artifact templates
    full = TPL_AR.render("artifact-rules", rule_count=3, generated="2026-08-01",
                         rules=text, categories="CATS", dictionary="DIC")
    check("artifact-rules renders, no leftover", "{{" not in full and "body one" in full)
    prompt = TPL_AR.render("artifact-system-prompt", rule_count=3, generated="2026-08-01", rules=text)
    check("artifact-system-prompt renders, no leftover", "{{" not in prompt and "body one" in prompt)


def t_readiness_gate():
    print("T5 adaptation readiness gate refuses without grouped/")
    import tempfile
    import shutil
    # Point at a nonexistent dir
    AD.GROUPED_DIR = Path(tempfile.mkdtemp()) / "nope"
    ok, why = AD.adaptation_ready()
    check("not ready without grouped/", not ok, why)
    AD.GROUPED_DIR = PROJECT / "ste-code" / "grouped"  # restore


def main():
    for t in (t_prompt_render, t_section_slicing, t_gate_logic,
              t_artifact_assembly, t_readiness_gate):
        t()
    print(f"\n{'='*50}\n{_passed} passed, {_failed} failed\n{'='*50}")
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    main()
