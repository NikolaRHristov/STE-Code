/** @type {import('prettier').Config} */
export default {
	// =========================================================================
	// STE-Code formatter configuration.
	//
	// Lifted from <repo>/Land/prettier.config.js and reduced to the
	// languages that actually exist in this repository. The STE-Code repo root
	// deliberately carries NO package.json and NO prettier config: this file is
	// always supplied explicitly with `prettier --config`, and every path in
	// .prettierignore is anchored to .agents/format/.
	//
	// Verified inventory (find over ste-code/ + .agents/, excl. node_modules):
	//   .md 778   .json 105   .py 136   .yaml 18   .sh 10   .toml 1   .js 1
	//   no .ts/.tsx/.css/.scss/.html/.vue/.rs/.jsonc  -> no plugins required.
	//   The single .toml (tools/linkcheck/lychee.toml) has no first-party
	//   prettier parser; a plugin is not worth one file, so it stays untouched.
	// =========================================================================

	// =========================================================================
	// Core Formatting Options
	// =========================================================================
	// Max line length before wrapping. 80 is standard for readability.
	printWidth: 80,

	// Use tabs for indentation (accessibility friendly).
	useTabs: true,

	// Number of spaces per tab (visual width).
	tabWidth: 4,

	// Always use semicolons at end of statements.
	semi: true,

	// Use double quotes instead of single quotes.
	singleQuote: false,

	// Trailing commas wherever valid. Helps git diffs.
	trailingComma: "all",

	// Print spaces between brackets in object literals. { foo: bar }
	bracketSpacing: true,

	// Put > on the same line as the last attribute in HTML/JSX.
	bracketSameLine: true,

	// Always include parens for arrow functions. (x) => x
	arrowParens: "always",

	// Quote properties in objects only when they were already quoted.
	quoteProps: "preserve",

	// Line endings: Linux/macOS style (LF). Pairs with the dos2unix stage.
	endOfLine: "lf",

	// Wrap markdown prose at the print width — this is what gives docs and
	// release notes their consistent, scannable line rhythm, and it is the
	// whitespace half of the STE-Code visual standard that Markdown.py audits.
	proseWrap: "always",

	// =========================================================================
	// Embedded / HTML Specifics
	// =========================================================================
	// CSS-style whitespace handling in HTML (respects display: inline).
	htmlWhitespaceSensitivity: "css",

	// Format fenced code blocks inside Markdown when the language is known.
	embeddedLanguageFormatting: "auto",

	// =========================================================================
	// Per-language Overrides
	// =========================================================================
	overrides: [
		{
			files: ["*.md", "*.markdown"],
			options: { parser: "markdown", proseWrap: "always" },
		},
		{
			files: "*.{yaml,yml}",
			// YAML is space-indented by contract (.editorconfig agrees);
			// tabs are illegal in YAML indentation.
			options: { parser: "yaml", useTabs: false, tabWidth: 2 },
		},
		{
			files: "*.json",
			excludeFiles: ["package.json", "package-lock.json"],
			options: { parser: "json", trailingComma: "none" },
		},
		{
			files: "*.jsonc",
			options: { parser: "jsonc", trailingComma: "none" },
		},
		{
			files: ["package.json", "package-lock.json"],
			// json-stringify keeps npm/pnpm's own canonical shape.
			options: { parser: "json-stringify", trailingComma: "none" },
		},
		{
			// Prettier's markdown parser also owns fenced-block reflow; keep
			// generated system prompts byte-stable by never inferring a parser
			// for plain text.
			files: "*.txt",
			options: { parser: undefined },
		},
	],
};
