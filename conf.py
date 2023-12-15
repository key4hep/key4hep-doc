# You should normally never do wildcard imports
# Here it is useful to allow the configuration to be maintained elsewhere
# from starterkit_ci.sphinx_config import *  # NOQA

project = "Key4hep"
copyright = "2020, Key4hep"
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
    "display_github": True,
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

# html_static_path += [
#    f'_static',
# ]

linkcheck_ignore = []

myst_heading_anchors = 3

myst_enable_extensions = ["colon_fence"]
