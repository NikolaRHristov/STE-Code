#!/usr/bin/env bash
# pre-tool-call-pace-delegate.sh — dispatch rate-limiter / queue for delegate_task.
#
# Problem it solves: firing many `delegate_task` (worker) calls at once makes
# every worker hammer the LLM gateway simultaneously and trip HTTP 429 (rate
# limit), which aborts the batch. There is no built-in RPM limiter in Hermes
# for subagent LLM calls, and `pre_llm_call` can only block (abort) or inject
# context — it cannot delay. So we pace DISPATCH instead: this hook runs before
# every `delegate_task` tool call, checks a sliding-window token bucket, and
# SLEEPS INLINE (acting as a queue) until a dispatch slot is free, then allows.
#
# Hooks live in ~/.hermes/config.yaml and are GLOBAL — this therefore protects
# every profile and every session with no per-profile wiring.
#
# Tuning (constants below):
#   MIN_GAP_SEC      minimum seconds between any two delegate_task dispatches
#   WINDOW_SEC       rolling window length for the per-window cap
#   MAX_PER_WINDOW   max delegate_task calls allowed inside WINDOW_SEC
#   MAX_SLEEP        hard cap on how long this hook will sleep before allowing
#                    (never wedge a dispatch forever; allow after this).
# Set MAX_PER_WINDOW/MIN_GAP conservatively for low-RPM models (e.g. free tiers).

MIN_GAP_SEC=10
WINDOW_SEC=60
MAX_PER_WINDOW=3
MAX_SLEEP=45

STATE_DIR="${HOME}/.hermes/agent-hooks"
STATE_FILE="${STATE_DIR}/dispatch_pace.state"
LOCK_DIR="${STATE_DIR}/dispatch_pace.lock"

# --- read stdin (hook JSON) -------------------------------------------------
INPUT="$(cat)"

# Only pace delegate_task. Everything else proceeds instantly.
TOOL="$(printf '%s' "$INPUT" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('tool_name',''))
except Exception:
    print('')" 2>/dev/null)"

if [ "$TOOL" != "delegate_task" ]; then
  printf '{}'      # not a worker dispatch -> proceed immediately
  exit 0
fi

# --- acquire lock (mkdir is atomic) ----------------------------------------
for _ in $(seq 1 50); do
  if mkdir "$LOCK_DIR" 2>/dev/null; then break; fi
  sleep 0.1
done
cleanup() { rmdir "$LOCK_DIR" 2>/dev/null; }
trap cleanup EXIT

# --- load prior state -------------------------------------------------------
NOW="$(date +%s)"
LAST=0
COUNT=0
if [ -f "$STATE_FILE" ]; then
  # state line: "<last_epoch> <space_separated_list_of_recent_epochs>"
  read -r LAST RECENT < "$STATE_FILE" 2>/dev/null
  [ -z "$LAST" ] && LAST=0
  # count epochs inside the rolling window
  for e in $RECENT; do
    if [ "$((NOW - e))" -lt "$WINDOW_SEC" ]; then
      COUNT=$((COUNT + 1))
    fi
  done
fi

# --- decide how long to wait (queue) ---------------------------------------
SLEEP_FOR=0
GAP_WAIT=$(( MIN_GAP_SEC - (NOW - LAST) ))
if [ "$GAP_WAIT" -gt "$SLEEP_FOR" ]; then SLEEP_FOR=$GAP_WAIT; fi
if [ "$COUNT" -ge "$MAX_PER_WINDOW" ]; then
  # window full: wait until the oldest in-window entry expires
  OLDEST=0
  for e in $RECENT; do
    if [ "$((NOW - e))" -lt "$WINDOW_SEC" ]; then
      if [ "$OLDEST" -eq 0 ] || [ "$e" -lt "$OLDEST" ]; then OLDEST=$e; fi
    fi
  done
  WIN_WAIT=$(( WINDOW_SEC - (NOW - OLDEST) + 1 ))
  if [ "$WIN_WAIT" -gt "$SLEEP_FOR" ]; then SLEEP_FOR=$WIN_WAIT; fi
fi

if [ "$SLEEP_FOR" -gt "$MAX_SLEEP" ]; then SLEEP_FOR=$MAX_SLEEP; fi

if [ "$SLEEP_FOR" -gt 0 ]; then
  sleep "$SLEEP_FOR"
  NOW="$(date +%s)"
fi

# --- record this dispatch & write state ------------------------------------
NEW_RECENT="$NOW"
for e in $RECENT; do
  if [ "$((NOW - e))" -lt "$WINDOW_SEC" ]; then
    NEW_RECENT="$NEW_RECENT $e"
  fi
done
printf '%s %s\n' "$NOW" "$NEW_RECENT" > "$STATE_FILE"

printf '{}'   # allow the dispatch to proceed
exit 0
