import sys
from pathlib import Path

_HERE = Path(__file__).resolve()
_R = next(
    p for p in _HERE.parents if (p / ".git").is_dir() or (p / "Makefile").is_file()
)
sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))

import ste_cli, ste_time, ste_retry

fail = 0


def check(ok, label):
    global fail
    print(f"  [{'ok' if ok else 'FAIL'}]   {label}")
    if not ok:
        fail += 1


print("ste_cli / ste_time / ste_retry")
# ste_time
check(ste_time.run_stamp()[:8].isdigit(), "run_stamp returns YYYYMMDD prefix")
check(ste_time.now_iso().startswith("20"), "now_iso returns ISO timestamp")
# ste_retry
calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ValueError("x")
    return "done"


check(
    ste_retry.retry(flaky, retries=3, backoff_s=0) == "done",
    "retry succeeds on 3rd attempt",
)
check(calls["n"] == 3, "retry made exactly 3 attempts")


def always_fail():
    raise RuntimeError("nope")


try:
    ste_retry.retry(always_fail, retries=2, backoff_s=0)
    check(False, "retry re-raises after exhaustion")
except RuntimeError:
    check(True, "retry re-raises after exhaustion")
print(f"\nRESULT: {'all checks passed' if not fail else f'{fail} failure(s)'}")
sys.exit(1 if fail else 0)
