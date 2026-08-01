#!/usr/bin/env python3
"""Report which prompt-bearing tools still hold their prompts inline.

The project already externalizes generated markdown via
``.agents/tools/lib/templater.py`` -- 23 tools use it, each with a
``templates/`` folder beside it. This audit finds the ones that never migrated,
so the remaining work is a finite, checkable list rather than a guess.

A tool is a MIGRATION TARGET when it both:
  - dispatches text to a model (hermes -z / a model flag / an LLM client), and
  - builds that text inline (a large f-string or constant), and
  - does not already import templater.

Read-only. Prints a work list ordered by payload size.
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path

SKIP = {"vendor", "archive", "__pycache__", "_scratch", "node_modules"}
MODEL_HINT = re.compile(
    r"hermes-oneshot-wrapper|hermes\b.*-z|--yolo|chat\.completions|"
    r"messages\.create|invoke_model|generate_content|agent-runner", re.I)
# Prose-shaped: instruction verbs or role framing, not SQL/log/argparse.
PROSE = re.compile(
    r"\b(you are|your job|your task|TASK:|OUTPUT:|do not|must|rewrite|"
    r"produce|generate|extract|refine|output only)\b", re.I)


def collect_docstring_ids(tree: ast.AST) -> set:
    """Ids of Constants that are docstrings -- documentation, never prompts."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef,
                             ast.ClassDef)):
            body = getattr(node, "body", None)
            if body and isinstance(body[0], ast.Expr) \
                    and isinstance(body[0].value, ast.Constant) \
                    and isinstance(body[0].value.value, str):
                out.add(id(body[0].value))
    return out


def inline_payloads(tree: ast.AST, min_len: int) -> list:
    """Large model-bound strings built inline: constants and f-strings."""
    docs = collect_docstring_ids(tree)
    out = []
    for node in ast.walk(tree):
        if isinstance(node, ast.JoinedStr):
            literal = sum(len(v.value) for v in node.values
                          if isinstance(v, ast.Constant)
                          and isinstance(v.value, str))
            fields = [v for v in node.values
                      if isinstance(v, ast.FormattedValue)]
            joined = "".join(v.value for v in node.values
                             if isinstance(v, ast.Constant)
                             and isinstance(v.value, str))
            if literal >= min_len and PROSE.search(joined):
                names = []
                for f in fields:
                    try:
                        names.append(ast.unparse(f.value))
                    except Exception:
                        names.append("?")
                out.append({"kind": "fstring", "line": node.lineno,
                            "chars": literal, "interpolations": names})
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            if id(node) in docs:
                continue
            if len(node.value) >= min_len and PROSE.search(node.value):
                out.append({"kind": "constant", "line": node.lineno,
                            "chars": len(node.value), "interpolations": []})
    return out


def audit(agents: Path, min_len: int) -> list:
    rows = []
    for path in sorted(agents.rglob("*.py")):
        if SKIP & set(path.parts):
            continue
        try:
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        dispatches = bool(MODEL_HINT.search(src))
        uses_templater = "templater" in src
        payloads = inline_payloads(tree, min_len)
        if not payloads:
            continue
        tpl_dir = path.parent / "templates"
        rows.append({
            "file": str(path.relative_to(agents.parent)),
            "family": path.parent.name,
            "dispatches": dispatches,
            "uses_templater": uses_templater,
            "has_templates_dir": tpl_dir.is_dir(),
            "payloads": payloads,
            "total_chars": sum(p["chars"] for p in payloads),
            "interp": sorted({n for p in payloads
                              for n in p["interpolations"]}),
        })
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--agents", default=".agents")
    ap.add_argument("--min-len", type=int, default=200)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = audit(Path(args.agents).resolve(), args.min_len)
    targets = [r for r in rows if r["dispatches"] and not r["uses_templater"]]
    done = [r for r in rows if r["uses_templater"]]
    internal = [r for r in rows if not r["dispatches"]
                and not r["uses_templater"]]

    if args.json:
        print(json.dumps({"targets": targets, "migrated": done,
                          "internal": internal}, indent=2))
        return 0

    print("MIGRATION TARGETS -- dispatch to a model, prompts still inline")
    print("=" * 72)
    for r in sorted(targets, key=lambda x: -x["total_chars"]):
        print("\n{}  ({} chars in {} block{})".format(
            r["file"], r["total_chars"], len(r["payloads"]),
            "" if len(r["payloads"]) == 1 else "s"))
        print("   templates/ dir: {}".format(
            "yes" if r["has_templates_dir"] else "NO -- create"))
        for p in r["payloads"]:
            print("     L{:<5} {:>6}c  {}".format(
                p["line"], p["chars"], p["kind"]))
        if r["interp"]:
            print("   placeholders needed: {}".format(
                ", ".join(r["interp"][:10])))
    print("\n" + "=" * 72)
    print("targets: {} files, {} chars total".format(
        len(targets), sum(r["total_chars"] for r in targets)))
    print("already migrated: {} files".format(len(done)))
    print("inline but no model dispatch (leave alone): {}".format(
        len(internal)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
