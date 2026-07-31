# Feedback: Use poll, not wait

## Date: 2026-07-31

**Issue:** The agent used `process(action='wait')` and `terminal(timeout=...)` which blocks the conversation for up to 60-300 seconds. This freezes the conversation and prevents the user from sending mid-turn messages.

**Solution:** Use `process(action='poll')` for checking background process status. Poll is non-blocking and returns immediately with current status. The user can then decide if they want to keep checking or move on.

**Additional issue:** Terminal commands with `sleep` loops in `timeout` mode also block the conversation. Use short `sleep` loops inside `background=true` processes instead.

**Best practice:**
- Launch long tasks with `terminal(background=true, notify_on_complete=true)`
- Check status with `process(action='poll', session_id=...)`
- Use `notify_on_complete=true` to get automatic completion notification
