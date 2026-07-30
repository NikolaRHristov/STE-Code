# Adding a Locale

1. Add the locale to the discovery grid in `.agents/references/translation-grid.md`
2. Create the directory: `mkdir -p translations/<locale>/{ste-code,SCE,ste-code-v2}`
3. Re-run discovery on the affected targets
4. Update `translations/catalog.md`
5. Commit: `feat(translations): Add <locale> scaffolding`
