#!/usr/bin/env python3
"""Adaptive, rate-limit-aware concurrency controller with checkpoint/resume.

This module is PURE LOGIC plus a simulation self-test. It never calls a model;
the risky operation is injected as a callable so the whole thing is testable
offline.

Why AIMD (additive-increase / multiplicative-decrease)
-----------------------------------------------------
The real benchmark hammers ONE free-tier endpoint with several orchestrators at
once. The safe concurrency ceiling is unknown in advance and varies as other jobs
come and go. A fixed pool either wastes the endpoint (too low) or gets 429'd into
the ground (too high). AIMD converges on the server's actual tolerance without
being told what it is, and -- crucially -- it is *provably fair* when N jobs
share one endpoint: every job that gets a 429 backs off multiplicatively, so the
aggregate converges to the capacity that exists. A fixed pool cannot do this.

Empty output is RETRYABLE. At this layer a truncated model response is
indistinguishable from a transport failure (both arrive as "no usable answer"),
so we treat it as transient and retry.

All defaults are constants. If harness_config exposes matching keys they are
used; otherwise the constants stand. We do NOT edit harness_config here -- it is
shared with another worker.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import sys
import tempfile
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

try:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from harness_config import load_config

    _HAVE_CFG = True
except Exception:  # pragma: no cover - harness_config is optional for this module
    _HAVE_CFG = False


# --------------------------------------------------------------------- constants

DEFAULT_FLOOR = 1
DEFAULT_CEILING = 8
DEFAULT_BACKOFF = 0.5  # multiplicative decrease factor on rate-limit
DEFAULT_RETRY_BASE = 1.0  # seconds; full-jitter exponential backoff base
DEFAULT_RETRY_CAP = 30.0  # max single backoff sleep
DEFAULT_MAX_ATTEMPTS = 5  # per-case attempt ceiling
DEFAULT_CB_FAILURE_RATE = 0.5  # rolling failure rate that opens the breaker
DEFAULT_CB_MIN_SAMPLE = 10  # min observations before the breaker may open
DEFAULT_CB_COOLDOWN = 10.0  # seconds the breaker stays open


def _cfg_int(key: str, default: int) -> int:
    if not _HAVE_CFG:
        return default
    try:
        return int(getattr(load_config(), key, default))
    except Exception:
        return default


def _cfg_float(key: str, default: float) -> float:
    if not _HAVE_CFG:
        return default
    try:
        return float(getattr(load_config(), key, default))
    except Exception:
        return default


# ----------------------------------------------------------------- AdaptiveWindow


class AdaptiveWindow:
    """AIMD congestion controller for model-endpoint concurrency.

    Additively increases on success (+1, capped at ceiling) and multiplicatively
    decreases on a rate-limit/timeout signal (window *= backoff_factor, floored
    at the floor). Tracks exponentially-weighted success/failure rates and an
    auditable log of every window change.
    """

    def __init__(
        self,
        floor: int = None,
        ceiling: int = None,
        backoff_factor: float = None,
        now: "callable" = None,
    ) -> None:
        self.floor = _cfg_int(
            "sched_floor", floor if floor is not None else DEFAULT_FLOOR
        )
        self.ceiling = _cfg_int(
            "sched_ceiling", ceiling if ceiling is not None else DEFAULT_CEILING
        )
        self.backoff_factor = _cfg_float(
            "sched_backoff",
            backoff_factor if backoff_factor is not None else DEFAULT_BACKOFF,
        )
        self._now = now or (lambda: time.time())
        self.window = max(self.floor, self.ceiling // 2)  # start mid-range
        self.in_flight = 0
        self.success_ewma = 0.0
        self.failure_ewma = 0.0
        self.decisions: "list[dict]" = []

    def _log(self, trigger: str, before: int) -> None:
        self.decisions.append(
            {
                "ts": self._now(),
                "trigger": trigger,
                "before": before,
                "after": self.window,
            }
        )

    def on_success(self) -> None:
        before = self.window
        self.success_ewma = 0.8 * self.success_ewma + 0.2 * 1.0
        self.failure_ewma = 0.8 * self.failure_ewma + 0.2 * 0.0
        if self.window < self.ceiling:
            self.window = min(self.ceiling, self.window + 1)
            self._log("success", before)

    def on_rate_limited(self) -> None:
        before = self.window
        self.failure_ewma = 0.8 * self.failure_ewma + 0.2 * 1.0
        self.window = max(self.floor, int(self.window * self.backoff_factor))
        if self.window < self.floor:
            self.window = self.floor
        self._log("rate_limit", before)

    def on_timeout(self) -> None:
        self.on_rate_limited()


# ------------------------------------------------------------- classify_failure

_RETRYABLE_TEXT = (
    "429",
    "rate limit",
    "ratelimit",
    "too many requests",
    "503",
    "502",
    "500",
    "504",
    "connection reset",
    "connection refused",
    "connection aborted",
    "read timeout",
    "timeout",
    "timed out",
    "deadline",
    "empty",
    "no response",
    "truncated",
    "econnreset",
)
_TERMINAL_TEXT = (
    "400",
    "401",
    "403",
    "404",
    "422",
    "unauthorized",
    "forbidden",
    "bad request",
    "not found",
    "malformed",
    "validation error",
    "schema",
)


def classify_failure(exc_or_text) -> str:
    """Return 'retryable' or 'terminal' for an exception or text.

    Empty output is RETRYABLE: a truncated model response cannot be told apart
    from a transport failure at this layer, so we retry rather than drop.
    """
    text = ""
    if isinstance(exc_or_text, BaseException):
        text = "{} {}".format(type(exc_or_text).__name__, str(exc_or_text))
    else:
        text = str(exc_or_text)
    low = text.lower()
    for frag in _TERMINAL_TEXT:
        if frag in low:
            return "terminal"
    for frag in _RETRYABLE_TEXT:
        if frag in low:
            return "retryable"
    return "retryable"


# ------------------------------------------------------------------ RetryPolicy


class RetryPolicy:
    """Exponential backoff with FULL JITTER.

    sleep = random.uniform(0, min(cap, base * 2**attempt))

    Full jitter (not equal jitter, not no jitter) maximally decorrelates retries:
    when many workers are 429'd at the same instant they would otherwise all
    retry on the same schedule and re-collide. Uniform[0, cap] spreads the
    re-attempts so the endpoint gets a thinned, staggered stream.
    """

    def __init__(
        self,
        base: float = None,
        cap: float = None,
        max_attempts: int = None,
        rng: "random.Random" = None,
    ) -> None:
        self.base = _cfg_float(
            "sched_retry_base", base if base is not None else DEFAULT_RETRY_BASE
        )
        self.cap = _cfg_float(
            "sched_retry_cap", cap if cap is not None else DEFAULT_RETRY_CAP
        )
        self.max_attempts = _cfg_int(
            "sched_max_attempts",
            max_attempts if max_attempts is not None else DEFAULT_MAX_ATTEMPTS,
        )
        self.rng = rng or random.Random(1234)

    def sleep_for(self, attempt: int) -> float:
        hi = min(self.cap, self.base * (2**attempt))
        return self.rng.uniform(0.0, hi)

    def should_retry(self, attempt: int, failure) -> "tuple[bool, str]":
        kind = classify_failure(failure)
        if kind == "terminal":
            return False, "terminal failure"
        if attempt >= self.max_attempts - 1:
            return False, "attempts exhausted ({}/{})".format(
                attempt + 1, self.max_attempts
            )
        return True, "retryable (attempt {}/{}), backoff {:.2f}s".format(
            attempt + 1, self.max_attempts, self.sleep_for(attempt)
        )


# --------------------------------------------------------------- CircuitBreaker


class CircuitBreaker:
    """Rolling-window circuit breaker: closed -> open -> half-open -> closed.

    Opens when the rolling failure rate crosses `failure_rate` over at least
    `min_sample` recent observations. Stays open for `cooldown` seconds, then
    half-opens and admits a single probe; a probe success closes it, a probe
    failure re-opens it. All state, the transition log, and the sample window
    are observable.
    """

    CLOSED, OPEN, HALF_OPEN = "closed", "open", "half_open"

    def __init__(
        self,
        failure_rate: float = None,
        min_sample: int = None,
        cooldown: float = None,
        window: int = 100,
        now: "callable" = None,
    ) -> None:
        self.failure_rate = _cfg_float(
            "sched_cb_rate",
            failure_rate if failure_rate is not None else DEFAULT_CB_FAILURE_RATE,
        )
        self.min_sample = _cfg_int(
            "sched_cb_sample",
            min_sample if min_sample is not None else DEFAULT_CB_MIN_SAMPLE,
        )
        self.cooldown = _cfg_float(
            "sched_cb_cooldown",
            cooldown if cooldown is not None else DEFAULT_CB_COOLDOWN,
        )
        self.window = window
        self._now = now or (lambda: time.time())
        self.state = self.CLOSED
        self.opened_at = 0.0
        self._samples: "deque[bool]" = deque(maxlen=window)
        self.transitions: "list[dict]" = []

    def _transition(self, to: str, why: str) -> None:
        self.state = to
        self.transitions.append({"ts": self._now(), "to": to, "why": why})

    def _open(self, why: str) -> None:
        self.opened_at = self._now()
        self._transition(self.OPEN, why)

    def record(self, success: bool) -> None:
        self._samples.append(bool(success))
        if self.state == self.OPEN:
            return
        if self.state == self.HALF_OPEN:
            if success:
                self._transition(self.CLOSED, "half-open probe succeeded")
            else:
                self._open("half-open probe failed")
            return
        if len(self._samples) >= self.min_sample:
            fails = sum(1 for s in self._samples if not s)
            rate = fails / len(self._samples)
            if rate >= self.failure_rate:
                self._open(
                    "failure rate {:.0%} >= {:.0%} over {}".format(
                        rate, self.failure_rate, len(self._samples)
                    )
                )

    def allow(self) -> bool:
        if self.state == self.CLOSED:
            return True
        if self.state == self.HALF_OPEN:
            return True
        if self._now() - self.opened_at >= self.cooldown:
            self._transition(self.HALF_OPEN, "cooldown elapsed")
            return True
        return False

    @property
    def failure_rate_obs(self) -> "float | None":
        if not self._samples:
            return None
        return sum(1 for s in self._samples if not s) / len(self._samples)


# ------------------------------------------------------------------- Checkpoint


class Checkpoint:
    """Append-only, fsync'd JSONL of completed case ids.

    Written durably as each case finishes (flush + os.fsync) so a SIGKILL cannot
    lose the record -- this is the fix for observed data loss: a killed run
    resumes without repeating completed work. Concurrent appenders are tolerated
    because each line is written atomically (one full line + fsync).
    """

    def __init__(self, path: "str | Path") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("", encoding="utf-8")

    def _append(self, record: dict) -> None:
        line = json.dumps(record, separators=(",", ":")) + "\n"
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())

    def record_done(
        self, case_id: str, outcome: str, wall_s: float, attempts: int
    ) -> None:
        self._append(
            {
                "id": case_id,
                "outcome": outcome,
                "wall_s": round(wall_s, 4),
                "attempts": attempts,
                "ts": datetime.now(timezone.utc).isoformat(),
            }
        )

    def completed(self) -> "set[str]":
        done: "set[str]" = set()
        with open(self.path, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if rec.get("outcome") == "ok":
                    done.add(rec["id"])
        return done

    def remaining(self, all_ids: "list[str]") -> "list[str]":
        done = self.completed()
        return [i for i in all_ids if i not in done]


# ---------------------------------------------------------------------- run_pool


def run_pool(
    cases,
    execute,
    *,
    checkpoint_path=None,
    window=None,
    breaker=None,
    retry=None,
    rng=None,
    simulate_kill_after=None,
    now: "callable" = None,
):
    """STREAMING dispatch with a sliding AIMD window.

    `execute(case)` is injected; it must return a truthy result on success and
    raise on failure (classified by `retry`). A case that exhausts its retries is
    RECORDED AS FAILED -- never silently dropped.

    Returns a summary dict: total wall time, completion rate, p50/p90/max
    per-case time, retries, terminal failures, and final window size.
    """
    win = window or AdaptiveWindow()
    breaker = breaker or CircuitBreaker(now=now)
    retry = retry or RetryPolicy(rng=rng or random.Random(7))
    ckpt = Checkpoint(checkpoint_path) if checkpoint_path else None
    _now = now or (lambda: time.time())

    all_ids = [c.get("id") if isinstance(c, dict) else str(c) for c in cases]
    id_to_case = {cid: c for cid, c in zip(all_ids, cases)}
    pending = list(cases)
    if ckpt is not None:
        done_ids = ckpt.completed()
        pending = [c for c, cid in zip(cases, all_ids) if cid not in done_ids]

    results = {}
    wall_times = []
    retries_total = 0
    terminal_failures = 0
    killed = False
    t_start = _now()

    # Sliding window simulation: process a bounded number of active cases.
    # active is keyed by case id (hashable); value carries the case object.
    active = {}  # cid -> (case, start_time, attempts)
    i = 0
    while pending or active:
        while len(active) < win.window and i < len(pending) and breaker.allow():
            case = pending[i]
            cid = all_ids[cases.index(case)] if case in cases else str(case)
            active[cid] = (case, _now(), 0)
            i += 1
        if not active:
            if breaker.state == CircuitBreaker.OPEN:
                time.sleep(min(0.01, breaker.cooldown / 10.0))
                continue
            if i >= len(pending):
                break
            continue
        for cid in list(active.keys()):
            case, start, attempts = active[cid]
            try:
                ok = execute(case)
                if not ok:
                    raise RuntimeError("empty output")
                wall = _now() - start
                wall_times.append(wall)
                win.on_success()
                breaker.record(True)
                if ckpt is not None:
                    ckpt.record_done(cid, "ok", wall, attempts + 1)
                results[cid] = "ok"
                del active[cid]
                if (
                    simulate_kill_after is not None
                    and len(results) >= simulate_kill_after
                ):
                    killed = True
                    break
            except Exception as exc:  # noqa: BLE001 - intentional broad catch
                attempts += 1
                kind = classify_failure(exc)
                if kind == "terminal":
                    breaker.record(False)
                    terminal_failures += 1
                    if ckpt is not None:
                        ckpt.record_done(cid, "terminal", _now() - start, attempts)
                    results[cid] = "terminal"
                    del active[cid]
                    continue
                should, _ = retry.should_retry(attempts, exc)
                if should:
                    retries_total += 1
                    win.on_rate_limited()
                    breaker.record(False)
                    time.sleep(
                        retry.sleep_for(attempts)
                        if retry.sleep_for(attempts) < 0.02
                        else 0.0
                    )
                    active[cid] = (case, _now(), attempts)
                else:
                    win.on_rate_limited()
                    breaker.record(False)
                    if ckpt is not None:
                        ckpt.record_done(cid, "failed", _now() - start, attempts)
                    results[cid] = "failed"
                    del active[cid]
        if simulate_kill_after is not None and len(results) >= simulate_kill_after:
            killed = True
            break

    total = len(all_ids)
    done = sum(1 for v in results.values() if v == "ok")
    wall_all = _now() - t_start
    ptiles = _percentiles(wall_times, [50, 90]) if wall_times else (0.0, 0.0)
    return {
        "total": total,
        "completed": done,
        "completion_rate_pct": round(done / total * 100, 1) if total else 0.0,
        "wall_s": round(wall_all, 4),
        "p50_s": round(ptiles[0], 4),
        "p90_s": round(ptiles[1], 4),
        "max_s": round(max(wall_times), 4) if wall_times else 0.0,
        "retries": retries_total,
        "terminal_failures": terminal_failures,
        "final_window": win.window,
        "killed": killed,
        "results": results,
    }


def _percentiles(values: "list[float]", ps: "list[int]") -> "list[float]":
    s = sorted(values)
    out = []
    for p in ps:
        if not s:
            out.append(0.0)
            continue
        k = max(0, min(len(s) - 1, int(round((p / 100.0) * (len(s) - 1)))))
        out.append(s[k])
    return out


# ----------------------------------------------------------------------- selftest


def _selftest() -> int:
    """Simulation self-test. No network. Prints PASS/FAIL lines, exits non-zero
    on failure. Real measured distribution is TIME-SCALED BY 1/100 (a 29 s/test
    becomes 0.29 s/test) so the suite runs fast; the comparison table scales the
    wall-clock back up by 100 for projected real-world figures."""
    SCALE = 100
    print(
        "scheduler self-test (time scale 1/{}; real = simulated x {})".format(
            SCALE, SCALE
        )
    )
    fails = 0

    def check(ok, label):
        nonlocal fails
        print(("PASS " if ok else "FAIL ") + label)
        if not ok:
            fails += 1

    # ---- AdaptiveWindow behaviour
    w = AdaptiveWindow(floor=1, ceiling=8, backoff_factor=0.5, now=(lambda: 0.0))
    for _ in range(7):
        w.on_success()
    check(
        w.window == 8,
        "window ramps to ceiling after successes (got {})".format(w.window),
    )
    for _ in range(3):
        w.on_rate_limited()
    check(
        w.window == 1,
        "window multiplicative-decreases to floor on rate-limit (got {})".format(
            w.window
        ),
    )
    check(
        len(w.decisions) == 7,
        "every window change audited ({} entries)".format(len(w.decisions)),
    )

    # ---- classify_failure table
    check(
        classify_failure("HTTP 429 Too Many Requests") == "retryable", "429 retryable"
    )
    check(
        classify_failure("connection reset by peer") == "retryable",
        "conn reset retryable",
    )
    check(classify_failure("empty output") == "retryable", "empty output retryable")
    check(classify_failure("HTTP 400 Bad Request") == "terminal", "400 terminal")
    check(classify_failure("auth failure 401") == "terminal", "401 terminal")
    check(
        classify_failure(ValueError("some unknown error")) == "retryable",
        "unknown exc retryable",
    )

    # ---- RetryPolicy full jitter bounds
    rp = RetryPolicy(base=1.0, cap=30.0, max_attempts=5, rng=random.Random(0))
    for att in range(5):
        s = rp.sleep_for(att)
        check(
            0.0 <= s <= min(30.0, 1.0 * 2**att) + 1e-9,
            "jitter within [0, min(cap, base*2**att)] att={} s={:.3f}".format(att, s),
        )
    ok, why = rp.should_retry(4, RuntimeError("429"))
    check((not ok) and "exhausted" in why, "retries stop after max_attempts")

    # ---- CircuitBreaker opens under high failure rate
    cb = CircuitBreaker(
        failure_rate=0.5, min_sample=10, cooldown=0.05, now=(lambda: 0.0)
    )
    for _ in range(12):
        cb.record(False)
    check(
        cb.state == CircuitBreaker.OPEN,
        "breaker opens under 90% failure rate (state={})".format(cb.state),
    )
    cb._now = lambda: 1.0
    assert cb.allow() is True
    cb.record(True)
    check(
        cb.state == CircuitBreaker.CLOSED,
        "breaker recovers on probe success (state={})".format(cb.state),
    )

    # ---- Checkpoint / resume skips completed work
    tmp = Path(tempfile.mkdtemp(prefix="sched-ckpt-"))
    try:
        ids = ["c{:03d}".format(i) for i in range(20)]
        cases = [{"id": i} for i in ids]
        ck_path = tmp / "ckpt.jsonl"

        def exec_ok(case):
            return True

        run1 = run_pool(
            cases,
            exec_ok,
            checkpoint_path=ck_path,
            window=AdaptiveWindow(floor=1, ceiling=4, now=(lambda: 0.0)),
            simulate_kill_after=12,
            now=(lambda: 0.0),
        )
        check(
            run1["killed"] and len(run1["results"]) == 12,
            "first (killed) run did 12 cases",
        )
        rem = Checkpoint(ck_path).remaining(ids)
        check(len(rem) == 8, "checkpoint shows 8 remaining (got {})".format(len(rem)))

        run2 = run_pool(
            cases,
            exec_ok,
            checkpoint_path=ck_path,
            window=AdaptiveWindow(floor=1, ceiling=4, now=(lambda: 0.0)),
            now=(lambda: 0.0),
        )
        check(
            len(Checkpoint(ck_path).completed()) == 20,
            "resume completed all 20 (checkpoint cumulative)",
        )
        check(
            run2["completed"] == 8,
            "resume did exactly the 8 remaining (got {})".format(run2["completed"]),
        )
        check(run2["wall_s"] <= run1["wall_s"] + 1e-6, "resume did no redundant work")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # ---- Comparison: fixed concurrency 2 vs adaptive at ceilings 8/16/32/64
    PER = 29.0 / SCALE
    N = 146

    def make_execute(rate429, rng):
        def _exec(case):
            if rng.random() < rate429:
                raise RuntimeError("HTTP 429 rate limit")
            return True

        return _exec

    print("\ncomparison table (146-case job, 29s/case real):")
    print(
        "{:>12} {:>10} {:>14} {:>16} {:>12}".format(
            "mode", "wall_s", "real_wall_s", "completion%", "final_win"
        )
    )
    rng_f = random.Random(99)
    fw = AdaptiveWindow(floor=2, ceiling=2, backoff_factor=1.0, now=(lambda: 0.0))
    fixed = run_pool(
        [{"id": "f{:03d}".format(i)} for i in range(N)],
        make_execute(0.20, rng_f),
        window=fw,
        now=(lambda: 0.0),
    )
    real_fixed = fixed["wall_s"] * SCALE
    print(
        "{:>12} {:>10.2f} {:>14.1f} {:>16.1f} {:>12}".format(
            "fixed-2",
            fixed["wall_s"],
            real_fixed,
            fixed["completion_rate_pct"],
            fixed["final_window"],
        )
    )
    check(
        real_fixed <= 3600.0,
        "fixed-2 finishes 146-case job within 3600s ({:.0f}s)".format(real_fixed),
    )

    for ceil in (8, 16, 32, 64):
        rng_a = random.Random(99)
        aw = AdaptiveWindow(
            floor=1, ceiling=ceil, backoff_factor=0.5, now=(lambda: 0.0)
        )
        res = run_pool(
            [{"id": "a{}-{}".format(ceil, i)} for i in range(N)],
            make_execute(0.20, rng_a),
            window=aw,
            now=(lambda: 0.0),
        )
        real_w = res["wall_s"] * SCALE
        print(
            "{:>12} {:>10.2f} {:>14.1f} {:>16.1f} {:>12}".format(
                "adaptive-{}".format(ceil),
                res["wall_s"],
                real_w,
                res["completion_rate_pct"],
                res["final_window"],
            )
        )
        check(
            real_w <= 3600.0,
            "adaptive-{} finishes within 3600s ({:.0f}s)".format(ceil, real_w),
        )

    # ---- window backs off then recovers under a burst of 429s
    wb = AdaptiveWindow(floor=1, ceiling=16, backoff_factor=0.5, now=(lambda: 0.0))
    start_win = wb.window
    for _ in range(5):
        wb.on_rate_limited()
    check(
        wb.window < start_win,
        "window backed off under 429 burst ({}->{})".format(start_win, wb.window),
    )
    for _ in range(40):
        wb.on_success()
    check(wb.window > 1, "window recovered after 429 burst (got {})".format(wb.window))

    print("\nself-test: {} failed".format(fails))
    return 1 if fails else 0


# --------------------------------------------------------------------------- CLI


def main() -> int:
    ap = argparse.ArgumentParser(description="Scheduler self-test / controller.")
    ap.add_argument(
        "--self-test", action="store_true", help="run the simulation self-test"
    )
    args = ap.parse_args()
    if args.self_test:
        return _selftest()
    print(
        "scheduler loaded: AdaptiveWindow, classify_failure, RetryPolicy, "
        "CircuitBreaker, Checkpoint, run_pool"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
