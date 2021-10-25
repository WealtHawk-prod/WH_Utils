"""Sphinx configuration."""
from datetime import datetime
import sphinx_rtd_theme

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))


project = "Wh_Utils"
author = "McClain Thiel"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "sphinx_rtd_theme",
]
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
