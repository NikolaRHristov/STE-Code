#!/usr/bin/env python3
"""Shared helper: load a STE-Code pipeline skill and embed it into a worker prompt.

The pipeline scripts (extract_batch.py, refine_batch.py, grouping, adaptation,
etc.) launch Hermes oneshot sub-agents via hermes-oneshot-wrapper.py. Those
sub-agents do NOT automatically inherit the STE-Code profile's skills (the
wrapper calls AIAgent directly). To guarantee every worker honors the pipeline
rules, each script embeds the relevant skill's SKILL.md text into the worker
prompt via this helper.

This complements the `ste-code` Hermes profile (which auto-loads the same skills
for interactive sessions). Prompt injection is the authoritative mechanism for
the batch workers; the profile is the convenience for human/agent sessions.

Usage:
    from skill_prompt import load_skill
    skill_text = load_skill("extraction")   # reads .agents/skills/extraction/SKILL.md
    prompt = f"{base_prompt}\n\n---\n{skill_text}\n---"
"""

import os
import re
from pathlib import Path

# Project root: this file lives at .agents/tools/lib/skill_prompt.py
# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

_PROJECT = _repo_root(__file__)
_SKILLS_DIR = _PROJECT / ".agents" / "skills"


def load_skill(name: str) -> str:
    """Return the body of .agents/skills/<name>/SKILL.md (frontmatter stripped).

    Returns "" if the skill file is missing (caller should still work).
    """
    skill_md = _SKILLS_DIR / name / "SKILL.md"
    if not skill_md.exists():
        return ""
    text = skill_md.read_text(encoding="utf-8")
    # Strip YAML frontmatter (--- ... ---) if present.
    if text.startswith("---"):
        # Find the closing --- of the frontmatter block.
        m = re.match(r"^---\s*\n.*?\n---\s*\n?", text, re.DOTALL)
        if m:
            text = text[m.end():]
    return text.strip()


def skill_section(name: str, heading: str = "PIPELINE SKILL (authoritative rules)") -> str:
    """Wrap a skill's body in a delimiter so the worker treats it as binding."""
    body = load_skill(name)
    if not body:
        return ""
    return (
        f"\n\n# {'='*60}\n"
        f"# {heading}: {name}\n"
        f"# {'='*60}\n\n"
        f"{body}\n"
    )


if __name__ == "__main__":
    import sys
    name = sys.argv[1] if len(sys.argv) > 1 else "extraction"
    print(skill_section(name))
