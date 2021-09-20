#!/usr/bin/env python3
import os
import sys

# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
    "sphinx_thebe",
    'IPython.sphinxext.ipython_console_highlighting',
    'IPython.sphinxext.ipython_directive',
    'myst_nb',
    'jupyter_sphinx',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'AutoGIS'
copyright = '2021, Henrikki Tenkanen, Vuokko Heikinheimo & Håvard Wallin Aagesen, Department of Geosciences and Geography, University of Helsinki'
author = 'Henrikki Tenkanen, Vuokko Heikinheimo & Håvard Wallin Aagesen'

# The short X.Y version.
version = '2021'
# The full version, including alpha/beta/rc tags.
release = 'site'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

html_theme = 'sphinx_book_theme'
html_logo = 'img/AutoGIS-logo.png'
html_title = ""

html_theme_options = {
    #"external_links": [],
    "repository_url": "https://github.com/Automating-GIS-processes/site/",
    "repository_branch": "master",
    "path_to_docs": "source/",
    #"twitter_url": "https://twitter.com/pythongis",
    "google_analytics_id": "UA-88382509-1",
    "use_edit_page_button": True,
    "use_repository_button": True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "thebe": True,
        "notebook_interface": "jupyterlab",
    "collapse_navigation" : False
    },
}

html_context = {
    # Enable the "Edit in GitHub link within the header of each page.
    'display_github': True,
    # Set the following variables to generate the resulting github URL for each page.
    # Format Template: https://{{ github_host|default("github.com") }}/{{ github_user }}/{{ github_repo }}/blob/{{ github_version }}{{ conf_py_path }}{{ pagename }}{{ suffix }}
    'github_user': 'Automating-GIS-processes',
    'github_repo': 'site',
    'github_version': 'master/',
    'conf_py_path': '/source/'
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_last_updated_fmt = ""

# -- Options for LaTeX output ---------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'AutoGIS.tex', 'AutoGIS Documentation',
     'Henrikki Tenkanen', 'manual'),
]

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'autogis', 'AutoGIS Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'AutoGIS', 'AutoGIS Documentation',
     author, 'AutoGIS', 'One line description of project.',
     'Miscellaneous'),
]

# Allow errors
execution_allow_errors = True

# Do not execute cells
jupyter_execute_notebooks = "off"
