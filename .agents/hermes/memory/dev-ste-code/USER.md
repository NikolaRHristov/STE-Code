§ User manages the `<github-org>` GitHub org (family of repos: <repo-a>,
<repo-b>, <repo-c>, <repo-d>). Maintains a strict separation: the STE-Code repo
is the single source for skills + persistent memory, tracked via relative
symlinks into per-profile live dirs (skills two-level, memory one-level).
Prefers declarative, anonymized memory (placeholders like
`<person>`/`<github-org>`, no quoted directives). Wants profile config to
disable ALL non-STE bundled skills so only `ste-code-*` run. Expects
delegated/poll-worker work to be verified on disk, not trusted from
self-reports. § § Parallel/background work: DEFAULT to poll workers over
delegate_task; KEEP delegate_task for quick small tasks. Poll worker =
background terminal proc launching a Hermes oneshot FROM A PROMPT FILE,
preferring `install.sh`/`link-*.sh` style idempotent scripts. Delegate =
produce/write output; poll worker = research/observe. Never trust delegate
self-reports — verify deliverables on disk. (Note: raw `hermes -z` is
--oneshot + YOLO auto-approve, NOT stricter than delegate_task; make poll
workers strict via minimal --toolsets / confined profile.) § § Engineering-style
preferences (from STE-Code dev-authoring sessions): Prefers PYTHON hooks over
bash for capability ("use python for the hooks, to make them more advanced").
Insists on SINGLE RESPONSIBILITY for hooks — one job each (the memory hook must
anonymise ONLY; the earlier LLM-restructure that spawned `hermes -z` oneshots
and caused 84-message runaway sessions violated SRP and was removed). Wants
LLM-powered features but with NO session clutter ("session db none") — achieve
via `HERMES_HOME=<temp>` so child sessions write to a throwaway state.db, not
the real store. Benchmark skills must be GOAL-FOCUSED and ENVIRONMENT-AGNOSTIC:
they say what + how, never leak jail/policy internals (the jail is STE-Code's
concern, enforced by harness/plugins). Memory ops fire-and-forget — never long
logged oneshot sessions.
