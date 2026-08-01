#!/usr/bin/env python3
"""Anonymization layer for harness artifacts.

Benchmark output routinely travels further than the machine that produced it:
into a repository, a pull request, a paper, a bug report. Anything that leaves
this machine must not carry the operator's identity, home directory, hostname,
or the internal name of the corpus under test.

This module redacts on the way OUT. It never changes what is measured, only how
it is reported, so an anonymized report and a raw report describe the same run.

Three levels:

  ``off``      no redaction (local debugging)
  ``paths``    filesystem identity only: absolute paths become root-relative,
               home directories collapse to ``~``, usernames and hostnames are
               masked. Numbers, labels and technique names survive intact.
  ``full``     ``paths`` plus semantic identity: the profile name, variant
               labels and directory names are replaced by stable pseudonyms
               (``variant-a1b2``), so the shape of the result is publishable
               without disclosing the corpus.

Pseudonyms are deterministic: the same input maps to the same alias for a given
salt, so two anonymized reports of the same run remain diffable and joinable.
Without the salt the mapping is not reversible.
"""
from __future__ import annotations

import getpass
import hashlib
import os
import re
import socket
from pathlib import Path

LEVELS = ("off", "paths", "full")
DEFAULT_SALT = "harness"


def _alias(value: str, prefix: str, salt: str, width: int = 4) -> str:
    digest = hashlib.blake2s(f"{salt}:{value}".encode("utf-8"), digest_size=8).hexdigest()
    return f"{prefix}-{digest[:width]}"


class Anonymizer:
    """Redacts identity from strings and JSON-like structures."""

    def __init__(self, level: str = "paths", *, root: "Path | None" = None,
                 salt: str = DEFAULT_SALT, extra_terms: "list[str] | None" = None) -> None:
        if level not in LEVELS:
            raise ValueError(f"unknown anonymization level {level!r}; expected one of {LEVELS}")
        self.level = level
        self.root = Path(root).resolve() if root else None
        self.salt = salt
        self._cache: "dict[str, str]" = {}

        terms = []
        for candidate in (extra_terms or []):
            if candidate:
                terms.append(str(candidate))
        # Machine identity. Collected defensively: any of these may fail in a
        # sandbox, and a failure must not disable redaction of the others.
        for getter in (lambda: getpass.getuser(), lambda: socket.gethostname(),
                       lambda: os.uname().nodename):
            try:
                value = getter()
            except Exception:
                continue
            if value and len(value) > 2:
                terms.append(value)
        if self.root is not None:
            terms.append(self.root.name)
            for part in self.root.parts:
                if len(part) > 2 and part not in ("/", "Users", "home", "Volumes"):
                    terms.append(part)
        # Longest first so that a containing term is masked before its substring.
        self.terms = sorted({t for t in terms if len(t) > 2}, key=len, reverse=True)

    # ------------------------------------------------------------- primitives

    @property
    def active(self) -> bool:
        return self.level != "off"

    def path(self, value: "str | Path") -> str:
        """Render a path without machine identity."""
        if not self.active:
            return str(value)
        text = str(value)
        if self.root is not None:
            try:
                return str(Path(text).resolve().relative_to(self.root))
            except (ValueError, OSError):
                pass
        home = str(Path.home())
        if text.startswith(home):
            text = "~" + text[len(home):]
        return self.text(text)

    def text(self, value: str) -> str:
        """Mask identity terms anywhere inside a free-text string."""
        if not self.active or not value:
            return value
        out = value
        for term in self.terms:
            if term in out:
                out = out.replace(term, _alias(term, "x", self.salt))
        # Any surviving absolute path is collapsed to its final component.
        out = re.sub(r"(/Users/|/home/|/Volumes/)[^\s'\"]+",
                     lambda m: ".../" + m.group(0).rstrip("/").rsplit("/", 1)[-1], out)
        return out

    def label(self, value: str, prefix: str = "label") -> str:
        """Pseudonymize a semantic label (only at ``full``)."""
        if self.level != "full" or not value:
            return value
        if value not in self._cache:
            self._cache[value] = _alias(value, prefix, self.salt)
        return self._cache[value]

    def variant(self, key: str) -> str:
        return self.label(key, "variant") if self.level == "full" else key

    # ---------------------------------------------------------------- mapping

    def report(self, document: dict) -> dict:
        """Return an anonymized copy of a stitch report.

        Only identity-bearing fields are touched; every count, rate and matrix
        cell is copied through unchanged.
        """
        if not self.active:
            return document
        import copy

        doc = copy.deepcopy(document)
        doc["anonymized"] = {"level": self.level, "salt_used": bool(self.salt)}

        profile = doc.get("profile", {})
        if isinstance(profile, dict):
            if "source" in profile:
                profile["source"] = self.path(profile["source"])
            if self.level == "full":
                profile["id"] = self.label(str(profile.get("id", "")), "profile")
                profile["display_name"] = self.label(
                    str(profile.get("display_name", "")), "corpus")
        if "base" in doc:
            doc["base"] = self.path(doc["base"])

        if self.level == "full":
            doc["variants"] = [self.variant(v) for v in doc.get("variants", [])]
            for row in doc.get("variant_ranking", []) or []:
                row["variant"] = self.variant(str(row.get("variant", "")))
                row["label"] = self.label(str(row.get("label", "")), "cfg")
                row["directory"] = self.label(str(row.get("directory", "")), "dir")
            timelines = doc.get("timelines")
            if isinstance(timelines, dict):
                doc["timelines"] = {self.variant(k): v for k, v in timelines.items()}
            cov = doc.get("coverage", {})
            if isinstance(cov, dict) and cov.get("missing"):
                cov["missing"] = [self.text(m) for m in cov["missing"]]
        return doc

    def markdown(self, text: str) -> str:
        return self.text(text) if self.active else text


def add_arguments(parser) -> None:
    """Attach the shared anonymization flags to a CLI parser."""
    parser.add_argument("--anonymize", choices=LEVELS, default="paths",
                        help="redaction level for emitted reports (default: paths)")
    parser.add_argument("--anonymize-salt", default=DEFAULT_SALT,
                        help="salt for deterministic pseudonyms; change to break linkability")


def from_args(args, root: "Path | None" = None,
              extra_terms: "list[str] | None" = None) -> Anonymizer:
    return Anonymizer(getattr(args, "anonymize", "paths"), root=root,
                      salt=getattr(args, "anonymize_salt", DEFAULT_SALT),
                      extra_terms=extra_terms)


if __name__ == "__main__":
    import json
    import sys

    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sample = {
        "profile": {"id": "corpus-x", "display_name": "Corpus X",
                    "source": str(root / "config" / "harness.json")},
        "base": str(root / "results" / "redblue"),
        "variants": ["0", "1"],
        "variant_ranking": [{"variant": "0", "label": "baseline", "directory": "level0",
                             "total_escapes": 12}],
        "timelines": {"0": [{"round": 1, "escapes": 12}]},
        "coverage": {"missing": [str(root / "results" / "redblue" / "v0")]},
    }
    for level in LEVELS:
        anon = Anonymizer(level, root=root)
        print(f"--- level={level} ---")
        print(json.dumps(anon.report(sample), indent=2)[:700])
