#!/usr/bin/env python3
"""Unified 4-mode STE-Code Benchmark.

Modes:
  1. original  — Plain LLM, no system prompt (baseline)
  2. sloppy    — Intentionally bad docs (worst case)
  3. ste-code  — Full Level 5 STE-Code standard (best case)
  4. ste-baseline — Original ASD-STE100 applied to code docs (reference)

Usage:
  python3 .agents/benchmark/run.py [--mode MODE] [--dry-run]
  python3 .agents/benchmark/run.py --compare  (run all 4 and compare)
"""

import os, sys, json, time, re
from pathlib import Path
from datetime import datetime, timezone

from benchmark_lib import PRINCIPLE_KEYWORDS, calc_correctness

PROJECT = Path(__file__).resolve().parent.parent.parent
BENCHMARK_DIR = Path(__file__).resolve().parent
TEST_DIR = BENCHMARK_DIR / "test-cases"
RESULTS_DIR = BENCHMARK_DIR / "results-v2"
MODEL = "deepseek-v4-pro"

# ── System prompts for each mode ──

PROMPT_ORIGINAL = """You are a helpful coding assistant. Respond to the user's request.

IMPORTANT: Do NOT create or modify any files. Output your response as text only."""

PROMPT_SLOPPY = """You are a lazy developer who writes quick, informal documentation.
Use slang, jargon, contractions, and skip articles. Be as sloppy as possible.
Never use full sentences. Omit subjects. Use passive voice everywhere.
This is internal code — no one will read it carefully.

IMPORTANT: Do NOT create or modify any files. Output your response as text only."""

PROMPT_STE_CODE = None  # Load from Level 5 artifacts

PROMPT_STE_CODE_SLIM = """You are STE-Code, Simplified Technical English for Code documentation.
Apply STE-Code rules to correct this text.

If you need to check a specific rule, read the file at:
  ste-code/adapted/a-secN-ruleX.Y.md

Available rules are in ste-code/adapted/ (51 deepened rule files).
Consult them freely. Use read_file to verify any uncertain rule application.

After correcting, output the result and a brief compliance summary.

IMPORTANT: Do NOT create or modify any files. Output text only."""

PROMPT_STE_BASELINE = """You are an ASD-STE100 Simplified Technical English checker.
Apply the original ASD-STE100 Issue 9 (January 2025) aerospace standard to this text.
Use approved words from the STE dictionary. Use active voice. Use imperative mood.
Do not use slang, jargon, or contractions. Write short, clear sentences.
Technical code nouns (keywords, frameworks, tools) are allowed.
The ASD-STE100 standard was developed by the AeroSpace and Defence Industries
Association of Europe (ASD), Brussels, Belgium. © ASD, 2025.

IMPORTANT: Do NOT create or modify any files. Output text only."""


def load_ste_code_level5():
    """Load a substantive Level 5 prompt from deepened rules."""
    rules_dir = PROJECT / "ste-code" / "adapted"
    rules = sorted(rules_dir.glob("a-sec*-rule*.md"))
    
    prompt = """You are STE-Code, Simplified Technical English for Code documentation.
Apply the FULL STE-Code Level 5 standard. Follow ALL 53 rules below.

"""
    for r in rules:
        lines = r.read_text().split("\n")
        title = lines[0].strip("# ").strip() if lines else r.stem
        prompt += f"## {title}\n"
        for line in lines[1:]:
            s = line.strip()
            if s and not s.startswith(">") and not s.startswith("##") and len(s) > 30:
                prompt += f"{s}\n\n"
                break
    
    synonym_file = PROJECT / "ste-code" / "data" / "synonym-table.json"
    if synonym_file.exists():
        data = json.loads(synonym_file.read_text())
        prompt += "\n## Synonym Table (Code Domain)\n"
        for pair in data.get("pairs", [])[:30]:
            avoid = ", ".join(pair["avoid"][:3])
            prompt += f"- {pair['approved']} -> NOT: {avoid}\n"
    
    prompt += """
## Output Rules
- Active voice, imperative mood for instructions
- Max 20 words per procedural sentence, 25 for descriptive
- One instruction per step. No nested clauses deeper than 2 levels.
- No semicolons. No contractions (don't -> do not). Include all articles.
- BREAKING: before destructive changes. DEPRECATED: before removed features.
- Apply all principles P1-P14.

IMPORTANT: Do NOT create or modify any files. Output text only.
"""
    return prompt


def generate_sloppy_tests():
    return [
        {
            "id": "sloppy-001", "category": "sloppy-docs",
            "description": "README with maximum sloppiness",
            "input": "this thing basically does a bunch of stuff u just gotta run npm install n itll work lol make sure u got node tho or it wont start. the config is like whatever just put ur keys in .env n ur good. if it breaks just restart it idk",
            "expected_principles": ["P1", "P4", "P10", "P14"],
            "forbidden_keywords": ["basically", "stuff", "gotta", "lol", "tho", "wont", "idk", "whatever", "ur"],
            "expected_keywords": ["install", "run", "configure", "restart"],
            "difficulty": "hard",
        },
        {
            "id": "sloppy-002", "category": "sloppy-docs",
            "description": "API doc with slang and contractions",
            "input": "POST /api/users — creates a user or whatever. body's gotta have email n password. if it doesn't work u'll get a 400. the token thingy goes in the header. don't forget to set Content-Type or it'll be mad.",
            "expected_principles": ["P1", "P4", "P10", "P14"],
            "forbidden_keywords": ["whatever", "gotta", "doesn't", "don't", "it'll", "thingy", "mad"],
            "expected_keywords": ["endpoint", "request body", "Authorization", "Content-Type"],
            "difficulty": "medium",
        },
        {
            "id": "sloppy-003", "category": "sloppy-docs",
            "description": "Commit message with no structure",
            "input": "fix stuff\n\ni changed some things and now it works better i think. also fixed that one bug that was annoying. idk what caused it but its fixed now lol.",
            "expected_principles": ["P4", "P10", "P11"],
            "forbidden_keywords": ["stuff", "things", "idk", "lol", "annoying", "i think"],
            "expected_keywords": ["fix", "change", "bug"],
            "difficulty": "easy",
        },
        {
            "id": "sloppy-004", "category": "sloppy-docs",
            "description": "Error message with no subject",
            "input": "error: failed. something went wrong. try again maybe.",
            "expected_principles": ["P4", "P10"],
            "forbidden_keywords": ["something", "maybe", "went wrong"],
            "expected_keywords": ["error", "failed", "try"],
            "difficulty": "easy",
        },
        {
            "id": "sloppy-005", "category": "sloppy-docs",
            "description": "Code comment with everything wrong",
            "input": "// this function does the thing with the stuff. its kinda slow but whatever. dont use it for big data lol. hopefully we'll fix it someday",
            "expected_principles": ["P1", "P4", "P10", "P14"],
            "forbidden_keywords": ["thing", "stuff", "kinda", "whatever", "dont", "lol", "hopefully", "someday"],
            "expected_keywords": ["function", "process", "data"],
            "difficulty": "medium",
        },
    ]


def generate_ste_baseline_tests():
    return [
        {
            "id": "ste-base-001", "category": "ste-baseline",
            "description": "Code docstring — does ASD-STE100 handle 'deploy' as a verb?",
            "input": "Deploy the application to the production environment. The deploy will take approximately 5 minutes.",
            "expected_principles": ["P12", "P13"],
            "forbidden_keywords": ["the deploy"],
            "expected_keywords": ["deploy", "deployment", "production"],
            "difficulty": "medium",
        },
        {
            "id": "ste-base-002", "category": "ste-baseline",
            "description": "API reference — can ASD-STE100 handle 'endpoint' as technical noun?",
            "input": "The endpoint returns a JSON object. Utilize the GET method to retrieve the data. Make sure you pass a valid token.",
            "expected_principles": ["P1", "P5"],
            "forbidden_keywords": ["utilize", "make sure"],
            "expected_keywords": ["endpoint", "GET", "token", "use"],
            "difficulty": "easy",
        },
        {
            "id": "ste-base-003", "category": "ste-baseline",
            "description": "Docker command — technical verb as noun",
            "input": "Do a build of the Docker image, then do a push to the registry. The deploy will start automatically.",
            "expected_principles": ["P12", "P13"],
            "forbidden_keywords": ["do a build", "do a push", "the deploy"],
            "expected_keywords": ["build", "push", "deployment", "Docker"],
            "difficulty": "medium",
        },
        {
            "id": "ste-base-004", "category": "ste-baseline",
            "description": "Framework-specific terms — next.js, useEffect",
            "input": "Initialize the Next.js application. The useEffect hook runs after render. Make sure you import React first.",
            "expected_principles": ["P5", "P6", "P8"],
            "forbidden_keywords": ["make sure"],
            "expected_keywords": ["Next.js", "useEffect", "React", "start"],
            "difficulty": "easy",
        },
        {
            "id": "ste-base-005", "category": "ste-baseline",
            "description": "Mixed aerospace + code terms — does STE handle both?",
            "input": "The aircraft engine maintenance procedure requires you to check the oil level. The database engine requires you to check the connection pool.",
            "expected_principles": ["P1", "P3", "P5"],
            "forbidden_keywords": ["requires you to"],
            "expected_keywords": ["engine", "check", "oil", "database", "connection"],
            "difficulty": "hard",
        },
    ]


def load_existing_tests():
    tests = []
    for cat_file in sorted(TEST_DIR.glob("category-*.json")):
        with open(cat_file) as f:
            cat_tests = json.load(f)
        for t in cat_tests:
            t["_file"] = cat_file.name
            tests.append(t)
    return tests


def run_worker(test_case, system_prompt, mode_name, run_dir):
    is_sloppy = "sloppy" in test_case.get("category", "")
    
    if is_sloppy:
        full_prompt = f"""{system_prompt}

Write documentation for this scenario (be as sloppy as instructed):
{test_case['input']}

Output ONLY the documentation text. No explanations."""
    else:
        task_input = test_case.get("prompt", test_case.get("input", ""))
        full_prompt = f"""{system_prompt}

## TASK
Check this text for compliance and correct it:
{task_input}

Output the corrected text, then a compliance summary."""
    
    prompt_file = run_dir / f"{test_case['id']}-prompt.txt"
    prompt_file.write_text(full_prompt)
    
    out_file = run_dir / f"{test_case['id']}-output.txt"
    
    pid = os.fork()
    if pid == 0:
        os.chdir(str(run_dir))
        with open(out_file, "w") as outf:
            os.dup2(outf.fileno(), 1)
            os.dup2(outf.fileno(), 2)
        os.execvp("hermes", ["hermes", "-z", full_prompt, "-m", MODEL, "--yolo"])
        os._exit(1)
    
    return pid


def calc_score(test_case, output):
    """Calculate correctness score 0-1 using benchmark_lib as the canonical source."""
    output_lower = output.lower()
    
    satisfied = []
    for p in test_case.get("expected_principles", []):
        if p in PRINCIPLE_KEYWORDS:
            found = any(kw.lower() in output_lower for kw in PRINCIPLE_KEYWORDS[p])
            if found or re.search(r'\b' + re.escape(p) + r'\b', output):
                satisfied.append(p)
    
    forbidden = test_case.get("forbidden_keywords", [])
    forbidden_found = [kw for kw in forbidden if kw.lower() in output_lower]
    
    expected = test_case.get("expected_keywords", [])
    expected_found = [kw for kw in expected if kw.lower() in output_lower]
    
    return calc_correctness(
        test_case.get("expected_principles", []),
        satisfied,
        forbidden_found,
        len(forbidden),
        expected_found,
        len(expected),
    )


def run_mode(mode_name, system_prompt, test_cases, dry_run=False):
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_dir = RESULTS_DIR / f"{mode_name}-{timestamp}"
    os.makedirs(run_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"  MODE: {mode_name} — {len(test_cases)} tests")
    print(f"{'='*60}")
    
    if dry_run:
        for tc in test_cases[:3]:
            print(f"  [{mode_name}] {tc['id']}: {tc['description']}")
        return None
    
    workers = {}
    for tc in test_cases:
        pid = run_worker(tc, system_prompt, mode_name, run_dir)
        workers[tc["id"]] = {"pid": pid, "start": time.time(), "tc": tc}
    
    print(f"  Launched {len(workers)} workers. Waiting...")
    
    MAX_WAIT = 600
    elapsed = 0
    pending = set(workers.keys())
    while pending and elapsed < MAX_WAIT:
        time.sleep(5)
        elapsed += 5
        for tid in list(pending):
            try:
                wpid, status = os.waitpid(workers[tid]["pid"], os.WNOHANG)
                if wpid != 0:
                    pending.discard(tid)
            except OSError:
                pending.discard(tid)
        if elapsed % 30 == 0 and pending:
            print(f"    ... {len(pending)} remaining ({elapsed}s)")
    
    results = []
    for tid, wdata in workers.items():
        tc = wdata["tc"]
        out_file = run_dir / f"{tid}-output.txt"
        try:
            output = out_file.read_text()
        except OSError as e:
            output = f"OUTPUT_MISSING: {e}"
        
        score = calc_score(tc, output)
        passed = score >= 0.7
        
        results.append({
            "id": tid,
            "category": tc.get("category", "unknown"),
            "score": score,
            "passed": passed,
            "latency_ms": int((time.time() - wdata["start"]) * 1000),
        })
    
    passed = sum(1 for r in results if r["passed"])
    scores = [r["score"] for r in results]
    avg_score = sum(scores) / len(scores) if scores else 0
    
    print(f"\n  {mode_name}: {passed}/{len(results)} passed ({passed/len(results)*100:.1f}%)")
    print(f"  Avg score: {avg_score:.3f}")
    
    aggregate = {
        "mode": mode_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results) * 100, 1),
        "avg_score": round(avg_score, 3),
        "results": results,
    }
    agg_file = run_dir / "aggregate.json"
    agg_file.write_text(json.dumps(aggregate, indent=2))
    
    return aggregate


def main():
    dry_run = "--dry-run" in sys.argv
    compare = "--compare" in sys.argv
    mode_filter = None
    for i, arg in enumerate(sys.argv):
        if arg == "--mode" and i + 1 < len(sys.argv):
            mode_filter = sys.argv[i + 1]
    
    global PROMPT_STE_CODE
    PROMPT_STE_CODE = load_ste_code_level5()
    print(f"Level 5 prompt: {len(PROMPT_STE_CODE)} chars")
    
    existing = load_existing_tests()
    sloppy = generate_sloppy_tests()
    ste_base = generate_ste_baseline_tests()
    
    modes = []
    if compare or not mode_filter:
        modes = [
            ("original", PROMPT_ORIGINAL, existing),
            ("sloppy", PROMPT_SLOPPY, sloppy),
            ("ste-code", PROMPT_STE_CODE, existing + sloppy + ste_base),
            ("ste-baseline", PROMPT_STE_BASELINE, ste_base + existing[:10]),
        ]
    elif mode_filter == "original":
        modes = [("original", PROMPT_ORIGINAL, existing)]
    elif mode_filter == "sloppy":
        modes = [("sloppy", PROMPT_SLOPPY, sloppy)]
    elif mode_filter == "ste-code":
        modes = [("ste-code", PROMPT_STE_CODE, existing + sloppy + ste_base)]
    elif mode_filter == "ste-baseline":
        modes = [("ste-baseline", PROMPT_STE_BASELINE, ste_base + existing[:10])]
    
    results = {}
    for mode_name, prompt, tests in modes:
        r = run_mode(mode_name, prompt, tests, dry_run)
        if r:
            results[mode_name] = r
    
    if len(results) >= 2:
        print(f"\n{'='*60}")
        print(f"  COMPARISON")
        print(f"{'='*60}")
        print(f"  {'Mode':<15} {'Tests':>6} {'Passed':>7} {'Rate':>7} {'Avg Score':>10}")
        print(f"  {'-'*47}")
        for mode_name, r in results.items():
            print(f"  {mode_name:<15} {r['total']:>6} {r['passed']:>7} {r['pass_rate']:>6}% {r['avg_score']:>10.3f}")
    
    if dry_run:
        print("\n  Dry run — no workers launched.")


if __name__ == "__main__":
    main()
