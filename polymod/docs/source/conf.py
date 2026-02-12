import os
import sys
sys.path.insert(0, os.path.abspath('../../build/lib.macosx-12.3-arm64-cpython-313'))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'polymod'
copyright = '2026, Indy Lyness'
author = 'Indy Lyness'
release = '3.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']

# docs/source/conf.py

extensions = [
    'sphinx.ext.autodoc',       # Essential: Reads your docstrings
    'sphinx.ext.napoleon',      # Essential: Parses NumPy style
    'sphinx.ext.viewcode',      # Optional: Links to code
]

# Configure Napoleon to understand your NumPy docstrings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_special_with_doc = True  # Useful if you documented __add__ etc.

# Optional: Change the theme to something nicer
html_theme = 'sphinx_rtd_theme' # (Requires: pip install sphinx_rtd_theme)
