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
scripts/fetch_external_sources.sh
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

**Note, that we also build a preview of the page when you open a PR, so building locally might not be necessary.**

### Generating / building algorithm overview pages

It's not strictly necessary to generate the overview tables of the existing
Gaudi algorithms and Marlin processors, but if you want to have them locally,
you will need to generate them first **inside a Key4hep software environment**.
In order to reproduce the official documentation run before building the
documentation as described above

```bash
scripts/generate_overview.sh \
    scripts/collect_gaudi_alg_info.py \
    docs/algorithm-overview.md \
    --filter-config scripts/filter_gaudi.yaml

scripts/generate_overview.sh \
    scripts/collect_marlin_processor_info.py \
    docs/processor-overview.md \
    --filter-config scripts/filter_marlin.yaml \
    --item-label processor \
    --property-label parameter
```

The `generate_overview.sh` script essentially does the following three things
- Call the collection script that produces an output in JSON (this is the first
  argument to the script)
- Pass that JSON output to `generate_overview_table.py` that generates an `.md`
  file with the necessary inline HTML for nice rendering. This also applies some
  filtering to avoid picking up algorithms from the Gaudi test suite as well as
  removing commonly available properties that are usually not interesting
- It concatenates this generated table to the existing documentation stub (this
  is the second argument to the script)

## Including changes from an external PR

In some cases the changes to the documentation happen in a different repository
(as we include external resources here). It's possible to make the pipeline that
builds the PR previews aware of this by using the phrase `include PR for
preview: <reference to the PR>` in the body of the pull request. **Currently
only one such external PR is supported.** Accepted formats for the PR reference are

- `<github-org>/<repo>#<pr-number>`
- url to the PR, i.e. `https://github.com/<github-org>/<repo>/pull/<pr-number>`

## Deploying to github pages

The deployment to github pages happens via the `gh-pages` branch. On this branch
the documentation goes into the `main` subdirectory, and we have a redirecting
[`index.html`](./index.html).

The branch is automatically populated via github actions. However, its history
is not really interesting (even though the action keeps it intact). In case the
repository gets too large, it is possible to remove the branch entirely and
start from scratch (the next run of the action will populate the branch again).
**Only the `index.html` file has to be put onto the branch first.**

We also make preview pages for PRs on this repository which will be placed onto
the `gh-pages` branch as well, but under a dedicated directory. This means that
they are generally reachable by people, if they know the corresponding full
reference.
