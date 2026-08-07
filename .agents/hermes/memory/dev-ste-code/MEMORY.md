§ Benchmark jail-layer mismatch (verified from source + empirically inside the
bench jail): harness is green (181/181 with
`PYTHONPYCACHEPREFIX=<tmp>/ste-bench-pycache`); the bench run failed ONLY
because the kernel (Seatbelt) jail layer allows only `.agents/benchmark/tests`
while the plugin layer allows the whole tree, so `py_compile` cache writes are
denied. Fix = run with `PYTHONPYCACHEPREFIX=<tmp>/ste-bench-pycache` (proven
green) or widen `jail-lib.sh` bench root. Re-run via
`bash .agents/benchmark/run_bench.sh --base <abs-or-default> --skip-live`.
Harness quirk: `--base` is relative to `tests/`, so use absolute or default. See
`.agents/benchmark/HANDOFF-bench-jail-mismatch.md` and
`RECONCILE-jail-verified.md`. § § selftest.py `FAIL compiles` under bench jail -
FIXED (2026-08-03): `test_modules_compile()` now compiles in-process to a
`cfile` under `$PYTHONPYCACHEPREFIX`/`<tmp>` (no cwd/project-write dependency).
`selftest.py` passes 180/180 UNDER the bench jail AND under dev. A new
"anonymous" profile would NOT fix it (policy.py `_STRICT_FALLBACK="bench"` →
unmapped names fall through to strictest). See HANDOFF-dev-lockdown-status.md
tail. § § ROOT-CAUSE FIX (2026-08-03): `policy.py` resolved `project_root` from
`os.getcwd()`, so a `hermes -z`/delegated CHILD spawned with
`cwd=<user-home>/.hermes` (or <user-home>) found no `.git` marker →
`project_root=None` → the real STE-Code repo was DROPPED from every policy's
write roots → child sessions "couldn't locate anything" (same root cause as the
84-message runaway memory sessions). Fixed by adding
`resolve_project_root_anchored()` (anchors to `policy.py`'s own location →
`<repo>`) and using it first in `build_context` (cwd-walk is now only a
fallback). Repo now resolves regardless of child cwd. Verified: dev & bench
write_roots contain the repo even under `cwd=<user-home>/.hermes`. § §
Memory-anonymise hook (WORKING, LLM-powered, no session clutter):
`post_tool_call` matcher `memory` (Hermes short-circuits `pre_tool_call` for
`_AGENT_LOOP_TOOLS` incl. memory, so `pre_tool_call` never fires for it).
Synchronous regex scrub (guaranteed, no PII on disk) + best-effort async LLM
refine. LLM refine runs `hermes -z` with `HERMES_HOME=<tmp>` (session written to
throwaway state.db → real store stays clean = "session db none") +
`--provider nous -m tencent/hy3:free` (NO base_url) + `-t ''` (no tools, can't
loop on jail) + `HERMES_ACCEPT_HOOKS=0`, debounced via lock+hash, falls back to
regex on any error. Source `.agents/hermes/hooks/post-memory-anonymise.py`. § §
Command-scrub `pre_tool_call` hook (WORKING): matcher `terminal` - splits
chained commands, drops descriptive `echo`/no-op noise, scrubs PII from commands
(reuses anonymiser regex), and jail-checks each sub-command against dev
write_roots/deny_roots (imports `.agents/hermes/jail/core/policy.py`, fallback
set) dropping any that would break the jail; returns `modify` with only the
essential+non-jail-breaking parts. Optional LLM 1-or-0 classifier via
`HERMES_SCRUB_LLM=1` (nous, no base_url, detached). Source
`.agents/hermes/hooks/pre-tool-call-scrub-commands.py`. § § `skill_manage`
resolver cannot locate symlinked STE-Code skills (frontmatter `source:` stale
`ste-code/` vs live `ste-code-benchmark/`). Work around by editing the SKILL.md
at the symlink source directly with `patch`/`write_file`. § § Operator-name
scrubbing needs `HERMES_OPERATOR_NAMES` in `<user-home>/.hermes/.env` (dev jail
blocks writing it; the heuristic Title-Case person-name pattern also fires).
Hook registration (both hooks) requires a SESSION RESTART to take effect. § Dev
jail (dev-ste-code profile) write roots: repo,
<user-home>/.hermes/profiles/dev-ste-code, <user-home>/.hermes/profiles, <tmp>,
<tmp>. Terminal WRITES to <user-home>/.hermes/* (config.yaml at top level,
agent-hooks/, .env, shell-hooks-allowlist.json, auth.json) are REFUSED. Profile
config is edited via <user-home>/.hermes/profiles/<p>/config.yaml (writable
root, symlinks to repo .agents/hermes/profiles/<p>/config.yaml). Allowlist/.env
edits need the user. Hook SOURCE files live in .agents/hermes/hooks/ (writable);
link via link-hooks.sh. Verify a memory/PII hook with a LIVE
`hermes -z -p dev-ste-code` session, not just `echo | python3` - pre_tool_call
never fires for memory (it's an _AGENT_LOOP_TOOL), so stdin-only tests miss the
dispatch gap. § § SKILL-LIBRARY DEBT (skill_manage name-resolution is broken in
the dev-ste-code profile across multiple sessions: `skill_view(name)` resolves
fine, but `patch`/`edit`/`write_file` return "Skill '<name>' not found in active
profile" for EVERY existing skill, bare or category-qualified. Only
`action='create'` resolves names. Consequence: new skills can be created but NOT
given references/ or scripts/ support files, and existing skills cannot be
amended. Workaround used: fold the detail into SKILL.md body at create time, and
inline any probe script as a copy-pasteable code block instead of scripts/.
RESOLVED (2026-08-03): (1)+(2) `agent-session-triage` dangling pointer fixed -
`references/project-root-resolution.md` created under `ste-code-jail-ops`,
worked case split to
`agent-session-triage/references/jail-project-root-case.md` +
`scripts/show_jail_context.py` (read-only jail-context probe). (3) jailed
poll-worker launch recipe (base64 prompt; flags BEFORE -z; HERMES_HOME prefix on
jail-exec.sh) added to `poll-worker-launch`. (4) project_root anchoring +
HERMES_HOME-prefix facts added to `ste-code-jail-ops` SKILL.md.
§
§ Output-write hygiene (STE-Code `.agents/tools`): the gated single funnel is `.agents/tools/lib/ste_io.py`. New/wrapped writes MUST go through `ste_io.write_text/write_json/mkdir`; raw `open("w")`/`Path.write_text`/`json.dump(open())` raise `FileNotFoundError` when the parent dir is missing. Added `ensure_parent_dir(path)` (confined, creates the parent tree only, returns resolved target) + `write_text(..., make_parents=True)` to close the "no directories existed" gap. Audit methodology when asked to guarantee-parent-dirs across many sites: do NOT scatter `mkdir`s — inventory every write site (RAW-vs-ste_io × guarded-vs-unguarded × test-vs-production), table it, filter docstring/`sys.stdout.write` noise, then make ONE helper / route through ste_io. Verified: production raw writes were already upstream-guarded, so the fix was one helper, not 44. Empty-checkout test: target a tree inside the repo that does not exist; `ensure_parent_dir` creates it; chain raw write; assert success; also assert a `<tmp>` escape raises `ste_io.GateError`. § § `skill_manage` resolver defect (dev-ste-code profile): `patch`/`edit` on EXISTING skills returns "not found" even though `skills_list` shows them. Workaround that works: edit the SKILL.md at its source with `patch`/`write_file` file tools (the resolver only breaks inside `skill_manage`). In a review/foreground context where file tools are also denied, you cannot patch via `skill_manage`; fall back to memory + recommend `hermes curator adopt` or a resolver fix. This blocks updating `ste-code-repo-hygiene` (where output-write hygiene §9 belongs) — pending resolver repair.