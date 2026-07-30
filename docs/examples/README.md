# STE-Code Examples

## Before/After — Code Documentation

### Docstring

**Non-STE:**
```python
def process_data(input_list, config_dict):
    """
    This function will take the input list and process it by going through
    each element and applying the transformation that's specified in the
    config dictionary, and then it'll return the processed list.
    """
```

**STE:**
```python
def process_data(items, config):
    """
    Transform each item in the list using the configuration.

    Args:
        items: The list of input items.
        config: The transformation configuration.

    Returns:
        The transformed list.
    """
```

### Commit Message

**Non-STE:**
```
fixed the bug where the thing was broken and some other stuff too
```

**STE:**
```
fix: Correct null pointer in UserService.getProfile()

The method returned null when the user had no profile record.
Add a null check and return an empty Profile object.
```

### Error Message

**Non-STE:**
```
Error: Something went wrong while trying to connect to the database.
Please try again later or contact support.
```

**STE:**
```
Error: Cannot connect to the database at localhost:5432.

Cause: Connection refused. The database service is not running.
Action: Start the database service. Run: systemctl start postgresql
```

### API Documentation

**Non-STE:**
```
GET /api/users/{id} — This endpoint is used to retrieve a user by
their unique identifier. It will return a JSON object containing all
of the user's information.
```

**STE:**
```
GET /api/users/{id}

Get a user by ID.

Path parameters:
  id (string, required) — The user ID.

Response (200):
  {
    "id": "string",
    "name": "string",
    "email": "string",
    "created_at": "ISO 8601 timestamp"
  }
```

## System Prompt Usage

Add to your LLM system prompt:

```
You are a coding agent. Your documentation follows STE-Code (Simplified
Technical English for Code):

- Use approved words. Prefer "use" over "utilize", "get" over "retrieve".
- Active voice. Imperative mood for instructions.
- One term per concept. No synonym drift.
- 20 words max per procedural sentence.
- No slang, jargon, or contractions.
- Technical code nouns (React, Docker, async/await) are allowed as-is.

Before responding, self-audit your documentation against these rules.
```

Full system prompt: `ste-code/artifacts/ste-code-distilled-system-prompt.txt`
