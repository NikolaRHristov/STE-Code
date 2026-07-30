# Commit Messages

STE-Code compliant commit messages follow conventional commits format with
approved vocabulary.

**Example:**
```
feat(auth): Add OAuth2 provider configuration

BREAKING: The AuthConfig type replaces the legacy Config type.
Update your imports from 'config' to 'auth-config'.
```

**Rules:**
- Type: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`
- Subject: ≤50 chars, imperative mood, lowercase
- Body: Active voice, no synonyms, one term per concept
- Signal words: `BREAKING:` before destructive changes, `DEPRECATED:` before removals
