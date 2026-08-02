#!/usr/bin/env python3
"""STE-Code Refinement Orchestrator — parallel batch pipeline.

Reads ste-code/extracted/*.md (the 109 worker outputs) and reformat each into
clean, standardized markdown under ste-code/refined/ following the 9 refinement
rules. Mirrors extract_batch.py: checkpoint + per-batch git commit + crash-safe
resume (--resume).

Launches each BATCH as its own background process so batches run in parallel
(multiple workers per file, many batches at once) — this is the "batch of many
workers" mode.

Usage:
  python3 refine_batch.py [start_batch] [num_batches] [--resume]
  python3 refine_batch.py            # all 37 batches, serial launch of parallel batches
  STE_MODEL=tencent/hy3:free python3 refine_batch.py 1 37

Model: resolved via STE_MODEL env var (default tencent/hy3:free), matching
extract_batch.py.
"""

import os
import sys
import time
import re
import json
import signal
import subprocess
import atexit
from pathlib import Path
from datetime import datetime, timezone

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
EXTRACTED_DIR = PROJECT / "ste-code" / "extracted"
REFINED_DIR = PROJECT / "ste-code" / "refined"
STATE_DIR = PROJECT / ".agents" / "state"
CHECKPOINT_PATH = STATE_DIR / "refine-checkpoint.json"

# ── Config ────────────────────────────────────────────────────────────────────
MODEL = os.environ.get("STE_MODEL", "tencent/hy3:free")
WORKERS_PER_BATCH = int(os.environ.get("REFINE_WORKERS_PER_BATCH", "3"))
TOTAL_WORKERS = 109
TIMEOUT_SECONDS = 600

VENV_PYTHON = str(Path.home() / ".hermes" / "hermes-agent" / "venv" / "bin" / "python3")
WRAPPER = str(PROJECT / ".agents" / "tools" / "lib" / "hermes-oneshot-wrapper.py")

FILENAME_RE = re.compile(r"^w(?P<worker>\d{3})-p(?P<start>\d{1,4})-(?P<end>\d{1,4})\.md$")

# ── Skill embedding: inject the refinement SKILL.md into every worker prompt ──
# The oneshot wrapper sub-agents do not auto-load the STE-Code profile skills,
# so the authoritative skill text is embedded. Edit the SKILL.md (not this
# script) to change refinement behavior.
import sys as _sys
_sys.path.insert(0, str(PROJECT / ".agents" / "tools" / "lib"))
from templater import lib_import

skill_prompt = lib_import("skill_prompt")

# ── Prompt text lives in templates/, not in this file ─────────────────────────
# See .agents/tools/lib/PROMPTS.md. Edit templates/refine-*.md to change
# wording; this script only supplies the values.
templater = lib_import("templater")
_TPL = templater.Templater(__file__)


def _word_count(text):
    """Count meaningful CONTENT words, ignoring markup tags and the repeated
    page-header boilerplate that Rule 7 mandates collapsing.

    The raw counter used to treat `<br>`->"br", `<mark>`->"mark", and every
    repeated "ASD-STE100 Simplified Technical English" / "Issue 9 2025-01-15" /
    "Page 2-1-C18" stamp as content words. That penalized CORRECT refinement
    (which strips those tags and collapses the stamps), so a perfectly refined
    file failed the >=98% parity gate. Normalizing first makes the gate measure
    real content parity, not formatting.
    """
    t = _MARKUP_TAG_RE.sub(" ", text)
    t = _BOILERPLATE_RE.sub(" ", t)
    return len(re.findall(r"[A-Za-z0-9]{2,}", t.lower()))


def _mark_text_coverage(src_txt, out_txt):
    """Return (missing_count, total_source_marks) measuring whether the TEXT
    inside <mark>…</mark> spans is preserved, not whether the raw <mark> tag
    counts match.

    Why: the PDF extraction often splits one annotated sentence into two <mark>
    spans (e.g. a lone `<mark>Non-STE:</mark>` label fragment followed by
    `<mark>_the sentence_</mark>`). A correct worker MERGES those into one clean
    `<mark>` span — preserving 100% of the marked words while REDUCING the raw
    tag count. The old `out_marks >= src_marks` check failed those correct files.

    We instead take each source mark's significant word-shingle and confirm it
    appears in the output's tag-stripped text. Pure label fragments ("STE:",
    "Non-STE:") carry no unique content and are skipped — their text always
    survives on the paired example line.
    """
    def norm(s):
        s = re.sub(r"<[^>]+>", " ", s)
        s = re.sub(r"[^a-z0-9 ]", " ", s.lower())
        return re.sub(r"\s+", " ", s).strip()

    src_spans = re.findall(r"<mark>(.*?)</mark>", src_txt, re.S)
    out_all = norm(out_txt)
    total = 0
    missing = 0
    for span in src_spans:
        n = norm(span)
        words = [w for w in n.split() if w not in ("ste", "non")]
        if len(words) < 2:
            continue
        # Skip dictionary column-HEADER labels ("Column 3: STE EXAMPLE",
        # "Column 4: Non-STE example"). These are preserved as the real
        # | STE example | Non-STE example | table header, so their literal
        # shingle intentionally won't match — not content loss.
        if "column" in words and ("example" in words or "ste" in words):
            continue
        total += 1
        shingle = " ".join(words[:6])
        if shingle not in out_all:
            missing += 1
    return missing, total


# HTML-ish structural tags (<br>, <u>, <mark>, </mark>, ...): formatting, not content.
_MARKUP_TAG_RE = re.compile(r"</?[a-zA-Z][^>]*>")

# Repeated per-page stamps that Rule 7 collapses into the single metadata block.
# Counting these as "content" made correct header-collapse look like word loss.
_BOILERPLATE_RE = re.compile(
    r"(?i)(ASD[-\s]?STE100(\s+Simplified\s+Technical\s+English)?"
    r"|Simplified\s+Technical\s+English"
    r"|Issue\s+9(\s*[-,]?\s*(2025-01-15|January\s+2025))?"
    r"|Part\s+\d+\s*[-–]\s*Dictionary"
    r"|Part\s+\d+\s*[-–]\s*Writing\s+rules"            # repeated running header
    r"|Subject[-\s]?to[-\s]?rule\s+index"               # repeated index running-header
    r"|Table\s+of\s+contents"
    r"|\d{4}-\d{2}-\d{2}"                                # date stamps (2024-04-30, ...)
    r"|Page\s+[A-Z0-9]+-[A-Z0-9\-]+"                 # Page 2-1-C18, Page HI-12
    r"|Page\s+\d+(\s*[–-]\s*\d+)?\s+of\s+434"        # Page 34 of 434, Page 34–35 of 434
    r"|Highlights)"
)


def _build_prompt(input_filename, output_filename, start_page, end_page):
    """Refinement worker prompt = tight wrapper + the authoritative refinement SKILL.md.

    The SKILL.md (rules 1-9, before/after examples, failure recovery) is the
    single source of truth. We embed it so the worker honors the exact protocol
    and we only have to edit the SKILL, not this script.
    """
    wrapper = _TPL.render(
        "refine-worker",
        input_filename=input_filename,
        output_filename=output_filename,
        start_page=start_page,
        end_page=end_page,
    )
    skill = skill_prompt.skill_section("refinement")
    return wrapper + skill + "\n\nOutput ONLY the refined markdown file. No explanations, no commentary.\n"


def _build_batch_prompt(files):
    """Multi-file worker prompt: embed the skill ONCE, then N sequential per-file
    tasks. One session refines several pages back-to-back.

    files: list of (input_filename, output_filename, start_page, end_page).

    Token math (measured): skill+wrapper ≈ 7.9k tok loaded once; each file costs
    ~5k tok (read+write+reason). 3 files ≈ 23k tok ≈ 9% of a 250k session, so
    context is never the limit. The ONLY risk is per-response output truncation
    on the free model, so the worker MUST finish and write each file completely
    before starting the next — each write is then its own bounded ~1.7k-tok
    generation. Files are independent; a failure on one does not block the rest.
    """
    n = len(files)
    task_blocks = []
    for i, (inp, out, s, e) in enumerate(files, 1):
        task_blocks.append(
            _TPL.render("refine-batch-task", i=i, n=n, inp=inp, out=out,
                        s=s, e=e)
        )
    tasks = "\n\n".join(task_blocks)
    wrapper = _TPL.render("refine-batch", n=n, tasks=tasks)
    skill = skill_prompt.skill_section("refinement")
    return wrapper + skill + f"\n\nOutput ONLY the {n} refined markdown files. No explanations, no commentary.\n"


def _load_checkpoint():
    if CHECKPOINT_PATH.exists():
        try:
            return json.load(open(CHECKPOINT_PATH))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_checkpoint(ckpt):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = str(CHECKPOINT_PATH) + ".tmp"
    try:
        with open(tmp, "w") as f:
            json.dump(ckpt, f, indent=2, default=str)
        os.replace(tmp, str(CHECKPOINT_PATH))
    except Exception:
        pass


_checkpoint = _load_checkpoint()


def find_workers():
    """Map worker_num -> (path, start, end) sorted by worker number."""
    workers = {}
    for f in EXTRACTED_DIR.glob("*.md"):
        m = FILENAME_RE.match(f.name)
        if not m:
            continue
        w = int(m.group("worker"))
        workers[w] = (f, int(m.group("start")), int(m.group("end")))
    return dict(sorted(workers.items()))


def git_commit_locked(files, msg):
    """Serialize git commits across parallel batches via a lock dir."""
    import time as _time
    lock = STATE_DIR / "refine-git-lock"
    deadline = _time.time() + 120
    while _time.time() < deadline:
        try:
            lock.mkdir(exist_ok=False)
            break
        except FileExistsError:
            _time.sleep(1)
    else:
        return False
    try:
        subprocess.run(["git", "add", *files], capture_output=True, text=True, cwd=str(PROJECT))
        r = subprocess.run(["git", "commit", "-m", msg, *files],
                           capture_output=True, text=True, cwd=str(PROJECT))
        return r.returncode == 0
    finally:
        import shutil
        shutil.rmtree(lock, ignore_errors=True)


def run_worker(worker_num, src_path, start, end):
    """Run a single refinement worker (foreground, returns True/False).

    Retries on transient failures (API 429 / rate-limit / no output) with
    exponential backoff, since the oneshot wrapper exits fast on rejection.
    """
    output_name = f"r{worker_num:03d}-p{start}-{end}.md"
    output_path = REFINED_DIR / output_name

    # checkpoint skip
    ck = _checkpoint.get(str(worker_num))
    if ck and ck.get("passed") and output_path.exists():
        print(f"  R{worker_num:03d}: ✓ Already refined (checkpoint skip)", flush=True)
        return True

    prompt = _build_prompt(src_path.name, output_name, start, end)
    tmp = PROJECT / ".agents" / "tmp"
    tmp.mkdir(parents=True, exist_ok=True)
    pf = tmp / f"refine-prompt-{worker_num:03d}.txt"
    pf.write_text(prompt)

    env = {**os.environ, "HERMES_REQUEST_TIMEOUT": "120", "STE_MODEL": MODEL}
    cmd = [VENV_PYTHON, WRAPPER, str(pf), "--model", MODEL]

    max_attempts = 4
    for attempt in range(1, max_attempts + 1):
        start_t = time.time()
        print(f"  R{worker_num:03d}: Refining {src_path.name} → {output_name} (attempt {attempt})...", flush=True)
        try:
            result = subprocess.run(cmd, capture_output=True, text=True,
                                    timeout=TIMEOUT_SECONDS, env=env, cwd=str(PROJECT))
            dur = time.time() - start_t
            if result.stderr:
                sl = result.stderr.lower()
                if "error" in sl or "traceback" in sl:
                    print(f"  R{worker_num:03d}: [stderr] {result.stderr[:300]}", flush=True)
        except subprocess.TimeoutExpired:
            print(f"  R{worker_num:03d}: [TIMEOUT] after {TIMEOUT_SECONDS}s", flush=True)
            return False
        except Exception as e:
            print(f"  R{worker_num:03d}: [ERROR] {e}", flush=True)
            return False

        if output_path.exists():
            sz = output_path.stat().st_size
            txt = output_path.read_text(encoding="utf-8")
            ok_size = sz >= 400
            ok_skel = txt.lstrip().startswith(f"# Page {start}")

            # ── AUTOMATED CONTENT-PARITY GATE ──
            # Hard backstop for the user's zero-content-loss requirement: the
            # refined file must not have lost content words or dropped the
            # source's <mark> annotated examples (e.g.
            # _<u><mark>Put out the cat.</mark></u>_). _word_count() normalizes
            # markup + Rule-7 boilerplate so this measures REAL content parity.
            src_txt = src_path.read_text(encoding="utf-8", errors="ignore")
            src_words = _word_count(src_txt)
            out_words = _word_count(txt)
            ok_parity = out_words >= int(src_words * 0.98)  # allow ≤2% content drift
            # Verify the <mark> annotated EXAMPLE TEXT survives, by content —
            # not by raw tag count. Workers legitimately MERGE PDF-split mark
            # fragments (a lone `<mark>Non-STE:</mark>` + `<mark>_text_</mark>`)
            # into one clean span, preserving all words while reducing the tag
            # count. _mark_text_coverage checks each source mark's word-shingle
            # appears in the output; label-only fragments are skipped.
            missing_marks, total_marks = _mark_text_coverage(src_txt, txt)
            ok_marks = missing_marks == 0

            if ok_size and ok_skel and ok_parity and ok_marks:
                _checkpoint[str(worker_num)] = {"passed": True, "output_size": sz,
                                                "duration": round(dur, 1)}
                _save_checkpoint(_checkpoint)
                print(f"  R{worker_num:03d}: [PASS] {sz}B ({dur:.1f}s) "
                      f"words {out_words}/{src_words} marks {total_marks-missing_marks}/{total_marks}", flush=True)
                return True
            else:
                reasons = []
                if not ok_size: reasons.append(f"size={sz}B")
                if not ok_skel: reasons.append("skeleton_missing")
                if not ok_parity: reasons.append(f"word_loss {out_words}/{src_words}")
                if not ok_marks: reasons.append(f"marks_lost {missing_marks}/{total_marks}")
                print(f"  R{worker_num:03d}: [FAIL] {'; '.join(reasons)} — retrying", flush=True)
        else:
            print(f"  R{worker_num:03d}: [FAIL] no output file — likely rate-limited, retrying", flush=True)

        # Backoff before retry (covers 429 / transient API rejection)
        backoff = 20 * attempt
        print(f"  R{worker_num:03d}: sleeping {backoff}s before retry...", flush=True)
        time.sleep(backoff)

    print(f"  R{worker_num:03d}: [GIVEUP] after {max_attempts} attempts", flush=True)
    return False


def process_batch(batch_num, workers_map):
    start_worker = (batch_num - 1) * WORKERS_PER_BATCH + 1
    members = [(w, workers_map[w]) for w in range(start_worker, start_worker + WORKERS_PER_BATCH)
               if w in workers_map]
    if not members:
        print(f"Batch {batch_num}: no workers", flush=True)
        return True

    ids = ", ".join(f"R{w:03d}" for w, _ in members)
    print(f"\n{'='*60}\nBatch {batch_num} — {ids}\n{'='*60}", flush=True)

    all_ok = True
    for w, (src, s, e) in members:
        ok = run_worker(w, src, s, e)
        if not ok:
            all_ok = False

    # git commit passed worker outputs (serialized across parallel batches)
    passed_files = []
    for w, (src, s, e) in members:
        out = REFINED_DIR / f"r{w:03d}-p{s}-{e}.md"
        if out.exists():
            passed_files.append(str(out.relative_to(PROJECT)))
    if passed_files:
        msg = f"Refine Batch {batch_num:02d} - {'PASS' if all_ok else 'PARTIAL'} - {ids}"
        ok = git_commit_locked(passed_files, msg)
        if ok:
            print(f"  ✓ Committed: {msg}", flush=True)
        else:
            print(f"  ✗ Commit failed: {msg}", flush=True)
    return all_ok


def main():
    resume = "--resume" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    start_batch = int(args[0]) if len(args) > 0 else 1
    num_batches = int(args[1]) if len(args) > 1 else 37

    workers_map = find_workers()
    print(f"STE-Code Refinement Pipeline", flush=True)
    print(f"Model: {MODEL}", flush=True)
    print(f"Workers available: {len(workers_map)} (batches of {WORKERS_PER_BATCH})", flush=True)
    print(f"Batches: {num_batches} (from {start_batch})", flush=True)
    print(f"Resume: {'yes' if resume else 'no'}", flush=True)

    atexit.register(lambda: _save_checkpoint(_checkpoint))
    signal.signal(signal.SIGTERM, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(0)))
    signal.signal(signal.SIGINT, lambda *_: (_save_checkpoint(_checkpoint), sys.exit(130)))

    for batch_num in range(start_batch, min(start_batch + num_batches, TOTAL_WORKERS // WORKERS_PER_BATCH + 2)):
        if (batch_num - 1) * WORKERS_PER_BATCH + 1 > TOTAL_WORKERS:
            break
        process_batch(batch_num, workers_map)

    final = len(list(REFINED_DIR.glob("r*.md")))
    print(f"\n{'='*60}\nDone. Files in refined/: {final}\n{'='*60}", flush=True)


if __name__ == "__main__":
    main()
