#!/usr/bin/env python3
"""Phase T — TRAJECTORY (optional test step; SEPARATE from finalize).

This tool lives in .agents/tools/trajectory/ and does NOT depend on or touch the
finalize tooling. It is an EXPERIMENTAL, long-session step that takes a final/
document and DISTILLS it into K PARAMETRIZED VARIANTS, then runs the SAME
benchmark against each variant as the "standard reference" — so we can measure
how the standard's delivery (paradigm, vocabulary, consumer, edge-case focus)
affects downstream agent compliance.

The worker PROMPT is EXTERNALIZED to .agents/tools/prompts/trajectory-worker.md
(single source of truth; edit the .md, not this .py), loaded via the shared
templater with {{placeholder}} substitution — matching the exact standard used by
extraction-worker.md / strip-commentary.md / continue-worker / extend-area.

KEY IDEA (per project owner): the parameters are the "mission" the information is
sent under. They change how the information is RECEIVED: the same rule, delivered
under parameter-set A vs B, becomes a different document — different paradigm,
examples, consumer framing, edge-case focus, hints. A developer can use this to
distill final/ into a version written specifically for agentic code documentation,
or for a specific library (with hints, pitfalls, gotchas), etc.

DESIGN (mocked/basic benchmark, to be reworked later)
----------------------------------------------------
- Parameters are a JSON file OR a default grid (see default_params()).
- For each (document, parameter-set) pair, launch ONE long worker session
  (hermes-oneshot-wrapper --debug) that DISTILLS the source rule into a variant.
- Variants are written to ste-code/parametarized/<doc>/v<k>.md.
- A benchmark runner executes the SAME benchmark suite with each variant as the
  system-prompt "standard reference", collecting scores per variant.
- Variants are written to ste-code/parametarized/<doc>/v<k>.md (deliverables).
- Benchmark RESULTS are written under .agents/benchmark/tests/parametarized/<doc>/
  (inside the single benchmark output root, where the harness output-root guard
  requires them) as run-*/aggregate-results.json. The aggregator pass-rate and
  avg correctness are folded back into bench-<k>.json next to the variant.
  CRITICAL: it writes ONLY under ste-code/parametarized/ (variants) and the
  benchmark tests root (results) — never under final/.
- Workers run in PARALLEL (default 3, capped <=3) but each variant is its OWN
  long session — so "3 on 1 file" => 3 different variant files, then 3 bench runs.

SAFETY: this step ONLY writes under ste-code/parametarized/ and .agents/tmp/.
It NEVER touches final/ or adapted/. It is an optional test step, fully separate
from the finalize pipeline. It must not run while finalize owns final/rules/.

Usage:
  python3 trajectory.py --list-params            # show the default parameter grid
  python3 trajectory.py a-sec1-rule1.1.md        # distill into K variants (default grid)
  python3 trajectory.py a-sec1-rule1.1.md --variants 3
  python3 trajectory.py a-sec1-rule1.1.md --params my-grid.json
  python3 trajectory.py --all                    # every final/rules/*.md
  python3 trajectory.py --workers 3              # parallelism (default 3, max 3)
  python3 trajectory.py --plan                   # DRY RUN: print plan, write nothing
"""

from __future__ import annotations

import os
import re
import sys
import json
import time
import signal
import subprocess
import threading
import atexit
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path

_R = next(
    p
    for p in _Path(__file__).resolve().parents
    if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
from ste_paths import venv_python  # noqa: E402
from ste_io import write_text, mkdir  # noqa: E402

# Every agent setting this stage uses is declared in config.yaml beside it.
from ste_config import load as _load_config  # noqa: E402

CFG = _load_config(__file__)
from ste_runtime import resolve as _resolve_runtime  # noqa: E402

RT = _resolve_runtime(__file__)
FINAL_RULES_DIR = PROJECT / "ste-code" / "final" / "rules"
PARAM_DIR = PROJECT / "ste-code" / "parametarized"
TMP_DIR = PROJECT / ".agents" / "tmp"
DEBUG_DIR = TMP_DIR / "oneshot-debug"
VENDOR_DIR = PROJECT / ".agents" / "vendor"
PROMPT_MD = PROJECT / ".agents" / "tools" / "prompts" / "trajectory-worker.md"

MODEL = CFG.model
VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = RT.wrapper  # resolved by ste_runtime pre-flight
TIMEOUT_SECONDS = 1800  # long, multi-turn distillation sessions
MAX_WORKERS = 3

SECTION_RULE_RE = re.compile(r"a-sec(\d+)-rule([\d.]+)\.md$")
RULE_H1_RE = re.compile(r"^#\s*Rule\s+(\d+\.\d+)\s*—\s*(.+?)\s*$", re.M)

# Shared templater ({{placeholder}} substitution) — matches the project standard.
sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import render_template  # noqa: E402

_lock = threading.Lock()


# ── default parameter grid (versatile "mission" axes) ────────────────────────
def default_params() -> list[dict]:
    """Each dict is ONE parametrization / mission. Produce K variants per doc.

    Mission axes (encoded into the run — they change how the rule is RECEIVED):
      target_consumer : who receives it (llm_tool / agent / human_block)
      use_case        : domain/library to distill for (generic / a library / agentic docs)
      paradigm_emphasis: lens to lead with (OO / FP / async / systems / declarative / general)
      example_density : how many Non-STE/STE pairs
      vocab_strictness: lenient / strict (Microsoft/Google/STE-Code approved only)
      edge_case_focus : concrete edge-cases to enumerate (X and/or Y)
      register        : voice (strict_spec / friendly_tutorial / terse_reference)
      format          : structural preference
    """
    return [
        {
            "id": "v1_agentic_llmtool",
            "target_consumer": "llm_coding_tool",
            "use_case": "agentic code documentation (inline docstrings, commit messages, PR descriptions, error messages emitted by the agent)",
            "paradigm_emphasis": "general (agent-facing)",
            "example_density": "dense (>=10 pairs)",
            "vocab_strictness": "strict (Microsoft/Google approved only)",
            "edge_case_focus": "edge-cases to ambiguous identifier names; edge-cases to generated/boilerplate code",
            "register": "terse_reference",
            "format": "DO/DON'T checklist + copy-paste patterns",
        },
        {
            "id": "v2_library_react",
            "target_consumer": "human_developer_block",
            "use_case": "React/TypeScript front-end library (components, hooks, props, JSX, effects)",
            "paradigm_emphasis": "declarative / functional",
            "example_density": "dense (>=10 pairs)",
            "vocab_strictness": "strict",
            "edge_case_focus": "edge-cases to conditional rendering; edge-cases to effect dependencies",
            "register": "friendly_tutorial",
            "format": "example-led with library HINTS (pitfalls/gotchas)",
        },
        {
            "id": "v3_systems_async",
            "target_consumer": "autonomous_agent",
            "use_case": "systems / async backend (goroutines, channels, concurrency, error wrapping)",
            "paradigm_emphasis": "systems / async",
            "example_density": "sparse (4-6 pairs)",
            "vocab_strictness": "lenient",
            "edge_case_focus": "edge-cases to concurrent mutation; edge-cases to cancellation/timeout",
            "register": "strict_spec",
            "format": "full sections + decision procedures",
        },
    ]


def _load_params(path: Path | None) -> list[dict]:
    if path and path.exists():
        try:
            data = json.load(open(path))
            if isinstance(data, list):
                return data
            if isinstance(data, dict) and "variants" in data:
                return data["variants"]
        except Exception:
            pass
    return default_params()


def _format_param_block(param: dict) -> str:
    """Render the parameter dict as a readable, fenced block for the prompt."""
    lines = ["```mission"]
    for k, v in param.items():
        if k == "id":
            continue
        lines.append(f"- {k}: {v}")
    lines.append("```")
    return "\n".join(lines)


# ── prompt loader (externalized .md) ─────────────────────────────────────────
def _build_variant_prompt(doc_path: Path, param: dict) -> str:
    src = doc_path.read_text(encoding="utf-8", errors="ignore")
    m = RULE_H1_RE.search(src)
    self_num = (
        m.group(1) if m else doc_path.stem.replace("a-sec", "").replace("rule", ".")
    )
    title = m.group(2).strip() if m else doc_path.stem
    return render_template(
        PROMPT_MD,
        src_name=doc_path.name,
        src_text=src,
        param_block=_format_param_block(param),
        out_path=str(PARAM_DIR / doc_path.stem / f"v_{param.get('id', 'x')}.md"),
        self_num=self_num,
        title=title,
    )


# ── benchmark runner (wired to the real harness) ──────────────────────────
def run_benchmark_variant(variant_path: Path, doc_stem: str, variant_id: str) -> dict:
    """Run the SAME static benchmark suite with the variant as the system prompt.

    The variant .md is the "standard reference" the suite is scored against.
    Results are written under the single benchmark output root
    (.agents/benchmark/tests/parametarized/<doc>/) so the harness output-root
    guard is satisfied; the distilled variant docs themselves stay in
    ste-code/parametarized/ (a deliverable, never under final/).

    Falls back to a stub record if the orchestrator cannot be launched, so a
    trajectory run never hard-crashes on a benchmark failure.
    """
    bench_root = (
        Path(__file__).resolve().parent.parent.parent
        / "benchmark"
        / "tests"
        / "parametarized"
    )
    results_dir = bench_root / doc_stem / f"bench-{variant_id}"
    mkdir(results_dir)
    orch = (
        Path(__file__).resolve().parent.parent.parent / "benchmark" / "orchestrator.py"
    )
    try:
        r = subprocess.run(
            [
                sys.executable,
                str(orch),
                "--system-prompt-file",
                str(variant_path),
                "--results-dir",
                str(results_dir),
                "--model",
                MODEL,
                "--max-workers",
                "3",
                "--timeout",
                "1800",
                "--poll-interval",
                "10",
            ],
            capture_output=True,
            text=True,
            timeout=2400,
        )
        ok = r.returncode == 0
        agg = results_dir / "aggregate-results.json"
        pass_rate = None
        avg_score = None
        if agg.exists():
            try:
                d = json.loads(agg.read_text())
                pass_rate = d.get("pass_rate_pct")
                avg_score = d.get("aggregates", {}).get("avg_correctness")
            except Exception:
                pass
        return {
            "variant": str(variant_path),
            "doc": doc_stem,
            "variant_id": variant_id,
            "status": "ran" if ok else "error",
            "pass_rate": pass_rate,
            "avg_score": avg_score,
            "results_dir": str(results_dir),
            "ran_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
    except Exception as e:  # never let a benchmark failure kill the trajectory
        return {
            "variant": str(variant_path),
            "doc": doc_stem,
            "variant_id": variant_id,
            "status": "MOCKED",
            "pass_rate": None,
            "avg_score": None,
            "note": "orchestrator unavailable ({}); wire fixed but run skipped".format(
                e
            ),
            "ran_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }


# ── one variant job ─────────────────────────────────────────────────────────
def produce_variant(doc_path: Path, param: dict, do_bench: bool) -> dict:
    stem = doc_path.stem
    vid = param.get("id", "x")
    out_dir = PARAM_DIR / stem
    mkdir(out_dir)
    out_path = out_dir / f"v_{vid}.md"

    prompt = _build_variant_prompt(doc_path, param)
    pf = TMP_DIR / f"traj-{stem}-{vid}.txt"
    write_text(pf, prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "1800", "STE_MODEL": MODEL}
    try:
        r = subprocess.run(
            [VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL, "--debug"],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        with _lock:
            print(f"  [TIMEOUT] {stem} {vid}", flush=True)
        return {"doc": stem, "variant": vid, "ok": False, "reason": "timeout"}

    (TMP_DIR / f"traj-traj-{stem}-{vid}.txt").write_text(
        "STDOUT:\n" + r.stdout + "\nSTDERR:\n" + r.stderr, encoding="utf-8"
    )

    ok = (
        out_path.exists()
        and out_path.stat().st_size >= 300
        and bool(re.match(r"^#\s*Rule", out_path.read_text(errors="ignore").lstrip()))
    )
    result = {"doc": stem, "variant": vid, "ok": ok, "path": str(out_path)}
    if ok and do_bench:
        bench = run_benchmark_variant(out_path, stem, vid)
        result["bench"] = bench
        # Persist the bench record next to the variant for traceability.
        (out_path.parent / f"bench-{vid}.json").write_text(
            json.dumps(bench, indent=2), encoding="utf-8"
        )
        with _lock:
            print(
                f"  ✓ {stem} -> {out_path.name} (bench {bench['status']})", flush=True
            )
    elif ok:
        with _lock:
            print(f"  ✓ {stem} -> {out_path.name}", flush=True)
    else:
        with _lock:
            print(f"  [WEAK] {stem} {vid}: variant not written validly", flush=True)
    return result


# ── plan / dry-run ──────────────────────────────────────────────────────────
def _plan(docs: list[Path], params: list[dict], bench: bool):
    print("TRAJECTORY PLAN (dry-run)")
    print(
        f"docs={len(docs)} variants/doc={len(params)} total_jobs={len(docs) * len(params)}"
    )
    print(
        f"benchmark per variant: {bench} (real orchestrator under tests/parametarized/)"
    )
    print(f"output root: {PARAM_DIR}")
    print(f"prompt template: {PROMPT_MD}")
    for d in docs[:8]:
        for p in params:
            print(f"  - {d.name}  ->  {PARAM_DIR / d.stem}/v_{p.get('id', 'x')}.md")
    if len(docs) > 8:
        print(f"  ... and {len(docs) - 8} more docs")
    print("END PLAN")


def main():
    args = sys.argv[1:]
    plan_only = "--plan" in args
    do_all = "--all" in args
    bench = "--bench" in args
    list_params = "--list-params" in args
    single = next((a for a in args if a.endswith(".md")), None)
    variants_n = None
    params_file = None
    for i, a in enumerate(args):
        if a == "--variants" and i + 1 < len(args):
            try:
                variants_n = int(args[i + 1])
            except ValueError:
                pass
        if a == "--params" and i + 1 < len(args):
            params_file = Path(args[i + 1])
    workers = MAX_WORKERS
    for i, a in enumerate(args):
        if a == "--workers" and i + 1 < len(args):
            try:
                workers = max(1, min(MAX_WORKERS, int(args[i + 1])))
            except ValueError:
                pass

    if list_params:
        print(json.dumps(default_params(), indent=2))
        return

    # resolve params (optionally trim to N variants)
    params = _load_params(params_file)
    if variants_n is not None:
        params = params[: max(1, variants_n)]

    # resolve docs
    if single:
        docs = [
            (FINAL_RULES_DIR / single)
            if (FINAL_RULES_DIR / single).exists()
            else Path(single)
        ]
        docs = [d for d in docs if d.exists()]
    elif do_all:
        docs = sorted(FINAL_RULES_DIR.glob("a-sec*-rule*.md"))
    else:
        print(
            "Specify a .md file, --all, or --list-params. Use --plan for dry-run.",
            file=sys.stderr,
        )
        sys.exit(2)

    if plan_only:
        _plan(docs, params, bench)
        return

    if not PROMPT_MD.exists():
        print(f"FATAL: prompt template missing: {PROMPT_MD}", file=sys.stderr)
        sys.exit(1)

    atexit.register(lambda: None)
    signal.signal(signal.SIGINT, lambda *_: sys.exit(130))
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(0))

    jobs = [(d, p) for d in docs for p in params]
    print(
        f"  trajectory: {len(jobs)} variant jobs across <= {workers} workers...",
        flush=True,
    )

    def _run(job):
        d, p = job
        return produce_variant(d, p, bench)

    results = []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(_run, jobs))

    ok = sum(1 for r in results if r.get("ok"))
    print(
        f"\n{'=' * 60}\nTRAJECTORY done: {ok}/{len(results)} variants written"
        + (
            f"; benchmarks: {sum(1 for r in results if r.get('bench'))}"
            if bench
            else ""
        )
        + f"\noutput: {PARAM_DIR}\n{'=' * 60}",
        flush=True,
    )
    sys.exit(0 if ok == len(results) else 1)


if __name__ == "__main__":
    main()
