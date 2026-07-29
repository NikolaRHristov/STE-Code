# Rule 2.1 — Multi-word Nouns (Maximum Three Words)

> **Source:** Adapted from ASD-STE100 Issue 9, Rule 2.1

## Original Rule

Write multi-word nouns of no more than three words.

In English, you can use one or more words to describe or modify a noun. Technical texts can contain long groups of words that have the function of one part of speech in a sentence. Usually, these groups of words are made of nouns and/or adjectives and are the subject or the object in a sentence. Such groups of words are known as multi-word nouns.

Long multi-word nouns are not easy to understand because the words in the multi-word noun can connect to each other differently. The main noun, or head noun of the group, is usually the last word of the multi-word noun. When the connections between words are not clear, ambiguity occurs. As a result, short multi-word nouns are easier to understand.

To help your reader, keep multi-word nouns to a maximum of three words.

To keep multi-word nouns short, you can use prepositions (for example, "of," "on," "in," and "for") and explain the multi-word nouns.

## STE-Code Adaptation

In code documentation, multi-word nouns frequently appear when describing system components, data structures, or configurations. Long chains of nouns and adjectives make documentation hard to parse, especially for non-native English readers.

Keep multi-word nouns to a maximum of three words. When a concept requires more than three words, break the multi-word noun into smaller units connected by prepositions such as "of," "for," "in," and "on." The main noun (head noun) should be the last word of each multi-word noun unit.

This rule applies to documentation prose, not to code identifiers (variable names, function names, class names). Code identifiers follow the naming conventions of the programming language and are not multi-word nouns in the STE sense.

### Examples

> **Non-STE:** The database connection pool configuration parameter validation fails when the timeout value is too low. (6 words in the multi-word noun)
> **STE:** The validation of the configuration parameters of the database connection pool fails when the timeout value is too low. (1 word, 2 words, and 3 words)

> **Non-STE:** Update the API response header compression threshold setting in the configuration file. (7 words in the multi-word noun)
> **STE:** In the configuration file, update the threshold setting for the compression of the API response headers. (2 words, 1 word, and 3 words)

> **Non-STE:** The user interface component rendering performance metric report shows a regression since the last release. (7 words in the multi-word noun)
> **STE:** The metric report for the rendering performance of the user interface components shows a regression since the last release. (2 words, 2 words, and 3 words)
