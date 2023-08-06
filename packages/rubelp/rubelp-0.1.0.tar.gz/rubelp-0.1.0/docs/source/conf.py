# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'rubelp'
copyright = '2023, Jérémy Bourdillat'
author = 'Jérémy Bourdillat'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.viewcode', 'sphinx.ext.autosummary', 
    'sphinx.ext.inheritance_diagram', 'sphinx.ext.graphviz']

templates_path = ['_templates']
exclude_patterns = []

language = 'fr'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

autodoc_default_options = {"members": True, "undoc-members": True, "private-members": True}
autosummary_generate = True

inheritance_graph_attrs = dict(rankdir="TB", size='""')