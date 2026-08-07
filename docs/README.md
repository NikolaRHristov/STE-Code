# docs/ — the STE-Code documentation site 📚

This directory holds the MkDocs sources for the site that GitHub Pages
publishes. It is documentation only: the pipeline reads nothing here.

The entry point is [`index.md`](index.md).

## Layout 🗂️

**`Tree`**

```text
mkdocs.yml              ← site config (repository ROOT, not this directory)
docs/
├── README.md           This file (excluded from the built site)
├── index.md            Home: what STE-Code is, and the level table
├── pipeline.md         The five stages that build the standard
├── contributing.md     Local pipeline run and contribution rules
└── roadmap/
    └── ROADMAP.md      Planned work on the linguistic layer
```

| File                 | Contents                                                     |
| -------------------- | ------------------------------------------------------------ |
| `index.md`           | Home: what STE-Code is, and the level table                  |
| `pipeline.md`        | The five stages that build the standard                      |
| `contributing.md`    | Local run instructions; points to the root `CONTRIBUTING.md` |
| `roadmap/ROADMAP.md` | Planned work on the linguistic layer                         |

`README.md` is excluded from the built site by the `exclude_docs` setting.

### Why `mkdocs.yml` is in the repository root ❓

MkDocs refuses a configuration file whose `docs_dir` is the directory that
contains the configuration file:

**`Terminal`**

```text
ERROR - Config value 'docs_dir': The 'docs_dir' should not be the parent
        directory of the config file. Use a child directory instead so that
        the 'docs_dir' is a sibling of the config file.
```

So the config sits at the repository root with `docs_dir: docs`. That is the
standard MkDocs and GitHub Pages layout.

## Preview the site 👀

**`Terminal`**

```bash
pip install mkdocs
mkdocs serve # http://127.0.0.1:8000
```

Run the commands from the repository root, where `mkdocs.yml` is.

## Build the site 🏗️

**`Terminal`**

```bash
mkdocs build --strict # writes ./site/, fails on a broken link or a warning
```

`site/` is build output. Do not commit it.

## Add a page ➕

1. Write the markdown file in `docs/`.
2. Add it to the `nav:` list in the root `mkdocs.yml`.
3. Run `mkdocs build --strict` to confirm the links and the navigation.

A `nav:` entry that names a file which does not exist fails the strict build.
Remove the entry when you delete the page.

## Publication 🚀

`.github/workflows/docs.yml` builds the site with `mkdocs build --strict` and
publishes it to GitHub Pages on each push to the default branch (`Current`), and
on manual dispatch.

One repository setting is required: **Settings → Pages → Build and deployment →
Source = GitHub Actions**.
