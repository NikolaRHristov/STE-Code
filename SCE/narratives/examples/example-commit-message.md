---
id: example-commit-message
version: 1.0.0
document-type: commit-message
rules-demonstrated: [P1, P4, P11, P13, P14]
---

# STE-Code Example — Commit Message

## Non-STE (Violations)

```
fixed the broken auth thing and also did some changes to make the login flow
work better when the user's session gets killed by the server
```

**Violations:**
- `fixed` → use `repair` (P1 — synonym table)
- `broken auth thing` → use the exact component name (P11 — one term per concept)
- `did some changes` → use `update` (P1 — synonym table)
- `gets killed` → passive voice in procedure (P4)
- Two actions in one sentence (rule-4.1)

## STE-Code Compliant

```
repair(AuthService): Repair session timeout — stop invalidating tokens on server restart

The AuthService deleted active tokens when the server restarted.
This caused users to log in again after each deployment.
Update the token store to persist tokens across restarts.
```

**Compliance:** 0 violations. Uses `repair`, `stop`, `update`, `delete` from approved verb list. One action per sentence. Active voice. American English spelling.
