# You should normally never do wildcard imports
# Here it is useful to allow the configuration to be maintained elsewhere
# from starterkit_ci.sphinx_config import *  # NOQA

import os

IN_GITHUB_ACTIONS_CI = os.environ.get("GITHUB_ACTIONS", False)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)

project = "Key4hep"
copyright = "2025, Key4hep"
author = "Key4hep"
html_static_path = ["static"]
html_logo = "static/logo.png"

exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "archive",
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
    linkcheck_ignore.extend(
        [
            r"https://opensource.org",  # cloudflare blocks requests from github actions
        ]
    )

if GITHUB_TOKEN:
    linkcheck_request_headers = {
        "https://github.com": {
            "Authorization": f"token {GITHUB_TOKEN}",
        }
    }

linkcheck_anchors_ignore_for_url = [
    r"https://github\.com/.*?/.*?/blob/[a-z0-9]+/.*\..*"
]

myst_heading_anchors = 4

myst_enable_extensions = ["colon_fence", "html_image"]
