#!/usr/bin/env python3
"""templater.py — generic external-markdown/prompt template loader for STE-Code tools.

WHY THIS EXISTS
---------------
Pipeline tools generate markdown and worker prompts. Historically that text lived
INLINE as big f-strings inside the .py (see refine_batch.py::_build_batch_prompt).
Inline prompts are painful to edit, impossible to diff/review cleanly, force ugly
escaping of literal braces/pipes (`\\\\|`), and mix content with control flow.

This loader externalizes every generated-markdown blob into its own editable
`.md` file under a tool's `templates/` folder, so each tool folder holds its
markdown organized per function, generically and easy to edit — without touching
Python to change wording.

PLACEHOLDER SYNTAX: {{name}}
----------------------------
Substitution uses DOUBLE-BRACE placeholders, NOT str.format()/f-strings. This is
deliberate: prompt/markdown content is full of literal single braces (JSON
examples, code fences, `{start}-{end}` prose) and literal pipes (`|` tables).
`.format()` would choke on all of those and require escaping every one. `{{name}}`
only ever matches an intended placeholder, so template authors write natural
markdown with zero escaping.

  template:  "# Page {{start}}-{{end}} of 434\\n> **Pages:** {{start}}-{{end}}"
  render(...): render_template(path, start=1, end=4)

STRICT BY DEFAULT
-----------------
render() raises if a template references a placeholder you did not supply, or if
you supply a variable the template never uses (both are bugs — a typo'd
placeholder silently shipping to a worker is exactly the kind of error that
corrupts output). Pass strict=False to relax (leaves unknown {{x}} verbatim,
ignores extra vars).

USAGE
-----
    from templater import Templater
    tpl = Templater(__file__)                 # templates/ next to the tool
    text = tpl.render("group_header", gid="001-front", pages="1-27", section="FRONT")

    # or one-shot, given an explicit path:
    from templater import render_template
    text = render_template(Path("/abs/templates/x.md"), name="value")
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List

_PLACEHOLDER_RE = re.compile(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}")


def find_placeholders(text: str) -> List[str]:
    """Return the ordered unique list of {{placeholder}} names in a template."""
    seen: Dict[str, None] = {}
    for m in _PLACEHOLDER_RE.finditer(text):
        seen.setdefault(m.group(1), None)
    return list(seen.keys())


def render_string(template: str, *, strict: bool = True, **vars: object) -> str:
    """Substitute {{name}} placeholders in `template` with str(vars[name]).

    strict=True (default): raise KeyError if the template needs a var you didn't
    pass, and ValueError if you passed a var the template never references.
    strict=False: leave unknown placeholders verbatim and ignore extra vars.
    """
    needed = set(find_placeholders(template))
    supplied = set(vars.keys())

    if strict:
        missing = needed - supplied
        if missing:
            raise KeyError(
                f"template needs placeholder(s) not supplied: {sorted(missing)}")
        extra = supplied - needed
        if extra:
            raise ValueError(
                f"variable(s) supplied but not used by template: {sorted(extra)}")

    def _sub(m: "re.Match[str]") -> str:
        name = m.group(1)
        if name in vars:
            return str(vars[name])
        return m.group(0)  # strict=False: leave {{name}} as-is

    return _PLACEHOLDER_RE.sub(_sub, template)


def render_template(path: Path, *, strict: bool = True, **vars: object) -> str:
    """Load a template file and render it. Raises FileNotFoundError if missing."""
    text = Path(path).read_text(encoding="utf-8")
    return render_string(text, strict=strict, **vars)


class Templater:
    """Loads templates from a `templates/` folder next to a tool's .py file.

    Construct with `Templater(__file__)`; call `.render("name", **vars)` to load
    and render `templates/name.md`. Templates are cached after first read.
    """

    def __init__(self, tool_file: str | Path, subdir: str = "templates"):
        self.base = Path(tool_file).resolve().parent / subdir
        self._cache: Dict[str, str] = {}

    def path(self, name: str) -> Path:
        """Resolve a template name to a path (adds .md if no suffix given)."""
        fname = name if name.endswith(".md") else f"{name}.md"
        return self.base / fname

    def load(self, name: str) -> str:
        """Return raw template text (cached). Raises FileNotFoundError if absent."""
        if name not in self._cache:
            p = self.path(name)
            if not p.exists():
                raise FileNotFoundError(f"template not found: {p}")
            self._cache[name] = p.read_text(encoding="utf-8")
        return self._cache[name]

    def render(self, name: str, *, strict: bool = True, **vars: object) -> str:
        """Load `templates/<name>.md` and render its {{placeholders}}."""
        return render_string(self.load(name), strict=strict, **vars)

    def placeholders(self, name: str) -> List[str]:
        """List the placeholders a template declares (for validation/tests)."""
        return find_placeholders(self.load(name))


if __name__ == "__main__":
    # Tiny self-check.
    t = "# {{title}}\n\nvalue={{title}} literal={not a placeholder} pipe=a|b\n"
    print(render_string(t, title="Hello"))
    assert find_placeholders(t) == ["title"]
    try:
        render_string("{{a}}", b=1)
    except KeyError as e:
        print("strict missing OK:", e)
    try:
        render_string("no placeholders", x=1)
    except ValueError as e:
        print("strict extra OK:", e)
    print("templater self-check passed")
