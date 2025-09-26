# Key4hep documentation
[![docs](https://img.shields.io/badge/docs-main-blue.svg)](https://key4hep.github.io/key4hep-doc/)

Key4hep central documentation

## Getting dependencies

Install python dependencies:

```sh
pip install -r requirements.txt
```

## Building locally

First fetch the documentation pages from other key4hep repositories:

```sh
.github/scripts/fetch_external_sources.sh 
```

If the sources already exist but you want to update them, use the `--force` option.

Then build the site locally:

```sh
sphinx-build -M html docs build
```

Check the links validity with:

```
sphinx-build -b linkcheck docs linkcheck
```

## Deploying to github pages

The deployment to github pages happens via the `gh-pages` branch. On this branch
the documentation goes into the `main` subdirectory, and we have a redirecting
[`index.html`](./index.html).

The branch is automatically populated via github actions. However, its history
is not really interesting (even though the action keeps it intact). In case the
repository gets too large, it is possible to remove the branch entirely and
start from scratch (the next run of the action will populate the branch again).
**Only the `index.html` file has to be put onto the branch first.**
