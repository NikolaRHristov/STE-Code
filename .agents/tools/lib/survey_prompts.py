#!/usr/bin/env python3
"""Survey embedded LLM prompts across .agents scripts.

Read-only reconnaissance. Finds string literals that are actually sent to a
model, as opposed to docstrings, log lines and SQL. The distinction matters:
extracting a docstring into a prompt file would be a regression, and missing a
real prompt would silently drop behaviour.

A string scores as a prompt on evidence, not vibes:
  - it flows into a known dispatch site (hermes -z, subprocess with a model
    flag, an LLM client call), or
  - it carries instruction-shaped markers (imperative openers, role framing,
    output contracts) AND placeholders.

Usage:
    python3 .agents/tools/lib/survey_prompts.py            # table
    python3 .agents/tools/lib/survey_prompts.py --json     # machine readable
"""

from __future__ import annotations

import argparse
import ast
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
AGENTS = HERE.parent.parent.parent  # .agents/
ROOT = AGENTS.parent

SKIP_PARTS = {"vendor", "archive", "__pycache__", "_scratch", "node_modules"}

# Placeholder dialects already in the tree. Order matters only for reporting.
PLACEHOLDER_PATTERNS = [
    ("angle_double", re.compile(r"<<[A-Z0-9_]+>>")),  # <<START>>
    ("brace_double", re.compile(r"\{\{[a-zA-Z0-9_]+\}\}")),  # {{name}}
    ("dollar_brace", re.compile(r"\$\{[a-zA-Z0-9_]+\}")),  # ${name}
    ("percent_named", re.compile(r"%\([a-zA-Z0-9_]+\)s")),  # %(name)s
    ("brace_named", re.compile(r"(?<!\{)\{[a-zA-Z_][a-zA-Z0-9_]*\}(?!\})")),
    ("brace_index", re.compile(r"(?<!\{)\{\d*\}(?!\})")),  # {} / {0}
]

# Instruction-shaped signals.
ROLE = re.compile(
    r"\b(you are|your job|your task|act as|you will|you must|as an? "
    r"(?:expert|agent|orchestrator|reviewer|worker))\b",
    re.I,
)
IMPERATIVE = re.compile(
    r"^\s*(read|write|extract|refine|adapt|generate|produce|analyse|analyze|"
    r"summarize|summarise|convert|rewrite|review|verify|check|classify|"
    r"translate|explain|list|output|return|do not|never|always)\b",
    re.I | re.M,
)
OUTPUT_CONTRACT = re.compile(
    r"\b(output only|reply with|respond with|return only|strict json|"
    r"do not (?:summarize|summarise|explain|preface|add)|"
    r"output contract|markdown only|no prose|no commentary)\b",
    re.I,
)
RUBRIC = re.compile(r"^\s*(?:\d+[.)]|[-*])\s+\S", re.M)

# Things that look wordy but are not prompts.
SQL = re.compile(r"\b(SELECT|INSERT INTO|CREATE TABLE|UPDATE\s+\w+\s+SET)\b")
ARGPARSE_HELP = re.compile(r"^\s*(usage:|%\(prog\)s)", re.I)

# Dispatch evidence: a call that ships text to a model.
MODEL_CALL_HINTS = re.compile(
    r"hermes\b|--yolo|\bmodel\b|completions?\.create|messages\.create|"
    r"chat\.completions|invoke_model|generate_content",
    re.I,
)


def iter_scripts(root: Path):
    for path in sorted(root.rglob("*.py")):
        if SKIP_PARTS & set(path.parts):
            continue
        yield path


def placeholders(text: str) -> dict:
    found = {}
    for name, rx in PLACEHOLDER_PATTERNS:
        hits = rx.findall(text)
        if hits:
            found[name] = sorted(set(hits))[:12]
    return found


def classify(node: ast.Constant, text: str, docstrings: set) -> dict:
    """Score one string literal. Returns a verdict dict."""
    signals = []
    if id(node) in docstrings:
        signals.append("docstring")
    if ROLE.search(text):
        signals.append("role")
    if OUTPUT_CONTRACT.search(text):
        signals.append("output_contract")
    if IMPERATIVE.search(text):
        signals.append("imperative")
    if len(RUBRIC.findall(text)) >= 3:
        signals.append("rubric")
    ph = placeholders(text)
    if ph:
        signals.append("placeholders")
    if SQL.search(text):
        signals.append("sql")
    if ARGPARSE_HELP.search(text):
        signals.append("argparse")

    strong = {"role", "output_contract"}
    weak = {"imperative", "rubric", "placeholders"}
    disqualify = {"sql", "argparse"}

    verdict = "other"
    if not disqualify & set(signals):
        if strong & set(signals):
            verdict = "prompt"
        elif len(weak & set(signals)) >= 2:
            verdict = "likely_prompt"
        elif "docstring" in signals:
            verdict = "docstring"
    elif "sql" in signals:
        verdict = "sql"
    elif "argparse" in signals:
        verdict = "argparse"

    # A docstring can still be a prompt (some tools use module docs as briefs),
    # but only if it carries an output contract -- otherwise it is just docs.
    if "docstring" in signals and verdict in ("prompt", "likely_prompt"):
        if "output_contract" not in signals:
            verdict = "docstring"

    return {"verdict": verdict, "signals": signals, "placeholders": ph}


def collect_docstring_ids(tree: ast.AST) -> set:
    out = set()
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
        ):
            body = getattr(node, "body", None)
            if (
                body
                and isinstance(body[0], ast.Expr)
                and isinstance(body[0].value, ast.Constant)
                and isinstance(body[0].value.value, str)
            ):
                out.add(id(body[0].value))
    return out


def survey(root: Path, min_len: int = 200) -> dict:
    rows = []
    per_file = defaultdict(lambda: Counter())
    for path in iter_scripts(root):
        try:
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src)
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        docs = collect_docstring_ids(tree)
        dispatches = bool(MODEL_CALL_HINTS.search(src))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            text = node.value
            if len(text) < min_len:
                continue
            info = classify(node, text, docs)
            if info["verdict"] in ("prompt", "likely_prompt"):
                info["file_dispatches_to_model"] = dispatches
            rel = str(path.relative_to(root.parent))
            per_file[rel][info["verdict"]] += 1
            rows.append(
                {
                    "file": rel,
                    "line": node.lineno,
                    "chars": len(text),
                    "verdict": info["verdict"],
                    "signals": info["signals"],
                    "placeholders": info["placeholders"],
                    "dispatches": dispatches,
                    "head": " ".join(text.strip().split())[:120],
                }
            )
    return {"rows": rows, "per_file": {k: dict(v) for k, v in per_file.items()}}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=str(AGENTS))
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-len", type=int, default=200)
    ap.add_argument("--only", default=None, help="filter by verdict, e.g. prompt")
    args = ap.parse_args()

    data = survey(Path(args.root).resolve(), args.min_len)
    rows = data["rows"]
    if args.only:
        rows = [r for r in rows if r["verdict"] == args.only]

    if args.json:
        print(json.dumps({"rows": rows, "per_file": data["per_file"]}, indent=2))
        return 0

    tally = Counter(r["verdict"] for r in data["rows"])
    print("scanned {} literals >= {} chars".format(len(data["rows"]), args.min_len))
    for k, v in tally.most_common():
        print("  {:<16} {}".format(k, v))
    print()
    real = [r for r in rows if r["verdict"] in ("prompt", "likely_prompt")]
    print("prompt candidates: {}".format(len(real)))
    by_file = defaultdict(list)
    for r in real:
        by_file[r["file"]].append(r)
    for f in sorted(by_file):
        group = by_file[f]
        disp = "→model" if group[0]["dispatches"] else "      "
        print(
            "\n{} {}  ({} candidate{})".format(
                disp, f, len(group), "" if len(group) == 1 else "s"
            )
        )
        for r in group:
            ph = ",".join(r["placeholders"]) or "-"
            print(
                "    L{:<5} {:>6}c  {:<14} ph={:<24} {}".format(
                    r["line"], r["chars"], r["verdict"], ph, r["head"][:70]
                )
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
