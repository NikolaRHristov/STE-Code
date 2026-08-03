#!/usr/bin/env python3
"""Capsule-sequenced execution engine (Unit 2).

Reads a ``sequence.yaml`` from the harness profile directory, resolves the
``sees`` dependency DAG, and runs each capsule in dependency order, passing only
the ``sees``-scoped escape corpus to BLUE capsules. Colours are unchanged: they
write the same sentinels, and BLUE accepts a scoped escape file via
``--escape-override``.

A run WITHOUT a sequence file degrades to the existing fixed order (backward
compatible) -- callers simply do not invoke ``run_sequence``.

Offline (--skip-live) timing offsets are encoded as ``timing`` metadata on the
scoped escapes (``delayed_<N>s``) so temporal patterns are visible in the
knowledge base without real wall-clock delays.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

import yaml

BENCH = Path(__file__).resolve().parent


def load_sequence(cfg, name: str = "sequence.yaml") -> "list[dict]":
    """Load all sequence definitions from the profile directory.

    The file may contain multiple YAML documents (one per topology); returns a
    list of sequence dicts. Returns [] if absent (caller falls back to the
    legacy fixed order)."""
    path = cfg.profile_dir / name
    if not path.exists():
        return []
    try:
        docs = [
            d
            for d in yaml.safe_load_all(path.read_text(encoding="utf-8"))
            if isinstance(d, dict)
        ]
    except (yaml.YAMLError, OSError):
        return []
    return docs


def resolve_order(seq: dict) -> "list[dict]":
    """Topologically sort capsules by ``sees``. Raises ValueError on a cycle."""
    caps = {c["id"]: c for c in seq.get("capsules", [])}
    order: "list[dict]" = []
    seen: "set[str]" = set()
    # repeated passes (small N; clear over Kahn-like greedy)
    remaining = dict(caps)
    while remaining:
        progressed = False
        for cid in list(remaining):
            deps = remaining[cid].get("sees", []) or []
            if all(d in seen for d in deps):
                order.append(remaining.pop(cid))
                seen.add(cid)
                progressed = True
        if not progressed:
            raise ValueError(
                "cycle in capsule sees graph: {}".format(sorted(remaining))
            )
    return order


def _scoped_escapes(
    base: Path, seq_id: str, capsule: dict, all_capsules: "dict[str, dict]"
) -> "Path | None":
    """Build (and write) the sees-scoped escape file for a BLUE capsule.

    A BLUE capsule at position p with sees=[R1,R2] reads the escape files from
    those RED capsules' conventional locations. Returns the path to the scoped
    file, or None if there is nothing to scope (unusual).
    """
    import json

    seen = capsule.get("sees", []) or []
    if not seen:
        return None
    collected = []
    for dep_id in seen:
        dep = all_capsules.get(dep_id)
        if not dep:
            continue
        rnd = int(dep.get("round", 1))
        variant = str(dep.get("variant", "0"))
        src = base / f"variant{variant}" / f"round{rnd}" / "escapes.json"
        if src.exists():
            try:
                collected.extend(json.loads(src.read_text()))
            except (json.JSONDecodeError, OSError):
                pass
    if not collected:
        return None
    # encode timing offset for offline temporal modelling
    offset = float(capsule.get("timing_offset_s", 0) or 0)
    if offset > 0:
        for e in collected:
            e["timing"] = "delayed_{}s".format(int(offset))
    out_dir = base / "capsules" / seq_id
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{capsule['id']}-escapes.json"
    out_path.write_text(json.dumps(collected, indent=2), encoding="utf-8")
    return out_path


def run_sequence(
    base: Path,
    seq: dict,
    cfg,
    *,
    skip_live: bool = True,
    await_timeout: float = 120.0,
    poll: float = 1.0,
) -> "list[dict]":
    """Execute a capsule sequence. Returns a list of per-capsule result records.

    Each capsule is launched as a subprocess of its colour module (red.py /
    blue.py). Sentinel polling reuses the colours' own handshake files, so no
    colour code changes except BLUE's ``--escape-override`` switch (added for
    this unit).
    """
    import json

    seq_id = seq.get("sequence_id", "seq")
    all_caps = {c["id"]: c for c in seq.get("capsules", [])}
    order = resolve_order(seq)
    results = []
    sentinels: "dict[str, Path]" = {}

    for cap in order:
        cid = cap["id"]
        colour = cap.get("colour", "RED").lower()
        variant = str(cap.get("variant", "0"))
        rnd = int(cap.get("round", 1))
        offset = float(cap.get("timing_offset_s", 0) or 0)

        # simulate wall-clock timing offset offline (real delay only if live)
        if offset > 0 and not skip_live:
            time.sleep(min(offset, 5.0))  # cap real waits in this harness

        # wait for all seen sentinels to exist (the sees DAG)
        for dep in cap.get("sees", []) or []:
            dep_path = sentinels.get(dep)
            if dep_path and not _await_file(dep_path, await_timeout, poll):
                results.append(
                    {"id": cid, "status": "await-timeout", "missing_dep": dep}
                )
                break
        else:
            # build scoped escapes for BLUE
            extra = []
            if colour == "blue":
                scoped = _scoped_escapes(base, seq_id, cap, all_caps)
                if scoped:
                    extra = ["--escape-override", str(scoped)]

            module = "red" if colour == "red" else "blue"
            cmd = [
                sys.executable,
                str(BENCH / f"{module}.py"),
                "--skip-live" if skip_live else "--model",
                "tencent/hy3:free" if not skip_live else "",
                "--tiers",
                variant,
                "--rounds",
                str(rnd),
                "--base",
                str(base),
                "--await-timeout",
                str(await_timeout),
                "--poll-interval",
                str(poll),
            ] + extra
            if colour == "blue":
                intent = cap.get("intent", "adversarial")
                if intent in ("helpful", "hybrid"):
                    cmd += ["--blue-intent", intent]
            cmd = [c for c in cmd if c]  # drop empty model arg
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(BENCH),
                timeout=int(await_timeout) + 60,
            )
            # record sentinel location for dependents
            sentinel = (
                base
                / f"variant{variant}"
                / f"round{rnd}"
                / ("purple.json" if colour == "red" else "blue-done.json")
            )
            sentinels[cid] = sentinel
            results.append(
                {
                    "id": cid,
                    "colour": colour,
                    "variant": variant,
                    "round": rnd,
                    "status": "done" if proc.returncode == 0 else "error",
                    "rc": proc.returncode,
                    "sentinel": str(sentinel),
                }
            )
    return results


def _await_file(path: Path, timeout: float, poll: float) -> bool:
    """Bounded wait for a sentinel file (mirrors the colours' own await)."""
    import os

    deadline = time.time() + timeout
    while time.time() < deadline:
        if path.exists():
            return True
        time.sleep(poll)
    return path.exists()


def summarize_entropy(seq: dict, escapes_by_capsule: "dict[str, list]") -> dict:
    """Unit 4 hook: report (technique, placement) cell coverage for a sequence.

    escape records must carry ``technique`` and ``placement``. Returns the
    distinct cell count and total escape count for the sequence.
    """
    cells = set()
    total = 0
    for cid, esc in escapes_by_capsule.items():
        for e in esc:
            if isinstance(e, dict) and e.get("technique") and e.get("placement"):
                cells.add((e["technique"], e["placement"]))
                total += 1
    return {
        "distinct_cells": len(cells),
        "total_escapes": total,
        "sequence_id": seq.get("sequence_id"),
    }


if __name__ == "__main__":
    from harness_config import load_config

    cfg = load_config()
    seqs = load_sequence(cfg)
    if not seqs:
        print("no sequence.yaml in profile dir; nothing to schedule")
        sys.exit(0)
    for seq in seqs:
        print(
            seq.get("sequence_id"), "-> order:", [c["id"] for c in resolve_order(seq)]
        )
