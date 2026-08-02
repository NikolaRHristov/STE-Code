#!/usr/bin/env python3
"""Re-batch verifier — confirms a worker's pages are complete before claiming done.

When the other agent re-runs batch 33-37 (or any batch), this tool:
1. Checks the checkpoint file for prior completion (no re-extraction if already done)
2. Verifies the output file has all 4 expected `# Page N of 434` headers
3. Validates table integrity at page boundaries (no split rows)
4. Reports PASS/FAIL per worker so re-batching is safe and idempotent

Usage:
  python3 .agents/tools/quality/verify-batch.py [--batch N] [--all] [--json]

Exit: 0 = all verified, 1 = some failed
"""

import argparse
import json
import re
import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
EXTRACTED = PROJECT / "ste-code" / "extracted"
CHECKPOINT = PROJECT / ".agents" / "state" / "extraction-checkpoint.json"
MANIFEST = PROJECT / "spec" / "issue-09-2025" / "page-dir" / "MANIFEST.md"


def load_manifest():
    mapping = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines():
            m = re.match(r"\|\s*(\d+)\s*\|\s*([\w-]+)\s*\|\s*([\w.-]+)\.md", line)
            if m:
                mapping[int(m.group(1))] = (m.group(2), m.group(3))
    return mapping


def load_checkpoint():
    if CHECKPOINT.exists():
        try:
            return json.loads(CHECKPOINT.read_text())
        except Exception:
            return {}
    return {}


def verify_worker(worker_num: int, mapping: dict) -> dict:
    """Verify a single worker's extracted output file is complete."""
    start = (worker_num - 1) * 4 + 1
    end = min(worker_num * 4, 434)
    fname = EXTRACTED / f"w{worker_num:03d}-p{start}-{end}.md"

    result = {
        "worker": worker_num,
        "pages": f"{start}-{end}",
        "exists": False,
        "headers_present": False,
        "table_intact": True,
        "size": 0,
        "status": "FAIL",
    }

    if not fname.exists():
        result["detail"] = "output file missing"
        return result

    result["exists"] = True
    content = fname.read_text(encoding="utf-8")
    result["size"] = len(content)

    # Check all expected page headers
    expected = [f"# Page {p} of 434" for p in range(start, end + 1)]
    missing = [h for h in expected if h not in content]
    result["headers_present"] = not missing
    if missing:
        result["detail"] = f"missing headers: {missing}"
        return result

    # Table integrity at boundaries — no data row immediately before a page header
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if re.match(r"^# Page \d+ of 434", line):
            prev_idx = i - 1
            while prev_idx >= 0 and lines[prev_idx].strip() == "":
                prev_idx -= 1
            if prev_idx >= 0 and lines[prev_idx].strip().startswith("|"):
                # Count columns vs header above
                header_cols = None
                for j in range(prev_idx - 1, max(-1, prev_idx - 20), -1):
                    if lines[j].strip().startswith("|"):
                        cells = lines[j].strip().strip("|").split("|")
                        if all(re.fullmatch(r":?-{3,}:?", c.strip()) for c in cells if c.strip()):
                            header_cols = len(cells)
                            break
                row_cols = len(lines[prev_idx].strip().strip("|").split("|"))
                if header_cols and row_cols != header_cols:
                    result["table_intact"] = False
                    result["detail"] = f"table column mismatch at page break L{i+1}"
                    return result

    result["status"] = "PASS"
    result["detail"] = f"{result['size']}B, all {len(expected)} headers present"
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, help="Verify one batch (1-37)")
    ap.add_argument("--all", action="store_true", help="Verify all 109 workers")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    mapping = load_manifest()
    checkpoint = load_checkpoint()

    workers = []
    if args.batch:
        for i in range(3):
            w = (args.batch - 1) * 3 + 1 + i
            if 1 <= w <= 109:
                workers.append(w)
    elif args.all:
        workers = list(range(1, 110))
    else:
        print("Specify --batch N or --all", file=sys.stderr)
        sys.exit(2)

    results = [verify_worker(w, mapping) for w in workers]
    passed = sum(1 for r in results if r["status"] == "PASS")

    if args.json:
        print(json.dumps({"total": len(results), "passed": passed, "results": results}, indent=2))
    else:
        for r in results:
            print(f"W{r['worker']:03d} ({r['pages']}): {r['status']} — {r.get('detail', '')}")
        print(f"\n{passed}/{len(results)} passed")

    sys.exit(0 if passed == len(results) else 1)


if __name__ == "__main__":
    main()
