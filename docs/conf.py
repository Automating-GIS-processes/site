# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Automating GIS Processes"
copyright = "2016-2022"
author = "Henrikki Tenkanen, Vuokko Heikinheimo, Håvard Wallin Aagesen, Christoph Fink"

version = "2022"
release = "2022"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_nb",
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

# The following are the main things that need to be updated every year
# These variables are replaced throughout the course documents
# (see the comment for the first item for an example)
myst_substitutions = {
    "year": "2022",  # use {{year}} in markdown files to replace it with the current value
    "starting_date": "Tuesday, 1 November 2022",
    "lectures_weekday_time_location": "Tuesday, 15:15-16:45, Exactum C222",
    "work_sessions_weekday_time_location": "Friday, 12:15-16:00, Physicum A113+A114 (GIS lab)",
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_logo = "_static/img/autogis-logo_300x210px.svg"
html_short_title = "AutoGIS"
html_title = ""

html_static_path = ["_static"]

html_theme = "sphinx_book_theme"
html_theme_options = {
    "collapse_navigation": False,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "notebook_interface": "jupyterlab",
    },
    "path_to_docs": "docs",
    "repository_branch": "main",
    "repository_url": "https://github.com/Automating-GIS-processes/site/",
    "use_edit_page_button": True,
    "use_repository_button": True,
}

nb_execution_mode = "force"
