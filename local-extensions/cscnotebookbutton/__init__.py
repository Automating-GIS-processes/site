#!/usr/bin/env python3


"""Add a launch button to start CSC notebooks."""


import pathlib

import sphinx.util.osutil


CSC_NOTEBOOK_ICON_PATH = pathlib.Path("_static/images/csc-notebook-icon_512x512px.svg")
EXTENSION_PATH = pathlib.Path(__file__).absolute().parent


def add_csc_notebook_button(app, pagename, templatename, context, doctree):
    """
    Add a launch button to start CSC notebooks.

    This can be used as a callback to the `sphinx.connect()`
    hook to add an additional item to `context["header_buttons"]`.

    See https://www.sphinx-doc.org/en/master/extdev/
      appapi.html#sphinx.application.Sphinx.connect
    Inspired in parts by https://github.com/executablebooks/
      sphinx-book-theme/blob/master/src/sphinx_book_theme/
      header_buttons/launch.py

    Works with sphinx-book-theme.

    Note: This currently only works if any other launch button is
    configured, e.g., Binder.
    """
    if app.env.metadata[pagename].get("kernelspec"):  # is notebook
        try:
            header_buttons = context["header_buttons"]
        except KeyError:
            return

        for item in header_buttons:
            try:
                if item["label"] == "launch-buttons":
                    launch_buttons = item["buttons"]
                    launch_buttons.append(
                        {
                            "type": "link",
                            "text": "CSC Notebooks",
                            "tooltip": "Open CSC Notebooks",
                            "icon": str(CSC_NOTEBOOK_ICON_PATH),
                            "url": "https://notebooks.csc.fi",
                            "tooltip_placement": "left",
                        }
                    )
                    _copy_icon_to_build_directory(app.builder.outdir)
                    break
            except KeyError:
                continue


def _copy_icon_to_build_directory(build_directory):
    """Copy the CSC Notebooks icon to the build directory."""
    origin = EXTENSION_PATH / CSC_NOTEBOOK_ICON_PATH
    destination = pathlib.Path(build_directory) / CSC_NOTEBOOK_ICON_PATH
    sphinx.util.osutil.ensuredir(destination.parent)
    sphinx.util.osutil.copyfile(origin, destination)


def setup(app):
    """
    Register extension with sphinx.

    This is a callback function called by sphinx when it loads the extension.
    """
    app.connect(
        "html-page-context",
        add_csc_notebook_button,
        priority=502,  # make sure we’re called at the right moment
    )

    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
