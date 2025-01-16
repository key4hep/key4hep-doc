# You should normally never do wildcard imports
# Here it is useful to allow the configuration to be maintained elsewhere
# from starterkit_ci.sphinx_config import *  # NOQA

import os

IN_GITHUB_ACTIONS_CI = os.environ.get("GITHUB_ACTIONS", False)


project = "Key4hep"
copyright = "2025, Key4hep"
author = "Key4hep"
# html_logo = "starterkit.png"

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store" "archive",
    "README.md",
]

html_theme = "sphinx_rtd_theme"

html_context = {
    "display_github": False,
    "github_user": "key4hep",
    "github_repo": "key4hep-doc",
    "github_version": "main",
    "conf_py_path": "/",
}

extensions = [
    "sphinx_copybutton",
    "sphinx_markdown_tables",
    "sphinx_design",
    "myst_parser",
]

source_suffix = {
    ".md": "markdown",
}

linkcheck_ignore = [
    r"https://twiki.cern.ch/twiki/bin/view",  # TWikis might need login
]
if IN_GITHUB_ACTIONS_CI:
    linkcheck_ignore.append(
        r"https://opensource.org",  # cloudflare blocks requests from github actions
    )


myst_heading_anchors = 4

myst_enable_extensions = ["colon_fence", "html_image"]
