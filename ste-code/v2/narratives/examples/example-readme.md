# Example: STE-Code Compliant README

> **Document type:** README  
> **Compliance:** 100% (0 violations)  
> **Principles applied:** P1, P2, P3, P4, P7, P9, P11, P12, P13, P14

---

## Before (Non-Compliant)

````markdown
## Getting Started

First, you gotta grab all the dependencies using npm. Then you can kick off the dev server.
The app talks to a Postgres database and uses Redis to keep sessions alive.
If something goes wrong, check the logs — the system will spit out an error.
⚠️ Make sure you've set up your .env file or things will explode.
````

### Violations Found

| Line | Original | Corrected | Principle |
|------|----------|-----------|-----------|
| 1 | grab | read | P1 — synonym: grab → read |
| 1 | kick off | start | P1 — synonym: kick off → start |
| 2 | talks to | connects to | P1 — synonym: talks to → connect |
| 2 | keep sessions alive | store sessions | P1 — synonym: keep → store |
| 3 | something goes wrong | an error occurs | P1 — unapproved expression |
| 3 | spit out | display | P1 — synonym: spit out → display |
| 4 | explode | fail | P1 — unapproved term |
| 4 | passive: things will explode | the application will fail | P12 — structure |

---

## After (Compliant)

````markdown
## Getting Started

1. Read the dependencies.

   ```bash
   npm install
   ```

2. Start the development server.

   ```bash
   npm run dev
   ```

The application connects to a PostgreSQL database and stores sessions in Redis.

If an error occurs, the application displays an error message in the terminal log.

> **NOTE:** Write all required values to `.env` before you start the application. The application will fail without a correct `.env` file.
````

### What Changed

- `grab` → `read` (synonym table: data-operations)
- `kick off` → `start` (synonym table: development-operations)
- `talks to` → `connects to` (synonym table: communication-operations)
- `keep sessions alive` → `stores sessions in` (synonym table: data-operations)
- `spit out` → `displays` (synonym table: application-operations)
- `explode` → `fail` (unapproved term removed)
- Warning converted to STE-Code NOTE format
- All code blocks now have language identifiers
