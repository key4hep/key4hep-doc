# You should normally never do wildcard imports
# Here it is useful to allow the configuration to be maintained elsewhere
from starterkit_ci.sphinx_config import *  # NOQA

project = 'Key4HEP'
copyright = '2020, Key4HEP'
author = 'Key4HEP'
html_logo = 'starterkit.png'

exclude_patterns += [
    'archive',
    'README.md',
]

html_context = {
    'display_github': True,
    'github_user': 'key4hep',
    'github_repo': 'key4hep-doc',
    'github_version': 'master',
    'conf_py_path': '/',
}

extensions = [
    'sphinx_copybutton',
    'sphinx_markdown_tables',
    'recommonmark',
]

source_suffix = {
    '.md': 'markdown',
}

html_static_path += [
    f'_static',
]

linkcheck_ignore += [
]


