# Poll, do not wait

A convention for every agent that launches long work in this project.

## Rule

Launch long tasks in the background and **poll** them. Never block the
conversation on a task you cannot interrupt.

| Do                                                   | Do not                                |
| ---------------------------------------------------- | ------------------------------------- |
| `terminal(background=True, notify_on_complete=True)` | `terminal(timeout=600)` on a long run |
| `process(action='poll')`                             | `process(action='wait')`              |
| a `sleep` loop **inside** a background process       | a `sleep` loop in the foreground      |

## Why

A blocking call freezes the session for as long as the task runs. The operator
cannot steer, correct a wrong parameter, or stop a bad run — the message they
send arrives only after the block ends, which is usually after the damage.

Polling returns immediately with the current status. The operator keeps control,
and the agent does other useful work between polls.

## Pattern

```python
# launch
terminal(command="python3 .agents/tools/<stage>/<stage>_batch.py 1",
         background=True, notify_on_complete=True)

# check — returns at once, no matter how long the task runs
process(action="poll", session_id="<id>")
```

Concurrency is capped: run at most **two** agent-backed workers at a time. Above
that the provider rate-limits and the failure rate rises faster than the
throughput gain.
