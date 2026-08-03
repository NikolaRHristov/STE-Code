# Hook examples (shipped in .agents/hermes/hooks/)

## post-memory-anonymise.py (post_tool_call, matcher: memory)

Single responsibility: ANONYMISE memory writes. Never restructure (the old
restructure subprocess was the runaway-session bug).

Two layers:

1. **Regex scrub (synchronous, guaranteed, no subprocess):** rewrites the store
   file (`MEMORY.md`/`USER.md`) in-process, replacing `/Users/<name>` →
   `<user-home>`, repo paths → `<repo>`, emails → `<email>`, IPs → `<ip>`, hosts
   → `<host>`, and Title-Case "Firstname Lastname" → `<person>` (no literal
   operator name committed to the repo; `HERMES_OPERATOR_NAMES` env handles the
   exact name). This runs on EVERY memory write — no PII hits disk.
2. **LLM refine (async, detached, best-effort):** spawns `hermes -z` with
   `HERMES_HOME=<temp>` (session → throwaway state.db = "session db none"),
   `--provider nous -m tencent/hy3:free` (NO base_url), `-t ''` (no tools, can't
   loop on jail), `HERMES_ACCEPT_HOOKS=0`. Debounced via a lock file + content
   hash; on ANY error the regex result stands. The child returns scrubbed
   markdown; the hook writes it back itself.

Why `post_tool_call` and not `pre_tool_call`: Hermes short-circuits
`_AGENT_LOOP_TOOLS` (memory, todo, session_search, delegate_task) in
`model_tools.py` BEFORE `pre_tool_call` dispatch, so a `pre_tool_call` matcher
`memory` never fires. `post_tool_call` fires via `_finish_agent_tool`.

## pre-tool-call-scrub-commands.py (pre_tool_call, matcher: terminal)

Pipeline: BREAK DOWN (split chained `&&`/`;`/`||`/`|`/newline into sub-commands,
quotes respected) → DROP NOISE (lone `echo`/`printf`/`sleep`/`clear`/etc. that
only print) → SCRUB PII (reuses the anonymiser regex) → JAIL-CHECK each
sub-command against dev write_roots/deny_roots (imports
`.agents/hermes/jail/ core/policy.py`, fallback set), dropping any that would
write outside the allowed roots → REASSEMBLE surviving parts and return
`{"action":"modify","args":{"command": <cleaned>}}`.

The jail check IS "instantiating the jail at this level" — the command is
pre-filtered so it cannot break the confinement before it ever runs.

Optional LLM "1-or-0" essential-classifier via `HERMES_SCRUB_LLM=1` (nous, no
base_url, detached) — OFF by default so the hook is deterministic and fast.

## Verified gotcha

A `threading.Thread(daemon=True)` spawned inside the hook is KILLED when the
short-lived hook process exits (~1s), before a ~10s LLM call finishes. Launch
the LLM pass as a DETACHED child
(`subprocess.Popen([..., "--llm-refine", str(store)], start_new_session=True)`)
that runs a synchronous worker mode in the child. That survives the parent exit.
