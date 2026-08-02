# Verify a skill-library reorg

Run from the STE-Code repo root.

## 1. Live skill load (must list every skill under its bucket)
```sh
env -u HERMES_HOME HERMES_PROFILE=dev-ste-code \
  HERMES_HOME=~/.hermes/profiles/dev-ste-code \
  hermes skills list --enabled-only 2>&1 | grep -E "enabled shown|│ [a-z]"
```
Expect: 0 default Hermes skills (no apple/creative/email/media/...), all STE
skills present, each showing its bucket as the Category column.

## 2. No dangling symlinks in the profile
```sh
find -L ~/.hermes/profiles/dev-ste-code/skills -maxdepth 1 -type l \
  ! -exec test -e {} \; -print
```
Expect: no output.

## 3. Old flat dirs gone
```sh
ls -d .agents/skills/adaptation .agents/skills/github .agents/skills/validation 2>&1
```
Expect: "No such file or directory" for each (they were folded into buckets).

## 4. Instruction-content preservation (0 missing lines)
For each moved skill, sample content lines from the SOURCE and confirm they are
substrings of the NEW file. Manual check:
```sh
grep -c "DISTINCTIVE_COMMAND_OR_SENTENCE" \
  .agents/skills/ste-code-authoring/<skill>/SKILL.md
```
Or read both files side by side with `read_file` and confirm the procedural
body is identical. A non-empty diff in the body (not the frontmatter) means
content was lost — restore from `/tmp/ste-skills-backup`.

## 5. Repo integrity
```sh
make check
```
Expect: 178/178, all policies passed.
