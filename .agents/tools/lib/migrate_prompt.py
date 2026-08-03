#!/usr/bin/env python3
"""Reusable harness for migrating an inline prompt into a template.

Three steps, each mechanical:

  extract  pull an f-string / constant out of a script as template text,
           converting {var} -> {{var}} using the AST (no retyping)
  preimage snapshot the script before editing, in-tree so relative paths
           still resolve
  verify   build the prompt from the preimage and from the migrated script
           with identical inputs, and diff

The verify step is the point. A prompt migration that changes wording changes
model behaviour, and nothing downstream would catch it.

Examples
--------
    # see what would be extracted
    python3 migrate_prompt.py extract \\
        --script .agents/tools/finalize/finalize_batch.py \\
        --function _build_prompt --min-len 1000

    # write it to the tool's templates/ folder
    python3 migrate_prompt.py extract --script ... --function _build_prompt \\
        --out .agents/tools/finalize/templates/finalize-worker.md

    # snapshot before editing
    python3 migrate_prompt.py preimage --script ...

    # after editing, prove nothing changed
    python3 migrate_prompt.py verify --script ... --function _build_prompt \\
        --kwargs-json samples/finalize.json
"""

from __future__ import annotations

import argparse
import ast
import difflib
import importlib.util
import json
import sys
from pathlib import Path

PREIMAGE_SUFFIX = "_preimage.py"


# ── extraction ───────────────────────────────────────────────────────────────


def joinedstr_to_template(node: ast.JoinedStr) -> tuple:
    """Rebuild an f-string as {{name}} template text.

    Returns (text, unresolved) where `unresolved` lists interpolations that are
    not bare names -- those need a human decision, because the expression has
    to move into the calling code.
    """
    parts, unresolved = [], []
    for v in node.values:
        if isinstance(v, ast.Constant) and isinstance(v.value, str):
            parts.append(v.value)
        elif isinstance(v, ast.FormattedValue):
            expr = ast.unparse(v.value)
            if expr.isidentifier():
                parts.append("{{" + expr + "}}")
            else:
                placeholder = (
                    expr.replace(".", "_")
                    .replace("(", "")
                    .replace(")", "")
                    .replace("[", "_")
                    .replace("]", "")
                    .replace(":", "_")
                    .replace(" ", "")
                )
                if not placeholder.isidentifier():
                    placeholder = "value{}".format(len(unresolved))
                parts.append("{{" + placeholder + "}}")
                unresolved.append((expr, placeholder))
    return "".join(parts), unresolved


def find_payload(tree: ast.AST, function: str, min_len: int):
    """Largest prompt-shaped string inside `function`."""
    best = None
    for fn in ast.walk(tree):
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if fn.name != function:
            continue
        for node in ast.walk(fn):
            if isinstance(node, ast.JoinedStr):
                size = sum(
                    len(v.value)
                    for v in node.values
                    if isinstance(v, ast.Constant) and isinstance(v.value, str)
                )
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                size = len(node.value)
            else:
                continue
            if size < min_len:
                continue
            if best is None or size > best[0]:
                best = (size, node)
    return best[1] if best else None


def cmd_extract(args) -> int:
    path = Path(args.script)
    tree = ast.parse(path.read_text(encoding="utf-8"))
    node = find_payload(tree, args.function, args.min_len)
    if node is None:
        print(
            "no payload >= {} chars in {}()".format(args.min_len, args.function),
            file=sys.stderr,
        )
        return 1
    if isinstance(node, ast.JoinedStr):
        text, unresolved = joinedstr_to_template(node)
    else:
        raw = node.value
        text = raw if isinstance(raw, str) else str(raw)
        unresolved = []

    if unresolved:
        print("EXPRESSIONS needing a variable in the caller:")
        for expr, name in unresolved:
            print("   {{{{{}}}}}  <-  {}".format(name, expr))
        print()
    if args.out:
        dest = Path(args.out)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if args.no_trailing_newline:
            text = text.rstrip("\n")
        dest.write_text(text, encoding="utf-8")
        print("wrote {} ({} chars)".format(dest, len(text)))
    else:
        sys.stdout.write(text)
    return 0


# ── preimage + verification ──────────────────────────────────────────────────


def preimage_path(script: Path) -> Path:
    return script.with_name("_" + script.stem + PREIMAGE_SUFFIX)


def cmd_preimage(args) -> int:
    script = Path(args.script)
    dest = preimage_path(script)
    dest.write_bytes(script.read_bytes())
    print("preimage -> {}".format(dest))
    print("(kept in-tree so PROJECT-relative imports still resolve)")
    return 0


def load(path: Path, alias: str):
    spec = importlib.util.spec_from_file_location(alias, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load {}".format(path))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[alias] = mod
    spec.loader.exec_module(mod)
    return mod


def norm(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def cmd_verify(args) -> int:
    script = Path(args.script)
    pre = preimage_path(script)
    if not pre.exists():
        print(
            "no preimage at {} -- run `preimage` before editing".format(pre),
            file=sys.stderr,
        )
        return 2

    kwargs = {}
    if args.kwargs_json:
        kwargs = json.loads(Path(args.kwargs_json).read_text(encoding="utf-8"))
    # Values tagged "path:<...>" become Path objects -- JSON has no such type,
    # and a builder that calls .name or .read_text() on a str would crash.
    for key, val in list(kwargs.items()):
        if isinstance(val, str) and val.startswith("path:"):
            kwargs[key] = Path(val[5:])
    posargs = json.loads(args.args_json) if args.args_json else []

    old = load(pre, "_pre_" + script.stem)
    new = load(script, "_new_" + script.stem)

    before = getattr(old, args.function)(*posargs, **kwargs)
    after = getattr(new, args.function)(*posargs, **kwargs)
    a, b = norm(before), norm(after)

    if a == b:
        print("IDENTICAL  {}()  ({} chars)".format(args.function, len(a)))
        if args.cleanup:
            pre.unlink()
            print("removed preimage")
        return 0

    print("DIFFERS    {}()".format(args.function))
    for i, line in enumerate(
        difflib.unified_diff(
            a.split("\n"),
            b.split("\n"),
            fromfile="before (inline)",
            tofile="after (template)",
            lineterm="",
        )
    ):
        print(line)
        if i > args.max_diff:
            print("... truncated")
            break
    return 1


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    e = sub.add_parser("extract")
    e.add_argument("--script", required=True)
    e.add_argument("--function", required=True)
    e.add_argument("--min-len", type=int, default=400)
    e.add_argument("--out")
    e.add_argument("--no-trailing-newline", action="store_true")
    e.set_defaults(fn=cmd_extract)

    p = sub.add_parser("preimage")
    p.add_argument("--script", required=True)
    p.set_defaults(fn=cmd_preimage)

    v = sub.add_parser("verify")
    v.add_argument("--script", required=True)
    v.add_argument("--function", required=True)
    v.add_argument("--kwargs-json")
    v.add_argument("--args-json")
    v.add_argument("--max-diff", type=int, default=60)
    v.add_argument(
        "--cleanup", action="store_true", help="delete the preimage when identical"
    )
    v.set_defaults(fn=cmd_verify)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
