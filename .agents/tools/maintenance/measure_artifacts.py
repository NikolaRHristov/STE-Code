#!/usr/bin/env python3
"""Measure artifact tiers: real bytes on disk + real LLM token counts.

Reads `ste-code/artifacts/<tier>/` (distilled) and `ste-code/artifacts/_base/<tier>/`
(deterministic boilerplate) and reports, per tier:

  * bytes on disk (sum of sub-document sizes, apparent size, not block size)
  * token count from real tokenizers (tiktoken o200k_base / cl100k_base)
  * distillation coverage (how many sub-docs are distilled vs still base)
  * projected final size, for tiers where distillation is incomplete

Token counts use `tiktoken`:
  o200k_base   GPT-4o, GPT-4.1, GPT-5, o-series
  cl100k_base  GPT-4, GPT-3.5-turbo, text-embedding-3

Claude and Llama tokenizers are not bundled; their counts sit within a few
percent of o200k_base for English prose, so o200k_base is the reported figure.

Usage:
    python3 .agents/tools/maintenance/measure_artifacts.py            # table
    python3 .agents/tools/maintenance/measure_artifacts.py --json     # machine readable
    python3 .agents/tools/maintenance/measure_artifacts.py --per-file # sub-doc breakdown
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[3]
ARTIFACTS = PROJECT / "ste-code" / "artifacts"
BASE = ARTIFACTS / "_base"

TIERS = ["level-2", "level-1", "level0", "level1", "level2", "level3", "level4", "level5"]

_ENCODERS: dict[str, "Any"] = {}


def encoder(name: str):
    """Return a cached tiktoken encoder, or None when tiktoken is absent."""
    if name not in _ENCODERS:
        try:
            import tiktoken  # type: ignore[import-not-found]
        except ImportError:
            return None
        _ENCODERS[name] = tiktoken.get_encoding(name)
    return _ENCODERS[name]


def count_tokens(text: str, enc_name: str = "o200k_base") -> int | None:
    enc = encoder(enc_name)
    if enc is None:
        return None
    return len(enc.encode(text, disallowed_special=()))


def subdocs(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    return sorted(p for p in directory.rglob("*") if p.is_file() and not p.name.startswith("."))


def measure_dir(directory: Path) -> dict:
    files = subdocs(directory)
    total_bytes = 0
    total_o200k = 0
    total_cl100k = 0
    per_file = []
    for path in files:
        raw = path.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        n_bytes = len(raw)
        o200k = count_tokens(text, "o200k_base")
        cl100k = count_tokens(text, "cl100k_base")
        total_bytes += n_bytes
        total_o200k += o200k or 0
        total_cl100k += cl100k or 0
        per_file.append(
            {
                "path": str(path.relative_to(PROJECT)),
                "bytes": n_bytes,
                "tokens_o200k": o200k,
                "tokens_cl100k": cl100k,
            }
        )
    return {
        "files": len(files),
        "bytes": total_bytes,
        "tokens_o200k": total_o200k,
        "tokens_cl100k": total_cl100k,
        "per_file": per_file,
        "largest_bytes": max((f["bytes"] for f in per_file), default=0),
    }


def measure_tier(tier: str) -> dict:
    dist = measure_dir(ARTIFACTS / tier)
    base = measure_dir(BASE / tier)

    dist_names = {Path(f["path"]).name for f in dist["per_file"]}
    base_names = {Path(f["path"]).name for f in base["per_file"] if Path(f["path"]).name != "_index.md"}
    pending = sorted(base_names - dist_names)

    # Projection: distilled sub-docs keep their measured size; sub-docs still
    # only present in _base are projected at the compression ratio already
    # observed for this tier (distilled bytes / matching base bytes).
    base_by_name = {Path(f["path"]).name: f for f in base["per_file"]}
    matched_base_bytes = sum(base_by_name[n]["bytes"] for n in dist_names if n in base_by_name)
    matched_dist_bytes = sum(f["bytes"] for f in dist["per_file"] if Path(f["path"]).name in base_by_name)
    ratio = (matched_dist_bytes / matched_base_bytes) if matched_base_bytes else 1.0

    pending_base_bytes = sum(base_by_name[n]["bytes"] for n in pending)
    pending_base_tokens = sum(base_by_name[n]["tokens_o200k"] or 0 for n in pending)
    projected_bytes = dist["bytes"] + int(pending_base_bytes * ratio)
    projected_tokens = dist["tokens_o200k"] + int(pending_base_tokens * ratio)

    return {
        "tier": tier,
        "distilled": {k: v for k, v in dist.items() if k != "per_file"},
        "base": {k: v for k, v in base.items() if k != "per_file"},
        "pending_subdocs": pending,
        "compression_ratio": round(ratio, 4),
        "projected_bytes": projected_bytes,
        "projected_tokens_o200k": projected_tokens,
        "complete": not pending,
        "per_file": dist["per_file"],
    }


def human_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n / (1024 * 1024):.2f} MB"


def human_tokens(n: int) -> str:
    if n < 1000:
        return f"{n}"
    if n < 1_000_000:
        return f"{n / 1000:.1f}K"
    return f"{n / 1_000_000:.2f}M"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="emit JSON")
    ap.add_argument("--per-file", action="store_true", help="print per sub-document rows")
    args = ap.parse_args()

    if encoder("o200k_base") is None:
        print("error: tiktoken is not installed; run `pip install tiktoken`", file=sys.stderr)
        return 2

    results = [measure_tier(t) for t in TIERS if (ARTIFACTS / t).is_dir()]

    if args.json:
        print(json.dumps({"tiers": results}, indent=2))
        return 0

    print(f"{'Tier':<9} {'Files':>5} {'Bytes':>10} {'o200k':>9} {'cl100k':>9} "
          f"{'Largest':>9} {'Projected':>10} {'Pending':>8}")
    print("-" * 82)
    for r in results:
        d = r["distilled"]
        print(
            f"{r['tier']:<9} {d['files']:>5} {human_bytes(d['bytes']):>10} "
            f"{human_tokens(d['tokens_o200k']):>9} {human_tokens(d['tokens_cl100k']):>9} "
            f"{human_bytes(d['largest_bytes']):>9} "
            f"{human_tokens(r['projected_tokens_o200k']):>10} {len(r['pending_subdocs']):>8}"
        )

    if args.per_file:
        for r in results:
            print(f"\n== {r['tier']}")
            for f in r["per_file"]:
                print(f"  {human_bytes(f['bytes']):>9} {human_tokens(f['tokens_o200k']):>8}  "
                      f"{Path(f['path']).name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
