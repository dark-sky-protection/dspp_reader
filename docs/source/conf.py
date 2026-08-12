# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
from importlib.metadata import version, PackageNotFoundError

sys.path.insert(0, os.path.abspath('../..'))

try:
    __version__ = version('dspp_reader')
except PackageNotFoundError:
    __version__ = '0.0.0'

version = '.'.join(__version__.split('.')[:2])
release = __version__
project = 'DSPP Reader'
copyright = '2025, NOIRLab'
author = 'Simón Torres, Guillermo Damke'
license = 'bsd3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.apidoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon'
]

apidoc_modules = [
    {
        'path': '../../dspp_reader',
        'destination': 'api',
        'exclude_patterns': ['_build', '**/test_*.py', '**/tests/*'],
        'separate_modules': True,
        'private': True,
    }
]

html_theme_options = {
    "navbar_start": [
        "navbar-logo",
        "version",
    ],
}
html_logo = '_static/img/logo_noirlab.png'


templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_static_path = ['_static']
