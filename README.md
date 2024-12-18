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
