#!/usr/bin/env python3
"""Prove a prompt migration changed nothing but where the text lives.

A prompt migration is a MOVE, not a rewrite. If the rendered template differs
from the original inline prompt by even a word, model behaviour changes and no
test downstream will notice. This makes that check mechanical.

Usage
-----
Capture the original prompt BEFORE migrating (from the pre-migration script):

    python3 verify_prompt_move.py capture --name refine-worker --stdin < old.txt

Then after migrating, render the template with the same variables and compare:

    python3 verify_prompt_move.py check --name refine-worker \\
        --template .agents/tools/refinement/templates/refine-worker.md \\
        --var input_filename=w001-p1-4.md --var start_page=1 --var end_page=4

Exit code 0 means byte-identical (modulo the normalization below). Anything else
prints a unified diff and exits 1.

Normalization
-------------
Line endings and trailing whitespace are normalized before comparison: the repo
mixes CRLF and LF, and that difference is not semantic. Everything else --
wording, spacing inside a line, blank-line structure -- must match exactly.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
STORE = HERE / ".prompt-baselines"


def normalize(text: str) -> str:
    """Strip differences that are not semantic: CRLF, trailing space, final NL."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [ln.rstrip() for ln in text.split("\n")]
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def load_templater():
    """Import templater.py by path (it lives beside this file)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "templater", str(HERE / "templater.py")
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load templater.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def cmd_capture(args) -> int:
    STORE.mkdir(parents=True, exist_ok=True)
    text = (
        sys.stdin.read() if args.stdin else Path(args.file).read_text(encoding="utf-8")
    )
    dest = STORE / "{}.txt".format(args.name)
    dest.write_text(text, encoding="utf-8")
    print("captured {} chars -> {}".format(len(text), dest))
    return 0


def cmd_check(args) -> int:
    baseline_path = STORE / "{}.txt".format(args.name)
    if not baseline_path.exists():
        print(
            "no baseline for '{}' -- run capture first".format(args.name),
            file=sys.stderr,
        )
        return 2
    baseline = normalize(baseline_path.read_text(encoding="utf-8"))

    variables = {}
    for pair in args.var or []:
        if "=" not in pair:
            print("bad --var {!r}, expected name=value".format(pair), file=sys.stderr)
            return 2
        k, v = pair.split("=", 1)
        variables[k] = v
    if args.vars_json:
        variables.update(json.loads(Path(args.vars_json).read_text(encoding="utf-8")))

    tpl = load_templater()
    rendered = tpl.render_template(
        Path(args.template), strict=not args.loose, **variables
    )
    rendered = normalize(rendered)

    if rendered == baseline:
        print("IDENTICAL  {} ({} chars)".format(args.name, len(rendered)))
        return 0

    print("DIFFERS    {}".format(args.name))
    diff = difflib.unified_diff(
        baseline.split("\n"),
        rendered.split("\n"),
        fromfile="inline (before)",
        tofile="template (after)",
        lineterm="",
    )
    shown = 0
    for line in diff:
        print(line)
        shown += 1
        if shown > args.max_diff:
            print("... diff truncated at {} lines".format(args.max_diff))
            break
    return 1


def cmd_list(args) -> int:
    if not STORE.exists():
        print("no baselines captured")
        return 0
    for p in sorted(STORE.glob("*.txt")):
        print("{:<40} {:>7} chars".format(p.stem, len(p.read_text(encoding="utf-8"))))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("capture", help="store the pre-migration prompt")
    c.add_argument("--name", required=True)
    c.add_argument("--file")
    c.add_argument("--stdin", action="store_true")
    c.set_defaults(fn=cmd_capture)

    k = sub.add_parser("check", help="render a template and compare")
    k.add_argument("--name", required=True)
    k.add_argument("--template", required=True)
    k.add_argument("--var", action="append")
    k.add_argument("--vars-json")
    k.add_argument(
        "--loose",
        action="store_true",
        help="non-strict render (leaves unknown placeholders)",
    )
    k.add_argument("--max-diff", type=int, default=60)
    k.set_defaults(fn=cmd_check)

    ls = sub.add_parser("list", help="show captured baselines")
    ls.set_defaults(fn=cmd_list)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
