# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'CartoGIS'
copyright = '2024, Kamyar Hasanzadeh'
author = 'Kamyar Hasanzadeh'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['nbsphinx']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_last_updated_fmt = "%d %B %Y"
html_logo = "static/logo/CartoGIS.png"
html_short_title = "CartoGIS"
html_title = ""

html_theme = "sphinx_book_theme"


html_theme_options = {
    "collapse_navigation": False,
    'search_bar_position': 'none',
    'nosidebar': True,
    "launch_buttons": {
        "binderhub_url": "https://mybinder.org",
        "notebook_interface": "classic"
    },
    "path_to_docs": "docs",
    "repository_branch": "main",
    "repository_url": "https://github.com/Carto-gis/site",
    "use_edit_page_button": True,
    "use_repository_button": True,
    'logo_only': True,
    'display_version': False,


}
html_static_path = ['_static']

nb_execution_mode = "force"
nb_execution_timeout = 120  # needed, e.g., when matplotlib updates its font cache
nb_execution_show_tb = True  # show errors
