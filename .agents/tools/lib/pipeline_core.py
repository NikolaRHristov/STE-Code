#!/usr/bin/env python3
"""pipeline_core.py — Shared enforcement library for ALL STE-Code pipeline tools.

Every skill+script pair imports from this module. It is the single source of
truth for:
  - STRICT_RULES (injected into every worker prompt)
  - Session isolation constants
  - Table-integrity checks (R2)
  - File-lock wrapper (R4 collision prevention)
  - Verify/re-batch idempotence (R5)
  - Context-window safety (R6)

Design principle (SESSION ISOLATION):
  One session = one operation = one read + one write.
  No script in this repo reads its own output back and edits it.
  Re-runs are idempotent: if output exists and is valid, SKIP.

All scripts MUST import from here rather than re-implementing checks.
This file is backed up in git; do not duplicate its logic elsewhere.
"""

from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Project root auto-detection (matches all tool scripts)
# ---------------------------------------------------------------------------
PROJECT = Path(__file__).resolve().parent.parent.parent.parent
CHECKPOINT = PROJECT / ".agents" / "state" / "extraction-checkpoint.json"
LOCKDIR = PROJECT / ".agents" / "state" / "locks"
LOCKDIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# STRICT RULES — injected into every worker prompt
# ---------------------------------------------------------------------------
STRICT_RULES = """STRICT EXTRACTION RULES — VIOLATION = HARD FAIL:
R1: Output MUST be verbatim from source pages. No summary, no cleanup, no reformat.
R2: Table rows are atomic. Never split/merge/reorder. Use <!-- TABLE CONTINUES ON NEXT PAGE --> at spans.
R3: NO freelance content — no commentary, examples, headers, footers, or notes. Only # Page N + **Page X** + verbatim body.
R4: Write exactly ONE file. Never touch another worker's file. Shared appends use lock-group.sh only.
R5: Re-runs are idempotent. If output exists and is valid, SKIP. No "improvements".
R6: If context is too small for 4 pages, request 2 pages. NEVER truncate. Never write partial output."""

# ---------------------------------------------------------------------------
# Session isolation: one job per session
# ---------------------------------------------------------------------------
ISOLATION_NOTE = """SESSION ISOLATION: This is ONE operation in its own session.
Read input, write output, exit. Do NOT re-read your output. Do NOT edit it.
Another session will handle the next stage."""

# ---------------------------------------------------------------------------
# R2: Table integrity helpers
# ---------------------------------------------------------------------------
def count_table_columns(row: str) -> int:
    """Count columns in a markdown table row (excluding leading/trailing pipes)."""
    if not row.strip().startswith("|"):
        return 0
    return len([c for c in row.strip().strip("|").split("|")])


def is_separator_row(row: str) -> bool:
    """Detect a markdown table separator row like |---|---|---|."""
    if not row.strip().startswith("|"):
        return False
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", c) for c in cells if c != "")


def find_table_breaks(content: str) -> List[Dict]:
    """Scan content for table rows split across page boundaries (R2 violation)."""
    issues = []
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"^# Page \d+ of 434", line):
            prev_idx = i - 1
            while prev_idx >= 0 and lines[prev_idx].strip() == "":
                prev_idx -= 1
            if prev_idx < 0:
                continue
            prev = lines[prev_idx]
            if prev.strip().startswith("|") and not is_separator_row(prev):
                header_cols = None
                for j in range(prev_idx - 1, max(-1, prev_idx - 20), -1):
                    if lines[j].strip().startswith("|"):
                        if is_separator_row(lines[j]):
                            header_cols = count_table_columns(lines[j])
                            break
                row_cols = count_table_columns(prev)
                if header_cols and row_cols != header_cols:
                    issues.append({
                        "type": "column_mismatch_at_page_boundary",
                        "line": i + 1,
                        "expected": header_cols,
                        "found": row_cols,
                    })
    return issues


# ---------------------------------------------------------------------------
# R3: Freelance-content detection
# ---------------------------------------------------------------------------
FREELANCE_PATTERNS = [
    r"^Here is the extraction",
    r"^I have extracted",
    r"^This page describes",
    r"^Below is",
    r"^Note:",
    r"^Summary:",
    r"^The following content",
    r"shutting down",
    r"Let me (check|verify|confirm)",
]


def detect_freelance(content: str) -> List[str]:
    """Return list of freelance-phrase violations in first 5 lines."""
    violations = []
    for i, line in enumerate(content.split("\n")[:5]):
        for pat in FREELANCE_PATTERNS:
            if re.match(pat, line.strip(), re.I):
                violations.append(f"L{i+1}: {line[:60]!r}")
    return violations


# ---------------------------------------------------------------------------
# R5: Idempotence / checkpoint helpers
# ---------------------------------------------------------------------------
def load_checkpoint() -> Dict:
    if CHECKPOINT.exists():
        try:
            return json.loads(CHECKPOINT.read_text())
        except Exception:
            return {}
    return {}


def is_worker_done(worker_num: int) -> bool:
    """R5: check if worker already passed (idempotent skip)."""
    cp = load_checkpoint()
    entry = cp.get(str(worker_num))
    return bool(entry and entry.get("passed"))


def save_checkpoint(worker_num: int, output_size: int, attempt: int = 1) -> None:
    """Atomically record a passed worker."""
    cp = load_checkpoint()
    cp[str(worker_num)] = {"passed": True, "attempt": attempt, "output_size": output_size}
    tmp = CHECKPOINT.with_suffix(".tmp")
    tmp.write_text(json.dumps(cp, indent=2, default=str))
    tmp.replace(CHECKPOINT)


# ---------------------------------------------------------------------------
# R4: File-lock wrapper (collision prevention for group/adapt writes)
# ---------------------------------------------------------------------------
def acquire_lock(target_stem: str, agent_id: str = "unknown") -> bool:
    """Acquire advisory lock. Returns True on success, False if busy."""
    lock = LOCKDIR / f"{target_stem}.lock"
    try:
        lock.mkdir(exist_ok=False)
        (lock / "owner").write_text(f"{agent_id} {Path.cwd().name}\n")
        return True
    except FileExistsError:
        return False


def release_lock(target_stem: str, agent_id: str = "unknown") -> bool:
    lock = LOCKDIR / f"{target_stem}.lock"
    if lock.is_dir():
        try:
            owner = (lock / "owner").read_text()
            if agent_id in owner or agent_id == "force":
                import shutil
                shutil.rmtree(lock)
                return True
        except Exception:
            pass
    return False


def check_lock(target_stem: str) -> bool:
    """Returns True if FREE (no lock), False if locked."""
    return not (LOCKDIR / f"{target_stem}.lock").is_dir()


# ---------------------------------------------------------------------------
# R6: Context-window safety
# ---------------------------------------------------------------------------
def safe_page_range(worker_num: int, max_pages: int = 4) -> Tuple[int, int]:
    """Return (start, end) for a worker. If max_pages exceeds safe context,
    the caller should split into smaller chunks — never truncate."""
    start = (worker_num - 1) * max_pages + 1
    end = min(worker_num * max_pages, 434)
    return start, end


def would_truncate(content: str) -> bool:
    """R6: detect if content looks truncated (incomplete last row)."""
    lines = content.rstrip().split("\n")
    if not lines:
        return False
    last = lines[-1].strip()
    # Incomplete table row (starts with | but doesn't end with |)
    if last.startswith("|") and not last.endswith("|"):
        return True
    return False


# ---------------------------------------------------------------------------
# Unified verifier — used by verify-batch.py and strict-guard.py
# ---------------------------------------------------------------------------
def verify_extracted_file(filepath: Path, start: int, end: int) -> Dict:
    """R1-R6 check for one extracted worker file. Returns result dict."""
    result = {
        "file": str(filepath.relative_to(PROJECT)) if filepath.is_relative_to(PROJECT) else str(filepath),
        "exists": False,
        "headers_ok": False,
        "table_ok": True,
        "freelance": [],
        "status": "FAIL",
    }
    if not filepath.exists():
        result["detail"] = "missing"
        return result

    result["exists"] = True
    content = filepath.read_text(encoding="utf-8")

    expected = [f"# Page {p} of 434" for p in range(start, end + 1)]
    missing = [h for h in expected if h not in content]
    result["headers_ok"] = not missing
    if missing:
        result["detail"] = f"missing headers: {missing}"
        return result

    breaks = find_table_breaks(content)
    result["table_ok"] = not breaks
    if breaks:
        result["detail"] = f"table break at L{breaks[0]['line']}"
        return result

    result["freelance"] = detect_freelance(content)
    if result["freelance"]:
        result["detail"] = f"freelance: {result['freelance'][0]}"
        return result

    result["status"] = "PASS"
    result["detail"] = f"{len(content)}B, {len(expected)} headers present"
    return result


if __name__ == "__main__":
    # Self-test
    print(f"PROJECT={PROJECT}")
    print(f"STRICT_RULES lines: {len(STRICT_RULES.splitlines())}")
    print(f"Lock dir: {LOCKDIR}")
    print("OK")
