#!/usr/bin/env python3
"""Stdlib-only fuzz corpus generator for the jail's shell argument analyser.

Generates adversarial ``terminal`` command strings and feeds each one to
``core.analysis.write_targets``, recording the command, the targets the
analyser extracted and a verdict flag into a JSONL corpus.

No third-party imports: the repo forbids external runtime dependencies.

Usage::

    python3 .agents/hermes/jail/tests/fuzz_corpus_generator.py 3000
    python3 .agents/hermes/jail/tests/fuzz_corpus_generator.py --count 10000

Exit status is non-zero ONLY when the analyser raised on some input, which is
a genuine defect worth reporting.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from typing import Dict, List, Tuple

JAIL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(JAIL_ROOT)))

if JAIL_ROOT not in sys.path:
    sys.path.insert(0, JAIL_ROOT)

from core import analysis  # noqa: E402  (path injection must come first)

DEFAULT_OUT = os.path.join(JAIL_ROOT, "tests", "fuzz_corpus.jsonl")

VERBS = [
    "mkdir",
    "touch",
    "rm",
    "cp",
    "mv",
    "ln",
    "tee",
    "dd",
    "tar",
    "unzip",
    "git",
    "curl",
    "wget",
    "sort",
    "gcc",
    "ps",
    "sed",
    "python3",
    "sh",
    "echo",
    "cat",
    "chmod",
    "rsync",
    "npm",
    "docker",
    "sudo",
    "env",
    "xargs",
    "nice",
]

REPO_RELATIVE = [
    ".agents/x",
    "Makefile",
    "tests/out.txt",
    "./build/artifact.o",
    ".agents/hermes/jail/core/analysis.py",
    "src/main.c",
    "a/b/c.txt",
]

REPO_ABSOLUTE = [
    os.path.join(REPO_ROOT, "Makefile"),
    os.path.join(REPO_ROOT, ".agents", "x"),
    os.path.join(REPO_ROOT, "tests", "out.txt"),
]

PARENT_ABSOLUTE = [
    "../x",
    "../../escape.txt",
    "../..",
    os.path.expanduser("~/.."),
    os.path.join(REPO_ROOT, "..", "sibling.txt"),
    "./../../out",
]

TMP_PATHS = [
    "/tmp/x",
    "/tmp/fuzz/out.log",
    "/var/tmp/y",
    "/dev/null",
    "/dev/stderr",
    "/dev/rdisk1",
]

HOME_PATHS = [
    "~/x",
    "~/.hermes/skills/a.md",
    "$HOME/y",
    "${HOME}/z/out",
    "~/../etc/passwd",
]

PATH_POOLS = [REPO_RELATIVE, REPO_ABSOLUTE, PARENT_ABSOLUTE, TMP_PATHS, HOME_PATHS]

PLAIN_FLAGS = [
    "-p",
    "-r",
    "-f",
    "-v",
    "-a",
    "-l",
    "-n",
    "-q",
    "--force",
    "--verbose",
    "-czf",
    "-xzf",
    "-tzf",
    "-9",
]

TRICKY_FLAGS = [
    "-o",
    "--output",
    "-C",
    "--directory",
    "-d",
    "-O",
    "--output-document",
    "--output-dir",
    "--backup-dir",
]

ATTACHED_FLAGS = ["--output={p}", "--directory={p}", "-o{p}", "of={p}"]

REDIRECTS = [">", ">>", "2>", "&>", "1>", "2>>", ">|"]
CHAINS = ["&&", ";", "|", "||", "\n", "&"]
WRAPPERS = [
    "sudo",
    "env",
    "xargs",
    "nice -n 5",
    "sudo -u root",
    "env -C /tmp",
    "xargs -I{}",
    "timeout 5",
    "nohup",
]


class CorpusGenerator:
    """Produces adversarial shell-command strings for the analyser."""

    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()

    # -- pieces ----------------------------------------------------------
    def path(self) -> str:
        pool = self.rng.choice(PATH_POOLS)
        raw = self.rng.choice(pool)
        return self.quote(raw)

    def quote(self, raw: str) -> str:
        roll = self.rng.random()
        if roll < 0.12:
            return '"%s"' % raw
        if roll < 0.20:
            return "'%s'" % raw
        if roll < 0.24 and " " not in raw:
            return raw.replace("/", "/", 1)
        return raw

    def flag(self) -> str:
        roll = self.rng.random()
        if roll < 0.55:
            return self.rng.choice(PLAIN_FLAGS)
        if roll < 0.85:
            return self.rng.choice(TRICKY_FLAGS)
        return self.rng.choice(ATTACHED_FLAGS).format(
            p=self.rng.choice(self.rng.choice(PATH_POOLS))
        )

    def simple_segment(self) -> List[str]:
        verb = self.rng.choice(VERBS)
        parts: List[str] = []
        if self.rng.random() < 0.18:
            parts.append(self.rng.choice(WRAPPERS))
        if self.rng.random() < 0.08:
            parts.append("HOME=/tmp/fakehome")
        parts.append(verb)
        if verb in {"python3", "sh"} and self.rng.random() < 0.5:
            inner = self.rng.choice(
                [
                    "import os; os.makedirs('%s')"
                    % self.rng.choice(self.rng.choice(PATH_POOLS)),
                    "open('%s','w').write('x')"
                    % self.rng.choice(self.rng.choice(PATH_POOLS)),
                    "cd .. && mkdir %s" % self.rng.choice(PARENT_ABSOLUTE),
                ]
            )
            parts.extend(["-c", "'%s'" % inner])
            return parts
        for _ in range(self.rng.randint(0, 3)):
            parts.append(self.flag())
            if parts[-1] in TRICKY_FLAGS and self.rng.random() < 0.8:
                parts.append(self.path())
        for _ in range(self.rng.randint(1, 3)):
            parts.append(self.path())
        if self.rng.random() < 0.35:
            parts.append(self.rng.choice(REDIRECTS))
            parts.append(self.path())
        return parts

    def random_command(self) -> str:
        """Return one adversarial command string of roughly 15-25 tokens."""
        tokens: List[str] = []
        if self.rng.random() < 0.25:
            tokens.extend(
                [
                    self.rng.choice(
                        ["cd ..", "cd ../..", "cd /tmp", "cd $HOME", "cd ${HOME}/x"]
                    ),
                    self.rng.choice(["&&", ";"]),
                ]
            )
        target = self.rng.randint(15, 25)
        while len(tokens) < target:
            tokens.extend(self.simple_segment())
            if len(tokens) < target:
                tokens.append(self.rng.choice(CHAINS))
        while tokens and tokens[-1] in CHAINS:
            tokens.pop()
        text = " ".join(tokens)
        if self.rng.random() < 0.05:
            text = "( %s )" % text
        return text


def run(count: int, out_path: str, seed: int | None) -> Tuple[int, int, int]:
    gen = CorpusGenerator(random.Random(seed))
    crashed = 0
    total_targets = 0
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        for index in range(count):
            command = gen.random_command()
            record: Dict[str, object] = {"i": index, "command": command}
            try:
                targets = analysis.write_targets(
                    "terminal", {"command": command}, REPO_ROOT
                )
                record["targets"] = [
                    {"label": label, "path": path} for label, path in targets
                ]
                record["verdict"] = "ok"
                total_targets += len(targets)
            except Exception as exc:  # noqa: BLE001 - a crash IS the finding
                crashed += 1
                record["targets"] = []
                record["verdict"] = "crash"
                record["error"] = "%s: %s" % (type(exc).__name__, exc)
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return count, crashed, total_targets


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "count_pos",
        nargs="?",
        type=int,
        default=None,
        help="number of commands (positional shorthand)",
    )
    parser.add_argument("--count", type=int, default=10000)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args(argv)

    count = args.count_pos if args.count_pos is not None else args.count
    generated, crashed, total_targets = run(count, args.out, args.seed)

    print("corpus:    %s" % args.out)
    print("generated: %d" % generated)
    print("crashed:   %d" % crashed)
    print("targets:   %d" % total_targets)
    if crashed:
        print("BUG: the analyser raised on %d input(s)." % crashed)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
