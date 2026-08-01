# docs/ — the STE-Code documentation site

This directory holds the sources of the MkDocs site that GitHub Pages
publishes. It is documentation only: nothing here is read by the pipeline.

## Layout

```text
mkdocs.yml              ← site config (repository ROOT, not this directory)
docs/
├── README.md           This file (excluded from the built site)
├── index.md            Home
├── pipeline.md         Six-stage A→F overview
├── stages/
│   ├── stage-a.md      Extraction
│   ├── stage-b.md      Refinement
│   ├── stage-c.md      Grouping
│   ├── stage-d.md      Adaptation
│   ├── stage-e.md      Extension
│   └── stage-f.md      Artifacts
├── contributing.md     Local pipeline run and contribution rules
└── roadmap/            Roadmap, grounding report, state reconciliation
```

### Why `mkdocs.yml` is in the repository root

MkDocs refuses a configuration file whose `docs_dir` is the directory that
contains the configuration file:

```text
ERROR - Config value 'docs_dir': The 'docs_dir' should not be the parent
        directory of the config file. Use a child directory instead so that
        the 'docs_dir' is a sibling of the config file.
```

So the config sits at the repository root with `docs_dir: docs`, which is the
standard MkDocs and GitHub Pages layout.

## Preview the site

```bash
pip install mkdocs
mkdocs serve            # http://127.0.0.1:8000
```

Run the commands from the repository root, where `mkdocs.yml` is.

## Build the site

```bash
mkdocs build --strict   # writes ./site/, fails on a broken link or a warning
```

`site/` is build output. Do not commit it.

## Publication

`.github/workflows/docs.yml` builds the site with `mkdocs build --strict` and
publishes it to GitHub Pages on each push to the default branch (`Current`),
and on manual dispatch.

One repository setting is required: **Settings → Pages → Build and deployment →
Source = GitHub Actions**.

## Add a page

1. Write the markdown file in `docs/`.
2. Add it to the `nav:` list in the root `mkdocs.yml`.
3. Run `mkdocs build --strict` to confirm the links and the navigation.
