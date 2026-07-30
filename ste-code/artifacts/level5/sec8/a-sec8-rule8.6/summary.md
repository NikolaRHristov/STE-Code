# Rule 8.6 — Elements That Count as One Word

## Original Rule Summary

Rule 8.6 specifies that when counting words for sentence length, certain multi-word elements each count as a single word. These elements are numbers, numbers together with units of measurement, abbreviations, alphanumeric identifiers, quoted text, titles and headings, and proper nouns of individuals, groups, organizations, and geopolitical entities. The rule exists because these elements function as single units of meaning even when they contain multiple whitespace-separated tokens. Applying Rule 8.6 reduces the effective word count of technical sentences by 3 to 8 words compared to naive word counting, making it easier to obey the 20-word procedural and 25-word descriptive sentence-length limits in Rule 8.7.

## STE-Code Adaptation

In code documentation, Rule 8.6 applies with the same seven categories but adapted to software contexts: numbers, numbers with units (e.g., `10 ms`, `20 MB`), abbreviations (e.g., `JWT`, `CI/CD`, `VPN`), alphanumeric identifiers (e.g., `E36L7`, commit hashes, semantic version strings), quoted text (e.g., UI labels, code snippets, formulas), titles and UI element labels, and proper nouns (e.g., `GitHub Actions`, `Apache Software Foundation`). Each of these collapses to one word for sentence-length counting. The rule has its largest impact in API documentation and README files, where identifiers, abbreviations, and proper nouns occur at the highest density. Generated documentation, framework names, code keywords, and nested quoted text are all handled under appropriate categories without requiring the author to rewrite them.

## Example Pairs

> **Non-STE:** The endpoint located at the uniform resource locator path of /api/v2/organizations/{organizationId}/repositories/{repositoryId}/branches accepts a Hypertext Transfer Protocol Secure GET request and requires an OAuth two point zero bearer token in the Authorization header with the format Bearer followed by a space and then the access token, and it returns a JavaScript Object Notation response body with a two hundred status code.
>
> **STE:** The `GET /api/v2/orgs/{orgId}/repos/{repoId}/branches` endpoint needs an OAuth 2.0 bearer token in the `Authorization` header. It returns a JSON response body with a 200 status code. (10 words, then 10 words)
>
> *Principles applied: P3 (use words only with approved meanings — "needs" not "requires"), P9 (prefer short, clear technical nouns — "orgId" not "organizationId"). The quoted path counts as 1 word. "OAuth 2.0" is a proper noun (1 word). "Authorization" is quoted text (1 word). "JSON" is an abbreviation (1 word). "200" is a number (1 word).*

> **Non-STE:** In the YAML Ain't Markup Language configuration file located at the path etc/application/configuration/production.yaml, set the property spring.datasource.hikari.maximumPoolSize to a value of fifty and set the property server.tomcat.maxThreads to a value of two hundred, then also make sure that the property logging.level.com.example is set to the value DEBUG and the property management.endpoints.web.exposure.include is set to the value health,info,metrics.
>
> **STE:** In `etc/application/config/production.yaml`, set `spring.datasource.hikari.maximumPoolSize` to 50. Set `server.tomcat.maxThreads` to 200. Set `logging.level.com.example` to `DEBUG`. Set `management.endpoints.web.exposure.include` to `health,info,metrics`. (8 words, 5 words, 6 words, 7 words)
>
> *Principles applied: P9 (prefer short, clear technical nouns — "config" not "configuration"), P12 (technical verbs like "set" are allowed). The file path is quoted text (1 word). Each property name is an alphanumeric identifier (1 word). "50" and "200" are numbers (1 word each).*

> **Non-STE:** Execute the structured query language migration script with the filename V2_3_1__add_user_preferences_table.sql which creates a new relational database table called user_preferences that has a universally unique identifier primary key column, a foreign key column referencing the users table on the id column with a cascade on delete action, and a JavaScript Object Notation Binary column for storing the preference data with a default value of an empty JSON object represented by the characters opening curly brace followed by closing curly brace.
>
> **STE:** Run the migration `V2_3_1__add_user_preferences_table.sql`. It makes the `user_preferences` table with a UUID primary key. The table has a foreign key to `users(id) ON DELETE CASCADE`. It has a JSONB column with the default value `{}`. (9 words, 11 words, 8 words, 10 words)
>
> *Principles applied: P12 (technical verbs like "run" are allowed — "Run" not "Execute"), P1 (use approved words — "makes" not "creates"). "V2_3_1__add_user_preferences_table.sql" is an alphanumeric identifier (1 word). "user_preferences" is quoted text (1 word). "UUID" is an abbreviation (1 word). "JSONB" is an abbreviation (1 word).*

## Principles Applied

P1 — Use approved words from the controlled terminology ("makes" not "creates", "run" not "execute")
P3 — Use approved words only with their approved meanings ("needs" not "requires")
P9 — Prefer short, clear technical nouns ("config" not "configuration", "orgId" not "organizationId")
P12 — Technical verbs are allowed ("set", "run" as code-domain technical verbs)
