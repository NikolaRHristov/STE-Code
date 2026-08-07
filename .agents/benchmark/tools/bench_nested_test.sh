#!/usr/bin/env bash
# bench_nested_test.sh - prove a benchmark-ste-code session can spawn its OWN
# bench worker (recursive containment) and that we can track the process tree.
#
# It does NOT rely on a human-written prompt disclosing the jail. Instead the
# bench session is told a vanilla task that, as part of doing the work, itself
# delegates a sub-task to a fresh bench session (via bench_spawn.sh, which
# force-reconfines it). We capture the PID tree with `pgrep`/`ps` to show the
# parent->child relationship and that both children share the bench policy.
set -u

REPO_ROOT="$(cd "$(dirname "$0")/../../.." && pwd -P)"
SPOOL="$REPO_ROOT/.agents/benchmark/tmp/nested-$(date +%Y%m%dT%H%M%S)"
mkdir -p "$SPOOL"
echo "SPOOL=$SPOOL"

# Vanilla task for the OUTER bench session. It does not mention the jail; it
# just asks the session to run a small job AND to spin up an inner worker that
# does a sub-job, recording each worker's PID to a file we can read back.
OUTER_PROMPT="$SPOOL/outer_prompt.txt"
cat >"$OUTER_PROMPT" <<'EOF'
You are a research assistant. Your ONLY job is to follow these mechanical steps
and write the result to the file given as the final argument. Do not write prose
instead of doing the steps.

STEP 1. Use the terminal tool to run EXACTLY this command (copy verbatim):
    bash .agents/benchmark/tools/bench_spawn.sh inner .agents/benchmark/tmp/inner_prompt.txt inner-run-1 && echo "INNER_PID=$!"
The command launches a helper worker. Capture the "INNER_PID=NNNN" line it
prints and keep that number.

STEP 2. Wait for the worker to finish, then use the read_file tool to read
    .agents/benchmark/tmp/inner_result.txt
and copy its contents.

STEP 3. Use the write_file tool to create the report file (the path given as the
final argument) containing exactly:
    - one sentence summarizing what the STE-Code project is for
    - the INNER_PID you captured in STEP 1
    - the worker's result you read in STEP 2

You MUST actually call the terminal, read_file, and write_file tools. Narrating
that you "would" run the command is not acceptable.
EOF

# Vanilla task for the INNER worker.
INNER_PROMPT="$REPO_ROOT/.agents/benchmark/tmp/inner_prompt.txt"
mkdir -p "$(dirname "$INNER_PROMPT")"
cat >"$INNER_PROMPT" <<'EOF'
You are a counting helper. Read the file you are given as the only argument,
count how many words it contains, and write only the number (and a one-line
note) back to that same file's sibling: .agents/benchmark/tmp/inner_result.txt
Do the work yourself.
EOF

# Launch the OUTER bench session (which will, in turn, launch the INNER one).
OUTER_OUT="$SPOOL/outer_out.txt"
HERMES_HOME=~/.hermes/profiles/benchmark-ste-code \
	STE_CODE_JAIL_POLICY=bench \
	HERMES_PROFILE=benchmark-ste-code \
	hermes -z "$(cat "$OUTER_PROMPT") $OUTER_OUT" --cli --yolo >"$SPOOL/outer.log" 2>&1 &
OUTER_PID=$!
echo "OUTER_PID=$OUTER_PID"

# Track the process tree while it runs. We match on single tokens (the prompt
# contains newlines, so matching the full cmdline splits across lines).
for i in $(seq 1 12); do
	sleep 3
	if ! kill -0 "$OUTER_PID" 2>/dev/null; then break; fi
	{
		echo "=== t=$((i * 3))s ==="
		# every hermes + bench_spawn process with pid/ppid
		ps -ax -o pid,ppid,args 2>/dev/null |
			grep -E "bench_spawn\.sh|inner_prompt|hermes -z" |
			grep -v grep |
			awk '{print "pid=" $1 " ppid=" $2 " " substr($0, index($0,$3))}' |
			cut -c1-120
	} >>"$SPOOL/proctree.log"
done

wait "$OUTER_PID"
echo "OUTER_EXIT=$?"

# Give the inner worker a moment if it was launched late.
sleep 5
echo "=== final proctree snapshot ===" >>"$SPOOL/proctree.log"
ps -ax -o pid,ppid,args 2>/dev/null |
	grep -E "bench_spawn\.sh|inner_prompt|hermes -z" |
	grep -v grep |
	awk '{print "pid=" $1 " ppid=" $2 " " substr($0, index($0,$3))}' |
	cut -c1-120 >>"$SPOOL/proctree.log"

echo "=== outer report ==="
cat "$OUTER_OUT" 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | tr -d '\r'
echo "=== inner result ==="
cat "$REPO_ROOT/.agents/benchmark/tmp/inner_result.txt" 2>/dev/null | sed 's/\x1b\[[0-9;]*m//g' | tr -d '\r'
echo
echo "SPOOL=$SPOOL"
