#!/usr/bin/env python3
"""Phase F — Final audit: counts, rails, consistency, level coverage, gap detection.

Usage:
  python3 .agents/tools/phase-f-run.py [--fix]
"""

import os, sys, json, subprocess
from pathlib import Path
from datetime import datetime, timezone

PROJECT = Path(__file__).resolve().parent.parent.parent
REPORT_FILE = PROJECT / ".agents" / "audit" / f"final-audit-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.md"

VENV_PYTHON = os.path.expanduser("~/.hermes/hermes-agent/venv/bin/python3")
WRAPPER = PROJECT / ".agents" / "tools" / "hermes-oneshot-wrapper.py"


def check(condition, name, detail=""):
    return {"name": name, "pass": condition, "detail": detail}


def run_checks():
    results = []

    # ── COUNTS ──
    adapted = sorted(PROJECT.glob("ste-code/adapted/a-sec*-rule*.md"))
    gr_rules = sorted(PROJECT.glob("ste-code/adapted/a-sec*-gr*.md"))
    artifacts = sorted(PROJECT.glob("ste-code/artifacts/*.txt"))
    templates = sorted(PROJECT.glob("ste-code/templates/*.md"))
    data_files = sorted(PROJECT.glob("ste-code/data/**/*.json"))
    vocabulary = sorted(PROJECT.glob("ste-code/data/vocabulary/*.json"))

    results.append(check(len(adapted) == 51, f"Rule files: {len(adapted)}/51"))
    results.append(check(len(gr_rules) == 4, f"GR rules: {len(gr_rules)}/4"))
    results.append(check(len(artifacts) >= 5, f"Artifact .txt files: {len(artifacts)}"))
    results.append(check(len(templates) >= 4, f"Template .md files: {len(templates)}"))
    results.append(check(len(data_files) >= 5, f"Data JSON files: {len(data_files)}"))
    results.append(check(len(vocabulary) >= 4, f"Vocabulary JSON files: {len(vocabulary)}"))

    # ── NO EMPTY FILES ──
    empty = []
    for d in ["ste-code/adapted", "ste-code/artifacts", "ste-code/templates", "ste-code/data"]:
        for f in (PROJECT / d).rglob("*"):
            if f.is_file() and f.stat().st_size == 0:
                empty.append(str(f.relative_to(PROJECT)))
    results.append(check(len(empty) == 0, "Zero-byte files", f"Found: {empty}" if empty else "None"))

    # ── RULE DEPTH ──
    thin_rules = [r.name for r in adapted if len(r.read_text().splitlines()) < 100]
    results.append(check(len(thin_rules) == 0, f"Rules <100 lines: {len(thin_rules)}", thin_rules[:5] if thin_rules else "All ≥100L"))

    avg_lines = sum(len(r.read_text().splitlines()) for r in adapted) // len(adapted) if adapted else 0
    results.append(check(avg_lines >= 200, f"Avg rule depth: {avg_lines}L (target ≥200)", ""))

    # ── LEVEL COVERAGE ──
    artifacts_dir = PROJECT / "ste-code" / "artifacts"
    artifacts_size = sum(f.stat().st_size for f in artifacts_dir.glob("*.txt")) if artifacts_dir.exists() else 0
    artifacts_tokens = artifacts_size // 4

    templates_dir = PROJECT / "ste-code" / "templates"
    templates_size = sum(f.stat().st_size for f in templates_dir.glob("*.md")) if templates_dir.exists() else 0

    rules_size = sum(r.stat().st_size for r in adapted) if adapted else 0
    dict_size = (PROJECT / "ste-code/adapted/a-dictionary.md").stat().st_size if (PROJECT / "ste-code/adapted/a-dictionary.md").exists() else 0

    levels = {
        -2: (50, artifacts_tokens >= 50),
        -1: (150, artifacts_tokens >= 150),
        0: (300, artifacts_tokens >= 300),
        1: (1200, artifacts_tokens >= 1200),
        2: (5000, artifacts_tokens + templates_size//4 >= 5000),
        3: (20000, artifacts_tokens + templates_size//4 >= 20000),
        4: (50000, dict_size//4 >= 50000),
        5: (100000, rules_size//4 >= 100000),
    }

    for level, (target, covered) in levels.items():
        status = "✓" if covered else "✗ GAP"
        results.append(check(covered, f"Level {level:+d} (~{target:,} tokens)", status))

    # ── BROKEN REFERENCES ──
    import re
    broken_refs = 0
    for f in PROJECT.rglob("*.md"):
        if ".git/" in str(f) or ".venv/" in str(f): continue
        content = f.read_text()
        for ref in re.findall(r"\]\(([^)]+)\)", content):
            if ref.startswith("http") or ref.startswith("#") or ref in ("...", "path"): continue
            target = (f.parent / ref).resolve()
            if ref.startswith('.agents/') or ref.startswith('ste-code/'):
                target = (Path('.') / ref).resolve()
            if not target.exists():
                broken_refs += 1
    results.append(check(broken_refs == 0, "Broken internal references", f"{broken_refs} broken" if broken_refs else "All valid"))

    # ── NON-STE/STE PAIR INTEGRITY ──
    pair_mismatch = 0
    for r in adapted:
        c = r.read_text()
        if c.count("**Non-STE:**") > c.count("**STE:**"):
            pair_mismatch += 1
    results.append(check(pair_mismatch == 0, "Non-STE/STE balance (Non-STE ≤ STE)", f"{pair_mismatch} mismatched" if pair_mismatch else "All balanced"))

    # ── GITIGNORE COVERAGE ──
    gitignore = (PROJECT / ".gitignore").read_text() if (PROJECT / ".gitignore").exists() else ""
    results.append(check(".agents/tmp/" in gitignore or ".agents/tmp/*.txt" in gitignore, "tmp/ in gitignore", ""))
    results.append(check(".agents/telemetry/" in gitignore, "telemetry/ in gitignore", ""))
    results.append(check(".agents/audit/" in gitignore, "audit/ in gitignore", ""))

    return results


def generate_level_artifacts():
    """Generate missing Level -2, -1, 0 artifacts if needed."""
    missing = []
    for level in [-2, -1, 0]:
        target = PROJECT / "ste-code" / "templates" / f"ste-code-level{level:+d}.md"
        if not target.exists():
            missing.append(level)

    if not missing:
        print("All level artifacts present.")
        return

    print(f"Generating {len(missing)} missing level artifacts: {missing}")
    prompt = f"""You are STE-Code. Generate compact system prompt templates for adaptation levels {missing}.

Read the distilled system prompt at ste-code/artifacts/ste-code-distilled-system-prompt.txt for reference.

For each level, generate a markdown file with YAML frontmatter (id, version, tokens, use-when, source):

Level -2 (~50 tokens): Absolute minimum — 1 sentence: "Write documentation that is clear, consistent, and unambiguous. Use approved words from the STE-Code standard."

Level -1 (~150 tokens): 14 principles as a compact numbered list, no examples.

Level 0 (~300 tokens): 14 principles + top 10 synonym pairs, no dictionary.

PRESERVE the ASD-STE100 source attribution in the frontmatter.

Use write_file for each output:
- ste-code/templates/ste-code-level--2.md
- ste-code/templates/ste-code-level--1.md
- ste-code/templates/ste-code-level-0.md

Report line counts and token estimates.
"""

    tmp = PROJECT / ".agents" / "tmp" / "phase-f-levels.txt"
    tmp.write_text(prompt)

    result = subprocess.run(
        [VENV_PYTHON, str(WRAPPER), str(tmp), "--model", "deepseek-v4-pro"],
        cwd=str(PROJECT), capture_output=True, text=True, timeout=300,
        env={**os.environ, "HERMES_REASONING_EFFORT": "medium"},
    )
    print(f"Level generation: exit={result.returncode}")
    if result.stdout:
        print(result.stdout[-300:])


def main():
    fix = "--fix" in sys.argv

    print("=" * 60)
    print("  STE-CODE PHASE F — FINAL AUDIT")
    print("=" * 60)
    print()

    results = run_checks()

    passed = sum(1 for r in results if r["pass"])
    failed = sum(1 for r in results if not r["pass"])

    for r in results:
        icon = "✓" if r["pass"] else "✗"
        print(f"  {icon} {r['name']}")
        if r["detail"] and not r["pass"]:
            print(f"     {r['detail']}")

    print(f"\n  Result: {passed}/{len(results)} checks passed ({failed} failed)")

    # Generate report
    report = f"""# Phase F — Final Audit Report

**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}

## Summary

| Metric | Value |
|--------|-------|
| Checks passed | {passed}/{len(results)} |
| Checks failed | {failed} |

## Results

"""
    for r in results:
        icon = "✓" if r["pass"] else "✗"
        report += f"- {icon} **{r['name']}**"
        if r["detail"]:
            report += f" — {r['detail']}"
        report += "\n"

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report)
    print(f"\n  Report: {REPORT_FILE.relative_to(PROJECT)}")

    if fix and failed > 0:
        print("\n  Running fixes...")
        generate_level_artifacts()

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
