/** @type {import('prettier').Config} */
export default {
  // ----------------------------------------------------------------------
  // Core formatting options — lifted from CodeEditorLand/Land/prettier.config.js
  // (markdown-relevant subset). Repo root carries NO prettier config; this
  // file is always supplied explicitly via `prettier --config`.
  // ----------------------------------------------------------------------
  printWidth: 80,
  useTabs: true,
  tabWidth: 4,
  trailingComma: "all",
  endOfLine: "lf",
  // Wrap markdown prose at the print width — gives docs / release notes
  // their consistent, scannable line rhythm.
  proseWrap: "always",
  overrides: [
    { files: "*.md", options: { parser: "markdown" } },
    { files: "*.{yaml,yml}", options: { parser: "yaml" } },
    {
      files: "*.json",
      excludeFiles: ["package.json"],
      options: { parser: "json", trailingComma: "none" },
    },
    {
      files: "package.json",
      options: { parser: "json-stringify", trailingComma: "none" },
    },
  ],
};
