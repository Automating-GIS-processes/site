# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Automating GIS Processes"
copyright = "2015-2022"
author = "Henrikki Tenkanen, Vuokko Heikinheimo, Håvard Wallin Aagesen, Christoph Fink"

version = "2022"
release = "2022"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_nb",
    "sphinx_thebe",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
source_suffix = {
    ".rst": "restructuredtext",
    ".ipynb": "myst-nb",
    ".myst": "myst-nb",
}
myst_enable_extensions = [
    "colon_fence",
    "substitution",
]
myst_substitutions = {
  "year": "2022",  # use {{year}} in markdown files to replace it with the current value
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = "_static/img/AutoGIS-logo.png"
html_short_title = "AutoGIS"
html_title = ""

html_static_path = ["_static"]

html_theme = "sphinx_book_theme"
html_theme_options = {
    "collapse_navigation": False,
    "path_to_docs": "docs",
    "repository_branch": "main",
    "repository_url": "https://github.com/Automating-GIS-processes/site/",
    "use_edit_page_button": True,
    "use_repository_button": True,
}

nb_execution_mode = "force"
