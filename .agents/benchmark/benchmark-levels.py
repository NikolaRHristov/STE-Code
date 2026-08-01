#!/usr/bin/env python3
"""Multi-Level Benchmark — run all 59 tests against each of 5 level prompts.

Launches 5 parallel benchmark orchestrators (one per level). Each orchestrator
runs all 59 test cases against its assigned system prompt. Results are compared
across levels to measure how compliance scales with prompt size.

Usage:
  python3 .agents/benchmark/benchmark-levels.py [--levels 1,2,3,4,5] [--model poolside/laguna-s-2.1:free]
                                                [--timeout 600] [--max-workers 10]
"""

import os, sys, subprocess, time, json
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
ORCHESTRATOR = PROJECT / ".agents" / "benchmark" / "orchestrator.py"
ARTIFACTS = PROJECT / "ste-code" / "artifacts"
RESULTS_BASE = PROJECT / ".agents" / "benchmark" / "results-levels"

# STE-Code now ships 8 deterministic tiers (artifacts/<tier>/system-prompt.txt),
# produced by finalize_artifacts.py. Every tier has a single concatenated
# system-prompt.txt, so the benchmark can feed any tier directly.
LEVEL_PROMPTS = {
    -2: ARTIFACTS / "level-2" / "system-prompt.txt",
    -1: ARTIFACTS / "level-1" / "system-prompt.txt",
    0:  ARTIFACTS / "level0"  / "system-prompt.txt",
    1:  ARTIFACTS / "level1"  / "system-prompt.txt",
    2:  ARTIFACTS / "level2"  / "system-prompt.txt",
    3:  ARTIFACTS / "level3"  / "system-prompt.txt",
    4:  ARTIFACTS / "level4"  / "system-prompt.txt",
    5:  ARTIFACTS / "level5"  / "system-prompt.txt",
}


def run_level(level, prompt_file, model, timeout, max_workers, results_dir):
    """Run the orchestrator for one level. Returns (level, success, results_path)."""
    level_dir = results_dir / f"level-{level}"
    level_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, str(ORCHESTRATOR),
        "--model", model,
        "--timeout", str(timeout),
        "--max-workers", str(max_workers),
        "--system-prompt-file", str(prompt_file),
        "--results-dir", str(level_dir),
    ]

    print(f"[Level {level}] Launching: {' '.join(cmd[-6:])}")
    start = time.time()

    try:
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT),
            capture_output=True,
            text=True,
            timeout=timeout + 120,  # Extra time beyond worker timeout
        )
        elapsed = time.time() - start
        success = result.returncode == 0
        status = "OK" if success else f"FAIL ({result.returncode})"
        print(f"[Level {level}] {status} in {elapsed:.0f}s")

        # Save raw output
        (level_dir / "stdout.txt").write_text(result.stdout or "")
        (level_dir / "stderr.txt").write_text(result.stderr or "")

        return level, success, level_dir

    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        print(f"[Level {level}] TIMEOUT after {elapsed:.0f}s")
        return level, False, level_dir


def collect_results(results_dirs, output_path):
    """Parse orchestrator results from each level and produce comparison."""
    report = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "levels": {},
    }

    for level, success, results_dir in results_dirs:
        level_data = {"success": success, "dir": str(results_dir)}

        # Try to find the orchestrator's summary/report file
        for pattern in ["**/report.json", "**/summary.json", "**/results.json"]:
            matches = list(results_dir.glob(pattern))
            if matches:
                try:
                    with open(matches[0]) as f:
                        level_data["results"] = json.load(f)
                except (json.JSONDecodeError, IOError):
                    level_data["results"] = {"error": "Could not parse results file"}
                break

        # Fallback: scan for individual worker outputs
        if "results" not in level_data:
            output_files = list(results_dir.glob("**/output-*.txt"))
            level_data["worker_outputs"] = len(output_files)
            level_data["results"] = {"workers_found": len(output_files)}

        report["levels"][str(level)] = level_data

    # Print comparison table
    print("\n" + "=" * 70)
    print("  MULTI-LEVEL BENCHMARK RESULTS")
    print("=" * 70)
    print(f"  {'Level':<8} {'Status':<8} {'Workers':<10} Details")
    print("  " + "-" * 66)

    for level in sorted(report["levels"].keys(), key=int):
        data = report["levels"][level]
        status = "OK" if data["success"] else "FAIL"
        workers = data.get("results", {}).get("workers_found", "?")
        tokens = LEVEL_PROMPTS.get(int(level))
        if tokens and tokens.exists():
            size = tokens.stat().st_size // 4  # ~tokens
            extra = f"~{size:,} tokens"
        else:
            extra = "~100K tokens (51 summaries)"
        print(f"  Level {level:<3}  {status:<8} {str(workers):<10} {extra}")

    print("=" * 70)

    # Write JSON report
    output_path.write_text(json.dumps(report, indent=2))
    print(f"\nFull report: {output_path}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Level STE-Code Benchmark")
    parser.add_argument("--levels", default="-2,-1,0,1,2,3,4,5",
                        help="Comma-separated tiers (default: all 8 tiers)")
    parser.add_argument("--model", default="poolside/laguna-s-2.1:free", help="Model to use")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per orchestrator (seconds)")
    parser.add_argument("--max-workers", type=int, default=0, help="Max concurrent workers (0=unlimited)")
    parser.add_argument("--dry-run", action="store_true", help="Print config without running")
    parser.add_argument("--results-dir", default=None, help="Custom results directory")
    args = parser.parse_args()

    levels = [int(x.strip()) for x in args.levels.split(",")]
    results_base = Path(args.results_dir) if args.results_dir else RESULTS_BASE
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    results_dir = results_base / timestamp

    print(f"Model: {args.model}")
    print(f"Levels: {levels}")
    print(f"Max workers per level: {args.max_workers or 'unlimited'}")
    print(f"Results: {results_dir}")
    print()

    if args.dry_run:
        for lv in levels:
            prompt = LEVEL_PROMPTS.get(lv)
            if prompt and prompt.exists():
                print(f"  Level {lv}: {prompt} ({prompt.stat().st_size//4:,} ~tokens)")
            else:
                print(f"  Level {lv}: PROMPT NOT FOUND")
        return

    results_dir.mkdir(parents=True, exist_ok=True)

    # Launch all levels in parallel
    processes = []
    for lv in levels:
        prompt = LEVEL_PROMPTS.get(lv)
        if not prompt or not prompt.exists():
            print(f"SKIP Level {lv}: prompt file not found")
            continue

        proc = subprocess.Popen(
            [sys.executable, str(ORCHESTRATOR),
             "--model", args.model,
             "--timeout", str(args.timeout),
             "--max-workers", str(args.max_workers),
             "--system-prompt-file", str(prompt),
             "--results-dir", str(results_dir / f"level-{lv}")],
            cwd=str(PROJECT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        processes.append((lv, proc))
        print(f"[Level {lv}] Launched (PID {proc.pid})")

    # Wait for all
    print(f"\nWaiting for {len(processes)} level orchestrators...\n")
    results = []
    for lv, proc in processes:
        try:
            stdout, stderr = proc.communicate(timeout=args.timeout + 120)
            success = proc.returncode == 0
            level_dir = results_dir / f"level-{lv}"
            (level_dir / "stdout.txt").write_text(stdout or "")
            (level_dir / "stderr.txt").write_text(stderr or "")
            status = "OK" if success else f"FAIL ({proc.returncode})"
            print(f"[Level {lv}] {status}")
            results.append((lv, success, level_dir))
        except subprocess.TimeoutExpired:
            proc.kill()
            print(f"[Level {lv}] TIMEOUT")
            results.append((lv, False, results_dir / f"level-{lv}"))

    # Collect and compare
    collect_results(results, results_dir / "comparison.json")


if __name__ == "__main__":
    main()
