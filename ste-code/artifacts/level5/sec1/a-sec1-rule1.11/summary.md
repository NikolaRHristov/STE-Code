# Rule 1.11 — Do Not Use Different Technical Nouns for the Same Item

## Original Rule Summary

Do not use different technical nouns for the same item. When you select a technical noun, use it consistently throughout your text. Changing the name of the same item in different sections causes confusion because the reader must determine whether you refer to the same item or to a different item. Always use the single approved technical noun for each item.

## STE-Code Adaptation

Do not use different code-domain technical nouns for the same item. When you select a code-domain technical noun for a class, endpoint, module, parameter, or any other software component, use that same noun consistently throughout your documentation. Code projects accumulate names from many sources — class names, route patterns, file paths, configuration keys, database tables, and colloquial developer terms. Mixing these names forces the reader to decide whether each name refers to the same item or to different items. Use the canonical name from the most authoritative source (source code, API spec, project glossary) and apply it everywhere.

## Examples

> **Non-STE:**
> 1. Initialize the UserService class.
> 2. Call the authenticate method on the AccountManager.
> 3. The UserHandler returns a session token.
>
> **STE:**
> 1. Initialize the UserService class.
> 2. Call the authenticate method on the UserService.
> 3. The UserService returns a session token.

> *Principle: P11. "UserService," "AccountManager," and "UserHandler" are three different code-domain technical nouns that refer to the same class. The reader cannot know whether these are three separate components or one component with multiple aliases. The STE version uses "UserService" consistently in all three sentences. The source of truth is the class name in the source code.*

> **Non-STE:**
> 1. Send a request to the /api/login path.
> 2. The authentication route returns a JSON Web Token.
> 3. Include the token from the login endpoint in subsequent requests.
>
> **STE:**
> 1. Send a request to the /api/login endpoint.
> 2. The /api/login endpoint returns a JSON Web Token.
> 3. Include the token from the /api/login endpoint in subsequent requests.

> *Principle: P11. "/api/login path," "authentication route," and "login endpoint" are three different names for the same API endpoint. The reader must determine whether these refer to the same URL or to three separate routes. The STE version uses the canonical term "/api/login endpoint" consistently. The URL path defined in the route handler or API specification is the authoritative name.*

> **Non-STE:**
> 1. Query the users_db collection to find the account document.
> 2. The member record contains the email field.
> 3. Update the last_login column in the person table.
>
> **STE:**
> 1. Query the users table to find the user record.
> 2. The user record contains the email field.
> 3. Update the last_login column in the users table.

> *Principles: P8, P11. "users_db collection," "member record," and "person table" are three inconsistent names for the same database entity. "Account document" and "member record" also refer to the same row concept. The STE version uses "users table" (matching the schema definition) and "user record" consistently. The canonical name comes from the database schema, which is the most authoritative source under P8.*

## Principles Applied

- **P8:** Use standard, well-known technical nouns from the most authoritative source (the class name in source code, the URL path in the route definition, the table name in the database schema)
- **P11:** One term per concept — use the same code-domain technical noun for the same item throughout the entire document
