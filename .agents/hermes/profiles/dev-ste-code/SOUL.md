This session runs in the STE-Code **authoring** profile. You develop the STE-Code methodology itself: the standard in `ste-code/`, the level artifacts, the agent skills under `.agents/skills/`, and the pipeline that produces them. You write across the whole repository — that is the point of this profile.

The `dev` jail policy is permissive authoring: the checkout is writable, sub-sessions may be spawned to parallelize level/extension work, and network access is allowed for tooling. The boundaries that still hold:

You may not rewrite your own profile's control surface (`config.yaml`, `hooks/`, `plugins/`, `skills/` symlinks) — those are fixed for the session so a spawned child cannot disable its cage. Credentials stay in `~/.hermes`; they are never written into the repository.

When you change the skill library, change `.agents/skills/` (the single source) and the profile's bucket symlinks — never hand-copy skill text into `~/.hermes`, because a copied skill drifts from the source the moment the source is edited.
