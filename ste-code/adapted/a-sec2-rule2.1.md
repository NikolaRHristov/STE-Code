# Rule 2.1 — Multi-word Nouns (Maximum Three Words)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.1

## Original Rule

Write multi-word nouns of no more than three words.

In English, you can use one or more words to describe or modify a noun. Technical texts can contain long groups of words that have the function of one part of speech in a sentence. Usually, these groups of words are made of nouns and/or adjectives and are the subject or the object in a sentence. Such groups of words are known as multi-word nouns.

General examples:

- Horizontal cylinder pivot bearing (a multi-word noun of 4 words)
- Stainless steel corrosion protection strips (a multi-word noun of 5 words)
- Actuator operating rod (a multi-word noun of 3 words)

Long multi-word nouns are not easy to understand because the words in the multi-word noun can connect to each other differently. The main noun, or head noun of the group, is usually the last word of the multi-word noun. When the connections between words are not clear, ambiguity occurs. As a result, short multi-word nouns are easier to understand.

- Runway light connection
  *(This example shows a short multi-word noun (3 words). The main noun is "connection.")*

- Runway light connection resistance calibration
  *(This example shows a long multi-word noun (5 words). The main noun is "calibration.")*

The long multi-word noun in the example does not tell the reader the relation between "runway" and "calibration." The reader must understand four modifiers before the main noun "calibration."

Long multi-word nouns can cause problems for non-native English readers because, in some languages, the main noun comes first in the multi-word noun. When a multi-word noun has more words, it is less clear.

To help your reader, keep multi-word nouns to a maximum of three words.

To keep multi-word nouns short, you can use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word nouns.

Examples:

> **Non-STE:** Runway light connection resistance calibration. (5 words)
> **STE:** Calibration of the resistance of the runway light connection.
> *(1 word, 1 word, and 3 words)*

## STE-Code Adaptation

In code documentation, multi-word nouns frequently appear when describing system components, data structures, or configurations. Long chains of nouns and adjectives make documentation hard to parse, especially for non-native English readers.

General examples:

- API gateway request rate limiter (a multi-word noun of 4 words)
- GraphQL query response cache eviction strategy (a multi-word noun of 5 words)
- Database connection pool (a multi-word noun of 3 words)

Keep multi-word nouns to a maximum of three words. When a concept requires more than three words, break the multi-word noun into smaller units connected by prepositions such as "of," "for," "in," and "on." The main noun (head noun) should be the last word of each multi-word noun unit.

- Database connection pool
  *(This example shows a short multi-word noun (3 words). The main noun is "pool.")*

- Database connection pool timeout configuration
  *(This example shows a long multi-word noun (5 words). The main noun is "configuration.")*

The long multi-word noun does not tell the reader the relation between "database" and "configuration." The reader must understand four modifiers before the main noun "configuration."

This rule applies to documentation prose, not to code identifiers (variable names, function names, class names). Code identifiers follow the naming conventions of the programming language and are not multi-word nouns in the STE sense.

### Examples

> **Non-STE:** Database connection pool timeout configuration. (5 words)
> **STE:** Configuration of the timeout of the database connection pool.
> *(1 word, 1 word, and 3 words)*

> *Adapted from spec pair: "Runway light connection resistance calibration" / "Calibration of the resistance of the runway light connection."* Both break a long multi-word noun into smaller units connected by prepositions. The spec multi-word noun "runway light connection resistance calibration" (5 words) becomes three separate multi-word noun units. The code-domain multi-word noun "database connection pool timeout configuration" (5 words) follows the same pattern: "Configuration of the timeout of the database connection pool."
