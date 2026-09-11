#!/usr/bin/env bash
# pre-api-request-pace.sh — per-API-call rate gate for Hermes LLM requests.
#
# Fires on the `pre_api_request` hook event, which Hermes invokes BEFORE every
# provider API call (parent turns, delegated/worker LLM calls, AND retries).
# The hook subprocess is awaited, so sleeping here DELAYS the real request —
# turning this script into a sliding-window queue that prevents the whole
# process (and its workers) from hammering a low-RPM provider (e.g. a free
# tencent/hy3:free tier) and tripping HTTP 429 / "can't reach the model".
#
# This is the per-call companion to pre-tool-call-pace-delegate.sh (which paces
# the delegate_task FAN-OUT). Together they bound both axes of rate pressure.
#
# Shared state file (machine-wide) — multiple concurrent Hermes sessions thus
# honour ONE global rate budget, which is exactly what you want across sessions.
#
# Tuning (constants below):
#   MIN_GAP_SEC      min seconds between ANY two API requests
#   WINDOW_SEC       rolling window for the per-window cap
#   MAX_PER_WINDOW   max API requests allowed inside WINDOW_SEC
#   MAX_SLEEP        hard ceiling on a single hook's wait (never wedge a call)
#   PROVIDER_OK      only pace this provider(s); skip others (regex on provider)
#
# For a low-RPM free model, widen the gap / lower the window cap. Start:
#   MIN_GAP_SEC=4, MAX_PER_WINDOW=5  (gentle)
# For very strict tiers try:
#   MIN_GAP_SEC=8, MAX_PER_WINDOW=2

MIN_GAP_SEC=4
WINDOW_SEC=60
MAX_PER_WINDOW=5
MAX_SLEEP=40
# Comma-separated provider regexes to pace; empty = pace all.
PROVIDER_OK=""

# --- read stdin hook JSON --------------------------------------------------
INPUT="$(cat)"

PROVIDER="$(printf '%s' "$INPUT" | python3 -c "import sys,json
try:
    d=json.load(sys.stdin)
    print(d.get('provider',''))
except Exception:
    print('')" 2>/dev/null)"

if [ -n "$PROVIDER_OK" ]; then
  if ! printf '%s' "$PROVIDER" | grep -qiE "($PROVIDER_OK)"; then
    printf '{}'   # not a provider we pace -> proceed immediately
    exit 0
  fi
fi

STATE_DIR="${HOME}/.hermes/agent-hooks"
STATE_FILE="${STATE_DIR}/api_pace.state"
LOCK_DIR="${STATE_DIR}/api_pace.lock"

# --- acquire lock (mkdir is atomic) ----------------------------------------
for _ in $(seq 1 50); do
  if mkdir "$LOCK_DIR" 2>/dev/null; then break; fi
  sleep 0.1
done
cleanup() { rmdir "$LOCK_DIR" 2>/dev/null; }
trap cleanup EXIT

# --- load prior state ------------------------------------------------------
NOW="$(date +%s)"
LAST=0
COUNT=0
RECENT=""
if [ -f "$STATE_FILE" ]; then
  read -r LAST RECENT < "$STATE_FILE" 2>/dev/null
  [ -z "$LAST" ] && LAST=0
  for e in $RECENT; do
    if [ "$((NOW - e))" -lt "$WINDOW_SEC" ]; then
      COUNT=$((COUNT + 1))
    fi
  done
fi

# --- decide wait (queue) ----------------------------------------------------
SLEEP_FOR=0
GAP_WAIT=$(( MIN_GAP_SEC - (NOW - LAST) ))
if [ "$GAP_WAIT" -gt "$SLEEP_FOR" ]; then SLEEP_FOR=$GAP_WAIT; fi
if [ "$COUNT" -ge "$MAX_PER_WINDOW" ]; then
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

# --- record this request & write state -------------------------------------
NEW_RECENT="$NOW"
for e in $RECENT; do
  if [ "$((NOW - e))" -lt "$WINDOW_SEC" ]; then
    NEW_RECENT="$NEW_RECENT $e"
  fi
done
printf '%s %s\n' "$NOW" "$NEW_RECENT" > "$STATE_FILE"

printf '{}'   # allow the request to proceed
exit 0
