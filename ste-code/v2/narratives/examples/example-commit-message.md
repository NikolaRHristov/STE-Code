# Example: STE-Code Compliant Commit Messages

> **Document type:** Commit message  
> **Constraint:** Max 72 chars subject, imperative mood, no jargon

---

## Commit Message Rules (STE-Code)

1. Subject line: imperative mood, max 72 characters.
2. Subject line: use an approved verb from dev-operations or data-operations.
3. Body: max 25 words per sentence.
4. Body: one change per commit message — one term per concept.
5. BREAKING CHANGE: must include version and migration path.

---

## Before / After Examples

### Example 1

```
❌ Before:
added some caching stuff and fixed a weird bug with the auth thing

✅ After:
feat(cache): store session tokens in Redis

Store session tokens in Redis instead of PostgreSQL.
This update reduces authentication latency by 40%.
```

### Example 2

```
❌ Before:
whoops, nuked the old migration, hopefully this fixes it

✅ After:
fix(db): repair User table migration rollback

Repair the rollback path for the User table migration.
The previous migration deleted the index incorrectly.
```

### Example 3 (BREAKING)

```
❌ Before:
changed the API, stuff might break

✅ After:
feat(api)!: update /users endpoint response schema

BREAKING CHANGE (v2.0.0): The /users endpoint now returns
a paginated response object instead of a flat array.

Migration: Update all callers to read response.data instead
of the root array. See docs/migration-v2.md for examples.
```
